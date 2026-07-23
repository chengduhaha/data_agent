# REPORT: RDS inventory report SQL — inv rollover witypestu stock rotation rds 11722 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_inventory.inv_rollover_witypestu_stock_rotation_rds_11722
- domain: RDS/vertica_inventory
- one_line_purpose: RDS inventory report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_inventory/inv_rollover_witypestu_stock_rotation_rds_11722.md
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
| **column_count** | 20 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_inventory inv_rollover_witypestu_stock_rotation_rds_11722" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_date` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dim_us.dim_pub_vendor_info` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dw_us.dwd_disty_inv_qty_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dw_us.dwd_disty_common_pos_di` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dm_us.dm_disty_pur_purch_forecast461_rtv2` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dw_us.dwd_pub_common_order_header_extend` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dw_us.dwd_disty_sales_open_order_detail` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |

### Key filters and ETL business logic
- `date_flag = current_date() - 1`
- `date_flag = current_date()`
- `cal.w = (select w_y from dates_us11722`
- `cal.m = (select m_t from dates_us11722`
- `vend_no > 0 only (no active_status filter). Match that grain so #t_res / final row counts align. create local temporary table t_vpl_us11722 on commit preserve rows as select a.vend…`
- `b.discontinued in ('N', 'n') ; drop table if exists t_inv_us11722; create local temporary table t_inv_us11722 on commit preserve rows as select b.prod_code as prod_code ,b.vpl_no a…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (18 objects).
2. Build staging temps (19 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_date"]
  P1["dim_us.dim_pub_part_info"]
  P2["dim_us.dim_pub_vendor_info"]
  P3["dw_us.dwd_disty_inv_qty_df"]
  P4["dw_us.dwd_disty_inv_aging_df"]
  P5["dw_us.dwd_disty_common_pos_di"]
  P6["dm_us.dm_disty_pur_purch_forecast461_rtv2"]
  P7["dw_us.dwd_pub_common_order_header_extend"]
  T0["dates_us11722"]
  T1["win_us11722"]
  T2["t_vpl_us11722"]
  T3["t_res_us11722"]
  T4["t_inv_us11722"]
  T5["t_aging_us11722"]
  T6["t_sales_us11722"]
  T7["t_sales_2_us11722"]
  T8["t_rec_mtd_us11722"]
  T9["so_alo_us11722"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_date` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_info` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `dw_us.dwd_disty_common_pos_di` | Permanent warehouse source |
| `dm_us.dm_disty_pur_purch_forecast461_rtv2` | Permanent warehouse source |
| `dw_us.dwd_pub_common_order_header_extend` | Permanent warehouse source |
| `dw_us.dwd_disty_sales_open_order_detail` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` | Permanent warehouse source |
| `dw_us.dws_disty_pur_ips_runrate_1w` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_info` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_hierarchy_info` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_pm_hierarchy_info` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_xref` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vend_master_etc` | Permanent warehouse source |
| `dim_us.dim_pub_list_box_detail` | Permanent warehouse source |
| `ods_us.ods_cis_corp_prod_code_detail` | Permanent warehouse source |
| `dates_us11722` | Report staging / temp table |
| `win_us11722` | Report staging / temp table |
| `t_vpl_us11722` | Report staging / temp table |
| `t_res_us11722` | Report staging / temp table |
| `t_inv_us11722` | Report staging / temp table |
| `t_aging_us11722` | Report staging / temp table |
| `t_sales_us11722` | Report staging / temp table |
| `t_sales_2_us11722` | Report staging / temp table |
| `t_rec_mtd_us11722` | Report staging / temp table |
| `so_alo_us11722` | Report staging / temp table |
| `t_roll_us11722` | Report staging / temp table |
| `max_week_us11722` | Report staging / temp table |
| `t_w4rr_us11722` | Report staging / temp table |
| `eom_us11722` | Report staging / temp table |
| `t_roll_2_us11722` | Report staging / temp table |
| `rds_11722_final_us` | Report staging / temp table |
| `rds_tmp_11722_us` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_us.dim_pub_date`, `dim_us.dim_pub_part_info`, `dim_us.dim_pub_vendor_info`, `dw_us.dwd_disty_inv_qty_df`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dwd_disty_common_pos_di`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `dim_us.dim_pub_vpl_info`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `dates_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `win_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `t_vpl_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `t_res_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `t_inv_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `t_aging_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `t_sales_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `t_sales_2_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `t_rec_mtd_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `so_alo_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `t_roll_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `max_week_us11722`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 14 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `sku_no` | `a.sku_no` | `sku_no` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:96` |
| `active_status` | `cast(null as varchar(20))` | — | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:197` |
| `vend_no` | `a.vend_no` | `vend_no` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:26` |
| `prod_code` | `cast(null as int)` | — | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:199` |
| `vpl_no` | `cast(null as int)` | — | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:199` |
| `s4w_reg` | `sum( case when a.date_flag >= w.d_4w_begin and a.date_flag < w.d_4w_end and a.from_loc_no <> 98 then ifnull(a.ship_qt...` | `date_flag`, `d_4w_begin`, `d_4w_end`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `s4w_ds` | `sum( case when a.date_flag >= w.d_4w_begin and a.date_flag < w.d_4w_end and a.from_loc_no = 98 then ifnull(a.ship_qty...` | `date_flag`, `d_4w_begin`, `d_4w_end`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `s4w_all` | `sum( case when a.date_flag >= w.d_4w_begin and a.date_flag < w.d_4w_end then ifnull(a.ship_qty * a.unit_cost, 0) else...` | `date_flag`, `d_4w_begin`, `d_4w_end`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `s13w_reg` | `sum( case when a.date_flag >= w.d_13w_begin and a.date_flag < w.d_4w_end and a.from_loc_no <> 98 then ifnull(a.ship_q...` | `date_flag`, `d_13w_begin`, `d_4w_end`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `s13w_ds` | `sum( case when a.date_flag >= w.d_13w_begin and a.date_flag < w.d_4w_end and a.from_loc_no = 98 then ifnull(a.ship_qt...` | `date_flag`, `d_13w_begin`, `d_4w_end`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `s13w_all` | `sum( case when a.date_flag >= w.d_13w_begin and a.date_flag < w.d_4w_end then ifnull(a.ship_qty * a.unit_cost, 0) els...` | `date_flag`, `d_13w_begin`, `d_4w_end`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `pmon_reg` | `sum( case when a.date_flag >= w.d_pmon_begin and a.date_flag < w.d_mtd_begin and a.from_loc_no <> 98 then ifnull(a.sh...` | `date_flag`, `d_pmon_begin`, `d_mtd_begin`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `pmon_ds` | `sum( case when a.date_flag >= w.d_pmon_begin and a.date_flag < w.d_mtd_begin and a.from_loc_no = 98 then ifnull(a.shi...` | `date_flag`, `d_pmon_begin`, `d_mtd_begin`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `pmon_all` | `sum( case when a.date_flag >= w.d_pmon_begin and a.date_flag < w.d_mtd_begin then ifnull(a.ship_qty * a.unit_cost, 0)...` | `date_flag`, `d_pmon_begin`, `d_mtd_begin`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `ppmon_reg` | `sum( case when a.date_flag >= w.d_ppmon_begin and a.date_flag < w.d_pmon_begin and a.from_loc_no <> 98 then ifnull(a....` | `date_flag`, `d_ppmon_begin`, `d_pmon_begin`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `ppmon_ds` | `sum( case when a.date_flag >= w.d_ppmon_begin and a.date_flag < w.d_pmon_begin and a.from_loc_no = 98 then ifnull(a.s...` | `date_flag`, `d_ppmon_begin`, `d_pmon_begin`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `ppmon_all` | `sum( case when a.date_flag >= w.d_ppmon_begin and a.date_flag < w.d_pmon_begin then ifnull(a.ship_qty * a.unit_cost, ...` | `date_flag`, `d_ppmon_begin`, `d_pmon_begin`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `mtd_reg` | `sum( case when a.date_flag >= w.d_mtd_begin and a.date_flag < current_date() and a.from_loc_no <> 98 then ifnull(a.sh...` | `date_flag`, `d_mtd_begin`, `current_date`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `mtd_ds` | `sum( case when a.date_flag >= w.d_mtd_begin and a.date_flag < current_date() and a.from_loc_no = 98 then ifnull(a.shi...` | `date_flag`, `d_mtd_begin`, `current_date`, `from_loc_no`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |
| `mtd_all` | `sum( case when a.date_flag >= w.d_mtd_begin and a.date_flag < current_date() then ifnull(a.ship_qty * a.unit_cost, 0)...` | `date_flag`, `d_mtd_begin`, `current_date`, `ship_qty`, `unit_cost` | `dw_us.dwd_disty_common_pos_di`, `win_us11722`, `dim_us.dim_pub_part_info`, `t_sales_us11722`, `t_sales_2_us11722`, `dm_us.dm_disty_pur_purch_forecast461_rtv2`, `t_rec_mtd_us11722`, `dw_us.dwd_pub_common_order_header_extend`, `dw_us.dwd_disty_sales_open_order_detail`, `so_alo_us11722`, `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dates_us11722` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:187` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` | no |

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
-- See full script: source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_date` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dim_us.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dm_us.dm_disty_pur_purch_forecast461_rtv2` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dwd_pub_common_order_header_extend` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dwd_disty_sales_open_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dw_us.dws_disty_pur_ips_runrate_1w` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dim_us.dim_pub_vpl_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dim_us.dim_pub_vpl_hierarchy_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dim_us.dim_pub_vpl_pm_hierarchy_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |
| `dim_us.dim_pub_vendor_xref` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` (source_kind: rds_report_sql).*
