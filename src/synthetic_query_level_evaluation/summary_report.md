# Synthetic Query-Level Benchmark

## Method
Tasks are LLM-invented, not drawn from top-100-eval-use-cases.md, but grounded in real tool slugs/descriptions fetched live from Composio for a curated toolkit family (never hallucinated). One Gemini call per task both writes the task text and decomposes it into per-query ground truth, identical in structure and scoring to the primary benchmark.

## Summary
- **Tasks accepted:** 10
- **Generation attempts:** 19
- **Rejected candidate groups:** 9
- **Query-level test cases:** 23
- **Average primary recall:** 80.4%
- **Average retrieval recall:** 80.4%
- **Any-required-tool hit rate:** 82.6%

## Latency
| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 2.59 | 2.59 |
| Median (P50) | 2.55 | 2.55 |
| Maximum | 4.05 | 4.05 |

## Failure Examples
Review alongside the invented task before assigning fault to search; task/query generation may itself be ambiguous.

### synthetic-010-q2 — recall 0.0%
- **Task:** A high-priority client onboarding checklist needs to be set up on our project tracking board, with specific team members assigned to review the documentation. Once the cards are prepped, the onboarding action items, including code repository access steps and required security toggles, must be appended directly into our central Notion workspace documentation page for the engineering team.
- **Query:** append task blocks and code snippets to the Notion engineering onboarding page
- **Required:** `NOTION_APPEND_TASK_BLOCKS; NOTION_APPEND_CODE_BLOCKS`
- **Missed:** `NOTION_APPEND_CODE_BLOCKS; NOTION_APPEND_TASK_BLOCKS`
- **Primary returned:** `NOTION_ADD_MULTIPLE_PAGE_CONTENT`

### synthetic-001-q3 — recall 0.0%
- **Task:** As an engineering manager transitioning our sprint tracking infrastructure, I need to verify a complex Jira expression for our new automation rules before setting up our workspaces. Simultaneously, I need to check my authenticated identity in Linear to ensure the correct bot account is authorized, and clean up our project feed by archiving an obsolete status update that is no longer relevant to the team.
- **Query:** Archive an obsolete project update in Linear to clean up the workspace status feed.
- **Required:** `LINEAR_ARCHIVE_PROJECT_UPDATE`
- **Missed:** `LINEAR_ARCHIVE_PROJECT_UPDATE`
- **Primary returned:** `LINEAR_UPDATE_LINEAR_PROJECT`

### synthetic-002-q1 — recall 0.0%
- **Task:** As the IT administrator for our growing enterprise, I need to set up a dedicated workspace for the new APAC expansion team in Slack. First, look up our enterprise directory contacts to verify the regional lead's account details. Then, create the new Enterprise team workspace and immediately provision a public coordination channel for them to begin onboarding.
- **Query:** Find the contact details and email for the APAC regional lead in our enterprise directory to prepare for workspace provisioning.
- **Required:** `GMAIL_GET_CONTACTS`
- **Missed:** `GMAIL_GET_CONTACTS`
- **Primary returned:** `SLACK_FIND_USER_BY_EMAIL_ADDRESS`

### synthetic-009-q2 — recall 0.0%
- **Task:** As part of our annual CRM and marketing cleanup, we need to retire obsolete data across platforms. First, I need to look up all the LinkedIn company pages and organizations where my account holds administrative roles so we know which brand spaces are active. Then, I need to clean out several outdated products from our product catalog and remove a batch of old promotional email records that are no longer needed for compliance archiving.
- **Query:** Archive the outdated product catalog items by their specific product IDs in HubSpot.
- **Required:** `HUBSPOT_ARCHIVE_PRODUCTS`
- **Missed:** `HUBSPOT_ARCHIVE_PRODUCTS`
- **Primary returned:** `HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID`

### synthetic-010-q1 — recall 50.0%
- **Task:** A high-priority client onboarding checklist needs to be set up on our project tracking board, with specific team members assigned to review the documentation. Once the cards are prepped, the onboarding action items, including code repository access steps and required security toggles, must be appended directly into our central Notion workspace documentation page for the engineering team.
- **Query:** add checklists to the onboarding card on the project board and assign the designated team members
- **Required:** `TRELLO_ADD_CHECKLISTS; TRELLO_ADD_MEMBER_TO_CARD`
- **Missed:** `TRELLO_ADD_MEMBER_TO_CARD`
- **Primary returned:** `TRELLO_ADD_CHECKLISTS; TRELLO_ADD_CHECKLISTS_CHECK_ITEMS_BY_ID_CHECKLIST`

## Generation Rejections
| Reason | Count |
|---|---:|
| Gemini marked the candidate group infeasible | 3 |
| fewer than the required number of toolkits actually used | 4 |
| invalid or invented required tool | 2 |
