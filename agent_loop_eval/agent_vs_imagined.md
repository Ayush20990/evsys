# Agent-issued queries vs one-shot imagined queries

Same tasks, two ways of producing the queries. The left column is what the one-shot decomposer predicted an agent would search for; the right is what an agent actually searched for while working the task with real results in front of it.

## Task 1
*Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify the assets remain iner...*

**Imagined (4 queries)**
- `check payment link capabilities and configuration`
- `create automated email and workflow`
- `verify asset status and test inertness`
- `create custom object registration ledger`

**Agent-issued (9 queries)**
- `Check payment link feasibility or creation in HubSpot`
- `Create a marketing email in HubSpot`
- `Create or manage workflows in HubSpot`
- `Create a new workflow in HubSpot`
- `Create custom object schema in HubSpot`
- `List payment links in HubSpot`
- `Get account info in HubSpot`
- `Get workflow by ID in HubSpot`
- `Get workflow by id in HubSpot`

## Task 2
*Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.*

**Imagined (3 queries)**
- `get upcoming Google Calendar meeting events`
- `create or update structured dataset content in Notion`
- `verify Notion content after writing`

**Agent-issued (8 queries)**
- `Retrieve upcoming Google Calendar meeting events`
- `Create or update Notion content or database pages with verification`
- `Search Notion pages`
- `List Google Calendar settings`
- `List Google Calendar events with time_min and time_max`
- `Create a new Notion page`
- `Add multiple page content in Notion`
- `Get page markdown in Notion for verification`

## Task 3
*Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.*

**Imagined (2 queries)**
- `download file from OneDrive`
- `upload file to OneDrive`

**Agent-issued (9 queries)**
- `find spreadsheet in OneDrive`
- `download file from OneDrive`
- `upload update file content OneDrive`
- `remote workbench execute python bash`
- `get recent items OneDrive root`
- `start sandbox daytona`
- `list root folder children OneDrive`
- `list items in OneDrive folder`
- `search items in OneDrive query`

## Task 4
*Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.*

**Imagined (4 queries)**
- `get approved cards from Trello workflow`
- `publish carousel content to LinkedIn with a first comment`
- `update Trello card status and activity logs`
- `modify Trello board workflow lists and structure`

**Agent-issued (12 queries)**
- `trello get cards in list or board`
- `linkedin create post and comment`
- `trello update card move list create list`
- `linkedin add comment to post`
- `trello create list on board`
- `trello get boards for member`
- `trello add comment to card`
- `trello search query`
- `trello search cards query`
- `linkedin get my info author urn`
- `linkedin create comment on post schema`
- `get definition for LINKEDIN_CREATE_COMMENT_ON_POST`

## Task 5
*Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, and write evidence-su...*

**Imagined (5 queries)**
- `search and read recent Gmail email threads`
- `search and retrieve ClickUp tasks and Notion CRM records`
- `create Gmail draft emails for partner outreach`
- `create and update ClickUp tasks`
- `write evidence-supported updates in Notion CRM records`

**Agent-issued (11 queries)**
- `partner operations pipeline gmail clickup notion`
- `search and read gmail email threads`
- `clickup create task handoff`
- `create gmail draft`
- `notion query database or search database`
- `search notion pages workspace`
- `list gmail threads messages`
- `clickup get tasks list`
- `search notion databases workspace pages`
- `notion fetch database data`
- `clickup get lists space folder`

## Task 6
*Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.*

**Imagined (0 queries)**
- _(workflow rejected during generation)_

**Agent-issued (7 queries)**
- `salesforce leads contacts campaign membership attendance status static list MQL lead activity reporting`
- `salesforce manage campaigns campaign members campaign member status static list`
- `salesforce create lead contact update campaign member status report`
- `salesforce update campaign member status attendance`
- `salesforce update campaign member status field`
- `salesforce update sobject campaign member`
- `salesforce custom rest api call or campaign member update`

## Task 7
*Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.*

**Imagined (5 queries)**
- `read recent emails`
- `get calendar events`
- `read incoming sms messages`
- `configure sms sending and receiving`
- `manage calendar access and events`

**Agent-issued (15 queries)**
- `aggregate productivity signals across email calendar github linkedin sms`
- `read email calendar github linkedin sms signals`
- `list emails read emails messages`
- `manage calendar access and events`
- `github repositories issues pull requests productivity signals`
- `linkedin profile posts messages productivity signals`
- `configure sms receiving and sending text messages`
- `configure sms receiving webhook inbound messages clicksend`
- `list messages emails in inbox`
- `agent_mail_list_messages`
- `googlecalendar_list_calendars`
- `github_list_repositories_for_the_authenticated_user`
- `linkedin_get_my_info`
- `clicksend_get_account`
- `agent_mail_list_inboxes`

## Task 8
*Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.*

**Imagined (1 queries)**
- `append summary to google docs`

**Agent-issued (7 queries)**
- `video transcript knowledge base archive google docs`
- `get public video transcripts transcript retrieval`
- `append to google docs google docs tools`
- `archive documents knowledge base archive mark incomplete`
- `google drive list files search files`
- `drive find file search query`
- `list all files in google drive`

## Task 9
*Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.*

**Imagined (2 queries)**
- `generate multimedia video from script and media assets`
- `send email with attachments and generate downloadable presentation link`

**Agent-issued (3 queries)**
- `create multimedia travel marketing assets from scripts and stock media`
- `deliver generated files by email and provide downloadable presentation content`
- `generate presentation gamma`

## Task 10
*Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, recording a customer pa...*

**Imagined (3 queries)**
- `search quickbooks bank account ledger transactions`
- `undo remove incorrect quickbooks ledger entry`
- `record customer payment quickbooks financial report`

**Agent-issued (5 queries)**
- `QuickBooks bank account ledger query transactions reconciliation`
- `QuickBooks create update delete void transaction ledger journal entry customer payment`
- `QuickBooks void delete transaction payment`
- `QuickBooks record customer payment`
- `QuickBooks get trial balance general ledger report`

## Query-count comparison

| Task | Imagined | Agent-issued |
|---|---:|---:|
| 1 | 4 | 9 |
| 2 | 3 | 8 |
| 3 | 2 | 9 |
| 4 | 4 | 12 |
| 5 | 5 | 11 |
| 6 | 0 | 7 |
| 7 | 5 | 15 |
| 8 | 1 | 7 |
| 9 | 2 | 3 |
| 10 | 3 | 5 |
| **mean** | **2.9** | **8.6** |
