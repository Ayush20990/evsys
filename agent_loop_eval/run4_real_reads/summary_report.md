# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 10
- **Tasks completed without error:** 6
- **Total queries captured:** 37
- **Queries per task:** mean 4.6, median 4, min 3, max 8
- **Tool executions:** 52 (32 real, 0 real-failed, 10 mocked)

## Per-task breakdown

| Task | Queries | Executions | Steps | Stop reason |
|---|---:|---:|---:|---|
| 1 | 4 | 5 | 10 | agent finished |
| 2 | 3 | 13 | 17 | agent finished |
| 3 | 8 | 9 | 18 | agent finished |
| 4 | 5 | 8 | 14 | agent finished |
| 5 | 6 | 3 | 10 | agent finished |
| 6 | 3 | 7 | 11 | agent finished |
| 7 | 5 | 6 | 12 | gemini quota exhausted |
| 8 | 3 | 1 | 5 | gemini quota exhausted |
| 9 | 0 | 0 | 1 | gemini quota exhausted |
| 10 | 0 | 0 | 1 | gemini quota exhausted |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `HubSpot payment links create or check feasibility` → `HUBSPOT_CREATE_DEALS`
2. `HubSpot create email marketing template` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
3. `HubSpot create workflow automation` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
4. `HubSpot create custom object schema` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `Retrieve upcoming Google Calendar meeting events` → `GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `Create or update Notion database or page content with verification` → `NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT`
3. `Search Notion database or pages` → `NOTION_SEARCH_NOTION_PAGE`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `Find and download a spreadsheet file from OneDrive` → `ONE_DRIVE_DOWNLOAD_FILE_BY_PATH`
2. `Search for files in OneDrive` → `ONE_DRIVE_SEARCH_ITEMS`
3. `Upload a file back to OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
4. `Update file content in OneDrive` → `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE, ONE_DRIVE_UPDATE_FILE_CONTENT`
5. `Run a python script or workbench command to manipulate files or execute code` → `E2B_POST_SANDBOXES, E2B_CONNECT_SANDBOX`
6. `Execute python code or workbench command` → `E2B_POST_SANDBOXES, E2B_CONNECT_SANDBOX`
7. `List available E2B sandbox templates` → `E2B_GET_HEALTH, E2B_LIST_SANDBOXES, E2B_LIST_TEMPLATES, E2B_LIST_WEBHOOKS`
8. `Upload file using OneDrive upload file tool` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `get cards from Trello board workflow` → `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD`
2. `publish post to LinkedIn` → `LINKEDIN_CREATE_LINKED_IN_POST`
3. `add comment to LinkedIn post` → `LINKEDIN_CREATE_COMMENT_ON_POST`
4. `update Trello card status or add comment` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
5. `update create Trello list on board` → `TRELLO_ADD_LISTS`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `gmail create draft search email threads` → `GMAIL_LIST_THREADS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID, GMAIL_CREATE_EMAIL_DRAFT`
2. `clickup create task update task handoff` → `CLICKUP_CREATE_TASK`
3. `notion query database update page crm` → `NOTION_FETCH_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_INSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE`
4. `notion search page database` → `NOTION_SEARCH_NOTION_PAGE`
5. `clickup update task details` → `CLICKUP_UPDATE_TASK, CLICKUP_GET_TASK`
6. `clickup get teams workspaces` → `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `Salesforce leads contacts campaign membership campaign attendance status static list MQL lead activity reporting` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS`
2. `Salesforce search campaigns campaign members attendance status` → `SALESFORCE_SEARCH_CAMPAIGNS, SALESFORCE_LIST_CAMPAIGNS`
3. `Salesforce MQL lead activity reporting leads contacts reports` → `SALESFORCE_GET_S_OBJECTS_UPDATED, SALESFORCE_GET_COMPOSITE_SOBJECTS, SALESFORCE_RUN_SOQL_QUERY`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `search email messages in gmail` → `GMAIL_FETCH_EMAILS`
2. `search calendar events in google calendar` → `GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_EVENTS_LIST`
3. `search github notifications or issues` → `GITHUB_LIST_NOTIFICATIONS`
4. `send and receive sms messages` → `CLICKSEND_CREATE_SMS_SEND`
5. `search linkedin profile and messages` → `LINKEDIN_GET_MY_INFO`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `Get public video transcripts or search videos` → `SUPADATA_GET_TRANSCRIPT, SUPADATA_GET_YOUTUBE_VIDEO, NOTION_CREATE_NOTION_PAGE`
2. `Search and append or edit Google Docs documents` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
3. `Search spreadsheet rows or database items or files to mark incomplete archive documents` → `NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_FETCH_DATABASE`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

_(no queries issued)_

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

_(no queries issued)_

