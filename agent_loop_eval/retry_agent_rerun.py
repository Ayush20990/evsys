"""Re-run the search-side failures with the agent allowed to retry, in its own words.

`retry_search_failures.py` answered "could search find these tools at all" using rephrasings
written by hand. This answers the sharper question: would THE AGENT have found them, given
permission to try again?

The difference matters. Hand-written retries prove the tool is reachable by someone who
already knows the answer. Agent-written retries prove whether an ordinary second attempt --
phrased by a model that does not know what it is looking for -- recovers. Only the second
tells you whether a production agent would have got there.

Only the four tasks whose failures were attributed to SEARCH are re-run. The agent-side
failures need no experiment: those queries never asked for the capability.

The only change is the prompt. The agent is told to judge whether the results actually
contain a tool for the step, and to search again in different words if not, up to a few
times. Everything else -- tools, mocking, connections, model -- is identical to run 8, so any
difference in outcome is attributable to retrying.

    python retry_agent_rerun.py
"""
from __future__ import annotations

import json
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai

import agent_loop_evaluation as loop
from agent_loop_evaluation import (
    COMPOSIO_API_KEY, GEMINI_API_KEY, GEMINI_RPM, ROOT, USER_ID,
    RateLimiter, ToolMetadata, connected_toolkits, parse_use_cases, save_json,
)

# The capabilities attributed to search in failure_analysis.md, and what would have satisfied
# each. Kept explicit so the check is against the same targets the analysis used.
TARGETS: dict[int, dict[str, Any]] = {
    16: {"capability": "Modify repository code and create pull requests",
         "expected": ["GITHUB_COMMIT_MULTIPLE_FILES", "GITHUB_CREATE_A_PULL_REQUEST",
                      "GITHUB_UPDATE_A_PULL_REQUEST", "GITHUB_MERGE_A_BRANCH"]},
    18: {"capability": "Search and extract recent job listings from web sources or job boards",
         "expected": ["BROWSER_TOOL_CREATE_TASK"]},
    28: {"capability": "Generate AI text-to-speech audio for the video voiceover",
         "expected": ["ELEVENLABS_TEXT_TO_SPEECH"]},
    72: {"capability": "Configure project environment variables on Vercel",
         "expected": ["VERCEL_ADD_ENVIRONMENT_VARIABLE", "VERCEL_DELETE_PROJECT_ENV",
                      "VERCEL_FILTER_PROJECT_ENVS", "VERCEL_GET_PROJECT_ENV"]},
}

RETRY_CLAUSE = """
- After each search, check whether the results actually contain a tool that performs the step
  you are on. If none of them does, say so and SEARCH AGAIN for that same step using different
  words -- a different phrasing, a different way of describing the action, or naming the
  application. Give a step up to three searches before moving on. Do not execute a tool that
  does not do what the step needs just because it is the closest result."""


def main() -> None:
    load_dotenv(override=True)
    composio = Composio(api_key=COMPOSIO_API_KEY)
    client = genai.Client(api_key=GEMINI_API_KEY)
    metadata = ToolMetadata(composio)
    limiter = RateLimiter(GEMINI_RPM)
    live, ids = connected_toolkits(composio)
    session = (composio.create(user_id=USER_ID, connected_accounts=ids) if ids
               else composio.create(user_id=USER_ID))

    # The single change under test: permission to retry, in the agent's own words.
    loop.SYSTEM_PROMPT = loop.SYSTEM_PROMPT.replace(
        "- Work through the whole task, including any verification the task asks for.",
        RETRY_CLAUSE + "\n- Work through the whole task, including any verification the task asks for.")

    cases = {c.identifier: c for c in parse_use_cases(loop.USE_CASES_FILE)}
    report = []
    for task_id, target in TARGETS.items():
        case = cases[task_id]
        print(f"\n=== task {task_id}: {target['capability']}")
        print(f"    looking for: {', '.join(target['expected'])}")
        trace = loop.run_task(client, session, metadata, limiter, case, live)
        expected = set(target["expected"])
        attempts = []
        for query in trace.queries:
            primary = set(query.get("primary_tool_slugs") or [])
            related = set(query.get("related_tool_slugs") or [])
            hit_p, hit_r = sorted(expected & primary), sorted(expected & related)
            attempts.append({"query": query["query"], "intent": query.get("intent", ""),
                             "outcome": "PRIMARY" if hit_p else "related" if hit_r else "miss",
                             "hit": hit_p or hit_r,
                             "primary": (query.get("primary_tool_slugs") or [])[:5]})
        found = next((a for a in attempts if a["outcome"] != "miss"), None)
        # Compare against run 8, where the agent had no permission to retry.
        before = json.loads((ROOT / "run8_full_100tasks" / f"task-{task_id:03d}.json")
                            .read_text(encoding="utf-8"))
        report.append({
            "task": task_id, "capability": target["capability"], "expected": target["expected"],
            "queries_before": len(before["queries"]), "queries_after": len(attempts),
            "attempts": attempts, "found": bool(found),
            "found_on_attempt": attempts.index(found) + 1 if found else None,
            "found_query": found["query"] if found else None,
            "found_as": found["outcome"] if found else None,
        })
        for index, attempt in enumerate(attempts, 1):
            hit = ", ".join(attempt["hit"]) or "-"
            print(f"    [{attempt['outcome']:>7}] {index}. {attempt['query'][:56]!r}  {hit}")
        print(f"    -> {'FOUND on attempt ' + str(report[-1]['found_on_attempt']) if found else 'never found'}")

    save_json(ROOT / "run8_full_100tasks" / "retry_agent_rerun.json", report)
    write_report(report)


def write_report(report: list[dict[str, Any]]) -> None:
    found = [r for r in report if r["found"]]
    md = ["# Would the agent have found it, if allowed to retry?", "",
          "In run 8 the agent never re-asked for a capability once, across 384 queries: mocked",
          "execution succeeds on any well-formed call, so nothing ever told it a result was wrong.",
          "Every failure in `failure_analysis.md` is therefore a first-attempt failure.", "",
          "This re-runs the four tasks whose failures were attributed to **search**, changing one",
          "thing: the agent is told to check whether the results actually contain a tool for the step,",
          "and to search again in different words if not — up to three tries. It phrases its own",
          "retries. Tools, mocking, connections and model are otherwise identical to run 8.", "",
          f"**{len(found)} of {len(report)} were found once the agent could retry.**", "",
          "| Task | Capability | Queries before → after | Found? | On attempt |",
          "|---|---|---|---|---|"]
    for r in report:
        verdict = f"**yes** (as `{r['found_as']}`)" if r["found"] else "**no**"
        md.append(f"| {r['task']} | {r['capability'][:44]} | {r['queries_before']} → "
                  f"{r['queries_after']} | {verdict} | {r['found_on_attempt'] or '—'} |")
    md += ["", "## What this means", "",
           "A capability the agent recovers on its own second or third attempt is not a retrieval",
           "defect. Search can reach the tool; the agent simply accepted a bad first answer because",
           "nothing told it otherwise. The fix belongs in the agent — notice a poor result and try",
           "again — not in the index.", "",
           "A capability still not found after the agent has genuinely tried again, in its own words,",
           "is the strongest retrieval evidence available here.", "",
           "**Caveat.** These are single runs at temperature 0.4, so the exact wording of each retry",
           "is not reproducible; a rerun would phrase things differently and could land differently.",
           "Read the pattern, not the individual query.", "", "---", ""]
    for r in report:
        md += [f"## Task {r['task']} — {r['capability']}", "",
               f"Looking for: {', '.join(f'`{s}`' for s in r['expected'])}", "",
               "| # | Query the agent chose | Result |", "|---|---|---|"]
        for index, attempt in enumerate(r["attempts"], 1):
            hit = ", ".join(f"`{s}`" for s in attempt["hit"])
            cell = {"PRIMARY": f"**found in primary** — {hit}",
                    "related": f"found, only in `related` — {hit}",
                    "miss": "not returned"}[attempt["outcome"]]
            md.append(f"| {index} | `{attempt['query'][:58]}` | {cell} |")
        md.append("")
    path = ROOT / "run8_full_100tasks" / "retry_agent_rerun.md"
    path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
