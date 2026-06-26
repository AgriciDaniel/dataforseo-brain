# DataForSEO Brain Adapter Plan

Status: required before domain-adapted maturity.

## Raw Input Types

- DataForSEO v3 documentation pages, free sandbox response samples, cost-capped live API response fixtures, and the seo-dataforseo MCP tool catalog and cost tiers

## Required Implementation

- Define one schema per raw input type.
- Build at least one real domain importer or ingestion path.
- Build one domain-specific synthesis module.
- Build one report renderer with source citations.
- Add sanitized fixtures and tests for every supported input type.

## Safety Refusals

- No endpoint, parameter, cost, or auth claim without a current official docs citation
- No credentials, tokens, or .env values in any repo artifact; secrets stay in ~/Desktop/Keys
- No live billable API call beyond the operator-approved $5 cap; track spend via the user_data endpoint and hard-stop
- No irreversible recommendation without owner, confidence, source, and rollback note

## Completion Gate

This plan is complete only when domain-specific importer, synthesis, report,
fixtures, and tests replace the generic scaffold.
