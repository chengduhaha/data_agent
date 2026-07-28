# dim_us.dim_pub_order_type

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_order_type
- domain: b-report-us
- one_line_purpose: Shared dimension for B Report attribute enrichment and join lookups

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_order_type`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_order_type`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive (`dw_us`/`dm_us`/`dim_us`): table family present; prefer canonical name without suffix variants.
- Vertica: same schema families mirrored; Vertica may lag Hive by several days on detail facts.
- Reconciliation: compare `MIN(date_flag)`, `MAX(date_flag)`, row counts when auditing cross-engine parity.

### Column Catalog (100% columns)

- documented_column_count: 18
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| order_type | int | engine metadata not exposed | — | 1 | — | dimension | order type | integer | domain_value_check_recommended | order type; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| order_type_descr | varchar(200) | engine metadata not exposed | — | 2 | — | dimension | order type descr | categorical_or_expression_text | domain_value_check_recommended | order type descr; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| order_source | varchar(200) | engine metadata not exposed | — | 3 | — | dimension | order source | categorical_or_expression_text | domain_value_check_recommended | order source; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| entry_datetime | timestamp | engine metadata not exposed | — | 4 | — | dimension | entry datetime | categorical_or_expression_text | domain_value_check_recommended | entry datetime; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| entry_id | int | engine metadata not exposed | — | 5 | — | key | entry id | integer | not_null_expected|dim_fk_check_recommended | entry id; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| rec_tran_no | int | engine metadata not exposed | — | 6 | — | key | rec tran no | integer | not_null_expected|dim_fk_check_recommended | rec tran no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| rec_void_no | int | engine metadata not exposed | — | 7 | — | key | rec void no | integer | not_null_expected|dim_fk_check_recommended | rec void no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| ship_tran_no | int | engine metadata not exposed | — | 8 | — | key | ship tran no | integer | not_null_expected|dim_fk_check_recommended | ship tran no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| ship_void_no | int | engine metadata not exposed | — | 9 | — | key | ship void no | integer | not_null_expected|dim_fk_check_recommended | ship void no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| module | varchar(200) | engine metadata not exposed | — | 10 | — | dimension | module | categorical_or_expression_text | domain_value_check_recommended | module; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| issue_tran_no | int | engine metadata not exposed | — | 11 | — | key | issue tran no | integer | not_null_expected|dim_fk_check_recommended | issue tran no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| change_tran_no | int | engine metadata not exposed | — | 12 | — | key | change tran no | integer | not_null_expected|dim_fk_check_recommended | change tran no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| delete_tran_no | int | engine metadata not exposed | — | 13 | — | key | delete tran no | integer | not_null_expected|dim_fk_check_recommended | delete tran no; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| sales | varchar(200) | engine metadata not exposed | — | 14 | — | dimension | sales | categorical_or_expression_text | domain_value_check_recommended | sales; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| autocred_type | varchar(200) | engine metadata not exposed | — | 15 | — | dimension | autocred type | categorical_or_expression_text | domain_value_check_recommended | autocred type; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| invoice_type | varchar(200) | engine metadata not exposed | — | 16 | — | dimension | invoice type | categorical_or_expression_text | domain_value_check_recommended | invoice type; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| order_type_descr_alt | varchar(200) | engine metadata not exposed | — | 17 | — | dimension | order type descr alt | categorical_or_expression_text | domain_value_check_recommended | order type descr alt; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |
| pl_flag | varchar(2) | engine metadata not exposed | — | 18 | — | dimension | pl flag | categorical_or_expression_text | domain_value_check_recommended | pl flag; Order-type reference attribute on `dim_us.dim_pub_order_type`; filter `sales = 'Y'` for shipped-order P&L scope. | — |


### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_order_type`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_order_dimension_us.dim_pub_order_type`
  - table_fqn: `ods_us.ods_cis_corp_pl_code`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `pl_flag` derivation (`code_type='ORDR'`, `usage='ORDR_TYPE_PL'`)
- downstream_n_hops:
  - table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi`
    hop: 1
    relation_type: filter_join
    via_job_or_view: inner join where `sales = 'Y'` (shipped-order scope)
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 2
    relation_type: filter_join
    via_job_or_view: inherited shipped-order scope from DWD chain
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high (BAF `dim_pub_order_type.sql` + B Report filter usage)


### Column Lineage and Derivation

- `order_type`: primary key from `ods_cis_corp_order_type.order_type`.
- `sales`: shipped-order inclusion flag; B Report uses `sales = 'Y'` as core business filter.
- `pl_flag`: derived `Y` when `sales='Y'` and order type matches P&L code list (`ods_cis_corp_pl_code`); else `N`.
- Transaction number columns (`rec_tran_no`, `ship_tran_no`, etc.): pass-through CIS order-type configuration metadata.


### Freshness and Load Path

- Producer flow: `public_order_dimension_us` job `dim_pub_order_type`.
- Vertica sync: `hive2vertica_dim_pub_order_type`.
- Expected completion window: 02:00-03:30 PT.
- Table size: ~399 order types on Vertica (2026-06-24 probe).
- Freshness confidence: medium.


## L2 Declarative Knowledge

### Business Definitions

- Domain: order-type reference controlling which orders count as sales / P&L in analytics.
- Trust tier: governed reference.
- Grain: one row per `order_type`.
- B Report critical filter: `sales = 'Y'` defines shipped-order profitability scope.



### Dimension Keys and Lookup Reference

- Primary role: dimension lookup target; join from fact tables on business key columns documented in Column Catalog.

### Time Field Semantics

- Static reference dimension (no `date_flag`); changes propagate on next dimension reload.
- Use `entry_datetime` only for audit of reference updates, not for metric time filtering.



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
table_fqn: dim_us.dim_pub_order_type
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
table_fqn: dim_us.dim_pub_order_type
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
table_fqn: dim_us.dim_pub_order_type
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
table_fqn: dim_us.dim_pub_order_type
anti_use: daily date_flag scan only; not routing_certified; do not copy for ranking
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt, SUM(net_sales) AS net_sales
FROM dim_us.dim_pub_order_type
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```