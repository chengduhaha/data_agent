# REPORT: RDS inventory report SQL — inv ship bo detail serial tracking rds 6525 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_inventory.inv_ship_bo_detail_serial_tracking_rds_6525
- domain: RDS/starrocks_inventory
- one_line_purpose: RDS inventory report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_inventory/inv_ship_bo_detail_serial_tracking_rds_6525.md
- ref_evidence: source/ref/RDS/starrocks_inventory/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `inventory` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_inventory` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 27 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_inventory inv_ship_bo_detail_serial_tracking_rds_6525" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_ca.dwd_disty_pub_dw_orders_extend_di` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `dw_ca.dwd_disty_brpt_bo_detail_df` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_location_info_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_ship_method` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_uni_eta_log_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `dm_ca.dm_pur_unieta_sku_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **upstream:** `ods_ca.ods_cis_corp_serial_nbr_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`
- **downstream:** `tempdb.t_6525` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `inventory` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_inventory/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `inventory` |
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

- **Source:** [source/contracts/rds/starrocks_inventory/metric-index.md](../../../../source/contracts/rds/starrocks_inventory/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |

### Key filters and ETL business logic
- `date_flag >= date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d') and date_flag < date_format(current_date(),'%Y-%m-%d') and cust_no = 1009095 ; insert into tempdb.t…`
- `inv_type = 1`
- `a.order_no=b.order_no AND a.order_type=b.order_type AND a.sku_no=b.sku_no ; drop table if exists tempdb.t_ser1_no_6525; create table tempdb.t_ser1_no_6525 as select order_no, order…`
- `t2_6525.order_no = b.order_no and t2_6525.order_type = b.order_type and t2_6525.sku_no = b.sku_no ; drop table if exists tempdb.track_6525; create table tempdb.track_6525 as select…`
- `t2_6525.order_type = b.order_type and t2_6525.order_no = b.order_no ; drop table if exists tempdb.rds_inv_qty_6525; create table tempdb.rds_inv_qty_6525 as select sku_no, loc_no, s…`
- `t2_6525.sku_no = b.sku_no and t2_6525.from_loc_no = b.loc_no ; drop table if exists tempdb.rds_tmp; create table tempdb.rds_tmp as select cust_po_no, order_type, order_no, order_li…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (13 objects).
2. Build staging temps (11 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_ca.dwd_disty_pub_dw_orders_extend_di"]
  P1["dw_ca.dwd_disty_brpt_bo_detail_df"]
  P2["ods_ca.ods_cis_corp_part_master_rt"]
  P3["ods_ca.ods_cis_corp_order_header_rt"]
  P4["ods_ca.ods_cis_corp_history_header_rt"]
  P5["ods_ca.ods_cis_corp_location_info_rt"]
  P6["ods_ca.ods_cis_corp_ship_method"]
  P7["ods_ca.ods_cis_corp_uni_eta_log_rt"]
  T0["tempdb.t_6525"]
  T1["tempdb.t1_6525"]
  T2["tempdb.eta"]
  T3["tempdb.t2_6525"]
  T4["tempdb.t_ser_no_6525"]
  T5["tempdb.t_ser1_no_6525"]
  T6["tempdb.track_6525"]
  T7["tempdb.track1_6525"]
  T8["tempdb.rds_inv_qty_6525"]
  T9["tempdb.rds_tmp"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  O2["tempdb.t_6525"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_ca.dwd_disty_pub_dw_orders_extend_di` | Permanent warehouse source |
| `dw_ca.dwd_disty_brpt_bo_detail_df` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_location_info_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_ship_method` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_uni_eta_log_rt` | Permanent warehouse source |
| `dm_ca.dm_pur_unieta_sku_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_serial_nbr_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_serial_nbr_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_carton_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_inv_qty_rt` | Permanent warehouse source |
| `tempdb.t_6525` | Report staging / temp table |
| `tempdb.t1_6525` | Report staging / temp table |
| `tempdb.eta` | Report staging / temp table |
| `tempdb.t2_6525` | Report staging / temp table |
| `tempdb.t_ser_no_6525` | Report staging / temp table |
| `tempdb.t_ser1_no_6525` | Report staging / temp table |
| `tempdb.track_6525` | Report staging / temp table |
| `tempdb.track1_6525` | Report staging / temp table |
| `tempdb.rds_inv_qty_6525` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |
| `tempdb.t_6525` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_ca.dwd_disty_pub_dw_orders_extend_di`, `dw_ca.dwd_disty_brpt_bo_detail_df`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `ods_ca.ods_cis_corp_serial_nbr_rt`, `ods_ca.ods_cis_corp_history_serial_nbr_rt`, `ods_ca.ods_cis_corp_carton_header_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.t_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.t1_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.eta`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.t2_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.t_ser_no_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.t_ser1_no_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `tempdb.track_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `tempdb.track1_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `tempdb.rds_inv_qty_6525`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 14 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `tempdb.t_6525`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `order_type` | `order_type` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:5` |
| `order_line_no` | `order_line_no` | `order_line_no` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:6` |
| `cust_po_no` | `cast(null as varchar(100))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:7` |
| `order_no` | `order_no` | `order_no` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:8` |
| `sku_no` | `sku_no` | `sku_no` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:9` |
| `part_no` | `cast(null as varchar(60))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:10` |
| `unit_net_price` | `unit_price` | `unit_price` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | rename | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:11` |
| `extend_net_price` | `order_qty*unit_price` | `order_qty`, `unit_price` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | arithmetic | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:49` |
| `invoice_date` | `cast(null as date)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:50` |
| `exp_ship_date` | `cast(null as varchar(10))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:14` |
| `ship_date` | `cast(null as date)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:50` |
| `order_qty` | `order_qty` | `order_qty` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:16` |
| `ship_qty` | `cast(null as int)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:16` |
| `ship_to_name` | `cast(null as varchar(60))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:10` |
| `ship_to_addr` | `cast(null as varchar(60))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:10` |
| `from_loc_no` | `cast(null as int)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:16` |
| `from_loc_name` | `cast(null as varchar(60))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:10` |
| `ship_method` | `cast(null as varchar(30))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:22` |
| `ship_desc` | `cast(null as varchar(60))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:10` |
| `tracking_no` | `cast(null as varchar(10000))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:24` |
| `serial_no` | `cast(null as varchar(30000))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:25` |
| `avail` | `cast(null as int)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:16` |
| `on_hand` | `cast(null as int)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:16` |
| `on_order` | `cast(null as int)` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:16` |
| `ETA` | `cast(null as varchar(10))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:14` |
| `ETA_code` | `cast(null as char(3))` | `char` | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:30` |
| `marketing_comments` | `cast(null as varchar(255))` | — | `dw_ca.dwd_disty_brpt_bo_detail_df`, `tempdb.t_6525`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_location_info_rt`, `ods_ca.ods_cis_corp_ship_method`, `ods_ca.ods_cis_corp_uni_eta_log_rt`, `dm_ca.dm_pur_unieta_sku_detail_rt`, `tempdb.t1_6525`, `tempdb.eta`, `min_cte` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql:31` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `inventory` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_ca.dwd_disty_pub_dw_orders_extend_di` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `dw_ca.dwd_disty_brpt_bo_detail_df` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_location_info_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_ship_method` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_uni_eta_log_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `dm_ca.dm_pur_unieta_sku_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_serial_nbr_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_history_serial_nbr_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_carton_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |
| `ods_ca.ods_cis_corp_inv_qty_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_inventory/etl/inv_ship_bo_detail_serial_tracking_rds_6525.sql` (source_kind: rds_report_sql).*
