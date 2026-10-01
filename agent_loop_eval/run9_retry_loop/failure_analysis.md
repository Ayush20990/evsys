# What went wrong — `run9_retry_loop`

The 100 use cases need **381 capabilities** between them. This is every one that was
not delivered, why, and whose problem it is to fix.

## The short version

- **Search almost always finds the right tool.** It failed to retrieve one for a fair, specific query in **5 of 381** cases.
- **It just does not always recommend it.** In **71** cases the right tool came back only under `related`, never as a primary recommendation. An agent acting on the recommendation misses all 71 — so this, not retrieval, is the thing worth fixing.
- **61 failures are the agent's own**: it either never searched for the capability (39) or asked too vaguely to find it (22). These say nothing about search quality.
- **21** need a tool that does not exist in the catalogue at all.

| What happened | Count | Whose problem |
|---|---:|---|
| Search found it but buried it | 71 | **Search — ranking** |
| The agent never looked for it | 39 | Agent |
| The agent asked too vaguely | 22 | Agent |
| No tool exists for it | 21 | Catalogue |
| Search missed a fair question | 5 | **Search — retrieval** |

**Search-side 76 · agent-side 61 · catalogue 21.**

---

## Search found the right tool but buried it

71 capabilities were delivered **only** in `related`. The tool was there; it
was never put forward. This is the largest fixable failure in the run, and counting it
needs no judgement — it is set membership.

| Task | What was needed | Tool that was buried |
|---|---|---|
| 2 | Retrieve upcoming calendar events | `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` |
| 2 | Retrieve Notion page content for verification after writing | `NOTION_GET_PAGE_MARKDOWN`, `NOTION_RETRIEVE_PAGE` |
| 5 | Query and inspect Notion CRM records and databases | `NOTION_FETCH_DATABASE`, `NOTION_FETCH_ROW`, `NOTION_QUERY_DATABASE_WITH_FILTER` |
| 5 | Write evidence-supported CRM status updates to Notion | `NOTION_UPDATE_PAGE` |
| 6 | Update existing Salesforce records (e.g., campaign attendance statuses) | `SALESFORCE_SOBJECT_ROWS_UPDATE` |
| 10 | Query existing QuickBooks transactions and entities for ledger reconciliation | `QUICKBOOKS_QUERY_ENTITIES` |
| 10 | Modify, delete, or undo incorrect QuickBooks ledger entries | `QUICKBOOKS_EXECUTE_BATCH_OPERATION` |
| 10 | Verify financial reports and transaction lists | `QUICKBOOKS_GET_REPORTS` |
| 12 | Add comments to Trello cards | `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD` |
| 12 | Search or retrieve Trello cards and boards | `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH` |
| 13 | Send outreach and marketing emails | `GMAIL_SEND_EMAIL` |
| 16 | Inspect source repository structure and file contents | `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_REPOSITORY_CONTENT` |
| 17 | Upload supporting media assets for video creation | `HEYGEN_UPLOAD_ASSET` |
| 18 | Search and extract recent job listings from web sources or job boards | `BROWSER_TOOL_CREATE_TASK` |
| 20 | Read and write Google Docs content and sections | `GOOGLEDOCS_GET_DOCUMENT_BY_ID`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT` |
| 20 | Inspect Zoho CRM module fields and metadata | `ZOHO_GET_MODULE_FIELDS` |
| 21 | Read spreadsheet structure, metadata, and cell values | `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_GET_SPREADSHEET_INFO` |
| 23 | Fetch full Zendesk ticket details and associated comments | `ZENDESK_GET_ZENDESK_TICKET_BY_ID` |
| 23 | Fetch single Zendesk user details by user ID for requester enrichment | `ZENDESK_GET_USER` |
| 25 | Fetch and extract content from web page URLs | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |
| 26 | Inspect file contents (downloading files for analysis) | `GOOGLEDRIVE_DOWNLOAD_FILE` |
| 27 | Verify Google Drive access and account details | `GOOGLEDRIVE_GET_ABOUT` |
| 29 | Inspect recent meeting notes and files from Google Drive | `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FOLDER` |
| 31 | Send notifications through WhatsApp or a Notis channel | `WHATSAPP_GET_PHONE_NUMBERS` |
| 33 | Retrieve conversation threads and message history to analyze broadcast replies and audience interaction | `KOMMO_LIST_CONVERSATIONS` |
| 35 | Post replies to Instagram comments in bulk | `INSTAGRAM_POST_IG_COMMENT_REPLIES` |
| 49 | Download or export files from Google Drive | `GOOGLEDRIVE_DOWNLOAD_FILE` |
| 50 | Verify the correct Slack workspace and authentication | `SLACK_TEST_AUTH` |
| 51 | Query Metabase for data and analytics evidence | `METABASE_POST_API_DATASET` |
| 51 | Retrieve spreadsheet evidence | `GOOGLESHEETS_BATCH_GET` |
| 52 | Retrieve existing memories from Mem0 | `MEM0_GET_MEMORIES_BY_ENTITY` |
| 52 | Inspect existing Zep context, user nodes, and graph structure | `ZEP_GET_USER_NODE` |
| 54 | Create and manage Google Ads campaigns | `GOOGLEADS_MUTATE_CAMPAIGNS` |
| 54 | Create and manage Google Ads ad groups | `GOOGLEADS_MUTATE_AD_GROUPS` |
| 55 | Manage worksheet properties and structure | `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES` |
| 56 | Inspect property definitions and metadata | `HUBSPOT_LIST_CONTACT_PROPERTIES`, `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` |
| 56 | Create associations between records | `HUBSPOT_CREATE_OBJECT_ASSOCIATION` |
| 57 | Analyze channel and trend performance on YouTube | `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CHANNEL_VIDEOS`, `YOUTUBE_SEARCH_YOU_TUBE` |
| 57 | Inspect Instagram posting context and media | `INSTAGRAM_GET_IG_USER_MEDIA` |
| 61 | Move messages into appropriate folders | `OUTLOOK_MOVE_MESSAGE` |
| 61 | Mark selected messages as read or update their properties | `OUTLOOK_UPDATE_EMAIL` |
| 63 | List calendar events | `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` |
| 63 | Retrieve ecommerce store orders, products, and shop details | `SHOPIFY_GET_SHOP_DETAILS` |
| 66 | Update email message body or properties | `OUTLOOK_UPDATE_EMAIL` |
| 67 | Retrieve field metadata and requirements for Salesforce objects | `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT` |
| 69 | Inspect individual URLs for indexing status and issues | `GOOGLE_SEARCH_CONSOLE_INSPECT_URL` |
| 71 | Check whether prior communication exists in email | `OUTLOOK_SEARCH_MESSAGES` |
| 72 | List branches in a GitHub repository | `GITHUB_LIST_BRANCHES` |
| 73 | Manage and update tasks in Google Tasks | `GOOGLETASKS_LIST_TASKS`, `GOOGLETASKS_PATCH_TASK` |
| 76 | Retrieve ClickUp planning context from docs and tasks | `CLICKUP_GET_FILTERED_TEAM_TASKS` |
| 80 | Audit Trello board access/memberships | `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD` |
| 80 | Find Trello member/assignee ID | `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_SEARCH_MEMBERS` |
| 81 | Retrieve video details or metadata in bulk | `YOUTUBE_GET_VIDEO_DETAILS_BATCH` |
| 82 | List and locate mail folders | `OUTLOOK_LIST_CHILD_MAIL_FOLDERS`, `OUTLOOK_LIST_MAIL_FOLDERS` |
| 82 | Delete unwanted messages | `OUTLOOK_DELETE_MESSAGE` |
| 84 | Create a new repository | `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY` |
| 85 | Search code and retrieve repository contents to investigate the codebase | `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_SEARCH_CODE` |
| 87 | Read content or block structures from specific Notion pages | `NOTION_FETCH_ALL_BLOCK_CONTENTS`, `NOTION_GET_PAGE_MARKDOWN` |
| 87 | Update existing Notion database rows or pages during reorganization | `NOTION_UPDATE_ROW_DATABASE` |
| 88 | Fetch detailed ticket information including comments and requester context | `ZENDESK_GET_ZENDESK_TICKET_BY_ID` |
| 88 | Enrich tickets with requester details | `ZENDESK_GET_USER` |
| 90 | Inspect existing presentation, slides, layouts, and page details | `GOOGLESLIDES_PRESENTATIONS_GET`, `GOOGLESLIDES_PRESENTATIONS_PAGES_GET` |
| 91 | Manage or retrieve Meta ads reporting and campaign status | `METAADS_GET_INSIGHTS` |
| 94 | List ad sets under an ad account | `METAADS_READ_ADSETS` |
| 94 | List ads under an ad account | `METAADS_LIST_ADS` |
| 95 | List bank transactions | `ZOHO_BOOKS_LIST_BANK_TRANSACTIONS` |
| 96 | Browse or retrieve repository structure and file contents | `GITHUB_GET_A_TREE` |
| 96 | Create commits in the GitHub repository | `GITHUB_COMMIT_MULTIPLE_FILES` |
| 96 | Verify commit details and CI check-run status | `GITHUB_GET_A_COMMIT`, `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` |
| 99 | Inspect Supabase schema and run read-only database queries | `SUPABASE_LIST_TABLES`, `SUPABASE_RUN_READ_ONLY_QUERY` |
| 100 | Query and retrieve Attio company records and their domains/attributes | `ATTIO_QUERY_RECORDS` |

## Search missed a fair question

5 cases where the query did identify what was needed and search still did
not return it. Each is laid out in full so it can be checked.

**These are first-attempt failures.** Across all 384 queries in this run the agent never
re-asked for a capability once -- not a single near-duplicate query. It searches once per
step and moves on, because mocked execution succeeds on any well-formed call and nothing
ever tells it a tool was wrong. So each case below is one shot, and search might well
recover on a rephrase; equally, this benchmark produces no evidence about retry
behaviour at all, which a production agent hitting real errors would exhibit.

#### Task 3 — Upload the modified workbook back to OneDrive and update the existing cloud item

- **Asked:** `upload file to OneDrive`
- **Needed:** `ONE_DRIVE_UPDATE_FILE_CONTENT`
- **Got:** primary: GOOGLEDRIVE_UPLOAD_FILE, ONE_DRIVE_ONEDRIVE_UPLOAD_FILE
  related: GOOGLEDRIVE_RESUMABLE_UPLOAD, GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_CREATE_PERMISSION, ONE_DRIVE_ONEDRIVE_CREATE_FOLDER
- **What went wrong:** The query explicitly names OneDrive and describes the file upload action, which directly maps to the ONE_DRIVE_UPDATE_FILE_CONTENT tool.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.
- **Judge:** The search engine returned tools for uploading new files or finding items in OneDrive, but none that update the content of an existing cloud item as required.

#### Task 22 — Open, manage, or merge branches and pull requests in GitHub

- **Asked:** `search github repositories pull requests issues workflows`
- **Needed:** `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`
- **Got:** primary: GMAIL_FETCH_EMAILS, GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY
  related: GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, GITHUB_GET_A_WORKFLOW_RUN, GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN, GITHUB_DOWNLOAD_WORKFLOW_RUN_LOGS, GITHUB_LIST_REPOSITORY_WORKFLOWS
- **What went wrong:** The query explicitly names GitHub and mentions pull requests, which directly aligns with the functionality of creating a pull request.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GMAIL_FETCH_EMAILS`
- **Judge:** None of the returned GitHub tools provide the ability to open, manage, or merge branches and pull requests.

#### Task 33 — Track system events, entity changes, and activity history to detect campaign sends and agent actions

- **Asked:** `Kommo CRM users agents responsible users`
- **Needed:** `KOMMO_LIST_EVENTS`
- **Got:** primary: KOMMO_LIST_USERS
  related: KOMMO_GET_USER, KOMMO_GET_ACCOUNT
- **What went wrong:** The query names Kommo CRM and asks for users and agents responsible, which directly aligns with tracking assignment changes and entity events performed by the tool.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `KOMMO_LIST_USERS`
- **Judge:** None of the returned tools provide the capability to track system events, entity changes, or activity history required for detecting campaign sends and agent actions in Kommo CRM.

#### Task 53 — List and retrieve short-link inventory data

- **Asked:** `list short links or url redirects`
- **Needed:** `TINYURL_LIST_URLS`
- **Got:** primary: TRELLO_GET_CARDS_BY_ID_CARD
  related: TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_GET_CARDS_BY_ID_CARD_BY_FIELD, TRELLO_GET_CARDS_CHECKLISTS_BY_ID_CARD, TRELLO_GET_CARDS_CUSTOM_FIELD_ITEMS_BY_ID_CARD, TRELLO_GET_CARDS_ATTACHMENTS_BY_ID_CARD
- **What went wrong:** The query directly describes the core action of listing short links and URL redirects, which precisely matches the functionality of the TinyURL list URLs tool.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.
- **Judge:** None of the returned Google Drive, Google Sheets, Trello, or scraping tools provide the specific capability to list and retrieve short-link inventory data from a short-link service like TinyURL.

#### Task 97 — Manage deal participants and primary contacts

- **Asked:** `update deal participants and primary contacts in Pipedrive`
- **Needed:** `PIPEDRIVE_ADD_DEAL_PARTICIPANT`, `PIPEDRIVE_LIST_PARTICIPANTS_OF_A_DEAL`
- **Got:** primary: PIPEDRIVE_UPDATE_DEAL
  related: PIPEDRIVE_UPDATE_DEAL_V2, PIPEDRIVE_GET_DEAL, PIPEDRIVE_SEARCH_PERSONS, PIPEDRIVE_GET_PERSON
- **What went wrong:** The query explicitly names the Pipedrive application and asks to perform the exact action of managing deal participants.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.
- **Judge:** Although PIPEDRIVE_LIST_DEAL_PERSONS can list participants, there is no tool returned that allows adding or managing deal participants and primary contacts.

## Queries that named an application and got a different one

Of 461 queries, 302 name an application. 8 of those got nothing from it in `primary`, and 4 got nothing from it anywhere.

Counted separately because it happens even when no capability was missed — task 1
asked for a HubSpot payment link and was answered entirely in Stripe.

| Task | Asked | Wanted from | Got | Named app absent entirely |
|---|---|---|---|---|
| 1 | `payment links commerce invoices HubSpot` | hubspot | `RAZORPAY_FETCH_ALL_PAYMENT_LINKS`, `STRIPE_LIST_PAYMENT_LINKS` | **yes** |
| 7 | `GitHub search issues pull requests notifications` | github | `GMAIL_FETCH_EMAILS` | no |
| 11 | `Send message or coordinate on Discord` | discord | `DISCORDBOT_CREATE_MESSAGE` | no |
| 13 | `send email outreach marketing campaign gmail works` | gmail | `SENDGRID_CREATE_A_CAMPAIGN`, `SENDGRID_SEND_A_CAMPAIGN` | no |
| 24 | `Search LinkedIn job listings` | linkedin | `COMPOSIO_SEARCH_WEB` | no |
| 33 | `Kommo CRM broadcasts marketing campaigns mass mess` | kommo | `SALESFORCE_SEND_MASS_EMAIL` | **yes** |
| 98 | `Search owned social media performance analytics or` | facebook, instagram, youtube | `CROWTERMINAL_INGEST_DATA` | **yes** |
| 98 | `Get social media performance paid ads website attr` | facebook, instagram, youtube | `METAADS_GET_INSIGHTS`, `METAADS_LIST_AD_NETWORK_ANALYTICS` | **yes** |

---

## Failures that are not search's fault

### The agent never looked for it (39)

No query it issued was aimed at this capability, so search was never asked.

| Task | Capability that was never searched for |
|---|---|
| 4 | Add a first comment to a LinkedIn post |
| 4 | Add a comment or update status on a Trello card |
| 4 | Move a Trello card to update its workflow status |
| 4 | Adjust the Trello board workflow structure by adding lists |
| 6 | Delete Salesforce records efficiently |
| 17 | Publish media to Instagram |
| 29 | Inspect recent meeting notes from Fathom |
| 31 | Retrieve financial market data or stock prices |
| 32 | Perform public web research and extract content from web pages |
| 32 | Automate browser workflows and check task progress for QA or web tasks |
| 32 | Search retail beverage catalogs and product listings |
| 32 | Execute fast LLM inference for content generation and summarization |
| 54 | Create and manage Google Ads campaign budgets |
| 54 | Create and manage Google Ads campaign-level targeting criteria |
| 54 | Create and manage Google Ads ad group criteria and keywords |
| 54 | Create and manage Google Ads ads including responsive search ads |
| 60 | Write, append, and update values in Google Sheets |
| 60 | Format cells in Google Sheets (e.g., highlighting duplicates) |
| 60 | Enrich contacts and find email addresses |
| 64 | Gather website traffic and analytics data |
| 64 | Create or update marketing email drafts in HubSpot |
| 68 | Execute database migrations via SQL queries |
| 68 | Verify CI status and workflow runs on GitHub |
| 68 | Check hosted deployment status and logs on Vercel |
| 69 | Scrape web pages to evaluate linked-page health, content, and crawl data |
| 70 | Transfer Vercel projects between accounts |
| 72 | Generate text content or responses using Gemini models |
| 72 | Generate images from text prompts using Gemini models |
| 72 | Generate videos from text prompts using Google Veo models |
| 72 | Check the status of or wait for a video generation operation to complete |
| 72 | Generate text embeddings using Gemini models |
| 72 | Count the number of tokens in text using Gemini tokenization |
| 72 | List available Gemini and Veo models and their capabilities |
| 73 | Get current date and time |
| 85 | Create commits, trees, and update references to patch the codebase and commit changes to a target branch |
| 85 | Merge the target branch into the destination branch |
| 85 | Retrieve branch references and commit details for workflow validation or context |
| 90 | Upload files such as images to be inserted into the presentation |
| 94 | List ad creatives under an ad account |

### The agent asked too vaguely (22)

It searched, but the query did not identify the tool it needed.

#### Task 7 — Configure SMS receiving/sending and manage SMS communications

- **Asked:** `SMS send receive configure messaging`
- **Needed:** `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_CREATE_SMS_SEND`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_GET_SMS_HISTORY`, `CLICKSEND_GET_SMS_INBOUND`, `CLICKSEND_GET_SMS_RECEIPTS`
- **Got:** primary: BREVO_CREATE_SMS_CAMPAIGN, MSG91_SEND_SMS
  related: BREVO_GET_CONTACT_LISTS, BREVO_GET_ALL_CONTACTS, BREVO_GET_ACCOUNT_INFO, BREVO_GET_SMS_CAMPAIGNS, BREVO_FIND_CONTACT, TELNYX_LIST_PHONE_NUMBERS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned tools handle sending and configuring SMS messaging, which matches the core tasks described in the query even though they are from different applications.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.

#### Task 11 — Coordinate operational tasks via Discord

- **Asked:** `Send message or coordinate on Discord`
- **Needed:** `DISCORDBOT_LIST_MESSAGES`
- **Got:** primary: DISCORDBOT_CREATE_MESSAGE
  related: DISCORDBOT_LIST_GUILD_CHANNELS, DISCORD_LIST_MY_GUILDS, DISCORDBOT_CREATE_WEBHOOK, DISCORDBOT_GET_CHANNEL, DISCORDBOT_EXECUTE_WEBHOOK, DISCORDBOT_TEST_AUTH
- **What went wrong:** query names discord but the step needs discordbot
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `DISCORDBOT_CREATE_MESSAGE`

#### Task 12 — Retrieve emails for project management and communication

- **Asked:** `send email`
- **Needed:** `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
- **Got:** primary: GMAIL_SEND_EMAIL, GMAIL_CREATE_EMAIL_DRAFT
  related: GMAIL_SEND_DRAFT, GMAIL_GET_DRAFT, GMAIL_UPDATE_DRAFT, GMAIL_REPLY_TO_THREAD, GMAIL_SEARCH_PEOPLE, GMAIL_LIST_SEND_AS
- **What went wrong:** The query 'send email' describes sending a message, whereas the target tool fetches and retrieves emails.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.

#### Task 13 — Audit website traffic and user analytics

- **Asked:** `search console analytics website traffic audit`
- **Needed:** `GOOGLE_ANALYTICS_RUN_REPORT`
- **Got:** primary: GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY
  related: GOOGLE_SEARCH_CONSOLE_GET_SITE, GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS, GOOGLE_SEARCH_CONSOLE_GET_SITEMAP, GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP, GOOGLE_SEARCH_CONSOLE_INSPECT_URL, GOOGLE_SEARCH_CONSOLE_ADD_SITE
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Search Console tools perform the same website traffic analysis and auditing function as the expected Google Analytics tools, just within a different Google ecosystem application.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GOOGLE_SEARCH_CONSOLE_LIST_SITES`, `GOOGLE_SEARCH_CONSOLE_LIST_SITES`

#### Task 13 — Create and manage marketing and contact lists

- **Asked:** `spreadsheet contacts CRM email list marketing`
- **Needed:** `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
- **Got:** primary: SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_SEARCH_CONTACTS
  related: SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT, SALESFORCE_QUERY_ALL, SALESFORCE_TOOLING_QUERY, SALESFORCE_GET_ACCOUNT, SALESFORCE_GET_CONTACT, SALESFORCE_SEARCH_LEADS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Salesforce tools manage contacts and data lists similarly to how the expected Brevo tool manages contact lists for marketing.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `SALESFORCE_RUN_SOQL_QUERY`

#### Task 16 — Modify source code and create pull requests

- **Asked:** `git repository source code github GitLab`
- **Needed:** `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`
- **Got:** primary: GITHUB_DOWNLOAD_A_REPOSITORY_ARCHIVE_ZIP, GITLAB_GET_RAW_FILE, GITHUB_GET_THE_LICENSE_FOR_A_REPOSITORY
  related: GITHUB_GET_A_REFERENCE, GITLAB_GET_FILE, GITLAB_GET_REPOSITORY_BRANCH, GITHUB_GET_REPOSITORY_CONTENT
- **What went wrong:** The query is a broad mix of git and repository terms rather than a specific request to atomically commit multiple files to GitHub.
- **The agent retried this step 2 times:**
    - attempt 1: `git repository source code github GitLab` → `GITHUB_DOWNLOAD_A_REPOSITORY_ARCHIVE_ZIP`, `GITLAB_GET_RAW_FILE`, `GITHUB_GET_THE_LICENSE_FOR_A_REPOSITORY`
    - attempt 1: `list repositories github` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_LIST_REPOSITORY_ISSUES`
- **Did it run one of the returned tools?** `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`

#### Task 16 — Investigate hosting, deployment, and DNS state

- **Asked:** `hosting deployment status Vercel Netlify AWS GCP`
- **Needed:** `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
- **Got:** primary: VERCEL_GET_DEPLOYMENTS, VERCEL_GET_DEPLOYMENT
  related: VERCEL_GET_PROJECTS, VERCEL_GET_TEAMS, VERCEL_LIST_DEPLOYMENT_ALIASES, VERCEL_LIST_DEPLOYMENT_CHECKS, VERCEL_GET_DEPLOYMENT_EVENTS2, VERCEL_GET_DEPLOYMENT_LOGS2
- **What went wrong:** query names vercel but the step needs cloudflare
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `VERCEL_GET_DEPLOYMENTS`

#### Task 17 — Read and update a booking schedule

- **Asked:** `Read and update a calendar booking schedule`
- **Needed:** `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
- **Got:** primary: GOOGLECALENDAR_PATCH_EVENT
  related: GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_EVENTS_INSTANCES, GOOGLECALENDAR_UPDATE_EVENT, GOOGLECALENDAR_LIST_CALENDARS, GOOGLECALENDAR_EVENTS_GET, GOOGLECALENDAR_EVENTS_LIST
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- Both the expected spreadsheet tool and the returned calendar tool deal with reading and modifying schedule bookings, fulfilling the core task of managing a calendar schedule in a different application.
- **The agent retried this step 2 times:**
    - attempt 1: `Read and update a calendar booking schedule` → `GOOGLECALENDAR_PATCH_EVENT`
    - attempt 1: `List calendar events` → `GOOGLECALENDAR_EVENTS_LIST`
- **Did it run one of the returned tools?** `GOOGLECALENDAR_EVENTS_LIST`

#### Task 21 — Update spreadsheet data, formulas, and add summary worksheets

- **Asked:** `search spreadsheets or excel files`
- **Needed:** `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_ADD_SHEET`
- **Got:** primary: GOOGLESHEETS_SEARCH_SPREADSHEETS, GOOGLEDRIVE_FIND_FILE
  related: GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_VALUES_GET, GOOGLESHEETS_BATCH_GET, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLESHEETS_GET_SPREADSHEET_INFO
- **What went wrong:** The query is too broad, asking generally about spreadsheets or excel files without identifying the specific Google Sheets batch update action required by the user's step.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GOOGLESHEETS_SEARCH_SPREADSHEETS`, `GOOGLEDRIVE_FIND_FILE`

#### Task 22 — Search CRM-style trial records in Airtable or Pipedrive

- **Asked:** `search CRM records contacts leads trials`
- **Needed:** `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
- **Got:** primary: SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_SEARCH_CONTACTS
  related: SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT, SALESFORCE_QUERY_ALL, SALESFORCE_TOOLING_QUERY, SALESFORCE_GET_ACCOUNT, SALESFORCE_GET_CONTACT, SALESFORCE_SEARCH_LEADS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Salesforce tools handle CRM records, contacts, and leads just like the expected Airtable tool, simply within a different CRM platform.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `SALESFORCE_RUN_SOQL_QUERY`

#### Task 22 — Inspect source code, manage files, and search code in GitHub

- **Asked:** `search github repositories pull requests issues workflows`
- **Needed:** `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_SEARCH_CODE`
- **Got:** primary: GMAIL_FETCH_EMAILS, GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY
  related: GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, GITHUB_GET_A_WORKFLOW_RUN, GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN, GITHUB_DOWNLOAD_WORKFLOW_RUN_LOGS, GITHUB_LIST_REPOSITORY_WORKFLOWS
- **What went wrong:** The query is a broad set of keywords related to GitHub general features, whereas the tool is specifically for atomically committing multiple files using the Git Data API.
- **The agent retried this step 2 times:**
    - attempt 1: `search github repositories pull requests issues workflows` → `GMAIL_FETCH_EMAILS`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
    - attempt 1: `list github repositories` → `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_LIST_REPOSITORY_ISSUES`
- **Did it run one of the returned tools?** `GMAIL_FETCH_EMAILS`, `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`

#### Task 27 — Create new folders in the destination

- **Asked:** `list folders in Google Drive`
- **Needed:** `GOOGLEDRIVE_CREATE_FOLDER`
- **Got:** primary: GOOGLEDRIVE_FIND_FILE
  related: GOOGLEDRIVE_LIST_SHARED_DRIVES, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_FIND_FOLDER, GOOGLEDRIVE_LIST_CHILDREN_V2, GOOGLEDRIVE_GET_ABOUT
- **What went wrong:** The query asks to list folders, whereas the tool's specific action is to create a new folder.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GOOGLEDRIVE_FIND_FILE`

#### Task 28 — Generate AI text-to-speech audio for the video

- **Asked:** `generate AI video voice`
- **Needed:** `ELEVENLABS_TEXT_TO_SPEECH`
- **Got:** primary: GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO
  related: GEMINI_GENERATE_IMAGE, HEYGEN_V2_TEMPLATES, HEYGEN_V2_VOICES, HEYGEN_V2_VIDEO_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS
- **What went wrong:** search answered the query as written -- HEYGEN_V2_VOICES does what it asked; the step needed something else. The results successfully cover both video generation using AI and AI voice creation through the Gemini and HeyGen tool integrations.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GEMINI_GENERATE_VIDEOS`

#### Task 30 — Collect recent email activity from Outlook mailbox

- **Asked:** `search emails or get messages`
- **Needed:** `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_SEARCH_MESSAGES`
- **Got:** primary: GMAIL_FETCH_EMAILS, GMAIL_LIST_DRAFTS
  related: GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, GMAIL_SEND_DRAFT, GMAIL_UPDATE_DRAFT, GMAIL_GET_DRAFT, GMAIL_DELETE_DRAFT, GMAIL_CREATE_EMAIL_DRAFT
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Gmail tools perform the same email retrieval and messaging tasks as the expected Outlook tool, just within a different email service.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GMAIL_FETCH_EMAILS`

#### Task 30 — Collect social page activity and posts from Facebook

- **Asked:** `social media page activity or posts`
- **Needed:** `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`
- **Got:** primary: LINKEDIN_GET_COMPANY_INFO
  related: LINKEDIN_GET_POST_CONTENT, LINKEDIN_LIST_REACTIONS, LINKEDIN_GET_MY_INFO, LINKEDIN_GET_ORG_PAGE_STATS, LINKEDIN_GET_SHARE_STATS
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- Both tools retrieve activity and posts from an online social media page or company profile.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.

#### Task 31 — Create and manage tasks or reminders

- **Asked:** `create task or reminder`
- **Needed:** `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`
- **Got:** primary: NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_INSERT_ROW_DATABASE
  related: NOTION_UPSERT_ROW_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_LIST_USERS, NOTION_INSERT_ROW_FROM_NL, NOTION_FETCH_ROW
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Notion tools allow creating structured entries and managing databases, which serves a similar organizational and record-keeping function as creating tasks or reminders.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.

#### Task 51 — Fetch and annotate support-thread evidence

- **Asked:** `fetch support threads or messages`
- **Needed:** `PLAIN_RUN_GRAPHQL_QUERY`
- **Got:** primary: GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID
  related: GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, GMAIL_LIST_THREADS, GMAIL_REPLY_TO_THREAD, GMAIL_GET_ATTACHMENT
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Gmail tools perform the same fundamental task of retrieving communication threads and messages as requested by the query, just in an email application instead of the expected platform.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GMAIL_FETCH_EMAILS`

#### Task 53 — Search for and discover relevant spreadsheets

- **Asked:** `find spreadsheet with short link inventory`
- **Needed:** `GOOGLESHEETS_SEARCH_SPREADSHEETS`
- **Got:** primary: GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_BATCH_GET
  related: GOOGLEDRIVE_FIND_FOLDER, GOOGLEDRIVE_LIST_CHILDREN_V2, GOOGLEDRIVE_DOWNLOAD_FILE, GOOGLESHEETS_VALUES_GET
- **What went wrong:** search answered the query as written -- GOOGLEDRIVE_FIND_FILE does what it asked; the step needed something else. The top results include tools to find files and read Google Sheets, which fully covers the request to find a spreadsheet containing short link inventory.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GOOGLEDRIVE_FIND_FILE`

#### Task 64 — Gather marketing performance data from advertising platforms

- **Asked:** `get marketing performance data`
- **Needed:** `GOOGLEADS_SEARCH_STREAM_GAQL`
- **Got:** primary: METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS, LINKEDIN_ADS_GET_AD_ANALYTICS
  related: METAADS_LIST_BUSINESS_AD_ACCOUNTS, METAADS_LIST_CLIENT_AD_ACCOUNTS, METAADS_GET_OBJECT, METAADS_READ_ADSETS, METAADS_GET_USER, METAADS_LIST_ADS, LINKEDIN_ADS_SEARCH_CAMPAIGNS, LINKEDIN_ADS_GET_AD_ACCOUNT, LINKEDIN_ADS_SEARCH_AD_ACCOUNTS, LINKEDIN_ADS_GET_TARGETING_ENTITIES, LINKEDIN_ADS_GET_TARGETING_FACETS, LINKEDIN_ADS_SEARCH_CREATIVES
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned tools retrieve marketing performance data and ad insights from alternative platforms like Meta and LinkedIn, fulfilling the query's general intent using different applications.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `METAADS_GET_AD_ACCOUNTS`

#### Task 70 — Trigger and monitor GitHub deployment workflows

- **Asked:** `create vercel deployment`
- **Needed:** `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`
- **Got:** primary: VERCEL_CREATE_PROJECT2, VERCEL_CREATE_NEW_DEPLOYMENT, VERCEL_GET_DEPLOYMENT
  related: VERCEL_GET_PROJECTS, VERCEL_GET_DEPLOYMENTS, VERCEL_ADD_ENVIRONMENT_VARIABLE, VERCEL_GET_DEPLOYMENT_EVENTS2, VERCEL_GET_DEPLOYMENT_LOGS2, VERCEL_LIST_DEPLOYMENT_CHECKS
- **What went wrong:** query names vercel but the step needs github
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** No — it ran nothing for this step.

#### Task 83 — Inspect related due-diligence email context

- **Asked:** `search emails or messages for due diligence`
- **Needed:** `OUTLOOK_GET_MESSAGE`, `OUTLOOK_SEARCH_MESSAGES`
- **Got:** primary: GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID
  related: GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, GMAIL_LIST_THREADS, GMAIL_LIST_LABELS, GMAIL_REPLY_TO_THREAD, GMAIL_BATCH_MODIFY_MESSAGES, GMAIL_CREATE_EMAIL_DRAFT
- **What went wrong:** query named no application; search returned an equivalent tool from another one -- The returned Gmail tools search emails and messages for due diligence just like the expected Outlook tools, simply using a different email provider.
- **Did the agent retry?** No — it accepted the first result for this step and moved on.
- **Did it run one of the returned tools?** `GMAIL_FETCH_EMAILS`

#### Task 87 — Archive or clean up Notion pages, blocks, or databases during reorganization

- **Asked:** `search notion databases or pages`
- **Needed:** `NOTION_DELETE_BLOCK`
- **Got:** primary: NOTION_SEARCH_NOTION_PAGE
  related: NOTION_FETCH_DATA, NOTION_RETRIEVE_PAGE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_FETCH_DATABASE, NOTION_GET_PAGE_MARKDOWN, NOTION_FETCH_ALL_BLOCK_CONTENTS
- **What went wrong:** The query asks to search for databases or pages, whereas the target tool performs the completely different action of deleting or archiving a block.
- **The agent retried this step 2 times:**
    - attempt 1: `search notion databases or pages` → `NOTION_SEARCH_NOTION_PAGE`
    - attempt 1: `fetch all notion data or list workspace items` → `NOTION_FETCH_DATA`, `NOTION_SEARCH_NOTION_PAGE`
- **Did it run one of the returned tools?** `NOTION_SEARCH_NOTION_PAGE`, `NOTION_FETCH_DATA`

### No tool exists for it (21)

Nothing in the catalogue does this, so nobody could have found it.

| Task | Capability with no tool behind it |
|---|---|
| 1 | Assess payment link feasibility |
| 1 | Verify the assets remain inert |
| 3 | Programmatically process and modify the spreadsheet workbook to add comparison summary worksheets/sections |
| 7 | Interact with and aggregate signals from LinkedIn |
| 8 | Retrieve public video transcript data for building and updating the knowledge base |
| 8 | Mark incomplete archive documents when transcript retrieval fails |
| 9 | Create and export downloadable presentation content |
| 11 | Check queue and system state files |
| 12 | Perform automation-maintenance operations on an automation platform |
| 29 | Notify collaborators regarding updates or workflows |
| 32 | Manage Discord roles and server interactions |
| 58 | Modify, commit, and push changes to the GitHub repository |
| 60 | Prepare and import leads into an Instantly campaign |
| 67 | Consolidate duplicate contact data |
| 69 | Retrieve backlink and link-equity signal data |
| 77 | Perform keyword research and targeting analysis for search campaigns |
| 82 | Cluster remaining unread emails for triage |
| 89 | Inspect meeting-booking setup |
| 94 | Update ad set targeting, pause objects, create custom audiences, and add exclusions |
| 94 | Retrieve pixel data |
| 96 | Run smoke tests in the local or remote environment |

---

## How much to trust these numbers

**Safe to quote as-is.** These come from set membership, with no judgement involved:

- 71 delivered only in `related`
- 39 never searched for by the agent
- 21 capabilities with no tool behind them

**Quote with the case list attached.** Splitting the rest between *the query was too vague* and *search should have found it* is a reading of the evidence, not a measurement. It was revised five times while this analysis was built — 19 to 11 to 5 to 1 to 2 to 4 — moving in both directions as each rule was corrected. Two corrections came from cases spotted by hand: search was being blamed for not returning Cloudflare tools to a query about Vercel, and Sheets tools to a query about calendar events. A later over-correction then excused a genuine GitHub miss.

Of the 5 recall failures, **0** rests on deterministic evidence — Composio's own `readOnlyHint` tags proving nothing returned could perform the change the query asked for. The others rest on LLM votes and are individually arguable.

**How each verdict was reached.** Deterministic checks run first, from Composio's own toolkit and read-only metadata: a query naming one application cannot be blamed for not returning another's tools, and a query asking to create something cannot be satisfied by read-only results. Only what those cannot settle goes to an LLM, asked a concrete question about a named tool and answered by a majority of three votes.

