# dim_us.dim_pub_vendor_info

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_vendor_info
- domain: b-report-us
- one_line_purpose: US vendor master — resolve `vend_no` from vendor names and enrich segment/master-vendor hierarchy

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_vendor_info`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_vendor_info`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive: `dim_us.dim_pub_vendor_info` verified present.
- Vertica: `dim_us.dim_pub_vendor_info` verified present.
- Row count (Vertica, 2026-06-25): 70,772 rows; `vend_no` unique at grain.
- Label cardinality: `vend_name` 64,232 distinct; `master_vend_no` 48,924 distinct master vendors.
- Snapshot variant: `dim_pub_vendor_info_df` for as-of `date_flag` vendor attributes.

### Column Catalog (100% columns)

- documented_column_count: 49
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| vend_no | int | engine metadata not exposed | — | 1 | Vendor number, generated sequencially | key | vend no | integer | not_null_expected|dim_fk_check_recommended | vend no; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | `dim_us.dim_pub_vendor_info.vend_no` |
| vend_name | varchar(200) | engine metadata not exposed | — | 2 | Name of the vendor | dimension | vend name | categorical_or_expression_text | domain_value_check_recommended | vend name; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| primary_loc | int | engine metadata not exposed | — | 3 | Primary location of the vendor,from vend_location | dimension | primary loc | integer | domain_value_check_recommended | primary loc; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| pay_to_loc | int | engine metadata not exposed | — | 4 | The location payments should be sent to | dimension | pay to loc | integer | domain_value_check_recommended | pay to loc; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| purchase_loc | int | engine metadata not exposed | — | 5 | Where the main location to purchase goods from | dimension | purchase loc | integer | domain_value_check_recommended | purchase loc; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| entry_datetime | timestamp | engine metadata not exposed | — | 6 | The datetime of record created | dimension | entry datetime | categorical_or_expression_text | domain_value_check_recommended | entry datetime; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| entry_id | int | engine metadata not exposed | — | 7 | The employee ID who created the record | key | entry id | integer | not_null_expected|dim_fk_check_recommended | entry id; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| discontinued | varchar(200) | engine metadata not exposed | — | 8 | Flag to indicate If the vendor is discontinued (Y, N) | dimension | discontinued | categorical_or_expression_text | domain_value_check_recommended | discontinued; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| restricted | varchar(200) | engine metadata not exposed | — | 9 | Flag to indicate If the vendor is restricted (Y: restricted, N or NULL: not restricted) | dimension | restricted | categorical_or_expression_text | domain_value_check_recommended | restricted; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_type | varchar(200) | engine metadata not exposed | — | 10 | Type of the vendor ( I-Inventory, E-Expense,F-Freight, R-ReferenceV#) | dimension | vend type | categorical_or_expression_text | domain_value_check_recommended | vend type; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| buyer_no | int | engine metadata not exposed | — | 11 | Buyer's ID who in charge of the purchasing from this vendor | key | buyer no | integer | not_null_expected|dim_fk_check_recommended | buyer no; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| rma_rep | int | engine metadata not exposed | — | 12 | Employee's ID  in charge of RMA to the vendor | dimension | rma rep | integer | domain_value_check_recommended | rma rep; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| ap_clerk | int | engine metadata not exposed | — | 13 | AP analyst's ID in charge of payment for the vendor | dimension | ap clerk | integer | domain_value_check_recommended | ap clerk; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| tolerance | int | engine metadata not exposed | — | 14 | Tolerance days of payment (from pay due day) | dimension | tolerance | integer | domain_value_check_recommended | tolerance; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| po_type | varchar(200) | engine metadata not exposed | — | 15 | po_type | dimension | po type | categorical_or_expression_text | domain_value_check_recommended | po type; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_pay_frt | varchar(200) | engine metadata not exposed | — | 16 | vend_pay_frt | dimension | vend pay frt | categorical_or_expression_text | domain_value_check_recommended | vend pay frt; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| fob | varchar(200) | engine metadata not exposed | — | 17 | fob | dimension | fob | categorical_or_expression_text | domain_value_check_recommended | fob; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| stock_rotation | int | engine metadata not exposed | — | 18 | stock_rotation | dimension | stock rotation | integer | domain_value_check_recommended | stock rotation; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| restock_fee | int | engine metadata not exposed | — | 19 | The fee of restock | dimension | restock fee | integer | domain_value_check_recommended | restock fee; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| ship_method | varchar(200) | engine metadata not exposed | — | 20 | Type of shipping | dimension | ship method | categorical_or_expression_text | domain_value_check_recommended | ship method; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| freight | varchar(200) | engine metadata not exposed | — | 21 | Freight vendor flag (null,F--Free Fare,P--Prepaid,C--Collect,T--3rd Party,B--Prepaid Collect,A--Prepaid Third Party) | dimension | freight | categorical_or_expression_text | domain_value_check_recommended | freight; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_category | varchar(200) | engine metadata not exposed | — | 22 | source from vend_master,It is not sure whether it is referenced by other data tables, so it is reserved | dimension | vend category | categorical_or_expression_text | domain_value_check_recommended | vend category; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| ap_hold_flag | varchar(200) | engine metadata not exposed | — | 23 | Flag to indicate If this vendor's payment need to be hold. (Y-Accounts Payable hold, N--Accounts Payable not hold, A--Accounts Payable hold,null) | dimension | ap hold flag | categorical_or_expression_text | domain_value_check_recommended | ap hold flag; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| company_no | varchar(200) | engine metadata not exposed | — | 24 | The company number | key | company no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | company no; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| universal_vend_no | int | engine metadata not exposed | — | 25 | The vend no that source from vendor_profile and profile_type = 'UNI_VEND' and profile_cat = 'CAT' | key | universal vend no | integer | not_null_expected | dim_fk_check_recommended | universal vend no; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | `dim_us.dim_pub_vendor_info.universal_vend_no` |
| universal_vend_name | varchar(200) | engine metadata not exposed | — | 26 | The vend name that source from vendor_profile and profile_type = 'UNI_VEND' and profile_cat = 'CAT' | dimension | universal vend name | categorical_or_expression_text | domain_value_check_recommended | universal vend name; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| master_vend_flag | varchar(200) | engine metadata not exposed | — | 27 | Flag to indicate if the vendor is primary vend_no,the value  is Y,N | dimension | master vend flag | categorical_or_expression_text | domain_value_check_recommended | master vend flag; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| master_vend_no | int | engine metadata not exposed | — | 28 | Primary vend_no that source from vendor_xref | key | master vend no | integer | not_null_expected|dim_fk_check_recommended | master vend no; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | `dim_us.dim_pub_vendor_info.vend_no` |
| vend_company | varchar(200) | engine metadata not exposed | — | 29 | Vendor's company | dimension | vend company | categorical_or_expression_text | domain_value_check_recommended | vend company; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_currency | varchar(200) | engine metadata not exposed | — | 30 | Vendor Currency | dimension | vend currency | categorical_or_expression_text | domain_value_check_recommended | vend currency; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_segment | varchar(200) | engine metadata not exposed | — | 31 | Vendor Segment | dimension | vend segment | categorical_or_expression_text | domain_value_check_recommended | vend segment; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| pas_code | varchar(200) | engine metadata not exposed | — | 32 | The code that source from vendor_profile and profile_type='PAS CODE' | dimension | pas code | categorical_or_expression_text | domain_value_check_recommended | pas code; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 33 | Etl time | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| consign_flag | varchar(200) | engine metadata not exposed | — | 34 | to define if the vendor is consigment vendor,enum value is Y,N | dimension | consign flag | categorical_or_expression_text | domain_value_check_recommended | consign flag; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| pur_vend_no | int | engine metadata not exposed | — | 35 | purchase vendor number, from vendor_xref.xref_no with xref_type of VEND_PURCH | key | pur vend no | integer | not_null_expected|dim_fk_check_recommended | pur vend no; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| pur_vend_name | varchar(200) | engine metadata not exposed | — | 36 | purchase vendor name from vend_master for corresponding value of pur_vend_no | dimension | pur vend name | categorical_or_expression_text | domain_value_check_recommended | pur vend name; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| master_vend_name | varchar(300) | engine metadata not exposed | — | 37 | master vend name | dimension | master vend name | categorical_or_expression_text | domain_value_check_recommended | master vend name; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| smb_vend_image_flag | varchar(2) | engine metadata not exposed | — | 38 | flag to indicate it has smb vend image | dimension | smb vend image flag | categorical_or_expression_text | domain_value_check_recommended | smb vend image flag; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| n_comp_brp_flag | int | engine metadata not exposed | — | 39 | Those flag defined for non A part on vendor | dimension | n comp brp flag | integer | domain_value_check_recommended | n comp brp flag; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_seg_code | varchar(6) | engine metadata not exposed | — | 40 | vendor segment(setup on vendor) | dimension | vend seg code | categorical_or_expression_text | domain_value_check_recommended | vend seg code; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| prefix | varchar(100) | engine metadata not exposed | — | 41 | prefix from dbo..vend_master_etc | dimension | prefix | categorical_or_expression_text | domain_value_check_recommended | prefix; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| diversity_status | int | engine metadata not exposed | — | 42 | vendor diversity status code | dimension | diversity status | integer | domain_value_check_recommended | diversity status; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| diversity_status_desc | varchar(100) | engine metadata not exposed | — | 43 | diversity status description | dimension | diversity status desc | categorical_or_expression_text | domain_value_check_recommended | diversity status desc; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_seg_name | varchar(100) | engine metadata not exposed | — | 44 | vendor segment name | dimension | vend seg name | categorical_or_expression_text | domain_value_check_recommended | vend seg name; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| cis_mk_name | varchar(100) | engine metadata not exposed | — | 45 | cis market name | dimension | cis mk name | categorical_or_expression_text | domain_value_check_recommended | cis mk name; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_rank | int | engine metadata not exposed | — | 46 | Vendor showcase level | dimension | vend rank | integer | domain_value_check_recommended | vend rank; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_pay_frt_amt | numeric(20,8) | engine metadata not exposed | — | 47 | vendor pay freight amount | measure | vend pay frt amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | vend pay frt amt; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| discont_pur | varchar(2) | engine metadata not exposed | — | 48 | Flag to indicate if purchases from the vendor are discontinued Y,N | dimension | discont pur | categorical_or_expression_text | domain_value_check_recommended | discont pur; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |
| vend_terms | varchar(10) | engine metadata not exposed | — | 49 | terms from CIS.vend_location | dimension | vend terms | categorical_or_expression_text | domain_value_check_recommended | vend terms; Vendor master attribute on `dim_us.dim_pub_vendor_info`; join on `vend_no` or `master_vend_no`. | — |

### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_vend_master`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_vendor_dimension_us.dim_pub_vendor_info`
  - table_fqn: `ods_us.ods_cis_corp_vendor_profile`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: segment, universal vendor, PAS code profiles
  - table_fqn: `ods_us.ods_cis_corp_vendor_xref`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: master vendor (`SRef`) linkage
- downstream_n_hops:
  - table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `vend_no` / segment enrichment
  - table_fqn: `dw_us.dws_disty_brpt_vend_mtd`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: vendor-slice serving mart
  - table_fqn: `dim_us.dim_pub_part_info`
    hop: 1
    relation_type: reference_lookup
    via_job_or_view: part rows carry `vend_no`
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high


### Column Lineage and Derivation

- `vend_no`: primary vendor key from `ods_cis_corp_vend_master`.
- `master_vend_no`, `master_vend_name`: derived via vendor xref (`SRef`) to master vendor row.
- `vend_seg_code`, `vend_segment`, `universal_vend_no`: from `ods_cis_corp_vendor_profile` pivots.
- `vend_name`, location and AP attributes: pass-through vendor master columns.


### Freshness and Load Path

- Producer: `public_vendor_dimension_us.dim_pub_vendor_info`; Vertica `hive2vertica_dim_pub_vendor_info`.
- Snapshot variant: `dim_pub_vendor_info_df` for as-of `date_flag` joins.
- Expected completion window: 02:00-04:00 PT.


## L2 Declarative Knowledge

### Business Definitions

- Domain: vendor master for B Report vendor/manufacturer analytics.
- Grain: one row per `vend_no`.
- Primary join: `fact.vend_no = dim.vend_no` for `vend_name`, `master_vend_no`, segment codes.



### Dimension Keys and Lookup Reference

- Primary key: `vend_no` (int) — fact join key for vendor on order lines and parts.
- Master vendor: `master_vend_no` / `master_vend_name` — roll-up key for manufacturer families (xref `SRef`).
- Universal vendor: `universal_vend_no` / `universal_vend_name` — cross-company universal manufacturer reference.
- Segment: `vend_seg_code`, `vend_segment`, `vend_seg_name` from vendor profile.

### Dimension Lookup / Join Reference

- `vend_no` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.vend_no = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `entry_id` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.entry_id = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `buyer_no` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.buyer_no = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `company_no` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.company_no = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `universal_vend_no` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.universal_vend_no = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `master_vend_no` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.master_vend_no = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `pur_vend_no` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.pur_vend_no = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `vend_pay_frt_amt` → `dim_us.dim_pub_vendor_info` | join: `dim_pub_vendor_info.vend_pay_frt_amt = dim_us.dim_pub_vendor_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)

### Identifier Search Profile

- searchable_identifier_columns:
  - column: `vend_name`
    data_type: varchar
    match_mode: exact then contains_like (`ILIKE '%token%'`)
  - column: `master_vend_name`
    data_type: varchar
    match_mode: exact then contains_like
  - column: `universal_vend_name`
    data_type: varchar
    match_mode: contains_like
  - column: `cis_mk_name`
    data_type: varchar
    match_mode: contains_like
  - column: `pur_vend_name`
    data_type: varchar
    match_mode: contains_like
- non_searchable_key_columns: `vend_no`, `master_vend_no`, `universal_vend_no`, `buyer_no` — integer keys only
- user_facing_aliases: `vendor`, `manufacturer`, `mfr` → search `vend_name` or `master_vend_name`
- resolution_flow: user vendor name → exact/`ILIKE` on `vend_name` or `master_vend_name` → obtain `vend_no` (or `master_vend_no` for roll-up) → join facts on `fact.vend_no = dim.vend_no`

### Column Profiling (key vs label)

| column_name | distinct_count | total_rows | uniqueness | safe_for_group_by | notes |
| --- | --- | --- | --- | --- | --- |
| vend_no | 70772 | 70772 | unique | yes | primary join key |
| vend_name | 64232 | 70772 | non_unique | no | search/filter only |
| master_vend_no | 48924 | 70772 | non_unique | filter_ok | master vendor roll-up |

### Time Field Semantics

- Base table is current-state vendor master; use `dim_pub_vendor_info_df` when as-of `date_flag` snapshot is required.

### Metrics Served

- Dimension attributes only; no fact metrics stored on this table


## L3 Procedural Knowledge

### Query and Routing Rules

- Use for vendor name → `vend_no` resolution when serving table lacks denormalized `vend_name`.
- Vendor ranking metrics: prefer `dw_us.dws_disty_brpt_vend_mtd` — see golden `jan-vendor-top5-ranking`.
- Master-vendor roll-up: filter or group by `master_vend_no` / `master_vend_name` when user asks about manufacturer family.
- Facts carry `vend_no` (int); label columns are on this dimension or denormalized on serving marts.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary key: `vend_no`
- Fact join: `fact.vend_no = dim_pub_vendor_info.vend_no`
- Master roll-up: `fact.master_vend_no = dim.master_vend_no` or join on `dim.master_vend_no`
- Part enrichment: `dim_pub_part_info.vend_no = dim_pub_vendor_info.vend_no`
- As-of join: `dim_pub_vendor_info_df` on `vend_no` AND `date_flag`
- High-risk pitfalls: `GROUP BY vend_name`; conflating `vend_no` with `master_vend_no`

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
table_fqn: dim_us.dim_pub_vendor_info
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
table_fqn: dim_us.dim_pub_vendor_info
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
table_fqn: dim_us.dim_pub_vendor_info
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

- Consumers: B Report order-line and vendor serving marts, `dim_pub_part_info` vendor enrichment.
- Use cases: vendor name resolution, master-vendor roll-ups, segment classification.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: scalar_lookup
table_fqn: dim_us.dim_pub_vendor_info
anti_use: lookup only; vendor ranking metrics use dws_disty_brpt_vend_mtd
-->
```sql
SELECT vend_no, vend_name, master_vend_no, master_vend_name, vend_seg_code, vend_segment
FROM dim_us.dim_pub_vendor_info
WHERE vend_name ILIKE '%CISCO%'
   OR master_vend_name ILIKE '%CISCO%'
ORDER BY vend_no
LIMIT 20;
```

Certified vendor ranking: `golden-questions.md` → `jan-vendor-top5-ranking`.
