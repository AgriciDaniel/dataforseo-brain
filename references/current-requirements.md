# Current Requirements - DataForSEO v3 (fast-moving facts)

These facts drift and are re-verified monthly, and again before every release. Captured 2026-06-26
from official documentation plus a $5-capped live API test pass against the production endpoint.
Backlinks and LLM Mentions access was re-verified live on 2026-07-08.

## Refresh Cadence
Monthly for endpoint, parameter, and pricing drift; re-verify cost and authentication facts before
every release. Pricing figures below are live-observed on 2026-06-26; DataForSEO adjusted rates across
selected APIs on 2026-07-01, so refresh exact figures before scaling.

## Required Source Standard
Use official, primary, vendor, or API documentation first. Record URL, retrieval date, version,
deprecation notes, and confidence.

## Platform
| Item | Current value (2026-06-26) | URL | Retrieved | Confidence |
|---|---|---|---:|---|
| API version | v3 | https://docs.dataforseo.com/v3/ | 2026-06-26 | high |
| Production base URL | https://api.dataforseo.com/v3 | https://docs.dataforseo.com/v3/auth/ | 2026-06-26 | high |
| Sandbox base URL (free dummy data) | https://sandbox.dataforseo.com/v3 | https://docs.dataforseo.com/v3/appendix/sandbox/ | 2026-06-26 | high |
| Authentication | HTTP Basic, base64(login:password); API password from API Access tab | https://docs.dataforseo.com/v3/auth/ | 2026-06-26 | high |
| Official MCP server | dataforseo-mcp-server, 10 modules, env-configured | https://github.com/dataforseo/mcp-server-typescript | 2026-06-26 | high |

## Throughput and retention
| Item | Current value | URL | Retrieved | Confidence |
|---|---|---|---:|---|
| Rate limit | 2000 API calls per minute | https://docs.dataforseo.com/v3/appendix/errors/ | 2026-06-26 | high |
| Simultaneous requests | 30 | https://docs.dataforseo.com/v3/appendix/errors/ | 2026-06-26 | high |
| Tasks per POST array | up to 100 (1 for Live) | https://docs.dataforseo.com/v3/appendix/errors/ | 2026-06-26 | high |
| Live timeout | 120 seconds | https://docs.dataforseo.com/v3/appendix/errors/ | 2026-06-26 | high |
| Retention | 30 days standard; raw HTML 7 days; Live not stored | https://docs.dataforseo.com/v3/appendix/sandbox/ | 2026-06-26 | high |

## Cost model (verified live 2026-06-26, cheapest variants)
| Endpoint family | Observed live cost (USD) | URL | Retrieved | Confidence |
|---|---|---|---:|---|
| DataForSEO Labs (most live endpoints) | ~0.0101-0.0105 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| Labs search_intent | ~0.0011 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| SERP Google/Bing organic Live Advanced (depth 10) | ~0.0020 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| Keywords Data Google Ads (search_volume / keywords_for_site) | ~0.075 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| Keywords Data clickstream search volume | ~0.15 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| Domain Analytics whois overview | ~0.101 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| Content Analysis search/summary | ~0.020 per call | https://dataforseo.com/pricing | 2026-06-26 | high |
| OnPage instant_pages | ~0.0001 per page | https://dataforseo.com/pricing | 2026-06-26 | high |
| Account minimum deposit | 50.00 pay-as-you-go | https://dataforseo.com/pricing | 2026-06-26 | high |

Full per-call ledger: `.raw/sources/dataforseo-research/_cost-log.json` (39 endpoints tested live, total spend $0.85 of a $5 cap).

## Access notes observed during live testing
The Backlinks API and the AI Optimization LLM Mentions endpoints returned status 40204 on 2026-06-26,
when those two modules were still subscription-gated. DataForSEO removed the remaining monthly
commitments on 2026-07-01 and moved all endpoints to pay-as-you-go. The 40204 result is now legacy
for these modules.

**Pay-as-you-go status (re-verified 2026-07-08): active.** Gated through 2026-06-26; removed 2026-07-01
when DataForSEO moved all APIs to pay-as-you-go.
- **Backlinks API:** no subscription and no activation step. Live re-probe returned `20000 Ok` for
  `/v3/backlinks/summary/live` and `/v3/backlinks/bulk_ranks/live`; fixtures:
  `.raw/sources/dataforseo-research/backlinks/fixtures/summary-live.json` and
  `.raw/sources/dataforseo-research/backlinks/fixtures/bulk_ranks-live.json`.
- **LLM Mentions API:** no subscription and no activation step. Usage remains per request and per row,
  roughly $1.1 per 1,000 data rows. Live re-probe returned `20000 Ok`
  for `/v3/ai_optimization/llm_mentions/search/live`; fixture:
  `.raw/sources/dataforseo-research/ai-optimization/fixtures/llm-mentions-search.json`.
- Probe cost log: `.raw/sources/dataforseo-research/_cost-log-2026-07-08-reprobe.json`.
- The former Make.com, n8n, and Google Sheets connector waiver is historical only because there is
  no monthly minimum left to waive.

### Recent changes (2026)
Newest first; official update publication dates (source https://dataforseo.com/updates, retrieved 2026-07-08):
- **2026-07-01** - DataForSEO moved all endpoints to **100% pay-as-you-go**, removed the Backlinks
  and LLM Mentions monthly commitments, and adjusted rates across selected APIs.
- **2026-06-10** - Amazon Merchant API gains real-time **Live endpoints** (previously task-based only).
- **2026-05-28** - **LLM Scraper (ChatGPT)** now returns **ad results** (sponsored placements in ChatGPT answers).
- **2026-05-05** - **API v2 fully closed**; no new v2 requests (task_get had a ~1-month grace window). v3 only.
- **2026-04-27** - **OnPage Lighthouse API**: seven new browser-simulation parameters.
- **2026-04-21** - **OnPage uncrawlable-resources** endpoint plus expanded summary data.

Sources: https://dataforseo.com/update/pricing-update-in-dataforseo-apis (retrieved 2026-07-08);
https://docs.dataforseo.com/v3/backlinks/overview/ (retrieved 2026-06-26);
historical comparison pages retrieved 2026-06-26:
https://dataforseo.com/help-center/backlinks-api-pricing-explained and
https://dataforseo.com/help-center/llm-mentions-api-subscription-explained.
