# Evsys

Evsys measures how well Composio's `COMPOSIO_SEARCH_TOOLS` finds the right tool for a search query: whether
it misses tools outright, ranks the right tool below wrong ones, confuses similar toolkits, is weak on
specific toolkits, or is slow.

## Why not just search the whole task

`top-100-eval-use-cases.md` gives 100 workflows, each with a description and a list of tools a human decided
were relevant to it somewhere. It's tempting to send that whole description to `COMPOSIO_SEARCH_TOOLS` as one
query and check whether the listed tools come back. That's the wrong test, for a simple reason: nobody
actually searches that way. An agent working through "prepare HubSpot launch assets for a paid event
registration flow" doesn't type that sentence into a tool search. It breaks the job into steps first — check
permissions, clone an email template, create a workflow — and searches for a tool at each step. The tool list
attached to a workflow is a pool of things that *might* get used somewhere in it, not the answer to one
search call.

So the benchmark works one level down from the workflow: it builds a search query for each step, and checks
retrieval against only the tool(s) that step needs.

## How a workflow turns into scored results

**Decomposition happens blind.** For a given task, an LLM call sees the task description only — no tool
list — and writes out the individual queries an agent would issue while working through it. This isn't a
minor detail: when the same call could see the candidate pool, its query wording started leaking pool
vocabulary. One early example: a query came out as "query ledger **entities**" because
`QUICKBOOKS_QUERY_ENTITIES` was sitting in view. Nobody says "entities" when describing a task to themselves;
that's the tool's internal name bleeding into what's supposed to be a natural query. Once the pool was
hidden from decomposition, the same step turned into "search quickbooks bank account ledger transactions" —
ordinary phrasing. How many queries a task gets is scaled to the size of its tool pool (roughly one query per
2–3 tools, with a floor and ceiling), but that's only used as a size hint — the pool's contents stay hidden.

**Labeling happens with full context, separately.** A second, independent call then sees those queries
alongside the candidate pool — but this time with each tool's actual description pulled live from Composio,
not just its slug. `GOOGLESUPER_FETCH_EMAILS` doesn't tell an LLM much by itself; its description does. For
every query, this call decides which pool tool(s) would genuinely satisfy it, and it's allowed to say none
of them do — a workflow's human-picked pool doesn't necessarily cover every sub-intent an agent might
generate from it, and forcing a bad match onto an uncovered query would corrupt the ground truth silently. A
query with no covering tool is recorded as "unlabelable" and left out of scoring.

Ground truth for a query is never a flat list. It's grouped: two tools that could each independently satisfy
the same need (say, either of two ways to search email) sit in one group, because either one is a full
success. Two operations that both have to happen (find an email *and* schedule a follow-up) become two
separate groups, because both are needed. A flat list can't tell these apart, and scoring one as if it were
the other either double-penalizes valid alternatives or lets a compositional query pass on half its work.

**A workflow only contributes test cases if both stages pass validation** — sane query counts, no invented
tool slugs, no query left unlabeled by the labeling call. A workflow that fails either check produces zero
test cases and gets logged with why, rather than partially poisoning the dataset.

**Scoring runs the query through search and checks group coverage.** A query's score is the fraction of its
requirement groups that search satisfied — group by group, not tool by tool, so alternatives inside a group
never get double-counted or under-counted. This is the strict score: it only credits what was pre-labeled.

**Anything strict scoring calls a miss gets a second opinion.** The labeling call is still one model's
judgment, made against a pool that was itself hand-picked at the workflow level — it can be wrong or
incomplete. So every query that misses at least one group gets a follow-up check: did search actually return
a tool, never pre-labeled, that would still genuinely satisfy that requirement? This check is told to hold
the line on vendor: if the task specifically names a product for that data ("in Salesforce", "our QuickBooks
ledger"), a same-shaped tool from a different vendor doesn't count, because it wouldn't actually reach the
data the task needs. This produces a second number, judged recall, reported next to the strict one — not in
place of it.

**A stalled quota doesn't lose work.** If a call to Gemini comes back looking like a quota or rate-limit
error, the run stops immediately instead of retrying into a dead quota for the rest of the workflow list.
Every generated query is written to a cache file the moment it's produced, so restarting later only pays for
what's still missing.

## What each number actually means

For one query with requirement groups $G_1, \dots, G_n$, and a search response split into a primary tool set
$P$ and a related tool set $R$:

- A group $G_i$ is **satisfied** if $G_i \cap (P \cup R) \neq \emptyset$ — at least one of its acceptable
  tools showed up anywhere in the response.
- A group is satisfied **on primary** if $G_i \cap P \neq \emptyset$ — the stricter version, ignoring related
  results.
- **`recall`** (strict retrieval recall) for that query = (number of groups satisfied) / $n$.
- **`primary_recall`** for that query = (number of groups satisfied on primary) / $n$.
- **`any_hit`** = true if at least one group was satisfied at all; **`primary_hit`** = true if at least one
  group was satisfied on primary specifically.
- **`judged_recall`** starts equal to `recall`. If `recall` < 1, the follow-up check (above) can additionally
  credit unmet groups where an actually-returned tool plausibly satisfies them; `judged_recall` becomes
  (groups satisfied strictly + groups newly credited) / $n$. It can only go up from `recall`, never down.

Every aggregate reported (average primary recall, average retrieval recall, any-required-group hit rate,
average judged recall) is simply the mean of the corresponding per-query value across all scored queries.
"Workflows accepted" counts distinct workflows with at least one scored query; "unlabelable queries" counts
queries where the labeling call found no group at all; "rejected" counts workflows where either stage failed
validation outright.

For every rejection reason with a real example, and a worked example of why a 2-tool query can score either
100% or 50% depending on whether those tools are alternatives or a composition, see
[`scoring_and_validation_reference.md`](scoring_and_validation_reference.md). For a hand-checked audit of the
scoring pipeline against raw API responses — confirming the arithmetic is correct and surfacing a few
ground-truth cases that look too narrow — see
[`manual_audit_workflows_1_5.md`](manual_audit_workflows_1_5.md).

The baseline benchmark (`single_tool_evaluation.py`) uses a plainer setup: one specific target tool, one
query built to retrieve it. `primary_hit` = target tool slug appears in $P$; `related_hit` = target appears
in $R$; `complete_miss` = appears in neither; `demotion` = appears in $R$ but not $P$ (found, but ranked
below the cutoff for primary). Rates are again just means across all sampled queries.

## What's in the repo

`src/query_level_workflow_evaluation.py` is the primary benchmark — everything above. `src/single_tool_evaluation.py`
is the baseline described just now: it samples individual tools across many toolkits and checks whether a
purpose-built query (with and without naming the app) finds each one. It's a floor, not a substitute — if a
tool can't be found from an easy, tailor-made query, a workflow's messier queries were never going to find it
either.

Two other scripts, `query_robustness_evaluation.py` and `synthetic_query_level_evaluation.py`, are still in
`src/` but predate the blind-decompose / grounded-label split described above. Their ground truth uses the
older flat-list schema, so their numbers aren't safely comparable to the current benchmark until they're
migrated to match it.

`agent_loop_eval/` is a separate benchmark answering a different question — see
`agent_loop_eval/README.md`. Where this one asks Gemini to *predict* an agent's queries in a single shot,
that one runs an actual tool-calling loop and records whatever the agent searches for while trying to make
progress. It exists because a prediction never sees a search result and so can never react to one, and
because a manager review raised the concern that predicted queries may not match what an agent really
issues. Query count there is emergent rather than capped by the formula below.

Both latency fields are recorded on every scored row: `api_search_latency_sec` is the successful search call
only, `end_to_end_latency_sec` adds in any failed attempts and retry backoff before it.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `COMPOSIO_API_KEY` and `GEMINI_API_KEY` in `.env` — both scripts need both.

## Running it

```powershell
.\.venv\Scripts\python.exe src\query_level_workflow_evaluation.py
.\.venv\Scripts\python.exe src\single_tool_evaluation.py
```

or the matching notebooks, `notebooks/01_query_level_workflow_evaluation.ipynb` and
`notebooks/04_single_tool_search_evaluation.ipynb`.

Every generation and every fetched tool description is cached to disk (`generation_cache.json`,
`tool_catalog_cache.json`, both git-ignored, both keyed per workflow), so a second run only pays for
workflows it hasn't seen yet. Search calls themselves aren't cached — re-running always re-searches
everything currently in the ground truth.

Constants worth knowing about, all in `query_level_workflow_evaluation.py` unless noted:

| Constant | Effect |
|---|---|
| `MAX_USE_CASES` | How many of the 100 workflows to attempt. Currently 100. |
| `MIN_QUERIES_FLOOR`, `MAX_QUERIES_CEILING`, `TOOLS_PER_QUERY_TARGET` | Bound how many queries a workflow's pool size can produce. |
| `DESCRIPTION_CHAR_LIMIT`, `TOOL_FETCH_CHUNK` | Tool-description truncation length and Composio fetch batch size. |
| `NUM_TOOLKITS_TO_SAMPLE`, `TOOLS_PER_TOOLKIT` (in `single_tool_evaluation.py`) | Sampling breadth and depth for the baseline. |

Before trusting an aggregate number, open `query_ground_truth.json` and read a handful of entries by hand —
especially after touching either prompt. Generated ground truth is only as good as it's been checked.

## Where things stand — 100 workflows attempted

| Metric | Value |
|---|---|
| Workflows accepted / attempted | 85 / 100 |
| Query-level test cases scored | 262 |
| Unlabelable queries (no pool tool fit) | 30 |
| Rejected workflows | 15 |
| Any-required-group hit rate | 71.0% |
| Retrieval recall, strict | 62.2% |
| Primary-only recall, strict | 48.5% |
| Judged recall | not usable this run — 0/262 queries got judged |

Latency: 2.52s average, 2.42s median, 3.33s P95, 12.73s max.

Search itself never touches Gemini, so the recall numbers above are complete and final regardless of quota.
Judging is the part that depends on Gemini, and it's been the actual bottleneck: the free tier caps out at
500 requests/day for this model, generation alone for 85 workflows uses roughly 170 of those, and judging
simply hasn't had daily budget left to finish. Three attempts so far judged 15, then 60, then 0 of the 262
queries before running out. An earlier, smaller pass (25 workflows) did get far enough through judging to be
informative: 66.7% strict recall against 81.3% judged recall there — a 14.6-point gap that's real evidence
strict scoring understates true performance, even though the 100-workflow number for judged recall isn't
usable yet.

### Single-tool baseline — 174 queries

65.5% primary hit, 7.5% related-only, 27.0% complete miss. Explicit queries (app named) beat implicit ones
69.0% to 62.1%. Spread across toolkits is wide — Jira and Airtable near 100%, GitHub at 0% on both explicit
and implicit phrasing across its 10 sampled tools.

## What the results say so far

Misses aren't empty results — search always returns *something*, just usually the wrong specific tool inside
the right general area. `QUICKBOOKS_GET_GENERAL_LEDGER_REPORT` comes back instead of
`QUICKBOOKS_QUERY_ENTITIES`; `HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID` instead of `HUBSPOT_ARCHIVE_PRODUCTS`. For an
agent that's arguably worse than an empty result, which at least signals "try again" instead of quietly doing
the wrong thing.

Generic phrasing pulls toward whatever toolkit the surrounding words suggest. A query like "send an email"
embedded in a task about jobs or marketing tends to surface a jobs or marketing tool instead of the plain
email-sending one — the domain vocabulary around the verb outweighs the verb itself.

Gemini's daily cap, not Composio's, is what's currently limiting how much of this benchmark can run end to
end in one sitting. The pipeline is built to fail safely into that limit rather than losing progress, but a
fully judged 100-workflow number needs either a bigger quota or a day where generation hasn't already spent
most of the budget before judging starts.

**Still needs work: how queries get worded during decomposition.** The blind-decomposition step sometimes
writes a query that's too generic, dropping a vendor name or scope detail that was in the task text (and even
in its own `intent` field) the whole time — so search gets blamed for missing something it was never told.
See `manual_audit_workflows_1_5.md` for real examples and what's actually happening.

### Corroborated independently by the agent-loop benchmark

Two findings show up in `agent_loop_eval/` as well, from live agent-issued queries rather than predicted
ones, which makes them harder to explain away as artefacts of how this benchmark phrases things.

**Found but not recommended.** Search *returns* the right tool far more often than it *promotes* it. Across
three agent-loop runs the split was 61%/27%, 67%/34% and 74%/46% — union recall against `primary`-only
recall. Roughly half the correct answers arrive demoted to `related`. The gap held across runs whose query
quality differed enormously, so it is a property of the ranking rather than of the phrasing. For an agent
acting on the primary recommendation, a demoted correct answer costs nearly what a miss costs.

**Naming the vendor doesn't reliably scope the search.** The cross-toolkit drift described above was easy to
dismiss while queries were bare (`"payment link"` returning Stripe on a HubSpot task is arguably fair). It
survives explicit scoping: `"HubSpot list payment links ecommerce"` still returned `STRIPE_LIST_PAYMENT_LINKS`
as the primary result, and the immediately following `"HubSpot list payment links"` returned
`HUBSPOT_LIST_EMAILS`.

**And a catalogue defect worth reporting upstream.** `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT`
and `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUB_SPOT_ACCOUNT` are both live and non-deprecated, with identical
display names and descriptions. A curated tool list can therefore name a slug search will never return,
because search surfaces the twin. Any set-intersection scorer counts that as a miss; this repo's scoring is
not yet corrected for it.

### What the agent-loop runs say about *this* benchmark's query cap

The dynamic cap here — `ceil(pool_size / TOOLS_PER_QUERY_TARGET)`, bounded by `MIN_QUERIES_FLOOR` and
`MAX_QUERIES_CEILING` — replaced a fixed 2-4 cap that left most of a large pool untested. The agent-loop
benchmark lets query count emerge from behaviour instead, with no cap at all, which sounds strictly better
and is not. Grouping its 20 tasks by the size of their reference tool list:

| Reference tools | Tasks | Union recall | Mean queries/task |
|---|---:|---:|---:|
| ≤ 6 | 6 | 69% | 4.5 |
| 7-13 | 8 | 59% | 4.1 |
| ≥ 14 | 6 | 38% | 5.7 |

Recall collapses on complex tasks while query count stays nearly flat — a task needing 25 tools gets 5.7
queries. A real agent does not search harder when there is more to find, so an emergent count under-samples
precisely the tasks where retrieval is hardest. The formula here scales coverage with pool size and the agent
loop does not; the two benchmarks fail in opposite directions, which is the argument for keeping both rather
than replacing this one.

Session-level recall is also confounded by query count, which makes it unsafe to compare across runs whose
execution policy differs. Comparing the agent loop's mocked and real-read runs over the same ten tasks: 86
queries at 74% union versus 50 queries at 63%, but 0.79 union hits per query versus 1.16. Real data lets an
agent stop searching once something works, so total recall falls while per-query quality rises. Hits-per-query
is the fairer statistic whenever the number of queries is not held fixed.

## Artifacts

```
src/query_level_workflow_evaluation/
  query_ground_truth.json     accepted queries with their requirement groups, plus unlabelable ones
  generation_audit.json       raw LLM output from both stages, and why anything was rejected
  search_results.csv          per-query recall, judged recall, latency, extras
  raw_search_results/*.json   full request/response for every scored query
  summary_report.md           the aggregate numbers and worked failure examples
  generation_cache.json       (git-ignored) resumable per-workflow cache of every generation
  tool_catalog_cache.json     (git-ignored) cached tool descriptions pulled from Composio
```

`src/single_tool_evaluation/` follows the same shape. Everything except the two caches is tracked in git.

The agent-loop benchmark keeps its own artifacts, one directory per run because its results are only
comparable within a fixed execution policy:

```
agent_loop_eval/
  RUNS.md                     which run is which, and which comparisons are legitimate
  run3_vs_run4_queries.md     query-by-query side-by-side, mocked vs real reads
  run1_real_reads_unconnected/  attempted real reads with no connections -- the derailment run
  run3_fully_mocked/            everything mocked; the retrieval baseline
  run4_real_reads/              real reads against nine connected toolkits
```

Each run directory holds per-task traces, the captured queries, a generated report, and the run log.

