# What went wrong — `run8_full_100tasks`

The 100 use cases need **433 capabilities** between them. This is every one that was
not delivered, why, and whose problem it is to fix.

## The short version

- **Search almost always finds the right tool.** It failed to retrieve one for a fair, specific query in **4 of 433** cases.
- **It just does not always recommend it.** In **83** cases the right tool came back only under `related`, never as a primary recommendation. An agent acting on the recommendation misses all 83 — so this, not retrieval, is the thing worth fixing.
- **52 failures are the agent's own**: it either never searched for the capability (28) or asked too vaguely to find it (24). These say nothing about search quality.
- **18** need a tool that does not exist in the catalogue at all.

| What happened | Count | Whose problem |
|---|---:|---|
| Search found it but buried it | 83 | **Search — ranking** |
| The agent never looked for it | 28 | Agent |
| The agent asked too vaguely | 24 | Agent |
| No tool exists for it | 18 | Catalogue |
| Search missed a fair question | 4 | **Search — retrieval** |

**Search-side 87 · agent-side 52 · catalogue 18.**

---

## Search found the right tool but buried it

83 capabilities were delivered **only** in `related`. The tool was there; it
was never put forward. This is the largest fixable failure in the run, and counting it
needs no judgement — it is set membership.

| Task | What was needed | Tool that was buried |
|---|---|---|
| 1 | Create or manage review-only automated confirmation email | `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION`, `HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL` |
| 3 | Upload the modified file back to OneDrive and verify the update | `ONE_DRIVE_UPDATE_FILE_CONTENT` |
| 4 | Add a comment or update status/logs on a Trello card | `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD` |
| 4 | Move a Trello card between lists (update status) | `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD` |
| 5 | Query, read, and update CRM records and status updates in Notion | `NOTION_FETCH_DATABASE`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_SEARCH_NOTION_PAGE` |
| 12 | Add comments to Trello cards | `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD` |
| 12 | Search or retrieve Trello cards and boards | `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH` |
| 13 | Audit website traffic and analytics performance | `GOOGLE_ANALYTICS_RUN_REPORT` |
| 15 | Retrieve invoice attachments from emails | `GMAIL_GET_ATTACHMENT` |
| 16 | Audit analytics and search performance | `GOOGLE_ANALYTICS_RUN_REPORT` |
| 17 | List, inspect, and select avatars and voices for HeyGen video generation | `HEYGEN_RETRIEVE_AVATAR_DETAILS`, `HEYGEN_V1_AVATAR_LIST`, `HEYGEN_V2_VOICES` |
| 20 | Manage and verify fields and records in Zoho CRM | `ZOHO_GET_MODULE_FIELDS` |
| 21 | Read spreadsheet data and metadata | `GOOGLESHEETS_BATCH_GET` |
| 21 | Create a new summary worksheet | `GOOGLESHEETS_ADD_SHEET` |
| 23 | Retrieve detailed ticket information and comments | `ZENDESK_GET_ZENDESK_TICKET_BY_ID` |
| 23 | Enrich tickets with requester and user context | `ZENDESK_GET_USER` |
| 25 | Fetch the content of job listing web pages | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |
| 29 | Inspect recent meeting notes and files from Google Drive | `GOOGLEDRIVE_DOWNLOAD_FILE` |
| 31 | Retrieve WhatsApp business account details to send notifications | `WHATSAPP_GET_PHONE_NUMBERS` |
| 33 | Retrieve conversations to analyze audience reach, replies, and WhatsApp campaign interactions | `KOMMO_LIST_CONVERSATIONS` |
| 36 | Inspect organization and repository access/ownership | `GITHUB_FIND_REPOSITORIES`, `GITHUB_GET_A_REPOSITORY` |
| 37 | Reply to or forward messages | `OUTLOOK_REPLY_EMAIL` |
| 38 | Read and update a Google Sheets tracking spreadsheet | `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_SEARCH_SPREADSHEETS`, `GOOGLESHEETS_UPDATE_VALUES_BATCH` |
| 39 | Read and update data in Google Spreadsheet reporting workbook | `GOOGLESHEETS_BATCH_GET` |
| 40 | Search and retrieve Notion pages and databases | `NOTION_SEARCH_NOTION_PAGE` |
| 40 | Create and update Notion pages, database rows, and block content | `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_INSERT_ROW_DATABASE` |
| 41 | Read content or export data from Google Docs / Google Drive | `GOOGLEDRIVE_DOWNLOAD_FILE` |
| 45 | Associate CRM records (such as contact, deal, line items, and quote) | `HUBSPOT_CREATE_OBJECT_ASSOCIATION` |
| 46 | Search and discover Notion pages and databases | `NOTION_SEARCH_NOTION_PAGE` |
| 46 | Create and update Notion pages, database rows, and properties | `NOTION_UPSERT_ROW_DATABASE` |
| 47 | Retrieve information about the existing campaign to be duplicated | `METAADS_GET_OBJECT` |
| 48 | Upload files to cloud storage | `GOOGLEDRIVE_RESUMABLE_UPLOAD` |
| 49 | Get file metadata to check properties before operations | `GOOGLEDRIVE_GET_FILE_METADATA` |
| 49 | Download or export files from Google Drive | `GOOGLEDRIVE_DOWNLOAD_FILE` |
| 50 | Find and resolve Slack channels by name or criteria | `SLACK_FIND_CHANNELS` |
| 51 | Query database for operational or user data evidence | `METABASE_POST_API_DATASET` |
| 53 | Browse public website URLs and check redirects or article accessibility | `BROWSER_TOOL_CREATE_TASK` |
| 54 | Create and manage Google Ads campaigns | `GOOGLEADS_MUTATE_CAMPAIGNS` |
| 54 | Create and manage ad groups in Google Ads | `GOOGLEADS_MUTATE_AD_GROUPS` |
| 55 | Retrieve spreadsheet metadata and data from worksheets | `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_GET_SPREADSHEET_INFO` |
| 55 | Apply cell formatting and auto-resize dimensions | `GOOGLESHEETS_FORMAT_CELL` |
| 56 | Inspect property definitions and metadata | `HUBSPOT_LIST_CONTACT_PROPERTIES`, `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` |
| 57 | Analyze channel and trend performance on YouTube | `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CHANNEL_VIDEOS` |
| 57 | Upload and manage YouTube Shorts | `YOUTUBE_MULTIPART_UPLOAD_VIDEO`, `YOUTUBE_UPDATE_VIDEO` |
| 60 | Write, append, and update values in Google Sheets | `GOOGLESHEETS_VALUES_UPDATE` |
| 60 | Apply formatting and styling to cells in Google Sheets | `GOOGLESHEETS_FORMAT_CELL` |
| 61 | Move messages between folders | `OUTLOOK_MOVE_MESSAGE` |
| 61 | Update email properties such as read status | `OUTLOOK_UPDATE_EMAIL` |
| 62 | Read the contents and structure of an existing Google Document | `GOOGLEDOCS_GET_DOCUMENT_BY_ID`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT` |
| 62 | Update an existing Google Document with edits, text changes, or structural modifications | `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT` |
| 63 | List calendar events for operational evidence | `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` |
| 64 | Draft or update marketing emails in HubSpot | `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_UPDATE_A_MARKETING_EMAIL` |
| 66 | Add attachments to email messages | `OUTLOOK_ADD_MAIL_ATTACHMENT` |
| 66 | Update email message content | `OUTLOOK_UPDATE_EMAIL` |
| 66 | Send existing email drafts | `OUTLOOK_SEND_DRAFT` |
| 67 | Retrieve field metadata and requirements for Salesforce objects | `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT` |
| 70 | Retrieve and manage Vercel project details, configurations, and metadata | `VERCEL_GET_PROJECT2`, `VERCEL_GET_PROJECTS` |
| 70 | Retrieve, inspect, and verify Vercel project domains and settings | `VERCEL_GET_PROJECT_DOMAINS`, `VERCEL_LIST_DOMAINS` |
| 70 | List and inspect GitHub repositories | `GITHUB_GET_A_REPOSITORY` |
| 71 | Check whether prior communication exists in email | `OUTLOOK_SEARCH_MESSAGES` |
| 71 | Retrieve a CRM-style contact record | `AIRTABLE_GET_RECORD`, `AIRTABLE_LIST_RECORDS` |
| 73 | Read and manage Notion pages and content | `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_SEARCH_NOTION_PAGE` |
| 78 | Get organization fields and add organization field | `PIPEDRIVE_GET_ALL_ORGANIZATION_FIELDS` |
| 79 | List and retrieve user playlists | `YOUTUBE_LIST_USER_PLAYLISTS` |
| 79 | Create and restructure playlists (add, modify, delete playlists and items, and reorder videos) | `YOUTUBE_UPDATE_PLAYLIST` |
| 81 | Retrieve video metadata in bulk or detail | `YOUTUBE_GET_VIDEO_DETAILS_BATCH` |
| 82 | List and inspect mail folders and subfolders | `OUTLOOK_LIST_MAIL_FOLDERS` |
| 82 | Delete unwanted messages | `OUTLOOK_DELETE_MESSAGE` |
| 83 | Search and retrieve related email context | `OUTLOOK_GET_MESSAGE`, `OUTLOOK_SEARCH_MESSAGES` |
| 84 | Fetch repository file contents and structure | `GITHUB_GET_A_TREE`, `GITHUB_GET_RAW_REPOSITORY_CONTENT`, `GITHUB_SEARCH_CODE` |
| 84 | Create a public static preview repository | `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY` |
| 85 | Manage branches and references | `GITHUB_GET_A_REFERENCE` |
| 87 | Modify or remove existing Notion pages, database rows, or blocks during reorganization | `NOTION_DELETE_BLOCK` |
| 88 | Fetch detailed ticket information and requester/order context | `ZENDESK_GET_USER`, `ZENDESK_GET_ZENDESK_TICKET_BY_ID` |
| 90 | Verify rendered slide results by generating page thumbnails | `GOOGLESLIDES_GET_PAGE_THUMBNAIL2` |
| 91 | List and get details for managed Facebook Pages | `FACEBOOK_LIST_MANAGED_PAGES` |
| 96 | Commit changes to the repository | `GITHUB_COMMIT_MULTIPLE_FILES` |
| 96 | Browse repository file structure | `GITHUB_GET_A_TREE` |
| 96 | Verify check-run status and CI results | `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` |
| 98 | Analyze Facebook Page managed content and engagement performance | `FACEBOOK_LIST_MANAGED_PAGES` |
| 99 | Update Notion page content and checklists | `NOTION_ADD_MULTIPLE_PAGE_CONTENT` |
| 99 | Inspect Supabase schema and database structure | `SUPABASE_LIST_TABLES`, `SUPABASE_RUN_READ_ONLY_QUERY` |
| 100 | Query and retrieve Attio company records and their domains/owners | `ATTIO_QUERY_RECORDS` |

## Search missed a fair question

4 cases where the query did identify what was needed and search still did
not return it. Each is laid out in full so it can be checked.

#### Task 16 — Modify repository code and create pull requests

- **Asked:** `Git repository file inspect and commit or pull request`
- **Needed:** `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`
- **Got:** primary: GITHUB_GET_A_REPOSITORY, GITHUB_GET_A_TREE, GITHUB_GET_REPOSITORY_CONTENT, GITHUB_LIST_COMMITS, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
  related: GITHUB_LIST_BRANCHES, GITHUB_GET_A_REFERENCE, GITHUB_GET_RAW_REPOSITORY_CONTENT, GITHUB_SEARCH_CODE
- **What went wrong:** The query describes core Git repository file inspection and commit/PR operations, which directly aligns with the functionality of a GitHub multi-file commit and repository modification tool. [3/3 votes] (query asks to 'commit' but every tool returned is tagged read-only, so the write half of the query was never answered)
- **Judge:** None of the returned GitHub tools provide the ability to modify repository code or create pull requests; the available tools only retrieve references and search issues or pull requests.

#### Task 18 — Search and extract recent job listings from web sources or job boards

- **Asked:** `Search job listings or job boards for remote hybrid contract data engineering jobs`
- **Needed:** `BROWSER_TOOL_CREATE_TASK`
- **Got:** primary: COMPOSIO_SEARCH_WEB
  related: COMPOSIO_SEARCH_FETCH_URL_CONTENT, COMPOSIO_SEARCH_NEWS, COMPOSIO_SEARCH_TRENDS, LINKEDIN_GET_POST_CONTENT
- **What went wrong:** The query explicitly describes a multi-step web scraping and browsing task across job boards, which directly maps to the browser automation tool's capabilities of navigating websites, filling forms, and extracting data. [3/3 votes]
- **Judge:** None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

#### Task 28 — Generate AI text-to-speech audio for the video voiceover

- **Asked:** `Generate AI video or text to speech voice`
- **Needed:** `ELEVENLABS_TEXT_TO_SPEECH`
- **Got:** primary: GEMINI_GENERATE_VIDEOS
  related: GEMINI_GENERATE_IMAGE, GEMINI_WAIT_FOR_VIDEO, TRELLO_GET_CARDS_BY_ID_CARD
- **What went wrong:** The query explicitly asks to 'Generate ... text to speech voice', which directly matches the primary function of the ElevenLabs text-to-speech tool. [3/3 votes]
- **Judge:** None of the returned tools provide text-to-speech audio generation capabilities.

#### Task 72 — Configure project environment variables on Vercel

- **Asked:** `deploy or manage vercel project`
- **Needed:** `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`
- **Got:** primary: VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT
  related: VERCEL_GET_TEAMS, VERCEL_GET_PROJECT2, VERCEL_SEARCH_REPO, GITHUB_GET_A_REPOSITORY, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_DEPLOYMENT_LOGS2
- **What went wrong:** The query asks to manage a Vercel project, which sufficiently captures the intent of configuring project-level settings like environment variables. [3/3 votes]
- **Judge:** None of the returned Vercel tools provide the capability to add or configure environment variables on a Vercel project.

## Queries that named an application and got a different one

Of 384 queries, 249 name an application. 6 of those got nothing from it in `primary`, and 3 got nothing from it anywhere.

Counted separately because it happens even when no capability was missed — task 1
asked for a HubSpot payment link and was answered entirely in Stripe.

| Task | Asked | Wanted from | Got | Named app absent entirely |
|---|---|---|---|---|
| 1 | `Create or check payment link in HubSpot` | hubspot | `STRIPE_CREATE_PAYMENT_LINK` | **yes** |
| 11 | `Send Discord channel message` | discord | `DISCORDBOT_CREATE_MESSAGE` | no |
| 24 | `Search LinkedIn job listings` | linkedin | `COMPOSIO_SEARCH_WEB` | no |
| 33 | `broadcast campaigns kommo crm` | kommo | `KIT_CREATE_BROADCAST` | **yes** |
| 57 | `create short video dog themed YouTube Shorts` | youtube | `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO` | no |
| 70 | `Transfer GitHub repository to another account or o` | github | `VERCEL_CREATE_PROJECT_TRANSFER_REQUEST` | **yes** |

---

## Failures that are not search's fault

### The agent never looked for it (28)

No query it issued was aimed at this capability, so search was never asked.

| Task | Capability that was never searched for |
|---|---|
| 2 | Verify Notion content after writing |
| 7 | Fetch and read email messages and threads |
| 12 | Fetch and search Gmail emails for project management |
| 19 | Fetch and read content from web pages or job postings |
| 27 | Create a new folder in Google Drive |
| 31 | Retrieve real-time market data and financial information |
| 32 | Public web research and content extraction |
| 32 | Browser automation and QA for web applications |
| 32 | Retail product and catalog search |
| 32 | Fast LLM inference and content generation |
| 33 | List leads to analyze conversions and campaign outcomes |
| 46 | Lookup workspace users for owner assignment |
| 53 | List and retrieve existing short links from a short-link management platform |
| 54 | Create and manage campaign budgets in Google Ads |
| 54 | Configure campaign-level targeting criteria |
| 54 | Add keywords and targeting criteria to ad groups |
| 54 | Create and manage ads including responsive search ads |
| 55 | Apply filters and sort options to data ranges |
| 55 | Modify worksheet properties and metadata |
| 68 | Verify CI check runs and workflow status |
| 68 | Apply database migrations via SQL execution |
| 68 | Check hosted deployment status and logs on Vercel |
| 69 | Scrape and crawl web pages to gather linked-page health and technical crawl data |
| 72 | Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models |
| 72 | Generate images using Gemini image models |
| 72 | Generate and poll/wait for videos using Google Veo models |
| 72 | Generate text embeddings using Gemini models |
| 73 | Get current date and time |

### The agent asked too vaguely (24)

It searched, but the query did not identify the tool it needed.

#### Task 9 — Search or source stock images for marketing assets

- **Asked:** `Create multimedia travel marketing assets from scripts and stock media`
- **Needed:** `COMPOSIO_SEARCH_IMAGE`
- **Got:** primary: GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE
  related: GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GET_VIDEOS_OPERATION, HEYGEN_V2_TEMPLATES, HEYGEN_V2_TEMPLATE_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned tools generate multimedia assets like videos and images from content inputs, which directly fulfills the query for creating travel marketing assets.

#### Task 12 — Search and list Slack messages and users for chat integration

- **Asked:** `Send a chat message`
- **Needed:** `SLACK_SEARCH_MESSAGES`, `SLACK_LIST_ALL_USERS`
- **Got:** primary: CLICKUP_CREATE_CHAT_MESSAGE
  related: CLICKUP_GET_CHAT_CHANNELS, CLICKUP_GET_CHAT_MESSAGES, CLICKUP_GET_SUBTYPES
- **What went wrong:** The query is too generic and describes a messaging action rather than a search action, making it ambiguous for a specific message-search tool. [0/3 votes]

#### Task 13 — Audit website search performance and indexing

- **Asked:** `Audit website search and traffic performance in analytics`
- **Needed:** `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITE`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`
- **Got:** primary: GOOGLESUPER_RUN_REPORT, GOOGLESUPER_BATCH_RUN_REPORTS
  related: GOOGLESUPER_LIST_PROPERTIES, GOOGLESUPER_CHECK_COMPATIBILITY, GOOGLESUPER_GET_METADATA, GOOGLE_ANALYTICS_RUN_REPORT, GOOGLE_ANALYTICS_BATCH_RUN_REPORTS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- Both the expected and returned tools retrieve and analyze website search and traffic performance data using Google reporting services.

#### Task 13 — Prepare and manage email marketing or contact lists

- **Asked:** `Search for contacts or create email lists in CRM or email marketing tool`
- **Needed:** `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
- **Got:** primary: GMAIL_GET_CONTACTS, GMAIL_SEARCH_PEOPLE
  related: GMAIL_GET_PEOPLE, GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Gmail tools manage contacts and user lists, which is the same functional work requested by the query for a CRM or email marketing tool.

#### Task 16 — Investigate hosting and deployment state via DNS/CDN configuration

- **Asked:** `Vercel Netlify Heroku deployment status inspect`
- **Needed:** `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
- **Got:** primary: VERCEL_GET_DEPLOYMENTS, VERCEL_GET_DEPLOYMENT, VERCEL_GET_DEPLOYMENT_LOGS2
  related: VERCEL_GET_PROJECT2, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_PROJECTS, VERCEL_GET_DEPLOYMENT_EVENTS2
- **What went wrong:** query names vercel but the step needs cloudflare

#### Task 17 — Attempt social media publishing on Instagram

- **Asked:** `Publish video to social media platforms`
- **Needed:** `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
- **Got:** primary: UPLOAD_POST_PUBLISH_POST, WOOP_SOCIAL_PUBLISH_POST_NOW
  related: UPLOAD_POST_LIST_PROFILES, UPLOAD_POST_GET_UPLOAD_STATUS, UPLOAD_POST_LIST_PLATFORM_DESTINATIONS, WOOP_SOCIAL_LIST_SOCIAL_ACCOUNTS, WOOP_SOCIAL_VALIDATE_POST
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned tools perform the exact same core function of publishing posts to social media platforms, just using different integrations than Instagram.

#### Task 17 — Read and update the booking schedule

- **Asked:** `Read and update bookings or calendar events`
- **Needed:** `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
- **Got:** primary: GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_PATCH_EVENT, GOOGLECALENDAR_DELETE_EVENT, GOOGLECALENDAR_CREATE_EVENT
  related: GOOGLECALENDAR_EVENTS_LIST, GOOGLECALENDAR_EVENTS_GET, GOOGLECALENDAR_EVENTS_INSTANCES, GOOGLECALENDAR_BATCH_EVENTS, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned calendar tools successfully handle reading, updating, and managing events, which matches the core task requested by the query.

#### Task 22 — look up CRM-style trial records

- **Asked:** `Search CRM trial records or contacts`
- **Needed:** `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
- **Got:** primary: SALESFORCE_LIST_CONTACTS, SALESFORCE_RUN_SOQL_QUERY
  related: SALESFORCE_QUERY, SALESFORCE_QUERY_ALL, SALESFORCE_GET_CONTACT
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Salesforce tools search CRM contacts and records, which is the exact same kind of work requested by the query, just in a different CRM application than Airtable or Pipedrive.

#### Task 22 — inspect and modify source code in GitHub, and handle branches

- **Asked:** `Search GitHub repositories issues pull requests workflows actions code`
- **Needed:** `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_MERGE_A_BRANCH`
- **Got:** primary: GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
  related: GITHUB_FIND_PULL_REQUESTS, GITHUB_LIST_REPOSITORY_ISSUES, GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_AN_ISSUE, GITHUB_LIST_PULL_REQUESTS_FILES, GITHUB_LIST_ISSUE_COMMENTS
- **What went wrong:** The query is a broad generic list of GitHub features rather than a specific request to atomically commit multiple files to a repository. [0/3 votes]

#### Task 22 — check CI workflow failures

- **Asked:** `Search GitHub repositories issues pull requests workflows actions code`
- **Needed:** `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_THE_COMBINED_STATUS_FOR_A_SPECIFIC_REFERENCE`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
- **Got:** primary: GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
  related: GITHUB_FIND_PULL_REQUESTS, GITHUB_LIST_REPOSITORY_ISSUES, GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_AN_ISSUE, GITHUB_LIST_PULL_REQUESTS_FILES, GITHUB_LIST_ISSUE_COMMENTS
- **What went wrong:** The query is a broad list of keywords related to GitHub rather than a specific description of downloading logs for a workflow job. [1/3 votes]

#### Task 30 — Retrieve social page activity or posts

- **Asked:** `Fetch social media page activity or posts`
- **Needed:** `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`
- **Got:** primary: LINKEDIN_GET_POST_CONTENT, LINKEDIN_LIST_REACTIONS
  related: LINKEDIN_GET_SHARE_STATS, LINKEDIN_GET_COMPANY_INFO, LINKEDIN_GET_ORG_PAGE_STATS, LINKEDIN_GET_NETWORK_SIZE
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned LinkedIn tools fetch post content and reactions, which performs essentially the same kind of social media page activity and post retrieval work described by the query, just on a different platform.

#### Task 31 — Create and manage tasks or reminders

- **Asked:** `Create reminder or task`
- **Needed:** `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`
- **Got:** primary: NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_INSERT_ROW_DATABASE
  related: NOTION_UPSERT_ROW_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_LIST_USERS, NOTION_INSERT_ROW_FROM_NL, NOTION_FETCH_ROW
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Notion tools allow creating and organizing tasks or database entries, which performs essentially the same task-management function as creating a reminder.

#### Task 39 — List and retrieve lead details, history, notes, and contacts from Kommo CRM

- **Asked:** `extract CRM leads to spreadsheet reporting workbook`
- **Needed:** `KOMMO_GET_LEAD`, `KOMMO_LIST_CONTACTS`, `KOMMO_LIST_EVENTS`, `KOMMO_LIST_LEADS`, `KOMMO_LIST_NOTES_BY_ENTITY`
- **Got:** primary: GOOGLESHEETS_SEARCH_SPREADSHEETS, GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_VALUES_GET, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS, GOOGLESHEETS_UPSERT_ROWS
  related: GMAIL_FETCH_EMAILS, GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_DOWNLOAD_FILE, GOOGLESHEETS_BATCH_GET, GOOGLECALENDAR_FIND_EVENT
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Google Sheets tools handle the spreadsheet reporting and data extraction requested by the query, serving the same functional purpose as the CRM lead export tool.

#### Task 41 — Commit code changes to a GitHub repository

- **Asked:** `commit changes and merge pull request in GitHub`
- **Needed:** `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_GET_REPOSITORY_CONTENT`
- **Got:** primary: GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD
  related: GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_COMMIT_STATUSES, TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD
- **What went wrong:** The query asks to merge a pull request, whereas the target tool is specifically for committing multiple files atomically. [0/3 votes]

#### Task 51 — Fetch and annotate support-thread evidence

- **Asked:** `fetch support thread messages and notes or annotations in customer support tool`
- **Needed:** `PLAIN_RUN_GRAPHQL_QUERY`
- **Got:** primary: HELPWISE_GET_CONVERSATION, ZENDESK_GET_ZENDESK_TICKET_BY_ID, FRESHDESK_LIST_ALL_TICKET_CONVERSATIONS
  related: HELPWISE_GET_NOTES, HELPWISE_GET_ATTACHMENTS, ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_UPDATE_ZENDESK_TICKET, FRESHDESK_VIEW_TICKET
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned tools retrieve support tickets, conversations, and messages from alternative customer support platforms like Helpwise, Zendesk, and Freshdesk, performing the exact same kind of work as the expected Plain GraphQL query.

#### Task 52 — Retrieve memory data from Mem0

- **Asked:** `Migrate memory data from Mem0 into Zep`
- **Needed:** `MEM0_GET_MEMORIES_BY_ENTITY`
- **Got:** primary: MEM0_EXPORT_DATA_BASED_ON_FILTERS, ZEP_ADD_SESSION_MEMORY
  related: ZEP_CREATE_SESSION, ZEP_GET_SESSION_MEMORY
- **What went wrong:** The query asks to migrate data into Zep, whereas the tool is specifically for retrieving memories from Mem0 by entity. [0/3 votes]

#### Task 52 — Inspect existing Zep context, user nodes, and graph structure

- **Asked:** `Inspect existing Zep context or get user sessions and memory`
- **Needed:** `ZEP_GET_USER_NODE`
- **Got:** primary: ZEP_GET_THREAD_USER_CONTEXT, ZEP_GET_SESSION_MEMORY, ZEP_GET_USER_SESSIONS
  related: ZEP_ADD_THREAD_MESSAGES, ZEP_CREATE_THREAD, ZEP_GET_THREAD_MESSAGES, ZEP_ADD_SESSION_MEMORY, ZEP_GET_SESSION
- **What went wrong:** search answered the query as written -- None does what it asked; the step needed something else. The search results successfully returned tools covering both inspecting existing Zep context and getting user sessions and memory.

#### Task 55 — Write, update, and manage values across multiple cell ranges

- **Asked:** `Google Sheets update spreadsheet formatting formulas data validation`
- **Needed:** `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`
- **Got:** primary: GOOGLESHEETS_SET_DATA_VALIDATION_RULE, GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES
  related: GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_GET_DATA_VALIDATION_RULES, GOOGLESHEETS_GET_CONDITIONAL_FORMAT_RULES, GOOGLESHEETS_FORMAT_CELL, GOOGLESHEETS_VALUES_UPDATE, GOOGLESHEETS_BATCH_GET
- **What went wrong:** search answered the query as written -- GOOGLESHEETS_BATCH_GET does what it asked; the step needed something else. The returned results cover updating spreadsheets, formatting, formulas (via values update/batch), and data validation.

#### Task 60 — Enrich contact data and find email addresses

- **Asked:** `instantly verify email or enrich contact`
- **Needed:** `HUNTER_DOMAIN_SEARCH`, `HUNTER_EMAIL_FINDER`
- **Got:** primary: INSTANTLY_CREATE_SUPERSEARCH_ENRICHMENT, INSTANTLY_SUPERSEARCH_ENRICHMENT_RUN_POST
  related: INSTANTLY_CREATE_LEAD_LIST, INSTANTLY_LIST_LEAD_LISTS, INSTANTLY_GET_LEAD_LIST, INSTANTLY_COUNT_LEADS_FROM_SUPERSEARCH, INSTANTLY_PATCH_SUPERSEARCH_ENRICHMENT_SETTINGS, INSTANTLY_GET_SUPERSEARCH_ENRICHMENT
- **What went wrong:** query names instantly but the step needs hunter

#### Task 64 — Gather marketing performance data from advertising platforms

- **Asked:** `get marketing performance data`
- **Needed:** `GOOGLEADS_SEARCH_STREAM_GAQL`
- **Got:** primary: METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS, LINKEDIN_ADS_GET_AD_ANALYTICS
  related: METAADS_LIST_BUSINESS_AD_ACCOUNTS, METAADS_LIST_CLIENT_AD_ACCOUNTS, METAADS_GET_OBJECT, METAADS_READ_ADSETS, METAADS_GET_USER, METAADS_LIST_ADS, LINKEDIN_ADS_SEARCH_CAMPAIGNS, LINKEDIN_ADS_GET_AD_ACCOUNT, LINKEDIN_ADS_SEARCH_AD_ACCOUNTS, LINKEDIN_ADS_GET_TARGETING_ENTITIES, LINKEDIN_ADS_GET_TARGETING_FACETS, LINKEDIN_ADS_SEARCH_CREATIVES
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned tools retrieve ad performance and analytics data from alternative marketing platforms, fulfilling the general request for marketing performance data just as the expected Google Ads tool would.

#### Task 64 — Gather web analytics and traffic performance data

- **Asked:** `search console query performance`
- **Needed:** `GOOGLE_ANALYTICS_RUN_REPORT`
- **Got:** primary: GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY
  related: GOOGLE_SEARCH_CONSOLE_GET_SITE, GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS, GOOGLE_SEARCH_CONSOLE_GET_SITEMAP, GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP, GOOGLE_SEARCH_CONSOLE_INSPECT_URL, GOOGLE_SEARCH_CONSOLE_ADD_SITE
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Search Console tools directly address the query's request for search performance data, serving the same functional purpose as the expected Analytics tool.

#### Task 70 — Trigger and monitor GitHub Actions deployments and workflows

- **Asked:** `trigger deploy Vercel deployment`
- **Needed:** `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
- **Got:** primary: VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT
  related: VERCEL_GET_TEAMS, VERCEL_GET_PROJECT2, VERCEL_SEARCH_REPO, GITHUB_GET_A_REPOSITORY, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_DEPLOYMENT_LOGS2
- **What went wrong:** query names vercel but the step needs github

#### Task 80 — Audit Trello board access and members for assignee lookup

- **Asked:** `Create Trello card attachment member`
- **Needed:** `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`
- **Got:** primary: TRELLO_ADD_CARDS, TRELLO_ADD_CARDS_ATTACHMENTS_BY_ID_CARD
  related: TRELLO_GET_CARDS_BY_ID_CARD, TRELLO_UPDATE_CARDS_BY_ID_CARD, TRELLO_GET_SEARCH, TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD
- **What went wrong:** The query asks to create a Trello card attachment member, whereas the tool retrieves board memberships and user roles. [0/3 votes]

#### Task 85 — Merge branches after approval

- **Asked:** `merge a pull request on GitHub`
- **Needed:** `GITHUB_MERGE_A_BRANCH`
- **Got:** primary: GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD
  related: GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_COMMIT_STATUSES, TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD
- **What went wrong:** search answered the query as written -- GITHUB_MERGE_A_PULL_REQUEST does what it asked; the step needed something else. The search results include a direct match for merging a pull request on GitHub.

### No tool exists for it (18)

Nothing in the catalogue does this, so nobody could have found it.

| Task | Capability with no tool behind it |
|---|---|
| 1 | Assess payment link feasibility |
| 1 | Verify assets remain inert |
| 3 | Programmatically process and modify the spreadsheet workbook |
| 8 | Mark incomplete archive documents when transcript retrieval fails |
| 11 | Check queue and system state files |
| 12 | Perform broader automation-maintenance operations |
| 20 | Manage and reconcile files in Google Drive |
| 29 | Notify collaborators |
| 43 | Verify or trigger recalculation of spreadsheet formulas |
| 58 | Validate the changes |
| 58 | Commit and push changes to the default branch |
| 67 | Consolidate or merge duplicate contact data |
| 69 | Retrieve backlink and link-equity signals for the target domain |
| 77 | Research targeting and keyword opportunities for the campaign |
| 77 | Build and verify the new search campaign including budget, targeting, keywords, ads, and assets |
| 89 | Inspect meeting-booking setup and configuration |
| 94 | Modify ad set targeting, pause objects, create custom audiences, and add exclusions |
| 94 | Retrieve pixel data |

---

## How much to trust these numbers

**Safe to quote as-is.** These come from set membership, with no judgement involved:

- 83 delivered only in `related`
- 28 never searched for by the agent
- 18 capabilities with no tool behind them

**Quote with the case list attached.** Splitting the rest between *the query was too vague* and *search should have found it* is a reading of the evidence, not a measurement. It was revised five times while this analysis was built — 19 to 11 to 5 to 1 to 2 to 4 — moving in both directions as each rule was corrected. Two corrections came from cases spotted by hand: search was being blamed for not returning Cloudflare tools to a query about Vercel, and Sheets tools to a query about calendar events. A later over-correction then excused a genuine GitHub miss.

Of the 4 recall failures, **1** rests on deterministic evidence — Composio's own `readOnlyHint` tags proving nothing returned could perform the change the query asked for. The others rest on LLM votes and are individually arguable.

**How each verdict was reached.** Deterministic checks run first, from Composio's own toolkit and read-only metadata: a query naming one application cannot be blamed for not returning another's tools, and a query asking to create something cannot be satisfied by read-only results. Only what those cannot settle goes to an LLM, asked a concrete question about a named tool and answered by a majority of three votes.

