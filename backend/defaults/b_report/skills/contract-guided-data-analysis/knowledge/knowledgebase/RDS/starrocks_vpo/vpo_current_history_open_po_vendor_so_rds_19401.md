# REPORT: RDS vpo report SQL — vpo current history open po vendor so rds 19401 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_vpo.vpo_current_history_open_po_vendor_so_rds_19401
- domain: RDS/starrocks_vpo
- one_line_purpose: RDS vpo report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_vpo/vpo_current_history_open_po_vendor_so_rds_19401.md
- ref_evidence: source/ref/RDS/starrocks_vpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `vpo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_vpo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 34 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_vpo vpo_current_history_open_po_vendor_so_rds_19401" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_manager_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_customer_header_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_territory_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_order_eta_code_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_vend_user_matrix_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **upstream:** `ods_us.ods_cis_corp_history_detail_rt` — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`
- **downstream:** `tempdb.rds_us_orders_19401` (report output) — `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `vpo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_vpo/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `vpo` |
| **Analysts** | Understand which warehouse tables feed this report |

### Fact key resolution
N/A — catalog-only / report SQL (not a FACT warehouse table load).

### Time field semantics
- **date_flag / report dates:** use predicates present in the evidence SQL; see L3 Key filters.

### Metrics served
| Category | Columns | Business reading |
|----------|---------|------------------|
| Report measures | See L3 column derivations | Derived in report SELECT list |

### Metric serving map
- Report output columns map 1:1 from final SELECT aliases (see L3).

### etl_metrics
*(Link to pack metric-index; formulas append-only — do not invent.)*

- **Source:** [source/contracts/rds/starrocks_vpo/metric-index.md](../../../../source/contracts/rds/starrocks_vpo/metric-index.md)
- **Business definition:** Not documented in repository unless listed in metric-index
- Formula SQL: use metric-index `final_effective_formula_sql` when present; otherwise Not documented in repository

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** predicates in the report SQL WHERE clauses (see Key filters).
**Technical predicates (load only):** N/A — not a warehouse partition load job.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |

### Key filters and ETL business logic
- `a.vend_no = 64351 ; drop table if exists tempdb.rds_us_orders_19401; create table tempdb.rds_us_orders_19401 as select distinct a.to_inv_type as inv_type, a.to_loc_no as loc_no, c.…`
- `a.mso is not null and b.profile_type = 'SAPID' and b.profile_cat = 'ORDR' and b.profile_c is not null ; drop table if exists tempdb.rds_us_vendor_po_19401; create table tempdb.rds_…`
- `b.vend_so_no is not null ; drop table if exists tempdb.rds_us_orders_2_19401; create table tempdb.rds_us_orders_2_19401 as select distinct a.inv_type, a.loc_no, a.vend_no, a.vend_n…`
- `b.order_type = 1 and b.delete_date is null ) x`
- `order_type = 2 and profile_type = 'ETASRC'`
- `list_box_code = 'SRC'`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (18 objects).
2. Build staging temps (9 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_part_info"]
  P1["ods_us.ods_cis_corp_order_header_rt"]
  P2["ods_us.ods_cis_corp_order_detail_rt"]
  P3["ods_us.ods_cis_corp_manager_rt"]
  P4["ods_us.ods_cis_corp_customer_header_rt"]
  P5["ods_us.ods_cis_corp_territory_rt"]
  P6["ods_us.ods_cis_corp_order_eta_code_rt"]
  P7["ods_us.ods_cis_corp_vend_user_matrix_rt"]
  T0["tempdb.rds_us_sku_19401"]
  T1["tempdb.rds_us_orders_19401"]
  T2["tempdb.rds_us_vendor_mso_19401"]
  T3["tempdb.rds_us_vendor_po_19401"]
  T4["tempdb.rds_us_orders_2_19401"]
  T5["tempdb.rds_us_vend_quote_19401"]
  T6["tempdb.rds_us_report_19401"]
  T7["tempdb.rds_tmp"]
  T8["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  O2["tempdb.rds_us_orders_19401"]
  P0 --> T0
  T8 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_manager_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_customer_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_territory_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_eta_code_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vend_user_matrix_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_profile` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_profile` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_eta_code_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_eu_custom_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_eu_custom_map_rt` | Permanent warehouse source |
| `dim_us.dim_pub_list_box_detail` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_eu_custom_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_profile_rt` | Permanent warehouse source |
| `tempdb.rds_us_sku_19401` | Report staging / temp table |
| `tempdb.rds_us_orders_19401` | Report staging / temp table |
| `tempdb.rds_us_vendor_mso_19401` | Report staging / temp table |
| `tempdb.rds_us_vendor_po_19401` | Report staging / temp table |
| `tempdb.rds_us_orders_2_19401` | Report staging / temp table |
| `tempdb.rds_us_vend_quote_19401` | Report staging / temp table |
| `tempdb.rds_us_report_19401` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |
| `tempdb.rds_us_orders_19401` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.rds_us_sku_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.rds_us_orders_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.rds_us_vendor_mso_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.rds_us_vendor_po_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.rds_us_orders_2_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.rds_us_vend_quote_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `tempdb.rds_us_report_19401`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 12 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `tempdb.rds_us_orders_19401`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `inv_type` | `a.to_inv_type` | `to_inv_type` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:24` |
| `loc_no` | `a.to_loc_no` | `to_loc_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:25` |
| `vend_no` | `c.vend_no` | `vend_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:26` |
| `vend_name` | `c.vend_name` | `vend_name` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:27` |
| `prod_code` | `c.prod_code` | `prod_code` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:28` |
| `vpl_no` | `c.vpl_no` | `vpl_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:29` |
| `mso` | `a.int_ref_no` | `int_ref_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:30` |
| `po_no` | `a.order_no` | `order_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:31` |
| `po_ln_no` | `b.order_line_no` | `order_line_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:32` |
| `sku_no` | `c.sku_no` | `sku_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:33` |
| `part_no` | `c.part_no` | `part_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:34` |
| `mfg_partno` | `c.mfg_partno` | `mfg_partno` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:35` |
| `sys_cost` | `c.sys_cost` | `sys_cost` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:36` |
| `base_cost` | `b.unit_cost` | `unit_cost` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:37` |
| `order_qty` | `b.order_qty` | `order_qty` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:38` |
| `open_qty` | `b.order_qty - ifnull(b.rec_qty, 0)` | `order_qty`, `rec_qty` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | coalesce | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:39` |
| `rec_qty` | `ifnull(b.rec_qty, 0)` | `rec_qty` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | coalesce | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:39` |
| `abc_code` | `c.abc_code` | `abc_code` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:41` |
| `entry_date` | `a.entry_datetime` | `entry_datetime` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:42` |
| `entry_id` | `a.entry_id` | `entry_id` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:43` |
| `entry_name` | `concat(d.firstname, ' ', d.lastname)` | `firstname`, `lastname` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | udf | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:44` |
| `buyer` | `concat(m.firstname, ' ', m.lastname)` | `firstname`, `lastname` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | udf | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:45` |
| `sales_rel_date` | `date_format(a.sales_rel_date, '%m/%d/%Y')` | `sales_rel_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | arithmetic | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:46` |
| `expected_date` | `date_format(a.expected_date, '%m/%d/%Y')` | `expected_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | arithmetic | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:47` |
| `ship_date` | `date_format(b.prod_exp_date, '%m/%d/%Y')` | `prod_exp_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | arithmetic | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:48` |
| `eta_date` | `date_format(b.expected_date, '%m/%d/%Y')` | `expected_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | arithmetic | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:49` |
| `eta_code` | `g.eta_code` | `eta_code` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:50` |
| `vendor_quote_id` | `cast(null as varchar(360))` | — | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | cast | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:51` |
| `cpo` | `aa.ext_ref` | `ext_ref` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:52` |
| `cust_no` | `a.to_acct_no` | `to_acct_no` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:53` |
| `cust_name` | `e.cust_name` | `cust_name` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:54` |
| `sales_terr` | `a.sales_terr` | `sales_terr` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:55` |
| `terr_name` | `f.terr_name` | `terr_name` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:56` |
| `end_user_name` | `a.ship_to_name` | `ship_to_name` | `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `tempdb.rds_us_sku_19401`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `tempdb.rds_us_orders_19401`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_history_eta_code_rt` | rename | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql:57` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` — Not documented as Azkaban partition |

**Plain language:** This is on-demand report SQL. Date windows come from the script body or runtime parameters, not from warehouse ETL bootstrap jobs.

### Data quality checks
- Row counts on `tempdb.rds_tmp` after report execution
- Spot-check measure totals vs source fact tables listed in L1 lineage

### Validation SQL
<!-- sql-artifact snippet_type: illustrative intent: audit -->
```sql
-- 1) row count on final output (session)
-- SELECT COUNT(*) FROM tempdb.rds_tmp;

-- 2) metric sum by a key dimension (replace <dim> / <metric> from final SELECT)
-- SELECT <dim>, SUM(<metric>) FROM tempdb.rds_tmp GROUP BY 1;

-- 3) grain duplicate check when natural key is known from SQL
-- SELECT <key_cols>, COUNT(*) FROM tempdb.rds_tmp GROUP BY <key_cols> HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- Temp table names and schemas differ by engine (`rdsetl` vs `tempdb`).
- Example SQL may use regional schemas (`dw_ca`, `dw_us`, `dw_xx` placeholders).

### Conflicts and open questions
- Schedule, SLA, and production report number ownership: Not documented in repository

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` | no |

### Access constraints
- Country/region schemas in FROM clauses; do not assume US-only.
- Vertica no-run policy while documenting: do not execute business SQL via Vertica MCP.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes (typical for RDS reports) |
| scan_risk_tier | medium |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Consumer | Use case |
|----------|----------|
| RDS report tooling | Execute curated example / production-like report SQL |
| Knowledgebase / agents | Lineage and filter documentation for `vpo` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_manager_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_customer_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_territory_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_order_eta_code_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_vend_user_matrix_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_history_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_history_profile` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_order_profile` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_history_eta_code_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_order_eu_custom_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |
| `ods_us.ods_cis_corp_eu_custom_map_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_vpo/etl/vpo_current_history_open_po_vendor_so_rds_19401.sql` (source_kind: rds_report_sql).*
