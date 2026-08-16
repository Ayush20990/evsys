# Agent believed it worked, judge disagreed — `run8_full_100tasks`

Each row is a tool the agent ran **while stating it was carrying out a specific step**,
where an independent judge then ruled that capability was never delivered. Recall cannot
see these: the agent records success and later steps proceed on a false premise.

The agent's stated purpose is matched to the capability semantically, one call per
capability. A capability no call was aimed at is a plain miss, not a disagreement, and is
counted in `failure_analysis.md` instead.

**18 cases.**

### Task 1

- Agent ran **`STRIPE_CREATE_PAYMENT_LINK`** (mocked)
  - agent's stated purpose: *"Assess payment link feasibility by attempting to create a Stripe payment link"*
  - capability the judge ruled unmet: **Assess payment link feasibility**
  - matched because: The agent explicitly stated its purpose for tool call 2 was to assess payment link feasibility by attempting to create a Stripe payment link.
  - judge: No available tool assesses the feasibility of a payment link in HubSpot.
- Agent ran **`HUBSPOT_GET_WORKFLOWS`** (mocked)
  - agent's stated purpose: *"Retrieve workflows to verify asset status and inertness"*
  - capability the judge ruled unmet: **Verify assets remain inert**
  - matched because: The agent explicitly stated its purpose for tool call 5 was to retrieve workflows to verify asset status and inertness.
  - judge: None of the returned tools provide the capability to verify that HubSpot assets remain inert.

### Task 7

- Agent ran **`GMAIL_GET_PROFILE`** (real)
  - agent's stated purpose: *"Fetch Gmail profile to check account availability and productivity signals"*
  - capability the judge ruled unmet: **Fetch and read email messages and threads**
  - would have accepted: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
  - matched because: The agent used GMAIL_GET_PROFILE with the purpose of checking account availability and productivity signals, which served as its attempt to interact with email services.
  - judge: None of the returned Gmail tools provide the capability to fetch and read email messages and threads.

### Task 8

- Agent ran **`SUPADATA_GET_TRANSCRIPT`** (mocked)
  - agent's stated purpose: *"Attempt to retrieve video transcript for knowledge base update"*
  - capability the judge ruled unmet: **Mark incomplete archive documents when transcript retrieval fails**
  - matched because: Tool call 3 was used to attempt transcript retrieval, which directly aligns with the condition for marking incomplete archive documents when that retrieval fails.
  - judge: None of the returned tools provide the capability to mark or update incomplete archive documents when transcript retrieval fails.

### Task 13

- Agent ran **`GOOGLESUPER_GET_METADATA`** (mock-rejected)
  - agent's stated purpose: *"Attempt to check GA4 metadata or run report to audit website traffic and search performance"*
  - capability the judge ruled unmet: **Audit website search performance and indexing**
  - would have accepted: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITE`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`
  - matched because: The agent explicitly stated its purpose for the first call was to audit website traffic and search performance.
  - judge: The returned tools only provide Google Analytics (GA4) and Gmail functionalities, but none of them support auditing website search performance and indexing like Google Search Console.
- Agent ran **`GMAIL_GET_CONTACTS`** (real)
  - agent's stated purpose: *"Retrieve Gmail contacts to prepare email marketing and outreach lists"*
  - capability the judge ruled unmet: **Prepare and manage email marketing or contact lists**
  - would have accepted: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
  - matched because: The agent explicitly stated its purpose for tool call 3 was to retrieve Gmail contacts in order to prepare email marketing and outreach lists.
  - judge: None of the returned tools provide the capability to create and manage email marketing lists or contact lists.

### Task 16

- Agent ran **`VERCEL_GET_DEPLOYMENTS`** (mocked)
  - agent's stated purpose: *"List Vercel deployments to check hosting and deployment state"*
  - capability the judge ruled unmet: **Investigate hosting and deployment state via DNS/CDN configuration**
  - would have accepted: `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
  - matched because: The agent explicitly stated its purpose for running the VERCEL_GET_DEPLOYMENTS tool was to check the hosting and deployment state.
  - judge: None of the returned Vercel or GitHub tools provide the ability to inspect DNS or CDN configuration for hosting and deployment state.

### Task 17

- Agent ran **`UPLOAD_POST_LIST_PROFILES`** (mocked)
  - agent's stated purpose: *"List Upload-Post profiles for social publishing"*
  - capability the judge ruled unmet: **Attempt social media publishing on Instagram**
  - would have accepted: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
  - matched because: The agent listed Upload-Post profiles with the stated purpose of social publishing, which corresponds to the attempt at publishing on Instagram.
  - judge: None of the returned tools provide the specific capability to publish social media posts to Instagram.
- Agent ran **`GOOGLECALENDAR_FIND_EVENT`** (real)
  - agent's stated purpose: *"Search calendar events to read booking schedule"*
  - capability the judge ruled unmet: **Read and update the booking schedule**
  - would have accepted: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND`
  - matched because: The agent explicitly stated the purpose of tool call 6 was to search calendar events to read the booking schedule.
  - judge: The available tools only cover Google Calendar management rather than the required Google Sheets booking schedule read and update capabilities.

### Task 18

- Agent ran **`COMPOSIO_SEARCH_WEB`** (mock-rejected)
  - agent's stated purpose: *"Search job boards or listings for remote or hybrid contract data-engineering-related jobs in a target region"*
  - capability the judge ruled unmet: **Search and extract recent job listings from web sources or job boards**
  - would have accepted: `BROWSER_TOOL_CREATE_TASK`
  - matched because: The agent explicitly stated its purpose was to search job boards or listings for remote or hybrid contract data-engineering-related jobs in a target region.
  - judge: None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

### Task 20

- Agent ran **`GOOGLEDRIVE_FIND_FILE`** (mocked)
  - agent's stated purpose: *"Search Google Drive for portal, billing, or project documentation files"*
  - capability the judge ruled unmet: **Manage and reconcile files in Google Drive**
  - matched because: Tool call 2 explicitly searched Google Drive to find and reconcile portal, billing, or project documentation files.
  - judge: Although there are tools for finding, getting metadata, and downloading files in Google Drive, there are no tools provided to manage (such as create, update, move, or delete) and reconcile files in Google Drive.

### Task 52

- Agent ran **`MEM0_EXPORT_DATA_BASED_ON_FILTERS`** (mock-rejected)
  - agent's stated purpose: *"Attempt to export memory data from Mem0"*
  - capability the judge ruled unmet: **Retrieve memory data from Mem0**
  - would have accepted: `MEM0_GET_MEMORIES_BY_ENTITY`
  - matched because: The agent explicitly stated its purpose for the first tool call was to attempt to export memory data from Mem0.
  - judge: None of the returned Mem0 tools provide the capability to retrieve individual memories by entity, as only an export job creation tool was provided.
- Agent ran **`ZEP_GET_USER_SESSIONS`** (mocked)
  - agent's stated purpose: *"Inspect existing Zep sessions for user"*
  - capability the judge ruled unmet: **Inspect existing Zep context, user nodes, and graph structure**
  - would have accepted: `ZEP_GET_USER_NODE`
  - matched because: Tool call 3 explicitly stated its purpose was to inspect existing Zep sessions for the user, matching the capability of inspecting existing Zep context.
  - judge: None of the returned Zep tools provide the capability to directly inspect existing user nodes and graph structure as specified by the missing ZEP_GET_USER_NODE capability.

### Task 64

- Agent ran **`METAADS_GET_AD_ACCOUNTS`** (mocked)
  - agent's stated purpose: *"List accessible Meta ad accounts to gather marketing performance data"*
  - capability the judge ruled unmet: **Gather marketing performance data from advertising platforms**
  - would have accepted: `GOOGLEADS_SEARCH_STREAM_GAQL`
  - matched because: The agent explicitly stated its purpose for this call was to list accessible Meta ad accounts in order to gather marketing performance data.
  - judge: None of the returned tools provide the ability to gather marketing performance data from advertising platforms like Google Ads.
- Agent ran **`METAADS_GET_AD_ACCOUNTS`** (mocked)
  - agent's stated purpose: *"List accessible Meta ad accounts to gather marketing performance data"*
  - capability the judge ruled unmet: **Gather web analytics and traffic performance data**
  - would have accepted: `GOOGLE_ANALYTICS_RUN_REPORT`
  - matched because: The agent explicitly stated its purpose for the first tool call was to gather marketing performance data.
  - judge: None of the returned tools provide Google Analytics website traffic and web analytics performance reporting.

### Task 72

- Agent ran **`GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`** (mocked)
  - agent's stated purpose: *"Create api/index.js with full proxy implementation"*
  - capability the judge ruled unmet: **Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models**
  - would have accepted: `GEMINI_GENERATE_CONTENT`, `GEMINI_LIST_MODELS`, `GEMINI_COUNT_TOKENS`
  - matched because: The agent explicitly stated its purpose for this call was to create the full proxy implementation in api/index.js, which covers handling the requested Gemini features.
  - judge: None of the returned tools provide capabilities for interacting with Gemini models, such as generating text, counting tokens, or listing models.
- Agent ran **`GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`** (mocked)
  - agent's stated purpose: *"Create api/index.js with full proxy implementation"*
  - capability the judge ruled unmet: **Generate images using Gemini image models**
  - would have accepted: `GEMINI_GENERATE_IMAGE`
  - matched because: The agent implemented the full proxy in api/index.js, which would have included handling Gemini image generation models as part of the requested API proxy scope.
  - judge: None of the returned tools provide the capability to generate images using Gemini image models.
- Agent ran **`GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`** (mocked)
  - agent's stated purpose: *"Create api/index.js with full proxy implementation"*
  - capability the judge ruled unmet: **Generate text embeddings using Gemini models**
  - would have accepted: `GEMINI_EMBED_CONTENT`
  - matched because: The agent implemented the full proxy in api/index.js, which was its stated attempt to cover all requested API features including text embeddings.
  - judge: None of the returned GitHub or Vercel tools provide the capability to generate text embeddings using Gemini models.

