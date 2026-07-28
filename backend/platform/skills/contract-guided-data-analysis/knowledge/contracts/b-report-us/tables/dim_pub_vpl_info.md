# dim_us.dim_pub_vpl_info

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_vpl_info
- domain: b-report-us
- one_line_purpose: Vendor product line (VPL) reference — resolve `vpl_no` from `vpl_code` and link vendor/VPC group

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_vpl_info`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_vpl_info`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive: `dim_us.dim_pub_vpl_info` verified present.
- Vertica: `dim_us.dim_pub_vpl_info` verified present.
- Row count (Vertica, 2026-06-25): 98,599 rows; `vpl_no` unique at grain.
- `vpl_code` 48,247 distinct — codes are not unique (multiple VPL rows may share a code pattern).
- Snapshot variant: `dim_pub_vpl_info_df` for as-of joins in B Report pre-load.

### Column Catalog (100% columns)

- documented_column_count: 22
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| vpl_no | int | engine metadata not exposed | — | 1 | Unique ID for VPC (Vendor Product Code) as defined in the dw_vend_pl table. | key | vpl no | integer | not_null_expected|dim_fk_check_recommended | vpl no; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | `dim_us.dim_pub_vpl_info.vpl_no` |
| vend_no | int | engine metadata not exposed | — | 2 | Synnex unique ID for each vendor as defined in vend_master table | key | vend no | integer | not_null_expected|dim_fk_check_recommended | vend no; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | `dim_us.dim_pub_vendor_info.vend_no` |
| vpl_code | varchar(200) | engine metadata not exposed | — | 3 | the code for one vpl | dimension | vpl code | categorical_or_expression_text | domain_value_check_recommended | vpl code; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| vpl_desc | varchar(200) | engine metadata not exposed | — | 4 | description for the vpl | dimension | vpl desc | categorical_or_expression_text | domain_value_check_recommended | vpl desc; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| entry_datetime | timestamp | engine metadata not exposed | — | 5 | Date record was inserted to table. NEVER update this column!! | dimension | entry datetime | categorical_or_expression_text | domain_value_check_recommended | entry datetime; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| entry_id | int | engine metadata not exposed | — | 6 | User ID of who inserted record into table. NEVER update this column!! | key | entry id | integer | not_null_expected|dim_fk_check_recommended | entry id; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| bid_factor | numeric(19,4) | engine metadata not exposed | — | 7 | Bid Factor from dw_vend_pl | measure | bid factor | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bid factor; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| retail_factor | numeric(19,4) | engine metadata not exposed | — | 8 | Retail Factor from dw_vend_pl | measure | retail factor | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | retail factor; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| tax_code | varchar(200) | engine metadata not exposed | — | 9 | tax code from dw_vend_pl | dimension | tax code | categorical_or_expression_text | domain_value_check_recommended | tax code; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| alt_vend_no | int | engine metadata not exposed | — | 10 | master vend no | key | alt vend no | integer | not_null_expected | dim_fk_check_recommended | alt vend no; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | `dim_us.dim_pub_vendor_info.vend_no` |
| alt_vpl_no | int | engine metadata not exposed | — | 11 | master vpl no | key | alt vpl no | integer | not_null_expected|dim_fk_check_recommended | alt vpl no; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| call_price | varchar(200) | engine metadata not exposed | — | 12 | Call Price | dimension | call price | categorical_or_expression_text | domain_value_check_recommended | call price; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| prod_type | varchar(200) | engine metadata not exposed | — | 13 | prod type | dimension | prod type | categorical_or_expression_text | domain_value_check_recommended | prod type; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| alt_seg_code | varchar(200) | engine metadata not exposed | — | 14 | master seg code | dimension | alt seg code | categorical_or_expression_text | domain_value_check_recommended | alt seg code; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| active | varchar(200) | engine metadata not exposed | — | 15 | Y / N toggle to indicate if record is active or not. | dimension | active | categorical_or_expression_text | domain_value_check_recommended | active; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| ec_flag | varchar(200) | engine metadata not exposed | — | 16 | used to mark the row if EC defined to use | dimension | ec flag | categorical_or_expression_text | domain_value_check_recommended | ec flag; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| dsv_type | varchar(200) | engine metadata not exposed | — | 17 | DSV: direct ship the product from vendor and they will pay the shipping cost. dsv type : Money,Qty | dimension | dsv type | categorical_or_expression_text | domain_value_check_recommended | dsv type; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| dsv_min_amt | numeric(19,4) | engine metadata not exposed | — | 18 | dsv min amt | measure | dsv min amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | dsv min amt; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| alt_seg_name | varchar(200) | engine metadata not exposed | — | 19 | Segment name for alt_seg_code | dimension | alt seg name | categorical_or_expression_text | domain_value_check_recommended | alt seg name; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| vpc_group_id | int | engine metadata not exposed | — | 20 | vpc group id | key | vpc group id | integer | not_null_expected|dim_fk_check_recommended | vpc group id; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 21 | Etl time | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |
| vpc_group_desc | varchar(100) | engine metadata not exposed | — | 22 | vpc group description | dimension | vpc group desc | categorical_or_expression_text | domain_value_check_recommended | vpc group desc; VPL (vendor product line) attribute on `dim_us.dim_pub_vpl_info`; join on `vpl_no`. | — |

### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_dw_vend_pl`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_vpl_dimension_us.dim_pub_vpl_info`
  - table_fqn: `ods_us.ods_cis_corp_vpc_group`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: BRPT `vpc_group_id` / `vpc_group_desc`
  - table_fqn: `ods_us.ods_cis_corp_vendor_profile`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: alternate segment code on VPL
- downstream_n_hops:
  - table_fqn: `dim_us.dim_pub_part_info`
    hop: 1
    relation_type: reference_lookup
    via_job_or_view: parts reference `vpl_no`
  - table_fqn: `dw_us.dws_disty_brpt_vpl_1d`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: VPL-level serving mart
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: extended P&L slice VPL attributes
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high


### Column Lineage and Derivation

- `vpl_no`, `vpl_code`, `vend_no`: core keys from `ods_cis_corp_dw_vend_pl`.
- `vpc_group_id`, `vpc_group_desc`: BRPT VPC group xref (`group_code = 'BRPT'`).
- `alt_seg_code`: coalesce from VPL and alternate VPL profile logic in ETL view.


### Freshness and Load Path

- Producer: `public_vpl_dimension_us.dim_pub_vpl_info`; Vertica `hive2vertica_dim_pub_vpl_info`.
- Snapshot: `dim_pub_vpl_info_df` for as-of joins in B Report pre-load.
- Expected completion window: 02:00-05:00 PT.


## L2 Declarative Knowledge

### Business Definitions

- Domain: vendor product line (VPL) reference for product/vendor profitability cuts.
- Grain: one row per `vpl_no`.
- Join: `fact.vpl_no = dim.vpl_no` for `vpl_code`, vendor linkage, VPC group.



### Dimension Keys and Lookup Reference

- Primary key: `vpl_no` (int).
- Vendor FK: `vend_no` → `dim_us.dim_pub_vendor_info`.
- Alternate VPL: `alt_vpl_no`, `alt_vend_no` for alternate product line assignments.
- VPC group: `vpc_group_id`, `vpc_group_desc` — BRPT profitability grouping.

### Dimension Lookup / Join Reference

- `vend_no` → `dim_us.dim_pub_vendor_info.vend_no` | join: `dim_pub_vpl_info.vend_no = dim_pub_vendor_info.vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `alt_vend_no` → `dim_us.dim_pub_vendor_info.vend_no` | join: `dim_pub_vpl_info.alt_vend_no = dim_pub_vendor_info.vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)


### Identifier Search Profile

- searchable_identifier_columns:
  - column: `vpl_code`
    data_type: varchar
    match_mode: exact then prefix_like (`ILIKE 'token%'`)
  - column: `vpl_desc`
    data_type: varchar
    match_mode: contains_like
  - column: `alt_seg_name`
    data_type: varchar
    match_mode: contains_like
  - column: `vpc_group_desc`
    data_type: varchar
    match_mode: contains_like
- non_searchable_key_columns: `vpl_no`, `vend_no`, `alt_vpl_no`, `vpc_group_id` — integer keys only
- user_facing_aliases: `vpl`, `product line`, `vendor product line`, `VPC`, `vpc group` → search `vpl_code` / `vpl_desc` / `vpc_group_desc`
- resolution_flow: user VPL code or description → search `vpl_code`/`vpl_desc` → obtain `vpl_no` → join facts on `fact.vpl_no = dim.vpl_no`

### Column Profiling (key vs label)

| column_name | distinct_count | total_rows | uniqueness | safe_for_group_by | notes |
| --- | --- | --- | --- | --- | --- |
| vpl_no | 98599 | 98599 | unique | yes | primary join key |
| vpl_code | 48247 | 98599 | non_unique | no | user search; not unique |
| vend_no | — | 98599 | — | filter_ok | FK to vendor dim |

### Time Field Semantics

- Base table current-state; B Report serving uses `dim_pub_vpl_info_df` partitioned by `date_flag`.

### Metrics Served

- Dimension attributes only; no fact metrics stored on this table


## L3 Procedural Knowledge

### Query and Routing Rules

- Use when user provides VPL code/description instead of integer `vpl_no`.
- VPL-level metrics: prefer `dw_us.dws_disty_brpt_vpl_1d` / `*_vpl_mtd` serving tables when available.
- `vpl_code` is not unique — always resolve to `vpl_no` before joining facts; disambiguate with `vend_no` when multiple matches.
- Facts carry `vpl_no` (int); `vpl_code` is on this dimension or denormalized on `pl_extend` / part dim.

### Dimension Join Patterns

- Primary key: `vpl_no`
- Fact join: `fact.vpl_no = dim_pub_vpl_info.vpl_no`
- Vendor: `dim_pub_vpl_info.vend_no = dim_pub_vendor_info.vend_no`
- Part: `dim_pub_part_info.vpl_no = dim_pub_vpl_info.vpl_no`
- Hierarchy: `dim_pub_vpl_hierarchy_info.vpl_no = dim_pub_vpl_info.vpl_no`
- As-of join: `dim_pub_vpl_info_df` on `vpl_no` AND `date_flag`

### Key Filters and ETL Business Logic

- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard Time-Filter SQL (3 snippets)

Time-filter snippets below apply to **fact/serving tables** joined to this dimension for metric questions. This dimension has no `date_flag`; use `*_df` snapshot variants when as-of attributes are required.

1) Natural month (month-end snapshot)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_pub_vpl_info
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
table_fqn: dim_us.dim_pub_vpl_info
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
table_fqn: dim_us.dim_pub_vpl_info
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

- Verify row count stability day-over-day; expect slow growth as new customers/vendors/parts onboard.
- Monitor duplicate-key risk on business keys (`cust_no`, `vend_no`, `sku_no`, `vpl_no`) — each should be unique at stated grain.
- For label columns used in user search (`*_name`, `part_no`, `vpl_code`), spot-check null rate and trim/whitespace anomalies.
- When joining to facts, validate match rate on integer FK columns; unmatched keys often indicate inactive master or cross-company scope mismatch.

### Metric Recompute Spot-Checks

- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.

### Conflicts and Open Questions

- No active conflicts on dimension grain or key semantics as of 2026-06-25.

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

- Consumers: `dim_pub_part_info`, `dws_disty_brpt_vpl_1d`, `pl_extend` VPL attributes.
- Use cases: VPL code resolution, vendor linkage, VPC group classification for profitability cuts.

### Representative Query Patterns

- No `routing_certified` patterns on this dimension table alone; certified metric SQL lives on serving marts (`dws_disty_brpt_*`, `dm_disty_brpt_*`) with dimension joins documented in `golden-questions.md`.

<!-- sql-artifact
snippet_type: illustrative
intent: scalar_lookup
table_fqn: dim_us.dim_pub_vpl_info
anti_use: lookup only; VPL metrics on dws_disty_brpt_vpl_* serving tables
-->
```sql
SELECT vpl_no, vpl_code, vpl_desc, vend_no, vpc_group_id, vpc_group_desc
FROM dim_us.dim_pub_vpl_info
WHERE vpl_code ILIKE 'HP%'
ORDER BY vpl_no
LIMIT 20;
```
