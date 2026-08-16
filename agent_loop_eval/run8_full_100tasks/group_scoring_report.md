# Group-based scoring — `run8_full_100tasks`

Requirement groups replace the flat reference list: alternatives share a group, distinct
capabilities get separate groups, and logged-but-unnecessary tools are dropped. A group is
satisfied if search surfaced ANY tool in it. See the module docstring for why flat recall
is biased in both directions.

## Summary

- **Tasks scored:** 98
- **Requirement groups:** 433 (from 983 logged tools; 189 dropped as not required)
- **Strict group recall:** 324/433 (75%)
- **Judged group recall:** 359/433 (83%)
- **Groups hit in `primary`:** 241/433 (56%)
- **Flat union recall, for comparison:** 601/983 (61%)

Judged recall is the honest headline: strict recall still misses valid alternatives that
search returned but the logged list never named.

## Per task

| Task | Queries | Groups | Strict | Judged | Primary | Flat union | Dropped |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 5 | 3/5 | 3/5 | 2/5 | 8/10 | 1 |
| 2 | 2 | 3 | 2/3 | 2/3 | 2/3 | 2/6 | 0 |
| 3 | 3 | 4 | 3/4 | 3/4 | 2/4 | 4/4 | 1 |
| 4 | 6 | 5 | 5/5 | 5/5 | 3/5 | 10/10 | 5 |
| 5 | 4 | 4 | 4/4 | 4/4 | 3/4 | 11/17 | 0 |
| 6 | 4 | 3 | 2/3 | 3/3 | 2/3 | 7/11 | 3 |
| 7 | 4 | 4 | 2/4 | 3/4 | 2/4 | 9/23 | 3 |
| 8 | 3 | 3 | 0/3 | 2/3 | 0/3 | 0/1 | 0 |
| 9 | 3 | 4 | 2/4 | 3/4 | 2/4 | 3/4 | 0 |
| 11 | 5 | 4 | 2/4 | 3/4 | 2/4 | 7/13 | 1 |
| 12 | 6 | 7 | 4/7 | 4/7 | 2/7 | 5/11 | 0 |
| 13 | 3 | 4 | 2/4 | 2/4 | 1/4 | 3/13 | 5 |
| 14 | 2 | 2 | 2/2 | 2/2 | 2/2 | 4/9 | 6 |
| 15 | 5 | 5 | 3/5 | 5/5 | 2/5 | 5/8 | 2 |
| 16 | 3 | 4 | 2/4 | 2/4 | 1/4 | 8/25 | 8 |
| 17 | 4 | 6 | 4/6 | 4/6 | 3/6 | 11/20 | 7 |
| 18 | 2 | 2 | 1/2 | 1/2 | 1/2 | 1/5 | 3 |
| 19 | 3 | 4 | 2/4 | 3/4 | 2/4 | 5/18 | 9 |
| 20 | 5 | 5 | 3/5 | 4/5 | 2/5 | 8/15 | 3 |
| 21 | 2 | 5 | 3/5 | 5/5 | 1/5 | 3/7 | 1 |
| 22 | 3 | 4 | 1/4 | 1/4 | 1/4 | 2/19 | 0 |
| 23 | 3 | 4 | 4/4 | 4/4 | 2/4 | 4/4 | 0 |
| 24 | 2 | 2 | 2/2 | 2/2 | 2/2 | 4/6 | 3 |
| 25 | 2 | 3 | 3/3 | 3/3 | 2/3 | 5/8 | 3 |
| 26 | 4 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 0 |
| 27 | 3 | 4 | 3/4 | 3/4 | 3/4 | 5/6 | 1 |
| 28 | 5 | 5 | 3/5 | 4/5 | 3/5 | 7/8 | 2 |
| 29 | 7 | 6 | 5/6 | 5/6 | 4/6 | 10/24 | 10 |
| 30 | 3 | 3 | 1/3 | 2/3 | 1/3 | 2/12 | 4 |
| 31 | 5 | 6 | 3/6 | 4/6 | 2/6 | 6/13 | 1 |
| 32 | 2 | 4 | 0/4 | 0/4 | 0/4 | 0/7 | 1 |
| 33 | 3 | 4 | 3/4 | 3/4 | 2/4 | 3/7 | 3 |
| 34 | 5 | 5 | 5/5 | 5/5 | 5/5 | 12/16 | 0 |
| 35 | 3 | 3 | 3/3 | 3/3 | 3/3 | 4/4 | 1 |
| 36 | 5 | 4 | 4/4 | 4/4 | 3/4 | 15/28 | 12 |
| 37 | 6 | 7 | 6/7 | 7/7 | 5/7 | 13/17 | 2 |
| 38 | 4 | 4 | 3/4 | 4/4 | 2/4 | 5/8 | 0 |
| 39 | 1 | 2 | 1/2 | 1/2 | 0/2 | 1/7 | 0 |
| 40 | 2 | 3 | 3/3 | 3/3 | 1/3 | 7/13 | 0 |
| 41 | 6 | 7 | 5/7 | 6/7 | 4/7 | 8/14 | 1 |
| 42 | 5 | 2 | 2/2 | 2/2 | 2/2 | 9/9 | 1 |
| 43 | 3 | 8 | 6/8 | 7/8 | 6/8 | 7/8 | 0 |
| 44 | 3 | 2 | 2/2 | 2/2 | 2/2 | 4/4 | 1 |
| 45 | 6 | 7 | 4/7 | 7/7 | 3/7 | 9/15 | 5 |
| 46 | 3 | 6 | 5/6 | 5/6 | 3/6 | 11/14 | 0 |
| 47 | 3 | 2 | 2/2 | 2/2 | 1/2 | 7/10 | 8 |
| 48 | 5 | 4 | 4/4 | 4/4 | 3/4 | 8/9 | 1 |
| 49 | 7 | 8 | 6/8 | 8/8 | 4/8 | 7/8 | 1 |
| 50 | 4 | 6 | 6/6 | 6/6 | 5/6 | 7/9 | 3 |
| 51 | 5 | 6 | 4/6 | 5/6 | 3/6 | 8/10 | 0 |
| 52 | 3 | 4 | 2/4 | 2/4 | 2/4 | 2/6 | 2 |
| 53 | 3 | 4 | 3/4 | 3/4 | 2/4 | 6/8 | 3 |
| 54 | 4 | 9 | 4/9 | 5/9 | 2/9 | 4/8 | 0 |
| 55 | 1 | 6 | 3/6 | 3/6 | 1/6 | 4/13 | 2 |
| 56 | 6 | 6 | 6/6 | 6/6 | 5/6 | 11/11 | 1 |
| 57 | 3 | 4 | 4/4 | 4/4 | 2/4 | 7/9 | 1 |
| 58 | 2 | 4 | 1/4 | 2/4 | 1/4 | 4/4 | 0 |
| 59 | 4 | 5 | 5/5 | 5/5 | 5/5 | 9/11 | 0 |
| 60 | 7 | 5 | 3/5 | 4/5 | 1/5 | 6/10 | 0 |
| 61 | 5 | 5 | 5/5 | 5/5 | 3/5 | 5/5 | 0 |
| 62 | 2 | 2 | 2/2 | 2/2 | 0/2 | 3/3 | 0 |
| 63 | 7 | 5 | 5/5 | 5/5 | 4/5 | 10/14 | 1 |
| 64 | 7 | 7 | 4/7 | 5/7 | 3/7 | 5/8 | 0 |
| 65 | 2 | 3 | 3/3 | 3/3 | 3/3 | 4/7 | 0 |
| 66 | 3 | 4 | 4/4 | 4/4 | 1/4 | 4/9 | 5 |
| 67 | 4 | 5 | 4/5 | 4/5 | 3/5 | 5/5 | 0 |
| 68 | 2 | 5 | 2/5 | 2/5 | 2/5 | 3/13 | 5 |
| 69 | 2 | 5 | 3/5 | 3/5 | 3/5 | 4/6 | 1 |
| 70 | 6 | 7 | 6/7 | 6/7 | 3/7 | 10/20 | 8 |
| 71 | 4 | 4 | 4/4 | 4/4 | 2/4 | 5/5 | 0 |
| 72 | 3 | 7 | 2/7 | 2/7 | 2/7 | 7/19 | 0 |
| 73 | 5 | 4 | 3/4 | 3/4 | 2/4 | 14/18 | 0 |
| 74 | 3 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 0 |
| 75 | 1 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 0 |
| 76 | 6 | 5 | 4/5 | 5/5 | 4/5 | 8/12 | 3 |
| 77 | 4 | 3 | 1/3 | 1/3 | 1/3 | 1/1 | 0 |
| 78 | 8 | 6 | 6/6 | 6/6 | 5/6 | 15/20 | 10 |
| 79 | 3 | 4 | 4/4 | 4/4 | 2/4 | 7/12 | 1 |
| 80 | 4 | 6 | 5/6 | 5/6 | 5/6 | 10/16 | 8 |
| 81 | 3 | 4 | 4/4 | 4/4 | 3/4 | 7/7 | 1 |
| 82 | 4 | 5 | 5/5 | 5/5 | 3/5 | 9/13 | 0 |
| 83 | 3 | 3 | 3/3 | 3/3 | 2/3 | 7/7 | 0 |
| 84 | 6 | 5 | 5/5 | 5/5 | 3/5 | 10/10 | 0 |
| 85 | 4 | 4 | 2/4 | 3/4 | 1/4 | 2/9 | 2 |
| 86 | 3 | 3 | 3/3 | 3/3 | 3/3 | 4/6 | 2 |
| 87 | 5 | 3 | 3/3 | 3/3 | 2/3 | 9/10 | 0 |
| 88 | 4 | 3 | 3/3 | 3/3 | 2/3 | 4/4 | 0 |
| 89 | 4 | 4 | 2/4 | 3/4 | 2/4 | 3/5 | 0 |
| 90 | 2 | 3 | 3/3 | 3/3 | 2/3 | 5/5 | 1 |
| 91 | 3 | 4 | 4/4 | 4/4 | 3/4 | 6/7 | 0 |
| 93 | 3 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 0 |
| 94 | 6 | 8 | 6/8 | 6/8 | 6/8 | 7/8 | 1 |
| 95 | 4 | 4 | 4/4 | 4/4 | 4/4 | 4/4 | 0 |
| 96 | 2 | 5 | 3/5 | 5/5 | 0/5 | 3/5 | 0 |
| 97 | 6 | 4 | 4/4 | 4/4 | 4/4 | 9/19 | 6 |
| 98 | 3 | 5 | 4/5 | 5/5 | 3/5 | 7/11 | 1 |
| 99 | 4 | 5 | 5/5 | 5/5 | 3/5 | 15/20 | 2 |
| 100 | 2 | 2 | 2/2 | 2/2 | 1/2 | 2/2 | 0 |

## Capabilities search never delivered

Groups unmet even after judging — these are the real retrieval failures.

**Task 1**
- Assess payment link feasibility — expected _(nothing listed provided it)_
  - judge: No available tool assesses the feasibility of a payment link in HubSpot.
- Verify assets remain inert — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to verify that HubSpot assets remain inert.

**Task 2**
- Verify Notion content after writing — expected `NOTION_GET_PAGE_MARKDOWN`, `NOTION_RETRIEVE_PAGE`
  - judge: None of the returned Notion tools provide a specific capability to retrieve and verify the page markdown or full page content after writing.

**Task 3**
- Programmatically process and modify the spreadsheet workbook — expected _(nothing listed provided it)_
  - judge: None of the returned OneDrive tools provide the capability to programmatically process and modify the contents of a spreadsheet workbook.

**Task 7**
- Fetch and read email messages and threads — expected `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
  - judge: None of the returned Gmail tools provide the capability to fetch and read email messages and threads.

**Task 8**
- Mark incomplete archive documents when transcript retrieval fails — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to mark or update incomplete archive documents when transcript retrieval fails.

**Task 9**
- Search or source stock images for marketing assets — expected `COMPOSIO_SEARCH_IMAGE`
  - judge: Although GEMINI_GENERATE_IMAGE can create images from text prompts, no provided tool offers the specific capability to search or source existing stock images from a stock media library.

**Task 11**
- Check queue and system state files — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the specific capability to check queue and system state files as required by the operations knowledge base task.

**Task 12**
- Fetch and search Gmail emails for project management — expected `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - judge: None of the returned Gmail tools provide the ability to fetch and search emails, as the available tools only cover sending, drafting, replying, managing aliases, and searching contacts.
- Search and list Slack messages and users for chat integration — expected `SLACK_SEARCH_MESSAGES`, `SLACK_LIST_ALL_USERS`
  - judge: The available tools are for ClickUp chat channels, whereas the missing capability specifically requires Slack message and user search integration.
- Perform broader automation-maintenance operations — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide capabilities for broader automation-maintenance operations.

**Task 13**
- Audit website search performance and indexing — expected `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITE`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`
  - judge: The returned tools only provide Google Analytics (GA4) and Gmail functionalities, but none of them support auditing website search performance and indexing like Google Search Console.
- Prepare and manage email marketing or contact lists — expected `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - judge: None of the returned tools provide the capability to create and manage email marketing lists or contact lists.

**Task 16**
- Modify repository code and create pull requests — expected `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`
  - judge: None of the returned GitHub tools provide the ability to modify repository code or create pull requests; the available tools only retrieve references and search issues or pull requests.
- Investigate hosting and deployment state via DNS/CDN configuration — expected `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - judge: None of the returned Vercel or GitHub tools provide the ability to inspect DNS or CDN configuration for hosting and deployment state.

**Task 17**
- Attempt social media publishing on Instagram — expected `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - judge: None of the returned tools provide the specific capability to publish social media posts to Instagram.
- Read and update the booking schedule — expected `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - judge: The available tools only cover Google Calendar management rather than the required Google Sheets booking schedule read and update capabilities.

**Task 18**
- Search and extract recent job listings from web sources or job boards — expected `BROWSER_TOOL_CREATE_TASK`
  - judge: None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

**Task 19**
- Fetch and read content from web pages or job postings — expected `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
  - judge: None of the returned tools provide the capability to fetch and read the full content of arbitrary web pages or specific job postings from URLs.

**Task 20**
- Manage and reconcile files in Google Drive — expected _(nothing listed provided it)_
  - judge: Although there are tools for finding, getting metadata, and downloading files in Google Drive, there are no tools provided to manage (such as create, update, move, or delete) and reconcile files in Google Drive.

**Task 22**
- look up CRM-style trial records — expected `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
  - judge: None of the returned tools support Airtable or Pipedrive CRM trial records, as the available CRM tools are exclusively for Salesforce.
- inspect and modify source code in GitHub, and handle branches — expected `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_MERGE_A_BRANCH`
  - judge: None of the returned GitHub tools provide the ability to inspect source code, modify files, create branches, or merge pull requests.
- check CI workflow failures — expected `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_THE_COMBINED_STATUS_FOR_A_SPECIFIC_REFERENCE`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - judge: None of the returned GitHub tools provide the ability to check or download CI workflow run failures.

**Task 27**
- Create a new folder in Google Drive — expected `GOOGLEDRIVE_CREATE_FOLDER`
  - judge: None of the returned Google Drive tools provide the capability to create a new folder.

**Task 28**
- Generate AI text-to-speech audio for the video voiceover — expected `ELEVENLABS_TEXT_TO_SPEECH`
  - judge: None of the returned tools provide text-to-speech audio generation capabilities.

**Task 29**
- Notify collaborators — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide a direct capability for notifying collaborators, as the available tools are focused on social media posting, Fathom meetings, Gmail, Google Docs/Drive/Sheets, and LinkedIn.

**Task 30**
- Retrieve social page activity or posts — expected `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`
  - judge: None of the returned LinkedIn or other tools provide a capability to retrieve social page activity or posts directly, only statistics, network size, company info, and reactions.

**Task 31**
- Retrieve real-time market data and financial information — expected `COMPOSIO_SEARCH_FINANCE`
  - judge: None of the returned tools provide the capability to retrieve real-time market data and financial information.
- Create and manage tasks or reminders — expected `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`
  - judge: None of the returned tools provide the capability to create and manage TickTick tasks or reminders.

**Task 32**
- Public web research and content extraction — expected `COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
  - judge: None of the returned tools provide public web research or content extraction capabilities, as they are exclusively related to Google Drive and Salesforce operations.
- Browser automation and QA for web applications — expected `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`
  - judge: None of the returned tools provide browser automation or QA capabilities for web applications, as they are entirely focused on Google Drive and Salesforce integrations.
- Retail product and catalog search — expected `COMPOSIO_SEARCH_SHOPPING`
  - judge: None of the returned tools provide retail product or catalog search capabilities, as they are exclusively related to Google Drive and Salesforce.
- Fast LLM inference and content generation — expected `COMPOSIO_SEARCH_GROQ_CHAT`
  - judge: None of the returned Google Drive or Salesforce tools provide fast LLM inference and content generation capabilities.

**Task 33**
- List leads to analyze conversions and campaign outcomes — expected `KOMMO_LIST_LEADS`
  - judge: Although KOMMO_GET_LEAD is available, there is no tool returned in the session that provides the capability to list leads (`KOMMO_LIST_LEADS`) in Kommo CRM.

**Task 39**
- List and retrieve lead details, history, notes, and contacts from Kommo CRM — expected `KOMMO_GET_LEAD`, `KOMMO_LIST_CONTACTS`, `KOMMO_LIST_EVENTS`, `KOMMO_LIST_LEADS`, `KOMMO_LIST_NOTES_BY_ENTITY`
  - judge: None of the returned tools interact with Kommo CRM to list or retrieve lead details, history, notes, or contacts.

**Task 41**
- Commit code changes to a GitHub repository — expected `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_GET_REPOSITORY_CONTENT`
  - judge: None of the returned GitHub tools provide the ability to commit code changes to a repository.

**Task 43**
- Verify or trigger recalculation of spreadsheet formulas — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the ability to verify or trigger a recalculation of spreadsheet formulas.

**Task 46**
- Lookup workspace users for owner assignment — expected `NOTION_LIST_USERS`
  - judge: None of the returned Notion tools provide the capability to list or lookup workspace users for owner assignment.

**Task 51**
- Fetch and annotate support-thread evidence — expected `PLAIN_RUN_GRAPHQL_QUERY`
  - judge: None of the returned tools provide the required Plain GraphQL query capability to fetch and annotate support-thread evidence.

**Task 52**
- Retrieve memory data from Mem0 — expected `MEM0_GET_MEMORIES_BY_ENTITY`
  - judge: None of the returned Mem0 tools provide the capability to retrieve individual memories by entity, as only an export job creation tool was provided.
- Inspect existing Zep context, user nodes, and graph structure — expected `ZEP_GET_USER_NODE`
  - judge: None of the returned Zep tools provide the capability to directly inspect existing user nodes and graph structure as specified by the missing ZEP_GET_USER_NODE capability.

**Task 53**
- List and retrieve existing short links from a short-link management platform — expected `TINYURL_LIST_URLS`
  - judge: None of the returned tools provide the capability to list and retrieve existing short links from a short-link management platform like TinyURL.

**Task 54**
- Create and manage campaign budgets in Google Ads — expected `GOOGLEADS_MUTATE_CAMPAIGN_BUDGETS`
  - judge: None of the returned Google Ads tools provide the capability to create and manage campaign budgets.
- Configure campaign-level targeting criteria — expected `GOOGLEADS_MUTATE_CAMPAIGN_CRITERIA`
  - judge: None of the returned Google Ads tools provide the capability to configure campaign-level targeting criteria.
- Add keywords and targeting criteria to ad groups — expected `GOOGLEADS_MUTATE_AD_GROUP_CRITERIA`
  - judge: None of the returned Google Ads tools provide the capability to add keywords and targeting criteria to ad groups.
- Create and manage ads including responsive search ads — expected `GOOGLEADS_MUTATE_AD_GROUP_ADS`
  - judge: None of the returned Google Ads tools provide the capability to create and manage ads, such as responsive search ads.

**Task 55**
- Write, update, and manage values across multiple cell ranges — expected `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`
  - judge: While GOOGLESHEETS_VALUES_UPDATE handles a single range, there is no tool returned that manages values across multiple cell ranges simultaneously as required by the batch update capability.
- Apply filters and sort options to data ranges — expected `GOOGLESHEETS_SET_BASIC_FILTER`
  - judge: None of the returned tools provide the capability to apply filters or sort options to data ranges.
- Modify worksheet properties and metadata — expected `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES`
  - judge: None of the returned tools provide the capability to modify worksheet properties and metadata.

**Task 58**
- Validate the changes — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to validate the frontend code changes locally or execute build/test checks.
- Commit and push changes to the default branch — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the ability to commit and push changes directly to the default branch (only creating pull requests, updating files, or committing multiple files via API without an explicit push mechanism).

**Task 60**
- Enrich contact data and find email addresses — expected `HUNTER_DOMAIN_SEARCH`, `HUNTER_EMAIL_FINDER`
  - judge: None of the returned tools provide the specific capability to enrich contact data and find email addresses using Hunter tools (such as HUNTER_DOMAIN_SEARCH or HUNTER_EMAIL_FINDER).

**Task 64**
- Gather marketing performance data from advertising platforms — expected `GOOGLEADS_SEARCH_STREAM_GAQL`
  - judge: None of the returned tools provide the ability to gather marketing performance data from advertising platforms like Google Ads.
- Gather web analytics and traffic performance data — expected `GOOGLE_ANALYTICS_RUN_REPORT`
  - judge: None of the returned tools provide Google Analytics website traffic and web analytics performance reporting.

**Task 67**
- Consolidate or merge duplicate contact data — expected _(nothing listed provided it)_
  - judge: None of the returned Salesforce tools provide the capability to consolidate or merge duplicate contact data.

**Task 68**
- Verify CI check runs and workflow status — expected `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - judge: None of the returned GitHub tools provide the ability to list check runs or workflow run statuses for a reference or repository.
- Apply database migrations via SQL execution — expected `SUPABASE_BETA_RUN_SQL_QUERY`
  - judge: None of the returned GitHub tools provide the ability to execute SQL queries or apply database migrations.
- Check hosted deployment status and logs on Vercel — expected `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_DEPLOYMENT_LOGS2`
  - judge: None of the returned GitHub tools provide the ability to check hosted deployment status and logs on Vercel.

**Task 69**
- Scrape and crawl web pages to gather linked-page health and technical crawl data — expected `FIRECRAWL_SCRAPE`
  - judge: The returned tools only manage and inspect Google Search Console properties and sitemaps, and none of them provide the capability to scrape and crawl web pages for linked-page health and technical crawl data.
- Retrieve backlink and link-equity signals for the target domain — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the ability to retrieve backlink and link-equity signals for the target domain.

**Task 70**
- Trigger and monitor GitHub Actions deployments and workflows — expected `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - judge: None of the returned GitHub tools provide the ability to trigger workflow dispatch events or list workflow runs for a repository.

**Task 72**
- Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models — expected `GEMINI_GENERATE_CONTENT`, `GEMINI_LIST_MODELS`, `GEMINI_COUNT_TOKENS`
  - judge: None of the returned tools provide capabilities for interacting with Gemini models, such as generating text, counting tokens, or listing models.
- Generate images using Gemini image models — expected `GEMINI_GENERATE_IMAGE`
  - judge: None of the returned tools provide the capability to generate images using Gemini image models.
- Generate and poll/wait for videos using Google Veo models — expected `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate and poll or wait for videos using Google Veo models.
- Generate text embeddings using Gemini models — expected `GEMINI_EMBED_CONTENT`
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate text embeddings using Gemini models.
- Configure project environment variables on Vercel — expected `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`
  - judge: None of the returned Vercel tools provide the capability to add or configure environment variables on a Vercel project.

**Task 73**
- Get current date and time — expected `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`
  - judge: None of the returned tools provide the capability to get the current date and time.

**Task 77**
- Research targeting and keyword opportunities for the campaign — expected _(nothing listed provided it)_
  - judge: None of the returned Google Ads tools provide keyword or targeting research capabilities such as generating keyword ideas or analyzing search volume.
- Build and verify the new search campaign including budget, targeting, keywords, ads, and assets — expected _(nothing listed provided it)_
  - judge: While there are individual tools to mutate campaigns and ad groups, no single tool or complete set provided covers the full requirement to build and verify a new search campaign including budget, targeting, keywords, ads, and assets end-to-end.

**Task 80**
- Audit Trello board access and members for assignee lookup — expected `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`
  - judge: None of the returned Trello tools provide the specific capability to audit board access and list board members for assignee lookup.

**Task 85**
- Merge branches after approval — expected `GITHUB_MERGE_A_BRANCH`
  - judge: None of the returned tools provide the capability to directly merge branches (such as GITHUB_MERGE_A_BRANCH), as the available merge tool only merges pull requests.

**Task 89**
- Inspect meeting-booking setup and configuration — expected _(nothing listed provided it)_
  - judge: None of the returned HubSpot or Gmail tools provide the capability to inspect or retrieve meeting-booking configuration and scheduling setup.

**Task 94**
- Modify ad set targeting, pause objects, create custom audiences, and add exclusions — expected _(nothing listed provided it)_
  - judge: While some tools are provided for Meta Ads, there is no tool available to modify existing ad set targeting, add exclusions, or pause individual ads/ad sets (only campaigns can be paused).
- Retrieve pixel data — expected _(nothing listed provided it)_
  - judge: None of the returned Meta Ads tools provide the capability to retrieve pixel data.

## Alternatives credited by the judge

Groups no expected tool matched, but a tool search actually returned did the job.
Each of these is a flat-recall false negative.

**Task 6**
- Update existing Salesforce records (e.g., campaign attendance statuses) — satisfied by `SALESFORCE_UPDATE_CONTACT`
  - The SALESFORCE_UPDATE_CONTACT tool directly provides the capability to update existing Salesforce contact records.

**Task 7**
- Access and interact with LinkedIn data — satisfied by `LINKEDIN_GET_MY_INFO`
  - The returned LinkedIn tools (such as LINKEDIN_GET_MY_INFO and LINKEDIN_CREATE_LINKED_IN_POST) provide direct capability to access and interact with LinkedIn data.

**Task 8**
- Append summarized entries to existing Google Docs — satisfied by `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`
  - The tool allows updating a section of a Google Docs document using Markdown content, which satisfies the capability to append summarized entries to existing Google Docs.
- Retrieve public video transcript data for building and updating a knowledge base — satisfied by `SUPADATA_GET_TRANSCRIPT`
  - The SUPADATA_GET_TRANSCRIPT tool specifically provides the capability to retrieve video transcripts from public video platforms like YouTube, fulfilling the requirement to fetch public video transcript data.

**Task 9**
- Compile or deliver downloadable presentation content — satisfied by `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN`
  - The GOOGLESLIDES_CREATE_SLIDES_MARKDOWN tool creates a presentation directly from Markdown content, fulfilling the requirement to provide downloadable presentation content.

**Task 11**
- Coordinate operational tasks and communicate via Discord — satisfied by `DISCORDBOT_CREATE_MESSAGE`
  - The tool DISCORDBOT_CREATE_MESSAGE allows sending messages to a Discord channel, directly supporting the operational task coordination and communication capability.

**Task 15**
- Persist invoice attachments to cloud storage — satisfied by `GOOGLEDRIVE_UPLOAD_FILE`
  - The GOOGLEDRIVE_UPLOAD_FILE tool allows uploading files to Google Drive, which directly satisfies the requirement to persist invoice attachments to cloud storage.
- Read and update spreadsheet ledgers — satisfied by `GOOGLESHEETS_VALUES_UPDATE`
  - The GOOGLESHEETS_VALUES_UPDATE tool sets values in a range of a Google Spreadsheet, delivering the needed capability to update spreadsheet ledgers.

**Task 19**
- Search the web for Java backend and Spring Boot job listings — satisfied by `SERPAPI_GOOGLE_JOBS_SEARCH`
  - The SERPAPI_GOOGLE_JOBS_SEARCH tool retrieves job search results directly from Google Jobs, fulfilling the requirement to search for Java backend and Spring Boot job listings.

**Task 20**
- Access and reconcile QuickBooks billing records — satisfied by `QUICKBOOKS_QUERY_ENTITIES`
  - The QUICKBOOKS_QUERY_ENTITIES tool (along with other QuickBooks tools like QUICKBOOKS_READ_INVOICE and QUICKBOOKS_LIST_INVOICES) provides the necessary capability to access and reconcile QuickBooks billing records.

**Task 21**
- Read reference document content and fiscal-period logic — satisfied by `GOOGLEDRIVE_DOWNLOAD_FILE`
  - The GOOGLEDRIVE_DOWNLOAD_FILE tool explicitly supports exporting Google Docs to plain text, thereby providing the needed capability to read reference document content.
- Update spreadsheet formulas and values — satisfied by `GOOGLESHEETS_UPDATE_VALUES_BATCH`
  - The GOOGLESHEETS_UPDATE_VALUES_BATCH tool is provided to set values across one or more ranges in a spreadsheet, thereby delivering the required capability to update spreadsheet values.

**Task 28**
- Archive the final asset in a repository — satisfied by `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`
  - The GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS tool allows creating or updating a file in a GitHub repository, which provides the capability to archive the final asset in a repository.

**Task 30**
- Retrieve recent email messages or query email activity — satisfied by `GMAIL_FETCH_EMAILS`
  - The GMAIL_FETCH_EMAILS tool directly provides the capability to retrieve recent email messages by supporting filtering and content retrieval from a Gmail account.

**Task 31**
- Send messages through a WhatsApp or Notis channel — satisfied by `WHATSAPP_SEND_MESSAGE`
  - The WHATSAPP_SEND_MESSAGE tool provides the capability to send text messages through WhatsApp.

**Task 37**
- Create calendar events — satisfied by `OUTLOOK_CALENDAR_CREATE_EVENT`
  - The OUTLOOK_CALENDAR_CREATE_EVENT tool provides the capability to create new Outlook calendar events.

**Task 38**
- Attempt to send a Slack direct message with CRM-derived context — satisfied by `SLACK_FIND_USERS`
  - The SLACK_FIND_USERS tool includes optimized email lookup to find users in a Slack workspace by criteria including email, directly covering the needed capability of finding a user to send a direct message to.

**Task 41**
- Update a Jira issue (add comments, assign, or transition state) — satisfied by `JIRA_EDIT_ISSUE`
  - The JIRA_EDIT_ISSUE tool allows updating an existing Jira issue's fields and operations, satisfying the requirement to update a Jira issue.

**Task 43**
- Write values, formulas, or updates to a Google Spreadsheet — satisfied by `GOOGLESHEETS_VALUES_UPDATE`
  - The GOOGLESHEETS_VALUES_UPDATE tool explicitly allows updating and writing values to a range in a Google Spreadsheet.

**Task 45**
- Create a new HubSpot deal — satisfied by `HUBSPOT_CREATE_DEALS`
  - The tool HUBSPOT_CREATE_DEALS allows creating multiple deals in HubSpot CRM, directly fulfilling the required capability of creating a HubSpot deal.
- Update quote properties, terms, or template settings — satisfied by `HUBSPOT_BATCH_UPDATE_QUOTES`
  - The HUBSPOT_BATCH_UPDATE_QUOTES tool explicitly provides the capability to update existing HubSpot quotes, which covers the needed action of updating quote properties, terms, or template settings.
- Inspect quote details, properties, or template settings — satisfied by `HUBSPOT_READ_BATCH_OF_QUOTES_BY_PROPERTY_VALUES`
  - The tool efficiently retrieves a batch of HubSpot CRM quotes by their IDs or properties, directly delivering the capability to inspect quote details.

**Task 49**
- Upload new files to Google Drive — satisfied by `GOOGLEDRIVE_CREATE_FILE`
  - The description for GOOGLEDRIVE_CREATE_FILE explicitly states that it supports file upload with content when the file_to_upload parameter is provided.
- Attempt spreadsheet correction or update — satisfied by `GOOGLESHEETS_VALUES_UPDATE`
  - The GOOGLESHEETS_VALUES_UPDATE tool allows updating or overwriting existing cell values in a Google Spreadsheet, directly fulfilling the need to attempt a spreadsheet correction or update.

**Task 51**
- Retrieve attachment download links — satisfied by `HELPWISE_GET_ATTACHMENT`
  - The HELPWISE_GET_ATTACHMENT tool explicitly retrieves attachment metadata including its download URL.

**Task 54**
- Discover Asana tools for listing tasks assigned to the current user — satisfied by `ASANA_GET_MULTIPLE_TASKS`
  - The ASANA_GET_MULTIPLE_TASKS tool retrieves a list of tasks allowing filtering by assignee and workspace, which delivers the capability to list tasks assigned to a user.

**Task 58**
- Modify code files in the repository — satisfied by `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`
  - The GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS tool allows creating or updating files in a GitHub repository, which directly provides the capability to modify code files.

**Task 60**
- Export or prepare leads for an Instantly campaign — satisfied by `INSTANTLY_ADD_LEADS_BULK`
  - The tool INSTANTLY_ADD_LEADS_BULK explicitly provides the capability to import or add multiple leads in bulk to an Instantly campaign or list.

**Task 64**
- Send an email brief — satisfied by `GMAIL_SEND_EMAIL`
  - The GMAIL_SEND_EMAIL tool allows sending an email message immediately via the Gmail API, which directly matches the needed capability to send an email brief.

**Task 76**
- Fetch ClickUp docs and tasks for planning context — satisfied by `CLICKUP_CLICK_UP_GET_DOC_PAGE_CONTENT`
  - The tool CLICKUP_CLICK_UP_GET_DOC_PAGE_CONTENT is available and provides the capability to fetch ClickUp document page content for planning context.

**Task 85**
- Create commits and modify file trees — satisfied by `GITHUB_COMMIT_MULTIPLE_FILES`
  - The GITHUB_COMMIT_MULTIPLE_FILES tool allows creating, updating, or deleting files in a repository as a single commit, which directly provides the capability to create commits and modify file trees.

**Task 89**
- Fetch and audit inbound emails from Gmail — satisfied by `GMAIL_FETCH_EMAILS`
  - The GMAIL_FETCH_EMAILS tool explicitly allows fetching a list of email messages from a Gmail account to audit inbound emails.

**Task 96**
- Retrieve specific commit details — satisfied by `GITHUB_LIST_COMMITS`
  - Although GITHUB_GET_A_COMMIT was not returned, GITHUB_LIST_COMMITS allows filtering by SHA and retrieving commit details for the repository.
- Fetch raw file content — satisfied by `GITHUB_GET_REPOSITORY_CONTENT`
  - The GITHUB_GET_REPOSITORY_CONTENT tool retrieves a file's Base64 encoded content from a GitHub repository, which effectively delivers the capability to fetch raw file content.

**Task 98**
- Analyze Google Analytics 4 (GA4) attribution and event performance — satisfied by `GOOGLE_ANALYTICS_RUN_REPORT`
  - The GOOGLE_ANALYTICS_RUN_REPORT tool allows running customized GA4 data reports to analyze event performance and attribution.

