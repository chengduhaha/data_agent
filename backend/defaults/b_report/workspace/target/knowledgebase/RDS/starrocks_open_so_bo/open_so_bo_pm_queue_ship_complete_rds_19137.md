# REPORT: RDS open_so_bo report SQL — open so bo pm queue ship complete rds 19137 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_open_so_bo.open_so_bo_pm_queue_ship_complete_rds_19137
- domain: RDS/starrocks_open_so_bo
- one_line_purpose: RDS open_so_bo report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_pm_queue_ship_complete_rds_19137.md
- ref_evidence: source/ref/RDS/starrocks_open_so_bo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `open_so_bo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_open_so_bo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 31 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_open_so_bo open_so_bo_pm_queue_ship_complete_rds_19137" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_us.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_order_soldto_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_customer_header_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_vend_user_matrix_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `dim_us.dim_pub_manager` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_location_info_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_order_profile_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **upstream:** `ods_us.ods_cis_corp_sales_que_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `open_so_bo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_open_so_bo/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `open_so_bo` |
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

- **Source:** [source/contracts/rds/starrocks_open_so_bo/metric-index.md](../../../../source/contracts/rds/starrocks_open_so_bo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |

### Key filters and ETL business logic
- `a.order_type in (1, 8) and a.delete_date is null and b.delete_date is null and a.ship_date is null and b.order_qty - ifnull(b.ship_qty,0) <> 0 and c.vend_no in (13208 ,81051,22084,…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (11 objects).
2. Build staging temps (4 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_us.ods_cis_corp_order_header_rt"]
  P1["ods_us.ods_cis_corp_order_detail_rt"]
  P2["dim_us.dim_pub_part_info"]
  P3["ods_us.ods_cis_corp_order_soldto_rt"]
  P4["ods_us.ods_cis_corp_customer_header_rt"]
  P5["ods_us.ods_cis_corp_vend_user_matrix_rt"]
  P6["dim_us.dim_pub_manager"]
  P7["ods_us.ods_cis_corp_location_info_rt"]
  T0["tempdb.rds_order_us19137"]
  T1["tempdb.pm_queue_us19137"]
  T2["tempdb.rds_tmp"]
  T3["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  P0 --> T0
  T3 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_us.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_soldto_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_customer_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vend_user_matrix_rt` | Permanent warehouse source |
| `dim_us.dim_pub_manager` | Permanent warehouse source |
| `ods_us.ods_cis_corp_location_info_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_profile_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_sales_que_rt` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `tempdb.rds_order_us19137` | Report staging / temp table |
| `tempdb.pm_queue_us19137` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `dw_us.dwd_disty_inv_qty_df`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.rds_order_us19137`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.pm_queue_us19137`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 7 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `id` | `uuid_numeric()` | `uuid_numeric` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | udf | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:4` |
| `order_no` | `a.order_no` | `order_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:5` |
| `order_type` | `a.order_type` | `order_type` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:6` |
| `order_line_no` | `b.order_line_no` | `order_line_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:7` |
| `to_acct_no` | `a.to_acct_no` | `to_acct_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:8` |
| `from_loc_no` | `a.from_loc_no` | `from_loc_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:9` |
| `loc_char` | `cast(null as char(4))` | `char` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:10` |
| `created_date` | `date_format(a.entry_datetime,'%m/%d/%Y')` | `entry_datetime`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:11` |
| `ship_date` | `date_format(a.ship_date,'%m/%d/%Y')` | `ship_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:12` |
| `printed_date` | `date_format(a.printed_date,'%m/%d/%Y')` | `printed_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:13` |
| `pick_date` | `date_format(a.pick_date,'%m/%d/%Y')` | `pick_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:14` |
| `qc_date` | `date_format(a.qc_date,'%m/%d/%Y')` | `qc_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:15` |
| `sku_no` | `b.sku_no` | `sku_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:16` |
| `vpl_no` | `c.vpl_no` | `vpl_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:17` |
| `sales_terr` | `a.sales_terr` | `sales_terr` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:18` |
| `sold_to_acct` | `cast(null as int)` | — | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:19` |
| `sold_to_cust_name` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:20` |
| `ship_to_name` | `a.ship_to_name` | `ship_to_name` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:21` |
| `deleted` | `date_format(a.delete_date,'%m/%d/%Y')` | `delete_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:22` |
| `sales_rel` | `date_format(a.sales_rel_date,'%m/%d/%Y')` | `sales_rel_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:23` |
| `credit_rel` | `date_format(a.credit_rel_date,'%m/%d/%Y')` | `credit_rel_date`, `m`, `d`, `Y` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | arithmetic | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:24` |
| `primary_id` | `cast(null as int)` | — | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:19` |
| `pm` | `cast(null as varchar(80))` | — | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:26` |
| `order_ship_complete` | `cast('N' as varchar(10))` | `N` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:27` |
| `pm_queue` | `cast('N' as varchar(10))` | `N` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:27` |
| `issue_date` | `a.issue_date` | `issue_date` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:29` |
| `ship_method` | `a.ship_method` | `ship_method` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:30` |
| `comments` | `cast(null as varchar(200))` | — | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:31` |
| `vend_no` | `c.vend_no` | `vend_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:32` |
| `inv_type` | `b.inv_type` | `inv_type` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:33` |
| `on_hand` | `cast(null as int)` | — | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`, `dim_us.dim_pub_manager`, `ods_us.ods_cis_corp_location_info_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_sales_que_rt`, `tempdb.pm_queue_us19137`, `dw_us.dwd_disty_inv_qty_df` | cast | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql:19` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `open_so_bo` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_us.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_order_soldto_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_customer_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_vend_user_matrix_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_location_info_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_order_profile_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `ods_us.ods_cis_corp_sales_que_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_pm_queue_ship_complete_rds_19137.sql` (source_kind: rds_report_sql).*
