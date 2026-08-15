# Group-based scoring — `run6_descriptions_20tasks`

Requirement groups replace the flat reference list: alternatives share a group, distinct
capabilities get separate groups, and logged-but-unnecessary tools are dropped. A group is
satisfied if search surfaced ANY tool in it. See the module docstring for why flat recall
is biased in both directions.

## Summary

- **Tasks scored:** 20
- **Requirement groups:** 88 (from 229 logged tools; 69 dropped as not required)
- **Strict group recall:** 54/88 (61%)
- **Judged group recall:** 62/88 (70%)
- **Groups hit in `primary`:** 40/88 (45%)
- **Flat union recall, for comparison:** 106/229 (46%)

Judged recall is the honest headline: strict recall still misses valid alternatives that
search returned but the logged list never named.

## Per task

| Task | Queries | Groups | Strict | Judged | Primary | Flat union | Dropped |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 4 | 3/4 | 3/4 | 2/4 | 8/10 | 6 |
| 2 | 3 | 3 | 3/3 | 3/3 | 3/3 | 6/6 | 0 |
| 3 | 4 | 5 | 4/5 | 4/5 | 3/5 | 4/4 | 0 |
| 4 | 4 | 5 | 2/5 | 2/5 | 2/5 | 7/10 | 5 |
| 5 | 3 | 6 | 4/6 | 5/6 | 3/6 | 9/17 | 1 |
| 6 | 4 | 4 | 3/4 | 3/4 | 2/4 | 7/11 | 2 |
| 7 | 6 | 4 | 2/4 | 3/4 | 2/4 | 7/23 | 3 |
| 8 | 3 | 3 | 1/3 | 2/3 | 1/3 | 1/1 | 0 |
| 9 | 3 | 4 | 2/4 | 4/4 | 2/4 | 3/4 | 0 |
| 10 | 5 | 5 | 3/5 | 4/5 | 1/5 | 3/6 | 2 |
| 11 | 5 | 3 | 1/3 | 1/3 | 1/3 | 10/13 | 1 |
| 12 | 3 | 7 | 4/7 | 4/7 | 2/7 | 5/11 | 0 |
| 13 | 3 | 4 | 3/4 | 3/4 | 2/4 | 3/13 | 4 |
| 14 | 2 | 3 | 3/3 | 3/3 | 2/3 | 4/9 | 2 |
| 15 | 3 | 5 | 4/5 | 5/5 | 1/5 | 6/8 | 2 |
| 16 | 4 | 5 | 3/5 | 3/5 | 3/5 | 6/25 | 15 |
| 17 | 5 | 6 | 3/6 | 3/6 | 3/6 | 7/20 | 10 |
| 18 | 2 | 2 | 1/2 | 1/2 | 1/2 | 1/5 | 3 |
| 19 | 3 | 3 | 2/3 | 2/3 | 2/3 | 4/18 | 10 |
| 20 | 4 | 7 | 3/7 | 4/7 | 2/7 | 5/15 | 3 |

## Capabilities search never delivered

Groups unmet even after judging — these are the real retrieval failures.

**Task 1**
- Assess payment link feasibility — expected _(nothing listed provided it)_
  - judge: None of the returned HubSpot tools provide the capability to assess payment-link feasibility.

**Task 3**
- Programmatically parse, modify, and add comparison summary worksheets to the Excel workbook — expected _(nothing listed provided it)_
  - judge: None of the returned OneDrive tools provide the capability to programmatically parse, modify, or add worksheets to an Excel workbook.

**Task 4**
- Add a comment/log to a Trello card — expected `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
  - judge: None of the returned Trello tools provide the capability to add a comment or log to a Trello card, as all available Trello tools are strictly for retrieval and reading.
- Update Trello card status by moving it to another list — expected `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
  - judge: None of the returned Trello tools provide the capability to update or move a card to another list.
- Adjust the Trello board workflow structure by adding a new list — expected `TRELLO_ADD_LISTS`
  - judge: None of the returned Trello tools provide the capability to create or add a new list to a board workflow structure.

**Task 5**
- fetch and read Gmail emails and threads — expected `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`, `GMAIL_LIST_THREADS`
  - judge: None of the returned Gmail tools provide the capability to fetch and read incoming email messages or threads.

**Task 6**
- Bulk create multiple Salesforce records efficiently — expected `SALESFORCE_POST_COMPOSITE_SOBJECTS`
  - judge: None of the returned tools support efficiently bulk creating multiple Salesforce records in a single operation.

**Task 7**
- Interact with or retrieve signals from LinkedIn — expected _(nothing listed provided it)_
  - judge: Although LinkedIn tools were returned, none of them provide the capability to retrieve or read personal productivity signals, posts, or messages from LinkedIn, as they are limited to creating shares and comments.

**Task 8**
- Manage and update archive documents to mark them as incomplete when transcript retrieval fails — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide the capability to manage and update archive documents to mark them as incomplete when transcript retrieval fails.

**Task 10**
- Post corrected ledger activity and create adjustment journal entries — expected `QUICKBOOKS_CREATE_JOURNAL_ENTRY`
  - judge: None of the returned QuickBooks tools provide the ability to create journal entries for posting corrected ledger activity or adjustments.

**Task 11**
- Read and coordinate operational messages and tasks via Discord — expected `DISCORDBOT_LIST_MESSAGES`
  - judge: Although several Discord tools were returned, none of them provide the capability to list or read messages from a channel (DISCORDBOT_LIST_MESSAGES), which is required to read and coordinate operational messages.
- Configure Gmail support labels and routing filters — expected `GMAIL_CREATE_FILTER`, `GMAIL_CREATE_LABEL`
  - judge: Although tools for listing and deleting Gmail filters and labels were returned, no tool was provided to create new Gmail support labels or routing filters.

**Task 12**
- Fetch and search email messages — expected `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - judge: None of the returned tools provide the capability to fetch and search email messages.
- Search and list users in Slack for chat and communication — expected `SLACK_LIST_ALL_USERS`, `SLACK_SEARCH_MESSAGES`
  - judge: None of the returned tools provide the capability to search and list users in Slack.
- Perform automation-maintenance operations — expected _(nothing listed provided it)_
  - judge: None of the returned Trello tools provide the capability to perform broader automation-maintenance operations.

**Task 13**
- Create and manage email contact lists and marketing audiences — expected `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - judge: None of the returned tools provide the ability to create and manage dedicated email contact lists and marketing audiences.

**Task 16**
- Audit Google Analytics data and reports — expected `GOOGLE_ANALYTICS_LIST_DATA_STREAMS`, `GOOGLE_ANALYTICS_RUN_REPORT`
  - judge: None of the returned Google Search Console, GitHub, OneDrive, or Vercel tools provide the capability to audit Google Analytics data and reports.
- Investigate hosting, deployment, and DNS configuration — expected `CLOUDFLARE_LIST_DNS_RECORDS`, `CLOUDFLARE_LIST_ZONES`
  - judge: None of the returned tools provide the ability to investigate DNS configuration or list DNS records for hosting and deployment state auditing.

**Task 17**
- Prepare and upload supporting media assets — expected `HEYGEN_UPLOAD_ASSET`
  - judge: None of the returned tools provide the HEYGEN_UPLOAD_ASSET capability needed to prepare and upload supporting media assets.
- Attempt social publishing of media — expected `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - judge: None of the returned tools provide the capability to publish media to Instagram or social platforms beyond Facebook.
- Read and update booking schedule — expected `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - judge: The returned tools only provide Google Calendar and Google Drive functionalities, which do not match the required Google Sheets capability to read and update a booking schedule.

**Task 18**
- Search and extract recent job listings from web sources or job boards — expected `BROWSER_TOOL_CREATE_TASK`
  - judge: None of the available search or fetch tools are specialized for browsing, navigating, or extracting job listing data specifically from job boards as required by the task.

**Task 19**
- Retrieve or create tailored resume documents — expected `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`
  - judge: None of the returned tools provide the capability to retrieve or create tailored resume documents via Google Drive or Google Docs.

**Task 20**
- Modify, update, and insert text content in Google Documents — expected `GOOGLEDOCS_INSERT_TEXT_ACTION`, `GOOGLEDOCS_REPLACE_ALL_TEXT`, `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`
  - judge: None of the returned Google Docs tools provide the capability to modify, update, or insert text content in a document.
- Update, write, and upsert data into Google Spreadsheets — expected `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`, `GOOGLESHEETS_VALUES_UPDATE`
  - judge: None of the returned Google Sheets tools provide the ability to update, write, or upsert data into spreadsheets; they only retrieve spreadsheet info or metadata.
- Manage and reconcile records in Zoho CRM — expected _(nothing listed provided it)_
  - judge: Although multiple Zoho CRM tools were returned to list, search, and get records or related lists, none of the provided tools support managing or updating/reconciling records in Zoho CRM.

## Alternatives credited by the judge

Groups no expected tool matched, but a tool search actually returned did the job.
Each of these is a flat-recall false negative.

**Task 5**
- update Notion page properties and status — satisfied by `NOTION_UPDATE_ROW_DATABASE`
  - The NOTION_UPDATE_ROW_DATABASE tool provides the capability to update properties and status for individual pages (rows) within a Notion database.

**Task 7**
- List, get, and manage calendar access and events — satisfied by `GOOGLECALENDAR_GET_CALENDAR`
  - The GOOGLECALENDAR_GET_CALENDAR tool provides the capability to retrieve a specific Google Calendar, satisfying the need to manage calendar access and events.

**Task 8**
- Retrieve public video transcript data for building and updating a knowledge base — satisfied by `SUPADATA_GET_TRANSCRIPT`
  - The SUPADATA_GET_TRANSCRIPT tool retrieves transcripts from videos on supported platforms like YouTube, directly matching the needed capability.

**Task 9**
- Search and retrieve stock images for marketing assets — satisfied by `GEMINI_GENERATE_IMAGE`
  - The GEMINI_GENERATE_IMAGE tool generates images from text prompts, which effectively fulfills the capability to retrieve or create stock/generative images for marketing assets.
- Provide downloadable presentation content and organize final deliverables — satisfied by `GAMMA_LIST_FOLDERS`
  - The GAMMA_LIST_FOLDERS tool provides the workspace folder retrieval capability needed to organize final presentation deliverables.

**Task 10**
- Record a customer payment — satisfied by `QUICKBOOKS_CREATE_PAYMENT`
  - The QUICKBOOKS_CREATE_PAYMENT tool explicitly records payment from customers against invoices in QuickBooks, directly matching the required capability.

**Task 15**
- Upload and persist invoice attachments to cloud storage — satisfied by `GOOGLEDRIVE_UPLOAD_FILE`
  - GOOGLEDRIVE_UPLOAD_FILE allows uploading and persisting invoice attachments to cloud storage (Google Drive).

**Task 20**
- Manage and reconcile records in QuickBooks — satisfied by `QUICKBOOKS_EXECUTE_BATCH_OPERATION`
  - The QUICKBOOKS_EXECUTE_BATCH_OPERATION tool allows creating, updating, deleting, and querying QuickBooks entities to manage and reconcile records.

