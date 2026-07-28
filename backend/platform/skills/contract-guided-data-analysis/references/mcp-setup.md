# Vertica MCP Setup

This skill requires a **Vertica MCP server** for execution-only SQL. Schema discovery via MCP is **forbidden** — all routing comes from bundled `knowledge/`.

## Required tools

| Tool | Purpose |
|------|---------|
| `run_query_safely` | Default evidence queries (aggregate-first, row threshold) |
| `execute_query_paginated` | Optional bounded replay of small result sets |

## Forbidden MCP tools

Do not use for this skill:

- `get_table_structure`
- `get_schema_tables`
- `get_schema_views`
- `get_table_projections`
- `get_database_schemas`

## Cursor

Add to `.cursor/mcp.json` (or user MCP settings):

```json
{
  "mcpServers": {
    "vertica-prod": {
      "url": "https://your-vertica-gateway.example/mcp",
      "headers": {
        "Authorization": "Bearer ${VERTICA_API_KEY}"
      }
    }
  }
}
```

Set environment variables per your org gateway docs (`VERTICA_HOST`, `VERTICA_DATABASE`, `VERTICA_USER`, `VERTICA_PASSWORD`, etc.).

## Claude Code / Codex / other agents

1. Install this skill zip into the agent's skills directory
2. Register the same Vertica MCP server your org provides
3. Ensure the agent can call `run_query_safely` — name may vary (`gateway-vertica-prod`, `vertica-prod`, `vertica-prod`); map to your deployment

## Execution rules

Full policy: [`vertica-rules.md`](vertica-rules.md)

- SELECT-only, partition-filtered from contract L3
- Aggregate-first: `SUM`, `COUNT`, `GROUP BY`, bounded `LIMIT`
- Zero rows → report **no data found**; do not broaden scope silently
