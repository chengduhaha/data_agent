# REPORT: RDS inventory report SQL — inv rollover true aging rds 10968 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_inventory.inv_rollover_true_aging_rds_10968
- domain: RDS/vertica_inventory
- one_line_purpose: RDS inventory report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_inventory/inv_rollover_true_aging_rds_10968.md
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
| **column_count** | 27 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_inventory inv_rollover_true_aging_rds_10968" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dw_us.dwd_disty_inv_true_aging_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dim_us.dim_pub_vendor_info` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dim_us.dim_pub_vpl_info` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dim_us.dim_pub_vend_user_matrix` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dim_us.dim_pub_manager` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dim_us.dim_disty_v_pm_vpc_matrix_view` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **upstream:** `dw_us.dwd_disty_inv_qty_df` — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |

### Key filters and ETL business logic
- `b.date_flag = current_date() - 1 and b.report_type = 240 and b.inv_type in (1, 2, 300)`
- `b.view_level = 'IT_PART' and b.date_flag = current_date() - 1 and b.inv_type in (1, 2, 300)`
- `b.date_flag = current_date() - 1 and b.inv_type in (1, 2, 300)`
- `a.date_flag = m.date_flag and a.vend_no = m.vend_no and a.vpl_no = m.vpl_no ; update report_us10968 a set vend_name = b.vend_name from dim_us.dim_pub_vendor_info b where a.vend_no …`
- `b.pm_role = 'PM' and b.is_primary = 'N' and b.is_backup = 'N' ; drop table if exists add_pm_agg_us10968; create local temporary table add_pm_agg_us10968 on commit preserve rows as …`
- `a.vend_no = g.vend_no and a.vpl_no = g.vpl_no ; update report_us10968 a set pm_director = trim(c.firstname) || ' ' || trim(c.lastname) ,pm_director_email = e.email from dim_us.dim_…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (12 objects).
2. Build staging temps (10 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_inv_aging_rollover_rtv2_df"]
  P1["dw_us.dwd_disty_inv_aging_df"]
  P2["dim_us.dim_pub_part_info"]
  P3["dw_us.dwd_disty_inv_true_aging_df"]
  P4["dim_us.dim_pub_vendor_info"]
  P5["dim_us.dim_pub_vpl_info"]
  P6["dim_us.dim_pub_vend_user_matrix"]
  P7["dim_us.dim_pub_manager"]
  T0["report_us10968"]
  T1["aging_us10968"]
  T2["true_aging_us10968"]
  T3["metrics_upd_us10968"]
  T4["add_pm_rows_us10968"]
  T5["add_pm_agg_us10968"]
  T6["report_us10968_vend"]
  T7["sku_oh_us10968"]
  T8["rdsetl.rds_tmp"]
  T9["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_true_aging_df` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_info` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_info` | Permanent warehouse source |
| `dim_us.dim_pub_vend_user_matrix` | Permanent warehouse source |
| `dim_us.dim_pub_manager` | Permanent warehouse source |
| `dim_us.dim_disty_v_pm_vpc_matrix_view` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `dim_us.dim_pub_vend_location_view` | Permanent warehouse source |
| `dim_us.dim_pub_terms_file_view` | Permanent warehouse source |
| `report_us10968` | Report staging / temp table |
| `aging_us10968` | Report staging / temp table |
| `true_aging_us10968` | Report staging / temp table |
| `metrics_upd_us10968` | Report staging / temp table |
| `add_pm_rows_us10968` | Report staging / temp table |
| `add_pm_agg_us10968` | Report staging / temp table |
| `report_us10968_vend` | Report staging / temp table |
| `sku_oh_us10968` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager`, `dim_us.dim_disty_v_pm_vpc_matrix_view`, `dw_us.dwd_disty_inv_qty_df`, `dim_us.dim_pub_vend_location_view`, `dim_us.dim_pub_terms_file_view`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `report_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `aging_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `true_aging_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `metrics_upd_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `add_pm_rows_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `add_pm_agg_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `report_us10968_vend`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `sku_oh_us10968`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `date_flag` | `b.date_flag` | `date_flag` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:6` |
| `vend_no` | `b.vend_no` | `vend_no` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:7` |
| `vend_name` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `vpl_no` | `b.vpl_no` | `vpl_no` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:9` |
| `vpc_code` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `all_rollover_amount_240_up` | `sum(ifnull(b.rollover, 0) * ifnull(b.ave_cost, 0))` | `rollover`, `ave_cost` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | agg | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:11` |
| `type_2_rollover_240_up` | `sum(case when b.inv_type = 2 then ifnull(b.rollover, 0) * ifnull(b.ave_cost, 0) else 0 end)` | `inv_type`, `rollover`, `ave_cost` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | case | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:12` |
| `all_true_240_up` | `cast(null as numeric(19, 4))` | `numeric` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:13` |
| `all_aging_360_up` | `cast(null as numeric(19, 4))` | `numeric` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:13` |
| `us_buyer` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `us_buyer_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `us_buyer_manager` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `us_buyer_manager_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `us_buyer_director` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `us_buyer_director_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm_manager` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm_manager_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `additional_pm` | `cast(null as varchar(600))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:25` |
| `additional_pm_email` | `cast(null as varchar(600))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:25` |
| `pm_director` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm_director_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm_vp` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `pm_vp_email` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `vcm` | `cast(null as varchar(60))` | — | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:8` |
| `total_oh_amt` | `cast(null as numeric(19, 4))` | `numeric` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df`, `dw_us.dwd_disty_inv_aging_df`, `dim_us.dim_pub_part_info`, `dw_us.dwd_disty_inv_true_aging_df`, `report_us10968`, `aging_us10968`, `true_aging_us10968`, `metrics_upd_us10968`, `dim_us.dim_pub_vendor_info`, `dim_us.dim_pub_vpl_info`, `dim_us.dim_pub_vend_user_matrix`, `dim_us.dim_pub_manager` | cast | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:13` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` | no |

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
-- See full script: source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dw_us.dwd_disty_inv_true_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_vpl_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_vend_user_matrix` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_disty_v_pm_vpc_matrix_view` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_vend_location_view` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |
| `dim_us.dim_pub_terms_file_view` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` (source_kind: rds_report_sql).*
