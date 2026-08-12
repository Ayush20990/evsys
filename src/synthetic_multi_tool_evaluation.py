"""Synthetic, coherent multi-tool evaluation for COMPOSIO_SEARCH_TOOLS.

This complements the manager-provided ground-truth benchmark.  It samples
only from curated, realistic toolkit families, asks Gemini to retain the
subset of candidate tools genuinely needed by one workflow, and then scores
search across *all* planner result entries.

Artifacts are written to synthetic_multi_tool_evaluation/:
  - generation_audit.json: candidates, Gemini responses, accepted/rejected cases
  - search_results.csv: per accepted workflow metrics and latency
  - raw_search_results/*.json: full request/response per evaluated workflow
  - summary_report.md: aggregate results and concrete failure examples
"""
from __future__ import annotations

import csv
import json
import os
import random
import statistics
import time
import traceback
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai

load_dotenv()
COMPOSIO_API_KEY = os.environ.get("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash-lite"

# Increase only after inspecting a small generated sample manually.
NUM_WORKFLOWS = 20
MIN_REQUIRED_TOOLS, MAX_CANDIDATE_TOOLS = 2, 8
MIN_PLAUSIBILITY = 4
RANDOM_SEED = 42
GEMINI_RPM, COMPOSIO_CALL_DELAY_SEC = 15, 0.5
USER_ID = "synthetic-multi-tool-eval-user"

OUTPUT_DIR = Path("synthetic_multi_tool_evaluation")
RAW_RESULTS_DIR = OUTPUT_DIR / "raw_search_results"
CACHE_PATH = OUTPUT_DIR / "generation_cache.json"
AUDIT_PATH = OUTPUT_DIR / "generation_audit.json"
RESULTS_CSV_PATH = OUTPUT_DIR / "search_results.csv"
REPORT_MD_PATH = OUTPUT_DIR / "summary_report.md"

# These families intentionally favour workflows like the manager examples,
# rather than arbitrary combinations such as GitHub + Spotify + accounting.
TOOLKIT_FAMILIES = [
    ["gmail", "googlecalendar", "slack"],
    ["gmail", "hubspot", "salesforce"],
    ["github", "slack", "linear", "jira"],
    ["trello", "clickup", "notion", "slack"],
    ["hubspot", "linkedin", "gmail"],
    ["googledrive", "googledocs", "googlesheets", "slack"],
]


@dataclass
class ToolInfo:
    slug: str
    toolkit: str
    description: str


class RateLimiter:
    def __init__(self, calls_per_minute: float):
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0.0

    def wait(self) -> None:
        remaining = self.min_interval - (time.monotonic() - self.last_call)
        if remaining > 0:
            time.sleep(remaining)
        self.last_call = time.monotonic()


def with_retry(fn, *args, max_retries=4, base_delay=2.0, timed=False, **kwargs):
    """Retry a call; timed=True returns successful-call latency only.

    The overall duration is measured by the caller, so it includes all failed
    attempts and backoff; the returned API latency excludes both.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            started = time.monotonic()
            result = fn(*args, **kwargs)
            return (result, time.monotonic() - started) if timed else result
        except Exception as error:
            last_error = error
            if attempt == max_retries - 1:
                break
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"  [retry] {attempt + 1}/{max_retries}: {error!r}; sleeping {delay:.1f}s")
            time.sleep(delay)
    raise last_error


def to_plain(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return obj
    return vars(obj) if hasattr(obj, "__dict__") else obj


def fetch_tools(composio: Composio) -> dict[str, list[ToolInfo]]:
    pool: dict[str, list[ToolInfo]] = {}
    requested = sorted({toolkit for family in TOOLKIT_FAMILIES for toolkit in family})
    for toolkit in requested:
        try:
            tools = []
            for tool in composio.tools.get(user_id=USER_ID, toolkits=[toolkit]):
                function = tool["function"] if isinstance(tool, dict) else tool.function
                slug = function["name"] if isinstance(function, dict) else function.name
                description = (function.get("description", "") if isinstance(function, dict) else getattr(function, "description", "")) or ""
                tools.append(ToolInfo(slug, toolkit, description))
            if tools:
                pool[toolkit] = tools
            print(f"[fetch] {toolkit}: {len(tools)} tools")
        except Exception as error:
            print(f"[fetch] skipping {toolkit}: {error!r}")
    return pool


def select_candidates(pool: dict[str, list[ToolInfo]]) -> list[ToolInfo] | None:
    eligible_families = [[toolkit for toolkit in family if toolkit in pool] for family in TOOLKIT_FAMILIES]
    eligible_families = [family for family in eligible_families if len(family) >= 2]
    if not eligible_families:
        return None
    family = random.choice(eligible_families)
    chosen_toolkits = random.sample(family, k=random.randint(2, min(3, len(family))))
    candidates = [random.choice(pool[toolkit]) for toolkit in chosen_toolkits]
    # Add a few additional candidates only from the same coherent family.
    available = [tool for toolkit in chosen_toolkits for tool in pool[toolkit] if tool.slug not in {item.slug for item in candidates}]
    random.shuffle(available)
    candidates.extend(available[:max(0, random.randint(0, MAX_CANDIDATE_TOOLS - len(candidates)))])
    return candidates[:MAX_CANDIDATE_TOOLS]


GENERATION_PROMPT = '''You are creating one realistic multi-tool workflow benchmark for an AI tool-search evaluator.

Candidate tools (you may use only these):
{candidates}

Return exactly one JSON object with these fields:
{{
  "feasible": true or false,
  "task": "A realistic user-facing workflow request, 25-90 words.",
  "required_tool_slugs": ["only candidate slugs that are genuinely required"],
  "dropped_tool_slugs": ["candidate slugs not required"],
  "plausibility_score": 1 to 5,
  "rationale": "brief explanation"
}}

Rules:
- The task must require 2 or more selected tools and resemble a real workplace workflow.
- Do not invent tools, apps, or tool slugs outside the candidates.
- Do not name internal tool slugs in task text.
- Do not force every candidate into the workflow; drop irrelevant candidates.
- Reject artificial or incoherent combinations by setting feasible=false.
'''


def parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def generate_case(client, limiter, candidates: list[ToolInfo]) -> tuple[dict[str, Any] | None, str | None]:
    candidate_text = "\n".join(f"- {tool.slug} ({tool.toolkit}): {tool.description[:350]}" for tool in candidates)
    def call():
        limiter.wait()
        response = client.models.generate_content(model=GEMINI_MODEL, contents=GENERATION_PROMPT.format(candidates=candidate_text))
        return (response.text or "").strip()
    try:
        raw = with_retry(call, max_retries=5, base_delay=3.0)
        return parse_json(raw), raw
    except Exception as error:
        return None, repr(error)


def validate_generated_case(case: dict[str, Any], candidates: list[ToolInfo]) -> str | None:
    allowed = {tool.slug for tool in candidates}
    required = case.get("required_tool_slugs") or []
    selected = set(required)
    if not case.get("feasible"):
        return "Gemini marked the candidate group infeasible"
    if not isinstance(case.get("task"), str) or not case["task"].strip():
        return "missing task text"
    if len(required) < MIN_REQUIRED_TOOLS:
        return f"fewer than {MIN_REQUIRED_TOOLS} required tools"
    if len(required) != len(selected):
        return "duplicate required tool slugs"
    if not selected <= allowed:
        return "Gemini invented a tool slug outside the candidates"
    if int(case.get("plausibility_score", 0)) < MIN_PLAUSIBILITY:
        return f"plausibility score below {MIN_PLAUSIBILITY}"
    return None


def load_cache() -> dict[str, Any]:
    return json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}


def save_cache(cache: dict[str, Any]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def build_synthetic_cases(pool: dict[str, list[ToolInfo]], client) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cache, limiter, accepted, audit = load_cache(), RateLimiter(GEMINI_RPM), [], []
    attempts, max_attempts = 0, NUM_WORKFLOWS * 4
    while len(accepted) < NUM_WORKFLOWS and attempts < max_attempts:
        attempts += 1
        candidates = select_candidates(pool)
        if not candidates:
            break
        key = "|".join(sorted(tool.slug for tool in candidates))
        generated, raw = (cache[key]["generated"], cache[key]["raw"]) if key in cache else generate_case(client, limiter, candidates)
        if key not in cache:
            cache[key] = {"generated": generated, "raw": raw}
            save_cache(cache)
        rejection = "generation error" if generated is None else validate_generated_case(generated, candidates)
        audit_row = {"attempt": attempts, "candidate_toolkits": sorted({tool.toolkit for tool in candidates}), "candidate_tools": [asdict(tool) for tool in candidates], "gemini_raw_response": raw, "generated": generated, "rejection_reason": rejection}
        audit.append(audit_row)
        if rejection:
            print(f"[generate] rejected: {rejection}")
            continue
        case_id = f"synthetic-{len(accepted) + 1:03d}"
        accepted.append({"case_id": case_id, "task": generated["task"].strip(), "expected_tools": generated["required_tool_slugs"], "candidate_toolkits": audit_row["candidate_toolkits"], "candidate_tools": audit_row["candidate_tools"], "dropped_tools": generated.get("dropped_tool_slugs", []), "plausibility_score": generated["plausibility_score"], "rationale": generated.get("rationale", "")})
        print(f"[generate] accepted {case_id}: {len(generated['required_tool_slugs'])} required tools")
    return accepted, audit


def extract_all_results(response: Any) -> dict[str, Any]:
    top = to_plain(response)
    data = top.get("data", top) or {}
    data = data if hasattr(data, "get") else {}
    result_entries = data.get("results") or []
    primary, related, result_toolkits = [], [], set()
    for entry in result_entries:
        entry = to_plain(entry)
        primary.extend(entry.get("primary_tool_slugs") or [])
        related.extend(entry.get("related_tool_slugs") or [])
        result_toolkits.update(entry.get("toolkits") or [])
    primary = list(dict.fromkeys(primary))
    related = [slug for slug in dict.fromkeys(related) if slug not in primary]
    return {"primary": primary, "related": related, "result_toolkits": sorted(result_toolkits), "no_results": not result_entries, "raw_error": data.get("error") or top.get("error"), "raw": top}


def evaluate(session, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, case in enumerate(cases, start=1):
        print(f"[search] ({index}/{len(cases)}) {case['case_id']}")
        started, error, api_latency = time.monotonic(), None, None
        plan = {"primary": [], "related": [], "result_toolkits": [], "no_results": True, "raw_error": None, "raw": {}}
        try:
            response, api_latency = with_retry(session.execute, "COMPOSIO_SEARCH_TOOLS", arguments={"query": case["task"]}, timed=True)
            end_to_end_latency = time.monotonic() - started
            plan = extract_all_results(response)
        except Exception as exc:
            end_to_end_latency = time.monotonic() - started
            error = repr(exc)
            traceback.print_exc()
        expected, primary, related = set(case["expected_tools"]), set(plan["primary"]), set(plan["related"])
        found = primary | related
        primary_hits, all_hits = expected & primary, expected & found
        missed, extras = expected - found, found - expected
        expected_prefixes = {slug.split("_")[0] for slug in expected if "_" in slug}
        cross_toolkit = sorted({slug.split("_")[0] for slug in extras if "_" in slug} - expected_prefixes)
        raw_path = RAW_RESULTS_DIR / f"{case['case_id']}.json"
        raw_path.write_text(json.dumps({"case": case, "request": {"tool": "COMPOSIO_SEARCH_TOOLS", "arguments": {"query": case["task"]}}, "response": plan["raw"]}, indent=2, default=str), encoding="utf-8")
        rows.append({"case_id": case["case_id"], "task": case["task"], "candidate_toolkits": "; ".join(case["candidate_toolkits"]), "expected_tools": "; ".join(sorted(expected)), "expected_count": len(expected), "plausibility_score": case["plausibility_score"], "recall_all": round(len(all_hits) / len(expected), 4), "recall_primary": round(len(primary_hits) / len(expected), 4), "precision_all": round(len(all_hits) / len(found), 4) if found else 0.0, "missed_count": len(missed), "missed_tools": "; ".join(sorted(missed)), "related_only_tools": "; ".join(sorted((expected & related) - primary)), "extra_count": len(extras), "extra_tools": "; ".join(sorted(extras)), "primary_tools": "; ".join(plan["primary"]), "related_tools": "; ".join(plan["related"]), "returned_toolkits": "; ".join(plan["result_toolkits"]), "cross_toolkit_extra_prefixes": "; ".join(cross_toolkit), "api_search_latency_sec": round(api_latency, 2) if api_latency is not None else None, "end_to_end_latency_sec": round(end_to_end_latency, 2), "error": error or plan["raw_error"], "no_results_returned": plan["no_results"], "raw_result_path": str(raw_path)})
        time.sleep(COMPOSIO_CALL_DELAY_SEC)
    return rows


def write_csv(rows: list[dict[str, Any]]) -> None:
    if rows:
        with RESULTS_CSV_PATH.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def report(rows: list[dict[str, Any]], accepted: list[dict[str, Any]], audit: list[dict[str, Any]]) -> None:
    valid = [row for row in rows if not row["error"]]
    rate = lambda field: sum(row[field] for row in valid) / len(valid) if valid else 0.0
    api = [row["api_search_latency_sec"] for row in valid if row["api_search_latency_sec"] is not None]
    end_to_end = [row["end_to_end_latency_sec"] for row in valid]
    rejected = [row for row in audit if row["rejection_reason"]]
    md = ["# Synthetic Multi-Tool Composio Search Evaluation\n", "## Scope", "Synthetic workflows are generated only from curated coherent toolkit families. Gemini selects the required subset of supplied candidate tools; all candidates, decisions, and raw responses are retained in the audit artifacts.\n", "## Summary", f"- **Accepted workflows:** {len(accepted)}", f"- **Generation attempts:** {len(audit)}", f"- **Rejected candidate groups:** {len(rejected)}", f"- **Successful search calls:** {len(valid)}/{len(rows)}", f"- **Average all-result recall:** {rate('recall_all'):.1%}", f"- **Average primary-only recall:** {rate('recall_primary'):.1%}", f"- **Average all-result precision:** {rate('precision_all'):.1%}"]
    if api:
        md.extend(["\n## Latency", "API/Search latency is only the successful request. End-to-end latency includes failed attempts and retry backoff.", "| Metric | API/Search (s) | End-to-end (s) |", "|---|---:|---:|", f"| Average | {statistics.mean(api):.2f} | {statistics.mean(end_to_end):.2f} |", f"| Median (P50) | {statistics.median(api):.2f} | {statistics.median(end_to_end):.2f} |", f"| P95 | {api[int(len(api) * .95)]:.2f} | {end_to_end[int(len(end_to_end) * .95)]:.2f} |", f"| Maximum | {max(api):.2f} | {max(end_to_end):.2f} |"]) 
    md.extend(["\n## Failure Examples", "Sorted by lowest recall, then most missing tools. These should be manually reviewed before being classified as product failures."])
    failures = sorted([row for row in valid if row["recall_all"] < 1], key=lambda row: (row["recall_all"], -row["missed_count"]))[:20]
    for row in failures:
        md.extend([f"\n### {row['case_id']} — Recall {row['recall_all']:.1%}, Precision {row['precision_all']:.1%}", f"- **Task:** {row['task']}", f"- **Expected:** `{row['expected_tools']}`", f"- **Missed:** `{row['missed_tools'] or '(none)'}`", f"- **Primary returned:** `{row['primary_tools'] or '(none)'}`", f"- **Related returned:** `{row['related_tools'] or '(none)'}`", f"- **Extra:** `{row['extra_tools'] or '(none)'}`"])
    if rejected:
        md.extend(["\n## Generation Rejections", "| Reason | Count |", "|---|---:|"])
        reasons: dict[str, int] = {}
        for row in rejected: reasons[row["rejection_reason"]] = reasons.get(row["rejection_reason"], 0) + 1
        md.extend(f"| {reason} | {count} |" for reason, count in sorted(reasons.items()))
    REPORT_MD_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[report] {REPORT_MD_PATH.resolve()}")


def main() -> None:
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY:
        raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    OUTPUT_DIR.mkdir(exist_ok=True)
    RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(RANDOM_SEED)
    composio, gemini = Composio(api_key=COMPOSIO_API_KEY), genai.Client(api_key=GEMINI_API_KEY)
    pool = fetch_tools(composio)
    accepted, audit = build_synthetic_cases(pool, gemini)
    AUDIT_PATH.write_text(json.dumps({"generated_at_utc": datetime.now(timezone.utc).isoformat(), "config": {"num_workflows": NUM_WORKFLOWS, "random_seed": RANDOM_SEED, "toolkit_families": TOOLKIT_FAMILIES}, "accepted_cases": accepted, "attempts": audit}, indent=2, default=str), encoding="utf-8")
    rows = evaluate(composio.create(user_id=USER_ID), accepted)
    write_csv(rows)
    report(rows, accepted, audit)


if __name__ == "__main__":
    main()
