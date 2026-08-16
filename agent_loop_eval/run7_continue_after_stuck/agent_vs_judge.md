# Agent believed it worked, judge disagreed — `run7_continue_after_stuck`

Each row is a tool the agent ran **while stating it was carrying out a specific step**,
where an independent judge then ruled that capability was never delivered. Recall cannot
see these: the agent records success and later steps proceed on a false premise.

The agent's stated purpose is matched to the capability semantically, one call per
capability. A capability no call was aimed at is a plain miss, not a disagreement, and is
counted in `failure_analysis.md` instead.

**7 cases.**

### Task 1

- Agent ran **`HUBSPOT_CREATE_FEEDBACK_SUBMISSION`** (mock-rejected)
  - agent's stated purpose: *"Assess payment-link feasibility and capabilities in HubSpot"*
  - capability the judge ruled unmet: **Assess payment-link feasibility**
  - matched because: The agent explicitly stated the purpose of the first tool call was to assess payment-link feasibility and capabilities in HubSpot.
  - judge: None of the returned HubSpot tools provide the capability to assess payment-link feasibility.

### Task 16

- Agent ran **`VERCEL_GET_DEPLOYMENTS`** (mocked)
  - agent's stated purpose: *"Get Vercel deployments"*
  - capability the judge ruled unmet: **Investigate hosting and deployment state via Cloudflare zones and DNS**
  - would have accepted: `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - matched because: The agent called Vercel deployments to investigate the hosting and deployment state.
  - judge: None of the returned Cloudflare or other tools provide the capability to list Cloudflare zones and DNS records required to investigate hosting and deployment state via Cloudflare.

### Task 17

- Agent ran **`GEMINI_GENERATE_IMAGE`** (mock-rejected)
  - agent's stated purpose: *"image"*
  - capability the judge ruled unmet: **Prepare and upload supporting media**
  - would have accepted: `HEYGEN_UPLOAD_ASSET`
  - matched because: The agent called GEMINI_GENERATE_IMAGE with the stated purpose 'image', which represents its attempt to prepare supporting media.
  - judge: None of the returned HeyGen tools provide the capability to prepare and upload supporting media.
- Agent ran **`LINKEDIN_CREATE_LINKED_IN_POST`** (mock-rejected)
  - agent's stated purpose: *"social"*
  - capability the judge ruled unmet: **Publish content to social media**
  - would have accepted: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - matched because: The agent called the LinkedIn create post tool with the stated purpose 'social', which matches the capability to publish content to social media.
  - judge: None of the returned tools provide the capability to publish content to social media.
- Agent ran **`GOOGLECALENDAR_CREATE_EVENT`** (mock-rejected)
  - agent's stated purpose: *"calendar"*
  - capability the judge ruled unmet: **Read and update a booking schedule**
  - would have accepted: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - matched because: The agent used the Google Calendar tool with the purpose 'calendar', which represents its attempt to read and update the booking schedule capability.
  - judge: Although Cal.com tools like CAL_POST_NEW_BOOKING_REQUEST and CAL_RESCHEDULE_BOOKING_BY_UID were returned, there were no Google Sheets tools provided to read and update a spreadsheet-based booking schedule as required by the task.

### Task 18

- Agent ran **`COMPOSIO_SEARCH_WEB`** (mocked)
  - agent's stated purpose: *"Search for remote or hybrid contract data engineering job listings"*
  - capability the judge ruled unmet: **Search and extract recent job listings from web sources or job boards**
  - would have accepted: `BROWSER_TOOL_CREATE_TASK`
  - matched because: The agent explicitly stated its purpose was to search for remote or hybrid contract data engineering job listings.
  - judge: None of the available search or fetch tools are capable of directly searching, parsing, and extracting structured job listings from job boards as required by the task.

### Task 19

- Agent ran **`NOTION_SEARCH_NOTION_PAGE`** (real)
  - agent's stated purpose: *"Search Notion for resume documents or candidate information"*
  - capability the judge ruled unmet: **Retrieve, create, or manage resume documents stored in Google Docs or Google Drive**
  - would have accepted: `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`, `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`, `GOOGLEDRIVE_DOWNLOAD_FILE`, `GOOGLEDRIVE_FIND_FILE`, `GOOGLEDRIVE_UPLOAD_FROM_URL`
  - matched because: The agent searched Notion for resume documents, which corresponds to retrieving or managing resume documents even though Google Docs or Drive was ultimately not used.
  - judge: None of the returned tools provide the capability to retrieve, create, or manage resume documents stored in Google Docs or Google Drive.

