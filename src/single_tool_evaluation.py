"""Single-tool explicit vs implicit COMPOSIO_SEARCH_TOOLS evaluation."""
from __future__ import annotations
import csv, json, os, random, time, traceback
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from composio import Composio
from dotenv import load_dotenv
from google import genai

load_dotenv()
COMPOSIO_API_KEY = os.environ.get("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash-lite"
TOOLKITS = ["github", "gmail", "slack"]
TOOLS_PER_TOOLKIT, RANDOM_SEED = 15, 12
SEARCH_TOP_K, GEMINI_RPM, COMPOSIO_CALL_DELAY_SEC = 6, 20, 0.5
CACHE_PATH, RESULTS_CSV_PATH = Path("query_cache.json"), Path("search_eval_results.csv")
DEBUG_DUMP_FIRST_RESPONSE, RAW_RESPONSE_MAX_CHARS = True, 20000
USER_ID = "search-tool-eval-user"

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

def fetch_tools(composio: Composio, toolkits: list[str], per_toolkit: int) -> list[ToolInfo]:
    random.seed(RANDOM_SEED); out = []
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
- 5 to 14 words.
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
    results, first_dump_shown = [], False
    for index, row in enumerate(query_rows):
        print(f"[search] ({index + 1}/{len(query_rows)}) [{row['variant']}] {row['slug']} <- \"{row['query']}\""); end_to_end_started, error, api_search_latency = time.monotonic(), None, None
        plan = {"primary": [], "related": [], "use_case": None, "plan_id": None, "recommended_plan_steps": [], "known_pitfalls": [], "no_results": True, "raw_error": None, "raw": None}
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
        results.append({**row, "primary_hit": primary_hit, "related_hit": related_hit, "complete_miss": not primary_hit and not related_hit, "demotion": related_hit and not primary_hit, "primary_rank": primary.index(target) + 1 if primary_hit else None, "num_primary": len(primary), "num_related": len(related), "primary_slugs": ";".join(primary), "related_slugs": ";".join(related), "use_case": plan["use_case"], "plan_id": plan["plan_id"], "recommended_plan_steps": " | ".join(plan["recommended_plan_steps"]), "known_pitfalls": " | ".join(plan["known_pitfalls"]), "no_results_returned": plan["no_results"], "api_search_latency_sec": round(api_search_latency, 2) if api_search_latency is not None else None, "end_to_end_latency_sec": round(end_to_end_latency, 2), "error": error or plan["raw_error"], "raw_response_json": json.dumps(plan["raw"], default=str)[:RAW_RESPONSE_MAX_CHARS] if plan["raw"] is not None else ""})
        time.sleep(COMPOSIO_CALL_DELAY_SEC)
    return results

def write_csv(rows, path):
    if rows:
        with path.open("w", newline="", encoding="utf-8") as file: writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
def summarize(rows):
    rate = lambda subset, field: sum(row[field] for row in subset) / len(subset) if subset else float("nan")
    print(f"Total queries: {len(rows)} | Primary hit: {rate(rows, 'primary_hit'):.1%} | Related hit: {rate(rows, 'related_hit'):.1%} | Complete miss: {rate(rows, 'complete_miss'):.1%}")
    for variant in ("explicit", "implicit"):
        subset = [row for row in rows if row["variant"] == variant]; print(f"{variant}: primary={rate(subset, 'primary_hit'):.1%}, related={rate(subset, 'related_hit'):.1%}, miss={rate(subset, 'complete_miss'):.1%} (n={len(subset)})")
    print(f"Full results written to: {RESULTS_CSV_PATH.resolve()}")

def main():
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY: raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    composio, gclient = Composio(api_key=COMPOSIO_API_KEY), genai.Client(api_key=GEMINI_API_KEY)
    tools = fetch_tools(composio, TOOLKITS, TOOLS_PER_TOOLKIT); rows = build_query_set(composio, gclient, tools); evaluated = run_eval(composio.create(user_id=USER_ID), rows)
    write_csv(evaluated, RESULTS_CSV_PATH); summarize(evaluated)
if __name__ == "__main__": main()
