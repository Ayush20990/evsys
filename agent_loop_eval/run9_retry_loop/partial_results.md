# Run 9 — partial results, tasks 1-4

Gemini credits ran out during the first chunk. Tasks 1-4 completed; 5-10 were saved with
zero queries and have been deleted so they re-run rather than being skipped as done.

**Everything below needs no LLM.** Requirement-group scoring, the judge and fault
attribution all need Gemini and have not run, so there is no capability-level recall yet --
only flat recall against the raw reference lists, which overstates failure for the reasons
in `README.md`.

## What run 9 changed, and whether it worked

**Yes.** 3 of 17 queries were retries (18%). Run 8 produced **zero** retries
across all 384 of its queries, because a mock succeeds on any well-formed call and nothing
ever told the agent a tool was wrong.

### Task 1 — the agent spent its full retry budget and still found nothing

The step was *assess payment-link feasibility in HubSpot*:

| Attempt | Query | Returned |
|---|---|---|
| 1 | `Check payment link creation and feasibility in HubSpot` | `HUBSPOT_CREATE_QUOTE_OBJECT, HUBSPOT_CREATE_FEEDBACK_SUBMISSION` |
| 2 | `payment link checkout HubSpot` | `HUBSPOT_CREATE_TIMELINE_EVENT` |
| 3 | `payment links commerce invoices HubSpot` | `RAZORPAY_FETCH_ALL_PAYMENT_LINKS, STRIPE_LIST_PAYMENT_LINKS` |
| 4 | `HubSpot payment links` | `HUBSPOT_CLONE_MARKETING_EMAIL` |

Four genuinely different phrasings, every one naming HubSpot, and no HubSpot payment tool
ever came back -- because the catalogue has none. Attempt 3 surfaced Razorpay and Stripe.

In run 8 the agent accepted `STRIPE_CREATE_PAYMENT_LINK` on its first attempt, ran it, and
reported the task complete. Here it kept asking, which is the behaviour the retry budget
was built for -- though it still reported the task complete at the end.

## Per task

| Task | Queries | Retries | Flat union | Flat primary | Completed |
|---|---:|---:|---:|---:|---|
| 1 | 8 | 3 | 8/10 | 4/10 | True |
| 2 | 2 | 0 | 6/6 | 2/6 | False |
| 3 | 3 | 0 | 3/4 | 3/4 | False |
| 4 | 4 | 0 | 6/10 | 1/10 | False |

Flat union 23/30 (77%) · flat primary 10/30 (33%).
Both are against raw reference lists, so treat them as a floor, not a measurement.

## Found but not recommended

13 of the 23 reference tools that search returned appeared **only** in
`related`, never as a primary recommendation -- 56% of everything it found.
This needs no judgement to count, and it matches run 8's dominant finding.

| Task | Tool returned only in `related` |
|---|---|
| 1 | `HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION` |
| 1 | `HUBSPOT_GET_WORKFLOWS` |
| 1 | `HUBSPOT_GET_WORKFLOW_BY_ID` |
| 1 | `HUBSPOT_LIST_GRANTED_SCOPES` |
| 2 | `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` |
| 2 | `NOTION_GET_PAGE_MARKDOWN` |
| 2 | `NOTION_REPLACE_PAGE_CONTENT` |
| 2 | `NOTION_RETRIEVE_PAGE` |
| 4 | `LINKEDIN_DELETE_POST` |
| 4 | `LINKEDIN_GET_MY_INFO` |
| 4 | `LINKEDIN_GET_POST_CONTENT` |
| 4 | `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD` |
| 4 | `TRELLO_GET_LISTS_CARDS_BY_ID_LIST` |

## Still to run

- Tasks 5-100 (the agent loop is Gemini-driven)
- Requirement-group scoring, the single judge, and fault attribution

`python run9.py 0` scores and analyses what exists without running new tasks;
`python run9.py 10` continues from task 5 and then analyses. Nothing finished is repeated.
