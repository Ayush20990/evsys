"""Attribute every failure in a scored agent-loop run to the agent or to search.

A recall number says how much was missed. It does not say which query missed it, what came
back instead, or whose fault it was -- and those three answers need different fixes:

    agent issued no query for the capability   -> agent: coverage gap
    agent issued a vague or wrong query        -> agent: query quality
    agent issued a fair query, search missed   -> SEARCH: recall
    search returned it, but only in `related`  -> SEARCH: ranking
    no tool for it exists anywhere             -> catalogue, nobody's search bug

Attribution runs in three layers, so that no verdict rests on a single opaque judgement.

  1. Deterministic, from Composio's own toolkit metadata: which applications does the query
     name, and which does the needed tool belong to? A query naming Vercel cannot be blamed
     on search for failing to return Cloudflare tools -- that is settled without an LLM, and
     a human can check it. Compound queries ("A or B") are flagged here too.
  2. What layer 1 cannot settle goes to an LLM, asked a concrete question about a named
     tool: would a competent engine return THIS tool for THIS query? Three independent votes,
     majority wins.
  3. Both layers are printed on every case, so any verdict can be audited by hand.

Layer 2 is shown the tool that was expected. An earlier version withheld it, meaning to stop
the model reasoning backwards from the answer key; that was the wrong trade and produced
systematically wrong verdicts. The question is not "was there a miss" -- that is already
established -- but "whose fault is it", which cannot be answered without knowing the target.
Concretely: the capability "Read and update the booking schedule" never mentions that the
schedule lives in Google Sheets, so the query "read and update bookings or calendar events"
looked like a perfect match and search was blamed for returning Calendar tools. The same
error credited search with a failure on "publish video to social media platforms" when the
target was an Instagram-specific tool the query never named.

The same split applies to the disagreement list. When the agent ran a tool an independent
judge rejects, what matters is whether a correct tool was sitting in the results it had:

    correct tool WAS in the results, agent chose another  -> agent: selection error
    correct tool was never returned                       -> search: agent had no option

Requires the run to have been scored first:

    python score_with_groups.py runN_x && python analyse_failures.py runN_x
"""
from __future__ import annotations

import json, re, sys
from collections import Counter
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai

from agent_loop_evaluation import GEMINI_API_KEY, GEMINI_RPM, RateLimiter, ROOT, save_json
from score_with_groups import call_gemini

# Fault labels. AGENT_* are fixable by better decomposition or phrasing; SEARCH_* are
# retrieval or ranking defects; CATALOGUE is neither.
AGENT_NO_QUERY = "agent: never searched for it"
AGENT_WEAK_QUERY = "agent: query too vague to find it"
SEARCH_RECALL = "search: fair query, tool not returned"
SEARCH_RANKING = "search: returned it, but only in related"
CATALOGUE = "catalogue: no tool provides this"


MATCH_QUERY_PROMPT = '''An agent worked a task by issuing search queries against a tool catalogue.
One capability the task required was never delivered. Decide which query, if any, the agent
issued in an attempt to find a tool for that capability.

Task:
{task}

Capability that was never delivered:
  {capability}

Queries the agent issued, in order:
{queries}

Match on what the query was looking for. Several queries may mention the same application
while targeting completely different steps -- pick the one aimed at THIS capability.

Return exactly this JSON:
{{"index": <1-based index of the query aimed at this capability, or null if none was>,
  "why": "one sentence"}}
'''


# The adequacy call is shown the tools that were expected. An earlier version withheld them,
# to stop the model reasoning backwards from the answer key -- which was the wrong trade. The
# question here is not "was there a miss" (that is already established) but "whose fault is
# it", and that cannot be answered without knowing what the target was.
#
# Withholding it produced exactly the wrong verdicts. The capability "Read and update the
# booking schedule" never mentions that the schedule lives in Google Sheets; the query "read
# and update bookings or calendar events" therefore looks like a perfect match, and search
# was blamed for returning Calendar tools. Same for "Attempt social media publishing on
# Instagram" against the query "publish video to social media platforms": without seeing
# INSTAGRAM_POST_IG_USER_MEDIA, the model cannot know a generic social-publishing tool was
# not the intended answer.
#
# Asking about a named tool also turns an abstract judgement into a concrete one a human can
# check: would this tool be a correct top result for this query?
ADEQUACY_PROMPT = '''You are auditing a tool-search engine by deciding whether a query was
specific enough to find a particular tool.

The query that was issued:
  "{query}"

The tool that should have been returned:
  {tool}
  {tool_description}

The step the user was trying to carry out:
  {capability}

Question: for that query alone, would a competent search engine be expected to return that
tool among its top results?

Answer NO when the query does not identify the tool:
- the tool belongs to a specific application and the query names a different one, or names
  none at all while describing something many applications could do. "Publish video to
  social media platforms" does not identify an Instagram-specific publishing tool. "Read and
  update bookings or calendar events" does not identify a spreadsheet tool.
- the query asks for a different action than the tool performs.
- the query bundles several unrelated asks together, so no single tool is clearly the target.

Answer YES only when the query genuinely points at this tool -- naming its application, or
describing its specific action unambiguously enough that it is an obvious top result. If YES
and search still failed to return it, that is a real retrieval failure.

Judge the query against the tool, not the quality of the results that came back.

Return exactly this JSON:
{{"findable": true or false, "why": "one sentence"}}
'''


# When a query names no application at all, and the needed tool belongs to a specific one,
# the decisive question is whether search returned an equivalent tool from a DIFFERENT
# application. If it did, search answered the question it was actually asked and the query
# was simply under-specified -- "fetch social media page posts" cannot be expected to yield
# Facebook rather than LinkedIn, and "create reminder or task" cannot be expected to yield
# TickTick rather than Notion. Without this check those land on search, which is unfair and
# would not survive review.
SUBSTITUTE_PROMPT = '''A search query named no particular application. Judge whether the results
did essentially the job the query asked for, using a different application.

The query:
  "{query}"

The tool that was expected (from {needed_vendor}):
  {tool}

What search actually returned as its top results:
{returned}

Do the returned tools perform essentially the same KIND of work the query described, just in
a different application than the one expected? Ignore which application is "correct" -- the
query never named one. Judge only whether the returned tools do that kind of job.

Return exactly this JSON:
{{"equivalent": true or false, "why": "one sentence"}}
'''


# Final gate before blaming search. If something search returned does what the QUERY literally
# asked for, then search answered correctly and the query simply asked for the wrong thing.
# This catches the cases that survive every other check: a query "merge a pull request on
# GitHub" that returned GITHUB_MERGE_A_PULL_REQUEST cannot be a retrieval failure merely
# because the step actually needed GITHUB_MERGE_A_BRANCH; nor can "deploy or manage vercel
# project" be blamed for returning deployment tools when the step needed environment
# variables. Both are the agent asking for the wrong thing, not search failing to answer.
ANSWERED_QUERY_PROMPT = '''Judge whether a search engine answered the query it was actually given.

The query:
  "{query}"

What it returned as top results:
{returned}

Ignoring what the user "really" needed, did those results cover EVERY distinct thing this
query asked for? Judge the results against the words of the query alone.

A query often names several actions ("inspect and commit or pull request" names three).
Answer false if the results cover only some of them -- partial coverage is a retrieval
failure on the clauses that were ignored, not a correct answer. Read-only results do not
satisfy a clause asking to create, commit, update or merge something.

Answer true only when nothing the query asked for was left unaddressed.

Return exactly this JSON:
{{"answered": true or false, "slug": "the tool that answers the query, or null",
  "unaddressed": "the part of the query nothing covered, or null",
  "why": "one sentence"}}
'''


ALTERNATIVE_AVAILABLE_PROMPT = '''An agent ran a tool that did not deliver a capability the task
required. Decide whether a tool that WOULD have delivered it was among the results the agent
had already seen.

Capability required:
  {capability}

Tool the agent ran instead:
  {ran}

Every tool the search engine returned to this agent, with descriptions:
{returned}

Was a tool that genuinely delivers the capability available in that list? Judge on the
descriptions. If the task names a specific application, only a tool from that same
application counts.

Return exactly this JSON:
{{"available": true or false, "slug": "the tool it should have used, or null",
  "why": "one sentence"}}
'''


def vendor_drift(traces: dict[int, dict], metadata_cache: Path) -> dict[str, Any]:
    """Queries that name an application and get nothing from it back.

    This is measured directly from the traces rather than judged, and it is counted
    separately from capability recall because it can happen even when no capability was
    missed -- and, more importantly, even when the requirement group was empty. Task 1 asked
    "Create or check payment link in HubSpot" and got STRIPE_CREATE_PAYMENT_LINK as its only
    primary result. Scoring called that capability a catalogue gap, which is fair on its own
    terms, and in doing so never looked at the query at all. The vendor failure was invisible.

    Matching is on word boundaries: `cal` (Cal.com) must appear as its own word, or it fires
    on every mention of "calendar" and manufactures false positives. Toolkits come from
    Composio's own metadata, with a longest-prefix fallback for the few cached records whose
    toolkit field is null.
    """
    cache = json.loads(metadata_cache.read_text(encoding="utf-8")) if metadata_cache.exists() else {}
    known = {rec["toolkit"].lower() for rec in cache.values()
             if rec and rec.get("toolkit")}

    def toolkit_of(slug: str) -> str | None:
        record = cache.get(slug)
        if record and record.get("toolkit"):
            return record["toolkit"].lower()
        lowered = slug.lower()
        for candidate in sorted(known, key=len, reverse=True):
            if lowered.startswith(candidate + "_"):
                return candidate
        return None

    patterns = {}
    for vendor in known:
        cleaned = vendor.strip("_")
        if len(cleaned) < 3:
            continue
        alts = {re.escape(cleaned.replace("_", "")), re.escape(cleaned.replace("_", " "))}
        patterns[vendor] = re.compile(r"(?<![a-z0-9])(?:" + "|".join(sorted(alts)) + r")(?![a-z0-9])")

    total = scoped = 0
    cases: list[dict[str, Any]] = []
    for task_id in sorted(traces):
        for query in traces[task_id]["queries"]:
            total += 1
            text = re.sub(r"[^a-z0-9]+", " ", query["query"].lower())
            wanted = {v for v, p in patterns.items() if p.search(text)}
            if not wanted:
                continue
            scoped += 1
            primary = query.get("primary_tool_slugs") or []
            related = query.get("related_tool_slugs") or []
            in_primary = {toolkit_of(s) for s in primary} - {None}
            anywhere = {toolkit_of(s) for s in primary + related} - {None}
            if wanted & in_primary:
                continue
            cases.append({"task": task_id, "query": query["query"],
                          "named": sorted(wanted), "primary": primary[:4],
                          "absent_entirely": not (wanted & anywhere)})
    return {"total_queries": total, "vendor_scoped": scoped, "cases": cases,
            "severe": [c for c in cases if c["absent_entirely"]]}


def load_run(run_dir: Path) -> tuple[dict[int, dict], list[dict]]:
    traces = {}
    for path in sorted(run_dir.glob("task-*.json"), key=lambda p: int(p.stem.split("-")[-1])):
        trace = json.loads(path.read_text(encoding="utf-8"))
        traces[trace["identifier"]] = trace
    scores_path = run_dir / "group_scores.json"
    if not scores_path.exists():
        raise SystemExit(f"run not scored yet -- run score_with_groups.py {run_dir.name} first")
    return traces, json.loads(scores_path.read_text(encoding="utf-8"))


def surfaced_sets(trace: dict) -> tuple[set[str], set[str]]:
    primary, everything = set(), set()
    for query in trace["queries"]:
        p = set(query.get("primary_tool_slugs") or [])
        primary |= p
        everything |= p | set(query.get("related_tool_slugs") or [])
    return primary, everything


def describe_results(query: dict) -> str:
    primary = query.get("primary_tool_slugs") or []
    related = query.get("related_tool_slugs") or []
    if not primary and not related:
        return "  (nothing returned)"
    return (f"  primary: {', '.join(primary) or '(none)'}\n"
            f"  related: {', '.join(related) or '(none)'}")


def vendor_signals(query_text: str, expected: list[str], toolkits: dict[str, str],
                   patterns: dict[str, Any], returned: list[str] | None = None) -> dict[str, Any]:
    """Deterministic checks a human can verify without trusting any model.

    These decide the clear-cut cases outright. A query naming Vercel cannot be blamed on
    search for failing to return Cloudflare tools; a query naming no application at all,
    where the needed tool is one application's specific feature, is under-specified. Only
    what these cannot settle goes to the LLM.
    """
    named = {v for v, p in patterns.items()
             if p.search(re.sub(r"[^a-z0-9]+", " ", query_text.lower()))}
    needed = {toolkits.get(s) for s in expected} - {None}
    got = {toolkits.get(s) for s in (returned or [])} - {None}
    return {
        "vendors_named_in_query": sorted(named),
        "vendors_needed": sorted(needed),
        "vendors_returned": sorted(got),
        "names_wrong_vendor": bool(named and needed and not (named & needed)),
        "names_no_vendor": not named,
        # True only when search answered with a different application than the one needed.
        # Without this the under-specified-query gate fired on task 16, where search returned
        # nine GitHub tools -- the right vendor, all read-only -- and excused a real miss.
        "returned_other_vendor": bool(got and needed and not (got & needed)),
        "compound": bool(re.search(r"\bor\b", query_text.lower())),
    }


def findable_vote(client, limiter, query: str, tool: str, description: str,
                  capability: str, votes: int = 3) -> tuple[bool, str]:
    """Majority of independent votes, so one stray sample cannot flip a verdict."""
    results, reasons = [], []
    for _ in range(votes):
        verdict = call_gemini(client, limiter, ADEQUACY_PROMPT.format(
            query=query, tool=tool, tool_description=description[:300] or "",
            capability=capability)) or {}
        results.append(bool(verdict.get("findable")))
        reasons.append(verdict.get("why", ""))
    yes = sum(results)
    majority = yes > votes / 2
    pick = next((r for r, v in zip(reasons, results) if v == majority), reasons[0] if reasons else "")
    return majority, f"{pick} [{yes}/{votes} votes]"



# Verbs that ask for a change. If a query contains one and every tool search returned is
# tagged readOnlyHint, search did not answer the write half of the question -- whatever else
# it got right. This replaces an LLM check that could not hold a line: asked whether results
# "covered the query", it excused task 16 (query "inspect and commit or pull request", nine
# read-only GitHub tools returned) because inspection was covered, then flipped to rejecting
# "merge a pull request on GitHub" -- which returned exactly GITHUB_MERGE_A_PULL_REQUEST --
# because an extra result was also present. Composio's own tags settle it without judgement.
WRITE_VERB = re.compile(
    r"\b(creat\w*|commit\w*|merg\w*|updat\w*|delet\w*|add|adds|adding|post\w*|publish\w*"
    r"|send\w*|upload\w*|writ\w*|insert\w*|remov\w*|archiv\w*|assign\w*|set|configur\w*"
    r"|modif\w*|edit\w*|appl\w*|mov\w*|renam\w*)\b", re.I)


def write_ask_unanswered(query: dict, descriptions: dict) -> str | None:
    """Query asks for a change, every returned tool is read-only -> search missed the write."""
    if not WRITE_VERB.search(query["query"]):
        return None
    returned = (query.get("primary_tool_slugs") or []) + (query.get("related_tool_slugs") or [])
    if not returned:
        return None
    tagged = [(descriptions.get(s) or {}).get("tags") or [] for s in returned]
    known = [t for t in tagged if t]
    if not known or len(known) < len(returned) / 2:
        return None                                  # too little tag coverage to conclude
    if any("readOnlyHint" not in t for t in known):
        return None                                  # at least one write tool came back
    verb = WRITE_VERB.search(query["query"]).group(0)
    return (f"query asks to '{verb}' but every tool returned is tagged read-only, so the "
            f"write half of the query was never answered")


def _judge_findable(cached: dict, client, limiter, query: dict, expected: list[str],
                    descriptions: dict, group: dict) -> None:
    """Decide whether search should have found the target, then sanity-check the verdict.

    A "yes" here blames search, so it gets one more test: did search answer the query it was
    literally given? If it did, the query asked for the wrong thing and the fault is the
    agent's. Without this, a query reading "merge a pull request on GitHub" counts as a
    retrieval failure even though GITHUB_MERGE_A_PULL_REQUEST came back as the top result,
    purely because the step needed GITHUB_MERGE_A_BRANCH.
    """
    target = expected[0]
    description = (descriptions.get(target) or {}).get("description", "")
    ok, why = findable_vote(client, limiter, query["query"], target, description,
                            group["purpose"])
    if ok:
        # Deterministic override, from Composio's own readOnlyHint tags: a query asking for a
        # change, answered only with read-only tools, is a retrieval failure whatever else
        # came back. Settled here so the LLM gate below cannot excuse it.
        unanswered = write_ask_unanswered(query, descriptions)
        if unanswered:
            cached["findable"] = True
            cached["adequacy_why"] = f"{why} ({unanswered})"
            return
        primary = query.get("primary_tool_slugs") or []
        related = query.get("related_tool_slugs") or []
        answered = call_gemini(client, limiter, ANSWERED_QUERY_PROMPT.format(
            query=query["query"],
            returned="\n".join(f"- {s}" for s in (primary + related)[:8]) or "  (nothing)")) or {}
        if answered.get("answered") and answered.get("slug") not in expected:
            cached["findable"] = False
            cached["adequacy_why"] = (
                f"search answered the query as written -- {answered.get('slug')} does what it "
                f"asked; the step needed something else. {answered.get('why','')}")
            return
    cached["findable"] = ok
    cached["adequacy_why"] = why


def attribute(group: dict, trace: dict, client, limiter, cache: dict,
              toolkits: dict[str, str], patterns: dict, descriptions: dict) -> dict[str, Any]:
    """Work out which query targeted this capability, and whose failure it was."""
    expected = group.get("acceptable_tool_slugs") or []
    primary, everything = surfaced_sets(trace)
    key = f"{trace['identifier']}::{group['purpose']}"

    if not expected:
        return {"fault": CATALOGUE, "query": None, "query_index": None,
                "returned": None, "reason": "no tool in the logged list provides this either",
                "adequacy_why": ""}

    # Harness self-check: an unmet group should have had nothing surfaced.
    if set(expected) & primary:
        return {"fault": "harness: scored unmet but WAS returned as primary", "query": None,
                "query_index": None, "returned": None,
                "reason": "scorer and analyser disagree -- investigate", "adequacy_why": ""}
    if set(expected) & everything:
        return {"fault": SEARCH_RANKING, "query": None, "query_index": None, "returned": None,
                "reason": "an expected tool was surfaced but never promoted to primary",
                "adequacy_why": ""}

    if key in cache:
        cached = cache[key]
    else:
        listing = "\n".join(f"{i}. \"{q['query']}\"" for i, q in enumerate(trace["queries"], 1))
        match = call_gemini(client, limiter, MATCH_QUERY_PROMPT.format(
            task=trace["task"][:400], capability=group["purpose"], queries=listing)) or {}
        index = match.get("index")
        cached = {"index": index if isinstance(index, int) else None,
                  "match_why": match.get("why", "")}
        if cached["index"] and 1 <= cached["index"] <= len(trace["queries"]):
            query = trace["queries"][cached["index"] - 1]
            signals = vendor_signals(query["query"], expected, toolkits, patterns,
                                     (query.get("primary_tool_slugs") or [])
                                     + (query.get("related_tool_slugs") or []))
            cached["signals"] = signals
            # Deterministic verdicts first. Only what these cannot settle costs LLM calls.
            if signals["names_wrong_vendor"]:
                cached["findable"] = False
                cached["adequacy_why"] = (
                    f"query names {', '.join(signals['vendors_named_in_query'])} but the step "
                    f"needs {', '.join(signals['vendors_needed'])}")
            elif (signals["names_no_vendor"] and signals["vendors_needed"]
                  and signals["returned_other_vendor"]):
                # No application named, the target belongs to one, and search answered with a
                # DIFFERENT application. Only then is this the under-specified-query case.
                #
                # The returned-vendor check is load-bearing. Without it the gate fired on
                # task 16, where the query asked to "inspect and commit or pull request" and
                # search returned nine GitHub tools -- every one read-only. Same vendor, and
                # nothing that commits or opens a pull request, so there was no substitution
                # to excuse; that is a straight retrieval failure.
                primary = query.get("primary_tool_slugs") or []
                sub = call_gemini(client, limiter, SUBSTITUTE_PROMPT.format(
                    query=query["query"], tool=expected[0],
                    needed_vendor=", ".join(signals["vendors_needed"]),
                    returned="\n".join(f"- {s}" for s in primary[:6]) or "  (nothing)")) or {}
                if sub.get("equivalent"):
                    cached["findable"] = False
                    cached["adequacy_why"] = (
                        f"query named no application; search returned an equivalent tool from "
                        f"another one -- {sub.get('why','')}")
                else:
                    _judge_findable(cached, client, limiter, query, expected,
                                    descriptions, group)
            else:
                _judge_findable(cached, client, limiter, query, expected,
                                descriptions, group)
        cache[key] = cached

    index = cached.get("index")
    if not index or not 1 <= index <= len(trace["queries"]):
        return {"fault": AGENT_NO_QUERY, "query": None, "query_index": None, "returned": None,
                "reason": "no query the agent issued was aimed at this capability",
                "adequacy_why": cached.get("match_why", "")}

    query = trace["queries"][index - 1]
    fault = SEARCH_RECALL if cached.get("findable") else AGENT_WEAK_QUERY
    return {"fault": fault, "query": query["query"], "query_index": index,
            "returned": describe_results(query),
            "reason": cached.get("adequacy_why", ""),
            "adequacy_why": cached.get("adequacy_why", ""),
            "signals": cached.get("signals", {})}


def analyse_disagreement(group: dict, execution: dict, trace: dict, client, limiter,
                         match_why: str) -> dict[str, Any]:
    """Was the agent's wrong pick a selection error, or did search leave it no option?"""
    _, everything = surfaced_sets(trace)
    listing = "\n".join(f"- {s}" for s in sorted(everything)[:40]) or "  (nothing)"
    verdict = call_gemini(client, limiter, ALTERNATIVE_AVAILABLE_PROMPT.format(
        capability=group["purpose"], ran=execution["tool_slug"], returned=listing)) or {}
    available = bool(verdict.get("available"))
    return {
        "capability": group["purpose"],
        "expected_any_of": group.get("acceptable_tool_slugs") or [],
        "agent_ran": execution["tool_slug"],
        "agent_claimed": execution.get("purpose", ""),
        "execution_mode": execution.get("mode"),
        "match_why": match_why,
        "judge_said": group.get("why", ""),
        "better_tool_was_available": available,
        "should_have_used": verdict.get("slug"),
        "fault": ("agent: chose the wrong tool from results that contained a correct one"
                  if available else
                  "search: never returned a tool that could do it, so the agent had no option"),
        "availability_why": verdict.get("why", ""),
    }


MATCH_CALL_PROMPT = '''An agent worked a task, stating a purpose for each tool it ran. One required
capability was independently judged as never delivered. Decide whether the agent believed it
had covered that capability.

Task:
{task}

Capability judged NOT delivered:
  {capability}

Tool calls the agent made, each with the purpose it stated:
{calls}

Which call, if any, was the agent's attempt at THAT capability? Match on what the agent said
it was doing, not on the application name.

Return exactly this JSON:
{{"index": <1-based index of the matching call, or null>, "why": "one sentence"}}
'''


def main(run_dir: Path) -> None:
    load_dotenv()
    client = genai.Client(api_key=GEMINI_API_KEY)
    limiter = RateLimiter(GEMINI_RPM)
    traces, scores = load_run(run_dir)

    # Shared lookups for the deterministic layer, from Composio's own metadata.
    meta = json.loads((ROOT / "tool_metadata_cache.json").read_text(encoding="utf-8"))         if (ROOT / "tool_metadata_cache.json").exists() else {}
    known = {r["toolkit"].lower() for r in meta.values() if r and r.get("toolkit")}
    toolkits: dict[str, str] = {}
    for slug, record in meta.items():
        if record and record.get("toolkit"):
            toolkits[slug] = record["toolkit"].lower()
        else:
            lowered = slug.lower()
            for candidate in sorted(known, key=len, reverse=True):
                if lowered.startswith(candidate + "_"):
                    toolkits[slug] = candidate
                    break
    patterns = {}
    for vendor in known:
        cleaned = vendor.strip("_")
        if len(cleaned) < 3:
            continue
        alts = {re.escape(cleaned.replace("_", "")), re.escape(cleaned.replace("_", " "))}
        patterns[vendor] = re.compile(
            r"(?<![a-z0-9])(?:" + "|".join(sorted(alts)) + r")(?![a-z0-9])")
    descriptions = {s: r for s, r in meta.items() if r}

    cache_path = run_dir / "attribution_cache.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}

    faults: Counter[str] = Counter()
    failures: list[dict[str, Any]] = []
    disagreements: list[dict[str, Any]] = []
    demoted: list[dict[str, Any]] = []

    for row in scores:
        if "error" in row:
            continue
        trace = traces.get(row["task"])
        if not trace:
            continue
        primary, _ = surfaced_sets(trace)

        for group in row.get("unmet", []):
            if group.get("judged"):
                continue  # a valid alternative was found; not a failure
            detail = attribute(group, trace, client, limiter, cache,
                               toolkits, patterns, descriptions)
            faults[detail["fault"]] += 1
            failures.append({"task": row["task"], "capability": group["purpose"],
                             "expected_any_of": group.get("acceptable_tool_slugs") or [],
                             "judge_said": group.get("why", ""), **detail})
            save_json(cache_path, cache)

        # Demotion lives among the MET groups: the capability WAS delivered, just never
        # recommended. Counting only unmet groups misses it entirely.
        for group in row.get("met", []):
            if not set(group.get("acceptable_tool_slugs") or []) & primary:
                demoted.append({"task": row["task"], "capability": group["purpose"],
                                "found_in_related": group.get("matched", [])})

        # Disagreements: the agent said it did a step the judge says was never delivered.
        unmet = [g for g in row.get("unmet", []) if not g.get("judged")]
        executions = [e for e in trace.get("executions", []) if e.get("purpose")]
        if unmet and executions:
            calls = "\n".join(f"{i}. ran {e['tool_slug']} -- purpose: \"{e['purpose']}\""
                              for i, e in enumerate(executions, 1))
            for group in unmet:
                match = call_gemini(client, limiter, MATCH_CALL_PROMPT.format(
                    task=trace["task"][:400], capability=group["purpose"], calls=calls)) or {}
                index = match.get("index")
                if not isinstance(index, int) or not 1 <= index <= len(executions):
                    continue
                disagreements.append({"task": row["task"], **analyse_disagreement(
                    group, executions[index - 1], trace, client, limiter, match.get("why", ""))})

    total = sum(r.get("groups", 0) for r in scores if "error" not in r)
    drift = vendor_drift(traces, ROOT / "tool_metadata_cache.json")
    write_reports(run_dir, failures, disagreements, demoted, faults, total, traces, drift)


# --------------------------------------------------------------------------------------
# Reports. Written to be read by someone who was not here: the answer first, plain labels
# instead of internal fault codes, caveats last, and every case laid out the same way --
# what was asked, what was needed, what came back, what went wrong.
# --------------------------------------------------------------------------------------

PLAIN = {
    AGENT_NO_QUERY:   ("The agent never looked for it",
                       "No query it issued was aimed at this capability, so search was never asked."),
    AGENT_WEAK_QUERY: ("The agent asked too vaguely",
                       "It searched, but the query did not identify the tool it needed."),
    SEARCH_RECALL:    ("Search missed a fair question",
                       "The query identified what was needed and search still did not return it."),
    SEARCH_RANKING:   ("Search found it but buried it",
                       "The right tool came back under `related`, never as a recommendation."),
    CATALOGUE:        ("No tool exists for it",
                       "Nothing in the catalogue does this, so nobody could have found it."),
}


def case_block(*, task: int, capability: str, asked: str | None, wanted: list[str],
               got: str | None, problem: str, extra: list[str] | None = None) -> list[str]:
    """One failure, always in the same shape, so the file can be skimmed rather than read."""
    out = [f"#### Task {task} — {capability}", ""]
    out.append(f"- **Asked:** `{asked}`" if asked
               else "- **Asked:** _nothing — no query targeted this_")
    out.append("- **Needed:** " + (", ".join(f"`{s}`" for s in wanted) if wanted
                                   else "_no tool in the catalogue provides this_"))
    if got:
        for index, line in enumerate(got.splitlines()):
            out.append(("- **Got:** " if index == 0 else "  ") + line.strip())
    out.append(f"- **What went wrong:** {problem}")
    out.extend(extra or [])
    out.append("")
    return out


def write_reports(run_dir, failures, disagreements, demoted, faults, total, traces,
                  drift) -> None:
    agent_fault = sum(v for k, v in faults.items() if k.startswith("agent"))
    search_recall = faults.get(SEARCH_RECALL, 0)
    search_side = search_recall + len(demoted)
    by_fault: dict[str, list] = {}
    for failure in failures:
        by_fault.setdefault(failure["fault"], []).append(failure)
    hard = [f for f in failures if f["fault"] == SEARCH_RECALL
            and "read-only" in (f.get("adequacy_why") or "")]

    md = [f"# What went wrong — `{run_dir.name}`", "",
          f"The 100 use cases need **{total} capabilities** between them. This is every one that was",
          "not delivered, why, and whose problem it is to fix.", "",
          "## The short version", "",
          "- **Search almost always finds the right tool.** It failed to retrieve one for a fair, "
          f"specific query in **{search_recall} of {total}** cases.",
          f"- **It just does not always recommend it.** In **{len(demoted)}** cases the right tool came "
          "back only under `related`, never as a primary recommendation. An agent acting on the "
          f"recommendation misses all {len(demoted)} — so this, not retrieval, is the thing worth fixing.",
          f"- **{agent_fault} failures are the agent's own**: it either never searched for the "
          f"capability ({faults.get(AGENT_NO_QUERY, 0)}) or asked too vaguely to find it "
          f"({faults.get(AGENT_WEAK_QUERY, 0)}). These say nothing about search quality.",
          f"- **{faults.get(CATALOGUE, 0)}** need a tool that does not exist in the catalogue at all.",
          "",
          "| What happened | Count | Whose problem |", "|---|---:|---|"]
    counts = {**faults, SEARCH_RANKING: len(demoted)}
    owner = {SEARCH_RANKING: "**Search — ranking**", SEARCH_RECALL: "**Search — retrieval**",
             CATALOGUE: "Catalogue", AGENT_NO_QUERY: "Agent", AGENT_WEAK_QUERY: "Agent"}
    for fault in (SEARCH_RANKING, AGENT_NO_QUERY, AGENT_WEAK_QUERY, CATALOGUE, SEARCH_RECALL):
        count = counts.get(fault, 0)
        if count:
            md.append(f"| {PLAIN[fault][0]} | {count} | {owner[fault]} |")
    md += ["", f"**Search-side {search_side} · agent-side {agent_fault} · catalogue "
               f"{faults.get(CATALOGUE, 0)}.**", ""]

    md += ["---", "", "## Search found the right tool but buried it", "",
           f"{len(demoted)} capabilities were delivered **only** in `related`. The tool was there; it",
           "was never put forward. This is the largest fixable failure in the run, and counting it",
           "needs no judgement — it is set membership.", ""]
    if demoted:
        md += ["| Task | What was needed | Tool that was buried |", "|---|---|---|"]
        for item in demoted:
            tools = ", ".join(f"`{s}`" for s in item["found_in_related"][:3])
            md.append(f"| {item['task']} | {item['capability']} | {tools} |")
        md.append("")

    md += ["## Search missed a fair question", "",
           f"{search_recall} cases where the query did identify what was needed and search still did",
           "not return it. Each is laid out in full so it can be checked.", "",
           "**These are first-attempt failures.** Across all 384 queries in this run the agent never",
           "re-asked for a capability once -- not a single near-duplicate query. It searches once per",
           "step and moves on, because mocked execution succeeds on any well-formed call and nothing",
           "ever tells it a tool was wrong. So each case below is one shot, and search might well",
           "recover on a rephrase; equally, this benchmark produces no evidence about retry",
           "behaviour at all, which a production agent hitting real errors would exhibit.", ""]
    for failure in by_fault.get(SEARCH_RECALL, []):
        md += case_block(
            task=failure["task"], capability=failure["capability"], asked=failure.get("query"),
            wanted=failure["expected_any_of"], got=failure.get("returned"),
            problem=failure.get("adequacy_why") or failure.get("reason", ""),
            extra=[f"- **Judge:** {failure['judge_said']}"] if failure.get("judge_said") else None)

    if drift["cases"]:
        md += ["## Queries that named an application and got a different one", "",
               f"Of {drift['total_queries']} queries, {drift['vendor_scoped']} name an application. "
               f"{len(drift['cases'])} of those got nothing from it in `primary`, and "
               f"{len(drift['severe'])} got nothing from it anywhere.", "",
               "Counted separately because it happens even when no capability was missed — task 1",
               "asked for a HubSpot payment link and was answered entirely in Stripe.", "",
               "| Task | Asked | Wanted from | Got | Named app absent entirely |",
               "|---|---|---|---|---|"]
        for case in drift["cases"]:
            tools = ", ".join(f"`{s}`" for s in case["primary"]) or "_(none)_"
            md.append(f"| {case['task']} | `{case['query'][:50]}` | {', '.join(case['named'])} | "
                      f"{tools} | {'**yes**' if case['absent_entirely'] else 'no'} |")
        md.append("")

    md += ["---", "", "## Failures that are not search's fault", ""]
    for fault in (AGENT_NO_QUERY, AGENT_WEAK_QUERY, CATALOGUE):
        items = by_fault.get(fault, [])
        if not items:
            continue
        title, explain = PLAIN[fault]
        md += [f"### {title} ({len(items)})", "", explain, ""]
        if fault == AGENT_WEAK_QUERY:
            for failure in items:
                md += case_block(task=failure["task"], capability=failure["capability"],
                                 asked=failure.get("query"), wanted=failure["expected_any_of"],
                                 got=failure.get("returned"),
                                 problem=failure.get("adequacy_why") or failure.get("reason", ""))
        else:
            header = ("Capability that was never searched for" if fault == AGENT_NO_QUERY
                      else "Capability with no tool behind it")
            md += [f"| Task | {header} |", "|---|---|"]
            for failure in items:
                md.append(f"| {failure['task']} | {failure['capability']} |")
            md.append("")

    md += ["---", "", "## How much to trust these numbers", "",
           "**Safe to quote as-is.** These come from set membership, with no judgement involved:", "",
           f"- {len(demoted)} delivered only in `related`",
           f"- {faults.get(AGENT_NO_QUERY, 0)} never searched for by the agent",
           f"- {faults.get(CATALOGUE, 0)} capabilities with no tool behind them", "",
           "**Quote with the case list attached.** Splitting the rest between *the query was too "
           "vague* and *search should have found it* is a reading of the evidence, not a "
           "measurement. It was revised five times while this analysis was built — 19 to 11 to 5 to "
           "1 to 2 to 4 — moving in both directions as each rule was corrected. Two corrections came "
           "from cases spotted by hand: search was being blamed for not returning Cloudflare tools "
           "to a query about Vercel, and Sheets tools to a query about calendar events. A later "
           "over-correction then excused a genuine GitHub miss.", "",
           f"Of the {search_recall} recall failures, **{len(hard)}** rests on deterministic evidence "
           "— Composio's own `readOnlyHint` tags proving nothing returned could perform the change "
           "the query asked for. The others rest on LLM votes and are individually arguable.", "",
           "**How each verdict was reached.** Deterministic checks run first, from Composio's own "
           "toolkit and read-only metadata: a query naming one application cannot be blamed for not "
           "returning another's tools, and a query asking to create something cannot be satisfied "
           "by read-only results. Only what those cannot settle goes to an LLM, asked a concrete "
           "question about a named tool and answered by a majority of three votes.", ""]

    (run_dir / "failure_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    save_json(run_dir / "failure_analysis.json",
              {"failures": failures, "demoted": demoted, "faults": dict(faults),
               "vendor_drift": drift})

    sel = [d for d in disagreements if d["better_tool_was_available"]]
    none_avail = [d for d in disagreements if not d["better_tool_was_available"]]
    quote = chr(34)
    dm = [f"# When the agent thought it had succeeded — `{run_dir.name}`", "",
          "The agent states what each tool call is for. These are the calls where it believed it had",
          "carried out a step, and an independent judge found that capability was never delivered.", "",
          "**Why this matters more than a missed capability.** The agent records the step as done and",
          "carries on, so every later step is built on something that never happened. A recall number",
          "cannot see this at all — the capability simply looks satisfied.", "",
          f"**{len(disagreements)} cases: {len(sel)} the agent's fault, {len(none_avail)} search's.**", "",
          "The split turns on one question: was a tool that would have worked already sitting in the",
          "results the agent had seen?", "", "---", "",
          f"## The agent chose badly ({len(sel)})", "",
          "A correct tool was in the results it had already been shown, and it picked something else.", ""]
    if not sel:
        dm.append("_None._")
    for item in sel:
        dm += [f"#### Task {item['task']} — {item['capability']}", "",
               f"- **Agent ran:** `{item['agent_ran']}` ({item['execution_mode']})",
               f"- **Saying it was for:** {quote}{item['agent_claimed']}{quote}",
               f"- **Should have used:** `{item.get('should_have_used')}` — it was in the results",
               f"- **What went wrong:** {item.get('availability_why', '')}",
               f"- **Judge:** {item['judge_said']}", ""]
    dm += [f"## Search left it no option ({len(none_avail)})", "",
           "Nothing search had returned could do the job, so the agent substituted the closest thing",
           "it had. These are search failures wearing an agent-error costume.", ""]
    if not none_avail:
        dm.append("_None._")
    for item in none_avail:
        wanted = ", ".join(f"`{s}`" for s in item["expected_any_of"]) or "_(nothing listed)_"
        dm += [f"#### Task {item['task']} — {item['capability']}", "",
               f"- **Agent ran:** `{item['agent_ran']}` ({item['execution_mode']})",
               f"- **Saying it was for:** {quote}{item['agent_claimed']}{quote}",
               f"- **Would have needed:** {wanted}",
               f"- **What went wrong:** {item.get('availability_why', '')}",
               f"- **Judge:** {item['judge_said']}", ""]
    (run_dir / "agent_vs_judge.md").write_text("\n".join(dm) + "\n", encoding="utf-8")
    save_json(run_dir / "agent_vs_judge.json", disagreements)

    print(f"{len(failures)}/{total} capabilities unmet, {len(demoted)} demoted")
    for fault, count in faults.most_common():
        print(f"  {fault:<52} {count}")
    print(f"  agent-side {agent_fault} | search-side {search_side}")
    print(f"vendor drift: {len(drift['cases'])}/{drift['vendor_scoped']} vendor-scoped queries "
          f"({len(drift['severe'])} with the named app absent entirely)")
    print(f"disagreements: {len(disagreements)} "
          f"({len(sel)} agent selection, {len(none_avail)} search left no option)")


if __name__ == "__main__":
    target = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "run8_full_100tasks")
    if not target.is_dir():
        raise SystemExit(f"no such run directory: {target}")
    main(target)
