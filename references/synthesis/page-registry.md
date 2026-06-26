# DataForSEO Brain — page registry (synthesis contract)

Authoritative list of every `wiki/` content note. Synthesis agents create exactly these files,
following `references/synthesis/note-template.md`. `[[wikilinks]]` may target ONLY slugs in this
registry (plus `index`, and the folder `_index` MOCs). Raw column = which
`.raw/sources/dataforseo-research/<dir>/` to read for facts. All notes: ≥80 lines, ≥8 wikilinks.

Folder hubs (created separately, link targets): `index`, `concepts/_index`, `platforms/_index`,
`entities/_index`, `flows/_index`, `decisions/_index`, `sources/_index`, `meta/dashboard`.

---

## concepts/  (cap-*)  — 31 notes

### Platform mechanics & appendix (12)  — raw: `appendix/`, plus `_research/cost-lifecycle-bestpractices.md`
| slug | scope |
|---|---|
| cap-platform-architecture | v3 API shape: base URL, `/v3/{module}/{function}`, the 12-module map, request/response envelope (tasks[]/result[]/cost/status). MASTER HUB — most notes link here. |
| cap-task-vs-live-execution | POST-task → tasks_ready → task_get (queue) vs Live (synchronous); latency/retry/idempotency; when each is forced. HUB. |
| cap-queue-priority-cost-model | Priority 1 vs 2, per-result vs per-request billing, balance/credits, the `cost` field, $50 min deposit. HUB. |
| cap-rate-limits-throughput | 2000 calls/min, 30 simultaneous, ≤100 tasks/POST, 120s live timeout, 429/40202 handling, batching. |
| cap-status-error-codes | 20000 OK / 20100 Task Created / 40xxx client / 50xxx server; task-level vs HTTP-level; retryable set. |
| cap-authentication-security | HTTP Basic auth, base64(login:password), API password ≠ account password, credential hygiene. |
| cap-sandbox-testing | sandbox.dataforseo.com free dummy-data endpoints; validate request shape at $0; CI patterns. |
| cap-webhooks-pingback-postback | pingback (ready GET) vs postback (result POST), `$id`/`$tag` templating, webhook_resend, vs polling. |
| cap-result-tiers-regular-advanced-html | Regular vs Advanced vs HTML result depth across SERP/OnPage; element coverage + cost deltas. |
| cap-locations-languages-targeting | location_code/name/coordinate, language_code, device/os; locations & languages helper endpoints. |
| cap-account-usage-userdata | appendix/user_data: balance, limits, money spent, daily cost-limit (40203), usage monitoring. |
| cap-data-collection-methodology | How DataForSEO sources data: own SERP scraping vs Google Ads API vs clickstream vs own backlink crawler; freshness/retention/accuracy. raw: `_research/competitive-market.md`. |

### Module capabilities (19)  — raw: the named module dir
| slug | scope | raw |
|---|---|---|
| cap-serp-api | SERP API hub: engines, Task/Live, Regular/Advanced/HTML, depth/cost; routes to verticals. | serp/ |
| cap-serp-google-verticals | Google AI Mode, AI Overview, Maps, Local Finder, News, Events, Images, Jobs, Autocomplete, Ads, Finance. | serp/ |
| cap-serp-non-google-engines | Bing, YouTube, Baidu, Yahoo, Seznam, Naver coverage + per-engine quirks (task-only engines). | serp/ |
| cap-keywords-data-api | Google Ads + Bing Ads volume/keywords-for-site/keywords-for-keywords/ad-traffic; lineage. | keywords-data/ |
| cap-trends-and-clickstream | Google Trends, DataForSEO Trends, Clickstream (real-volume signals, bulk). | keywords-data/ |
| cap-ai-optimization-api | LLM Responses (ChatGPT/Claude/Gemini/Perplexity), LLM Scraper, AI Keyword Data. | ai-optimization/ |
| cap-llm-mentions-visibility | LLM Mentions: search, top domains/pages, aggregated, cross-model — brand/citation visibility in AI answers. | ai-optimization/, _research/ai-geo-practice.md |
| cap-domain-analytics | Technologies (stack detection) + Whois (registration intel). | domain-analytics/ |
| cap-labs-keyword-research | Labs keyword engine (Google/Amazon/Play/App Store): ideas, suggestions, related, difficulty, intent, overview, historical. | labs/ |
| cap-labs-competitor-research | SERP competitors, ranked keywords, competitors-domain, domain/page intersection, relevant pages, rank overview, historical, bulk traffic. | labs/ |
| cap-labs-market-analysis | Categories, top searches, categories-for-domain/keywords — demand mapping. | labs/ |
| cap-onpage-api | Crawler: task mgmt, summary, pages, resources, duplicates, links, redirects, non-indexable, waterfall, density, raw HTML, parsing, screenshot, instant pages, Lighthouse, microdata. | onpage/ |
| cap-backlinks-api | Summary, history, backlinks, anchors, referring domains/networks, competitors, intersections, domain pages, timeseries, new/lost. | backlinks/ |
| cap-backlinks-bulk-metrics | Bulk endpoints: ranks, spam score, backlinks, referring domains, new/lost (≤1000 targets). | backlinks/ |
| cap-content-analysis-api | Search, summary, sentiment, rating distribution, phrase/category trends over a citation DB. | content-analysis/ |
| cap-merchant-api | Amazon (ASIN/sellers/products/reviews) + Google Shopping (products/info/sellers/reviews). | merchant/ |
| cap-app-data-api | Google Play + Apple App Store: searches, list, info, reviews, listings (ASO). | app-data/ |
| cap-business-data-api | Google My Business/Hotels/Reviews/Q&A, Trustpilot, Tripadvisor, Pinterest, Business Listings. | business-data/ |
| cap-databases | Pre-indexed SERP/keyword/backlink/whois/business repositories; cost/freshness vs live. | databases/ |

### Integration / cross-cutting (2)  — raw: `_research/mcp-integration-ecosystem.md`, `appendix/`
| slug | scope |
|---|---|
| cap-mcp-server-integration | Official DataForSEO MCP server: 10 modules, env config, transports, when MCP beats raw REST. |
| cap-geo-ai-search-optimization | GEO/AEO: tracking + optimizing presence in AI answers; which DFS APIs feed it; KPIs/limits. raw: `_research/ai-geo-practice.md`. |

---

## platforms/  (plat-*)  — 10 notes  (surface from DataForSEO's lens)
| slug | scope | raw |
|---|---|---|
| plat-google-search | Google organic + SERP features + AI Overviews/AI Mode as a data surface. | serp/, labs/ |
| plat-google-maps-local | Maps, Local Finder, Google Business Profile, Hotels as local-SEO surfaces. | serp/, business-data/ |
| plat-bing-search | Bing SERP + Bing Ads keyword data; Copilot/Microsoft angle. | serp/, keywords-data/ |
| plat-youtube | YouTube SERP, video info, comments as search/discovery surface. | serp/ |
| plat-other-search-engines | Baidu, Yahoo, Seznam, Naver regional coverage + gaps. | serp/ |
| plat-amazon-marketplace | Amazon as product/keyword/review surface (Merchant + Labs Amazon). | merchant/, labs/ |
| plat-google-shopping | Google Shopping product/seller/review data. | merchant/ |
| plat-app-stores | Apple App Store + Google Play as ASO surfaces. | app-data/, labs/ |
| plat-review-platforms | Trustpilot, Tripadvisor, Google Reviews, Pinterest — reputation/sentiment. | business-data/, content-analysis/ |
| plat-ai-assistants | ChatGPT, Claude, Gemini, Perplexity as answer surfaces DFS queries/monitors. | ai-optimization/, _research/ai-geo-practice.md |

---

## entities/  (ent-*)  — 8 notes  (raw: `_research/competitive-market.md`, `_research/mcp-integration-ecosystem.md`)
| slug | scope |
|---|---|
| ent-dataforseo | The vendor: raw-data API positioning (no dashboard), scale, pricing philosophy, trust. |
| ent-dataforseo-mcp-server | Official MCP server repo: modules, env config, releases, agent integration. |
| ent-ahrefs | Competitor: AhrefsBot crawler, largest link index, subscription + API units. |
| ent-semrush | Competitor: all-in-one SaaS, keyword/traffic estimates, API units. |
| ent-moz | Competitor: DA/PA metrics, Link Explorer, smaller index. |
| ent-google-ads-keyword-planner | Upstream data source for Keywords Data; GKP bucketing limits DFS smooths. |
| ent-clickstream-data | Clickstream providers behind DataForSEO Trends / real-volume signals. |
| ent-llm-model-providers | OpenAI/Anthropic/Google/Perplexity as the models powering AI Optimization. |

---

## flows/  (play-*)  — 10 notes  (step-by-step: trigger → API sequence → cost/cadence → output → pitfalls)
| slug | scope | raw |
|---|---|---|
| play-rank-tracking-pipeline | Daily/weekly rank tracking: SERP Standard + scheduling + webhooks; time-series storage. | serp/, appendix/ |
| play-keyword-research-workflow | Seed → Keywords Data volume → Labs ideas/related/difficulty/intent → prioritize. | keywords-data/, labs/ |
| play-backlink-audit | Backlinks summary → referring domains → new/lost → bulk spam → cleanup. | backlinks/ |
| play-technical-site-audit | OnPage crawl → summary → duplicates/redirects/non-indexable → Lighthouse → fix list. | onpage/ |
| play-local-seo-tracking | Maps/Local Finder ranks + Business Profile + reviews per location. | serp/, business-data/ |
| play-ai-visibility-tracking | GEO loop: LLM Mentions cross-model + LLM Responses sampling → citation dashboard. | ai-optimization/, _research/ai-geo-practice.md |
| play-ecommerce-product-research | Amazon/Shopping Merchant + Labs Amazon + App Data reviews → product/ASO intel. | merchant/, app-data/, labs/ |
| play-competitor-gap-analysis | Labs domain intersection + ranked keywords + Backlinks intersection + Technologies. | labs/, backlinks/, domain-analytics/ |
| play-content-strategy-brief | SERP scrape + Labs market/keywords + Content Analysis sentiment → brief. | serp/, labs/, content-analysis/ |
| play-cost-optimized-pipeline | Sandbox → bulk endpoints → Standard+webhooks → spend monitoring. THE money-saving flow. | appendix/, _research/cost-lifecycle-bestpractices.md |

---

## decisions/  (dec-*)  — 7 notes  (the judgment spine; most-linked)
| slug | scope | raw |
|---|---|---|
| dec-which-api-for-which-job | Master router: job-to-be-done → module/endpoint (decision table). MOST-LINKED. | all |
| dec-live-vs-standard-vs-priority | When to pay Live vs queue Standard vs Priority — latency/cost/volume matrix. | appendix/, _research/cost-lifecycle-bestpractices.md |
| dec-mcp-vs-raw-rest | MCP server (agent-native) vs raw REST (production scale) tradeoffs. | _research/mcp-integration-ecosystem.md |
| dec-dataforseo-vs-ahrefs-semrush-moz | Data source, pricing model, freshness, build-vs-buy; when DFS wins/loses. | _research/competitive-market.md |
| dec-cost-control-strategy | The optimization playbook: Live vs Standard, bulk, Labs vs live, sandbox, depth. | _research/cost-lifecycle-bestpractices.md |
| dec-labs-vs-live-apis | Pre-indexed Labs/Databases (cheap, slightly stale) vs live SERP/Keywords (fresh, costlier). | labs/, databases/, serp/ |
| dec-when-not-to-use-dataforseo | Anti-patterns: need a UI, tiny volume, non-technical team, per-user latency, niche regions. | _research/competitive-market.md |
