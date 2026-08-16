# Agent-Loop Query Benchmark

## Method
Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: `search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told nothing about which tools exist -- it has to discover them by searching, then react to what comes back. Every query it issues is recorded. Query count is emergent: no cap, no formula, the agent stops searching when it stops needing tools.

Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs to a toolkit with a live connected account. Mocks are generated from the tool's declared `output_parameters`, so they are structurally indistinguishable from a real response. With no accounts connected, every call is mocked and no external API is touched.

## Summary
- **Tasks attempted:** 100
- **Tasks completed without error:** 100
- **Total queries captured:** 384
- **Queries per task:** mean 3.8, median 4, min 1, max 8
- **Tool executions:** 348 (90 real, 0 real-failed, 187 mocked)

### Task completion

- **Reported:** 97/100 tasks called `finish_task` (3 truncated before reporting)
- **Completed:** 54/97 of those reported

| Blocked by | Tasks | Counts against search? |
|---|---:|---|
| `data_absent` | 37 | no - the account lacks the record, not a search problem |
| `no_suitable_tool` | 4 | **yes** - retrieval failure |
| `tool_failed` | 2 | no - execution error, not retrieval |

Completion is the agent's own report. It is a weak signal on its own -- an agent can believe it finished when it did not -- so read it next to the recall numbers rather than instead of them.

## Per-task breakdown

| Task | Queries | Executions | Steps | Completed | Blocked by | Stop reason |
|---|---:|---:|---:|---|---|---|
| 1 | 4 | 7 | 12 | yes | not_blocked | agent finished |
| 2 | 2 | 10 | 13 | no | data_absent | agent finished |
| 3 | 3 | 1 | 5 | no | tool_failed | agent finished |
| 4 | 6 | 0 | 7 | no | data_absent | agent finished |
| 5 | 4 | 3 | 8 | no | data_absent | agent finished |
| 6 | 4 | 0 | 5 | yes | not_blocked | agent finished |
| 7 | 4 | 7 | 12 | yes | not_blocked | agent finished |
| 8 | 3 | 6 | 10 | yes | not_blocked | agent finished |
| 9 | 3 | 5 | 9 | yes | not_blocked | agent finished |
| 10 | 4 | 4 | 9 | no | data_absent | agent finished |
| 11 | 5 | 0 | 6 | yes | not_blocked | agent finished |
| 12 | 6 | 0 | 7 | yes | not_blocked | agent finished |
| 13 | 3 | 4 | 8 | yes | not_blocked | agent finished |
| 14 | 2 | 1 | 4 | yes | not_blocked | agent finished |
| 15 | 5 | 7 | 13 | yes | not_blocked | agent finished |
| 16 | 3 | 1 | 5 | yes | not_blocked | agent finished |
| 17 | 4 | 6 | 11 | yes | data_absent | agent finished |
| 18 | 2 | 6 | 9 | no | tool_failed | agent finished |
| 19 | 3 | 3 | 7 | yes | not_blocked | agent finished |
| 20 | 5 | 3 | 9 | no | data_absent | agent finished |
| 21 | 2 | 3 | 6 | no | data_absent | agent finished |
| 22 | 3 | 0 | 4 | yes | not_blocked | agent finished |
| 23 | 3 | 1 | 5 | yes | not_blocked | agent finished |
| 24 | 2 | 2 | 5 | yes | not_blocked | agent finished |
| 25 | 2 | 2 | 5 | yes | not_blocked | agent finished |
| 26 | 4 | 1 | 6 | yes | data_absent | agent finished |
| 27 | 3 | 5 | 9 | yes | not_blocked | agent finished |
| 28 | 5 | 6 | 12 | yes | not_blocked | agent finished |
| 29 | 7 | 0 | 8 | yes | not_blocked | agent finished |
| 30 | 3 | 2 | 6 | yes | not_blocked | agent finished |
| 31 | 5 | 0 | 6 | yes | not_blocked | agent finished |
| 32 | 2 | 1 | 4 | yes | not_blocked | agent finished |
| 33 | 3 | 3 | 7 | no | data_absent | agent finished |
| 34 | 5 | 5 | 11 | yes | not_blocked | agent finished |
| 35 | 3 | 1 | 5 | yes | not_blocked | agent finished |
| 36 | 5 | 1 | 7 | yes | not_blocked | agent finished |
| 37 | 6 | 0 | 7 | yes | not_blocked | agent finished |
| 38 | 4 | 7 | 12 | yes | data_absent | agent finished |
| 39 | 1 | 1 | 3 | no | data_absent | agent finished |
| 40 | 2 | 22 | 24 | - | - | step ceiling reached |
| 41 | 6 | 0 | 7 | no | data_absent | agent finished |
| 42 | 5 | 19 | 24 | - | - | step ceiling reached |
| 43 | 3 | 1 | 5 | no | data_absent | agent finished |
| 44 | 3 | 3 | 7 | no | data_absent | agent finished |
| 45 | 6 | 6 | 13 | yes | not_blocked | agent finished |
| 46 | 3 | 0 | 4 | yes | no_suitable_tool | agent finished |
| 47 | 3 | 0 | 4 | no | no_suitable_tool | agent finished |
| 48 | 5 | 3 | 9 | yes | not_blocked | agent finished |
| 49 | 7 | 1 | 5 | yes | data_absent | agent finished |
| 50 | 4 | 6 | 11 | yes | not_blocked | agent finished |
| 51 | 5 | 0 | 6 | no | data_absent | agent finished |
| 52 | 3 | 6 | 10 | yes | not_blocked | agent finished |
| 53 | 3 | 1 | 5 | no | data_absent | agent finished |
| 54 | 4 | 4 | 9 | yes | data_absent | agent finished |
| 55 | 1 | 0 | 2 | no | data_absent | agent finished |
| 56 | 6 | 8 | 15 | yes | not_blocked | agent finished |
| 57 | 3 | 6 | 10 | no | data_absent | agent finished |
| 58 | 2 | 2 | 5 | no | data_absent | agent finished |
| 59 | 4 | 2 | 7 | yes | data_absent | agent finished |
| 60 | 7 | 2 | 10 | no | data_absent | agent finished |
| 61 | 5 | 3 | 9 | yes | data_absent | agent finished |
| 62 | 2 | 1 | 4 | no | data_absent | agent finished |
| 63 | 7 | 7 | 15 | yes | data_absent | agent finished |
| 64 | 7 | 7 | 15 | no | data_absent | agent finished |
| 65 | 2 | 2 | 5 | no | data_absent | agent finished |
| 66 | 3 | 0 | 4 | no | data_absent | agent finished |
| 67 | 4 | 0 | 5 | yes | not_blocked | agent finished |
| 68 | 2 | 2 | 5 | no | data_absent | agent finished |
| 69 | 2 | 1 | 4 | no | data_absent | agent finished |
| 70 | 6 | 0 | 7 | no | data_absent | agent finished |
| 71 | 4 | 2 | 7 | no | data_absent | agent finished |
| 72 | 3 | 7 | 11 | yes | not_blocked | agent finished |
| 73 | 5 | 0 | 6 | no | data_absent | agent finished |
| 74 | 3 | 4 | 8 | yes | not_blocked | agent finished |
| 75 | 1 | 2 | 4 | yes | not_blocked | agent finished |
| 76 | 6 | 6 | 13 | no | data_absent | agent finished |
| 77 | 4 | 4 | 9 | no | no_suitable_tool | agent finished |
| 78 | 8 | 4 | 13 | yes | not_blocked | agent finished |
| 79 | 3 | 7 | 11 | yes | not_blocked | agent finished |
| 80 | 4 | 6 | 11 | no | data_absent | agent finished |
| 81 | 3 | 0 | 4 | yes | not_blocked | agent finished |
| 82 | 4 | 3 | 8 | yes | data_absent | agent finished |
| 83 | 3 | 5 | 9 | no | data_absent | agent finished |
| 84 | 6 | 9 | 16 | yes | not_blocked | agent finished |
| 85 | 4 | 1 | 6 | no | data_absent | agent finished |
| 86 | 3 | 8 | 12 | no | data_absent | agent finished |
| 87 | 5 | 4 | 10 | yes | not_blocked | agent finished |
| 88 | 4 | 2 | 7 | yes | data_absent | agent finished |
| 89 | 4 | 3 | 8 | yes | not_blocked | agent finished |
| 90 | 2 | 1 | 4 | no | data_absent | agent finished |
| 91 | 3 | 0 | 4 | no | data_absent | agent finished |
| 92 | 4 | 5 | 10 | no | no_suitable_tool | agent finished |
| 93 | 3 | 21 | 24 | - | - | step ceiling reached |
| 94 | 6 | 1 | 8 | yes | not_blocked | agent finished |
| 95 | 4 | 4 | 9 | no | data_absent | agent finished |
| 96 | 2 | 0 | 3 | no | data_absent | agent finished |
| 97 | 6 | 0 | 7 | no | no_suitable_tool | agent finished |
| 98 | 3 | 3 | 7 | no | data_absent | agent finished |
| 99 | 4 | 3 | 8 | no | data_absent | agent finished |
| 100 | 2 | 3 | 6 | yes | not_blocked | agent finished |

## Queries the agent actually issued

### Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th...*

1. `Create or check payment link in HubSpot` → `STRIPE_CREATE_PAYMENT_LINK`
2. `Create marketing email or automated email in HubSpot` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
3. `Create workflow in HubSpot` → `HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT`
4. `Create custom object schema in HubSpot` → `HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS, HUBSPOT_CREATE_BATCH_OF_PROPERTIES`

### Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

1. `retrieve upcoming google calendar meeting events` → `GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `notion create update database page content structured dataset` → `NOTION_INSERT_ROW_DATABASE, NOTION_ADD_MULTIPLE_PAGE_CONTENT, NOTION_SEARCH_NOTION_PAGE`

### Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

1. `Search or list files in OneDrive to find a spreadsheet` → `ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN`
2. `Download file content from OneDrive item ID` → `ONE_DRIVE_GET_ITEM, ONE_DRIVE_DOWNLOAD_FILE`
3. `Upload or update file in OneDrive` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

1. `trello get cards in list or board` → `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_LISTS_CARDS_BY_ID_LIST`
2. `linkedin post carousel image document` → `LINKEDIN_CREATE_LINKED_IN_POST`
3. `linkedin add comment post` → `LINKEDIN_CREATE_COMMENT_ON_POST`
4. `trello update card comment list` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
5. `trello update card list position` → `TRELLO_UPDATE_CARDS_POS_BY_ID_CARD`
6. `trello create list board` → `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_ADD_LISTS`

### Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a...*

1. `Search Gmail messages or threads for partner outreach` → `GMAIL_LIST_THREADS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID`
2. `Create draft email in Gmail` → `GMAIL_CREATE_EMAIL_DRAFT`
3. `ClickUp create task or update task` → `CLICKUP_CREATE_TASK`
4. `Notion create database page or update database page` → `NOTION_QUERY_DATABASE, NOTION_INSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE, NOTION_CREATE_NOTION_PAGE`

### Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

1. `Manage Salesforce leads` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS`
2. `Manage Salesforce contacts` → `SALESFORCE_SEARCH_CONTACTS, SALESFORCE_LIST_CONTACTS, SALESFORCE_GET_SOBJECT_RELATIONSHIP, SALESFORCE_DELETE_CONTACT`
3. `Manage Salesforce campaign membership and attendance statuses` → `SALESFORCE_SEARCH_CONTACTS, SALESFORCE_SEARCH_CAMPAIGNS, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN`
4. `Manage campaign-based static list and MQL lead activity reporting` → `SALESFORCE_LIST_LEADS`

### Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

1. `Aggregate personal productivity signals across email calendar GitHub LinkedIn SMS` → `LINKEDIN_GET_MY_INFO, GMAIL_GET_PROFILE, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`
2. `Send and receive SMS messages` → `CLICKSEND_CREATE_SMS_SEND`
3. `Manage Google Calendar access and events` → `GOOGLECALENDAR_EVENTS_LIST, GOOGLECALENDAR_CREATE_EVENT, GOOGLECALENDAR_PATCH_EVENT`
4. `Fetch GitHub repositories and user activity` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`

### Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

1. `search public video transcripts` → `YOUTUBE_SEARCH_YOU_TUBE, COMPOSIO_SEARCH_WEB`
2. `get video transcript` → `SUPADATA_GET_TRANSCRIPT`
3. `append document google docs` → `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`

### Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

1. `Create multimedia travel marketing assets from scripts and stock media` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE`
2. `Send email and presentation content` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
3. `Google Slides presentation create` → `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN, GOOGLESLIDES_PRESENTATIONS_CREATE, GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE, GOOGLEDRIVE_CREATE_PERMISSION`

### Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec...*

1. `QuickBooks query bank account ledger transactions` → `QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`
2. `QuickBooks delete void purchase invoice payment transaction` → `QUICKBOOKS_READ_INVOICE`
3. `QuickBooks create purchase journal entry deposit` → `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
4. `QuickBooks create payment customer payment` → `QUICKBOOKS_CREATE_PAYMENT`

### Task 11
*Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure...*

1. `Search OneDrive files or documents` → `ONE_DRIVE_SEARCH_DRIVE_ITEMS, ONE_DRIVE_SEARCH_ITEMS`
2. `Create or update OneDrive files or Word documents` → `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE, ONE_DRIVE_GET_ITEM`
3. `Send Discord channel message` → `DISCORDBOT_CREATE_MESSAGE`
4. `Read file or check queue status` → `CLORO_GET_ASYNC_QUEUE_STATUS, FAL_AI_QUEUE_GET_STATUS, FIRECRAWL_QUEUE_GET, VERIFIEDEMAIL_CHECK_FILE_STATUS`
5. `Configure Gmail labels and routing` → `GMAIL_LIST_LABELS, GMAIL_CREATE_LABEL`

### Task 12
*Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.*

1. `Retrieve comments from a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD`
2. `Update a Trello card` → `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION`
3. `Update a Trello card details` → `TRELLO_UPDATE_CARDS_BY_ID_CARD`
4. `Send an email` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
5. `Send a chat message` → `CLICKUP_CREATE_CHAT_MESSAGE`
6. `Send webhook or trigger automation` → `GOOGLECALENDAR_EVENTS_WATCH`

### Task 13
*Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.*

1. `Audit website search and traffic performance in analytics` → `GOOGLESUPER_RUN_REPORT, GOOGLESUPER_BATCH_RUN_REPORTS`
2. `Search for contacts or create email lists in CRM or email marketing tool` → `GMAIL_GET_CONTACTS, GMAIL_SEARCH_PEOPLE`
3. `Send email message` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 14
*Find software engineering job listings matching role, location, remote-work, and salary criteria, compile the results, and send or provide them to someone.*

1. `search software engineering job listings by criteria` → `COMPOSIO_SEARCH_WEB`
2. `send email or message` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 15
*Process pending invoice emails, persist invoice attachments to cloud storage, update spreadsheet ledgers, verify calculated totals, and label processed messages.*

1. `Search Gmail messages with pending invoice query` → `GMAIL_FETCH_EMAILS`
2. `Upload file to cloud storage or Google Drive` → `GOOGLEDRIVE_UPLOAD_FILE, ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
3. `Append row or update Google Sheets spreadsheet` → `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
4. `Find spreadsheet file in Google Drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_CREATE_FOLDER, GOOGLEDRIVE_UPLOAD_FILE, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_MOVE_FILE`
5. `Add label to Gmail messages` → `GMAIL_ADD_LABEL_TO_EMAIL, GMAIL_BATCH_MODIFY_MESSAGES`

### Task 16
*Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host...*

1. `Search website analytics and search performance report` → `GOOGLESUPER_RUN_REPORT, GOOGLESUPER_BATCH_RUN_REPORTS`
2. `Git repository file inspect and commit or pull request` → `GITHUB_GET_A_REPOSITORY, GITHUB_GET_A_TREE, GITHUB_GET_REPOSITORY_CONTENT, GITHUB_LIST_COMMITS, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`
3. `Vercel Netlify Heroku deployment status inspect` → `VERCEL_GET_DEPLOYMENTS, VERCEL_GET_DEPLOYMENT, VERCEL_GET_DEPLOYMENT_LOGS2`

### Task 17
*Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.*

1. `Create an AI avatar promo video in HeyGen` → `HEYGEN_V2_VIDEO_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`
2. `Publish video to social media platforms` → `UPLOAD_POST_PUBLISH_POST, WOOP_SOCIAL_PUBLISH_POST_NOW`
3. `Send an email support message` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
4. `Read and update bookings or calendar events` → `GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_PATCH_EVENT, GOOGLECALENDAR_DELETE_EVENT, GOOGLECALENDAR_CREATE_EVENT`

### Task 18
*Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.*

1. `Search job listings or job boards for remote hybrid contract data engineering jobs` → `COMPOSIO_SEARCH_WEB`
2. `Send an email` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 19
*Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.*

1. `search for java backend spring boot jobs` → `SERPAPI_GOOGLE_JOBS_SEARCH`
2. `search or retrieve resume documents in drive or storage` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_DOWNLOAD_FILE`
3. `send email via gmail` → `GMAIL_SEND_EMAIL`

### Task 20
*Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records...*

1. `search or get contacts in Zoho CRM` → `ZOHO_SEARCH_ZOHO_RECORDS, ZOHO_CREATE_ZOHO_RECORD`
2. `read rows or write data in Google Sheets` → `GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_UPDATE_VALUES_BATCH`
3. `read or update Google Docs content` → `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
4. `search or list files in Google Drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
5. `QuickBooks invoices customers billing` → `QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_LIST_INVOICES, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`

### Task 21
*Read reference documents and a spreadsheet, discover fiscal-period logic from available workspace sources, update spreadsheet formulas, and create a summary worksheet.*

1. `read reference documents and spreadsheet in workspace` → `NOTION_SEARCH_NOTION_PAGE, NOTION_GET_PAGE_MARKDOWN, GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_DOWNLOAD_FILE`
2. `update spreadsheet formulas and create worksheet` → `GOOGLESHEETS_CREATE_GOOGLE_SHEET1, GOOGLESHEETS_UPDATE_VALUES_BATCH, GOOGLESHEETS_FORMAT_CELL`

### Task 22
*The user was managing unread email triage and urgent alerts, looking up CRM-style trial records, inspecting and modifying source code in GitHub, opening or merging branches, and checking CI workflow f...*

1. `Search unread emails and alerts in email application` → `GMAIL_FETCH_EMAILS`
2. `Search CRM trial records or contacts` → `SALESFORCE_LIST_CONTACTS, SALESFORCE_RUN_SOQL_QUERY`
3. `Search GitHub repositories issues pull requests workflows actions code` → `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`

### Task 23
*Analyze and triage Zendesk support tickets at scale: search ticket queues, enrich tickets with requester/order context, add private AI triage notes and tags, verify queues are drained, and aggregate p...*

1. `Search Zendesk support tickets` → `ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_SEARCH_ZENDESK`
2. `add private comment and tags to a Zendesk ticket` → `ZENDESK_UPDATE_ZENDESK_TICKET`
3. `get user details or orders context` → `GMAIL_GET_PROFILE, TWITTER_USER_LOOKUP_BY_USERNAMES, TWITTER_USER_LOOKUP_ME`

### Task 24
*Build a recurring job-search digest by finding relevant LinkedIn job listings and sending the result or status update via Gmail.*

1. `Search LinkedIn job listings` → `COMPOSIO_SEARCH_WEB`
2. `send email gmail` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`

### Task 25
*Find relevant job listings from public web/job sources, tailor them to a software profile, and email the curated list through Gmail.*

1. `Search job listings on public web sources` → `COMPOSIO_SEARCH_WEB`
2. `Send email using Gmail` → `GMAIL_SEND_EMAIL`

### Task 26
*Organize Google Drive image and PDF files by finding candidates, inspecting their contents, renaming files, adding descriptions, moving exact duplicates to a review folder, and verifying metadata chan...*

1. `find files in Google Drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
2. `inspect file content or read text from PDF image Google Drive` → `FIRECRAWL_EXTRACT, OCR_WEB_SERVICE_RECOGNIZE, GOOGLEDRIVE_DOWNLOAD_FILE`
3. `update file metadata rename description Google Drive` → `GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_UPDATE_FILE_PUT`
4. `move file or update parents Google Drive` → `GOOGLEDRIVE_MOVE_FILE`

### Task 27
*Verify Google Drive access, inspect folders, copy a nested folder/file structure from one Drive account or folder area to another, and share the destination with collaborators.*

1. `list files or folders in Google Drive` → `GOOGLEDRIVE_FIND_FILE`
2. `copy file or folder in Google Drive` → `GOOGLEDRIVE_COPY_FILE_ADVANCED, GOOGLEDRIVE_CREATE_SHORTCUT_TO_FILE`
3. `share file or folder permissions Google Drive` → `GOOGLEDRIVE_CREATE_PERMISSION, GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`

### Task 28
*Analyze recent Instagram Reel performance, generate a new short-form branded video with AI video and voice tools, publish it as an Instagram Reel, verify the post, and attempt to archive the final ass...*

1. `Get recent Instagram Reel performance metrics` → `INSTAGRAM_GET_IG_USER_MEDIA, INSTAGRAM_GET_IG_MEDIA_INSIGHTS`
2. `Generate AI video or text to speech voice` → `GEMINI_GENERATE_VIDEOS`
3. `publish Instagram Reel post` → `INSTAGRAM_POST_IG_USER_MEDIA, INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
4. `Verify Instagram post status or media details` → `INSTAGRAM_GET_POST_STATUS`
5. `Upload or store asset in GitHub or repository` → `GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER, GITHUB_COMMIT_MULTIPLE_FILES`

### Task 29
*Automate a complex growth and content operations workflow: publish scheduled social content across multiple platforms, notify collaborators, update tracking spreadsheets, log lead and outreach activit...*

1. `publish social media content to multiple platforms` → `FACEBOOK_CREATE_PHOTO_POST, INSTAGRAM_POST_IG_USER_MEDIA, INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH, LINKEDIN_CREATE_LINKED_IN_POST`
2. `send notification message to collaborators or channel` → `SLACK_SEND_MESSAGE, GMAIL_SEND_EMAIL`
3. `update spreadsheet rows or data` → `GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_UPSERT_ROWS, GMAIL_FETCH_EMAILS`
4. `log lead and outreach activity in CRM or database` → `SALESFORCE_CREATE_TASK`
5. `send message via Telegram bot` → `TELEGRAM_SEND_MESSAGE`
6. `inspect recent meeting notes from Fathom and Google Drive` → `FATHOM_LIST_MEETINGS, FATHOM_GET_RECORDING_SUMMARY, FATHOM_GET_RECORDING_TRANSCRIPT`
7. `search google drive files meeting notes` → `GOOGLEDRIVE_FIND_FILE`

### Task 30
*Generate recurring daily activity summaries by collecting recent email activity, social page activity, and Fireflies meeting transcripts for a local-day reporting window.*

1. `Fetch recent emails or messages for daily activity summary` → `GMAIL_FETCH_EMAILS`
2. `Fetch social media page activity or posts` → `LINKEDIN_GET_POST_CONTENT, LINKEDIN_LIST_REACTIONS`
3. `Fetch Fireflies meeting transcripts` → `FIREFLIES_GET_TRANSCRIPTS`

### Task 31
*Monitor and inspect Outlook email messages, summarize or verify their contents, sometimes process attachments or market data, create reminders/tasks, and attempt to send concise notifications through ...*

1. `Search Outlook email messages` → `OUTLOOK_SEARCH_MESSAGES`
2. `Download or get attachments from Outlook email message` → `OUTLOOK_LIST_OUTLOOK_ATTACHMENTS, OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT`
3. `Create reminder or task` → `NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_INSERT_ROW_DATABASE`
4. `Send WhatsApp message` → `WHATSAPP_SEND_MESSAGE`
5. `Send Notis message or notification` → `SLACK_SEND_MESSAGE, GMAIL_SEND_EMAIL`

### Task 32
*The session covered multiple unrelated workflows: public web research, financial-product research, real-estate listing checks, browser QA for a web prototype, attempted Discord role updates, GitHub re...*

1. `search session notes or recent activity logs` → `SALESFORCE_SEARCH_ACCOUNTS, SALESFORCE_LIST_NOTES`
2. `search files or documents in storage or drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`

### Task 33
*Analyze WhatsApp-style broadcast campaigns in Kommo CRM, including detected campaign sends, audience reach, replies, conversions, templates, segments, and related agent activity.*

1. `whatsapp broadcast campaigns kommo crm audience reach replies conversions templates segments agent activity` → `KOMMO_LIST_TEMPLATES, ACTIVE_CAMPAIGN_GET_SMS_BROADCAST_METRICS_SNAPSHOT`
2. `broadcast campaigns kommo crm` → `KIT_CREATE_BROADCAST`
3. `agent activity kommo crm` → `KOMMO_LIST_EVENTS`

### Task 34
*Audit and maintain Pipedrive CRM data: find deals and contacts, inspect activities/notes/pipeline stages, analyze sales-development activity hygiene, move long-horizon deals to a long-term review stag...*

1. `Find deals and contacts in Pipedrive CRM` → `PIPEDRIVE_SEARCH_PERSONS, PIPEDRIVE_LIST_PERSON_DEALS, PIPEDRIVE_GET_ALL_DEALS`
2. `Inspect activities notes pipeline stages in Pipedrive CRM` → `PIPEDRIVE_GET_ALL_ACTIVITIES_ASSIGNED_TO_A_PARTICULAR_USER`
3. `Get pipeline stages and notes in Pipedrive CRM` → `PIPEDRIVE_GET_ALL_STAGES`
4. `Move deals to a stage and create activities in Pipedrive CRM` → `PIPEDRIVE_UPDATE_DEAL`
5. `Create activity Pipedrive CRM` → `PIPEDRIVE_ADD_AN_ACTIVITY`

### Task 35
*Fetch paginated Instagram media comments, identify comments needing replies, post reply ratings in bulk, and later clean up duplicate or mistaken replies.*

1. `fetch paginated instagram media comments` → `INSTAGRAM_GET_IG_MEDIA_COMMENTS`
2. `post reply ratings in bulk or create comment replies in bulk instagram` → `INSTAGRAM_POST_IG_COMMENT_REPLIES`
3. `delete or clean up Instagram comment reply` → `INSTAGRAM_GET_IG_USER_MEDIA, INSTAGRAM_GET_IG_MEDIA_COMMENTS, INSTAGRAM_DELETE_COMMENT`

### Task 36
*Manage a GitHub repository workflow: authenticate, inspect organization/repository access, create and label pull requests, inspect CI and workflow logs, merge approved changes, dispatch build/deploy/d...*

1. `GitHub authenticate organization repository access pull request workflow CI logs merge dispatch deploy troubleshoot` → `LINEAR_GET_CURRENT_USER, GITHUB_GET_THE_AUTHENTICATED_USER, GMAIL_GET_PROFILE, SLACK_TEST_AUTH, GOOGLESHEETS_SEARCH_SPREADSHEETS`
2. `GitHub list repositories organization access inspect` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER, GITHUB_GET_A_TREE, GITHUB_GET_REPOSITORY_CONTENT`
3. `GitHub create pull request label inspect workflow run logs merge dispatch troubleshooting` → `GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
4. `GitHub add labels pull request workflow logs dispatch` → `GITHUB_ADD_LABELS_TO_AN_ISSUE`
5. `GitHub workflow runs log dispatch` → `GITHUB_LIST_REPOSITORY_WORKFLOWS, GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT, GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY, GITHUB_GET_A_WORKFLOW_RUN`

### Task 37
*Manage and triage Outlook email at scale: query inbox messages, inspect bodies and attachments, reply or forward selected messages, create and organize folders, move or delete messages, download attac...*

1. `Search or list emails in Outlook inbox` → `GMAIL_FETCH_EMAILS, OUTLOOK_SEARCH_MESSAGES`
2. `Get Outlook message body and list or download attachments` → `OUTLOOK_GET_MESSAGE, OUTLOOK_LIST_OUTLOOK_ATTACHMENTS, OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT`
3. `Reply or forward Outlook email message` → `OUTLOOK_CREATE_DRAFT_REPLY, OUTLOOK_SEND_DRAFT`
4. `Create mail folder in Outlook` → `OUTLOOK_CREATE_MAIL_FOLDER`
5. `Move or delete Outlook message` → `OUTLOOK_BATCH_UPDATE_MESSAGES, OUTLOOK_BATCH_MOVE_MESSAGES`
6. `Create calendar event or invite in Outlook` → `OUTLOOK_CALENDAR_CREATE_EVENT`

### Task 38
*Analyze Salesforce opportunity and pipeline data, read and update a Google Sheets tracking spreadsheet, search a Salesforce account, and attempt to send a Slack direct message with CRM-derived context...*

1. `Analyze Salesforce opportunity and pipeline data` → `SALESFORCE_RUN_SOQL_QUERY`
2. `read and update Google Sheets spreadsheet` → `GOOGLESHEETS_CREATE_GOOGLE_SHEET1, GOOGLESHEETS_VALUES_GET, GOOGLESHEETS_VALUES_UPDATE`
3. `search a Salesforce account` → `SALESFORCE_SEARCH_ACCOUNTS, SALESFORCE_RUN_SOQL_QUERY`
4. `send Slack direct message` → `SLACK_SEND_MESSAGE, SLACKBOT_SEND_MESSAGE`

### Task 39
*Audit and reconcile CRM lead activity into a spreadsheet-based reporting workbook, including lead extraction, source classification, social-seller separation, outcome tracking, summary updates, and fi...*

1. `extract CRM leads to spreadsheet reporting workbook` → `GOOGLESHEETS_SEARCH_SPREADSHEETS, GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_VALUES_GET, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS, GOOGLESHEETS_UPSERT_ROWS`

### Task 40
*Create, iteratively refine, verify, and operationalize a Notion specification page, then create related Linear implementation issues and relationships.*

1. `Create a Notion page` → `NOTION_CREATE_NOTION_PAGE`
2. `Create a Linear issue` → `LINEAR_CREATE_LINEAR_ISSUE`

### Task 41
*Implement and release a protected budget dashboard feature by reading Google Sheets and Google Docs data, retrieving deployment secrets from Vercel, committing and merging code changes, verifying depl...*

1. `read rows or spreadsheet data from Google Sheets` → `GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_VALUES_GET`
2. `get content or read document from Google Docs` → `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT, GOOGLEDOCS_SEARCH_DOCUMENTS`
3. `get deployment secrets or environment variables from Vercel` → `VERCEL_FILTER_PROJECT_ENVS`
4. `commit changes and merge pull request in GitHub` → `GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
5. `list or get deployments on Vercel` → `VERCEL_GET_PROJECTS, VERCEL_GET_DEPLOYMENTS`
6. `update or edit issue in Jira` → `JIRA_GET_ISSUE_TYPES, JIRA_EDIT_ISSUE, JIRA_GET_ISSUE, JIRA_GET_ISSUE_EDIT_METADATA`

### Task 42
*Manage calendar accounts and events across multiple calendar accounts, send a Slack direct message with meeting details, share calendars between accounts, and create/update calendar events for persona...*

1. `List calendar accounts or calendars across multiple accounts` → `GOOGLECALENDAR_LIST_CALENDARS`
2. `Send a Slack direct message` → `SLACK_SEND_MESSAGE, SLACKBOT_SEND_MESSAGE`
3. `Add rule to calendar access control list ACL sharing calendar` → `GOOGLECALENDAR_ACL_INSERT, GOOGLECALENDAR_ACL_UPDATE, GOOGLECALENDAR_ACL_LIST`
4. `Create calendar event google calendar` → `GOOGLECALENDAR_CREATE_EVENT`
5. `Update calendar event google calendar` → `GOOGLECALENDAR_PATCH_EVENT`

### Task 43
*Read an existing Google spreadsheet, preserve formulas and current values, add and populate new tabs with formulas and supporting details, verify recalculation, and organize related Google Drive docum...*

1. `Read an existing Google spreadsheet and get values and formulas` → `GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_BATCH_GET`
2. `Add and populate new tabs with formulas in Google spreadsheet` → `GOOGLESHEETS_ADD_SHEET, GOOGLESHEETS_UPDATE_VALUES_BATCH`
3. `Organize Google Drive documents files folders` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_CREATE_FOLDER, GOOGLEDRIVE_UPLOAD_FILE, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_MOVE_FILE`

### Task 44
*Browse a Bitbucket repository directory tree and retrieve selected repository file contents.*

1. `Browse a Bitbucket repository directory tree` → `BITBUCKET_LIST_REPOSITORY_PATHS, BITBUCKET_GET_REPOSITORIES_SRC`
2. `Retrieve file contents from Bitbucket repository` → `BITBUCKET_GET_FILE_FROM_REPOSITORY, BITBUCKET_BROWSE_REPOSITORY_PATH`
3. `List repositories in a workspace` → `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE`

### Task 45
*Create and publish a HubSpot quote for a CRM contact by first finding the contact, creating a deal, creating line items and a quote, applying quote terms and template settings, publishing the quote, a...*

1. `Search for a contact in HubSpot CRM` → `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA`
2. `Create a deal in HubSpot CRM` → `HUBSPOT_CREATE_CONTACTS, HUBSPOT_CREATE_DEALS, HUBSPOT_SEARCH_DEALS`
3. `Create a quote or line items in HubSpot` → `HUBSPOT_CREATE_QUOTE_OBJECT`
4. `Create line items in HubSpot CRM` → `HUBSPOT_CREATE_LINE_ITEMS, HUBSPOT_CREATE_LINE_ITEM`
5. `Publish quote or update quote in HubSpot` → `HUBSPOT_CREATE_QUOTE_OBJECT, HUBSPOT_CREATE_LINE_ITEMS`
6. `Inspect quote properties or template settings in HubSpot` → `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE`

### Task 46
*Create, update, query, and verify Notion database rows and page content for generic deal-room style pages, including owner lookup, bulk content replacement, child-page preservation, and database filte...*

1. `Notion database search and update rows` → `NOTION_FETCH_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_INSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE`
2. `fetch block contents page content Notion` → `NOTION_FETCH_ALL_BLOCK_CONTENTS`
3. `delete block contents or clear page content Notion` → `NOTION_REPLACE_PAGE_CONTENT`

### Task 47
*Duplicate an existing Meta Ads campaign using the Meta Marketing API copies capability.*

1. `Duplicate a Meta Ads campaign using Meta Marketing API` → `METAADS_CREATE_CAMPAIGN`
2. `copy campaign duplicate campaign Meta Marketing API` → `METAADS_LIST_ADS, METAADS_GET_AD_CREATIVE`
3. `copy campaign Meta Ads API` → `METAADS_CREATE_CAMPAIGN`

### Task 48
*Generate and post-process a long text-to-speech audio asset, upload it to cloud storage, research YouTube content opportunities and comments, then update YouTube channel branding metadata.*

1. `generate text to speech audio asset in text-to-speech application` → `ELEVENLABS_TEXT_TO_SPEECH, ELEVENLABS_GET_VOICES`
2. `post-process audio or edit audio in audio processing application` → `ERANOL_ENHANCE_AUDIO, ELEVENLABS_STREAM_AUDIO_ISOLATION`
3. `upload file to cloud storage or s3 or google drive` → `GOOGLEDRIVE_UPLOAD_FILE, ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`
4. `search youtube videos or comments or content opportunities in youtube application` → `YOUTUBE_LIST_COMMENT_THREADS2`
5. `update youtube channel branding metadata or channel details` → `YOUTUBE_UPDATE_CHANNEL`

### Task 49
*Organize recently uploaded receipt and invoice files in Google Drive: find recent files, download/convert images to PDFs, upload or update Drive files, create destination folders, rename and move docu...*

1. `search list recent files in Google Drive` → `GOOGLEDRIVE_FIND_FILE`
2. `convert image to PDF or download file in Google Drive` → `TEXT_TO_PDF_START_ASYNC_CONVERSION, TEXT_TO_PDF_UPLOAD_FILE, TEXT_TO_PDF_CONVERT_TEXT_TO_PDF`
3. `upload update file in Google Drive` → `GOOGLEDRIVE_UPLOAD_UPDATE_FILE`
4. `create folder in Google Drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_CREATE_FOLDER`
5. `rename move file in Google Drive` → `GOOGLEDRIVE_UPDATE_FILE_PUT`
6. `trash delete file in Google Drive` → `GOOGLEDRIVE_TRASH_FILE, GOOGLEDRIVE_GOOGLE_DRIVE_DELETE_FOLDER_OR_FILE_ACTION`
7. `update spreadsheet cells Google Sheets` → `GOOGLESHEETS_VALUES_UPDATE, GOOGLESHEETS_FORMAT_CELL`

### Task 50
*Verify the correct Slack workspace, identify members of a Slack channel, send an approved direct message to selected members, and remediate accidental sends in the wrong workspace.*

1. `verify slack workspace` → `SLACK_TEST_AUTH, NOTION_GET_ABOUT_USER`
2. `list members of a slack channel` → `SLACK_RETRIEVE_CONVERSATION_MEMBERS_LIST`
3. `send direct message to slack user` → `SLACK_SEND_MESSAGE, SLACK_OPEN_DM`
4. `delete a slack message` → `SLACK_DELETES_A_MESSAGE_FROM_A_CHAT`

### Task 51
*Fetch and annotate support-thread evidence, retrieve attachment download links, and later verify an Instagram DM tool fix using Instagram reads/sends plus Metabase, Datadog, and spreadsheet evidence.*

1. `fetch support thread messages and notes or annotations in customer support tool` → `HELPWISE_GET_CONVERSATION, ZENDESK_GET_ZENDESK_TICKET_BY_ID, FRESHDESK_LIST_ALL_TICKET_CONVERSATIONS`
2. `retrieve attachment download links from helpwise or zendesk or freshdesk conversation` → `HELPWISE_GET_ATTACHMENT, HELPWISE_GET_ATTACHMENTS, ZENDESK_DOWNLOAD_CUSTOM_OBJECT_RECORD_ATTACHMENT`
3. `verify Instagram DM tool fix using Instagram reads sends and Metabase Datadog spreadsheet evidence` → `INSTAGRAM_LIST_ALL_MESSAGES, INSTAGRAM_LIST_ALL_CONVERSATIONS, INSTAGRAM_SEND_TEXT_MESSAGE, INSTAGRAM_GET_CONVERSATION`
4. `query metabase datadog and google sheets for metrics and logs and spreadsheet evidence` → `DATADOG_SEARCH_LOGS`
5. `read and write spreadsheet data in google sheets or excel` → `GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_UPDATE_VALUES_BATCH`

### Task 52
*Migrate a user's memory data from Mem0 into Zep, inspect existing Zep context, attempt to organize migrated content by project-like scopes, and verify that the imported content is searchable.*

1. `Migrate memory data from Mem0 into Zep` → `MEM0_EXPORT_DATA_BASED_ON_FILTERS, ZEP_ADD_SESSION_MEMORY`
2. `Inspect existing Zep context or get user sessions and memory` → `ZEP_GET_THREAD_USER_CONTEXT, ZEP_GET_SESSION_MEMORY, ZEP_GET_USER_SESSIONS`
3. `Search memory or graph or documents in Zep` → `ZEP_CREATE_GRAPH, ZEP_ADD_SESSION_MEMORY, ZEP_GET_SESSION_MEMORY, ZEP_GRAPH_SEARCH`

### Task 53
*Audit a short-link inventory by finding an existing spreadsheet registry, reading help-center mapping tabs, listing existing short links, and attempting to compare them with live public website articl...*

1. `find spreadsheet registry short links` → `GOOGLESHEETS_SEARCH_SPREADSHEETS, GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_BATCH_GET`
2. `read spreadsheet values or get spreadsheet data` → `GOOGLESHEETS_BATCH_GET`
3. `make an HTTP request or fetch a web page URL` → `SCRAPE_DO_GET_PAGE`

### Task 54
*Audit advertising account health and performance, probe analytics property access, create and verify a new Google Ads search campaign with budget, targeting, ad group, keywords, and responsive search ...*

1. `google ads account health and performance audit` → `GOOGLEADS_SEARCH_STREAM_GAQL, GOOGLE_ANALYTICS_RUN_REPORT`
2. `list accessible google ads customer accounts` → `GOOGLEADS_LIST_ACCESSIBLE_CUSTOMERS`
3. `list google analytics properties` → `GOOGLE_ANALYTICS_LIST_ACCOUNT_SUMMARIES`
4. `list tasks assigned to current user in Asana` → `ASANA_GET_MULTIPLE_TASKS`

### Task 55
*Automate and refine a complex Google Sheets financial/workforce model: apply formatting, dropdown validation, filters, formulas, instructional text, payroll-style calculations, and employee allocation...*

1. `Google Sheets update spreadsheet formatting formulas data validation` → `GOOGLESHEETS_SET_DATA_VALIDATION_RULE, GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES`

### Task 56
*Clean up and enrich HubSpot CRM records by listing contacts and companies, matching contacts to companies, assigning segmentation values from job title and company industry, creating required CRM prop...*

1. `list all contacts in HubSpot CRM` → `HUBSPOT_LIST_CONTACTS`
2. `list all companies in HubSpot CRM` → `HUBSPOT_LIST_COMPANIES`
3. `create a new property in HubSpot CRM` → `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE`
4. `update batch of contacts in HubSpot CRM` → `HUBSPOT_UPDATE_CONTACTS, HUBSPOT_UPDATE_CONTACT`
5. `associate contacts and companies in HubSpot CRM` → `HUBSPOT_CREATE_OBJECT_ASSOCIATION`
6. `bulk import contacts and companies into HubSpot CRM` → `HUBSPOT_CREATE_COMPANIES, HUBSPOT_CREATE_CONTACTS, HUBSPOT_CREATE_BATCH_OF_OBJECTS`

### Task 57
*Create short dog-themed videos, analyze channel and trend performance, upload and manage YouTube Shorts, and inspect Instagram posting context.*

1. `create short video dog themed YouTube Shorts` → `GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO`
2. `YouTube channel analytics trend performance` → `YOUTUBE_GET_CHANNEL_STATISTICS`
3. `Instagram post context inspection manage posts` → `INSTAGRAM_GET_IG_USER_MEDIA`

### Task 58
*Inspect and modify a GitHub repository frontend, validate the changes if possible, then commit and push the changes directly to the default branch.*

1. `GitHub repository file inspect modify commit push` → `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`
2. `search github repositories list user repos` → `GITHUB_LIST_REPOSITORIES_FOR_A_USER, GITHUB_SEARCH_CODE, GITHUB_GET_REPOSITORY_CONTENT`

### Task 59
*Manage an Outlook mailbox by fetching recent inbox messages, classifying and moving messages or whole threads into routing folders, marking VIP emails high importance, creating staged reply drafts, an...*

1. `fetch recent inbox messages in Outlook` → `OUTLOOK_QUERY_EMAILS, OUTLOOK_LIST_MAIL_FOLDER_MESSAGES`
2. `move message to folder in Outlook` → `OUTLOOK_LIST_MAIL_FOLDERS, OUTLOOK_QUERY_EMAILS, OUTLOOK_BATCH_MOVE_MESSAGES`
3. `update email importance in Outlook` → `OUTLOOK_QUERY_EMAILS, OUTLOOK_BATCH_UPDATE_MESSAGES`
4. `create draft reply in Outlook` → `OUTLOOK_CREATE_DRAFT_REPLY`

### Task 60
*Manage lead data in Google Sheets: read existing tabs, append and correct lead rows, enrich contacts, detect duplicate email addresses, highlight duplicate rows, and attempt to prepare leads for impor...*

1. `google sheets get spreadsheet or read tabs` → `GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_GET_SPREADSHEET_INFO`
2. `google sheets search spreadsheets` → `GOOGLESHEETS_SEARCH_SPREADSHEETS`
3. `google drive find file or search files` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
4. `google sheets create spreadsheet` → `GOOGLESHEETS_UPSERT_ROWS, GOOGLESHEETS_CREATE_GOOGLE_SHEET1, NOTION_INSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE, NOTION_SEARCH_NOTION_PAGE`
5. `google sheets format conditional formatting duplicate highlight` → `GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES`
6. `instantly campaign leads add` → `INSTANTLY_LIST_LEADS, INSTANTLY_ADD_LEADS_BULK`
7. `instantly verify email or enrich contact` → `INSTANTLY_CREATE_SUPERSEARCH_ENRICHMENT, INSTANTLY_SUPERSEARCH_ENRICHMENT_RUN_POST`

### Task 61
*Manage Outlook mailbox organization by discovering folders, finding messages by sender/read status, moving messages into appropriate folders, marking selected messages as read, verifying counts, and s...*

1. `list or discover folders in Outlook mailbox` → `OUTLOOK_LIST_MAIL_FOLDERS`
2. `search or list messages in Outlook mailbox` → `OUTLOOK_QUERY_EMAILS, OUTLOOK_LIST_MAIL_FOLDER_MESSAGES`
3. `move messages to folder in Outlook` → `OUTLOOK_LIST_MAIL_FOLDERS, OUTLOOK_QUERY_EMAILS, OUTLOOK_BATCH_MOVE_MESSAGES`
4. `mark message as read in Outlook` → `OUTLOOK_BATCH_UPDATE_MESSAGES`
5. `send HTML email with CC in Outlook` → `OUTLOOK_SEND_EMAIL`

### Task 62
*Update an existing Google Docs nutrition-planning document by changing table content for two dinner entries, adding shared batch-cooking instructions, recalculating related summary content, and verify...*

1. `search or read Google Docs document` → `NOTION_SEARCH_NOTION_PAGE, GOOGLEDOCS_SEARCH_DOCUMENTS`
2. `update or edit Google Docs document` → `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN, GMAIL_CREATE_EMAIL_DRAFT, GMAIL_SEND_DRAFT`

### Task 63
*Collect operational evidence across spreadsheets, calendar, code repository, ecommerce store, and drive; generate formatted daily dashboard/report tabs; append log rows; and verify the written spreads...*

1. `Read spreadsheet data or get spreadsheet values in Google Sheets or Excel` → `GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_VALUES_GET`
2. `List calendar events or get calendar details` → `GOOGLECALENDAR_EVENTS_LIST`
3. `Get GitHub repository commits or pull requests or repository data` → `GITHUB_LIST_PULL_REQUESTS, GITHUB_LIST_COMMITS`
4. `List ecommerce orders or Shopify orders or products` → `SHOPIFY_GET_SHOP_DETAILS, SHOPIFY_GET_PRODUCTS, SHOPIFY_GET_ORDERS_WITH_FILTERS`
5. `List files or search files in Google Drive` → `GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA`
6. `Append values to spreadsheet or update spreadsheet rows` → `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
7. `Create a new sheet or tab in Google Sheets` → `GOOGLESHEETS_CREATE_GOOGLE_SHEET1`

### Task 64
*Prepare marketing and CRM automation work: gather marketing performance data, send a brief by email, analyze search query data, and scaffold a HubSpot customer follow-up campaign with custom propertie...*

1. `get marketing performance data` → `METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS, LINKEDIN_ADS_GET_AD_ANALYTICS`
2. `send email` → `GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT`
3. `search console query performance` → `GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
4. `HubSpot custom properties email drafts contacts` → `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE, HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE`
5. `create HubSpot property` → `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE`
6. `create HubSpot marketing email` → `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`
7. `batch update contacts HubSpot` → `HUBSPOT_UPDATE_CONTACTS, HUBSPOT_UPDATE_CONTACT`

### Task 65
*Read and update Google Sheets-based SEO planning templates, enrich them with Search Console performance data, and verify that spreadsheet formulas and cleanup steps produced the expected results.*

1. `Read and update Google Sheets spreadsheet` → `GOOGLESHEETS_CREATE_GOOGLE_SHEET1, GOOGLESHEETS_VALUES_GET, GOOGLESHEETS_VALUES_UPDATE`
2. `Search Console performance data analytics` → `GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`

### Task 66
*Create customized application emails with resume and cover letter PDFs, stage them as Outlook drafts, update attachments and body text, then send the finalized drafts after confirmation.*

1. `create outlook email draft` → `OUTLOOK_CREATE_DRAFT`
2. `generate resume cover letter PDF` → `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF`
3. `read file or storage` → `GOOGLEDRIVE_DOWNLOAD_FILE, BOX_DOWNLOAD_FILE`

### Task 67
*Manage Salesforce opportunity pipeline data: list open opportunities, update opportunity stages and required fields, verify record changes, consolidate duplicate contact data, and create a follow-up t...*

1. `List open opportunities in Salesforce` → `SALESFORCE_RUN_SOQL_QUERY`
2. `Update opportunity stages and required fields in Salesforce` → `SALESFORCE_UPDATE_OPPORTUNITY, SALESFORCE_SOBJECT_ROWS_UPDATE`
3. `Consolidate duplicate contact data in Salesforce` → `SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_GET_CONTACT, SALESFORCE_UPDATE_CONTACT, SALESFORCE_DELETE_CONTACT`
4. `Create a follow-up task linked to CRM records in Salesforce` → `SALESFORCE_CREATE_TASK`

### Task 68
*Modify a GitHub-hosted backend application, add protected console and lead-care functionality, configure deployment/runtime infrastructure, apply database migrations, and verify CI plus hosted deploym...*

1. `Search GitHub repositories or files` → `GITHUB_SEARCH_REPOSITORIES, GITHUB_FIND_REPOSITORIES`
2. `Create or update file in GitHub repository` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`

### Task 69
*Perform a technical SEO audit around sitemap migration, indexability, linked-page health, and backlink/link-equity signals using Google Search Console and supporting crawl data.*

1. `Google Search Console technical SEO audit sitemap migration indexability link equity` → `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY, GOOGLE_SEARCH_CONSOLE_INSPECT_URL`
2. `List sitemaps Google Search Console` → `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`

### Task 70
*Migrate Vercel projects and GitHub repositories between connected accounts, preserve domains and settings, add deployment workflows, trigger/verify deployments, and audit repository access.*

1. `Migrate Vercel projects between accounts` → `NEON_TRANSFER_PROJECTS_BETWEEN_ORGANIZATIONS, VERCEL_CREATE_PROJECT_TRANSFER_REQUEST`
2. `Transfer GitHub repository to another account or organization` → `VERCEL_CREATE_PROJECT_TRANSFER_REQUEST`
3. `Vercel domain and project settings` → `VERCEL_ADD_PROJECT_DOMAIN, VERCEL_GET_DOMAIN_CONFIG`
4. `trigger deploy Vercel deployment` → `VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT`
5. `audit repository access collaborator permissions GitHub` → `GITHUB_LIST_BRANCHES, GITHUB_GET_BRANCH_PROTECTION, GITHUB_LIST_REPOSITORY_COLLABORATORS`
6. `create or update file contents in GitHub repository workflow` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`

### Task 71
*Automate a personalized outbound email workflow: check whether prior communication exists, retrieve a CRM-style contact record, send an Outlook email, then update the Airtable record to mark outreach ...*

1. `check whether prior communication exists in Gmail` → `GMAIL_LIST_HISTORY, GMAIL_FETCH_EMAILS`
2. `retrieve a CRM contact record` → `SALESFORCE_GET_ACCOUNT, SALESFORCE_CREATE_NOTE`
3. `send an Outlook email` → `OUTLOOK_SEND_EMAIL`
4. `update Airtable record` → `AIRTABLE_UPDATE_RECORD`

### Task 72
*Build, repair, deploy, configure, and test a Vercel-hosted GitHub-backed API proxy for Gemini text, image, video, embeddings, model listing, OpenAI-compatible paths, and tool-call-style outputs.*

1. `create or manage github repository` → `GITHUB_GET_A_REPOSITORY, GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER`
2. `deploy or manage vercel project` → `VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT`
3. `create or update file github repository` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`

### Task 73
*Manage a large operational workflow across Google Tasks, Xero, and Notion: update and move task records, create and revise invoices, record payments, consolidate Notion rules, and track operational fo...*

1. `Google Tasks update and move task records` → `GOOGLETASKS_PATCH_TASK, GOOGLETASKS_INSERT_TASK, GOOGLETASKS_MOVE_TASK`
2. `Xero create and revise invoices` → `XERO_GET_CONTACTS, XERO_CREATE_INVOICE`
3. `Xero record payments` → `XERO_GET_CONNECTIONS, XERO_LIST_INVOICES, XERO_CREATE_PAYMENT, XERO_LIST_ACCOUNTS`
4. `Notion consolidate rules and track operational follow ups` → `NOTION_CREATE_DATABASE`
5. `Notion query database update page content` → `NOTION_FETCH_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_UPDATE_PAGE`

### Task 74
*Analyze Salesforce opportunity pipeline data by discovering a custom field, retrieving stage metadata, querying filtered opportunity records, fetching stage-change history, and computing stage convers...*

1. `Discover custom fields in Salesforce` → `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT, SALESFORCE_RUN_SOQL_QUERY`
2. `Retrieve stage metadata or picklist values for Salesforce Opportunity stage field` → `SALESFORCE_GET_PICKLIST_VALUES_BY_RECORD_TYPE, SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT`
3. `Fetch stage change history for Salesforce Opportunity object` → `SALESFORCE_RUN_SOQL_QUERY`

### Task 75
*Fetch recent Slack conversation history and threaded replies from one or more conversations for downstream review or export.*

1. `fetch slack conversation history and threaded replies` → `SLACK_FETCH_CONVERSATION_HISTORY, SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION, SLACKBOT_FETCH_CONVERSATION_HISTORY, SLACKBOT_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION`

### Task 76
*Build a cross-channel marketing and operations report by pulling Meta Ads performance and account status, GA4 funnel and revenue data, Instagram profile/insights, Microsoft Clarity friction metrics, a...*

1. `Retrieve Meta Ads performance metrics and account status` → `METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS`
2. `Retrieve Google Analytics 4 report funnel and revenue data` → `GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT, GOOGLE_ANALYTICS_RUN_REPORT`
3. `Retrieve Instagram profile and insights performance` → `INSTAGRAM_GET_USER_INFO`
4. `Retrieve Microsoft Clarity friction metrics and session recordings` → `MICROSOFT_CLARITY_DATA_EXPORT, POSTHOG_RETRIEVE_SESSION_RECORDING_DETAILS`
5. `Retrieve ClickUp tasks and documents for planning context` → `CLICKUP_GET_TASKS, CLICKUP_CREATE_TASK, CLICKUP_UPDATE_TASK`
6. `Retrieve ClickUp documents` → `CLICKUP_GET_AUTHORIZED_USER, CLICKUP_CLICK_UP_SEARCH_DOCS, CLICKUP_CLICK_UP_GET_DOC_CONTENT, CLICKUP_GET_DOC_PAGE_LISTING, CLICKUP_CLICK_UP_GET_DOC_PAGE_CONTENT`

### Task 77
*Audit a Google Ads client account under a manager account, research targeting and keywords, then build and verify a new search campaign with budget, targeting, keywords, ads, and assets.*

1. `google ads get manager client accounts` → `GOOGLEADS_LIST_SUB_ACCOUNTS`
2. `google ads audit campaigns keywords performance` → `GOOGLEADS_SEARCH_STREAM_GAQL, GOOGLE_ANALYTICS_RUN_REPORT`
3. `google ads create mutate campaigns budgets keywords ads assets` → `GOOGLEADS_GET_CAMPAIGN_BY_NAME, GOOGLEADS_CREATE_CUSTOMER_LIST, GOOGLEADS_ADD_OR_REMOVE_TO_CUSTOMER_LIST`
4. `google ads mutate operations campaigns keywords ad groups ads` → `GOOGLEADS_SEARCH_STREAM_GAQL`

### Task 78
*Audit and clean Pipedrive CRM data by exporting paginated leads and related records, then bulk-normalizing titles, organization names, duplicate organizations, deal and lead titles, lead labels, and c...*

1. `export paginated leads and related records from Pipedrive CRM` → `PIPEDRIVE_GET_ALL_LEADS`
2. `get all organizations and deals from Pipedrive CRM` → `PIPEDRIVE_GET_ALL_DEALS`
3. `get all organizations from Pipedrive CRM` → `PIPEDRIVE_GET_ALL_ORGANIZATIONS`
4. `update organization details in Pipedrive CRM` → `PIPEDRIVE_UPDATE_AN_ORGANIZATION`
5. `update deal details in Pipedrive CRM` → `PIPEDRIVE_UPDATE_DEAL, PIPEDRIVE_ADD_FILE, PIPEDRIVE_UPDATE_A_NOTE, PIPEDRIVE_ADD_AN_ACTIVITY`
6. `update lead details in Pipedrive CRM` → `PIPEDRIVE_UPDATE_LEAD`
7. `update custom fields or lead labels in Pipedrive CRM` → `PIPEDRIVE_UPDATE_PERSON_FIELD`
8. `get lead labels in Pipedrive CRM` → `PIPEDRIVE_GET_ALL_LEAD_LABELS`

### Task 79
*Audit and manage a YouTube channel by collecting channel/video data, analyzing performance, listing and restructuring playlists, adding/removing/reordering playlist videos, and researching high-perfor...*

1. `YouTube channel details statistics analytics` → `YOUTUBE_GET_CHANNEL_STATISTICS`
2. `YouTube playlist management list create update delete items` → `YOUTUBE_DELETE_PLAYLIST`
3. `YouTube video search research topics trends` → `COMPOSIO_SEARCH_WEB, YOUTUBE_SEARCH_YOU_TUBE, YOUTUBE_GET_VIDEO_DETAILS_BATCH`

### Task 80
*Audit Meta Ads account access, inspect performance for a specific ad set, identify improvement actions, then create a Trello card with an attached report and assignee; also attempt to clean up a fault...*

1. `Meta Ads account access audit` → `METAADS_GET_USER, METAADS_GET_AD_ACCOUNTS`
2. `Meta Ads ad set performance insights` → `METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS`
3. `Create Trello card attachment member` → `TRELLO_ADD_CARDS, TRELLO_ADD_CARDS_ATTACHMENTS_BY_ID_CARD`
4. `Delete Trello card attachment` → `TRELLO_DELETE_CARD_ATTACHMENT`

### Task 81
*Inventory YouTube channel videos, generate and update video metadata in bulk, verify updates, and fetch captions/transcript for a YouTube video.*

1. `youtube list channel videos` → `YOUTUBE_LIST_CHANNEL_VIDEOS`
2. `youtube update video metadata` → `YOUTUBE_UPDATE_VIDEO`
3. `youtube get video captions transcript` → `YOUTUBE_LOAD_CAPTIONS, YOUTUBE_LIST_CAPTION_TRACK`

### Task 82
*Manage and clean up Outlook inbox messages by finding matches from senders, subject patterns, unread status, and folder locations; move matched emails into target folders, move unwanted emails to Dele...*

1. `search outlook emails by sender subject unread folder` → `OUTLOOK_QUERY_EMAILS`
2. `move outlook email to folder deleted items` → `OUTLOOK_BATCH_MOVE_MESSAGES`
3. `outlook mail rules create remove` → `OUTLOOK_LIST_EMAIL_RULES, OUTLOOK_DELETE_EMAIL_RULE`
4. `create outlook email rule` → `OUTLOOK_LIST_EMAIL_RULES, OUTLOOK_CREATE_EMAIL_RULE`

### Task 83
*Read files from a Microsoft cloud document library, inspect related due-diligence email context, locate supporting documents, and attempt to replace existing document contents.*

1. `read files from microsoft cloud document library sharepointonedrive` → `ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN, ONE_DRIVE_DOWNLOAD_FILE`
2. `search emails outlook due diligence` → `OUTLOOK_QUERY_EMAILS`
3. `update replace upload file content sharepoint onedrive` → `ONE_DRIVE_UPDATE_FILE_CONTENT, SHARE_POINT_UPLOAD_FILE`

### Task 84
*Use GitHub to inspect accessible repositories and branches, fetch repository files, update multiple repository files, create a public static preview repository, enable GitHub Pages, and commit generat...*

1. `List repositories on GitHub` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER, GITHUB_FIND_PULL_REQUESTS`
2. `List branches of a repository on GitHub` → `GITHUB_LIST_BRANCHES`
3. `Fetch repository content or file from GitHub` → `GITHUB_GET_REPOSITORY_CONTENT`
4. `Create or update repository files on GitHub` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`
5. `Create a repository on GitHub` → `GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER`
6. `Enable GitHub Pages on a repository` → `GITHUB_CREATE_OR_UPDATE_GITHUB_PAGES_SITE, GITHUB_GET_A_REPOSITORY`

### Task 85
*Investigate and patch a codebase hosted on GitHub, commit changes to a target branch, document the change, and merge that branch into the destination branch after approval.*

1. `search issues or pull requests on GitHub` → `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`
2. `get repository content commit changes create branch merge pull request GitHub` → `GITHUB_GET_REPOSITORY_CONTENT, GITHUB_COMMIT_MULTIPLE_FILES, GITHUB_CREATE_A_PULL_REQUEST`
3. `merge a pull request on GitHub` → `GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
4. `list user repositories on GitHub` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`

### Task 86
*Retrieve Salesforce CRM report and query data for a business-performance brief, then send Slack notifications with the generated results.*

1. `Retrieve Salesforce CRM report data` → `SALESFORCE_RUN_REPORT, SALESFORCE_GET_REPORT_INSTANCE`
2. `Execute a SOQL query against Salesforce data` → `SALESFORCE_RUN_SOQL_QUERY`
3. `Send Slack message or notification` → `SLACK_SEND_MESSAGE, SLACKBOT_SEND_MESSAGE`

### Task 87
*Set up and reorganize business lead-tracking and governance records in Notion, after initially exploring tools for social posting, web research, CRM lead handling, and website publishing.*

1. `Notion search database pages` → `NOTION_QUERY_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER`
2. `Notion search pages and databases` → `NOTION_SEARCH_NOTION_PAGE`
3. `create Notion database` → `NOTION_CREATE_DATABASE`
4. `create Notion database row page` → `NOTION_CREATE_NOTION_PAGE, NOTION_INSERT_ROW_DATABASE`
5. `add content to Notion page markdown blocks` → `NOTION_ADD_MULTIPLE_PAGE_CONTENT`

### Task 88
*Bulk triage new Zendesk support tickets across multiple support mailboxes, enrich tickets with requester/order context, add private internal AI triage notes, tag tickets as analyzed, and verify privat...*

1. `search Zendesk support tickets across multiple mailboxes` → `ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_SEARCH_ZENDESK`
2. `get customer order context and details` → `SALESFORCE_RUN_SOQL_QUERY`
3. `update ticket comments and tags in Zendesk` → `ZENDESK_UPDATE_ZENDESK_TICKET`
4. `add comment to Zendesk ticket` → `ZENDESK_UPDATE_ZENDESK_TICKET`

### Task 89
*Audit inbound email and HubSpot marketing/automation assets to understand an external funnel, compare it with existing marketing emails and workflows, and inspect meeting-booking setup.*

1. `search emails or inbound messages` → `GMAIL_FETCH_EMAILS`
2. `HubSpot marketing emails and workflows` → `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUB_SPOT_ACCOUNT, HUBSPOT_GET_AGGREGATED_STATISTICS, HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL`
3. `HubSpot automation workflows` → `HUBSPOT_GET_ALL_WORKFLOWS`
4. `HubSpot meeting booking scheduling links` → `HUBSPOT_CREATE_MEETING`

### Task 90
*Create and refine a Google Slides presentation by inspecting existing slides and layouts, adding styled slides, inserting an image, and verifying the rendered result.*

1. `google slides inspect presentation slides and layouts` → `GOOGLESLIDES_PRESENTATIONS_GET`
2. `google slides batch update create slide insert image` → `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE`

### Task 91
*Manage Meta ads reporting and campaign status, and handle Facebook Page inbox workflows including reading conversations and sending private replies or bulk follow-up messages.*

1. `Fetch Meta ads reports and manage campaign status` → `METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS`
2. `Update Meta ads campaign status active paused` → `METAADS_GET_OBJECT, METAADS_UPDATE_CAMPAIGN`
3. `Facebook page inbox conversations messages replies` → `FACEBOOK_GET_PAGE_CONVERSATIONS, FACEBOOK_GET_CONVERSATION_MESSAGES, FACEBOOK_SEND_MESSAGE`

### Task 92
*Migrate active Todoist projects, sections, tasks, subtasks, labels, due dates, priorities, durations, and assignment metadata into a private ClickUp Space, then verify the migration without modifying ...*

1. `Get all projects and tasks from Todoist` → `TODOIST_GET_ALL_PROJECTS`
2. `Create ClickUp space and tasks` → `CLICKUP_CREATE_SPACE, CLICKUP_CREATE_FOLDER, CLICKUP_CREATE_LIST, CLICKUP_CREATE_TASK`
3. `Get sections and tasks from Todoist` → `TODOIST_LIST_SECTIONS, TODOIST_GET_ALL_TASKS`
4. `Get ClickUp workspaces` → `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES`

### Task 93
*Analyze Salesforce CRM data by discovering schema, running SOQL queries, extracting a large set of related records, and computing a cohort-based return-rate metric.*

1. `Salesforce discover schema and describe objects` → `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT`
2. `Salesforce describe global objects` → `SALESFORCE_GET_ALL_CUSTOM_OBJECTS, SALESFORCE_GET_SUPPORTED_OBJECTS_DIRECTORY`
3. `Salesforce run SOQL query` → `SALESFORCE_RUN_SOQL_QUERY`

### Task 94
*Audit and optimize a Meta Ads account: retrieve account, campaign, ad set, ad, creative, performance, targeting, and pixel data; then apply confirmed optimization changes including pausing objects, ch...*

1. `Retrieve Meta Ads account campaign ad set ad creative performance targeting pixel data` → `METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS`
2. `Retrieve campaigns creatives targeting pixels Meta Ads` → `METAADS_LIST_ADS, METAADS_GET_AD_CREATIVE`
3. `pause objects change ad set targeting reactivate campaign create custom audiences add exclusions Meta Ads` → `METAADS_GET_OBJECT, METAADS_UPDATE_CAMPAIGN`
4. `update ad set targeting status Meta Ads` → `METAADS_READ_ADSETS, METAADS_CREATE_AD_SET`
5. `create custom audience Meta Ads` → `METAADS_CREATE_CUSTOM_AUDIENCE`
6. `update ad set properties targeting exclusions Meta Ads` → `METAADS_CREATE_AD_SET`

### Task 95
*Fetch Zoho Books bank accounts and bank transactions, then handle uncategorized bank-feed transactions for reconciliation.*

1. `Get list of bank accounts from Zoho Books` → `ZOHO_BOOKS_LIST_BANK_ACCOUNTS, ZOHO_BOOKS_GET_BANK_ACCOUNT`
2. `List organizations in Zoho Books` → `ZOHO_BOOKS_LIST_ORGANIZATIONS`
3. `categorize bank transactions or bank feed in Zoho Books` → `ZOHO_BOOKS_CATEGORIZE_UNCATEGORIZED_TRANSACTION, ZOHO_BOOKS_EXCLUDE_BANK_TRANSACTION, ZOHO_BOOKS_CATEGORIZE_AS_CUSTOMER_PAYMENT_REFUND`
4. `List uncategorized bank transactions in Zoho Books` → `ZOHO_BOOKS_LIST_BANK_TRANSACTIONS`

### Task 96
*Implement several sequential feature-track boundaries in a GitHub repository, commit each boundary separately, run smoke tests after each commit, then verify the final branch head and check-run status...*

1. `GitHub repository management, branches, commits, and check runs` → `GITHUB_LIST_PULL_REQUESTS, GITHUB_LIST_BRANCHES, GITHUB_LIST_COMMITS, GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY, GITHUB_GET_A_REPOSITORY`
2. `Create commit or files in GitHub repository` → `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`

### Task 97
*Manage Pipedrive CRM records: find deals and contacts, update deal participants and primary contacts, log notes and activities, schedule follow-ups, inspect deal and organization custom fields, and bu...*

1. `Find deals and contacts in Pipedrive CRM` → `PIPEDRIVE_SEARCH_PERSONS, PIPEDRIVE_LIST_PERSON_DEALS, PIPEDRIVE_GET_ALL_DEALS`
2. `Update deal participants and primary contacts in Pipedrive CRM` → `PIPEDRIVE_UPDATE_DEAL`
3. `Log notes and activities and schedule follow-ups in Pipedrive CRM` → `PIPEDRIVE_GET_ACTIVITY, PIPEDRIVE_UPDATE_ACTIVITY, PIPEDRIVE_ADD_AN_ACTIVITY`
4. `Inspect deal and organization custom fields in Pipedrive CRM` → `PIPEDRIVE_GET_ALL_DEAL_FIELDS`
5. `Inspect organization custom fields in Pipedrive CRM` → `PIPEDRIVE_GET_ALL_ORGANIZATION_FIELDS, PIPEDRIVE_ADD_ORGANIZATION_FIELD`
6. `Bulk reclassify deals across pipeline stages based on contract timing data in Pipedrive CRM` → `PIPEDRIVE_UPDATE_A_DEAL`

### Task 98
*Analyze owned social media, paid ads, and website attribution performance across YouTube, Instagram, Facebook Page, Meta Ads, and GA4 for a recent multi-month reporting window.*

1. `Get social media analytics and metrics for YouTube, Instagram, and Facebook Page` → `YOUTUBE_GET_CHANNEL_STATISTICS, INSTAGRAM_GET_USER_INSIGHTS, FACEBOOK_GET_PAGE_INSIGHTS, INSTAGRAM_GET_IG_MEDIA, INSTAGRAM_GET_IG_MEDIA_INSIGHTS`
2. `Get Meta Ads performance insights and ad campaign analytics` → `METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS`
3. `Get GA4 website attribution and traffic performance reports` → `GOOGLESUPER_RUN_REPORT, GOOGLESUPER_BATCH_RUN_REPORTS`

### Task 99
*Maintain and review a Notion-based project task page and append-only log for a technical project, including reading state, posting review/decision rows, updating task-page checklists, and inspecting a...*

1. `read notion pages and databases` → `NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER`
2. `create notion page or update database row or append block` → `NOTION_QUERY_DATABASE, NOTION_INSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE, NOTION_CREATE_NOTION_PAGE`
3. `list databases in notion workspace` → `NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATA`
4. `inspect supabase schema` → `SUPABASE_GET_TABLE_SCHEMAS, SUPABASE_BETA_RUN_SQL_QUERY`

### Task 100
*Extract CRM list-entry records from Attio, join them with Attio company domains, and prepare a domain-to-owner mapping for downstream processing.*

1. `Extract CRM list-entry records and company domains from Attio` → `ATTIO_POST_V2_LISTS_LIST_ENTRIES_QUERY`
2. `List companies and get company domains in Attio` → `ATTIO_LIST_COMPANIES`

