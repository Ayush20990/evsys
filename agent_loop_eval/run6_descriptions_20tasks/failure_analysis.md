# Failure analysis — `run6_descriptions_20tasks`

26 capabilities went unmet out of 88 required (30%), after the judge credited valid alternatives.

## Failures by cause

| Cause | Count | What it means | Who fixes it |
|---|---:|---|---|
| `never-returned` | 20 | no expected tool appeared in any search result | search recall |
| `catalogue-gap` | 6 | the task needs a capability no logged tool provides | product/catalogue, not search |

## Delivered, but not recommended

14 capabilities were satisfied ONLY by a tool in `related` — search held the
right tool and never promoted it. An agent acting on the primary recommendation would
have missed these, so in practice they sit between a hit and a miss.

| Task | Capability | Found only in `related` |
|---|---|---|
| 1 | Create a review-only automated confirmation email | `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION` |
| 3 | Upload or update the modified workbook back to OneDrive | `ONE_DRIVE_UPDATE_FILE_CONTENT` |
| 5 | query and read Notion databases and pages | `NOTION_FETCH_DATABASE`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_SEARCH_NOTION_PAGE` |
| 6 | Update existing Salesforce records (e.g., campaign attendance statuses or lead details) | `SALESFORCE_SOBJECT_ROWS_UPDATE` |
| 10 | Modify, delete, or undo incorrect ledger entries and transactions | `QUICKBOOKS_EXECUTE_BATCH_OPERATION` |
| 10 | Verify financial reports | `QUICKBOOKS_GET_REPORTS` |
| 12 | Add comments to Trello cards | `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD` |
| 12 | Perform broader project management and search across Trello boards | `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH` |
| 13 | Audit website search performance, indexing, and sitemaps | `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` |
| 14 | Fetch webpage content from job listings or search result URLs | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |
| 15 | Retrieve invoice attachments from emails | `GMAIL_GET_ATTACHMENT` |
| 15 | Read and update spreadsheet ledgers and verify totals | `GOOGLESHEETS_UPDATE_VALUES_BATCH` |
| 15 | Update or label processed email messages | `GMAIL_BATCH_MODIFY_MESSAGES` |
| 20 | Discover metadata and fields in Zoho CRM | `ZOHO_GET_MODULE_FIELDS` |

## Every unmet capability

### Task 1
> Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify th

- **Assess payment link feasibility** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned HubSpot tools provide the capability to assess payment-link feasibility.

### Task 3
> Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.

- **Programmatically parse, modify, and add comparison summary worksheets to the Excel workbook** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned OneDrive tools provide the capability to programmatically parse, modify, or add worksheets to an Excel workbook.

### Task 4
> Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.

- **Add a comment/log to a Trello card** — `never-returned`
  - expected: `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Trello tools provide the capability to add a comment or log to a Trello card, as all available Trello tools are strictly for retrieval and reading.
- **Update Trello card status by moving it to another list** — `never-returned`
  - expected: `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Trello tools provide the capability to update or move a card to another list.
- **Adjust the Trello board workflow structure by adding a new list** — `never-returned`
  - expected: `TRELLO_ADD_LISTS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Trello tools provide the capability to create or add a new list to a board workflow structure.

### Task 5
> Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, a

- **fetch and read Gmail emails and threads** — `never-returned`
  - expected: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`, `GMAIL_LIST_THREADS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Gmail tools provide the capability to fetch and read incoming email messages or threads.

### Task 6
> Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.

- **Bulk create multiple Salesforce records efficiently** — `never-returned`
  - expected: `SALESFORCE_POST_COMPOSITE_SOBJECTS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools support efficiently bulk creating multiple Salesforce records in a single operation.

### Task 7
> Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.

- **Interact with or retrieve signals from LinkedIn** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: Although LinkedIn tools were returned, none of them provide the capability to retrieve or read personal productivity signals, posts, or messages from LinkedIn, as they are limited to creating shares and comments.

### Task 8
> Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.

- **Manage and update archive documents to mark them as incomplete when transcript retrieval fails** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned tools provide the capability to manage and update archive documents to mark them as incomplete when transcript retrieval fails.

### Task 10
> Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, rec

- **Post corrected ledger activity and create adjustment journal entries** — `never-returned`
  - expected: `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned QuickBooks tools provide the ability to create journal entries for posting corrected ledger activity or adjustments.

### Task 11
> Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure

- **Read and coordinate operational messages and tasks via Discord** — `never-returned`
  - expected: `DISCORDBOT_LIST_MESSAGES`
  - no expected tool appeared anywhere in any search result
  - judge: Although several Discord tools were returned, none of them provide the capability to list or read messages from a channel (DISCORDBOT_LIST_MESSAGES), which is required to read and coordinate operational messages.
- **Configure Gmail support labels and routing filters** — `never-returned`
  - expected: `GMAIL_CREATE_FILTER`, `GMAIL_CREATE_LABEL`
  - no expected tool appeared anywhere in any search result
  - judge: Although tools for listing and deleting Gmail filters and labels were returned, no tool was provided to create new Gmail support labels or routing filters.

### Task 12
> Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.

- **Fetch and search email messages** — `never-returned`
  - expected: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to fetch and search email messages.
- **Search and list users in Slack for chat and communication** — `never-returned`
  - expected: `SLACK_LIST_ALL_USERS`, `SLACK_SEARCH_MESSAGES`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to search and list users in Slack.
- **Perform automation-maintenance operations** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: None of the returned Trello tools provide the capability to perform broader automation-maintenance operations.

### Task 13
> Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.

- **Create and manage email contact lists and marketing audiences** — `never-returned`
  - expected: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the ability to create and manage dedicated email contact lists and marketing audiences.

### Task 16
> Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate host

- **Audit Google Analytics data and reports** — `never-returned`
  - expected: `GOOGLE_ANALYTICS_LIST_DATA_STREAMS`, `GOOGLE_ANALYTICS_RUN_REPORT`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Search Console, GitHub, OneDrive, or Vercel tools provide the capability to audit Google Analytics data and reports.
- **Investigate hosting, deployment, and DNS configuration** — `never-returned`
  - expected: `CLOUDFLARE_LIST_DNS_RECORDS`, `CLOUDFLARE_LIST_ZONES`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the ability to investigate DNS configuration or list DNS records for hosting and deployment state auditing.

### Task 17
> Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.

- **Prepare and upload supporting media assets** — `never-returned`
  - expected: `HEYGEN_UPLOAD_ASSET`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the HEYGEN_UPLOAD_ASSET capability needed to prepare and upload supporting media assets.
- **Attempt social publishing of media** — `never-returned`
  - expected: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to publish media to Instagram or social platforms beyond Facebook.
- **Read and update booking schedule** — `never-returned`
  - expected: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - no expected tool appeared anywhere in any search result
  - judge: The returned tools only provide Google Calendar and Google Drive functionalities, which do not match the required Google Sheets capability to read and update a booking schedule.

### Task 18
> Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.

- **Search and extract recent job listings from web sources or job boards** — `never-returned`
  - expected: `BROWSER_TOOL_CREATE_TASK`
  - no expected tool appeared anywhere in any search result
  - judge: None of the available search or fetch tools are specialized for browsing, navigating, or extracting job listing data specifically from job boards as required by the task.

### Task 19
> Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.

- **Retrieve or create tailored resume documents** — `never-returned`
  - expected: `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned tools provide the capability to retrieve or create tailored resume documents via Google Drive or Google Docs.

### Task 20
> Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records

- **Modify, update, and insert text content in Google Documents** — `never-returned`
  - expected: `GOOGLEDOCS_INSERT_TEXT_ACTION`, `GOOGLEDOCS_REPLACE_ALL_TEXT`, `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Docs tools provide the capability to modify, update, or insert text content in a document.
- **Update, write, and upsert data into Google Spreadsheets** — `never-returned`
  - expected: `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`, `GOOGLESHEETS_VALUES_UPDATE`
  - no expected tool appeared anywhere in any search result
  - judge: None of the returned Google Sheets tools provide the ability to update, write, or upsert data into spreadsheets; they only retrieve spreadsheet info or metadata.
- **Manage and reconcile records in Zoho CRM** — `catalogue-gap`
  - expected: _(nothing listed)_
  - the task needs this, and no tool in the logged list provided it either
  - judge: Although multiple Zoho CRM tools were returned to list, search, and get records or related lists, none of the provided tools support managing or updating/reconciling records in Zoho CRM.

