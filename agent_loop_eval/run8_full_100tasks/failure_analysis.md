# Failure analysis — `run8_full_100tasks`

74 of 433 required capabilities went unmet after the judge credited
valid alternatives, plus 83 delivered but never recommended.

Every failure below is attributed: which query was meant to find the tool, what search
returned for it, and whether the query was good enough that search should have found it.

## Where the fault lies

| Fault | Count | Meaning |
|---|---:|---|
| agent: never searched for it | 28 | the agent never searched for this capability at all |
| search: fair query, tool not returned | 19 | the agent asked a fair question and search did not return the tool |
| catalogue: no tool provides this | 18 | no tool in the catalogue provides this |
| agent: query too vague to find it | 9 | the agent searched, but too vaguely for any engine to resolve |
| search: returned it, but only in related (from met groups) | 83 | delivered only in `related`, never promoted |

**Agent-side: 37. Search-side: 102. Catalogue: 18.**

Agent-side failures are fixable by better decomposition or phrasing and say nothing
about retrieval quality. Search-side failures are the ones that belong in a report on
the search tool.

## Delivered, but never recommended

83 capabilities were satisfied only by a tool in `related`. An agent acting
on the primary recommendation would have missed every one.

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

## Every unmet capability, with its query

### Task 1

> Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify the assets remain iner

**Assess payment link feasibility**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: No available tool assesses the feasibility of a payment link in HubSpot.

**Verify assets remain inert**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the capability to verify that HubSpot assets remain inert.

### Task 2

> Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.

**Verify Notion content after writing**

- needed: `NOTION_GET_PAGE_MARKDOWN`, `NOTION_RETRIEVE_PAGE`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent did not issue any search query aimed at verifying the Notion content after writing.
- judge: None of the returned Notion tools provide a specific capability to retrieve and verify the page markdown or full page content after writing.

### Task 3

> Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.

**Programmatically process and modify the spreadsheet workbook**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned OneDrive tools provide the capability to programmatically process and modify the contents of a spreadsheet workbook.

### Task 7

> Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.

**Fetch and read email messages and threads**

- needed: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a search query aimed at finding a tool to fetch and read email messages and threads.
- judge: None of the returned Gmail tools provide the capability to fetch and read email messages and threads.

### Task 8

> Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.

**Mark incomplete archive documents when transcript retrieval fails**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the capability to mark or update incomplete archive documents when transcript retrieval fails.

### Task 9

> Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.

**Search or source stock images for marketing assets**

- needed: `COMPOSIO_SEARCH_IMAGE`
- **fault: agent: query too vague to find it**
- query the agent issued (#1): `Create multimedia travel marketing assets from scripts and stock media`
- search returned:
```
  primary: GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE, HEYGEN_V2_VIDEO_GENERATE
  related: GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GET_VIDEOS_OPERATION, HEYGEN_V2_TEMPLATES, HEYGEN_V2_TEMPLATE_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS
```
- why: The query asks for video creation and generation from scripts and stock media, whereas the target capability is specifically about searching or sourcing stock images.
- judge: Although GEMINI_GENERATE_IMAGE can create images from text prompts, no provided tool offers the specific capability to search or source existing stock images from a stock media library.

### Task 11

> Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure Gmail support label

**Check queue and system state files**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the specific capability to check queue and system state files as required by the operations knowledge base task.

### Task 12

> Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.

**Fetch and search Gmail emails for project management**

- needed: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a query to fetch or search Gmail emails for project management.
- judge: None of the returned Gmail tools provide the ability to fetch and search emails, as the available tools only cover sending, drafting, replying, managing aliases, and searching contacts.

**Search and list Slack messages and users for chat integration**

- needed: `SLACK_SEARCH_MESSAGES`, `SLACK_LIST_ALL_USERS`
- **fault: agent: query too vague to find it**
- query the agent issued (#5): `Send a chat message`
- search returned:
```
  primary: CLICKUP_CREATE_CHAT_MESSAGE
  related: CLICKUP_GET_CHAT_CHANNELS, CLICKUP_GET_CHAT_MESSAGES, CLICKUP_GET_SUBTYPES
```
- why: The query asks to send a chat message, whereas the required capability is to search and list Slack messages and users.
- judge: The available tools are for ClickUp chat channels, whereas the missing capability specifically requires Slack message and user search integration.

**Perform broader automation-maintenance operations**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide capabilities for broader automation-maintenance operations.

### Task 13

> Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.

**Audit website search performance and indexing**

- needed: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITE`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`
- **fault: search: fair query, tool not returned**
- query the agent issued (#1): `Audit website search and traffic performance in analytics`
- search returned:
```
  primary: GOOGLESUPER_RUN_REPORT, GOOGLESUPER_BATCH_RUN_REPORTS
  related: GOOGLESUPER_LIST_PROPERTIES, GOOGLESUPER_CHECK_COMPATIBILITY, GOOGLESUPER_GET_METADATA, GOOGLE_ANALYTICS_RUN_REPORT, GOOGLE_ANALYTICS_BATCH_RUN_REPORTS
```
- why: The query explicitly asks for website search and traffic performance analysis in analytics, which directly maps to the capability of auditing website search performance and indexing.
- judge: The returned tools only provide Google Analytics (GA4) and Gmail functionalities, but none of them support auditing website search performance and indexing like Google Search Console.

**Prepare and manage email marketing or contact lists**

- needed: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Search for contacts or create email lists in CRM or email marketing tool`
- search returned:
```
  primary: GMAIL_GET_CONTACTS, GMAIL_SEARCH_PEOPLE
  related: GMAIL_GET_PEOPLE, GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID
```
- why: The query explicitly asks for contact search and email list creation capabilities within a CRM or email marketing tool, which directly aligns with the required capability.
- judge: None of the returned tools provide the capability to create and manage email marketing lists or contact lists.

### Task 16

> Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate hosting/deployment state

**Modify repository code and create pull requests**

- needed: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Git repository file inspect and commit or pull request`
- search returned:
```
  primary: GITHUB_GET_A_REPOSITORY, GITHUB_GET_A_TREE, GITHUB_GET_REPOSITORY_CONTENT, GITHUB_LIST_COMMITS, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
  related: GITHUB_LIST_BRANCHES, GITHUB_GET_A_REFERENCE, GITHUB_GET_RAW_REPOSITORY_CONTENT, GITHUB_SEARCH_CODE
```
- why: The query explicitly asks for git repository file inspection, committing, and pull requests, which directly aligns with the required capability of modifying repository code and creating pull requests.
- judge: None of the returned GitHub tools provide the ability to modify repository code or create pull requests; the available tools only retrieve references and search issues or pull requests.

**Investigate hosting and deployment state via DNS/CDN configuration**

- needed: `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
- **fault: search: fair query, tool not returned**
- query the agent issued (#3): `Vercel Netlify Heroku deployment status inspect`
- search returned:
```
  primary: VERCEL_GET_DEPLOYMENTS, VERCEL_GET_DEPLOYMENT, VERCEL_GET_DEPLOYMENT_LOGS2
  related: VERCEL_GET_PROJECT2, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_PROJECTS, VERCEL_GET_DEPLOYMENT_EVENTS2
```
- why: The query specifically targets deployment status inspection across major hosting platforms like Vercel and Netlify, which is conceptually aligned with investigating hosting and deployment state.
- judge: None of the returned Vercel or GitHub tools provide the ability to inspect DNS or CDN configuration for hosting and deployment state.

### Task 17

> Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.

**Attempt social media publishing on Instagram**

- needed: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Publish video to social media platforms`
- search returned:
```
  primary: UPLOAD_POST_PUBLISH_POST, WOOP_SOCIAL_PUBLISH_POST_NOW
  related: UPLOAD_POST_LIST_PROFILES, UPLOAD_POST_GET_UPLOAD_STATUS, UPLOAD_POST_LIST_PLATFORM_DESTINATIONS, WOOP_SOCIAL_LIST_SOCIAL_ACCOUNTS, WOOP_SOCIAL_VALIDATE_POST
```
- why: The query asks for publishing video to social media platforms, which is a direct and appropriate description for finding tools that publish posts to Instagram and other social networks.
- judge: None of the returned tools provide the specific capability to publish social media posts to Instagram.

**Read and update the booking schedule**

- needed: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
- **fault: search: fair query, tool not returned**
- query the agent issued (#4): `Read and update bookings or calendar events`
- search returned:
```
  primary: GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_PATCH_EVENT, GOOGLECALENDAR_DELETE_EVENT, GOOGLECALENDAR_CREATE_EVENT
  related: GOOGLECALENDAR_EVENTS_LIST, GOOGLECALENDAR_EVENTS_GET, GOOGLECALENDAR_EVENTS_INSTANCES, GOOGLECALENDAR_BATCH_EVENTS, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS
```
- why: The query explicitly asks for reading and updating bookings and calendar events, which directly aligns with the required capability.
- judge: The available tools only cover Google Calendar management rather than the required Google Sheets booking schedule read and update capabilities.

### Task 18

> Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.

**Search and extract recent job listings from web sources or job boards**

- needed: `BROWSER_TOOL_CREATE_TASK`
- **fault: search: fair query, tool not returned**
- query the agent issued (#1): `Search job listings or job boards for remote hybrid contract data engineering jobs`
- search returned:
```
  primary: COMPOSIO_SEARCH_WEB
  related: COMPOSIO_SEARCH_FETCH_URL_CONTENT, COMPOSIO_SEARCH_NEWS, COMPOSIO_SEARCH_TRENDS, LINKEDIN_GET_POST_CONTENT
```
- why: The query explicitly asks to search job listings and job boards for specific data engineering roles, which directly targets the required capability of searching and extracting recent job listings.
- judge: None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

### Task 19

> Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.

**Fetch and read content from web pages or job postings**

- needed: `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target fetching or reading content from web pages or job postings.
- judge: None of the returned tools provide the capability to fetch and read the full content of arbitrary web pages or specific job postings from URLs.

### Task 20

> Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records.

**Manage and reconcile files in Google Drive**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: Although there are tools for finding, getting metadata, and downloading files in Google Drive, there are no tools provided to manage (such as create, update, move, or delete) and reconcile files in Google Drive.

### Task 22

> The user was managing unread email triage and urgent alerts, looking up CRM-style trial records, inspecting and modifying source code in GitHub, opening or merging branches, and checking CI workflow failures.

**look up CRM-style trial records**

- needed: `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Search CRM trial records or contacts`
- search returned:
```
  primary: SALESFORCE_LIST_CONTACTS, SALESFORCE_RUN_SOQL_QUERY
  related: SALESFORCE_QUERY, SALESFORCE_QUERY_ALL, SALESFORCE_GET_CONTACT
```
- why: The query explicitly asks to search CRM trial records and contacts, which clearly targets Salesforce contact and query tools for CRM data retrieval.
- judge: None of the returned tools support Airtable or Pipedrive CRM trial records, as the available CRM tools are exclusively for Salesforce.

**inspect and modify source code in GitHub, and handle branches**

- needed: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_MERGE_A_BRANCH`
- **fault: agent: query too vague to find it**
- query the agent issued (#3): `Search GitHub repositories issues pull requests workflows actions code`
- search returned:
```
  primary: GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
  related: GITHUB_FIND_PULL_REQUESTS, GITHUB_LIST_REPOSITORY_ISSUES, GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_AN_ISSUE, GITHUB_LIST_PULL_REQUESTS_FILES, GITHUB_LIST_ISSUE_COMMENTS
```
- why: The query asks for searching repositories, issues, pull requests, and workflows, but does not ask for tools to inspect, modify source code, or handle branches.
- judge: None of the returned GitHub tools provide the ability to inspect source code, modify files, create branches, or merge pull requests.

**check CI workflow failures**

- needed: `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_THE_COMBINED_STATUS_FOR_A_SPECIFIC_REFERENCE`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
- **fault: search: fair query, tool not returned**
- query the agent issued (#3): `Search GitHub repositories issues pull requests workflows actions code`
- search returned:
```
  primary: GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
  related: GITHUB_FIND_PULL_REQUESTS, GITHUB_LIST_REPOSITORY_ISSUES, GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_AN_ISSUE, GITHUB_LIST_PULL_REQUESTS_FILES, GITHUB_LIST_ISSUE_COMMENTS
```
- why: The query explicitly includes 'workflows' and 'actions', which directly target the capability of checking CI workflow failures, so a competent search engine should have been able to find the relevant tool.
- judge: None of the returned GitHub tools provide the ability to check or download CI workflow run failures.

### Task 27

> Verify Google Drive access, inspect folders, copy a nested folder/file structure from one Drive account or folder area to another, and share the destination with collaborators.

**Create a new folder in Google Drive**

- needed: `GOOGLEDRIVE_CREATE_FOLDER`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target the creation of a new folder in Google Drive.
- judge: None of the returned Google Drive tools provide the capability to create a new folder.

### Task 28

> Analyze recent Instagram Reel performance, generate a new short-form branded video with AI video and voice tools, publish it as an Instagram Reel, verify the post, and attempt to archive the final asset in a repository.

**Generate AI text-to-speech audio for the video voiceover**

- needed: `ELEVENLABS_TEXT_TO_SPEECH`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Generate AI video or text to speech voice`
- search returned:
```
  primary: GEMINI_GENERATE_VIDEOS
  related: GEMINI_GENERATE_IMAGE, GEMINI_WAIT_FOR_VIDEO, TRELLO_GET_CARDS_BY_ID_CARD
```
- why: The query explicitly asks for text-to-speech voice generation, which directly matches the required capability for creating AI voiceovers.
- judge: None of the returned tools provide text-to-speech audio generation capabilities.

### Task 29

> Automate a complex growth and content operations workflow: publish scheduled social content across multiple platforms, notify collaborators, update tracking spreadsheets, log lead and outreach activity, send Telegram rep

**Notify collaborators**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide a direct capability for notifying collaborators, as the available tools are focused on social media posting, Fathom meetings, Gmail, Google Docs/Drive/Sheets, and LinkedIn.

### Task 30

> Generate recurring daily activity summaries by collecting recent email activity, social page activity, and Fireflies meeting transcripts for a local-day reporting window.

**Retrieve social page activity or posts**

- needed: `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Fetch social media page activity or posts`
- search returned:
```
  primary: LINKEDIN_GET_POST_CONTENT, LINKEDIN_LIST_REACTIONS
  related: LINKEDIN_GET_SHARE_STATS, LINKEDIN_GET_COMPANY_INFO, LINKEDIN_GET_ORG_PAGE_STATS, LINKEDIN_GET_NETWORK_SIZE
```
- why: The query directly and accurately describes the required capability of fetching social media page activity and posts, leaving no ambiguity about the intended action.
- judge: None of the returned LinkedIn or other tools provide a capability to retrieve social page activity or posts directly, only statistics, network size, company info, and reactions.

### Task 31

> Monitor and inspect Outlook email messages, summarize or verify their contents, sometimes process attachments or market data, create reminders/tasks, and attempt to send concise notifications through WhatsApp or a Notis 

**Retrieve real-time market data and financial information**

- needed: `COMPOSIO_SEARCH_FINANCE`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries searched for real-time market data or financial information.
- judge: None of the returned tools provide the capability to retrieve real-time market data and financial information.

**Create and manage tasks or reminders**

- needed: `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`
- **fault: search: fair query, tool not returned**
- query the agent issued (#3): `Create reminder or task`
- search returned:
```
  primary: NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_INSERT_ROW_DATABASE
  related: NOTION_UPSERT_ROW_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_LIST_USERS, NOTION_INSERT_ROW_FROM_NL, NOTION_FETCH_ROW
```
- why: The query directly asks for the capability to create reminders or tasks, which clearly matches the required functionality.
- judge: None of the returned tools provide the capability to create and manage TickTick tasks or reminders.

### Task 32

> The session covered multiple unrelated workflows: public web research, financial-product research, real-estate listing checks, browser QA for a web prototype, attempted Discord role updates, GitHub repository inspection 

**Public web research and content extraction**

- needed: `COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: Neither of the issued queries targets public web research or content extraction, as they only search internal logs, session notes, and stored files.
- judge: None of the returned tools provide public web research or content extraction capabilities, as they are exclusively related to Google Drive and Salesforce operations.

**Browser automation and QA for web applications**

- needed: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: Neither of the issued queries targets browser automation or QA capabilities, as they only search for session notes, logs, files, and documents.
- judge: None of the returned tools provide browser automation or QA capabilities for web applications, as they are entirely focused on Google Drive and Salesforce integrations.

**Retail product and catalog search**

- needed: `COMPOSIO_SEARCH_SHOPPING`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target retail product and catalog search, as they only search through session notes, activity logs, and stored files.
- judge: None of the returned tools provide retail product or catalog search capabilities, as they are exclusively related to Google Drive and Salesforce.

**Fast LLM inference and content generation**

- needed: `COMPOSIO_SEARCH_GROQ_CHAT`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: Neither of the issued queries targets fast LLM inference or content generation capabilities.
- judge: None of the returned Google Drive or Salesforce tools provide fast LLM inference and content generation capabilities.

### Task 33

> Analyze WhatsApp-style broadcast campaigns in Kommo CRM, including detected campaign sends, audience reach, replies, conversions, templates, segments, and related agent activity.

**List leads to analyze conversions and campaign outcomes**

- needed: `KOMMO_LIST_LEADS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries specifically targeted listing leads to analyze conversions and campaign outcomes.
- judge: Although KOMMO_GET_LEAD is available, there is no tool returned in the session that provides the capability to list leads (`KOMMO_LIST_LEADS`) in Kommo CRM.

### Task 39

> Audit and reconcile CRM lead activity into a spreadsheet-based reporting workbook, including lead extraction, source classification, social-seller separation, outcome tracking, summary updates, and final verification.

**List and retrieve lead details, history, notes, and contacts from Kommo CRM**

- needed: `KOMMO_GET_LEAD`, `KOMMO_LIST_CONTACTS`, `KOMMO_LIST_EVENTS`, `KOMMO_LIST_LEADS`, `KOMMO_LIST_NOTES_BY_ENTITY`
- **fault: agent: query too vague to find it**
- query the agent issued (#1): `extract CRM leads to spreadsheet reporting workbook`
- search returned:
```
  primary: GOOGLESHEETS_SEARCH_SPREADSHEETS, GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_VALUES_GET, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS, GOOGLESHEETS_UPSERT_ROWS
  related: GMAIL_FETCH_EMAILS, GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_DOWNLOAD_FILE, GOOGLESHEETS_BATCH_GET, GOOGLECALENDAR_FIND_EVENT
```
- why: The query asks for Google Sheets spreadsheet reporting tools, whereas the capability requires listing and retrieving lead details from Kommo CRM.
- judge: None of the returned tools interact with Kommo CRM to list or retrieve lead details, history, notes, or contacts.

### Task 41

> Implement and release a protected budget dashboard feature by reading Google Sheets and Google Docs data, retrieving deployment secrets from Vercel, committing and merging code changes, verifying deployments, and updatin

**Commit code changes to a GitHub repository**

- needed: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_GET_REPOSITORY_CONTENT`
- **fault: agent: query too vague to find it**
- query the agent issued (#4): `commit changes and merge pull request in GitHub`
- search returned:
```
  primary: GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD
  related: GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_COMMIT_STATUSES, TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD
```
- why: The query asks for committing changes and merging a pull request, but committing code changes is a distinct capability from merging a pull request.
- judge: None of the returned GitHub tools provide the ability to commit code changes to a repository.

### Task 43

> Read an existing Google spreadsheet, preserve formulas and current values, add and populate new tabs with formulas and supporting details, verify recalculation, and organize related Google Drive documents.

**Verify or trigger recalculation of spreadsheet formulas**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the ability to verify or trigger a recalculation of spreadsheet formulas.

### Task 46

> Create, update, query, and verify Notion database rows and page content for generic deal-room style pages, including owner lookup, bulk content replacement, child-page preservation, and database filtering.

**Lookup workspace users for owner assignment**

- needed: `NOTION_LIST_USERS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target looking up workspace users for owner assignment; they focus on database rows, block contents, and clearing page content instead.
- judge: None of the returned Notion tools provide the capability to list or lookup workspace users for owner assignment.

### Task 51

> Fetch and annotate support-thread evidence, retrieve attachment download links, and later verify an Instagram DM tool fix using Instagram reads/sends plus Metabase, Datadog, and spreadsheet evidence.

**Fetch and annotate support-thread evidence**

- needed: `PLAIN_RUN_GRAPHQL_QUERY`
- **fault: search: fair query, tool not returned**
- query the agent issued (#1): `fetch support thread messages and notes or annotations in customer support tool`
- search returned:
```
  primary: HELPWISE_GET_CONVERSATION, ZENDESK_GET_ZENDESK_TICKET_BY_ID, FRESHDESK_LIST_ALL_TICKET_CONVERSATIONS
  related: HELPWISE_GET_NOTES, HELPWISE_GET_ATTACHMENTS, ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_UPDATE_ZENDESK_TICKET, FRESHDESK_VIEW_TICKET
```
- why: The query specifically asks to fetch support thread messages and notes in a customer support tool, which directly aligns with the capability to fetch and annotate support-thread evidence.
- judge: None of the returned tools provide the required Plain GraphQL query capability to fetch and annotate support-thread evidence.

### Task 52

> Migrate a user's memory data from Mem0 into Zep, inspect existing Zep context, attempt to organize migrated content by project-like scopes, and verify that the imported content is searchable.

**Retrieve memory data from Mem0**

- needed: `MEM0_GET_MEMORIES_BY_ENTITY`
- **fault: search: fair query, tool not returned**
- query the agent issued (#1): `Migrate memory data from Mem0 into Zep`
- search returned:
```
  primary: MEM0_EXPORT_DATA_BASED_ON_FILTERS, ZEP_ADD_SESSION_MEMORY
  related: ZEP_CREATE_SESSION, ZEP_GET_SESSION_MEMORY
```
- why: The query explicitly asks to migrate memory data from Mem0 into Zep, which directly encompasses the capability to retrieve memory data from Mem0 as part of the migration process.
- judge: None of the returned Mem0 tools provide the capability to retrieve individual memories by entity, as only an export job creation tool was provided.

**Inspect existing Zep context, user nodes, and graph structure**

- needed: `ZEP_GET_USER_NODE`
- **fault: search: fair query, tool not returned**
- query the agent issued (#2): `Inspect existing Zep context or get user sessions and memory`
- search returned:
```
  primary: ZEP_GET_THREAD_USER_CONTEXT, ZEP_GET_SESSION_MEMORY, ZEP_GET_USER_SESSIONS
  related: ZEP_ADD_THREAD_MESSAGES, ZEP_CREATE_THREAD, ZEP_GET_THREAD_MESSAGES, ZEP_ADD_SESSION_MEMORY, ZEP_GET_SESSION
```
- why: The query explicitly names Zep and asks to inspect context, sessions, and memory, which directly aligns with the required capability.
- judge: None of the returned Zep tools provide the capability to directly inspect existing user nodes and graph structure as specified by the missing ZEP_GET_USER_NODE capability.

### Task 53

> Audit a short-link inventory by finding an existing spreadsheet registry, reading help-center mapping tabs, listing existing short links, and attempting to compare them with live public website article URLs and redirects

**List and retrieve existing short links from a short-link management platform**

- needed: `TINYURL_LIST_URLS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target listing or retrieving existing short links from a short-link management platform.
- judge: None of the returned tools provide the capability to list and retrieve existing short links from a short-link management platform like TinyURL.

### Task 54

> Audit advertising account health and performance, probe analytics property access, create and verify a new Google Ads search campaign with budget, targeting, ad group, keywords, and responsive search ad, and later discov

**Create and manage campaign budgets in Google Ads**

- needed: `GOOGLEADS_MUTATE_CAMPAIGN_BUDGETS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a query to find a tool for creating and managing campaign budgets in Google Ads.
- judge: None of the returned Google Ads tools provide the capability to create and manage campaign budgets.

**Configure campaign-level targeting criteria**

- needed: `GOOGLEADS_MUTATE_CAMPAIGN_CRITERIA`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a search query aimed at configuring campaign-level targeting criteria.
- judge: None of the returned Google Ads tools provide the capability to configure campaign-level targeting criteria.

**Add keywords and targeting criteria to ad groups**

- needed: `GOOGLEADS_MUTATE_AD_GROUP_CRITERIA`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a query to find a tool for adding keywords and targeting criteria to ad groups.
- judge: None of the returned Google Ads tools provide the capability to add keywords and targeting criteria to ad groups.

**Create and manage ads including responsive search ads**

- needed: `GOOGLEADS_MUTATE_AD_GROUP_ADS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a query to find tools for creating and managing ads or responsive search ads.
- judge: None of the returned Google Ads tools provide the capability to create and manage ads, such as responsive search ads.

### Task 55

> Automate and refine a complex Google Sheets financial/workforce model: apply formatting, dropdown validation, filters, formulas, instructional text, payroll-style calculations, and employee allocation logic across multip

**Write, update, and manage values across multiple cell ranges**

- needed: `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`
- **fault: agent: query too vague to find it**
- query the agent issued (#1): `Google Sheets update spreadsheet formatting formulas data validation`
- search returned:
```
  primary: GOOGLESHEETS_SET_DATA_VALIDATION_RULE, GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES
  related: GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_GET_DATA_VALIDATION_RULES, GOOGLESHEETS_GET_CONDITIONAL_FORMAT_RULES, GOOGLESHEETS_FORMAT_CELL, GOOGLESHEETS_VALUES_UPDATE, GOOGLESHEETS_BATCH_GET
```
- why: The query asks for formatting, formulas, and data validation, whereas the required capability is writing, updating, and managing values across multiple cell ranges.
- judge: While GOOGLESHEETS_VALUES_UPDATE handles a single range, there is no tool returned that manages values across multiple cell ranges simultaneously as required by the batch update capability.

**Apply filters and sort options to data ranges**

- needed: `GOOGLESHEETS_SET_BASIC_FILTER`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The only query issued focuses on formatting, formulas, and data validation, but does not search for tools related to applying filters and sort options.
- judge: None of the returned tools provide the capability to apply filters or sort options to data ranges.

**Modify worksheet properties and metadata**

- needed: `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent's only query focused on formatting, formulas, and data validation, but did not issue any search to modify worksheet properties and metadata.
- judge: None of the returned tools provide the capability to modify worksheet properties and metadata.

### Task 58

> Inspect and modify a GitHub repository frontend, validate the changes if possible, then commit and push the changes directly to the default branch.

**Validate the changes**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the capability to validate the frontend code changes locally or execute build/test checks.

**Commit and push changes to the default branch**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the ability to commit and push changes directly to the default branch (only creating pull requests, updating files, or committing multiple files via API without an explicit push mechanism).

### Task 60

> Manage lead data in Google Sheets: read existing tabs, append and correct lead rows, enrich contacts, detect duplicate email addresses, highlight duplicate rows, and attempt to prepare leads for import into an Instantly 

**Enrich contact data and find email addresses**

- needed: `HUNTER_DOMAIN_SEARCH`, `HUNTER_EMAIL_FINDER`
- **fault: search: fair query, tool not returned**
- query the agent issued (#7): `instantly verify email or enrich contact`
- search returned:
```
  primary: INSTANTLY_CREATE_SUPERSEARCH_ENRICHMENT, INSTANTLY_SUPERSEARCH_ENRICHMENT_RUN_POST
  related: INSTANTLY_CREATE_LEAD_LIST, INSTANTLY_LIST_LEAD_LISTS, INSTANTLY_GET_LEAD_LIST, INSTANTLY_COUNT_LEADS_FROM_SUPERSEARCH, INSTANTLY_PATCH_SUPERSEARCH_ENRICHMENT_SETTINGS, INSTANTLY_GET_SUPERSEARCH_ENRICHMENT
```
- why: The query explicitly asks to verify email and enrich contact data, which directly targets the required capability.
- judge: None of the returned tools provide the specific capability to enrich contact data and find email addresses using Hunter tools (such as HUNTER_DOMAIN_SEARCH or HUNTER_EMAIL_FINDER).

### Task 64

> Prepare marketing and CRM automation work: gather marketing performance data, send a brief by email, analyze search query data, and scaffold a HubSpot customer follow-up campaign with custom properties, email drafts, and

**Gather marketing performance data from advertising platforms**

- needed: `GOOGLEADS_SEARCH_STREAM_GAQL`
- **fault: search: fair query, tool not returned**
- query the agent issued (#1): `get marketing performance data`
- search returned:
```
  primary: METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS, LINKEDIN_ADS_GET_AD_ANALYTICS
  related: METAADS_LIST_BUSINESS_AD_ACCOUNTS, METAADS_LIST_CLIENT_AD_ACCOUNTS, METAADS_GET_OBJECT, METAADS_READ_ADSETS, METAADS_GET_USER, METAADS_LIST_ADS, LINKEDIN_ADS_SEARCH_CAMPAIGNS, LINKEDIN_ADS_GET_AD_ACCOUNT, LINKEDIN_ADS_SEARCH_AD_ACCOUNTS, LINKEDIN_ADS_GET_TARGETING_ENTITIES, LINKEDIN_ADS_GET_TARGETING_FACETS, LINKEDIN_ADS_SEARCH_CREATIVES
```
- why: The query directly asks to get marketing performance data, which clearly matches the intended capability of gathering performance metrics from advertising platforms.
- judge: None of the returned tools provide the ability to gather marketing performance data from advertising platforms like Google Ads.

**Gather web analytics and traffic performance data**

- needed: `GOOGLE_ANALYTICS_RUN_REPORT`
- **fault: search: fair query, tool not returned**
- query the agent issued (#3): `search console query performance`
- search returned:
```
  primary: GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY
  related: GOOGLE_SEARCH_CONSOLE_GET_SITE, GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS, GOOGLE_SEARCH_CONSOLE_GET_SITEMAP, GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP, GOOGLE_SEARCH_CONSOLE_INSPECT_URL, GOOGLE_SEARCH_CONSOLE_ADD_SITE
```
- why: The query specifically asks for search console query performance, which directly aligns with gathering web analytics and traffic performance data from Google Search Console.
- judge: None of the returned tools provide Google Analytics website traffic and web analytics performance reporting.

### Task 67

> Manage Salesforce opportunity pipeline data: list open opportunities, update opportunity stages and required fields, verify record changes, consolidate duplicate contact data, and create a follow-up task linked to CRM re

**Consolidate or merge duplicate contact data**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned Salesforce tools provide the capability to consolidate or merge duplicate contact data.

### Task 68

> Modify a GitHub-hosted backend application, add protected console and lead-care functionality, configure deployment/runtime infrastructure, apply database migrations, and verify CI plus hosted deployment status.

**Verify CI check runs and workflow status**

- needed: `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target the verification of CI check runs and workflow status.
- judge: None of the returned GitHub tools provide the ability to list check runs or workflow run statuses for a reference or repository.

**Apply database migrations via SQL execution**

- needed: `SUPABASE_BETA_RUN_SQL_QUERY`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent did not issue any search queries specifically aimed at finding a tool to apply database migrations via SQL execution.
- judge: None of the returned GitHub tools provide the ability to execute SQL queries or apply database migrations.

**Check hosted deployment status and logs on Vercel**

- needed: `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_DEPLOYMENT_LOGS2`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a query to check hosted deployment status or logs on Vercel.
- judge: None of the returned GitHub tools provide the ability to check hosted deployment status and logs on Vercel.

### Task 69

> Perform a technical SEO audit around sitemap migration, indexability, linked-page health, and backlink/link-equity signals using Google Search Console and supporting crawl data.

**Scrape and crawl web pages to gather linked-page health and technical crawl data**

- needed: `FIRECRAWL_SCRAPE`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target web scraping or crawling to gather linked-page health and technical crawl data.
- judge: The returned tools only manage and inspect Google Search Console properties and sitemaps, and none of them provide the capability to scrape and crawl web pages for linked-page health and technical crawl data.

**Retrieve backlink and link-equity signals for the target domain**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned tools provide the ability to retrieve backlink and link-equity signals for the target domain.

### Task 70

> Migrate Vercel projects and GitHub repositories between connected accounts, preserve domains and settings, add deployment workflows, trigger/verify deployments, and audit repository access.

**Trigger and monitor GitHub Actions deployments and workflows**

- needed: `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
- **fault: agent: query too vague to find it**
- query the agent issued (#4): `trigger deploy Vercel deployment`
- search returned:
```
  primary: VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT
  related: VERCEL_GET_TEAMS, VERCEL_GET_PROJECT2, VERCEL_SEARCH_REPO, GITHUB_GET_A_REPOSITORY, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_DEPLOYMENT_LOGS2
```
- why: The query specifically asks for Vercel deployment tools, which is materially different from the required capability of triggering and monitoring GitHub Actions deployments and workflows.
- judge: None of the returned GitHub tools provide the ability to trigger workflow dispatch events or list workflow runs for a repository.

### Task 72

> Build, repair, deploy, configure, and test a Vercel-hosted GitHub-backed API proxy for Gemini text, image, video, embeddings, model listing, OpenAI-compatible paths, and tool-call-style outputs.

**Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models**

- needed: `GEMINI_GENERATE_CONTENT`, `GEMINI_LIST_MODELS`, `GEMINI_COUNT_TOKENS`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent did not issue any queries searching for tools related to generating text, model listing, token counting, or handling tool-call-style outputs using Gemini models.
- judge: None of the returned tools provide capabilities for interacting with Gemini models, such as generating text, counting tokens, or listing models.

**Generate images using Gemini image models**

- needed: `GEMINI_GENERATE_IMAGE`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent never issued a search query looking for a tool to generate images using Gemini image models.
- judge: None of the returned tools provide the capability to generate images using Gemini image models.

**Generate and poll/wait for videos using Google Veo models**

- needed: `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent did not issue any search query related to Google Veo models or video generation and polling.
- judge: None of the returned GitHub or Vercel tools provide the capability to generate and poll or wait for videos using Google Veo models.

**Generate text embeddings using Gemini models**

- needed: `GEMINI_EMBED_CONTENT`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: The agent did not issue any search query related to generating text embeddings using Gemini models.
- judge: None of the returned GitHub or Vercel tools provide the capability to generate text embeddings using Gemini models.

**Configure project environment variables on Vercel**

- needed: `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`
- **fault: agent: query too vague to find it**
- query the agent issued (#2): `deploy or manage vercel project`
- search returned:
```
  primary: VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT
  related: VERCEL_GET_TEAMS, VERCEL_GET_PROJECT2, VERCEL_SEARCH_REPO, GITHUB_GET_A_REPOSITORY, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_DEPLOYMENT_LOGS2
```
- why: The query asks about deploying or managing a project rather than specifically targeting the configuration of environment variables.
- judge: None of the returned Vercel tools provide the capability to add or configure environment variables on a Vercel project.

### Task 73

> Manage a large operational workflow across Google Tasks, Xero, and Notion: update and move task records, create and revise invoices, record payments, consolidate Notion rules, and track operational follow-ups.

**Get current date and time**

- needed: `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`
- **fault: agent: never searched for it**
- no query the agent issued was aimed at this capability
- why: None of the issued queries target the capability of getting the current date and time.
- judge: None of the returned tools provide the capability to get the current date and time.

### Task 77

> Audit a Google Ads client account under a manager account, research targeting and keywords, then build and verify a new search campaign with budget, targeting, keywords, ads, and assets.

**Research targeting and keyword opportunities for the campaign**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned Google Ads tools provide keyword or targeting research capabilities such as generating keyword ideas or analyzing search volume.

**Build and verify the new search campaign including budget, targeting, keywords, ads, and assets**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: While there are individual tools to mutate campaigns and ad groups, no single tool or complete set provided covers the full requirement to build and verify a new search campaign including budget, targeting, keywords, ads, and assets end-to-end.

### Task 80

> Audit Meta Ads account access, inspect performance for a specific ad set, identify improvement actions, then create a Trello card with an attached report and assignee; also attempt to clean up a faulty attachment.

**Audit Trello board access and members for assignee lookup**

- needed: `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`
- **fault: agent: query too vague to find it**
- query the agent issued (#3): `Create Trello card attachment member`
- search returned:
```
  primary: TRELLO_ADD_CARDS, TRELLO_ADD_CARDS_ATTACHMENTS_BY_ID_CARD
  related: TRELLO_GET_CARDS_BY_ID_CARD, TRELLO_UPDATE_CARDS_BY_ID_CARD, TRELLO_GET_SEARCH, TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD
```
- why: The query asks for creating card attachments and members, whereas the required capability is auditing board access and members for assignee lookup.
- judge: None of the returned Trello tools provide the specific capability to audit board access and list board members for assignee lookup.

### Task 85

> Investigate and patch a codebase hosted on GitHub, commit changes to a target branch, document the change, and merge that branch into the destination branch after approval.

**Merge branches after approval**

- needed: `GITHUB_MERGE_A_BRANCH`
- **fault: search: fair query, tool not returned**
- query the agent issued (#3): `merge a pull request on GitHub`
- search returned:
```
  primary: GITHUB_CREATE_A_PULL_REQUEST, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_MERGE_A_PULL_REQUEST, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD, TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD
  related: GITHUB_GET_A_PULL_REQUEST, GITHUB_GET_COMMIT_STATUSES, TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD
```
- why: The query asks to merge a pull request on GitHub, which directly matches the required capability to merge branches after approval using GitHub pull requests.
- judge: None of the returned tools provide the capability to directly merge branches (such as GITHUB_MERGE_A_BRANCH), as the available merge tool only merges pull requests.

### Task 89

> Audit inbound email and HubSpot marketing/automation assets to understand an external funnel, compare it with existing marketing emails and workflows, and inspect meeting-booking setup.

**Inspect meeting-booking setup and configuration**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned HubSpot or Gmail tools provide the capability to inspect or retrieve meeting-booking configuration and scheduling setup.

### Task 94

> Audit and optimize a Meta Ads account: retrieve account, campaign, ad set, ad, creative, performance, targeting, and pixel data; then apply confirmed optimization changes including pausing objects, changing ad set target

**Modify ad set targeting, pause objects, create custom audiences, and add exclusions**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: While some tools are provided for Meta Ads, there is no tool available to modify existing ad set targeting, add exclusions, or pause individual ads/ad sets (only campaigns can be paused).

**Retrieve pixel data**

- needed: _(nothing listed)_
- **fault: catalogue: no tool provides this**
- no tool in the logged list provides this either
- judge: None of the returned Meta Ads tools provide the capability to retrieve pixel data.

