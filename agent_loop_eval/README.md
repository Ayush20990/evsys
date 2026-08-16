# Agent-loop query benchmark

Records the search queries an LLM issues while *actually working* a task, instead of asking it to
predict them up front. Built to answer a review point: predicted queries may not resemble what a real
agent issues, and a prediction never sees a search result so it can never react to one.

Tasks come from the first 20 entries of `../src/top-100-eval-use-cases.md`.

```powershell
python agent_loop_evaluation.py                        # run the loop, writes traces/
python score_with_groups.py run7_continue_after_stuck  # requirement-group + judge scoring
python analyse_failures.py run7_continue_after_stuck   # failure classes + agent/judge conflicts
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

## Current results — `run7_continue_after_stuck`

| Metric | Run 6 | Run 7 |
|---|---:|---:|
| **Judged group recall** | 70% | **63/84 (75%)** |
| Strict group recall | 61% | **56/84 (67%)** |
| Groups delivered as `primary` | 45% | 39/84 (46%) |
| *Flat union recall (superseded)* | *46%* | *119/229 (52%)* |
| Queries | 73 | 82 |
| Tasks reaching a clean finish | 19/20 | **20/20** |
| Capabilities abandoned | n/a | 0 |

229 logged tools collapse to **84 real capabilities**. Every task ended with the agent calling
`finish_task` — no step ceilings, no quota stops, no search-failure stops.

Failure breakdown, from `failure_analysis.md`:

| Outcome | Count | Meaning |
|---|---:|---|
| Delivered on `primary` | 39 | search recommended the right tool |
| **Delivered only in `related`** | **17** | search *held* the right tool and never promoted it |
| Credited alternative | 7 | judge accepted a tool the logged list never named |
| `never-returned` | 16 | no acceptable tool appeared in any result |
| `catalogue-gap` | 5 | the task needs this and no logged tool provides it either |

### Finding 1: found, but not recommended

75% of required capabilities were delivered; only **46%** arrived as a `primary` recommendation. The
17 demoted capabilities are the single largest correctable failure class — search already has those
tools, it just ranks them below the fold. An agent acting on the primary recommendation misses them.
The gap has held across every run and both scoring methods.

### Finding 2: the agent cannot tell it picked wrong

`agent_vs_judge.md` lists calls where the agent **stated** it was carrying out a step, and an
independent judge ruled that capability was never delivered. Seven cases in run 7. These are
invisible to recall — the agent records success and later steps build on a false premise:

- Task 1 — stated *"Assess payment-link feasibility in HubSpot"*, ran
  `HUBSPOT_CREATE_FEEDBACK_SUBMISSION`.
- Task 16 — stated *"Get Vercel deployments"* for a capability requiring Cloudflare zones and DNS.
- Task 17 — ran `LINKEDIN_CREATE_LINKED_IN_POST` for a capability requiring Instagram publishing,
  and `GOOGLECALENDAR_CREATE_EVENT` for a spreadsheet-backed booking schedule.

The pattern is cross-vendor substitution: a plausible tool from the wrong application. Mocked
execution cannot correct this without consulting the ground truth, which would leak the answer key,
so it can only be detected after the fact by comparing the agent's own claim against the judge.

### Finding 3: naming the vendor does not scope the search

`"HubSpot list payment links ecommerce"` returned `STRIPE_LIST_PAYMENT_LINKS` as its primary result;
the next query, `"HubSpot list payment links"`, returned `HUBSPOT_LIST_EMAILS`.

### Finding 4: a catalogue defect

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
| `run7_continue_after_stuck/` | **current run** — traces, queries, all reports |
| `RUNS.md` | run index and what each earlier run established |

Each scored run carries `group_scoring_report.md` (recall), `failure_analysis.md` (why each
capability was missed, plus the demoted list) and `agent_vs_judge.md` (calls the agent believed
worked that the judge rejected).

Each run directory holds per-task traces, captured queries, the generated reports, and the run log.
A new run writes to `traces/` and overwrites the top-level report files, so archive them into a
`runN_*/` directory before starting another.

Traces from runs with real reads may contain fragments of real account data via the agent's queries
and summaries; execution *results* are never stored. A scan for emails and URLs came back clean, but
re-check before publishing anywhere public.
