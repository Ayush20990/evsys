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

So ground truth is defined **per intent, not per task**. Each generated query carries its own ground truth,
drawn only from the task's candidate pool, structured as one or more **requirement groups**:

- Within a group, **any one** tool satisfies it — these are true alternatives (e.g. either
  `GMAIL_SEARCH_EMAILS` or `GMAIL_FETCH_EMAILS` would do).
- Across groups, **all** are required — these are genuinely compositional intents (e.g. find an email AND
  schedule a follow-up).

A flat required-tool list can't express "either tool is fine," and scoring it as a plain set silently
penalized correct alternative-tool hits as partial misses. Recall is `groups_satisfied / total_groups`.

The number of queries per workflow also scales with the candidate-pool size instead of a fixed cap
(`query_count_range()` in `query_level_workflow_evaluation.py`: roughly 1 query per 2–3 candidate tools, floor
1–2, ceiling 10). A fixed 2–4 cap was measured to silently drop genuine sub-intents for complex workflows —
on average 51% of a workflow's candidate tools were never assigned to any query under that cap.

Because ground truth is still one LLM's opinion, constrained to a human-curated pool built for the *whole*
workflow rather than derived fresh for each atomic query, every query search still misses gets a cheap
secondary **judged-recall** pass: an independent Gemini call, given the workflow's context, checks whether
an *actually-returned* tool — even one never pre-labeled — plausibly satisfies the missed requirement. This
is reported as `judged_recall` alongside strict recall, never in place of it, and it's vendor-scoped: if the
workflow explicitly names a vendor for that data/action (e.g. "in Salesforce"), only a same-vendor tool can
be credited, so a functionally similar competitor tool doesn't inflate the number.

Every generated decomposition is validated before use (query count in the computed range, no invented slugs,
1–4 tools per group, no duplicate queries); failures are recorded with a rejection reason rather than
silently dropped.

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
| `MAX_USE_CASES` | `query_level_workflow_evaluation.py` | Workflows decomposed. Currently **25** → 82 queries. Raise to 100 for the full suite. |
| `MIN_QUERIES_FLOOR`, `MAX_QUERIES_CEILING`, `TOOLS_PER_QUERY_TARGET` | `query_level_workflow_evaluation.py` | Query-count-per-workflow scales with pool size (`query_count_range()`); these bound the floor/ceiling and the tools-per-query ratio. |
| `MAX_SOURCE_QUERIES` | `query_robustness_evaluation.py` | Source intents × 3 variants = search calls. Currently **60** → 180 searches. |
| `NUM_TASKS` | `synthetic_query_level_evaluation.py` | LLM-invented tasks generated. Currently **10** — one Gemini call per accepted task (task text + decomposition combined into a single call to keep this cheap). |
| `NUM_TOOLKITS_TO_SAMPLE`, `TOOLS_PER_TOOLKIT` | `single_tool_evaluation.py` | Sampling breadth and depth. |

Start small — set `MAX_USE_CASES` to 5–8 and read `query_ground_truth.json` by hand before trusting any
aggregate. The generated mappings should be spot-checked before the numbers mean anything.

## Results

Current run: 25 workflows accepted, 0 rejected on validation → 82 query-level tests (requirement-group
schema, dynamic query cap, judged recall); 60 intents from the *previous* flat-schema ground truth × 3
phrasings → 180 robustness searches; 10 synthetic tasks (19 attempts, 9 rejected) → 23 query-level tests
(also previous flat schema); 174 single-tool queries across 20 toolkits.

### 1. Query-level workflow benchmark — 82 queries, requirement-group schema

| Metric | Value |
|---|---|
| Any-required-group hit rate | 73.2% |
| Retrieval recall (strict, groups satisfied) | 66.7% |
| Primary-only recall (strict) | 54.1% |
| **Judged recall** (strict + plausible unlabeled hits, vendor-scoped) | **81.3%** |
| Perfect strict-recall queries | 49 / 82 |
| Total misses (no group satisfied at all) | 22 / 82 |
| Queries that needed the judge pass | 33 / 82 |

Latency: 2.77 s average, 2.50 s median, 4.61 s P95, 8.63 s maximum.

The 14.6-point gap between strict and judged recall is the direct answer to "is recall the right metric":
strict recall alone understates real performance by roughly that much, because a meaningful fraction of
"misses" are search correctly finding a valid tool we simply hadn't pre-labeled as acceptable. The judge is
deliberately conservative and vendor-scoped — it explicitly rejected credit for e.g. `EMELIA_LIST_CAMPAIGNS`
returned for a Salesforce-specific query, and for `CALENDLY_UPDATE_EVENT_TYPE` returned for a
HubSpot-workflow query — so 81.3% is not an inflated ceiling, and both numbers should be read together, not
either one alone.

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
   schema separates real compositionality from mere alternatives. 1-group queries: 70.2% recall / 61.4%
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

5. **Judged recall (81.3%) vs strict recall (66.7%): a 14.6-point gap directly caused by ground-truth
   incompleteness**, not by search actually improving. This is the concrete, measured answer to "is recall
   the right metric" — a meaningful slice of what strict scoring calls a miss is really search finding a
   correct-but-unlabeled tool. Report both numbers; neither alone is trustworthy in isolation.

6. **Latency is stable but has a long tail:** ~2.5–2.9 s median across benchmarks, with outliers past 8 s.

## Known gaps

- **Benchmarks 2 and 3 haven't been migrated to the requirement-group + judged-recall schema yet.** Their
  numbers in this document (robustness: explicit 82.5% / implicit 34.2% / paraphrase 53.3%; synthetic: 82.6%
  any-hit) were computed under the older flat-required-tool-list scoring, before the group/judged-recall
  redesign in benchmark 1. They're internally consistent and the phrasing-sensitivity finding is real, but
  they aren't directly comparable to benchmark 1's current numbers, and re-running them under the new schema
  might shift them (probably upward, for the same reason benchmark 1's judged recall exceeds its strict
  recall). Do this before citing 2 or 3 alongside 1 in the same table.
- **Coverage of the candidate pool is still well under 100%** (47% for the current 25-workflow run) even
  after replacing the fixed query cap with a dynamic one. This is now believed to be expected rather than a
  bug: the human-curated pool intentionally includes "might be needed" tools (verification steps,
  alternates, optional paths) that one realistic decomposition won't all touch — see Methodology.

## Artifacts

Each benchmark writes a self-contained directory under `src/`:

```
src/query_level_workflow_evaluation/
  query_ground_truth.json     generated intents + per-query required/supporting tools
  generation_audit.json       raw Gemini responses, validation rejections
  search_results.csv          per-query metrics, ranks, extras, latency
  raw_search_results/*.json   full request + response per query
  summary_report.md           aggregate metrics and failure examples
```

`src/query_robustness_evaluation/` and `src/single_tool_evaluation/` follow the same layout.
Only the Gemini generation caches are git-ignored; every scored artifact and audit trail is tracked.

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
