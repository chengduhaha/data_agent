# REPORT: Typical Inventory example: comprehensive US inventory qty/aging/runrate/RIO/customer output. (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_inventory.inv_qty_aging_runrate_rio_alloc_customer_rds_us13208
- domain: RDS/vertica_inventory
- one_line_purpose: RDS inventory report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_inventory/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.md
- ref_evidence: source/ref/RDS/vertica_inventory/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `inventory` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_inventory` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 68 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_inventory inv_qty_aging_runrate_rio_alloc_customer_rds_us13208" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_inv_qty_df` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `ods_us.ods_cis_corp_inv_qty` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dw_us.dwd_pub_pur_inv_qty_rt` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dim_us.dim_pub_vendor_info` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dw_us.dws_disty_pur_ips_runrate_1w` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dim_us.dim_pub_sku_cost` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dim_us.dim_pub_location_info` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dim_us.dim_pub_vendor_xref` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `inventory` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_inventory/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/vertica_inventory/metric-index.md](../../../../source/contracts/rds/vertica_inventory/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |

### Key filters and ETL business logic
- `date_flag = '2024-04-08'`
- `b.date_flag ='2024-04-08' ) diq LEFT JOIN dw_us.dwd_pub_pur_inv_qty_rt iq ON diq.loc_no = iq.loc_NO AND diq.inv_type = iq.inv_type AND diq.sku_no = iq.sku_no INNER JOIN dim_us.dim_…`
- `sum_type = 'WITYPESTD' AND inv_type IN (1) ) ,only_runrate_skus AS ( SELECT DISTINCT '2024-04-08' AS date_flag ,pm.sku_no ,dr.inv_type ,pm.ave_cost ,pm.po_cost ,pm.bundle_kit ,pm.p…`
- `on_hand_qty > 0`
- `a1.on_hand_qty > 0 ) a WHERE iq.sku_no = a.sku_no AND iq.sku_no IN ( SELECT sku_no FROM ( SELECT sku_no ,count(DISTINCT ave_cost) icount FROM inv_qty_temp`
- `iq.sku_no = sc.sku_no AND iq.sku_no IN ( SELECT sku_no FROM ( SELECT sku_no ,count(DISTINCT ave_cost) icount FROM inv_qty_temp`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (12 objects).
2. Build staging temps (2 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_inv_qty_df"]
  P1["ods_us.ods_cis_corp_inv_qty"]
  P2["dw_us.dwd_pub_pur_inv_qty_rt"]
  P3["dim_us.dim_pub_part_info"]
  P4["dim_us.dim_pub_vendor_info"]
  P5["dw_us.dws_disty_pur_ips_runrate_1w"]
  P6["dim_us.dim_pub_sku_cost"]
  P7["dim_us.dim_pub_location_info"]
  T0["inv_qty_temp"]
  T1["dim_pub_sku_cost"]
  O0["rdsetl.rds_tmp"]
  P0 --> T0
  T1 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `ods_us.ods_cis_corp_inv_qty` | Permanent warehouse source |
| `dw_us.dwd_pub_pur_inv_qty_rt` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_info` | Permanent warehouse source |
| `dw_us.dws_disty_pur_ips_runrate_1w` | Permanent warehouse source |
| `dim_us.dim_pub_sku_cost` | Permanent warehouse source |
| `dim_us.dim_pub_location_info` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_xref` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `dm_us.dm_disty_sales_rio_sku_inv_loc` | Permanent warehouse source |
| `dim_us.dim_pub_customer_info` | Permanent warehouse source |
| `inv_qty_temp` | Report staging / temp table |
| `dim_pub_sku_cost` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_us.dwd_disty_inv_qty_df`, `ods_us.ods_cis_corp_inv_qty`, `dw_us.dwd_pub_pur_inv_qty_rt`, `dim_us.dim_pub_part_info`, `dim_us.dim_pub_vendor_info`, `dw_us.dws_disty_pur_ips_runrate_1w`, `dim_us.dim_pub_sku_cost`, `dim_us.dim_pub_location_info`, `dim_us.dim_pub_vendor_xref`, `dw_us.dwd_disty_inv_aging_df`, `dm_us.dm_disty_sales_rio_sku_inv_loc`, `dim_us.dim_pub_customer_info`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `inv_qty_temp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `dim_pub_sku_cost`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `row_cnt` | `MAX(row_id) OVER()` | `row_id` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | agg | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:895` |
| `row_id` | `sl.row_id` | `row_id` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:901` |
| `abc_code` | `qa.abc_code` | `abc_code` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:902` |
| `prod_type` | `qa.prod_type` | `prod_type` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:903` |
| `pp_code` | `qa.pp_code` | `pp_code` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:904` |
| `purch_vend_no` | `qa.purch_vend_no` | `purch_vend_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:905` |
| `vend_no` | `qa.vend_no` | `vend_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:906` |
| `prod_code` | `qa.prod_code` | `prod_code` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:907` |
| `vpl_no` | `qa.vpl_no` | `vpl_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:908` |
| `vpl_code` | `qa.vpl_code` | `vpl_code` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:909` |
| `part_no` | `qa.part_no` | `part_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:910` |
| `sku_no` | `qa.sku_no` | `sku_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:767` |
| `inv_type` | `qa.inv_type` | `inv_type` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:768` |
| `forecast_category` | `qa.forecast_category` | `forecast_category` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:913` |
| `po_cost` | `ifnull(qa.po_cost,0)` | `po_cost` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | coalesce | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:914` |
| `ave_cost` | `ifnull(qa.ave_cost,0)` | `ave_cost` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | coalesce | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:915` |
| `po_cost_fx` | `qa.po_cost_fx` | `po_cost_fx` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:917` |
| `ave_cost_fx` | `qa.ave_cost_fx` | `ave_cost_fx` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:918` |
| `age1` | `ia.age1` | `age1` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:920` |
| `age2` | `ia.age2` | `age2` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:921` |
| `age3` | `ia.age3` | `age3` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:922` |
| `age4` | `ia.age4` | `age4` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:772` |
| `age5` | `ia.age5` | `age5` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:924` |
| `age6` | `ia.age6` | `age6` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:925` |
| `age7` | `ia.age7` | `age7` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:926` |
| `age8` | `ia.age8` | `age8` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:927` |
| `age9` | `ia.age9` | `age9` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:928` |
| `age_91` | `ia.age91` | `age91` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:929` |
| `age_10` | `ia.age10` | `age10` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:930` |
| `age_11` | `ia.age11` | `age11` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:931` |
| `age_12` | `ia.age12` | `age12` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:932` |
| `age_13` | `ia.age13` | `age13` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:933` |
| `age_14` | `ia.age14` | `age14` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:934` |
| `on_hand_qty` | `qa.on_hand_qty` | `on_hand_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:770` |
| `on_order_qty` | `qa.on_order_qty` | `on_order_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:771` |
| `bo_qty` | `qa.bo_qty` | `bo_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:938` |
| `alloc_qty` | `case when asq.sku_no is not null then ifnull(asq.alloc_kwo,0)+ifnull(asq.alloc_rio,0)+ifnull(asq.alloc_so,0) else qa....` | `sku_no`, `alloc_kwo`, `alloc_rio`, `alloc_so`, `alloc_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | case | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:939` |
| `alloc_kwo` | `asq.alloc_kwo` | `alloc_kwo` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:939` |
| `alloc_so` | `asq.alloc_so` | `alloc_so` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:939` |
| `intran_in` | `qa.intran_in` | `intran_in` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:770` |
| `wip_qty` | `qa.wip_qty` | `wip_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:944` |
| `avail_qty` | `case when asq.sku_no is not null then asq.avail_qty else qa.avail_qty end` | `sku_no`, `avail_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | case | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:945` |
| `usd_ext_cost` | `qa.usd_ext_cost` | `usd_ext_cost` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:946` |
| `ext_cost` | `qa.ext_cost` | `ext_cost` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:947` |
| `loc_no` | `qa.loc_no` | `loc_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:949` |
| `loc_char` | `qa.loc_char` | `loc_char` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:950` |
| `rio_qty` | `rl.rio_qty` | `rio_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:951` |
| `bundle_kit` | `qa.bundle_kit` | `bundle_kit` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:953` |
| `vend_currency` | `qa.vend_currency` | `vend_currency` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:954` |
| `rr_10` | `rr.rr10` | `rr10` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | rename | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:956` |
| `rr4` | `rr.rr4` | `rr4` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:957` |
| `rr2` | `rr.rr2` | `rr2` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:958` |
| `rr1` | `rr.rr1` | `rr1` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:956` |
| `rr0` | `rr.rr0` | `rr0` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:960` |
| `mfg_partno` | `qa.mfg_partno` | `mfg_partno` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:962` |
| `purch_vend_name` | `qa.purch_vend_name` | `purch_vend_name` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:963` |
| `vend_name` | `qa.vend_name` | `vend_name` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:964` |
| `short_desc` | `qa.short_desc` | `short_desc` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:965` |
| `long_desc` | `qa.long_desc` | `long_desc` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:966` |
| `mar_comment` | `qa.mar_comment` | `mar_comment` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:967` |
| `alloc_rio` | `case when asq.alloc_rio is null then ifnull(rlt.rio_qty ,0) else asq.alloc_rio end` | `alloc_rio`, `rio_qty` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | case | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:968` |
| `total` | `ifnull(qa.on_hand_qty,0)+ifnull(qa.intran_in,0)` | `on_hand_qty`, `intran_in` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | coalesce | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:969` |
| `pp_data_no` | `qa.pp_data_no` | `pp_data_no` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:970` |
| `weight` | `qa.weight` | `weight` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:971` |
| `cu_length` | `qa.cu_length` | `cu_length` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:971` |
| `cu_width` | `qa.cu_width` | `cu_width` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:971` |
| `cu_height` | `qa.cu_height` | `cu_height` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:971` |
| `custno` | `qa.custno \|\| '-' \|\| ch.cust_name` | `custno`, `cust_name` | `qtysum_all`, `sku_list_final`, `inv_aging`, `runrate`, `rio_loc`, `rio_loc_total`, `alloc_sum_qty`, `cnt`, `dim_us.dim_pub_customer_info` | arithmetic | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:971` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` — Not documented as Azkaban partition |

**Plain language:** This is on-demand report SQL. Date windows come from the script body or runtime parameters, not from warehouse ETL bootstrap jobs.

### Data quality checks
- Row counts on `rdsetl.rds_tmp` after report execution
- Spot-check measure totals vs source fact tables listed in L1 lineage

### Validation SQL
<!-- sql-artifact snippet_type: illustrative intent: audit -->
```sql
-- 1) row count on final output (session)
-- SELECT COUNT(*) FROM rdsetl.rds_tmp;

-- 2) metric sum by a key dimension (replace <dim> / <metric> from final SELECT)
-- SELECT <dim>, SUM(<metric>) FROM rdsetl.rds_tmp GROUP BY 1;

-- 3) grain duplicate check when natural key is known from SQL
-- SELECT <key_cols>, COUNT(*) FROM rdsetl.rds_tmp GROUP BY <key_cols> HAVING COUNT(*) > 1;
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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` | no |

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
-- See full script: source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `ods_us.ods_cis_corp_inv_qty` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dw_us.dwd_pub_pur_inv_qty_rt` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dim_us.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dw_us.dws_disty_pur_ips_runrate_1w` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dim_us.dim_pub_sku_cost` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dim_us.dim_pub_location_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dim_us.dim_pub_vendor_xref` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dm_us.dm_disty_sales_rio_sku_inv_loc` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |
| `dim_us.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` (source_kind: rds_report_sql).*
