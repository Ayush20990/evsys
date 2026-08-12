"""Secondary benchmark: robustness of query-level ground truth.

Runs semantically equivalent explicit, implicit, and paraphrased versions of
the query-level labels produced by query_level_workflow_evaluation.py.
"""
from __future__ import annotations

import csv, json, os, random, statistics, time
from pathlib import Path
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai
from query_level_workflow_evaluation import (
    GEMINI_MODEL, RateLimiter, extract_results, retry, score_query, save_json,
)

load_dotenv()
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USER_ID = "query-robustness-eval-user"
SOURCE_GROUND_TRUTH = Path(__file__).resolve().parent / "query_level_workflow_evaluation" / "query_ground_truth.json"
OUTPUT_DIR = Path(__file__).resolve().parent / "query_robustness_evaluation"
CACHE_PATH = OUTPUT_DIR / "variant_cache.json"
VARIANTS_PATH = OUTPUT_DIR / "query_variants.json"
RESULTS_PATH = OUTPUT_DIR / "search_results.csv"
REPORT_PATH = OUTPUT_DIR / "summary_report.md"
RAW_DIR = OUTPUT_DIR / "raw_search_results"

MAX_SOURCE_QUERIES = 60  # 60 source intents x 3 variants = 180 searches
GEMINI_RPM, SEARCH_DELAY_SEC = 15, 0.5

VARIANT_PROMPT = '''Rewrite this tool-search query into exactly three variants without changing its intended operation(s) or required tool set.

Original query: {query}
Required candidate tools: {required}

Return exactly JSON:
{{"variants": [
  {{"dimension":"explicit","query":"same intent; naturally mention relevant app names"}},
  {{"dimension":"implicit","query":"same intent; do not mention app names"}},
  {{"dimension":"paraphrase","query":"same intent in distinctly different natural phrasing"}}
]}}

Rules: each query must be a realistic search query, not mention internal tool slugs, and preserve the same required operations. Do not add operations.
'''


def load_json(path: Path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback


def parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"): text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text.strip())


def generate_variants(client, limiter, source: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    prompt = VARIANT_PROMPT.format(query=source["query"], required=", ".join(source["required_tools"]))
    def call():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        raw = retry(call, max_retries=5, base_delay=3.0)
        return parse_json(raw), raw
    except Exception as error:
        return None, repr(error)


def validate(payload: Any) -> str | None:
    expected = {"explicit", "implicit", "paraphrase"}
    variants = payload.get("variants") if isinstance(payload, dict) else None
    if not isinstance(variants, list) or len(variants) != 3: return "expected exactly three variants"
    dimensions = {item.get("dimension") for item in variants}
    if dimensions != expected: return "variant dimensions are missing or duplicated"
    if any(not isinstance(item.get("query"), str) or len(item["query"].split()) < 3 for item in variants): return "empty or implausibly short variant"
    return None


def write_csv(rows):
    if rows:
        with RESULTS_PATH.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def write_report(rows, audit):
    valid = [row for row in rows if not row["error"]]
    rate = lambda group, field: sum(row[field] for row in group)/len(group) if group else 0
    md = ["# Query Robustness Benchmark\n", "## Method", "Uses query-level ground truth from the primary workflow-decomposition benchmark. For the same intent, it compares explicit app mentions, implicit wording, and a paraphrase; expected tools are unchanged. This isolates search robustness from workflow decomposition.\n", "## Summary", f"- **Source intents sampled:** {len({row['source_query_id'] for row in rows})}", f"- **Variant search calls:** {len(rows)}", f"- **Generation failures:** {sum(1 for item in audit if item.get('rejection_reason'))}", "\n| Variant | Queries | Any-hit rate | Avg recall | Primary-hit rate |", "|---|---:|---:|---:|---:|"]
    for dimension in ("explicit", "implicit", "paraphrase"):
        group = [row for row in valid if row["variant_dimension"] == dimension]
        md.append(f"| {dimension} | {len(group)} | {rate(group, 'any_hit'):.1%} | {rate(group, 'recall'):.1%} | {rate(group, 'primary_hit'):.1%} |")
    failures = sorted([row for row in valid if row["recall"] < 1], key=lambda row: (row["recall"], row["variant_dimension"]))[:20]
    md.extend(["\n## Failure Examples", "Review these alongside the original query before assigning fault to search; variants may expose query-generation ambiguity."])
    for row in failures:
        md.extend([f"\n### {row['query_id']} — {row['variant_dimension']}, recall {row['recall']:.1%}", f"- **Query:** {row['query']}", f"- **Required:** `{'; '.join(row['required_tools'])}`", f"- **Missed:** `{row['missed_tools'] or '(none)'}`", f"- **Primary returned:** `{row['primary_tools'] or '(none)'}`"])
    REPORT_PATH.write_text("\n".join(md)+"\n", encoding="utf-8")


def main():
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY: raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    if not SOURCE_GROUND_TRUTH.exists(): raise FileNotFoundError("Run query_level_workflow_evaluation.py first to create query_ground_truth.json")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True); RAW_DIR.mkdir(exist_ok=True)
    source_queries = load_json(SOURCE_GROUND_TRUTH, {})["queries"][:MAX_SOURCE_QUERIES]
    cache, limiter, variants, audit = load_json(CACHE_PATH, {}), RateLimiter(GEMINI_RPM), [], []
    client = genai.Client(api_key=GEMINI_API_KEY)
    for index, source in enumerate(source_queries, 1):
        key = source["query_id"]
        if key in cache: payload, raw = cache[key]["payload"], cache[key]["raw"]
        else:
            print(f"[variants] {index}/{len(source_queries)} {key}")
            payload, raw = generate_variants(client, limiter, source); cache[key] = {"payload": payload, "raw": raw}; save_json(CACHE_PATH, cache)
        rejection = "generation error" if payload is None else validate(payload)
        audit.append({"source_query_id": key, "raw": raw, "generated": payload, "rejection_reason": rejection})
        if rejection: continue
        for item in payload["variants"]:
            variants.append({**source, "source_query_id": key, "query_id": f"{key}-{item['dimension']}", "query": item["query"], "variant_dimension": item["dimension"]})
    save_json(VARIANTS_PATH, {"source": str(SOURCE_GROUND_TRUTH), "variants": variants, "audit": audit})
    session = Composio(api_key=COMPOSIO_API_KEY).create(user_id=USER_ID)
    rows = []
    for index, variant in enumerate(variants, 1):
        print(f"[search] {index}/{len(variants)} {variant['query_id']}")
        rows.append(score_query(session, variant, RAW_DIR)); time.sleep(SEARCH_DELAY_SEC)
    write_csv(rows); write_report(rows, audit)


if __name__ == "__main__": main()
