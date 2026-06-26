# Source Map

## Raw Sources

- DataForSEO v3 documentation pages, free sandbox response samples, cost-capped live API response fixtures, and the seo-dataforseo MCP tool catalog and cost tiers

## Enrichment Sources

- Official docs.dataforseo.com/v3 documentation
- dataforseo.com pricing page and help center
- Official DataForSEO MCP server repository

## Import Strategy

- Copy raw source files into `.raw/sources/`.
- Record path, hash, retrieval date, owner, and source type.
- Record external research sources in `references/source-ledger.json`.
- Record implemented schemas and adapters in `references/adapter-manifest.json`.
- Create a source note under `wiki/sources/`.
- Link affected entities, workflows, and deliverables.
