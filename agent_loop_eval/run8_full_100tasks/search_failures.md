# Search failures

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
