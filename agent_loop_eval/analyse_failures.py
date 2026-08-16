"""Attribute every failure in a scored agent-loop run to the agent or to search.

A recall number says how much was missed. It does not say which query missed it, what came
back instead, or whose fault it was -- and those three answers need different fixes:

    agent issued no query for the capability   -> agent: coverage gap
    agent issued a vague or wrong query        -> agent: query quality
    agent issued a fair query, search missed   -> SEARCH: recall
    search returned it, but only in `related`  -> SEARCH: ranking
    no tool for it exists anywhere             -> catalogue, nobody's search bug

Attribution runs in two LLM stages per unmet capability. First, which of the agent's queries
was aimed at this capability -- the agent's queries are free text, so this cannot be a string
match. Second, given that query, *should* a competent search engine have returned a tool that
does the job? A query naming the application and the action is fair, and missing it is
search's failure; a query too vague to identify the capability is the agent's failure. The
judgement is made without showing the model which tools were expected, so it cannot reason
backwards from the answer key.

The same split applies to the disagreement list. When the agent ran a tool an independent
judge rejects, what matters is whether a correct tool was sitting in the results it had:

    correct tool WAS in the results, agent chose another  -> agent: selection error
    correct tool was never returned                       -> search: agent had no option

Requires the run to have been scored first:

    python score_with_groups.py runN_x && python analyse_failures.py runN_x
"""
from __future__ import annotations

import json, sys
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


ADEQUACY_PROMPT = '''You are auditing a tool-search engine. Judge whether a query was good enough
that a competent search engine SHOULD have found the right tool.

The capability the user needed:
  {capability}

The query that was issued:
  "{query}"

What the search engine returned for it:
{returned}

Would THIS query, as written, lead a competent engine to a tool that does THAT capability?

This is not a question about whether the query is well phrased in general. It is about
whether the query actually asks for the capability above.

Answer false when the query asks for something materially different from the capability,
even if it is a perfectly good query for what it does ask. In particular:
- it names a different application than the capability requires (a query about Vercel
  deployments cannot be expected to return Cloudflare DNS tools; a query about calendar
  events cannot be expected to return spreadsheet tools);
- it asks for a different action (reading when the capability is writing, listing when the
  capability is updating);
- it is so generic that many unrelated capabilities would match it equally well.

Answer true only when the query genuinely targets this capability -- naming the right
application, or describing the action unambiguously enough that the right tool is the
obvious answer -- and search still failed to return it.

Judge the query against the capability, not against the quality of the results. Poor results
for a query that did ask the right thing is exactly the failure being measured, and counts
as adequate=true.

Return exactly this JSON:
{{"adequate": true or false, "why": "one sentence explaining the verdict"}}
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


def attribute(group: dict, trace: dict, client, limiter, cache: dict) -> dict[str, Any]:
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
            verdict = call_gemini(client, limiter, ADEQUACY_PROMPT.format(
                capability=group["purpose"], query=query["query"],
                returned=describe_results(query))) or {}
            cached["adequate"] = bool(verdict.get("adequate"))
            cached["adequacy_why"] = verdict.get("why", "")
        cache[key] = cached

    index = cached.get("index")
    if not index or not 1 <= index <= len(trace["queries"]):
        return {"fault": AGENT_NO_QUERY, "query": None, "query_index": None, "returned": None,
                "reason": "no query the agent issued was aimed at this capability",
                "adequacy_why": cached.get("match_why", "")}

    query = trace["queries"][index - 1]
    fault = SEARCH_RECALL if cached.get("adequate") else AGENT_WEAK_QUERY
    return {"fault": fault, "query": query["query"], "query_index": index,
            "returned": describe_results(query),
            "reason": cached.get("adequacy_why", ""),
            "adequacy_why": cached.get("adequacy_why", "")}


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
            detail = attribute(group, trace, client, limiter, cache)
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
    write_reports(run_dir, failures, disagreements, demoted, faults, total, traces)


def write_reports(run_dir, failures, disagreements, demoted, faults, total, traces) -> None:
    agent_fault = sum(v for k, v in faults.items() if k.startswith("agent"))
    search_fault = sum(v for k, v in faults.items() if k.startswith("search")) + len(demoted)

    md = [f"# Failure analysis — `{run_dir.name}`", "",
          f"{len(failures)} of {total} required capabilities went unmet after the judge credited",
          f"valid alternatives, plus {len(demoted)} delivered but never recommended.", "",
          "Every failure below is attributed: which query was meant to find the tool, what search",
          "returned for it, and whether the query was good enough that search should have found it.",
          "",
          "## Where the fault lies", "",
          "| Fault | Count | Meaning |", "|---|---:|---|"]
    meaning = {
        AGENT_NO_QUERY: "the agent never searched for this capability at all",
        AGENT_WEAK_QUERY: "the agent searched, but too vaguely for any engine to resolve",
        SEARCH_RECALL: "the agent asked a fair question and search did not return the tool",
        SEARCH_RANKING: "search returned the right tool but left it in `related`",
        CATALOGUE: "no tool in the catalogue provides this",
    }
    for fault, count in faults.most_common():
        md.append(f"| {fault} | {count} | {meaning.get(fault, 'investigate')} |")
    md.append(f"| {SEARCH_RANKING} (from met groups) | {len(demoted)} | "
              f"delivered only in `related`, never promoted |")
    md += ["",
           f"**Agent-side: {agent_fault}. Search-side: {search_fault}. "
           f"Catalogue: {faults.get(CATALOGUE, 0)}.**", "",
           "Agent-side failures are fixable by better decomposition or phrasing and say nothing",
           "about retrieval quality. Search-side failures are the ones that belong in a report on",
           "the search tool.", ""]

    md += ["## Delivered, but never recommended", "",
           f"{len(demoted)} capabilities were satisfied only by a tool in `related`. An agent acting",
           "on the primary recommendation would have missed every one.", ""]
    if demoted:
        md += ["| Task | Capability | Found only in `related` |", "|---|---|---|"]
        for item in demoted:
            tools = ", ".join(f"`{s}`" for s in item["found_in_related"][:3])
            md.append(f"| {item['task']} | {item['capability']} | {tools} |")
    md.append("")

    md += ["## Every unmet capability, with its query", ""]
    by_task: dict[int, list] = {}
    for failure in failures:
        by_task.setdefault(failure["task"], []).append(failure)
    for task in sorted(by_task):
        md += [f"### Task {task}", "", f"> {traces[task]['task'][:220]}", ""]
        for f in by_task[task]:
            expected = ", ".join(f"`{s}`" for s in f["expected_any_of"]) or "_(nothing listed)_"
            md += [f"**{f['capability']}**", "",
                   f"- needed: {expected}",
                   f"- **fault: {f['fault']}**"]
            if f.get("query"):
                md.append(f"- query the agent issued (#{f['query_index']}): `{f['query']}`")
                md.append(f"- search returned:\n```\n{f['returned']}\n```")
            else:
                md.append(f"- {f['reason']}")
            if f.get("adequacy_why"):
                md.append(f"- why: {f['adequacy_why']}")
            if f.get("judge_said"):
                md.append(f"- judge: {f['judge_said']}")
            md.append("")

    (run_dir / "failure_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    save_json(run_dir / "failure_analysis.json",
              {"failures": failures, "demoted": demoted, "faults": dict(faults)})

    sel = [d for d in disagreements if d["better_tool_was_available"]]
    nooption = [d for d in disagreements if not d["better_tool_was_available"]]
    dm = [f"# Agent believed it worked, judge disagreed — `{run_dir.name}`", "",
          "Each case is a tool the agent ran **while stating it was carrying out a specific step**,",
          "where an independent judge ruled that capability was never delivered. Recall cannot see",
          "these: the agent records success and later steps proceed on a false premise.", "",
          f"**{len(disagreements)} cases — {len(sel)} the agent's fault, {len(nooption)} search's.**", "",
          "The split is the useful part. If a tool that would have worked was sitting in the results",
          "the agent had already seen, it chose badly. If no such tool was ever returned, the agent",
          "had no option and the failure is search's.", "",
          "## Agent selection errors — a correct tool was available and not chosen", ""]
    if not sel:
        dm.append("_None._")
    for item in sel:
        dm += [f"**Task {item['task']} — {item['capability']}**", "",
               f"- agent ran `{item['agent_ran']}` ({item['execution_mode']}), stating: "
               f"*\"{item['agent_claimed']}\"*",
               f"- should have used: `{item.get('should_have_used')}`",
               f"- why: {item.get('availability_why', '')}",
               f"- judge: {item['judge_said']}", ""]
    dm += ["## Search left the agent no option — nothing returned could do it", ""]
    if not nooption:
        dm.append("_None._")
    for item in nooption:
        expected = ", ".join(f"`{s}`" for s in item["expected_any_of"]) or "_(nothing listed)_"
        dm += [f"**Task {item['task']} — {item['capability']}**", "",
               f"- agent ran `{item['agent_ran']}` ({item['execution_mode']}), stating: "
               f"*\"{item['agent_claimed']}\"*",
               f"- would have needed: {expected}",
               f"- why: {item.get('availability_why', '')}",
               f"- judge: {item['judge_said']}", ""]
    (run_dir / "agent_vs_judge.md").write_text("\n".join(dm) + "\n", encoding="utf-8")
    save_json(run_dir / "agent_vs_judge.json", disagreements)

    print(f"{len(failures)}/{total} capabilities unmet, {len(demoted)} demoted")
    for fault, count in faults.most_common():
        print(f"  {fault:<52} {count}")
    print(f"  agent-side {agent_fault} | search-side {search_fault}")
    print(f"disagreements: {len(disagreements)} "
          f"({len(sel)} agent selection, {len(nooption)} search left no option)")


if __name__ == "__main__":
    target = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "run8_full_100tasks")
    if not target.is_dir():
        raise SystemExit(f"no such run directory: {target}")
    main(target)
