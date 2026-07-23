# dm_us.dm_disty_brpt_pm_mtd

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dm_us.dm_disty_brpt_pm_mtd
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (mtd) by business slice

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dm_us.dm_disty_brpt_pm_mtd`
- Layer: DM
- Canonical/Derived: Derived aggregation/serving
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dm_us.dm_disty_brpt_pm_mtd`

### Grain, Scope, Exclusions

- Grain: month-to-date cumulative through each date_flag
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
| month_no | int | engine metadata not exposed | — | 1 | month_no from dim_pub_date.m | key | month_no from dim_pub_date.m | integer | not_null_expected | Internal fiscal month index from `dim_us.dim_pub_date.m`. | `dim_us.dim_pub_date.m` |
| pm_id | int | engine metadata not exposed | — | 2 | PM id | key | PM id | integer | not_null_expected | Product manager identifier at PM MTD serving grain. | — |
| pm_name | string | engine metadata not exposed | — | 3 | PM name | dimension | PM name | categorical | domain_value_check_recommended | Denormalized PM display name. | — |
| pm_mgr_id | int | engine metadata not exposed | — | 4 | PM manager id | key | PM manager id | integer | not_null_expected | PM manager hierarchy key. | — |
| pm_manager_name | string | engine metadata not exposed | — | 5 | PM manager name | dimension | PM manager name | categorical | domain_value_check_recommended | Denormalized manager name. | — |
| pm_dir_id | int | engine metadata not exposed | — | 6 | PM director id | key | PM director id | integer | not_null_expected | PM director hierarchy key. | — |
| pm_director_name | string | engine metadata not exposed | — | 7 | PM director name | dimension | PM director name | categorical | domain_value_check_recommended | Denormalized director name. | — |
| pm_vp_id | int | engine metadata not exposed | — | 8 | PM vp id | key | PM vp id | integer | not_null_expected | PM VP hierarchy key. | — |
| pm_vp_name | string | engine metadata not exposed | — | 9 | PM vp name | dimension | PM vp name | categorical | domain_value_check_recommended | Denormalized VP name. | — |
| seg_code | string | engine metadata not exposed | — | 10 | vendor segment code | dimension | vendor segment code | categorical | domain_value_check_recommended | Vendor segment on PM slice. | — |
| company_no | int | engine metadata not exposed | — | 11 | company_no | key | company_no | integer | not_null_expected | Company partition key. | — |
| goal_nsales | decimal(20,8) | engine metadata not exposed | — | 12 | Nsales Goal | measure | Nsales Goal | decimal_currency_or_ratio | non_negative_expected | Goal target for net sales at PM grain. | — |
| goal_gm | decimal(20,8) | engine metadata not exposed | — | 13 | GM goal | measure | GM goal | decimal_currency_or_ratio | non_negative_expected | Goal target for gross margin. | — |
| gross_sales | decimal(20,8) | engine metadata not exposed | — | 14 | sum from part_mtd | measure | gross sales | decimal_currency_or_ratio | non_negative_expected | MTD cumulative gross sales at PM grain. | — |
| net_sales | decimal(20,8) | engine metadata not exposed | — | 15 | sum from part_mtd | measure | net sales | decimal_currency_or_ratio | non_negative_expected | MTD cumulative net sales at PM grain; alias revenue in golden Q4. | — |

### Lineage

(N-degree)
- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: dw_us.dws_disty_brpt_part_mtd
  - hop: 1
  - relation_type: aggregate
  - via_job_or_view: brpt_product_loading
- downstream_n_hops:
  - table_fqn: dm_us.dm_disty_brpt_pm_mtd
  - hop: 0
  - relation_type: serving
  - via_job_or_view: B Report PM mart load
- lineage_last_verified_at: 2026-06-22T05:16:14Z
  - source_type: compass
  - confidence: low
- lineage_notes:
  - Compass catalog lookup executed first; CK lineage used as fallback evidence.
### Column Lineage and Derivation
- column_lineage:
  - column_name: key_metric_bundle
  - lineage_type: derived
  - source_columns:
    - source_table: —
    - source_column: —
  - derivation_formula: delete from dw_${country}.dws_disty_brpt_pl_extend_mtd              where date_flag between '${ago_91_days_month_start}' and '${ago_91_days}';
  - etl_sql_ref:

### Freshness and Load Path

- Expected completion window: 03:00-03:20 PT (America/Los_Angeles) for core disty B-report daily/addition flows
- Load pattern: Azkaban-scheduled Spark SQL ETL with Hive write and Vertica sync
- Freshness note: aggregated `*_mtd`/`*_comb_mtd` tables refresh daily; detail fact may show Hive/Vertica date lag

## L2 Declarative Knowledge

### Business Definitions

- Domain: US B Report shipped-order profitability and operating performance analytics.
- Trust tier: governed serving
- Key context: - Business definitions: Uses B Report P&L ontology (BTL/PDT/NGM/OPL/TGM and related adjustment items).
- Key metrics or fields: net_sales, gross_sales, gm_amt, tgm_amt, ngm_amt, oplgm_amt
- Trust tier: curated

### Dimension Keys and Lookup Reference

- `cust_no` → `dim_us.dim_pub_customer_info` (`cust_name`, `cust_type`, `sales_terr`)
- `vend_no` → `dim_us.dim_pub_vendor_info` (`vend_name`, `master_vend_no`, `vend_seg_code`)
- `sku_no` → `dim_us.dim_pub_part_info` (`part_no`, `short_desc`, `vpl_no`)
- `vpl_no` → `dim_us.dim_pub_vpl_info` (`vpl_code`, `vpl_desc`, `vend_no`)
- `pm_id` → `dim_us.dim_pub_vpl_hierarchy_info` (PM/Buyer hierarchy attributes)

### Time Field Semantics

- `date_flag`: business date; primary filter field for natural-month and as-of-date queries.
- `month_no`: internal fiscal period index from `dim_us.dim_pub_date.m`; **not** YYYYMM — map via date dimension.
- `*_mtd`/`*_comb_mtd` columns: month-to-date cumulative values through `date_flag`; for month-total reporting use month-end `date_flag` row only.
- `*_1d` columns: single-day snapshot values for `date_flag`.
- `*_wtd` columns: week-to-date cumulative through `date_flag`.

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

- Prefer this table when required dimensions and time suffix match the question grain.
- Fall back to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` for order-line recalculation or missing dimensions.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary keys: —
- Common join keys: date_flag/dt_week/dt_month and entity keys (sku_no, cust_no, vend_no, vpl_no, pm, buyer, sales, BD hierarchy by table group).
- High-risk join pitfalls: Mixing 1d/wtd/mtd/comb_mtd grains in one aggregation causes double counting.

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
table_fqn: dm_us.dm_disty_brpt_pm_mtd
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dm_disty_brpt_pm_mtd
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dm_us.dm_disty_brpt_pm_mtd
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dm_disty_brpt_pm_mtd t
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
table_fqn: dm_us.dm_disty_brpt_pm_mtd
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT d.month_start, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dm_disty_brpt_pm_mtd t
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

- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
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

- Consumers: PM, Sales, Buyer, BD and executive analysis views.
- Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards.

### Representative Query Patterns

Golden reference: `golden-questions.md` → `pm-735781-revenue-jan-2026` (routing-certified).

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_lookup
table_fqn: dm_us.dm_disty_brpt_pm_mtd
grain: date_flag_month_end + pm_id
golden_ref: b-report-us#pm-735781-revenue-jan-2026
verified_at: 2026-06-24
verified_engine: vertica
verified_shape: rows=1; columns=revenue
anti_use: PM slice only; use cust_mtd for customer cuts
-->
```sql
SELECT SUM(t.net_sales) AS revenue
FROM dm_us.dm_disty_brpt_pm_mtd t
JOIN (
  SELECT MAX(date_flag) AS date_flag
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-01-01'
    AND date_flag < '2026-02-01'
) d ON t.date_flag = d.date_flag
WHERE t.pm_id = 735781;
```

<!-- sql-artifact
snippet_type: illustrative
intent: audit
table_fqn: dm_us.dm_disty_brpt_pm_mtd
anti_use: daily date_flag scan only; not routing_certified
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt, SUM(net_sales) AS net_sales
FROM dm_us.dm_disty_brpt_pm_mtd
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```