# Manual audit: workflows 1–5

Companion to `scoring_and_validation_reference.md`. Independently recomputed recall for all 20 scored
queries from workflows 1–5, straight from the raw saved API responses in `raw_search_results/*.json`, and
compared against what `search_results.csv` reports — a check on the scoring pipeline itself, not just the
ground truth. Then looked at what actually came back on each miss to judge whether it reads as a genuine
search failure or a too-narrow ground truth.

## Result: scoring mechanics check out completely

All 20 queries match exactly — 0 mismatches between the CSV's recorded recall and an independent
recomputation using the same set-intersection logic (`group tools ∩ (primary ∪ related) ≠ ∅`), done by hand
outside the script.

| Query | CSV recall | Manually recomputed recall | Match |
|---|---:|---:|---|
| workflow-001-q1 | 0.00 | 0.00 | OK |
| workflow-001-q2 | 0.00 | 0.00 | OK |
| workflow-001-q3 | 0.00 | 0.00 | OK |
| workflow-001-q4 | 0.00 | 0.00 | OK |
| workflow-002-q1 | 1.00 | 1.00 | OK |
| workflow-002-q2 | 0.50 | 0.50 | OK |
| workflow-002-q3 | 1.00 | 1.00 | OK |
| workflow-003-q1 | 1.00 | 1.00 | OK |
| workflow-003-q2 | 0.00 | 0.00 | OK |
| workflow-004-q1 | 0.00 | 0.00 | OK |
| workflow-004-q2 | 0.50 | 0.50 | OK |
| workflow-004-q3 | 1.00 | 1.00 | OK |
| workflow-004-q4 | 1.00 | 1.00 | OK |
| workflow-005-q1 | 1.00 | 1.00 | OK |
| workflow-005-q2 | 0.50 | 0.50 | OK |
| workflow-005-q3 | 1.00 | 1.00 | OK |
| workflow-005-q4 | 1.00 | 1.00 | OK |
| workflow-005-q5 | 0.00 | 0.00 | OK |

The extraction and scoring logic (`extract_results()` / `score_query()`) is doing exactly what it's supposed
to. No bugs found here.

## But the pass surfaced 3 likely ground-truth gaps

Looking past the pass/fail number at *what actually came back* on the misses, three of them read less like
genuine search failures and more like the ground truth being narrower than it should be:

| Query | Ground truth required | What search actually returned | Judgment |
|---|---|---|---|
| `workflow-003-q2` "upload file to OneDrive" | `ONE_DRIVE_UPDATE_FILE_CONTENT` only | `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE` (primary) | Search found a genuine OneDrive upload tool — just not the one specific one pre-labeled. Plausibly should have been an alternative in the same group. |
| `workflow-004-q1` "get approved cards from Trello workflow" | `TRELLO_GET_LISTS_CARDS_BY_ID_LIST` only | `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD_BY_FILTER` (primary) | The query never actually specifies a list vs. a board — a board-level filtered fetch is arguably just as valid an answer. |
| `workflow-005-q5` "write evidence-supported updates in Notion CRM records" | `NOTION_UPDATE_PAGE` only | `NOTION_UPDATE_ROW_DATABASE` / `NOTION_UPSERT_ROW_DATABASE` (primary) | Whether "CRM record" means a database row or a page is genuinely ambiguous from the query text alone; search picked the database-row reading. |

These are exactly the class of case `judged_recall` exists to catch — but none of the three actually got
judged. This 100-workflow run's judging pass hit Gemini's daily quota before reaching any of them (0/262
judged overall — see `read.md`). Right now they're counted as flat misses with no second look, when a fair
reading suggests at least the OneDrive and Trello cases probably deserve credit.

## Contrast: a genuinely correct miss, verified against the live API

`workflow-004-q2`, *"publish carousel content to LinkedIn with a first comment"*, ground truth:

```json
"requirement_groups": [
  { "acceptable_tool_slugs": ["LINKEDIN_CREATE_LINKED_IN_POST"], "purpose": "publish post to LinkedIn" },
  { "acceptable_tool_slugs": ["LINKEDIN_CREATE_COMMENT_ON_POST"], "purpose": "add first comment to LinkedIn post" }
]
```

Re-ran the same query live against `COMPOSIO_SEARCH_TOOLS` directly (outside the pipeline) to double-check.
The response's `related_tool_slugs` came back as `['LINKEDIN_GET_MY_INFO', 'LINKEDIN_INITIALIZE_IMAGE_UPLOAD',
'LINKEDIN_GET_POST_CONTENT', 'LINKEDIN_REGISTER_IMAGE_UPLOAD', 'LINKEDIN_DELETE_POST',
'LINKEDIN_GET_COMPANY_INFO']` — `LINKEDIN_CREATE_COMMENT_ON_POST` never appears anywhere in the response:
not primary, not related, not even mentioned in the full `tool_schemas` block that came back alongside it.
This one is an unambiguous, correctly-scored miss at 50% recall — not a gray area like the three above.

## Net takeaway

The pipeline's arithmetic is trustworthy — every recall value checked traces correctly back to the raw
response. The open risk is entirely in ground-truth completeness for compositional or ambiguous queries,
which was already a documented limitation (`judged_recall` exists specifically to catch it); this audit just
puts three concrete names on it from a small, hand-checked sample. Worth extending this same manual pass to
workflows 6–10 to see whether the pattern holds at a larger sample before treating the ~3-in-18 rate as
representative.
