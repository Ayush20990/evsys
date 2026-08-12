# Evsys

This repository evaluates the retrieval quality of Composio's `COMPOSIO_SEARCH_TOOLS` tool through three complementary methods:

1. **Single-tool query retrieval** — samples tools from selected toolkits, asks Gemini to create explicit and implicit natural-language queries, and measures whether each original tool returns as a primary or related result.
2. **Multi-tool workflow retrieval** — evaluates a Markdown ground-truth (The markdown file provided)
3. **Synthetic multi-tool stress test** — uses curated coherent toolkit families, Gemini feasibility/subset selection, and full audit logs to generate realistic workflows beyond the manager-provided cases.

All evaluators record two latency fields: `api_search_latency_sec` is the duration of the successful search API call only, while `end_to_end_latency_sec` includes failed retries and retry backoff.

## Methods tried and current results

| Method | What it tests | Current result | Key takeaway |
|---|---|---|---|
| Single-tool explicit vs. implicit retrieval | Gemini generates one query per sampled tool, with and without an app name. The evaluator measures primary hits, related-only hits, misses, and latency. | 90 queries: 62.2% primary hit rate and 33.3% complete-miss rate. Explicit queries achieved 64.4% primary hits vs. 60.0% for implicit queries. | Naming the app helped modestly; GitHub retrieval was materially weaker than Gmail and Slack. |
| Manager-provided multi-tool workflows | 100 realistic, ground-truth workflows. The evaluator aggregates tool slugs across every Composio result entry and measures coverage/recall, precision, extras, and latency. | 33.9% average all-result recall and 38.3% precision. Average API/Search latency was 3.35 seconds. | Retrieval degrades sharply as workflows require more tools: 71.4% recall for 1-3 expected tools, falling to 20.3% for 13+ tools. |
| Synthetic coherent multi-tool stress test | Curated toolkit families are sampled; Gemini creates a feasible workflow and confirms the required subset of supplied candidates. Full generation and search audit artifacts are saved. | 20 accepted workflows: 35.0% all-result recall, 32.5% primary-only recall, and 12.1% precision. Average API/Search latency was 2.77 seconds. | The stress test found frequent complete misses and many near-match or cross-toolkit extras, while preserving an auditable record of all rejected candidate groups. |

Detailed artifacts are available in [the single-tool report](src/single_tool_evaluation/summary_report.md), [the multi-tool report](src/evaluation/composio_search_eval_report.md), and [the synthetic multi-tool report](src/synthetic_multi_tool_evaluation/summary_report.md).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `COMPOSIO_API_KEY` in `.env`. The single-tool and synthetic multi-tool evaluators additionally need `GEMINI_API_KEY`.

## Run

Open either notebook in Jupyter and run its cells in order:

- `notebooks/01_single_tool_search_evaluation.ipynb`
- `notebooks/02_multi_tool_search_evaluation.ipynb`
- `notebooks/03_synthetic_multi_tool_evaluation.ipynb`

The second evaluator expects `top-100-eval-use-cases.md` in the repository root. Single-tool artifacts are written to `src/single_tool_evaluation/`; synthetic artifacts are written to `src/synthetic_multi_tool_evaluation/`. Only generated-query caches are ignored by Git.
