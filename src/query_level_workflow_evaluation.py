"""Primary benchmark: decompose human workflows into query-level search tests.

The 100 workflow tool lists are candidate pools, not expected output from one
search request. Ground truth is built in two DELIBERATELY SEPARATE stages so
neither leaks into the other:

  Stage A (blind decomposition): Gemini sees ONLY the task text and breaks it
  into realistic search queries -- exactly like a real agent, which has no
  visibility into what tools exist before it searches. It never sees the
  candidate pool here.

  Stage B (grounded labeling): a second, independent Gemini call sees the
  queries from stage A plus the candidate pool's FULL tool descriptions (not
  just slugs -- see below) and assigns per-query ground truth. A query may
  end up with no matching tool at all; that's recorded, not forced.

This split exists because giving the pool to the same call that writes the
queries lets tool-name vocabulary leak into query phrasing (observed: a query
asking to "query ledger entities" when the pool contained
QUICKBOOKS_QUERY_ENTITIES -- "entities" is API jargon, not how a person
phrases a task). That inflates retrieval scores relative to a genuinely blind
search.

Labeling is also grounded in real tool DESCRIPTIONS fetched live from
Composio (composio.tools.get(user_id=..., tools=[...])), not bare slugs.
Asking an LLM to infer semantics from an opaque name like
GOOGLESUPER_FETCH_EMAILS is unnecessary noise in the ground truth.

Two further corrections carried over from the previous version:

1. Query count scales with candidate-pool size instead of a fixed 2-4 cap
   (query_count_range()) -- a fixed cap silently dropped genuine sub-intents
   for complex workflows (measured: 51% of a workflow's candidate tools, on
   average, were never assigned to any query under the old cap).

2. Ground truth per query is a list of requirement GROUPS, not one flat
   required-tool list. Within a group, ANY ONE tool satisfies it (true
   alternatives, e.g. GMAIL_SEARCH_EMAILS vs GMAIL_FETCH_EMAILS); across
   groups, ALL are required (genuinely compositional intents). A flat list
   cannot express "either tool is fine" and was silently scoring correct
   alternative-tool hits as partial misses.

Because ground truth is still an LLM's opinion, queries that miss a
requirement group after search also get a cheap secondary "judged recall"
pass: an independent, vendor-scoped Gemini call checks whether any tool
search ACTUALLY returned -- even one never pre-labeled -- plausibly satisfies
that requirement. Reported alongside strict recall, never in place of it.
"""
from __future__ import annotations

import csv, json, math, os, random, re, statistics, time, traceback
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai

load_dotenv()
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash-lite"
USER_ID = "query-level-workflow-eval-user"
USE_CASES_FILE = Path(__file__).resolve().parent / "top-100-eval-use-cases.md"
OUTPUT_DIR = Path(__file__).resolve().parent / "query_level_workflow_evaluation"
GROUND_TRUTH_PATH = OUTPUT_DIR / "query_ground_truth.json"
AUDIT_PATH = OUTPUT_DIR / "generation_audit.json"
RESULTS_PATH = OUTPUT_DIR / "search_results.csv"
REPORT_PATH = OUTPUT_DIR / "summary_report.md"
RAW_DIR = OUTPUT_DIR / "raw_search_results"
CACHE_PATH = OUTPUT_DIR / "generation_cache.json"
TOOL_CATALOG_CACHE_PATH = OUTPUT_DIR / "tool_catalog_cache.json"

MAX_USE_CASES = 100          # lower for an inexpensive smoke test
MIN_QUERIES_FLOOR = 2       # every workflow gets at least this many queries
MAX_QUERIES_CEILING = 10    # hard cap regardless of pool size, to bound cost
TOOLS_PER_QUERY_TARGET = 2.5  # ~1 query per this many candidate tools
DESCRIPTION_CHAR_LIMIT = 400  # truncate long tool descriptions to bound prompt size
TOOL_FETCH_CHUNK = 40        # composio.tools.get(tools=[...]) batch size
GEMINI_RPM = 15
SEARCH_DELAY_SEC = 0.5
RANDOM_SEED = 42


def query_count_range(pool_size: int) -> tuple[int, int]:
    """Scale the query-count range to the candidate pool instead of a fixed cap.

    Pools of 1-2 tools get min_q=1 so a single genuine query isn't padded with
    a forced, near-duplicate second one just to hit a floor. Pool size is
    only ever used to set this bound -- it is never shown to the model during
    decomposition (see module docstring).
    """
    max_q = min(MAX_QUERIES_CEILING, max(MIN_QUERIES_FLOOR, math.ceil(pool_size / TOOLS_PER_QUERY_TARGET)))
    min_q = 1 if pool_size <= 2 else min(MIN_QUERIES_FLOOR, max_q)
    return min_q, max_q


@dataclass
class UseCase:
    id: int
    task: str
    candidate_tools: list[str]
    description: str


class RateLimiter:
    def __init__(self, rpm: float): self.interval, self.last = 60 / rpm, 0.0
    def wait(self):
        remaining = self.interval - (time.monotonic() - self.last)
        if remaining > 0: time.sleep(remaining)
        self.last = time.monotonic()


def to_plain(value: Any) -> Any:
    if hasattr(value, "model_dump"): return value.model_dump()
    if isinstance(value, dict): return value
    return vars(value) if hasattr(value, "__dict__") else value


class QuotaExhaustedError(RuntimeError):
    """Raised instead of retrying when an error looks like an exhausted API
    quota or rate limit -- retrying that with backoff just wastes wall-clock
    time against a dead quota for every remaining call in the run."""


QUOTA_ERROR_MARKERS = ("resource_exhausted", "quota", "429", "rate limit")


def is_quota_error(error: BaseException) -> bool:
    text = str(error).lower()
    return any(marker in text for marker in QUOTA_ERROR_MARKERS)


def retry(call, *args, timed=False, max_retries=4, base_delay=2.0, **kwargs):
    last_error = None
    for attempt in range(max_retries):
        try:
            started = time.monotonic(); value = call(*args, **kwargs)
            return (value, time.monotonic() - started) if timed else value
        except Exception as error:
            if is_quota_error(error):
                raise QuotaExhaustedError(f"looks like an exhausted quota/rate limit, aborting retries: {error!r}") from error
            last_error = error
            if attempt < max_retries - 1:
                delay = base_delay * 2 ** attempt + random.random()
                print(f"  [retry] {attempt + 1}/{max_retries}: {error!r}; sleeping {delay:.1f}s")
                time.sleep(delay)
    raise last_error


def parse_use_cases(path: Path) -> list[UseCase]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"(\d+)\.\s+\*\*(.*?)\*\*\s*\n\s*-\s*Tools:\s*(.*?)\s*\n\s*-\s*Description:\s*(.*?)(?=\n\d+\.\s+\*\*|\Z)", re.DOTALL)
    cases = []
    for ident, task, raw_tools, description in pattern.findall(text):
        tools = [item.strip() for item in raw_tools.replace("`", "").split(",") if item.strip()]
        cases.append(UseCase(int(ident), task.strip(), tools, description.strip()))
    if not cases: raise ValueError("No use cases parsed; inspect the Markdown format.")
    return cases


def load_json(path: Path, fallback): return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback
def save_json(path: Path, value): path.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")
def strip_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"): text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text.strip()


def fetch_tool_catalog(composio: Composio, slugs: list[str]) -> dict[str, str]:
    """Fetch real descriptions for every candidate slug across all use cases,
    in batches, cached to disk keyed by slug (descriptions are stable)."""
    cache = load_json(TOOL_CATALOG_CACHE_PATH, {})
    missing = [slug for slug in slugs if slug not in cache]
    for start in range(0, len(missing), TOOL_FETCH_CHUNK):
        chunk = missing[start:start + TOOL_FETCH_CHUNK]
        print(f"[catalog] fetching descriptions for {len(chunk)} tools ({start + len(chunk)}/{len(missing)} new)")
        try:
            tools = retry(lambda: composio.tools.get(user_id=USER_ID, tools=chunk), max_retries=3, base_delay=2.0)
            found = set()
            for tool in tools:
                function = tool["function"] if isinstance(tool, dict) else tool.function
                function = function if isinstance(function, dict) else function.model_dump()
                name, description = function.get("name"), (function.get("description") or "").strip()
                if name:
                    cache[name] = description[:DESCRIPTION_CHAR_LIMIT]
                    found.add(name)
            for slug in chunk:
                if slug not in found: cache[slug] = ""  # not resolvable; labeler treats as unknown
        except QuotaExhaustedError:
            save_json(TOOL_CATALOG_CACHE_PATH, cache); raise
        except Exception as error:
            print(f"  [catalog] fetch failed for this chunk: {error!r}")
            for slug in chunk: cache.setdefault(slug, "")
        save_json(TOOL_CATALOG_CACHE_PATH, cache)
    return cache


DECOMPOSE_PROMPT = '''You are an agent that has just been given a high-level task. You do NOT know what
tools or APIs exist -- your only option is to call a tool-search function once you know what to search for.

Task:
{task}

Break this task down into {minimum}-{maximum} concrete, realistic search queries you would issue to a
tool-search engine while working through it, in the order you would naturally need them. Each query should
target ONE genuine, distinct sub-intent -- a specific action or lookup this task requires.

Return exactly JSON:
{{"queries":[{{"query":"short natural search query, no internal tool/API names","intent":"one precise sentence describing exactly what capability this query needs"}}]}}

Rules:
- Never send the whole task as one query.
- Do not pad with filler queries just to reach the maximum, and do not skip a clearly distinct sub-intent
  just to stay under it -- let the task's real complexity decide the count within the given range.
- Write purely from the task text above; you have no knowledge of what tools exist.
'''

LABEL_PROMPT = '''A workflow was decomposed into the search queries below by an agent that could not see any
tool catalog. Now assign ground truth: for each query, decide which of the AVAILABLE TOOLS below (if any)
would genuinely satisfy it. Base this on each tool's DESCRIPTION, not its name -- names can be misleading.

Workflow:
{task}

Queries (in order):
{queries}

Available tools (the ONLY tools you may reference):
{catalog}

For each query, return zero or more REQUIREMENT GROUPS:
- If two or more tools could each, independently, fully satisfy the query (true alternatives), put them in
  the SAME group.
- If the query genuinely needs multiple different operations performed together (compositional), use
  SEPARATE groups, one per operation.
- If NONE of the available tools would genuinely satisfy this query, return an empty list for it. Do not
  force a poor match just to fill it in -- an honest "no match" is a valid and useful outcome.
- Most queries need exactly one group with one tool.

Return exactly JSON:
{{"query_labels":[{{"query_index":1,"requirement_groups":[{{"acceptable_tool_slugs":["slug(s) that alone satisfy this one need"],"purpose":"short phrase for what this group accomplishes"}}]}}]}}

Rules:
- query_labels must have exactly one entry per query above, in order, with matching query_index (1-based).
- Every requirement group needs 1-4 acceptable tool slugs, all from the available tools. Do not invent slugs.
- Every query needs 0-3 requirement groups.
'''


def generate_decomposition(client, limiter, case: UseCase, min_q: int, max_q: int) -> tuple[dict[str, Any] | None, str]:
    prompt = DECOMPOSE_PROMPT.format(task=case.task, minimum=min_q, maximum=max_q)
    def call():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        raw = retry(call, max_retries=5, base_delay=3.0)
        return json.loads(strip_json(raw)), raw
    except QuotaExhaustedError:
        raise
    except Exception as error:
        return None, repr(error)


def validate_decomposition(payload: Any, min_q: int, max_q: int) -> str | None:
    if not isinstance(payload, dict) or not isinstance(payload.get("queries"), list): return "missing queries list"
    queries = payload["queries"]
    if not min_q <= len(queries) <= max_q: return "query count outside configured range"
    seen = set()
    for item in queries:
        query, intent = item.get("query"), item.get("intent")
        if not isinstance(query, str) or len(query.split()) < 3: return "empty or implausibly short query"
        if not isinstance(intent, str) or not intent.strip(): return "missing intent"
        if query.lower() in seen: return "duplicate query"
        seen.add(query.lower())
    return None


def generate_labels(client, limiter, case: UseCase, queries: list[dict[str, Any]], catalog: dict[str, str]) -> tuple[dict[str, Any] | None, str]:
    queries_text = "\n".join(f"{i}. {item['query']}  (intent: {item['intent']})" for i, item in enumerate(queries, start=1))
    catalog_text = "\n\n".join(f"Tool: {slug}\nDescription: {catalog.get(slug) or '(no description available)'}" for slug in case.candidate_tools)
    prompt = LABEL_PROMPT.format(task=case.task, queries=queries_text, catalog=catalog_text)
    def call():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        raw = retry(call, max_retries=5, base_delay=3.0)
        return json.loads(strip_json(raw)), raw
    except QuotaExhaustedError:
        raise
    except Exception as error:
        return None, repr(error)


def validate_labels(payload: Any, queries: list[dict[str, Any]], allowed: set[str]) -> str | None:
    if not isinstance(payload, dict) or not isinstance(payload.get("query_labels"), list): return "missing query_labels list"
    labels = payload["query_labels"]
    if len(labels) != len(queries): return "query_labels count mismatch"
    indices = {item.get("query_index") for item in labels}
    if indices != set(range(1, len(queries) + 1)): return "query_labels indices incomplete or invalid"
    for item in labels:
        groups = item.get("requirement_groups")
        if not isinstance(groups, list) or len(groups) > 3: return "invalid requirement group count"
        for group in groups:
            slugs = group.get("acceptable_tool_slugs") if isinstance(group, dict) else None
            if not slugs or not 1 <= len(slugs) <= 4 or not set(slugs) <= allowed: return "invalid or invented required tool"
            if not isinstance(group.get("purpose"), str) or not group["purpose"].strip(): return "requirement group missing purpose"
    return None


def build_ground_truth(cases: list[UseCase], client, catalog: dict[str, str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Two-stage, cached per workflow. Returns (accepted rows, unlabelable
    queries -- valid decomposition but no candidate tool fit, kept for
    audit/reporting but never scored, audit log)."""
    cache, limiter, accepted, unlabelable, audit = load_json(CACHE_PATH, {}), RateLimiter(GEMINI_RPM), [], [], []
    for case in cases[:MAX_USE_CASES]:
        min_q, max_q = query_count_range(len(case.candidate_tools))
        cache_key = str(case.id)
        entry = cache.get(cache_key, {})
        try:
            if "decompose" in entry:
                decompose_payload, decompose_raw = entry["decompose"]["payload"], entry["decompose"]["raw"]
            else:
                print(f"[decompose] workflow {case.id} (pool={len(case.candidate_tools)}, target {min_q}-{max_q} queries, blind)")
                decompose_payload, decompose_raw = generate_decomposition(client, limiter, case, min_q, max_q)
                entry["decompose"] = {"payload": decompose_payload, "raw": decompose_raw}
                cache[cache_key] = entry; save_json(CACHE_PATH, cache)

            decompose_rejection = "generation error" if decompose_payload is None else validate_decomposition(decompose_payload, min_q, max_q)
            if decompose_rejection:
                audit.append({"use_case": asdict(case), "stage": "decompose", "query_range": [min_q, max_q], "gemini_raw_response": decompose_raw, "generated": decompose_payload, "rejection_reason": decompose_rejection})
                print(f"  rejected at decompose: {decompose_rejection}"); continue

            queries = decompose_payload["queries"]
            allowed = set(case.candidate_tools)
            if "label" in entry:
                label_payload, label_raw = entry["label"]["payload"], entry["label"]["raw"]
            else:
                print(f"[label] workflow {case.id} ({len(queries)} queries, grounded in {len(allowed)} tool descriptions)")
                label_payload, label_raw = generate_labels(client, limiter, case, queries, catalog)
                entry["label"] = {"payload": label_payload, "raw": label_raw}
                cache[cache_key] = entry; save_json(CACHE_PATH, cache)
        except QuotaExhaustedError as error:
            print(f"\n[ABORTED at workflow {case.id}] {error}\n"
                  f"Stopping generation early -- {len({row['workflow_id'] for row in accepted})} workflows / "
                  f"{len(accepted)} queries already accepted are kept and will still be searched+scored below. "
                  f"Already-generated workflows are cached in {CACHE_PATH.name}; re-run this script later "
                  f"(after the quota resets) to continue from workflow {case.id} onward.\n")
            break

        label_rejection = "generation error" if label_payload is None else validate_labels(label_payload, queries, allowed)
        audit.append({"use_case": asdict(case), "stage": "label", "query_range": [min_q, max_q], "decompose_generated": decompose_payload, "gemini_raw_response": label_raw, "generated": label_payload, "rejection_reason": label_rejection})
        if label_rejection:
            print(f"  rejected at label: {label_rejection}"); continue

        for label_item in label_payload["query_labels"]:
            query_item = queries[label_item["query_index"] - 1]
            query_id = f"workflow-{case.id:03d}-q{label_item['query_index']}"
            groups = label_item["requirement_groups"]
            if not groups:
                unlabelable.append({"query_id": query_id, "workflow_id": case.id, "workflow_task": case.task, "query": query_item["query"], "intent": query_item["intent"], "candidate_tools": case.candidate_tools})
                continue
            accepted.append({"query_id": query_id, "workflow_id": case.id, "workflow_task": case.task, "query": query_item["query"].strip(), "intent": query_item["intent"], "requirement_groups": groups, "candidate_tools": case.candidate_tools})
    return accepted, unlabelable, audit


def extract_results(response: Any) -> dict[str, Any]:
    top = to_plain(response); data = top.get("data", top) or {}; data = data if hasattr(data, "get") else {}
    primaries, related, toolkits = [], [], []
    entries = data.get("results") or []
    for entry in entries:
        entry = to_plain(entry)
        primaries.extend(entry.get("primary_tool_slugs") or [])
        related.extend(entry.get("related_tool_slugs") or [])
        toolkits.extend(entry.get("toolkits") or [])
    primary = list(dict.fromkeys(primaries)); related = [slug for slug in dict.fromkeys(related) if slug not in primary]
    return {"primary": primary, "related": related, "toolkits": list(dict.fromkeys(toolkits)), "raw": top, "no_results": not entries, "error": data.get("error") or top.get("error")}


def score_query(session, row: dict[str, Any], raw_dir: Path) -> dict[str, Any]:
    started, error, api_latency = time.monotonic(), None, None
    plan = {"primary": [], "related": [], "toolkits": [], "raw": {}, "no_results": True, "error": None}
    try:
        response, api_latency = retry(session.execute, "COMPOSIO_SEARCH_TOOLS", arguments={"query": row["query"]}, timed=True)
        end_to_end = time.monotonic() - started; plan = extract_results(response)
    except QuotaExhaustedError:
        raise
    except Exception as exc:
        end_to_end = time.monotonic() - started; error = repr(exc); traceback.print_exc()
    groups = row["requirement_groups"]
    primary, related = set(plan["primary"]), set(plan["related"])
    found = primary | related
    satisfied_any = [bool(set(g["acceptable_tool_slugs"]) & found) for g in groups]
    satisfied_primary = [bool(set(g["acceptable_tool_slugs"]) & primary) for g in groups]
    total = len(groups)
    missed_groups = [g for g, hit in zip(groups, satisfied_any) if not hit]
    all_group_slugs = {slug for g in groups for slug in g["acceptable_tool_slugs"]}
    raw_path = raw_dir / f"{row['query_id']}.json"
    save_json(raw_path, {"query_ground_truth": row, "request": {"query": row["query"]}, "response": plan["raw"]})
    return {**row, "expected_groups": total, "primary_hit": any(satisfied_primary), "any_hit": any(satisfied_any),
            "primary_recall": round(sum(satisfied_primary) / total, 4) if total else 0.0,
            "recall": round(sum(satisfied_any) / total, 4) if total else 0.0,
            "missed_groups": "; ".join(" | ".join(g["acceptable_tool_slugs"]) for g in missed_groups),
            "missed_purposes": "; ".join(g["purpose"] for g in missed_groups),
            "extra_tools": "; ".join(sorted(found - all_group_slugs)),
            "primary_tools": "; ".join(plan["primary"]), "related_tools": "; ".join(plan["related"]),
            "returned_toolkits": "; ".join(plan["toolkits"]),
            "api_search_latency_sec": round(api_latency, 2) if api_latency is not None else None,
            "end_to_end_latency_sec": round(end_to_end, 2), "error": error or plan["error"],
            "no_results_returned": plan["no_results"], "raw_result_path": str(raw_path),
            # Defaults to strict recall (already 1.0 groups satisfied -> nothing to judge).
            # Only rows with recall < 1 go through judge_unmet_groups, which overwrites this.
            "judged_recall": round(sum(satisfied_any) / total, 4) if total else 0.0, "judged_notes": "", "was_judged": False}


JUDGE_PROMPT = '''A tool-search system was asked this query (part of the larger workflow below) and returned
some tools. For each requirement below that its PRE-LABELED acceptable tools did NOT satisfy, decide whether
any of the tools it ACTUALLY RETURNED would still plausibly satisfy it.

Workflow this query is part of (for vendor/system context only):
{workflow_task}

Query: {query}

Unmet requirements (numbered; each needs ANY ONE tool that performs this purpose):
{unmet_groups}

Tools actually returned by search:
{returned_tools}

Be conservative, and apply this vendor rule strictly:
- If the pre-labeled acceptable tools for a requirement all belong to one specific product/vendor that the
  workflow explicitly names for this data or action (e.g. "in Salesforce", "in HubSpot", "our QuickBooks
  ledger"), only credit a returned tool that belongs to that SAME vendor. A different vendor's
  similar-sounding tool must NOT be credited even if it performs an equivalent operation -- it would not
  actually reach the data the task needs.
- If the workflow does not name a specific vendor for this particular action, a different but operationally
  equivalent tool MAY be credited.
- Otherwise, only mark a group satisfied if a returned tool clearly performs that exact operation.

Return exactly JSON:
{{"judgments": [{{"group_index": 1, "satisfied_by": "RETURNED_TOOL_SLUG or null", "confidence": "high|medium|low"}}]}}
Default to null when unsure.
'''


def judge_unmet_groups(client, limiter, row: dict[str, Any]) -> dict[str, Any]:
    """Cheap secondary check: would an actually-returned (but unlabeled) tool
    plausibly satisfy a missed requirement group? Reported as judged_recall
    alongside strict recall -- never used to overwrite it. Vendor-scoped: a
    functionally similar tool from a different named vendor is not credited."""
    groups = row["requirement_groups"]
    satisfied_any = [bool(set(g["acceptable_tool_slugs"]) & set((row["primary_tools"] + "; " + row["related_tools"]).split("; "))) for g in groups]
    unmet = [(i, g) for i, (g, hit) in enumerate(zip(groups, satisfied_any), start=1) if not hit]
    returned = sorted({t for t in (row["primary_tools"] + "; " + row["related_tools"]).split("; ") if t})
    if not unmet or not returned:
        return {"judged_recall": row["recall"], "judged_notes": "", "was_judged": True}
    unmet_text = "\n".join(f"{i}. {g['purpose']} (pre-labeled options were: {', '.join(g['acceptable_tool_slugs'])})" for i, g in unmet)
    prompt = JUDGE_PROMPT.format(workflow_task=row["workflow_task"], query=row["query"], unmet_groups=unmet_text, returned_tools="\n".join(f"- {t}" for t in returned))
    def call():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        raw = retry(call, max_retries=3, base_delay=2.0)
        payload = json.loads(strip_json(raw))
        judged_satisfied = set()
        notes = []
        for item in payload.get("judgments") or []:
            idx, tool, confidence = item.get("group_index"), item.get("satisfied_by"), item.get("confidence")
            if tool and tool in returned and confidence in ("high", "medium"):
                judged_satisfied.add(idx)
                notes.append(f"group {idx} <- {tool} ({confidence})")
        newly_satisfied = sum(1 for i, _ in unmet if i in judged_satisfied)
        total = len(groups)
        judged_recall = round((sum(satisfied_any) + newly_satisfied) / total, 4) if total else 0.0
        return {"judged_recall": judged_recall, "judged_notes": "; ".join(notes), "was_judged": True}
    except QuotaExhaustedError:
        raise
    except Exception as error:
        return {"judged_recall": row["recall"], "judged_notes": f"judge error: {error!r}", "was_judged": True}


def write_csv(rows, path: Path):
    if rows:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def write_report(rows, accepted, unlabelable, audit):
    valid = [row for row in rows if not row["error"]]; rejected = [row for row in audit if row["rejection_reason"]]
    mean = lambda field: sum(row[field] for row in valid)/len(valid) if valid else 0
    actually_judged = [row for row in valid if row.get("was_judged")]
    api, e2e = sorted(row["api_search_latency_sec"] for row in valid if row["api_search_latency_sec"] is not None), sorted(row["end_to_end_latency_sec"] for row in valid)
    md = ["# Query-Level Workflow Benchmark\n", "## Method",
          "Ground truth is built in two separate passes so neither leaks into the other: stage A blindly "
          "decomposes each task into search queries (no tool pool visible); stage B labels each query against "
          "the candidate pool's real tool descriptions (not just slugs). Ground truth per query is one or more "
          "requirement groups (any one tool within a group satisfies it; all groups are required); a query can "
          "also come back with no matching candidate tool at all, which is recorded rather than forced. Query "
          "count scales with the candidate-pool size instead of a fixed cap. Queries that miss a group get a "
          "secondary judged-recall pass checking whether an actually-returned, unlabeled tool would still "
          "plausibly satisfy it.\n",
          "## Summary",
          f"- **Workflows accepted:** {len({row['workflow_id'] for row in accepted})}",
          f"- **Query-level test cases (scored):** {len(rows)}",
          f"- **Unlabelable queries (valid decomposition, no candidate tool fit -- not scored):** {len(unlabelable)}",
          f"- **Rejected workflow decompositions/labelings:** {len(rejected)}",
          f"- **Average primary recall (strict):** {mean('primary_recall'):.1%}",
          f"- **Average retrieval recall (strict):** {mean('recall'):.1%}",
          f"- **Any-required-group hit rate:** {mean('any_hit'):.1%}",
          f"- **Average judged recall (strict + plausible unlabeled hits, same denominator as strict recall):** {mean('judged_recall'):.1%}",
          f"- **Queries sent through the judge pass (recall < 1):** {len(actually_judged)}/{len(valid)}"]
    if api: md.extend(["\n## Latency", "API/Search latency is the successful call only; end-to-end includes failed attempts and retry backoff.\n", "| Metric | API/Search (s) | End-to-end (s) |", "|---|---:|---:|", f"| Average | {statistics.mean(api):.2f} | {statistics.mean(e2e):.2f} |", f"| Median (P50) | {statistics.median(api):.2f} | {statistics.median(e2e):.2f} |", f"| P95 | {api[int(len(api)*.95)]:.2f} | {e2e[int(len(e2e)*.95)]:.2f} |", f"| Maximum | {api[-1]:.2f} | {e2e[-1]:.2f} |"])
    md.extend(["\n## Failure Examples", "These are query-level candidates for manual review, not automatic product-bug conclusions. `judged_recall` is a plausibility check, not a second ground truth."])
    for row in sorted([row for row in valid if row["recall"] < 1], key=lambda x: (x["recall"], -x["expected_groups"]))[:20]:
        judged_line = f"- **Judged recall:** {row['judged_recall']:.1%}" + (f" ({row['judged_notes']})" if row["judged_notes"] else "") if row.get("was_judged") else ""
        md.extend([f"\n### {row['query_id']} — recall {row['recall']:.1%}", f"- **Query:** {row['query']}", f"- **Missed purposes:** `{row['missed_purposes'] or '(none)'}`", f"- **Missed (any-of groups):** `{row['missed_groups'] or '(none)'}`", judged_line, f"- **Primary returned:** `{row['primary_tools'] or '(none)'}`"])
    if unlabelable:
        md.extend(["\n## Unlabelable Queries", "Stage A produced a genuine sub-intent that stage B found no candidate tool for. Not scored -- reviewed here instead of silently dropped."])
        for row in unlabelable[:15]: md.extend([f"\n### {row['query_id']}", f"- **Query:** {row['query']}", f"- **Intent:** {row['intent']}"])
    REPORT_PATH.write_text("\n".join(md)+"\n", encoding="utf-8")


def main():
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY: raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True); RAW_DIR.mkdir(exist_ok=True); random.seed(RANDOM_SEED)
    cases = parse_use_cases(USE_CASES_FILE); composio, client = Composio(api_key=COMPOSIO_API_KEY), genai.Client(api_key=GEMINI_API_KEY)
    all_slugs = sorted({slug for case in cases[:MAX_USE_CASES] for slug in case.candidate_tools})
    try:
        catalog = fetch_tool_catalog(composio, all_slugs)
    except QuotaExhaustedError as error:
        print(f"\n[ABORTED before generation started] {error}\nNothing to save yet -- re-run once the quota resets.")
        return

    # build_ground_truth already catches QuotaExhaustedError internally and returns whatever it accumulated,
    # so no try/except needed here -- proceeding to search with a partial ground truth is fine and expected.
    ground_truth, unlabelable, audit = build_ground_truth(cases, client, catalog)
    save_json(GROUND_TRUTH_PATH, {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "queries": ground_truth, "unlabelable": unlabelable})
    save_json(AUDIT_PATH, {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "attempts": audit})
    if not ground_truth:
        print("No ground truth accepted; nothing to search."); return

    session = composio.create(user_id=USER_ID); rows = []
    try:
        for index, row in enumerate(ground_truth, 1):
            print(f"[search] {index}/{len(ground_truth)} {row['query_id']}"); rows.append(score_query(session, row, RAW_DIR)); time.sleep(SEARCH_DELAY_SEC)
    except QuotaExhaustedError as error:
        print(f"\n[ABORTED during search, {len(rows)}/{len(ground_truth)} queries done] {error}\n"
              f"Saving completed results now; re-run later to search the rest (ground truth is already saved, "
              f"so nothing generated is lost).\n")
        write_csv(rows, RESULTS_PATH); write_report(rows, ground_truth, unlabelable, audit)
        return

    judge_limiter = RateLimiter(GEMINI_RPM)
    to_judge = [row for row in rows if not row["error"] and row["recall"] < 1]
    try:
        for index, row in enumerate(to_judge, 1):
            print(f"[judge] {index}/{len(to_judge)} {row['query_id']}")
            row.update(judge_unmet_groups(client, judge_limiter, row))
    except QuotaExhaustedError as error:
        print(f"\n[ABORTED during judging] {error}\nStrict-recall results are complete and saved; remaining "
              f"queries keep judged_recall == strict recall as a conservative fallback rather than a real judgment.\n")
    write_csv(rows, RESULTS_PATH); write_report(rows, ground_truth, unlabelable, audit)


if __name__ == "__main__": main()
