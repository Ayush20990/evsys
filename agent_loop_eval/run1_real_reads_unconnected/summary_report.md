# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is gated on Composio's own `readOnlyHint` tag. Read-only tools run for real, so their failures and empty results are genuine signal the agent can react to. Everything else is answered by a mock generated from the tool's declared `output_parameters`; the real API is never called for a write.

## Summary
- **Tasks attempted:** 10
- **Tasks completed without error:** 10
- **Total queries captured:** 85
- **Queries per task:** mean 8.5, median 8, min 7, max 11
- **Tool executions:** 16 (0 real, 12 real-failed, 4 mocked)

## Per-task breakdown

| Task | Queries | Executions | Steps | Stop reason |
|---|---:|---:|---:|---|
| 1 | 11 | 2 | 14 | agent finished |
| 2 | 7 | 1 | 9 | agent finished |
| 3 | 9 | 1 | 11 | agent finished |
| 4 | 7 | 1 | 9 | agent finished |
| 5 | 7 | 3 | 11 | agent finished |
| 6 | 11 | 1 | 13 | agent finished |
| 7 | 10 | 1 | 12 | agent finished |
| 8 | 7 | 1 | 9 | agent finished |
| 9 | 9 | 4 | 14 | agent finished |
| 10 | 7 | 1 | 9 | agent finished |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `hubspot` → `HUBSPOT_CREATE_PRODUCTS, HUBSPOT_CREATE_COMPANIES`
2. `payment link` → `GOCARDLESS_MCP_CREATE_PAYMENT_LINK, STRIPE_GET_PAYMENT_LINK, STRIPE_UPDATE_PAYMENT_LINK, RAZORPAY_NOTIFY_PAYMENT_LINK, POOF_CREATE_PAYMENT_LINK, FLUTTERWAVE_CREATE_PAYMENT_LINK, STRIPE_CREATE_PAYMENT_LINK`
3. `hubspot email workflow custom object` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`
4. `hubspot email workflow` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
5. `hubspot email` → `HUBSPOT_CREATE_EMAIL`
6. `hubspot marketing email` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
7. `hubspot list granted scopes` → `HUBSPOT_LIST_GRANTED_SCOPES`
8. `COMPOSIO_MANAGE_CONNECTIONS` → `RAGIE_LIST_CONNECTIONS_CONNECTIONS_GET`
9. `manage connections` → `CONVEYOR_GET_CONNECTIONS, CELIGO_REGISTER_CONNECTIONS_BULK, ROCKETADMIN_GET_CONNECTIONS`
10. `stripe create payment link` → `STRIPE_CREATE_PAYMENT_LINK`
11. `stripe list payment links` → `STRIPE_LIST_PAYMENT_LINKS`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `Google Calendar` → `GOOGLESUPER_CREATE_CALENDAR, GOOGLESUPER_CLEAR_CALENDAR`
2. `calendar events` → `GOOGLECALENDAR_CREATE_EVENT, GOOGLECALENDAR_FIND_FREE_SLOTS`
3. `list calendar events` → `GOOGLECALENDAR_EVENTS_LIST`
4. `Notion` → `NOTION_QUERY_DATABASE, NOTION_UPSERT_ROW_DATABASE, NOTION_APPEND_CODE_BLOCKS, NOTION_ARCHIVE_NOTION_PAGE`
5. `Notion list search pages databases` → `NOTION_SEARCH_NOTION_PAGE`
6. `COMPOSIO_MANAGE_CONNECTIONS` → `COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
7. `connection` → `CELIGO_REGISTER_CONNECTION, PRISMA_CREATE_CONNECTION`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `onedrive` → `ONE_DRIVE_LIST_ONEDRIVE_SHARED_ITEMS, ONE_DRIVE_ONEDRIVE_FIND_FOLDER, ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE, ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
2. `search files or download file` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_DOWNLOAD_FILE`
3. `onedrive search items` → `ONE_DRIVE_SEARCH_ITEMS`
4. `download file onedrive` → `ONE_DRIVE_GET_DRIVE_ITEM_BY_SHARING_URL, ONE_DRIVE_DOWNLOAD_FILE`
5. `upload file onedrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
6. `update file content onedrive` → `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE, ONE_DRIVE_UPDATE_FILE_CONTENT`
7. `manage connections` → `CONVEYOR_GET_CONNECTIONS, CELIGO_REGISTER_CONNECTIONS_BULK, ROCKETADMIN_GET_CONNECTIONS`
8. `composio manage connections` → `AGENTY_CONNECTIONS_GET_ALL`
9. `connection` → `CELIGO_REGISTER_CONNECTION, PRISMA_CREATE_CONNECTION`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `trello` → `TRELLO_ADD_BOARDS, TRELLO_ADD_CHECKLISTS, TRELLO_ADD_CARDS, TRELLO_CREATE_ORGANIZATION`
2. `linkedin` → `LINKEDIN_CREATE_LINKED_IN_POST`
3. `get trello cards` → `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD`
4. `get my member info trello` → `TRELLO_GET_MEMBERS_ME`
5. `manage connections` → `CONVEYOR_GET_CONNECTIONS, NANGO_CONNECTION_GET, ROCKETADMIN_GET_CONNECTIONS`
6. `COMPOSIO_MANAGE_CONNECTIONS` → `RAGIE_LIST_CONNECTIONS_CONNECTIONS_GET, TURBOT_PIPES_CREATE_USER_WORKSPACE_CONNECTION, TURBOT_PIPES_CREATE_ORG_CONNECTION, TURBOT_PIPES_TEST_USER_WORKSPACE_CONNECTION, CELIGO_GET_INTEGRATION_CONNECTIONS`
7. `connection` → `CELIGO_REGISTER_CONNECTION, PRISMA_CREATE_CONNECTION`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `Gmail` → `GMAIL_REPLY_TO_THREAD, GMAIL_UPDATE_LANGUAGE_SETTINGS, GMAIL_DELETE_THREAD, GMAIL_SEARCH_PEOPLE, GMAIL_LIST_LABELS, GMAIL_LIST_THREADS, GMAIL_FETCH_EMAILS, GMAIL_LIST_FILTERS`
2. `ClickUp` → `CLICKUP_GET_TASKS, CLICKUP_CREATE_TASK, CLICKUP_UPDATE_TASK`
3. `Notion` → `NOTION_UPSERT_ROW_DATABASE, NOTION_APPEND_CODE_BLOCKS, NOTION_QUERY_DATABASE, NOTION_ARCHIVE_NOTION_PAGE`
4. `List Notion databases` → `NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATA, NOTION_QUERY_DATABASE`
5. `connection` → `CELIGO_REGISTER_CONNECTION, PRISMA_CREATE_CONNECTION`
6. `COMPOSIO_MANAGE_CONNECTIONS` → `COMPOSIO_SEARCH_EVENT, COMPOSIO_SEARCH_GROQ_CHAT, COMPOSIO_SEARCH_IMAGE`
7. `COMPOSIO` → `COMPOSIO_SEARCH_WALMART, COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_SHOPPING, COMPOSIO_SEARCH_IMAGE, COMPOSIO_SEARCH_GROQ_CHAT, COMPOSIO_SEARCH_TRENDS, COMPOSIO_SEARCH_HOTELS, COMPOSIO_SEARCH_NEWS, COMPOSIO_SEARCH_AMAZON, COMPOSIO_SEARCH_FLIGHTS`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `Salesforce leads contacts campaigns` → `KOMMO_LIST_LEADS, SALESFORCE_LIST_LEADS, SALESFORCE_RUN_SOQL_QUERY`
2. `Salesforce campaign membership static list MQL activity reporting` → `SALESFORCE_ADD_CONTACT_TO_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN`
3. `Salesforce` → `SALESFORCE_CREATE_CUSTOM_FIELD`
4. `campaign` → `KLAVIYO_GET_CAMPAIGN_CAMPAIGN_MESSAGES, KLAVIYO_CREATE_CAMPAIGN, KLAVIYO_GET_CAMPAIGN, KLAVIYO_GET_CAMPAIGNS, MAILCHIMP_ADD_CAMPAIGN`
5. `lead contact report` → `NUTSHELL_LIST_LEADS_REPORT`
6. `SALESFORCE` → `SALESFORCE_CREATE_CUSTOM_FIELD`
7. `LIST_LEADS` → `HELLOLEADS_LIST_LEADS`
8. `SALESFORCE_ADD_LEAD_TO_CAMPAIGN` → `SALESFORCE_ADD_LEAD_TO_CAMPAIGN`
9. `SOQL` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS, SALESFORCE_QUERY_MORE, SALESFORCE_SERVICE_CLOUD_QUERY_ALL_SOQL, SALESFORCE_LIST_OPPORTUNITIES, SALESFORCE_SERVICE_CLOUD_QUERY_SOQL`
10. `COMPOSIO_MANAGE_CONNECTIONS` → `CONVEYOR_GET_CONNECTIONS, ROCKETADMIN_GET_CONNECTIONS, RAGIE_LIST_CONNECTIONS_CONNECTIONS_GET, TELNYX_LIST_CONNECTIONS, NANGO_LIST_CONNECTIONS, TURBOT_PIPES_ACTOR_LIST_CONNECTIONS, CELIGO_GET_INTEGRATION_CONNECTIONS`
11. `connection` → `CELIGO_REGISTER_CONNECTION, PRISMA_CREATE_CONNECTION`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `email` → `MALWAREBYTES_MCP_REPUTATION_CHECK_EMAIL`
2. `calendar` → `GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_CREATE_EVENT`
3. `GitHub` → `DEEPWIKI_MCP_ASK_QUESTION`
4. `SMS` → `CLICKSEND_CREATE_SMS_SEND`
5. `LinkedIn` → `LINKEDIN_CREATE_LINKED_IN_POST`
6. `gmail` → `GMAIL_REPLY_TO_THREAD, GMAIL_UPDATE_LANGUAGE_SETTINGS, GMAIL_DELETE_THREAD, GMAIL_SEARCH_PEOPLE, GMAIL_LIST_THREADS, GMAIL_FETCH_EMAILS, GMAIL_LIST_FILTERS, GMAIL_LIST_LABELS`
7. `github repository issues pull requests` → `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`
8. `linkedin profile feed` → `LINKEDIN_GET_MY_INFO`
9. `clicksend receive sms webhook messages` → `CLICKSEND_GET_SMS_INBOUND, CLICKSEND_GET_SMS_HISTORY`
10. `COMPOSIO_MANAGE_CONNECTIONS` → `RAGIE_LIST_CONNECTIONS_CONNECTIONS_GET, TURBOT_PIPES_CREATE_USER_WORKSPACE_CONNECTION, TURBOT_PIPES_CREATE_ORG_CONNECTION, TURBOT_PIPES_TEST_USER_WORKSPACE_CONNECTION, CELIGO_GET_INTEGRATION_CONNECTIONS, CONVEYOR_GET_CONNECTIONS`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `knowledge base video transcript google docs` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_GET_DOCUMENT_BY_ID, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
2. `video transcript archive` → `YOUTUBE_VIDEO_DETAILS, YOUTUBE_LIST_CAPTION_TRACK, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
3. `archive file drive storage` → `DROPBOX_ARCHIVE_TEAM_FOLDER`
4. `file drive list read update` → `EXCEL_LIST_FILES, ONE_DRIVE_UPDATE_DRIVE_ITEMS_PERMISSIONS`
5. `drive file list search` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
6. `COMPOSIO_MANAGE_CONNECTIONS` → `CONVEYOR_GET_CONNECTIONS, CELIGO_GET_INTEGRATION_CONNECTIONS, ROCKETADMIN_GET_CONNECTIONS, CELIGO_CREATE_CONNECTION, RAGIE_LIST_CONNECTIONS_CONNECTIONS_GET, CELIGO_REGISTER_CONNECTIONS_BULK, TELNYX_LIST_CONNECTIONS`
7. `connection manage auth` → `CELIGO_CREATE_CONNECTION`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `travel marketing assets` → `GEMINI_GENERATE_IMAGE, CANVA_CREATE_URL_ASSET_UPLOAD_JOB, CANVA_POST_DESIGNS`
2. `email` → `OUTLOOK_SEND_EMAIL, GMAIL_SEND_EMAIL, ZOHO_MAIL_MESSAGES_SEND_EMAIL, SURECONTACT_SEND_EMAIL`
3. `search scripts travel` → `COMPOSIO_SEARCH_FLIGHTS`
4. `presentation download content` → `SLIDESGPT_MCP_CREATE_SLIDES`
5. `generate image travel marketing` → `GEMINI_GENERATE_IMAGE`
6. `video travel marketing` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE`
7. `generate video` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO`
8. `slidesgpt` → `SLIDESGPT_MCP_CREATE_SLIDES, SLIDESGPT_MCP_APPLY_THEME`
9. `send email` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `QuickBooks bank account ledger transaction reconcile` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
2. `quickbooks query bank transactions` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
3. `quickbooks delete update void transaction` → `QUICKBOOKS_READ_INVOICE`
4. `quickbooks payment create customer` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_CUSTOMER`
5. `quickbooks create payment` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_CREATE_BILL_PAYMENT`
6. `quickbooks payment invoice` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_PAYMENT`
7. `COMPOSIO_MANAGE_CONNECTIONS` → `RAGIE_LIST_CONNECTIONS_CONNECTIONS_GET, TURBOT_PIPES_CREATE_USER_WORKSPACE_CONNECTION, TURBOT_PIPES_CREATE_ORG_CONNECTION, TURBOT_PIPES_TEST_USER_WORKSPACE_CONNECTION, CELIGO_GET_INTEGRATION_CONNECTIONS`

