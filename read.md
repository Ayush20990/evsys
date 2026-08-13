# Evsys — `COMPOSIO_SEARCH_TOOLS` retrieval evaluation

This repository measures the retrieval quality of Composio's `COMPOSIO_SEARCH_TOOLS`: incorrect or missed
tool retrieval, poor ranking, cross-toolkit confusion, toolkit-specific weakness, and latency.

## The core idea

A high-level task is not a search query. `top-100-eval-use-cases.md` lists every tool that *might* be
touched somewhere in a whole workflow — it is not what one search call should return. A real agent doesn't
search that way either: it breaks the task into smaller steps and searches for one tool at a time.

```
High-level task → break into steps → one search query per step → COMPOSIO_SEARCH_TOOLS → tools found
```

So this benchmark builds ground truth **per query, not per task**, and scores each query against only the
tool(s) that step genuinely needs.

## How it works, step by step

**1. A workflow is read in.** `top-100-eval-use-cases.md` gives a task description plus a candidate pool of
tools a human decided are relevant somewhere in that task. That pool is treated as a superset, never as the
answer key.

**2. The task is decomposed into queries — blindly.** An LLM call sees *only the task text*, nothing about
the tool pool, and writes 1 to ~10 realistic search queries (the exact count scales with how large the
task's tool pool is, as a proxy for its complexity — but the pool itself stays hidden). This mimics a real
agent, which has no visibility into what tools exist before it searches. Keeping the pool hidden here matters:
if the same call could see the pool, tool-name jargon leaked straight into query wording (observed example:
a query asked to "query ledger **entities**" purely because `QUICKBOOKS_QUERY_ENTITIES` was visible — no
real person phrases a task that way). Blind decomposition removes that leak.

**3. Each query is labeled — grounded in real tool descriptions.** A second, independent LLM call now sees
the queries from step 2 *and* the candidate pool, but with each tool's actual description fetched live from
Composio, not just its slug. It decides, per query, which pool tool(s) would genuinely satisfy it. This
matters because a name like `GOOGLESUPER_FETCH_EMAILS` tells an LLM almost nothing on its own — the real
description is needed to judge a match honestly.

Ground truth per query is one or more **requirement groups**:
- Tools *within* a group are alternatives — any one of them is a full success.
- *Across* groups, all are required — this only happens for genuinely compositional queries (two different
  operations needed together).

A query is also allowed to come back with **zero matching tools** — meaning this task's human-curated pool
genuinely doesn't cover that specific sub-intent. That's recorded and reported honestly, not forced into a
bad match and not silently dropped.

**4. A workflow is only "accepted" if both stages pass validation.** Decomposition is rejected if the query
count is out of range, a query is nonsense, or queries duplicate each other. Labeling is rejected if it
invents a tool slug outside the candidate pool, mislabels the group count, or doesn't cover every query it
was given. A rejected workflow contributes zero test cases — it's logged with a reason, never silently
patched over.

**5. Every accepted query is run through `COMPOSIO_SEARCH_TOOLS` and scored.** Recall = fraction of
requirement groups satisfied (any one tool per group, found in the primary or related results). This is
**strict recall** — a query only counts as a hit if search returned a tool that was pre-labeled correct.

**6. Misses get a second look — judged recall.** Ground truth from steps 2–3 is still one LLM's opinion. So
every query that misses a requirement group gets one more check: does the tool search *actually returned*
plausibly satisfy that requirement, even though it was never pre-labeled? This check is vendor-scoped — if
the task names a specific product for that data (e.g. "in Salesforce"), only a same-vendor tool can be
credited, so a functionally similar competitor tool doesn't inflate the score. Reported as `judged_recall`
**alongside** strict recall, never replacing it — both numbers matter together.

**7. Quota-safe by design.** If a Gemini call looks like a quota/rate-limit error, the run stops immediately
(no wasted retries) and saves everything completed so far — generated queries, search scores, and whatever
was judged. Every generated query is cached to disk per workflow, so re-running later only pays for what's
still missing; nothing already done is repeated or lost.

## What's in the repo

| Script | Role |
|---|---|
| `src/query_level_workflow_evaluation.py` | **Primary benchmark.** Everything described above. |
| `src/single_tool_evaluation.py` | **Baseline.** A simpler, independent check: sample individual tools across many toolkits, ask an LLM for one query that should retrieve each one (with and without naming the app), and see if it comes back as a primary or related result. Useful as a sanity floor — if a tool can't be found from an easy, purpose-built query, complex-workflow retrieval was never going to find it either. |

Two earlier scripts (`query_robustness_evaluation.py`, `synthetic_query_level_evaluation.py`) still exist in
`src/` but are not part of this documentation for now — they predate the two-stage blind-decompose /
grounded-label redesign above and would need to be migrated to it before their numbers are trustworthy
alongside the primary benchmark's. Revisit them later if that phrasing-robustness and synthetic-task coverage
is wanted again.

Both latency fields are reported everywhere: `api_search_latency_sec` covers only the successful search call,
while `end_to_end_latency_sec` includes failed attempts and retry backoff.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `COMPOSIO_API_KEY` and `GEMINI_API_KEY` in `.env`. Both scripts need both keys.

## Run

```powershell
.\.venv\Scripts\python.exe src\query_level_workflow_evaluation.py
.\.venv\Scripts\python.exe src\single_tool_evaluation.py
```

Notebooks: `notebooks/01_query_level_workflow_evaluation.ipynb`, `notebooks/04_single_tool_search_evaluation.ipynb`.

### Controlling cost

Every generation is cached to disk (`generation_cache.json`, keyed per workflow) and tool descriptions are
cached too (`tool_catalog_cache.json`) — re-runs only pay for what's new. Search calls are not cached.

| Constant | Effect |
|---|---|
| `MAX_USE_CASES` | Workflows attempted, out of the 100 in `top-100-eval-use-cases.md`. Currently **100**. |
| `MIN_QUERIES_FLOOR`, `MAX_QUERIES_CEILING`, `TOOLS_PER_QUERY_TARGET` | Bound how many queries a workflow's pool size can produce. |
| `DESCRIPTION_CHAR_LIMIT`, `TOOL_FETCH_CHUNK` | Tool-description truncation and Composio batch-fetch size. |
| `NUM_TOOLKITS_TO_SAMPLE`, `TOOLS_PER_TOOLKIT` (in `single_tool_evaluation.py`) | Sampling breadth/depth for the baseline. |

Start small and read `query_ground_truth.json` by hand before trusting any aggregate — the generated
decompositions and labels should be spot-checked, especially after any prompt change.

## Results

*Full run, 100 workflows attempted:*

| Metric | Value |
|---|---|
| Workflows accepted / attempted | 85 / 100 |
| Query-level test cases (scored) | 262 |
| Unlabelable queries (no pool tool fit — not scored) | 30 |
| Rejected workflow decompositions/labelings | 15 |
| Any-required-group hit rate | 71.0% |
| Retrieval recall (strict) | 62.2% |
| Primary-only recall (strict) | 48.5% |
| Judged recall | **not usable this run — 0/262 queries judged** |

Latency: 2.52s average, 2.42s median, 3.33s P95, 12.73s maximum.

Strict-recall numbers above are complete and final — search runs on Composio, not Gemini, so quota never
touched them. Judging is a different story: this run hit Gemini's **daily** free-tier cap
(`GenerateRequestsPerDayPerProjectPerModel-FreeTier`, 500 requests/day) right at the start of the judge
phase, after generation alone had already used a large share of that budget across ~170 decompose+label
calls. Two earlier attempts judged 15/262 and 60/262 before hitting the same wall; this run judged 0. Judged
recall needs a day with enough quota headroom left after generation to get through all 262 judge calls in
one pass — until then, treat strict recall as the trustworthy number and judged recall as not yet measured.

### Single-tool baseline — 174 queries

Primary hit 65.5%, related-only 7.5%, complete miss 27.0%. Explicit 69.0% vs. implicit 62.1%.
Per-toolkit spread is wide: Jira and Airtable near 100%, while **GitHub scored 0%** on both explicit and
implicit queries across 10 sampled tools.

## Key findings

1. **All misses so far are confidently wrong, not empty results.** Search never returns nothing — it returns
   a plausible-looking but incorrect tool, which is worse for an agent than an empty result it could recover
   from. Recurring pattern: the right *toolkit* is found, but a near-neighbour tool inside or outside it gets
   returned instead of the one actually needed (e.g. `QUICKBOOKS_GET_GENERAL_LEDGER_REPORT` instead of
   `QUICKBOOKS_QUERY_ENTITIES`; `HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID` instead of `HUBSPOT_ARCHIVE_PRODUCTS`).

2. **Cross-toolkit intrusion is common.** A generic-sounding query (e.g. "send an email") frequently pulls in
   a domain-matching but wrong-vendor tool instead of the generic operation the task actually needs, especially
   when the query's surrounding vocabulary (job, marketing, support) has a strong toolkit association of its
   own.

3. **Judged recall exceeds strict recall by a wide margin whenever it actually runs** — from an earlier,
   smaller 25-workflow pass that got substantially further through judging before quota cut it off: 66.7%
   strict vs. 81.3% judged, a 14.6-point gap. That's direct, measured evidence that some fraction of "misses"
   are really search finding a correct tool the human-curated pool simply never listed as acceptable for that
   specific query. Strict recall alone understates real performance; judged recall is not yet reliably
   available at the current 100-workflow scale (see below).

4. **Gemini's free-tier *daily* quota (500 requests/day for this model) is the practical bottleneck**, not
   Composio's. Search has run to completion every time; judging has been interrupted three times running at
   this scale (15/262, then 60/262, then 0/262 judged), because generation alone (~170 calls for 85 accepted
   workflows) already consumes most of the daily budget before judging can start. The pipeline survives this
   cleanly (see step 7 above — nothing is lost or corrupted), but a full, reliable judged-recall number at
   100-workflow scale needs either a higher-quota key or judging run as its own pass on a day when generation
   hasn't already spent the budget.

## Artifacts

```
src/query_level_workflow_evaluation/
  query_ground_truth.json     accepted queries (requirement groups) + unlabelable queries
  generation_audit.json       raw LLM responses for both decompose and label stages, rejection reasons
  search_results.csv          per-query metrics: strict recall, judged recall, latency, extras
  raw_search_results/*.json   full request + response per query
  summary_report.md           aggregate metrics, failure examples, unlabelable-query list
  generation_cache.json       (git-ignored) resumable cache of every LLM generation, keyed per workflow
  tool_catalog_cache.json     (git-ignored) cached real tool descriptions fetched from Composio
```

`src/single_tool_evaluation/` follows the same shape. Only the generation/catalog caches are git-ignored —
every scored artifact and audit trail is tracked.
