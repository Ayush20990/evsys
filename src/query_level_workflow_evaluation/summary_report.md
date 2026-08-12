# Query-Level Workflow Benchmark

## Method
Each human workflow is decomposed into agent-like search queries, with the query count scaled to the candidate pool size instead of a fixed cap. Ground truth per query is one or more requirement groups (any one tool within a group satisfies it; all groups are required). Queries that miss a group get a secondary judged-recall pass checking whether an actually-returned, unlabeled tool would still plausibly satisfy it.

## Summary
- **Workflows accepted:** 25
- **Query-level test cases:** 82
- **Rejected workflow decompositions:** 0
- **Average primary recall (strict):** 54.1%
- **Average retrieval recall (strict):** 66.7%
- **Any-required-group hit rate:** 73.2%
- **Average judged recall (strict + plausible unlabeled hits, same denominator as strict recall):** 81.3%
- **Queries sent through the judge pass (recall < 1):** 33/82

## Latency
API/Search latency is the successful call only; end-to-end includes failed attempts and retry backoff.

| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 2.77 | 2.77 |
| Median (P50) | 2.50 | 2.50 |
| P95 | 4.61 | 4.61 |
| Maximum | 8.63 | 8.63 |

## Failure Examples
These are query-level candidates for manual review, not automatic product-bug conclusions. `judged_recall` is a plausibility check, not a second ground truth.

### workflow-006-q2 — recall 0.0%
- **Query:** search campaigns and add contact to campaign
- **Missed purposes:** `find the relevant campaign; add the contact to the campaign`
- **Missed (any-of groups):** `SALESFORCE_SEARCH_CAMPAIGNS; SALESFORCE_ADD_CONTACT_TO_CAMPAIGN`
- **Judged recall:** 0.0%
- **Primary returned:** `EMELIA_LIST_CAMPAIGNS; EMELIA_ADD_CONTACT_TO_CAMPAIGN`

### workflow-007-q4 — recall 0.0%
- **Query:** send and receive SMS messages
- **Missed purposes:** `send SMS messages; receive and get inbound SMS messages`
- **Missed (any-of groups):** `CLICKSEND_CREATE_SMS_SEND; CLICKSEND_GET_SMS_INBOUND`
- **Judged recall:** 50.0% (group 1 <- MSG91_SEND_SMS (high))
- **Primary returned:** `BREVO_CREATE_SMS_CAMPAIGN; MSG91_SEND_SMS`

### workflow-015-q1 — recall 0.0%
- **Query:** fetch pending invoice emails and get attachments
- **Missed purposes:** `retrieve email messages; download invoice file attachments`
- **Missed (any-of groups):** `GMAIL_FETCH_EMAILS; GMAIL_GET_ATTACHMENT`
- **Judged recall:** 100.0% (group 1 <- GOOGLESUPER_FETCH_EMAILS (high); group 2 <- GOOGLESUPER_GET_ATTACHMENT (high))
- **Primary returned:** `SUPPORTBEE_FETCH_EMAILS; GOOGLESUPER_FETCH_EMAILS; GOOGLESUPER_GET_ATTACHMENT`

### workflow-019-q2 — recall 0.0%
- **Query:** retrieve and read the candidate's existing resume document from storage
- **Missed purposes:** `Locate the resume file in Google Drive; Fetch the contents of the resume document`
- **Missed (any-of groups):** `GOOGLEDRIVE_FIND_FILE; GOOGLEDRIVE_DOWNLOAD_FILE | GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`
- **Judged recall:** 0.0%
- **Primary returned:** `BREEZY_HR_GET_CANDIDATE_RESUME`

### workflow-023-q2 — recall 0.0%
- **Query:** update tickets with AI triage notes, tags, and enrich with requester context
- **Missed purposes:** `add private AI triage notes and tags to tickets; enrich tickets with requester and order context`
- **Missed (any-of groups):** `ZENDESK_UPDATE_ZENDESK_TICKET; ZENDESK_GET_USER`
- **Judged recall:** 50.0% (group 1 <- ZENDESK_UPDATE_TICKETS_TAGS (medium))
- **Primary returned:** `ZENDESK_UPDATE_TICKETS_TAGS`

### workflow-001-q1 — recall 0.0%
- **Query:** create a review-only marketing email and clone it for the launch
- **Missed purposes:** `clone the confirmation email for the event registration flow`
- **Missed (any-of groups):** `HUBSPOT_CLONE_MARKETING_EMAIL`
- **Judged recall:** 0.0%
- **Primary returned:** `MAILCHIMP_REPLICATE_CAMPAIGN`

### workflow-001-q2 — recall 0.0%
- **Query:** create a disabled automation workflow for event registration
- **Missed purposes:** `create the disabled confirmation workflow in HubSpot`
- **Missed (any-of groups):** `HUBSPOT_CREATE_WORKFLOW`
- **Judged recall:** 0.0%
- **Primary returned:** `CALENDLY_UPDATE_EVENT_TYPE`

### workflow-008-q1 — recall 0.0%
- **Query:** add summarized text entries to an existing Google Doc
- **Missed purposes:** `insert summarized text into Google Docs`
- **Missed (any-of groups):** `GOOGLEDOCS_INSERT_TEXT_ACTION`
- **Judged recall:** 100.0% (group 1 <- GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN (high))
- **Primary returned:** `GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`

### workflow-008-q2 — recall 0.0%
- **Query:** update google document with transcript summary data
- **Missed purposes:** `update document content with new text`
- **Missed (any-of groups):** `GOOGLEDOCS_INSERT_TEXT_ACTION`
- **Judged recall:** 100.0% (group 1 <- GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN (high))
- **Primary returned:** `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT; GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`

### workflow-009-q1 — recall 0.0%
- **Query:** search and generate stock image assets
- **Missed purposes:** `search for stock images`
- **Missed (any-of groups):** `COMPOSIO_SEARCH_IMAGE`
- **Judged recall:** 0.0%
- **Primary returned:** `GEMINI_GENERATE_IMAGE`

### workflow-009-q2 — recall 0.0%
- **Query:** send generated media files via email
- **Missed purposes:** `send generated files through email`
- **Missed (any-of groups):** `GMAIL_SEND_EMAIL`
- **Judged recall:** 100.0% (group 1 <- OUTLOOK_SEND_EMAIL (high))
- **Primary returned:** `SALESFORCE_SEND_EMAIL; OUTLOOK_SEND_EMAIL`

### workflow-010-q1 — recall 0.0%
- **Query:** query existing bank account transactions and company ledger entities
- **Missed purposes:** `query existing ledger and transaction entities`
- **Missed (any-of groups):** `QUICKBOOKS_QUERY_ENTITIES`
- **Judged recall:** 100.0% (group 1 <- QUICKBOOKS_GET_GENERAL_LEDGER_REPORT (high))
- **Primary returned:** `ZOHO_BOOKS_LIST_BANK_ACCOUNTS; QUICKBOOKS_GET_GENERAL_LEDGER_REPORT`

### workflow-013-q3 — recall 0.0%
- **Query:** send outreach email for marketing and press engagement
- **Missed purposes:** `send outreach emails to contacts`
- **Missed (any-of groups):** `GMAIL_SEND_EMAIL`
- **Judged recall:** 0.0%
- **Primary returned:** `SENDGRID_SEND_A_TEST_MARKETING_EMAIL; HUBSPOT_CLONE_MARKETING_EMAIL`

### workflow-015-q2 — recall 0.0%
- **Query:** upload invoice files to cloud storage
- **Missed purposes:** `save invoice attachments to cloud storage`
- **Missed (any-of groups):** `GOOGLEDRIVE_UPLOAD_FROM_URL`
- **Judged recall:** 100.0% (group 1 <- GOOGLEDRIVE_UPLOAD_FILE (high))
- **Primary returned:** `GOOGLEDRIVE_UPLOAD_FILE; ONE_DRIVE_ONEDRIVE_UPLOAD_FILE`

### workflow-017-q4 — recall 0.0%
- **Query:** send an email regarding infrastructure issues
- **Missed purposes:** `Send the support email`
- **Missed (any-of groups):** `GMAIL_SEND_EMAIL | GMAIL_SEND_DRAFT`
- **Judged recall:** 0.0%
- **Primary returned:** `JIRA_SEND_NOTIFICATION_FOR_ISSUE`

### workflow-018-q1 — recall 0.0%
- **Query:** search for remote data engineering contract job listings on LinkedIn
- **Missed purposes:** `execute searches for job listings on LinkedIn`
- **Missed (any-of groups):** `LINKEDIN_PROXY_EXECUTE`
- **Judged recall:** 0.0%
- **Primary returned:** `COMPOSIO_SEARCH_WEB`

### workflow-020-q4 — recall 0.0%
- **Query:** manage zoho crm records
- **Missed purposes:** `execute queries or actions against Zoho CRM`
- **Missed (any-of groups):** `ZOHO_PROXY_EXECUTE`
- **Judged recall:** 100.0% (group 1 <- ZOHO_CREATE_ZOHO_RECORD (high))
- **Primary returned:** `ZOHO_LIST_MODULES; ZOHO_GET_MODULE_FIELDS; ZOHO_SEARCH_ZOHO_RECORDS`

### workflow-020-q5 — recall 0.0%
- **Query:** manage quickbooks billing data
- **Missed purposes:** `execute operations for billing records in QuickBooks`
- **Missed (any-of groups):** `QUICKBOOKS_PROXY_EXECUTE`
- **Judged recall:** 0.0%
- **Primary returned:** `QUICKBOOKS_QUERY_ENTITIES; QUICKBOOKS_GET_TRANSACTION_LIST_REPORT`

### workflow-022-q1 — recall 0.0%
- **Query:** fetch unread emails and process alerts
- **Missed purposes:** `retrieve unread email messages for triage`
- **Missed (any-of groups):** `GMAIL_FETCH_EMAILS`
- **Judged recall:** 100.0% (group 1 <- INSTANTLY_LIST_EMAILS (medium))
- **Primary returned:** `STACK_EXCHANGE_GET_USER_UNREAD_NOTIFICATIONS; BENCHMARK_EMAIL_GET_NOTIFICATION; INSTANTLY_COUNT_UNREAD_EMAILS`

### workflow-022-q2 — recall 0.0%
- **Query:** look up CRM trial records and organizations
- **Missed purposes:** `find CRM trial and organization records`
- **Missed (any-of groups):** `AIRTABLE_LIST_RECORDS | PIPEDRIVE_SEARCH_ORGANIZATIONS`
- **Judged recall:** 0.0%
- **Primary returned:** `SALESFORCE_SEARCH_ACCOUNTS; SALESFORCE_SEARCH_OPPORTUNITIES; SALESFORCE_GET_ACCOUNT; SALESFORCE_GET_OPPORTUNITY; CAPSULE_CRM_LIST_PARTIES; CAPSULE_CRM_RUN_FILTER_QUERY`
