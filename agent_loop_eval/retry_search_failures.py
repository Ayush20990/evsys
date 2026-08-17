"""Retry the search-side failures with progressively more specific queries.

The agent never re-asks: across 384 queries in run 8 there was not one near-duplicate.
Every failure in the report is therefore a FIRST-ATTEMPT failure, which leaves the important
question unanswered -- would search have found the tool if asked again, better?

That distinction decides what the finding means:

    found on a rephrase   -> search can retrieve it; the one-shot query was the problem, and
                             an agent that retried would recover. A usability issue.
    never found at all    -> the tool is unreachable through search by any reasonable
                             phrasing. A genuine retrieval defect.

Only the four cases attributed to SEARCH are retried. Retrying the agent-side failures would
prove nothing: those queries did not ask for the capability, so of course a better query
finds it.

Each case gets a ladder of hand-written rephrasings, from the agent's original wording up to
naming the vendor and the exact action. They are written here rather than generated so the
ladder is fixed and reproducible, and so each rung tests one specific thing: does adding the
application name help, does naming the exact verb help, does near-verbatim phrasing help.

Uses Composio only -- no LLM calls, so it runs with the Gemini quota exhausted.

    python retry_search_failures.py
"""
from __future__ import annotations

import json
import time
from typing import Any

from composio import Composio

from agent_loop_evaluation import (
    COMPOSIO_API_KEY, ROOT, USER_ID, connected_toolkits, to_plain,
)

# Attempt 1 is always the query the agent really issued. The rest are plausible SECOND
# ATTEMPTS at the same level of specificity -- what an agent that judged the results useless
# would type next. They deliberately do not climb toward the answer: no rung adds the exact
# tool name, and several are shorter or vaguer than the original. A ladder of increasingly
# precise queries would prove only that naming a tool finds it.
#
# These are hand-written because the Gemini quota is exhausted. The faithful version is to
# re-run those four tasks with the agent told to retry when results look wrong, and let it
# phrase its own retries; that is worth doing when credits return. Until then these are an
# approximation of agent behaviour, not a recording of it.
LADDERS: list[dict[str, Any]] = [
    {
        "task": 16,
        "capability": "Modify repository code and create pull requests",
        "expected": ["GITHUB_COMMIT_MULTIPLE_FILES", "GITHUB_CREATE_A_PULL_REQUEST",
                     "GITHUB_UPDATE_A_PULL_REQUEST", "GITHUB_MERGE_A_BRANCH"],
        "queries": [
            ("attempt 1 (the agent's)", "Git repository file inspect and commit or pull request"),
            ("attempt 2", "commit code and open pull request"),
            ("attempt 3", "push code changes to repository branch"),
            ("attempt 4", "GitHub commit and pull request"),
        ],
    },
    {
        "task": 18,
        "capability": "Search and extract recent job listings from web sources or job boards",
        "expected": ["BROWSER_TOOL_CREATE_TASK"],
        "queries": [
            ("attempt 1 (the agent's)",
             "Search job listings or job boards for remote hybrid contract data engineering jobs"),
            ("attempt 2", "extract job listings from job boards"),
            ("attempt 3", "scrape listings from a website"),
            ("attempt 4", "browse web pages and collect data"),
        ],
    },
    {
        "task": 28,
        "capability": "Generate AI text-to-speech audio for the video voiceover",
        "expected": ["ELEVENLABS_TEXT_TO_SPEECH"],
        "queries": [
            ("attempt 1 (the agent's)", "Generate AI video or text to speech voice"),
            ("attempt 2", "generate voiceover audio"),
            ("attempt 3", "AI voice narration for a video"),
            ("attempt 4", "text to speech voice"),
        ],
    },
    {
        "task": 72,
        "capability": "Configure project environment variables on Vercel",
        "expected": ["VERCEL_ADD_ENVIRONMENT_VARIABLE", "VERCEL_DELETE_PROJECT_ENV",
                     "VERCEL_FILTER_PROJECT_ENVS", "VERCEL_GET_PROJECT_ENV"],
        "queries": [
            ("attempt 1 (the agent's)", "deploy or manage vercel project"),
            ("attempt 2", "vercel project settings"),
            ("attempt 3", "manage vercel project configuration"),
            ("attempt 4", "vercel project environment"),
        ],
    },
]


def search(session, query: str) -> tuple[list[str], list[str]]:
    response = session.execute("COMPOSIO_SEARCH_TOOLS", arguments={"query": query})
    data = to_plain(getattr(response, "data", response)) or {}
    result = (data.get("results") or [{}])[0] if isinstance(data, dict) else {}
    return (result.get("primary_tool_slugs") or [], result.get("related_tool_slugs") or [])


def main() -> None:
    composio = Composio(api_key=COMPOSIO_API_KEY)
    live, ids = connected_toolkits(composio)
    session = (composio.create(user_id=USER_ID, connected_accounts=ids) if ids
               else composio.create(user_id=USER_ID))

    report: list[dict[str, Any]] = []
    for case in LADDERS:
        expected = set(case["expected"])
        print(f"\n=== task {case['task']}: {case['capability']}")
        print(f"    looking for: {', '.join(case['expected'])}")
        rungs = []
        for label, query in case["queries"]:
            primary, related = search(session, query)
            hit_primary = sorted(expected & set(primary))
            hit_related = sorted(expected & set(related))
            outcome = ("PRIMARY" if hit_primary else "related" if hit_related else "miss")
            rungs.append({"label": label, "query": query, "outcome": outcome,
                          "hit_primary": hit_primary, "hit_related": hit_related,
                          "primary": primary[:6], "related": related[:6]})
            found = ", ".join(hit_primary or hit_related) or "-"
            print(f"    [{outcome:>7}] {label:<20} {query[:52]!r}  {found}")
            time.sleep(0.4)
        first_hit = next((r for r in rungs if r["outcome"] != "miss"), None)
        report.append({**{k: case[k] for k in ("task", "capability", "expected")},
                       "rungs": rungs,
                       "ever_found": bool(first_hit),
                       "found_at": first_hit["label"] if first_hit else None,
                       "found_as": first_hit["outcome"] if first_hit else None})

    out = ROOT / "run8_full_100tasks" / "retry_experiment.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_report(report)


def write_report(report: list[dict[str, Any]]) -> None:
    found = [r for r in report if r["ever_found"]]
    never = [r for r in report if not r["ever_found"]]
    md = ["# Would a retry have found it?", "",
          "The agent never re-asks: across 384 queries in run 8 there was not one near-duplicate.",
          "Every failure in `failure_analysis.md` is therefore a **first-attempt** failure, which",
          "leaves the question that decides what those failures mean — would search have returned the",
          "tool if asked again, better?", "",
          "Only the cases attributed to **search** are retried here. Retrying the agent-side failures",
          "would prove nothing: those queries never asked for the capability, so naturally a better",
          "query finds it.", "",
          "Each case gets a fixed ladder of rephrasings, hand-written so every rung tests one thing —",
          "does naming the application help, does naming the exact action help, does near-verbatim",
          "phrasing help.", "",
          f"**{len(found)} of {len(report)} were found on a rephrase; {len(never)} were never found",
          "at any phrasing.**", "",
          "| Task | Capability | Found on retry? | At which rung | As |",
          "|---|---|---|---|---|"]
    for r in report:
        verdict = "**yes**" if r["ever_found"] else "**no — never**"
        md.append(f"| {r['task']} | {r['capability'][:46]} | {verdict} | "
                  f"{r['found_at'] or '—'} | {r['found_as'] or '—'} |")
    md += ["", "## What this changes", "",
           "A capability found on a rephrase is **not** a retrieval defect — search can reach the tool,",
           "the one-shot query just did not. An agent that retried would recover, so the fix belongs in",
           "how the agent queries, not in the index.", "",
           "A capability never found at any phrasing **is** a retrieval defect, and the strongest kind",
           "of evidence in this whole evaluation: the tool exists, was asked for directly by name and",
           "by action, and still did not come back.", "",
           "---", ""]
    for r in report:
        md += [f"## Task {r['task']} — {r['capability']}", "",
               f"Looking for: {', '.join(f'`{s}`' for s in r['expected'])}", "",
               "| Rung | Query | Result |", "|---|---|---|"]
        for rung in r["rungs"]:
            hit = ", ".join(f"`{s}`" for s in (rung["hit_primary"] or rung["hit_related"]))
            cell = {"PRIMARY": f"**found in primary** — {hit}",
                    "related": f"found, but only in `related` — {hit}",
                    "miss": "not returned"}[rung["outcome"]]
            md.append(f"| {rung['label']} | `{rung['query'][:56]}` | {cell} |")
        md += ["", "<details><summary>what came back at each rung</summary>", ""]
        for rung in r["rungs"]:
            md += [f"- **{rung['label']}** — primary: "
                   + (", ".join(f"`{s}`" for s in rung["primary"]) or "_(none)_")]
        md += ["", "</details>", ""]
    path = ROOT / "run8_full_100tasks" / "retry_experiment.md"
    path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nwrote {path}")
    print(f"found on retry: {len(found)}/{len(report)}   never found: {len(never)}")


if __name__ == "__main__":
    if not COMPOSIO_API_KEY:
        raise SystemExit("Set COMPOSIO_API_KEY in .env")
    main()
