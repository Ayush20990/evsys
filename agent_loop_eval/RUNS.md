# Run index

`run6_descriptions_20tasks/` is current — see `README.md` for its results. Earlier runs are kept only
because each one established something that shaped the current design.

| Run | Change from previous | What it established |
|---|---|---|
| 1 | real reads attempted, 0 connections | Gating real execution on `readOnlyHint` alone is not enough |
| 2 | fully mocked | *(superseded — same prompt defect as run 1, not kept)* |
| 3 | prompt fixed | The terse queries were a harness defect, not model behaviour |
| 4 | real reads, 9 toolkits connected | Real data makes the agent search less, breaking cross-run recall comparisons |
| 5 | 20 tasks, completion tracking | Query count does not scale with task complexity |
| 6 | tool descriptions + schemas returned | Descriptions fix tool choice and argument construction |

## What each run established

**Run 1 — `readOnlyHint` is a safety gate, not a feasibility check.** Real execution was gated on the
tag alone, but the toolkits had no connected accounts, so every call returned a 400 whose message
says *"To fix this, call COMPOSIO_MANAGE_CONNECTIONS"*. The agent obeyed, searched for that tool, got
unrelated products back, and abandoned the task. 21% of all queries were consumed this way and every
task derailed. Real execution now requires the tag **and** an ACTIVE connection under this `USER_ID`,
and infrastructure errors never reach the agent.

**Run 3 — the terse queries were mine, not the model's.** Runs 1 and 2 produced single-word searches
(`'email'`, `'workflow'`) that were nearly written up as a finding about agent behaviour. The prompt
had said *"search for ONE capability at a time"* and *"issue one focused query"*; removing that
guidance changed nothing, which made the model look responsible, and terseness reproduced across
three Gemini tiers. The actual cause: removing the brevity instruction left no *quality* bar at all.
The primary benchmark's `DECOMPOSE_PROMPT` gets well-formed queries from the same model by
constraining specificity and requiring an `intent` sentence. Porting both fixed it.

*The general lesson: reproducing a result across models proves nothing if every run shares the
harness under suspicion.*

**Run 4 — recall comparisons across execution policies are invalid.** Over the same ten tasks, mocked
run 3 scored 74% union from 86 queries; real-read run 4 scored 63% from 50. But hits per query went
0.79 → 1.16. Real data lets the agent stop searching once something works, so session recall falls as
quality rises.

**Run 5 — emergent query count under-samples hard tasks.** Grouped by reference-list size: ≤6 tools
gave 69% recall, 7-13 gave 59%, ≥14 gave 38% — while queries per task stayed near 4-6 throughout. A
task needing 25 tools got 5.7 queries. This is the same coverage failure the primary benchmark fixed
with `ceil(pool_size / TOOLS_PER_QUERY_TARGET)`, so an emergent count is not automatically better
than a formula.

Run 5 also added `finish_task` and the `blocked_by` split, and exposed a bug where `toolkit_of()`
resolved every `ONE_DRIVE_*` slug to `one`, silently mocking OneDrive reads despite a live connection.

**Run 6 — descriptions change behaviour, not headline recall.** Returning each tool's description and
parameter schema alongside the slug:

| | Run 5 | Run 6 |
|---|---:|---:|
| Queries | 94 | 73 |
| Real executions | 15 | 34 |
| Mock-rejected calls | 11 | 2 |
| Executions using a reference tool | 45% | 60% |
| Hits per query | 1.20 | 1.45 |
| Flat union recall | 49% | 46% |

Every quality signal improved while flat recall fell — the third run showing that metric moving
opposite to agent quality, which is what prompted the switch to group-based scoring.

## Layout

Each run directory holds per-task traces (`task-0NN.json`), `agent_queries.json`, the generated
reports, and the run log. Runs scored with `score_with_groups.py` also carry `group_scoring_report.md`,
`group_scores.json` and `group_cache.json`.
