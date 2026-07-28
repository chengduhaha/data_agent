# dim_us.dim_disty_bd_project_user

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_disty_bd_project_user
- domain: b-report-us
- one_line_purpose: Shared dimension for B Report attribute enrichment and join lookups

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_disty_bd_project_user`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_disty_bd_project_user`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive (`dw_us`/`dm_us`/`dim_us`): table family present; prefer canonical name without suffix variants.
- Vertica: same schema families mirrored; Vertica may lag Hive by several days on detail facts.
- Reconciliation: compare `MIN(date_flag)`, `MAX(date_flag)`, row counts when auditing cross-engine parity.

### Column Catalog (100% columns)

- documented_column_count: 15
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| project_no | int | engine metadata not exposed | — | 1 | — | key | project no | integer | not_null_expected|dim_fk_check_recommended | project no; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| project_name | varchar(300) | engine metadata not exposed | — | 2 | — | dimension | project name | categorical_or_expression_text | domain_value_check_recommended | project name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| task_no | int | engine metadata not exposed | — | 3 | — | key | task no | integer | not_null_expected|dim_fk_check_recommended | task no; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| task_name | varchar(30) | engine metadata not exposed | — | 4 | — | dimension | task name | categorical_or_expression_text | domain_value_check_recommended | task name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_rep_id | int | engine metadata not exposed | — | 5 | — | key | bd rep id | integer | not_null_expected|dim_fk_check_recommended | bd rep id; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_rep_name | varchar(100) | engine metadata not exposed | — | 6 | — | dimension | bd rep name | categorical_or_expression_text | domain_value_check_recommended | bd rep name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_mgr_id | int | engine metadata not exposed | — | 7 | — | key | bd mgr id | integer | not_null_expected|dim_fk_check_recommended | bd mgr id; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_mgr_name | varchar(100) | engine metadata not exposed | — | 8 | — | dimension | bd mgr name | categorical_or_expression_text | domain_value_check_recommended | bd mgr name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_dir_id | int | engine metadata not exposed | — | 9 | — | key | bd dir id | integer | not_null_expected|dim_fk_check_recommended | bd dir id; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_dir_name | varchar(100) | engine metadata not exposed | — | 10 | — | dimension | bd dir name | categorical_or_expression_text | domain_value_check_recommended | bd dir name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_vp_id | int | engine metadata not exposed | — | 11 | — | key | bd vp id | integer | not_null_expected|dim_fk_check_recommended | bd vp id; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_vp_name | varchar(100) | engine metadata not exposed | — | 12 | — | dimension | bd vp name | categorical_or_expression_text | domain_value_check_recommended | bd vp name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_svp_id | int | engine metadata not exposed | — | 13 | — | key | bd svp id | integer | not_null_expected|dim_fk_check_recommended | bd svp id; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| bd_svp_name | varchar(100) | engine metadata not exposed | — | 14 | — | dimension | bd svp name | categorical_or_expression_text | domain_value_check_recommended | bd svp name; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |
| entry_datetime | timestamp | engine metadata not exposed | — | 15 | — | dimension | entry datetime | categorical_or_expression_text | domain_value_check_recommended | entry datetime; BD project/task hierarchy attribute on `dim_us.dim_disty_bd_project_user`; join on `project_no` + `task_no`. | — |


### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_bd_project_task`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `bd_dw.bd_project_user_us.load_bd_project_user`
  - table_fqn: `ods_us.ods_cis_corp_bd_project`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: project name / manager linkage
  - table_fqn: `ods_us.ods_userinfo_mymdm_bd_hierarchy`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: director / VP / SVP hierarchy IDs
- downstream_n_hops:
  - table_fqn: `dim_us.dim_disty_bd_project_user_df`
    hop: 1
    relation_type: snapshot_copy
    via_job_or_view: `dim_disty_bd_project_user_df.py` (date_flag partition)
  - table_fqn: `dw_us.dws_disty_brpt_bd_proj_task_mtd`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: BD project/task B Report marts
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high


### Column Lineage and Derivation

- `project_no` + `task_no`: composite business key from BD project task ODS.
- `bd_rep_id` / `bd_rep_name`: BD representative from project task and manager tables.
- `bd_mgr_id` through `bd_svp_id`: rolled up from `ods_userinfo_mymdm_bd_hierarchy` by division.


### Freshness and Load Path

- Producer: `bd_dw.bd_project_user_us` flow `load_bd_project_user` (B Report pre-load dependency).
- Snapshot: `brpt_common_pre_loading_us.dim_disty_bd_project_user_df` after base dimension.
- Expected completion window: 02:00-03:00 PT.


## L2 Declarative Knowledge

### Business Definitions

- Domain: BD (business development) project and task ownership hierarchy for B Report BD slices.
- Grain: one row per (`project_no`, `task_no`).
- Primary use: map BD project metrics to rep/manager/director/VP hierarchy.



### Dimension Keys and Lookup Reference

- Primary role: dimension lookup target; join from fact tables on business key columns documented in Column Catalog.

### Time Field Semantics

- Base table is current-state; use `dim_disty_bd_project_user_df` partitioned by `date_flag` for as-of joins.



### Metrics Served

- Dimension attributes only; no fact metrics stored on this table

## L3 Procedural Knowledge

### Query and Routing Rules

- Prefer this table when required dimensions and time suffix match the question grain.
- Fall back to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` for order-line recalculation or missing dimensions.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary keys: —
- Common join keys: dimension business key fields referenced by DWD/DWS/DM tables
- High-risk join pitfalls: Key type mismatch and duplicate-key expansion.

### Key Filters and ETL Business Logic

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For profitability metrics on this table, always filter `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

### Standard Time-Filter SQL (3 snippets)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_disty_bd_project_user
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dim_us.dim_disty_bd_project_user
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi t
JOIN dim_us.dim_pub_date f
  ON t.date_flag = f.date_flag
WHERE f.fyear = 2026
GROUP BY f.fyear, f.month;
```

3) Recent N-month trend without double counting

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dim_us.dim_disty_bd_project_user
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_trunc('MM', date_flag) AS month_start, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= add_months(current_date, -6)
GROUP BY date_trunc('MM', date_flag)
ORDER BY month_start;
```

### Metric Selection Guidance

- Use this table for dashboard and period-comparison queries when dimensions match.
- Use DWD base for formula debugging, order_type adjustments, and transaction-level audit.
- Canonical metric formulas and routing: see `metric-index.md`.

## L4 Validation

### Data Quality Checks

- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).

### Metric Recompute Spot-Checks

- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.

### Conflicts and Open Questions

- Conflict item:
  - claim_a: —
  - claim_b: —
  - status: Needs Clarification
  - user_decision: awaiting governed routing precedence confirmation
- Open: PM/Buyer hierarchy unmatched-rate baseline across full month window not yet decomposed by fallback branch.

## L5 Runtime View

### Query Path and Engine Preference

- Primary: Vertica `dw_us`/`dm_us` for BI dashboards (fresher on detail facts).
- Fallback: Hive for reconciliation or when Vertica unavailable.
- Metadata: domain table docs and `metric-index.md` for routing.

### Access Constraints

- Standard `dw_us`/`dm_us`/`dim_us` role-based access applies.
- No table-specific ACL exceptions documented.

## L6 Access and Consumption

### Primary Consumers and Use Cases

- Consumers: B Report semantic layer, dashboard queries, and BI users.
- Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: audit
table_fqn: dim_us.dim_disty_bd_project_user
anti_use: daily date_flag scan only; not routing_certified; do not copy for ranking
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt, SUM(net_sales) AS net_sales
FROM dim_us.dim_disty_bd_project_user
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```