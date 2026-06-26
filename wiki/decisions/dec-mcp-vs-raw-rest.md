---
type: decision
title: "MCP server vs raw REST"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, decision, mcp, integration]
related:
  - "[[ent-dataforseo-mcp-server]]"
  - "[[cap-mcp-server-integration]]"
  - "[[dec-which-api-for-which-job]]"
---

# MCP server vs raw REST

> When to hand DataForSEO to an agent over MCP, and when to call the v3 REST API (or client libs) directly. Sits under [[index|DataForSEO Brain]] → [[decisions/_index|Decisions]].

## Overview
DataForSEO ships an official Model Context Protocol server ([[ent-dataforseo-mcp-server]]) alongside its raw v3 REST API ([[cap-platform-architecture]]). MCP lets an agent describe a task in natural language and "handles all technical details automatically"; REST forces you to specify parameters and wire integration code per task. Neither dominates; the right call depends on whether the consumer is an interactive agent or an unattended production pipeline.

## The tradeoffs
- Token economics: a good REST API is "generous" - hundreds of small composable endpoints - which is cheap for code but drowns an LLM, since every tool definition is loaded into context and taxed in tokens each turn. Curated MCP can deliver ~50-80% fewer LLM tokens with zero consumer-side integration code, at the cost of ~15-25% added latency from JSON-RPC overhead. Naive MCP can INCREASE tokens if many servers each expose dozens of verbose tools - exactly why DataForSEO ships `ENABLED_MODULES` and field-config to shrink the surface ([[cap-mcp-server-integration]]).
- Auth model: MCP suits interactive sessions; many MCP paths assume a per-user session and lack a static-credential, server-to-server option. REST gives clean machine auth (HTTP Basic) for unattended jobs ([[cap-authentication-security]]).

## Decision rules
- Choose MCP for: agent-native prototyping, interactive runtimes (Claude Code, Cursor, ChatGPT), multi-tool reasoning, "idea to running prototype in minutes."
- Choose raw REST (or the official client libs) for: production batch jobs, scheduled enrichment, high-throughput parallel calls, and traditional backend integration where deterministic, statically-authenticated server-to-server calls matter.
- Hybrid is common: prototype a workflow over MCP, then harden the proven calls into a REST/client-lib pipeline.

## Practical integration paths
- MCP transports: stdio (`npx dataforseo-mcp-server`), Streamable HTTP, or the hosted endpoint `https://mcp.dataforseo.com/mcp` - all accept the same Basic Auth.
- REST clients: official Python `dataforseo-client` (PyPI), community PHP clients, plus Postman/OpenAPI specs.
- No-code middle ground: the official n8n node, Make, Zapier, Sheets connectors for reporting without code.

## When to use / how it fits
- This decision sits on top of [[dec-which-api-for-which-job]]: first pick the endpoint, then pick the access layer.
- MCP is the natural front door for [[play-ai-visibility-tracking]] and conversational SEO over [[plat-ai-assistants]]; REST powers [[play-cost-optimized-pipeline]] and scheduled flows like [[play-rank-tracking-pipeline]].

## Gotchas / limits
- Loading all MCP modules wastes context and money; always set `ENABLED_MODULES`.
- MCP's per-session auth assumption makes it awkward for unattended cron jobs - prefer REST there.
- JSON-RPC latency overhead (~15-25%) matters for tight, high-volume loops; REST/client libs are leaner at scale.

## Token-cost intuition
- Every MCP tool definition is loaded into the agent's context and taxed on every turn, so exposing all DataForSEO modules can cost more tokens than it saves.
- Curated to a few modules, MCP can cut LLM tokens ~50-80% versus hand-describing each REST call, because the agent no longer re-specifies parameters in prose.
- The ~15-25% JSON-RPC latency tax is acceptable for interactive use but compounds in tight high-volume loops.

## Migration pattern
1. Prototype the workflow conversationally over MCP with `ENABLED_MODULES` narrowed.
2. Capture the exact endpoints and parameters the agent settled on.
3. Re-implement those calls in the Python client or raw REST for the production pipeline.
4. Keep MCP for ad-hoc analysis; keep REST for scheduled, statically-authenticated jobs.

## Auth reminder
- Both surfaces use the same HTTP Basic credentials; the API password is distinct from the dashboard password and should live in a secret/env var ([[cap-authentication-security]]).

## Bottom line
- Prototype and explore over MCP; run production and scheduled jobs over REST or the official client libs.
- Use `ENABLED_MODULES` either way to keep the tool surface (and token cost) small.

## Related
- [[index]]
- [[decisions/_index]]
- [[ent-dataforseo-mcp-server]]
- [[ent-dataforseo]]
- [[cap-mcp-server-integration]]
- [[cap-platform-architecture]]
- [[cap-authentication-security]]
- [[dec-which-api-for-which-job]]
- [[dec-cost-control-strategy]]
- [[plat-ai-assistants]]

## Sources
- DataForSEO MCP Server: Bridging the Gap Between AI Models and SEO Data - https://dataforseo.com/blog/dataforseo-mcp-server-bridging-the-gap-between-ai-models-and-seo-data - retrieved 2026-06-26
- MCP vs. REST (WorkOS engineering blog) - https://workos.com/blog/mcp-vs-rest - retrieved 2026-06-26
- DataForSEO MCP Server (TypeScript) - repo + README - https://github.com/dataforseo/mcp-server-typescript - retrieved 2026-06-26
- Official DataForSEO Python Client (GitHub) - https://github.com/dataforseo/PythonClient - retrieved 2026-06-26
- DataForSEO API v3 - Authentication - https://docs.dataforseo.com/v3/auth/ - retrieved 2026-06-26
