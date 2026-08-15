# Agent-loop query benchmark

Records the search queries an LLM issues while *actually working* a task, instead of asking it to
predict them up front. Built to answer a review point: predicted queries may not resemble what a real
agent issues, and a prediction never sees a search result so it can never react to one.

Tasks come from the first 20 entries of `../src/top-100-eval-use-cases.md`.

```powershell
python agent_loop_evaluation.py                    # run the loop, writes traces/
python score_with_groups.py run6_descriptions_20tasks   # score an existing run
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

## Current results — `run6_descriptions_20tasks`

| Metric | Value |
|---|---:|
| **Judged group recall** | **62/88 (70%)** |
| Strict group recall | 54/88 (61%) |
| Groups delivered as `primary` | 40/88 (45%) |
| *Flat union recall (superseded metric)* | *106/229 (46%)* |
| Queries | 73 across 20 tasks, 6.4 words each |
| Executions | 34 real, 20 mocked, 2 rejected |
| Tasks completed | 11/19 reporting; 8 blocked by `data_absent` |
| Search-failure stops | 0 |

229 logged tools collapse to **88 real capabilities**. Task 13 is typical: flat recall 3/13, group
recall 3/4 — ten of those thirteen entries were never requirements.

### Finding 1: found, but not recommended

70% of required capabilities were delivered, but only **45%** arrived as a `primary` recommendation —
the rest were demoted to `related`. The gap has held across every run and both scoring methods, so it
is a property of the ranking, not of query phrasing. For an agent that acts on the primary
recommendation, a demoted correct answer costs about what a miss costs. **This is the strongest
finding here.**

### Finding 2: naming the vendor does not scope the search

`"HubSpot list payment links ecommerce"` returned `STRIPE_LIST_PAYMENT_LINKS` as its primary result;
the next query, `"HubSpot list payment links"`, returned `HUBSPOT_LIST_EMAILS`. Explicit vendor
scoping in the query text is not reliably respected.

### Finding 3: confirmed capability gaps

Groups the judge confirmed search never delivered, having checked every tool actually returned:

- **Task 5** — fetching and reading Gmail messages. Returned Gmail tools were, in the judge's words,
  "strictly limited to managing drafts".
- **Task 4** — three Trello capabilities: add a comment to a card, move a card between lists, add a
  list to a board.
- **Task 6** — bulk record creation in Salesforce (`POST_COMPOSITE_SOBJECTS`).

### Finding 4: a catalogue defect

`HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT` and
`HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUB_SPOT_ACCOUNT` are both live and non-deprecated with
identical display names and descriptions. A curated list can therefore name a slug search will never
return, because search surfaces the twin. Worth reporting upstream.

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

## Known issue: the circuit breaker ends the whole task

Thrashing — repeatedly searching for one capability that never returns anything usable — trips a
breaker that stops the task. **It should skip that capability and continue to the next step, but
currently it returns and the runner moves to the next task.**

This is the same defect already fixed for absent data, arriving through a different door: steps after
the stuck one are never searched for, and then score as retrieval misses although search was never
asked. Nothing reported here is affected — the breaker fired zero times in run 6 — but it must be
fixed before a run where it does fire.

The fix is to inject a corrective message ("stop searching for this capability, record it unmet, move
on") instead of returning, keeping a hard stop only as a much higher backstop.

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
| `run6_descriptions_20tasks/` | **current run** — traces, queries, reports |
| `RUNS.md` | run index and what each earlier run established |

Each run directory holds per-task traces, captured queries, the generated reports, and the run log.
A new run writes to `traces/` and overwrites the top-level report files, so archive them into a
`runN_*/` directory before starting another.

Traces from runs with real reads may contain fragments of real account data via the agent's queries
and summaries; execution *results* are never stored. A scan for emails and URLs came back clean, but
re-check before publishing anywhere public.
