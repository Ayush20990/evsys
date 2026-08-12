"""Ground-truth multi-tool COMPOSIO_SEARCH_TOOLS evaluation."""
from __future__ import annotations
import csv, json, os, re, statistics, time, traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple
from composio import Composio
from dotenv import load_dotenv

load_dotenv()
COMPOSIO_API_KEY = os.environ.get("COMPOSIO_API_KEY")
USE_CASES_FILE = Path("top-100-eval-use-cases.md")
EVAL_DIR = Path("evaluation"); RAW_RESULTS_DIR = EVAL_DIR / "raw_results"
RESULTS_CSV_PATH = EVAL_DIR / "composio_search_eval_results.csv"; REPORT_MD_PATH = EVAL_DIR / "composio_search_eval_report.md"
COMPOSIO_CALL_DELAY_SEC, USER_ID = 1.0, "eval-user-multi-tool"
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class UseCase:
    id: int
    prompt: str
    expected_tools: set[str]
    description: str

def parse_use_cases(filepath: Path) -> list[UseCase]:
    if not filepath.exists(): raise FileNotFoundError(f"Could not find {filepath}. Please ensure it is in the working directory.")
    pattern = re.compile(r'(\d+)\.\s+\*\*(.*?)\*\*\s*-\s*Tools:\s*(.*?)\s*-\s*Description:\s*(.*?)(?=\n\d+\.\s+\*\*|\Z)', re.DOTALL)
    cases = [UseCase(int(uid), prompt.strip(), {tool.strip() for tool in raw.replace('`', '').split(',') if tool.strip()}, description.strip()) for uid, prompt, raw, description in pattern.findall(filepath.read_text(encoding="utf-8"))]
    print(f"[parse] Successfully loaded {len(cases)} use cases."); return cases

def to_plain(obj: Any) -> dict:
    if hasattr(obj, "model_dump"): return obj.model_dump()
    if isinstance(obj, dict): return obj
    return vars(obj) if hasattr(obj, "__dict__") else obj

def extract_tools_from_response(response: Any) -> dict:
    top = to_plain(response); data = top.get("data", top) or {}; data = data if hasattr(data, "get") else {}
    results = data.get("results") or []; primary, related = set(), set()
    for result in results:
        result = to_plain(result); primary.update(result.get("primary_tool_slugs") or []); related.update(result.get("related_tool_slugs") or [])
    related -= primary
    return {"primary_found": primary, "related_found": related, "total_found": primary | related, "no_results": not results, "raw_error": data.get("error") or top.get("error"), "raw": top}

def with_retry(fn, *args, max_retries=3, base_delay=2.0, **kwargs) -> Tuple[Any, int, float]:
    """Return the response, retry count, and successful-call duration only."""
    last_err = None
    for attempt in range(max_retries):
        try:
            api_started = time.monotonic()
            result = fn(*args, **kwargs)
            return result, attempt, time.monotonic() - api_started
        except Exception as error: last_err = error; print(f"  [Retry {attempt + 1}/{max_retries}] API error: {error}. Waiting..."); time.sleep(base_delay * (2 ** attempt))
    raise last_err

def run_eval(session, use_cases):
    rows = []
    for index, case in enumerate(use_cases):
        print(f"[search] ({index + 1}/{len(use_cases)}) Executing Use Case #{case.id}..."); end_to_end_started, error, retries, api_search_latency = time.monotonic(), None, 0, None
        plan = {"primary_found": set(), "related_found": set(), "total_found": set(), "no_results": True, "raw_error": None, "raw": {}}
        try:
            response, retries, api_search_latency = with_retry(session.execute, "COMPOSIO_SEARCH_TOOLS", arguments={"query": case.prompt})
            end_to_end_latency = time.monotonic() - end_to_end_started
            plan = extract_tools_from_response(response)
        except Exception as exc:
            end_to_end_latency = time.monotonic() - end_to_end_started
            error = repr(exc); traceback.print_exc()
        (RAW_RESULTS_DIR / f"use_case_{case.id:03d}.json").write_text(json.dumps({"use_case_id": case.id, "prompt": case.prompt, "expected_tools": list(case.expected_tools), "composio_response": plan["raw"]}, indent=2, default=str), encoding="utf-8")
        expected, found_all, found_primary = case.expected_tools, plan["total_found"], plan["primary_found"]
        hits_all, hits_primary = expected & found_all, expected & found_primary
        recall_all = len(hits_all) / len(expected) if expected else 0.0; recall_primary = len(hits_primary) / len(expected) if expected else 0.0
        precision_all = len(hits_all) / len(found_all) if found_all else 0.0; precision_primary = len(hits_primary) / len(found_primary) if found_primary else 0.0
        rows.append({"use_case_id": case.id, "prompt": case.prompt, "expected_count": len(expected), "expected_tools": "; ".join(sorted(expected)), "recall_all": round(recall_all, 4), "recall_primary": round(recall_primary, 4), "precision_all": round(precision_all, 4), "precision_primary": round(precision_primary, 4), "missed_count": len(expected - found_all), "missed_tools": "; ".join(sorted(expected - found_all)), "extra_count": len(found_all - expected), "extra_tools": "; ".join(sorted(found_all - expected)), "found_primary": "; ".join(sorted(found_primary)), "found_related": "; ".join(sorted(plan["related_found"])), "api_search_latency_sec": round(api_search_latency, 2) if api_search_latency is not None else None, "end_to_end_latency_sec": round(end_to_end_latency, 2), "retries": retries, "error": error or plan["raw_error"], "no_results_returned": plan["no_results"]})
        time.sleep(COMPOSIO_CALL_DELAY_SEC)
    return rows

def write_csv(rows, path):
    if rows:
        with path.open("w", newline="", encoding="utf-8") as file: writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

def generate_markdown_report(rows):
    valid = [row for row in rows if not row["error"] and not row["no_results_returned"]]
    if not valid: print("No valid queries to summarize."); return
    avg_recall = sum(row["recall_all"] for row in valid) / len(valid); avg_precision = sum(row["precision_all"] for row in valid) / len(valid)
    api_latencies = sorted(row["api_search_latency_sec"] for row in valid if row["api_search_latency_sec"] is not None)
    end_to_end_latencies = sorted(row["end_to_end_latency_sec"] for row in valid)
    buckets = {"1-3": [], "4-7": [], "8-12": [], "13+": []}; stats = {}
    for row in valid:
        buckets["1-3" if row["expected_count"] <= 3 else "4-7" if row["expected_count"] <= 7 else "8-12" if row["expected_count"] <= 12 else "13+"].append(row)
        found = set(row["found_primary"].split("; ") + row["found_related"].split("; "))
        for tool in filter(None, row["expected_tools"].split("; ")):
            toolkit = tool.split("_")[0] if "_" in tool else "UNKNOWN"; stats.setdefault(toolkit, {"expected": 0, "found": 0}); stats[toolkit]["expected"] += 1; stats[toolkit]["found"] += tool in found
    def latency_rows(label, values):
        return [f"| {label} average | {statistics.mean(values):.2f} |", f"| {label} median (P50) | {statistics.median(values):.2f} |", f"| {label} P95 | {values[int(len(values) * 0.95)]:.2f} |", f"| {label} max | {values[-1]:.2f} |"]
    md = ["# Composio Search Multi-Tool Evaluation Report\n", "## 1. Executive Summary", f"- **Total Use Cases:** {len(rows)}", f"- **Successful API Responses:** {len(valid)}", f"- **Failed/Empty Responses:** {len(rows) - len(valid)}", f"- **Average Recall (All):** {avg_recall:.1%}", f"- **Average Precision (All):** {avg_precision:.1%}\n", "## 2. Latency Metrics", "API/Search latency measures only the successful `COMPOSIO_SEARCH_TOOLS` call. End-to-end latency includes all failed attempts and retry backoff.\n", "| Metric | Time (seconds) |", "|--------|----------------|"] + latency_rows("API/Search", api_latencies) + latency_rows("End-to-end", end_to_end_latencies) + ["\n## 3. Performance by Query Complexity", "| Expected Tools | Case Count | Avg Recall | Avg Precision |", "|----------------|------------|------------|---------------|"]
    for label, bucket in buckets.items():
        if bucket: md.append(f"| {label} | {len(bucket)} | {sum(row['recall_all'] for row in bucket)/len(bucket):.1%} | {sum(row['precision_all'] for row in bucket)/len(bucket):.1%} |")
    md.extend(["\n## 4. Performance by Toolkit", "| Toolkit | Total Expected | Found | Recall |", "|---------|----------------|-------|--------|"])
    for toolkit, stat in sorted(stats.items(), key=lambda item: item[1]["expected"], reverse=True): md.append(f"| {toolkit} | {stat['expected']} | {stat['found']} | {stat['found']/stat['expected']:.1%} |")
    md.extend(["\n## 5. Top 15 Worst Performing Workflows", "Sorted by lowest recall, then highest missing tool count.\n"])
    for row in sorted((row for row in valid if row["recall_all"] < 1), key=lambda item: (item["recall_all"], -item["missed_count"]))[:15]: md.extend([f"### Use Case #{row['use_case_id']} - Recall: {row['recall_all']:.1%} | Precision: {row['precision_all']:.1%}", f"- **Missed ({row['missed_count']}):** `{row['missed_tools'][:150]}...`", f"- **Extra returned ({row['extra_count']}):** `{row['extra_tools'][:150]}...`", f"- **Prompt Excerpt:** _{row['prompt'][:100]}..._\n"])
    REPORT_MD_PATH.write_text("\n".join(md), encoding="utf-8"); print(f"Markdown report successfully generated at: {REPORT_MD_PATH.resolve()}")

def main():
    if not COMPOSIO_API_KEY: raise ValueError("Set COMPOSIO_API_KEY in .env")
    composio = Composio(api_key=COMPOSIO_API_KEY); cases = parse_use_cases(USE_CASES_FILE); rows = run_eval(composio.create(user_id=USER_ID), cases); write_csv(rows, RESULTS_CSV_PATH); generate_markdown_report(rows)
if __name__ == "__main__": main()
