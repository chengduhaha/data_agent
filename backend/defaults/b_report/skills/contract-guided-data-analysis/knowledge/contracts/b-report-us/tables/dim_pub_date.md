# Table Contract Header

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_date
- domain: b-report-us
- one_line_purpose: Shared calendar dimension for B Report date_flag and fiscal joins

# dim_us.dim_pub_date

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_date`
- Layer: DIM
- Canonical/Derived: Canonical
- Owner team: Disty analytics / POS reporting
- Verified in Hive: yes
- Verified in Vertica: yes

### Grain, Scope, Exclusions

- Grain: dimension key level
- Scope: US POS reporting (`dim_us` baseline)
- Exclusions: Component lines (`order_line_type = 'Comp'`) excluded by default in standard POS revenue reports; credit order_type 114 excluded unless adjustment report

### Cross-Engine Presence

- Hive: yes (same table name under `dw_us` / `dm_us` / `dim_us` family)
- Vertica: yes
- Reconciliation notes: US-primary documentation; CA/MX/BR schemas follow same table names with regional data scope

### Column Catalog (100% columns)

- documented_column_count: 32
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| date_flag | date(8) | True | engine metadata not exposed | 1 | — | key | date flag | business_date | grain_key | date flag on POS domain dim table. | — |
| u_version | char(1)(1) | True | engine metadata not exposed | 2 | — | technical | u version | categorical_text | standard | u version on POS domain dim table. | — |
| q | int(8) | True | engine metadata not exposed | 3 | — | technical | q | categorical_text | standard | q on POS domain dim table. | — |
| fq | int(8) | True | engine metadata not exposed | 4 | — | technical | fq | categorical_text | standard | fq on POS domain dim table. | — |
| m | int(8) | True | engine metadata not exposed | 5 | — | technical | m | categorical_text | standard | m on POS domain dim table. | — |
| w | int(8) | True | engine metadata not exposed | 6 | — | technical | w | categorical_text | standard | w on POS domain dim table. | — |
| d | int(8) | True | engine metadata not exposed | 7 | — | technical | d | categorical_text | standard | d on POS domain dim table. | — |
| year | int(8) | True | engine metadata not exposed | 8 | — | technical | year | categorical_text | standard | year on POS domain dim table. | — |
| qtr | int(8) | True | engine metadata not exposed | 9 | — | technical | qtr | categorical_text | standard | qtr on POS domain dim table. | — |
| month | int(8) | True | engine metadata not exposed | 10 | — | technical | month | categorical_text | standard | month on POS domain dim table. | — |
| week | int(8) | True | engine metadata not exposed | 11 | — | technical | week | categorical_text | standard | week on POS domain dim table. | — |
| day | int(8) | True | engine metadata not exposed | 12 | — | technical | day | categorical_text | standard | day on POS domain dim table. | — |
| doy | int(8) | True | engine metadata not exposed | 13 | — | technical | doy | categorical_text | standard | doy on POS domain dim table. | — |
| fyear | int(8) | True | engine metadata not exposed | 14 | — | technical | fyear | categorical_text | standard | fyear on POS domain dim table. | — |
| fqtr | int(8) | True | engine metadata not exposed | 15 | — | technical | fqtr | categorical_text | standard | fqtr on POS domain dim table. | — |
| fdoy | int(8) | True | engine metadata not exposed | 16 | — | technical | fdoy | categorical_text | standard | fdoy on POS domain dim table. | — |
| dow | int(8) | True | engine metadata not exposed | 17 | — | technical | dow | categorical_text | standard | dow on POS domain dim table. | — |
| dname | char(3)(3) | True | engine metadata not exposed | 18 | — | technical | dname | categorical_text | standard | dname on POS domain dim table. | — |
| bonuswk | int(8) | True | engine metadata not exposed | 19 | — | technical | bonuswk | categorical_text | standard | bonuswk on POS domain dim table. | — |
| holiday | numeric(19,4)(16) | True | engine metadata not exposed | 20 | — | measure | holiday | currency_amount | standard | holiday on POS domain dim table. | — |
| payroll | numeric(19,4)(16) | True | engine metadata not exposed | 21 | — | measure | payroll | currency_amount | standard | payroll on POS domain dim table. | — |
| sales | numeric(19,4)(16) | True | engine metadata not exposed | 22 | — | measure | sales | currency_amount | standard | sales on POS domain dim table. | — |
| comment | varchar(80)(80) | True | engine metadata not exposed | 23 | — | dimension | comment | categorical_text | standard | comment on POS domain dim table. | — |
| weekday | int(8) | True | engine metadata not exposed | 24 | — | technical | weekday | categorical_text | standard | weekday on POS domain dim table. | — |
| week_flag | varchar(200)(200) | True | engine metadata not exposed | 25 | — | dimension | week flag | categorical_text | standard | week flag on POS domain dim table. | — |
| month_flag | varchar(200)(200) | True | engine metadata not exposed | 26 | — | dimension | month flag | categorical_text | standard | month flag on POS domain dim table. | — |
| quarter_flag | varchar(200)(200) | True | engine metadata not exposed | 27 | — | dimension | quarter flag | categorical_text | standard | quarter flag on POS domain dim table. | — |
| f_quarter_flag | varchar(200)(200) | True | engine metadata not exposed | 28 | — | dimension | f quarter flag | categorical_text | standard | f quarter flag on POS domain dim table. | — |
| month_name | varchar(200)(200) | True | engine metadata not exposed | 29 | — | dimension | month name | categorical_text | standard | month name on POS domain dim table. | — |
| week_flag2 | varchar(100)(100) | True | engine metadata not exposed | 30 | — | dimension | week flag2 | categorical_text | standard | week flag2 on POS domain dim table. | — |
| w2 | int(8) | True | engine metadata not exposed | 31 | — | technical | w2 | categorical_text | standard | w2 on POS domain dim table. | — |
| week2 | int(8) | True | engine metadata not exposed | 32 | — | technical | week2 | categorical_text | standard | week2 on POS domain dim table. | — |

### Lineage

- upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
- downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

### Freshness and Load Path

- Expected completion window: 05:00-07:30 PT (daily disty load dependency chain)
- Load pattern: Daily incremental by `date_flag`
- Freshness note: Align POS report date filters with latest loaded `date_flag`

## L2 Declarative Knowledge

### Business Definitions

- Shared dimension for POS attribute enrichment.

### Dimension Keys and Lookup Reference

- No dimension key columns detected on this table.

### Time Field Semantics

- `date_flag`: use when column exists; otherwise join via hub order keys.

### Metrics Served

- Canonical POS metrics on hub; this table provides context columns only. See `metric-index.md` when measures are derived here.

## L3 Procedural Knowledge

### Query and Routing Rules

- Prefer this table when POS report requires its attributes at documented grain.
- For metric questions on sales amount/qty, route to hub unless SPA/SCM enrichment explicitly needed.


### Dimension Join Patterns

- See domain-knowledge.md join graph when used with POS hub.

### Key Filters and ETL Business Logic

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

### Standard Time-Filter SQL (3 snippets)


1) Natural month (template — adjust table/grain)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_pub_date
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_date
WHERE date_flag >= DATE_TRUNC('month', ADD_MONTHS(CURRENT_DATE, -1))
  AND date_flag < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY date_flag;
```

2) Fiscal period (join dim_us.dim_pub_date when date_flag present)

3) Recent trend at table native grain


### Metric Selection Guidance

- See `metric-index.md` for formula authority and table routing.

## L4 Validation

### Data Quality Checks

- Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.

### Metric Recompute Spot-Checks

- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.

### Conflicts and Open Questions

- Validate join cardinality to POS hub before production report use.

## L5 Runtime View

### Query Path and Engine Preference

- Primary consumption: Vertica (`dim_us.dim_pub_date`)
- Hive available for reconciliation and Spark-side debugging

### Access Constraints

- Standard disty US schema access policies apply

## L6 Access and Consumption

### Primary Consumers and Use Cases

- Vertica RDS POS custom reports (499 scripts scanned: US 367, CA 124, MX 7, BR 1)
- Vendor/customer POS exports, SPA/SCM claim detail, serial/RMA tracing reports

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: audit
table_fqn: dim_us.dim_pub_date
anti_use: daily date_flag scan only; not routing_certified; do not copy for ranking
-->
```sql
SELECT *
FROM dim_us.dim_pub_date
LIMIT 100;
```
