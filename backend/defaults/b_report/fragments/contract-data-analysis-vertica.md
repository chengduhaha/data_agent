# Contract Data Analysis — Vertica and MCP Rules

Apply when using **contract-guided-data-analysis** skill (not for general questions or email/ETL intake).

## Local-first prerequisite

Complete routing from `/knowledge/org/source/contracts/{domain}/`, `/knowledge/org/source/ref/{domain}/`, WKB `l1_catalog`, and `/knowledge/org/target/knowledgebase/{domain}/` before any MCP.

- **Never** read `source/contracts/**/golden-questions.md`
- **Never** read `source/contracts/b-report-us/tables/**` or `source/contracts/pos/tables/**`
- **Never** use Vertica metadata tools for schema discovery
- **Never** read `/workspace/target/analysis/**` for SQL shape (output-only artifacts)

## Vertica MCP (execution only)

**Server:** `gateway-vertica-prod`

| Allowed | Forbidden |
|---------|-----------|
| `run_query_safely` (default `row_threshold=1000`) | Schema/metadata discovery |
| `execute_query_paginated` (rare) | Exploratory `SELECT *` for learning schema |

### Query shape

- SELECT-only; partition-filtered (`date_flag`, etc.) from contract L3 / domain-knowledge Time Scope Ontology
- **Calendar month MTD:** month-end `date_flag` snapshot — resolve via `dim_us.dim_pub_date` using `MAX(date_flag)` over a calendar month `date_flag` range; **do not** use `month_flag = 'Y'`
- **Customer ranking:** `SUM(ifnull(ngm_amt,0))` + `GROUP BY cust_no`, `WHERE cust_no > 0` — aggregate before period pivot (territory sub-rows exist)
- **MoM ranking:** default **`ORDER BY mom_pct ASC`** for "MoM Top N"; use `DESC` only when user asks for increase/growth
- **P&L items (NGM):** wide component columns from `metric-index.md` `ngm_amt` formula (`gm_amt`, `btl`, `ap_finance`, `cust_rebate`, etc.) — **not** `pl_item`; not VPL unless user requests product line
- **Vendor MTD:** prefer `dws_disty_brpt_vend_mtd` (not `*_comb_mtd`) with `SUM(ifnull(col,0))` + `GROUP BY vend_no` for month-end comparisons
- **Company-wide P&L variance:** `dws_disty_brpt_pl_extend_mtd`, sum components per month-end `date_flag`, rank by `ABS(apr - mar)` per component
- **Forbidden:** `month_flag = 'Y'` on `dim_pub_date` — use `MAX(date_flag)` per calendar month instead
- Aggregate-first: `SUM(ifnull(col,0))`, `GROUP BY`, `LIMIT` for rankings
- **b-report-us order filters (non-default):** do **not** apply `dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1` unless the question explicitly asks for shipped orders only. For DWD profitability pulls, still use `segment_exclude = 'N'` per `/knowledge/org/source/ref/b-report-us/special_logic.txt`.
- `dw_us.dwd_disty_brpt_orders_pl_etl_mi`: always `segment_exclude = 'N'`, `virtual_type = 0`, `dim_pub_order_type.sales = 'Y'`

### Zero rows

Report **no data found** with scope; do not hop domains or run metadata discovery.

## Agent efficiency (data_agent chat)

- Do **not** use the `task` tool / subagents for contract-guided analysis — run evidence SQL in the main agent.
- Minimize graph steps: batch `read_file` for contract references; do not re-read the same path in one turn unless content changed.
- Prefer one well-scoped `run_query_safely` per evidence need over many small probe queries.
