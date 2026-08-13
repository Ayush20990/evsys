# Agent-issued queries vs one-shot imagined queries

Same tasks, two ways of producing the queries. The left column is what the one-shot decomposer predicted an agent would search for; the right is what an agent actually searched for while working the task with real results in front of it.

## Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify the assets remain iner...*

**Imagined (4 queries)**
- `check payment link capabilities and configuration`
- `create automated email and workflow`
- `verify asset status and test inertness`
- `create custom object registration ledger`

**Agent-issued (7 queries)**
- `hubspot`
- `payment link`
- `email`
- `workflow`
- `custom object`
- `hubspot email`
- `hubspot workflow`

## Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

**Imagined (3 queries)**
- `get upcoming Google Calendar meeting events`
- `create or update structured dataset content in Notion`
- `verify Notion content after writing`

**Agent-issued (5 queries)**
- `Google Calendar`
- `Notion`
- `Notion database query or search`
- `Notion search database`
- `Notion insert row database`

## Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

**Imagined (2 queries)**
- `download file from OneDrive`
- `upload file to OneDrive`

**Agent-issued (12 queries)**
- `onedrive spreadsheet`
- `search onedrive files`
- `upload onedrive file`
- `update file content onedrive`
- `download file onedrive`
- `workbench python file execution`
- `execute python code`
- `composio remote workbench`
- `ONE_DRIVE_SEARCH_ITEMS`
- `ONE_DRIVE_LIST_DRIVES`
- `ONE_DRIVE_LIST_FOLDER_CHILDREN`
- `ONE_DRIVE_ONEDRIVE_FIND_FILE`

## Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

**Imagined (4 queries)**
- `get approved cards from Trello workflow`
- `publish carousel content to LinkedIn with a first comment`
- `update Trello card status and activity logs`
- `modify Trello board workflow lists and structure`

**Agent-issued (12 queries)**
- `trello`
- `linkedin`
- `get trello cards`
- `trello search boards`
- `linkedin create post`
- `linkedin comment`
- `trello create list update card`
- `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER`
- `TRELLO_GET_SEARCH`
- `LINKEDIN_GET_MY_INFO`
- `TRELLO_UPDATE_LISTS_BY_ID_LIST`
- `TRELLO_ADD_LISTS`

## Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, and write evidence-su...*

**Imagined (5 queries)**
- `search and read recent Gmail email threads`
- `search and retrieve ClickUp tasks and Notion CRM records`
- `create Gmail draft emails for partner outreach`
- `create and update ClickUp tasks`
- `write evidence-supported updates in Notion CRM records`

**Agent-issued (9 queries)**
- `gmail`
- `clickup`
- `notion`
- `list database notion`
- `search notion page`
- `clickup get teams`
- `get spaces clickup`
- `search notion page database`
- `gmail list messages`

## Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

**Imagined (0 queries)**
- _(workflow rejected during generation)_

**Agent-issued (12 queries)**
- `Salesforce leads contacts campaign`
- `campaign contact member static list MQL activity reporting Salesforce`
- `Salesforce campaign`
- `Salesforce lead contact campaign member status report`
- `lead status MQL activity campaign member`
- `CampaignMember status`
- `update campaign member status`
- `Salesforce update campaign member`
- `Salesforce list leads contacts campaigns`
- `Salesforce search campaigns`
- `Salesforce list leads`
- `Salesforce list contacts`

## Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

**Imagined (5 queries)**
- `read recent emails`
- `get calendar events`
- `read incoming sms messages`
- `configure sms sending and receiving`
- `manage calendar access and events`

**Agent-issued (12 queries)**
- `email`
- `calendar`
- `github`
- `linkedin`
- `sms`
- `gmail`
- `list events`
- `google calendar events list`
- `github commits`
- `linkedin my info`
- `clicksend sms history`
- `google calendar list calendars`

## Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

**Imagined (1 queries)**
- `append summary to google docs`

**Agent-issued (6 queries)**
- `video transcript knowledge base`
- `google docs append`
- `knowledge base archive document mark incomplete`
- `list files or search files or workspace or database or filesystem or storage`
- `GOOGLEDRIVE_FIND_FILE`
- `search youtube video`

## Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

**Imagined (2 queries)**
- `generate multimedia video from script and media assets`
- `send email with attachments and generate downloadable presentation link`

**Agent-issued (7 queries)**
- `travel marketing assets script media`
- `email deliver presentation content`
- `send email`
- `generate image`
- `get user email address`
- `get profile`
- `search contacts or user profile`

## Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, recording a customer pa...*

**Imagined (3 queries)**
- `search quickbooks bank account ledger transactions`
- `undo remove incorrect quickbooks ledger entry`
- `record customer payment quickbooks financial report`

**Agent-issued (13 queries)**
- `QuickBooks`
- `bank ledger transaction`
- `QuickBooks ledger account transaction bank`
- `QuickBooks transaction create update delete void payment adjustment`
- `QuickBooks payment deposit journal entry`
- `QuickBooks payment deposit`
- `QuickBooks report balance sheet trial balance`
- `QuickBooks query accounts`
- `QuickBooks get transaction list report`
- `QuickBooks query payment invoice journal deposit`
- `QuickBooks create deposit`
- `QuickBooks delete transaction void journal payment deposit`
- `QuickBooks update delete journal entry payment deposit`

## Query-count comparison

| Task | Imagined | Agent-issued |
|---|---:|---:|
| 1 | 4 | 7 |
| 2 | 3 | 5 |
| 3 | 2 | 12 |
| 4 | 4 | 12 |
| 5 | 5 | 9 |
| 6 | 0 | 12 |
| 7 | 5 | 12 |
| 8 | 1 | 6 |
| 9 | 2 | 7 |
| 10 | 3 | 13 |
| **mean** | **2.9** | **9.5** |
