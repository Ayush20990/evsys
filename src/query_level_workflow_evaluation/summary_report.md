# Query-Level Workflow Benchmark

## Method
Ground truth is built in two separate passes so neither leaks into the other: stage A blindly decomposes each task into search queries (no tool pool visible); stage B labels each query against the candidate pool's real tool descriptions (not just slugs). Ground truth per query is one or more requirement groups (any one tool within a group satisfies it; all groups are required); a query can also come back with no matching candidate tool at all, which is recorded rather than forced. Query count scales with the candidate-pool size instead of a fixed cap. Queries that miss a group get a secondary judged-recall pass checking whether an actually-returned, unlabeled tool would still plausibly satisfy it.

## Summary
- **Workflows accepted:** 9
- **Query-level test cases (scored):** 29
- **Unlabelable queries (valid decomposition, no candidate tool fit -- not scored):** 3
- **Rejected workflow decompositions/labelings:** 1
- **Average primary recall (strict):** 46.6%
- **Average retrieval recall (strict):** 67.2%
- **Any-required-group hit rate:** 79.3%
- **Average judged recall (strict + plausible unlabeled hits, same denominator as strict recall):** 75.9%
- **Queries sent through the judge pass (recall < 1):** 13/29

## Latency
API/Search latency is the successful call only; end-to-end includes failed attempts and retry backoff.

| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 2.75 | 2.75 |
| Median (P50) | 2.62 | 2.62 |
| P95 | 3.70 | 3.70 |
| Maximum | 6.73 | 6.73 |

## Failure Examples
These are query-level candidates for manual review, not automatic product-bug conclusions. `judged_recall` is a plausibility check, not a second ground truth.

### workflow-001-q2 — recall 0.0%
- **Query:** create automated email and workflow
- **Missed purposes:** `create or prepare the review-only automated confirmation email; create the confirmation workflow`
- **Missed (any-of groups):** `HUBSPOT_CLONE_MARKETING_EMAIL | HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION; HUBSPOT_CREATE_WORKFLOW`
- **Judged recall:** 0.0%
- **Primary returned:** `GOOGLESHEETS_BATCH_GET; GMAIL_SEND_EMAIL; GOOGLESHEETS_UPSERT_ROWS`

### workflow-001-q1 — recall 0.0%
- **Query:** check payment link capabilities and configuration
- **Missed purposes:** `check permissions and scopes for payment link features`
- **Missed (any-of groups):** `HUBSPOT_LIST_GRANTED_SCOPES`
- **Judged recall:** 0.0%
- **Primary returned:** `STRIPE_UPDATE_PAYMENT_LINK; STRIPE_GET_PAYMENT_LINK`

### workflow-001-q3 — recall 0.0%
- **Query:** verify asset status and test inertness
- **Missed purposes:** `verify the status and configuration of the created assets`
- **Missed (any-of groups):** `HUBSPOT_GET_WORKFLOW_BY_ID | HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL`
- **Judged recall:** 0.0%
- **Primary returned:** `BLAZEMETER_GET_WORKSPACES_ASSETS2; BLAZEMETER_VALIDATE_WORKSPACES_ASSETS; WEBFLOW_GET_ASSET; DATABRICKS_CLEANROOMS_CLEAN_ROOM_ASSETS_GET`

### workflow-001-q4 — recall 0.0%
- **Query:** create custom object registration ledger
- **Missed purposes:** `create a custom-object registration ledger schema`
- **Missed (any-of groups):** `HUBSPOT_CREATE_OBJECT_SCHEMA`
- **Judged recall:** 0.0%
- **Primary returned:** `ZENDESK_CREATE_CUSTOM_OBJECT_RECORD; HIGHLEVEL_CREATE_OBJECT_RECORD`

### workflow-003-q2 — recall 0.0%
- **Query:** upload file to OneDrive
- **Missed purposes:** `upload modified file content back to OneDrive`
- **Missed (any-of groups):** `ONE_DRIVE_UPDATE_FILE_CONTENT`
- **Judged recall:** 100.0% (group 1 <- ONE_DRIVE_ONEDRIVE_UPLOAD_FILE (high))
- **Primary returned:** `GOOGLEDRIVE_UPLOAD_FILE; ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### workflow-005-q5 — recall 0.0%
- **Query:** write evidence-supported updates in Notion CRM records
- **Missed purposes:** `Update Notion CRM records with status updates`
- **Missed (any-of groups):** `NOTION_UPDATE_PAGE`
- **Judged recall:** 100.0% (group 1 <- NOTION_UPDATE_ROW_DATABASE (high))
- **Primary returned:** `NOTION_UPDATE_ROW_DATABASE; NOTION_UPDATE_BLOCK`

### workflow-002-q2 — recall 50.0%
- **Query:** create or update structured dataset content in Notion
- **Missed purposes:** `Create a new page in Notion for the structured dataset`
- **Missed (any-of groups):** `NOTION_CREATE_NOTION_PAGE`
- **Judged recall:** 50.0%
- **Primary returned:** `NOTION_FETCH_DATABASE; NOTION_QUERY_DATABASE_WITH_FILTER; NOTION_UPSERT_ROW_DATABASE`

### workflow-004-q2 — recall 50.0%
- **Query:** publish carousel content to LinkedIn with a first comment
- **Missed purposes:** `add first comment to LinkedIn post`
- **Missed (any-of groups):** `LINKEDIN_CREATE_COMMENT_ON_POST`
- **Judged recall:** 50.0%
- **Primary returned:** `LINKEDIN_CREATE_LINKED_IN_POST`

### workflow-005-q2 — recall 50.0%
- **Query:** search and retrieve ClickUp tasks and Notion CRM records
- **Missed purposes:** `Retrieve Notion CRM records`
- **Missed (any-of groups):** `NOTION_QUERY_DATABASE_WITH_FILTER | NOTION_SEARCH_NOTION_PAGE`
- **Judged recall:** 50.0%
- **Primary returned:** `CLICKUP_GET_VIEW_TASKS; CLICKUP_GET_TASKS`

### workflow-007-q6 — recall 50.0%
- **Query:** configure sms sending and receiving
- **Missed purposes:** `configure receiving sms`
- **Missed (any-of groups):** `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND | CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`
- **Judged recall:** 50.0%
- **Primary returned:** `CLICKSEND_CREATE_SMS_SEND`

### workflow-007-q7 — recall 50.0%
- **Query:** manage calendar access and events
- **Missed purposes:** `manage calendar events`
- **Missed (any-of groups):** `GOOGLECALENDAR_BATCH_EVENTS`
- **Judged recall:** 100.0% (group 2 <- GOOGLECALENDAR_CREATE_EVENT (high))
- **Primary returned:** `GOOGLECALENDAR_FIND_FREE_SLOTS; GOOGLECALENDAR_FIND_EVENT; GOOGLECALENDAR_CREATE_EVENT`

### workflow-010-q2 — recall 50.0%
- **Query:** undo remove incorrect quickbooks ledger entry
- **Missed purposes:** `remove or undo incorrect ledger entries`
- **Missed (any-of groups):** `QUICKBOOKS_EXECUTE_BATCH_OPERATION`
- **Judged recall:** 50.0%
- **Primary returned:** `NETSUITE_DELETE_JOURNAL_ENTRY; QUICKBOOKS_CREATE_JOURNAL_ENTRY`

### workflow-010-q3 — recall 50.0%
- **Query:** record customer payment quickbooks financial report
- **Missed purposes:** `verify financial reports`
- **Missed (any-of groups):** `QUICKBOOKS_GET_REPORTS`
- **Judged recall:** 50.0%
- **Primary returned:** `QUICKBOOKS_QUERY_ENTITIES; QUICKBOOKS_CREATE_PAYMENT`

## Unlabelable Queries
Stage A produced a genuine sub-intent that stage B found no candidate tool for. Not scored -- reviewed here instead of silently dropped.

### workflow-007-q3
- **Query:** fetch github activity
- **Intent:** Retrieve GitHub contributions, pull requests, and activity logs for productivity tracking.

### workflow-007-q4
- **Query:** check linkedin updates
- **Intent:** Gather professional network notifications and signals from LinkedIn.

### workflow-008-q1
- **Query:** fetch public video transcripts
- **Intent:** This query searches for a tool capable of retrieving transcript data from public videos to build the knowledge base.
