# Agent believed it worked, judge disagreed — `run8_full_100tasks`

Each case is a tool the agent ran **while stating it was carrying out a specific step**,
where an independent judge ruled that capability was never delivered. Recall cannot see
these: the agent records success and later steps proceed on a false premise.

**17 cases — 6 the agent's fault, 11 search's.**

The split is the useful part. If a tool that would have worked was sitting in the results
the agent had already seen, it chose badly. If no such tool was ever returned, the agent
had no option and the failure is search's.

## Agent selection errors — a correct tool was available and not chosen

**Task 13 — Audit website search performance and indexing**

- agent ran `GOOGLESUPER_GET_METADATA` (mock-rejected), stating: *"Attempt to check GA4 metadata or run report to audit website traffic and search performance"*
- should have used: `GOOGLESUPER_RUN_REPORT`
- why: The list includes Google Search Console tools (prefixed with GOOGLESUPER), and GOOGLESUPER_RUN_REPORT or GOOGLESUPER_BATCH_RUN_REPORTS can be used to audit website search performance and indexing data.
- judge: The returned tools only provide Google Analytics (GA4) and Gmail functionalities, but none of them support auditing website search performance and indexing like Google Search Console.

**Task 17 — Attempt social media publishing on Instagram**

- agent ran `UPLOAD_POST_LIST_PROFILES` (mocked), stating: *"List Upload-Post profiles for social publishing"*
- should have used: `UPLOAD_POST_PUBLISH_POST`
- why: The UPLOAD_POST_PUBLISH_POST tool provides the necessary capability to publish posts on platforms like Instagram from the same upload service family.
- judge: None of the returned tools provide the specific capability to publish social media posts to Instagram.

**Task 17 — Read and update the booking schedule**

- agent ran `GOOGLECALENDAR_FIND_EVENT` (real), stating: *"Search calendar events to read booking schedule"*
- should have used: `GOOGLECALENDAR_PATCH_EVENT`
- why: The list contains Google Calendar tools like GOOGLECALENDAR_PATCH_EVENT and GOOGLECALENDAR_EVENTS_LIST that allow reading and updating booking schedules.
- judge: The available tools only cover Google Calendar management rather than the required Google Sheets booking schedule read and update capabilities.

**Task 52 — Inspect existing Zep context, user nodes, and graph structure**

- agent ran `ZEP_GET_USER_SESSIONS` (mocked), stating: *"Inspect existing Zep sessions for user"*
- should have used: `ZEP_GET_THREAD_USER_CONTEXT`
- why: ZEP_GET_THREAD_USER_CONTEXT is available in the list and provides the capability to inspect user context, nodes, and graph structure.
- judge: None of the returned Zep tools provide the capability to directly inspect existing user nodes and graph structure as specified by the missing ZEP_GET_USER_NODE capability.

**Task 64 — Gather marketing performance data from advertising platforms**

- agent ran `METAADS_GET_AD_ACCOUNTS` (mocked), stating: *"List accessible Meta ad accounts to gather marketing performance data"*
- should have used: `LINKEDIN_ADS_GET_AD_ANALYTICS`
- why: The LinkedIn Ads tool for getting ad analytics provides the necessary capability to gather marketing performance data from advertising platforms.
- judge: None of the returned tools provide the ability to gather marketing performance data from advertising platforms like Google Ads.

**Task 64 — Gather web analytics and traffic performance data**

- agent ran `METAADS_GET_AD_ACCOUNTS` (mocked), stating: *"List accessible Meta ad accounts to gather marketing performance data"*
- should have used: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`
- why: The Google Search Console search analytics query tool directly provides web analytics and traffic performance data from Google Search.
- judge: None of the returned tools provide Google Analytics website traffic and web analytics performance reporting.

## Search left the agent no option — nothing returned could do it

**Task 1 — Assess payment link feasibility**

- agent ran `STRIPE_CREATE_PAYMENT_LINK` (mocked), stating: *"Assess payment link feasibility by attempting to create a Stripe payment link"*
- would have needed: _(nothing listed)_
- why: None of the listed tools provide the capability to assess payment link feasibility for Stripe.
- judge: No available tool assesses the feasibility of a payment link in HubSpot.

**Task 1 — Verify assets remain inert**

- agent ran `HUBSPOT_GET_WORKFLOWS` (mocked), stating: *"Retrieve workflows to verify asset status and inertness"*
- would have needed: _(nothing listed)_
- why: None of the tools listed in the search results provide the capability to verify that assets remain inert.
- judge: None of the returned tools provide the capability to verify that HubSpot assets remain inert.

**Task 7 — Fetch and read email messages and threads**

- agent ran `GMAIL_GET_PROFILE` (real), stating: *"Fetch Gmail profile to check account availability and productivity signals"*
- would have needed: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
- why: Although there are Gmail tools in the list, none of them provide the capability to fetch and read email messages and threads.
- judge: None of the returned Gmail tools provide the capability to fetch and read email messages and threads.

**Task 8 — Mark incomplete archive documents when transcript retrieval fails**

- agent ran `SUPADATA_GET_TRANSCRIPT` (mocked), stating: *"Attempt to retrieve video transcript for knowledge base update"*
- would have needed: _(nothing listed)_
- why: None of the tools listed in the search results provide the capability to mark incomplete archive documents.
- judge: None of the returned tools provide the capability to mark or update incomplete archive documents when transcript retrieval fails.

**Task 13 — Prepare and manage email marketing or contact lists**

- agent ran `GMAIL_GET_CONTACTS` (real), stating: *"Retrieve Gmail contacts to prepare email marketing and outreach lists"*
- would have needed: `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
- why: None of the listed Gmail tools provide the capability to prepare and manage email marketing or contact lists beyond retrieving contacts.
- judge: None of the returned tools provide the capability to create and manage email marketing lists or contact lists.

**Task 16 — Investigate hosting and deployment state via DNS/CDN configuration**

- agent ran `VERCEL_GET_DEPLOYMENTS` (mocked), stating: *"List Vercel deployments to check hosting and deployment state"*
- would have needed: `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
- why: None of the provided tools offer DNS or CDN configuration investigation capabilities for Vercel.
- judge: None of the returned Vercel or GitHub tools provide the ability to inspect DNS or CDN configuration for hosting and deployment state.

**Task 18 — Search and extract recent job listings from web sources or job boards**

- agent ran `COMPOSIO_SEARCH_WEB` (mock-rejected), stating: *"Search job boards or listings for remote or hybrid contract data-engineering-related jobs in a target region"*
- would have needed: `BROWSER_TOOL_CREATE_TASK`
- why: None of the available tools provide specific job board search capabilities, as COMPOSIO_SEARCH_WEB only performs general web searches.
- judge: None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

**Task 20 — Manage and reconcile files in Google Drive**

- agent ran `GOOGLEDRIVE_FIND_FILE` (mocked), stating: *"Search Google Drive for portal, billing, or project documentation files"*
- would have needed: _(nothing listed)_
- why: None of the available tools provide the capability to manage and reconcile files in Google Drive.
- judge: Although there are tools for finding, getting metadata, and downloading files in Google Drive, there are no tools provided to manage (such as create, update, move, or delete) and reconcile files in Google Drive.

**Task 52 — Retrieve memory data from Mem0**

- agent ran `MEM0_EXPORT_DATA_BASED_ON_FILTERS` (mock-rejected), stating: *"Attempt to export memory data from Mem0"*
- would have needed: `MEM0_GET_MEMORIES_BY_ENTITY`
- why: Although the list contains various Zep memory tools, there is no tool specifically for Mem0 memory retrieval present in the search results.
- judge: None of the returned Mem0 tools provide the capability to retrieve individual memories by entity, as only an export job creation tool was provided.

**Task 72 — Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models**

- agent ran `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` (mocked), stating: *"Create api/index.js with full proxy implementation"*
- would have needed: `GEMINI_GENERATE_CONTENT`, `GEMINI_LIST_MODELS`, `GEMINI_COUNT_TOKENS`
- why: None of the listed tools provide Gemini model interaction, token counting, or text generation capabilities.
- judge: None of the returned tools provide capabilities for interacting with Gemini models, such as generating text, counting tokens, or listing models.

**Task 72 — Generate images using Gemini image models**

- agent ran `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` (mocked), stating: *"Create api/index.js with full proxy implementation"*
- would have needed: `GEMINI_GENERATE_IMAGE`
- why: None of the provided GitHub or Vercel tools offer Gemini image generation capabilities.
- judge: None of the returned tools provide the capability to generate images using Gemini image models.

