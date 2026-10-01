# Group-based scoring — `run9_retry_loop`

Requirement groups replace the flat reference list: alternatives share a group, distinct
capabilities get separate groups, and logged-but-unnecessary tools are dropped. A group is
satisfied if search surfaced ANY tool in it. See the module docstring for why flat recall
is biased in both directions.

## Summary

- **Tasks scored:** 86
- **Requirement groups:** 381 (from 833 logged tools; 155 dropped as not required)
- **Strict group recall:** 275/381 (72%)
- **Judged group recall:** 294/381 (77%)
- **Groups hit in `primary`:** 204/381 (54%)
- **Flat union recall, for comparison:** 508/833 (61%)

Judged recall is the honest headline: strict recall still misses valid alternatives that
search returned but the logged list never named.

## Per task

| Task | Queries | Groups | Strict | Judged | Primary | Flat union | Dropped |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 8 | 5 | 3/5 | 3/5 | 3/5 | 8/10 | 6 |
| 2 | 2 | 3 | 3/3 | 3/3 | 1/3 | 6/6 | 0 |
| 3 | 3 | 4 | 2/4 | 2/4 | 2/4 | 3/4 | 0 |
| 4 | 4 | 5 | 1/5 | 1/5 | 1/5 | 6/10 | 5 |
| 5 | 5 | 5 | 5/5 | 5/5 | 3/5 | 16/17 | 1 |
| 6 | 4 | 4 | 2/4 | 3/4 | 1/4 | 5/11 | 0 |
| 7 | 5 | 4 | 2/4 | 2/4 | 2/4 | 5/23 | 3 |
| 8 | 3 | 3 | 1/3 | 1/3 | 1/3 | 1/1 | 0 |
| 9 | 4 | 4 | 2/4 | 3/4 | 2/4 | 3/4 | 0 |
| 10 | 5 | 5 | 4/5 | 5/5 | 1/5 | 5/6 | 2 |
| 11 | 7 | 4 | 2/4 | 2/4 | 2/4 | 8/13 | 1 |
| 12 | 5 | 7 | 4/7 | 5/7 | 2/7 | 5/11 | 0 |
| 13 | 3 | 4 | 2/4 | 2/4 | 1/4 | 6/13 | 4 |
| 14 | 2 | 2 | 2/2 | 2/2 | 2/2 | 4/9 | 4 |
| 15 | 8 | 5 | 4/5 | 5/5 | 4/5 | 7/8 | 1 |
| 16 | 4 | 4 | 2/4 | 2/4 | 1/4 | 4/25 | 13 |
| 17 | 7 | 6 | 4/6 | 4/6 | 3/6 | 11/20 | 6 |
| 18 | 3 | 2 | 2/2 | 2/2 | 1/2 | 4/5 | 3 |
| 19 | 3 | 3 | 3/3 | 3/3 | 3/3 | 5/18 | 9 |
| 20 | 5 | 5 | 3/5 | 5/5 | 1/5 | 5/15 | 3 |
| 21 | 6 | 4 | 2/4 | 3/4 | 1/4 | 3/7 | 1 |
| 22 | 4 | 5 | 2/5 | 2/5 | 2/5 | 4/19 | 0 |
| 23 | 4 | 4 | 4/4 | 4/4 | 2/4 | 4/4 | 0 |
| 24 | 2 | 2 | 2/2 | 2/2 | 2/2 | 4/6 | 3 |
| 25 | 2 | 3 | 3/3 | 3/3 | 2/3 | 5/8 | 3 |
| 26 | 5 | 4 | 4/4 | 4/4 | 3/4 | 5/5 | 0 |
| 27 | 4 | 5 | 4/5 | 4/5 | 3/5 | 5/6 | 0 |
| 28 | 6 | 5 | 3/5 | 4/5 | 3/5 | 7/8 | 1 |
| 29 | 6 | 6 | 3/6 | 4/6 | 2/6 | 5/24 | 10 |
| 30 | 4 | 3 | 1/3 | 1/3 | 1/3 | 2/12 | 5 |
| 31 | 4 | 4 | 2/4 | 2/4 | 1/4 | 7/13 | 1 |
| 32 | 2 | 5 | 0/5 | 0/5 | 0/5 | 0/7 | 1 |
| 33 | 4 | 5 | 3/5 | 4/5 | 2/5 | 3/7 | 2 |
| 34 | 6 | 4 | 4/4 | 4/4 | 4/4 | 10/16 | 0 |
| 35 | 2 | 3 | 3/3 | 3/3 | 2/3 | 4/4 | 1 |
| 49 | 6 | 7 | 6/7 | 7/7 | 5/7 | 7/8 | 1 |
| 50 | 5 | 4 | 4/4 | 4/4 | 3/4 | 7/9 | 2 |
| 51 | 5 | 6 | 4/6 | 5/6 | 2/6 | 9/10 | 0 |
| 52 | 6 | 4 | 4/4 | 4/4 | 2/4 | 5/6 | 2 |
| 53 | 3 | 4 | 2/4 | 2/4 | 2/4 | 4/8 | 3 |
| 54 | 6 | 9 | 4/9 | 5/9 | 2/9 | 4/8 | 0 |
| 55 | 3 | 6 | 6/6 | 6/6 | 5/6 | 7/13 | 2 |
| 56 | 6 | 6 | 6/6 | 6/6 | 4/6 | 10/11 | 1 |
| 57 | 4 | 4 | 4/4 | 4/4 | 2/4 | 9/9 | 1 |
| 58 | 3 | 2 | 1/2 | 1/2 | 1/2 | 3/4 | 0 |
| 59 | 6 | 5 | 5/5 | 5/5 | 5/5 | 10/11 | 0 |
| 60 | 4 | 5 | 1/5 | 1/5 | 1/5 | 4/10 | 0 |
| 61 | 6 | 5 | 5/5 | 5/5 | 3/5 | 5/5 | 0 |
| 62 | 6 | 2 | 2/2 | 2/2 | 2/2 | 3/3 | 0 |
| 63 | 6 | 5 | 5/5 | 5/5 | 3/5 | 8/14 | 0 |
| 64 | 6 | 7 | 3/7 | 4/7 | 3/7 | 3/8 | 0 |
| 65 | 5 | 3 | 3/3 | 3/3 | 3/3 | 6/7 | 0 |
| 66 | 4 | 4 | 4/4 | 4/4 | 3/4 | 5/9 | 5 |
| 67 | 5 | 5 | 4/5 | 4/5 | 3/5 | 5/5 | 0 |
| 68 | 5 | 5 | 2/5 | 2/5 | 2/5 | 3/13 | 5 |
| 69 | 3 | 5 | 3/5 | 3/5 | 2/5 | 4/6 | 1 |
| 70 | 6 | 7 | 5/7 | 5/7 | 5/7 | 13/20 | 6 |
| 71 | 6 | 4 | 4/4 | 4/4 | 3/4 | 5/5 | 0 |
| 72 | 5 | 12 | 4/12 | 5/12 | 3/12 | 9/19 | 1 |
| 73 | 4 | 4 | 3/4 | 3/4 | 2/4 | 9/18 | 0 |
| 74 | 3 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 0 |
| 75 | 2 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 0 |
| 76 | 5 | 5 | 5/5 | 5/5 | 4/5 | 8/12 | 2 |
| 77 | 9 | 3 | 1/3 | 2/3 | 1/3 | 1/1 | 0 |
| 78 | 6 | 4 | 4/4 | 4/4 | 4/4 | 14/20 | 12 |
| 79 | 4 | 4 | 4/4 | 4/4 | 4/4 | 9/12 | 1 |
| 80 | 5 | 7 | 7/7 | 7/7 | 5/7 | 12/16 | 6 |
| 81 | 3 | 4 | 4/4 | 4/4 | 3/4 | 7/7 | 1 |
| 82 | 5 | 6 | 5/6 | 5/6 | 3/6 | 11/13 | 1 |
| 83 | 4 | 3 | 2/3 | 2/3 | 2/3 | 3/7 | 0 |
| 84 | 6 | 5 | 5/5 | 5/5 | 4/5 | 10/10 | 0 |
| 85 | 4 | 4 | 1/4 | 1/4 | 0/4 | 2/9 | 1 |
| 86 | 5 | 2 | 2/2 | 2/2 | 2/2 | 4/6 | 1 |
| 87 | 4 | 5 | 4/5 | 4/5 | 2/5 | 9/10 | 0 |
| 88 | 4 | 4 | 4/4 | 4/4 | 2/4 | 4/4 | 0 |
| 89 | 5 | 4 | 2/4 | 3/4 | 2/4 | 3/5 | 0 |
| 90 | 3 | 4 | 3/4 | 3/4 | 2/4 | 4/5 | 0 |
| 91 | 2 | 3 | 3/3 | 3/3 | 2/3 | 5/7 | 2 |
| 93 | 4 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 0 |
| 94 | 5 | 9 | 6/9 | 6/9 | 4/9 | 6/8 | 1 |
| 95 | 5 | 4 | 4/4 | 4/4 | 3/4 | 4/4 | 0 |
| 96 | 3 | 4 | 3/4 | 3/4 | 0/4 | 4/5 | 0 |
| 97 | 6 | 5 | 4/5 | 4/5 | 4/5 | 14/19 | 3 |
| 98 | 5 | 4 | 3/4 | 4/4 | 3/4 | 9/11 | 3 |
| 99 | 6 | 4 | 4/4 | 4/4 | 3/4 | 15/20 | 2 |
| 100 | 4 | 2 | 2/2 | 2/2 | 1/2 | 2/2 | 0 |

## Capabilities search never delivered

Groups unmet even after judging — these are the real retrieval failures.

**Task 1**
- Assess payment link feasibility — expected _(nothing listed provided it)_
  - judge: None of the returned HubSpot tools provide the capability to assess payment link feasibility.
- Verify the assets remain inert — expected _(nothing listed provided it)_
  - judge: None of the returned HubSpot tools provide the capability to verify that created assets remain inert and inactive.

**Task 3**
- Programmatically process and modify the spreadsheet workbook to add comparison summary worksheets/sections — expected _(nothing listed provided it)_
  - judge: None of the returned OneDrive tools provide the capability to programmatically process, modify, or add summary worksheets to a spreadsheet workbook.
- Upload the modified workbook back to OneDrive and update the existing cloud item — expected `ONE_DRIVE_UPDATE_FILE_CONTENT`
  - judge: The search engine returned tools for uploading new files or finding items in OneDrive, but none that update the content of an existing cloud item as required.

**Task 4**
- Add a first comment to a LinkedIn post — expected `LINKEDIN_CREATE_COMMENT_ON_POST`
  - judge: None of the returned tools provide the capability to add a first comment to a LinkedIn post.
- Add a comment or update status on a Trello card — expected `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
  - judge: The returned Trello tools are strictly for reading data (getting boards, cards, checklists, and members), and none of them provide the capability to add a comment or update the status of a Trello card.
- Move a Trello card to update its workflow status — expected `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
  - judge: None of the returned Trello tools provide the capability to move a card or update its list ID.
- Adjust the Trello board workflow structure by adding lists — expected `TRELLO_ADD_LISTS`
  - judge: None of the returned Trello tools provide the capability to add lists to adjust the board workflow structure.

**Task 6**
- Delete Salesforce records efficiently — expected `SALESFORCE_DELETE_SOBJECT_COLLECTIONS`
  - judge: None of the returned tools provide the ability to delete Salesforce records efficiently in bulk or collections.

**Task 7**
- Configure SMS receiving/sending and manage SMS communications — expected `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_CREATE_SMS_SEND`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_GET_SMS_HISTORY`, `CLICKSEND_GET_SMS_INBOUND`, `CLICKSEND_GET_SMS_RECEIPTS`
  - judge: The returned Brevo tools only support creating marketing SMS campaigns and managing contacts, but do not provide the required capabilities for receiving SMS, viewing SMS history, or managing inbound/outbound SMS communications.
- Interact with and aggregate signals from LinkedIn — expected _(nothing listed provided it)_
  - judge: Although there are several LinkedIn tools returned, none of them provide the capability to interact with and aggregate personal signals or messages from LinkedIn.

**Task 8**
- Retrieve public video transcript data for building and updating the knowledge base — expected _(nothing listed provided it)_
  - judge: While YouTube tools are available to list or attempt loading captions, none can reliably retrieve public video transcript data for arbitrary videos without ownership restrictions.
- Mark incomplete archive documents when transcript retrieval fails — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the specific capability to mark incomplete archive documents when transcript retrieval fails.

**Task 9**
- Create and export downloadable presentation content — expected _(nothing listed provided it)_
  - judge: None of the returned tools are capable of creating and exporting downloadable presentation content.

**Task 11**
- Coordinate operational tasks via Discord — expected `DISCORDBOT_LIST_MESSAGES`
  - judge: None of the returned Discord tools provide the capability to list messages (`DISCORDBOT_LIST_MESSAGES`), only sending messages, creating webhooks, or fetching channel metadata and guild lists.
- Check queue and system state files — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to check queue and system state files.

**Task 12**
- Retrieve emails for project management and communication — expected `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - judge: None of the returned Gmail tools provide the ability to search or fetch received email messages for project management purposes, as they are limited to drafting, sending, replying, and managing drafts or contacts.
- Perform automation-maintenance operations on an automation platform — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide capabilities for performing automation-maintenance operations on an automation platform.

**Task 13**
- Audit website traffic and user analytics — expected `GOOGLE_ANALYTICS_RUN_REPORT`
  - judge: None of the returned tools provide website traffic and user analytics capabilities such as running Google Analytics reports.
- Create and manage marketing and contact lists — expected `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - judge: None of the returned SendGrid or other tools provide the capability to create and manage new marketing contact lists.

**Task 16**
- Modify source code and create pull requests — expected `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`
  - judge: None of the returned GitHub tools provide the ability to modify source code or create pull requests, as they are limited to retrieving references, issues, comments, and archives.
- Investigate hosting, deployment, and DNS state — expected `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - judge: None of the returned Vercel or GitHub tools provide the specific Cloudflare DNS zone management and record-listing capabilities needed to inspect DNS state.

**Task 17**
- Publish media to Instagram — expected `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - judge: None of the returned tools provide the capability to publish media to Instagram.
- Read and update a booking schedule — expected `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - judge: The available tools only support Google Calendar operations and lack the required capability to read and update a Google Sheets booking schedule.

**Task 21**
- Update spreadsheet data, formulas, and add summary worksheets — expected `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_ADD_SHEET`
  - judge: None of the returned Google Sheets tools provide the capability to update data, formulas, or add summary worksheets, as they are limited to searching, listing, and reading values.

**Task 22**
- Search CRM-style trial records in Airtable or Pipedrive — expected `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
  - judge: None of the returned tools provide access to Airtable or Pipedrive, as the available CRM tools are exclusively for Salesforce.
- Inspect source code, manage files, and search code in GitHub — expected `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_SEARCH_CODE`
  - judge: None of the returned GitHub tools provide the ability to inspect source code, manage files, or search code in repositories.
- Open, manage, or merge branches and pull requests in GitHub — expected `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`
  - judge: None of the returned GitHub tools provide the ability to open, manage, or merge branches and pull requests.

**Task 27**
- Create new folders in the destination — expected `GOOGLEDRIVE_CREATE_FOLDER`
  - judge: None of the returned tools provide the capability to create new folders in Google Drive.

**Task 28**
- Generate AI text-to-speech audio for the video — expected `ELEVENLABS_TEXT_TO_SPEECH`
  - judge: None of the returned tools provide text-to-speech audio generation, as the HeyGen tools generate full avatar videos rather than text-to-speech audio.

**Task 29**
- Inspect recent meeting notes from Fathom — expected `FATHOM_GET_RECORDING_SUMMARY`, `FATHOM_LIST_MEETINGS`
  - judge: None of the returned tools provide the capability to inspect meeting notes or recordings specifically from Fathom.
- Notify collaborators regarding updates or workflows — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to notify collaborators regarding updates or workflows.

**Task 30**
- Collect recent email activity from Outlook mailbox — expected `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_SEARCH_MESSAGES`
  - judge: The search engine returned Gmail tools, but the required capability specifically called for collecting recent email activity from an Outlook mailbox.
- Collect social page activity and posts from Facebook — expected `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`
  - judge: None of the returned Facebook tools collect page activity or posts, as the available social tools are strictly limited to LinkedIn.

**Task 31**
- Retrieve financial market data or stock prices — expected `COMPOSIO_SEARCH_FINANCE`
  - judge: None of the returned Notion, Outlook, or WhatsApp tools provide the capability to retrieve financial market data or stock prices.
- Create and manage tasks or reminders — expected `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`
  - judge: None of the returned Notion, Outlook, or WhatsApp tools provide the ability to create and manage TickTick tasks or reminders.

**Task 32**
- Perform public web research and extract content from web pages — expected `COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
  - judge: None of the returned tools provide public web search or URL content extraction capabilities, as they are strictly focused on Intercom, Salesforce, and Slack.
- Automate browser workflows and check task progress for QA or web tasks — expected `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`
  - judge: None of the returned Intercom, Salesforce, or Slack tools provide browser automation or task progress checking for QA or web tasks.
- Search retail beverage catalogs and product listings — expected `COMPOSIO_SEARCH_SHOPPING`
  - judge: None of the returned Intercom, Salesforce, or Slack tools provide the capability to search retail beverage catalogs and product listings.
- Execute fast LLM inference for content generation and summarization — expected `COMPOSIO_SEARCH_GROQ_CHAT`
  - judge: None of the returned Intercom, Salesforce, or Slack tools provide fast LLM inference for content generation and summarization.
- Manage Discord roles and server interactions — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide capabilities for managing Discord roles or server interactions.

**Task 33**
- Track system events, entity changes, and activity history to detect campaign sends and agent actions — expected `KOMMO_LIST_EVENTS`
  - judge: None of the returned tools provide the capability to track system events, entity changes, or activity history required for detecting campaign sends and agent actions in Kommo CRM.

**Task 51**
- Fetch and annotate support-thread evidence — expected `PLAIN_RUN_GRAPHQL_QUERY`
  - judge: None of the returned tools provide the ability to fetch and annotate support-thread evidence from Plain (PLAIN_RUN_GRAPHQL_QUERY), as the available tools are limited to Datadog, Gmail, Google Drive, Google Sheets, Instagram, and Metabase.

**Task 53**
- Search for and discover relevant spreadsheets — expected `GOOGLESHEETS_SEARCH_SPREADSHEETS`
  - judge: Although Google Drive discovery tools were returned, no dedicated Google Sheets search tool was provided to find relevant spreadsheets by content or query.
- List and retrieve short-link inventory data — expected `TINYURL_LIST_URLS`
  - judge: None of the returned Google Drive, Google Sheets, Trello, or scraping tools provide the specific capability to list and retrieve short-link inventory data from a short-link service like TinyURL.

**Task 54**
- Create and manage Google Ads campaign budgets — expected `GOOGLEADS_MUTATE_CAMPAIGN_BUDGETS`
  - judge: None of the returned tools provide the capability to create and manage Google Ads campaign budgets.
- Create and manage Google Ads campaign-level targeting criteria — expected `GOOGLEADS_MUTATE_CAMPAIGN_CRITERIA`
  - judge: None of the returned tools provide the capability to create and manage campaign-level targeting criteria in Google Ads.
- Create and manage Google Ads ad group criteria and keywords — expected `GOOGLEADS_MUTATE_AD_GROUP_CRITERIA`
  - judge: None of the returned Google Ads tools provide the capability to create and manage ad group criteria and keywords (such as GOOGLEADS_MUTATE_AD_GROUP_CRITERIA).
- Create and manage Google Ads ads including responsive search ads — expected `GOOGLEADS_MUTATE_AD_GROUP_ADS`
  - judge: None of the returned Google Ads or Asana tools provide the capability to create or manage Google Ads ads, such as responsive search ads.

**Task 58**
- Modify, commit, and push changes to the GitHub repository — expected _(nothing listed provided it)_
  - judge: The returned tools only provide search, listing, and file retrieval capabilities, lacking any tool to modify, commit, or push changes to a GitHub repository.

**Task 60**
- Write, append, and update values in Google Sheets — expected `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_VALUES_UPDATE`
  - judge: None of the returned Google Drive or Google Sheets tools provide the ability to write, append, or update cell values inside an existing Google Spreadsheet.
- Format cells in Google Sheets (e.g., highlighting duplicates) — expected `GOOGLESHEETS_FORMAT_CELL`
  - judge: None of the returned Google Drive or Google Sheets tools provide the capability to format cells or highlight duplicate rows in a Google Sheet.
- Enrich contacts and find email addresses — expected `HUNTER_DOMAIN_SEARCH`, `HUNTER_EMAIL_FINDER`
  - judge: None of the returned Google Drive, Google Sheets, or Instantly tools provide the ability to enrich contacts and find email addresses.
- Prepare and import leads into an Instantly campaign — expected _(nothing listed provided it)_
  - judge: Although there are Instantly tools available for listing and retrieving campaign and lead data, none of the returned tools provide the capability to prepare and import leads into an Instantly campaign.

**Task 64**
- Gather marketing performance data from advertising platforms — expected `GOOGLEADS_SEARCH_STREAM_GAQL`
  - judge: None of the returned Google Search Console or HubSpot tools provide the capability to gather marketing performance data from advertising platforms like Google Ads.
- Gather website traffic and analytics data — expected `GOOGLE_ANALYTICS_RUN_REPORT`
  - judge: None of the returned tools provide the ability to gather website traffic and analytics data (such as Google Analytics reports).
- Create or update marketing email drafts in HubSpot — expected `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_UPDATE_A_MARKETING_EMAIL`
  - judge: None of the returned HubSpot tools support creating or updating marketing email drafts.

**Task 67**
- Consolidate duplicate contact data — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the ability to consolidate duplicate contact data; they only allow listing, searching, updating, or deleting individual contacts.

**Task 68**
- Execute database migrations via SQL queries — expected `SUPABASE_BETA_RUN_SQL_QUERY`
  - judge: None of the returned Bitbucket or GitHub tools provide the ability to execute database migrations via SQL queries.
- Verify CI status and workflow runs on GitHub — expected `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - judge: None of the returned GitHub tools provide functionality to list check runs or workflow runs for verifying CI status.
- Check hosted deployment status and logs on Vercel — expected `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_DEPLOYMENT_LOGS2`
  - judge: None of the returned tools provide Vercel deployment status or log retrieval capabilities.

**Task 69**
- Scrape web pages to evaluate linked-page health, content, and crawl data — expected `FIRECRAWL_SCRAPE`
  - judge: None of the returned Google Search Console tools provide the ability to scrape web pages for evaluating linked-page health and content.
- Retrieve backlink and link-equity signal data — expected _(nothing listed provided it)_
  - judge: None of the returned Google Search Console tools provide backlink and link-equity signal data retrieval capabilities.

**Task 70**
- Transfer Vercel projects between accounts — expected `VERCEL_CREATE_PROJECT_TRANSFER_REQUEST`
  - judge: None of the returned Vercel tools provide the capability to transfer existing projects between accounts or create a project transfer request.
- Trigger and monitor GitHub deployment workflows — expected `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
  - judge: None of the returned GitHub or Vercel tools provide the specific capability to trigger a workflow dispatch event or list workflow runs for a repository.

**Task 72**
- Generate text content or responses using Gemini models — expected `GEMINI_GENERATE_CONTENT`
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate text content using Gemini models.
- Generate images from text prompts using Gemini models — expected `GEMINI_GENERATE_IMAGE`
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate images from text prompts using Gemini models.
- Generate videos from text prompts using Google Veo models — expected `GEMINI_GENERATE_VIDEOS`
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate videos from text prompts using Google Veo models.
- Check the status of or wait for a video generation operation to complete — expected `GEMINI_WAIT_FOR_VIDEO`
  - judge: None of the returned GitHub or Vercel tools provide the capability to check the status of or wait for a Gemini video generation operation to complete.
- Generate text embeddings using Gemini models — expected `GEMINI_EMBED_CONTENT`
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate text embeddings using Gemini models.
- Count the number of tokens in text using Gemini tokenization — expected `GEMINI_COUNT_TOKENS`
  - judge: None of the returned tools provide the capability to count tokens in text using Gemini tokenization.
- List available Gemini and Veo models and their capabilities — expected `GEMINI_LIST_MODELS`
  - judge: None of the returned GitHub or Vercel tools provide the capability to list available Gemini and Veo models and their capabilities.

**Task 73**
- Get current date and time — expected `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`
  - judge: None of the returned tools provide the capability to get the current date and time.

**Task 77**
- Perform keyword research and targeting analysis for search campaigns — expected _(nothing listed provided it)_
  - judge: None of the available Google Ads or Keyword.com tools provide the capability to perform keyword research (such as generating keyword ideas, search volume estimation, or forecasting) for new search campaigns.

**Task 82**
- Cluster remaining unread emails for triage — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to cluster remaining unread emails for triage in Outlook.

**Task 83**
- Inspect related due-diligence email context — expected `OUTLOOK_GET_MESSAGE`, `OUTLOOK_SEARCH_MESSAGES`
  - judge: The search engine returned Gmail tools, but the task specifically requires inspecting Outlook email context.

**Task 85**
- Create commits, trees, and update references to patch the codebase and commit changes to a target branch — expected `GITHUB_CREATE_A_COMMIT`, `GITHUB_CREATE_A_TREE`, `GITHUB_UPDATE_A_REFERENCE`
  - judge: The search engine only returned discovery, search, and retrieval tools for GitHub, lacking any tools capable of creating commits, trees, or updating references.
- Merge the target branch into the destination branch — expected `GITHUB_MERGE_A_BRANCH`
  - judge: None of the returned tools provide the capability to merge a branch into a destination branch.
- Retrieve branch references and commit details for workflow validation or context — expected `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_COMMIT`
  - judge: None of the returned GitHub tools provide the ability to retrieve specific branch references or commit details for workflow validation.

**Task 87**
- Archive or clean up Notion pages, blocks, or databases during reorganization — expected `NOTION_DELETE_BLOCK`
  - judge: None of the returned Notion tools provide the capability to archive or delete pages, blocks, or databases.

**Task 89**
- Inspect meeting-booking setup — expected _(nothing listed provided it)_
  - judge: None of the returned Gmail or HubSpot tools provide functionality for inspecting meeting-booking setups like calendar links, scheduling pages, or meeting configurations.

**Task 90**
- Upload files such as images to be inserted into the presentation — expected `GOOGLEDRIVE_UPLOAD_FILE`
  - judge: None of the returned Google Drive or Google Slides tools provide the capability to upload local files like images into Google Drive so they can be inserted into a presentation.

**Task 94**
- List ad creatives under an ad account — expected `METAADS_LIST_AD_CREATIVES`
  - judge: None of the returned Meta Ads tools provide the capability to list ad creatives under an ad account.
- Update ad set targeting, pause objects, create custom audiences, and add exclusions — expected _(nothing listed provided it)_
  - judge: While some Meta Ads tools were returned, none of them provide the capability to update ad set targeting or add exclusions.
- Retrieve pixel data — expected _(nothing listed provided it)_
  - judge: None of the returned Meta Ads tools provide the capability to retrieve pixel data.

**Task 96**
- Run smoke tests in the local or remote environment — expected _(nothing listed provided it)_
  - judge: None of the returned GitHub tools provide the ability to run smoke tests locally or in a remote environment.

**Task 97**
- Manage deal participants and primary contacts — expected `PIPEDRIVE_ADD_DEAL_PARTICIPANT`, `PIPEDRIVE_LIST_PARTICIPANTS_OF_A_DEAL`
  - judge: Although PIPEDRIVE_LIST_DEAL_PERSONS can list participants, there is no tool returned that allows adding or managing deal participants and primary contacts.

## Alternatives credited by the judge

Groups no expected tool matched, but a tool search actually returned did the job.
Each of these is a flat-recall false negative.

**Task 6**
- Create Salesforce records such as leads, contacts, and campaign members — satisfied by `SALESFORCE_CREATE_LEAD`
  - The tool SALESFORCE_CREATE_LEAD explicitly provides the capability to create new lead records in Salesforce.

**Task 9**
- Search or source stock images — satisfied by `GEMINI_GENERATE_IMAGE`
  - The GEMINI_GENERATE_IMAGE tool generates images from text prompts using Gemini models, which provides the capability to create visual media assets for travel marketing.

**Task 10**
- Record a customer payment — satisfied by `QUICKBOOKS_CREATE_PAYMENT`
  - The QUICKBOOKS_CREATE_PAYMENT tool explicitly records payments from customers against invoices in QuickBooks Online, directly matching the needed capability.

**Task 12**
- Search or list Slack messages and users for project coordination — satisfied by `SLACK_FIND_USERS`
  - The SLACK_FIND_USERS tool allows finding users in a Slack workspace by criteria such as email, name, or display name, thus delivering the needed capability to find Slack users for project coordination.

**Task 15**
- Persist invoice attachments to cloud storage — satisfied by `GOOGLEDRIVE_UPLOAD_FILE`
  - The GOOGLEDRIVE_UPLOAD_FILE tool genuinely provides the capability to upload and persist files to cloud storage.

**Task 20**
- Manage records and data in QuickBooks billing systems — satisfied by `QUICKBOOKS_QUERY_ENTITIES`
  - The QUICKBOOKS_QUERY_ENTITIES tool allows executing SQL-like queries to manage and retrieve data across QuickBooks Online entities such as customers, invoices, bills, and payments.
- Search, read, and organize files within Google Drive — satisfied by `GOOGLEDRIVE_FIND_FILE`
  - The tool GOOGLEDRIVE_FIND_FILE provides comprehensive file and folder discovery capabilities to search and locate files within Google Drive.

**Task 21**
- Read document content and reference materials — satisfied by `GOOGLEDRIVE_EXPORT_GOOGLE_WORKSPACE_FILE`
  - The tool exports Google Docs to a specified format and returns the content, fulfilling the need to read document content.

**Task 28**
- Archive the final video asset in a repository — satisfied by `GOOGLEDRIVE_UPLOAD_FILE`
  - The Google Drive upload and creation tools provided allow storing and archiving the final video asset into a repository/cloud storage folder.

**Task 29**
- Publish scheduled social content across multiple platforms — satisfied by `POSTIZ_MCP_INTEGRATIONSCHEDULEPOSTTOOL`
  - The POSTIZ_MCP_INTEGRATIONSCHEDULEPOSTTOOL allows scheduling and publishing social media posts across platforms supported by Postiz integrations.

**Task 33**
- Retrieve pipeline stages to map campaign conversions to sales funnel steps — satisfied by `KOMMO_LIST_LEADS_PIPELINES`
  - The tool KOMMO_LIST_LEADS_PIPELINES provides the capability to list lead pipelines and their stages in Kommo CRM to map campaign conversions to sales funnel steps.

**Task 49**
- Upload new files to Google Drive — satisfied by `GOOGLEDRIVE_CREATE_FILE`
  - The description for GOOGLEDRIVE_CREATE_FILE explicitly states that it supports file upload with content when file_to_upload is provided, which matches the required capability to upload new files to Google Drive.

**Task 51**
- Retrieve attachment download links — satisfied by `GMAIL_GET_ATTACHMENT`
  - The GMAIL_GET_ATTACHMENT tool retrieves specific attachments by ID from a message, directly delivering the capability to get attachment download links and data.

**Task 54**
- List tasks assigned to the current user in Asana — satisfied by `ASANA_GET_MULTIPLE_TASKS`
  - The ASANA_GET_MULTIPLE_TASKS tool retrieves a list of tasks with the ability to filter by assignee and workspace, which directly fulfills the requirement to list tasks assigned to the current user.

**Task 64**
- Send an email brief — satisfied by `GMAIL_SEND_EMAIL`
  - The GMAIL_SEND_EMAIL tool directly enables sending an email brief immediately via the Gmail API.

**Task 72**
- Delete files from a GitHub repository — satisfied by `GITHUB_COMMIT_MULTIPLE_FILES`
  - The GITHUB_COMMIT_MULTIPLE_FILES tool explicitly supports deleting files from a GitHub repository as part of an atomic commit operation.

**Task 77**
- Create and configure new search campaigns, budgets, targeting, keywords, ads, and assets — satisfied by `GOOGLEADS_MUTATE_CAMPAIGNS`
  - The set of GOOGLEADS_MUTATE_* and GOOGLESUPER_MUTATE_* tools collectively provide the necessary capabilities to create and configure campaign budgets, campaigns, ad groups, keywords, ads, and assets.

**Task 89**
- Fetch and audit inbound email messages — satisfied by `GMAIL_FETCH_EMAILS`
  - The GMAIL_FETCH_EMAILS tool explicitly fetches a list of email messages from a Gmail account, directly fulfilling the needed capability to fetch and audit inbound email messages.

**Task 98**
- Analyze website attribution performance using Google Analytics — satisfied by `GOOGLE_ANALYTICS_RUN_REPORT`
  - The GOOGLE_ANALYTICS_RUN_REPORT tool allows running customized GA4 data reports to analyze website attribution performance.

