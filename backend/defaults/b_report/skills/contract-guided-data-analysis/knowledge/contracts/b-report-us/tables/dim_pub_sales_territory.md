# dim_us.dim_pub_sales_territory

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_sales_territory
- domain: b-report-us
- one_line_purpose: US sales territory master — resolve `sales_terr` from territory names and enrich sub-group/group hierarchy

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_sales_territory`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_sales_territory`

### Grain, Scope, Exclusions

- Grain: one row per `sales_terr` per `date_flag` snapshot (Vertica mirror); CIS territory master attributes plus denormalized sub-group/group descriptions.
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive: `dim_us.dim_pub_sales_territory_df` verified present (partitioned by `date_flag` for as-of history).
- Vertica: `dim_us.dim_pub_sales_territory` verified present (daily `hive2vertica` snapshot).
- Row count (Vertica, 2026-06-26): 2,813 rows; `sales_terr` unique at grain on active snapshot.
- Label cardinality: `terr_name` 2,084 distinct (20 nulls); `group_desc` / `sub_group_desc` denormalized from CIS hierarchy ODS.
- Active snapshot probe: `date_flag` = 2026-06-25 (single day loaded on Vertica mirror at probe time).

### Column Catalog (100% columns)

- documented_column_count: 33
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sales_terr | int | engine metadata not exposed | — | 1 | — | key | sales territory id | integer | not_null_expected | Primary territory business key; join from facts as `cust_terr` / `sales_terr`. | — |
| terr_name | varchar(100) | engine metadata not exposed | — | 2 | — | dimension | territory display name | categorical_or_expression_text | domain_value_check_recommended | Human-readable territory label for search and display; not unique (~2,084 distinct on 2,813 territories). | — |
| region | int | engine metadata not exposed | — | 3 | — | dimension | region | integer | domain_value_check_recommended | region; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| start_date | timestamp | engine metadata not exposed | — | 4 | — | dimension | start date | categorical_or_expression_text | domain_value_check_recommended | start date; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| end_date | timestamp | engine metadata not exposed | — | 5 | — | dimension | end date | categorical_or_expression_text | domain_value_check_recommended | end date; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| reviewer | int | engine metadata not exposed | — | 6 | — | dimension | reviewer | integer | domain_value_check_recommended | reviewer; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| entry_datetime | timestamp | engine metadata not exposed | — | 7 | — | dimension | entry datetime | categorical_or_expression_text | domain_value_check_recommended | entry datetime; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| entry_id | int | engine metadata not exposed | — | 8 | — | key | entry id | integer | not_null_expected|dim_fk_check_recommended | entry id; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| cust_type | int | engine metadata not exposed | — | 9 | — | key | customer sales type | integer | not_null_expected|dim_fk_check_recommended | Territory-associated customer type code; decode labels via `dim_pub_sales_cust_type`. | `dim_us.dim_pub_sales_cust_type.cust_type` |
| group_id | int | engine metadata not exposed | — | 10 | — | key | territory group id | integer | not_null_expected|dim_fk_check_recommended | Territory group code; `group_desc` denormalized from CIS territory group ODS. | — |
| primary_id | int | engine metadata not exposed | — | 11 | — | key | primary sales rep id | integer | not_null_expected|dim_fk_check_recommended | Primary salesperson user id assigned to territory with `primary_pcnt` split. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_id1 | int | engine metadata not exposed | — | 12 | — | key | backup sales rep id 1 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt1` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_id2 | int | engine metadata not exposed | — | 13 | — | key | backup sales rep id 2 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt2` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_id3 | int | engine metadata not exposed | — | 14 | — | key | backup sales rep id 3 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt3` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| primary_pcnt | numeric(20,8) | engine metadata not exposed | — | 15 | — | measure | primary pcnt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | primary pcnt; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_pcnt1 | numeric(20,8) | engine metadata not exposed | — | 16 | — | measure | backup pcnt1 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt1; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_pcnt2 | numeric(20,8) | engine metadata not exposed | — | 17 | — | measure | backup pcnt2 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt2; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_pcnt3 | numeric(20,8) | engine metadata not exposed | — | 18 | — | measure | backup pcnt3 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt3; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| sub_group_id | int | engine metadata not exposed | — | 19 | — | key | sub group id | integer | not_null_expected|dim_fk_check_recommended | sub group id; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| cred_analyst | int | engine metadata not exposed | — | 20 | — | dimension | cred analyst | integer | domain_value_check_recommended | cred analyst; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_id4 | int | engine metadata not exposed | — | 21 | — | key | backup sales rep id 4 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt4` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_id5 | int | engine metadata not exposed | — | 22 | — | key | backup sales rep id 5 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt5` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_id6 | int | engine metadata not exposed | — | 23 | — | key | backup sales rep id 6 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt6` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_id7 | int | engine metadata not exposed | — | 24 | — | key | backup sales rep id 7 | integer | dim_fk_check_recommended | Backup salesperson user id with `backup_pcnt7` allocation. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| backup_pcnt4 | numeric(20,8) | engine metadata not exposed | — | 25 | — | measure | backup pcnt4 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt4; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_pcnt5 | numeric(20,8) | engine metadata not exposed | — | 26 | — | measure | backup pcnt5 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt5; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_pcnt6 | numeric(20,8) | engine metadata not exposed | — | 27 | — | measure | backup pcnt6 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt6; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| backup_pcnt7 | numeric(20,8) | engine metadata not exposed | — | 28 | — | measure | backup pcnt7 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | backup pcnt7; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| house | varchar(1) | engine metadata not exposed | — | 29 | — | dimension | house | categorical_or_expression_text | domain_value_check_recommended | house; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 30 | — | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| sub_group_desc | varchar(100) | engine metadata not exposed | — | 31 | — | dimension | sub group desc | categorical_or_expression_text | domain_value_check_recommended | sub group desc; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| group_desc | varchar(100) | engine metadata not exposed | — | 32 | — | dimension | group desc | categorical_or_expression_text | domain_value_check_recommended | group desc; Sales territory attribute on `dim_us.dim_pub_sales_territory`; join on `sales_terr` (use `_df` for as-of `date_flag`). | — |
| date_flag | date | engine metadata not exposed | — | 33 | — | key | date flag | YYYY-MM-DD | not_null_expected|dim_fk_check_recommended | Business date partition; use month-end row for MTD month totals. | `dim_us.dim_pub_date.date_flag` |


### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_territory`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_customer_dimension_us.dim_pub_sales_territory_df`
  - table_fqn: `ods_us.ods_cis_corp_territory_sub_group`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `sub_group_desc` enrichment
  - table_fqn: `ods_us.ods_cis_corp_territory_group`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `group_desc` enrichment
- downstream_n_hops:
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `dim_pub_sales_territory_df` territory hierarchy labels
  - table_fqn: `dw_us.dws_disty_brpt_cust_mtd`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: customer serving mart territory attributes
- lineage_last_verified_at: 2026-06-26
- lineage_confidence: high


### Column Lineage and Derivation

- `sales_terr`: primary territory key from CIS territory master.
- `terr_name`, `region`, hierarchy IDs: pass-through / joined from territory, sub-group, and group ODS tables.
- `primary_id`, `backup_id*`, `primary_pcnt`, `backup_pcnt*`: sales-rep assignment split metadata on territory.
- `date_flag` on Vertica table: snapshot date from `dim_pub_sales_territory_df` daily load.


### Freshness and Load Path

- Producer: `public_customer_dimension_us` → `dim_pub_sales_territory_df` → Vertica `dim_pub_sales_territory`.
- B Report dependency: `brpt_common_pre_loading_us` waits on `dim_pub_sales_territory_df`.
- Expected completion window: 02:00-03:30 PT.


## L2 Declarative Knowledge

### Business Definitions

- Domain: sales territory reference for customer geography and sales-hierarchy rollups.
- Grain: one row per `sales_terr` per `date_flag` snapshot on Vertica mirror.
- Primary join: `cust_terr` / `sales_terr` on facts and serving tables.



### Dimension Keys and Lookup Reference

- Primary key: `sales_terr` (int) — join from facts and customer master as `cust_terr` / `sales_terr`.
- Snapshot grain on Vertica: `sales_terr` + `date_flag` (daily mirror from `dim_pub_sales_territory_df`).
- Hierarchy labels: `sub_group_id` / `sub_group_desc`, `group_id` / `group_desc` (territory roll-up metadata on same row).
- Outbound FK: `cust_type` → `dim_us.dim_pub_sales_cust_type`; rep assignment IDs (`primary_id`, `backup_id*`) reference sales-rep user keys used with `dim_pub_sales_hierarchy_by_terr_user_role`.
- For primary rep/mgr/dir/vp chain on a territory, prefer `dim_pub_sales_hierarchy_primary_role_by_terr_view` when the question is sales-organization hierarchy rather than raw territory attributes.

### Dimension Lookup / Join Reference

- `cust_type` → `dim_us.dim_pub_sales_cust_type.cust_type` | join: `dim_pub_sales_territory.cust_type = dim_pub_sales_cust_type.cust_type` | lookup labels: `cust_type_descr`, `division_desc` | cardinality: many:1 | confidence: high
- `primary_id` / `backup_id*` → `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` | join: `dim_pub_sales_territory.primary_id = dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` | lookup labels: `sales_rep_name`, manager chain via hierarchy view | cardinality: many:1 | confidence: medium (rep assignment metadata; prefer hierarchy view for org labels)
- `date_flag` → `dim_us.dim_pub_date.date_flag` | join: `dim_pub_sales_territory.date_flag = dim_pub_date.date_flag` | lookup labels: `fyear`, `month`, `fqtr` | cardinality: many:1 | confidence: high


### Identifier Search Profile

- searchable_identifier_columns:
  - column: `terr_name`
    data_type: varchar
    match_mode: exact then contains_like (`ILIKE '%token%'`)
  - column: `group_desc`
    data_type: varchar
    match_mode: contains_like
  - column: `sub_group_desc`
    data_type: varchar
    match_mode: contains_like
- non_searchable_key_columns: `sales_terr`, `group_id`, `sub_group_id`, `primary_id`, `backup_id1`–`backup_id7`, `cust_type`, `region` — integer keys; do not compare alphanumeric user tokens to these columns
- user_facing_aliases: `territory`, `sales territory`, `terr` → search `terr_name` then join on `sales_terr`
- resolution_flow: user territory name token → exact/`ILIKE` on `terr_name` (optionally `group_desc` / `sub_group_desc` for hierarchy context) → obtain `sales_terr` → join facts on `fact.cust_terr = dim.sales_terr` with matching `date_flag` when using `_df` / Vertica snapshot

### Column Profiling (key vs label)

| column_name | distinct_count | total_rows | uniqueness | safe_for_group_by | notes |
| --- | --- | --- | --- | --- | --- |
| sales_terr | 2813 | 2813 | unique | yes | primary join key |
| terr_name | 2084 | 2813 | non_unique | no | display/search; ~20 nulls |
| cust_type | 141 | 2813 | non_unique | filter_ok | FK to `dim_pub_sales_cust_type` |
| region | 12 | 2813 | non_unique | filter_ok | geographic region code |

### Time Field Semantics

- `date_flag`: daily snapshot partition on Vertica mirror (`hive2vertica_dim_pub_sales_territory` loads one business day at a time). Vertica probe 2026-06-26: active snapshot `2026-06-25`, 2,813 rows. Hive `dim_pub_sales_territory_df` retains historical partitions for as-of joins in B Report ETL.
- `start_date` / `end_date`: territory assignment validity window from CIS. Observed on active snapshot: `start_date` from 1991-10-26; `end_date` through 2026-06-08.
- `sales_terr` (int): business territory key — join from facts as `cust_terr`; not searchable with free-text user tokens (use `terr_name`).

### Metrics Served

- Dimension attributes only; no fact metrics stored on this table


## L3 Procedural Knowledge

### Query and Routing Rules

- Use when resolving territory names to `sales_terr` or enriching `cust_terr` with `terr_name`, sub-group/group hierarchy.
- B Report serving tables often denormalize territory labels — prefer `dws_disty_brpt_terr_mtd` / `dws_disty_brpt_cust_mtd` for metric questions when territory attributes are already present.
- As-of joins: use `dim_pub_sales_territory_df` on `sales_terr` AND `date_flag` (B Report `pl_extend` pattern); Vertica `dim_pub_sales_territory` carries the latest synced snapshot day.
- For sales-rep / manager / director / VP labels by territory, prefer `dim_pub_sales_hierarchy_primary_role_by_terr_view` over reconstructing from `primary_id` alone.
- Facts carry `cust_terr` (int); they do **not** have `terr_name` — filter user territory tokens via this dimension or denormalized serving slice.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary key: `sales_terr`
- Fact join: `fact.cust_terr = dim_pub_sales_territory.sales_terr` (and `fact.date_flag = dim.date_flag` for snapshot/as-of)
- Customer master: `dim_pub_customer_info.sales_terr = dim_pub_sales_territory.sales_terr`
- Cust type decode: `dim_pub_sales_territory.cust_type = dim_pub_sales_cust_type.cust_type`
- Sales hierarchy (preferred): `dim_pub_sales_hierarchy_primary_role_by_terr_view.sales_terr = dim_pub_sales_territory.sales_terr`
- High-risk pitfalls: matching user text to integer `sales_terr`; joining without `date_flag` alignment on historical `_df` snapshots; duplicate `terr_name` labels mapping to multiple territories — aggregate at `sales_terr` after resolution

### Key Filters and ETL Business Logic

- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard Time-Filter SQL (3 snippets)

Time-filter snippets below apply to **fact/serving tables** joined to this dimension for metric questions. Use `dim_pub_sales_territory_df` with matching `date_flag` when as-of territory attributes are required.

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_pub_sales_territory
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
table_fqn: dim_us.dim_pub_sales_territory
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
table_fqn: dim_us.dim_pub_sales_territory
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

- Verify row count stability day-over-day on active Vertica snapshot (~2,800 territories; slow growth as CIS adds territories).
- Monitor duplicate-key risk on `sales_terr` — must be unique per `date_flag` snapshot.
- For `terr_name`, spot-check null rate (20 nulls observed) and duplicate labels mapping to multiple `sales_terr` values.
- When joining from facts on `cust_terr`, validate match rate against `date_flag`-aligned `dim_pub_sales_territory_df` for historical months.

### Metric Recompute Spot-Checks

- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.

### Conflicts and Open Questions

- No active conflicts on dimension grain or key semantics as of 2026-06-26.

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

- Consumers: B Report `pl_extend` / `cust_mtd` pre-load, `dim_pub_customer_info` territory enrichment, territory serving marts (`dws_disty_brpt_terr_*`).
- Use cases: territory name resolution, sub-group/group hierarchy labels, credit-territory classification (`cust_type`, `house`), rep assignment metadata on territory master.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: scalar_lookup
table_fqn: dim_us.dim_pub_sales_territory
anti_use: lookup only; aggregate metrics on dws_disty_brpt_terr_mtd or cust_mtd
-->
```sql
SELECT sales_terr, terr_name, sub_group_desc, group_desc, cust_type, region
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = (SELECT MAX(date_flag) FROM dim_us.dim_pub_sales_territory)
  AND terr_name ILIKE '%Northeast%'
ORDER BY sales_terr
LIMIT 20;
```

Certified territory-scoped metric SQL: see `golden-questions.md` and `dws_disty_brpt_terr_mtd` / `dws_disty_brpt_cust_mtd` routing in `metric-index.md`.
