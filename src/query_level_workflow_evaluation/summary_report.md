# Query-Level Workflow Benchmark

## Method
Ground truth is built in two separate passes so neither leaks into the other: stage A blindly decomposes each task into search queries (no tool pool visible); stage B labels each query against the candidate pool's real tool descriptions (not just slugs). Ground truth per query is one or more requirement groups (any one tool within a group satisfies it; all groups are required); a query can also come back with no matching candidate tool at all, which is recorded rather than forced. Query count scales with the candidate-pool size instead of a fixed cap. Queries that miss a group get a secondary judged-recall pass checking whether an actually-returned, unlabeled tool would still plausibly satisfy it.

## Summary
- **Workflows accepted:** 85
- **Query-level test cases (scored):** 262
- **Unlabelable queries (valid decomposition, no candidate tool fit -- not scored):** 30
- **Rejected workflow decompositions/labelings:** 15
- **Average primary recall (strict):** 48.5%
- **Average retrieval recall (strict):** 62.2%
- **Any-required-group hit rate:** 71.0%
- **Average judged recall (strict + plausible unlabeled hits, same denominator as strict recall):** 62.2%
- **Queries sent through the judge pass (recall < 1):** 0/262

## Latency
API/Search latency is the successful call only; end-to-end includes failed attempts and retry backoff.

| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 2.52 | 2.52 |
| Median (P50) | 2.42 | 2.42 |
| P95 | 3.33 | 3.33 |
| Maximum | 12.73 | 12.73 |

## Failure Examples
These are query-level candidates for manual review, not automatic product-bug conclusions. `judged_recall` is a plausibility check, not a second ground truth.

### workflow-020-q4 — recall 0.0%
- **Query:** update customer records and project documentation across Zoho CRM, Google Docs, and Google Sheets
- **Missed purposes:** `update customer records in Zoho CRM; update project documentation in Google Docs; update project documentation and records in Google Sheets`
- **Missed (any-of groups):** `ZOHO_PROXY_EXECUTE; GOOGLEDOCS_INSERT_TEXT_ACTION | GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN; GOOGLESHEETS_UPSERT_ROWS | GOOGLESHEETS_VALUES_UPDATE`

- **Primary returned:** `ZOHO_UPDATE_RELATED_RECORDS`

### workflow-051-q3 — recall 0.0%
- **Query:** query Metabase, Datadog, and spreadsheets for verification evidence
- **Missed purposes:** `Query Metabase for analytics verification; Search Datadog logs for verification evidence; Retrieve spreadsheet data for verification`
- **Missed (any-of groups):** `METABASE_POST_API_DATASET; DATADOG_SEARCH_LOGS; GOOGLESHEETS_BATCH_GET`

- **Primary returned:** `METABASE_METABASE_POST_API_EE_METABOT_TOOLS_GET_DASH_DETAILS`

### workflow-089-q1 — recall 0.0%
- **Query:** search inbound emails and HubSpot marketing assets
- **Missed purposes:** `Search and retrieve inbound emails; Retrieve HubSpot marketing emails; Retrieve HubSpot automation workflows`
- **Missed (any-of groups):** `GOOGLESUPER_FETCH_EMAILS; HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUB_SPOT_ACCOUNT; HUBSPOT_GET_WORKFLOWS | HUBSPOT_GET_ALL_WORKFLOWS`

- **Primary returned:** `HUBSPOT_SEARCH_EMAILS; HUBSPOT_GET_EMAILS`

### workflow-001-q2 — recall 0.0%
- **Query:** create automated email and workflow
- **Missed purposes:** `create or prepare the review-only automated confirmation email; create the confirmation workflow`
- **Missed (any-of groups):** `HUBSPOT_CLONE_MARKETING_EMAIL | HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION; HUBSPOT_CREATE_WORKFLOW`

- **Primary returned:** `INTERCOM_CREATE_DATA_EVENT; INTERCOM_CREATE_TICKET_TYPE; INTERCOM_CREATE_TICKET_TYPE_ATTRIBUTE; INTERCOM_UPDATE_TICKET_TYPE`

### workflow-012-q4 — recall 0.0%
- **Query:** send email and chat messages
- **Missed purposes:** `Handle email communications; Handle chat communications`
- **Missed (any-of groups):** `GMAIL_FETCH_EMAILS; SLACK_SEARCH_MESSAGES`

- **Primary returned:** `OUTLOOK_SEND_EMAIL; MICROSOFT_TEAMS_TEAMS_POST_CHAT_MESSAGE`

### workflow-037-q2 — recall 0.0%
- **Query:** inspect email bodies and download attachments
- **Missed purposes:** `Inspect email bodies; Download attachments`
- **Missed (any-of groups):** `OUTLOOK_GET_MESSAGE; OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT`

- **Primary returned:** `UNISENDER_GET_MESSAGES`

### workflow-037-q4 — recall 0.0%
- **Query:** reply or forward email messages
- **Missed purposes:** `Reply to email messages; Forward email messages`
- **Missed (any-of groups):** `OUTLOOK_REPLY_EMAIL; OUTLOOK_FORWARD_MESSAGE`

- **Primary returned:** `GMAIL_SEND_EMAIL; GMAIL_REPLY_TO_THREAD`

### workflow-039-q1 — recall 0.0%
- **Query:** extract CRM lead activity data into spreadsheet workbook
- **Missed purposes:** `List raw leads from CRM; Import lead data into spreadsheet workbook`
- **Missed (any-of groups):** `KOMMO_LIST_LEADS; GOOGLESHEETS_VALUES_UPDATE`

- **Primary returned:** `GONG_GET_CRM_OBJECTS_V2_CRM_ENTITIES; GOOGLESHEETS_UPSERT_ROWS; ZOHO_GET_RELATED_RECORDS`

### workflow-039-q3 — recall 0.0%
- **Query:** track lead outcomes and update verification summary
- **Missed purposes:** `Track lead conversion outcomes; Update summary and verification in spreadsheet workbook`
- **Missed (any-of groups):** `KOMMO_GET_LEAD; GOOGLESHEETS_VALUES_UPDATE`

- **Primary returned:** `INSTANTLY_GET_VERIFICATION_STATS_FOR_LEAD_LIST; INSTANTLY_GET_LEAD`

### workflow-046-q3 — recall 0.0%
- **Query:** create and update database rows
- **Missed purposes:** `Update existing database row property values; Create and update database rows in bulk or by matching filter`
- **Missed (any-of groups):** `NOTION_UPDATE_PAGE; NOTION_UPSERT_ROW_DATABASE`

- **Primary returned:** `ROCKETADMIN_PUT_TABLE_ROW; NOTION_UPDATE_ROW_DATABASE`

### workflow-070-q3 — recall 0.0%
- **Query:** transfer domain vercel project
- **Missed purposes:** `Retrieve domains attached to a Vercel project; List domains from Vercel to check ownership and details`
- **Missed (any-of groups):** `VERCEL_GET_PROJECT_DOMAINS; VERCEL_LIST_DOMAINS`

- **Primary returned:** `VERCEL_MOVE_PROJECT_DOMAIN; VERCEL_TRANSFER_IN_DOMAIN; VERCEL_CREATE_OR_TRANSFER_DOMAIN`

### workflow-078-q4 — recall 0.0%
- **Query:** normalize deal and lead titles and labels
- **Missed purposes:** `normalize deal titles; normalize lead titles`
- **Missed (any-of groups):** `PIPEDRIVE_UPDATE_DEAL; PIPEDRIVE_UPDATE_LEAD`

- **Primary returned:** `PIPEDRIVE_GET_ALL_LEAD_LABELS`

### workflow-001-q1 — recall 0.0%
- **Query:** check payment link capabilities and configuration
- **Missed purposes:** `check permissions and scopes for payment link features`
- **Missed (any-of groups):** `HUBSPOT_LIST_GRANTED_SCOPES`

- **Primary returned:** `STRIPE_UPDATE_PAYMENT_LINK; STRIPE_GET_PAYMENT_LINK`

### workflow-001-q3 — recall 0.0%
- **Query:** verify asset status and test inertness
- **Missed purposes:** `verify the status and configuration of the created assets`
- **Missed (any-of groups):** `HUBSPOT_GET_WORKFLOW_BY_ID | HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL`

- **Primary returned:** `BLAZEMETER_VALIDATE_WORKSPACES_ASSETS; BLAZEMETER_GET_WORKSPACES_ASSETS2; DATABRICKS_CLEANROOMS_CLEAN_ROOM_ASSETS_GET; WEBFLOW_GET_ASSET; REPAIRSHOPR_GET_ASSET`

### workflow-001-q4 — recall 0.0%
- **Query:** create custom object registration ledger
- **Missed purposes:** `create a custom-object registration ledger schema`
- **Missed (any-of groups):** `HUBSPOT_CREATE_OBJECT_SCHEMA`

- **Primary returned:** `ZENDESK_CREATE_CUSTOM_OBJECT_RECORD`

### workflow-003-q2 — recall 0.0%
- **Query:** upload file to OneDrive
- **Missed purposes:** `upload modified file content back to OneDrive`
- **Missed (any-of groups):** `ONE_DRIVE_UPDATE_FILE_CONTENT`

- **Primary returned:** `GOOGLEDRIVE_UPLOAD_FILE; ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### workflow-004-q1 — recall 0.0%
- **Query:** get approved cards from Trello workflow
- **Missed purposes:** `retrieve cards from a specific Trello list`
- **Missed (any-of groups):** `TRELLO_GET_LISTS_CARDS_BY_ID_LIST`

- **Primary returned:** `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD_BY_FILTER`

### workflow-005-q5 — recall 0.0%
- **Query:** write evidence-supported updates in Notion CRM records
- **Missed purposes:** `Update Notion CRM records with status updates`
- **Missed (any-of groups):** `NOTION_UPDATE_PAGE`

- **Primary returned:** `NOTION_UPSERT_ROW_DATABASE; NOTION_UPDATE_ROW_DATABASE`

### workflow-007-q5 — recall 0.0%
- **Query:** read incoming sms messages
- **Missed purposes:** `read incoming sms messages`
- **Missed (any-of groups):** `CLICKSEND_GET_SMS_INBOUND`

- **Primary returned:** `TELTEL_RECEIVE_INBOUND_SMS`

### workflow-011-q3 — recall 0.0%
- **Query:** send and read Discord messages
- **Missed purposes:** `Retrieve Discord messages`
- **Missed (any-of groups):** `DISCORDBOT_LIST_MESSAGES`

- **Primary returned:** `DISCORDBOT_CREATE_MESSAGE`

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

### workflow-011-q2
- **Query:** check queue and system state files
- **Intent:** Inspect current system state files and operational queues to assess the system's status.

### workflow-012-q5
- **Query:** run automation platform maintenance
- **Intent:** Execute and maintain workflows and automation operations on an integration platform.

### workflow-015-q2
- **Query:** upload file attachments to cloud storage bucket
- **Intent:** Persist the downloaded invoice attachments securely into cloud storage.

### workflow-017-q5
- **Query:** booking schedule management
- **Intent:** Read and update the booking schedule as needed.

### workflow-028-q4
- **Query:** archive video asset in repository
- **Intent:** Store and archive the final video asset into a designated repository.

### workflow-030-q4
- **Query:** generate daily activity summary
- **Intent:** Compile the collected emails, social activity, and meeting transcripts into a cohesive daily summary.

### workflow-031-q4
- **Query:** send notifications through WhatsApp or a Notis channel
- **Intent:** Transmit concise notification messages to designated recipients via WhatsApp or Notis.

### workflow-033-q2
- **Query:** get WhatsApp campaign replies conversions and segments
- **Intent:** Analyze audience replies, downstream conversions, and targeted segments for WhatsApp broadcast campaigns.

### workflow-034-q3
- **Query:** analyze sales development activity hygiene
- **Intent:** Analyze sales-development activity hygiene metrics across deals and contacts.

### workflow-038-q3
- **Query:** send Slack direct message
- **Intent:** Send a direct message via Slack with context derived from the CRM.

### workflow-047-q2
- **Query:** copy meta ads campaign
- **Intent:** Duplicate the existing Meta Ads campaign using the copies capability of the Meta Marketing API.

### workflow-049-q2
- **Query:** convert image files to PDF format
- **Intent:** Download image files and convert them into PDF format for standardized document storage.
