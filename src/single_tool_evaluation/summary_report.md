# Composio Search Single-Tool Evaluation Report

_Generated 2026-08-12T15:42:51.426388+00:00_

**Toolkits tested this run:** tinyurl, linear, elevenlabs, airtable, firecrawl, gemini, youtube, kommo, github, googledocs, quickbooks, one, cloudflare, datadog, zendesk, jira, googletasks, google, zep, discord

## Summary
- **Total queries:** 174
- **Primary hit rate:** 65.5%
- **Related hit rate:** 7.5%
- **Demotion rate:** 7.5%
- **Complete miss rate:** 27.0%

## Explicit vs. Implicit Queries
| Variant | Queries | Primary hit | Related hit | Demoted | Complete miss |
|---|---:|---:|---:|---:|---:|
| explicit | 87 | 69.0% | 11.5% | 11.5% | 19.5% |
| implicit | 87 | 62.1% | 3.4% | 3.4% | 34.5% |

## Primary Hit Rate by Toolkit
| Toolkit | Queries | Explicit | Implicit |
|---|---:|---:|---:|
| airtable | 10 | 100.0% | 80.0% |
| cloudflare | 10 | 100.0% | 80.0% |
| datadog | 10 | 80.0% | 80.0% |
| discord | 10 | 40.0% | 60.0% |
| elevenlabs | 10 | 80.0% | 80.0% |
| firecrawl | 10 | 60.0% | 40.0% |
| gemini | 10 | 40.0% | 40.0% |
| github | 10 | 0.0% | 0.0% |
| googledocs | 10 | 60.0% | 80.0% |
| googletasks | 10 | 40.0% | 40.0% |
| jira | 10 | 100.0% | 100.0% |
| kommo | 10 | 80.0% | 40.0% |
| linear | 10 | 60.0% | 40.0% |
| quickbooks | 10 | 80.0% | 80.0% |
| tinyurl | 4 | 100.0% | 100.0% |
| youtube | 10 | 80.0% | 80.0% |
| zendesk | 10 | 80.0% | 80.0% |
| zep | 10 | 80.0% | 40.0% |

## Latency
API/Search latency is the successful API call only; end-to-end latency includes retry backoff and failed attempts.
| Metric | API/Search (s) | End-to-end (s) |
|---|---:|---:|
| Average | 3.08 | 3.08 |
| Maximum | 10.17 | 10.17 |

## Failure Examples (20 of 47 complete misses)
| Variant | Toolkit | Target tool | Query | Primary tools returned | Error |
|---|---|---|---|---|---|
| implicit | linear | `LINEAR_GET_ISSUE_DEFAULTS` | Get the default state and estimate for a new team issue. | `LINEAR_CREATE_LINEAR_ISSUE` |  |
| explicit | linear | `LINEAR_GET_ALL_LINEAR_TEAMS` | List all linear teams in my workspace. | `LINEAR_LIST_LINEAR_TEAMS;LINEAR_LIST_LINEAR_PROJECTS` |  |
| implicit | linear | `LINEAR_GET_ALL_LINEAR_TEAMS` | List all the workspace teams to see their IDs and names. | `SLACK_LIST_ENTERPRISE_TEAMS;ASANA_GET_TEAMS_IN_WORKSPACE;NINOX_LIST_TEAMS` |  |
| implicit | linear | `LINEAR_CREATE_LINEAR_COMMENT` | Add a comment to the bug issue about the login failure. | `JIRA_ADD_COMMENT` |  |
| implicit | elevenlabs | `ELEVENLABS_CANCEL_CONVAI_BATCH_CALL` | Cancel the ongoing batch calling campaign right now. | `LEMLIST_GET_LIST_CAMPAIGNS;LEMLIST_GET_CAMPAIGN_BY_ID;LEMLIST_POST_PAUSE_CAMPAIGN;INSTANTLY_PAUSE_CAMPAIGN` |  |
| explicit | elevenlabs | `ELEVENLABS_CREATE_CONVAI_KNOWLEDGE_BASE_RAG_INDEX` | Use elevenlabs to compute RAG indexes for my knowledge base documents. | `ELEVENLABS_GET_CONVAI_KNOWLEDGE_BASE` |  |
| implicit | airtable | `AIRTABLE_DELETE_RECORD` | Permanently delete record rec12345 from my contacts table. | `OUTLOOK_DELETE_CONTACT_PERMANENTLY` |  |
| implicit | firecrawl | `FIRECRAWL_BATCH_SCRAPE` | Scrape these ten URLs concurrently and return the text content. | `COMPOSIO_SEARCH_FETCH_URL_CONTENT` |  |
| implicit | firecrawl | `FIRECRAWL_CREDIT_USAGE_GET` | How many credits do I have left on my account? | `ACTIVE_CAMPAIGN_GET_SMS_CREDITS;PILOTERR_USAGE_GET;ERANOL_GET_ACCOUNT_CREDITS;EXTRACTA_AI_GET_CREDITS;KIEAI_GET_ACCOUNT_CREDITS;OPEN_REGISTER_GET_CREDIT_USAGE` |  |
| explicit | gemini | `GEMINI_COUNT_TOKENS` | Can you use gemini to count the tokens in this text? | `OPENAI_GET_INPUT_TOKEN_COUNTS` |  |
| implicit | gemini | `GEMINI_COUNT_TOKENS` | Count how many tokens are in this paragraph. | `OPENAI_GET_INPUT_TOKEN_COUNTS;ELEVENLABS_CALCULATE_CONVAI_AGENT_LLM_USAGE` |  |
| explicit | gemini | `GEMINI_GET_VIDEOS_OPERATION` | Check the status of my Gemini video generation operation. | `GEMINI_WAIT_FOR_VIDEO` |  |
| implicit | gemini | `GEMINI_GET_VIDEOS_OPERATION` | Check the status of my ongoing video generation operation. | `GEMINI_WAIT_FOR_VIDEO` |  |
| explicit | gemini | `GEMINI_EMBED_CONTENT` | Use Gemini to generate text embeddings for this article. | `API_NINJAS_GENERATE_TEXT_EMBEDDINGS` |  |
| implicit | gemini | `GEMINI_EMBED_CONTENT` | Convert this text into a numerical vector for similarity comparison. | `OPENAI_CREATE_CHAT_COMPLETION;OPENAI_CREATE_EMBEDDINGS;COMPOSIO_SEARCH_GROQ_CHAT` |  |
| explicit | youtube | `YOUTUBE_LIST_COMMENT_THREADS` | List the top comment threads on this YouTube video for analysis. | `YOUTUBE_LIST_COMMENT_THREADS2` |  |
| implicit | youtube | `YOUTUBE_LIST_COMMENT_THREADS` | Fetch the comment threads and replies for this YouTube video ID. | `YOUTUBE_LIST_COMMENT_THREADS2` |  |
| implicit | kommo | `KOMMO_GET_PIPELINE_STATUS` | Can you fetch the details for pipeline status ID 4582? | `GITLAB_GET_SINGLE_PIPELINE` |  |
| implicit | kommo | `KOMMO_GET_PIPELINE` | Can you get the details for pipeline ID 12345? | `POSTHOG_RETRIEVE_PIPELINE_PLUGIN_DETAILS_BY_ID;HUBSPOT_GET_PIPELINE_BY_ID;POSTHOG_RETRIEVE_PIPELINE_DESTINATION_DETAILS;PIPEDRIVE_GET_PIPELINE` |  |
| implicit | kommo | `KOMMO_CREATE_CONTACT` | Add a new contact to the CRM with this phone number. | `GODIAL_ADD_CONTACT;CENTRALSTATIONCRM_CREATE_PERSON_CONTACT_DETAIL` |  |
