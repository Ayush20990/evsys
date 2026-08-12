"""Single-tool explicit vs implicit COMPOSIO_SEARCH_TOOLS evaluation.

Toolkits are randomly sampled (deterministically, via RANDOM_SEED) from
ALL_TOOLKITS on every run. Change NUM_TOOLKITS_TO_SAMPLE / RANDOM_SEED to
control how many toolkits get tested and which ones get picked.

Outputs:
  - query_cache.json                 cached Gemini-generated queries (unchanged)
  - search_eval_results.csv          per-query results, one row per query (unchanged)
  - full_run_dump.json               NEW: raw dump of everything tried this run
                                      (sampled tools, generated queries, every
                                      search request + full untruncated response)
  - summary_report.md / .html        NEW: aggregated numbers + 10-20 failure
                                      examples, in both markdown and html
"""
from __future__ import annotations
import csv, json, os, random, time, traceback
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

# Full pool of toolkits to sample from. A random subset is chosen each run
# (seeded, so re-running with the same RANDOM_SEED reproduces the same pick).
ALL_TOOLKITS = [
    "github", "googlesheets", "outlook", "notion", "pipedrive", "hubspot", "gmail",
    "googledrive", "instagram", "youtube", "salesforce", "metaads", "clickup", "trello",
    "google", "composio", "vercel", "one", "slack", "googlecalendar", "browser",
    "facebook", "gemini", "googledocs", "kommo", "linkedin", "clicksend", "googleads",
    "heygen", "zendesk", "quickbooks", "xero", "zoho", "airtable", "linear", "zep",
    "supabase", "bitbucket", "googletasks", "googleslides", "brevo", "cloudflare",
    "elevenlabs", "ticktick", "jira", "shopify", "todoist", "cal", "discordbot",
    "fathom", "fireflies", "datadog", "hunter", "attio", "telegram", "whatsapp",
    "discord", "metabase", "plain", "mem0", "tinyurl", "ahrefs", "firecrawl",
    "microsoft", "googlesuper",
]

NUM_TOOLKITS_TO_SAMPLE = 50
TOOLS_PER_TOOLKIT, RANDOM_SEED = 20, 12
SEARCH_TOP_K, GEMINI_RPM, COMPOSIO_CALL_DELAY_SEC = 6, 15, 0.5

OUTPUT_DIR = Path(__file__).resolve().parent / "single_tool_evaluation"
CACHE_PATH = OUTPUT_DIR / "query_cache.json"
RESULTS_CSV_PATH = OUTPUT_DIR / "search_eval_results.csv"
DUMP_JSON_PATH = OUTPUT_DIR / "full_run_dump.json"
SUMMARY_MD_PATH = OUTPUT_DIR / "summary_report.md"
SUMMARY_HTML_PATH = OUTPUT_DIR / "summary_report.html"

DEBUG_DUMP_FIRST_RESPONSE, RAW_RESPONSE_MAX_CHARS = True, 20000
USER_ID = "search-tool-eval-user"
MAX_FAILURE_EXAMPLES = 20
MIN_FAILURE_EXAMPLES = 10


class RateLimiter:
    def __init__(self, calls_per_minute: float): self.min_interval, self._last_call = 60.0 / calls_per_minute, 0.0
    def wait(self):
        remaining = self.min_interval - (time.monotonic() - self._last_call)
        if remaining > 0: time.sleep(remaining)
        self._last_call = time.monotonic()


def with_retry(fn, *args, max_retries=5, base_delay=2.0, retry_on=(Exception,),
               return_api_latency=False, **kwargs):
    """Retry a call and optionally return the successful-attempt duration.

    The optional duration surrounds only the successful function invocation;
    it deliberately excludes retry backoff and time spent in failed attempts.
    """
    last_err = None
    for attempt in range(max_retries):
        try:
            api_started = time.monotonic()
            result = fn(*args, **kwargs)
            api_latency = time.monotonic() - api_started
            return (result, api_latency) if return_api_latency else result
        except retry_on as error:
            last_err = error
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"  [retry] attempt {attempt + 1}/{max_retries} failed: {error!r} -> sleeping {delay:.1f}s")
            time.sleep(delay)
    raise last_err


@dataclass
class ToolInfo:
    slug: str
    toolkit: str
    description: str


def select_toolkits(pool: list[str], count: int) -> list[str]:
    """Randomly (but deterministically, via the caller's random.seed) pick toolkits."""
    picked = random.sample(pool, min(count, len(pool)))
    print(f"[toolkits] randomly selected {len(picked)}/{len(pool)}: {picked}")
    return picked


def fetch_tools(composio: Composio, toolkits: list[str], per_toolkit: int) -> list[ToolInfo]:
    out = []
    for toolkit in toolkits:
        infos = []
        for tool in composio.tools.get(user_id=USER_ID, toolkits=[toolkit]):
            function = tool["function"] if isinstance(tool, dict) else tool.function
            name = function["name"] if isinstance(function, dict) else function.name
            desc = (function.get("description", "") if isinstance(function, dict) else getattr(function, "description", "")) or ""
            infos.append(ToolInfo(name, toolkit, desc))
        infos = random.sample(infos, per_toolkit) if len(infos) > per_toolkit else infos
        print(f"[fetch] {toolkit}: sampled {len(infos)} tools"); out.extend(infos)
    return out


PROMPT_TEMPLATE = '''You are generating a test query for a tool-search evaluation.

Tool slug: {slug}
Toolkit/app: {toolkit}
Tool description: {description}

Write ONE short, natural request a real user would type to an AI assistant that would require calling exactly this tool. {style_instruction}

Rules:
- 5 to 30 words.
- Plain imperative or conversational style (e.g. "create a github issue for this bug").
- Do NOT mention the tool's slug or internal name.
- Output ONLY the query text, nothing else (no quotes, no preamble).
'''


def load_cache(): return json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
def save_cache(cache): CACHE_PATH.write_text(json.dumps(cache, indent=2))


def gemini_generate_query(client, limiter, tool, variant):
    style = f"Naturally mention the app/toolkit name ({tool.toolkit}) in the request." if variant == "explicit" else "Do NOT mention the app/toolkit name at all — describe only the action/intent."
    prompt = PROMPT_TEMPLATE.format(slug=tool.slug, toolkit=tool.toolkit, description=tool.description[:500], style_instruction=style)
    def call():
        limiter.wait(); text = (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip().strip('"').strip()
        if not text: raise ValueError("empty Gemini response")
        return text
    return with_retry(call, max_retries=5, base_delay=3.0)


def build_query_set(composio, gclient, tools):
    cache, limiter, rows = load_cache(), RateLimiter(GEMINI_RPM), []
    for index, tool in enumerate(tools):
        entry, changed = cache.get(tool.slug, {}), False
        for variant in ("explicit", "implicit"):
            if variant not in entry:
                print(f"[gemini] ({index + 1}/{len(tools)}) generating '{variant}' query for {tool.slug}")
                try: entry[variant] = gemini_generate_query(gclient, limiter, tool, variant)
                except Exception as error: print(f"  [warn] giving up on {tool.slug}/{variant}: {error!r}"); entry[variant] = None
                changed = True
        cache[tool.slug] = entry
        if changed: save_cache(cache)
        rows.extend({"slug": tool.slug, "toolkit": tool.toolkit, "variant": variant, "query": entry[variant]} for variant in ("explicit", "implicit") if entry.get(variant))
    return rows


def to_plain(obj: Any) -> Any:
    if hasattr(obj, "model_dump"): return obj.model_dump()
    if isinstance(obj, dict): return obj
    return vars(obj) if hasattr(obj, "__dict__") else obj


def extract_plan(response: Any) -> dict:
    top = to_plain(response); data = top.get("data", top) or {}; data = data if hasattr(data, "get") else {}
    results = data.get("results") or []; result = to_plain(results[0]) if results else {}; result = result if hasattr(result, "get") else {}
    primary = list(result.get("primary_tool_slugs") or []); related = [slug for slug in list(result.get("related_tool_slugs") or []) if slug not in primary]
    return {"primary": primary, "related": related, "use_case": result.get("use_case"), "plan_id": result.get("plan_id"), "recommended_plan_steps": list(result.get("recommended_plan_steps") or []), "known_pitfalls": list(result.get("known_pitfalls") or []), "no_results": not results, "raw_error": data.get("error") or top.get("error"), "raw": top}


def run_eval(session, query_rows):
    """Returns (csv_results, dump_entries). dump_entries carry the FULL,
    untruncated request/response for every call so nothing is lost for the
    full_run_dump.json artifact; csv_results carry the truncated version
    used for the CSV."""
    results, dump_entries, first_dump_shown = [], [], False
    for index, row in enumerate(query_rows):
        print(f"[search] ({index + 1}/{len(query_rows)}) [{row['variant']}] {row['slug']} <- \"{row['query']}\""); end_to_end_started, error, api_search_latency = time.monotonic(), None, None
        plan = {"primary": [], "related": [], "use_case": None, "plan_id": None, "recommended_plan_steps": [], "known_pitfalls": [], "no_results": True, "raw_error": None, "raw": None}
        request_payload = {"tool": "COMPOSIO_SEARCH_TOOLS", "arguments": {"query": row["query"]}}
        try:
            response, api_search_latency = with_retry(
                session.execute, "COMPOSIO_SEARCH_TOOLS",
                arguments={"query": row["query"]}, max_retries=4, base_delay=2.0,
                return_api_latency=True,
            )
            end_to_end_latency = time.monotonic() - end_to_end_started
            if DEBUG_DUMP_FIRST_RESPONSE and not first_dump_shown: print(json.dumps(to_plain(response), indent=2, default=str)[:3000]); first_dump_shown = True
            plan = extract_plan(response)
        except Exception as exc:
            end_to_end_latency = time.monotonic() - end_to_end_started
            error = repr(exc); traceback.print_exc()
        target, primary, related = row["slug"], plan["primary"], plan["related"]
        primary_hit, related_hit = target in primary, target in related
        final_error = error or plan["raw_error"]
        results.append({**row, "primary_hit": primary_hit, "related_hit": related_hit, "complete_miss": not primary_hit and not related_hit, "demotion": related_hit and not primary_hit, "primary_rank": primary.index(target) + 1 if primary_hit else None, "num_primary": len(primary), "num_related": len(related), "primary_slugs": ";".join(primary), "related_slugs": ";".join(related), "use_case": plan["use_case"], "plan_id": plan["plan_id"], "recommended_plan_steps": " | ".join(plan["recommended_plan_steps"]), "known_pitfalls": " | ".join(plan["known_pitfalls"]), "no_results_returned": plan["no_results"], "api_search_latency_sec": round(api_search_latency, 2) if api_search_latency is not None else None, "end_to_end_latency_sec": round(end_to_end_latency, 2), "error": final_error, "raw_response_json": json.dumps(plan["raw"], default=str)[:RAW_RESPONSE_MAX_CHARS] if plan["raw"] is not None else ""})
        dump_entries.append({
            "index": index, "slug": row["slug"], "toolkit": row["toolkit"], "variant": row["variant"],
            "query": row["query"], "request": request_payload, "raw_response": plan["raw"],
            "primary_hit": primary_hit, "related_hit": related_hit,
            "api_search_latency_sec": round(api_search_latency, 2) if api_search_latency is not None else None,
            "end_to_end_latency_sec": round(end_to_end_latency, 2), "error": final_error,
        })
        time.sleep(COMPOSIO_CALL_DELAY_SEC)
    return results, dump_entries


def write_csv(rows, path):
    if rows:
        with path.open("w", newline="", encoding="utf-8") as file: writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def write_dump(toolkits, tools, query_rows, dump_entries, path):
    """Full, mostly-untruncated dump of everything tried this run: which
    toolkits/tools were sampled, every generated query, and every search
    request + full raw response."""
    payload = {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "gemini_model": GEMINI_MODEL,
            "random_seed": RANDOM_SEED,
            "num_toolkits_sampled": len(toolkits),
            "toolkits_sampled": toolkits,
            "tools_per_toolkit": TOOLS_PER_TOOLKIT,
        },
        "tools_sampled": [asdict(t) for t in tools],
        "generated_queries": query_rows,
        "search_calls": dump_entries,
    }
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Full run dump written to: {path.resolve()}")


def summarize(rows):
    rate = lambda subset, field: sum(row[field] for row in subset) / len(subset) if subset else float("nan")
    print(f"Total queries: {len(rows)} | Primary hit: {rate(rows, 'primary_hit'):.1%} | Related hit: {rate(rows, 'related_hit'):.1%} | Complete miss: {rate(rows, 'complete_miss'):.1%}")
    for variant in ("explicit", "implicit"):
        subset = [row for row in rows if row["variant"] == variant]; print(f"{variant}: primary={rate(subset, 'primary_hit'):.1%}, related={rate(subset, 'related_hit'):.1%}, miss={rate(subset, 'complete_miss'):.1%} (n={len(subset)})")
    print(f"Full results written to: {RESULTS_CSV_PATH.resolve()}")


def build_report_data(rows, toolkits):
    """Aggregate everything the summary report (md + html) needs, so both
    renderers stay in sync off one source of truth."""
    rate = lambda subset, field: sum(row[field] for row in subset) / len(subset) if subset else 0.0
    successful = [row for row in rows if not row["error"]]
    api_latencies = [row["api_search_latency_sec"] for row in successful if row["api_search_latency_sec"] is not None]
    e2e_latencies = [row["end_to_end_latency_sec"] for row in successful]

    variant_table = []
    for variant in ("explicit", "implicit"):
        subset = [row for row in rows if row["variant"] == variant]
        variant_table.append({"variant": variant, "n": len(subset), "primary": rate(subset, "primary_hit"), "related": rate(subset, "related_hit"), "demoted": rate(subset, "demotion"), "miss": rate(subset, "complete_miss")})

    toolkit_table = []
    for toolkit in sorted({row["toolkit"] for row in rows}):
        subset = [row for row in rows if row["toolkit"] == toolkit]
        explicit = [row for row in subset if row["variant"] == "explicit"]
        implicit = [row for row in subset if row["variant"] == "implicit"]
        toolkit_table.append({"toolkit": toolkit, "explicit_primary": rate(explicit, "primary_hit"), "implicit_primary": rate(implicit, "primary_hit"), "n": len(subset)})

    misses = [row for row in rows if row["complete_miss"]]
    failures = [{"variant": row["variant"], "slug": row["slug"], "toolkit": row["toolkit"], "query": row["query"], "primary_slugs": row["primary_slugs"] or "(none)", "error": row["error"] or ""} for row in misses[:MAX_FAILURE_EXAMPLES]]

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "toolkits_tested": toolkits,
        "total": len(rows),
        "primary_hit_rate": rate(rows, "primary_hit"),
        "related_hit_rate": rate(rows, "related_hit"),
        "demotion_rate": rate(rows, "demotion"),
        "complete_miss_rate": rate(rows, "complete_miss"),
        "variant_table": variant_table,
        "toolkit_table": toolkit_table,
        "latency": {
            "avg_api": sum(api_latencies) / len(api_latencies) if api_latencies else None,
            "max_api": max(api_latencies) if api_latencies else None,
            "avg_e2e": sum(e2e_latencies) / len(e2e_latencies) if e2e_latencies else None,
            "max_e2e": max(e2e_latencies) if e2e_latencies else None,
        },
        "failures": failures,
        "total_misses": len(misses),
    }


def render_markdown_report(data: dict) -> str:
    pct = lambda x: f"{x:.1%}" if x is not None else "n/a"
    md = [
        "# Composio Search Single-Tool Evaluation Report\n",
        f"_Generated {data['generated_at_utc']}_\n",
        f"**Toolkits tested this run:** {', '.join(data['toolkits_tested'])}\n",
        "## Summary",
        f"- **Total queries:** {data['total']}",
        f"- **Primary hit rate:** {pct(data['primary_hit_rate'])}",
        f"- **Related hit rate:** {pct(data['related_hit_rate'])}",
        f"- **Demotion rate:** {pct(data['demotion_rate'])}",
        f"- **Complete miss rate:** {pct(data['complete_miss_rate'])}\n",
        "## Explicit vs. Implicit Queries",
        "| Variant | Queries | Primary hit | Related hit | Demoted | Complete miss |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in data["variant_table"]:
        md.append(f"| {row['variant']} | {row['n']} | {pct(row['primary'])} | {pct(row['related'])} | {pct(row['demoted'])} | {pct(row['miss'])} |")
    md.extend(["\n## Primary Hit Rate by Toolkit", "| Toolkit | Queries | Explicit | Implicit |", "|---|---:|---:|---:|"])
    for row in data["toolkit_table"]:
        md.append(f"| {row['toolkit']} | {row['n']} | {pct(row['explicit_primary'])} | {pct(row['implicit_primary'])} |")
    lat = data["latency"]
    if lat["avg_api"] is not None:
        md.extend([
            "\n## Latency",
            "API/Search latency is the successful API call only; end-to-end latency includes retry backoff and failed attempts.",
            "| Metric | API/Search (s) | End-to-end (s) |",
            "|---|---:|---:|",
            f"| Average | {lat['avg_api']:.2f} | {lat['avg_e2e']:.2f} |",
            f"| Maximum | {lat['max_api']:.2f} | {lat['max_e2e']:.2f} |",
        ])
    if data["failures"]:
        md.append(f"\n## Failure Examples ({len(data['failures'])} of {data['total_misses']} complete misses)")
        md.extend(["| Variant | Toolkit | Target tool | Query | Primary tools returned | Error |", "|---|---|---|---|---|---|"])
        for row in data["failures"]:
            query = row["query"].replace("|", "\\|")
            primary = row["primary_slugs"].replace("|", "\\|")
            error = row["error"].replace("|", "\\|")
            md.append(f"| {row['variant']} | {row['toolkit']} | `{row['slug']}` | {query} | `{primary}` | {error} |")
    else:
        md.append("\n## Failure Examples\nNo complete misses this run.")
    return "\n".join(md) + "\n"


def render_html_report(data: dict) -> str:
    pct = lambda x: f"{x:.1%}" if x is not None else "n/a"
    def table(headers, rows):
        head = "".join(f"<th>{h}</th>" for h in headers)
        body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in r) + "</tr>" for r in rows)
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

    variant_rows = [[row["variant"], row["n"], pct(row["primary"]), pct(row["related"]), pct(row["demoted"]), pct(row["miss"])] for row in data["variant_table"]]
    toolkit_rows = [[row["toolkit"], row["n"], pct(row["explicit_primary"]), pct(row["implicit_primary"])] for row in data["toolkit_table"]]
    lat = data["latency"]
    latency_html = ""
    if lat["avg_api"] is not None:
        latency_html = "<h2>Latency</h2><p>API/Search latency is the successful API call only; end-to-end latency includes retry backoff and failed attempts.</p>" + table(
            ["Metric", "API/Search (s)", "End-to-end (s)"],
            [["Average", f"{lat['avg_api']:.2f}", f"{lat['avg_e2e']:.2f}"], ["Maximum", f"{lat['max_api']:.2f}", f"{lat['max_e2e']:.2f}"]],
        )
    failures_html = "<p>No complete misses this run.</p>"
    if data["failures"]:
        failure_rows = [[row["variant"], row["toolkit"], f"<code>{row['slug']}</code>", row["query"], f"<code>{row['primary_slugs']}</code>", row["error"]] for row in data["failures"]]
        failures_html = f"<p>{len(data['failures'])} of {data['total_misses']} complete misses shown.</p>" + table(
            ["Variant", "Toolkit", "Target tool", "Query", "Primary tools returned", "Error"], failure_rows
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Composio Search Single-Tool Evaluation Report</title>
<style>
  body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 16px; color: #1a1a1a; }}
  h1, h2 {{ border-bottom: 1px solid #e0e0e0; padding-bottom: 6px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0 28px; font-size: 14px; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
  th {{ background: #f4f4f4; }}
  code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 3px; }}
  .stats {{ display: flex; gap: 24px; flex-wrap: wrap; margin: 16px 0 28px; }}
  .stat {{ background: #f8f8f8; border-radius: 8px; padding: 12px 18px; min-width: 140px; }}
  .stat .label {{ font-size: 12px; color: #666; }}
  .stat .value {{ font-size: 22px; font-weight: 600; }}
</style>
</head>
<body>
<h1>Composio Search Single-Tool Evaluation Report</h1>
<p><em>Generated {data['generated_at_utc']}</em></p>
<p><strong>Toolkits tested this run:</strong> {', '.join(data['toolkits_tested'])}</p>
<div class="stats">
  <div class="stat"><div class="label">Total queries</div><div class="value">{data['total']}</div></div>
  <div class="stat"><div class="label">Primary hit rate</div><div class="value">{pct(data['primary_hit_rate'])}</div></div>
  <div class="stat"><div class="label">Related hit rate</div><div class="value">{pct(data['related_hit_rate'])}</div></div>
  <div class="stat"><div class="label">Demotion rate</div><div class="value">{pct(data['demotion_rate'])}</div></div>
  <div class="stat"><div class="label">Complete miss rate</div><div class="value">{pct(data['complete_miss_rate'])}</div></div>
</div>
<h2>Explicit vs. Implicit Queries</h2>
{table(["Variant", "Queries", "Primary hit", "Related hit", "Demoted", "Complete miss"], variant_rows)}
<h2>Primary Hit Rate by Toolkit</h2>
{table(["Toolkit", "Queries", "Explicit", "Implicit"], toolkit_rows)}
{latency_html}
<h2>Failure Examples</h2>
{failures_html}
</body>
</html>
"""


def write_summary_reports(rows, toolkits):
    data = build_report_data(rows, toolkits)
    SUMMARY_MD_PATH.write_text(render_markdown_report(data), encoding="utf-8")
    SUMMARY_HTML_PATH.write_text(render_html_report(data), encoding="utf-8")
    print(f"Summary report written to: {SUMMARY_MD_PATH.resolve()} and {SUMMARY_HTML_PATH.resolve()}")
    if data["total_misses"] < MIN_FAILURE_EXAMPLES:
        print(f"[note] only {data['total_misses']} complete misses this run (fewer than {MIN_FAILURE_EXAMPLES}); "
              f"widen NUM_TOOLKITS_TO_SAMPLE or TOOLS_PER_TOOLKIT if you need more failure examples.")


def main():
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY: raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(RANDOM_SEED)
    toolkits = select_toolkits(ALL_TOOLKITS, NUM_TOOLKITS_TO_SAMPLE)
    composio, gclient = Composio(api_key=COMPOSIO_API_KEY), genai.Client(api_key=GEMINI_API_KEY)
    tools = fetch_tools(composio, toolkits, TOOLS_PER_TOOLKIT)
    rows = build_query_set(composio, gclient, tools)
    evaluated, dump_entries = run_eval(composio.create(user_id=USER_ID), rows)
    write_csv(evaluated, RESULTS_CSV_PATH)
    write_dump(toolkits, tools, rows, dump_entries, DUMP_JSON_PATH)
    summarize(evaluated)
    write_summary_reports(evaluated, toolkits)


if __name__ == "__main__": main()
