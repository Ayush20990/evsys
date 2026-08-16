# When the agent thought it had succeeded — `run8_full_100tasks`

The agent states what each tool call is for. These are the calls where it believed it had
carried out a step, and an independent judge found that capability was never delivered.

**Why this matters more than a missed capability.** The agent records the step as done and
carries on, so every later step is built on something that never happened. A recall number
cannot see this at all — the capability simply looks satisfied.

**18 cases: 5 the agent's fault, 13 search's.**

The split turns on one question: was a tool that would have worked already sitting in the
results the agent had seen?

---

## The agent chose badly (5)

A correct tool was in the results it had already been shown, and it picked something else.

#### Task 13 — Audit website search performance and indexing

- **Agent ran:** `GOOGLESUPER_GET_METADATA` (mock-rejected)
- **Saying it was for:** "Attempt to check GA4 metadata or run report to audit website traffic and search performance"
- **Should have used:** `GOOGLESUPER_RUN_REPORT` — it was in the results
- **What went wrong:** The list includes Google Search Console (GOOGLESUPER) reporting tools that can audit website search performance and indexing, specifically GOOGLESUPER_RUN_REPORT.
- **Judge:** The returned tools only provide Google Analytics (GA4) and Gmail functionalities, but none of them support auditing website search performance and indexing like Google Search Console.

#### Task 17 — Attempt social media publishing on Instagram

- **Agent ran:** `UPLOAD_POST_LIST_PROFILES` (mocked)
- **Saying it was for:** "List Upload-Post profiles for social publishing"
- **Should have used:** `UPLOAD_POST_PUBLISH_POST` — it was in the results
- **What went wrong:** The UPLOAD_POST_PUBLISH_POST tool provides the necessary capability to attempt social media publishing using the Upload Post platform.
- **Judge:** None of the returned tools provide the specific capability to publish social media posts to Instagram.

#### Task 17 — Read and update the booking schedule

- **Agent ran:** `GOOGLECALENDAR_FIND_EVENT` (real)
- **Saying it was for:** "Search calendar events to read booking schedule"
- **Should have used:** `GOOGLECALENDAR_PATCH_EVENT` — it was in the results
- **What went wrong:** The list contains Google Calendar tools like GOOGLECALENDAR_PATCH_EVENT and GOOGLECALENDAR_EVENTS_LIST which allow reading and updating booking schedules.
- **Judge:** The available tools only cover Google Calendar management rather than the required Google Sheets booking schedule read and update capabilities.

#### Task 52 — Inspect existing Zep context, user nodes, and graph structure

- **Agent ran:** `ZEP_GET_USER_SESSIONS` (mocked)
- **Saying it was for:** "Inspect existing Zep sessions for user"
- **Should have used:** `ZEP_GET_THREAD_USER_CONTEXT` — it was in the results
- **What went wrong:** The tool ZEP_GET_THREAD_USER_CONTEXT is designed to inspect user context and graph structure for a thread, whereas ZEP_GET_USER_SESSIONS only retrieves session lists.
- **Judge:** None of the returned Zep tools provide the capability to directly inspect existing user nodes and graph structure as specified by the missing ZEP_GET_USER_NODE capability.

#### Task 64 — Gather web analytics and traffic performance data

- **Agent ran:** `METAADS_GET_AD_ACCOUNTS` (mocked)
- **Saying it was for:** "List accessible Meta ad accounts to gather marketing performance data"
- **Should have used:** `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` — it was in the results
- **What went wrong:** The Google Search Console tool provides web analytics and search traffic performance data directly related to website performance.
- **Judge:** None of the returned tools provide Google Analytics website traffic and web analytics performance reporting.

## Search left it no option (13)

Nothing search had returned could do the job, so the agent substituted the closest thing
it had. These are search failures wearing an agent-error costume.

#### Task 1 — Assess payment link feasibility

- **Agent ran:** `STRIPE_CREATE_PAYMENT_LINK` (mocked)
- **Saying it was for:** "Assess payment link feasibility by attempting to create a Stripe payment link"
- **Would have needed:** _(nothing listed)_
- **What went wrong:** None of the listed Stripe or HubSpot tools assess the feasibility of a payment link.
- **Judge:** No available tool assesses the feasibility of a payment link in HubSpot.

#### Task 1 — Verify assets remain inert

- **Agent ran:** `HUBSPOT_GET_WORKFLOWS` (mocked)
- **Saying it was for:** "Retrieve workflows to verify asset status and inertness"
- **Would have needed:** _(nothing listed)_
- **What went wrong:** None of the tools listed in the search results provide the capability to verify that assets remain inert.
- **Judge:** None of the returned tools provide the capability to verify that HubSpot assets remain inert.

#### Task 7 — Fetch and read email messages and threads

- **Agent ran:** `GMAIL_GET_PROFILE` (real)
- **Saying it was for:** "Fetch Gmail profile to check account availability and productivity signals"
- **Would have needed:** `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
- **What went wrong:** No tool for fetching or reading email messages and threads from Gmail was present in the provided list.
- **Judge:** None of the returned Gmail tools provide the capability to fetch and read email messages and threads.

#### Task 8 — Mark incomplete archive documents when transcript retrieval fails

- **Agent ran:** `SUPADATA_GET_TRANSCRIPT` (mocked)
- **Saying it was for:** "Attempt to retrieve video transcript for knowledge base update"
- **Would have needed:** _(nothing listed)_
- **What went wrong:** None of the tools in the provided list offer the capability to mark incomplete archive documents.
- **Judge:** None of the returned tools provide the capability to mark or update incomplete archive documents when transcript retrieval fails.

#### Task 13 — Prepare and manage email marketing or contact lists

- **Agent ran:** `GMAIL_GET_CONTACTS` (real)
- **Saying it was for:** "Retrieve Gmail contacts to prepare email marketing and outreach lists"
- **Would have needed:** `BREVO_CREATE_CONTACT_LIST`, `BREVO_GET_CONTACT_LISTS`
- **What went wrong:** None of the provided tools offer the capability to prepare and manage email marketing or contact lists beyond retrieving individual contacts or people.
- **Judge:** None of the returned tools provide the capability to create and manage email marketing lists or contact lists.

#### Task 16 — Investigate hosting and deployment state via DNS/CDN configuration

- **Agent ran:** `VERCEL_GET_DEPLOYMENTS` (mocked)
- **Saying it was for:** "List Vercel deployments to check hosting and deployment state"
- **Would have needed:** `CLOUDFLARE_LIST_ZONES`, `CLOUDFLARE_LIST_DNS_RECORDS`
- **What went wrong:** None of the available tools provide functionality to investigate DNS or CDN configurations.
- **Judge:** None of the returned Vercel or GitHub tools provide the ability to inspect DNS or CDN configuration for hosting and deployment state.

#### Task 18 — Search and extract recent job listings from web sources or job boards

- **Agent ran:** `COMPOSIO_SEARCH_WEB` (mock-rejected)
- **Saying it was for:** "Search recent remote or hybrid contract data engineering job listings"
- **Would have needed:** `BROWSER_TOOL_CREATE_TASK`
- **What went wrong:** None of the available tools provide specialized job board search or listing extraction capabilities.
- **Judge:** None of the available search tools provide the dedicated browser task automation required to dynamically navigate, extract, and validate live job listings from web-based job boards.

#### Task 20 — Manage and reconcile files in Google Drive

- **Agent ran:** `GOOGLEDRIVE_FIND_FILE` (mocked)
- **Saying it was for:** "Search Google Drive for portal, billing, or project documentation files"
- **Would have needed:** _(nothing listed)_
- **What went wrong:** None of the available tools provide the capability to manage and reconcile files in Google Drive.
- **Judge:** Although there are tools for finding, getting metadata, and downloading files in Google Drive, there are no tools provided to manage (such as create, update, move, or delete) and reconcile files in Google Drive.

#### Task 52 — Retrieve memory data from Mem0

- **Agent ran:** `MEM0_EXPORT_DATA_BASED_ON_FILTERS` (mock-rejected)
- **Saying it was for:** "Attempt to export memory data from Mem0"
- **Would have needed:** `MEM0_GET_MEMORIES_BY_ENTITY`
- **What went wrong:** Although the list contains Mem0 and Zep tools, there is no other Mem0 tool available in the search results that retrieves memory data.
- **Judge:** None of the returned Mem0 tools provide the capability to retrieve individual memories by entity, as only an export job creation tool was provided.

#### Task 64 — Gather marketing performance data from advertising platforms

- **Agent ran:** `METAADS_GET_AD_ACCOUNTS` (mocked)
- **Saying it was for:** "List accessible Meta ad accounts to gather marketing performance data"
- **Would have needed:** `GOOGLEADS_SEARCH_STREAM_GAQL`
- **What went wrong:** Although there are LinkedIn Ads analytics tools in the list, the prompt does not specify LinkedIn and the agent ran a Meta Ads tool, meaning no equivalent Meta Ads performance data tool was available.
- **Judge:** None of the returned tools provide the ability to gather marketing performance data from advertising platforms like Google Ads.

#### Task 72 — Generate text, handle model listing, token counting, and tool-call-style outputs using Gemini models

- **Agent ran:** `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` (mocked)
- **Saying it was for:** "Create api/index.js with full proxy implementation"
- **Would have needed:** `GEMINI_GENERATE_CONTENT`, `GEMINI_LIST_MODELS`, `GEMINI_COUNT_TOKENS`
- **What went wrong:** None of the provided tools offer Gemini model interaction, text generation, token counting, or model listing capabilities.
- **Judge:** None of the returned tools provide capabilities for interacting with Gemini models, such as generating text, counting tokens, or listing models.

#### Task 72 — Generate images using Gemini image models

- **Agent ran:** `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` (mocked)
- **Saying it was for:** "Create api/index.js with full proxy implementation"
- **Would have needed:** `GEMINI_GENERATE_IMAGE`
- **What went wrong:** None of the tools provided in the search results offer image generation capabilities using Gemini models.
- **Judge:** None of the returned tools provide the capability to generate images using Gemini image models.

#### Task 72 — Generate text embeddings using Gemini models

- **Agent ran:** `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` (mocked)
- **Saying it was for:** "Create api/index.js with full proxy implementation"
- **Would have needed:** `GEMINI_EMBED_CONTENT`
- **What went wrong:** None of the tools listed provide functionality for generating text embeddings using Gemini models.
- **Judge:** None of the returned GitHub or Vercel tools provide the capability to generate text embeddings using Gemini models.

