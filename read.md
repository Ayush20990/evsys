# Evsys — `COMPOSIO_SEARCH_TOOLS` retrieval evaluation

This repository measures the retrieval quality of Composio's `COMPOSIO_SEARCH_TOOLS`: incorrect or missed
tool retrieval, poor ranking, cross-toolkit confusion, toolkit-specific weakness, and latency.

## Methodology

The central design decision is that **a high-level task is not a search query.** The tasks in
`src/top-100-eval-use-cases.md` list every tool that might be touched while solving the whole workflow.
A real agent never searches that way — it decomposes first:

```
High-level task → agent decomposes → fundamental search intents → queries → COMPOSIO_SEARCH_TOOLS → tools
```

So ground truth is defined **per intent, not per task**, and it's built in two deliberately separate Gemini
calls so neither stage leaks into the other:

- **Stage A (blind decomposition):** Gemini sees *only the task text* and breaks it into realistic search
  queries — it never sees the candidate pool. This matters: giving the pool to the same call that writes the
  queries lets tool-name vocabulary leak into query phrasing. Observed before this split: a generated query
  asked to "query ledger **entities**" because the pool contained `QUICKBOOKS_QUERY_ENTITIES` — "entities"
  is API jargon, not something a person planning a task says. That leakage made retrieval look artificially
  easier than a genuinely blind search would be. After the split, the equivalent query reads "search
  quickbooks bank account ledger transactions" — no jargon, task vocabulary only.
- **Stage B (grounded labeling):** a second, independent call sees stage A's queries plus the candidate
  pool's **real tool descriptions**, fetched live from Composio (`composio.tools.get(user_id=..., tools=[...])`),
  not bare slugs. Asking an LLM to infer semantics from an opaque name like `GOOGLESUPER_FETCH_EMAILS` is
  unnecessary noise in the ground truth; the labeler now reads the actual description before deciding.

Each query's ground truth is one or more **requirement groups**:

- Within a group, **any one** tool satisfies it — these are true alternatives (e.g. either
  `GMAIL_SEARCH_EMAILS` or `GMAIL_FETCH_EMAILS` would do).
- Across groups, **all** are required — these are genuinely compositional intents (e.g. find an email AND
  schedule a follow-up).

A flat required-tool list can't express "either tool is fine," and scoring it as a plain set silently
penalized correct alternative-tool hits as partial misses. Recall is `groups_satisfied / total_groups`.

Stage B can also honestly say **no candidate tool fits a query** — recorded as "unlabelable" and reported,
not scored and not silently dropped. This surfaces genuine sub-intents the human-curated pool doesn't cover
(e.g. a task mentioning LinkedIn/GitHub signals whose pool has no matching tool for that specific ask),
which the earlier single-call design had no way to express — it would have been forced to either skip the
sub-intent invisibly or stretch some other pool tool onto it.

The number of queries per workflow also scales with the candidate-pool size instead of a fixed cap
(`query_count_range()`: roughly 1 query per 2–3 candidate tools, floor 1–2, ceiling 10) — pool size is used
only to set this bound, and is never shown to the model during decomposition. A fixed 2–4 cap was measured
to silently drop genuine sub-intents for complex workflows — on average 51% of a workflow's candidate tools
were never assigned to any query under that cap.

Because ground truth is still an LLM's opinion, every query search still misses gets a cheap secondary
**judged-recall** pass: an independent Gemini call, given the workflow's context, checks whether an
*actually-returned* tool — even one never pre-labeled — plausibly satisfies the missed requirement. This is
reported as `judged_recall` alongside strict recall, never in place of it, and it's vendor-scoped: if the
workflow explicitly names a vendor for that data/action (e.g. "in Salesforce"), only a same-vendor tool can
be credited, so a functionally similar competitor tool doesn't inflate the number.

Every generated decomposition and labeling is validated before use (query count in the computed range, no
invented slugs, 1–4 tools per group, query_labels indices must match 1:1); failures are recorded with a
rejection reason rather than silently dropped.

## Benchmarks

| # | Script | What it tests |
|---|---|---|
| 1 | `src/query_level_workflow_evaluation.py` | **Primary.** Decomposes each workflow in `top-100-eval-use-cases.md` into a pool-scaled number of agent-like search intents with per-query, requirement-group ground truth, then scores strict + judged retrieval, ranking, and latency. |
| 2 | `src/query_robustness_evaluation.py` | **Secondary — diagnostic.** Re-runs benchmark 1's intents as explicit / implicit / paraphrased variants with the required tools held constant, isolating phrasing sensitivity from decomposition quality. Not a second ground-truth source; see note below. ⚠️ still on the older flat-required-tool schema — see Known gaps. |
| 3 | `src/synthetic_query_level_evaluation.py` | **Tertiary.** LLM-invented tasks independent of `top-100-eval-use-cases.md`, grounded in real tool slugs/descriptions fetched live from Composio so ground truth is never hallucinated. ⚠️ still on the older flat-required-tool schema — see Known gaps. |
| 4 | `src/single_tool_evaluation.py` | **Baseline.** Samples tools across many toolkits and asks whether one natural query retrieves that specific tool, explicitly and implicitly. |

**On the explicit/implicit distinction (benchmark 2):** a real agent doesn't decompose a task and then
deliberately choose to omit the app name — whatever phrasing the decomposition step lands on is however
explicit or implicit it happens to be. So forcing artificial explicit/implicit variants of an
already-decomposed query isn't simulating a second real agent; it's a controlled probe that isolates one
variable (does naming the app change retrieval, holding intent fixed). It's kept as a diagnostic precisely
because the result is large and load-bearing (see Findings), not because it's a second benchmark of
ground-truth validity — that role belongs to benchmarks 1 and 3, which never manufacture query variants.

Both latency fields are reported everywhere: `api_search_latency_sec` covers only the successful search call,
while `end_to_end_latency_sec` includes failed attempts and retry backoff.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `COMPOSIO_API_KEY` and `GEMINI_API_KEY` in `.env`. All three benchmarks need both keys.

## Run

Run the scripts directly, in this order — benchmark 2 consumes benchmark 1's ground truth, the others are independent:

```powershell
.\.venv\Scripts\python.exe src\query_level_workflow_evaluation.py
.\.venv\Scripts\python.exe src\query_robustness_evaluation.py
.\.venv\Scripts\python.exe src\synthetic_query_level_evaluation.py
.\.venv\Scripts\python.exe src\single_tool_evaluation.py
```

Equivalent notebooks are in `notebooks/`, numbered in the same order (`01_query_level_workflow_evaluation.ipynb`,
`02_query_robustness_evaluation.ipynb`, `03_synthetic_query_level_evaluation.ipynb`,
`04_single_tool_search_evaluation.ipynb`); each just `%run`s its script.

### Controlling cost

Gemini generations are cached to disk and keyed by workflow, so re-runs only pay for *new* work. The search
calls are not cached. Scale each benchmark with these constants:

| Constant | File | Effect |
|---|---|---|
| `MAX_USE_CASES` | `query_level_workflow_evaluation.py` | Workflows decomposed. Currently **10** (held here pending review of the two-stage redesign before scaling — see Results). Each workflow now costs 2 Gemini calls (decompose + label) instead of 1. |
| `MIN_QUERIES_FLOOR`, `MAX_QUERIES_CEILING`, `TOOLS_PER_QUERY_TARGET` | `query_level_workflow_evaluation.py` | Query-count-per-workflow scales with pool size (`query_count_range()`); these bound the floor/ceiling and the tools-per-query ratio. |
| `DESCRIPTION_CHAR_LIMIT`, `TOOL_FETCH_CHUNK` | `query_level_workflow_evaluation.py` | Tool-description truncation length and Composio batch-fetch size for `fetch_tool_catalog()`, cached to `tool_catalog_cache.json`. |
| `MAX_SOURCE_QUERIES` | `query_robustness_evaluation.py` | Source intents × 3 variants = search calls. Currently **60** → 180 searches. |
| `NUM_TASKS` | `synthetic_query_level_evaluation.py` | LLM-invented tasks generated. Currently **10** — one Gemini call per accepted task (task text + decomposition combined into a single call to keep this cheap). |
| `NUM_TOOLKITS_TO_SAMPLE`, `TOOLS_PER_TOOLKIT` | `single_tool_evaluation.py` | Sampling breadth and depth. |

Start small — set `MAX_USE_CASES` to 5–8 and read `query_ground_truth.json` by hand before trusting any
aggregate. The generated mappings should be spot-checked before the numbers mean anything.

## Results

Current run: 9 of 10 attempted workflows accepted (1 rejected on labeling validation) → 29 scored query-level
tests + 3 unlabelable, under the two-stage blind-decompose / grounded-label schema described above; 60
intents from the *previous single-call, flat-schema* ground truth × 3 phrasings → 180 robustness searches;
10 synthetic tasks (19 attempts, 9 rejected) → 23 query-level tests (also previous schema); 174 single-tool
queries across 20 toolkits.

### 1. Query-level workflow benchmark — 29 queries, two-stage schema (10-workflow smoke test)

Held at 10 workflows pending further review before scaling — see Run for how to raise `MAX_USE_CASES`.

| Metric | Value |
|---|---|
| Any-required-group hit rate | 79.3% |
| Retrieval recall (strict, groups satisfied) | 67.2% |
| Primary-only recall (strict) | 46.6% |
| **Judged recall** (strict + plausible unlabeled hits, vendor-scoped) | **75.9%** |
| Unlabelable queries (no candidate tool fit, not scored) | 3 |
| Queries that needed the judge pass | 13 / 29 |

Latency: 2.75 s average, 2.62 s median, 3.70 s P95, 6.73 s maximum.

These numbers are broadly consistent in shape with the prior 25-workflow, single-call-schema run (66.7%
strict / 81.3% judged recall there) — the two-stage split didn't wildly swing the headline numbers on this
small sample, which is reassuring, but the *ground truth itself* is now measurably cleaner (see the
QuickBooks example above), so these numbers should be trusted more even where the values are similar.
Because the schema changed, don't treat this run and the prior 25-workflow numbers as directly comparable —
re-run at matching scale before drawing a before/after conclusion.

### 2. Query robustness benchmark — 180 searches

| Variant | Queries | Any-hit | Recall | Primary-hit |
|---|---:|---:|---:|---:|
| explicit (app named) | 60 | 88.3% | 82.5% | 75.0% |
| paraphrase | 60 | 55.0% | 53.3% | 51.7% |
| implicit (no app named) | 60 | 36.7% | 34.2% | 33.3% |

### 3. Synthetic query-level benchmark — 23 queries, 10 tasks

Tasks are LLM-invented from scratch (never seen `top-100-eval-use-cases.md`), grounded in real tool slugs
fetched live from Composio for a curated toolkit family. 9 of 19 generation attempts were rejected before
search ran at all (3 infeasible, 4 didn't genuinely span enough toolkits, 2 invented a tool slug outside
the fetched candidates) — validation catches bad ground truth before it can pollute the metrics.

| Metric | Value |
|---|---|
| Any-required-tool hit rate | 82.6% |
| Retrieval recall (primary ∪ related) | 80.4% |
| Primary-only recall | 80.4% |

Latency: 2.59 s average, 2.55 s median, 4.05 s maximum. Failures follow the same shape as benchmark 1 —
near-neighbour substitution within the right toolkit (`NOTION_ADD_MULTIPLE_PAGE_CONTENT` for
`NOTION_APPEND_CODE_BLOCKS`; `HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID` for `HUBSPOT_ARCHIVE_PRODUCTS`;
`SLACK_FIND_USER_BY_EMAIL_ADDRESS` for `GMAIL_GET_CONTACTS`) — reinforcing that this is a real search
property, not an artifact of how `top-100-eval-use-cases.md` happens to be written.

### 4. Single-tool baseline — 174 queries

Primary hit 65.5%, related-only 7.5%, complete miss 27.0%. Explicit 69.0% vs. implicit 62.1%.
Latency 3.08 s average, 10.17 s maximum. Per-toolkit spread is wide: Jira and Airtable near 100%,
while **GitHub scored 0% on both explicit and implicit queries** across 10 sampled tools.

## Key findings

1. **Phrasing sensitivity is the dominant failure mode.** Holding the intent and expected tools fixed and
   only removing the app name drops recall from 82.5% to 34.2% — a 48-point collapse. Paraphrasing alone
   costs 29 points. Search is leaning heavily on literal app-name matching rather than intent.
   The single-tool baseline understates this badly (7-point gap), because short single-tool queries are far
   easier than real workflow intents.

2. **Compositional queries (2+ requirement groups) genuinely underperform**, now that the requirement-group
   schema separates real compositionality from mere alternatives. *(From the 25-workflow single-call run —
   larger sample than the current 10-workflow two-stage smoke test.)* 1-group queries: 70.2% recall / 61.4%
   primary recall. 2+-group queries: 58.7% recall / 37.3% primary recall — a real, unconfounded drop. Under
   the earlier flat-list schema this looked like "recall stays flat, only ranking drops" — that read was an
   artifact of OR-alternatives being scored as AND-required; the corrected picture is that multi-operation
   queries are harder on both axes.

3. **Generic action verbs lose to domain-matching toolkits.** `GMAIL_SEND_EMAIL` and `GMAIL_FETCH_EMAILS`
   are the most-missed tools across the run. Queries like "send curated job digest email" or "send outreach
   email for marketing" return `SENDGRID_SEND_A_TEST_MARKETING_EMAIL`, `HUBSPOT_CLONE_MARKETING_EMAIL`, or
   job-board tools — the domain noun in the query ("job", "marketing") outweighs the actual operation
   ("send an email"). The judge pass does *not* rescue these: sending email is rarely vendor-locked, so if a
   returned tool genuinely sent email it would be credited, and mostly it wasn't a real send-email tool at all.

4. **Cross-toolkit intrusion is common and systematic.** Most frequent intruder prefixes across the run:
   `SALESFORCE` (20, mostly CRM-adjacent tasks pulling in Salesforce over the actually-requested CRM/tool),
   `MAILCHIMP` (15), `GOOGLEDRIVE` (13), `EXCEL` (8), `OUTLOOK` (7), `EMELIA` (6), `BREVO` (6). Some of these
   are legitimate near-misses the judge credits (e.g. `OUTLOOK_SEND_EMAIL` for a generic "send email" need);
   others are exactly the vendor-mismatch the judge is built to reject (e.g. `EMELIA_LIST_CAMPAIGNS` for an
   explicitly-Salesforce campaign query).

5. **Judged recall consistently exceeds strict recall by a large margin** — 81.3% vs 66.7% on the 25-workflow
   single-call run, 75.9% vs 67.2% on the current 10-workflow two-stage run — directly caused by ground-truth
   incompleteness, not by search actually improving. This is the concrete, measured answer to "is recall the
   right metric" — a meaningful slice of what strict scoring calls a miss is really search finding a
   correct-but-unlabeled tool. Report both numbers; neither alone is trustworthy in isolation.

6. **Latency is stable but has a long tail:** ~2.5–2.9 s median across benchmarks, with outliers past 8 s.

## Known gaps

- **Benchmarks 2 and 3 haven't been migrated to the two-stage blind-decompose / grounded-label schema yet.**
  Their numbers in this document (robustness: explicit 82.5% / implicit 34.2% / paraphrase 53.3%; synthetic:
  82.6% any-hit) were computed under the oldest single-call, flat-required-tool-list scoring — before even
  the requirement-group redesign, let alone the decompose/label split. They're internally consistent and the
  phrasing-sensitivity finding is real, but they aren't directly comparable to benchmark 1's current numbers.
  Do this before citing 2 or 3 alongside 1 in the same table.
- **Benchmark 1 itself has two schema generations now**, both present in this document: the 25-workflow
  requirement-group run (single-call, pool visible during decomposition) and the current 10-workflow
  two-stage run (blind decompose, grounded label). Don't average or directly compare across them — re-run
  the two-stage version at matching scale first.
- **Coverage of the candidate pool is well under 100%** even after replacing the fixed query cap with a
  dynamic one, and this is now believed to be expected rather than a bug: the human-curated pool
  intentionally includes "might be needed" tools (verification steps, alternates, optional paths) that one
  realistic decomposition won't all touch — see Methodology. The two-stage schema makes this concrete via
  "unlabelable" queries: genuine sub-intents stage A finds that stage B can't match to any pool tool at all.

## Artifacts

Each benchmark writes a self-contained directory under `src/`:

```
src/query_level_workflow_evaluation/
  query_ground_truth.json     scored queries (requirement groups) + unlabelable queries (no pool tool fit)
  generation_audit.json       raw Gemini responses for both stages, validation rejections
  search_results.csv          per-query metrics, judged recall, latency
  raw_search_results/*.json   full request + response per query
  summary_report.md           aggregate metrics, failure examples, unlabelable-query list
  tool_catalog_cache.json     (git-ignored) cached real tool descriptions fetched from Composio
```

`src/query_robustness_evaluation/` and `src/single_tool_evaluation/` follow the same layout.
Only the Gemini generation and tool-catalog caches are git-ignored; every scored artifact and audit trail is tracked.

## Removed benchmarks

Two earlier evaluators were deleted because they sent an **entire multi-step task as a single search query**
and compared the result against the task's whole tool list — the exact failure this project's methodology
exists to avoid. Their headline numbers (≈34% recall) measured decomposition-free querying, not search quality,
and should not be cited:

- `multi_tool_evaluation.py` — whole task from the 100-use-case file as one query.
- `synthetic_multi_tool_evaluation.py` — Gemini-invented tasks, but still one query per whole task.

`synthetic_query_level_evaluation.py` (benchmark 3) replaces the coverage the deleted synthetic evaluator
provided — independent, LLM-invented tasks — but decomposes each into per-query ground truth the same way
benchmark 1 does, instead of scoring the whole task as one search.
