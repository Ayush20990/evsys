# Agent-loop query benchmark

Records the search queries an LLM issues while *actually working* a task, instead of asking it to
predict them up front. Built to answer a review point: predicted queries may not resemble what a real
agent issues, and a prediction never sees a search result so it can never react to one.

Tasks come from `../src/top-100-eval-use-cases.md` — all 100 as of the current run.

```powershell
python agent_loop_evaluation.py                        # run the loop, writes traces/
python score_with_groups.py run8_full_100tasks  # requirement-group + judge scoring
python analyse_failures.py run8_full_100tasks   # failure classes + agent/judge conflicts
```

## How it works

The model gets a task and three tools — `search_tools`, `execute_tool`, `finish_task` — and works the
task step by step. Every query it issues is recorded. Query count is emergent; there is no cap and no
`ceil(pool_size / 2.5)` formula.

**Search results carry full tool descriptions and parameter schemas.** A real agent never picks from
bare slugs: it reads what a tool does, and it cannot construct a call without the schema. This is
Composio's public catalogue data, so it adds realism without leaking anything about the reference
tools.

**Execution is mocked unless it can be real.** A tool runs for real only when it carries Composio's
`readOnlyHint` tag *and* its toolkit has an ACTIVE connected account under this `USER_ID`. Everything
else — all writes, and reads on unconnected toolkits — gets a mock built from the tool's declared
`output_parameters`, validated against its required inputs so invalid calls are rejected rather than
rubber-stamped. **Nothing is ever written to a connected account.**

Nine toolkits are connected: `cal`, `clickup`, `gmail`, `googlecalendar`, `linkedin`, `notion`,
`one_drive`, `salesforce`, `trello`.

## Scoring: requirement groups, not flat lists

The `Tools:` lists in the use-case file are **execution logs of past agent sessions, not requirement
sets**. Measured across all 100: every description narrates a past run, #32 states outright that "the
agent repeatedly used tool search to find tools", 13 task texts describe attempts rather than
successes, 51 of 100 contain three or more same-toolkit same-verb tools, and auth probes plus
`*_PROXY_EXECUTE` passthroughs are 3.4% of all 1008 entries.

Scoring recall against those lists is wrong in three ways at once:

| Defect in the list | Effect on flat recall |
|---|---|
| Logged-but-unnecessary tools (probes, proxies, retries) | too harsh |
| Valid alternatives the list never named | too harsh |
| Capabilities the task needs but the log never covered | **too generous** |

`score_with_groups.py` fixes all three by deriving requirements from the **task** rather than the log:

- **Stage A** — group the logged tools into requirement groups. Alternatives share a group; distinct
  capabilities get separate groups; superset noise is dropped. A capability with no listed tool still
  becomes a group, with an empty slug list.
- **Stage B (strict)** — a group is satisfied if search surfaced *any* tool in it.
- **Stage C (judged)** — unmet groups are re-checked against what search actually returned, so a
  correct tool the log never named still counts. Vendor-scoped, so a Stripe tool cannot satisfy a
  HubSpot need.

It reads saved traces, so re-scoring any completed run costs no agent quota.

## Current results — `run8_full_100tasks`

All 100 use cases, 384 queries, no quota stop and no crashes. 98 of 100 scored (two tasks the
grouping stage could not label cleanly).

| Metric | 20 tasks (run 7) | **100 tasks (run 8)** |
|---|---:|---:|
| **Judged group recall** | 75% | **359/433 (83%)** |
| Strict group recall | 67% | **324/433 (75%)** |
| Groups delivered as `primary` | 46% | **241/433 (56%)** |
| *Flat union recall (superseded)* | *52%* | *601/983 (61%)* |
| Queries | 82 | 384 (6.6 words each) |
| Clean finishes | 20/20 | 97/100 |
| Capabilities abandoned | 0 | 0 |

**983 logged tools collapse to 433 real capabilities** — 189 dropped outright as auth probes,
`PROXY_EXECUTE` fallbacks or duplicate variants, the rest merged into alternative groups. Flat recall
was measuring log noise for roughly half of what it counted.

### Finding 1: only 19 of 433 capabilities are true search-recall failures

Every unmet capability is attributed: which query was meant to find it, what search returned for
that query, and whether the query was good enough that search should have found it. The judgement is
made on the query alone, without showing the model the expected tools, so it cannot reason backwards
from the answer key.

| Fault | Count | Meaning |
|---|---:|---|
| **`search: returned it, but only in related`** | **83** | search *had* the tool and left it below the fold |
| `agent: never searched for it` | 28 | no query targeted this capability at all |
| **`search: fair query, tool not returned`** | **19** | **the true recall failure** |
| `catalogue: no tool provides this` | 18 | not a search bug |
| `agent: query too vague to find it` | 9 | searched, but no engine could resolve it |

**Agent-side 37 · search-side 102 · catalogue 18.**

The reframe matters: of 433 required capabilities, search genuinely failed to retrieve only **19
(4.4%)**. Its far larger problem is **ranking** — 83 capabilities where the right tool was returned
and never promoted. And 37 failures are the agent's own, fixable by better decomposition, which
would be misread as retrieval failures by any recall metric.

The clearest true recall failure, task 16:

```
capability : Modify repository code and create pull requests
query      : "Git repository file inspect and commit or pull request"
needed     : GITHUB_COMMIT_MULTIPLE_FILES, GITHUB_CREATE_A_PULL_REQUEST
returned   : GITHUB_GET_A_REPOSITORY, GITHUB_GET_A_TREE, GITHUB_GET_REPOSITORY_CONTENT,
             GITHUB_LIST_COMMITS, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
```

The query names the application and asks for commit and pull-request actions. Search returned nine
GitHub tools, every one of them read-only. The write tools it asked for exist and were not returned.

### Finding 2: recall is flat across task complexity, but `primary` is not

| Reference tools | Tasks | Judged | On `primary` | Queries/task |
|---|---:|---:|---:|---:|
| ≤ 6 | 29 | 84% | 60% | 2.9 |
| 7-13 | 47 | 83% | 52% | 3.9 |
| ≥ 14 | 22 | 82% | 59% | 4.9 |

Judged recall barely moves with task size — 84% / 83% / 82% — which is the opposite of what flat
recall showed on 20 tasks (69% / 59% / 38%). That collapse was an artefact of flat scoring: large
tasks carry more log noise, so they accumulate more phantom misses. Once capabilities replace log
entries, complexity stops mattering. **A concrete case for not scoring against the raw lists.**

### Finding 3: when the agent picks wrong, search usually left it no choice

`agent_vs_judge.md` — 17 cases where the agent **stated** it was carrying out a step and an
independent judge ruled that capability was never delivered. Invisible to recall: the agent records
success and later steps build on a false premise.

Split by whether a correct tool was sitting in the results the agent had already seen:

| | Count | Fault |
|---|---:|---|
| A correct tool was available and not chosen | 6 | agent: selection error |
| **No returned tool could do it** | **11** | **search: the agent had no option** |

Two thirds of the time the agent was not choosing badly — nothing it had been shown could do the
job, so it substituted the closest thing. The recurring shape is cross-vendor: a LinkedIn post tool
for an Instagram publish, a Calendar event for a spreadsheet-backed schedule.

### Finding 4: naming the vendor does not scope the search

`"HubSpot list payment links ecommerce"` returned `STRIPE_LIST_PAYMENT_LINKS` as its primary result;
the next query, `"HubSpot list payment links"`, returned `HUBSPOT_LIST_EMAILS`. A GitHub-only query
in run 8 returned two Trello tools among its results.

### Finding 5: a catalogue defect

`HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT` and
`HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUB_SPOT_ACCOUNT` are both live and non-deprecated with
identical display names and descriptions, so a curated list can name a slug search will never return.

### On comparing runs

Session-level recall is dominated by **query count**, not retrieval quality: a better agent searches
less, so its recall looks worse. Run 6 issued 22% fewer queries than run 5 while more than doubling
real executions and cutting argument errors from 11 to 2 — and its flat recall fell 3 points. Use
hits-per-query, or group recall, whenever query count is not held fixed.

Query count also fails to scale with task complexity: grouping run 5's tasks by reference-list size
gave 69% recall at ≤6 tools, 59% at 7-13, and 38% at ≥14 — while queries per task stayed near 4-6
throughout. An emergent query count under-samples exactly the hardest tasks, which is the same
coverage failure the primary benchmark fixed with its dynamic cap. The two benchmarks fail in
opposite directions.

## Search failure, and why a stuck step no longer ends the task

Two behaviours look alike from outside. **Front-loading** — several searches for *different*
capabilities before any execution — is healthy and explicitly asked for. **Thrashing** — re-asking
the same capability because nothing usable comes back — is not. A search counts as unproductive only
when it returns nothing or repeats a capability already asked; four consecutive of those, or a query
repeated past the limit, trips a breaker.

Tripping it **abandons that capability, not the task**: the agent is told to stop searching for it,
record it as unmet, and move to the next step. Only a task that stalls three times is stopped
outright. An earlier version returned immediately, which killed the task and skipped every remaining
step — the same defect already fixed for absent data, arriving by a different route, where unsearched
steps then scored as retrieval misses. The breaker fired zero times in run 7.

## Other limitations

- **Wrong-but-well-formed calls succeed.** The mock validates required parameters, not intent. It
  cannot know a tool is the wrong tool without consulting the ground truth being evaluated, and
  consulting it would leak the answer key. Real execution exposes this on the read path; the write
  path stays blind.
- **Self-reported completion is weak.** In run 5 one task reported `no_suitable_tool` after finding
  suitable tools for four of its five steps. Read completion alongside recall, never instead of it.
- **The accounts are not the tasks' accounts**, so correct tools often return empty. The agent is
  told this explicitly and still searches for later steps' tools, so recall is unaffected; completion
  is not, which is why `blocked_by` separates `data_absent` from `no_suitable_tool`.

## Layout

| Path | What |
|---|---|
| `agent_loop_evaluation.py` | the loop |
| `score_with_groups.py` | requirement-group + judge scoring |
| `analyse_failures.py` | failure classification and agent/judge disagreements |
| `run8_full_100tasks/` | **current run** — all 100 tasks, traces, queries, all reports |
| `RUNS.md` | run index and what each earlier run established |

Each scored run carries three reports:

- `group_scoring_report.md` — recall, strict and judged, per task.
- `failure_analysis.md` — every unmet capability with the query that was meant to find it, what
  search returned for that query, and a fault verdict.
- `agent_vs_judge.md` — calls the agent believed worked that the judge rejected, split by whether a
  correct tool was available to it.

**Attribution is an LLM judgement and is not perfect.** Borderline cases where a query overlaps a
capability without targeting it can still land on the wrong side. An earlier version of the adequacy
prompt graded "is this a well-formed query" rather than "does this query ask for this capability",
which blamed search for not returning Cloudflare DNS tools to a query about Vercel deployments, and
Sheets tools to a query about calendar events. Tightening it moved three cases from search to agent;
at least one vendor-overlap case is still classified as a search failure and is arguably the agent's.
Treat the 19 as an upper bound.

Each run directory holds per-task traces, captured queries, the generated reports, and the run log.
A new run writes to `traces/` and overwrites the top-level report files, so archive them into a
`runN_*/` directory before starting another.

Traces from runs with real reads may contain fragments of real account data via the agent's queries
and summaries; execution *results* are never stored. A scan for emails and URLs came back clean, but
re-check before publishing anywhere public.
