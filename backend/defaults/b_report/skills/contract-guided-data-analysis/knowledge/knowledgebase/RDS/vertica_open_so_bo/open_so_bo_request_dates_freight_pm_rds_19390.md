# REPORT: RDS open_so_bo report SQL — open so bo request dates freight pm rds 19390 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_open_so_bo.open_so_bo_request_dates_freight_pm_rds_19390
- domain: RDS/vertica_open_so_bo
- one_line_purpose: RDS open_so_bo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_request_dates_freight_pm_rds_19390.md
- ref_evidence: source/ref/RDS/vertica_open_so_bo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `open_so_bo` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_open_so_bo` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 41 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_open_so_bo open_so_bo_request_dates_freight_pm_rds_19390" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_sales_open_order_detail` — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql`
- **upstream:** `ods_us.ods_cis_corp_order_frt_detail` — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql`
- **upstream:** `dim_us.dim_pub_vpl_pm_hierarchy_info` — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `open_so_bo` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_open_so_bo/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/vertica_open_so_bo/metric-index.md](../../../../source/contracts/rds/vertica_open_so_bo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` |

### Key filters and ETL business logic
- `a.request_delivery_date is not null or a.requested_ship_date is not null ; update t_orders_19390 a set pm_name = b.pm_name, pm_manager_name = b.pm_manager_name, pm_director_name = …`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (3 objects).
2. Build staging temps (3 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_sales_open_order_detail"]
  P1["ods_us.ods_cis_corp_order_frt_detail"]
  P2["dim_us.dim_pub_vpl_pm_hierarchy_info"]
  T0["t_orders_19390"]
  T1["rdsetl.rds_tmp"]
  T2["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T2 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_sales_open_order_detail` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_frt_detail` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_pm_hierarchy_info` | Permanent warehouse source |
| `t_orders_19390` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `t_orders_19390`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 6 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `a.order_type` | `order_type` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:4` |
| `order_no` | `a.order_no` | `order_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:5` |
| `from_loc_no` | `a.from_loc_no` | `from_loc_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:6` |
| `from_loc_char` | `a.from_loc_char` | `from_loc_char` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:7` |
| `inv_type` | `a.inv_type` | `inv_type` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:8` |
| `sales_terr` | `a.sales_terr` | `sales_terr` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:9` |
| `terr_name` | `a.terr_name` | `terr_name` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:10` |
| `sales_rep_id` | `a.sales_rep_id` | `sales_rep_id` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:11` |
| `sales_rep_name` | `a.sales_rep_name` | `sales_rep_name` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:12` |
| `ship_method` | `a.ship_method` | `ship_method` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:13` |
| `service_days` | `b.service_days` | `service_days` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:14` |
| `expected_date` | `a.expected_date` | `expected_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:15` |
| `request_delivery_date` | `a.request_delivery_date` | `request_delivery_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:16` |
| `requested_ship_date` | `a.requested_ship_date` | `requested_ship_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:17` |
| `bill_to_cust_no` | `a.cust_no` | `cust_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:18` |
| `bill_to_cust_name` | `a.cust_name` | `cust_name` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:19` |
| `bill_to_cust_addr` | `a.bill_to_cust_addr` | `bill_to_cust_addr` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:20` |
| `bill_to_cust_zip` | `a.bill_to_cust_zip` | `bill_to_cust_zip` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:21` |
| `bill_to_cust_city` | `a.bill_to_cust_city` | `bill_to_cust_city` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:22` |
| `bill_to_cust_state` | `a.bill_to_cust_state` | `bill_to_cust_state` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:23` |
| `bill_to_cust_country` | `a.bill_to_cust_country` | `bill_to_cust_country` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:24` |
| `bill_to_contact_name` | `a.bill_to_contact_name` | `bill_to_contact_name` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:25` |
| `bill_to_contact_email` | `a.bill_to_contact_email` | `bill_to_contact_email` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:26` |
| `bill_to_contact_phone` | `a.bill_to_contact_phone` | `bill_to_contact_phone` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:27` |
| `order_date` | `a.order_date` | `order_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:28` |
| `sales_rel_date` | `a.sales_rel_date` | `sales_rel_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:29` |
| `credit_rel_date` | `a.credit_rel_date` | `credit_rel_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:30` |
| `sku_no` | `a.sku_no` | `sku_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:31` |
| `vpl_no` | `a.vpl_no` | `vpl_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:32` |
| `vend_no` | `a.vend_no` | `vend_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:33` |
| `part_no` | `a.part_no` | `part_no` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:34` |
| `mfg_partno` | `a.mfg_partno` | `mfg_partno` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:35` |
| `order_qty` | `a.order_qty` | `order_qty` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:36` |
| `ship_qty` | `a.ship_qty` | `ship_qty` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:37` |
| `base_cost` | `a.base_cost` | `base_cost` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:38` |
| `eta_code` | `a.eta_code` | `eta_code` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:39` |
| `eta_date` | `a.eta_date` | `eta_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:40` |
| `est_delivery_date` | `a.est_delivery_date` | `est_delivery_date` | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:41` |
| `pm_name` | `cast(null as varchar(80))` | — | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:42` |
| `pm_manager_name` | `cast(null as varchar(80))` | — | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:42` |
| `pm_director_name` | `cast(null as varchar(80))` | — | `dw_us.dwd_disty_sales_open_order_detail`, `ods_us.ods_cis_corp_order_frt_detail`, `dim_us.dim_pub_vpl_pm_hierarchy_info`, `t_orders_19390`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:42` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` | no |

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
-- See full script: source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_sales_open_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` |
| `ods_us.ods_cis_corp_order_frt_detail` | FROM/JOIN source | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` |
| `dim_us.dim_pub_vpl_pm_hierarchy_info` | FROM/JOIN source | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` (source_kind: rds_report_sql).*
