# dw_us.dws_disty_brpt_cust_mtd

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dw_us.dws_disty_brpt_cust_mtd
- domain: b-report-us
- one_line_purpose: Customer-level B Report P&L and goals MTD serving table (cust + territory + sales hierarchy grain)

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dw_us.dws_disty_brpt_cust_mtd`
- Layer: DWS
- Canonical/Derived: Derived aggregation/serving
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dw_us.dws_disty_brpt_cust_mtd`

### Grain, Scope, Exclusions

- Grain: one row per (`date_flag`, `cust_no`, `mcust_no`, `cust_terr`, `cust_type`, `division`, `terr_sub_group`, `terr_group`, sales hierarchy IDs, `company_no`) with MTD-cumulative measures through `date_flag`.
- Scope: US disty B Report customer profitability, backorder/open-order aging, run-rate, and sales goals.
- Exclusions: Non-US schemas, backup/temp variants (`_bkp`, `_temp`); goal-only rows may appear when `table_goal` has targets without shipped P&L (`cust_no` coalesced to -3).

### Cross-Engine Presence

- Hive: min `2024-10-23`, max `2026-01-31`, count `182,866` (June 2026 probe).
- Vertica: min `2022-12-31`, max `2026-06-22`, count `3,496,784` (June 2026 probe).
- Vertica holds full historical range; Hive tail is materially shorter — prefer Vertica for production dashboards and cross-month history.
- Sync path: `hive2vertica_dws_disty_brpt_cust_mtd` in `brpt_customer_loading_us` / `refresh_goal_hourly_us` (daily `date_flag` overwrite).

### Column Catalog (100% columns)

- documented_column_count: 145
- catalog_status: complete

| column_name | data_type | nullable | column_comment | semantic_role |
| --- | --- | --- | --- | --- |
| month_no | int | engine metadata not exposed | — | key |
| cust_no | int | engine metadata not exposed | — | key |
| cust_name | varchar(100) | engine metadata not exposed | — | dimension |
| mcust_no | int | engine metadata not exposed | — | key |
| mcust_name | varchar(100) | engine metadata not exposed | — | dimension |
| cust_terr | int | engine metadata not exposed | — | dimension |
| terr_name | varchar(100) | engine metadata not exposed | — | dimension |
| cust_type | int | engine metadata not exposed | — | dimension |
| cust_type_desc | varchar(100) | engine metadata not exposed | — | dimension |
| division | int | engine metadata not exposed | — | dimension |
| division_desc | varchar(100) | engine metadata not exposed | — | dimension |
| terr_sub_group | int | engine metadata not exposed | — | dimension |
| sub_group_desc | varchar(100) | engine metadata not exposed | — | dimension |
| terr_group | int | engine metadata not exposed | — | dimension |
| terr_group_desc | varchar(100) | engine metadata not exposed | — | dimension |
| sales_rep_id | int | engine metadata not exposed | — | key |
| sales_sup_id | int | engine metadata not exposed | — | key |
| sales_mgr_id | int | engine metadata not exposed | — | key |
| sales_dir_id | int | engine metadata not exposed | — | key |
| sales_vp_id | int | engine metadata not exposed | — | key |
| company_no | int | engine metadata not exposed | — | key |
| gross_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| net_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| gross_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| net_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| scm_usage | numeric(20,8) | engine metadata not exposed | — | dimension |
| ds_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| stock_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| ds_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| stock_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| ds_scm_usage | numeric(20,8) | engine metadata not exposed | — | dimension |
| stock_scm_usage | numeric(20,8) | engine metadata not exposed | — | dimension |
| total_unit | int | engine metadata not exposed | — | measure |
| total_weight | numeric(20,8) | engine metadata not exposed | — | measure |
| net_income | numeric(20,8) | engine metadata not exposed | — | dimension |
| invest_capital | numeric(20,8) | engine metadata not exposed | — | dimension |
| cgp | numeric(20,8) | engine metadata not exposed | — | dimension |
| total_btl | numeric(20,8) | engine metadata not exposed | — | measure |
| tgm_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| gm_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| ngm_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| oplgm_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| bo_gross_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| bo_gross_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| bo_total_unit | int | engine metadata not exposed | — | measure |
| bo_gm_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| so_gross_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| so_gross_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| so_total_unit | int | engine metadata not exposed | — | measure |
| so_gm_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| bo_age0_7 | numeric(20,8) | engine metadata not exposed | — | dimension |
| bo_age8_14 | numeric(20,8) | engine metadata not exposed | — | dimension |
| bo_age15_21 | numeric(20,8) | engine metadata not exposed | — | dimension |
| bo_age21_up | numeric(20,8) | engine metadata not exposed | — | dimension |
| so_age0_7 | numeric(20,8) | engine metadata not exposed | — | dimension |
| so_age8_14 | numeric(20,8) | engine metadata not exposed | — | dimension |
| so_age15_21 | numeric(20,8) | engine metadata not exposed | — | dimension |
| so_age21_up | numeric(20,8) | engine metadata not exposed | — | dimension |
| rr_unit | int | engine metadata not exposed | — | measure |
| rr_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| rr_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| rr_gm | numeric(20,8) | engine metadata not exposed | — | dimension |
| rr_ngm | numeric(20,8) | engine metadata not exposed | — | dimension |
| rr_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| rr_cgp | numeric(20,8) | engine metadata not exposed | — | dimension |
| rr_total_btl | numeric(20,8) | engine metadata not exposed | — | dimension |
| rr_tgm | numeric(20,8) | engine metadata not exposed | — | dimension |
| ap_finance | numeric(20,8) | engine metadata not exposed | — | dimension |
| inv_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| inv_reserve | numeric(20,8) | engine metadata not exposed | — | dimension |
| cr_risk_cterm | numeric(20,8) | engine metadata not exposed | — | dimension |
| flr_synnex | numeric(20,8) | engine metadata not exposed | — | dimension |
| direct_credit | numeric(20,8) | engine metadata not exposed | — | dimension |
| csgn_edi_fee | numeric(20,8) | engine metadata not exposed | — | dimension |
| corporate | numeric(20,8) | engine metadata not exposed | — | dimension |
| sfs | numeric(20,8) | engine metadata not exposed | — | dimension |
| scm_risk | numeric(20,8) | engine metadata not exposed | — | dimension |
| flr_vendor | numeric(20,8) | engine metadata not exposed | — | dimension |
| cust_finance_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| cust_pmt_disc | numeric(20,8) | engine metadata not exposed | — | dimension |
| cvr_rm | numeric(20,8) | engine metadata not exposed | — | dimension |
| ar_fin_recovery | numeric(20,8) | engine metadata not exposed | — | dimension |
| mfg_oh | numeric(20,8) | engine metadata not exposed | — | dimension |
| cust_finance | numeric(20,8) | engine metadata not exposed | — | dimension |
| rma | numeric(20,8) | engine metadata not exposed | — | dimension |
| hc_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| order_overhead | numeric(20,8) | engine metadata not exposed | — | dimension |
| margin_share | numeric(20,8) | engine metadata not exposed | — | dimension |
| ap_adj | numeric(20,8) | engine metadata not exposed | — | dimension |
| pdt | numeric(20,8) | engine metadata not exposed | — | dimension |
| scm_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| infrastructure | numeric(20,8) | engine metadata not exposed | — | dimension |
| marketing | numeric(20,8) | engine metadata not exposed | — | dimension |
| coop | numeric(20,8) | engine metadata not exposed | — | dimension |
| one_time_btl | numeric(20,8) | engine metadata not exposed | — | dimension |
| hbtl | numeric(20,8) | engine metadata not exposed | — | dimension |
| scm_profit_adj | numeric(20,8) | engine metadata not exposed | — | dimension |
| hc_pm | numeric(20,8) | engine metadata not exposed | — | dimension |
| hc_bd | numeric(20,8) | engine metadata not exposed | — | dimension |
| btl | numeric(20,8) | engine metadata not exposed | — | dimension |
| btl_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| btl_backout | numeric(20,8) | engine metadata not exposed | — | dimension |
| cust_rebate | numeric(20,8) | engine metadata not exposed | — | dimension |
| mof | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_out_load | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_out_exp | numeric(20,8) | engine metadata not exposed | — | dimension |
| whoh_pack | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_ob_recovery | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_ib_recovery | numeric(20,8) | engine metadata not exposed | — | dimension |
| others | numeric(20,8) | engine metadata not exposed | — | dimension |
| others_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| scm_disc | numeric(20,8) | engine metadata not exposed | — | dimension |
| scm_ndisc | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_in | numeric(20,8) | engine metadata not exposed | — | dimension |
| trans_btl | numeric(20,8) | engine metadata not exposed | — | dimension |
| trans_btl_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| btl_sales_for_opl | numeric(20,8) | engine metadata not exposed | — | measure |
| trans_btl_sales_for_opl | numeric(20,8) | engine metadata not exposed | — | measure |
| pdt_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| cust_rebate_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| cvr_rm_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| btl_backout_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| cust_pmt_disc_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| cust_finance_sales_for_opl | numeric(20,8) | engine metadata not exposed | — | measure |
| rma_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| ar_fin_recovery_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| order_overhead_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_out_exp_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| frt_ob_recovery_for_opl | numeric(20,8) | engine metadata not exposed | — | dimension |
| etl_timestamp | timestamp | engine metadata not exposed | — | technical |
| goal_nsales | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_gm | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_ngm | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_opl_gm | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_tgm | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_dos | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_pdt | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_total_btl | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_cust_cnt | int | engine metadata not exposed | — | measure |
| fx_cost | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_soft_sales | numeric(20,8) | engine metadata not exposed | — | measure |
| date_flag | date | engine metadata not exposed | — | key |
| oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| rr_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | measure |
| goal_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | measure |


### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_mtd`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: `dws_disty_brpt_cust_mtd.py` (sum by customer keys)
  - table_fqn: `dw_us.dwd_disty_sales_report_goal_view`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: `dws_disty_brpt_cust_mtd.py` (`table_goal` CTE)
  - table_fqn: `dim_us.dim_pub_customer_info_df`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `dws_disty_brpt_cust_mtd.py` (cust_name, mcust_name)
  - table_fqn: `dim_us.dim_pub_sales_territory_df`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: territory and sales-manager hierarchy joins
- downstream_n_hops:
  - table_fqn: `dw_us.dws_disty_brpt_cust_comb_mtd`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: `dws_disty_brpt_cust_comb_mtd.py`
  - table_fqn: `dw_us.dws_disty_brpt_terr_mtd`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: `dws_disty_brpt_terr_mtd.py`
  - table_fqn: `dm_us.dm_disty_brpt_sales_mtd`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: `dm_disty_brpt_sales_mtd.py`
- lineage_last_verified_at: 2026-06-23
- lineage_confidence: high (Compass graph + BAF ETL chain aligned)

### Column Lineage and Derivation

- `month_no`: `${month_no}` from job parameter mapped to `dim_us.dim_pub_date.m` for `date_flag`.
- Core measures (`net_sales`, `gm_amt`, `ngm_amt`, `oplgm_amt`, `total_btl`, P&L components): `SUM(...)` from `dw_us.dws_disty_brpt_pl_extend_mtd` grouped by customer dimension keys for `date_flag = '${date_flag}'`.
- Goal columns (`goal_*`): aggregated from `dw_us.dwd_disty_sales_report_goal_view` where `period = ${month_no}` and `goal_type = 'NORMAL'`, full-joined to P&L on `cust_no`, `cust_terr`, `cust_type`, `division`, `company_no`.
- Denormalized labels (`cust_name`, `mcust_name`, `terr_name`, hierarchy desc fields): left joins to `dim_pub_customer_info_df`, `dim_pub_sales_territory_df`, ODS territory/cust-type/division tables as of `date_flag`.
- `mcust_no` on goal rows: taken from `dim_pub_customer_info_df`, not goal table (goal `master_cust_no` is intentionally ignored in ETL comment).


### Freshness and Load Path

- Producer jobs: `dws_disty_brpt_cust_mtd` in `brpt_customer_loading_us` (after `dws_disty_brpt_pl_extend_mtd`) and `refresh_goal_hourly_us` (goal refresh cadence).
- Expected completion window: `06:00-08:30 PT` after daily B-report common load; goal columns may refresh on `08:30-18:30 PT` hourly cadence from `refresh_goal_hourly_us`.
- Load pattern: Spark SQL overwrite partition `date_flag`; Vertica sync via `hive2vertica_dws_disty_brpt_cust_mtd`.
- Freshness confidence: medium (schedule-derived; execution history not re-profiled this run).

## L2 Declarative Knowledge

### Business Definitions

- Domain: US B Report customer profitability, goals, and sales-territory performance at MTD grain.
- Trust tier: governed serving (customer slice of B Report P&L ontology: BTL/PDT/NGM/OPL/TGM and related adjustments).
- Key metrics: `net_sales`, `gross_sales`, `gm_amt`, `tgm_amt`, `ngm_amt`, `oplgm_amt`, `oplgm_plus_amt`, `total_btl`, plus `goal_*` variance columns.
- Compass catalog description: P&L summary by dt_month + cust_no level.

### Dimension Keys and Lookup Reference

- dimension_key_column: `cust_no`
  - referenced_dimension_table_fqn: `dim_us.dim_pub_customer_info`
  - join_condition_template: `serving.cust_no = dim.cust_no` (names denormalized on serving table)
  - recommended_lookup_attributes: `cust_name`, `cust_type`, `status`
  - cardinality_expectation: many:1
  - association_confidence: high
  - cross_domain_flag: false
- dimension_key_column: `mcust_no`
  - referenced_dimension_table_fqn: `dim_us.dim_pub_customer_info`
  - join_condition_template: `serving.mcust_no = dim.cust_no`
  - recommended_lookup_attributes: `cust_name` as `mcust_name`, master/sub hierarchy
  - cardinality_expectation: many:1
  - association_confidence: high
  - cross_domain_flag: false
- dimension_key_column: `cust_terr`
  - referenced_dimension_table_fqn: `dim_us.dim_pub_sales_territory`
  - join_condition_template: `serving.cust_terr = dim.sales_terr AND serving.date_flag = dim.date_flag` (when using `_df` snapshot)
  - recommended_lookup_attributes: `terr_name`, `sub_group_id`, `group_id`
  - cardinality_expectation: many:1
  - association_confidence: high
  - cross_domain_flag: false
- dimension_key_column: `sales_rep_id`
  - referenced_dimension_table_fqn: `dim_us.dim_pub_sales_rep_terr_df`
  - join_condition_template: primary rep on `cust_terr` for `date_flag`
  - recommended_lookup_attributes: `sales_rep_name`, `manager_id` chain via `dim_pub_sales_mgr_dept_df`
  - cardinality_expectation: many:1
  - association_confidence: medium
  - cross_domain_flag: false

### Time Field Semantics

- `date_flag`: business date; primary filter field. Sample range Vertica: `2022-12-31` to `2026-06-22`.
- `month_no`: internal fiscal period index (`dim_us.dim_pub_date.m`); **not** YYYYMM. Observed range: `360`–`402` (43 distinct values).
- MTD measure columns: month-to-date cumulative through each `date_flag`; for closed-month totals use the last `date_flag` in the calendar month only.
- Goal columns refresh with `refresh_goal_hourly_us`; P&L measures follow `dws_disty_brpt_pl_extend_mtd` daily load.

### Metrics Served

- net_sales: canonical formula in `metric-index.md`
- gross_sales: canonical formula in `metric-index.md`
- gm_amt: canonical formula in `metric-index.md`
- tgm_amt: canonical formula in `metric-index.md`
- ngm_amt: canonical formula in `metric-index.md`
- oplgm_amt: canonical formula in `metric-index.md`
- oplgm_plus_amt: canonical formula in `metric-index.md`
- total_btl: canonical formula in `metric-index.md`

## L3 Procedural Knowledge

### Query and Routing Rules

- Prefer this table for customer / master-customer / territory / sales-hierarchy profitability and goal variance at MTD grain.
- Master-customer filter: `mcust_name` (or `mcust_no` when known). Sub-customer ranking/breakdown: **GROUP BY `cust_no`**, display `MAX(cust_name)`; never GROUP BY `cust_name` alone (names are not unique). See golden `b-report-us#cdw-sub-customer-ranking` and `domain-knowledge.md` Entity Key Registry.
- Fall back to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` for order-line audit, vendor/SKU cuts, or formula debugging.
- Fall back to `dw_us.dws_disty_brpt_cust_comb_mtd` when the question needs cm/pm/ppm/lm period columns on one row.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary keys: `date_flag` + customer grain (`cust_no`, `mcust_no`, `cust_terr`, `cust_type`, `division`, territory group keys, sales hierarchy IDs).
- `cust_name` / `mcust_name` are denormalized — avoid re-joining `dim_pub_customer_info` unless validating drift.
- High-risk pitfall: summing MTD rows across multiple `date_flag` values within the same month double-counts cumulative measures.

### Key Filters and ETL Business Logic

- Upstream P&L already reflects shipped-order scope from `dws_disty_brpt_pl_extend_mtd` (sourced from order-line fact with `dim_pub_order_type.sales = 'Y'`).
- Goal join: `goal_type = 'NORMAL'`, `period = month_no`, `cust_no <> 0`; full join preserves goal-only customers.
- Goal join intentionally omits `terr_sub_group` / `terr_group` on join keys to avoid duplicate rows from dirty goal data (ETL comment in script).
- `mcust_no` for goal rows comes from `dim_pub_customer_info_df`, not the goal table.
- Technical sync: `hive2vertica` uses `where date_flag = '${date_flag}'` only — not a business filter.

### Standard Time-Filter SQL (3 snippets)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date subquery only
-->
```sql
SELECT SUM(t.ngm_amt) AS ngm_amt, SUM(t.net_sales) AS net_sales
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN (
  SELECT date_flag,
         ROW_NUMBER() OVER (ORDER BY date_flag DESC) AS rn
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
) d ON t.date_flag = d.date_flag AND d.rn = 1;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: fiscal_month
anti_use: fiscal breakdown only; not sub-customer ranking
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN dim_us.dim_pub_date f
  ON t.date_flag = f.date_flag
WHERE f.fyear = 2026
  AND f.month IN (1, 2)
GROUP BY f.fyear, f.month
ORDER BY f.fyear, f.month;
```

3) Recent N-month trend without double counting

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: month_start
anti_use: trend pattern only; not entity breakdown
-->
```sql
SELECT d.month_start, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN (
  SELECT date_flag,
         date_trunc('MM', date_flag) AS month_start,
         ROW_NUMBER() OVER (PARTITION BY date_trunc('MM', date_flag) ORDER BY date_flag DESC) AS rn
  FROM dim_us.dim_pub_date
  WHERE date_flag >= add_months(current_date, -6)
) d
  ON t.date_flag = d.date_flag
WHERE d.rn = 1
GROUP BY d.month_start
ORDER BY d.month_start;
```

### Metric Selection Guidance

- Use this table for dashboard and period-comparison queries when dimensions match.
- Use DWD base for formula debugging, order_type adjustments, and transaction-level audit.
- Canonical metric formulas and routing: see `metric-index.md`.

## L4 Validation

### Data Quality Checks

- Verify row counts and `date_flag` coverage after each monthly close (compare Hive vs Vertica tail dates).
- Check `cust_no` / `mcust_no` match rates against `dim_us.dim_pub_customer_info` on sample `date_flag`.
- Monitor null or sentinel `-3` rates on hierarchy keys (`sales_rep_id`, `terr_sub_group`) after dimension snapshot joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).

### Metric Recompute Spot-Checks

- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.

### Conflicts and Open Questions

- Conflict item:
  - claim_a: Multiple pre-aggregated tables may serve same metric at different slices/grains.
  - claim_b: Routing precedence across sibling tables not explicitly documented.
  - status: Needs Clarification
  - user_decision: awaiting governed routing precedence confirmation
- Open: goal-vs-actual variance when goal rows exist without matching P&L rows (full join branch) not yet baselined by month.

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

- Consumers: PM, Sales, Buyer, BD and executive analysis views.
- Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards.

### Representative Query Patterns

Golden reference: `golden-questions.md` → `cdw-sub-customer-ranking` (routing-certified).

<!-- sql-artifact
snippet_type: routing_certified
intent: ranking
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: date_flag_month_end + cust_no
golden_ref: b-report-us#cdw-sub-customer-ranking
verified_at: 2026-06-23
verified_engine: vertica
verified_shape: rows=16; columns=cust_no,sub_customer,net_sales
anti_use: do not GROUP BY cust_name; golden SQL copy only
-->
```sql
-- Sub-customer net sales ranking under a master customer (month-end snapshot)
SELECT t.cust_no,
       MAX(t.cust_name) AS sub_customer,
       SUM(t.net_sales) AS net_sales
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN (
  SELECT date_flag,
         ROW_NUMBER() OVER (ORDER BY date_flag DESC) AS rn
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-04-01' AND date_flag < '2026-05-01'
) d ON t.date_flag = d.date_flag AND d.rn = 1
WHERE t.mcust_name = 'CDW LOGISTICS'
GROUP BY t.cust_no
ORDER BY net_sales DESC
LIMIT 20;
```

<!-- sql-artifact
snippet_type: illustrative
intent: audit
table_fqn: dw_us.dws_disty_brpt_cust_mtd
anti_use: daily date_flag scan only; not for ranking or month-end KPI
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt, SUM(net_sales) AS net_sales
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```