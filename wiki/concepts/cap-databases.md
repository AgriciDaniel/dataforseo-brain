---
type: concept
title: "Databases (Capability)"
domain: dataforseo
subdomain: databases
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, databases, bulk-data]
related:
  - "[[cap-labs-keyword-research]]"
  - "[[cap-serp-api]]"
  - "[[dec-labs-vs-live-apis]]"
  - "[[cap-platform-architecture]]"
---

# Databases (Capability)

> DataForSEO Databases are pre-indexed, downloadable dataset dumps (JSON/CSV) of SERP, keyword, app, backlink, business, and whois data, delivered to your own storage rather than served per API call. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
Databases are the bulk-delivery alternative to live and Labs APIs. Instead of querying one keyword or domain at a time over REST, you license a whole dataset, which DataForSEO ships to your client-side storage as periodic dumps. This suits teams that want to load billions of rows into their own warehouse and run their own analytics, rather than paying per request. The model is documented at the Databases overview rather than as standard `/v3/{module}/{function}` endpoints, because the deliverable is a file, not a JSON response.

## What it covers
- Google: Regular SERP (organic, paid, featured snippets), Advanced SERP (all SERP elements plus knowledge graphs, top stories, Page Rank, Domain Rank), Historical SERP (millions of monthly snapshots since August 2021), Keyword (billions of search terms enriched with Google Ads data), Historical Keyword (since the beginning of 2019), Unified Search (Advanced SERP plus Keyword across 67 regions), and Unified Search Historical.
- Bing: Keyword (millions of search terms enriched with Bing Ads data).
- App and Marketplace: Google Play SERPs and Listings, App Store SERPs and Listings, and Amazon Products (keywords, listings, title, description, price, rating, delivery info).
- Specialized: Backlink Summary (JSON/CSV), Business Listings (millions of point-of-interest records), and Whois Domains (whois plus search-visibility data).

## Key parameters / inputs
| field | notes |
|---|---|
| database / category | which dataset to license (for example Advanced SERP, Keyword, Business Listings) |
| location parameters | location coverage affects size and price |
| format | JSON or CSV, depending on the dataset |
| delivery target | client-side storage: AWS S3, SFTP, Google Cloud, etc. |
| refresh | updated dumps available at 50% of the standard price |

## Response / what you get back
The deliverable is a dataset dump, not a per-call JSON envelope. SERP databases contain the same element structure exposed by the live SERP API (organic, paid, featured snippets, and, for Advanced, knowledge graphs, top stories, and the Page/Domain Rank fields). Keyword databases carry search terms enriched with Google Ads or Bing Ads metrics. App and marketplace databases carry app id, icon, reviews count, rating, price, and product listing fields. Specialized databases carry backlink summary metrics, POI records, or whois plus visibility data. Files arrive in JSON (and CSV for several categories) in your storage bucket.

## Cost & method notes
- Pricing is not per request: "The cost of a specific database depends on its size and location parameters." Refresh/updated databases are available at "50% of the standard price."
- Update cadence varies by dataset: SERPs and app listings refresh on roughly 60-and-90-day cycles; keyword data updates once a month; Historical SERP reaches back to August 2021 and Historical Keyword to the beginning of 2019.
- This is the cheapest per-row option at scale but the least fresh and highest upfront commitment; see [[dec-labs-vs-live-apis]] and [[dec-cost-control-strategy]].

## When to use / how it fits
Choose Databases when you need the whole haystack in your own warehouse: building an internal keyword tool, training models, or running analytics that would be uneconomical as millions of live calls. For targeted, fresh lookups use [[cap-serp-api]] or [[cap-keywords-data-api]]; for cheap pre-indexed analytics without managing dumps, use [[cap-labs-keyword-research]] and [[cap-labs-competitor-research]]. Databases are the bulk extreme of [[play-cost-optimized-pipeline]]; route the choice via [[dec-which-api-for-which-job]].

The decision is essentially build-vs-buy at the storage layer. A live or Labs call gives you a fresh slice on demand with no infrastructure; a database gives you the entire corpus to query offline but shifts ingestion, storage, indexing, and refresh management onto your team. Unified Search and Unified Search Historical bundle Advanced SERP and Keyword data together across 67 regions, which is the closest the catalog comes to a one-stop dataset. The Backlink Summary database is the bulk-download counterpart to the gated [[cap-backlinks-api]], useful when the per-call add-on is uneconomical for your volume.

## Gotchas / limits
- Freshness lags live APIs by design: 60-90 day SERP/app cycles and monthly keyword updates mean Databases are wrong for near-real-time tracking.
- Pricing is quote-based on size and location, not a flat per-call rate, so it requires a procurement conversation.
- You own the storage, ingestion, and querying; there is no DataForSEO dashboard over the data.
- Coverage and format vary by category (some JSON-only, some JSON and CSV); confirm per dataset before committing.
- Historical SERP coverage begins August 2021 and Historical Keyword coverage begins in early 2019; no dump reaches earlier than its category's start date regardless of size.
- Advanced SERP, Historical SERP, and the app/marketplace sets ship JSON-only, while Regular SERP, Keyword, Backlink Summary, and Whois Domains also offer CSV; plan your loader for the format each dataset uses.
- A refresh is the same dataset re-shipped at 50% of standard price, so total cost of ownership includes recurring update fees, not just the first download.
- Bing coverage in the catalog is keyword-only; there is no standalone Bing SERP database, so Bing SERP analysis still routes through the live [[cap-serp-api]].
- The Whois Domains dataset pairs registration data with search-visibility data, which supports domain-investing and prospecting workflows beyond pure SEO.

## Related
- [[cap-labs-keyword-research]]
- [[cap-labs-competitor-research]]
- [[cap-serp-api]]
- [[cap-keywords-data-api]]
- [[cap-domain-analytics]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[plat-google-search]]
- [[play-cost-optimized-pipeline]]
- [[dec-labs-vs-live-apis]]
- [[dec-cost-control-strategy]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/databases/overview/ (retrieved 2026-06-26)
