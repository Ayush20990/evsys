# Composio Search Single-Tool Evaluation Report

## Summary

- **Total queries:** 90
- **Primary hit rate:** 62.2%
- **Related hit rate:** 3.3%
- **Demotion rate:** 3.3%
- **Complete miss rate:** 33.3%

## Explicit vs. Implicit Queries

| Variant | Queries | Primary hit | Related hit | Complete miss |
|---|---:|---:|---:|---:|
| explicit | 45 | 64.4% | 6.7% | 28.9% |
| implicit | 45 | 60.0% | 0.0% | 37.8% |

## Primary Hit Rate by Toolkit

| Toolkit | Explicit | Implicit |
|---|---:|---:|
| github | 46.7% | 33.3% |
| gmail | 80.0% | 80.0% |
| slack | 66.7% | 66.7% |

## Latency

API/Search latency is the successful API call only; end-to-end latency includes retry backoff and failed attempts.

| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 3.17 | 3.17 |
| Maximum | 12.28 | 12.28 |

No retry backoff was reflected in this run: API/Search and end-to-end measurements were effectively identical.

## Interpretation

Explicit app naming improved the primary hit rate by 4.4 percentage points and reduced complete misses by 8.9 points. GitHub was notably weaker than Gmail and Slack, especially for similarly named repository, organization, secret, variable, and project operations. Several implicit GitHub queries returned equivalent-looking actions from unrelated integrations, indicating a useful area for contrast-set testing.
