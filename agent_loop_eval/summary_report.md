# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 10
- **Tasks completed without error:** 9
- **Total queries captured:** 86
- **Queries per task:** mean 8.6, median 8, min 3, max 15
- **Tool executions:** 70 (0 real, 0 real-failed, 55 mocked)

## Per-task breakdown

| Task | Queries | Executions | Steps | Stop reason |
|---|---:|---:|---:|---|
| 1 | 9 | 8 | 18 | agent finished |
| 2 | 8 | 10 | 18 | step ceiling reached |
| 3 | 9 | 9 | 18 | step ceiling reached |
| 4 | 12 | 6 | 18 | step ceiling reached |
| 5 | 11 | 7 | 18 | step ceiling reached |
| 6 | 7 | 11 | 18 | step ceiling reached |
| 7 | 15 | 3 | 18 | step ceiling reached |
| 8 | 7 | 8 | 16 | agent finished |
| 9 | 3 | 6 | 10 | agent finished |
| 10 | 5 | 2 | 8 | gemini quota exhausted |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `Check payment link feasibility or creation in HubSpot` → `HUBSPOT_CREATE_FEEDBACK_SUBMISSION`
2. `Create a marketing email in HubSpot` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
3. `Create or manage workflows in HubSpot` → `HUBSPOT_GET_ALL_WORKFLOWS`
4. `Create a new workflow in HubSpot` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
5. `Create custom object schema in HubSpot` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`
6. `List payment links in HubSpot` → `HUBSPOT_LIST_DEALS`
7. `Get account info in HubSpot` → `HUBSPOT_GET_ACCOUNT_INFO`
8. `Get workflow by ID in HubSpot` → `HUBSPOT_GET_WORKFLOW_BY_ID, HUBSPOT_GET_WORKFLOWS`
9. `Get workflow by id in HubSpot` → `HUBSPOT_GET_ALL_WORKFLOWS`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `Retrieve upcoming Google Calendar meeting events` → `GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `Create or update Notion content or database pages with verification` → `NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT`
3. `Search Notion pages` → `NOTION_SEARCH_NOTION_PAGE`
4. `List Google Calendar settings` → `GOOGLECALENDAR_SETTINGS_LIST, GOOGLESUPER_SETTINGS_LIST`
5. `List Google Calendar events with time_min and time_max` → `GOOGLECALENDAR_EVENTS_LIST`
6. `Create a new Notion page` → `NOTION_CREATE_NOTION_PAGE`
7. `Add multiple page content in Notion` → `NOTION_ADD_MULTIPLE_PAGE_CONTENT`
8. `Get page markdown in Notion for verification` → `NOTION_GET_PAGE_MARKDOWN`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `find spreadsheet in OneDrive` → `ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN`
2. `download file from OneDrive` → `ONE_DRIVE_GET_DRIVE_ITEM_BY_SHARING_URL, ONE_DRIVE_DOWNLOAD_FILE`
3. `upload update file content OneDrive` → `ONE_DRIVE_UPDATE_FILE_CONTENT`
4. `remote workbench execute python bash` → `DAYTONA_EXECUTE_COMMAND`
5. `get recent items OneDrive root` → `ONE_DRIVE_LIST_ROOT_DRIVE_CHANGES, ONE_DRIVE_GET_RECENT_ITEMS`
6. `start sandbox daytona` → `DAYTONA_START_SANDBOX, DAYTONA_START_COMPUTER_USE`
7. `list root folder children OneDrive` → `ONE_DRIVE_ONEDRIVE_FIND_FOLDER, ONE_DRIVE_LIST_FOLDER_CHILDREN`
8. `list items in OneDrive folder` → `ONE_DRIVE_ONEDRIVE_LIST_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN`
9. `search items in OneDrive query` → `ONE_DRIVE_SEARCH_ITEMS`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `trello get cards in list or board` → `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_LISTS_CARDS_BY_ID_LIST`
2. `linkedin create post and comment` → `LINKEDIN_CREATE_LINKED_IN_POST`
3. `trello update card move list create list` → `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD, TRELLO_ADD_CARDS, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD, TRELLO_UPDATE_CARDS_BY_ID_CARD`
4. `linkedin add comment to post` → `LINKEDIN_CREATE_COMMENT_ON_POST`
5. `trello create list on board` → `TRELLO_ADD_LISTS`
6. `trello get boards for member` → `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER_BY_FILTER`
7. `trello add comment to card` → `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
8. `trello search query` → `TRELLO_GET_SEARCH_MEMBERS`
9. `trello search cards query` → `TRELLO_GET_SEARCH`
10. `linkedin get my info author urn` → `LINKEDIN_GET_MY_INFO`
11. `linkedin create comment on post schema` → `LINKEDIN_CREATE_COMMENT_ON_POST`
12. `get definition for LINKEDIN_CREATE_COMMENT_ON_POST` → `LINKEDIN_CREATE_COMMENT_ON_POST`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `partner operations pipeline gmail clickup notion` → `NOTION_INSERT_ROW_FROM_NL, NOTION_UPSERT_ROW_DATABASE`
2. `search and read gmail email threads` → `GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID`
3. `clickup create task handoff` → `CLICKUP_CREATE_TASK`
4. `create gmail draft` → `GMAIL_CREATE_EMAIL_DRAFT`
5. `notion query database or search database` → `NOTION_QUERY_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER`
6. `search notion pages workspace` → `NOTION_SEARCH_NOTION_PAGE`
7. `list gmail threads messages` → `GMAIL_LIST_THREADS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID`
8. `clickup get tasks list` → `CLICKUP_GET_FILTERED_TEAM_TASKS, CLICKUP_GET_TASK`
9. `search notion databases workspace pages` → `NOTION_SEARCH_NOTION_PAGE`
10. `notion fetch database data` → `NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_QUERY_DATABASE`
11. `clickup get lists space folder` → `CLICKUP_GET_FOLDERLESS_LISTS, CLICKUP_GET_FOLDERS, CLICKUP_GET_LISTS`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `salesforce leads contacts campaign membership attendance status static list MQL lead activity reporting` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS`
2. `salesforce manage campaigns campaign members campaign member status static list` → `SALESFORCE_SEARCH_CONTACTS, SALESFORCE_SEARCH_CAMPAIGNS, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN`
3. `salesforce create lead contact update campaign member status report` → `SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN, SALESFORCE_UPDATE_LEAD, SALESFORCE_CREATE_LEAD`
4. `salesforce update campaign member status attendance` → `SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_UPDATE_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN`
5. `salesforce update campaign member status field` → `SALESFORCE_UPDATE_CAMPAIGN`
6. `salesforce update sobject campaign member` → `SALESFORCE_UPDATE_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN`
7. `salesforce custom rest api call or campaign member update` → `SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `aggregate productivity signals across email calendar github linkedin sms` → `HUBSPOT_GET_AGGREGATED_STATISTICS, HUBSPOT_GET_AGGREGATED_STATISTIC_INTERVALS`
2. `read email calendar github linkedin sms signals` → `HUBSPOT_READ_EMAIL`
3. `list emails read emails messages` → `HUBSPOT_LIST_EMAILS, ZOHO_MAIL_MESSAGES_LIST_EMAILS`
4. `manage calendar access and events` → `GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_CREATE_EVENT`
5. `github repositories issues pull requests productivity signals` → `GITHUB_GET_A_REPOSITORY, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`
6. `linkedin profile posts messages productivity signals` → `LINKEDIN_GET_MY_INFO, LINKEDIN_CREATE_LINKED_IN_POST`
7. `configure sms receiving and sending text messages` → `CLICKSEND_CREATE_SMS_SEND`
8. `configure sms receiving webhook inbound messages clicksend` → `CLICKSEND_GET_SMS_INBOUND, CLICKSEND_GET_SMS_HISTORY`
9. `list messages emails in inbox` → `AGENT_MAIL_LIST_MESSAGES, MAILTRAP_LIST_MESSAGES`
10. `agent_mail_list_messages` → `AGENT_MAIL_LIST_MESSAGES`
11. `googlecalendar_list_calendars` → `GOOGLECALENDAR_LIST_CALENDARS`
12. `github_list_repositories_for_the_authenticated_user` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`
13. `linkedin_get_my_info` → `LINKEDIN_GET_MY_INFO`
14. `clicksend_get_account` → `CLICKSEND_GET_ACCOUNT, CLICKSEND_GET_RESELLER`
15. `agent_mail_list_inboxes` → `AGENT_MAIL_LIST_INBOXES`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `video transcript knowledge base archive google docs` → `ELEVENLABS_MOVE_BULK_CONVAI_KNOWLEDGE_BASE, ELEVENREADER_MOVE_KNOWLEDGE_BASE_ENTITIES`
2. `get public video transcripts transcript retrieval` → `SUPADATA_GET_TRANSCRIPT, SUPADATA_GET_YOUTUBE_VIDEO`
3. `append to google docs google docs tools` → `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_GET_DOCUMENT_BY_ID, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_INSERT_TEXT_ACTION`
4. `archive documents knowledge base archive mark incomplete` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_GET_DOCUMENT_BY_ID, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
5. `google drive list files search files` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
6. `drive find file search query` → `GOOGLEDRIVE_FIND_FILE`
7. `list all files in google drive` → `GOOGLEDRIVE_FIND_FILE`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `create multimedia travel marketing assets from scripts and stock media` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE`
2. `deliver generated files by email and provide downloadable presentation content` → `GMAIL_SEND_EMAIL`
3. `generate presentation gamma` → `GAMMA_GENERATE_GAMMA, GAMMA_GET_GAMMA_FILE_URLS`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `QuickBooks bank account ledger query transactions reconciliation` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
2. `QuickBooks create update delete void transaction ledger journal entry customer payment` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
3. `QuickBooks void delete transaction payment` → `QUICKBOOKS_READ_INVOICE`
4. `QuickBooks record customer payment` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_PAYMENT`
5. `QuickBooks get trial balance general ledger report` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_GET_REPORT_TRIAL_BALANCE`

