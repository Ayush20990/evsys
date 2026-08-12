# Synthetic Multi-Tool Composio Search Evaluation

## Scope
Synthetic workflows are generated only from curated coherent toolkit families. Gemini selects the required subset of supplied candidate tools; all candidates, decisions, and raw responses are retained in the audit artifacts.

## Summary
- **Accepted workflows:** 20
- **Generation attempts:** 41
- **Rejected candidate groups:** 21
- **Successful search calls:** 20/20
- **Average all-result recall:** 35.0%
- **Average primary-only recall:** 32.5%
- **Average all-result precision:** 12.1%

## Latency
API/Search latency is only the successful request. End-to-end latency includes failed attempts and retry backoff.
| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 2.77 | 2.77 |
| Median (P50) | 2.70 | 2.70 |
| P95 | 3.46 | 3.46 |
| Maximum | 3.63 | 3.63 |

## Failure Examples
Sorted by lowest recall, then most missing tools. These should be manually reviewed before being classified as product failures.

### synthetic-017 — Recall 0.0%, Precision 0.0%
- **Task:** Please review the details in the customer confirmation email I just received and create a new account entry in our CRM system with that company information. Afterwards, make sure to clean up and permanently remove the draft we no longer need from my email client.
- **Expected:** `GMAIL_DELETE_DRAFT; GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID; SALESFORCE_CREATE_ACCOUNT`
- **Missed:** `GMAIL_DELETE_DRAFT; GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID; SALESFORCE_CREATE_ACCOUNT`
- **Primary returned:** `CONSTANT_CONTACT_DELETE_EMAIL_CAMPAIGN; STRIPE_DELETE_INVOICE; CENTRALSTATIONCRM_CREATE_COMPANIES; ALTOVIZ_DELETE_SALE_INVOICE; PIPELINE_CRM_CREATE_COMPANY; SQUARE_DELETE_INVOICE`
- **Related returned:** `CONSTANT_CONTACT_LIST_EMAIL_CAMPAIGNS; CONSTANT_CONTACT_GET_EMAIL_CAMPAIGN; STRIPE_GET_INVOICES_INVOICE; STRIPE_VOID_INVOICE; CENTRALSTATIONCRM_SEARCH_COMPANIES`
- **Extra:** `ALTOVIZ_DELETE_SALE_INVOICE; CENTRALSTATIONCRM_CREATE_COMPANIES; CENTRALSTATIONCRM_SEARCH_COMPANIES; CONSTANT_CONTACT_DELETE_EMAIL_CAMPAIGN; CONSTANT_CONTACT_GET_EMAIL_CAMPAIGN; CONSTANT_CONTACT_LIST_EMAIL_CAMPAIGNS; PIPELINE_CRM_CREATE_COMPANY; SQUARE_DELETE_INVOICE; STRIPE_DELETE_INVOICE; STRIPE_GET_INVOICES_INVOICE; STRIPE_VOID_INVOICE`

### synthetic-001 — Recall 0.0%, Precision 0.0%
- **Task:** Please create a new Google Doc summarizing our latest quarterly metrics using the raw text report I've provided. Once the document is generated, immediately share it with our department lead's email address so they can review the permissions and access the draft.
- **Expected:** `GOOGLEDRIVE_CREATE_FILE_FROM_TEXT; GOOGLEDRIVE_CREATE_PERMISSION`
- **Missed:** `GOOGLEDRIVE_CREATE_FILE_FROM_TEXT; GOOGLEDRIVE_CREATE_PERMISSION`
- **Primary returned:** `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`
- **Related returned:** `GOOGLEDOCS_CREATE_DOCUMENT; GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN; GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN; GOOGLEDOCS_INSERT_TABLE_ACTION; GEMINI_GENERATE_IMAGE; GOOGLEDOCS_INSERT_INLINE_IMAGE`
- **Extra:** `GEMINI_GENERATE_IMAGE; GOOGLEDOCS_CREATE_DOCUMENT; GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN; GOOGLEDOCS_INSERT_INLINE_IMAGE; GOOGLEDOCS_INSERT_TABLE_ACTION; GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN; GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`

### synthetic-002 — Recall 0.0%, Precision 0.0%
- **Task:** We need to set up our new self-hosted CI runner by assigning specific custom operational labels to it in GitHub. Once that is done, please post a confirmation update directly into our #devops-deployments Slack channel so the team knows the runner is fully configured and ready for production builds.
- **Expected:** `GITHUB_ADD_RUNNER_LABELS; SLACK_CHAT_POST_MESSAGE`
- **Missed:** `GITHUB_ADD_RUNNER_LABELS; SLACK_CHAT_POST_MESSAGE`
- **Primary returned:** `GITHUB_SET_STATUS_CHECK_CONTEXTS; MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE; GITHUB_CREATE_A_DEPLOYMENT`
- **Related returned:** `MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS; MICROSOFT_TEAMS_TEAMS_LIST; GITHUB_GET_STATUS_CHECKS_PROTECTION; GITHUB_UPDATE_STATUS_CHECK_PROTECTION; GITHUB_GET_A_REFERENCE`
- **Extra:** `GITHUB_CREATE_A_DEPLOYMENT; GITHUB_GET_A_REFERENCE; GITHUB_GET_STATUS_CHECKS_PROTECTION; GITHUB_SET_STATUS_CHECK_CONTEXTS; GITHUB_UPDATE_STATUS_CHECK_PROTECTION; MICROSOFT_TEAMS_TEAMS_LIST; MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS; MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE`

### synthetic-004 — Recall 0.0%, Precision 0.0%
- **Task:** Hey team, we are archiving an old project channel on Slack today. Could you please search Slack for all recent files and messages related to the 'Project-X-Migration' channel to make sure we didn't miss any critical documentation, and then permanently clean out and delete those old project notification emails from my Gmail inbox to free up space?
- **Expected:** `GMAIL_BATCH_DELETE_MESSAGES; SLACK_ASSISTANT_SEARCH_CONTEXT`
- **Missed:** `GMAIL_BATCH_DELETE_MESSAGES; SLACK_ASSISTANT_SEARCH_CONTEXT`
- **Primary returned:** `SLACK_SEARCH_MESSAGES; GMAIL_DELETE_FILTER`
- **Related returned:** `GMAIL_LIST_FILTERS; GMAIL_GET_FILTER; SLACK_RETRIEVE_MESSAGE_PERMALINK_URL; SLACK_SEARCH_ALL`
- **Extra:** `GMAIL_DELETE_FILTER; GMAIL_GET_FILTER; GMAIL_LIST_FILTERS; SLACK_RETRIEVE_MESSAGE_PERMALINK_URL; SLACK_SEARCH_ALL; SLACK_SEARCH_MESSAGES`

### synthetic-006 — Recall 0.0%, Precision 0.0%
- **Task:** Our engineering team is setting up a new shared workspace on Slack and needs to ensure proper access controls. Please verify our integration by testing connectivity to our communication platform, and then search our Enterprise workspace to locate the specific engineering channel where we will deploy our coordination tools.
- **Expected:** `SLACK_ADMIN_CONVERSATIONS_SEARCH; SLACK_API_TEST`
- **Missed:** `SLACK_ADMIN_CONVERSATIONS_SEARCH; SLACK_API_TEST`
- **Primary returned:** `SLACK_LIST_ALL_CHANNELS; SLACK_LIST_ALL_USERS; SLACK_TEST_AUTH`
- **Related returned:** `SLACK_ASSISTANT_SEARCH_INFO; SLACK_LIST_CONVERSATIONS; SLACK_FIND_CHANNELS; SLACK_FIND_USERS; SLACK_SEARCH_ALL; SLACK_FETCH_CONVERSATION_HISTORY`
- **Extra:** `SLACK_ASSISTANT_SEARCH_INFO; SLACK_FETCH_CONVERSATION_HISTORY; SLACK_FIND_CHANNELS; SLACK_FIND_USERS; SLACK_LIST_ALL_CHANNELS; SLACK_LIST_ALL_USERS; SLACK_LIST_CONVERSATIONS; SLACK_SEARCH_ALL; SLACK_TEST_AUTH`

### synthetic-012 — Recall 0.0%, Precision 0.0%
- **Task:** Hey team, we need to post our weekly progress report for the Q3 Mobile Redesign project in Linear. Once the update is posted, please take the attachment link confirming our updated design specs and attach it directly to our tracking issue LIN-402 so the reviewers can easily find it.
- **Expected:** `LINEAR_CREATE_ATTACHMENT; LINEAR_CREATE_PROJECT_UPDATE`
- **Missed:** `LINEAR_CREATE_ATTACHMENT; LINEAR_CREATE_PROJECT_UPDATE`
- **Primary returned:** `LINEAR_UPDATE_ISSUE`
- **Related returned:** `LINEAR_SEARCH_ISSUES; LINEAR_LIST_ISSUES_BY_TEAM_ID; LINEAR_CREATE_LINEAR_COMMENT; LINEAR_RUN_QUERY_OR_MUTATION; LINEAR_LIST_LINEAR_STATES; LINEAR_GET_LINEAR_ISSUE`
- **Extra:** `LINEAR_CREATE_LINEAR_COMMENT; LINEAR_GET_LINEAR_ISSUE; LINEAR_LIST_ISSUES_BY_TEAM_ID; LINEAR_LIST_LINEAR_STATES; LINEAR_RUN_QUERY_OR_MUTATION; LINEAR_SEARCH_ISSUES; LINEAR_UPDATE_ISSUE`

### synthetic-013 — Recall 0.0%, Precision 0.0%
- **Task:** We need to set up a dedicated workspace communication channel for the upcoming product launch and document our initial launch strategy right away. Please create a new public Slack channel named 'product-launch-2024' for the team, and also generate a new Google Doc titled 'Launch Strategy' with our opening notes to keep everyone aligned.
- **Expected:** `GOOGLEDOCS_CREATE_DOCUMENT; SLACK_CREATE_CHANNEL_BASED_CONVERSATION`
- **Missed:** `GOOGLEDOCS_CREATE_DOCUMENT; SLACK_CREATE_CHANNEL_BASED_CONVERSATION`
- **Primary returned:** `SLACK_CREATE_CHANNEL`
- **Related returned:** `SLACK_TEST_AUTH; SLACK_FIND_CHANNELS; SLACK_LIST_ALL_CHANNELS; SLACK_SET_THE_TOPIC_OF_A_CONVERSATION; SLACK_INVITE_USERS_TO_A_SLACK_CHANNEL; SLACK_SEND_MESSAGE`
- **Extra:** `SLACK_CREATE_CHANNEL; SLACK_FIND_CHANNELS; SLACK_INVITE_USERS_TO_A_SLACK_CHANNEL; SLACK_LIST_ALL_CHANNELS; SLACK_SEND_MESSAGE; SLACK_SET_THE_TOPIC_OF_A_CONVERSATION; SLACK_TEST_AUTH`

### synthetic-015 — Recall 0.0%, Precision 0.0%
- **Task:** Hey team, we just finalized the project notes and uploaded the final design assets into our workspace documentation. Can you append the latest meeting summary text blocks to our main Notion project page, and then link the related ClickUp bug tracking task to the primary milestone task so we keep our tracking clean?
- **Expected:** `CLICKUP_ADD_TASK_LINK; NOTION_APPEND_TEXT_BLOCKS`
- **Missed:** `CLICKUP_ADD_TASK_LINK; NOTION_APPEND_TEXT_BLOCKS`
- **Primary returned:** `NOTION_APPEND_MEDIA_BLOCKS; NOTION_APPEND_TASK_BLOCKS; CLICKUP_UPDATE_TASK`
- **Related returned:** `NOTION_CREATE_FILE_UPLOAD; NOTION_SEND_FILE_UPLOAD; NOTION_FETCH_BLOCK_CONTENTS; NOTION_SEARCH_NOTION_PAGE; NOTION_UPDATE_BLOCK; CLICKUP_GET_TASK`
- **Extra:** `CLICKUP_GET_TASK; CLICKUP_UPDATE_TASK; NOTION_APPEND_MEDIA_BLOCKS; NOTION_APPEND_TASK_BLOCKS; NOTION_CREATE_FILE_UPLOAD; NOTION_FETCH_BLOCK_CONTENTS; NOTION_SEARCH_NOTION_PAGE; NOTION_SEND_FILE_UPLOAD; NOTION_UPDATE_BLOCK`

### synthetic-010 — Recall 33.3%, Precision 16.7%
- **Task:** We are restructuring our project documentation and tracking. Please create a new Trello board named 'Q3 Product Roadmap' for our upcoming campaign tasks. At the same time, set up a corresponding ClickUp Doc in our workspace to serve as the master project brief, and append the initial outline paragraphs to our existing Notion planning page so the team has immediate access to all resources.
- **Expected:** `CLICKUP_CREATE_DOC; NOTION_APPEND_TEXT_BLOCKS; TRELLO_ADD_BOARDS`
- **Missed:** `CLICKUP_CREATE_DOC; TRELLO_ADD_BOARDS`
- **Primary returned:** `CLICKUP_CREATE_DOC_PAGE; NOTION_APPEND_TEXT_BLOCKS`
- **Related returned:** `CLICKUP_CLICK_UP_UPDATE_DOC_PAGE; CLICKUP_GET_DOC_PAGE_LISTING; NOTION_SEARCH_NOTION_PAGE; NOTION_ADD_MULTIPLE_PAGE_CONTENT`
- **Extra:** `CLICKUP_CLICK_UP_UPDATE_DOC_PAGE; CLICKUP_CREATE_DOC_PAGE; CLICKUP_GET_DOC_PAGE_LISTING; NOTION_ADD_MULTIPLE_PAGE_CONTENT; NOTION_SEARCH_NOTION_PAGE`

### synthetic-018 — Recall 33.3%, Precision 25.0%
- **Task:** I need to clean up my workspace by removing outdated records. Please delete the unsent draft regarding the old marketing campaign from my email account, and then archive the batch of defunct company profiles and associated CRM objects that we no longer use in our database.
- **Expected:** `GMAIL_DELETE_DRAFT; HUBSPOT_ARCHIVE_BATCH_OF_OBJECTS; HUBSPOT_ARCHIVE_COMPANIES`
- **Missed:** `GMAIL_DELETE_DRAFT; HUBSPOT_ARCHIVE_COMPANIES`
- **Primary returned:** `HUBSPOT_ARCHIVE_BATCH_OF_OBJECTS`
- **Related returned:** `HUBSPOT_READ_APAGE_OF_OBJECTS_BY_TYPE; HUBSPOT_SEARCH_CRM_OBJECTS_BY_CRITERIA; HUBSPOT_READ_BATCH_OF_CRM_OBJECTS_BY_ID_OR_PROPERTY_VALUES`
- **Extra:** `HUBSPOT_READ_APAGE_OF_OBJECTS_BY_TYPE; HUBSPOT_READ_BATCH_OF_CRM_OBJECTS_BY_ID_OR_PROPERTY_VALUES; HUBSPOT_SEARCH_CRM_OBJECTS_BY_CRITERIA`

### synthetic-019 — Recall 33.3%, Precision 14.3%
- **Task:** Please review the latest vendor email regarding our contract renewal, download the attached agreement document for my records, and then clean up our HubSpot CRM by archiving the outdated company profile associated with their old subsidiary ID.
- **Expected:** `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID; GMAIL_GET_ATTACHMENT; HUBSPOT_ARCHIVE_COMPANIES`
- **Missed:** `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID; GMAIL_GET_ATTACHMENT`
- **Primary returned:** `HUBSPOT_ARCHIVE_COMPANY; HUBSPOT_ARCHIVE_COMPANIES`
- **Related returned:** `HUBSPOT_GET_COMPANY; HUBSPOT_SEARCH_COMPANIES; HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID; HUBSPOT_PERMANENTLY_DELETE_CONTACT_VIA_GDPR; HUBSPOT_LIST_COMPANIES`
- **Extra:** `HUBSPOT_ARCHIVE_COMPANY; HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID; HUBSPOT_GET_COMPANY; HUBSPOT_LIST_COMPANIES; HUBSPOT_PERMANENTLY_DELETE_CONTACT_VIA_GDPR; HUBSPOT_SEARCH_COMPANIES`

### synthetic-020 — Recall 33.3%, Precision 14.3%
- **Task:** Please retrieve the latest email messages from our client's thread ID to review their contact details, fetch our saved Google contacts to cross-reference their organizational data, and then forward the relevant message to our account manager for immediate follow-up.
- **Expected:** `GMAIL_FETCH_MESSAGE_BY_THREAD_ID; GMAIL_FORWARD_MESSAGE; GMAIL_GET_CONTACTS`
- **Missed:** `GMAIL_FORWARD_MESSAGE; GMAIL_GET_CONTACTS`
- **Primary returned:** `GMAIL_FETCH_MESSAGE_BY_THREAD_ID; GOOGLESUPER_FETCH_MESSAGE_BY_THREAD_ID`
- **Related returned:** `GMAIL_LIST_THREADS; GMAIL_REPLY_TO_THREAD; GMAIL_MODIFY_THREAD_LABELS; GOOGLESUPER_LIST_THREADS; GOOGLESUPER_REPLY_TO_THREAD`
- **Extra:** `GMAIL_LIST_THREADS; GMAIL_MODIFY_THREAD_LABELS; GMAIL_REPLY_TO_THREAD; GOOGLESUPER_FETCH_MESSAGE_BY_THREAD_ID; GOOGLESUPER_LIST_THREADS; GOOGLESUPER_REPLY_TO_THREAD`

### synthetic-007 — Recall 50.0%, Precision 12.5%
- **Task:** I need to share my project calendar with a new contractor and also clean out obsolete notification emails from my inbox. First, grant access to 'contractor@example.com' on my main calendar. Then, permanently delete all the outdated alert messages from my inbox in bulk to ensure proper mailbox hygiene.
- **Expected:** `GMAIL_BATCH_DELETE_MESSAGES; GOOGLECALENDAR_ACL_INSERT`
- **Missed:** `GMAIL_BATCH_DELETE_MESSAGES`
- **Primary returned:** `OUTLOOK_DELETE_CALENDAR_PERMANENTLY; GOOGLECALENDAR_ACL_INSERT; OUTLOOK_CREATE_ME_CALENDAR_PERMISSION`
- **Related returned:** `OUTLOOK_LIST_ME_CALENDAR_PERMISSIONS; OUTLOOK_DELETE_ME_CALENDAR_PERMISSION; OUTLOOK_LIST_CALENDARS; GMAIL_FETCH_EMAILS; GMAIL_SEARCH_PEOPLE`
- **Extra:** `GMAIL_FETCH_EMAILS; GMAIL_SEARCH_PEOPLE; OUTLOOK_CREATE_ME_CALENDAR_PERMISSION; OUTLOOK_DELETE_CALENDAR_PERMANENTLY; OUTLOOK_DELETE_ME_CALENDAR_PERMISSION; OUTLOOK_LIST_CALENDARS; OUTLOOK_LIST_ME_CALENDAR_PERMISSIONS`

### synthetic-009 — Recall 50.0%, Precision 16.7%
- **Task:** Our engineering team is launching a new project and needs a dedicated workspace. Please set up a new public Slack channel for the team discussions, and simultaneously create a corresponding central project folder in our Google Drive so we can start organizing our initial documentation and deliverables.
- **Expected:** `GOOGLEDRIVE_CREATE_FILE; SLACK_CREATE_CHANNEL`
- **Missed:** `GOOGLEDRIVE_CREATE_FILE`
- **Primary returned:** `SLACK_CREATE_CHANNEL; SLACK_CREATE_CHANNEL_BASED_CONVERSATION`
- **Related returned:** `SLACK_INVITE_USERS_TO_A_SLACK_CHANNEL; SLACK_SET_THE_TOPIC_OF_A_CONVERSATION; SLACK_SEND_MESSAGE; SLACK_LIST_AVAILABLE_WORKSPACES`
- **Extra:** `SLACK_CREATE_CHANNEL_BASED_CONVERSATION; SLACK_INVITE_USERS_TO_A_SLACK_CHANNEL; SLACK_LIST_AVAILABLE_WORKSPACES; SLACK_SEND_MESSAGE; SLACK_SET_THE_TOPIC_OF_A_CONVERSATION`

### synthetic-011 — Recall 50.0%, Precision 25.0%
- **Task:** Please clean up our team's calendar permissions by updating an existing sharing rule on our primary project calendar via patch semantics, and also locate and fetch a specific important email message by its ID to review an attached agreement referenced in the calendar notes.
- **Expected:** `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID; GOOGLECALENDAR_ACL_PATCH`
- **Missed:** `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`
- **Primary returned:** `GOOGLECALENDAR_ACL_PATCH`
- **Related returned:** `GOOGLECALENDAR_LIST_CALENDARS; GMAIL_FETCH_EMAILS; GMAIL_SEARCH_PEOPLE`
- **Extra:** `GMAIL_FETCH_EMAILS; GMAIL_SEARCH_PEOPLE; GOOGLECALENDAR_LIST_CALENDARS`

### synthetic-016 — Recall 50.0%, Precision 20.0%
- **Task:** Hey team, we're kicking off our new infrastructure initiative. Please create a dedicated project in Linear for this effort, and then post an initial project status update detailing our goals and timeline for the upcoming quarter so everyone is aligned.
- **Expected:** `LINEAR_CREATE_LINEAR_PROJECT; LINEAR_CREATE_PROJECT_UPDATE`
- **Missed:** `LINEAR_CREATE_PROJECT_UPDATE`
- **Primary returned:** `LINEAR_CREATE_LINEAR_PROJECT; LINEAR_RUN_QUERY_OR_MUTATION`
- **Related returned:** `LINEAR_LIST_LINEAR_TEAMS; LINEAR_LIST_LINEAR_PROJECTS; LINEAR_GET_CURRENT_USER`
- **Extra:** `LINEAR_GET_CURRENT_USER; LINEAR_LIST_LINEAR_PROJECTS; LINEAR_LIST_LINEAR_TEAMS; LINEAR_RUN_QUERY_OR_MUTATION`

### synthetic-008 — Recall 66.7%, Precision 22.2%
- **Task:** We are finalizing a client-facing project document and need to clean up its formatting before handing it over. Please remove the bullet points from the introductory section, and delete the existing header from the default section. Afterward, attach a custom metadata tag indicating the document status as 'finalized' so the team can easily track it in our storage.
- **Expected:** `GOOGLEDOCS_DELETE_HEADER; GOOGLEDOCS_DELETE_PARAGRAPH_BULLETS; GOOGLEDRIVE_ADD_PROPERTY`
- **Missed:** `GOOGLEDRIVE_ADD_PROPERTY`
- **Primary returned:** `GOOGLEDOCS_DELETE_HEADER; GOOGLEDOCS_DELETE_FOOTER; GOOGLESUPER_DELETE_HEADER; GOOGLEDOCS_DELETE_PARAGRAPH_BULLETS`
- **Related returned:** `GOOGLEDOCS_CREATE_HEADER; GOOGLEDOCS_CREATE_FOOTER; GOOGLESUPER_GET_DOCUMENT_BY_ID; GMAIL_FETCH_EMAILS; GMAIL_SEARCH_PEOPLE`
- **Extra:** `GMAIL_FETCH_EMAILS; GMAIL_SEARCH_PEOPLE; GOOGLEDOCS_CREATE_FOOTER; GOOGLEDOCS_CREATE_HEADER; GOOGLEDOCS_DELETE_FOOTER; GOOGLESUPER_DELETE_HEADER; GOOGLESUPER_GET_DOCUMENT_BY_ID`

## Generation Rejections
| Reason | Count |
|---|---:|
| Gemini invented a tool slug outside the candidates | 3 |
| Gemini marked the candidate group infeasible | 17 |
| duplicate required tool slugs | 1 |
