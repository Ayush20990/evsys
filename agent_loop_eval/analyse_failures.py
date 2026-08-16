"""Classify every failure in a scored agent-loop run, and isolate agent/judge disagreements.

Recall says how much was missed. It does not say *why*, and the causes need different fixes:
a capability the catalogue lacks is a product gap, a capability search held but ranked below
the fold is a ranking bug, and a capability the agent believed it had solved with a tool an
independent judge rejects is a precision problem that recall cannot see at all.

That last class is the reason this script exists. The agent now states a `purpose` on every
execute_tool call -- its own claim about which step the call carries out. Comparing that
claim against the judge's verdict on the same capability separates two failures that are
identical in the recall number:

    search returned nothing usable        -> the agent knows it failed
    the agent acted on a tool that does   -> the agent believes it succeeded, and a
    not actually do the job                  downstream step then builds on a false premise

The second is strictly worse for an agent in production, and invisible without the claim.

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


def load_run(run_dir: Path) -> tuple[dict[int, dict], list[dict]]:
    traces = {}
    for path in sorted(run_dir.glob("task-*.json"), key=lambda p: int(p.stem.split("-")[-1])):
        trace = json.loads(path.read_text(encoding="utf-8"))
        traces[trace["identifier"]] = trace
    scores_path = run_dir / "group_scores.json"
    if not scores_path.exists():
        raise SystemExit(f"run not scored yet -- run score_with_groups.py {run_dir.name} first")
    return traces, json.loads(scores_path.read_text(encoding="utf-8"))


def classify(group: dict, trace: dict) -> tuple[str, str]:
    """Why did this capability go unmet? Returns (category, note)."""
    expected = group.get("acceptable_tool_slugs") or []
    surfaced = set()
    primary = set()
    for query in trace["queries"]:
        p = set(query.get("primary_tool_slugs") or [])
        primary |= p
        surfaced |= p | set(query.get("related_tool_slugs") or [])

    if not expected:
        return ("catalogue-gap",
                "the task needs this, and no tool in the logged list provided it either")
    # An unmet group by definition had NO expected tool surfaced, so it cannot also have
    # been surfaced-but-demoted. Demotion is a failure of MET groups and is counted
    # separately in main(); an expected tool showing up here would mean the scorer and this
    # classifier disagree, which is a harness bug worth surfacing loudly.
    if set(expected) & primary:
        return ("scoring-anomaly", "an expected tool WAS returned as primary yet scored unmet")
    if set(expected) & surfaced:
        return ("scoring-anomaly", "an expected tool WAS surfaced yet scored unmet")
    abandoned = [a["query"] for a in trace.get("abandoned_capabilities") or []]
    if abandoned:
        return ("searched-and-abandoned",
                f"the agent gave up after repeated fruitless searches ({len(abandoned)} abandoned)")
    return ("never-returned", "no expected tool appeared anywhere in any search result")


MATCH_PROMPT = '''An agent worked a task, stating a purpose for each tool it ran. One required
capability was independently judged as never delivered. Decide whether the agent believed it
had covered that capability.

Task:
{task}

Capability judged NOT delivered:
  {capability}

Tool calls the agent made, each with the purpose it stated:
{calls}

Which call, if any, was the agent's attempt at THAT capability? Match on what the agent said
it was doing, not on the application name -- several calls will share an application while
aiming at completely different steps.

Return exactly this JSON:
{{"index": <1-based index of the matching call, or null if none was aimed at this capability>,
  "why": "one sentence"}}
'''


def find_disagreements(trace: dict, row: dict, client, limiter) -> list[dict[str, Any]]:
    """Calls where the agent believed it covered a capability the judge says was never met.

    The agent's `purpose` is free text, so it cannot be joined to a capability by string
    equality. An earlier version matched on toolkit instead, which paired every HubSpot call
    with every unmet HubSpot capability -- reporting that the agent "believed" it had
    assessed payment-link feasibility when its stated purpose was creating a marketing
    email. That inflates the list with pairs the agent never claimed.

    Matching is therefore semantic, and returns at most one call per capability: the one the
    agent actually aimed at it. A capability no call was aimed at is not a disagreement --
    it is a plain miss, already counted in the failure analysis.
    """
    from score_with_groups import call_gemini

    unmet = [g for g in row.get("unmet", []) if not g.get("judged")]
    executions = [e for e in trace.get("executions", []) if e.get("purpose")]
    if not unmet or not executions:
        return []

    listing = "\n".join(f"{i}. ran {e['tool_slug']} -- purpose: \"{e['purpose']}\""
                        for i, e in enumerate(executions, 1))
    out = []
    for group in unmet:
        verdict = call_gemini(client, limiter, MATCH_PROMPT.format(
            task=trace["task"][:400], capability=group["purpose"], calls=listing))
        index = (verdict or {}).get("index")
        if not isinstance(index, int) or not 1 <= index <= len(executions):
            continue
        execution = executions[index - 1]
        out.append({
            "capability": group["purpose"],
            "expected_any_of": group.get("acceptable_tool_slugs") or [],
            "agent_ran": execution["tool_slug"],
            "agent_claimed": execution["purpose"],
            "execution_mode": execution.get("mode"),
            "match_reason": (verdict or {}).get("why", ""),
            "judge_said": group.get("why", ""),
        })
    return out


def main(run_dir: Path) -> None:
    load_dotenv()
    client = genai.Client(api_key=GEMINI_API_KEY)
    limiter = RateLimiter(GEMINI_RPM)
    traces, scores = load_run(run_dir)
    categories: Counter[str] = Counter()
    failures: list[dict[str, Any]] = []
    disagreements: list[dict[str, Any]] = []

    for row in scores:
        if "error" in row:
            continue
        trace = traces.get(row["task"])
        if not trace:
            continue
        for group in row.get("unmet", []):
            if group.get("judged"):
                continue  # a valid alternative was found; not a failure
            category, note = classify(group, trace)
            categories[category] += 1
            failures.append({
                "task": row["task"], "capability": group["purpose"],
                "category": category, "note": note,
                "expected_any_of": group.get("acceptable_tool_slugs") or [],
                "judge_said": group.get("why", ""),
            })
        for item in find_disagreements(trace, row, client, limiter):
            disagreements.append({"task": row["task"], **item})

    # Demotion is a distinct failure and the most common one: the capability WAS delivered,
    # just never as a primary recommendation. It lives among the MET groups, so counting only
    # unmet groups misses it entirely -- and it is the finding that has held across every run.
    demoted: list[dict[str, Any]] = []
    for row in scores:
        if "error" in row:
            continue
        trace = traces.get(row["task"])
        if not trace:
            continue
        primary = set()
        for query in trace["queries"]:
            primary |= set(query.get("primary_tool_slugs") or [])
        for group in row.get("met", []):
            if not set(group.get("acceptable_tool_slugs") or []) & primary:
                demoted.append({"task": row["task"], "capability": group["purpose"],
                                "matched_in_related": group.get("matched", [])})

    total_groups = sum(r.get("groups", 0) for r in scores if "error" not in r)
    write_reports(run_dir, failures, disagreements, categories, total_groups, traces, demoted)


def write_reports(run_dir: Path, failures, disagreements, categories, total_groups,
                  traces, demoted) -> None:
    md = [f"# Failure analysis — `{run_dir.name}`", "",
          f"{len(failures)} capabilities went unmet out of {total_groups} required "
          f"({100*len(failures)/total_groups:.0f}%), after the judge credited valid alternatives.",
          "", "## Failures by cause", "",
          "| Cause | Count | What it means | Who fixes it |", "|---|---:|---|---|"]
    meaning = {
        "never-returned": ("no expected tool appeared in any search result",
                           "search recall"),
        "ranked-related-only": ("the right tool was returned but never promoted to primary",
                                "**ranking** — the tool was there"),
        "catalogue-gap": ("the task needs a capability no logged tool provides",
                          "product/catalogue, not search"),
        "searched-and-abandoned": ("the agent searched repeatedly and gave up",
                                   "search recall"),
        "scoring-anomaly": ("an expected tool was returned as primary yet scored unmet",
                            "**this harness** — investigate"),
    }
    for category, count in categories.most_common():
        what, who = meaning.get(category, ("", ""))
        md.append(f"| `{category}` | {count} | {what} | {who} |")

    md += ["", "## Delivered, but not recommended", "",
           f"{len(demoted)} capabilities were satisfied ONLY by a tool in `related` — search held the",
           "right tool and never promoted it. An agent acting on the primary recommendation would",
           "have missed these, so in practice they sit between a hit and a miss.", ""]
    if demoted:
        md += ["| Task | Capability | Found only in `related` |", "|---|---|---|"]
        for item in demoted:
            tools = ", ".join(f"`{s}`" for s in item["matched_in_related"][:3])
            md.append(f"| {item['task']} | {item['capability']} | {tools} |")
    else:
        md.append("_None._")

    md += ["", "## Every unmet capability", ""]
    by_task: dict[int, list] = {}
    for failure in failures:
        by_task.setdefault(failure["task"], []).append(failure)
    for task in sorted(by_task):
        md.append(f"### Task {task}")
        md.append(f"> {traces[task]['task'][:200]}")
        md.append("")
        for failure in by_task[task]:
            expected = ", ".join(f"`{s}`" for s in failure["expected_any_of"]) or "_(nothing listed)_"
            md.append(f"- **{failure['capability']}** — `{failure['category']}`")
            md.append(f"  - expected: {expected}")
            md.append(f"  - {failure['note']}")
            if failure["judge_said"]:
                md.append(f"  - judge: {failure['judge_said']}")
        md.append("")

    (run_dir / "failure_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    save_json(run_dir / "failure_analysis.json",
              {"failures": failures, "categories": dict(categories)})

    dm = [f"# Agent believed it worked, judge disagreed — `{run_dir.name}`", "",
          "Each row is a tool the agent ran **while stating it was carrying out a specific step**,",
          "where an independent judge then ruled that capability was never delivered. Recall cannot",
          "see these: the agent records success and later steps proceed on a false premise.", "",
          "The agent's stated purpose is matched to the capability semantically, one call per",
          "capability. A capability no call was aimed at is a plain miss, not a disagreement, and is",
          "counted in `failure_analysis.md` instead.", ""]
    if not disagreements:
        dm.append("_None in this run._")
    else:
        dm += [f"**{len(disagreements)} cases.**", ""]
        by_task = {}
        for item in disagreements:
            by_task.setdefault(item["task"], []).append(item)
        for task in sorted(by_task):
            dm.append(f"### Task {task}")
            dm.append("")
            for item in by_task[task]:
                dm.append(f"- Agent ran **`{item['agent_ran']}`** ({item['execution_mode']})")
                dm.append(f"  - agent's stated purpose: *\"{item['agent_claimed']}\"*")
                dm.append(f"  - capability the judge ruled unmet: **{item['capability']}**")
                if item["expected_any_of"]:
                    dm.append(f"  - would have accepted: "
                              f"{', '.join('`'+s+'`' for s in item['expected_any_of'])}")
                if item.get("match_reason"):
                    dm.append(f"  - matched because: {item['match_reason']}")
                if item["judge_said"]:
                    dm.append(f"  - judge: {item['judge_said']}")
            dm.append("")
    (run_dir / "agent_vs_judge.md").write_text("\n".join(dm) + "\n", encoding="utf-8")
    save_json(run_dir / "agent_vs_judge.json", disagreements)

    print(f"failures: {len(failures)}/{total_groups} capabilities unmet, "
          f"{len(demoted)} delivered but demoted to related")
    for category, count in categories.most_common():
        print(f"  {category:<24} {count}")
    print(f"agent/judge disagreements: {len(disagreements)}")
    print(f"wrote {run_dir/'failure_analysis.md'} and {run_dir/'agent_vs_judge.md'}")


if __name__ == "__main__":
    target = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "run6_descriptions_20tasks")
    if not target.is_dir():
        raise SystemExit(f"no such run directory: {target}")
    main(target)
