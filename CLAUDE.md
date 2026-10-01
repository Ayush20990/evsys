# Evsys — orientation

Loaded automatically each session. Read this before exploring the repo; it exists so a new
session does not have to re-derive what is already settled. `CONTEXT.md` holds the fuller
version — open it only when this is not enough.

## What this is

Measuring whether Composio's `COMPOSIO_SEARCH_TOOLS` returns the right tool for a query.
Two benchmarks against `src/top-100-eval-use-cases.md` (100 workflows, each with a task and a
tool list):

- `src/query_level_workflow_evaluation.py` — predicted queries. Docs: `read.md`
- `agent_loop_eval/` — a real agent loop, capturing what it actually searches for

## Settled findings — do not re-derive

1. **Ranking, not retrieval, is the dominant failure.** 83 capabilities returned but left in
   `related`, against 4 genuine recall misses, over 100 tasks.
2. **The `Tools:` lists are execution logs, not requirement sets** — they include auth probes,
   retries and `*_PROXY_EXECUTE` fallbacks. Hence requirement-group scoring rather than flat
   set intersection.
3. **Naming the application does not scope the search.** `"HubSpot list payment links"` →
   `STRIPE_LIST_PAYMENT_LINKS` as the primary result.

## Current work

**Run 9** (`agent_loop_eval/run9_retry_loop/`), in progress, chunked. Adds a retry budget:
the agent judges whether the tool it ran did the job and searches again — 4 attempts per step.
Run 8 (`run8_full_100tasks/`, complete, judged recall 83%) is the comparison baseline.

```powershell
cd agent_loop_eval
python run9.py 10    # next 10 unfinished tasks, then score + analyse
python run9.py 0     # re-analyse only; cached, costs ~no Gemini quota
```

Everything is cached and resumable — traces, requirement groups, judge verdicts, attribution.
Nothing finished is repeated. **Do not delete the `*_cache.json` files in a run directory.**

## Gemini quota — check here before debugging an "exhausted" message

- A **rate limit is not exhaustion**. 429 means either. Only "credits are depleted" /
  "prepayment credits" is fatal. `is_quota_error` must **not** match `"billing"` — the ordinary
  rate-limit message says "check your plan and billing details".
- **`Cannot send a request, as the client has been closed`** is the google-genai SDK dropping
  its transport, not a bad key. `call_gemini` rebuilds and retries.
- After any key swap, check `.env` line 3 for a pasted `#` prefix — it produces "API key not
  valid", surfaced as the closed-client error.
- Spare keys are parked in `.env` as `#AQ.…` comment lines and rotated automatically. Only
  genuine exhaustion advances the rotation.

## How this project reports numbers

- **Quotable directly:** counts from set membership (delivered only in `related`, never
  searched for, catalogue gaps).
- **Quotable only with the case list:** any split of agent fault vs search fault. That split
  was revised five times, in both directions.
- **Always give the denominator.** "4 failures" is not evidence; "4 of 20 phrasings" is.

## Working style that fits this repo

- Verify before reporting. Several wrong conclusions here came from plausible-looking
  reasoning that a two-minute check would have overturned — always check tool descriptions and
  schemas rather than inferring from slug names.
- Anything measured through an LLM harness is a property of the harness until a known-good
  configuration says otherwise.
- Say plainly when a number is not trustworthy yet, and why.
