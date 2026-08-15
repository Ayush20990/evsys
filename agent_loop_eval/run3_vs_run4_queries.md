# Run 3 (fully mocked) vs Run 4 (real reads) — query-by-query

Same 10 tasks, same model, same prompt. The only difference is execution: run 3 mocked every
tool call, run 4 executed read-only tools for real against 9 connected toolkits (`cal`,
`clickup`, `gmail`, `googlecalendar`, `linkedin`, `notion`, `one_drive`, `salesforce`,
`trello`). Writes stayed mocked in both.

**Read the totals with care.** Run 4 exhausted the Gemini quota during task 7, so tasks 7-10 are
truncated or empty and their numbers reflect that, not retrieval. Only tasks 1-6 are comparable.

## Tasks 1-6 (both runs completed)

| Task | run3 queries | run3 union | run3 primary | run4 queries | run4 union | run4 primary | run4 real execs |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 8/10 | 4/10 | 4 | 8/10 | 2/10 | 0/5 |
| 2 | 8 | 6/6 | 4/6 | 3 | 6/6 | 3/6 | 10/13 |
| 3 | 9 | 4/4 | 3/4 | 8 | 4/4 | 2/4 | 3/9 |
| 4 | 12 | 10/10 | 8/10 | 5 | 9/10 | 3/10 | 6/8 |
| 5 | 11 | 16/17 | 8/17 | 6 | 16/17 | 9/17 | 3/3 |
| 6 | 7 | 7/11 | 4/11 | 3 | 4/11 | 2/11 | 7/7 |
| **total** | **56** | **51/58 (88%)** | **31/58 (53%)** | **29** | **47/58 (81%)** | **21/58 (36%)** | |

Union hits per query: run3 **0.91**, run4 **1.62**. Run 4's lower totals come from
issuing half as many queries, not from worse retrieval — with real data the agent finds a working
tool and moves on instead of re-searching.

## Task 1

> Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify the assets remain inert, and attempt to create a custom-object registration ledger.

**Run 3 — fully mocked** — 9 queries, union 8/10, primary 4/10, stop: _agent finished_

execution: `{'mocked': 5, 'mock-rejected': 3}`

1. `Check payment link feasibility or creation in HubSpot`
   - intent: Assess payment link feasibility in HubSpot
   - primary: HUBSPOT_CREATE_FEEDBACK_SUBMISSION
2. `Create a marketing email in HubSpot`
   - intent: Search for HubSpot tools relating to marketing email creation
   - primary: HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL
3. `Create or manage workflows in HubSpot`
   - intent: Search for HubSpot tools relating to workflows
   - primary: HUBSPOT_GET_ALL_WORKFLOWS
4. `Create a new workflow in HubSpot`
   - intent: Search for HubSpot tools to create workflows
   - primary: HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT
5. `Create custom object schema in HubSpot`
   - intent: Search for HubSpot tools for custom objects and schemas
   - primary: HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS
6. `List payment links in HubSpot`
   - intent: Search for HubSpot tools to list existing payment links or payment configuration
   - primary: HUBSPOT_LIST_DEALS
7. `Get account info in HubSpot`
   - intent: Search for HubSpot account info tools
   - primary: HUBSPOT_GET_ACCOUNT_INFO
8. `Get workflow by ID in HubSpot`
   - intent: Get workflow details to inspect action structure
   - primary: HUBSPOT_GET_WORKFLOW_BY_ID, HUBSPOT_GET_WORKFLOWS
9. `Get workflow by id in HubSpot`
   - intent: Search for workflow verification or get workflow details tool
   - primary: HUBSPOT_GET_ALL_WORKFLOWS

| tool | mode | empty |
|---|---|---|
| `HUBSPOT_GET_ACCOUNT_INFO` | mocked |  |
| `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL` | mocked |  |
| `HUBSPOT_CREATE_WORKFLOW` | mock-rejected |  |
| `HUBSPOT_GET_WORKFLOWS` | mocked |  |
| `HUBSPOT_CREATE_WORKFLOW` | mock-rejected |  |
| `HUBSPOT_CREATE_WORKFLOW` | mocked |  |
| `HUBSPOT_CREATE_OBJECT_SCHEMA` | mock-rejected |  |
| `HUBSPOT_CREATE_OBJECT_SCHEMA` | mocked |  |

missed: `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT`, `HUBSPOT_SEARCH_EMAILS`

**Run 4 — real reads** — 4 queries, union 8/10, primary 2/10, stop: _agent finished_

execution: `{'mocked': 3, 'mock-rejected': 2}`

1. `HubSpot payment links create or check feasibility`
   - intent: Assess payment link feasibility in HubSpot marketing or sales tools
   - primary: HUBSPOT_CREATE_DEALS
2. `HubSpot create email marketing template`
   - intent: Create an automated confirmation email in HubSpot marketing or email tools
   - primary: HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL
3. `HubSpot create workflow automation`
   - intent: Create a disabled confirmation workflow in HubSpot automation tools
   - primary: HUBSPOT_CREATE_WORKFLOW, HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA, HUBSPOT_UPDATE_CONTACT
4. `HubSpot create custom object schema`
   - intent: Attempt to create a custom-object registration ledger in HubSpot schema tools
   - primary: HUBSPOT_CREATE_OBJECT_SCHEMA, HUBSPOT_UPDATE_OBJECT_SCHEMA, HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS

| tool | mode | empty |
|---|---|---|
| `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL` | mocked |  |
| `HUBSPOT_CREATE_WORKFLOW` | mock-rejected |  |
| `HUBSPOT_CREATE_WORKFLOW` | mocked |  |
| `HUBSPOT_CREATE_OBJECT_SCHEMA` | mock-rejected |  |
| `HUBSPOT_CREATE_OBJECT_SCHEMA` | mocked |  |

missed: `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT`, `HUBSPOT_SEARCH_EMAILS`

## Task 2

> Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.

**Run 3 — fully mocked** — 8 queries, union 6/6, primary 4/6, stop: _step ceiling reached_

execution: `{'mocked': 5, 'mock-rejected': 5}`

1. `Retrieve upcoming Google Calendar meeting events`
   - intent: Retrieve upcoming Google Calendar meeting events
   - primary: GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS
2. `Create or update Notion content or database pages with verification`
   - intent: Create or update Notion content containing a large structured dataset with verification
   - primary: NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT
3. `Search Notion pages`
   - intent: Search Notion pages to find a suitable parent page or database
   - primary: NOTION_SEARCH_NOTION_PAGE
4. `List Google Calendar settings`
   - intent: List Google Calendar settings to get timezone
   - primary: GOOGLECALENDAR_SETTINGS_LIST, GOOGLESUPER_SETTINGS_LIST
5. `List Google Calendar events with time_min and time_max`
   - intent: List Google Calendar events with time_min and time_max
   - primary: GOOGLECALENDAR_EVENTS_LIST
6. `Create a new Notion page`
   - intent: Create a new Notion page with parent id
   - primary: NOTION_CREATE_NOTION_PAGE
7. `Add multiple page content in Notion`
   - intent: Add multiple page content in Notion
   - primary: NOTION_ADD_MULTIPLE_PAGE_CONTENT
8. `Get page markdown in Notion for verification`
   - intent: Get page markdown in Notion for verification
   - primary: NOTION_GET_PAGE_MARKDOWN

| tool | mode | empty |
|---|---|---|
| `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` | mocked |  |
| `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` | mock-rejected |  |
| `GOOGLECALENDAR_SETTINGS_LIST` | mocked |  |
| `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` | mock-rejected |  |
| `GOOGLECALENDAR_LIST_CALENDARS` | mocked |  |
| `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` | mock-rejected |  |
| `GOOGLECALENDAR_EVENTS_LIST` | mocked |  |
| `NOTION_SEARCH_NOTION_PAGE` | mocked |  |
| `NOTION_CREATE_NOTION_PAGE` | mock-rejected |  |
| `NOTION_ADD_MULTIPLE_PAGE_CONTENT` | mock-rejected |  |

**Run 4 — real reads** — 3 queries, union 6/6, primary 3/6, stop: _agent finished_

execution: `{'real': 10, 'mock-rejected': 3}`

1. `Retrieve upcoming Google Calendar meeting events`
   - intent: Retrieve upcoming Google Calendar meeting events
   - primary: GOOGLECALENDAR_GET_CURRENT_DATE_TIME, GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS
2. `Create or update Notion database or page content with verification`
   - intent: Create or update Notion content containing a large structured dataset with verification
   - primary: NOTION_CREATE_NOTION_PAGE, NOTION_ADD_MULTIPLE_PAGE_CONTENT
3. `Search Notion database or pages`
   - intent: Search Notion database or pages
   - primary: NOTION_SEARCH_NOTION_PAGE

| tool | mode | empty |
|---|---|---|
| `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` | real |  |
| `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` | real |  |
| `GOOGLECALENDAR_SETTINGS_LIST` | real |  |
| `GOOGLECALENDAR_LIST_CALENDARS` | real |  |
| `GOOGLECALENDAR_EVENTS_LIST` | real | yes |
| `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` | real |  |
| `NOTION_SEARCH_NOTION_PAGE` | real |  |
| `NOTION_CREATE_NOTION_PAGE` | mock-rejected |  |
| `NOTION_ADD_MULTIPLE_PAGE_CONTENT` | mock-rejected |  |
| `NOTION_GET_PAGE_MARKDOWN` | real |  |
| `NOTION_RETRIEVE_PAGE` | real |  |
| `NOTION_GET_PAGE_MARKDOWN` | real |  |
| `NOTION_CREATE_NOTION_PAGE` | mock-rejected |  |

## Task 3

> Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.

**Run 3 — fully mocked** — 9 queries, union 4/4, primary 3/4, stop: _step ceiling reached_

execution: `{'mocked': 6, 'mock-rejected': 3}`

1. `find spreadsheet in OneDrive`
   - intent: Find a spreadsheet file in OneDrive
   - primary: ONE_DRIVE_SEARCH_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN
2. `download file from OneDrive`
   - intent: Download a file from OneDrive
   - primary: ONE_DRIVE_GET_DRIVE_ITEM_BY_SHARING_URL, ONE_DRIVE_DOWNLOAD_FILE
3. `upload update file content OneDrive`
   - intent: Upload a file back to OneDrive item or update file content in OneDrive
   - primary: ONE_DRIVE_UPDATE_FILE_CONTENT
4. `remote workbench execute python bash`
   - intent: Remote workbench execute python or bash to process spreadsheets or download upload files
   - primary: DAYTONA_EXECUTE_COMMAND
5. `get recent items OneDrive root`
   - intent: Get recent items or root items in OneDrive
   - primary: ONE_DRIVE_LIST_ROOT_DRIVE_CHANGES, ONE_DRIVE_GET_RECENT_ITEMS
6. `start sandbox daytona`
   - intent: Start a daytona sandbox
   - primary: DAYTONA_START_SANDBOX, DAYTONA_START_COMPUTER_USE
7. `list root folder children OneDrive`
   - intent: List root folder children in OneDrive
   - primary: ONE_DRIVE_ONEDRIVE_FIND_FOLDER, ONE_DRIVE_LIST_FOLDER_CHILDREN
8. `list items in OneDrive folder`
   - intent: List files and folders in OneDrive item
   - primary: ONE_DRIVE_ONEDRIVE_LIST_ITEMS, ONE_DRIVE_LIST_FOLDER_CHILDREN
9. `search items in OneDrive query`
   - intent: Search items in OneDrive with a query string
   - primary: ONE_DRIVE_SEARCH_ITEMS

| tool | mode | empty |
|---|---|---|
| `ONE_DRIVE_GET_RECENT_ITEMS` | mocked |  |
| `ONE_DRIVE_SEARCH_ITEMS` | mock-rejected |  |
| `ONE_DRIVE_LIST_ROOT_DRIVE_CHANGES` | mocked |  |
| `DAYTONA_START_SANDBOX` | mock-rejected |  |
| `ONE_DRIVE_GET_ROOT` | mocked |  |
| `ONE_DRIVE_LIST_FOLDER_CHILDREN` | mocked |  |
| `ONE_DRIVE_ONEDRIVE_LIST_ITEMS` | mocked |  |
| `ONE_DRIVE_SEARCH_ITEMS` | mock-rejected |  |
| `ONE_DRIVE_LIST_DRIVES` | mocked |  |

**Run 4 — real reads** — 8 queries, union 4/4, primary 2/4, stop: _agent finished_

execution: `{'mock-rejected': 2, 'mocked': 4, 'real': 3}`

1. `Find and download a spreadsheet file from OneDrive`
   - intent: Find and download a spreadsheet file from OneDrive
   - primary: ONE_DRIVE_DOWNLOAD_FILE_BY_PATH
2. `Search for files in OneDrive`
   - intent: Search for files in OneDrive
   - primary: ONE_DRIVE_SEARCH_ITEMS
3. `Upload a file back to OneDrive`
   - intent: Upload a file back to OneDrive
   - primary: ONE_DRIVE_ONEDRIVE_UPLOAD_FILE
4. `Update file content in OneDrive`
   - intent: Update an existing file content in OneDrive
   - primary: ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE, ONE_DRIVE_UPDATE_FILE_CONTENT
5. `Run a python script or workbench command to manipulate files or execute code`
   - intent: Run a python script or workbench command to manipulate files or execute code
   - primary: E2B_POST_SANDBOXES, E2B_CONNECT_SANDBOX
6. `Execute python code or workbench command`
   - intent: Execute python code or workbench command
   - primary: E2B_POST_SANDBOXES, E2B_CONNECT_SANDBOX
7. `List available E2B sandbox templates`
   - intent: List available E2B sandbox templates
   - primary: E2B_GET_HEALTH, E2B_LIST_SANDBOXES, E2B_LIST_TEMPLATES
8. `Upload file using OneDrive upload file tool`
   - intent: Upload file using OneDrive upload file tool
   - primary: ONE_DRIVE_ONEDRIVE_UPLOAD_FILE

| tool | mode | empty |
|---|---|---|
| `ONE_DRIVE_SEARCH_ITEMS` | mock-rejected |  |
| `ONE_DRIVE_SEARCH_ITEMS` | mocked |  |
| `ONE_DRIVE_DOWNLOAD_FILE_BY_PATH` | real |  |
| `ONE_DRIVE_DOWNLOAD_FILE_BY_PATH` | real |  |
| `E2B_POST_SANDBOXES` | mock-rejected |  |
| `E2B_LIST_TEMPLATES` | mocked |  |
| `E2B_POST_SANDBOXES` | mocked |  |
| `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE` | mocked |  |
| `ONE_DRIVE_GET_ITEM` | real |  |

## Task 4

> Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.

**Run 3 — fully mocked** — 12 queries, union 10/10, primary 8/10, stop: _step ceiling reached_

execution: `{'mocked': 5, 'mock-rejected': 1}`

1. `trello get cards in list or board`
   - intent: Find cards in a Trello board to locate approved carousel content
   - primary: TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_LISTS_CARDS_BY_ID_LIST
2. `linkedin create post and comment`
   - intent: Search for tools related to LinkedIn posting and comments
   - primary: LINKEDIN_CREATE_LINKED_IN_POST
3. `trello update card move list create list`
   - intent: Search for Trello tools to update cards, move cards, create lists, or change workflow structure
   - primary: TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD, TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD, TRELLO_ADD_CARDS
4. `linkedin add comment to post`
   - intent: Search for LinkedIn tools to add a comment to a post
   - primary: LINKEDIN_CREATE_COMMENT_ON_POST
5. `trello create list on board`
   - intent: Search for Trello tools to create a list on a board
   - primary: TRELLO_ADD_LISTS
6. `trello get boards for member`
   - intent: Search for Trello tools to get authenticated member boards
   - primary: TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER_BY_FILTER
7. `trello add comment to card`
   - intent: Search for Trello tools to create a comment on a card
   - primary: TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD
8. `trello search query`
   - intent: Search for Trello search tool
   - primary: TRELLO_GET_SEARCH_MEMBERS
9. `trello search cards query`
   - intent: Search Trello board or global search
   - primary: TRELLO_GET_SEARCH
10. `linkedin get my info author urn`
   - intent: Get LinkedIn my info to get author URN
   - primary: LINKEDIN_GET_MY_INFO
11. `linkedin create comment on post schema`
   - intent: Search tools for creating comment on linkedin post with correct schema
   - primary: LINKEDIN_CREATE_COMMENT_ON_POST
12. `get definition for LINKEDIN_CREATE_COMMENT_ON_POST`
   - intent: Search tool definition for linkedin create comment on post
   - primary: LINKEDIN_CREATE_COMMENT_ON_POST

| tool | mode | empty |
|---|---|---|
| `TRELLO_GET_MEMBERS_ME` | mocked |  |
| `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER` | mocked |  |
| `TRELLO_GET_SEARCH` | mocked |  |
| `LINKEDIN_GET_MY_INFO` | mocked |  |
| `LINKEDIN_CREATE_LINKED_IN_POST` | mocked |  |
| `LINKEDIN_CREATE_COMMENT_ON_POST` | mock-rejected |  |

**Run 4 — real reads** — 5 queries, union 9/10, primary 3/10, stop: _agent finished_

execution: `{'real': 6, 'mock-rejected': 1, 'mocked': 1}`

1. `get cards from Trello board workflow`
   - intent: Find approved carousel content from a Trello board workflow
   - primary: TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD
2. `publish post to LinkedIn`
   - intent: Publish carousel content to LinkedIn
   - primary: LINKEDIN_CREATE_LINKED_IN_POST
3. `add comment to LinkedIn post`
   - intent: Add a comment to a LinkedIn post
   - primary: LINKEDIN_CREATE_COMMENT_ON_POST
4. `update Trello card status or add comment`
   - intent: Update Trello card status or add comments/logs
   - primary: TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD, TRELLO_UPDATE_ACTIONS_TEXT_BY_ID_ACTION
5. `update create Trello list on board`
   - intent: Update Trello board workflow structure lists
   - primary: TRELLO_ADD_LISTS

| tool | mode | empty |
|---|---|---|
| `TRELLO_GET_MEMBERS_ME` | real |  |
| `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER_BY_FILTER` | real |  |
| `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER_BY_FILTER` | real | yes |
| `LINKEDIN_GET_MY_INFO` | real |  |
| `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD` | real |  |
| `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD` | real |  |
| `LINKEDIN_CREATE_LINKED_IN_POST` | mock-rejected |  |
| `TRELLO_ADD_LISTS` | mocked |  |

missed: `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`

## Task 5

> Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, and write evidence-supported CRM status updates.

**Run 3 — fully mocked** — 11 queries, union 16/17, primary 8/17, stop: _step ceiling reached_

execution: `{'mocked': 6, 'mock-rejected': 1}`

1. `partner operations pipeline gmail clickup notion`
   - intent: Find and manage partner operations across Gmail, ClickUp, and Notion
   - primary: NOTION_INSERT_ROW_FROM_NL, NOTION_UPSERT_ROW_DATABASE
2. `search and read gmail email threads`
   - intent: Search for tools to interact with Gmail email threads and messages
   - primary: GMAIL_FETCH_EMAILS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID
3. `clickup create task handoff`
   - intent: Search for tools to create and manage ClickUp tasks and handoffs
   - primary: CLICKUP_CREATE_TASK
4. `create gmail draft`
   - intent: Search for Gmail draft creation tool
   - primary: GMAIL_CREATE_EMAIL_DRAFT
5. `notion query database or search database`
   - intent: Search for Notion database query or search tools
   - primary: NOTION_QUERY_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER
6. `search notion pages workspace`
   - intent: Search Notion pages or search workspace for databases
   - primary: NOTION_SEARCH_NOTION_PAGE
7. `list gmail threads messages`
   - intent: List Gmail emails or threads
   - primary: GMAIL_LIST_THREADS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID
8. `clickup get tasks list`
   - intent: ClickUp get tasks or lists
   - primary: CLICKUP_GET_FILTERED_TEAM_TASKS, CLICKUP_GET_TASK
9. `search notion databases workspace pages`
   - intent: Get Notion databases or pages in workspace
   - primary: NOTION_SEARCH_NOTION_PAGE
10. `notion fetch database data`
   - intent: Get Notion databases or fetch data in Notion
   - primary: NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_QUERY_DATABASE
11. `clickup get lists space folder`
   - intent: ClickUp get lists in space
   - primary: CLICKUP_GET_FOLDERLESS_LISTS, CLICKUP_GET_FOLDERS, CLICKUP_GET_LISTS

| tool | mode | empty |
|---|---|---|
| `NOTION_SEARCH_NOTION_PAGE` | mocked |  |
| `NOTION_SEARCH_NOTION_PAGE` | mocked |  |
| `GMAIL_LIST_THREADS` | mocked |  |
| `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` | mocked |  |
| `NOTION_SEARCH_NOTION_PAGE` | mocked |  |
| `GMAIL_FETCH_EMAILS` | mocked |  |
| `CLICKUP_GET_SPACES` | mock-rejected |  |

missed: `CLICKUP_UPDATE_TASK`

**Run 4 — real reads** — 6 queries, union 16/17, primary 9/17, stop: _agent finished_

execution: `{'real': 3}`

1. `gmail create draft search email threads`
   - intent: Search for gmail tools to create outreach drafts or scan email threads
   - primary: GMAIL_LIST_THREADS, GMAIL_FETCH_MESSAGE_BY_THREAD_ID, GMAIL_CREATE_EMAIL_DRAFT
2. `clickup create task update task handoff`
   - intent: Search for ClickUp tools to create task handoffs and inspect update handoffs
   - primary: CLICKUP_CREATE_TASK
3. `notion query database update page crm`
   - intent: Search for Notion tools to scan CRM records and write status updates
   - primary: NOTION_FETCH_DATABASE, NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_INSERT_ROW_DATABASE
4. `notion search page database`
   - intent: Search for Notion search page to find CRM database id
   - primary: NOTION_SEARCH_NOTION_PAGE
5. `clickup update task details`
   - intent: Search for ClickUp tasks update tool
   - primary: CLICKUP_UPDATE_TASK, CLICKUP_GET_TASK
6. `clickup get teams workspaces`
   - intent: Search for ClickUp teams workspaces to get team id for clickup operations
   - primary: CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES

| tool | mode | empty |
|---|---|---|
| `GMAIL_LIST_THREADS` | real |  |
| `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` | real |  |
| `NOTION_SEARCH_NOTION_PAGE` | real |  |

missed: `NOTION_UPDATE_PAGE`

## Task 6

> Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.

**Run 3 — fully mocked** — 7 queries, union 7/11, primary 4/11, stop: _step ceiling reached_

execution: `{'mocked': 9, 'mock-rejected': 2}`

1. `salesforce leads contacts campaign membership attendance status static list MQL lead activity reporting`
   - intent: Search Salesforce tools for managing leads, contacts, campaign membership, campaign status, static lists, and MQL lead activity reporting
   - primary: SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS
2. `salesforce manage campaigns campaign members campaign member status static list`
   - intent: Search Salesforce tools for managing campaigns, campaign members, campaign member status, and static lists
   - primary: SALESFORCE_SEARCH_CONTACTS, SALESFORCE_SEARCH_CAMPAIGNS, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN
3. `salesforce create lead contact update campaign member status report`
   - intent: Search all Salesforce tools to see what creation, update, and reporting tools are available
   - primary: SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_CONTACT_TO_CAMPAIGN
4. `salesforce update campaign member status attendance`
   - intent: Search Salesforce tools for updating campaign member status and campaign members
   - primary: SALESFORCE_ADD_LEAD_TO_CAMPAIGN, SALESFORCE_UPDATE_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN
5. `salesforce update campaign member status field`
   - intent: Search Salesforce tools for updating campaign member records directly
   - primary: SALESFORCE_UPDATE_CAMPAIGN
6. `salesforce update sobject campaign member`
   - intent: Search Salesforce tools for updating generic sObjects or campaign members
   - primary: SALESFORCE_UPDATE_CAMPAIGN, SALESFORCE_REMOVE_FROM_CAMPAIGN
7. `salesforce custom rest api call or campaign member update`
   - intent: Search for campaign member management tools or custom API calls
   - primary: SALESFORCE_REMOVE_FROM_CAMPAIGN, SALESFORCE_ADD_LEAD_TO_CAMPAIGN

| tool | mode | empty |
|---|---|---|
| `SALESFORCE_GET_ORG_LIMITS` | mocked |  |
| `SALESFORCE_RUN_SOQL_QUERY` | mock-rejected |  |
| `SALESFORCE_LIST_LEADS` | mocked |  |
| `SALESFORCE_SEARCH_CAMPAIGNS` | mocked |  |
| `SALESFORCE_SEARCH_LEADS` | mocked |  |
| `SALESFORCE_SEARCH_CONTACTS` | mocked |  |
| `SALESFORCE_RUN_SOQL_QUERY` | mock-rejected |  |
| `SALESFORCE_RUN_SOQL_QUERY` | mocked |  |
| `SALESFORCE_RUN_SOQL_QUERY` | mocked |  |
| `SALESFORCE_RUN_SOQL_QUERY` | mocked |  |
| `SALESFORCE_RUN_SOQL_QUERY` | mocked |  |

missed: `SALESFORCE_CREATE_A_RECORD`, `SALESFORCE_CREATE_S_OBJECT_RECORD`, `SALESFORCE_DELETE_SOBJECT_COLLECTIONS`, `SALESFORCE_SOBJECT_ROWS_UPDATE`

**Run 4 — real reads** — 3 queries, union 4/11, primary 2/11, stop: _agent finished_

execution: `{'real': 7}`

1. `Salesforce leads contacts campaign membership campaign attendance status static list MQL lead activity reporting`
   - intent: Manage Salesforce leads contacts campaigns and campaign members
   - primary: SALESFORCE_RUN_SOQL_QUERY, SALESFORCE_LIST_LEADS
2. `Salesforce search campaigns campaign members attendance status`
   - intent: Search Salesforce campaigns and campaign members
   - primary: SALESFORCE_SEARCH_CAMPAIGNS, SALESFORCE_LIST_CAMPAIGNS
3. `Salesforce MQL lead activity reporting leads contacts reports`
   - intent: Report on MQL lead activity in Salesforce
   - primary: SALESFORCE_GET_S_OBJECTS_UPDATED, SALESFORCE_GET_COMPOSITE_SOBJECTS, SALESFORCE_RUN_SOQL_QUERY

| tool | mode | empty |
|---|---|---|
| `SALESFORCE_LIST_LEADS` | real | yes |
| `SALESFORCE_LIST_CAMPAIGNS` | real | yes |
| `SALESFORCE_RUN_SOQL_QUERY` | real |  |
| `SALESFORCE_RUN_SOQL_QUERY` | real | yes |
| `SALESFORCE_RUN_SOQL_QUERY` | real | yes |
| `SALESFORCE_RUN_SOQL_QUERY` | real | yes |
| `SALESFORCE_RUN_SOQL_QUERY` | real | yes |

missed: `SALESFORCE_CREATE_A_RECORD`, `SALESFORCE_CREATE_S_OBJECT_RECORD`, `SALESFORCE_DELETE_SOBJECT_COLLECTIONS`, `SALESFORCE_POST_COMPOSITE_SOBJECTS`, `SALESFORCE_SEARCH_CONTACTS`, `SALESFORCE_SEARCH_LEADS`, `SALESFORCE_SOBJECT_ROWS_UPDATE`

## Task 7

> Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.

**Run 3 — fully mocked** — 15 queries, union 8/23, primary 5/23, stop: _step ceiling reached_

execution: `{'mocked': 3}`

1. `aggregate productivity signals across email calendar github linkedin sms`
   - intent: Aggregate personal productivity signals across email, calendar, github, linkedin, and sms
   - primary: HUBSPOT_GET_AGGREGATED_STATISTICS, HUBSPOT_GET_AGGREGATED_STATISTIC_INTERVALS
2. `read email calendar github linkedin sms signals`
   - intent: Search for tools to read email, calendar, github, linkedin, and sms productivity signals
   - primary: HUBSPOT_READ_EMAIL
3. `list emails read emails messages`
   - intent: Search for email tools across all available integrations or apps
   - primary: HUBSPOT_LIST_EMAILS, ZOHO_MAIL_MESSAGES_LIST_EMAILS
4. `manage calendar access and events`
   - intent: Search for calendar management and events tools
   - primary: GOOGLECALENDAR_FIND_FREE_SLOTS, GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_CREATE_EVENT
5. `github repositories issues pull requests productivity signals`
   - intent: Search for GitHub tools for repository and issue activity signals
   - primary: GITHUB_GET_A_REPOSITORY, GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS
6. `linkedin profile posts messages productivity signals`
   - intent: Search for LinkedIn tools for profile and activity signals
   - primary: LINKEDIN_GET_MY_INFO, LINKEDIN_CREATE_LINKED_IN_POST
7. `configure sms receiving and sending text messages`
   - intent: Search for SMS tools to configure SMS receiving and sending
   - primary: CLICKSEND_CREATE_SMS_SEND
8. `configure sms receiving webhook inbound messages clicksend`
   - intent: Search for SMS receiving webhook or inbox configuration tools
   - primary: CLICKSEND_GET_SMS_INBOUND, CLICKSEND_GET_SMS_HISTORY
9. `list messages emails in inbox`
   - intent: Search for email listing tools in Zoho Mail or HubSpot
   - primary: AGENT_MAIL_LIST_MESSAGES, MAILTRAP_LIST_MESSAGES
10. `agent_mail_list_messages`
   - intent: Search for agent mail list messages tool execution
   - primary: AGENT_MAIL_LIST_MESSAGES
11. `googlecalendar_list_calendars`
   - intent: Search for calendar list calendars tool execution
   - primary: GOOGLECALENDAR_LIST_CALENDARS
12. `github_list_repositories_for_the_authenticated_user`
   - intent: Search for GitHub list repositories tool execution
   - primary: GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER
13. `linkedin_get_my_info`
   - intent: Search for LinkedIn get my info tool execution
   - primary: LINKEDIN_GET_MY_INFO
14. `clicksend_get_account`
   - intent: Search for ClickSend get account tool execution
   - primary: CLICKSEND_GET_ACCOUNT, CLICKSEND_GET_RESELLER
15. `agent_mail_list_inboxes`
   - intent: Search for agent mail list inboxes tool execution
   - primary: AGENT_MAIL_LIST_INBOXES

| tool | mode | empty |
|---|---|---|
| `AGENT_MAIL_LIST_INBOXES` | mocked |  |
| `GOOGLECALENDAR_LIST_CALENDARS` | mocked |  |
| `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` | mocked |  |

missed: `CAL_CONNECT_TO_CALENDAR`, `CAL_RETRIEVE_CALENDAR_LIST`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_POST_NUMBERS_BUY`, `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`, `GOOGLECALENDAR_ACL_INSERT`, `GOOGLECALENDAR_ACL_UPDATE`, `GOOGLECALENDAR_BATCH_EVENTS`, `GOOGLECALENDAR_EVENTS_GET`, `GOOGLECALENDAR_EVENTS_LIST`, `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`, `LINKEDIN_PROXY_EXECUTE`

**Run 4 — real reads** — 5 queries, union 10/23, primary 3/23, stop: _quota exhausted_

execution: `{'real': 3, 'mocked': 1, 'mock-rejected': 2}`

1. `search email messages in gmail`
   - intent: Search email messages across the inbox
   - primary: GMAIL_FETCH_EMAILS
2. `search calendar events in google calendar`
   - intent: Search calendar events
   - primary: GOOGLECALENDAR_FIND_EVENT, GOOGLECALENDAR_EVENTS_LIST
3. `search github notifications or issues`
   - intent: Search github notifications and issues
   - primary: GITHUB_LIST_NOTIFICATIONS
4. `send and receive sms messages`
   - intent: Send and receive SMS messages
   - primary: CLICKSEND_CREATE_SMS_SEND
5. `search linkedin profile and messages`
   - intent: Search linkedin profile and messages
   - primary: LINKEDIN_GET_MY_INFO

| tool | mode | empty |
|---|---|---|
| `GMAIL_FETCH_EMAILS` | real |  |
| `GOOGLECALENDAR_EVENTS_LIST` | real | yes |
| `GITHUB_LIST_NOTIFICATIONS` | mocked |  |
| `LINKEDIN_GET_MY_INFO` | real |  |
| `CLICKSEND_CREATE_SMS_SEND` | mock-rejected |  |
| `CLICKSEND_CREATE_SMS_SEND` | mock-rejected |  |

missed: `CAL_CONNECT_TO_CALENDAR`, `CAL_RETRIEVE_CALENDAR_LIST`, `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_ACCOUNT`, `CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_GET_SMS_INBOUND`, `CLICKSEND_POST_NUMBERS_BUY`, `GOOGLECALENDAR_ACL_INSERT`, `GOOGLECALENDAR_ACL_UPDATE`, `GOOGLECALENDAR_BATCH_EVENTS`, `LINKEDIN_PROXY_EXECUTE`

## Task 8

> Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.

**Run 3 — fully mocked** — 7 queries, union 1/1, primary 1/1, stop: _agent finished_

execution: `{'mocked': 8}`

1. `video transcript knowledge base archive google docs`
   - intent: Search for tools related to video transcripts, knowledge base, archive documents, and Google Docs.
   - primary: ELEVENLABS_MOVE_BULK_CONVAI_KNOWLEDGE_BASE, ELEVENREADER_MOVE_KNOWLEDGE_BASE_ENTITIES
2. `get public video transcripts transcript retrieval`
   - intent: Search for tools to retrieve public video transcripts or search videos/transcripts.
   - primary: SUPADATA_GET_TRANSCRIPT, SUPADATA_GET_YOUTUBE_VIDEO
3. `append to google docs google docs tools`
   - intent: Search for tools related to Google Docs or appending to Google Docs.
   - primary: GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_GET_DOCUMENT_BY_ID, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN
4. `archive documents knowledge base archive mark incomplete`
   - intent: Search for tools related to archive documents or knowledge base files/folders.
   - primary: GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN, GOOGLEDOCS_GET_DOCUMENT_BY_ID
5. `google drive list files search files`
   - intent: Search for files or documents in Google Drive to find the archive documents or existing Google Docs mentioned in the task.
   - primary: GOOGLEDRIVE_FIND_FILE, GOOGLEDRIVE_GET_FILE_METADATA
6. `drive find file search query`
   - intent: Search Google Drive files with a query to find archive or knowledge base documents.
   - primary: GOOGLEDRIVE_FIND_FILE
7. `list all files in google drive`
   - intent: Search for listing all files in Google Drive.
   - primary: GOOGLEDRIVE_FIND_FILE

| tool | mode | empty |
|---|---|---|
| `GOOGLEDRIVE_FIND_FILE` | mocked |  |
| `GOOGLEDRIVE_FIND_FILE` | mocked |  |
| `GOOGLEDRIVE_FIND_FILE` | mocked |  |
| `GOOGLEDRIVE_FIND_FILE` | mocked |  |
| `GOOGLEDOCS_SEARCH_DOCUMENTS` | mocked |  |
| `GOOGLEDOCS_SEARCH_DOCUMENTS` | mocked |  |
| `GOOGLEDRIVE_FIND_FILE` | mocked |  |
| `GOOGLEDOCS_SEARCH_DOCUMENTS` | mocked |  |

**Run 4 — real reads** — 3 queries, union 0/1, primary 0/1, stop: _quota exhausted_

execution: `{'mocked': 1}`

1. `Get public video transcripts or search videos`
   - intent: Search public video transcript data
   - primary: SUPADATA_GET_TRANSCRIPT, SUPADATA_GET_YOUTUBE_VIDEO, NOTION_CREATE_NOTION_PAGE
2. `Search and append or edit Google Docs documents`
   - intent: Search google docs to find existing documents to append summarized entries
   - primary: GOOGLEDOCS_SEARCH_DOCUMENTS, GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT, GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN
3. `Search spreadsheet rows or database items or files to mark incomplete archive documents`
   - intent: Search archive documents or spreadsheets to mark incomplete records when transcript retrieval failed
   - primary: NOTION_QUERY_DATABASE_WITH_FILTER, NOTION_FETCH_DATABASE

| tool | mode | empty |
|---|---|---|
| `GOOGLEDOCS_SEARCH_DOCUMENTS` | mocked |  |

missed: `GOOGLEDOCS_INSERT_TEXT_ACTION`

## Task 9

> Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.

**Run 3 — fully mocked** — 3 queries, union 3/4, primary 3/4, stop: _agent finished_

execution: `{'mocked': 6}`

1. `create multimedia travel marketing assets from scripts and stock media`
   - intent: Search for tools related to creating multimedia travel marketing assets, scripts, stock media, and generative media.
   - primary: GEMINI_GENERATE_VIDEOS, GEMINI_WAIT_FOR_VIDEO, GEMINI_GENERATE_IMAGE
2. `deliver generated files by email and provide downloadable presentation content`
   - intent: Search for tools to deliver generated files by email and provide downloadable presentation content.
   - primary: GMAIL_SEND_EMAIL
3. `generate presentation gamma`
   - intent: Search for Gamma presentation generation tools
   - primary: GAMMA_GENERATE_GAMMA, GAMMA_GET_GAMMA_FILE_URLS

| tool | mode | empty |
|---|---|---|
| `GEMINI_GENERATE_VIDEOS` | mocked |  |
| `GEMINI_GENERATE_IMAGE` | mocked |  |
| `GEMINI_WAIT_FOR_VIDEO` | mocked |  |
| `GAMMA_GENERATE_GAMMA` | mocked |  |
| `GAMMA_GET_GAMMA_FILE_URLS` | mocked |  |
| `GMAIL_SEND_EMAIL` | mocked |  |

missed: `COMPOSIO_SEARCH_IMAGE`

**Run 4 — real reads** — 0 queries, union 0/4, primary 0/4, stop: _quota exhausted_

execution: `{}`

_no queries issued_


missed: `COMPOSIO_SEARCH_IMAGE`, `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`, `GMAIL_SEND_EMAIL`

## Task 10

> Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, recording a customer payment, and verifying financial reports.

**Run 3 — fully mocked** — 5 queries, union 5/6, primary 2/6, stop: _quota exhausted_

execution: `{'mocked': 2}`

1. `QuickBooks bank account ledger query transactions reconciliation`
   - intent: Search for QuickBooks tools to query bank transactions and reconcile ledger accounts.
   - primary: QUICKBOOKS_QUERY_ACCOUNT, QUICKBOOKS_GET_TRANSACTION_LIST_REPORT
2. `QuickBooks create update delete void transaction ledger journal entry customer payment`
   - intent: Search for QuickBooks tools to create, update, delete, or void transactions and ledger entries.
   - primary: QUICKBOOKS_CREATE_JOURNAL_ENTRY
3. `QuickBooks void delete transaction payment`
   - intent: Search for QuickBooks tools to void or delete incorrect transactions or payments.
   - primary: QUICKBOOKS_READ_INVOICE
4. `QuickBooks record customer payment`
   - intent: Search for QuickBooks tools to record a customer payment.
   - primary: QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_CREATE_PAYMENT
5. `QuickBooks get trial balance general ledger report`
   - intent: Search for QuickBooks tools to verify financial reports like trial balance and general ledger.
   - primary: QUICKBOOKS_QUERY_ENTITIES, QUICKBOOKS_GET_REPORT_TRIAL_BALANCE

| tool | mode | empty |
|---|---|---|
| `QUICKBOOKS_GET_COMPANY_INFO` | mocked |  |
| `QUICKBOOKS_QUERY_ACCOUNT` | mocked |  |

missed: `QUICKBOOKS_PROXY_EXECUTE`

**Run 4 — real reads** — 0 queries, union 0/6, primary 0/6, stop: _quota exhausted_

execution: `{}`

_no queries issued_


missed: `QUICKBOOKS_CREATE_JOURNAL_ENTRY`, `QUICKBOOKS_EXECUTE_BATCH_OPERATION`, `QUICKBOOKS_GET_COMPANY_INFO`, `QUICKBOOKS_GET_REPORTS`, `QUICKBOOKS_PROXY_EXECUTE`, `QUICKBOOKS_QUERY_ENTITIES`
