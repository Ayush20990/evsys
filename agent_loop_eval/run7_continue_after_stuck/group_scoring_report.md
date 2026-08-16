# Group-based scoring — `run7_continue_after_stuck`

Requirement groups replace the flat reference list: alternatives share a group, distinct
capabilities get separate groups, and logged-but-unnecessary tools are dropped. A group is
satisfied if search surfaced ANY tool in it. See the module docstring for why flat recall
is biased in both directions.

## Summary

- **Tasks scored:** 20
- **Requirement groups:** 84 (from 229 logged tools; 67 dropped as not required)
- **Strict group recall:** 56/84 (67%)
- **Judged group recall:** 63/84 (75%)
- **Groups hit in `primary`:** 39/84 (46%)
- **Flat union recall, for comparison:** 119/229 (52%)

Judged recall is the honest headline: strict recall still misses valid alternatives that
search returned but the logged list never named.

## Per task

| Task | Queries | Groups | Strict | Judged | Primary | Flat union | Dropped |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 4 | 3/4 | 3/4 | 2/4 | 8/10 | 1 |
| 2 | 2 | 3 | 3/3 | 3/3 | 2/3 | 6/6 | 0 |
| 3 | 2 | 5 | 4/5 | 4/5 | 2/5 | 4/4 | 0 |
| 4 | 5 | 5 | 3/5 | 3/5 | 2/5 | 8/10 | 5 |
| 5 | 5 | 6 | 5/6 | 5/6 | 4/6 | 13/17 | 1 |
| 6 | 4 | 3 | 2/3 | 3/3 | 2/3 | 6/11 | 1 |
| 7 | 6 | 4 | 2/4 | 2/4 | 2/4 | 8/23 | 3 |
| 8 | 4 | 2 | 1/2 | 2/2 | 0/2 | 1/1 | 0 |
| 9 | 3 | 4 | 2/4 | 3/4 | 2/4 | 3/4 | 0 |
| 10 | 6 | 5 | 4/5 | 5/5 | 1/5 | 5/6 | 2 |
| 11 | 6 | 4 | 2/4 | 2/4 | 2/4 | 10/13 | 1 |
| 12 | 7 | 7 | 4/7 | 4/7 | 2/7 | 5/11 | 0 |
| 13 | 3 | 3 | 1/3 | 2/3 | 1/3 | 2/13 | 8 |
| 14 | 2 | 3 | 3/3 | 3/3 | 2/3 | 4/9 | 4 |
| 15 | 3 | 4 | 4/4 | 4/4 | 3/4 | 8/8 | 2 |
| 16 | 4 | 5 | 3/5 | 3/5 | 3/5 | 6/25 | 15 |
| 17 | 6 | 5 | 2/5 | 2/5 | 2/5 | 9/20 | 12 |
| 18 | 2 | 2 | 1/2 | 1/2 | 1/2 | 1/5 | 3 |
| 19 | 3 | 5 | 4/5 | 4/5 | 2/5 | 4/18 | 6 |
| 20 | 5 | 5 | 3/5 | 5/5 | 2/5 | 8/15 | 3 |

## Capabilities search never delivered

Groups unmet even after judging — these are the real retrieval failures.

**Task 1**
- Assess payment-link feasibility — expected _(nothing listed provided it)_
  - judge: None of the returned HubSpot tools provide the capability to assess payment-link feasibility.

**Task 3**
- Programmatically process and add comparison summary worksheets to the spreadsheet — expected _(nothing listed provided it)_
  - judge: None of the returned OneDrive tools provide the capability to programmatically process and add comparison summary worksheets to a spreadsheet.

**Task 4**
- Add a first comment to a LinkedIn post — expected `LINKEDIN_CREATE_COMMENT_ON_POST`
  - judge: None of the returned LinkedIn tools provide the capability to add a comment to an existing post.
- Add a comment or update status/logs on a Trello card — expected `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
  - judge: None of the returned tools provide the capability to add comments to a Trello card, as the available update tools only modify card attributes like name, description, due date, or labels.

**Task 5**
- scan recent email threads in Gmail — expected `GMAIL_LIST_THREADS`, `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - judge: None of the returned Gmail tools provide the ability to scan or fetch recent email threads to compare against CRM records.

**Task 7**
- Configure, receive, and send SMS messages — expected `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_CREATE_SMS_SEND`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_GET_SMS_HISTORY`, `CLICKSEND_GET_SMS_INBOUND`, `CLICKSEND_GET_SMS_RECEIPTS`
  - judge: The returned Brevo tools only support creating SMS marketing campaigns and managing contacts, not configuring, receiving, or sending individual SMS messages as required.
- Access and interact with LinkedIn productivity signals — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide functionality to access or interact with LinkedIn productivity signals.

**Task 9**
- Search and retrieve stock images for marketing assets — expected `COMPOSIO_SEARCH_IMAGE`
  - judge: The available tools only generate images via AI or manage Gmail and Google Slides, but do not provide the capability to search and retrieve stock images.

**Task 11**
- Coordinate operational tasks and communicate via Discord — expected `DISCORDBOT_LIST_MESSAGES`
  - judge: None of the returned Discord tools provide the capability to list messages from a channel, which was required for coordinating operational tasks.
- Check queue and system state files — expected _(nothing listed provided it)_
  - judge: None of the returned OneDrive, Discord, or Gmail tools provide the capability to check queue and system state files.

**Task 12**
- Retrieve emails for project management and automation maintenance — expected `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
  - judge: None of the returned Gmail tools provide the capability to fetch or retrieve emails.
- Search or list Slack messages and users for chat-based operations — expected `SLACK_SEARCH_MESSAGES`, `SLACK_LIST_ALL_USERS`
  - judge: None of the returned Slack tools provide the capability to search or list Slack messages.
- Perform automation-platform maintenance operations — expected _(nothing listed provided it)_
  - judge: None of the returned tools provide automation-platform maintenance operations as required by the task.

**Task 13**
- Manage email contact lists and audiences — expected `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - judge: None of the returned tools provide the functionality to manage or create email contact lists and audiences.

**Task 16**
- Audit Google Analytics data and reports — expected `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_LIST_DATA_STREAMS`
  - judge: None of the returned Google Search Console or Vercel tools provide the capability to audit Google Analytics data and reports.
- Investigate hosting and deployment state via Cloudflare zones and DNS — expected `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - judge: None of the returned Cloudflare or other tools provide the capability to list Cloudflare zones and DNS records required to investigate hosting and deployment state via Cloudflare.

**Task 17**
- Prepare and upload supporting media — expected `HEYGEN_UPLOAD_ASSET`
  - judge: None of the returned HeyGen tools provide the capability to prepare and upload supporting media.
- Publish content to social media — expected `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - judge: None of the returned tools provide the capability to publish content to social media.
- Read and update a booking schedule — expected `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - judge: Although Cal.com tools like CAL_POST_NEW_BOOKING_REQUEST and CAL_RESCHEDULE_BOOKING_BY_UID were returned, there were no Google Sheets tools provided to read and update a spreadsheet-based booking schedule as required by the task.

**Task 18**
- Search and extract recent job listings from web sources or job boards — expected `BROWSER_TOOL_CREATE_TASK`
  - judge: None of the available search or fetch tools are capable of directly searching, parsing, and extracting structured job listings from job boards as required by the task.

**Task 19**
- Retrieve, create, or manage resume documents stored in Google Docs or Google Drive — expected `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_UPLOAD_FROM_URL`
  - judge: None of the returned tools provide the capability to retrieve, create, or manage resume documents stored in Google Docs or Google Drive.

## Alternatives credited by the judge

Groups no expected tool matched, but a tool search actually returned did the job.
Each of these is a flat-recall false negative.

**Task 6**
- Update Salesforce records (campaign attendance statuses, lead activity) — satisfied by `SALESFORCE_UPDATE_LEAD`
  - The SALESFORCE_UPDATE_LEAD tool provides the capability to update existing lead records in Salesforce.

**Task 8**
- Retrieve public video transcript data — satisfied by `SUPADATA_GET_TRANSCRIPT`
  - The SUPADATA_GET_TRANSCRIPT tool explicitly retrieves transcripts from YouTube and other video platforms, fulfilling the needed capability.

**Task 9**
- Create or export downloadable presentation content — satisfied by `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN`
  - The GOOGLESLIDES_CREATE_SLIDES_MARKDOWN tool directly enables the creation of presentation content from markdown text.

**Task 10**
- Record customer payments — satisfied by `QUICKBOOKS_CREATE_PAYMENT`
  - The QUICKBOOKS_CREATE_PAYMENT tool directly matches the required capability by providing functionality to create a payment record in QuickBooks Online for customer payments against invoices.

**Task 13**
- Send outreach emails for marketing and press engagement — satisfied by `GMAIL_SEND_DRAFT`
  - Although the expected tool was GMAIL_SEND_EMAIL, GMAIL_SEND_DRAFT fulfills the capability of sending outreach emails by sending a prepared draft to the recipients.

**Task 20**
- Access and manage QuickBooks accounting and billing records — satisfied by `QUICKBOOKS_QUERY_ENTITIES`
  - The QUICKBOOKS_QUERY_ENTITIES tool (along with other QuickBooks tools returned) provides the necessary capability to access and manage QuickBooks accounting and billing records.
- Search, access, and manage files in Google Drive — satisfied by `GOOGLEDRIVE_FIND_FILE`
  - The GOOGLEDRIVE_FIND_FILE tool provides comprehensive search, access, and file discovery capabilities across Google Drive.

