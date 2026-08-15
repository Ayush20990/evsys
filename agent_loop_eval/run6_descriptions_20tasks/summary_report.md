# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 20
- **Tasks completed without error:** 20
- **Total queries captured:** 73
- **Queries per task:** mean 3.6, median 4, min 2, max 6
- **Tool executions:** 56 (34 real, 0 real-failed, 20 mocked)

### Task completion

- **Reported:** 19/20 tasks called `finish_task` (1 truncated before reporting)
- **Completed:** 11/19 of those reported

| Blocked by | Tasks | Counts against search? |
|---|---:|---|
| `data_absent` | 8 | no - the account lacks the record, not a search problem |

Completion is the agent's own report. It is a weak signal on its own -- an agent can believe it finished when it did not -- so read it next to the recall numbers rather than instead of them.

## Per-task breakdown

| Task | Queries | Executions | Steps | Completed | Blocked by | Stop reason |
|---|---:|---:|---:|---|---|---|
| 1 | 4 | 4 | 9 | yes | not_blocked | agent finished |
| 2 | 3 | 21 | 24 | - | - | step ceiling reached |
| 3 | 4 | 5 | 10 | no | data_absent | agent finished |
| 4 | 4 | 1 | 6 | no | data_absent | agent finished |
| 5 | 3 | 2 | 6 | yes | data_absent | agent finished |
| 6 | 4 | 0 | 5 | yes | not_blocked | agent finished |
| 7 | 6 | 6 | 13 | yes | not_blocked | agent finished |
| 8 | 3 | 0 | 4 | yes | not_blocked | agent finished |
| 9 | 3 | 4 | 8 | yes | not_blocked | agent finished |
| 10 | 5 | 0 | 6 | no | data_absent | agent finished |
| 11 | 5 | 0 | 6 | yes | not_blocked | agent finished |
| 12 | 3 | 0 | 4 | yes | not_blocked | agent finished |
| 13 | 3 | 0 | 4 | no | data_absent | agent finished |
| 14 | 2 | 2 | 5 | yes | not_blocked | agent finished |
| 15 | 3 | 0 | 4 | no | data_absent | agent finished |
| 16 | 4 | 1 | 6 | no | data_absent | agent finished |
| 17 | 5 | 0 | 6 | no | data_absent | agent finished |
| 18 | 2 | 2 | 5 | yes | not_blocked | agent finished |
| 19 | 3 | 4 | 8 | yes | not_blocked | agent finished |
| 20 | 4 | 4 | 9 | no | data_absent | agent finished |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `Check payment link feasibility or status in HubSpot` → `HUBSPOT_GET_ACCOUNT_INFO`
2. `Create marketing email in HubSpot` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
3. `Create workflow in HubSpot` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
4. `Create custom object schema in HubSpot` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `retrieve upcoming Google Calendar meeting events` → `GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `create or update Notion database pages or content structured dataset` → `NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT`
3. `verify Notion page content after writing or get page markdown` → `NOTION_GET_PAGE_MARKDOWN`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `Search or list files in OneDrive` → `ONE_DRIVE_ONEDRIVE_LIST_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN`
2. `Download content of a file from OneDrive` → `ONE_DRIVE_GET_ITEM, ONE_DRIVE_DOWNLOAD_FILE`
3. `Upload or update a file in OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
4. `Search items in OneDrive` → `ONE_DRIVE_SEARCH_ITEMS`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `get cards in a Trello list` → `TRELLO_GET_LISTS_CARDS_BY_ID_LIST`
2. `get member boards Trello` → `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER, TRELLO_GET_BOARDS_BY_ID_BOARD`
3. `create share update post LinkedIn` → `LINKEDIN_CREATE_LINKED_IN_POST`
4. `create comment LinkedIn post` → `LINKEDIN_CREATE_COMMENT_ON_POST`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `Gmail outreach drafts and scan email threads` → `GMAIL_LIST_DRAFTS, GMAIL_CREATE_EMAIL_DRAFT`
2. `ClickUp tasks handoffs` → `CLICKUP_CREATE_TASK, CLICKUP_UPDATE_TASK, CLICKUP_GET_TASK`
3. `Notion CRM database pages` → `NOTION_QUERY_DATABASE, NOTION_INSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE, NOTION_CREATE_NOTION_PAGE`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `Salesforce lead creation and management` → `SALESFORCE_CREATE_LEAD, SALESFORCE_SEARCH_LEADS`
2. `Salesforce contact creation and management` → `SALESFORCE_SEARCH_CONTACTS, SALESFORCE_CREATE_CONTACT`
3. `Salesforce campaign campaign members static list reporting` → `SALESFORCE_RUN_SOQL_QUERY`
4. `create campaign member or static list in Salesforce` → `SALESFORCE_ADD_CONTACT_TO_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `Search emails in Gmail or mail service` → `GMAIL_FETCH_EMAILS`
2. `Search calendar events and manage calendar access` → `GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_CREATE_EVENT, GOOGLECALENDAR_DELETE_EVENT`
3. `GitHub search issues pull requests notifications` → `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`
4. `LinkedIn messages notifications posts` → `LINKEDIN_CREATE_LINKED_IN_POST, LINKEDIN_GET_MY_INFO`
5. `SMS send receive text messages Twilio` → `CHATBOTKIT_SET_UP_TWILIO_INTEGRATION, CHATBOTKIT_CREATE_TWILIO_INTEGRATION`
6. `Send SMS message text` → `CLICKSEND_CREATE_SMS_SEND`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `Search video transcripts public API` → `YOUTUBE_LIST_CHANNEL_VIDEOS, SUPADATA_GET_TRANSCRIPT`
2. `mark update archive document status database markdown spreadsheet` → `NOTION_UPDATE_ROW_DATABASE, NOTION_ARCHIVE_NOTION_PAGE, NOTION_MOVE_PAGE`
3. `append text content to Google Doc` → `GOOGLEDOCS_INSERT_TEXT_ACTION`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `generate multimedia travel marketing assets from scripts stock generative media` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE`
2. `send email with generated files or attachments` → `GMAIL_SEND_EMAIL`
3. `create presentation or slides downloadable presentation content` → `GAMMA_GENERATE_GAMMA, GAMMA_GET_GAMMA_FILE_URLS, GAMMA_LIST_THEMES`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `Get list of bank transactions or ledger entries in QuickBooks` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
2. `Delete or void transaction or ledger entry in QuickBooks` → `QUICKBOOKS_READ_INVOICE`
3. `Create journal entry or purchase or deposit in QuickBooks` → `QUICKBOOKS_CREATE_PURCHASE, QUICKBOOKS_QUERY_ACCOUNT`
4. `Create payment or receive payment from customer in QuickBooks` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_PAYMENT`
5. `Get financial reports or Trial Balance or General Ledger in QuickBooks` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_GET_REPORT_TRIAL_BALANCE`

### Task 11
*Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure...*

1. `OneDrive file management and operations knowledge base` → `ONE_DRIVE_LIST_FOLDER_CHILDREN, ONE_DRIVE_ONEDRIVE_CREATE_FOLDER, ONE_DRIVE_SEARCH_ITEMS`
2. `create document text file office onedrive` → `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE`
3. `send discord message operations channel` → `DISCORDBOT_CREATE_MESSAGE`
4. `read file content queue system state file` → `ONE_DRIVE_GET_ITEM, ONE_DRIVE_DOWNLOAD_FILE`
5. `configure gmail labels filters routing` → `GMAIL_LIST_FILTERS`

### Task 12
*Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.*

1. `Retrieve Trello card comments` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD`
2. `Update a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
3. `Update a Trello card properties` → `TRELLO_UPDATE_CARDS_BY_ID_CARD`

### Task 13
*Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.*

1. `search analytics website traffic audit report` → `GOOGLE_ANALYTICS_RUN_REPORT, GOOGLE_ANALYTICS_BATCH_RUN_REPORTS`
2. `contacts mailing list CRM spreadsheet` → `GOOGLESHEETS_UPSERT_ROWS`
3. `send email gmail outreach marketing press` → `GMAIL_SEND_EMAIL`

### Task 14
*Find software engineering job listings matching role, location, remote-work, and salary criteria, compile the results, and send or provide them to someone.*

1. `search job listings software engineering role location remote salary` → `COMPOSIO_SEARCH_WEB`
2. `send email message slack discord teams` → `GMAIL_SEND_EMAIL, SALESFORCE_SEND_EMAIL, SALESFORCE_SEND_EMAIL_FROM_TEMPLATE`

### Task 15
*Process pending invoice emails, persist invoice attachments to cloud storage, update spreadsheet ledgers, verify calculated totals, and label processed messages.*

1. `Search email messages for pending invoice emails` → `GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
2. `Upload file to cloud storage Google Drive` → `GOOGLEDRIVE_UPLOAD_FILE, ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
3. `Update spreadsheet row Google Sheets` → `GOOGLESHEETS_VALUES_UPDATE, GOOGLESHEETS_FORMAT_CELL`

### Task 16
*Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host...*

1. `Audit analytics and search performance for a website` → `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY, GOOGLE_SEARCH_CONSOLE_INSPECT_URL`
2. `List verified sites in Google Search Console` → `GOOGLE_SEARCH_CONSOLE_LIST_SITES`
3. `GitHub repository pull request code modification` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS, GITHUB_COMMIT_MULTIPLE_FILES`
4. `Get Vercel deployment status or Netlify or GitHub deployments` → `VERCEL_GET_PROJECTS, VERCEL_GET_DEPLOYMENTS`

### Task 17
*Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.*

1. `heygen create video with avatar and voice` → `HEYGEN_V2_VIDEO_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`
2. `google drive upload media file` → `GOOGLEDRIVE_UPLOAD_FILE, GOOGLEDRIVE_UPLOAD_FROM_URL`
3. `social media post publish tweet linkedin facebook` → `FACEBOOK_CREATE_POST, LINKEDIN_CREATE_LINKED_IN_POST`
4. `gmail send email support` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
5. `calendar events list update booking schedule` → `GOOGLECALENDAR_EVENTS_LIST, GOOGLECALENDAR_CREATE_EVENT, GOOGLECALENDAR_PATCH_EVENT, GOOGLECALENDAR_DELETE_EVENT, GOOGLECALENDAR_FIND_EVENT`

### Task 18
*Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.*

1. `Search for jobs or job listings on job boards` → `COMPOSIO_SEARCH_WEB`
2. `Send an email using Gmail or SMTP` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 19
*Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.*

1. `search for job postings or listings` → `COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
2. `retrieve or manage resume documents or files` → `NOTION_SEARCH_NOTION_PAGE, NOTION_GET_PAGE_MARKDOWN`
3. `send email via Gmail` → `GMAIL_SEND_EMAIL`

### Task 20
*Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records...*

1. `Google Docs search and get document content` → `GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`
2. `Google Sheets search spreadsheet data` → `GOOGLESHEETS_SEARCH_SPREADSHEETS`
3. `Zoho CRM search contacts leads accounts` → `ZOHO_SEARCH_ZOHO_RECORDS, ZOHO_GET_ZOHO_RECORDS`
4. `QuickBooks search invoices customers payments` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_LIST_INVOICES, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`

