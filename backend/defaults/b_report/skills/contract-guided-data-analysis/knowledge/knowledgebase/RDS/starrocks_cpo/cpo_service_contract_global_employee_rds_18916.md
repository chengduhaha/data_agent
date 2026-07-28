# REPORT: select count(*) from rds_us_customers_18916 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_cpo.cpo_service_contract_global_employee_rds_18916
- domain: RDS/starrocks_cpo
- one_line_purpose: RDS cpo report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_cpo/cpo_service_contract_global_employee_rds_18916.md
- ref_evidence: source/ref/RDS/starrocks_cpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `cpo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_cpo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 14 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_cpo cpo_service_contract_global_employee_rds_18916" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_customer_info` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `dim_us.dim_pub_manager` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_gbl.ods_cis_mygbl_global_employee` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_gbl.ods_cis_mygbl_global_location_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_us.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_us.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_us.ods_cis_corp_order_soldto_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **upstream:** `ods_us.ods_cis_corp_history_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`
- **downstream:** `tempdb.rds_us_report_18916` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `cpo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_cpo/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `cpo` |
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

- **Source:** [source/contracts/rds/starrocks_cpo/metric-index.md](../../../../source/contracts/rds/starrocks_cpo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |

### Key filters and ETL business logic
- `ifnull(m.title,'') <> 'Buyer' ; -- select count(*) from rds_us_users_18916 drop table if exists rds_us_orders_18916; create table rds_us_orders_18916 as select a.order_type, a.orde…`
- `a.entry_datetime >= date_add(current_date(), interval -1 month) and a.entry_datetime < date_add(current_date(), interval -0 day) and a.order_type = 8 ; insert into rds_us_orders_18…`
- `a.entry_datetime >= date_add(current_date(), interval -1 month) and a.entry_datetime < date_add(current_date(), interval -0 day) and a.order_type = 1 and ifnull(a.int_ref_type,0) <…`
- `a.entry_date >= date_add(current_date(), interval -1 month) and a.entry_date < date_add(current_date(), interval -0 day) and a.contract_type = 1 and a.vendor_no = 64956 ; -- select…`
- `tempdb.rds_us_report_18916.cpo_type = 2 and tempdb.rds_us_report_18916.from_loc_no = 98 and tempdb.rds_us_report_18916.cpo_id = a.order_no and a.order_type = 2 ; update tempdb.rds_…`
- `userid = 738084 ; drop table if exists rds_us_rds_usrep_18916; create table rds_us_rds_usrep_18916 ( userid int(11) ) primary key (userid) distributed by hash (userid) ; insert int…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (21 objects).
2. Build staging temps (15 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_customer_info"]
  P1["dim_us.dim_pub_manager"]
  P2["ods_gbl.ods_cis_mygbl_global_employee"]
  P3["ods_gbl.ods_cis_mygbl_global_location_rt"]
  P4["ods_us.ods_cis_corp_order_header_rt"]
  P5["ods_us.ods_cis_corp_order_detail_rt"]
  P6["ods_us.ods_cis_corp_part_master_rt"]
  P7["ods_us.ods_cis_corp_order_soldto_rt"]
  T0["rds_us_customers_18916"]
  T1["rds_us_users_18916"]
  T2["rds_us_orders_18916"]
  T3["rds_us_orders_125_18916"]
  T4["tempdb.rds_us_report_18916"]
  T5["rds_us_rds_bjrep_18916"]
  T6["rds_us_rds_phrep_18916"]
  T7["rds_us_rds_indrep_18916"]
  T8["rds_us_rds_usrep_18916"]
  T9["rds_us_dim_18916"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  O2["tempdb.rds_us_report_18916"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_customer_info` | Permanent warehouse source |
| `dim_us.dim_pub_manager` | Permanent warehouse source |
| `ods_gbl.ods_cis_mygbl_global_employee` | Permanent warehouse source |
| `ods_gbl.ods_cis_mygbl_global_location_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_soldto_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_soldto_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_inv_tran_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_inv_tran_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_service_contract_header` | Permanent warehouse source |
| `ods_us.ods_cis_corp_service_contract_line_sum` | Permanent warehouse source |
| `ods_us.ods_cis_corp_from_ref_type_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_location_info_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_manager_rt` | Permanent warehouse source |
| `ods_gbl.ods_cis_mygbl_global_job_code` | Permanent warehouse source |
| `rds_us_customers_18916` | Report staging / temp table |
| `rds_us_users_18916` | Report staging / temp table |
| `rds_us_orders_18916` | Report staging / temp table |
| `rds_us_orders_125_18916` | Report staging / temp table |
| `tempdb.rds_us_report_18916` | Report staging / temp table |
| `rds_us_rds_bjrep_18916` | Report staging / temp table |
| `rds_us_rds_phrep_18916` | Report staging / temp table |
| `rds_us_rds_indrep_18916` | Report staging / temp table |
| `rds_us_rds_usrep_18916` | Report staging / temp table |
| `rds_us_dim_18916` | Report staging / temp table |
| `rds_us_orders_sum_18916` | Report staging / temp table |
| `rds_us_orders_delete_18916` | Report staging / temp table |
| `rds_us_orders_delete_partial_18916` | Report staging / temp table |
| `rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |
| `tempdb.rds_us_report_18916` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_us.dim_pub_customer_info`, `dim_us.dim_pub_manager`, `ods_gbl.ods_cis_mygbl_global_employee`, `ods_gbl.ods_cis_mygbl_global_location_rt`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_inv_tran_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_us_customers_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_us_users_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_us_orders_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_us_orders_125_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.rds_us_report_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rds_us_rds_bjrep_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rds_us_rds_phrep_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rds_us_rds_indrep_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `rds_us_rds_usrep_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rds_us_dim_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `rds_us_orders_sum_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `rds_us_orders_delete_18916`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 14 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 16 -- finalize `tempdb.rds_us_report_18916`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `a.order_type` | `order_type` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:40` |
| `order_no` | `a.order_no` | `order_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:41` |
| `cpo_no` | `trim(a.ext_ref)` | `ext_ref` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | udf | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:42` |
| `order_line_no` | `b.order_line_no` | `order_line_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:43` |
| `order_delete_date` | `a.delete_date` | `delete_date` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:44` |
| `order_line_delete_date` | `b.delete_date` | `delete_date` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:45` |
| `entry_datetime` | `a.entry_datetime` | `entry_datetime` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:46` |
| `total_order` | `a.total_order` | `total_order` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:47` |
| `entry_id` | `a.entry_id` | `entry_id` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:48` |
| `to_acct_no` | `a.to_acct_no` | `to_acct_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:49` |
| `from_ref_type` | `c.from_ref_type` | `from_ref_type` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:50` |
| `cpo_id` | `a.int_ref_no` | `int_ref_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:51` |
| `cpo_type` | `a.int_ref_type` | `int_ref_type` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:52` |
| `from_loc_no` | `a.from_loc_no` | `from_loc_no` | `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_inv_tran_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_inv_tran_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_soldto_rt`, `ods_us.ods_cis_corp_service_contract_header`, `ods_us.ods_cis_corp_service_contract_line_sum`, `rds_us_orders_125_18916` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql:53` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `cpo` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_gbl.ods_cis_mygbl_global_employee` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_gbl.ods_cis_mygbl_global_location_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_order_soldto_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_history_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_history_soldto_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_inv_tran_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_history_inv_tran_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_service_contract_header` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |
| `ods_us.ods_cis_corp_service_contract_line_sum` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_cpo/etl/cpo_service_contract_global_employee_rds_18916.sql` (source_kind: rds_report_sql).*
