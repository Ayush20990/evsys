"""Contrast the queries an agent actually issued against the ones the primary
benchmark imagined for the same tasks.

Both pipelines start from the same use cases, so the interesting question is not
which scores better -- they have different ground truth -- but whether the agent
phrases and segments its searches the way the one-shot decomposer predicted it would.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENT = ROOT / "agent_queries.json"
IMAGINED = ROOT.parent / "src" / "query_level_workflow_evaluation" / "query_ground_truth.json"
OUT = ROOT / "agent_vs_imagined.md"


def main() -> None:
    agent = json.loads(AGENT.read_text(encoding="utf-8"))
    imagined_rows = json.loads(IMAGINED.read_text(encoding="utf-8"))["queries"]

    by_workflow: dict[int, list[str]] = {}
    for row in imagined_rows:
        by_workflow.setdefault(int(row["workflow_id"]), []).append(row["query"])

    md = [
        "# Agent-issued queries vs one-shot imagined queries\n",
        "Same tasks, two ways of producing the queries. The left column is what the "
        "one-shot decomposer predicted an agent would search for; the right is what an "
        "agent actually searched for while working the task with real results in front "
        "of it.\n",
    ]

    agent_counts, imagined_counts = [], []
    for task in agent["tasks"]:
        ident = task["identifier"]
        mine = task["queries"]
        theirs = by_workflow.get(ident, [])
        agent_counts.append(len(mine))
        imagined_counts.append(len(theirs))

        md.append(f"## Task {ident}")
        md.append(f"*{task['task'][:220]}{'...' if len(task['task']) > 220 else ''}*\n")
        md.append(f"**Imagined ({len(theirs)} queries)**")
        md.extend(f"- `{q}`" for q in theirs) if theirs else md.append("- _(workflow rejected during generation)_")
        md.append(f"\n**Agent-issued ({len(mine)} queries)**")
        md.extend(f"- `{q}`" for q in mine) if mine else md.append("- _(none)_")
        md.append("")

    if agent_counts:
        md.append("## Query-count comparison\n")
        md.append("| Task | Imagined | Agent-issued |")
        md.append("|---|---:|---:|")
        for task, mine, theirs in zip(agent["tasks"], agent_counts, imagined_counts):
            md.append(f"| {task['identifier']} | {theirs} | {mine} |")
        md.append(f"| **mean** | **{sum(imagined_counts)/len(imagined_counts):.1f}** | "
                  f"**{sum(agent_counts)/len(agent_counts):.1f}** |")

    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
