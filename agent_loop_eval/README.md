# Agent-loop query benchmark

Captures the search queries an LLM issues while *actually working* a task, instead of asking it to
imagine them up front. Built to answer a specific critique: the queries the primary benchmark scores
against don't look like the queries a real agent produces.

Tasks come from the first 10 entries of `../src/top-100-eval-use-cases.md`.

## Why this exists

`../src/query_level_workflow_evaluation.py` asks Gemini, in one shot, to predict the queries an agent
*would* issue for a task. That prediction never sees a search result, so it can't react to one. This
script runs a real tool-calling loop instead: the model gets the task and two tools, and whatever it
searches for while genuinely trying to make progress is what gets recorded. Query count is emergent —
no cap, no `ceil(pool_size / 2.5)` formula.

## The query-distribution difference — measured, but NOT yet explained

Same 9 tasks, both methods:

| | One-shot imagined | Agent-issued |
|---|---:|---:|
| Queries per task | 3.2 | 9.2 |
| Words per query | 6.0 | 2.9 |

The loop issues ~3x more queries, each about half as long: keyword fragments (`"payment link"`,
`"hubspot email"`) rather than sentences (`"check payment link capabilities and configuration"`).

**Do not read this as "agents query in keywords."** The cause is unestablished, and at least one
strong candidate is this harness rather than agent behaviour. Task 1 makes the problem obvious — from
a task that says *"create a review-only automated confirmation email"* and *"create a disabled
confirmation workflow"*, the agent searched `'email'`, `'workflow'`, `'custom object'`. Single generic
words. That is severe context loss, not plausible agent behaviour.

### Cause 1 — the prompt: TESTED, REJECTED

The original `SYSTEM_PROMPT` said *"Search for ONE capability at a time"* and `SEARCH_DECLARATION`
said *"Issue one focused query describing the single capability you need right now"* — three separate
instructions to atomise queries. Reporting the resulting atomisation as a property of agents would
have been circular.

Both were removed; the tool description now says only *"Search the tool catalogue for tools you could
use."* **The terseness did not change.** Task 1 still produced `'hubspot'`, `'payment'`, `'email'`,
`'workflow'`, `'schema'`, `'marketing'` — and repeated `'email'` twice while issuing `'HUBSPOT'`
directly after `'hubspot'`. The prompt was not the cause.

### Cause 2 — model tier: REPRODUCES ACROSS EVERY MODEL REACHABLE

| Model | Task-1 queries |
|---|---|
| `gemini-3.5-flash-lite` | `'hubspot'`, `'payment'`, `'email'`, `'workflow'`, `'custom object'` |
| `gemini-3.5-flash` | `'hubspot'`, `'hubspot email'`, `'hubspot workflow'` |
| `gemini-3-flash-preview` | `'hubspot payment email workflow custom object'` (keyword bag, not a sentence) |
| `gemini-2.5-pro`, `gemini-2.5-flash` | retired — 404 |
| `gemini-3.1-pro-preview`, `gemini-pro-latest`, `gemini-flash-latest` | quota exhausted, untestable |

Every reachable model produces keyword-style queries. The larger preview model produces *longer*
queries but still concatenated keywords rather than natural phrasing.

### What this actually licenses you to say

**"Gemini flash-tier models issue keyword-fragment queries."** That is supported.

**"Agents issue keyword-fragment queries."** That is *not* supported. No pro-tier model was
reachable, and nothing here speaks to how a Claude- or GPT-class agent phrases searches. Treat the
3.2 → 9.2 queries-per-task and 6.0 → 2.9 words-per-query figures as properties of this harness on
flash-tier Gemini, not as a discovered fact about agents. Confirming or killing the claim needs a
pro-tier or non-Gemini model.

The recall and derailment results are unaffected — they depend on which queries were issued, not on
why they were phrased that way.

See `agent_vs_imagined.md` for the side-by-side.

## Two scoring hazards found by inspection

**Slug-lookup queries (fixed by flagging).** The agent sometimes searches for a tool slug verbatim
(`'HUBSPOT_CREATE_WORKFLOW'`) after seeing it in an earlier response. Search returns it by exact
match, so it tests lookup rather than retrieval, and the scorer counted it as a hit. These were 11%
of queries in both runs. Excluding them moves run 2 from 67%→66% union and 34%→32% primary — small,
but the headline figures are the *un*corrected ones. Queries now carry `is_slug_lookup` so scoring
can drop them.

**The mock rubber-stamped invalid calls (fixed).** `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL` was called
with *no arguments at all* and the mock returned success, so the agent proceeded believing it had
created an email. The mock now validates arguments against the tool's declared `required` input
parameters and returns a failure when any are missing — a pure schema check that never consults the
ground truth, so it cannot leak the answer key. It immediately caught
`HUBSPOT_CREATE_OBJECT_SCHEMA` being called with all four required parameters missing.

## Results

Two runs over the same 10 tasks. They differ only in execution policy.

| | Run 1 — real reads, unconnected | Run 2 — fully mocked |
|---|---:|---:|
| Queries | 85 | 95 |
| Connection-hunting queries | 18 (21%) | **0 (0%)** |
| Tool executions | 16 (12 failed) | 52 (all mocked) |
| Union recall | 56/92 (61%) | **62/92 (67%)** |
| Primary-only recall | 25/92 (27%) | **31/92 (34%)** |

*Union recall* = reference tool appeared anywhere in a response (`primary` ∪ `related`) across the
session. *Primary-only* = it appeared in `primary_tool_slugs`.

**Note on comparability:** these are scored against each use case's full reference tool list, which is
a different ground truth from the primary benchmark's requirement groups. Do not compare 67% against
that benchmark's 62.2%/81.3% — they measure different things.

### Finding 1: half the correct tools are demoted to `related`

Search surfaces the right tool 67% of the time but promotes it to `primary` only 34% — roughly half
the correct answers are present but not recommended. This is stable across both runs (61/27 and
67/34), so it's a property of the ranking, not an artifact of run 1's derailment. For an agent that
mostly acts on the primary recommendation, a demoted correct answer is close to a miss.

### Finding 2: bare-capability queries drift across vendors

The agent frequently drops the vendor from its query. In task 1 (a HubSpot task) it searched
`"payment link"`, got `STRIPE_*` / `GOCARDLESS_*` / `RAZORPAY_*` back, and by query 10 had abandoned
HubSpot entirely for `"stripe create payment link"`. This is the same cross-vendor drift already
noted in `../read.md`, but arising from the *agent's own* phrasing rather than the decomposer's — so
it's a real retrieval-side property, not a generation artifact.

### Finding 3: the readOnlyHint gate was wrong, and why

Run 1 gated real execution on Composio's `readOnlyHint` tag alone. That tag answers *"is this safe to
run?"* — it does not answer *"can this actually run?"* With 15 auth configs but **0 connected
accounts**, every real read returned:

```
400 - No active connection found for toolkit(s) 'hubspot' in this session.
      To fix this, call COMPOSIO_MANAGE_CONNECTIONS ...
```

The agent then *correctly obeyed* that instruction, searched `"COMPOSIO_MANAGE_CONNECTIONS"`, got
`RAGIE_LIST_CONNECTIONS` / `CELIGO_REGISTER_CONNECTION` / `PRISMA_CREATE_CONNECTION` back, and
abandoned the task. 12 of 16 executions failed this way and 21% of all queries were consumed by it.

This reproduces the "the LLM stopped acting as an agent mid-session" failure that motivated this
work. The cause is not an LLM quirk: the API embedded an instruction in its error, and the agent
followed it.

Run 2 gates on **both** conditions — `readOnlyHint` **and** a live connected account — so with no
connections everything mocks. Derailment went to zero and recall rose ~7 points on both measures,
with the same search engine and the same tasks.

## Execution policy

A tool runs for real only when it both carries `readOnlyHint` (cannot write) and belongs to a toolkit
with a live connected account (can authenticate). Everything else gets a mock generated from the
tool's declared `output_parameters`, so it is structurally indistinguishable from a real response.
Connected toolkits are detected at startup, so completing the OAuth flow later switches real reads on
automatically with no code change.

**Known limitation.** The mock succeeds on any syntactically valid call. It cannot know a tool is the
*wrong* tool without consulting the ground truth being evaluated, and consulting it would leak the
answer key into trace generation — the agent would be corrected by an oracle it wouldn't have in
production. The cost is that wrong-tool picks don't trigger self-correction, so recovery queries are
undersampled. Connecting accounts recovers this on the read path, where failures become genuine.

## Files

| Path | What |
|---|---|
| `agent_loop_evaluation.py` | The loop. `python agent_loop_evaluation.py` |
| `compare_with_imagined.py` | Builds `agent_vs_imagined.md` |
| `summary_report.md` | Run 2 report, incl. every query issued |
| `agent_vs_imagined.md` | Side-by-side vs the one-shot decomposition |
| `agent_queries.json` | Captured queries, machine-readable |
| `traces/` | Full per-task traces (run 2) |
| `run1_real_reads_unconnected/` | Run 1, kept for the comparison above |

## Ground truth is never shown to the agent

The model receives the task text and nothing else — `case.task` is the sole content of the opening
message, and the system prompt names no tool, toolkit or vendor. Each use case's reference tool list
(`case.tools`) is carried only on the trace object and written to `agent_queries.json`, both consumed
*after* the run for offline scoring. Verified by inspection of the prompt-construction path; worth
re-checking if that path is ever edited, since leakage there would silently invalidate every recall
number here.

## Next

- **Resolve the query-phrasing question above before quoting the distribution numbers.** Neutral
  prompt wording plus a frontier model; that is the blocking item.
- Complete the OAuth flow (auth configs exist; connected accounts are still 0) to get real read
  execution and genuine recovery queries.
- Feed agent-issued queries back into the primary benchmark's scoring to measure retrieval against
  realistic phrasing rather than imagined phrasing.
- Extend past 10 tasks once the above is settled.
