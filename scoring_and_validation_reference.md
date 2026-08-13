# Validation rejections and scoring examples

Companion reference to `read.md`, with worked examples pulled from the actual 100-workflow run
(`src/query_level_workflow_evaluation/generation_audit.json` and `query_ground_truth.json`).

## All rejection reasons

Two independent validators run — one for the blind decomposition stage, one for the grounded labeling
stage — plus a generic `"generation error"` used whenever the LLM call itself failed or returned unparseable
JSON, at either stage. A rejected workflow contributes **zero** test cases; nothing partial is kept.

### Decomposition stage (`validate_decomposition`)

| Reason | Trigger | Example |
|---|---|---|
| `missing queries list` | Payload isn't a dict, or `"queries"` isn't a list | *(didn't occur in this run)* — LLM returns malformed JSON like `{"result": [...]}` instead of `{"queries": [...]}` |
| `query count outside configured range` | Query count falls outside the workflow's computed `[min_q, max_q]` | **Real, workflow 35**: range was `[2, 2]` (tiny 4-tool pool) but the model returned 3 queries — fetch paginated Instagram comments, post bulk reply ratings, delete duplicate comments |
| `empty or implausibly short query` | A query string is missing or under 3 words | **Real, workflow 29**: one of 7 returned queries failed the word-count check |
| `missing intent` | The one-sentence `intent` field is missing or blank | *(didn't occur)* — a query present but its `intent` field is `""` |
| `duplicate query` | Two queries are identical, case-insensitive | *(didn't occur)* — model repeats "search notion for records" twice with different casing elsewhere |

### Labeling stage (`validate_labels`)

| Reason | Trigger | Example |
|---|---|---|
| `missing query_labels list` | Payload isn't a dict, or `"query_labels"` isn't a list | *(didn't occur)* |
| `query_labels count mismatch` | Number of labels returned ≠ number of queries sent in | *(didn't occur)* — 4 queries sent, only 3 labels returned |
| `query_labels indices incomplete or invalid` | The `query_index` values aren't exactly `1..N` | *(didn't occur)* — indices `[1, 2, 2, 4]`, missing `3` |
| `invalid requirement group count` | A query's `requirement_groups` isn't a list, or has more than 3 groups | **Real, workflow 6**: query 1 ("search leads/contacts, create/update records") got 4 groups — `SALESFORCE_SEARCH_LEADS`, `SALESFORCE_SEARCH_CONTACTS`, `SALESFORCE_CREATE_S_OBJECT_RECORD`/`SALESFORCE_CREATE_A_RECORD`, `SALESFORCE_SOBJECT_ROWS_UPDATE` — one group too many |
| `invalid or invented required tool` | A group's tool list is empty, has more than 4 tools, or references a slug outside that workflow's candidate pool | **Real, workflow 40**: a group referenced `NOTION_UPDATE_SCHEMA_DATABASE`, which wasn't in that workflow's candidate pool |
| `requirement group missing purpose` | A group has tools but no `purpose` text | *(didn't trigger first in this run, but present in the same workflow-40 payload — that group's `purpose` was `''`; the pool-membership check above it fires first)* |

`"generation error"` covers both stages: the LLM call itself raised (network error, malformed/non-JSON
response) before validation could even run.

## Scoring example: does a 2-tool query returning 1 tool count as a hit, or 50%?

It depends entirely on whether the two tools sit in the same requirement group (alternatives) or in
separate groups (composition) — the exact distinction the requirement-groups schema exists to capture.

### Case A — alternatives (same group) → a full hit, not 50%

Real example, `workflow-001-q3`, *"verify asset status and test inertness"*:

```json
"requirement_groups": [
  {
    "acceptable_tool_slugs": ["HUBSPOT_GET_WORKFLOW_BY_ID", "HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL"],
    "purpose": "verify the status and configuration of the created assets"
  }
]
```

One group, two acceptable tools. Scoring checks `group_tools ∩ found_tools ≠ ∅` — if search returns
*either* tool, the group is satisfied. `recall = 1 satisfied / 1 group = 100%`.

### Case B — composition (separate groups) → 50%

Real example, `workflow-004-q2`, *"publish carousel content to LinkedIn with a first comment"*:

```json
"requirement_groups": [
  { "acceptable_tool_slugs": ["LINKEDIN_CREATE_LINKED_IN_POST"], "purpose": "publish post to LinkedIn" },
  { "acceptable_tool_slugs": ["LINKEDIN_CREATE_COMMENT_ON_POST"], "purpose": "add first comment to LinkedIn post" }
]
```

Two separate groups, each needing its own tool. In the actual run, search returned only
`LINKEDIN_CREATE_LINKED_IN_POST`: group 1 satisfied, group 2 missed. `recall = 1 satisfied / 2 groups = 50%`.

**Rule of thumb:** same group → any one tool is a complete success for that requirement; separate groups →
each missed group costs `1/n` of that query's recall.
