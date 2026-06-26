---
type: platform
title: "AI Assistants as DataForSEO Surfaces"
domain: dataforseo
subdomain: ai-optimization
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, ai-optimization, geo, llm]
related:
  - "[[cap-ai-optimization-api]]"
  - "[[cap-llm-mentions-visibility]]"
  - "[[play-ai-visibility-tracking]]"
---

# AI Assistants as DataForSEO Surfaces

> ChatGPT, Claude, Gemini, and Perplexity as answer surfaces that DataForSEO queries, scrapes, and monitors for brand mentions and citations. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
Generative engines are now a discovery surface alongside classic search, and DataForSEO exposes them through the AI Optimization API. The data layer has four parts: LLM Responses (send a prompt to a model and get a structured answer with citations), LLM Scraper (cheaper real-time collection of the consumer ChatGPT and Gemini interfaces), LLM Mentions (a queryable database of where brands and domains are cited inside AI answers), and AI Keyword Data (AI search volume derived from People Also Ask). This is raw infrastructure for Generative Engine Optimization (GEO), not a finished dashboard, so teams build their own tracking on top.

## What it covers
- LLM Responses for `chat_gpt`, `claude`, `gemini`, `perplexity`: structured answers with reasoning items, message items, source `annotations[]` (title, url), and `fan_out_queries[]`. ChatGPT, Claude, and Gemini support Live plus Standard; Perplexity is Live-only.
- LLM Scraper for `chat_gpt` and `gemini`: scrapes the live consumer interface, returning markdown, `search_results[]`, `sources[]`, typed items (text, table, images, products), and `brand_entities[]`.
- LLM Mentions: five Live-only endpoints (search, top_pages, top_domains, aggregated_metrics, cross_aggregated_metrics) tracking mentions and citations in Google AI Overview and ChatGPT.
- AI Keyword Data `keywords_search_volume`: `ai_search_volume` and `ai_monthly_searches` (12-month trend), computed from People Also Ask SERP data.

## Key parameters / inputs
- LLM Responses: `user_prompt` (required, up to 500 chars), `model_name` (required), `max_output_tokens`, `temperature`, `top_p`, `system_message`, `message_chain` (up to 10), and `web_search` / `force_web_search` / `use_reasoning` where the model supports them.
- LLM Scraper: `keyword` (up to 2000 chars), one location field, one language field, `force_web_search`.
- LLM Mentions: `target` array of up to 10 entities, each a `domain` (with search_scope sources/search_results) or `keyword` (with match_type word/partial and search_scope question/answer/brand_entities/fan_out_queries), plus `platform` (chat_gpt or google), location/language, `initial_dataset_filters`.
- AI Keyword Data: `keywords` (up to 1000, max 250 chars each), one location field, one language field.

## Response / what you get back
- LLM Responses result: `model_name`, `input_tokens`, `output_tokens`, `reasoning_tokens`, `web_search`, `money_spent` (USD, the third-party model charge passed through), `items[]` (reasoning and message sections with optional source annotations), `fan_out_queries[]`.
- LLM Mentions search item: `platform`, `model_name` (for google always `google_ai_overview`), `question`, `answer` (markdown), `sources[]` (source_name, snippet, title, domain, url, position, publication_date), `ai_search_volume`, `brand_entities[]`.
- Aggregation endpoints group by location, language, platform, `sources_domain[]`, `search_results_domain[]`, `brand_entities_title[]`, with `mentions` and `ai_search_volume` per group (`impressions` is deprecated and returns null).

## Cost & method notes
- Per the research report and live pricing pages: LLM Responses costs $0.0006 per task plus the underlying model token charge on Live, or $0.0002 plus a $0.01 refundable prepayment per task on Standard; LLM Scraper (ChatGPT and Gemini only) about $0.0012 per page Standard, $0.0024 Priority, $0.004 Live (approximate); LLM Mentions about $0.10 per request plus $0.001 per row with a $100 monthly minimum; AI Keyword Data about $0.01 per task plus $0.0001 per keyword.
- LLM Responses, Scraper, and Mentions all run up to 120s with 30 concurrent Live tasks per platform; 2000 calls/min. See [[cap-rate-limits-throughput]] and [[cap-task-vs-live-execution]].

## When to use / how it fits
- The GEO tracking loop combining LLM Mentions cross-model with LLM Responses sampling: [[play-ai-visibility-tracking]].
- Brand and citation visibility tracking: [[cap-llm-mentions-visibility]] and [[cap-geo-ai-search-optimization]].
- The model providers behind the surface: [[ent-llm-model-providers]].
- Choosing the AI Optimization endpoint for the job: [[dec-which-api-for-which-job]].

## Gotchas / limits
- Coverage is asymmetric: LLM Mentions covers Google AI Overview across multiple locations but ChatGPT only for United States (location_code 2840) and English. The launch set was Google AI Overview plus ChatGPT (US, GPT-5).
- LLM Responses source `annotations` may return empty even when `web_search` is true; some models do not support `web_search` (for example o1, o3-mini).
- Platforms overlap little in their citations, so each engine must be tracked separately.
- Practitioner evidence (GEO paper, Ahrefs) shows quotations, statistics, cited sources, YouTube mentions, and branded web mentions correlate with AI visibility far more than backlinks; keyword stuffing does not transfer. See [[cap-geo-ai-search-optimization]].
- ChatGPT web answers lean on Bing's index and Perplexity leans heavily on community discourse (Reddit), so the underlying source mix differs sharply per engine.
- DataForSEO is raw infrastructure, not a SaaS dashboard, so prompt design, scoring logic, and share-of-voice math are the caller's responsibility; finished trackers (Profound, Peec, Otterly) sit in a complementary category.

## Related
- [[cap-ai-optimization-api]]
- [[cap-llm-mentions-visibility]]
- [[cap-geo-ai-search-optimization]]
- [[cap-trends-and-clickstream]]
- [[cap-task-vs-live-execution]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-rate-limits-throughput]]
- [[play-ai-visibility-tracking]]
- [[ent-llm-model-providers]]
- [[plat-google-search]]
- [[plat-bing-search]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/ai_optimization/llm_responses/overview/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/search/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live/ - retrieved 2026-06-26
- https://dataforseo.com/update/introducing-llm-mentions-api - retrieved 2026-06-26
- https://dataforseo.com/pricing/ai-optimization/llm-responses - retrieved 2026-06-26
- https://dataforseo.com/pricing/ai-optimization/llm-scraper - retrieved 2026-06-26
- https://arxiv.org/abs/2311.09735 - retrieved 2026-06-26
