"""Export the agent-loop runs as a flat, shareable dataset.

Everything comes from what was recorded during the runs -- nothing is re-queried and no
model is called. For each run directory given, three views of the same data are written to
`dataset/`:

  queries.csv        one row per search the agent issued: the task, the query, what search
                     returned in `primary` and `related`, and which of those were correct.
  capabilities.csv   one row per capability a task requires: the tools that would satisfy
                     it, whether it was delivered (as primary, only in related, or not at
                     all), and when not, whose fault and which query was meant to find it.
  tasks.jsonl        one record per task with all of the above nested, plus the tools the
                     agent actually executed and how the task ended.

"Correct" is judged against the task's requirement groups. A task the grouping stage could
not score has no groups; its queries are judged against the raw `Tools:` list instead, and
the `scoring_basis` column says which was used.

    python build_dataset.py run8_full_100tasks run9_retry_loop
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dataset"

GROUPS = "requirement groups"
REFERENCE = "reference Tools list (task not scored)"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def joined(items) -> str:
    return "; ".join(items or [])


def capabilities_of(score: dict | None) -> list[dict]:
    if not score or "met" not in score:
        return []
    return score["met"] + score["unmet"]


def build_task(run: str, trace: dict, score: dict | None, faults: dict) -> dict:
    task_id = int(trace["identifier"])
    caps = capabilities_of(score)
    if caps:
        basis = GROUPS
        correct = {s for c in caps for s in c["acceptable_tool_slugs"]}
    else:
        basis = REFERENCE
        correct = set(trace["reference_tools"])

    queries = []
    for i, q in enumerate(trace["queries"], 1):
        primary, related = q.get("primary_tool_slugs") or [], q.get("related_tool_slugs") or []
        hit_primary = [s for s in primary if s in correct]
        hit_related = [s for s in related if s in correct]
        returned = set(primary) | set(related)
        queries.append({
            "query_index": i,
            "query": q["query"],
            "intent": q.get("intent", ""),
            "attempt": q.get("attempt", 1),
            "is_retry": q.get("is_retry", False),
            "is_slug_lookup": q.get("is_slug_lookup", False),
            "primary_tools": primary,
            "related_tools": related,
            "correct_in_primary": hit_primary,
            "correct_in_related": hit_related,
            "result": ("correct tool in primary" if hit_primary
                       else "correct tool only in related" if hit_related
                       else "no correct tool returned"),
            "capabilities_served": [c["purpose"] for c in caps
                                    if returned & set(c["acceptable_tool_slugs"])],
        })

    capabilities = []
    for c in caps:
        matched = c.get("matched") or []
        surfaced = next((q for q in queries
                         if set(matched) & set(q["primary_tools"] + q["related_tools"])), None)
        fault = faults.get((task_id, c["purpose"]), {})
        if matched:
            in_primary = any(set(matched) & set(q["primary_tools"]) for q in queries)
            outcome = "delivered as primary" if in_primary else "delivered only in related"
        elif c.get("judged"):
            outcome = "delivered (judge accepted a different tool)"
        else:
            outcome = "not delivered"
        capabilities.append({
            "capability": c["purpose"],
            "acceptable_tools": c["acceptable_tool_slugs"],
            "outcome": outcome,
            "matched_tools": matched or ([c["judged_slug"]] if c.get("judged_slug") else []),
            "delivering_query": surfaced["query"] if surfaced else "",
            "fault": fault.get("fault", ""),
            "targeting_query": fault.get("query") or "",
            "search_returned": (fault.get("returned") or "").strip(),
            "judge_reason": c.get("why", ""),
            "fault_reason": fault.get("reason", ""),
        })

    return {
        "run": run,
        "task_id": task_id,
        "task": trace["task"],
        "reference_tools": trace["reference_tools"],
        "scoring_basis": basis,
        "completed": trace.get("completed"),
        "stop_reason": trace.get("stop_reason"),
        "unmet_steps": trace.get("unmet_steps") or [],
        "queries": queries,
        "capabilities": capabilities,
        "executions": [{"tool": e["tool_slug"], "purpose": e.get("purpose", ""),
                        "mode": e.get("mode", ""), "successful": e.get("successful")}
                       for e in trace.get("executions") or []],
    }


def build_run(run: str) -> list[dict]:
    run_dir = ROOT / run
    scores = {s["task"]: s for s in load(run_dir / "group_scores.json")}
    analysis = run_dir / "failure_analysis.json"
    faults = ({(f["task"], f["capability"]): f for f in load(analysis)["failures"]}
              if analysis.exists() else {})
    return [build_task(run, load(p), scores.get(int(p.stem.split("-")[1])), faults)
            for p in sorted(run_dir.glob("task-*.json"))]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: joined(v) if isinstance(v, list) else v for k, v in row.items()})


def main(runs: list[str]) -> None:
    OUT.mkdir(exist_ok=True)
    tasks = [t for run in runs for t in build_run(run)]
    head = lambda t: {"run": t["run"], "task_id": t["task_id"], "task": t["task"]}

    write_csv(OUT / "queries.csv",
              [{**head(t), "scoring_basis": t["scoring_basis"], **q}
               for t in tasks for q in t["queries"]])
    write_csv(OUT / "capabilities.csv",
              [{**head(t), **c} for t in tasks for c in t["capabilities"]])
    with (OUT / "tasks.jsonl").open("w", encoding="utf-8") as fh:
        for t in tasks:
            fh.write(json.dumps(t, ensure_ascii=False) + "\n")

    for run in runs:
        ts = [t for t in tasks if t["run"] == run]
        qs = [q for t in ts for q in t["queries"]]
        cs = [c for t in ts for c in t["capabilities"]]
        count = lambda rows, key, val: sum(r[key] == val for r in rows)
        print(f"{run}: {len(ts)} tasks, {sum(t['scoring_basis'] == GROUPS for t in ts)} scored")
        print(f"  queries {len(qs)}: primary {count(qs, 'result', 'correct tool in primary')}, "
              f"related only {count(qs, 'result', 'correct tool only in related')}, "
              f"none {count(qs, 'result', 'no correct tool returned')}")
        print(f"  capabilities {len(cs)}: "
              + ", ".join(f"{o} {count(cs, 'outcome', o)}" for o in
                          ["delivered as primary", "delivered only in related",
                           "delivered (judge accepted a different tool)", "not delivered"]))


if __name__ == "__main__":
    main(sys.argv[1:] or ["run8_full_100tasks", "run9_retry_loop"])
