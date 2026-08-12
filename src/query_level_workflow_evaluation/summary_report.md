# Query-Level Workflow Benchmark

## Method
Each human workflow is decomposed into agent-like search queries. Its listed tools are a candidate pool; Gemini labels only the tools genuinely required per query. Every Composio result entry is aggregated before scoring.

## Summary
- **Workflows accepted:** 24
- **Query-level test cases:** 79
- **Rejected workflow decompositions:** 1
- **Average primary recall:** 63.9%
- **Average retrieval recall:** 77.8%
- **Any-required-tool hit rate:** 84.8%

## Latency
API/Search latency is the successful call only; end-to-end includes failed attempts and retry backoff.

| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 3.10 | 3.10 |
| Median (P50) | 2.87 | 2.87 |
| P95 | 4.59 | 4.59 |
| Maximum | 10.63 | 10.63 |

## Failure Examples
These are query-level candidates for manual review, not automatic product-bug conclusions.

### workflow-022-q2 — recall 0.0%
- **Query:** find CRM trial records and organization details
- **Required:** `PIPEDRIVE_SEARCH_ORGANIZATIONS; AIRTABLE_LIST_RECORDS`
- **Missed:** `AIRTABLE_LIST_RECORDS; PIPEDRIVE_SEARCH_ORGANIZATIONS`
- **Primary returned:** `NETHUNT_CRM_FIND_RECORDS`

### workflow-001-q2 — recall 0.0%
- **Query:** create automated review email for registration confirmation
- **Required:** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Missed:** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Primary returned:** `RESEND_CREATE_TEMPLATE; RESEND_SEND_EMAIL`

### workflow-001-q3 — recall 0.0%
- **Query:** create a disabled confirmation workflow
- **Required:** `HUBSPOT_CREATE_WORKFLOW`
- **Missed:** `HUBSPOT_CREATE_WORKFLOW`
- **Primary returned:** `KADOA_CREATE_WORKFLOW_TRIGGER`

### workflow-006-q4 — recall 0.0%
- **Query:** run soql query for mql lead activity reporting
- **Required:** `SALESFORCE_RUN_SOQL_QUERY`
- **Missed:** `SALESFORCE_RUN_SOQL_QUERY`
- **Primary returned:** `SALESFORCE_LIST_LEADS`

### workflow-010-q1 — recall 0.0%
- **Query:** query existing bank account ledger transactions
- **Required:** `QUICKBOOKS_QUERY_ENTITIES`
- **Missed:** `QUICKBOOKS_QUERY_ENTITIES`
- **Primary returned:** `MERCURY_MCP_GET_ACCOUNTS; MERCURY_MCP_LIST_TRANSACTIONS; MERCURY_MCP_GET_CURRENT_DATE`

### workflow-010-q3 — recall 0.0%
- **Query:** fetch financial reports to verify reconciliation
- **Required:** `QUICKBOOKS_GET_REPORTS`
- **Missed:** `QUICKBOOKS_GET_REPORTS`
- **Primary returned:** `QUICKBOOKS_GET_REPORT_TRIAL_BALANCE; FREEAGENT_GET_THE_OPENING_BALANCES`

### workflow-014-q3 — recall 0.0%
- **Query:** send email compilation of software engineering jobs
- **Required:** `GMAIL_SEND_EMAIL`
- **Missed:** `GMAIL_SEND_EMAIL`
- **Primary returned:** `DICE_MCP_SEARCH_JOBS; ZIPRECRUITER_MCP_SEARCH_JOBS`

### workflow-017-q3 — recall 0.0%
- **Query:** send support email for infrastructure issues
- **Required:** `GMAIL_SEND_EMAIL`
- **Missed:** `GMAIL_SEND_EMAIL`
- **Primary returned:** `BENCHMARK_EMAIL_SEND_SUPPORT_FEEDBACK`

### workflow-018-q1 — recall 0.0%
- **Query:** search LinkedIn for remote data engineering contract jobs
- **Required:** `LINKEDIN_PROXY_EXECUTE`
- **Missed:** `LINKEDIN_PROXY_EXECUTE`
- **Primary returned:** `COMPOSIO_SEARCH_WEB; COMPOSIO_SEARCH_FETCH_URL_CONTENT`

### workflow-018-q3 — recall 0.0%
- **Query:** send curated job digest email
- **Required:** `GMAIL_SEND_EMAIL`
- **Missed:** `GMAIL_SEND_EMAIL`
- **Primary returned:** `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL`

### workflow-024-q2 — recall 0.0%
- **Query:** send job digest email to candidate
- **Required:** `GMAIL_SEND_EMAIL`
- **Missed:** `GMAIL_SEND_EMAIL`
- **Primary returned:** `DICE_MCP_SEARCH_JOBS; DICE_MCP_GET_CANDIDATE`

### workflow-025-q2 — recall 0.0%
- **Query:** send curated job listings via email
- **Required:** `GMAIL_SEND_EMAIL`
- **Missed:** `GMAIL_SEND_EMAIL`
- **Primary returned:** `ZIPRECRUITER_MCP_SEARCH_JOBS; DICE_MCP_SEARCH_JOBS`

### workflow-005-q1 — recall 50.0%
- **Query:** search notion for partner CRM records
- **Required:** `NOTION_QUERY_DATABASE_WITH_FILTER; NOTION_SEARCH_NOTION_PAGE`
- **Missed:** `NOTION_QUERY_DATABASE_WITH_FILTER`
- **Primary returned:** `NOTION_SEARCH_NOTION_PAGE`

### workflow-007-q1 — recall 50.0%
- **Query:** fetch recent emails and check calendar schedule
- **Required:** `GMAIL_FETCH_EMAILS; GOOGLECALENDAR_EVENTS_LIST`
- **Missed:** `GOOGLECALENDAR_EVENTS_LIST`
- **Primary returned:** `OUTLOOK_GET_SCHEDULE; SUPPORTBEE_FETCH_EMAILS; CAL_FETCH_SCHEDULE_BY_ID; GMAIL_FETCH_EMAILS`

### workflow-011-q1 — recall 50.0%
- **Query:** search and download strategy documents from OneDrive
- **Required:** `ONE_DRIVE_ONEDRIVE_FIND_FILE; ONE_DRIVE_DOWNLOAD_FILE_BY_PATH`
- **Missed:** `ONE_DRIVE_ONEDRIVE_FIND_FILE`
- **Primary returned:** `ONE_DRIVE_GET_ITEM; ONE_DRIVE_DOWNLOAD_FILE`

### workflow-011-q3 — recall 50.0%
- **Query:** configure Gmail support labels and filters for routing
- **Required:** `GMAIL_CREATE_LABEL; GMAIL_CREATE_FILTER`
- **Missed:** `GMAIL_CREATE_FILTER`
- **Primary returned:** `GMAIL_LIST_LABELS; GMAIL_CREATE_LABEL`

### workflow-012-q3 — recall 50.0%
- **Query:** search Slack messages and list users for project management
- **Required:** `SLACK_SEARCH_MESSAGES; SLACK_LIST_ALL_USERS`
- **Missed:** `SLACK_LIST_ALL_USERS`
- **Primary returned:** `SLACK_SEARCH_MESSAGES`

### workflow-016-q1 — recall 50.0%
- **Query:** fetch website traffic and search performance analytics
- **Required:** `GOOGLE_ANALYTICS_RUN_REPORT; GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
- **Missed:** `GOOGLE_ANALYTICS_RUN_REPORT`
- **Primary returned:** `AHREFS_RETRIEVE_TOP_PAGES_FROM_SITE_EXPLORER; SIMPLE_ANALYTICS_GET_AGGREGATED_STATS; GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`

### workflow-016-q3 — recall 50.0%
- **Query:** create a pull request with code fixes
- **Required:** `GITHUB_CREATE_A_PULL_REQUEST; GITHUB_COMMIT_MULTIPLE_FILES`
- **Missed:** `GITHUB_COMMIT_MULTIPLE_FILES`
- **Primary returned:** `GITHUB_CREATE_A_PULL_REQUEST`

### workflow-017-q4 — recall 50.0%
- **Query:** read and update booking schedule in google sheets
- **Required:** `GOOGLESHEETS_BATCH_GET; GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
- **Missed:** `GOOGLESHEETS_BATCH_GET`
- **Primary returned:** `GOOGLESHEETS_CREATE_GOOGLE_SHEET1; GOOGLESHEETS_VALUES_GET; GOOGLESHEETS_VALUES_UPDATE`
