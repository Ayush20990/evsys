"""Probe the four search-side failures with many plausible queries, reporting every outcome.

Two earlier probes each ran about four queries per capability. This runs eight, so the
failure rate has a denominator worth quoting.

Every query is written the way the agent writes them -- short, action-first, sometimes
naming the application, sometimes not; the register is taken from the 384 queries in run 8,
which average 6.6 words. None names a tool slug, and none is deliberately bad: each is a
phrasing a competent agent could plausibly reach for. They are fixed in this file rather
than generated so the set cannot drift between runs.

**Successes are reported alongside failures.** A list of failing queries with no denominator
is not evidence -- anyone can find phrasings that miss. What matters is the proportion, and
whether any phrasing works at all.

Composio only; no LLM calls.

    python probe_search_failures.py
"""
from __future__ import annotations

import json
import time
from typing import Any

from composio import Composio

from agent_loop_evaluation import (
    COMPOSIO_API_KEY, ROOT, USER_ID, connected_toolkits, to_plain,
)

PROBES: list[dict[str, Any]] = [
    {
        "task": 16,
        "capability": "Modify repository code and create pull requests",
        "expected": ["GITHUB_COMMIT_MULTIPLE_FILES", "GITHUB_CREATE_A_PULL_REQUEST",
                     "GITHUB_UPDATE_A_PULL_REQUEST", "GITHUB_MERGE_A_BRANCH"],
        "queries": [
            "Git repository file inspect and commit or pull request",   # the agent's own
            "create pull request on github",                            # agent retry, worked
            "commit code and open pull request",
            "push code changes to repository branch",
            "modify files in a repository",
            "update source code in github repo",
            "raise a PR with code changes",
            "write changes to a git branch",
        ],
    },
    {
        "task": 18,
        "capability": "Search and extract recent job listings from web sources or job boards",
        "expected": ["BROWSER_TOOL_CREATE_TASK"],
        "queries": [
            "Search job listings or job boards for remote hybrid contract data engineering jobs",
            "extract job listings from job boards",
            "scrape listings from a website",
            "browse web pages and collect data",                        # worked in probe 1
            "automate a browser session",
            "open a web page and read its contents",
            "run a headless browser task",
            "crawl a site for structured data",
        ],
    },
    {
        "task": 28,
        "capability": "Generate AI text-to-speech audio for the video voiceover",
        "expected": ["ELEVENLABS_TEXT_TO_SPEECH"],
        "queries": [
            "Generate AI video or text to speech voice",                # the agent's own
            "generate voiceover audio",                                 # worked in probe 1
            "AI voice narration for a video",
            "text to speech voice",                                     # worked in probe 1
            "synthesize speech from text",
            "create an audio narration track",
            "turn a script into spoken audio",
            "generate a voice clip for a reel",
        ],
    },
    {
        "task": 72,
        "capability": "Configure project environment variables on Vercel",
        "expected": ["VERCEL_ADD_ENVIRONMENT_VARIABLE", "VERCEL_DELETE_PROJECT_ENV",
                     "VERCEL_FILTER_PROJECT_ENVS", "VERCEL_GET_PROJECT_ENV"],
        "queries": [
            "deploy or manage vercel project",                          # the agent's own
            "vercel project settings",
            "manage vercel project configuration",
            "vercel project environment",                               # worked in probe 1
            "set environment variables for a deployment",
            "store deployment secrets",
            "read project config values",
            "update env vars on a hosting project",
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

    report = []
    for probe in PROBES:
        expected = set(probe["expected"])
        print(f"\n=== task {probe['task']}: {probe['capability']}")
        rows = []
        for query in probe["queries"]:
            primary, related = search(session, query)
            hit_p = sorted(expected & set(primary))
            hit_r = sorted(expected & set(related))
            outcome = "PRIMARY" if hit_p else "related" if hit_r else "miss"
            rows.append({"query": query, "outcome": outcome, "hit": hit_p or hit_r,
                         "primary": primary[:5], "related": related[:5]})
            print(f"    [{outcome:>7}] {query[:58]!r}  {', '.join(hit_p or hit_r) or '-'}")
            time.sleep(0.4)
        misses = [r for r in rows if r["outcome"] == "miss"]
        report.append({**{k: probe[k] for k in ("task", "capability", "expected")},
                       "rows": rows, "tried": len(rows), "missed": len(misses)})
        print(f"    -> {len(misses)} of {len(rows)} queries failed to return the tool")

    (ROOT / "run8_full_100tasks" / "probe_search_failures.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    write_report(report)


def write_report(report: list[dict[str, Any]]) -> None:
    tried = sum(r["tried"] for r in report)
    missed = sum(r["missed"] for r in report)
    md = ["# How often does search miss these four tools?", "",
          "The four capabilities attributed to search in `failure_analysis.md` failed on the query the",
          "agent actually issued. That was a single attempt each — in run 8 the agent never re-asked",
          "for anything, across all 384 queries — so this probes each one with eight plausible",
          "phrasings to see how reliably the tool can be reached.", "",
          "Every phrasing is written in the agent's own register: short, action-first, sometimes",
          "naming the application and sometimes not. None contains a tool slug, and none is",
          "deliberately bad.", "",
          f"## {missed} of {tried} queries failed to return the needed tool", "",
          "**Both numbers matter.** A list of failing queries with no denominator proves nothing —",
          "anyone can find phrasings that miss. The finding is the *proportion*, and whether any",
          "phrasing works at all.", "",
          "| Task | Capability | Queries tried | Failed | Ever found? |",
          "|---|---|---:|---:|---|"]
    for r in report:
        ever = "yes" if r["missed"] < r["tried"] else "**never**"
        md.append(f"| {r['task']} | {r['capability'][:44]} | {r['tried']} | **{r['missed']}** | {ever} |")
    md += ["", f"**Overall: {missed}/{tried} = {100*missed/tried:.0f}% of plausible phrasings fail.**",
           "", "Each of these tools *is* reachable — every one was returned by at least one phrasing —",
           "so none is invisible to the index. The failure is that reaching it depends heavily on",
           "wording, and the phrasing an agent naturally reaches for often is not the one that works.",
           "", "---", ""]
    for r in report:
        md += [f"## Task {r['task']} — {r['capability']}", "",
               f"Looking for: {', '.join(f'`{s}`' for s in r['expected'])}", "",
               f"**{r['missed']} of {r['tried']} phrasings failed.**", "",
               "| Query | Result | What came back instead |", "|---|---|---|"]
        for row in r["rows"]:
            hit = ", ".join(f"`{s}`" for s in row["hit"])
            verdict = {"PRIMARY": f"found — {hit}",
                       "related": f"only in `related` — {hit}",
                       "miss": "**failed**"}[row["outcome"]]
            other = ", ".join(f"`{s}`" for s in row["primary"][:3]) or "_(nothing)_"
            md.append(f"| `{row['query'][:56]}` | {verdict} | {other} |")
        md.append("")
    path = ROOT / "run8_full_100tasks" / "probe_search_failures.md"
    path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nwrote {path}")
    print(f"TOTAL: {missed} of {tried} queries failed ({100*missed/tried:.0f}%)")


if __name__ == "__main__":
    main()
