# Current Requirements - DataForSEO v3 (fast-moving facts)

These facts drift and are re-verified monthly, and again before every release. Captured 2026-06-26
from official documentation plus a $5-capped live API test pass against the production endpoint.

## Refresh Cadence
Monthly for endpoint, parameter, and pricing drift; re-verify cost and authentication facts before
every release. Pricing figures below are live-observed on 2026-06-26 and supersede any cached tier table.

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
The Backlinks API and the AI Optimization LLM Mentions endpoints returned status 40204 (access denied)
on the test account: both require an active add-on subscription separate from pay-as-you-go credit.
Their request and response shapes are still documented from the official docs in
`.raw/sources/dataforseo-research/backlinks/` and `.../ai-optimization/`.

**Subscription status (re-verified 2026-06-26): NOT removed.** A claim that DataForSEO dropped the
Backlinks subscription around May 2026 was checked against the official pricing page, the help-center
"Backlinks API pricing & subscription explained" article, AND a live API re-probe, and is false/unconfirmed.
- **Backlinks API:** still a **$100/month prepaid minimum**, credited to account balance and spendable on
  any DataForSEO API (not a sunk access fee). Still 40204-gated until activated. The minimum is **waived
  only when Backlinks is called via the Make.com, n8n, or Google Sheets connectors** (long-standing wording,
  not a 2026 change). Activation is a one-time dashboard action at
  **https://app.dataforseo.com/backlinks-subscription** (Plans and Subscriptions -> Backlinks API ->
  Activate -> Gain Access, then the payment form); it does not turn on automatically from balance.
- **LLM Mentions API:** a **separate, unchanged $100/month** subscription; activating one does not unlock
  the other. Also 40204-gated; usage priced $0.10/request + $0.001/row.

### Recent changes (2026)
Newest first; official update publication dates (source https://dataforseo.com/updates, retrieved 2026-06-26):
- **2026-06-10** - Amazon Merchant API gains real-time **Live endpoints** (previously task-based only).
- **2026-05-28** - **LLM Scraper (ChatGPT)** now returns **ad results** (sponsored placements in ChatGPT answers).
- **2026-05-05** - **API v2 fully closed**; no new v2 requests (task_get had a ~1-month grace window). v3 only.
- **2026-04-27** - **OnPage Lighthouse API**: seven new browser-simulation parameters.
- **2026-04-21** - **OnPage uncrawlable-resources** endpoint plus expanded summary data.

Sources: https://docs.dataforseo.com/v3/backlinks/overview/ (retrieved 2026-06-26);
https://dataforseo.com/help-center/backlinks-api-pricing-explained (retrieved 2026-06-26);
https://dataforseo.com/help-center/llm-mentions-api-subscription-explained (retrieved 2026-06-26);
https://app.dataforseo.com/backlinks-subscription (retrieved 2026-06-26).
