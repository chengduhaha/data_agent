# Vertica MCP — Execution Only

**Prerequisite:** Local research gate passed. SQL compiled from contracts / `golden_cases` / `metric-index`. Vertica is never the first source consulted.

---

## Server and tools

**Server:** `gateway-vertica-prod`

| Purpose | Tool |
|---------|------|
| Evidence queries (default) | `run_query_safely` — `row_threshold=1000` |
| Bounded paging (rare) | `execute_query_paginated` |

**Forbidden** — schema discovery:

- `get_table_structure`, `get_schema_tables`, `get_schema_views`
- `get_table_projections`, `get_database_schemas`

Grain, columns, partition keys come from `/knowledge/org/source/contracts/**` and WKB L1 snapshots.

---

## Safety rules

1. **SELECT-only** — no DDL/DML
2. **Partition-scoped** — filter `date_flag`, `dt_month`, etc. from contract L3
3. **Aggregate-first** — `SUM`, `COUNT`, `GROUP BY` + `LIMIT` for rankings/trends
4. **No wide extracts** — avoid `SELECT *` on large tables
5. **Anomaly exception** — user asks top-N order lines (e.g. 10 negative NGM orders): bounded row list allowed without extra summarization
6. **Entity Phase-1** — `SELECT` on contract-named dim varchar columns only; `LIMIT 20`

---

## Zero-row handling

If `run_query_safely` returns **zero rows** for the scoped query:

- Answer **no data found** with domain, period, and filters
- Set `result_status: no_data_found`
- Do not retry with alternate domain or schema discovery

---

## Metric aggregation pattern

```sql
SELECT
    ${group_by_cols},
    SUM(ifnull(${metric_col}, 0)) AS ${metric_alias}
FROM ${schema}.${table}
WHERE ${partition_col} IN (${resolved_period_literals})
  AND ${entity_filters}
GROUP BY ${group_by_cols}
ORDER BY ${sort_col} ${sort_dir}
LIMIT ${limit_n};
```

Use formulas from `metric-index.md` when column is computed, not physical.

---

## Entity label probe (Phase-1)

```sql
SELECT ${join_key_col}, ${label_col}
FROM ${dim_schema}.${dim_table}
WHERE ${label_col} ILIKE '%${user_token}%'
LIMIT 20;
```

Only when `domain-knowledge.md` / table ISP documents searchable varchar columns.

---

## Record in analysis artifact

Under **Vertica validation**:

| Check | SQL summary | Rows | Result |
|-------|-------------|------|--------|
| Aggregated metric | `SUM(net_sales) …` | n | value or no_data_found |

Do not paste large raw result sets. Summarize aggregates only.

---

## MCP unavailable

Report Vertica MCP unavailable; set `result_status: no_data_found` if evidence required and not obtainable. Do not use metadata tools as fallback.
