# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 10
- **Tasks completed without error:** 10
- **Total queries captured:** 95
- **Queries per task:** mean 9.5, median 10, min 5, max 13
- **Tool executions:** 52 (0 real, 0 real-failed, 52 mocked)

## Per-task breakdown

| Task | Queries | Executions | Steps | Stop reason |
|---|---:|---:|---:|---|
| 1 | 7 | 5 | 13 | agent finished |
| 2 | 5 | 7 | 13 | agent finished |
| 3 | 12 | 6 | 18 | step ceiling reached |
| 4 | 12 | 4 | 17 | agent finished |
| 5 | 9 | 6 | 16 | agent finished |
| 6 | 12 | 3 | 16 | agent finished |
| 7 | 12 | 6 | 18 | step ceiling reached |
| 8 | 6 | 3 | 10 | agent finished |
| 9 | 7 | 7 | 15 | agent finished |
| 10 | 13 | 5 | 18 | step ceiling reached |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `hubspot` → `HUBSPOT_CREATE_PRODUCTS, HUBSPOT_CREATE_COMPANIES`
2. `payment link` → `STRIPE_GET_PAYMENT_LINK, STRIPE_UPDATE_PAYMENT_LINK, STRIPE_CREATE_PAYMENT_LINK`
3. `email` → `MALWAREBYTES_MCP_REPUTATION_CHECK_EMAIL, OUTLOOK_SEND_EMAIL, ZOHO_MAIL_MESSAGES_SEND_EMAIL, HUBSPOT_CREATE_EMAIL, SALESFORCE_SEND_EMAIL_FROM_TEMPLATE, MAILCHIMP_SEND_TEST_EMAIL, GMAIL_SEND_EMAIL`
4. `workflow` → `BOX_START_WORKFLOW, KADOA_PAUSE_WORKFLOW, GITHUB_GET_A_WORKFLOW, SALESFLARE_CREATE_WORKFLOW, KADOA_RESUME_WORKFLOW`
5. `custom object` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES, SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT, SALESFORCE_RUN_SOQL_QUERY`
6. `hubspot email` → `HUBSPOT_CREATE_EMAIL`
7. `hubspot workflow` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `Google Calendar` → `GOOGLESUPER_CREATE_CALENDAR, GOOGLECALENDAR_LIST_CALENDAR_RESOURCES, GOOGLECALENDAR_DUPLICATE_CALENDAR, GOOGLECALENDAR_EVENTS_LIST, GOOGLECALENDAR_CREATE_CALENDAR, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS, GOOGLECALENDAR_CREATE_EVENT`
2. `Notion` → `NOTION_UPSERT_ROW_DATABASE, NOTION_APPEND_CODE_BLOCKS, NOTION_QUERY_DATABASE, NOTION_ARCHIVE_NOTION_PAGE`
3. `Notion database query or search` → `NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER`
4. `Notion search database` → `NOTION_SEARCH_NOTION_PAGE`
5. `Notion insert row database` → `NOTION_FETCH_DATABASE, NOTION_INSERT_ROW_DATABASE`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `onedrive spreadsheet` → `ONE_DRIVE_DOWNLOAD_ITEM_AS_FORMAT, ONE_DRIVE_RESTORE_ITEM_VERSION, ONE_DRIVE_DOWNLOAD_ITEM_VERSION`
2. `search onedrive files` → `ONE_DRIVE_SEARCH_ITEMS`
3. `upload onedrive file` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
4. `update file content onedrive` → `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE, ONE_DRIVE_UPDATE_FILE_CONTENT`
5. `download file onedrive` → `ONE_DRIVE_GET_DRIVE_ITEM_BY_SHARING_URL, ONE_DRIVE_DOWNLOAD_FILE`
6. `workbench python file execution` → `E2B_POST_SANDBOXES, E2B_CONNECT_SANDBOX`
7. `execute python code` → `E2B_POST_SANDBOXES, E2B_CONNECT_SANDBOX`
8. `composio remote workbench` → `COMPOSIO_SEARCH_WEB`
9. `ONE_DRIVE_SEARCH_ITEMS` → `ONE_DRIVE_SEARCH_ITEMS`
10. `ONE_DRIVE_LIST_DRIVES` → `ONE_DRIVE_LIST_DRIVES`
11. `ONE_DRIVE_LIST_FOLDER_CHILDREN` → `ONE_DRIVE_ONEDRIVE_LIST_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN`
12. `ONE_DRIVE_ONEDRIVE_FIND_FILE` → `ONE_DRIVE_ONEDRIVE_FIND_FILE`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `trello` → `TRELLO_ADD_BOARDS, TRELLO_ADD_CHECKLISTS, TRELLO_ADD_CARDS, TRELLO_CREATE_ORGANIZATION`
2. `linkedin` → `LINKEDIN_GET_PERSON`
3. `get trello cards` → `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD`
4. `trello search boards` → `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER, TRELLO_GET_BOARDS_BY_ID_BOARD`
5. `linkedin create post` → `LINKEDIN_CREATE_LINKED_IN_POST`
6. `linkedin comment` → `LINKEDIN_CREATE_COMMENT_ON_POST`
7. `trello create list update card` → `TRELLO_ADD_CARDS`
8. `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER` → `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER`
9. `TRELLO_GET_SEARCH` → `TRELLO_GET_SEARCH, TRELLO_GET_CARDS_BY_ID_CARD`
10. `LINKEDIN_GET_MY_INFO` → `LINKEDIN_GET_MY_INFO`
11. `TRELLO_UPDATE_LISTS_BY_ID_LIST` → `TRELLO_UPDATE_LISTS_POS_BY_ID_LIST`
12. `TRELLO_ADD_LISTS` → `TRELLO_ADD_LISTS`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `gmail` → `GMAIL_REPLY_TO_THREAD, GMAIL_UPDATE_LANGUAGE_SETTINGS, GMAIL_DELETE_THREAD, GMAIL_SEARCH_PEOPLE, GMAIL_LIST_LABELS, GMAIL_LIST_THREADS, GMAIL_FETCH_EMAILS, GMAIL_LIST_FILTERS`
2. `clickup` → `CLICKUP_GET_TASKS, CLICKUP_CREATE_TASK, CLICKUP_UPDATE_TASK`
3. `notion` → `NOTION_UPSERT_ROW_DATABASE, NOTION_APPEND_CODE_BLOCKS, NOTION_QUERY_DATABASE, NOTION_ARCHIVE_NOTION_PAGE`
4. `list database notion` → `NOTION_FETCH_DATABASE`
5. `search notion page` → `NOTION_SEARCH_NOTION_PAGE`
6. `clickup get teams` → `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES`
7. `get spaces clickup` → `CLICKUP_GET_SPACES`
8. `search notion page database` → `NOTION_SEARCH_NOTION_PAGE`
9. `gmail list messages` → `GMAIL_FETCH_EMAILS`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `Salesforce leads contacts campaign` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS`
2. `campaign contact member static list MQL activity reporting Salesforce` → `SALESFORCE_ADD_CONTACT_TO_CAMPAIGN`
3. `Salesforce campaign` → `SALESFORCE_CREATE_CAMPAIGN`
4. `Salesforce lead contact campaign member status report` → `SALESFORCE_RUN_SOQL_QUERY`
5. `lead status MQL activity campaign member` → `SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN`
6. `CampaignMember status` → `SALESFORCE_ADD_CONTACT_TO_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN`
7. `update campaign member status` → `SALESFORCE_REMOVE_FROM_CAMPAIGN, MAILCHIMP_UPDATE_LIST_MEMBER`
8. `Salesforce update campaign member` → `SALESFORCE_UPDATE_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN`
9. `Salesforce list leads contacts campaigns` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_SEARCH_CONTACTS`
10. `Salesforce search campaigns` → `SALESFORCE_SEARCH_CAMPAIGNS, SALESFORCE_LIST_CAMPAIGNS`
11. `Salesforce list leads` → `KOMMO_LIST_LEADS, SALESFORCE_LIST_LEADS, SALESFORCE_RUN_SOQL_QUERY`
12. `Salesforce list contacts` → `SALESFORCE_LIST_CONTACTS, SALESFORCE_RUN_SOQL_QUERY`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `email` → `OUTLOOK_SEND_EMAIL`
2. `calendar` → `GOOGLECALENDAR_GET_CALENDAR`
3. `github` → `GITHUB_LIST_REPOSITORY_CONTRIBUTORS`
4. `linkedin` → `LINKEDIN_CREATE_LINKED_IN_POST`
5. `sms` → `CLICKSEND_CREATE_SMS_SEND`
6. `gmail` → `GMAIL_REPLY_TO_THREAD, GMAIL_UPDATE_LANGUAGE_SETTINGS, GMAIL_DELETE_THREAD, GMAIL_SEARCH_PEOPLE, GMAIL_LIST_LABELS, GMAIL_LIST_THREADS, GMAIL_FETCH_EMAILS, GMAIL_LIST_FILTERS`
7. `list events` → `SYMPLA_LIST_EVENTS, EVENTZILLA_LIST_EVENTS, FOMO_LIST_EVENTS, DATADOG_LIST_EVENTS, COINMARKETCAL_LIST_EVENTS, EVENTEE_LIST_EVENTS, EXA_LIST_EVENTS`
8. `google calendar events list` → `GOOGLECALENDAR_EVENTS_LIST`
9. `github commits` → `GITHUB_LIST_COMMITS`
10. `linkedin my info` → `LINKEDIN_GET_MY_INFO`
11. `clicksend sms history` → `CLICKSEND_GET_STATISTICS_SMS, CLICKSEND_SMS_HISTORY_GET`
12. `google calendar list calendars` → `GOOGLECALENDAR_LIST_CALENDARS, GOOGLESUPER_LIST_CALENDARS`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `video transcript knowledge base` → `YOUTUBE_VIDEO_DETAILS, YOUTUBE_LIST_CAPTION_TRACK, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
2. `google docs append` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`
3. `knowledge base archive document mark incomplete` → `ELEVENREADER_MOVE_KNOWLEDGE_BASE_ENTITIES, SYNTHFLOW_AI_DELETE_KNOWLEDGE_BASE`
4. `list files or search files or workspace or database or filesystem or storage` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_DOWNLOAD_FILE, ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_DOWNLOAD_FILE`
5. `GOOGLEDRIVE_FIND_FILE` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
6. `search youtube video` → `YOUTUBE_SEARCH_YOU_TUBE, YOUTUBE_GET_VIDEO_DETAILS_BATCH`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `travel marketing assets script media` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE`
2. `email deliver presentation content` → `SLIDESGPT_MCP_CREATE_SLIDES`
3. `send email` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
4. `generate image` → `GEMINI_GENERATE_IMAGE`
5. `get user email address` → `OUTLOOK_GET_USER_BY_EMAIL`
6. `get profile` → `KLAVIYO_GET_PROFILE, DICE_MCP_GET_CANDIDATE`
7. `search contacts or user profile` → `COMPOSIO_SEARCH_WEB`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `QuickBooks` → `QUICKBOOKS_CREATE_BILL`
2. `bank ledger transaction` → `PAYSTACK_FETCH_BALANCE_LEDGER`
3. `QuickBooks ledger account transaction bank` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
4. `QuickBooks transaction create update delete void payment adjustment` → `QUICKBOOKS_READ_INVOICE`
5. `QuickBooks payment deposit journal entry` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
6. `QuickBooks payment deposit` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_PAYMENT`
7. `QuickBooks report balance sheet trial balance` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_GET_REPORT_TRIAL_BALANCE`
8. `QuickBooks query accounts` → `QUICKBOOKS_GET_REPORT_ACCOUNT_LIST, QUICKBOOKS_QUERY_ACCOUNT`
9. `QuickBooks get transaction list report` → `QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
10. `QuickBooks query payment invoice journal deposit` → `QUICKBOOKS_QUERY_ENTITIES`
11. `QuickBooks create deposit` → `QUICKBOOKS_CREATE_DEPOSIT`
12. `QuickBooks delete transaction void journal payment deposit` → `QUICKBOOKS_READ_INVOICE`
13. `QuickBooks update delete journal entry payment deposit` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`

