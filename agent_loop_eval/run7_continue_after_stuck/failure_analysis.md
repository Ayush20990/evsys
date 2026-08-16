# Failure analysis — `run7_continue_after_stuck`

21 capabilities went unmet out of 84 required (25%), after the judge credited valid alternatives.

## Failures by cause

| Cause | Count | What it means | Who fixes it |
|---|---:|---|---|
| `never-returned` | 16 | no expected tool appeared in any search result | search recall |
| `catalogue-gap` | 5 | the task needs a capability no logged tool provides | product/catalogue, not search |

## Delivered, but not recommended

17 capabilities were satisfied ONLY by a tool in `related` — search held the
right tool and never promoted it. An agent acting on the primary recommendation would
have missed these, so in practice they sit between a hit and a miss.

| Task | Capability | Found only in `related` |
|---|---|---|
| 1 | Find and clone/create/update marketing emails for the confirmation message | `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION`, `HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL` |
| 2 | Verify Notion content after writing | `NOTION_GET_PAGE_MARKDOWN`, `NOTION_RETRIEVE_PAGE` |
| 3 | Download the spreadsheet file from OneDrive | `ONE_DRIVE_DOWNLOAD_FILE` |
| 3 | Upload the modified spreadsheet back to OneDrive to update the file content | `ONE_DRIVE_UPDATE_FILE_CONTENT` |
| 4 | Move a Trello card to a different list | `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD` |
| 5 | write evidence-supported CRM status updates in Notion | `NOTION_UPDATE_PAGE` |
| 8 | Insert summarized entries into existing Google Docs | `GOOGLEDOCS_INSERT_TEXT_ACTION` |
| 10 | Query existing QuickBooks transactions and ledger entities | `QUICKBOOKS_QUERY_ENTITIES` |
| 10 | Modify, delete, or undo incorrect ledger entries and transactions | `QUICKBOOKS_EXECUTE_BATCH_OPERATION` |
| 10 | Retrieve and verify financial reports | `QUICKBOOKS_GET_REPORTS` |
| 12 | Add comments to Trello cards | `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD` |
| 12 | Search or retrieve Trello cards and boards | `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH` |
| 14 | Fetch and read job listing page contents | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |
| 15 | Label or update processed email messages | `GMAIL_BATCH_MODIFY_MESSAGES` |
| 19 | Fetch and extract text or content from job listing web pages | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |
| 19 | Read or check existing emails in Gmail | `GMAIL_FETCH_EMAILS` |
| 20 | Inspect and manage Zoho CRM module metadata and records | `ZOHO_GET_MODULE_FIELDS` |

## Every unmet capability

### Task 1
> Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th

- **Assess payment-link feasibility** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned HubSpot tools provide the capability to assess payment-link feasibility.

### Task 3
> Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.

- **Programmatically process and add comparison summary worksheets to the spreadsheet** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned OneDrive tools provide the capability to programmatically process and add comparison summary worksheets to a spreadsheet.

### Task 4
> Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.

- **Add a first comment to a LinkedIn post** — `never-returned`
  - expected: `LINKEDIN_CREATE_COMMENT_ON_POST`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned LinkedIn tools provide the capability to add a comment to an existing post.
- **Add a comment or update status/logs on a Trello card** — `never-returned`
  - expected: `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to add comments to a Trello card, as the available update tools only modify card attributes like name, description, due date, or labels.

### Task 5
> Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a

- **scan recent email threads in Gmail** — `never-returned`
  - expected: `GMAIL_LIST_THREADS`, `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Gmail tools provide the ability to scan or fetch recent email threads to compare against CRM records.

### Task 7
> Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.

- **Configure, receive, and send SMS messages** — `never-returned`
  - expected: `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_CREATE_SMS_SEND`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_GET_SMS_HISTORY`, `CLICKSEND_GET_SMS_INBOUND`, `CLICKSEND_GET_SMS_RECEIPTS`
  - no expected tool appeared anywhere in any search result
  - judge: The returned Brevo tools only support creating SMS marketing campaigns and managing contacts, not configuring, receiving, or sending individual SMS messages as required.
- **Access and interact with LinkedIn productivity signals** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide functionality to access or interact with LinkedIn productivity signals.

### Task 9
> Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.

- **Search and retrieve stock images for marketing assets** — `never-returned`
  - expected: `COMPOSIO_SEARCH_IMAGE`
  - no expected tool appeared anywhere in any search result
  - judge: The available tools only generate images via AI or manage Gmail and Google Slides, but do not provide the capability to search and retrieve stock images.

### Task 11
> Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure

- **Coordinate operational tasks and communicate via Discord** — `never-returned`
  - expected: `DISCORDBOT_LIST_MESSAGES`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Discord tools provide the capability to list messages from a channel, which was required for coordinating operational tasks.
- **Check queue and system state files** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned OneDrive, Discord, or Gmail tools provide the capability to check queue and system state files.

### Task 12
> Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.

- **Retrieve emails for project management and automation maintenance** — `never-returned`
  - expected: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Gmail tools provide the capability to fetch or retrieve emails.
- **Search or list Slack messages and users for chat-based operations** — `never-returned`
  - expected: `SLACK_SEARCH_MESSAGES`, `SLACK_LIST_ALL_USERS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Slack tools provide the capability to search or list Slack messages.
- **Perform automation-platform maintenance operations** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide automation-platform maintenance operations as required by the task.

### Task 13
> Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.

- **Manage email contact lists and audiences** — `never-returned`
  - expected: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the functionality to manage or create email contact lists and audiences.

### Task 16
> Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host

- **Audit Google Analytics data and reports** — `never-returned`
  - expected: `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_LIST_DATA_STREAMS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Search Console or Vercel tools provide the capability to audit Google Analytics data and reports.
- **Investigate hosting and deployment state via Cloudflare zones and DNS** — `never-returned`
  - expected: `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Cloudflare or other tools provide the capability to list Cloudflare zones and DNS records required to investigate hosting and deployment state via Cloudflare.

### Task 17
> Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.

- **Prepare and upload supporting media** — `never-returned`
  - expected: `HEYGEN_UPLOAD_ASSET`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned HeyGen tools provide the capability to prepare and upload supporting media.
- **Publish content to social media** — `never-returned`
  - expected: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to publish content to social media.
- **Read and update a booking schedule** — `never-returned`
  - expected: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - no expected tool appeared anywhere in any search result
  - judge: Although Cal.com tools like CAL_POST_NEW_BOOKING_REQUEST and CAL_RESCHEDULE_BOOKING_BY_UID were returned, there were no Google Sheets tools provided to read and update a spreadsheet-based booking schedule as required by the task.

### Task 18
> Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.

- **Search and extract recent job listings from web sources or job boards** — `never-returned`
  - expected: `BROWSER_TOOL_CREATE_TASK`
  - no expected tool appeared anywhere in any search result
  - judge: None of the available search or fetch tools are capable of directly searching, parsing, and extracting structured job listings from job boards as required by the task.

### Task 19
> Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.

- **Retrieve, create, or manage resume documents stored in Google Docs or Google Drive** — `never-returned`
  - expected: `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_UPLOAD_FROM_URL`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to retrieve, create, or manage resume documents stored in Google Docs or Google Drive.

