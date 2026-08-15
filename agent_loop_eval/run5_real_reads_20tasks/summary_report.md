# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 20
- **Tasks completed without error:** 20
- **Total queries captured:** 94
- **Queries per task:** mean 4.7, median 5, min 2, max 9
- **Tool executions:** 69 (15 real, 0 real-failed, 43 mocked)

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
| 1 | 5 | 7 | 13 | yes | not_blocked | agent finished |
| 2 | 3 | 8 | 12 | yes | not_blocked | agent finished |
| 3 | 5 | 1 | 7 | no | data_absent | agent finished |
| 4 | 5 | 0 | 6 | no | data_absent | agent finished |
| 5 | 6 | 0 | 7 | no | data_absent | agent finished |
| 6 | 5 | 3 | 9 | yes | data_absent | agent finished |
| 7 | 6 | 0 | 7 | yes | not_blocked | agent finished |
| 8 | 5 | 1 | 7 | yes | not_blocked | agent finished |
| 9 | 4 | 8 | 13 | yes | not_blocked | agent finished |
| 10 | 6 | 5 | 12 | no | data_absent | agent finished |
| 11 | 5 | 0 | 6 | no | no_suitable_tool | agent finished |
| 12 | 4 | 1 | 6 | no | data_absent | agent finished |
| 13 | 3 | 3 | 7 | yes | not_blocked | agent finished |
| 14 | 2 | 2 | 5 | yes | not_blocked | agent finished |
| 15 | 4 | 5 | 10 | no | data_absent | agent finished |
| 16 | 5 | 2 | 8 | no | data_absent | agent finished |
| 17 | 9 | 14 | 24 | yes | not_blocked | agent finished |
| 18 | 4 | 3 | 8 | yes | not_blocked | agent finished |
| 19 | 3 | 3 | 7 | yes | not_blocked | agent finished |
| 20 | 5 | 3 | 9 | no | data_absent | agent finished |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `check payment link feasibility or status in hubspot` → `STRIPE_GET_PAYMENT_LINK, HUBSPOT_GET_ACCOUNT_INFO`
2. `create email in hubspot` → `HUBSPOT_CREATE_EMAIL`
3. `create workflow in hubspot` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
4. `verify status or check settings of hubspot assets or workflows` → `HUBSPOT_GET_ACCOUNT_INFO`
5. `create custom object schema in hubspot` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `Retrieve upcoming Google Calendar meeting events` → `GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `Create or update Notion content containing a large structured dataset` → `NOTION_INSERT_ROW_DATABASE, NOTION_ADD_MULTIPLE_PAGE_CONTENT, NOTION_SEARCH_NOTION_PAGE`
3. `Verify Notion content after writing` → `NOTION_SEARCH_NOTION_PAGE, NOTION_GET_PAGE_MARKDOWN`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `Find a spreadsheet file in OneDrive` → `ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_GET_ITEM`
2. `Download a file from OneDrive` → `ONE_DRIVE_GET_ITEM, ONE_DRIVE_DOWNLOAD_FILE`
3. `Upload a file back to OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
4. `Verify cloud copy of a file in OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE, ONE_DRIVE_ONEDRIVE_FIND_FILE`
5. `Search items in OneDrive` → `ONE_DRIVE_SEARCH_ITEMS`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `Find approved cards in Trello board` → `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD_BY_FILTER, TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD`
2. `Publish a carousel post to LinkedIn` → `LINKEDIN_CREATE_LINKED_IN_POST`
3. `Add a comment to a LinkedIn post` → `LINKEDIN_CREATE_COMMENT_ON_POST`
4. `Update a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
5. `Create a list on a Trello board` → `TRELLO_ADD_LISTS`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `Create draft email in Gmail` → `GMAIL_CREATE_EMAIL_DRAFT`
2. `Create task in ClickUp` → `CLICKUP_CREATE_TASK`
3. `Update task in ClickUp` → `CLICKUP_UPDATE_TASK, CLICKUP_GET_TASK`
4. `Search database in Notion` → `NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_QUERY_DATABASE`
5. `Update database row page in Notion` → `NOTION_UPDATE_ROW_DATABASE`
6. `Search messages in Gmail` → `GMAIL_FETCH_EMAILS`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `salesforce manage leads contacts and campaign membership` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_SEARCH_CONTACTS`
2. `salesforce manage campaign members and attendance statuses` → `SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN`
3. `salesforce campaign static list and MQL lead activity reporting` → `SALESFORCE_RUN_SOQL_QUERY`
4. `salesforce run soql query lead activity reporting mql` → `SALESFORCE_RUN_SOQL_QUERY`
5. `run soql query` → `SALESFORCE_RUN_SOQL_QUERY`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `search emails in gmail` → `GMAIL_FETCH_EMAILS`
2. `search calendar events in google calendar` → `GOOGLECALENDAR_FIND_EVENT`
3. `fetch github activity and PRs or issues` → `GITHUB_LIST_COMMITS, GITHUB_FIND_PULL_REQUESTS, GITHUB_LIST_REPOSITORY_EVENTS`
4. `fetch linkedin activity or messages or posts` → `LINKEDIN_GET_COMPANY_INFO`
5. `send or receive sms messages` → `BREVO_CREATE_SMS_CAMPAIGN, MSG91_SEND_SMS`
6. `manage google calendar access and create events` → `GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_CREATE_EVENT, GOOGLECALENDAR_DELETE_EVENT`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `Search for video transcripts` → `FIREFLIES_SEARCH_TRANSCRIPTS, FIREFLIES_GET_TRANSCRIPTS`
2. `Update or mark archive documents in Google Drive or Notion` → `NOTION_UPDATE_ROW_DATABASE, NOTION_ARCHIVE_NOTION_PAGE, NOTION_MOVE_PAGE`
3. `Append text or content to an existing Google Doc` → `GOOGLEDOCS_INSERT_TEXT_ACTION`
4. `search youtube videos or transcripts` → `YOUTUBE_SEARCH_YOU_TUBE, YOUTUBE_GET_VIDEO_DETAILS_BATCH`
5. `get transcript for a youtube video` → `YOUTUBE_VIDEO_DETAILS, YOUTUBE_LIST_CAPTION_TRACK`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `generate multimedia travel marketing assets or videos from scripts` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE`
2. `send email with attachments or links` → `GMAIL_SEND_EMAIL`
3. `create presentation slides or export presentation content` → `GAMMA_GENERATE_GAMMA, GAMMA_GET_GAMMA_FILE_URLS, GAMMA_LIST_THEMES`
4. `search google drive files or documents` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `QuickBooks query bank transactions` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
2. `QuickBooks delete or void transaction` → `QUICKBOOKS_READ_INVOICE`
3. `QuickBooks create journal entry` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
4. `QuickBooks create payment` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_CREATE_BILL_PAYMENT`
5. `QuickBooks get financial reports balance sheet trial balance` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_GET_REPORT_TRIAL_BALANCE`
6. `QuickBooks create payment receive payment` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_PAYMENT`

### Task 11
*Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure...*

1. `Search OneDrive files` → `ONE_DRIVE_SEARCH_ITEMS`
2. `Create file in OneDrive` → `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE`
3. `Send Discord message` → `DISCORDBOT_CREATE_MESSAGE`
4. `Read queue and system state files` → `CLORO_GET_ASYNC_QUEUE_STATUS`
5. `Configure Gmail labels and filters` → `GMAIL_LIST_LABELS, GMAIL_CREATE_LABEL`

### Task 12
*Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.*

1. `retrieve Trello card comments` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD`
2. `update a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
3. `send email and slack message` → `SLACK_SEND_MESSAGE, GMAIL_SEND_EMAIL`
4. `automation platform trigger or run` → `GOOGLECALENDAR_CREATE_EVENT`

### Task 13
*Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.*

1. `audit website search traffic performance` → `GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
2. `prepare email marketing contact lists spreadsheet` → `GMAIL_GET_CONTACTS, GMAIL_SEARCH_PEOPLE`
3. `send outreach emails gmail` → `GMAIL_SEND_EMAIL`

### Task 14
*Find software engineering job listings matching role, location, remote-work, and salary criteria, compile the results, and send or provide them to someone.*

1. `Search software engineering job listings` → `COMPOSIO_SEARCH_WEB`
2. `Send email or message with job listings` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 15
*Process pending invoice emails, persist invoice attachments to cloud storage, update spreadsheet ledgers, verify calculated totals, and label processed messages.*

1. `search email messages for pending invoices` → `GMAIL_FETCH_EMAILS`
2. `upload file attachment to cloud storage drive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
3. `append row or update spreadsheet ledger` → `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
4. `add label to email message` → `GMAIL_ADD_LABEL_TO_EMAIL, GMAIL_BATCH_MODIFY_MESSAGES`

### Task 16
*Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host...*

1. `Audit analytics and search performance for website in Google Analytics or Search Console` → `GOOGLESUPER_RUN_REPORT, GOOGLESUPER_BATCH_RUN_REPORTS`
2. `Inspect and modify source code repository in GitHub or GitLab` → `GITLAB_GET_FILE, GITLAB_GET_RAW_FILE, GITLAB_UPDATE_REPOSITORY_FILE`
3. `Create pull request or merge request in GitHub or GitLab` → `GITHUB_MERGE_A_PULL_REQUEST`
4. `Investigate hosting and deployment state in Vercel or Netlify or AWS` → `VERCEL_GET_DEPLOYMENTS, VERCEL_GET_DEPLOYMENT`
5. `List Google Analytics properties` → `GOOGLE_ANALYTICS_LIST_ACCOUNT_SUMMARIES`

### Task 17
*Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.*

1. `create video with heygen avatar` → `HEYGEN_V2_VIDEO_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`
2. `generate image or media` → `GEMINI_GENERATE_VIDEOS`
3. `publish post to social media or twitter or linkedin` → `TWITTER_USER_LOOKUP_BY_USERNAME, TWITTER_CREATION_OF_A_POST, LINKEDIN_GET_MY_INFO, LINKEDIN_CREATE_LINKED_IN_POST`
4. `send email support ticket` → `BENCHMARK_EMAIL_GENERATE_TICKET, FRESHDESK_CREATE_TICKET_OUTBOUND_EMAIL, SALESFORCE_SEND_EMAIL, GMAIL_SEND_EMAIL`
5. `booking schedule calendar appointments` → `GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_CREATE_EVENT, CAL_LIST_EVENT_TYPES, CAL_GET_AVAILABLE_SLOTS_INFO, CAL_POST_NEW_BOOKING_REQUEST`
6. `heygen avatars voices list` → `HEYGEN_V2_VOICES`
7. `heygen list avatars` → `HEYGEN_LIST_ALL_AVATAR_GROUPS, HEYGEN_LIST_GROUP_AVATARS`
8. `cal com list bookings` → `CAL_FETCH_ALL_BOOKINGS, CAL_LIST_EVENT_TYPES`
9. `reschedule booking by uid cal` → `CAL_RESCHEDULE_BOOKING_BY_UID`

### Task 18
*Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.*

1. `Search job boards for remote hybrid contract data engineering jobs` → `COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
2. `Compile curated digest of job listings` → `DICE_MCP_SEARCH_JOBS, ZIPRECRUITER_MCP_SEARCH_JOBS`
3. `Send email with job digest` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
4. `Search jobs on job boards` → `COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_FETCH_URL_CONTENT`

### Task 19
*Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.*

1. `Search for Java backend and Spring Boot jobs in job search application` → `COMPOSIO_SEARCH_WEB, COMPOSIO_SEARCH_FETCH_URL_CONTENT`
2. `Search for or create resume documents in Google Drive or document storage` → `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`
3. `Send email through Gmail application` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 20
*Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records...*

1. `Search and update customer records in Zoho CRM` → `ZOHO_SEARCH_ZOHO_RECORDS, ZOHO_GET_ZOHO_RECORDS`
2. `Search and read files in Google Drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
3. `Read and update spreadsheet data in Google Sheets` → `GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_UPDATE_VALUES_BATCH`
4. `Read and update documents in Google Docs` → `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
5. `Access invoices and billing records in QuickBooks` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_LIST_INVOICES, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`

