# Search failures

Two kinds. The first is search not returning a tool that exists. The second is search
answering a query that named one application with a different application's tool, promoted
as the primary recommendation.

---

# Part 1 — search did not return the tool

## Task 16 — Audit analytics and search performance for a website, inspect and modify its source repository, create pull requests with SEO, tracking, caching, routing, and accessibility fixes, and investigate hosting/deployment state.

**Capability:** Modify repository code and create pull requests

Tools the agent needed: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`

Queries that failed to return them:

1. `Git repository file inspect and commit or pull request`
   - returned: `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_COMMITS`
2. `submit code changes for review`
   - returned: `GITHUB_SUBMIT_A_REVIEW_FOR_A_PULL_REQUEST`, `GITHUB_CREATE_A_REVIEW_FOR_A_PULL_REQUEST`
3. `check in code to version control`
   - returned: `SHARE_POINT_CHECK_IN_FILE`, `ONE_DRIVE_CHECKIN_ITEM`
4. `record file edits in version control`
   - returned: `GITHUB_LIST_COMMITS`, `GITHUB_LIST_REPOSITORY_CONTRIBUTORS`

## Task 18 — Find recent remote or hybrid contract data-engineering-related job listings in a target region, validate/extract job details from job boards, compile a curated digest, and email it to someone.

**Capability:** Search and extract recent job listings from web sources or job boards

Tools the agent needed: `BROWSER_TOOL_CREATE_TASK`

Queries that failed to return them:

1. `Search job listings or job boards for remote hybrid contract data engineering jobs`
   - returned: `COMPOSIO_SEARCH_WEB`
2. `extract job listings from job boards`
   - returned: `COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
3. `scrape listings from a website`
   - returned: `HYPERBROWSER_START_EXTRACT_JOB`, `HYPERBROWSER_GET_EXTRACT_JOB_STATUS`, `HYPERBROWSER_GET_EXTRACT_JOB_RESULT`
4. `open a web page and read its contents`
   - returned: `COMPOSIO_SEARCH_FETCH_URL_CONTENT`

## Task 28 — Analyze recent Instagram Reel performance, generate a new short-form branded video with AI video and voice tools, publish it as an Instagram Reel, verify the post, and attempt to archive the final asset in a repository.

**Capability:** Generate AI text-to-speech audio for the video voiceover

Tools the agent needed: `ELEVENLABS_TEXT_TO_SPEECH`

Queries that failed to return them:

1. `Generate AI video or text to speech voice`
   - returned: `GEMINI_GENERATE_VIDEOS`
2. `AI voice narration for a video`
   - returned: `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`
3. `create an audio narration track`
   - returned: `ELEVENREADER_CREATE_AUDIO_NATIVE_PROJECT`, `ELEVENREADER_UPDATE_AUDIO_NATIVE_PROJECT_CONTENT`
4. `voice synthesis for a video`
   - returned: `HEYGEN_GENERATE_TEXT_TO_SPEECH`, `HEYGEN_GENERATE_VOICE_AUDIO_PREVIEW`, `HEYGEN_LIST_TTS_VOICES`, `HEYGEN_V2_VOICES`

## Task 72 — Build, repair, deploy, configure, and test a Vercel-hosted GitHub-backed API proxy for Gemini text, image, video, embeddings, model listing, OpenAI-compatible paths, and tool-call-style outputs.

**Capability:** Configure project environment variables on Vercel

Tools the agent needed: `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`, `VERCEL_GET_PROJECT_ENV`

Queries that failed to return them:

1. `deploy or manage vercel project`
   - returned: `VERCEL_CREATE_NEW_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENT`
2. `vercel project settings`
   - returned: `VERCEL_GET_PROJECT`, `VERCEL_UPDATE_PROJECT`
3. `manage vercel project configuration`
   - returned: `VERCEL_GET_PROJECTS`, `VERCEL_GET_DEPLOYMENTS`
4. `store deployment secrets`
   - returned: `DOPPLER_SECRETS_UPDATE`, `DOPPLER_SECRETS_DOWNLOAD`

---

# Part 2 — search answered with a different application

In each case the query named an application and search promoted another application's tool
as its primary result. What the agent did next differs, and is stated per case.

## Task 1 — Prepare HubSpot launch assets for a paid event registration flow: assess payment-link feasibility, create a review-only automated confirmation email, create a disabled confirmation workflow, verify the assets remain inert, and attempt to create a custom-object registration ledger.

**Query:** `Create or check payment link in HubSpot`

**Returned:** `STRIPE_CREATE_PAYMENT_LINK`

**The agent then ran** `STRIPE_CREATE_PAYMENT_LINK`, stating it was for: *"Assess payment link feasibility by attempting to create a Stripe payment link"*

**Outcome:** **Reported the task COMPLETE, with nothing unmet** — while two capabilities (assess payment-link feasibility, verify assets remain inert) were in fact never delivered. The evaluation catches this nowhere: recall calls them catalogue gaps, completion calls the task done.

**Why this is still a search failure:** HubSpot has no payment or link tool in the catalogue at all, so search could not have returned one. The failure is that it promoted a Stripe tool to `primary` for a query that said *in HubSpot*, instead of signalling that the named application had nothing. That silent substitution is what let the agent believe it had assessed HubSpot.

## Task 24 — Build a recurring job-search digest by finding relevant LinkedIn job listings and sending the result or status update via Gmail.

**Query:** `Search LinkedIn job listings`

**Returned:** `COMPOSIO_SEARCH_WEB`

**The agent then ran** `COMPOSIO_SEARCH_WEB`, stating it was for: *"Search for relevant LinkedIn job listings using Exa web search"*

**Outcome:** Reported the task complete. Group scoring found no unmet capability here, so this is the weakest of the three — the substitution may well have been adequate.

**Why this is still a search failure:** LinkedIn has no job-listing tool in the catalogue, so again search had nothing to return. It answered a LinkedIn-scoped query with a generic web search promoted to `primary`, and the agent recorded the result as LinkedIn listings.

## Task 57 — Create short dog-themed videos, analyze channel and trend performance, upload and manage YouTube Shorts, and inspect Instagram posting context.

**Query:** `create short video dog themed YouTube Shorts`

**Returned:** `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`

**The agent then ran** `GEMINI_GENERATE_VIDEOS`, stating it was for: *"Generate a short dog-themed video using Gemini Veo"*

**Outcome:** **Reported the task NOT complete** and listed the step as unmet. The agent was honest here, so this is a search observation rather than a silent failure.

**Why this is still a search failure:** The query named YouTube; search returned Gemini video generation. Defensible in part — the step really was video creation — but YouTube upload tools do exist (`YOUTUBE_MULTIPART_UPLOAD_VIDEO`) and none was surfaced for a query naming YouTube.
