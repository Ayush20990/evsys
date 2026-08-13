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

## Resolved: the terse queries were a prompt defect, not agent behaviour

Two earlier runs produced single-word searches (`'email'`, `'workflow'`) and were nearly written up
as a finding about how agents phrase queries. They were a defect in this harness, now fixed. The
diagnosis came from an obvious anchor that had been sitting in the repo the whole time: the primary
benchmark's one-shot `DECOMPOSE_PROMPT` gets well-formed queries out of *the same* flash-lite model.
So the model was never the constraint.

Comparing the two prompts showed the working one constrains **specificity** — "concrete, realistic
search queries", "a specific action or lookup" — and separately requires an `intent` sentence per
query. The agent prompt had neither. Its first version instead constrained **brevity** ("ONE
capability at a time", "one focused query"), and removing that guidance without adding a quality bar
left the queries just as bare, which is what made the model look like the culprit. Specificity and
brevity are separate axes; only the first one should be constrained.

The fix ports both properties across: `search_tools` now takes `intent` alongside `query`, and asks
for a concrete description while saying nothing about length.

| | Run 2 (defective prompt) | Run 3 (fixed) |
|---|---|---|
| Task-1 queries | `'hubspot'`, `'payment'`, `'email'`, `'workflow'` | `'HubSpot create marketing email'`, `'HubSpot create custom object definition schema'` |
| Words per query | 2.9 | **5.6** |
| Slug-lookup queries | 11% | **0** |
| Union recall | 67% | **74%** |
| Primary-only recall | 34% | **46%** |

The lesson is methodological: two runs' worth of results were shaped by prompt wording, and the
symptom looked like a model limitation. Anything measured through an LLM harness is a property of the
harness until a known-good configuration says otherwise.

## Historical: the retracted query-distribution claim

Same 9 tasks, both methods:

| | One-shot imagined | Agent-issued |
|---|---:|---:|
| Queries per task | 3.2 | 9.2 |
| Words per query | 6.0 | 2.9 |

The loop issues ~3x more queries, each about half as long: keyword fragments (`"payment link"`,
`"hubspot email"`) rather than sentences (`"check payment link capabilities and configuration"`).

**This claim is withdrawn — the cause was the prompt (see the resolved section above).** The tell was
visible at the time: from a task that says *"create a review-only automated confirmation email"* and
*"create a disabled confirmation workflow"*, the agent searched `'email'`, `'workflow'`,
`'custom object'`. That is severe context loss, not a plausible way for any agent to phrase a search.
With the prompt fixed, the same model and the same task produce `'HubSpot create marketing email'`,
and words-per-query lands at 5.3 against the imagined 6.0 — so the length difference was never real.
What survives is the query *count*: 8.8 per task versus 3.2 imagined.

### How the wrong conclusion nearly got locked in

Worth keeping, because the reasoning failed in a specific and repeatable way.

**Step 1 — blamed the prompt, correctly.** The original prompt said *"Search for ONE capability at a
time"* and *"Issue one focused query describing the single capability you need right now"*: three
instructions to atomise queries. Reporting the resulting fragments as agent behaviour would have been
circular.

**Step 2 — removed it, and drew the wrong lesson from the result.** With that guidance stripped, the
tool description said only *"Search the tool catalogue for tools you could use."* Terseness did not
change, and that was recorded as *"the prompt was not the cause"*. The actual explanation: removing
the brevity instruction left **no quality bar at all**, so nothing pulled the queries toward being
specific. Constrain-brevity and constrain-nothing produce the same bare output for different reasons.

**Step 3 — blamed the model, on evidence that looked strong.** Terseness reproduced everywhere
reachable: `gemini-3.5-flash-lite` gave `'hubspot'`, `'payment'`, `'email'`; `gemini-3.5-flash` gave
`'hubspot'`, `'hubspot email'`; `gemini-3-flash-preview` gave the keyword bag
`'hubspot payment email workflow custom object'`. `gemini-2.5-pro` and `2.5-flash` were retired (404),
and `3.1-pro-preview`, `pro-latest`, `flash-latest` were all quota-exhausted. Consistency across three
tiers looked like a model property. It was really the same defective harness applied three times —
every configuration shared the one variable that mattered.

**What resolved it:** the primary benchmark's `DECOMPOSE_PROMPT` already produced good queries from
the *same* flash-lite model. One known-good configuration in the same repo beat three consistent
readings from the broken one. The general form: reproducing a result across models says nothing if
every run shares the harness under suspicion.

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

Three runs over the same 10 tasks. **Run 3 is the current one**; 1 and 2 are kept because the
differences between them are what exposed two harness defects.

| | Run 1 real reads | Run 2 mocked | Run 3 mocked + fixed prompt |
|---|---:|---:|---:|
| Queries | 85 | 95 | 86 |
| Words per query | 2.9 | 2.9 | **5.6** |
| Connection-hunting | 18 (21%) | 0 | **0** |
| Slug-lookup queries | 9 (11%) | 10 (11%) | **0** |
| Union recall | 56/92 (61%) | 62/92 (67%) | **68/92 (74%)** |
| Primary-only recall | 25/92 (27%) | 31/92 (34%) | **42/92 (46%)** |

*Union recall* = reference tool appeared anywhere in a response (`primary` ∪ `related`) across the
session. *Primary-only* = it appeared in `primary_tool_slugs`.

**Run 3's 74% is a floor, not a measurement.** Six tasks hit the 18-step ceiling and one exhausted
the Gemini quota, so seven of ten stopped before finishing. Truncated tasks cannot search for
capabilities they never reached. On the five tasks scored mid-run before truncation dominated, union
recall was 94% — tasks 2, 3 and 4 each hit 100% (6/6, 4/4, 10/10). Raising `MAX_STEPS` is the single
change most likely to move this number.

**Note on comparability:** these are scored against each use case's full reference tool list, which is
a different ground truth from the primary benchmark's requirement groups. Do not compare 74% against
that benchmark's 62.2%/81.3% — they measure different things.

### Finding 1: the right tool is usually found, but only half the time recommended

Union 74% vs primary-only 46%. Search *has* the correct tool far more often than it *promotes* it;
the rest are demoted to `related`. The gap has held across all three runs — 61/27, 67/34, 74/46 —
which spans wildly different query quality, so it is a property of the ranking rather than an
artifact of any one run's phrasing. For an agent that acts on the primary recommendation, a demoted
correct answer costs nearly as much as a miss. **This is the most robust finding here.**

### Finding 2: naming the vendor does not prevent cross-vendor drift

Run 2's version of this was weak: the agent searched a bare `"payment link"` on a HubSpot task and
got Stripe back, which is arguably fair given the query. Run 3 removed that excuse — the query was
`"HubSpot list payment links ecommerce"`, with the vendor stated explicitly, and search still
returned `STRIPE_LIST_PAYMENT_LINKS` as the primary result. An immediately following
`"HubSpot list payment links"` returned `HUBSPOT_LIST_EMAILS`. Explicit vendor scoping in the query
is not reliably respected.

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

- **Raise `MAX_STEPS` above 18.** Seven of ten tasks in run 3 stopped early, so 74% union recall is a
  floor set by truncation rather than by retrieval.
- Complete the OAuth flow (auth configs exist; connected accounts are still 0) to get real read
  execution and genuine recovery queries.
- Feed agent-issued queries back into the primary benchmark's scoring to measure retrieval against
  realistic phrasing rather than imagined phrasing.
- Extend past 10 tasks once the above is settled.
