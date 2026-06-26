---
type: concept
title: "Domain Analytics API"
domain: dataforseo
subdomain: domain-analytics
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, domain-analytics, technographics]
related:
  - "[[cap-backlinks-api]]"
  - "[[cap-data-collection-methodology]]"
  - "[[play-competitor-gap-analysis]]"
---

# Domain Analytics API

> Technology-stack detection and Whois registration intelligence, enriched with backlink and SERP metrics. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The Domain Analytics module answers two questions about a domain: what software it runs, and who/when it was registered. The Technologies sub-API is a technographics engine (a Wappalyzer-style stack detector) over DataForSEO's crawl of millions of domains, and the Whois sub-API turns registration records into a queryable, filterable dataset enriched with backlink and organic/paid SERP metrics. Both are Live-only. This module is the technographic and ownership layer that complements keyword, SERP, and backlink data in competitive research.

## What it covers
Technologies (`/v3/domain_analytics/technologies/`):
- **domain_technologies**: the full stack for one `target` domain, returning a `technologies` object grouped into web_development, add_ons, servers, content, media, location, plus meta, contacts, and social graph.
- **technologies_summary**: counts of domains by country, language, and content_language for given technologies, groups, categories, or keywords.
- **technology_stats** and **aggregation_technologies**: popularity stats and technologies commonly used alongside a target technology.
- **domains_by_technology** and **domains_by_html_terms**: reverse lookup of domains using a technology or matching HTML terms, with filtering, sorting, and pagination.

Whois (`/v3/domain_analytics/whois/`):
- **overview**: filtered, sorted lists of domains with registration dates, registrar, EPP status codes, TLD, plus `metrics` (organic and paid SERP positions and ETV) and `backlinks_info`.
- A **technologies reference** endpoint lists the full technologies, groups, and categories taxonomy plus available filters, locations, and languages, and a **whois filters** reference lists the filterable fields.
- `technology_paths` use a `$group_id.$category_id` path form, and `mode` toggles exact (`as_is`) vs partial (`entry`) matching across the reverse-lookup endpoints.

## Key parameters / inputs
| field | notes |
|---|---|
| target | domain_technologies; single domain to analyze |
| technologies / groups / categories / keywords | summary and reverse-lookup selectors; max 10 each |
| mode | as_is (exact) or entry (partial matching) |
| filters | up to 8; operators include <, <=, >, >=, =, <>, in, not_in, like, not_like, regex (Whois) |
| order_by | up to 3 sort rules (domain_rank, last_visited, country_iso_code, etc.) |
| limit / offset / offset_token | pagination; limit max 1000 (Whois) or 10,000 (domains_by_technology); offset_token for >100,000 |

## Response / what you get back
domain_technologies returns a `domain_technology_item` with `domain`, `title`, `description`, `meta_keywords`, `domain_rank`, `last_visited`, `country_iso_code`, `language_code`, `content_language_code`, `phone_numbers`, `emails`, `social_graph_urls`, and the nested `technologies` object (for example web_development.javascript_libraries = jQuery, servers.cdn = Cloudflare, servers.databases = MySQL). Whois overview items carry `created_datetime`, `changed_datetime`, `expiration_datetime`, `first_seen`, `epp_status_codes`, `tld`, `registered`, `registrar`, plus a `metrics` object (organic/paid pos_1, pos_2_3, etv, count, estimated_paid_traffic_cost) and a `backlinks_info` object (referring_domains, dofollow, backlinks, time_update).

## Cost & method notes
- Both sub-APIs are Live-only and charged per request. In the cost log, domain_technologies ran $0.01 and whois overview ran $0.101 (Whois is markedly pricier because of the backlink and SERP enrichment).
- Up to 2000 requests/min, one task at a time. See [[cap-queue-priority-cost-model]] and [[cap-task-vs-live-execution]].

## When to use / how it fits
Domain Analytics powers the technographic and ownership legs of [[play-competitor-gap-analysis]]: detect a competitor's CMS, CDN, and analytics, find all domains running a given technology for lead lists, and use Whois to filter domains by registration age, registrar, and traffic. The crawl-based sourcing is described in [[cap-data-collection-methodology]], and the backlink metrics that enrich Whois come from the index behind [[cap-backlinks-api]]. Route by job in [[dec-which-api-for-which-job]]; for pre-indexed alternatives see [[cap-databases]].

## Gotchas / limits
- Selector arrays cap at 10 entries; filters cap at 8; sort rules cap at 3.
- domains_by_technology requires limit + offset <= 10,000; use `offset_token` beyond 100,000 results.
- Technologies reflects the last crawl (`last_visited`), so very new or very small sites may be stale or absent.
- Whois `registered` is false when a domain has expired, which is itself a useful drop-catching signal.
- The Whois `metrics` and `backlinks_info` enrichment is sourced from DataForSEO's own backlink index, so coverage tracks that index rather than the live web.
- aggregation_technologies internal list limits (`internal_groups_list_limit`, `internal_categories_list_limit`, `internal_technologies_list_limit`) default to 5/5/10 and can be overridden by `internal_list_limit`.

## Related
- [[cap-backlinks-api]]
- [[cap-data-collection-methodology]]
- [[play-competitor-gap-analysis]]
- [[cap-databases]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[cap-locations-languages-targeting]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/domain_analytics/technologies/domain_technologies/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/domain_analytics/technologies/technologies_summary/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/domain_analytics/technologies/domains_by_technology/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/domain_analytics/whois/overview/live/ (retrieved 2026-06-26)
