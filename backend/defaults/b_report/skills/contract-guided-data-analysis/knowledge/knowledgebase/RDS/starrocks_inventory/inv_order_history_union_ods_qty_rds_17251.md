# REPORT: case when a1.ship_date is not null (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_inventory.inv_order_history_union_ods_qty_rds_17251
- domain: RDS/starrocks_inventory
- one_line_purpose: RDS inventory report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_inventory/inv_order_history_union_ods_qty_rds_17251.md
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
| **column_count** | 22 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_inventory inv_order_history_union_ods_qty_rds_17251" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_us.ods_cis_corp_mc_order_ref_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_manager_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_territory_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_customer_mymdm_customer_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_order_profile_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_history_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |

### Key filters and ETL business logic
- `c.vend_no IN (81051)`
- `c.vend_no IN (81051) ; drop table if exists tempdb.tmp_us_sku_17251; create table tempdb.tmp_us_sku_17251 as select distinct SKU as sku_no from tempdb.tmp_us_report_17251 ; drop ta…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (11 objects).
2. Build staging temps (5 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_us.ods_cis_corp_mc_order_ref_rt"]
  P1["ods_us.ods_cis_corp_order_detail_rt"]
  P2["dim_us.dim_pub_part_info"]
  P3["ods_us.ods_cis_corp_order_header_rt"]
  P4["ods_us.ods_cis_corp_manager_rt"]
  P5["ods_us.ods_cis_corp_territory_rt"]
  P6["ods_us.ods_customer_mymdm_customer_header_rt"]
  P7["ods_us.ods_cis_corp_order_profile_rt"]
  T0["tempdb.tmp_us_report_17251"]
  T1["tempdb.tmp_us_sku_17251"]
  T2["tempdb.tmp_us_oh_17251"]
  T3["tempdb.rds_tmp"]
  T4["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  P0 --> T0
  T4 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_us.ods_cis_corp_mc_order_ref_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_manager_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_territory_rt` | Permanent warehouse source |
| `ods_us.ods_customer_mymdm_customer_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_profile_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_us.ods_dw_prod_dws_dw_inv_qty` | Permanent warehouse source |
| `tempdb.tmp_us_report_17251` | Report staging / temp table |
| `tempdb.tmp_us_sku_17251` | Report staging / temp table |
| `tempdb.tmp_us_oh_17251` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_dw_prod_dws_dw_inv_qty`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.tmp_us_report_17251`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.tmp_us_sku_17251`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.tmp_us_oh_17251`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 8 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `Order` | `a.order_no as 'Order #'` | `order_no` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:3` |
| `Date` | `b.entry_datetime as 'Order Date'` | `entry_datetime` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:4` |
| `type` | `a.order_type as 'Order type'` | `order_type`, `type` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:5` |
| `Line` | `a.order_line_no as 'Order Line#'` | `order_line_no`, `Line` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:6` |
| `Cust` | `a1.to_acct_no as 'Cust'` | `to_acct_no`, `Cust` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:7` |
| `Name` | `f.cust_name as 'Cust Name'` | `cust_name`, `Cust`, `Name` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:8` |
| `Qty` | `b.order_qty as 'Qty'` | `order_qty`, `Qty` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:9` |
| `PO` | `a.int_ref_no as 'Synnex PO#'` | `int_ref_no`, `Synnex`, `PO` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:10` |
| `Date` | `a.entry_datetime as 'PO Created Date'` | `entry_datetime`, `PO`, `Created` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:11` |
| `SKU` | `b.sku_no as 'SKU'` | `sku_no`, `SKU` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:12` |
| `Part` | `c.mfg_partno as 'MFG Part#'` | `mfg_partno`, `MFG`, `Part` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:13` |
| `Part` | `c.part_no as 'Part#'` | `part_no`, `Part` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:14` |
| `Warehouse` | `a1.from_loc_no as 'Warehouse'` | `from_loc_no`, `Warehouse` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:15` |
| `Creator` | `concat(d.firstname, ' ', d.lastname) as 'Creator'` | `firstname`, `lastname`, `Creator` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | udf | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:16` |
| `Terr` | `a1.sales_terr as 'Sales Terr#'` | `sales_terr`, `Sales`, `Terr` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:17` |
| `Name` | `e.terr_name as 'Sales Terr Name'` | `terr_name`, `Sales`, `Terr`, `Name` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:18` |
| `COMPLETE` | `h.profile_c as 'ORDER STATUS SHIP COMPLETE'` | `profile_c`, `STATUS`, `SHIP`, `COMPLETE` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:23` |
| `Status` | `case when a1.delete_date is not null then 'Yes' else 'No' end as 'ORDER Delete Status'` | `delete_date`, `Yes`, `No`, `Delete`, `Status` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | case | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:3` |
| `Status` | `a1.ship_method as 'Ship Method Status'` | `ship_method`, `Ship`, `Method`, `Status` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:28` |
| `Date` | `a1.invoice_date as 'Invoice Date'` | `invoice_date`, `Invoice` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:29` |
| `CREATOR` | `concat(g.firstname, ' ', g.lastname) as 'SALES ORDER CREATOR'` | `firstname`, `lastname`, `SALES`, `CREATOR` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | udf | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:30` |
| `PO` | `a1.ext_ref as 'Customer PO#'` | `ext_ref`, `Customer`, `PO` | `ods_us.ods_cis_corp_mc_order_ref_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_manager_rt`, `ods_us.ods_cis_corp_territory_rt`, `ods_us.ods_customer_mymdm_customer_header_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `tempdb.tmp_us_report_17251`, `tempdb.tmp_us_sku_17251` | partial | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql:31` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` | no |

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
-- See full script: source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_us.ods_cis_corp_mc_order_ref_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_manager_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_territory_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_customer_mymdm_customer_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_order_profile_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_history_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |
| `ods_us.ods_dw_prod_dws_dw_inv_qty` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_inventory/etl/inv_order_history_union_ods_qty_rds_17251.sql` (source_kind: rds_report_sql).*
