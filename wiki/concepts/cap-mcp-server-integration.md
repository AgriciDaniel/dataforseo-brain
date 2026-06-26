---
type: concept
title: "MCP Server Integration"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, mcp, integration]
related:
  - "[[ent-dataforseo-mcp-server]]"
  - "[[dec-mcp-vs-raw-rest]]"
  - "[[cap-authentication-security]]"
---

# MCP Server Integration

> The official DataForSEO Model Context Protocol server that lets AI assistants call SEO APIs through natural language. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The official DataForSEO MCP server is a TypeScript/Node.js implementation of Anthropic's Model Context Protocol, published under Apache-2.0 (around 221 stars / 120 forks on GitHub in mid-2026). It exposes selected DataForSEO APIs as MCP tools so agents like Claude Code, Cursor, and ChatGPT can request SEO data via prompts instead of hand-coded REST calls. It uses a JSON-RPC client-server architecture and removes per-source integration work. The package is published on npm as `dataforseo-mcp-server` (latest 2.9.9 at retrieval, Jun 2026) and requires Node.js >=20.0.0 (per `package.json` engines; the README still says v14+ and the marketing page 18+, both stale). The v2.9.9 line added Historical SERPs (date params), an `exclude_targets` field on the backlinks domain-intersection tool, tool annotations/titles, OAuth/MCP auth improvements, and Cloudflare Worker deploy. The vendor and repo are profiled in [[ent-dataforseo-mcp-server]].

## What it covers
The server is organized into modules, each wrapping an API family and exposing multiple tools. The README (the authoritative superset) lists ten modules:
- **SERP** (Google, Bing, Yahoo results), **KEYWORDS_DATA** (volume, CPC, clickstream), **ONPAGE** (crawling), **DATAFORSEO_LABS** (proprietary databases), **BACKLINKS** (links and referring domains), **BUSINESS_DATA** (reviews, listings), **DOMAIN_ANALYTICS** (technologies, Whois), **CONTENT_ANALYSIS** (citation tracking, sentiment), **AI_OPTIMIZATION** (keyword discovery, conversational optimization, LLM benchmarking), and **MERCHANT** (product, pricing, seller data).
- Marketing pages sometimes list only the "seven major" modules and omit AI_OPTIMIZATION and MERCHANT; this is a documentation lag, not a contradiction.
- By default the server registers hundreds of tools, which consumes significant LLM context, so operators are expected to narrow the surface.
- Officially documented clients include Claude Desktop, Claude Code, Cursor, ChatGPT, Gemini CLI, and Docker; reported agent workflows include keyword clustering, backlink comparison, and competitor analysis from conversational prompts.

## Key parameters / inputs
Environment variables and config:
| var | role |
|---|---|
| DATAFORSEO_USERNAME | required; API login (account email) |
| DATAFORSEO_PASSWORD | required; auto-generated API password (not the dashboard password) |
| ENABLED_MODULES | comma-separated allow-list (for example "SERP,KEYWORDS_DATA,ONPAGE"); primary permission gate; all modules load if unset |
| ENABLED_PROMPTS | allow-list of prompt templates (for example top_3_google_result_domains) |
| DATAFORSEO_FULL_RESPONSE | true returns unfiltered raw API responses (default false) |
| DATAFORSEO_SIMPLE_FILTER | true flattens the filter schema for LLMs that struggle with nested structures |

A `field-config.json` (`supported_fields` keyed by tool name) further trims returned fields via `--configuration field-config.json`.

## Response / what you get back
Tools return the underlying DataForSEO API result, optionally filtered. Modules are built on a `BaseModule` class (a `getTools()` method) registered in `modules.config.ts`. Transports available:
- **stdio** (default): `npx dataforseo-mcp-server`, the local mode Claude Desktop uses.
- **Streamable HTTP**: `npx dataforseo-mcp-server http` (port 3000); works with most modern MCP clients but not Claude Desktop.
- **SSE** (legacy/deprecated): `npx dataforseo-mcp-server sse`.
- **Hosted remote**: DataForSEO runs managed endpoints at `https://mcp.dataforseo.com/mcp` (streamable HTTP) and `https://mcp.dataforseo.com/http` (HTTP/SSE), so no self-hosting is required.
- **Cloudflare Worker**: an `index-worker.js` build with `POST /mcp`, `GET /sse`, `GET /health`, deployable via wrangler.

## Cost & method notes
- The MCP server itself is free and open source; usage bills against your DataForSEO account at the same per-endpoint cost as raw REST. See [[cap-queue-priority-cost-model]].
- Curated MCP can cut LLM tokens roughly 50-80% with no consumer-side integration code, at the cost of roughly 15-25% added latency from JSON-RPC overhead; naive MCP with too many verbose tools can increase tokens, which is exactly why ENABLED_MODULES and field-config exist.

## When to use / how it fits
Choose MCP for agent-native prototyping and interactive runtimes (Claude Code, Cursor, ChatGPT), multi-tool reasoning, and going from idea to running prototype in minutes. Choose raw REST or the official client libraries for production batch jobs, scheduled enrichment, and high-throughput statically-authenticated server-to-server calls. The full tradeoff is the decision [[dec-mcp-vs-raw-rest]]. Auth is the same HTTP Basic scheme as REST, covered in [[cap-authentication-security]]. The AI_OPTIMIZATION module surfaces the capabilities in [[cap-ai-optimization-api]].

## Gotchas / limits
- Default loads all modules and hundreds of tools, drowning the agent's context; always set ENABLED_MODULES.
- MCP suits interactive sessions; many MCP paths assume a per-user session and lack a clean static-credential server-to-server option, where REST is stronger.
- Streamable HTTP transport does not work with Claude Desktop; use stdio there.
- The same 2000 calls/min and per-endpoint limits in [[cap-rate-limits-throughput]] apply, since MCP is a thin wrapper over the same APIs.

## Related
- [[ent-dataforseo-mcp-server]]
- [[dec-mcp-vs-raw-rest]]
- [[cap-authentication-security]]
- [[ent-dataforseo]]
- [[cap-ai-optimization-api]]
- [[cap-rate-limits-throughput]]
- [[cap-platform-architecture]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://github.com/dataforseo/mcp-server-typescript (retrieved 2026-06-26)
- https://dataforseo.com/help-center/setting-up-the-official-dataforseo-mcp-server-simple-guide (retrieved 2026-06-26)
- https://dataforseo.com/model-context-protocol (retrieved 2026-06-26)
- https://www.npmjs.com/package/dataforseo-mcp-server (retrieved 2026-06-26)
- https://github.com/dataforseo/mcp-server-typescript/blob/master/package.json (retrieved 2026-06-26)
- https://workos.com/blog/mcp-vs-rest (retrieved 2026-06-26)
