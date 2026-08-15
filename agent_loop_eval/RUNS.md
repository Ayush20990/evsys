# Run index

Five runs exist. They differ in execution policy, prompt quality and task count, so only some pairs
are comparable. `run5_real_reads_20tasks/` is current.

| Folder | Execution | Tasks | Queries | Union | Primary | What it is for |
|---|---|---:|---:|---:|---:|---|
| `run1_real_reads_unconnected/` | real attempted, 0 connections | 10 | 85 | 61% | 27% | why gating on `readOnlyHint` alone fails |
| *(run 2, superseded)* | fully mocked | 10 | 95 | 67% | 34% | not kept — same prompt defect as run 1 |
| `run3_fully_mocked/` | fully mocked | 10 | 86 | 74% | 46% | mocked baseline |
| `run4_real_reads/` | real reads, 9 toolkits | 10 | 37 | — | — | quota died at task 7; superseded by run 5 |
| `run5_real_reads_20tasks/` | real reads, 9 toolkits | **20** | 94 | 49% | 21% | **current**; first run with completion tracking |

Headline percentages are not comparable across rows with different task counts — see below.

## Reading run 5

**49% union is not a drop from run 3's 74%.** Run 5 covers 20 tasks, and tasks 11-20 have much larger
reference tool lists. On tasks 1-10 alone:

| | Queries | Union | Primary | Union hits per query |
|---|---:|---:|---:|---:|
| run 3 (mocked) | 86 | 68/92 (74%) | 42/92 (46%) | 0.79 |
| run 5 (real reads) | 50 | 58/92 (63%) | 27/92 (29%) | **1.16** |

Run 5 issued 42% fewer queries and found 1.16 useful tools per query against run 3's 0.79. Real data
lets the agent stop searching once something works, so session-level recall falls while per-query
quality rises. **Session recall is a function of how many queries a task happens to produce**, which
makes it unsafe to compare across runs with different execution policies. Hits-per-query is the
fairer statistic.

## Finding: query count does not scale with task complexity

Grouping run 5's 20 tasks by the size of their reference tool list:

| Reference tools | Tasks | Union recall | Mean queries/task |
|---|---:|---:|---:|
| ≤ 6 | 6 | 69% | 4.5 |
| 7-13 | 8 | 59% | 4.1 |
| ≥ 14 | 6 | **38%** | 5.7 |

Recall collapses on complex tasks while the query count stays almost flat. A task needing 25 tools
gets 5.7 queries — the agent does not search more when there is more to find.

This matters beyond this benchmark: it is the same coverage failure the primary benchmark fixed with
its dynamic cap, `ceil(pool_size / TOOLS_PER_QUERY_TARGET)`. Letting query count emerge from agent
behaviour is more realistic, but it is *not* automatically better coverage — an emergent count
under-samples exactly the tasks where retrieval is hardest. The two benchmarks fail in opposite
directions, and neither number should be read without that context.

## Task completion (new in run 5)

The agent calls `finish_task` when it stops, reporting `completed`, `unmet_steps` and `blocked_by`.
The `blocked_by` split exists because "did not complete" conflates unrelated causes:

| blocked_by | Count | Counts against search? |
|---|---:|---|
| `not_blocked` | 11 | n/a — completed |
| `data_absent` | 8 | **no** — the tool existed, the account had no such record |
| `no_suitable_tool` | 1 | would be yes, but see below |

11 of 20 tasks completed. Nearly every failure was `data_absent`, which is expected: these tasks were
written against accounts we do not have, so correct tools legitimately return nothing.

**The single `no_suitable_tool` report does not survive inspection.** Task 11 found
`ONE_DRIVE_SEARCH_ITEMS`, `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE`, `DISCORDBOT_CREATE_MESSAGE` and
`GMAIL_CREATE_LABEL`, then declared all five of its steps unmet. Only step 4 genuinely failed
(`"Read queue and system state files"` returned `CLORO_GET_ASYNC_QUEUE_STATUS`, an unrelated product)
and the agent generalised that to the whole task. Self-reported completion is a weak signal on its
own — read it next to the recall numbers, never instead of them.

## Execution in run 5

15 real, 43 mocked, 11 mock-rejected, 4 empty reads. Real execution stays a minority because most
reference tools are writes, which are mocked by design, and because 11 of the 20 tasks use toolkits
that are not connected.

- **0 infrastructure fallbacks** — the session's connected-account binding held throughout.
- **0 slug-lookup queries**, 6.1 words per query — prompt quality is stable across runs 3-5.
- **4 empty reads** correctly flagged, with no false recovery queries.

## Fix carried into run 5: discovery continues past a blocked step

Earlier runs let a missing file suppress the searches for everything downstream of it. If a task says
fetch a file, edit it and upload it, and no such file exists, the agent would stop — and the edit and
upload tools would score as retrieval misses despite search never being asked for them.

The prompt now requires searching for a step's tool even when the step cannot be carried out.
Verified on task 3 (OneDrive, no spreadsheet present): the agent searched for the download, upload and
verify tools anyway and scored 4/4 union recall while correctly reporting `data_absent`.

## Layout

Each run directory holds per-task traces (`task-0NN.json`), `agent_queries.json`, `summary_report.md`
and the run log. `run3_vs_run4_queries.md` is a query-by-query side-by-side of the mocked and
real-read runs.

A new run writes to `traces/` and overwrites `agent_queries.json` / `summary_report.md` at the top
level — archive those into a `runN_*/` directory before starting another, or the previous run is lost
(run 3's traces had to be recovered from git after exactly that).

## Caveat on real-read traces

Runs 4 and 5 executed real reads, so traces may contain fragments of real account data reachable via
the agent's later queries and its `final_message`. Execution *results* are never stored — only
`tool_slug`, `arguments` and `mode`. A scan for emails and URLs in run 4 came back clean; re-check
before publishing anywhere public.
