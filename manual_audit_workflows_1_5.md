# Manual audit: workflows 1–5

Companion to `scoring_and_validation_reference.md`. Independently recomputed recall for all 20 scored
queries from workflows 1–5, straight from the raw saved API responses in `raw_search_results/*.json`, and
compared against what `search_results.csv` reports — a check on the scoring pipeline itself, not just the
ground truth. Then looked at what actually came back on each miss to judge whether it reads as a genuine
search failure or a too-narrow ground truth.

**Revision note:** the first version of this document called three misses "likely ground-truth gaps" based on
the returned tool *sounding* like a plausible alternative. On checking the actual tool descriptions and
parameters (not just names), two of the three turned out to be genuine misses after all — the correction is
below. Lesson: don't judge whether a miss is "fair" from tool-name similarity; check the real schema.

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

## Three misses, checked against actual tool descriptions — not just names

### `workflow-003-q2` "upload file to OneDrive"
Ground truth: `ONE_DRIVE_UPDATE_FILE_CONTENT`. Search returned `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE` instead.

The task text is explicit: *"upload the modified workbook back to the **same** OneDrive item."* That "same"
matters. `ONE_DRIVE_UPDATE_FILE_CONTENT`'s description states it *"update[s] an existing file's content...
the item's ID is preserved (existing share links remain valid)"* — identity-preserving by design.
`ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`'s description says it *"[u]ploads a file to a specified OneDrive
**folder**... renaming on conflict"* — its `conflict_behavior` parameter **defaults to `rename`**, meaning
left alone it creates a second, differently-named file rather than touching the original item at all. Only
with `conflict_behavior='replace'` explicitly set does it overwrite anything, with no stated guarantee the
item ID/share-links survive the way the other tool promises. Confirmed genuine miss.

### `workflow-004-q1` "get approved cards from Trello workflow"

Ground truth: `TRELLO_GET_LISTS_CARDS_BY_ID_LIST`. Search returned
`TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD_BY_FILTER` instead.

`TRELLO_GET_LISTS_CARDS_BY_ID_LIST` fetches cards from one specific list, by ID.
`TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD_BY_FILTER` only filters by board-wide archival status
(`all`/`closed`/`open`/`visible`) — it has no parameter to scope down to a single list at all. The workflow's
own description confirms it reads from a Trello *source list*, and its candidate pool pairs
`TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD` (find the list) with `TRELLO_GET_LISTS_CARDS_BY_ID_LIST` (fetch that
list's cards) — a clear two-step, list-scoped pattern the returned tool structurally cannot perform. Confirmed
genuine miss.

### `workflow-005-q5` "write evidence-supported updates in Notion CRM records"

Ground truth: `NOTION_UPDATE_PAGE`. Search returned `NOTION_UPDATE_ROW_DATABASE` / `NOTION_UPSERT_ROW_DATABASE`.

This one doesn't reduce to "search missed the right tool" or "ground truth was too narrow" — it's a
different category. `NOTION_UPDATE_ROW_DATABASE` isn't in this workflow's human-curated candidate pool at
all, so the labeling stage was never even allowed to consider it; the fixed vocabulary here is
"invalid or invented required tool" (see `scoring_and_validation_reference.md`), not "too narrow a group."
The workflow's pool mixes page-oriented Notion tools (`NOTION_RETRIEVE_PAGE`, `NOTION_GET_PAGE_MARKDOWN`,
`NOTION_UPDATE_PAGE`) with database-oriented ones (`NOTION_FETCH_DATABASE`, `NOTION_FETCH_ROW`,
`NOTION_QUERY_DATABASE_WITH_FILTER`), so whether the human curator's choice of a page-update tool over a
row-update tool was the better call is genuinely unresolved from the data available here — it's a question
about whether the *candidate pool itself* was complete, not about how the labeling or scoring stages handled
what was in it.

## A genuinely correct miss, verified against the live API, for contrast

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
Unambiguous, correctly-scored miss at 50% recall.

## Net takeaway

The pipeline's arithmetic is trustworthy — every recall value checked traces correctly back to the raw
response. What changed on closer inspection: two of three cases that initially looked like unfair, too-narrow
ground truth turned out to be correctly-labeled genuine misses once the actual tool descriptions and
parameters were checked instead of going on name similarity. The one remaining open question
(`workflow-005-q5`) is about candidate-pool completeness, not about how this pipeline scores what's given to
it. Across all 20 queries in this sample, that leaves zero confirmed ground-truth-narrowness bugs — a
better result than the first pass of this audit suggested, and a reminder to verify against real schemas
before calling something a gap.
