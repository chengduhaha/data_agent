# Template Domain — Query Workflow

Replace this file with domain-specific rules when creating a new domain.

## Order of Operations

1. Read `objects.yaml` to match user terms to `object_type` and logical `property` names.
2. Build Object Query DSL (logical names only).
3. Compile to SQL per skill `dsl-compile.md`.
4. Execute via MCP tool named in `domain.yaml` → `mcp_tools`.

## Domain-Specific Rules

<!-- Add rules here, e.g.: -->
<!-- - Reseller filters: OR hasSourceResellerNo and hasSourceMasterResellerNo -->
<!-- - Default fiscal calendar for quarter expansion -->
<!-- - Metric shortcuts: "renewals overall" → AgreementLineRenewalRate -->

## Answer

Ground every number in MCP query results. No LLM arithmetic.
