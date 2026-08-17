# Would a retry have found it?

The agent never re-asks: across 384 queries in run 8 there was not one near-duplicate.
Every failure in `failure_analysis.md` is therefore a **first-attempt** failure, which
leaves the question that decides what those failures mean — would search have returned the
tool if asked again, better?

Only the cases attributed to **search** are retried here. Retrying the agent-side failures
would prove nothing: those queries never asked for the capability, so naturally a better
query finds it.

Each case gets a fixed ladder of rephrasings, hand-written so every rung tests one thing —
does naming the application help, does naming the exact action help, does near-verbatim
phrasing help.

**4 of 4 were found on a rephrase; 0 were never found
at any phrasing.**

| Task | Capability | Found on retry? | At which rung | As |
|---|---|---|---|---|
| 16 | Modify repository code and create pull request | **yes** | attempt 2 | PRIMARY |
| 18 | Search and extract recent job listings from we | **yes** | attempt 4 | PRIMARY |
| 28 | Generate AI text-to-speech audio for the video | **yes** | attempt 2 | PRIMARY |
| 72 | Configure project environment variables on Ver | **yes** | attempt 4 | PRIMARY |

## What this changes

A capability found on a rephrase is **not** a retrieval defect — search can reach the tool,
the one-shot query just did not. An agent that retried would recover, so the fix belongs in
how the agent queries, not in the index.

A capability never found at any phrasing **is** a retrieval defect, and the strongest kind
of evidence in this whole evaluation: the tool exists, was asked for directly by name and
by action, and still did not come back.

---

## Task 16 — Modify repository code and create pull requests

Looking for: `GITHUB_COMMIT_MULTIPLE_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_MERGE_A_BRANCH`

| Rung | Query | Result |
|---|---|---|
| attempt 1 (the agent's) | `Git repository file inspect and commit or pull request` | not returned |
| attempt 2 | `commit code and open pull request` | **found in primary** — `GITHUB_COMMIT_MULTIPLE_FILES` |
| attempt 3 | `push code changes to repository branch` | **found in primary** — `GITHUB_COMMIT_MULTIPLE_FILES` |
| attempt 4 | `GitHub commit and pull request` | **found in primary** — `GITHUB_CREATE_A_PULL_REQUEST` |

<details><summary>what came back at each rung</summary>

- **attempt 1 (the agent's)** — primary: `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_A_TREE`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_LIST_COMMITS`, `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS`
- **attempt 2** — primary: `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_COMMIT_MULTIPLE_FILES`
- **attempt 3** — primary: `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_COMMIT_MULTIPLE_FILES`
- **attempt 4** — primary: `GITHUB_CREATE_A_PULL_REQUEST`

</details>

## Task 18 — Search and extract recent job listings from web sources or job boards

Looking for: `BROWSER_TOOL_CREATE_TASK`

| Rung | Query | Result |
|---|---|---|
| attempt 1 (the agent's) | `Search job listings or job boards for remote hybrid cont` | not returned |
| attempt 2 | `extract job listings from job boards` | not returned |
| attempt 3 | `scrape listings from a website` | not returned |
| attempt 4 | `browse web pages and collect data` | **found in primary** — `BROWSER_TOOL_CREATE_TASK` |

<details><summary>what came back at each rung</summary>

- **attempt 1 (the agent's)** — primary: `COMPOSIO_SEARCH_WEB`
- **attempt 2** — primary: `COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`
- **attempt 3** — primary: `FIRECRAWL_SCRAPE`, `FIRECRAWL_CRAWL_V2`, `FIRECRAWL_CRAWL_GET`
- **attempt 4** — primary: `BROWSER_TOOL_CREATE_TASK`, `BROWSER_TOOL_WATCH_TASK`

</details>

## Task 28 — Generate AI text-to-speech audio for the video voiceover

Looking for: `ELEVENLABS_TEXT_TO_SPEECH`

| Rung | Query | Result |
|---|---|---|
| attempt 1 (the agent's) | `Generate AI video or text to speech voice` | not returned |
| attempt 2 | `generate voiceover audio` | **found in primary** — `ELEVENLABS_TEXT_TO_SPEECH` |
| attempt 3 | `AI voice narration for a video` | not returned |
| attempt 4 | `text to speech voice` | **found in primary** — `ELEVENLABS_TEXT_TO_SPEECH` |

<details><summary>what came back at each rung</summary>

- **attempt 1 (the agent's)** — primary: `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`
- **attempt 2** — primary: `ELEVENLABS_GET_VOICES`, `ELEVENLABS_TEXT_TO_SPEECH`
- **attempt 3** — primary: `GEMINI_GENERATE_VIDEOS`, `GEMINI_WAIT_FOR_VIDEO`
- **attempt 4** — primary: `ELEVENLABS_TEXT_TO_SPEECH`, `ELEVENLABS_GET_VOICES`

</details>

## Task 72 — Configure project environment variables on Vercel

Looking for: `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_DELETE_PROJECT_ENV`, `VERCEL_FILTER_PROJECT_ENVS`, `VERCEL_GET_PROJECT_ENV`

| Rung | Query | Result |
|---|---|---|
| attempt 1 (the agent's) | `deploy or manage vercel project` | not returned |
| attempt 2 | `vercel project settings` | not returned |
| attempt 3 | `manage vercel project configuration` | not returned |
| attempt 4 | `vercel project environment` | **found in primary** — `VERCEL_ADD_ENVIRONMENT_VARIABLE` |

<details><summary>what came back at each rung</summary>

- **attempt 1 (the agent's)** — primary: `VERCEL_CREATE_NEW_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENT`
- **attempt 2** — primary: `VERCEL_GET_PROJECT`, `VERCEL_UPDATE_PROJECT`
- **attempt 3** — primary: `VERCEL_GET_PROJECT2`, `VERCEL_UPDATE_PROJECT2`
- **attempt 4** — primary: `VERCEL_ADD_ENVIRONMENT_VARIABLE`, `VERCEL_CREATE_NEW_DEPLOYMENT`, `VERCEL_GET_DEPLOYMENTS`

</details>

