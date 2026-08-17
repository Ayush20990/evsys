# How often does search miss these four tools?

The four capabilities attributed to search in `failure_analysis.md` failed on the query the
agent actually issued. That was a single attempt each — in run 8 the agent never re-asked
for anything, across all 384 queries — so this probes each one with eight plausible
phrasings to see how reliably the tool can be reached.

Every phrasing is written in the agent's own register: short, action-first, sometimes
naming the application and sometimes not. None contains a tool slug, and none is
deliberately bad.

## 13 of 32 queries failed to return the needed tool

**Both numbers matter.** A list of failing queries with no denominator proves nothing —
anyone can find phrasings that miss. The finding is the *proportion*, and whether any
phrasing works at all.

| Task | Capability | Queries tried | Failed | Ever found? |
|---|---|---:|---:|---|
| 16 | Modify repository code and create pull reque | 8 | **1** | yes |
| 18 | Search and extract recent job listings from  | 8 | **5** | yes |
| 28 | Generate AI text-to-speech audio for the vid | 8 | **2** | yes |
| 72 | Configure project environment variables on V | 8 | **5** | yes |

**Overall: 13/32 = 41% of plausible phrasings fail.**

Each of these tools *is* reachable — every one was returned by at least one phrasing —
so none is invisible to the index. The failure is that reaching it depends heavily on
wording, and the phrasing an agent naturally reaches for often is not the one that works.

---

## Task 16 — Modify repository code and create pull requests

Looking for: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`

**1 of 8 phrasings failed.**

| Query | Result | What came back instead |
|---|---|---|
| `Git repository file inspect and commit or pull request` | **failed** | `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT` |
| `create pull request on github` | found — `GITHUB_CREATE_A_PULL_REQUEST` | `GITHUB_CREATE_A_PULL_REQUEST` |
| `commit code and open pull request` | found — `GITHUB_COMMIT_MULTIPLE_FILES` | `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_COMMIT_MULTIPLE_FILES` |
| `push code changes to repository branch` | found — `GITHUB_COMMIT_MULTIPLE_FILES` | `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_COMMIT_MULTIPLE_FILES` |
| `modify files in a repository` | only in `related` — `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST` | `GITHUB_GET_REPOSITORY_CONTENT` |
| `update source code in github repo` | only in `related` — `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST` | `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` |
| `raise a PR with code changes` | found — `GITHUB_CREATE_A_PULL_REQUEST` | `GITHUB_CREATE_A_PULL_REQUEST` |
| `write changes to a git branch` | only in `related` — `GITHUB_COMMIT_MULTIPLE_FILES` | `GITHUB_CREATE_A_TREE`, `GITHUB_CREATE_A_COMMIT`, `GITHUB_UPDATE_A_REFERENCE` |

## Task 18 — Search and extract recent job listings from web sources or job boards

Looking for: `BROWSER_TOOL_CREATE_TASK`

**5 of 8 phrasings failed.**

| Query | Result | What came back instead |
|---|---|---|
| `Search job listings or job boards for remote hybrid cont` | **failed** | `COMPOSIO_SEARCH_WEB` |
| `extract job listings from job boards` | **failed** | `COMPOSIO_SEARCH_WEB` |
| `scrape listings from a website` | **failed** | `HYPERBROWSER_START_EXTRACT_JOB`, `HYPERBROWSER_GET_EXTRACT_JOB_STATUS`, `HYPERBROWSER_GET_EXTRACT_JOB_RESULT` |
| `browse web pages and collect data` | found — `BROWSER_TOOL_CREATE_TASK` | `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK` |
| `automate a browser session` | found — `BROWSER_TOOL_CREATE_TASK` | `BROWSER_TOOL_CREATE_TASK` |
| `open a web page and read its contents` | **failed** | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |
| `run a headless browser task` | found — `BROWSER_TOOL_CREATE_TASK` | `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK` |
| `crawl a site for structured data` | **failed** | `FIRECRAWL_CRAWL_V2`, `FIRECRAWL_EXTRACT`, `FIRECRAWL_SCRAPE` |

## Task 28 — Generate AI text-to-speech audio for the video voiceover

Looking for: `ELEVENLABS_TEXT_TO_SPEECH`

**2 of 8 phrasings failed.**

| Query | Result | What came back instead |
|---|---|---|
| `Generate AI video or text to speech voice` | **failed** | `GEMINI_GENERATE_VIDEOS` |
| `generate voiceover audio` | found — `ELEVENLABS_TEXT_TO_SPEECH` | `ELEVENLABS_GET_VOICES`, `ELEVENLABS_TEXT_TO_SPEECH` |
| `AI voice narration for a video` | only in `related` — `ELEVENLABS_TEXT_TO_SPEECH` | `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO` |
| `text to speech voice` | found — `ELEVENLABS_TEXT_TO_SPEECH` | `LMNT_SYNTHESIZE_SPEECH`, `ELEVENLABS_GENERATE_A_RANDOM_VOICE`, `ELEVENLABS_TEXT_TO_SPEECH` |
| `synthesize speech from text` | found — `ELEVENLABS_TEXT_TO_SPEECH` | `ELEVENLABS_TEXT_TO_SPEECH`, `ELEVENLABS_GET_VOICES` |
| `create an audio narration track` | **failed** | `OPENAI_CREATE_SPEECH`, `ELEVENREADER_CREATE_AUDIO_NATIVE_PROJECT`, `ELEVENREADER_UPDATE_AUDIO_NATIVE_PROJECT_CONTENT` |
| `turn a script into spoken audio` | found — `ELEVENLABS_TEXT_TO_SPEECH` | `ELEVENLABS_GET_VOICES`, `ELEVENLABS_TEXT_TO_SPEECH` |
| `generate a voice clip for a reel` | found — `ELEVENLABS_TEXT_TO_SPEECH` | `ELEVENLABS_GET_VOICES`, `ELEVENLABS_TEXT_TO_SPEECH` |

## Task 72 — Configure project environment variables on Vercel

Looking for: `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`, `VERCEL_GET_PROJECT_ENV`

**5 of 8 phrasings failed.**

| Query | Result | What came back instead |
|---|---|---|
| `deploy or manage vercel project` | **failed** | `VERCEL_CREATE_NEW_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENT` |
| `vercel project settings` | **failed** | `VERCEL_GET_PROJECT`, `VERCEL_UPDATE_PROJECT` |
| `manage vercel project configuration` | **failed** | `VERCEL_GET_PROJECT2`, `VERCEL_UPDATE_PROJECT2` |
| `vercel project environment` | found — `VERCEL_ADD_ENVIRONMENT_VARIABLE` | `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_CREATE_NEW_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENTS` |
| `set environment variables for a deployment` | only in `related` — `VERCEL_FILTER_PROJECT_ENVS` | `BITBUCKET_GET_DEPLOYMENT_ENVIRONMENT_VARIABLES`, `VERCEL_BATCH_REMOVE_PROJECT_ENV`, `VERCEL_CREATE_PROJECT2` |
| `store deployment secrets` | **failed** | `DOPPLER_SECRETS_UPDATE`, `DOPPLER_SECRETS_DOWNLOAD` |
| `read project config values` | **failed** | `CLICKUP_GET_SPACES` |
| `update env vars on a hosting project` | found — `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_FILTER_PROJECT_ENVS` | `VERCEL_FILTER_PROJECT_ENVS`, `VERCEL_EDIT_PROJECT_ENV`, `VERCEL_ADD_ENVIRONMENT_VARIABLE` |

