# 100 Use Cases for Eval Building

1. **Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify the assets remain inert, and attempt to create a custom-object registration ledger.**

   - Tools: `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_CREATE_OBJECT_SCHEMA`, `HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION`, `HUBSPOT_CREATE_WORKFLOW`, `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT`, `HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL`, `HUBSPOT_GET_WORKFLOWS`, `HUBSPOT_GET_WORKFLOW_BY_ID`, `HUBSPOT_LIST_GRANTED_SCOPES`, `HUBSPOT_SEARCH_EMAILS`
   - Description: The workflow used HubSpot to prepare a paid-event registration launch.

2. **Retrieve upcoming Google Calendar meeting events and create or update Notion content containing a large structured dataset, with verification after writing.**

   - Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_CREATE_NOTION_PAGE`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_REPLACE_PAGE_CONTENT`, `NOTION_RETRIEVE_PAGE`
   - Description: The workflow first retrieved upcoming Google Calendar events in several time windows.

3. **Find a spreadsheet in OneDrive, download it, programmatically add comparison summary worksheets/sections, upload the modified workbook back to the same OneDrive item, and verify the cloud copy.**

   - Tools: `ONE_DRIVE_DOWNLOAD_FILE`, `ONE_DRIVE_GET_ITEM`, `ONE_DRIVE_SEARCH_ITEMS`, `ONE_DRIVE_UPDATE_FILE_CONTENT`
   - Description: The workflow searched OneDrive for a spreadsheet, downloaded it through a staged content URL, inspected and modified the workbook in a sandbox, saved a replacement file, uploaded it back to the same OneDrive item using upload sessions, and confirmed the final cloud metadata.

4. **Publish approved carousel content from a Trello workflow to LinkedIn, add a first comment, update Trello status/logs, and adjust the Trello board workflow structure.**

   - Tools: `LINKEDIN_CREATE_COMMENT_ON_POST`, `LINKEDIN_CREATE_LINKED_IN_POST`, `LINKEDIN_DELETE_POST`, `LINKEDIN_GET_MY_INFO`, `LINKEDIN_GET_POST_CONTENT`, `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`, `TRELLO_ADD_LISTS`, `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD`, `TRELLO_GET_LISTS_CARDS_BY_ID_LIST`, `TRELLO_UPDATE_CARDS_ID_LIST_BY_ID_CARD`
   - Description: The workflow began by reading a Trello source list to find a card and its carousel attachments.

5. **Manage a partner-operations pipeline across Gmail, ClickUp, and Notion: create outreach drafts and task handoffs, inspect and update existing handoffs, scan recent email threads against CRM records, and write evidence-supported CRM status updates.**

   - Tools: `CLICKUP_CREATE_TASK`, `CLICKUP_GET_TASK`, `CLICKUP_GET_TASKS`, `CLICKUP_UPDATE_TASK`, `GMAIL_CREATE_EMAIL_DRAFT`, `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`, `GMAIL_GET_DRAFT`, `GMAIL_LIST_THREADS`, `NOTION_FETCH_DATABASE`, `NOTION_FETCH_ROW`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_RETRIEVE_PAGE`, `NOTION_SEARCH_NOTION_PAGE`, `NOTION_UPDATE_PAGE`
   - Description: The workflow orchestrated a partner-operations lifecycle.

6. **Manage Salesforce leads, contacts, campaign membership, campaign attendance statuses, a campaign-based static list, and MQL lead activity reporting.**

   - Tools: `SALESFORCE_ADD_CONTACT_TO_CAMPAIGN`, `SALESFORCE_CREATE_A_RECORD`, `SALESFORCE_CREATE_S_OBJECT_RECORD`, `SALESFORCE_DELETE_SOBJECT_COLLECTIONS`, `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT`, `SALESFORCE_POST_COMPOSITE_SOBJECTS`, `SALESFORCE_RUN_SOQL_QUERY`, `SALESFORCE_SEARCH_CAMPAIGNS`, `SALESFORCE_SEARCH_CONTACTS`, `SALESFORCE_SEARCH_LEADS`, `SALESFORCE_SOBJECT_ROWS_UPDATE`
   - Description: The workflow used Salesforce to manage campaign-related data at scale.

7. **Aggregate and act on personal productivity signals across email, calendar, GitHub, LinkedIn, and SMS; additionally configure SMS receiving/sending and manage calendar access/events.**

   - Tools: `CAL_CONNECT_TO_CALENDAR`, `CAL_RETRIEVE_CALENDAR_LIST`, `CLICKSEND_CREATE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_CREATE_SMS_SEND`, `CLICKSEND_DELETE_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_ACCOUNT`, `CLICKSEND_GET_AUTOMATIONS_SMS_INBOUND`, `CLICKSEND_GET_NUMBERS_SEARCH`, `CLICKSEND_GET_SMS_HISTORY`, `CLICKSEND_GET_SMS_INBOUND`, `CLICKSEND_GET_SMS_RECEIPTS`, `CLICKSEND_POST_NUMBERS_BUY`, `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`, `GOOGLECALENDAR_ACL_INSERT`, `GOOGLECALENDAR_ACL_UPDATE`, `GOOGLECALENDAR_BATCH_EVENTS`, `GOOGLECALENDAR_EVENTS_GET`, `GOOGLECALENDAR_EVENTS_LIST`, `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`, `GOOGLECALENDAR_LIST_CALENDARS`, `LINKEDIN_PROXY_EXECUTE`
   - Description: The workflow attempted to build a personal action feed from Gmail, GitHub, Google Calendar, LinkedIn, and SMS.

8. **Build and update a knowledge base from public video transcript data, mark incomplete archive documents when transcript retrieval failed, and append summarized entries to existing Google Docs.**

   - Tools: `GOOGLEDOCS_INSERT_TEXT_ACTION`
   - Description: The workflow centered on building and maintaining a Google Docs knowledge base from public video transcript data.

9. **Create multimedia travel marketing assets from scripts and stock/generative media, then deliver generated files by email and provide downloadable presentation content.**

   - Tools: `COMPOSIO_SEARCH_IMAGE`, `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`, `GMAIL_SEND_EMAIL`
   - Description: The workflow began with searches for natural TTS and narrated AI video tools, then used Gemini to generate multiple asynchronous video clips in batches and poll them to completion.

10. **Reconcile an organization's QuickBooks bank-account ledger by querying existing transactions, removing or undoing incorrect entries, posting corrected ledger activity, creating adjustment entries, recording a customer payment, and verifying financial reports.**

   - Tools: `QUICKBOOKS_CREATE_JOURNAL_ENTRY`, `QUICKBOOKS_EXECUTE_BATCH_OPERATION`, `QUICKBOOKS_GET_COMPANY_INFO`, `QUICKBOOKS_GET_REPORTS`, `QUICKBOOKS_PROXY_EXECUTE`, `QUICKBOOKS_QUERY_ENTITIES`
   - Description: The workflow reconciled an organization's QuickBooks ledger for a bank account.

11. **Maintain an internal OneDrive-based operations knowledge base, create and verify strategy/support documents, coordinate operational tasks via Discord, check queue and system state files, and configure Gmail support labels and routing.**

   - Tools: `DISCORDBOT_LIST_MESSAGES`, `DISCORDBOT_TEST_AUTH`, `GMAIL_CREATE_FILTER`, `GMAIL_CREATE_LABEL`, `ONE_DRIVE_DOWNLOAD_FILE`, `ONE_DRIVE_DOWNLOAD_FILE_BY_PATH`, `ONE_DRIVE_GET_ITEM`, `ONE_DRIVE_LIST_FOLDER_CHILDREN`, `ONE_DRIVE_ONEDRIVE_CREATE_FOLDER`, `ONE_DRIVE_ONEDRIVE_CREATE_TEXT_FILE`, `ONE_DRIVE_ONEDRIVE_FIND_FILE`, `ONE_DRIVE_ONEDRIVE_FIND_FOLDER`, `ONE_DRIVE_SEARCH_ITEMS`
   - Description: The workflow centered on maintaining an internal OneDrive-based operations system.

12. **Retrieve Trello card comments, update Trello cards, and perform broader project-management and automation-maintenance operations across task boards, email, chat, and an automation platform.**

   - Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`, `SLACK_LIST_ALL_USERS`, `SLACK_SEARCH_MESSAGES`, `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`, `TRELLO_GET_BOARDS_ACTIONS_BY_ID_BOARD`, `TRELLO_GET_CARDS_ACTIONS_BY_ID_CARD`, `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH`, `TRELLO_UPDATE_CARDS_BY_ID_CARD`, `TRELLO_UPDATE_CARDS_CLOSED_BY_ID_CARD`
   - Description: The session began with a Trello comment-retrieval use case.

13. **Audit website search and traffic performance, prepare email marketing/contact lists, and send outreach emails for marketing and press engagement.**

   - Tools: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`, `BREVO_LIST_EMAIL_CAMPAIGNS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`, `GMAIL_SEND_EMAIL`, `GOOGLE_ANALYTICS_LIST_ACCOUNTS`, `GOOGLE_ANALYTICS_LIST_PROPERTIES`, `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_SEARCH_CONSOLE_GET_SITE`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`, `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP`
   - Description: The workflow began by searching for tools across website analytics, search performance, community engagement, and email marketing.

14. **Find software engineering job listings matching role, location, remote-work, and salary criteria, compile the results, and send or provide them to someone.**

   - Tools: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`, `COMPOSIO_SEARCH_EXA_ANSWER`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`, `COMPOSIO_SEARCH_GROQ_CHAT`, `COMPOSIO_SEARCH_NEWS`, `COMPOSIO_SEARCH_WEB`, `GMAIL_PROXY_EXECUTE`, `GMAIL_SEND_EMAIL`
   - Description: The workflow attempted to gather many software engineering job listings matching remote or Bengaluru-style location and salary constraints, verify listings through search, URL fetching, and browser automation, then email the compiled results.

15. **Process pending invoice emails, persist invoice attachments to cloud storage, update spreadsheet ledgers, verify calculated totals, and label processed messages.**

   - Tools: `GMAIL_BATCH_MODIFY_MESSAGES`, `GMAIL_FETCH_EMAILS`, `GMAIL_GET_ATTACHMENT`, `GMAIL_LIST_LABELS`, `GOOGLEDRIVE_UPLOAD_FROM_URL`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`
   - Description: The workflow searched for relevant Gmail, Google Sheets, and Google Drive tools; read multiple spreadsheet ledgers; fetched pending Gmail messages; downloaded invoice attachments; inspected PDFs outside app tools; uploaded selected invoice PDFs into Drive folders; updated spreadsheet rows, notes, links, rates, and…

16. **Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate hosting/deployment state.**

   - Tools: `CLOUDFLARE_LIST_ACCOUNTS`, `CLOUDFLARE_LIST_DNS_RECORDS`, `CLOUDFLARE_LIST_ZONES`, `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_AN_ISSUE`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_GET_A_BRANCH`, `GITHUB_GET_A_PULL_REQUEST`, `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_A_TREE`, `GITHUB_GET_RAW_REPOSITORY_CONTENT`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_GET_THE_COMBINED_STATUS_FOR_A_SPECIFIC_REFERENCE`, `GITHUB_LIST_BRANCHES`, `GITHUB_LIST_COMMITS`, `GITHUB_LIST_PULL_REQUESTS`, `GITHUB_LIST_PULL_REQUESTS_FILES`, `GITHUB_LIST_REPOSITORIES_FOR_A_USER`, `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_MERGE_A_BRANCH`, `GITHUB_SEARCH_CODE`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GOOGLE_ANALYTICS_LIST_DATA_STREAMS`, `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
   - Description: The workflow started with GA4 and Search Console reporting to identify tracking gaps and SEO opportunities for a website.

17. **Create AI avatar promo videos using a HeyGen avatar and voice, prepare supporting media, attempt social publishing, send a support email for infrastructure issues, and read/update a booking schedule.**

   - Tools: `GMAIL_CREATE_EMAIL_DRAFT`, `GMAIL_DELETE_DRAFT`, `GMAIL_SEND_DRAFT`, `GMAIL_SEND_EMAIL`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`, `HEYGEN_RETRIEVE_AVATAR_DETAILS`, `HEYGEN_RETRIEVE_SHARABLE_VIDEO_URL`, `HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`, `HEYGEN_UPLOAD_ASSET`, `HEYGEN_V1_AVATAR_LIST`, `HEYGEN_V2_USER_REMAINING_QUOTA`, `HEYGEN_V2_VIDEO_GENERATE`, `HEYGEN_V2_VOICES`, `INSTAGRAM_GET_IG_MEDIA`, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_LIST_ALL_MESSAGES`, `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`, `INSTAGRAM_SEND_TEXT_MESSAGE`
   - Description: The workflow started with HeyGen avatar-video creation.

18. **Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.**

   - Tools: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_STOP_TASK`, `BROWSER_TOOL_WATCH_TASK`, `GMAIL_SEND_EMAIL`, `LINKEDIN_PROXY_EXECUTE`
   - Description: The workflow repeatedly searched for remote or hybrid contract data-engineering-related roles across job boards, fetched or rendered pages, filtered and compiled job cards, and sent the results by Gmail.

19. **Find relevant Java backend and Spring Boot jobs, build or retrieve tailored resume documents, and email job alerts or applications through Gmail.**

   - Tools: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_GET_SESSION`, `BROWSER_TOOL_STOP_TASK`, `BROWSER_TOOL_WATCH_TASK`, `COMPOSIO_SEARCH_EXA_ANSWER`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`, `COMPOSIO_SEARCH_GROQ_CHAT`, `COMPOSIO_SEARCH_WEB`, `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID`, `GMAIL_SEND_EMAIL`, `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_UPLOAD_FROM_URL`, `LINKEDIN_PROXY_EXECUTE`, `LINKEDIN_SEARCH_AD_TARGETING_ENTITIES`
   - Description: The workflow attempted to search recent Java backend and Spring Boot jobs, extract or verify job details, create tailored resume documents, find recruiter or careers contacts, and send job alert/application emails.

20. **Maintain and reconcile CRM, portal, billing, and project documentation across Google Docs, Google Sheets, Zoho CRM, Google Drive, and QuickBooks while verifying live system fields and updating records.**

   - Tools: `GOOGLEDOCS_GET_DOCUMENT_BY_ID`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDOCS_INSERT_TEXT_ACTION`, `GOOGLEDOCS_REPLACE_ALL_TEXT`, `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_PROXY_EXECUTE`, `GOOGLESHEETS_SEARCH_SPREADSHEETS`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`, `GOOGLESHEETS_VALUES_GET`, `GOOGLESHEETS_VALUES_UPDATE`, `QUICKBOOKS_PROXY_EXECUTE`, `ZOHO_GET_MODULE_FIELDS`, `ZOHO_PROXY_EXECUTE`
   - Description: The workflow centered on updating a set of internal system-design documents, reconciling them with live CRM metadata, logging changes in a tracker, and performing related billing operations.

21. **Read reference documents and a spreadsheet, discover fiscal-period logic from available workspace sources, update spreadsheet formulas, and create a summary worksheet.**

   - Tools: `GMAIL_FETCH_EMAILS`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLESHEETS_ADD_SHEET`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_GET_SPREADSHEET_INFO`
   - Description: The workflow read reference document text, inspected a spreadsheet's structure and formulas, searched Drive and Gmail for fiscal-period context, then updated the spreadsheet with derived period labels and revised retention formulas.

22. **The user was managing unread email triage and urgent alerts, looking up CRM-style trial records, inspecting and modifying source code in GitHub, opening or merging branches, and checking CI workflow failures.**

   - Tools: `AIRTABLE_GET_BASE_SCHEMA`, `AIRTABLE_LIST_BASES`, `AIRTABLE_LIST_RECORDS`, `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_GET_THE_COMBINED_STATUS_FOR_A_SPECIFIC_REFERENCE`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`, `GITHUB_MERGE_A_BRANCH`, `GITHUB_SEARCH_CODE`, `GMAIL_BATCH_MODIFY_MESSAGES`, `GMAIL_FETCH_EMAILS`, `GMAIL_SEND_EMAIL`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`
   - Description: The workflow combined several independent tasks.

23. **Analyze and triage Zendesk support tickets at scale: search ticket queues, enrich tickets with requester/order context, add private AI triage notes and tags, verify queues are drained, and aggregate product-support trends over a large historical ticket set.**

   - Tools: `ZENDESK_GET_USER`, `ZENDESK_GET_ZENDESK_TICKET_BY_ID`, `ZENDESK_SEARCH_ZENDESK`, `ZENDESK_UPDATE_ZENDESK_TICKET`
   - Description: The workflow used Zendesk to manage a high-volume support operation.

24. **Build a recurring job-search digest by finding relevant LinkedIn job listings and sending the result or status update via Gmail.**

   - Tools: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`, `COMPOSIO_SEARCH_NEWS`, `COMPOSIO_SEARCH_TRENDS`, `COMPOSIO_SEARCH_WEB`, `GMAIL_SEND_EMAIL`
   - Description: The workflow tried to generate a job digest from LinkedIn job listings and email it through Gmail.

25. **Find relevant job listings from public web/job sources, tailor them to a software profile, and email the curated list through Gmail.**

   - Tools: `COMPOSIO_SEARCH_FETCH_URL_CONTENT`, `COMPOSIO_SEARCH_WEB`, `GMAIL_CREATE_EMAIL_DRAFT`, `GMAIL_FETCH_EMAILS`, `GMAIL_GET_PROFILE`, `GMAIL_PROXY_EXECUTE`, `GMAIL_SEND_EMAIL`, `LINKEDIN_PROXY_EXECUTE`
   - Description: The workflow searched public sources for job postings using web search, fetched selected posting pages for validation, and used an uploaded resume-like document to tailor a curated job list.

26. **Organize Google Drive image and PDF files by finding candidates, inspecting their contents, renaming files, adding descriptions, moving exact duplicates to a review folder, and verifying metadata changes.**

   - Tools: `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_GET_FILE_METADATA`, `GOOGLEDRIVE_MOVE_FILE`, `GOOGLEDRIVE_UPDATE_FILE_PUT`
   - Description: The workflow organized a large Google Drive collection of images and PDFs.

27. **Verify Google Drive access, inspect folders, copy a nested folder/file structure from one Drive account or folder area to another, and share the destination with collaborators.**

   - Tools: `GOOGLEDRIVE_COPY_FILE_ADVANCED`, `GOOGLEDRIVE_CREATE_FOLDER`, `GOOGLEDRIVE_CREATE_PERMISSION`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_GET_ABOUT`, `GOOGLEDRIVE_GET_FILE_METADATA`
   - Description: The workflow started by checking Google Drive connectivity and folder visibility.

28. **Analyze recent Instagram Reel performance, generate a new short-form branded video with AI video and voice tools, publish it as an Instagram Reel, verify the post, and attempt to archive the final asset in a repository.**

   - Tools: `ELEVENLABS_TEXT_TO_SPEECH`, `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`, `INSTAGRAM_GET_IG_MEDIA`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
   - Description: The workflow first inspected recent Instagram media and fetched Reel performance metrics.

29. **Automate a complex growth and content operations workflow: publish scheduled social content across multiple platforms, notify collaborators, update tracking spreadsheets, log lead and outreach activity, send Telegram reports, and inspect recent meeting notes from Fathom and Google Drive.**

   - Tools: `FACEBOOK_CREATE_PHOTO_POST`, `FACEBOOK_PROXY_EXECUTE`, `FACEBOOK_UPLOAD_PHOTOS_BATCH`, `FACEBOOK_UPLOAD_VIDEO`, `FATHOM_GET_RECORDING_SUMMARY`, `FATHOM_LIST_MEETINGS`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FOLDER`, `GOOGLEDRIVE_LIST_FILES`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_UPSERT_ROWS`, `GOOGLESHEETS_VALUES_GET`, `GOOGLESHEETS_VALUES_UPDATE`, `INSTAGRAM_GET_CONVERSATION`, `INSTAGRAM_GET_IG_MEDIA`, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_LIST_ALL_CONVERSATIONS`, `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`, `INSTAGRAM_SEND_TEXT_MESSAGE`, `LINKEDIN_PROXY_EXECUTE`, `TELEGRAM_SEND_MESSAGE`, `YOUTUBE_MULTIPART_UPLOAD_VIDEO`
   - Description: The workflow combined content publishing, reporting, and operations tracking.

30. **Generate recurring daily activity summaries by collecting recent email activity, social page activity, and Fireflies meeting transcripts for a local-day reporting window.**

   - Tools: `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_PAGE_TAGGED_POSTS`, `FIREFLIES_GET_TRANSCRIPTS`, `FIREFLIES_GET_TRANSCRIPT_BY_ID`, `OUTLOOK_GET_MESSAGE`, `OUTLOOK_GET_PROFILE`, `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_SEARCH_MESSAGES`, `PIPEDRIVE_SEARCH_DEALS`, `PIPEDRIVE_SEARCH_ORGANIZATIONS`, `PIPEDRIVE_SEARCH_PERSONS`
   - Description: The workflow repeatedly gathered daily business activity from multiple sources: Outlook messages across several accounts, Fireflies meeting transcripts for local-day windows, and Facebook page activity.

31. **Monitor and inspect Outlook email messages, summarize or verify their contents, sometimes process attachments or market data, create reminders/tasks, and attempt to send concise notifications through WhatsApp or a Notis channel.**

   - Tools: `COMPOSIO_SEARCH_FINANCE`, `OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT`, `OUTLOOK_GET_MAIL_FOLDER_MESSAGE`, `OUTLOOK_GET_MESSAGE`, `OUTLOOK_GET_PROFILE`, `OUTLOOK_LIST_MESSAGES`, `OUTLOOK_LIST_OUTLOOK_ATTACHMENTS`, `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_SEARCH_MESSAGES`, `TICKTICK_CREATE_TASK`, `TICKTICK_GET_TASK_BY_PROJECT_AND_ID`, `TICKTICK_LIST_ALL_TASKS`, `WHATSAPP_GET_PHONE_NUMBERS`
   - Description: The workflow repeatedly processed Outlook email events: retrieving messages, extracting sender/subject/body/metadata, handling large HTML responses, recovering bad message IDs, inspecting attachments, and occasionally creating TickTick tasks or fetching market data.

32. **The session covered multiple unrelated workflows: public web research, financial-product research, real-estate listing checks, browser QA for a web prototype, attempted Discord role updates, GitHub repository inspection setup, and retail beverage catalog research.**

   - Tools: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`, `COMPOSIO_SEARCH_GROQ_CHAT`, `COMPOSIO_SEARCH_SHOPPING`, `COMPOSIO_SEARCH_WEB`, `DISCORD_PROXY_EXECUTE`
   - Description: The agent repeatedly used tool search to find tools, then mostly completed public web and financial research via Composio Search web/fetch tools, browser-based listing extraction and web QA via Browser Tool, and several evidence-summarization passes.

33. **Analyze WhatsApp-style broadcast campaigns in Kommo CRM, including detected campaign sends, audience reach, replies, conversions, templates, segments, and related agent activity.**

   - Tools: `KOMMO_LIST_CONVERSATIONS`, `KOMMO_LIST_ENTITY_TAGS`, `KOMMO_LIST_EVENTS`, `KOMMO_LIST_LEADS`, `KOMMO_LIST_NOTES_BY_ENTITY`, `KOMMO_LIST_PIPELINE_STAGES`, `KOMMO_LIST_TEMPLATES`
   - Description: The workflow started with a request to list messaging broadcasts in Kommo CRM with delivery and read statistics.

34. **Audit and maintain Pipedrive CRM data: find deals and contacts, inspect activities/notes/pipeline stages, analyze sales-development activity hygiene, move long-horizon deals to a long-term review stage, create follow-up tasks for deals without future activity, and reassign mismatched deal owners.**

   - Tools: `PIPEDRIVE_ADD_AN_ACTIVITY`, `PIPEDRIVE_GET_ALL_ACTIVITIES_ASSIGNED_TO_A_PARTICULAR_USER`, `PIPEDRIVE_GET_ALL_DEAL_FIELDS`, `PIPEDRIVE_GET_ALL_NOTES`, `PIPEDRIVE_GET_ALL_PIPELINES`, `PIPEDRIVE_GET_ALL_STAGES`, `PIPEDRIVE_GET_DEAL`, `PIPEDRIVE_GET_DEALS_IN_A_PIPELINE`, `PIPEDRIVE_GET_DEALS_IN_A_STAGE`, `PIPEDRIVE_GET_ORGANIZATION`, `PIPEDRIVE_GET_PERSON`, `PIPEDRIVE_LIST_DEAL_ACTIVITIES`, `PIPEDRIVE_SEARCH_DEALS`, `PIPEDRIVE_SEARCH_PERSONS`, `PIPEDRIVE_UPDATE_DEAL`, `PIPEDRIVE_UPDATE_DEAL_V2`
   - Description: The workflow used Pipedrive to inspect deal records, people, activities, notes, stages, and pipelines; then it performed CRM hygiene operations.

35. **Fetch paginated Instagram media comments, identify comments needing replies, post reply ratings in bulk, and later clean up duplicate or mistaken replies.**

   - Tools: `INSTAGRAM_DELETE_COMMENT`, `INSTAGRAM_GET_IG_COMMENT_REPLIES`, `INSTAGRAM_GET_IG_MEDIA_COMMENTS`, `INSTAGRAM_POST_IG_COMMENT_REPLIES`
   - Description: The workflow processed a large Instagram comment thread on a media item.

36. **Manage a GitHub repository workflow: authenticate, inspect organization/repository access, create and label pull requests, inspect CI and workflow logs, merge approved changes, dispatch build/deploy/destroy workflows, and troubleshoot deployment failures.**

   - Tools: `GITHUB_ADD_LABELS_TO_AN_ISSUE`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_CREATE_A_REFERENCE`, `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`, `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_FIND_REPOSITORIES`, `GITHUB_GET_A_BRANCH`, `GITHUB_GET_A_COMMIT`, `GITHUB_GET_A_PULL_REQUEST`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_RAW_REPOSITORY_CONTENT`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`, `GITHUB_LIST_COMMITS`, `GITHUB_LIST_ISSUE_COMMENTS`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_LIST_LABELS_FOR_A_REPOSITORY`, `GITHUB_LIST_ORGANIZATIONS_FOR_THE_AUTHENTICATED_USER`, `GITHUB_LIST_ORGANIZATION_REPOSITORIES`, `GITHUB_LIST_PULL_REQUESTS`, `GITHUB_LIST_PULL_REQUESTS_FILES`, `GITHUB_LIST_REPOSITORIES_FOR_A_USER`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_WORKFLOW`, `GITHUB_MERGE_A_PULL_REQUEST`, `GITHUB_SEARCH_CODE`, `GITHUB_SEARCH_REPOSITORIES`
   - Description: The workflow connected GitHub, verified organization and repository access, enumerated repositories, opened multiple pull requests, applied protection labels, inspected CI status and logs, merged approved pull requests with SHA-pinned squash merges, edited repository files through branches and content commits…

37. **Manage and triage Outlook email at scale: query inbox messages, inspect bodies and attachments, reply or forward selected messages, create and organize folders, move or delete messages, download attachments, and create a calendar invite.**

   - Tools: `OUTLOOK_BATCH_MOVE_MESSAGES`, `OUTLOOK_CREATE_MAIL_FOLDER`, `OUTLOOK_CREATE_ME_EVENT`, `OUTLOOK_CREATE_USER_MAIL_FOLDERS_CHILD_FOLDERS`, `OUTLOOK_DELETE_MAIL_FOLDER`, `OUTLOOK_DELETE_MESSAGE`, `OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT`, `OUTLOOK_FORWARD_MESSAGE`, `OUTLOOK_GET_MESSAGE`, `OUTLOOK_LIST_CHILD_MAIL_FOLDERS`, `OUTLOOK_LIST_MAIL_FOLDERS`, `OUTLOOK_LIST_OUTLOOK_ATTACHMENTS`, `OUTLOOK_MOVE_MAIL_FOLDER`, `OUTLOOK_MOVE_MESSAGE`, `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_REPLY_EMAIL`, `OUTLOOK_SEARCH_MESSAGES`
   - Description: The workflow started with Outlook attachment retrieval, then expanded into a large email-management and triage operation.

38. **Analyze Salesforce opportunity and pipeline data, read and update a Google Sheets tracking spreadsheet, search a Salesforce account, and attempt to send a Slack direct message with CRM-derived context.**

   - Tools: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_SEARCH_SPREADSHEETS`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `SALESFORCE_QUERY`, `SALESFORCE_RUN_SOQL_QUERY`, `SALESFORCE_SEARCH_ACCOUNTS`, `SLACK_FIND_USER_BY_EMAIL_ADDRESS`
   - Description: The workflow was dominated by Salesforce reporting: querying opportunities, resolving owners and teams, producing counts and aggregate amounts, and retrieving detailed pages.

39. **Audit and reconcile CRM lead activity into a spreadsheet-based reporting workbook, including lead extraction, source classification, social-seller separation, outcome tracking, summary updates, and final verification.**

   - Tools: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_VALUES_UPDATE`, `KOMMO_GET_LEAD`, `KOMMO_LIST_CONTACTS`, `KOMMO_LIST_EVENTS`, `KOMMO_LIST_LEADS`, `KOMMO_LIST_NOTES_BY_ENTITY`
   - Description: The workflow performed a complex CRM-to-spreadsheet reconciliation.

40. **Create, iteratively refine, verify, and operationalize a Notion specification page, then create related Linear implementation issues and relationships.**

   - Tools: `LINEAR_CREATE_LINEAR_ISSUE`, `LINEAR_LIST_LINEAR_LABELS`, `LINEAR_LIST_LINEAR_PROJECTS`, `LINEAR_LIST_LINEAR_TEAMS`, `LINEAR_RUN_QUERY_OR_MUTATION`, `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_DELETE_BLOCK`, `NOTION_FETCH_BLOCK_CONTENTS`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_INSERT_ROW_DATABASE`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_SEARCH_NOTION_PAGE`, `NOTION_UPDATE_ROW_DATABASE`
   - Description: The workflow used Notion to find existing specification material, create a new database-backed specification page, append a large structured body, perform many subsequent anchored insertions and cleanup edits, and promote the row status.

41. **Implement and release a protected budget dashboard feature by reading Google Sheets and Google Docs data, retrieving deployment secrets from Vercel, committing and merging code changes, verifying deployments, and updating a Jira issue.**

   - Tools: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_DELETE_A_REFERENCE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_MERGE_A_PULL_REQUEST`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_GET_SHEET_NAMES`, `JIRA_ADD_COMMENT`, `JIRA_ASSIGN_ISSUE`, `JIRA_TRANSITION_ISSUE`, `VERCEL_FILTER_PROJECT_ENVS`, `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_PROJECT_ENV`
   - Description: The workflow gathered spreadsheet data, retrieved a service account-related secret from Vercel, built and merged repository changes for a protected budget dashboard, verified staging and production deployments, diagnosed and fixed a Google Doc HTML parsing issue, and kept the associated Jira issue updated through…

42. **Manage calendar accounts and events across multiple calendar accounts, send a Slack direct message with meeting details, share calendars between accounts, and create/update calendar events for personal and work planning.**

   - Tools: `GOOGLECALENDAR_ACL_INSERT`, `GOOGLECALENDAR_CALENDAR_LIST_INSERT`, `GOOGLECALENDAR_CREATE_EVENT`, `GOOGLECALENDAR_EVENTS_LIST`, `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`, `GOOGLECALENDAR_PATCH_EVENT`, `SLACK_FIND_USERS`, `SLACK_OPEN_DM`, `SLACK_SEND_MESSAGE`
   - Description: The workflow connected and validated calendar accounts, created events, opened a Slack DM to a resolved user, and sent meeting details.

43. **Read an existing Google spreadsheet, preserve formulas and current values, add and populate new tabs with formulas and supporting details, verify recalculation, and organize related Google Drive documents.**

   - Tools: `GOOGLEDRIVE_CREATE_FOLDER`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_MOVE_FILE`, `GOOGLESHEETS_ADD_SHEET`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_GET_SPREADSHEET_INFO`
   - Description: The workflow started by searching for tools to read and update a Google spreadsheet.

44. **Browse a Bitbucket repository directory tree and retrieve selected repository file contents.**

   - Tools: `BITBUCKET_BROWSE_REPOSITORY_PATH`, `BITBUCKET_GET_FILE_FROM_REPOSITORY`, `BITBUCKET_GET_REPOSITORY`, `BITBUCKET_LIST_REPOSITORY_PATHS`
   - Description: The workflow searched for Bitbucket tools, browsed a repository directory, recursively listed subdirectories and files, and fetched selected file contents.

45. **Create and publish a HubSpot quote for a CRM contact by first finding the contact, creating a deal, creating line items and a quote, applying quote terms and template settings, publishing the quote, and inspecting quote/template properties.**

   - Tools: `HUBSPOT_CREATE_DEAL`, `HUBSPOT_CREATE_LINE_ITEM`, `HUBSPOT_CREATE_OBJECT_ASSOCIATION`, `HUBSPOT_CREATE_QUOTE_OBJECT`, `HUBSPOT_GET_QUOTE`, `HUBSPOT_LIST_ASSOCIATION_TYPES`, `HUBSPOT_LIST_CONTACTS`, `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE`, `HUBSPOT_READ_APAGE_OF_OBJECTS_BY_TYPE`, `HUBSPOT_READ_ASSOCIATIONS_BATCH`, `HUBSPOT_READ_CRM_OBJECT_BY_ID`, `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE`, `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA`, `HUBSPOT_SEARCH_CRM_OBJECTS_BY_CRITERIA`, `HUBSPOT_UPDATE_QUOTE`
   - Description: The workflow began by finding an existing HubSpot contact, then creating a deal with a valid pipeline stage and contact association.

46. **Create, update, query, and verify Notion database rows and page content for generic deal-room style pages, including owner lookup, bulk content replacement, child-page preservation, and database filtering.**

   - Tools: `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_CREATE_NOTION_PAGE`, `NOTION_FETCH_ALL_BLOCK_CONTENTS`, `NOTION_FETCH_BLOCK_CONTENTS`, `NOTION_FETCH_DATABASE`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_LIST_USERS`, `NOTION_QUERY_DATABASE`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_REPLACE_PAGE_CONTENT`, `NOTION_RETRIEVE_PAGE`, `NOTION_SEARCH_NOTION_PAGE`, `NOTION_UPDATE_PAGE`, `NOTION_UPSERT_ROW_DATABASE`
   - Description: The workflow centered on Notion database and page management.

47. **Duplicate an existing Meta Ads campaign using the Meta Marketing API copies capability.**

   - Tools: `METAADS_CREATE_AD`, `METAADS_CREATE_AD_SET`, `METAADS_CREATE_CAMPAIGN`, `METAADS_DELETE_CAMPAIGN`, `METAADS_GET_AD_CREATIVE`, `METAADS_GET_INSIGHTS`, `METAADS_GET_OBJECT`, `METAADS_LIST_ADS`, `METAADS_READ_ADSETS`, `METAADS_UPDATE_CAMPAIGN`
   - Description: The user wanted to duplicate a Meta Ads campaign using a copies-style endpoint.

48. **Generate and post-process a long text-to-speech audio asset, upload it to cloud storage, research YouTube content opportunities and comments, then update YouTube channel branding metadata.**

   - Tools: `ELEVENLABS_GET_USER_SUBSCRIPTION_INFO`, `ELEVENLABS_TEXT_TO_SPEECH`, `GOOGLEDRIVE_CREATE_FOLDER`, `GOOGLEDRIVE_RESUMABLE_UPLOAD`, `YOUTUBE_GET_CHANNEL_STATISTICS`, `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_COMMENT_THREADS2`, `YOUTUBE_SEARCH_YOU_TUBE`, `YOUTUBE_UPDATE_CHANNEL`
   - Description: The workflow first checked remaining text-to-speech quota, generated a long narration in multiple ElevenLabs chunks, then used sandbox audio processing to trim, concatenate, normalize, and encode a finished MP3.

49. **Organize recently uploaded receipt and invoice files in Google Drive: find recent files, download/convert images to PDFs, upload or update Drive files, create destination folders, rename and move documents, trash originals or duplicates, verify results, and attempt a spreadsheet correction.**

   - Tools: `GOOGLEDRIVE_COPY_FILE_ADVANCED`, `GOOGLEDRIVE_CREATE_FOLDER`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_GET_FILE_METADATA`, `GOOGLEDRIVE_TRASH_FILE`, `GOOGLEDRIVE_UPDATE_FILE_PUT`, `GOOGLEDRIVE_UPLOAD_FILE`
   - Description: The workflow used Google Drive to find recently uploaded receipt files, confirm folder context, download image files, convert them to PDFs, upload the PDFs into invoice folders, create a new folder structure, rename and move documents, trash originals and duplicates, and verify final folder contents.

50. **Verify the correct Slack workspace, identify members of a Slack channel, send an approved direct message to selected members, and remediate accidental sends in the wrong workspace.**

   - Tools: `SLACK_DELETES_A_MESSAGE_FROM_A_CHAT`, `SLACK_FETCH_CONVERSATION_HISTORY`, `SLACK_FIND_CHANNELS`, `SLACK_LIST_ALL_USERS`, `SLACK_OPEN_DM`, `SLACK_RETRIEVE_CONVERSATION_MEMBERS_LIST`, `SLACK_SEARCH_MESSAGES`, `SLACK_SEND_MESSAGE`, `SLACK_TEST_AUTH`
   - Description: The workflow began by searching for Slack tools to verify a connection, identify channel members, and send direct messages.

51. **Fetch and annotate support-thread evidence, retrieve attachment download links, and later verify an Instagram DM tool fix using Instagram reads/sends plus Metabase, Datadog, and spreadsheet evidence.**

   - Tools: `DATADOG_LIST_LOG_INDEXES`, `DATADOG_SEARCH_LOGS`, `GOOGLESHEETS_BATCH_GET`, `INSTAGRAM_GET_CONVERSATION`, `INSTAGRAM_GET_PAGE_CONVERSATIONS`, `INSTAGRAM_LIST_ALL_CONVERSATIONS`, `INSTAGRAM_LIST_ALL_MESSAGES`, `INSTAGRAM_SEND_TEXT_MESSAGE`, `METABASE_POST_API_DATASET`, `PLAIN_RUN_GRAPHQL_QUERY`
   - Description: The workflow first used Plain GraphQL to fetch support-thread timelines, recover from schema validation errors, create internal attribution notes, and generate clean attachment download URLs.

52. **Migrate a user's memory data from Mem0 into Zep, inspect existing Zep context, attempt to organize migrated content by project-like scopes, and verify that the imported content is searchable.**

   - Tools: `MEM0_GET_MEMORIES_BY_ENTITY`, `ZEP_CREATE_GRAPH`, `ZEP_GET_PROJECT_INFO`, `ZEP_GET_USER_NODE`, `ZEP_GRAPH_SEARCH`, `ZEP_LIST_GROUPS_ORDERED`
   - Description: The workflow began by reading existing Zep context, then connected Mem0 and enumerated multiple memory entities.

53. **Audit a short-link inventory by finding an existing spreadsheet registry, reading help-center mapping tabs, listing existing short links, and attempting to compare them with live public website article URLs and redirects.**

   - Tools: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_GET_SESSION`, `BROWSER_TOOL_STOP_TASK`, `BROWSER_TOOL_WATCH_TASK`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_SEARCH_SPREADSHEETS`, `GOOGLESHEETS_VALUES_GET`, `TINYURL_LIST_URLS`
   - Description: The workflow began as a short-link and help-center mapping audit.

54. **Audit advertising account health and performance, probe analytics property access, create and verify a new Google Ads search campaign with budget, targeting, ad group, keywords, and responsive search ad, and later discover Asana tools for listing tasks assigned to the current user.**

   - Tools: `GOOGLEADS_MUTATE_AD_GROUPS`, `GOOGLEADS_MUTATE_AD_GROUP_ADS`, `GOOGLEADS_MUTATE_AD_GROUP_CRITERIA`, `GOOGLEADS_MUTATE_CAMPAIGNS`, `GOOGLEADS_MUTATE_CAMPAIGN_BUDGETS`, `GOOGLEADS_MUTATE_CAMPAIGN_CRITERIA`, `GOOGLEADS_SEARCH_STREAM_GAQL`, `GOOGLE_ANALYTICS_LIST_ACCOUNT_SUMMARIES`
   - Description: The workflow began with analytics property discovery, then shifted into a multi-account Google Ads audit using GAQL for account, campaign, billing, change-history, policy, and performance checks.

55. **Automate and refine a complex Google Sheets financial/workforce model: apply formatting, dropdown validation, filters, formulas, instructional text, payroll-style calculations, and employee allocation logic across multiple worksheets.**

   - Tools: `GOOGLESHEETS_AUTO_RESIZE_DIMENSIONS`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_CLEAR_VALUES`, `GOOGLESHEETS_FORMAT_CELL`, `GOOGLESHEETS_GET_SPREADSHEET_INFO`, `GOOGLESHEETS_SET_BASIC_FILTER`, `GOOGLESHEETS_SET_DATA_VALIDATION_RULE`, `GOOGLESHEETS_SPREADSHEETS_VALUES_BATCH_CLEAR`, `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_UPSERT_ROWS`, `GOOGLESHEETS_VALUES_GET`
   - Description: The workflow automated a complex Google Sheets model.

56. **Clean up and enrich HubSpot CRM records by listing contacts and companies, matching contacts to companies, assigning segmentation values from job title and company industry, creating required CRM properties, updating contacts in bulk, creating associations, and attempting a later bulk import of companies and contacts.**

   - Tools: `HUBSPOT_CREATE_COMPANIES`, `HUBSPOT_CREATE_CONTACTS`, `HUBSPOT_CREATE_OBJECT_ASSOCIATION`, `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE`, `HUBSPOT_LIST_ASSOCIATION_TYPES`, `HUBSPOT_LIST_COMPANIES`, `HUBSPOT_LIST_CONTACTS`, `HUBSPOT_LIST_CONTACT_PROPERTIES`, `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE`, `HUBSPOT_UPDATE_BATCH_OF_OBJECTS_BY_IDOR_PROPERTY_VALUES`, `HUBSPOT_UPDATE_CONTACTS`
   - Description: The workflow began by connecting HubSpot, discovering contact and company schema, and exporting contacts and companies.

57. **Create short dog-themed videos, analyze channel and trend performance, upload and manage YouTube Shorts, and inspect Instagram posting context.**

   - Tools: `GEMINI_GENERATE_IMAGE`, `GEMINI_GENERATE_VIDEOS`, `INSTAGRAM_GET_IG_USER_MEDIA`, `YOUTUBE_DELETE_VIDEO`, `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CHANNEL_VIDEOS`, `YOUTUBE_MULTIPART_UPLOAD_VIDEO`, `YOUTUBE_SEARCH_YOU_TUBE`, `YOUTUBE_UPDATE_VIDEO`
   - Description: The workflow began by discovering tools for Gemini/Veo video generation and YouTube upload, then analyzed the authenticated YouTube channel's videos to identify high-performing patterns.

58. **Inspect and modify a GitHub repository frontend, validate the changes if possible, then commit and push the changes directly to the default branch.**

   - Tools: `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`
   - Description: The workflow targeted a deep frontend code audit and modification in a GitHub repository.

59. **Manage an Outlook mailbox by fetching recent inbox messages, classifying and moving messages or whole threads into routing folders, marking VIP emails high importance, creating staged reply drafts, and producing a structured list of items needing replies.**

   - Tools: `OUTLOOK_BATCH_MOVE_MESSAGES`, `OUTLOOK_BATCH_UPDATE_MESSAGES`, `OUTLOOK_CREATE_DRAFT_REPLY`, `OUTLOOK_CREATE_REPLY_ALL_DRAFT`, `OUTLOOK_GET_MAIL_FOLDER`, `OUTLOOK_GET_MESSAGE`, `OUTLOOK_LIST_MAIL_FOLDERS`, `OUTLOOK_LIST_MAIL_FOLDER_MESSAGES`, `OUTLOOK_MOVE_MESSAGE`, `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_UPDATE_EMAIL`
   - Description: The workflow repeatedly triaged an Outlook inbox.

60. **Manage lead data in Google Sheets: read existing tabs, append and correct lead rows, enrich contacts, detect duplicate email addresses, highlight duplicate rows, and attempt to prepare leads for import into an Instantly campaign.**

   - Tools: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_FORMAT_CELL`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_GET_SPREADSHEET_INFO`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_VALUES_GET`, `GOOGLESHEETS_VALUES_UPDATE`, `HUNTER_DOMAIN_SEARCH`, `HUNTER_EMAIL_FINDER`
   - Description: The workflow centered on maintaining lead spreadsheets.

61. **Manage Outlook mailbox organization by discovering folders, finding messages by sender/read status, moving messages into appropriate folders, marking selected messages as read, verifying counts, and sending HTML report emails with CC recipients.**

   - Tools: `OUTLOOK_LIST_MAIL_FOLDERS`, `OUTLOOK_MOVE_MESSAGE`, `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_SEND_EMAIL`, `OUTLOOK_UPDATE_EMAIL`
   - Description: The workflow used Outlook to organize mailbox messages and send report emails.

62. **Update an existing Google Docs nutrition-planning document by changing table content for two dinner entries, adding shared batch-cooking instructions, recalculating related summary content, and verifying the final document.**

   - Tools: `GOOGLEDOCS_GET_DOCUMENT_BY_ID`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT`
   - Description: The workflow began by searching for Google Docs tools, then fetched both structured and plaintext versions of an existing document.

63. **Collect operational evidence across spreadsheets, calendar, code repository, ecommerce store, and drive; generate formatted daily dashboard/report tabs; append log rows; and verify the written spreadsheet outputs.**

   - Tools: `GITHUB_LIST_COMMITS`, `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLESHEETS_ADD_SHEET`, `GOOGLESHEETS_APPEND_DIMENSION`, `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_FORMAT_CELL`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`, `GOOGLESHEETS_UPDATE_DIMENSION_PROPERTIES`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `SHOPIFY_GET_ORDERS_WITH_FILTERS`, `SHOPIFY_GET_PRODUCTS`, `SHOPIFY_GET_SHOP_DETAILS`
   - Description: The workflow gathered status data from several connected systems, read existing spreadsheet records, attempted ecommerce store reads, checked calendar and repository activity, searched recent Drive changes, then created new formatted report tabs in an existing spreadsheet.

64. **Prepare marketing and CRM automation work: gather marketing performance data, send a brief by email, analyze search query data, and scaffold a HubSpot customer follow-up campaign with custom properties, email drafts, and bulk contact updates.**

   - Tools: `GOOGLEADS_SEARCH_STREAM_GAQL`, `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `HUBSPOT_CLONE_MARKETING_EMAIL`, `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE`, `HUBSPOT_UPDATE_A_MARKETING_EMAIL`, `HUBSPOT_UPDATE_CONTACTS`, `OUTLOOK_SEND_EMAIL`
   - Description: The workflow first pulled marketing analytics and search performance data, with the ads query blocked by quota errors, then sent an email brief successfully through Outlook.

65. **Read and update Google Sheets-based SEO planning templates, enrich them with Search Console performance data, and verify that spreadsheet formulas and cleanup steps produced the expected results.**

   - Tools: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_BATCH_UPDATE`, `GOOGLESHEETS_CLEAR_VALUES`, `GOOGLESHEETS_GET_SHEET_NAMES`, `GOOGLESHEETS_VALUES_GET`, `GOOGLESHEETS_VALUES_UPDATE`, `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
   - Description: The workflow discovered spreadsheet worksheet names, inspected template headers and formulas, wrote structured SEO planning data into fixed spreadsheet regions, verified formula-derived outputs, queried Search Console page metrics for comparative date windows, processed a large analytics response, and cleaned stale or…

66. **Create customized application emails with resume and cover letter PDFs, stage them as Outlook drafts, update attachments and body text, then send the finalized drafts after confirmation.**

   - Tools: `OUTLOOK_ADD_MAIL_ATTACHMENT`, `OUTLOOK_CREATE_DRAFT`, `OUTLOOK_DELETE_MESSAGE`, `OUTLOOK_DELETE_MESSAGE_ATTACHMENT`, `OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT`, `OUTLOOK_LIST_MESSAGES`, `OUTLOOK_LIST_OUTLOOK_ATTACHMENTS`, `OUTLOOK_SEND_DRAFT`, `OUTLOOK_UPDATE_EMAIL`
   - Description: The workflow began as sending Outlook emails with PDF attachments, then expanded into generating multiple resume and cover letter PDFs, staging a large set of Outlook drafts, validating and replacing attachments, updating body wording, and sending the finalized drafts after confirmation.

67. **Manage Salesforce opportunity pipeline data: list open opportunities, update opportunity stages and required fields, verify record changes, consolidate duplicate contact data, and create a follow-up task linked to CRM records.**

   - Tools: `SALESFORCE_CREATE_TASK`, `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT`, `SALESFORCE_RUN_SOQL_QUERY`, `SALESFORCE_SOBJECT_ROWS_UPDATE`, `SALESFORCE_UPDATE_OPPORTUNITY`
   - Description: The workflow used Salesforce tools to query open opportunities, inspect object metadata for relevant fields, update multiple opportunity stages and required fields, recover from validation failures by querying missing supporting data, verify persisted changes, consolidate duplicate contact information with generic…

68. **Modify a GitHub-hosted backend application, add protected console and lead-care functionality, configure deployment/runtime infrastructure, apply database migrations, and verify CI plus hosted deployment status.**

   - Tools: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`, `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`, `GITHUB_LIST_CHECK_RUN_ANNOTATIONS`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`, `SUPABASE_BETA_RUN_SQL_QUERY`, `SUPABASE_GETS_PROJECT_S_SERVICE_HEALTH_STATUS`, `SUPABASE_RUN_READ_ONLY_QUERY`, `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_DEPLOYMENT_LOGS2`
   - Description: The workflow evolved from reading repository files into a large full-stack development and deployment effort.

69. **Perform a technical SEO audit around sitemap migration, indexability, linked-page health, and backlink/link-equity signals using Google Search Console and supporting crawl data.**

   - Tools: `AHREFS_RETRIEVE_SUBSCRIPTION_LIMITS_AND_USAGE`, `FIRECRAWL_SCRAPE`, `GOOGLE_SEARCH_CONSOLE_GET_SITEMAP`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`, `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
   - Description: The workflow investigated a website migration and SEO-health problem.

70. **Migrate Vercel projects and GitHub repositories between connected accounts, preserve domains and settings, add deployment workflows, trigger/verify deployments, and audit repository access.**

   - Tools: `GITHUB_COMPARE_TWO_COMMITS`, `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`, `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`, `GITHUB_DOWNLOAD_JOB_LOGS_FOR_A_WORKFLOW_RUN`, `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_JOBS_FOR_A_WORKFLOW_RUN`, `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_LIST_REPOSITORY_COLLABORATORS`, `GITHUB_LIST_REPOSITORY_INVITATIONS`, `GITHUB_LIST_REPOSITORY_SECRETS`, `GITHUB_LIST_WORKFLOW_RUNS_FOR_A_REPOSITORY`, `VERCEL_CREATE_PROJECT_TRANSFER_REQUEST`, `VERCEL_GET_AUTH_USER`, `VERCEL_GET_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENTS`, `VERCEL_GET_PROJECT2`, `VERCEL_GET_PROJECTS`, `VERCEL_GET_PROJECT_DOMAINS`, `VERCEL_LIST_DOMAINS`
   - Description: The workflow migrated web hosting projects and code repositories from one connected account to another.

71. **Automate a personalized outbound email workflow: check whether prior communication exists, retrieve a CRM-style contact record, send an Outlook email, then update the Airtable record to mark outreach as completed.**

   - Tools: `AIRTABLE_GET_RECORD`, `AIRTABLE_LIST_RECORDS`, `AIRTABLE_UPDATE_RECORD`, `OUTLOOK_SEARCH_MESSAGES`, `OUTLOOK_SEND_EMAIL`
   - Description: The workflow attempted to automate outbound outreach.

72. **Build, repair, deploy, configure, and test a Vercel-hosted GitHub-backed API proxy for Gemini text, image, video, embeddings, model listing, OpenAI-compatible paths, and tool-call-style outputs.**

   - Tools: `GEMINI_COUNT_TOKENS`, `GEMINI_EMBED_CONTENT`, `GEMINI_GENERATE_CONTENT`, `GEMINI_GENERATE_IMAGE`, `GEMINI_GENERATE_VIDEOS`, `GEMINI_LIST_MODELS`, `GEMINI_WAIT_FOR_VIDEO`, `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`, `GITHUB_DELETE_A_FILE`, `GITHUB_GET_RAW_REPOSITORY_CONTENT`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_BRANCHES`, `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_CREATE_NEW_DEPLOYMENT`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`, `VERCEL_GET_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENT_EVENTS2`, `VERCEL_GET_DEPLOYMENT_LOGS2`
   - Description: The workflow started by inspecting an existing Vercel deployment, reading and modifying a GitHub-backed serverless project, then repeatedly deploying to Vercel and testing endpoints.

73. **Manage a large operational workflow across Google Tasks, Xero, and Notion: update and move task records, create and revise invoices, record payments, consolidate Notion rules, and track operational follow-ups.**

   - Tools: `GOOGLECALENDAR_GET_CURRENT_DATE_TIME`, `GOOGLETASKS_DELETE_TASK`, `GOOGLETASKS_INSERT_TASK`, `GOOGLETASKS_LIST_TASKS`, `GOOGLETASKS_PATCH_TASK`, `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_FETCH_BLOCK_CONTENTS`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_REPLACE_PAGE_CONTENT`, `NOTION_RETRIEVE_PAGE`, `NOTION_SEARCH_NOTION_PAGE`, `XERO_CREATE_CONTACT`, `XERO_CREATE_INVOICE`, `XERO_CREATE_PAYMENT`, `XERO_GET_CONTACTS`, `XERO_GET_INVOICE`, `XERO_LIST_INVOICES`, `XERO_POST_INVOICE_UPDATE`
   - Description: The workflow maintained a complex operations backlog: tasks were listed, updated, copied between lists, completed, and deleted in Google Tasks; Xero contacts, invoices, invoice updates, and payments were created or verified; Notion pages were searched, appended to, fetched, and replaced; and several failures were…

74. **Analyze Salesforce opportunity pipeline data by discovering a custom field, retrieving stage metadata, querying filtered opportunity records, fetching stage-change history, and computing stage conversion and skip metrics.**

   - Tools: `SALESFORCE_GET_ALL_FIELDS_FOR_OBJECT`, `SALESFORCE_RUN_SOQL_QUERY`
   - Description: The workflow used Salesforce metadata and SOQL tools to analyze opportunity pipeline progression.

75. **Fetch recent Slack conversation history and threaded replies from one or more conversations for downstream review or export.**

   - Tools: `SLACK_FETCH_CONVERSATION_HISTORY`, `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION`
   - Description: The workflow searched for Slack history-retrieval tools, then fetched recent parent messages from many Slack conversations.

76. **Build a cross-channel marketing and operations report by pulling Meta Ads performance and account status, GA4 funnel and revenue data, Instagram profile/insights, Microsoft Clarity friction metrics, and ClickUp docs/tasks for planning context.**

   - Tools: `CLICKUP_GET_DOC_PAGE_CONTENT`, `CLICKUP_GET_DOC_PAGE_LISTING`, `CLICKUP_GET_FILTERED_TEAM_TASKS`, `CLICKUP_GET_LIST_MEMBERS`, `CLICKUP_GET_WORKSPACE_SEATS`, `GOOGLE_ANALYTICS_BATCH_RUN_REPORTS`, `GOOGLE_ANALYTICS_RUN_REPORT`, `INSTAGRAM_GET_USER_INFO`, `INSTAGRAM_GET_USER_INSIGHTS`, `METAADS_GET_INSIGHTS`, `METAADS_GET_OBJECT`, `MICROSOFT_CLARITY_DATA_EXPORT`
   - Description: The workflow gathered Meta Ads campaign and account data, GA4 event/channel/revenue reports, Instagram profile and insight metrics, and Microsoft Clarity friction exports.

77. **Audit a Google Ads client account under a manager account, research targeting and keywords, then build and verify a new search campaign with budget, targeting, keywords, ads, and assets.**

   - Tools: `GOOGLEADS_SEARCH_STREAM_GAQL`
   - Description: The workflow started by discovering and verifying access to a Google Ads client account under a manager account.

78. **Audit and clean Pipedrive CRM data by exporting paginated leads and related records, then bulk-normalizing titles, organization names, duplicate organizations, deal and lead titles, lead labels, and custom-field data.**

   - Tools: `PIPEDRIVE_ADD_ORGANIZATION_FIELD`, `PIPEDRIVE_DELETE_LEAD`, `PIPEDRIVE_GET_ALL_DEALS`, `PIPEDRIVE_GET_ALL_LEADS`, `PIPEDRIVE_GET_ALL_LEAD_LABELS`, `PIPEDRIVE_GET_ALL_NOTES`, `PIPEDRIVE_GET_ALL_ORGANIZATIONS`, `PIPEDRIVE_GET_ALL_ORGANIZATION_FIELDS`, `PIPEDRIVE_GET_ALL_PERSONS`, `PIPEDRIVE_GET_DEAL`, `PIPEDRIVE_GET_LEAD_FIELDS`, `PIPEDRIVE_GET_ONE_LEAD`, `PIPEDRIVE_GET_ORGANIZATION`, `PIPEDRIVE_GET_PERSON`, `PIPEDRIVE_LIST_ORGANIZATION_PERSONS`, `PIPEDRIVE_MERGE_ORGANIZATIONS`, `PIPEDRIVE_UPDATE_AN_ORGANIZATION`, `PIPEDRIVE_UPDATE_DEAL`, `PIPEDRIVE_UPDATE_LEAD`, `PIPEDRIVE_UPDATE_ORGANIZATION`
   - Description: The workflow began with a Pipedrive lead export request and expanded into a large CRM data-cleanup operation.

79. **Audit and manage a YouTube channel by collecting channel/video data, analyzing performance, listing and restructuring playlists, adding/removing/reordering playlist videos, and researching high-performing YouTube topics.**

   - Tools: `YOUTUBE_ADD_VIDEO_TO_PLAYLIST`, `YOUTUBE_CREATE_PLAYLIST`, `YOUTUBE_DELETE_PLAYLIST_ITEM`, `YOUTUBE_GET_CHANNEL_STATISTICS`, `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CHANNEL_SECTIONS`, `YOUTUBE_LIST_CHANNEL_VIDEOS`, `YOUTUBE_LIST_PLAYLIST_ITEMS`, `YOUTUBE_LIST_USER_PLAYLISTS`, `YOUTUBE_SEARCH_YOU_TUBE`, `YOUTUBE_UPDATE_PLAYLIST`, `YOUTUBE_UPDATE_PLAYLIST_ITEM`
   - Description: The workflow used YouTube tools to gather channel state, enumerate uploads and playlists, fetch public video statistics, analyze performance, update and create playlists, reconcile playlist contents, recover from transient playlist-item failures, deduplicate entries, test reordering, and perform search-based topic…

80. **Audit Meta Ads account access, inspect performance for a specific ad set, identify improvement actions, then create a Trello card with an attached report and assignee; also attempt to clean up a faulty attachment.**

   - Tools: `FACEBOOK_GET_CURRENT_USER`, `METAADS_GET_AD_ACCOUNTS`, `METAADS_GET_INSIGHTS`, `METAADS_GET_OBJECT`, `METAADS_READ_ADSETS`, `TRELLO_ADD_CARDS`, `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD`, `TRELLO_ADD_CARDS_ATTACHMENTS_BY_ID_CARD`, `TRELLO_DELETE_CARD_ATTACHMENT`, `TRELLO_GET_BOARDS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERSHIPS_BY_ID_BOARD`, `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`, `TRELLO_GET_CARDS_BY_ID_CARD`, `TRELLO_GET_SEARCH_MEMBERS`
   - Description: The workflow began by trying to access Meta Ads accounts, required an active connection, then successfully listed accessible ad accounts.

81. **Inventory YouTube channel videos, generate and update video metadata in bulk, verify updates, and fetch captions/transcript for a YouTube video.**

   - Tools: `YOUTUBE_GET_CHANNEL_STATISTICS`, `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CAPTION_TRACK`, `YOUTUBE_LIST_CHANNEL_VIDEOS`, `YOUTUBE_LIST_PLAYLIST_ITEMS`, `YOUTUBE_LOAD_CAPTIONS`, `YOUTUBE_UPDATE_VIDEO`
   - Description: The workflow used YouTube tools to inventory channel uploads, enrich video records with full metadata, generate bulk descriptions and tags, apply updates, verify persistence, and retry a single failed write.

82. **Manage and clean up Outlook inbox messages by finding matches from senders, subject patterns, unread status, and folder locations; move matched emails into target folders, move unwanted emails to Deleted Items, create and remove temporary rules, and cluster remaining unread emails for triage.**

   - Tools: `OUTLOOK_BATCH_MOVE_MESSAGES`, `OUTLOOK_CREATE_MAIL_FOLDER_MESSAGE_RULE`, `OUTLOOK_DELETE_EMAIL_RULE`, `OUTLOOK_DELETE_MESSAGE`, `OUTLOOK_GET_MESSAGE`, `OUTLOOK_LIST_CHILD_MAIL_FOLDERS`, `OUTLOOK_LIST_EMAIL_RULES`, `OUTLOOK_LIST_MAIL_FOLDERS`, `OUTLOOK_LIST_MAIL_FOLDER_MESSAGES`, `OUTLOOK_MOVE_MESSAGE`, `OUTLOOK_MOVE_MESSAGE_FROM_FOLDER`, `OUTLOOK_QUERY_EMAILS`, `OUTLOOK_SEARCH_MESSAGES`
   - Description: The workflow managed an Outlook mailbox by identifying messages from exact senders and subject patterns, resolving top-level and nested folder IDs, moving matched messages into target folders, moving unwanted messages to Deleted Items or deleting them, and clustering remaining unread email.

83. **Read files from a Microsoft cloud document library, inspect related due-diligence email context, locate supporting documents, and attempt to replace existing document contents.**

   - Tools: `ONE_DRIVE_DOWNLOAD_FILE`, `ONE_DRIVE_GET_DRIVE_ITEM_BY_SHARING_URL`, `ONE_DRIVE_LIST_FOLDER_CHILDREN`, `ONE_DRIVE_SEARCH_ITEMS`, `ONE_DRIVE_UPDATE_FILE_CONTENT`, `OUTLOOK_GET_MESSAGE`, `OUTLOOK_SEARCH_MESSAGES`
   - Description: The workflow began by resolving a SharePoint-backed sharing link through OneDrive.

84. **Use GitHub to inspect accessible repositories and branches, fetch repository files, update multiple repository files, create a public static preview repository, enable GitHub Pages, and commit generated content/configuration files.**

   - Tools: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY`, `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`, `GITHUB_CREATE_OR_UPDATE_GITHUB_PAGES_SITE`, `GITHUB_GET_A_BRANCH`, `GITHUB_GET_A_TREE`, `GITHUB_GET_RAW_REPOSITORY_CONTENT`, `GITHUB_LIST_BRANCHES`, `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_SEARCH_CODE`
   - Description: The workflow used GitHub to discover repositories, validate branches and file paths, retrieve raw content, make many repository file updates, create a public static preview repository, publish it with GitHub Pages, and batch-commit generated content/configuration assets.

85. **Investigate and patch a codebase hosted on GitHub, commit changes to a target branch, document the change, and merge that branch into the destination branch after approval.**

   - Tools: `GITHUB_CREATE_A_COMMIT`, `GITHUB_CREATE_A_TREE`, `GITHUB_GET_A_COMMIT`, `GITHUB_GET_A_REFERENCE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_MERGE_A_BRANCH`, `GITHUB_SEARCH_CODE`, `GITHUB_UPDATE_A_REFERENCE`, `_1PASSWORD_LIST_VAULTS`
   - Description: The workflow used GitHub tools to read repository content, locate a relevant source file, inspect and patch authentication/session handling, create commits on a target branch, update documentation, and merge the branch into the destination branch.

86. **Retrieve Salesforce CRM report and query data for a business-performance brief, then send Slack notifications with the generated results.**

   - Tools: `SALESFORCE_GET_REPORT`, `SALESFORCE_GET_SUPPORT`, `SALESFORCE_QUERY`, `SALESFORCE_RUN_REPORT`, `SALESFORCE_RUN_SOQL_QUERY`, `SLACK_SEND_MESSAGE`
   - Description: The workflow attempted to notify a Slack recipient, but Slack delivery failed because there was no active connection and later attempts used invalid Slack send slugs.

87. **Set up and reorganize business lead-tracking and governance records in Notion, after initially exploring tools for social posting, web research, CRM lead handling, and website publishing.**

   - Tools: `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_CREATE_NOTION_PAGE`, `NOTION_DELETE_BLOCK`, `NOTION_FETCH_ALL_BLOCK_CONTENTS`, `NOTION_FETCH_DATA`, `NOTION_FETCH_DATABASE`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_INSERT_ROW_DATABASE`, `NOTION_QUERY_DATABASE`, `NOTION_UPDATE_ROW_DATABASE`
   - Description: The workflow began with broad tool discovery for social posting, Notion updates, web research, CRM activity, and website publishing.

88. **Bulk triage new Zendesk support tickets across multiple support mailboxes, enrich tickets with requester/order context, add private internal AI triage notes, tag tickets as analyzed, and verify private-comment visibility.**

   - Tools: `ZENDESK_GET_USER`, `ZENDESK_GET_ZENDESK_TICKET_BY_ID`, `ZENDESK_SEARCH_ZENDESK`, `ZENDESK_UPDATE_ZENDESK_TICKET`
   - Description: The agent repeatedly searched Zendesk for new tickets without an analyzed marker across several support mailboxes, extracted and enriched ticket context with requester custom fields, inspected full comment threads for ambiguous or repeated cases, and posted private internal AI triage notes with tags.

89. **Audit inbound email and HubSpot marketing/automation assets to understand an external funnel, compare it with existing marketing emails and workflows, and inspect meeting-booking setup.**

   - Tools: `GOOGLESUPER_FETCH_EMAILS`, `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUB_SPOT_ACCOUNT`, `HUBSPOT_GET_ALL_WORKFLOWS`, `HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL`, `HUBSPOT_GET_WORKFLOWS`
   - Description: The workflow searched Gmail for emails from a specific sender domain across multiple connected Google accounts, first collecting metadata and then fetching full bodies for a narrower email window.

90. **Create and refine a Google Slides presentation by inspecting existing slides and layouts, adding styled slides, inserting an image, and verifying the rendered result.**

   - Tools: `GOOGLEDRIVE_UPLOAD_FILE`, `GOOGLESLIDES_GET_PAGE_THUMBNAIL2`, `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE`, `GOOGLESLIDES_PRESENTATIONS_GET`, `GOOGLESLIDES_PRESENTATIONS_PAGES_GET`
   - Description: The workflow read an existing Google Slides deck and prior deck examples, extracted layout and styling information, created several new styled slides with raw batch updates, recovered from batch-update validation errors, verified results with thumbnails, attempted but did not complete a Drive-based image upload, then…

91. **Manage Meta ads reporting and campaign status, and handle Facebook Page inbox workflows including reading conversations and sending private replies or bulk follow-up messages.**

   - Tools: `FACEBOOK_GET_CONVERSATION_MESSAGES`, `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_PAGE_DETAILS`, `FACEBOOK_LIST_MANAGED_PAGES`, `FACEBOOK_SEND_MESSAGE`, `METAADS_GET_INSIGHTS`, `METAADS_GET_OBJECT`
   - Description: The workflow combined Meta Ads reporting and Facebook Page inbox operations.

92. **Migrate active Todoist projects, sections, tasks, subtasks, labels, due dates, priorities, durations, and assignment metadata into a private ClickUp Space, then verify the migration without modifying Todoist source data.**

   - Tools: `CLICKUP_CREATE_FOLDER`, `CLICKUP_CREATE_LIST`, `CLICKUP_CREATE_SPACE`, `CLICKUP_CREATE_SPACE_TAG`, `CLICKUP_CREATE_TASK`, `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES`, `CLICKUP_GET_FILTERED_TEAM_TASKS`, `CLICKUP_GET_FOLDERS`, `CLICKUP_GET_LISTS`, `CLICKUP_GET_SPACE`, `CLICKUP_GET_SPACES`, `CLICKUP_GET_SPACE_TAGS`, `CLICKUP_GET_TASK`, `CLICKUP_UPDATE_SPACE`, `CLICKUP_UPDATE_TASK`, `CLICKUP_UPDATE_WORKSPACE_ACL`, `TODOIST_GET_ALL_PROJECTS`, `TODOIST_GET_ALL_TASKS`, `TODOIST_LIST_SECTIONS`
   - Description: The workflow read active Todoist tasks, projects, and sections with pagination, then created a dedicated private ClickUp Space.

93. **Analyze Salesforce CRM data by discovering schema, running SOQL queries, extracting a large set of related records, and computing a cohort-based return-rate metric.**

   - Tools: `SALESFORCE_GET_ALL_CUSTOM_OBJECTS`, `SALESFORCE_RUN_SOQL_QUERY`
   - Description: The workflow began with Salesforce schema discovery, then used SOQL to profile stages, custom objects, field behavior, and record relationships.

94. **Audit and optimize a Meta Ads account: retrieve account, campaign, ad set, ad, creative, performance, targeting, and pixel data; then apply confirmed optimization changes including pausing objects, changing ad set targeting, reactivating a campaign, creating custom audiences, and adding exclusions.**

   - Tools: `METAADS_GET_AD_ACCOUNTS`, `METAADS_GET_INSIGHTS`, `METAADS_GET_OBJECT`, `METAADS_LIST_ADS`, `METAADS_LIST_AD_CREATIVES`, `METAADS_PROXY_EXECUTE`, `METAADS_READ_ADSETS`, `METAADS_UPDATE_CAMPAIGN`
   - Description: The workflow began as a Meta Ads audit: account, campaign, ad set, ad, creative, performance, and breakdown data were fetched and normalized.

95. **Fetch Zoho Books bank accounts and bank transactions, then handle uncategorized bank-feed transactions for reconciliation.**

   - Tools: `ZOHO_BOOKS_CATEGORIZE_UNCATEGORIZED_TRANSACTION`, `ZOHO_BOOKS_LIST_BANK_ACCOUNTS`, `ZOHO_BOOKS_LIST_BANK_TRANSACTIONS`, `ZOHO_BOOKS_LIST_ORGANIZATIONS`
   - Description: The workflow began by discovering Zoho Books tools for listing bank accounts and bank transactions.

96. **Implement several sequential feature-track boundaries in a GitHub repository, commit each boundary separately, run smoke tests after each commit, then verify the final branch head and check-run status.**

   - Tools: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_GET_A_COMMIT`, `GITHUB_GET_A_TREE`, `GITHUB_GET_RAW_REPOSITORY_CONTENT`, `GITHUB_LIST_CHECK_RUNS_FOR_A_REF`
   - Description: The workflow used GitHub tools to inspect a repository branch, fetch relevant source, test, and planning content, implement several dependent feature-track boundaries, run smoke tests in a sandbox, and commit each boundary separately.

97. **Manage Pipedrive CRM records: find deals and contacts, update deal participants and primary contacts, log notes and activities, schedule follow-ups, inspect deal and organization custom fields, and bulk reclassify deals across pipeline stages based on contract timing data.**

   - Tools: `PIPEDRIVE_ADD_AN_ACTIVITY`, `PIPEDRIVE_ADD_DEAL_PARTICIPANT`, `PIPEDRIVE_ADD_NOTE`, `PIPEDRIVE_GET_ALL_DEAL_FIELDS`, `PIPEDRIVE_GET_ALL_ORGANIZATIONS`, `PIPEDRIVE_GET_ALL_ORGANIZATION_FIELDS`, `PIPEDRIVE_GET_ALL_PIPELINES`, `PIPEDRIVE_GET_ALL_STAGES`, `PIPEDRIVE_GET_DEAL`, `PIPEDRIVE_GET_DEALS_IN_A_PIPELINE`, `PIPEDRIVE_GET_DEALS_IN_A_STAGE`, `PIPEDRIVE_GET_DETAILS_OF_AN_ORGANIZATION`, `PIPEDRIVE_LIST_DEAL_ACTIVITIES`, `PIPEDRIVE_LIST_PARTICIPANTS_OF_A_DEAL`, `PIPEDRIVE_SEARCH_DEALS`, `PIPEDRIVE_SEARCH_PERSONS`, `PIPEDRIVE_UPDATE_AN_ORGANIZATION`, `PIPEDRIVE_UPDATE_DEAL`, `PIPEDRIVE_UPDATE_ORGANIZATION`
   - Description: The workflow used Pipedrive to locate relevant deals and people, add a person as a deal participant, update a deal’s primary contact, record email outreach as notes and activities, and create future follow-up reminders.

98. **Analyze owned social media, paid ads, and website attribution performance across YouTube, Instagram, Facebook Page, Meta Ads, and GA4 for a recent multi-month reporting window.**

   - Tools: `FACEBOOK_LIST_MANAGED_PAGES`, `GOOGLE_ANALYTICS_RUN_PIVOT_REPORT`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_GET_USER_INFO`, `INSTAGRAM_GET_USER_INSIGHTS`, `METAADS_GET_AD_ACCOUNTS`, `METAADS_GET_INSIGHTS`, `YOUTUBE_GET_CHANNEL_STATISTICS`, `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, `YOUTUBE_LIST_CHANNEL_VIDEOS`
   - Description: The workflow attempted a cross-platform performance audit.

99. **Maintain and review a Notion-based project task page and append-only log for a technical project, including reading state, posting review/decision rows, updating task-page checklists, and inspecting a Supabase schema to support implementation decisions.**

   - Tools: `NOTION_ADD_MULTIPLE_PAGE_CONTENT`, `NOTION_DELETE_BLOCK`, `NOTION_FETCH_ALL_BLOCK_CONTENTS`, `NOTION_FETCH_BLOCK_CONTENTS`, `NOTION_FETCH_BLOCK_METADATA`, `NOTION_FETCH_DATABASE`, `NOTION_FETCH_ROW`, `NOTION_GET_PAGE_MARKDOWN`, `NOTION_INSERT_ROW_DATABASE`, `NOTION_PROXY_EXECUTE`, `NOTION_QUERY_DATABASE`, `NOTION_QUERY_DATABASE_WITH_FILTER`, `NOTION_RETRIEVE_PAGE`, `NOTION_SEARCH_NOTION_PAGE`, `NOTION_UPDATE_BLOCK`, `NOTION_UPDATE_PAGE`, `NOTION_UPDATE_ROW_DATABASE`, `NOTION_UPSERT_ROW_DATABASE`, `SUPABASE_LIST_TABLES`, `SUPABASE_RUN_READ_ONLY_QUERY`
   - Description: The agent used Notion extensively to read a technical project task page, inspect and update a project log database, create many review/decision rows, restructure task-page checklist blocks, and verify final rendering.

100. **Extract CRM list-entry records from Attio, join them with Attio company domains, and prepare a domain-to-owner mapping for downstream processing.**

   - Tools: `ATTIO_POST_V2_LISTS_LIST_ENTRIES_QUERY`, `ATTIO_QUERY_RECORDS`
   - Description: The workflow searched for Attio tools, attempted to bulk fetch list entries and company records, and initially hit remote execution helper and memory-processing failures.
