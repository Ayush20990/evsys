# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 20
- **Tasks completed without error:** 20
- **Total queries captured:** 82
- **Queries per task:** mean 4.1, median 4, min 2, max 7
- **Tool executions:** 52 (13 real, 0 real-failed, 26 mocked)

### Task completion

- **Reported:** 20/20 tasks called `finish_task` (0 truncated before reporting)
- **Completed:** 11/20 of those reported

| Blocked by | Tasks | Counts against search? |
|---|---:|---|
| `data_absent` | 8 | no - the account lacks the record, not a search problem |
| `no_suitable_tool` | 1 | **yes** - retrieval failure |

Completion is the agent's own report. It is a weak signal on its own -- an agent can believe it finished when it did not -- so read it next to the recall numbers rather than instead of them.

## Per-task breakdown

| Task | Queries | Executions | Steps | Completed | Blocked by | Stop reason |
|---|---:|---:|---:|---|---|---|
| 1 | 4 | 4 | 9 | yes | not_blocked | agent finished |
| 2 | 2 | 11 | 14 | no | data_absent | agent finished |
| 3 | 2 | 0 | 3 | no | data_absent | agent finished |
| 4 | 5 | 2 | 4 | no | data_absent | agent finished |
| 5 | 5 | 0 | 6 | yes | not_blocked | agent finished |
| 6 | 4 | 0 | 5 | yes | not_blocked | agent finished |
| 7 | 6 | 0 | 7 | yes | not_blocked | agent finished |
| 8 | 4 | 3 | 8 | yes | not_blocked | agent finished |
| 9 | 3 | 3 | 7 | yes | not_blocked | agent finished |
| 10 | 6 | 0 | 7 | no | data_absent | agent finished |
| 11 | 6 | 0 | 7 | yes | not_blocked | agent finished |
| 12 | 7 | 0 | 8 | yes | data_absent | agent finished |
| 13 | 3 | 1 | 5 | no | data_absent | agent finished |
| 14 | 2 | 1 | 4 | no | no_suitable_tool | agent finished |
| 15 | 3 | 0 | 4 | no | data_absent | agent finished |
| 16 | 4 | 2 | 7 | no | data_absent | agent finished |
| 17 | 6 | 13 | 20 | yes | data_absent | agent finished |
| 18 | 2 | 2 | 5 | yes | not_blocked | agent finished |
| 19 | 3 | 5 | 9 | yes | not_blocked | agent finished |
| 20 | 5 | 5 | 11 | no | data_absent | agent finished |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `Check payment link feasibility or capabilities in HubSpot` → `HUBSPOT_CREATE_FEEDBACK_SUBMISSION`
2. `Create marketing email in HubSpot` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
3. `Create automated workflow in HubSpot` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
4. `Create custom object schema in HubSpot` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `Retrieve upcoming Google Calendar meeting events` → `GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `Create or update Notion content database pages` → `NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `find file in OneDrive` → `ONE_DRIVE_ONEDRIVE_FIND_FILE, ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_GET_ITEM`
2. `upload file to OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `Search cards in Trello board by list or label` → `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_LISTS_CARDS_BY_ID_LIST`
2. `Get member boards Trello` → `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER, TRELLO_GET_BOARDS_BY_ID_BOARD`
3. `Create a share post on LinkedIn` → `LINKEDIN_CREATE_LINKED_IN_POST`
4. `Update card or move card to another list in Trello` → `TRELLO_UPDATE_CARDS_BY_ID_CARD`
5. `Create list or update list on Trello board` → `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_ADD_LISTS`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `create an email draft in Gmail` → `GMAIL_CREATE_EMAIL_DRAFT`
2. `create a task in ClickUp` → `CLICKUP_CREATE_TASK`
3. `update an existing task in ClickUp` → `CLICKUP_UPDATE_TASK, CLICKUP_GET_TASK`
4. `query or update Notion database pages` → `NOTION_QUERY_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER`
5. `update a Notion page property` → `NOTION_UPDATE_ROW_DATABASE`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `salesforce leads` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS`
2. `salesforce contacts` → `SALESFORCE_LIST_CONTACTS, SALESFORCE_RUN_SOQL_QUERY`
3. `salesforce campaign membership attendance statuses` → `SALESFORCE_ADD_CONTACT_TO_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN`
4. `salesforce campaign static list mql lead activity reporting` → `SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_LIST_LEADS`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `Read or aggregate emails for productivity signals` → `GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
2. `List or fetch calendar events` → `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
3. `Search or fetch GitHub issues PRs or activity` → `GITHUB_LIST_COMMITS, GITHUB_FIND_PULL_REQUESTS, GITHUB_LIST_REPOSITORY_EVENTS`
4. `Search or fetch LinkedIn activity or posts` → `LINKEDIN_GET_COMPANY_INFO`
5. `Send or receive SMS messages` → `BREVO_CREATE_SMS_CAMPAIGN, MSG91_SEND_SMS`
6. `Create modify or delete calendar events` → `GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_PATCH_EVENT, GOOGLECALENDAR_DELETE_EVENT, GOOGLECALENDAR_CREATE_EVENT`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `search or retrieve public video transcripts` → `YOUTUBE_LIST_CHANNEL_VIDEOS, SUPADATA_GET_TRANSCRIPT`
2. `search archive documents or knowledge base database` → `NOTION_SEARCH_NOTION_PAGE, NOTION_GET_PAGE_MARKDOWN`
3. `append content to Google Docs` → `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN, GMAIL_CREATE_EMAIL_DRAFT, GMAIL_SEND_DRAFT`
4. `append content to end of Google Doc` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `Create video or multimedia marketing assets from scripts and stock media` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO`
2. `Send an email with attachments` → `GMAIL_SEND_EMAIL`
3. `Create or update presentation content in Google Slides` → `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `QuickBooks get transactions bank account ledger` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
2. `QuickBooks delete void purchase invoice payment transaction` → `MOCO_DELETE_PURCHASE_PAYMENT`
3. `QuickBooks delete void transaction purchase invoice bill payment` → `QUICKBOOKS_READ_INVOICE`
4. `QuickBooks create journal entry adjustment` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
5. `QuickBooks create customer payment` → `QUICKBOOKS_CREATE_PAYMENT`
6. `QuickBooks get financial reports balance sheet profit loss trial balance` → `QUICKBOOKS_GET_BALANCE_SHEET_REPORT`

### Task 11
*Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure...*

1. `search or list files in OneDrive` → `ONE_DRIVE_ONEDRIVE_LIST_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN`
2. `create or upload file in OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
3. `send message or manage channels in Discord` → `DISCORDBOT_CREATE_MESSAGE`
4. `read file or check queue in system or storage` → `ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN, ONE_DRIVE_DOWNLOAD_FILE`
5. `configure labels or routing or filters in Gmail` → `GMAIL_LIST_LABELS, GMAIL_CREATE_LABEL`
6. `create filter or routing rule in Gmail` → `GMAIL_FETCH_EMAILS, GMAIL_LIST_THREADS`

### Task 12
*Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.*

1. `Retrieve comments from a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD`
2. `Update a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
3. `Update Trello card properties such as name or description` → `TRELLO_UPDATE_CARDS_BY_ID_CARD`
4. `List or manage Trello boards and lists` → `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER`
5. `Send an email message` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
6. `Send a chat message on Slack or similar chat platform` → `SLACK_SEND_MESSAGE, SLACKBOT_SEND_MESSAGE`
7. `Manage workflows or automations in Make or Zapier` → `DOCSAUTOMATOR_CREATE_AUTOMATION, HUBSPOT_CREATE_WORKFLOW`

### Task 13
*Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.*

1. `Retrieve website search performance and traffic analytics` → `COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
2. `Google Analytics website traffic audit search performance` → `GOOGLE_ANALYTICS_RUN_REPORT, GOOGLE_ANALYTICS_BATCH_RUN_REPORTS`
3. `Send email outreach marketing campaign` → `GMAIL_CREATE_EMAIL_DRAFT, GMAIL_SEND_DRAFT`

### Task 14
*Find software engineering job listings matching role, location, remote-work, and salary criteria, compile the results, and send or provide them to someone.*

1. `search software engineering job listings by role location remote salary` → `COMPOSIO_SEARCH_WEB`
2. `send message or email communication tool` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 15
*Process pending invoice emails, persist invoice attachments to cloud storage, update spreadsheet ledgers, verify calculated totals, and label processed messages.*

1. `Search messages in Gmail with query` → `GMAIL_FETCH_EMAILS`
2. `Upload file to Google Drive` → `GOOGLEDRIVE_UPLOAD_FILE, GOOGLEDRIVE_UPLOAD_FROM_URL`
3. `Append row or update spreadsheet in Google Sheets` → `GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_UPSERT_ROWS, GMAIL_FETCH_EMAILS`

### Task 16
*Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host...*

1. `audit analytics and search performance website` → `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY, GOOGLE_SEARCH_CONSOLE_INSPECT_URL`
2. `list verified sites google search console` → `GOOGLE_SEARCH_CONSOLE_LIST_SITES`
3. `inspect modify source repository and create pull requests git github` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_COMMIT_MULTIPLE_FILES, GITHUB_CREATE_A_PULL_REQUEST`
4. `investigate hosting and deployment state vercel netlify render aws` → `VERCEL_GET_DEPLOYMENTS, VERCEL_GET_DEPLOYMENT`

### Task 17
*Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.*

1. `Create AI avatar promo video using HeyGen avatar and voice` → `HEYGEN_V2_VIDEO_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`
2. `Prepare supporting media images audio video` → `GEMINI_GENERATE_IMAGE, GEMINI_GENERATE_VIDEOS`
3. `Publish post to social media platforms` → `LINKEDIN_CREATE_LINKED_IN_POST`
4. `Send support email for infrastructure issues` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
5. `Read and update booking schedule calendar appointments` → `GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_CREATE_EVENT, CAL_LIST_EVENT_TYPES, CAL_GET_AVAILABLE_SLOTS_INFO, CAL_POST_NEW_BOOKING_REQUEST`
6. `List HeyGen avatars` → `HEYGEN_LIST_ALL_AVATAR_GROUPS, HEYGEN_LIST_GROUP_AVATARS`

### Task 18
*Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.*

1. `search job board listings remote hybrid contract data engineering` → `COMPOSIO_SEARCH_WEB`
2. `send email message` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 19
*Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.*

1. `search job postings or job boards for Java backend and Spring Boot jobs` → `COMPOSIO_SEARCH_WEB`
2. `retrieve or build tailored resume documents` → `NOTION_SEARCH_NOTION_PAGE, NOTION_GET_PAGE_MARKDOWN`
3. `send email through Gmail` → `GMAIL_SEND_EMAIL`

### Task 20
*Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records...*

1. `search or read google docs documentation` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_GET_DOCUMENT_BY_ID, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
2. `search or read google sheets` → `GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_VALUES_GET`
3. `search or get zoho crm records` → `ZOHO_SEARCH_ZOHO_RECORDS, ZOHO_GET_ZOHO_RECORDS`
4. `search or read quickbooks invoices or customers` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_READ_INVOICE`
5. `search google drive files or folders` → `GOOGLEDRIVE_FIND_FILE`

