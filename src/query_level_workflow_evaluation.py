"""Primary benchmark: decompose human workflows into query-level search tests.

The 100 workflow tool lists are candidate pools, not expected output from one
search request. Gemini simulates an agent's decomposition and labels each
generated search query with the candidate tools genuinely required for it.
"""
from __future__ import annotations

import csv, json, os, random, re, statistics, time, traceback
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

MAX_USE_CASES = 25       # lower for an inexpensive smoke test
MAX_QUERIES_PER_WORKFLOW = 4
MIN_QUERIES_PER_WORKFLOW = 2
GEMINI_RPM = 15
SEARCH_DELAY_SEC = 0.5
RANDOM_SEED = 42


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


def retry(call, *args, timed=False, max_retries=4, base_delay=2.0, **kwargs):
    last_error = None
    for attempt in range(max_retries):
        try:
            started = time.monotonic(); value = call(*args, **kwargs)
            return (value, time.monotonic() - started) if timed else value
        except Exception as error:
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


DECOMPOSITION_PROMPT = '''You are simulating an agent deciding how to search for tools while completing a workflow.

High-level workflow:
{task}

Human-provided candidate tool pool (these are NOT all required for every search):
{candidates}

Generate {minimum} to {maximum} realistic, concrete COMPOSIO_SEARCH_TOOLS queries an agent would make while solving this workflow. Return exactly JSON:
{{"queries":[{{"query":"short natural search query","required_tool_slugs":["candidate slugs genuinely required by THIS query"],"supporting_tool_slugs":["optional relevant candidate slugs"],"rationale":"why the required tools fit this query"}}]}}

Rules:
- Decompose the workflow; never send the whole workflow as one search query.
- Every query needs 1-3 required tools. Use multiple only for one genuinely compositional intent.
- Required/supporting slugs MUST be from the candidate pool. Do not invent slugs.
- Do not list a tool merely because it appears in the workflow; label it only if this query needs it.
- Write queries an agent would naturally use, not internal tool names.
'''


def strip_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"): text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text.strip()


def generate_queries(client, limiter, case: UseCase) -> tuple[dict[str, Any] | None, str]:
    candidates = "\n".join(f"- {slug}" for slug in case.candidate_tools)
    prompt = DECOMPOSITION_PROMPT.format(task=case.task, candidates=candidates, minimum=MIN_QUERIES_PER_WORKFLOW, maximum=MAX_QUERIES_PER_WORKFLOW)
    def call():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        raw = retry(call, max_retries=5, base_delay=3.0)
        return json.loads(strip_json(raw)), raw
    except Exception as error:
        return None, repr(error)


def validate_generation(payload: Any, candidate_tools: list[str]) -> str | None:
    if not isinstance(payload, dict) or not isinstance(payload.get("queries"), list): return "missing queries list"
    queries = payload["queries"]
    if not MIN_QUERIES_PER_WORKFLOW <= len(queries) <= MAX_QUERIES_PER_WORKFLOW: return "query count outside configured range"
    allowed, seen = set(candidate_tools), set()
    for item in queries:
        query, required = item.get("query"), item.get("required_tool_slugs") or []
        if not isinstance(query, str) or len(query.split()) < 3: return "empty or implausibly short query"
        if not required or len(required) > 3 or not set(required) <= allowed: return "invalid or invented required tool"
        if not set(item.get("supporting_tool_slugs") or []) <= allowed: return "invented supporting tool"
        if query.lower() in seen: return "duplicate query"
        seen.add(query.lower())
    return None


def load_json(path: Path, fallback): return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback
def save_json(path: Path, value): path.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")


def build_ground_truth(cases: list[UseCase], client) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cache, limiter, accepted, audit = load_json(CACHE_PATH, {}), RateLimiter(GEMINI_RPM), [], []
    for case in cases[:MAX_USE_CASES]:
        cache_key = str(case.id)
        if cache_key in cache: payload, raw = cache[cache_key]["payload"], cache[cache_key]["raw"]
        else:
            print(f"[generate] workflow {case.id}")
            payload, raw = generate_queries(client, limiter, case)
            cache[cache_key] = {"payload": payload, "raw": raw}; save_json(CACHE_PATH, cache)
        rejection = "generation error" if payload is None else validate_generation(payload, case.candidate_tools)
        audit.append({"use_case": asdict(case), "gemini_raw_response": raw, "generated": payload, "rejection_reason": rejection})
        if rejection:
            print(f"  rejected: {rejection}"); continue
        for query_index, item in enumerate(payload["queries"], start=1):
            accepted.append({"query_id": f"workflow-{case.id:03d}-q{query_index}", "workflow_id": case.id, "workflow_task": case.task, "query": item["query"].strip(), "required_tools": item["required_tool_slugs"], "supporting_tools": item.get("supporting_tool_slugs") or [], "rationale": item.get("rationale", ""), "candidate_tools": case.candidate_tools})
    return accepted, audit


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
    except Exception as exc:
        end_to_end = time.monotonic() - started; error = repr(exc); traceback.print_exc()
    required, primary, related = set(row["required_tools"]), set(plan["primary"]), set(plan["related"])
    found, primary_hits, all_hits = primary | related, required & primary, required & (primary | related)
    raw_path = raw_dir / f"{row['query_id']}.json"
    save_json(raw_path, {"query_ground_truth": row, "request": {"query": row["query"]}, "response": plan["raw"]})
    return {**row, "expected_count": len(required), "primary_hit": bool(primary_hits), "any_hit": bool(all_hits), "primary_recall": round(len(primary_hits)/len(required), 4), "recall": round(len(all_hits)/len(required), 4), "primary_rank": min((plan["primary"].index(tool)+1 for tool in primary_hits), default=None), "related_only_tools": "; ".join(sorted((required & related) - primary)), "missed_tools": "; ".join(sorted(required - found)), "extra_tools": "; ".join(sorted(found - required)), "primary_tools": "; ".join(plan["primary"]), "related_tools": "; ".join(plan["related"]), "returned_toolkits": "; ".join(plan["toolkits"]), "api_search_latency_sec": round(api_latency, 2) if api_latency is not None else None, "end_to_end_latency_sec": round(end_to_end, 2), "error": error or plan["error"], "no_results_returned": plan["no_results"], "raw_result_path": str(raw_path)}


def write_csv(rows, path: Path):
    if rows:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def write_report(rows, accepted, audit):
    valid = [row for row in rows if not row["error"]]; rejected = [row for row in audit if row["rejection_reason"]]
    mean = lambda field: sum(row[field] for row in valid)/len(valid) if valid else 0
    api, e2e = sorted(row["api_search_latency_sec"] for row in valid if row["api_search_latency_sec"] is not None), sorted(row["end_to_end_latency_sec"] for row in valid)
    md = ["# Query-Level Workflow Benchmark\n", "## Method", "Each human workflow is decomposed into agent-like search queries. Its listed tools are a candidate pool; Gemini labels only the tools genuinely required per query. Every Composio result entry is aggregated before scoring.\n", "## Summary", f"- **Workflows accepted:** {len({row['workflow_id'] for row in accepted})}", f"- **Query-level test cases:** {len(rows)}", f"- **Rejected workflow decompositions:** {len(rejected)}", f"- **Average primary recall:** {mean('primary_recall'):.1%}", f"- **Average retrieval recall:** {mean('recall'):.1%}", f"- **Any-required-tool hit rate:** {mean('any_hit'):.1%}"]
    if api: md.extend(["\n## Latency", "API/Search latency is the successful call only; end-to-end includes failed attempts and retry backoff.\n", "| Metric | API/Search (s) | End-to-end (s) |", "|---|---:|---:|", f"| Average | {statistics.mean(api):.2f} | {statistics.mean(e2e):.2f} |", f"| Median (P50) | {statistics.median(api):.2f} | {statistics.median(e2e):.2f} |", f"| P95 | {api[int(len(api)*.95)]:.2f} | {e2e[int(len(e2e)*.95)]:.2f} |", f"| Maximum | {api[-1]:.2f} | {e2e[-1]:.2f} |"])
    md.extend(["\n## Failure Examples", "These are query-level candidates for manual review, not automatic product-bug conclusions."])
    for row in sorted([row for row in valid if row["recall"] < 1], key=lambda x: (x["recall"], -x["expected_count"]))[:20]: md.extend([f"\n### {row['query_id']} — recall {row['recall']:.1%}", f"- **Query:** {row['query']}", f"- **Required:** `{'; '.join(row['required_tools'])}`", f"- **Missed:** `{row['missed_tools'] or '(none)'}`", f"- **Primary returned:** `{row['primary_tools'] or '(none)'}`"])
    REPORT_PATH.write_text("\n".join(md)+"\n", encoding="utf-8")


def main():
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY: raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True); RAW_DIR.mkdir(exist_ok=True); random.seed(RANDOM_SEED)
    cases = parse_use_cases(USE_CASES_FILE); composio, client = Composio(api_key=COMPOSIO_API_KEY), genai.Client(api_key=GEMINI_API_KEY)
    ground_truth, audit = build_ground_truth(cases, client)
    save_json(GROUND_TRUTH_PATH, {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "queries": ground_truth})
    save_json(AUDIT_PATH, {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "attempts": audit})
    session = composio.create(user_id=USER_ID); rows = []
    for index, row in enumerate(ground_truth, 1):
        print(f"[search] {index}/{len(ground_truth)} {row['query_id']}"); rows.append(score_query(session, row, RAW_DIR)); time.sleep(SEARCH_DELAY_SEC)
    write_csv(rows, RESULTS_PATH); write_report(rows, ground_truth, audit)


if __name__ == "__main__": main()
