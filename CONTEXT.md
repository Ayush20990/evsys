# Start here

Read this file first in a new session. It is the shortest path to being useful on this repo:
what exists, what is settled, what is in progress, and the mistakes worth not repeating.
Everything here is deliberately terse — the detail lives in the files named at each point.

## What this project measures

Whether Composio's `COMPOSIO_SEARCH_TOOLS` returns the right tool for a search query: outright
misses, right tool ranked below wrong ones, cross-toolkit confusion, latency.

Two benchmarks, answering different questions:

| | Question | Entry point |
|---|---|---|
| **Primary** | Does search return the right tool for a *predicted* query? | `src/query_level_workflow_evaluation.py`, documented in `read.md` |
| **Agent loop** | What does a *real agent* search for, and does search serve it? | `agent_loop_eval/`, documented in its `README.md` |

Both score against `src/top-100-eval-use-cases.md` — 100 workflows, each with a task
description and a list of tools.

## The three findings that hold up

1. **Ranking is the dominant failure, not retrieval.** Over 100 tasks: 83 capabilities where
   search returned the right tool but left it in `related`, against 4 where a fair query
   genuinely missed. An agent acting on the primary recommendation loses all 83.
2. **The `Tools:` lists are execution logs, not requirement sets.** Every description narrates
   a past session; #32 says outright the agent used tool search to find them. 13 task texts
   describe attempts rather than successes; auth probes and `*_PROXY_EXECUTE` are 3.4% of
   1008 entries. Scoring against them raw is wrong in three directions at once — hence
   requirement-group scoring.
3. **Naming the application does not reliably scope the search.** `"HubSpot list payment links
   ecommerce"` returned `STRIPE_LIST_PAYMENT_LINKS` as its primary result.

## Where things stand

**Run 8** (`agent_loop_eval/run8_full_100tasks/`) — complete, all 100 tasks. Judged group
recall 83%, delivered as `primary` 56%. This is the baseline to compare against.

**Run 9** (`agent_loop_eval/run9_retry_loop/`) — in progress, runs in chunks. Adds a retry
budget: the agent works step by step, judges whether the tool it ran did the job, and searches
again in different words up to 4 times before recording the step unmet.

Run 8 produced *zero* retries across 384 queries, because a mock succeeds on any well-formed
call and nothing ever told the agent a tool was wrong. Run 9's first tasks retry roughly 18%
of the time, so the mechanism works.

```powershell
cd agent_loop_eval
python run9.py 10     # next 10 unfinished tasks, then score + analyse
python run9.py 0      # re-score and re-analyse only; costs ~no quota, safe to repeat
```

Nothing finished is ever repeated: traces, requirement groups, judge verdicts and attribution
are all cached per task or per capability.

## Gemini quota — read before debugging any "exhausted" message

Several hours were lost to this. In order of how much damage each caused:

- **`is_quota_error` must not match `"billing"`.** Google's ordinary *rate-limit* message says
  "check your plan and billing details". Matching it treated every per-minute limit as
  terminal and abandoned whole chunks while the key was fine.
- **A rate limit is not exhaustion.** 429 means either. Only "credits are depleted" /
  "prepayment credits" is fatal; everything else backs off and retries.
- **`run_task` must re-raise `QuotaExhaustedError`.** Swallowing it meant `main()` never saw
  an exhausted key, so rotation never fired while seven unused keys sat in `.env`.
- **`Cannot send a request, as the client has been closed`** is the google-genai SDK closing
  its transport, not a key problem. `call_gemini` rebuilds the client and retries. Untreated
  it silently poisoned a scoring pass: 22 judge calls failed, cached as negatives, judged
  recall fell 37/55 → 33/55 with no visible error.
- **Check `.env` line 3 after any key swap.** A pasted `#` prefix (from the parked
  `#AQ.…` comment lines) produces "API key not valid", reported as the closed-client error.

**Key rotation:** every `AQ.…` string in `.env` is a candidate — active first, then any parked
as comments. Paste spares as comment lines; they are picked up at the next invocation. Only
genuine credit exhaustion advances the rotation.

## Mistakes already made, with the correction

Recorded because each was caught only after producing wrong numbers.

- **Blaming search without knowing the target.** The adequacy judge was not shown the expected
  tool, so it could not tell that "read and update bookings or calendar events" was aimed at a
  *Sheets* capability, and blamed search for returning Calendar tools. Attribution now runs
  deterministic checks first (vendor mismatch, write verb vs `readOnlyHint`) and only asks the
  model what those cannot settle.
- **Reporting a metric that moved opposite to quality.** Flat recall fell while every quality
  signal rose, because a better agent searches less. Session recall is confounded by query
  count; use group recall, or hits-per-query.
- **A prompt defect read as a model limitation.** Single-word queries (`'email'`, `'workflow'`)
  were nearly written up as agent behaviour. The cause was this harness telling the model to
  "search for ONE capability at a time". Anything measured through an LLM harness is a
  property of the harness until a known-good configuration says otherwise.
- **Caching failed calls.** A failed judge call cached as `{}` becomes a permanent "not
  satisfied". Only cache a real verdict.
- **Counting queries that never asked for the capability.** A first draft of the search-failure
  list drew from a run where the agent worked the whole task, so "Google Analytics report"
  appeared as a commit/pull-request failure. Only on-target queries count.

## Reporting rules for this project

- **Quote directly:** counts from set membership — capabilities delivered only in `related`,
  never searched for, catalogue gaps. No judgement involved.
- **Quote with the case list attached:** anything splitting agent fault from search fault. That
  split was revised five times in both directions; `failure_analysis.md` prints the query,
  results and reasoning for every case so any row can be checked.
- **Always give the denominator.** "4 failures" is not evidence; "4 of 20 phrasings" is.
