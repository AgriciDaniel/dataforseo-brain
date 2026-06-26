---
type: concept
title: "AI Optimization API"
domain: dataforseo
subdomain: ai-optimization
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, ai-optimization, llm]
related:
  - "[[cap-llm-mentions-visibility]]"
  - "[[cap-geo-ai-search-optimization]]"
  - "[[ent-llm-model-providers]]"
---

# AI Optimization API

> A data layer for querying LLMs, scraping their consumer answers, and measuring AI search volume. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The AI Optimization API is DataForSEO's interface to the generative-search era. It is raw infrastructure (no dashboard) split into four endpoint groups: LLM Responses (call models via API), LLM Scraper (scrape the consumer ChatGPT/Gemini web UI), AI Keyword Data (AI search volume), and LLM Mentions (brand/citation visibility, covered separately in [[cap-llm-mentions-visibility]]). It lets teams test what each model says about a brand, collect cited sources, and size AI demand programmatically. Everything is pay-as-you-go with sandbox testing available.

## What it covers
- **LLM Responses** (`/v3/ai_optimization/{provider}/llm_responses/`): structured answers from ChatGPT, Claude, Gemini, and Perplexity through one interface. ChatGPT/Claude/Gemini support Live and Standard; Perplexity is Live-only (`task_post_supported: false`). Each provider has a `/models/` endpoint that is the source of truth for accepted `model_name` strings: the live `/v3/ai_optimization/claude/llm_responses/models` endpoint currently accepts claude-sonnet-4-6, claude-opus-4-8, claude-sonnet-4-5, and claude-opus-4-5, among others. The static docs page lists older models and lags Anthropic's release cadence, so always re-poll the `/models/` endpoint before pinning a version. Live LLM Responses calls are pay-as-you-go accessible with no subscription (verified 2026-06-26; fixtures captured at `.raw/sources/dataforseo-research/ai-optimization/fixtures/llm-responses-*.json`).
- **LLM Scraper** (`/v3/ai_optimization/{provider}/llm_scraper/`): scrapes the live ChatGPT and Gemini web interfaces for a keyword, returning the markdown answer, `search_results[]`, `sources[]`, typed `items[]` (text, tables, images, products, local businesses), and `brand_entities[]`. Advanced and HTML output. **Recent change (2026-05-28): the ChatGPT LLM Scraper now returns ad results.** It surfaces the **sponsored / ad placements that appear inside ChatGPT responses**, so the scraped items can now include paid results alongside the organic answer - relevant for tracking how ads show up in AI answers and for GEO competitive monitoring.
- **AI Keyword Data** (`/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live`): `ai_search_volume` and 12-month `ai_monthly_searches`, calculated from People Also Ask SERP data. Live-only, up to 1,000 keywords.
- **LLM Mentions** (`/v3/ai_optimization/llm_mentions/`): the brand and citation visibility tracker, split out into its own note [[cap-llm-mentions-visibility]].
- **Reference endpoints**: each provider has a `/models/` endpoint to enumerate available model versions, and AI Keyword Data has `/locations_and_languages/` for valid targeting.

## Key parameters / inputs
| field | notes |
|---|---|
| user_prompt | LLM Responses; required; up to 500 chars |
| model_name | required; basic name resolves to latest version |
| keyword | LLM Scraper; up to 2000 chars |
| keywords | AI Keyword Data; max 1000, up to 250 chars each |
| max_output_tokens / temperature / top_p | generation controls (temperature and top_p cannot combine); `max_output_tokens` ranges 16-2048 for non-reasoning models and 1024-4096 for reasoning models |
| web_search / force_web_search | enable or force the model to cite current web info (`force_web_search` is ChatGPT/Claude only) |
| web_search_country_iso_code / web_search_city | geo-target the web grounding (e.g. "FR", "Paris"); ChatGPT and Claude only |
| use_reasoning | Claude and Gemini reasoning mode (min ~1024 tokens) |
| message_chain / system_message | up to 10 prior turns; role/tone control |
| location_* / language_* | LLM Scraper and AI Keyword Data targeting |

## Response / what you get back
LLM Responses returns `model_name`, `input_tokens`, `output_tokens`, `reasoning_tokens`, `web_search`, `money_spent` (the third-party model's token charge, passed through), `items[]` (reasoning and message objects, each with `sections[]` of type/text and optional `annotations[]` of web sources with title and url), and `fan_out_queries[]`. LLM Scraper returns `markdown`, `sources[]`, `search_results[]`, typed items (e.g. `gemini_text`, `gemini_table`, `gemini_images`, `gemini_source`), and `brand_entities[]`. AI Keyword Data returns `ai_search_volume` and `ai_monthly_searches[]`.

## Cost & method notes
- Pricing combines DataForSEO's per-task cost with the model's pass-through `money_spent`. LLM Responses Live is $0.0006/task plus token charges; the Standard queue is $0.0002 plus a $0.01 refundable prepayment per task (auto-refunded down to the actual LLM cost, settling in up to ~72h) per the live pricing page, which is authoritative over the older raw-note $0.0006 Standard figure. LLM Scraper (ChatGPT and Gemini only) is $0.0012/page Standard, $0.0024 Priority, $0.004 Live (treat as approximate where the pricing page is unreachable). AI Keyword Data is $0.01/task plus $0.0001/keyword.
- In the cost log, AI Keyword Data search_volume ran $0.0101. See [[cap-queue-priority-cost-model]] and [[cap-task-vs-live-execution]].

## When to use / how it fits
Use LLM Responses to A/B what models say about your brand vs competitors, LLM Scraper as the budget option for real consumer answers with brand detection, and AI Keyword Data to find rising AI-phrased queries. This API powers [[play-ai-visibility-tracking]] and underpins [[cap-geo-ai-search-optimization]]. The models behind it are profiled in [[ent-llm-model-providers]] and the answer surfaces in [[plat-ai-assistants]]. Route by job in [[dec-which-api-for-which-job]].

## Gotchas / limits
- Execution time is up to 120 seconds per task; 30 concurrent Live tasks per account per platform; 2000 calls/min; one task per Live call.
- `annotations` can return empty even when `web_search` is true; some ChatGPT models (o3-mini, o1, o1-pro) do not support web_search.
- Perplexity Sonar models use web_search by default and are Live-only.
- `money_spent` is variable and stacks on top of the base task cost, so budget for both.
- LLM Responses temperature and top_p cannot be used together, and Claude cannot combine `force_web_search` with `use_reasoning`.
- Reasoning models can produce output that exceeds `max_output_tokens` when web search or reasoning is enabled.

## Related
- [[cap-llm-mentions-visibility]]
- [[cap-geo-ai-search-optimization]]
- [[ent-llm-model-providers]]
- [[plat-ai-assistants]]
- [[play-ai-visibility-tracking]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/ai_optimization/chat_gpt/llm_responses/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/claude/llm_responses/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/claude/llm_responses/models/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/gemini/llm_scraper/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/overview/ (retrieved 2026-06-26)
- https://dataforseo.com/pricing/ai-optimization/llm-responses (retrieved 2026-06-26)
- https://dataforseo.com/pricing/ai-optimization/llm-scraper (retrieved 2026-06-26)
- https://dataforseo.com/apis/ai-optimization-api (retrieved 2026-06-26)
- https://dataforseo.com/updates/category/announcement (retrieved 2026-06-26 - Ad Results Support in LLM Scraper API, published 2026-05-28)
