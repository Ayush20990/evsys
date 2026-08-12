# Composio Search Multi-Tool Evaluation Report

## 1. Executive Summary
- **Total Use Cases:** 100
- **Successful API Responses:** 100
- **Failed/Empty Responses:** 0
- **Average Recall (All):** 33.9%
- **Average Precision (All):** 38.3%

## 2. Latency Metrics
API/Search latency measures only the successful `COMPOSIO_SEARCH_TOOLS` call. End-to-end latency includes all failed attempts and retry backoff.

| Metric | Time (seconds) |
|--------|----------------|
| API/Search average | 3.35 |
| API/Search median (P50) | 2.81 |
| API/Search P95 | 9.70 |
| API/Search max | 10.29 |
| End-to-end average | 3.35 |
| End-to-end median (P50) | 2.81 |
| End-to-end P95 | 9.70 |
| End-to-end max | 10.29 |

## 3. Performance by Query Complexity
| Expected Tools | Case Count | Avg Recall | Avg Precision |
|----------------|------------|------------|---------------|
| 1-3 | 7 | 71.4% | 23.4% |
| 4-7 | 31 | 42.4% | 36.6% |
| 8-12 | 32 | 30.1% | 40.2% |
| 13+ | 30 | 20.3% | 41.4% |

## 4. Performance by Toolkit
| Toolkit | Total Expected | Found | Recall |
|---------|----------------|-------|--------|
| GITHUB | 117 | 16 | 13.7% |
| GOOGLESHEETS | 73 | 19 | 26.0% |
| OUTLOOK | 72 | 34 | 47.2% |
| NOTION | 68 | 20 | 29.4% |
| PIPEDRIVE | 59 | 15 | 25.4% |
| HUBSPOT | 44 | 11 | 25.0% |
| GMAIL | 39 | 6 | 15.4% |
| GOOGLEDRIVE | 35 | 12 | 34.3% |
| INSTAGRAM | 34 | 10 | 29.4% |
| YOUTUBE | 34 | 11 | 32.4% |
| SALESFORCE | 28 | 12 | 42.9% |
| METAADS | 28 | 15 | 53.6% |
| CLICKUP | 25 | 5 | 20.0% |
| TRELLO | 23 | 4 | 17.4% |
| GOOGLE | 22 | 5 | 22.7% |
| COMPOSIO | 20 | 2 | 10.0% |
| VERCEL | 20 | 2 | 10.0% |
| ONE | 18 | 3 | 16.7% |
| SLACK | 18 | 6 | 33.3% |
| GOOGLECALENDAR | 17 | 0 | 0.0% |
| BROWSER | 17 | 7 | 41.2% |
| FACEBOOK | 14 | 4 | 28.6% |
| GEMINI | 13 | 4 | 30.8% |
| GOOGLEDOCS | 12 | 3 | 25.0% |
| KOMMO | 12 | 2 | 16.7% |
| LINKEDIN | 11 | 3 | 27.3% |
| CLICKSEND | 10 | 0 | 0.0% |
| GOOGLEADS | 9 | 4 | 44.4% |
| HEYGEN | 8 | 8 | 100.0% |
| ZENDESK | 8 | 2 | 25.0% |
| QUICKBOOKS | 7 | 3 | 42.9% |
| XERO | 7 | 2 | 28.6% |
| ZOHO | 6 | 5 | 83.3% |
| AIRTABLE | 6 | 1 | 16.7% |
| LINEAR | 5 | 0 | 0.0% |
| ZEP | 5 | 0 | 0.0% |
| SUPABASE | 5 | 1 | 20.0% |
| BITBUCKET | 4 | 4 | 100.0% |
| GOOGLETASKS | 4 | 0 | 0.0% |
| GOOGLESLIDES | 4 | 4 | 100.0% |
| BREVO | 3 | 0 | 0.0% |
| CLOUDFLARE | 3 | 0 | 0.0% |
| ELEVENLABS | 3 | 0 | 0.0% |
| TICKTICK | 3 | 0 | 0.0% |
| JIRA | 3 | 0 | 0.0% |
| SHOPIFY | 3 | 0 | 0.0% |
| TODOIST | 3 | 2 | 66.7% |
| CAL | 2 | 0 | 0.0% |
| DISCORDBOT | 2 | 0 | 0.0% |
| FATHOM | 2 | 0 | 0.0% |
| FIREFLIES | 2 | 2 | 100.0% |
| DATADOG | 2 | 0 | 0.0% |
| HUNTER | 2 | 0 | 0.0% |
| ATTIO | 2 | 1 | 50.0% |
| TELEGRAM | 1 | 0 | 0.0% |
| WHATSAPP | 1 | 0 | 0.0% |
| DISCORD | 1 | 0 | 0.0% |
| METABASE | 1 | 0 | 0.0% |
| PLAIN | 1 | 0 | 0.0% |
| MEM0 | 1 | 0 | 0.0% |
| TINYURL | 1 | 0 | 0.0% |
| AHREFS | 1 | 0 | 0.0% |
| FIRECRAWL | 1 | 0 | 0.0% |
| MICROSOFT | 1 | 0 | 0.0% |
|  | 1 | 0 | 0.0% |
| GOOGLESUPER | 1 | 0 | 0.0% |

## 5. Top 15 Worst Performing Workflows
Sorted by lowest recall, then highest missing tool count.

### Use Case #7 - Recall: 0.0% | Precision: 0.0%
- **Missed (23):** `CAL_CONNECT_TO_CALENDAR; CAL_RETRIEVE_CALENDAR_LIST; CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND; CLICKSEND_CREATE_SMS_SEND; CLICKSEND_DELETE_AUTOMATIONS...`
- **Extra returned (7):** `ACTIVE_CAMPAIGN_GET_SMS_BROADCAST_METRICS_SNAPSHOT; ACTIVE_CAMPAIGN_LIST_SMS_BROADCASTS; CALENDARHERO_GET_SEARCH_RESULT; CALENDARHERO_SEARCH_INTEGRATI...`
- **Prompt Excerpt:** _Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS..._

### Use Case #72 - Recall: 0.0% | Precision: 0.0%
- **Missed (19):** `GEMINI_COUNT_TOKENS; GEMINI_EMBED_CONTENT; GEMINI_GENERATE_CONTENT; GEMINI_GENERATE_IMAGE; GEMINI_GENERATE_VIDEOS; GEMINI_LIST_MODELS; GEMINI_WAIT_FOR...`
- **Extra returned (3):** `VERCEL_CREATE_PROJECT2; VERCEL_GET_PROJECT2; VERCEL_UPDATE_PROJECT2...`
- **Prompt Excerpt:** _Build, repair, deploy, configure, and test a Vercel-hosted GitHub-backed API proxy for Gemini text, ..._

### Use Case #41 - Recall: 0.0% | Precision: 0.0%
- **Missed (14):** `GITHUB_COMMIT_MULTIPLE_FILES; GITHUB_CREATE_A_PULL_REQUEST; GITHUB_DELETE_A_REFERENCE; GITHUB_GET_REPOSITORY_CONTENT; GITHUB_MERGE_A_PULL_REQUEST; GOO...`
- **Extra returned (2):** `VERCEL_GET_PROJECT2; VERCEL_UPDATE_PROJECT_PROTECTION_BYPASS...`
- **Prompt Excerpt:** _Implement and release a protected budget dashboard feature by reading Google Sheets and Google Docs ..._

### Use Case #13 - Recall: 0.0% | Precision: 0.0%
- **Missed (13):** `BREVO_CREATE_CONTACT_LIST; BREVO_GET_CONTACT_LISTS; BREVO_LIST_EMAIL_CAMPAIGNS; GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID; GMAIL_SEND_EMAIL; GOOGLE_ANALYTICS_...`
- **Extra returned (8):** `MAILCHIMP_ADD_OR_UPDATE_LIST_MEMBER; MAILCHIMP_BATCH_SUBSCRIBE_OR_UNSUBSCRIBE; MAILCHIMP_GET_BATCH_OPERATION_STATUS; MAILCHIMP_GET_LISTS_INFO; MAILCHI...`
- **Prompt Excerpt:** _Audit website search and traffic performance, prepare email marketing/contact lists, and send outrea..._

### Use Case #40 - Recall: 0.0% | Precision: 0.0%
- **Missed (13):** `LINEAR_CREATE_LINEAR_ISSUE; LINEAR_LIST_LINEAR_LABELS; LINEAR_LIST_LINEAR_PROJECTS; LINEAR_LIST_LINEAR_TEAMS; LINEAR_RUN_QUERY_OR_MUTATION; NOTION_ADD...`
- **Extra returned (4):** `LINEAR_CREATE_LINEAR_ISSUE_RELATION; LINEAR_GET_LINEAR_ISSUE; LINEAR_LIST_LINEAR_ISSUES; LINEAR_SEARCH_ISSUES...`
- **Prompt Excerpt:** _Create, iteratively refine, verify, and operationalize a Notion specification page, then create rela..._

### Use Case #60 - Recall: 0.0% | Precision: 0.0%
- **Missed (10):** `GOOGLESHEETS_BATCH_GET; GOOGLESHEETS_FORMAT_CELL; GOOGLESHEETS_GET_SHEET_NAMES; GOOGLESHEETS_GET_SPREADSHEET_INFO; GOOGLESHEETS_SPREADSHEETS_VALUES_AP...`
- **Extra returned (8):** `INSTANTLY_COUNT_LEADS_FROM_SUPERSEARCH; INSTANTLY_CREATE_LEAD_LIST; INSTANTLY_CREATE_SUPERSEARCH_ENRICHMENT; INSTANTLY_GET_LEAD_LIST; INSTANTLY_GET_SU...`
- **Prompt Excerpt:** _Manage lead data in Google Sheets: read existing tabs, append and correct lead rows, enrich contacts..._

### Use Case #15 - Recall: 0.0% | Precision: 0.0%
- **Missed (8):** `GMAIL_BATCH_MODIFY_MESSAGES; GMAIL_FETCH_EMAILS; GMAIL_GET_ATTACHMENT; GMAIL_LIST_LABELS; GOOGLEDRIVE_UPLOAD_FROM_URL; GOOGLESHEETS_BATCH_GET; GOOGLES...`
- **Extra returned (1):** `WORKDAY_SEND_SUPPLIER_INVOICE_ATTACHMENTS_FOR_SCANNING...`
- **Prompt Excerpt:** _Process pending invoice emails, persist invoice attachments to cloud storage, update spreadsheet led..._

### Use Case #25 - Recall: 0.0% | Precision: 0.0%
- **Missed (8):** `COMPOSIO_SEARCH_FETCH_URL_CONTENT; COMPOSIO_SEARCH_WEB; GMAIL_CREATE_EMAIL_DRAFT; GMAIL_FETCH_EMAILS; GMAIL_GET_PROFILE; GMAIL_PROXY_EXECUTE; GMAIL_SE...`
- **Extra returned (3):** `DICE_MCP_SEARCH_JOBS; SERPAPI_GOOGLE_DOMAINS_LIST; ZIPRECRUITER_MCP_SEARCH_JOBS...`
- **Prompt Excerpt:** _Find relevant job listings from public web/job sources, tailor them to a software profile, and email..._

### Use Case #64 - Recall: 0.0% | Precision: 0.0%
- **Missed (8):** `GOOGLEADS_SEARCH_STREAM_GAQL; GOOGLE_ANALYTICS_RUN_REPORT; GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY; HUBSPOT_CLONE_MARKETING_EMAIL; HUBSPOT_CREATE...`
- **Extra returned (7):** `HUBSPOT_CREATE_BATCH_OF_OBJECTS; HUBSPOT_CREATE_COMPANIES; HUBSPOT_CREATE_CONTACTS; HUBSPOT_CREATE_OBJECT_ASSOCIATION; HUBSPOT_LIST_ASSOCIATION_TYPES;...`
- **Prompt Excerpt:** _Prepare marketing and CRM automation work: gather marketing performance data, send a brief by email,..._

### Use Case #39 - Recall: 0.0% | Precision: 0.0%
- **Missed (7):** `GOOGLESHEETS_BATCH_GET; GOOGLESHEETS_VALUES_UPDATE; KOMMO_GET_LEAD; KOMMO_LIST_CONTACTS; KOMMO_LIST_EVENTS; KOMMO_LIST_LEADS; KOMMO_LIST_NOTES_BY_ENTI...`
- **Extra returned (3):** `BROWSER_TOOL_CREATE_TASK; BROWSER_TOOL_GET_SESSION; BROWSER_TOOL_WATCH_TASK...`
- **Prompt Excerpt:** _Audit and reconcile CRM lead activity into a spreadsheet-based reporting workbook, including lead ex..._

### Use Case #83 - Recall: 0.0% | Precision: 0.0%
- **Missed (7):** `ONE_DRIVE_DOWNLOAD_FILE; ONE_DRIVE_GET_DRIVE_ITEM_BY_SHARING_URL; ONE_DRIVE_LIST_FOLDER_CHILDREN; ONE_DRIVE_SEARCH_ITEMS; ONE_DRIVE_UPDATE_FILE_CONTEN...`
- **Extra returned (8):** `GOOGLEDRIVE_DOWNLOAD_FILE; GOOGLEDRIVE_DOWNLOAD_FILE_OPERATION; GOOGLEDRIVE_EXPORT_GOOGLE_WORKSPACE_FILE; GOOGLEDRIVE_FIND_FILE; GOOGLEDRIVE_GET_ABOUT...`
- **Prompt Excerpt:** _Read files from a Microsoft cloud document library, inspect related due-diligence email context, loc..._

### Use Case #2 - Recall: 0.0% | Precision: 0.0%
- **Missed (6):** `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS; NOTION_ADD_MULTIPLE_PAGE_CONTENT; NOTION_CREATE_NOTION_PAGE; NOTION_GET_PAGE_MARKDOWN; NOTION_REPLACE_PAGE_C...`
- **Extra returned (11):** `NOTION_APPEND_MEDIA_BLOCKS; NOTION_CREATE_DATABASE; NOTION_FETCH_DATA; NOTION_FETCH_DATABASE; NOTION_INSERT_ROW_DATABASE; NOTION_INSERT_ROW_FROM_NL; N...`
- **Prompt Excerpt:** _Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a la..._

### Use Case #24 - Recall: 0.0% | Precision: 0.0%
- **Missed (6):** `BROWSER_TOOL_CREATE_TASK; BROWSER_TOOL_WATCH_TASK; COMPOSIO_SEARCH_NEWS; COMPOSIO_SEARCH_TRENDS; COMPOSIO_SEARCH_WEB; GMAIL_SEND_EMAIL...`
- **Extra returned (4):** `DICE_MCP_SEARCH_JOBS; GMAIL_FETCH_MESSAGE_BY_THREAD_ID; GMAIL_LIST_THREADS; GMAIL_MODIFY_THREAD_LABELS...`
- **Prompt Excerpt:** _Build a recurring job-search digest by finding relevant LinkedIn job listings and sending the result..._

### Use Case #52 - Recall: 0.0% | Precision: 0.0%
- **Missed (6):** `MEM0_GET_MEMORIES_BY_ENTITY; ZEP_CREATE_GRAPH; ZEP_GET_PROJECT_INFO; ZEP_GET_USER_NODE; ZEP_GRAPH_SEARCH; ZEP_LIST_GROUPS_ORDERED...`
- **Extra returned (6):** `MEM0_GET_USER_MEMORY_STATS; MEM0_RETRIEVE_ALL_EVENTS_FOR_THE_CURRENTLY_LOGGED_IN_USER; MEM0_RETRIEVE_LIST_OF_MEMORY_EVENTS; ZEP_ADD_THREAD_MESSAGES; Z...`
- **Prompt Excerpt:** _Migrate a user's memory data from Mem0 into Zep, inspect existing Zep context, attempt to organize m..._

### Use Case #86 - Recall: 0.0% | Precision: 0.0%
- **Missed (6):** `SALESFORCE_GET_REPORT; SALESFORCE_GET_SUPPORT; SALESFORCE_QUERY; SALESFORCE_RUN_REPORT; SALESFORCE_RUN_SOQL_QUERY; SLACK_SEND_MESSAGE...`
- **Extra returned (11):** `SALESFORCE_ADD_OPPORTUNITY_LINE_ITEM; SALESFORCE_GET_OPPORTUNITY; SALESFORCE_LIST_ACCOUNTS; SALESFORCE_LIST_OPPORTUNITIES; SALESFORCE_RETRIEVE_OPPORTU...`
- **Prompt Excerpt:** _Retrieve Salesforce CRM report and query data for a business-performance brief, then send Slack noti..._
