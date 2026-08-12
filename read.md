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

So ground truth is defined **per intent, not per task**. Each generated query carries its own small set of
`required_tools` (genuinely needed for that one intent) and `supporting_tools` (relevant but not required),
drawn only from the task's candidate pool. Scoring is recall over the required set, so a query expecting
two tools and retrieving one scores 0.5 rather than a binary miss.

Every generated decomposition is validated before use (query count in range, no invented slugs, 1–3 required
tools per query, no duplicates); failures are recorded with a rejection reason rather than silently dropped.

## Benchmarks

| # | Script | What it tests |
|---|---|---|
| 1 | `src/query_level_workflow_evaluation.py` | **Primary.** Decomposes each workflow in `top-100-eval-use-cases.md` into 2–4 agent-like search intents with per-query ground truth, then scores retrieval, ranking, and latency. |
| 2 | `src/query_robustness_evaluation.py` | **Secondary — diagnostic.** Re-runs benchmark 1's intents as explicit / implicit / paraphrased variants with the required tools held constant, isolating phrasing sensitivity from decomposition quality. Not a second ground-truth source; see note below. |
| 3 | `src/synthetic_query_level_evaluation.py` | **Tertiary.** LLM-invented tasks independent of `top-100-eval-use-cases.md`, grounded in real tool slugs/descriptions fetched live from Composio so ground truth is never hallucinated. Same per-query decomposition and scoring as benchmark 1. |
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
| `MAX_USE_CASES` | `query_level_workflow_evaluation.py` | Workflows decomposed. Currently **25** → 79 queries. Raise to 100 for the full suite. |
| `MAX_QUERIES_PER_WORKFLOW` | `query_level_workflow_evaluation.py` | Upper bound on intents per workflow (default 4). |
| `MAX_SOURCE_QUERIES` | `query_robustness_evaluation.py` | Source intents × 3 variants = search calls. Currently **60** → 180 searches. |
| `NUM_TASKS` | `synthetic_query_level_evaluation.py` | LLM-invented tasks generated. Currently **10** — one Gemini call per accepted task (task text + decomposition combined into a single call to keep this cheap). |
| `NUM_TOOLKITS_TO_SAMPLE`, `TOOLS_PER_TOOLKIT` | `single_tool_evaluation.py` | Sampling breadth and depth. |

Start small — set `MAX_USE_CASES` to 5–8 and read `query_ground_truth.json` by hand before trusting any
aggregate. The generated mappings should be spot-checked before the numbers mean anything.

## Results

Current run: 25 workflows attempted (24 accepted, 1 rejected on validation) → 79 query-level tests;
60 of those intents × 3 phrasings → 180 robustness searches; 10 synthetic tasks (19 attempts, 9 rejected)
→ 23 query-level tests; 174 single-tool queries across 20 toolkits.

### 1. Query-level workflow benchmark — 79 queries

| Metric | Value |
|---|---|
| Any-required-tool hit rate | 84.8% |
| Retrieval recall (primary ∪ related) | 77.8% |
| Primary-only recall | 63.9% |
| Fully correct queries | 56 / 79 |
| Total misses (nothing required retrieved) | 12 / 79 |

| Query shape | Queries | Recall | Primary recall |
|---|---:|---:|---:|
| 1 required tool | 48 | 77.1% | 68.8% |
| 2+ required tools | 31 | 79.0% | 56.5% |

Latency: 3.10 s average, 2.87 s median, 4.59 s P95, 10.63 s maximum.

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

2. **Multi-tool intents fail at ranking, not retrieval.** Going from 1 to 2+ required tools leaves total
   recall flat (77.1% → 79.0%) but drops primary recall (68.8% → 56.5%). The right tools are found and then
   demoted into `related`. 18 of 79 queries had a required tool appear only as related. This contradicts the
   earlier whole-task benchmark's conclusion that recall collapses with tool count — that was an artifact of
   the invalid method, not a real property of search.

3. **Generic action verbs lose to domain-matching toolkits.** `GMAIL_SEND_EMAIL` accounts for 5 of the 12
   total misses. Queries like "send curated job digest email" return `DICE_MCP_SEARCH_JOBS`,
   `ZIPRECRUITER_MCP_SEARCH_JOBS`, or `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL` — the domain noun in the query
   ("job", "support", "marketing") outweighs the actual operation ("send an email").

4. **Cross-toolkit intrusion is common and systematic.** Most frequent intruders across the run: `EXCEL` (8),
   `GOOGLEDRIVE` (8), `MERCURY` (7), `HEYGEN` (5), `GOOGLESHEETS` (5), `RESEND` (4), `KADOA` (4),
   `FREEAGENT` (4). These are near-neighbour products substituting for the requested one — e.g.
   "create a disabled confirmation workflow" returns `KADOA_CREATE_WORKFLOW_TRIGGER` instead of
   `HUBSPOT_CREATE_WORKFLOW`; QuickBooks ledger queries return `MERCURY_MCP_LIST_TRANSACTIONS`.

5. **All 12 total misses returned results** — search never returned nothing, it returned confidently wrong
   tools. That is worse for an agent than an empty result, which it could recover from.

6. **Latency is stable but has a long tail:** ~2.9 s median across benchmarks, with outliers past 10 s.

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
