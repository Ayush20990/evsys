# Query Robustness Benchmark

## Method
Uses query-level ground truth from the primary workflow-decomposition benchmark. For the same intent, it compares explicit app mentions, implicit wording, and a paraphrase; expected tools are unchanged. This isolates search robustness from workflow decomposition.

## Summary
- **Source intents sampled:** 60
- **Variant search calls:** 180
- **Generation failures:** 0

| Variant | Queries | Any-hit rate | Avg recall | Primary-hit rate |
|---|---:|---:|---:|---:|
| explicit | 60 | 88.3% | 82.5% | 75.0% |
| implicit | 60 | 36.7% | 34.2% | 33.3% |
| paraphrase | 60 | 55.0% | 53.3% | 51.7% |

## Failure Examples
Review these alongside the original query before assigning fault to search; variants may expose query-generation ambiguity.

### workflow-001-q2-explicit — explicit, recall 0.0%
- **Query:** set up an automated review email in HubSpot for registration confirmation
- **Required:** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Missed:** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Primary returned:** `HUBSPOT_CREATE_EMAIL`

### workflow-003-q3-explicit — explicit, recall 0.0%
- **Query:** upload the revised workbook to OneDrive and verify the cloud file
- **Required:** `ONE_DRIVE_UPDATE_FILE_CONTENT`
- **Missed:** `ONE_DRIVE_UPDATE_FILE_CONTENT`
- **Primary returned:** `GOOGLEDRIVE_UPLOAD_FILE; ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### workflow-006-q1-explicit — explicit, recall 0.0%
- **Query:** look up existing contacts and leads in Salesforce
- **Required:** `SALESFORCE_SEARCH_LEADS; SALESFORCE_SEARCH_CONTACTS`
- **Missed:** `SALESFORCE_SEARCH_CONTACTS; SALESFORCE_SEARCH_LEADS`
- **Primary returned:** `SALESFORCE_RUN_SOQL_QUERY; SALESFORCE_LIST_LEADS`

### workflow-014-q2-explicit — explicit, recall 0.0%
- **Query:** fetch job posting details from https://example.com/job-listing using Web Scraper
- **Required:** `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
- **Missed:** `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
- **Primary returned:** `SCRAPE_DO_GET_PAGE; SCRAPE_DO_CREATE_ASYNC_JOB; BRIGHTDATA_LIST_WEB_UNLOCKER_ZONES; BRIGHTDATA_WEB_UNLOCKER`

### workflow-014-q3-explicit — explicit, recall 0.0%
- **Query:** email me a compiled list of software engineering jobs using Gmail
- **Required:** `GMAIL_SEND_EMAIL`
- **Missed:** `GMAIL_SEND_EMAIL`
- **Primary returned:** `DICE_MCP_SEARCH_JOBS`

### workflow-017-q4-explicit — explicit, recall 0.0%
- **Query:** check and modify booking schedule in Google Sheets
- **Required:** `GOOGLESHEETS_BATCH_GET; GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
- **Missed:** `GOOGLESHEETS_BATCH_GET; GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
- **Primary returned:** `CAL_RETRIEVE_BOOKING_DETAILS_BY_UID; CAL_EDIT_BOOKING_BY_ID; CAL_RESCHEDULE_BOOKING_BY_UID`

### workflow-018-q1-explicit — explicit, recall 0.0%
- **Query:** search LinkedIn for remote contract data engineering positions
- **Required:** `LINKEDIN_PROXY_EXECUTE`
- **Missed:** `LINKEDIN_PROXY_EXECUTE`
- **Primary returned:** `LINKEDIN_SEARCH_AD_TARGETING_ENTITIES`

### workflow-001-q2-implicit — implicit, recall 0.0%
- **Query:** create an automated review email for registration confirmation
- **Required:** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Missed:** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Primary returned:** `PENPOT_PREPARE_REGISTER_PROFILE`

### workflow-001-q3-implicit — implicit, recall 0.0%
- **Query:** Make a new workflow in a disabled state
- **Required:** `HUBSPOT_CREATE_WORKFLOW`
- **Missed:** `HUBSPOT_CREATE_WORKFLOW`
- **Primary returned:** `LINEAR_RUN_QUERY_OR_MUTATION`

### workflow-001-q4-implicit — implicit, recall 0.0%
- **Query:** set up a new data structure definition for tracking registration records
- **Required:** `HUBSPOT_CREATE_OBJECT_SCHEMA`
- **Missed:** `HUBSPOT_CREATE_OBJECT_SCHEMA`
- **Primary returned:** `STRIPE_CREATE_TAX_REGISTRATION`

### workflow-002-q2-implicit — implicit, recall 0.0%
- **Query:** create a fresh document and insert formatted sections into it
- **Required:** `NOTION_CREATE_NOTION_PAGE; NOTION_ADD_MULTIPLE_PAGE_CONTENT`
- **Missed:** `NOTION_ADD_MULTIPLE_PAGE_CONTENT; NOTION_CREATE_NOTION_PAGE`
- **Primary returned:** `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN; GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`

### workflow-002-q3-implicit — implicit, recall 0.0%
- **Query:** pull up the document text to verify the recorded details
- **Required:** `NOTION_RETRIEVE_PAGE; NOTION_GET_PAGE_MARKDOWN`
- **Missed:** `NOTION_GET_PAGE_MARKDOWN; NOTION_RETRIEVE_PAGE`
- **Primary returned:** `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`

### workflow-003-q1-implicit — implicit, recall 0.0%
- **Query:** search and locate the spreadsheet document
- **Required:** `ONE_DRIVE_SEARCH_ITEMS`
- **Missed:** `ONE_DRIVE_SEARCH_ITEMS`
- **Primary returned:** `GOOGLESHEETS_SEARCH_DEVELOPER_METADATA; GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW`

### workflow-003-q2-implicit — implicit, recall 0.0%
- **Query:** save a spreadsheet from cloud storage to local disk
- **Required:** `ONE_DRIVE_DOWNLOAD_FILE`
- **Missed:** `ONE_DRIVE_DOWNLOAD_FILE`
- **Primary returned:** `GOOGLEDRIVE_DOWNLOAD_FILE`

### workflow-003-q3-implicit — implicit, recall 0.0%
- **Query:** save the updated spreadsheet back to the cloud and check the file
- **Required:** `ONE_DRIVE_UPDATE_FILE_CONTENT`
- **Missed:** `ONE_DRIVE_UPDATE_FILE_CONTENT`
- **Primary returned:** `ONE_DRIVE_UPDATE_WORKBOOK_RANGE`

### workflow-004-q3-implicit — implicit, recall 0.0%
- **Query:** change the status of a task card and post a new comment
- **Required:** `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD; TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`
- **Missed:** `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD; TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
- **Primary returned:** `NOTION_UPDATE_ROW_DATABASE; NOTION_CREATE_COMMENT; CLICKUP_UPDATE_TASK; CLICKUP_CREATE_TASK_COMMENT`

### workflow-005-q1-implicit — implicit, recall 0.0%
- **Query:** find CRM records for our partners
- **Required:** `NOTION_QUERY_DATABASE_WITH_FILTER; NOTION_SEARCH_NOTION_PAGE`
- **Missed:** `NOTION_QUERY_DATABASE_WITH_FILTER; NOTION_SEARCH_NOTION_PAGE`
- **Primary returned:** `NETHUNT_CRM_FIND_RECORDS`

### workflow-005-q2-implicit — implicit, recall 0.0%
- **Query:** get recent conversations from our partner
- **Required:** `GMAIL_LIST_THREADS; GMAIL_FETCH_MESSAGE_BY_THREAD_ID`
- **Missed:** `GMAIL_FETCH_MESSAGE_BY_THREAD_ID; GMAIL_LIST_THREADS`
- **Primary returned:** `PIPEDRIVE_GET_CONVERSATIONS`

### workflow-005-q3-implicit — implicit, recall 0.0%
- **Query:** set up a handoff assignment item
- **Required:** `CLICKUP_CREATE_TASK`
- **Missed:** `CLICKUP_CREATE_TASK`
- **Primary returned:** `PAGERDUTY_CREATE_HANDOFF_NOTIFICATION_RULE; PAGERDUTY_UPDATE_ONCALL_HANDOFF_NOTIFICATION_RULE`

### workflow-005-q4-implicit — implicit, recall 0.0%
- **Query:** modify the pipeline stage on this customer record
- **Required:** `NOTION_UPDATE_PAGE`
- **Missed:** `NOTION_UPDATE_PAGE`
- **Primary returned:** `PIPEDRIVE_UPDATE_DEAL`
