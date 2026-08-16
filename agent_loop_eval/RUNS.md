# Run index

`run8_full_100tasks/` is current — see `README.md` for its results. Earlier runs are kept only
because each one established something that shaped the current design.

| Run | Change from previous | What it established |
|---|---|---|
| 1 | real reads attempted, 0 connections | Gating real execution on `readOnlyHint` alone is not enough |
| 2 | fully mocked | *(superseded — same prompt defect as run 1, not kept)* |
| 3 | prompt fixed | The terse queries were a harness defect, not model behaviour |
| 4 | real reads, 9 toolkits connected | Real data makes the agent search less, breaking cross-run recall comparisons |
| 5 | 20 tasks, completion tracking | Query count does not scale with task complexity |
| 6 | tool descriptions + schemas returned | Descriptions fix tool choice and argument construction |
| 7 | stuck step abandons capability, not task; agent states a `purpose` per call | Every task finishes; agent/judge disagreements become measurable |
| 8 | **all 100 use cases** | Judged recall is flat across task complexity; demotion outnumbers outright misses |

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

**Run 7 — a stuck step no longer ends the task, and the agent states its intent.** Two changes.
Tripping the thrashing breaker now abandons the capability and lets the task continue; previously it
returned, killing the task and leaving every later step unsearched. And `execute_tool` now requires a
`purpose` — the agent's own claim about which step a call carries out — which is what makes
`agent_vs_judge.md` possible: without it, a call can only be matched to a capability by toolkit, and
that pairs every HubSpot call with every unmet HubSpot capability.

| | Run 6 | Run 7 |
|---|---:|---:|
| Judged group recall | 70% | **75%** |
| Strict group recall | 61% | **67%** |
| Tasks reaching a clean finish | 19/20 | **20/20** |
| Capabilities abandoned | n/a | 0 |

Run 7 made 21 write-tool calls against run 6's fewer, which is why its real-execution count is lower
(13 vs 34) and its mock-rejections higher (13 vs 2): writes are mocked by design and create-tools
have complex required parameters. Every read-only call on a connected toolkit still ran for real,
13 of 13, so the gate is behaving.

**Run 8 — the full 100.** 384 queries, no quota stop, no abandons, 97/100 clean finishes. Two crashes
during the first attempt produced three harness fixes worth keeping: `arguments_json` can arrive as a
dict rather than a JSON string (only `JSONDecodeError` was caught, so a `TypeError` killed the run at
task 51 after 25 minutes); `main()` now guards each task so one failure cannot cost the other 99; and
completed traces are skipped on restart, so a late crash no longer discards an hour of work.

| | Run 7 (20 tasks) | Run 8 (100 tasks) |
|---|---:|---:|
| Judged group recall | 75% | **83%** |
| Strict group recall | 67% | **75%** |
| Delivered as `primary` | 46% | **56%** |
| Flat union recall | 52% | 61% |

983 logged tools reduce to 433 capabilities, 189 dropped outright as probes, proxies or duplicates.

The finding that only the full set could establish: **judged recall barely varies with task size**
(84% / 83% / 82% across ≤6, 7-13 and ≥14 reference tools), whereas flat recall on 20 tasks had shown
a collapse from 69% to 38%. That collapse was an artefact — larger tasks carry more log noise, so
they accumulate more phantom misses. It disappears once capabilities replace log entries.

Scoring needed `MAX_GROUPS` raised from 8 to 12; complex tasks legitimately need more groups, and 8
rejected three tasks outright. Two tasks remain unscored where the grouping stage could not produce
a clean label.
