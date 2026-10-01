# Search failures — run 9

Every query below was issued by the agent during run 9, and every result is what `COMPOSIO_SEARCH_TOOLS` returned for it. Nothing is reconstructed or rephrased after the fact.

- **5** capabilities where a fair query returned the needed tool nowhere.
- **71** where search did return it, but ranked it into `related` while `primary` held something else.

---

## Part 1 — the needed tool was not returned at all

### Task 3 — Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.

**Capability:** Upload the modified workbook back to OneDrive and update the existing cloud item

Tools the agent needed: `ONE_DRIVE_UPDATE_FILE_CONTENT`

Query the agent issued, and what came back:

1. `upload file to OneDrive`
   - primary: GOOGLEDRIVE_UPLOAD_FILE, ONE_DRIVE_ONEDRIVE_UPLOAD_FILE
   - related: GOOGLEDRIVE_RESUMABLE_UPLOAD, GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_CREATE_PERMISSION, ONE_DRIVE_ONEDRIVE_CREATE_FOLDER

The agent ran nothing from these results and moved on.

### Task 22 — The user was managing unread email triage and urgent alerts, looking up CRM-style trial records, inspecting and modifying source code in GitHub, opening or merging branches, and checking CI workflow failures.

**Capability:** Open, manage, or merge branches and pull requests in GitHub

Tools the agent needed: `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`

Query the agent issued, and what came back:

1. `search github repositories pull requests issues workflows`
   - primary: GMAIL_FETCH_EMAILS, GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY
   - related: GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, GITHUB_GET_A_WORKFLOW_RUN, GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN, GITHUB_DOWNLOAD_WORKFLOW_RUN_LOGS, GITHUB_LIST_REPOSITORY_WORKFLOWS

The agent did **not** notice: it ran `GMAIL_FETCH_EMAILS` from these results and carried on as though the step were done.

### Task 33 — Analyze WhatsApp-style broadcast campaigns in Kommo CRM, including detected campaign sends, audience reach, replies, conversions, templates, segments, and related agent activity.

**Capability:** Track system events, entity changes, and activity history to detect campaign sends and agent actions

Tools the agent needed: `KOMMO_LIST_EVENTS`

Query the agent issued, and what came back:

1. `Kommo CRM users agents responsible users`
   - primary: KOMMO_LIST_USERS
   - related: KOMMO_GET_USER, KOMMO_GET_ACCOUNT

The agent did **not** notice: it ran `KOMMO_LIST_USERS` from these results and carried on as though the step were done.

### Task 53 — Audit a short-link inventory by finding an existing spreadsheet registry, reading help-center mapping tabs, listing existing short links, and attempting to compare them with live public website article URLs and redirects.

**Capability:** List and retrieve short-link inventory data

Tools the agent needed: `TINYURL_LIST_URLS`

Query the agent issued, and what came back:

1. `list short links or url redirects`
   - primary: TRELLO_GET_CARDS_BY_ID_CARD
   - related: TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_GET_CARDS_BY_ID_CARD_BY_FIELD, TRELLO_GET_CARDS_CHECKLISTS_BY_ID_CARD, TRELLO_GET_CARDS_CUSTOM_FIELD_ITEMS_BY_ID_CARD, TRELLO_GET_CARDS_ATTACHMENTS_BY_ID_CARD

The agent ran nothing from these results and moved on.

### Task 97 — Manage Pipedrive CRM records: find deals and contacts, update deal participants and primary contacts, log notes and activities, schedule follow-ups, inspect deal and organization custom fields, and bulk reclassify deals across pipeline stages based on contract timing data.

**Capability:** Manage deal participants and primary contacts

Tools the agent needed: `PIPEDRIVE_ADD_DEAL_PARTICIPANT`, `PIPEDRIVE_LIST_PARTICIPANTS_OF_A_DEAL`

Query the agent issued, and what came back:

1. `update deal participants and primary contacts in Pipedrive`
   - primary: PIPEDRIVE_UPDATE_DEAL
   - related: PIPEDRIVE_UPDATE_DEAL_V2, PIPEDRIVE_GET_DEAL, PIPEDRIVE_SEARCH_PERSONS, PIPEDRIVE_GET_PERSON

The agent ran nothing from these results and moved on.

---

## Part 2 — the needed tool was returned, but only in `related`

Retrieval found these. Ranking put something else in `primary`, which is the position an agent acts on.

### Task 2 — Retrieve upcoming calendar events

Needed: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`

Query: `Retrieve upcoming events from Google Calendar`

   - primary: GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST
   - related: GOOGLECALENDAR_GET_CALENDAR, GOOGLECALENDAR_SETTINGS_LIST, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS, GOOGLECALENDAR_LIST_CALENDARS, GOOGLECALENDAR_EVENTS_GET

### Task 2 — Retrieve Notion page content for verification after writing

Needed: `NOTION_GET_PAGE_MARKDOWN`, `NOTION_RETRIEVE_PAGE`

Query: `Create or update Notion content containing a structured dataset`

   - primary: NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT
   - related: NOTION_SEARCH_NOTION_PAGE, NOTION_RETRIEVE_PAGE, NOTION_UPDATE_PAGE, NOTION_REPLACE_PAGE_CONTENT, NOTION_GET_PAGE_MARKDOWN

### Task 5 — Query and inspect Notion CRM records and databases

Needed: `NOTION_FETCH_DATABASE`, `NOTION_FETCH_ROW`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_RETRIEVE_PAGE`, `NOTION_SEARCH_NOTION_PAGE`

Query: `update page in Notion`

   - primary: NOTION_UPDATE_ROW_DATABASE
   - related: NOTION_FETCH_ROW, NOTION_FETCH_DATABASE, NOTION_UPDATE_PAGE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_RETRIEVE_PAGE, NOTION_SEARCH_NOTION_PAGE

### Task 5 — Write evidence-supported CRM status updates to Notion

Needed: `NOTION_UPDATE_PAGE`

Query: `update page in Notion`

   - primary: NOTION_UPDATE_ROW_DATABASE
   - related: NOTION_FETCH_ROW, NOTION_FETCH_DATABASE, NOTION_UPDATE_PAGE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_RETRIEVE_PAGE, NOTION_SEARCH_NOTION_PAGE

### Task 6 — Update existing Salesforce records (e.g., campaign attendance statuses)

Needed: `SALESFORCE_SOBJECT_ROWS_UPDATE`

Query: `Salesforce campaign member status list reporting`

   - primary: SALESFORCE_RUN_SOQL_QUERY
   - related: SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT, SALESFORCE_SOBJECT_ROWS_UPDATE, SALESFORCE_GET_A_BATCH_OF_RECORDS, SALESFORCE_GET_ORG_LIMITS, SALESFORCE_GET_ALL_CUSTOM_OBJECTS, SALESFORCE_QUERY_ALL

### Task 10 — Query existing QuickBooks transactions and entities for ledger reconciliation

Needed: `QUICKBOOKS_QUERY_ENTITIES`

Query: `QuickBooks delete void remove transaction entry`

   - primary: QUICKBOOKS_READ_INVOICE
   - related: QUICKBOOKS_UPDATE_FULL_INVOICE, QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_EXECUTE_BATCH_OPERATION, QUICKBOOKS_UPDATE_SPARSE_INVOICE, QUICKBOOKS_GET_ITEM, QUICKBOOKS_CREATE_ITEM

### Task 10 — Modify, delete, or undo incorrect QuickBooks ledger entries

Needed: `QUICKBOOKS_EXECUTE_BATCH_OPERATION`

Query: `QuickBooks delete void remove transaction entry`

   - primary: QUICKBOOKS_READ_INVOICE
   - related: QUICKBOOKS_UPDATE_FULL_INVOICE, QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_EXECUTE_BATCH_OPERATION, QUICKBOOKS_UPDATE_SPARSE_INVOICE, QUICKBOOKS_GET_ITEM, QUICKBOOKS_CREATE_ITEM

### Task 10 — Verify financial reports and transaction lists

Needed: `QUICKBOOKS_GET_REPORTS`

Query: `QuickBooks generate financial report balance sheet trial balance`

   - primary: QUICKBOOKS_GET_BALANCE_SHEET_REPORT
   - related: QUICKBOOKS_GET_REPORTS, QUICKBOOKS_GET_REPORT_ACCOUNT_LIST, QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_READ_ACCOUNT, QUICKBOOKS_GET_REPORT_TRIAL_BALANCE

### Task 12 — Add comments to Trello cards

Needed: `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`

Query: `update Trello card details`

   - primary: TRELLO_UPDATE_CARDS_BY_ID_CARD
   - related: TRELLO_GET_CARDS_BY_ID_CARD, TRELLO_GET_SEARCH, TRELLO_UPDATE_CARDS_DESC_BY_ID_CARD, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD

### Task 12 — Search or retrieve Trello cards and boards

Needed: `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH`

Query: `retrieve Trello card comments`

   - primary: TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD
   - related: TRELLO_GET_CARDS_BY_ID_CARD, TRELLO_GET_ACTIONS_BY_ID_ACTION, TRELLO_GET_BATCH, TRELLO_GET_SEARCH, TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD

### Task 13 — Send outreach and marketing emails

Needed: `GMAIL_SEND_EMAIL`

Query: `send email outreach marketing campaign gmail workspace`

   - primary: SENDGRID_CREATE_A_CAMPAIGN, SENDGRID_SEND_A_CAMPAIGN
   - related: GMAIL_SEARCH_PEOPLE, SENDGRID_RETRIEVE_ALL_LISTS, SENDGRID_SEND_A_TEST_MARKETING_EMAIL, GMAIL_CREATE_EMAIL_DRAFT, GMAIL_SEND_EMAIL

### Task 16 — Inspect source repository structure and file contents

Needed: `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_REPOSITORY_CONTENT`

Query: `list repositories github`

   - primary: GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER, GITHUB_LIST_REPOSITORY_ISSUES
   - related: GITHUB_GET_AN_ISSUE, GITHUB_LIST_ISSUE_COMMENTS, GITHUB_GET_A_REPOSITORY, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS, GITHUB_GET_THE_AUTHENTICATED_USER

### Task 17 — Upload supporting media assets for video creation

Needed: `HEYGEN_UPLOAD_ASSET`

Query: `Create a video using a HeyGen avatar and voice`

   - primary: HEYGEN_V2_VIDEO_GENERATE, HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS
   - related: HEYGEN_V1_AVATAR_LIST, HEYGEN_V2_VOICES, HEYGEN_V2_USER_REMAINING_QUOTA, HEYGEN_UPLOAD_ASSET, HEYGEN_RETRIEVE_SHARABLE_VIDEO_URL, HEYGEN_RETRIEVE_AVATAR_DETAILS

### Task 18 — Search and extract recent job listings from web sources or job boards

Needed: `BROWSER_TOOL_CREATE_TASK`

Query: `fetch URL content web page text markdown`

   - primary: COMPOSIO_SEARCH_FETCH_URL_CONTENT
   - related: COMPOSIO_SEARCH_WEB, BROWSER_TOOL_CREATE_TASK, BROWSER_TOOL_WATCH_TASK, BROWSER_TOOL_STOP_TASK, COMPOSIO_SEARCH_VERCEL_AI_CHAT

### Task 20 — Read and write Google Docs content and sections

Needed: `GOOGLEDOCS_GET_DOCUMENT_BY_ID`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`

Query: `search google docs documents`

   - primary: GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDRIVE_FIND_FILE
   - related: GOOGLEDRIVE_GET_ABOUT, GOOGLEDRIVE_LIST_SHARED_DRIVES, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT, GOOGLEDOCS_GET_DOCUMENT_BY_ID

### Task 20 — Inspect Zoho CRM module fields and metadata

Needed: `ZOHO_GET_MODULE_FIELDS`

Query: `search zoho crm records`

   - primary: ZOHO_SEARCH_ZOHO_RECORDS, ZOHO_GET_ZOHO_RECORDS
   - related: ZOHO_LIST_MODULES, ZOHO_GET_MODULE_FIELDS, ZOHO_GET_RELATED_LISTS, ZOHO_GET_RELATED_RECORDS

### Task 21 — Read spreadsheet structure, metadata, and cell values

Needed: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_GET_SPREADSHEET_INFO`

Query: `search spreadsheets or excel files`

   - primary: GOOGLESHEETS_SEARCH_SPREADSHEETS, GOOGLEDRIVE_FIND_FILE
   - related: GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_VALUES_GET, GOOGLESHEETS_BATCH_GET, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLESHEETS_GET_SPREADSHEET_INFO

### Task 23 — Fetch full Zendesk ticket details and associated comments

Needed: `ZENDESK_GET_ZENDESK_TICKET_BY_ID`

Query: `search zendesk tickets`

   - primary: ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_SEARCH_ZENDESK
   - related: ZENDESK_GET_ZENDESK_TICKET_BY_ID, ZENDESK_GET_USER, ZENDESK_GET_ABOUT_ME, ZENDESK_GET_VIEWS_TICKETS, ZENDESK_GET_SEARCH_COUNT, ZENDESK_GET_SEARCH_EXPORT

### Task 23 — Fetch single Zendesk user details by user ID for requester enrichment

Needed: `ZENDESK_GET_USER`

Query: `search zendesk tickets`

   - primary: ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_SEARCH_ZENDESK
   - related: ZENDESK_GET_ZENDESK_TICKET_BY_ID, ZENDESK_GET_USER, ZENDESK_GET_ABOUT_ME, ZENDESK_GET_VIEWS_TICKETS, ZENDESK_GET_SEARCH_COUNT, ZENDESK_GET_SEARCH_EXPORT

### Task 25 — Fetch and extract content from web page URLs

Needed: `COMPOSIO_SEARCH_FETCH_URL_CONTENT`

Query: `search job listings web search`

   - primary: COMPOSIO_SEARCH_WEB
   - related: COMPOSIO_SEARCH_FETCH_URL_CONTENT, COMPOSIO_SEARCH_NEWS, COMPOSIO_SEARCH_TRENDS, LINKEDIN_GET_POST_CONTENT

### Task 26 — Inspect file contents (downloading files for analysis)

Needed: `GOOGLEDRIVE_DOWNLOAD_FILE`

Query: `Download read inspect file contents Google Drive`

   - primary: GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT
   - related: GOOGLEDRIVE_DOWNLOAD_FILE, GOOGLEDRIVE_LIST_SHARED_DRIVES, GOOGLEDOCS_GET_DOCUMENT_BY_ID, GOOGLEDRIVE_GET_ABOUT

### Task 27 — Verify Google Drive access and account details

Needed: `GOOGLEDRIVE_GET_ABOUT`

Query: `list folders in Google Drive`

   - primary: GOOGLEDRIVE_FIND_FILE
   - related: GOOGLEDRIVE_LIST_SHARED_DRIVES, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_FIND_FOLDER, GOOGLEDRIVE_LIST_CHILDREN_V2, GOOGLEDRIVE_GET_ABOUT

### Task 29 — Inspect recent meeting notes and files from Google Drive

Needed: `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FOLDER`

Query: `Search Google Drive files`

   - primary: GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA
   - related: GOOGLEDRIVE_FIND_FOLDER, GOOGLEDRIVE_LIST_SHARED_DRIVES, GOOGLEDRIVE_GET_ABOUT, GOOGLEDRIVE_LIST_CHILDREN_V2, GOOGLEDRIVE_DOWNLOAD_FILE, GOOGLEDRIVE_EXPORT_GOOGLE_WORKSPACE_FILE

### Task 31 — Send notifications through WhatsApp or a Notis channel

Needed: `WHATSAPP_GET_PHONE_NUMBERS`

Query: `send whatsapp message or notification`

   - primary: WHATSAPP_SEND_MESSAGE
   - related: WHATSAPP_GET_PHONE_NUMBERS, WHATSAPP_GET_PHONE_NUMBER, WHATSAPP_GET_MESSAGE_TEMPLATES, WHATSAPP_SEND_TEMPLATE_MESSAGE, WHATSAPP_GET_TEMPLATE_STATUS, WHATSAPP_CREATE_MESSAGE_TEMPLATE

### Task 33 — Retrieve conversation threads and message history to analyze broadcast replies and audience interaction

Needed: `KOMMO_LIST_CONVERSATIONS`

Query: `Kommo CRM broadcast campaigns whatsapp analytics segments templates`

   - primary: KOMMO_LIST_TEMPLATES
   - related: KOMMO_LIST_CONVERSATIONS

### Task 35 — Post replies to Instagram comments in bulk

Needed: `INSTAGRAM_POST_IG_COMMENT_REPLIES`

Query: `fetch instagram media comments pagination`

   - primary: INSTAGRAM_GET_IG_MEDIA_COMMENTS
   - related: INSTAGRAM_GET_IG_USER_MEDIA, INSTAGRAM_GET_IG_COMMENT_REPLIES, INSTAGRAM_POST_IG_MEDIA_COMMENTS, INSTAGRAM_POST_IG_COMMENT_REPLIES, INSTAGRAM_GET_IG_MEDIA, INSTAGRAM_GET_USER_INFO

### Task 49 — Download or export files from Google Drive

Needed: `GOOGLEDRIVE_DOWNLOAD_FILE`

Query: `Search for recent files in Google Drive`

   - primary: GOOGLEDRIVE_FIND_FILE
   - related: GOOGLEDRIVE_GET_ABOUT, GOOGLEDRIVE_GET_FILE_METADATA, GOOGLEDRIVE_LIST_SHARED_DRIVES, GOOGLEDRIVE_DOWNLOAD_FILE, GOOGLEDRIVE_LIST_CHANGES, GOOGLEDRIVE_GET_CHANGES_START_PAGE_TOKEN

### Task 50 — Verify the correct Slack workspace and authentication

Needed: `SLACK_TEST_AUTH`

Query: `Verify or get details about the current Slack workspace`

   - primary: SLACK_GET_APP_PERMISSION_SCOPES
   - related: SLACK_TEST_AUTH

### Task 51 — Query Metabase for data and analytics evidence

Needed: `METABASE_POST_API_DATASET`

Query: `search for metabase dashboards or questions`

   - primary: METABASE_GET_API_SEARCH, METABASE_GET_DASHBOARD_BY_ID, METABASE_GET_API_CARD_ID
   - related: METABASE_GET_API_COLLECTION, METABASE_GET_API_COLLECTION_ID_ITEMS, METABASE_GET_CARD_DASHBOARDS, METABASE_LIST_DATABASES, METABASE_POST_API_DATASET, METABASE_GET_TABLE_SCHEMA

### Task 51 — Retrieve spreadsheet evidence

Needed: `GOOGLESHEETS_BATCH_GET`

Query: `search for spreadsheets or google sheets`

   - primary: GOOGLESHEETS_SEARCH_SPREADSHEETS
   - related: GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_GET_SHEET_NAMES, GOOGLESHEETS_BATCH_GET, GOOGLESHEETS_CREATE_GOOGLE_SHEET1, GOOGLEDRIVE_FIND_FILE

### Task 52 — Retrieve existing memories from Mem0

Needed: `MEM0_GET_MEMORIES_BY_ENTITY`

Query: `Search mem0 to retrieve user memory data`

   - primary: MEM0_RETRIEVE_MEMORY_LIST
   - related: MEM0_UPDATE_MEMORY_DETAILS_BY_ID, MEM0_LIST_ENTITIES_WITH_OPTIONAL_ORG_AND_PROJECT_FILTERS, MEM0_RETRIEVE_MEMORY_BY_UNIQUE_IDENTIFIER, MEM0_GET_USER_MEMORY_STATS, MEM0_GET_MEMORIES_BY_ENTITY

### Task 52 — Inspect existing Zep context, user nodes, and graph structure

Needed: `ZEP_GET_USER_NODE`

Query: `Zep inspect context migrate memories search`

   - primary: ZEP_GRAPH_SEARCH
   - related: ZEP_GET_USER_NODE, ZEP_GET_EDGE, ZEP_GET_NODE_EDGES, ZEP_GET_THREAD_USER_CONTEXT, ZEP_GET_SESSION_MEMORY

### Task 54 — Create and manage Google Ads campaigns

Needed: `GOOGLEADS_MUTATE_CAMPAIGNS`

Query: `audit advertising account health and performance in Google Ads`

   - primary: GOOGLEADS_SEARCH_STREAM_GAQL, GOOGLE_ANALYTICS_RUN_REPORT
   - related: GOOGLEADS_MUTATE_CAMPAIGNS, GOOGLEADS_MUTATE_AD_GROUPS, GOOGLEADS_GET_CAMPAIGN_BY_ID, GOOGLE_ANALYTICS_LIST_GOOGLE_ADS_LINKS, GOOGLEADS_LIST_ACCESSIBLE_CUSTOMERS

### Task 54 — Create and manage Google Ads ad groups

Needed: `GOOGLEADS_MUTATE_AD_GROUPS`

Query: `audit advertising account health and performance in Google Ads`

   - primary: GOOGLEADS_SEARCH_STREAM_GAQL, GOOGLE_ANALYTICS_RUN_REPORT
   - related: GOOGLEADS_MUTATE_CAMPAIGNS, GOOGLEADS_MUTATE_AD_GROUPS, GOOGLEADS_GET_CAMPAIGN_BY_ID, GOOGLE_ANALYTICS_LIST_GOOGLE_ADS_LINKS, GOOGLEADS_LIST_ACCESSIBLE_CUSTOMERS

### Task 55 — Manage worksheet properties and structure

Needed: `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES`

Query: `Google Sheets format and edit spreadsheet`

   - primary: GOOGLESHEETS_CREATE_GOOGLE_SHEET1, GOOGLESHEETS_UPDATE_VALUES_BATCH, GOOGLESHEETS_FORMAT_CELL
   - related: GOOGLESHEETS_ADD_SHEET, GOOGLESHEETS_UPDATE_SHEET_PROPERTIES, GOOGLESHEETS_GET_SPREADSHEET_INFO, GOOGLESHEETS_UPDATE_DIMENSION_PROPERTIES, GOOGLEDRIVE_CREATE_PERMISSION, GOOGLESHEETS_VALUES_UPDATE

### Task 56 — Inspect property definitions and metadata

Needed: `HUBSPOT_LIST_CONTACT_PROPERTIES`, `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE`

Query: `list contacts in HubSpot CRM`

   - primary: HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA
   - related: HUBSPOT_LIST_CONTACT_PROPERTIES, HUBSPOT_LIST_CONTACTS, HUBSPOT_SEARCH_CRM_OBJECTS_BY_CRITERIA, HUBSPOT_READ_CONTACT, HUBSPOT_RETRIEVE_OBJECT_SCHEMA

### Task 56 — Create associations between records

Needed: `HUBSPOT_CREATE_OBJECT_ASSOCIATION`

Query: `create associations between contacts and companies in HubSpot`

   - primary: HUBSPOT_CREATE_CONTACT_FROM_NL, HUBSPOT_REMOVE_ASSOCIATION, HUBSPOT_READ_ASSOCIATIONS_BATCH, HUBSPOT_CREATE_BATCH_OF_OBJECTS, HUBSPOT_LIST_OBJECT_ASSOCIATIONS, HUBSPOT_CREATE_DEALS
   - related: HUBSPOT_LIST_CONTACT_PROPERTIES, HUBSPOT_CREATE_CONTACT, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_CREATE_OBJECT_ASSOCIATION, HUBSPOT_LIST_ASSOCIATION_TYPES

### Task 57 — Analyze channel and trend performance on YouTube

Needed: `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CHANNEL_VIDEOS`, `YOUTUBE_SEARCH_YOU_TUBE`

Query: `Analyze YouTube channel and trend performance`

   - primary: YOUTUBE_GET_CHANNEL_STATISTICS, SUPADATA_SEARCH_YOUTUBE, DATAFORSEO_CREATE_KEYWORDS_DATA_GOOGLE_TRENDS_EXPLORE_TASK, TEXTCORTEX_CREATE_VIDEO_DESCRIPTION
   - related: GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY, YOUTUBE_SEARCH_YOU_TUBE, YOUTUBE_LIST_CHANNEL_VIDEOS, YOUTUBE_GET_VIDEO_DETAILS_BATCH, YOUTUBE_GET_CHANNEL_ID_BY_HANDLE, DATAFORSEO_GET_KW_GOOGLE_TRENDS_EXPLORE_TASK_BY_ID

### Task 57 — Inspect Instagram posting context and media

Needed: `INSTAGRAM_GET_IG_USER_MEDIA`

Query: `Inspect Instagram posting context`

   - primary: INSTAGRAM_GET_IG_MEDIA
   - related: INSTAGRAM_GET_IG_USER_MEDIA, INSTAGRAM_GET_IG_MEDIA_INSIGHTS, INSTAGRAM_GET_IG_MEDIA_COMMENTS

### Task 61 — Move messages into appropriate folders

Needed: `OUTLOOK_MOVE_MESSAGE`

Query: `move messages into folders in Outlook`

   - primary: OUTLOOK_LIST_MAIL_FOLDERS, OUTLOOK_QUERY_EMAILS, OUTLOOK_BATCH_MOVE_MESSAGES
   - related: OUTLOOK_MOVE_MESSAGE, OUTLOOK_LIST_CHILD_MAIL_FOLDERS, OUTLOOK_GET_MESSAGE, OUTLOOK_CREATE_MAIL_FOLDER, OUTLOOK_LIST_MAIL_FOLDER_MESSAGES, OUTLOOK_SEARCH_MESSAGES

### Task 61 — Mark selected messages as read or update their properties

Needed: `OUTLOOK_UPDATE_EMAIL`

Query: `mark messages as read in Outlook`

   - primary: OUTLOOK_BATCH_UPDATE_MESSAGES
   - related: OUTLOOK_QUERY_EMAILS, OUTLOOK_GET_MESSAGE, OUTLOOK_UPDATE_EMAIL, OUTLOOK_LIST_MAIL_FOLDER_MESSAGES

### Task 63 — List calendar events

Needed: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`

Query: `calendar events list search`

   - primary: GOOGLECALENDAR_EVENTS_LIST
   - related: GOOGLECALENDAR_LIST_CALENDARS, GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_GET_CALENDAR, GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_EVENTS_INSTANCES, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS

### Task 63 — Retrieve ecommerce store orders, products, and shop details

Needed: `SHOPIFY_GET_SHOP_DETAILS`

Query: `shopify ecommerce store order products list`

   - primary: SHOPIFY_GET_PRODUCTS_PAGINATED
   - related: SHOPIFY_COUNT_PRODUCTS, SHOPIFY_RETRIEVES_A_SINGLE_PRODUCT, SHOPIFY_BULK_QUERY_OPERATION, SHOPIFY_GET_SHOP_DETAILS, SHOPIFY_GET_PRODUCT_IMAGES, SHOPIFY_RETRIEVES_A_LIST_OF_PRODUCTS

### Task 66 — Update email message body or properties

Needed: `OUTLOOK_UPDATE_EMAIL`

Query: `Outlook create draft email with attachments`

   - primary: OUTLOOK_CREATE_DRAFT, OUTLOOK_ADD_MAIL_ATTACHMENT
   - related: OUTLOOK_LIST_OUTLOOK_ATTACHMENTS, OUTLOOK_GET_MESSAGE, OUTLOOK_UPDATE_EMAIL, OUTLOOK_SEND_DRAFT, OUTLOOK_QUERY_EMAILS, OUTLOOK_CREATE_ATTACHMENT_UPLOAD_SESSION

### Task 67 — Retrieve field metadata and requirements for Salesforce objects

Needed: `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT`

Query: `list open opportunities in Salesforce`

   - primary: SALESFORCE_RUN_SOQL_QUERY
   - related: SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT, SALESFORCE_GET_OPPORTUNITY, SALESFORCE_LIST_OPPORTUNITIES, SALESFORCE_GET_RECORD_COUNTS

### Task 69 — Inspect individual URLs for indexing status and issues

Needed: `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`

Query: `google search console sitemap migration indexability`

   - primary: GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP
   - related: GOOGLE_SEARCH_CONSOLE_LIST_SITES, GOOGLE_SEARCH_CONSOLE_GET_SITE, GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS, GOOGLE_SEARCH_CONSOLE_GET_SITEMAP, GOOGLE_SEARCH_CONSOLE_ADD_SITE, GOOGLE_SEARCH_CONSOLE_INSPECT_URL

### Task 71 — Check whether prior communication exists in email

Needed: `OUTLOOK_SEARCH_MESSAGES`

Query: `Send an email via Outlook`

   - primary: OUTLOOK_SEND_EMAIL
   - related: OUTLOOK_CREATE_DRAFT, OUTLOOK_SEND_DRAFT, OUTLOOK_UPDATE_EMAIL, OUTLOOK_ADD_MAIL_ATTACHMENT, OUTLOOK_GET_MAIL_TIPS, OUTLOOK_SEARCH_MESSAGES

### Task 72 — List branches in a GitHub repository

Needed: `GITHUB_LIST_BRANCHES`

Query: `GitHub repository file creation and management`

   - primary: GITHUB_GET_REPOSITORY_CONTENT, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS
   - related: GITHUB_LIST_BRANCHES, GITHUB_GET_A_REFERENCE, GITHUB_GET_A_TREE, GITHUB_GET_RAW_REPOSITORY_CONTENT, GITHUB_CREATE_A_PULL_REQUEST, GITHUB_COMMIT_MULTIPLE_FILES

### Task 73 — Manage and update tasks in Google Tasks

Needed: `GOOGLETASKS_LIST_TASKS`, `GOOGLETASKS_PATCH_TASK`

Query: `Google Tasks list tasks`

   - primary: GOOGLETASKS_LIST_ALL_TASKS
   - related: GOOGLETASKS_LIST_TASK_LISTS, GOOGLETASKS_LIST_TASKS, GOOGLETASKS_GET_TASK, GOOGLETASKS_PATCH_TASK, GOOGLETASKS_GET_TASK_LIST, GOOGLETASKS_BATCH_EXECUTE

### Task 76 — Retrieve ClickUp planning context from docs and tasks

Needed: `CLICKUP_GET_FILTERED_TEAM_TASKS`

Query: `pull ClickUp docs and tasks for planning context`

   - primary: CLICKUP_GET_SPACES, CLICKUP_GET_FOLDERLESS_LISTS, CLICKUP_GET_TASKS
   - related: CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES, CLICKUP_GET_LISTS, CLICKUP_GET_SHARED_HIERARCHY, CLICKUP_GET_FILTERED_TEAM_TASKS, CLICKUP_GET_LIST, CLICKUP_GET_FOLDERS

### Task 80 — Audit Trello board access/memberships

Needed: `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`

Query: `Trello create card with attachment and assign member`

   - primary: TRELLO_ADD_CARDS
   - related: TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_CARDS_BY_ID_CARD, TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD, TRELLO_GET_SEARCH_MEMBERS, TRELLO_UPDATE_CARDS_BY_ID_CARD, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD

### Task 80 — Find Trello member/assignee ID

Needed: `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_SEARCH_MEMBERS`

Query: `Trello create card with attachment and assign member`

   - primary: TRELLO_ADD_CARDS
   - related: TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_CARDS_BY_ID_CARD, TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD, TRELLO_GET_SEARCH_MEMBERS, TRELLO_UPDATE_CARDS_BY_ID_CARD, TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD

### Task 81 — Retrieve video details or metadata in bulk

Needed: `YOUTUBE_GET_VIDEO_DETAILS_BATCH`

Query: `list youtube channel videos`

   - primary: YOUTUBE_LIST_CHANNEL_VIDEOS
   - related: YOUTUBE_GET_VIDEO_DETAILS_BATCH, YOUTUBE_GET_CHANNEL_STATISTICS, YOUTUBE_LIST_PLAYLIST_ITEMS, YOUTUBE_GET_CHANNEL_ID_BY_HANDLE, YOUTUBE_GET_CHANNEL_ACTIVITIES

### Task 82 — List and locate mail folders

Needed: `OUTLOOK_LIST_CHILD_MAIL_FOLDERS`, `OUTLOOK_LIST_MAIL_FOLDERS`

Query: `Search Outlook inbox messages and filter by sender subject unread status folder`

   - primary: OUTLOOK_LIST_CHILD_FOLDER_MESSAGES, OUTLOOK_QUERY_EMAILS, OUTLOOK_LIST_MAIL_FOLDER_MESSAGES
   - related: OUTLOOK_GET_CHILD_FOLDER_MESSAGE, OUTLOOK_GET_CHILD_MAIL_FOLDER, OUTLOOK_LIST_MAIL_FOLDERS, OUTLOOK_SEARCH_MESSAGES, OUTLOOK_LIST_CHILD_MAIL_FOLDERS

### Task 82 — Delete unwanted messages

Needed: `OUTLOOK_DELETE_MESSAGE`

Query: `Move Outlook email message to folder or deleted items`

   - primary: OUTLOOK_BATCH_MOVE_MESSAGES
   - related: OUTLOOK_QUERY_EMAILS, OUTLOOK_LIST_MAIL_FOLDERS, OUTLOOK_MOVE_MESSAGE, OUTLOOK_DELETE_MESSAGE, OUTLOOK_GET_MESSAGE, OUTLOOK_SEARCH_MESSAGES

### Task 84 — Create a new repository

Needed: `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY`

Query: `create a repository in GitHub`

   - primary: GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER
   - related: GITHUB_GET_A_REPOSITORY, GITHUB_LIST_ORGANIZATIONS_FOR_THE_AUTHENTICATED_USER, GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY, GITHUB_UPDATE_A_REPOSITORY, GITHUB_COMMIT_MULTIPLE_FILES, GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS

### Task 85 — Search code and retrieve repository contents to investigate the codebase

Needed: `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_SEARCH_CODE`

Query: `GitHub list user repositories`

   - primary: GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER
   - related: GITHUB_GET_THE_AUTHENTICATED_USER, GITHUB_LIST_ORGANIZATIONS_FOR_THE_AUTHENTICATED_USER, GITHUB_FIND_REPOSITORIES, GITHUB_GET_A_REPOSITORY, GITHUB_LIST_REPOSITORIES_FOR_A_USER, GITHUB_GET_REPOSITORY_CONTENT

### Task 87 — Read content or block structures from specific Notion pages

Needed: `NOTION_FETCH_ALL_BLOCK_CONTENTS`, `NOTION_GET_PAGE_MARKDOWN`

Query: `search notion databases or pages`

   - primary: NOTION_SEARCH_NOTION_PAGE
   - related: NOTION_FETCH_DATA, NOTION_RETRIEVE_PAGE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_FETCH_DATABASE, NOTION_GET_PAGE_MARKDOWN, NOTION_FETCH_ALL_BLOCK_CONTENTS

### Task 87 — Update existing Notion database rows or pages during reorganization

Needed: `NOTION_UPDATE_ROW_DATABASE`

Query: `create row or add page to notion database`

   - primary: NOTION_SEARCH_NOTION_PAGE, NOTION_FETCH_DATABASE, NOTION_INSERT_ROW_DATABASE
   - related: NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_UPSERT_ROW_DATABASE, NOTION_UPDATE_ROW_DATABASE, NOTION_QUERY_DATABASE

### Task 88 — Fetch detailed ticket information including comments and requester context

Needed: `ZENDESK_GET_ZENDESK_TICKET_BY_ID`

Query: `Search and list support tickets in Zendesk`

   - primary: ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_SEARCH_ZENDESK
   - related: ZENDESK_GET_ZENDESK_TICKET_BY_ID, ZENDESK_GET_USER, ZENDESK_GET_ABOUT_ME, ZENDESK_GET_VIEWS_TICKETS, ZENDESK_GET_SEARCH_COUNT, ZENDESK_GET_SEARCH_EXPORT

### Task 88 — Enrich tickets with requester details

Needed: `ZENDESK_GET_USER`

Query: `Search and list support tickets in Zendesk`

   - primary: ZENDESK_LIST_ZENDESK_TICKETS, ZENDESK_SEARCH_ZENDESK
   - related: ZENDESK_GET_ZENDESK_TICKET_BY_ID, ZENDESK_GET_USER, ZENDESK_GET_ABOUT_ME, ZENDESK_GET_VIEWS_TICKETS, ZENDESK_GET_SEARCH_COUNT, ZENDESK_GET_SEARCH_EXPORT

### Task 90 — Inspect existing presentation, slides, layouts, and page details

Needed: `GOOGLESLIDES_PRESENTATIONS_GET`, `GOOGLESLIDES_PRESENTATIONS_PAGES_GET`

Query: `search or inspect google slides presentations and layouts`

   - primary: GOOGLEDRIVE_FIND_FILE
   - related: GOOGLEDRIVE_GET_FILE_METADATA, GOOGLESLIDES_PRESENTATIONS_GET, GOOGLESLIDES_PRESENTATIONS_PAGES_GET, GOOGLESLIDES_GET_PAGE_THUMBNAIL2, GOOGLEDRIVE_LIST_SHARED_DRIVES

### Task 91 — Manage or retrieve Meta ads reporting and campaign status

Needed: `METAADS_GET_INSIGHTS`

Query: `manage Meta ads reporting and campaign status`

   - primary: NOTION_APPEND_TEXT_BLOCKS, NOTION_FETCH_BLOCK_CONTENTS
   - related: METAADS_GET_INSIGHTS, NOTION_RETRIEVE_PAGE, NOTION_UPDATE_BLOCK, NOTION_REPLACE_PAGE_CONTENT

### Task 94 — List ad sets under an ad account

Needed: `METAADS_READ_ADSETS`

Query: `retrieve Meta Ads account campaign ad set ad creative performance targeting pixel data`

   - primary: METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS
   - related: METAADS_LIST_BUSINESS_AD_ACCOUNTS, METAADS_LIST_CLIENT_AD_ACCOUNTS, METAADS_GET_OBJECT, METAADS_READ_ADSETS, METAADS_GET_USER, METAADS_LIST_ADS

### Task 94 — List ads under an ad account

Needed: `METAADS_LIST_ADS`

Query: `retrieve Meta Ads account campaign ad set ad creative performance targeting pixel data`

   - primary: METAADS_GET_AD_ACCOUNTS, METAADS_GET_INSIGHTS
   - related: METAADS_LIST_BUSINESS_AD_ACCOUNTS, METAADS_LIST_CLIENT_AD_ACCOUNTS, METAADS_GET_OBJECT, METAADS_READ_ADSETS, METAADS_GET_USER, METAADS_LIST_ADS

### Task 95 — List bank transactions

Needed: `ZOHO_BOOKS_LIST_BANK_TRANSACTIONS`

Query: `fetch bank accounts in zoho books`

   - primary: ZOHO_BOOKS_GET_BANK_ACCOUNT, ZOHO_BOOKS_LIST_BANK_ACCOUNTS
   - related: ZOHO_BOOKS_LIST_ORGANIZATIONS, ZOHO_BOOKS_LIST_BANK_TRANSACTIONS, ZOHO_BOOKS_CREATE_BANK_TRANSACTION

### Task 96 — Browse or retrieve repository structure and file contents

Needed: `GITHUB_GET_A_TREE`

Query: `create commit create or update file repository tests check status`

   - primary: GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS
   - related: GITHUB_CREATE_A_PULL_REQUEST, GITHUB_GET_A_BRANCH, GITHUB_GET_REPOSITORY_CONTENT, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_GET_A_TREE, GITHUB_COMMIT_MULTIPLE_FILES

### Task 96 — Create commits in the GitHub repository

Needed: `GITHUB_COMMIT_MULTIPLE_FILES`

Query: `create commit create or update file repository tests check status`

   - primary: GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS
   - related: GITHUB_CREATE_A_PULL_REQUEST, GITHUB_GET_A_BRANCH, GITHUB_GET_REPOSITORY_CONTENT, GITHUB_LIST_CHECK_RUNS_FOR_A_REF, GITHUB_GET_A_TREE, GITHUB_COMMIT_MULTIPLE_FILES

### Task 96 — Verify commit details and CI check-run status

Needed: `GITHUB_GET_A_COMMIT`, `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`

Query: `GitHub repository commit files run tests check status`

   - primary: GITHUB_GET_A_REPOSITORY, GITHUB_LIST_COMMITS, GITHUB_LIST_REPOSITORY_ISSUES
   - related: GITHUB_FIND_REPOSITORIES, GITHUB_FIND_PULL_REQUESTS, GITHUB_GET_AN_ISSUE, GITHUB_GET_A_COMMIT, GITHUB_GET_A_BRANCH, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS

### Task 99 — Inspect Supabase schema and run read-only database queries

Needed: `SUPABASE_LIST_TABLES`, `SUPABASE_RUN_READ_ONLY_QUERY`

Query: `supabase inspect schema tables`

   - primary: SUPABASE_GET_TABLE_SCHEMAS, SUPABASE_BETA_RUN_SQL_QUERY
   - related: SUPABASE_RUN_READ_ONLY_QUERY, SUPABASE_LIST_TABLES, SUPABASE_SELECT_FROM_TABLE, SUPABASE_LIST_ALL_PROJECTS, SUPABASE_APPLY_A_MIGRATION, SUPABASE_GENERATE_TYPESCRIPT_TYPES

### Task 100 — Query and retrieve Attio company records and their domains/attributes

Needed: `ATTIO_QUERY_RECORDS`

Query: `list records in attio companies object`

   - primary: ATTIO_LIST_COMPANIES
   - related: ATTIO_QUERY_RECORDS, ATTIO_LIST_ATTRIBUTES, ATTIO_GET_OBJECT, ATTIO_LIST_OBJECTS, ATTIO_FIND_RECORD
