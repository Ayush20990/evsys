"""Write search_failures.md for a run, from that run's own measurements only.

Run 8's equivalent was assembled by hand from a separate probing pass that invented extra
phrasings for capabilities the agent never queried well. Nothing here is invented: every
query listed is one the agent actually issued during the run, and every result listed is
what search actually returned for it. A capability the agent never searched for produces no
entry, because there is no search failure to report -- that is an agent failure and belongs
in failure_analysis.md.

Two kinds of search failure are reported, kept apart because they are different defects:

  missed    a fair, on-target query, and the needed tool came back nowhere -- not in
            `primary`, not in `related`. Retrieval failed.
  demoted   search did return the needed tool, but only in `related`, while `primary` held
            something else. Retrieval worked and ranking failed. An agent acting on the
            primary recommendation -- which is what agents do -- loses these all the same.

    python build_search_failures.py run9_retry_loop
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def wrap_returned(blob: str | None) -> list[str]:
    """The stored `returned` blob is already two labelled lines; keep them as written."""
    if not blob:
        return ["   - returned: (nothing)"]
    return [f"   - {line.strip()}" for line in blob.strip().splitlines() if line.strip()]


def query_that_surfaced(trace: dict, tool: str) -> dict | None:
    """The query whose `related` carried this tool -- the evidence that search had it."""
    for query in trace.get("queries", []):
        if tool in (query.get("related_tool_slugs") or []):
            return query
    return None


def main() -> None:
    run_dir = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "run9_retry_loop")
    analysis = load(run_dir / "failure_analysis.json")
    traces = {t["identifier"]: t for t in
              (load(p) for p in sorted(run_dir.glob("task-*.json")))}

    missed = [f for f in analysis["failures"]
              if f["fault"] == "search: fair query, tool not returned"]
    demoted = analysis["demoted"]

    out: list[str] = [
        "# Search failures — run 9",
        "",
        f"Every query below was issued by the agent during run 9, and every result is what "
        f"`COMPOSIO_SEARCH_TOOLS` returned for it. Nothing is reconstructed or rephrased "
        f"after the fact.",
        "",
        f"- **{len(missed)}** capabilities where a fair query returned the needed tool nowhere.",
        f"- **{len(demoted)}** where search did return it, but ranked it into `related` while "
        f"`primary` held something else.",
        "",
        "---",
        "",
        "## Part 1 — the needed tool was not returned at all",
        "",
    ]

    for f in missed:
        trace = traces.get(f["task"], {})
        out += [f"### Task {f['task']} — {trace.get('task', '').strip()}", ""]
        out += [f"**Capability:** {f['capability']}", ""]
        out += ["Tools the agent needed: "
                + ", ".join(f"`{t}`" for t in f["expected_any_of"]), ""]
        out += ["Query the agent issued, and what came back:", ""]
        for attempt in f.get("attempts") or [{"query": f["query"], "returned": f["returned"]}]:
            out.append(f"{attempt.get('attempt', 1)}. `{attempt['query']}`")
            out += wrap_returned(attempt.get("returned"))
        out += [""]
        # Whether the agent noticed is the difference between a slow task and a wrong answer.
        if f.get("retried"):
            out.append("The agent recognised the result was wrong and searched again.")
        elif f.get("ran_a_returned_tool"):
            out.append(
                "The agent did **not** notice: it ran "
                + ", ".join(f"`{t}`" for t in f["ran_a_returned_tool"])
                + " from these results and carried on as though the step were done.")
        else:
            out.append("The agent ran nothing from these results and moved on.")
        out += [""]

    out += ["---", "",
            "## Part 2 — the needed tool was returned, but only in `related`", "",
            "Retrieval found these. Ranking put something else in `primary`, which is the "
            "position an agent acts on.", ""]

    for d in demoted:
        trace = traces.get(d["task"], {})
        tool = d["found_in_related"][0]
        query = query_that_surfaced(trace, tool)
        out += [f"### Task {d['task']} — {d['capability']}", ""]
        out += ["Needed: " + ", ".join(f"`{t}`" for t in d["found_in_related"]), ""]
        if query:
            out += [f"Query: `{query['query']}`", "",
                    "   - primary: " + (", ".join(query.get("primary_tool_slugs") or [])
                                        or "(nothing)"),
                    "   - related: " + (", ".join(query.get("related_tool_slugs") or [])
                                        or "(nothing)"),
                    ""]
        else:
            out += ["_Surfaced across more than one query; see the trace._", ""]

    path = run_dir / "search_failures.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {path}")
    print(f"  part 1: {len(missed)} not returned at all")
    print(f"  part 2: {len(demoted)} returned but demoted to related")


if __name__ == "__main__":
    main()
