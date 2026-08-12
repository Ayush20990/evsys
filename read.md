# Evsys

This repository evaluates the retrieval quality of Composio's `COMPOSIO_SEARCH_TOOLS` tool through two distinct methods:

1. **Single-tool query retrieval** — samples tools from selected toolkits, asks Gemini to create explicit and implicit natural-language queries, and measures whether each original tool returns as a primary or related result.
2. **Multi-tool workflow retrieval** — evaluates a Markdown ground-truth suite of use cases with one or more expected tool slugs, reporting precision, recall, latency, and workflow-level misses.

Both evaluators record two latency fields: `api_search_latency_sec` is the duration of the successful search API call only, while `end_to_end_latency_sec` includes failed retries and retry backoff.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `COMPOSIO_API_KEY` in `.env`. The first evaluator additionally needs `GEMINI_API_KEY`.

## Run

Open either notebook in Jupyter and run its cells in order:

- `notebooks/01_single_tool_search_evaluation.ipynb`
- `notebooks/02_multi_tool_search_evaluation.ipynb`

The second evaluator expects `top-100-eval-use-cases.md` in the repository root. Results are intentionally ignored by Git.

## Security

Never commit `.env` or paste live keys into source code. `.env.example` documents the expected variable names.
