"""Tertiary benchmark: LLM-invented tasks, decomposed and scored the same way
as the primary benchmark, but independent of top-100-eval-use-cases.md.

Unlike the human-written use cases, these tasks have no pre-supplied tool
list. Ground truth cannot be invented from nothing without risking
hallucinated tool slugs, so this script grounds each task in a pool of real
tool slugs/descriptions fetched live from Composio for a curated, coherent
toolkit family. One Gemini call per task both (a) writes a top-100-style task
description without naming any tools, and (b) decomposes that task into 2-4
concrete search queries, each labeled with the required tools genuinely
needed for that one query -- drawn only from the fetched candidate pool.
Scoring reuses the exact query_level_workflow_evaluation scoring path.

Kept deliberately small (NUM_TASKS = 10): each task costs one Gemini call
plus a handful of Composio search calls, so a full run stays fast and cheap.
"""
from __future__ import annotations

import json, os, random, time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai

from query_level_workflow_evaluation import (
    GEMINI_MODEL, RateLimiter, retry, score_query, save_json, strip_json, write_csv,
)

load_dotenv()
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USER_ID = "synthetic-query-level-eval-user"

OUTPUT_DIR = Path(__file__).resolve().parent / "synthetic_query_level_evaluation"
GROUND_TRUTH_PATH = OUTPUT_DIR / "query_ground_truth.json"
AUDIT_PATH = OUTPUT_DIR / "generation_audit.json"
RESULTS_PATH = OUTPUT_DIR / "search_results.csv"
REPORT_PATH = OUTPUT_DIR / "summary_report.md"
RAW_DIR = OUTPUT_DIR / "raw_search_results"
CACHE_PATH = OUTPUT_DIR / "generation_cache.json"

NUM_TASKS = 10            # kept small; raise once mappings are manually reviewed
MIN_QUERIES_PER_TASK, MAX_QUERIES_PER_TASK = 2, 4
MIN_TOOLKITS_PER_TASK = 2  # forces genuinely cross-toolkit tasks, like top-100
MAX_CANDIDATE_TOOLS = 8
MIN_PLAUSIBILITY = 4
RANDOM_SEED = 7
GEMINI_RPM, SEARCH_DELAY_SEC = 15, 0.5

# Same rationale as the deleted synthetic evaluator: coherent families instead
# of arbitrary combinations, so rejections aren't dominated by incoherence.
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


def fetch_tools(composio: Composio) -> dict[str, list[ToolInfo]]:
    pool: dict[str, list[ToolInfo]] = {}
    for toolkit in sorted({t for family in TOOLKIT_FAMILIES for t in family}):
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
    eligible = [[toolkit for toolkit in family if toolkit in pool] for family in TOOLKIT_FAMILIES]
    eligible = [family for family in eligible if len(family) >= MIN_TOOLKITS_PER_TASK]
    if not eligible:
        return None
    family = random.choice(eligible)
    chosen = random.sample(family, k=random.randint(MIN_TOOLKITS_PER_TASK, min(3, len(family))))
    candidates = [random.choice(pool[toolkit]) for toolkit in chosen]
    rest = [tool for toolkit in chosen for tool in pool[toolkit] if tool.slug not in {c.slug for c in candidates}]
    random.shuffle(rest)
    candidates.extend(rest[:max(0, random.randint(1, MAX_CANDIDATE_TOOLS - len(candidates)))])
    return candidates[:MAX_CANDIDATE_TOOLS]


GENERATION_PROMPT = '''You are creating one realistic multi-step workplace task for an AI tool-search benchmark,
in the same style as a human-written workflow brief -- a short paragraph describing what someone
needs done, NOT a list of tool calls or API names.

Candidate tools available to whoever solves this task (internal reference only -- never name
slugs, APIs, or product-internal terms in the task text or the queries):
{candidates}

Return exactly one JSON object:
{{
  "feasible": true or false,
  "task": "25-90 word realistic task description spanning at least {min_toolkits} of the candidate toolkits above. No tool/slug names.",
  "queries": [
    {{"query": "a concrete, natural search query an agent would issue while solving this task",
      "required_tool_slugs": ["1-3 candidate slugs genuinely required by THIS query"],
      "supporting_tool_slugs": ["other relevant candidate slugs, optional"],
      "rationale": "why the required tools fit this one query"}}
  ],
  "plausibility_score": 1 to 5,
  "rationale": "brief explanation of why the task and decomposition are coherent"
}}

Rules:
- Decompose the task into {min_queries}-{max_queries} queries; never one query for the whole task.
- Every query needs 1-3 required tool slugs, taken only from the candidates. Do not invent slugs.
- Do not force every candidate into the task; drop candidates that don't fit.
- Reject artificial or incoherent candidate combinations by setting feasible=false.
'''


def generate_task(client, limiter, candidates: list[ToolInfo]) -> tuple[dict[str, Any] | None, str]:
    candidate_text = "\n".join(f"- {tool.slug} ({tool.toolkit}): {tool.description[:300]}" for tool in candidates)
    prompt = GENERATION_PROMPT.format(candidates=candidate_text, min_toolkits=MIN_TOOLKITS_PER_TASK, min_queries=MIN_QUERIES_PER_TASK, max_queries=MAX_QUERIES_PER_TASK)
    def call():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        raw = retry(call, max_retries=5, base_delay=3.0)
        return json.loads(strip_json(raw)), raw
    except Exception as error:
        return None, repr(error)


def validate_generation(payload: Any, candidates: list[ToolInfo]) -> str | None:
    allowed = {tool.slug for tool in candidates}
    if not isinstance(payload, dict):
        return "not a JSON object"
    if not payload.get("feasible"):
        return "Gemini marked the candidate group infeasible"
    if not isinstance(payload.get("task"), str) or len(payload["task"].split()) < 15:
        return "missing or implausibly short task text"
    queries = payload.get("queries")
    if not isinstance(queries, list) or not MIN_QUERIES_PER_TASK <= len(queries) <= MAX_QUERIES_PER_TASK:
        return "query count outside configured range"
    used_toolkits = set()
    for item in queries:
        query, required = item.get("query"), item.get("required_tool_slugs") or []
        if not isinstance(query, str) or len(query.split()) < 3:
            return "empty or implausibly short query"
        if not required or len(required) > 3 or not set(required) <= allowed:
            return "invalid or invented required tool"
        if not set(item.get("supporting_tool_slugs") or []) <= allowed:
            return "invented supporting tool"
        used_toolkits.update(slug.split("_")[0].lower() for slug in required)
    if int(payload.get("plausibility_score", 0)) < MIN_PLAUSIBILITY:
        return f"plausibility score below {MIN_PLAUSIBILITY}"
    if len({tool.toolkit for tool in candidates if tool.slug.split("_")[0].lower() in used_toolkits}) < MIN_TOOLKITS_PER_TASK:
        return "fewer than the required number of toolkits actually used"
    return None


def load_json(path: Path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback


def build_ground_truth(pool: dict[str, list[ToolInfo]], client) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cache, limiter, accepted, audit = load_json(CACHE_PATH, {}), RateLimiter(GEMINI_RPM), [], []
    tasks_accepted, attempts, max_attempts = 0, 0, NUM_TASKS * 4
    while tasks_accepted < NUM_TASKS and attempts < max_attempts:
        attempts += 1
        candidates = select_candidates(pool)
        if not candidates:
            break
        key = "|".join(sorted(tool.slug for tool in candidates))
        if key in cache:
            payload, raw = cache[key]["payload"], cache[key]["raw"]
        else:
            print(f"[generate] attempt {attempts}: {sorted({t.toolkit for t in candidates})}")
            payload, raw = generate_task(client, limiter, candidates)
            cache[key] = {"payload": payload, "raw": raw}
            save_json(CACHE_PATH, cache)
        rejection = "generation error" if payload is None else validate_generation(payload, candidates)
        audit.append({"attempt": attempts, "candidate_toolkits": sorted({t.toolkit for t in candidates}), "candidate_tools": [asdict(t) for t in candidates], "gemini_raw_response": raw, "generated": payload, "rejection_reason": rejection})
        if rejection:
            print(f"  rejected: {rejection}")
            continue
        tasks_accepted += 1
        task_id = f"synthetic-{tasks_accepted:03d}"
        for query_index, item in enumerate(payload["queries"], start=1):
            accepted.append({"query_id": f"{task_id}-q{query_index}", "workflow_id": task_id, "workflow_task": payload["task"].strip(), "query": item["query"].strip(), "required_tools": item["required_tool_slugs"], "supporting_tools": item.get("supporting_tool_slugs") or [], "rationale": item.get("rationale", ""), "candidate_tools": [t.slug for t in candidates], "candidate_toolkits": sorted({t.toolkit for t in candidates}), "plausibility_score": payload["plausibility_score"]})
        print(f"[generate] accepted {task_id} ({tasks_accepted}/{NUM_TASKS}): {len(payload['queries'])} queries")
    return accepted, audit


def main():
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY:
        raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    OUTPUT_DIR.mkdir(exist_ok=True)
    RAW_DIR.mkdir(exist_ok=True)
    random.seed(RANDOM_SEED)
    composio, client = Composio(api_key=COMPOSIO_API_KEY), genai.Client(api_key=GEMINI_API_KEY)
    pool = fetch_tools(composio)
    ground_truth, audit = build_ground_truth(pool, client)
    save_json(GROUND_TRUTH_PATH, {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "config": {"num_tasks": NUM_TASKS, "random_seed": RANDOM_SEED, "toolkit_families": TOOLKIT_FAMILIES}, "queries": ground_truth})
    save_json(AUDIT_PATH, {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "attempts": audit})
    session = composio.create(user_id=USER_ID)
    rows = []
    for index, row in enumerate(ground_truth, 1):
        print(f"[search] {index}/{len(ground_truth)} {row['query_id']}")
        rows.append(score_query(session, row, RAW_DIR))
        time.sleep(SEARCH_DELAY_SEC)
    write_csv(rows, RESULTS_PATH)
    write_report(rows, ground_truth, audit)


def write_report(rows, accepted, audit):
    import statistics
    valid = [row for row in rows if not row["error"]]
    rejected = [row for row in audit if row["rejection_reason"]]
    mean = lambda field: sum(row[field] for row in valid) / len(valid) if valid else 0
    api = sorted(row["api_search_latency_sec"] for row in valid if row["api_search_latency_sec"] is not None)
    e2e = sorted(row["end_to_end_latency_sec"] for row in valid)
    md = ["# Synthetic Query-Level Benchmark\n", "## Method",
          "Tasks are LLM-invented, not drawn from top-100-eval-use-cases.md, but grounded in real tool "
          "slugs/descriptions fetched live from Composio for a curated toolkit family (never hallucinated). "
          "One Gemini call per task both writes the task text and decomposes it into per-query ground truth, "
          "identical in structure and scoring to the primary benchmark.\n",
          "## Summary",
          f"- **Tasks accepted:** {len({row['workflow_id'] for row in accepted})}",
          f"- **Generation attempts:** {len(audit)}",
          f"- **Rejected candidate groups:** {len(rejected)}",
          f"- **Query-level test cases:** {len(rows)}",
          f"- **Average primary recall:** {mean('primary_recall'):.1%}",
          f"- **Average retrieval recall:** {mean('recall'):.1%}",
          f"- **Any-required-tool hit rate:** {mean('any_hit'):.1%}"]
    if api:
        md.extend(["\n## Latency", "| Metric | API/Search (s) | End-to-end (s) |", "|---|---:|---:|",
                    f"| Average | {statistics.mean(api):.2f} | {statistics.mean(e2e):.2f} |",
                    f"| Median (P50) | {statistics.median(api):.2f} | {statistics.median(e2e):.2f} |",
                    f"| Maximum | {api[-1]:.2f} | {e2e[-1]:.2f} |"])
    md.extend(["\n## Failure Examples", "Review alongside the invented task before assigning fault to search; task/query generation may itself be ambiguous."])
    for row in sorted([row for row in valid if row["recall"] < 1], key=lambda x: (x["recall"], -x["expected_count"]))[:20]:
        md.extend([f"\n### {row['query_id']} — recall {row['recall']:.1%}", f"- **Task:** {row['workflow_task']}", f"- **Query:** {row['query']}", f"- **Required:** `{'; '.join(row['required_tools'])}`", f"- **Missed:** `{row['missed_tools'] or '(none)'}`", f"- **Primary returned:** `{row['primary_tools'] or '(none)'}`"])
    if rejected:
        md.extend(["\n## Generation Rejections", "| Reason | Count |", "|---|---:|"])
        reasons: dict[str, int] = {}
        for row in rejected:
            reasons[row["rejection_reason"]] = reasons.get(row["rejection_reason"], 0) + 1
        md.extend(f"| {reason} | {count} |" for reason, count in sorted(reasons.items()))
    REPORT_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
