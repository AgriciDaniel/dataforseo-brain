---
type: entity
title: "DataForSEO MCP Server (official)"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, mcp, integration, agents]
related:
  - "[[ent-dataforseo]]"
  - "[[cap-mcp-server-integration]]"
  - "[[dec-mcp-vs-raw-rest]]"
---

# DataForSEO MCP Server (official)

> The official TypeScript/Node Model Context Protocol server that lets AI agents call DataForSEO APIs through one standardized interface. Sits under [[index|DataForSEO Brain]] → [[entities/_index|Entities]].

## Overview
The DataForSEO MCP server is a TypeScript / Node.js implementation of Anthropic's Model Context Protocol that lets AI assistants call selected DataForSEO APIs and obtain SEO data through a single standardized interface. It is published by DataForSEO under the Apache-2.0 license (~221 stars / ~120 forks on GitHub as of mid-2026). The framing is that MCP removes per-source custom integration work: it uses a JSON-RPC client-server architecture so non-technical users can request premium SEO data via natural-language prompts instead of hand-coded API calls.

## Modules / tools exposed
The server is organized into modules, each wrapping an API family and exposing multiple tools (from the README, the authoritative superset):
- SERP - real-time Google, Bing, Yahoo results
- KEYWORDS_DATA - search volume, CPC, clickstream keyword metrics
- ONPAGE - website crawling and on-page performance
- DATAFORSEO_LABS - proprietary keyword/SERP/domain databases and algorithms
- BACKLINKS - inbound links and referring-domain analysis
- BUSINESS_DATA - reviews/listings (Google, Trustpilot, Tripadvisor)
- DOMAIN_ANALYTICS - technology-stack detection and Whois
- CONTENT_ANALYSIS - citation tracking and sentiment
- AI_OPTIMIZATION - keyword discovery, conversational optimization, LLM benchmarking
- MERCHANT - product/pricing/seller data (Google Shopping, Amazon)

By default the server registers hundreds of tools, which consumes significant LLM context; modules are built on a `BaseModule` class (`getTools()`), registered in `modules.config.ts`, so operators are expected to narrow the surface.

## Configuration (env vars)
- `DATAFORSEO_USERNAME` - required (API login)
- `DATAFORSEO_PASSWORD` - required (API password, not the dashboard password - see [[cap-authentication-security]])
- `ENABLED_MODULES` - comma-separated allow-list (e.g. `"SERP,KEYWORDS_DATA,ONPAGE"`); the primary permission gate. If unset, all modules load.
- `ENABLED_PROMPTS` - allow-list of prompt templates (e.g. `top_3_google_result_domains`)
- `DATAFORSEO_FULL_RESPONSE` - `true` returns unfiltered raw responses (default `false`)
- `DATAFORSEO_SIMPLE_FILTER` - `true` flattens the filter schema for LLMs that struggle with nesting
- A JSON `field-config.json` (`supported_fields` map keyed by tool) further trims returned fields, passed with `--configuration field-config.json`.

## Transports & distribution
- stdio (default) - `npx dataforseo-mcp-server` (the mode Claude Desktop uses)
- Streamable HTTP - `npx dataforseo-mcp-server http` (port 3000; not Claude Desktop)
- SSE - legacy/deprecated
- Hosted remote - DataForSEO runs `https://mcp.dataforseo.com/mcp` (streamable HTTP) and `https://mcp.dataforseo.com/http` (HTTP/SSE), so no self-hosting is required
- Cloudflare Worker - `index-worker.js` build with `POST /mcp`, `GET /sse`, `GET /health`, deployable via `wrangler`
- Published on npm as `dataforseo-mcp-server` (latest 2.9.9 at retrieval, Jun 2026; requires Node.js >=20.0.0 per `package.json` engines - the README still says v14+ and the MCP page 18+, both stale). The v2.9.9 line added Historical SERPs (date params), an `exclude_targets` field on the backlinks domain-intersection tool, tool annotations/titles, and OAuth/MCP auth improvements. Documented clients: Claude Desktop, Claude Code, Cursor, ChatGPT, Gemini CLI, Docker.

## When to use / how it fits
- MCP fits agent-native prototyping and interactive runtimes; raw REST fits production batch jobs - the full tradeoff is [[dec-mcp-vs-raw-rest]].
- The capability deep-dive is [[cap-mcp-server-integration]]; the vendor behind it is [[ent-dataforseo]].
- Powers conversational SEO over surfaces like [[plat-ai-assistants]] and flows such as [[play-ai-visibility-tracking]].

## Gotchas / limits
- Loading all modules drowns the agent in tool definitions and tokens; always set `ENABLED_MODULES` to shrink both attack surface and token cost.
- Marketing/help pages sometimes list only the "seven major" modules, omitting AI_OPTIMIZATION and MERCHANT; the README is the superset (documentation lag, not a contradiction).
- Many MCP paths assume a per-user interactive session and lack a clean static-credential, server-to-server auth option - a reason to prefer REST for unattended jobs.

## Related
- [[index]]
- [[entities/_index]]
- [[ent-dataforseo]]
- [[ent-llm-model-providers]]
- [[cap-mcp-server-integration]]
- [[cap-authentication-security]]
- [[cap-platform-architecture]]
- [[dec-mcp-vs-raw-rest]]
- [[dec-which-api-for-which-job]]
- [[plat-ai-assistants]]

## Sources
- DataForSEO MCP Server (TypeScript) - repo + README - https://github.com/dataforseo/mcp-server-typescript - retrieved 2026-06-26
- Setting Up the Official DataForSEO MCP Server: Simple Guide - https://dataforseo.com/help-center/setting-up-the-official-dataforseo-mcp-server-simple-guide - retrieved 2026-06-26
- DataForSEO Model Context Protocol (official MCP page) - https://dataforseo.com/model-context-protocol - retrieved 2026-06-26
- dataforseo-mcp-server (npm package) - https://www.npmjs.com/package/dataforseo-mcp-server - retrieved 2026-06-26
- MCP server package.json (version 2.9.9, engines.node >=20.0.0) - https://github.com/dataforseo/mcp-server-typescript/blob/master/package.json - retrieved 2026-06-26
- DataForSEO API v3 - Authentication - https://docs.dataforseo.com/v3/auth/ - retrieved 2026-06-26
