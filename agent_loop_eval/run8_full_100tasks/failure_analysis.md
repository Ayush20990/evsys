# Failure analysis — `run8_full_100tasks`

74 capabilities went unmet out of 433 required (17%), after the judge credited valid alternatives.

## Failures by cause

| Cause | Count | What it means | Who fixes it |
|---|---:|---|---|
| `never-returned` | 56 | no expected tool appeared in any search result | search recall |
| `catalogue-gap` | 18 | the task needs a capability no logged tool provides | product/catalogue, not search |

## Delivered, but not recommended

83 capabilities were satisfied ONLY by a tool in `related` — search held the
right tool and never promoted it. An agent acting on the primary recommendation would
have missed these, so in practice they sit between a hit and a miss.

| Task | Capability | Found only in `related` |
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

## Every unmet capability

### Task 1
> Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th

- **Assess payment link feasibility** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: No available tool assesses the feasibility of a payment link in HubSpot.
- **Verify assets remain inert** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the capability to verify that HubSpot assets remain inert.

### Task 2
> Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.

- **Verify Notion content after writing** — `never-returned`
  - expected: `NOTION_GET_PAGE_MARKDOWN`, `NOTION_RETRIEVE_PAGE`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Notion tools provide a specific capability to retrieve and verify the page markdown or full page content after writing.

### Task 3
> Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.

- **Programmatically process and modify the spreadsheet workbook** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned OneDrive tools provide the capability to programmatically process and modify the contents of a spreadsheet workbook.

### Task 7
> Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.

- **Fetch and read email messages and threads** — `never-returned`
  - expected: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Gmail tools provide the capability to fetch and read email messages and threads.

### Task 8
> Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.

- **Mark incomplete archive documents when transcript retrieval fails** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the capability to mark or update incomplete archive documents when transcript retrieval fails.

### Task 9
> Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.

- **Search or source stock images for marketing assets** — `never-returned`
  - expected: `COMPOSIO_SEARCH_IMAGE`
  - no expected tool appeared anywhere in any search result
  - judge: Although GEMINI_GENERATE_IMAGE can create images from text prompts, no provided tool offers the specific capability to search or source existing stock images from a stock media library.

### Task 11
> Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure

- **Check queue and system state files** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the specific capability to check queue and system state files as required by the operations knowledge base task.

### Task 12
> Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.

- **Fetch and search Gmail emails for project management** — `never-returned`
  - expected: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Gmail tools provide the ability to fetch and search emails, as the available tools only cover sending, drafting, replying, managing aliases, and searching contacts.
- **Search and list Slack messages and users for chat integration** — `never-returned`
  - expected: `SLACK_SEARCH_MESSAGES`, `SLACK_LIST_ALL_USERS`
  - no expected tool appeared anywhere in any search result
  - judge: The available tools are for ClickUp chat channels, whereas the missing capability specifically requires Slack message and user search integration.
- **Perform broader automation-maintenance operations** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide capabilities for broader automation-maintenance operations.

### Task 13
> Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.

- **Audit website search performance and indexing** — `never-returned`
  - expected: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITE`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`
  - no expected tool appeared anywhere in any search result
  - judge: The returned tools only provide Google Analytics (GA4) and Gmail functionalities, but none of them support auditing website search performance and indexing like Google Search Console.
- **Prepare and manage email marketing or contact lists** — `never-returned`
  - expected: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to create and manage email marketing lists or contact lists.

### Task 16
> Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host

- **Modify repository code and create pull requests** — `never-returned`
  - expected: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to modify repository code or create pull requests; the available tools only retrieve references and search issues or pull requests.
- **Investigate hosting and deployment state via DNS/CDN configuration** — `never-returned`
  - expected: `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Vercel or GitHub tools provide the ability to inspect DNS or CDN configuration for hosting and deployment state.

### Task 17
> Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.

- **Attempt social media publishing on Instagram** — `never-returned`
  - expected: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the specific capability to publish social media posts to Instagram.
- **Read and update the booking schedule** — `never-returned`
  - expected: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - no expected tool appeared anywhere in any search result
  - judge: The available tools only cover Google Calendar management rather than the required Google Sheets booking schedule read and update capabilities.

### Task 18
> Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.

- **Search and extract recent job listings from web sources or job boards** — `never-returned`
  - expected: `BROWSER_TOOL_CREATE_TASK`
  - no expected tool appeared anywhere in any search result
  - judge: None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

### Task 19
> Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.

- **Fetch and read content from web pages or job postings** — `never-returned`
  - expected: `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to fetch and read the full content of arbitrary web pages or specific job postings from URLs.

### Task 20
> Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records

- **Manage and reconcile files in Google Drive** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: Although there are tools for finding, getting metadata, and downloading files in Google Drive, there are no tools provided to manage (such as create, update, move, or delete) and reconcile files in Google Drive.

### Task 22
> The user was managing unread email triage and urgent alerts, looking up CRM-style trial records, inspecting and modifying source code in GitHub, opening or merging branches, and checking CI workflow f

- **look up CRM-style trial records** — `never-returned`
  - expected: `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools support Airtable or Pipedrive CRM trial records, as the available CRM tools are exclusively for Salesforce.
- **inspect and modify source code in GitHub, and handle branches** — `never-returned`
  - expected: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_MERGE_A_BRANCH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to inspect source code, modify files, create branches, or merge pull requests.
- **check CI workflow failures** — `never-returned`
  - expected: `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_THE_COMBINED_STATUS_FOR_A_SPECIFIC_REFERENCE`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to check or download CI workflow run failures.

### Task 27
> Verify Google Drive access, inspect folders, copy a nested folder/file structure from one Drive account or folder area to another, and share the destination with collaborators.

- **Create a new folder in Google Drive** — `never-returned`
  - expected: `GOOGLEDRIVE_CREATE_FOLDER`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Drive tools provide the capability to create a new folder.

### Task 28
> Analyze recent Instagram Reel performance, generate a new short-form branded video with AI video and voice tools, publish it as an Instagram Reel, verify the post, and attempt to archive the final ass

- **Generate AI text-to-speech audio for the video voiceover** — `never-returned`
  - expected: `ELEVENLABS_TEXT_TO_SPEECH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide text-to-speech audio generation capabilities.

### Task 29
> Automate a complex growth and content operations workflow: publish scheduled social content across multiple platforms, notify collaborators, update tracking spreadsheets, log lead and outreach activit

- **Notify collaborators** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide a direct capability for notifying collaborators, as the available tools are focused on social media posting, Fathom meetings, Gmail, Google Docs/Drive/Sheets, and LinkedIn.

### Task 30
> Generate recurring daily activity summaries by collecting recent email activity, social page activity, and Fireflies meeting transcripts for a local-day reporting window.

- **Retrieve social page activity or posts** — `never-returned`
  - expected: `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned LinkedIn or other tools provide a capability to retrieve social page activity or posts directly, only statistics, network size, company info, and reactions.

### Task 31
> Monitor and inspect Outlook email messages, summarize or verify their contents, sometimes process attachments or market data, create reminders/tasks, and attempt to send concise notifications through 

- **Retrieve real-time market data and financial information** — `never-returned`
  - expected: `COMPOSIO_SEARCH_FINANCE`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to retrieve real-time market data and financial information.
- **Create and manage tasks or reminders** — `never-returned`
  - expected: `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to create and manage TickTick tasks or reminders.

### Task 32
> The session covered multiple unrelated workflows: public web research, financial-product research, real-estate listing checks, browser QA for a web prototype, attempted Discord role updates, GitHub re

- **Public web research and content extraction** — `never-returned`
  - expected: `COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide public web research or content extraction capabilities, as they are exclusively related to Google Drive and Salesforce operations.
- **Browser automation and QA for web applications** — `never-returned`
  - expected: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide browser automation or QA capabilities for web applications, as they are entirely focused on Google Drive and Salesforce integrations.
- **Retail product and catalog search** — `never-returned`
  - expected: `COMPOSIO_SEARCH_SHOPPING`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide retail product or catalog search capabilities, as they are exclusively related to Google Drive and Salesforce.
- **Fast LLM inference and content generation** — `never-returned`
  - expected: `COMPOSIO_SEARCH_GROQ_CHAT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Drive or Salesforce tools provide fast LLM inference and content generation capabilities.

### Task 33
> Analyze WhatsApp-style broadcast campaigns in Kommo CRM, including detected campaign sends, audience reach, replies, conversions, templates, segments, and related agent activity.

- **List leads to analyze conversions and campaign outcomes** — `never-returned`
  - expected: `KOMMO_LIST_LEADS`
  - no expected tool appeared anywhere in any search result
  - judge: Although KOMMO_GET_LEAD is available, there is no tool returned in the session that provides the capability to list leads (`KOMMO_LIST_LEADS`) in Kommo CRM.

### Task 39
> Audit and reconcile CRM lead activity into a spreadsheet-based reporting workbook, including lead extraction, source classification, social-seller separation, outcome tracking, summary updates, and fi

- **List and retrieve lead details, history, notes, and contacts from Kommo CRM** — `never-returned`
  - expected: `KOMMO_GET_LEAD`, `KOMMO_LIST_CONTACTS`, `KOMMO_LIST_EVENTS`, `KOMMO_LIST_LEADS`, `KOMMO_LIST_NOTES_BY_ENTITY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools interact with Kommo CRM to list or retrieve lead details, history, notes, or contacts.

### Task 41
> Implement and release a protected budget dashboard feature by reading Google Sheets and Google Docs data, retrieving deployment secrets from Vercel, committing and merging code changes, verifying depl

- **Commit code changes to a GitHub repository** — `never-returned`
  - expected: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_GET_REPOSITORY_CONTENT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to commit code changes to a repository.

### Task 43
> Read an existing Google spreadsheet, preserve formulas and current values, add and populate new tabs with formulas and supporting details, verify recalculation, and organize related Google Drive docum

- **Verify or trigger recalculation of spreadsheet formulas** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the ability to verify or trigger a recalculation of spreadsheet formulas.

### Task 46
> Create, update, query, and verify Notion database rows and page content for generic deal-room style pages, including owner lookup, bulk content replacement, child-page preservation, and database filte

- **Lookup workspace users for owner assignment** — `never-returned`
  - expected: `NOTION_LIST_USERS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Notion tools provide the capability to list or lookup workspace users for owner assignment.

### Task 51
> Fetch and annotate support-thread evidence, retrieve attachment download links, and later verify an Instagram DM tool fix using Instagram reads/sends plus Metabase, Datadog, and spreadsheet evidence.

- **Fetch and annotate support-thread evidence** — `never-returned`
  - expected: `PLAIN_RUN_GRAPHQL_QUERY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the required Plain GraphQL query capability to fetch and annotate support-thread evidence.

### Task 52
> Migrate a user's memory data from Mem0 into Zep, inspect existing Zep context, attempt to organize migrated content by project-like scopes, and verify that the imported content is searchable.

- **Retrieve memory data from Mem0** — `never-returned`
  - expected: `MEM0_GET_MEMORIES_BY_ENTITY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Mem0 tools provide the capability to retrieve individual memories by entity, as only an export job creation tool was provided.
- **Inspect existing Zep context, user nodes, and graph structure** — `never-returned`
  - expected: `ZEP_GET_USER_NODE`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Zep tools provide the capability to directly inspect existing user nodes and graph structure as specified by the missing ZEP_GET_USER_NODE capability.

### Task 53
> Audit a short-link inventory by finding an existing spreadsheet registry, reading help-center mapping tabs, listing existing short links, and attempting to compare them with live public website articl

- **List and retrieve existing short links from a short-link management platform** — `never-returned`
  - expected: `TINYURL_LIST_URLS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to list and retrieve existing short links from a short-link management platform like TinyURL.

### Task 54
> Audit advertising account health and performance, probe analytics property access, create and verify a new Google Ads search campaign with budget, targeting, ad group, keywords, and responsive search 

- **Create and manage campaign budgets in Google Ads** — `never-returned`
  - expected: `GOOGLEADS_MUTATE_CAMPAIGN_BUDGETS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Ads tools provide the capability to create and manage campaign budgets.
- **Configure campaign-level targeting criteria** — `never-returned`
  - expected: `GOOGLEADS_MUTATE_CAMPAIGN_CRITERIA`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Ads tools provide the capability to configure campaign-level targeting criteria.
- **Add keywords and targeting criteria to ad groups** — `never-returned`
  - expected: `GOOGLEADS_MUTATE_AD_GROUP_CRITERIA`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Ads tools provide the capability to add keywords and targeting criteria to ad groups.
- **Create and manage ads including responsive search ads** — `never-returned`
  - expected: `GOOGLEADS_MUTATE_AD_GROUP_ADS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Ads tools provide the capability to create and manage ads, such as responsive search ads.

### Task 55
> Automate and refine a complex Google Sheets financial/workforce model: apply formatting, dropdown validation, filters, formulas, instructional text, payroll-style calculations, and employee allocation

- **Write, update, and manage values across multiple cell ranges** — `never-returned`
  - expected: `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`
  - no expected tool appeared anywhere in any search result
  - judge: While GOOGLESHEETS_VALUES_UPDATE handles a single range, there is no tool returned that manages values across multiple cell ranges simultaneously as required by the batch update capability.
- **Apply filters and sort options to data ranges** — `never-returned`
  - expected: `GOOGLESHEETS_SET_BASIC_FILTER`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to apply filters or sort options to data ranges.
- **Modify worksheet properties and metadata** — `never-returned`
  - expected: `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to modify worksheet properties and metadata.

### Task 58
> Inspect and modify a GitHub repository frontend, validate the changes if possible, then commit and push the changes directly to the default branch.

- **Validate the changes** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the capability to validate the frontend code changes locally or execute build/test checks.
- **Commit and push changes to the default branch** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the ability to commit and push changes directly to the default branch (only creating pull requests, updating files, or committing multiple files via API without an explicit push mechanism).

### Task 60
> Manage lead data in Google Sheets: read existing tabs, append and correct lead rows, enrich contacts, detect duplicate email addresses, highlight duplicate rows, and attempt to prepare leads for impor

- **Enrich contact data and find email addresses** — `never-returned`
  - expected: `HUNTER_DOMAIN_SEARCH`, `HUNTER_EMAIL_FINDER`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the specific capability to enrich contact data and find email addresses using Hunter tools (such as HUNTER_DOMAIN_SEARCH or HUNTER_EMAIL_FINDER).

### Task 64
> Prepare marketing and CRM automation work: gather marketing performance data, send a brief by email, analyze search query data, and scaffold a HubSpot customer follow-up campaign with custom propertie

- **Gather marketing performance data from advertising platforms** — `never-returned`
  - expected: `GOOGLEADS_SEARCH_STREAM_GAQL`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the ability to gather marketing performance data from advertising platforms like Google Ads.
- **Gather web analytics and traffic performance data** — `never-returned`
  - expected: `GOOGLE_ANALYTICS_RUN_REPORT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide Google Analytics website traffic and web analytics performance reporting.

### Task 67
> Manage Salesforce opportunity pipeline data: list open opportunities, update opportunity stages and required fields, verify record changes, consolidate duplicate contact data, and create a follow-up t

- **Consolidate or merge duplicate contact data** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned Salesforce tools provide the capability to consolidate or merge duplicate contact data.

### Task 68
> Modify a GitHub-hosted backend application, add protected console and lead-care functionality, configure deployment/runtime infrastructure, apply database migrations, and verify CI plus hosted deploym

- **Verify CI check runs and workflow status** — `never-returned`
  - expected: `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to list check runs or workflow run statuses for a reference or repository.
- **Apply database migrations via SQL execution** — `never-returned`
  - expected: `SUPABASE_BETA_RUN_SQL_QUERY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to execute SQL queries or apply database migrations.
- **Check hosted deployment status and logs on Vercel** — `never-returned`
  - expected: `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_DEPLOYMENT_LOGS2`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to check hosted deployment status and logs on Vercel.

### Task 69
> Perform a technical SEO audit around sitemap migration, indexability, linked-page health, and backlink/link-equity signals using Google Search Console and supporting crawl data.

- **Scrape and crawl web pages to gather linked-page health and technical crawl data** — `never-returned`
  - expected: `FIRECRAWL_SCRAPE`
  - no expected tool appeared anywhere in any search result
  - judge: The returned tools only manage and inspect Google Search Console properties and sitemaps, and none of them provide the capability to scrape and crawl web pages for linked-page health and technical crawl data.
- **Retrieve backlink and link-equity signals for the target domain** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the ability to retrieve backlink and link-equity signals for the target domain.

### Task 70
> Migrate Vercel projects and GitHub repositories between connected accounts, preserve domains and settings, add deployment workflows, trigger/verify deployments, and audit repository access.

- **Trigger and monitor GitHub Actions deployments and workflows** — `never-returned`
  - expected: `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub tools provide the ability to trigger workflow dispatch events or list workflow runs for a repository.

### Task 72
> Build, repair, deploy, configure, and test a Vercel-hosted GitHub-backed API proxy for Gemini text, image, video, embeddings, model listing, OpenAI-compatible paths, and tool-call-style outputs.

- **Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models** — `never-returned`
  - expected: `GEMINI_GENERATE_CONTENT`, `GEMINI_LIST_MODELS`, `GEMINI_COUNT_TOKENS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide capabilities for interacting with Gemini models, such as generating text, counting tokens, or listing models.
- **Generate images using Gemini image models** — `never-returned`
  - expected: `GEMINI_GENERATE_IMAGE`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to generate images using Gemini image models.
- **Generate and poll/wait for videos using Google Veo models** — `never-returned`
  - expected: `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate and poll or wait for videos using Google Veo models.
- **Generate text embeddings using Gemini models** — `never-returned`
  - expected: `GEMINI_EMBED_CONTENT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate text embeddings using Gemini models.
- **Configure project environment variables on Vercel** — `never-returned`
  - expected: `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Vercel tools provide the capability to add or configure environment variables on a Vercel project.

### Task 73
> Manage a large operational workflow across Google Tasks, Xero, and Notion: update and move task records, create and revise invoices, record payments, consolidate Notion rules, and track operational fo

- **Get current date and time** — `never-returned`
  - expected: `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to get the current date and time.

### Task 77
> Audit a Google Ads client account under a manager account, research targeting and keywords, then build and verify a new search campaign with budget, targeting, keywords, ads, and assets.

- **Research targeting and keyword opportunities for the campaign** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned Google Ads tools provide keyword or targeting research capabilities such as generating keyword ideas or analyzing search volume.
- **Build and verify the new search campaign including budget, targeting, keywords, ads, and assets** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: While there are individual tools to mutate campaigns and ad groups, no single tool or complete set provided covers the full requirement to build and verify a new search campaign including budget, targeting, keywords, ads, and assets end-to-end.

### Task 80
> Audit Meta Ads account access, inspect performance for a specific ad set, identify improvement actions, then create a Trello card with an attached report and assignee; also attempt to clean up a fault

- **Audit Trello board access and members for assignee lookup** — `never-returned`
  - expected: `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Trello tools provide the specific capability to audit board access and list board members for assignee lookup.

### Task 85
> Investigate and patch a codebase hosted on GitHub, commit changes to a target branch, document the change, and merge that branch into the destination branch after approval.

- **Merge branches after approval** — `never-returned`
  - expected: `GITHUB_MERGE_A_BRANCH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to directly merge branches (such as GITHUB_MERGE_A_BRANCH), as the available merge tool only merges pull requests.

### Task 89
> Audit inbound email and HubSpot marketing/automation assets to understand an external funnel, compare it with existing marketing emails and workflows, and inspect meeting-booking setup.

- **Inspect meeting-booking setup and configuration** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned HubSpot or Gmail tools provide the capability to inspect or retrieve meeting-booking configuration and scheduling setup.

### Task 94
> Audit and optimize a Meta Ads account: retrieve account, campaign, ad set, ad, creative, performance, targeting, and pixel data; then apply confirmed optimization changes including pausing objects, ch

- **Modify ad set targeting, pause objects, create custom audiences, and add exclusions** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: While some tools are provided for Meta Ads, there is no tool available to modify existing ad set targeting, add exclusions, or pause individual ads/ad sets (only campaigns can be paused).
- **Retrieve pixel data** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned Meta Ads tools provide the capability to retrieve pixel data.

