# REPORT: Please correct the attached Inventory Report.  US Report 5501. (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_inventory.inv_qty_aging_runrate_rio_location_rds_5501
- domain: RDS/starrocks_inventory
- one_line_purpose: RDS inventory report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_inventory/inv_qty_aging_runrate_rio_location_rds_5501.md
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
| **column_count** | 94 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_inventory inv_qty_aging_runrate_rio_location_rds_5501" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_us.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `dw_us.dwd_disty_inv_qty_df` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `ods_us.ods_cis_corp_cws_cop_ship_progress` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `dw_us.dws_disty_pur_ips_runrate_1w` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `ods_us.ods_cis_corp_bom_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `ods_us.ods_cis_corp_bom_cost_var_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `ods_us.ods_cis_corp_part_prod_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `ods_us.ods_cis_corp_dw_vend_pl_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **upstream:** `ods_us.ods_cis_corp_vend_master_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |

### Key filters and ETL business logic
- `b.prod_type IN ('A', 'K', 'R', 'S') AND b.abc_code IN ('A', 'B', 'C', 'T', 'E') AND b.vend_no IN (13439, 50633)`
- `cws.order_type = 18`
- `rds_tmp.sku_no = b.sku_no AND rds_tmp.inv_type = b.inv_type; create table tempdb.t_total_qty_rio_5501 as SELECT sku_no, inv_type, SUM(COALESCE(cws.order_qty, 0)) as total_qty_rio F…`
- `rds_tmp.sku_no = b.sku_no AND rds_tmp.inv_type = b.inv_type; -- Update Other_RIO UPDATE tempdb.rds_tmp SET Other_RIO = total_qty_rio - DFR_RIO - DAT_RIO - DGA_RIO - DSW_RIO - DIN_R…`
- `rds_tmp.sku_no = b.sku_no AND rds_tmp.inv_type = b.inv_type; -- Create BOM table CREATE TABLE tempdb.t_bom_5501 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS SELECT uuid_numeric() as …`
- `t_kit_5501.sku_no = b.sku_no; -- Update main table with BOM costs UPDATE tempdb.rds_tmp SET bom_system_cost = b.bom_system_cost + COALESCE(b.cost_variance, 0), bom_base_cost = b.bo…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (13 objects).
2. Build staging temps (10 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_us.ods_cis_corp_part_master_rt"]
  P1["dw_us.dwd_disty_inv_qty_df"]
  P2["ods_us.ods_cis_corp_cws_cop_ship_progress"]
  P3["dw_us.dwd_disty_inv_aging_df"]
  P4["dw_us.dws_disty_pur_ips_runrate_1w"]
  P5["ods_us.ods_cis_corp_bom_rt"]
  P6["ods_us.ods_cis_corp_bom_cost_var_rt"]
  P7["ods_us.ods_cis_corp_part_prod_detail_rt"]
  T0["tempdb.rds_tmp"]
  T1["tempdb.t_sku_5501"]
  T2["tempdb.t_rio_5501"]
  T3["tempdb.t_total_qty_rio_5501"]
  T4["tempdb.t_rr_5501_max_week"]
  T5["tempdb.t_rr_5501"]
  T6["tempdb.t_bom_5501"]
  T7["tempdb.t_var_5501"]
  T8["tempdb.t_kit_5501"]
  T9["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_us.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cws_cop_ship_progress` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `dw_us.dws_disty_pur_ips_runrate_1w` | Permanent warehouse source |
| `ods_us.ods_cis_corp_bom_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_bom_cost_var_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_part_prod_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_dw_vend_pl_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vend_master_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vendor_xref_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vend_user_matrix_rt` | Permanent warehouse source |
| `dim_us.dim_pub_manager` | Permanent warehouse source |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.t_sku_5501` | Report staging / temp table |
| `tempdb.t_rio_5501` | Report staging / temp table |
| `tempdb.t_total_qty_rio_5501` | Report staging / temp table |
| `tempdb.t_rr_5501_max_week` | Report staging / temp table |
| `tempdb.t_rr_5501` | Report staging / temp table |
| `tempdb.t_bom_5501` | Report staging / temp table |
| `tempdb.t_var_5501` | Report staging / temp table |
| `tempdb.t_kit_5501` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `ods_us.ods_cis_corp_bom_rt`, `ods_us.ods_cis_corp_bom_cost_var_rt`, `ods_us.ods_cis_corp_part_prod_detail_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_vend_master_rt`, `ods_us.ods_cis_corp_vendor_xref_rt`, `ods_us.ods_cis_corp_vend_user_matrix_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.t_sku_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.t_rio_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.t_total_qty_rio_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.t_rr_5501_max_week`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.t_rr_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `tempdb.t_bom_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `tempdb.t_var_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `tempdb.t_kit_5501`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `id` | `uuid_numeric()` | `uuid_numeric` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | udf | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:24` |
| `abc_code` | `b.abc_code` | `abc_code` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:25` |
| `prod_type` | `b.prod_type` | `prod_type` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:26` |
| `pp` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `pur_vend_no` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `vend_no` | `b.vend_no` | `vend_no` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:29` |
| `prod_code` | `b.prod_code` | `prod_code` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:30` |
| `vpl_no` | `b.vpl_no` | `vpl_no` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:31` |
| `vpl_code` | `CAST(NULL AS VARCHAR(40))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:32` |
| `part_no` | `b.part_no` | `part_no` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:33` |
| `sku_no` | `b.sku_no` | `sku_no` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:34` |
| `inv_type` | `1` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | rename | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:1` |
| `base_cost` | `COALESCE(b.po_cost, 0)` | `po_cost` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | coalesce | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:36` |
| `bom_base_cost` | `CAST(NULL AS DECIMAL(18,2))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:37` |
| `bom_system_cost` | `CAST(NULL AS DECIMAL(18,2))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:37` |
| `it_qty1` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty2` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty3` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty4` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty5e` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty6e` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty7e` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty8e` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty9e` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty8e1` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty8e2` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty9e1` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty9e2` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty9e3` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty9e4` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `it_qty10e` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `oh` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `oo` | `SUM(a.on_order_qty)` | `on_order_qty` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:56` |
| `bo` | `SUM(a.bo_qty)` | `bo_qty` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:57` |
| `alloc` | `SUM(a.alloc_qty)` | `alloc_qty` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:58` |
| `it` | `SUM(a.intran_in)` | `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:59` |
| `wip` | `SUM(a.wip_qty)` | `wip_qty` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:60` |
| `avail` | `SUM(a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty)` | `on_hand_qty`, `bo_qty`, `intran_in`, `intran_out`, `alloc_qty` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:61` |
| `total` | `SUM(COALESCE(on_hand_qty, 0) + COALESCE(intran_in, 0))` | `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:62` |
| `ext_amt` | `SUM(COALESCE(on_hand_qty, 0) + COALESCE(intran_in, 0)) * COALESCE(b.po_cost, 0)` | `on_hand_qty`, `intran_in`, `po_cost` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:62` |
| `other` | `CAST(0 AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:64` |
| `DFR` | `SUM(CASE WHEN loc_no = 3 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:65` |
| `DAT` | `SUM(CASE WHEN loc_no = 4 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:66` |
| `DGA` | `SUM(CASE WHEN loc_no = 502 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:67` |
| `DSW` | `SUM(CASE WHEN loc_no = 503 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:68` |
| `DIN` | `SUM(CASE WHEN loc_no = 504 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:69` |
| `DFW` | `SUM(CASE WHEN loc_no = 505 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:70` |
| `DFO` | `SUM(CASE WHEN loc_no = 506 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:71` |
| `DGR` | `SUM(CASE WHEN loc_no = 507 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:72` |
| `DCH` | `SUM(CASE WHEN loc_no = 6 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:73` |
| `DTN` | `SUM(CASE WHEN loc_no = 7 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:74` |
| `DDC` | `SUM(CASE WHEN loc_no = 9 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:75` |
| `DOR` | `SUM(CASE WHEN loc_no = 10 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:76` |
| `DON` | `SUM(CASE WHEN loc_no = 12 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:77` |
| `DOH` | `SUM(CASE WHEN loc_no = 14 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:78` |
| `DFL` | `SUM(CASE WHEN loc_no = 16 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:79` |
| `DNW` | `SUM(CASE WHEN loc_no = 27 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END)` | `loc_no`, `on_hand_qty`, `intran_in` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | case | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:80` |
| `rr10` | `CAST(0 AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:64` |
| `rr4` | `CAST(0 AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:64` |
| `rr2` | `CAST(0 AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:64` |
| `rr1` | `CAST(0 AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:64` |
| `wtd` | `CAST(0 AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:64` |
| `mfg_partno` | `b.mfg_partno` | `mfg_partno` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:86` |
| `pur_vend_name` | `CAST(NULL AS VARCHAR(60))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:87` |
| `vend_name` | `CAST(NULL AS VARCHAR(60))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:87` |
| `on_hand` | `SUM(on_hand_qty)` | `on_hand_qty` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:89` |
| `us_buyer` | `CAST(NULL AS VARCHAR(50))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:90` |
| `us_manager` | `CAST(NULL AS VARCHAR(50))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:90` |
| `PM` | `CAST(NULL AS VARCHAR(50))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:90` |
| `qty60up` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `age60up` | `CAST(NULL AS DECIMAL(18,2))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:37` |
| `age90up` | `CAST(NULL AS DECIMAL(18,2))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:37` |
| `qty270up` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `age270up` | `CAST(NULL AS DECIMAL(18,2))` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:37` |
| `short_desc` | `b.short_desc` | `short_desc` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:98` |
| `long_desc` | `b.long_desc` | `long_desc` | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:99` |
| `total_qty_rio` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `Other_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DFR_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DAT_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DGA_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DSW_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DIN_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DFW_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DFO_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DGR_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DCH_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DTN_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DDC_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DOR_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DON_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DOH_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DFL_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |
| `DNW_RIO` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_qty_df`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_sku_5501`, `tempdb.t_rio_5501`, `tempdb.ods_cis_corp_cws_cop_ship_progress`, `tempdb.t_total_qty_rio_5501`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tempdb.t_rr_5501_max_week`, `tempdb.t_rr_5501` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:27` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` | no |

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
-- See full script: source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_us.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_cws_cop_ship_progress` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `dw_us.dws_disty_pur_ips_runrate_1w` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_bom_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_bom_cost_var_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_part_prod_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_dw_vend_pl_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_vend_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_vendor_xref_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `ods_us.ods_cis_corp_vend_user_matrix_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` (source_kind: rds_report_sql).*
