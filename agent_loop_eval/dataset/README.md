# Agent-loop search dataset

What an LLM agent searched for while working through 100 real automation tasks, what
Composio's `COMPOSIO_SEARCH_TOOLS` returned, and whether the right tool came back.

Two runs are included, told apart by the `run` column:

| Run | What it is | Tasks | Tasks scored | Queries | Capabilities |
|---|---|---:|---:|---:|---:|
| `run8_full_100tasks` | Baseline agent loop | 100 | 98 | 384 | 433 |
| `run9_retry_loop` | Same, but the agent may retry a step up to 4 times if the tool it ran did not do the job | 100 | 86 | 461 | 381 |

Tasks come from [`src/top-100-eval-use-cases.md`](../../src/top-100-eval-use-cases.md).
Search returns two lists per query: `primary` (what it recommends) and `related` (other
candidates). Agents generally act on `primary`.

## Files

**`queries.csv`** — one row per search query the agent issued.

| Column | Meaning |
|---|---|
| `task` | The task the agent was working on |
| `query`, `intent` | What the agent searched for, and the step it said the search was for |
| `attempt`, `is_retry` | Run 9 only: which attempt at this step (1–4) |
| `primary_tools`, `related_tools` | What search returned, `; `-separated |
| `correct_in_primary`, `correct_in_related` | Which returned tools were correct for this task |
| `result` | `correct tool in primary` / `correct tool only in related` / `no correct tool returned` |
| `capabilities_served` | Which required capabilities this query returned a correct tool for |
| `scoring_basis` | What "correct" was checked against (see below) |

**`capabilities.csv`** — one row per capability a task requires.

| Column | Meaning |
|---|---|
| `capability` | One thing the task needs done, e.g. "Create a pull request" |
| `acceptable_tools` | Any one of these satisfies it |
| `outcome` | `delivered as primary` / `delivered only in related` / `delivered (judge accepted a different tool)` / `not delivered` |
| `matched_tools`, `delivering_query` | The tool that satisfied it, and the first query that returned it |
| `fault` | For `not delivered`: `agent: never searched for it`, `agent: query too vague to find it`, `search: fair query, tool not returned`, or `catalogue: no tool provides this` |
| `targeting_query`, `search_returned` | The query meant to find it, and what search gave back |
| `judge_reason`, `fault_reason` | The LLM judge's explanation |

**`tasks.jsonl`** — one JSON object per task with everything above nested, plus the tools
the agent actually executed and how the task ended.

## How "correct" was decided

A task's `Tools:` list in the source file is a log of one past session — it includes auth
probes, retries and fallbacks, not just what the task needs. So each task was first reduced
to **requirement groups**: the distinct capabilities it needs, each with the tools that would
satisfy it. A query is correct if it returns any tool in any of the task's groups.

16 tasks (2 in run 8, 14 in run 9) could not be grouped. For those, `scoring_basis` reads
`reference Tools list (task not scored)` and queries are checked against the raw list, which
is looser. They have no rows in `capabilities.csv`.

## Caveats

- `delivered (judge accepted a different tool)` and every `fault` label come from an LLM
  judge. The split between agent fault and search fault has been revised several times
  during this project; treat it as approximate. Whether a tool appeared in `primary` or
  `related` is plain set membership and is exact.
- Tool calls were mostly mocked: write tools never ran for real, and read tools ran for real
  only on the few connected accounts. The agent was judged on what it *searched for*, not on
  real side effects.

Regenerate with `python agent_loop_eval/build_dataset.py`.
