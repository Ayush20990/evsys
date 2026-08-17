"""Probe each search-side failure with ~20 on-target phrasings, to find four defensible ones.

The earlier probe tried eight phrasings per capability and turned up only one failure for
task 16 and three for task 28 -- not enough to characterise those capabilities. This widens
the set to about twenty each.

Every query here has to pass three tests, or it is not evidence:

  1. It asks for THIS capability. Nothing borrowed from another step of the task; the earlier
     draft made that mistake and produced "Google Analytics report" as a commit/pull-request
     failure, which would collapse the moment anyone read it.
  2. It is a phrasing an agent could plausibly reach for -- short, action-first, describing
     the job rather than the tool. Nothing contrived to fail.
  3. It never names a tool slug. Naming the tool tests nothing.

Successes are recorded too, and the denominator is reported alongside every failure count.
Twenty queries producing four failures is a 20% failure rate, and saying so is what makes
those four defensible rather than selected.

Composio only, no LLM calls.

    python probe_wide.py
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
            "commit code and open pull request",
            "push code changes to repository branch",
            "GitHub commit and pull request",
            "create pull request on github",
            "modify files in a repository",
            "update source code in github repo",
            "raise a PR with code changes",
            "write changes to a git branch",
            "apply code changes to a repository",
            "save edited files back to the repo",
            "submit code changes for review",
            "check in code to version control",
            "upload changed files to a repository",
            "propose changes to a branch",
            "publish code changes to a repo",
            "record file edits in version control",
            "add files to a repository and request a merge",
            "send a code change upstream",
            "merge an approved branch",
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
            "browse web pages and collect data",
            "automate a browser session",
            "open a web page and read its contents",
            "run a headless browser task",
            "crawl a site for structured data",
            "visit a site and pull out listings",
            "navigate a website and extract fields",
            "read job postings from a careers page",
            "gather postings from an external site",
            "fetch listings from a public web page",
            "collect job adverts from the web",
            "drive a browser to gather results",
            "extract structured records from a page",
            "pull job data off a job board",
            "load a page and parse its listings",
            "harvest listings from web sources",
            "operate a browser to read a site",
        ],
    },
    {
        "task": 28,
        "capability": "Generate AI text-to-speech audio for the video voiceover",
        "expected": ["ELEVENLABS_TEXT_TO_SPEECH"],
        "queries": [
            "Generate AI video or text to speech voice",                # the agent's own
            "generate voiceover audio",
            "AI voice narration for a video",
            "text to speech voice",
            "synthesize speech from text",
            "create an audio narration track",
            "turn a script into spoken audio",
            "generate a voice clip for a reel",
            "make audio from written text",
            "read a script aloud with an AI voice",
            "produce spoken narration for a clip",
            "voice synthesis for a video",
            "generate a speech audio file",
            "add a voice track to a video",
            "convert a caption into audio",
            "create spoken word audio",
            "narrate text with a synthetic voice",
            "build an audio voiceover",
            "render text as speech",
            "get an AI to speak a script",
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
            "vercel project environment",
            "set environment variables for a deployment",
            "store deployment secrets",
            "read project config values",
            "update env vars on a hosting project",
            "configure build environment for a project",
            "add a secret to a deployment project",
            "list configuration values for a project",
            "change project settings on the host",
            "manage secrets for a web project",
            "set a config variable on the deployment platform",
            "retrieve environment configuration",
            "edit deployment environment values",
            "remove an environment variable from a project",
            "view project environment settings",
            "define build-time variables",
            "apply configuration to a hosted project",
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
            if outcome == "miss":
                print(f"    [FAIL] {query[:60]!r} -> {', '.join(primary[:3]) or '(nothing)'}")
            time.sleep(0.35)
        misses = [r for r in rows if r["outcome"] == "miss"]
        report.append({**{k: probe[k] for k in ("task", "capability", "expected")},
                       "rows": rows, "tried": len(rows), "missed": len(misses)})
        print(f"    -> {len(misses)} of {len(rows)} on-target phrasings failed")

    (ROOT / "run8_full_100tasks" / "probe_wide.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    total = sum(r["tried"] for r in report)
    failed = sum(r["missed"] for r in report)
    print(f"\nTOTAL: {failed} of {total} on-target queries failed ({100*failed/total:.0f}%)")
    for r in report:
        print(f"  task {r['task']}: {r['missed']} failures available")


if __name__ == "__main__":
    main()
