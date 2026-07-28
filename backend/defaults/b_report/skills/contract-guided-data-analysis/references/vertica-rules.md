# Contract Data Analysis — Vertica and MCP Rules

Apply when using **contract-guided-data-analysis** skill or writing `{output_dir}/**` artifacts.

## Clarification before routing

Before local metric/table routing finalization, evidence SQL, three-section answers, or `{output_dir}/**`:

1. Apply [`analysis-clarification.md`](analysis-clarification.md) and [`output-contract.md`](output-contract.md) § Ambiguity Handling.
2. Ask only when a **hard routing slot** is missing (time when `user_must_specify`, unresolved business term, true entity/metric name clash, vague “item” with multiple pack meanings, ranking sense when baseline is undefined and material, grouping definition, entity/scope, population/filter scope). → **ask the user and stop**. Do not invent defaults (e.g. do not assume “less” means top-N lowest). Do **not** ask for breakdown dimension on attribution / root-cause — proceed with multi-angle exploration unless another hard slot is open. If the question already states hard slots clearly, proceed.
3. Never ask for KB-owned technical facts (tables, formulas, flows, joins, `segment_exclude`, vendor key choice) — resolve from pack or fail closed.

## Local-first prerequisite

Complete routing from `knowledge/contracts/{domain}/`, `knowledge/ref/{domain}/` (special logic), and `knowledge/storage/wkb/` (`l1_catalog` metadata) before any MCP. Prefer **embedded** KB L2/L3 special-logic / relationship maps when present on the resolved table doc.

- **Never** read `knowledge/contracts/**/golden-questions.md`
- **Never** read `knowledge/contracts/b-report-us/tables/**` or `knowledge/contracts/pos/tables/**`
- **Never** use Bitbucket MCP for table/metric/schema discovery
- **Never** use Vertica metadata tools (`get_table_structure`, `get_schema_tables`, `get_schema_views`, `get_table_projections`, `get_database_schemas`)
- **Always** check `knowledge/ref/{domain}/special_logic.txt` for the resolved table(s) when that file exists for the domain

## Vertica MCP (execution only)

**Server:** `vertica-prod`

| Allowed | Forbidden |
|---------|-----------|
| `run_query_safely` (default `row_threshold=1000`) | Schema/metadata discovery |
| Bounded `execute_query_paginated` for small replays | Exploratory `SELECT *` for learning schema |
| Phase-1 dim label probe (`LIMIT 20`) on contract-named columns | Inferring joins/metrics not in local md |

### Query shape

- **SELECT-only**; partition-filtered from contract L3 (`date_flag`, etc.)
- **Aggregate-first:** `SUM(ifnull(col,0))`, `COUNT`, `GROUP BY`, `LIMIT` for rankings/trends
- **Exception:** explicit anomaly / top-N order-line requests (bounded rows, no summarization required)
- **b-report-us order filters (non-default):** do **not** apply `dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1` unless the question explicitly asks for shipped orders only (or that specific scope). For DWD profitability pulls, still use `segment_exclude = 'N'` per `knowledge/ref/b-report-us/special_logic.txt`.

### Zero rows

Return **no data found** with scope; do not hop domains or discover schema.

## Bitbucket MCP

- **Forbidden** for analysis research
- **Allowed** only when user explicitly requests ETL source and local WKB/knowledgebase already names the file path

## WKB intents (this skill)

Use only: `nl2sql_metric`, `find_table_schema`, `data_engineering`. Do not use `incident_debug`.

## Analysis output

- Path: `{output_dir}/{slug}_{YYYYMMDD}.md`
- Set `external_mcp_research: none` unless documented Bitbucket exception
- Set `result_status: data_found | no_data_found`
- Cite `metric-index.md` metric ids; never cite `golden-questions.md`

## RDS report generation (`rds_report_generation`)

When the question is **RDS SQL / report generation** (not KPI-only lookup on an RDS pack), load [`rds-report-sql.md`](rds-report-sql.md) as a short mode pointer before compiling deliverable SQL:

1. Read and apply [`rds-report-sql.md`](rds-report-sql.md) for intent detection, rule-load order, and deliverable shape.
2. Deliverable shape: working `CREATE LOCAL TEMP TABLE tmp_<step>_<region>_<report#> ON COMMIT PRESERVE ROWS AS` steps, then `rdsetl.rds_tmp` + `rdsetl.rds_tmp_body` (StarRocks: `tempdb.*` only if requested). Drop working `tmp_*` after deliverables.
3. **Evidence CTE extracts / large multi-CTE SELECT scripts are not valid RDS report deliverables.**
4. Vertica MCP remains SELECT aggregate / count **validation only**. Do not execute DDL that creates `rdsetl.rds_tmp` on prod via MCP unless the user explicitly asks.
5. User-facing answer **must** include the final fenced report SQL for this mode; standard KPI paths still must not paste SQL.

This skill does **not** embed the RDS dialect / temp-table / formatting / region-routing rule bodies — those live in the host environment's own RDS tooling (e.g. Cursor `rds-*.mdc` rules) when available.

See [`vertica-query.md`](vertica-query.md) and [`local-research-first.md`](local-research-first.md).
