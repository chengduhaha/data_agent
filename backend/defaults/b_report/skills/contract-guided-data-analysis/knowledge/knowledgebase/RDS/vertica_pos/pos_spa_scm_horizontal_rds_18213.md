# REPORT: Typical POS example: horizontal SPA/SCM expense groups on POS order lines. (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_pos.pos_spa_scm_horizontal_rds_18213
- domain: RDS/vertica_pos
- one_line_purpose: RDS pos report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_pos/pos_spa_scm_horizontal_rds_18213.md
- ref_evidence: source/ref/RDS/vertica_pos/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `pos` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_pos` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 33 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_pos pos_spa_scm_horizontal_rds_18213" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_common_pos_di` — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`
- **upstream:** `dim_us.dim_pub_part_info_rt` — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`
- **upstream:** `dw_us.dwd_pub_common_history_header_extend` — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`
- **upstream:** `dim_us.dim_pub_order_type` — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`
- **upstream:** `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `pos` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_pos/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `pos` |
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

- **Source:** [source/contracts/rds/vertica_pos/metric-index.md](../../../../source/contracts/rds/vertica_pos/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |

### Key filters and ETL business logic
- `1 = 1 and f.date_flag >= cast(trunc(timestampadd (dd, -1, getdate()), 'year') as date) and f.date_flag < current_date() and f.order_line_type <> 'Comp' and f.order_type not in (sel…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (5 objects).
2. Build staging temps (4 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_common_pos_di"]
  P1["dim_us.dim_pub_part_info_rt"]
  P2["dw_us.dwd_pub_common_history_header_extend"]
  P3["dim_us.dim_pub_order_type"]
  P4["dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di"]
  T0["table_final_data_us_18213"]
  T1["rds_scm_us_18213"]
  T2["rdsetl.rds_tmp"]
  T3["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T3 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_common_pos_di` | Permanent warehouse source |
| `dim_us.dim_pub_part_info_rt` | Permanent warehouse source |
| `dw_us.dwd_pub_common_history_header_extend` | Permanent warehouse source |
| `dim_us.dim_pub_order_type` | Permanent warehouse source |
| `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` | Permanent warehouse source |
| `table_final_data_us_18213` | Report staging / temp table |
| `rds_scm_us_18213` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_final_data_us_18213`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_scm_us_18213`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 7 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_no` | `f.order_no` | `order_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:10` |
| `order_type` | `f.order_type` | `order_type` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:11` |
| `order_line_no` | `f.order_line_no` | `order_line_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:12` |
| `ship_date` | `to_char(f.ship_date,'MM/DD/YYYY')` | `to_char`, `ship_date`, `MM`, `DD`, `YYYY` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | arithmetic | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:13` |
| `vend_no` | `f.vend_no` | `vend_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:14` |
| `vend_name` | `f.vend_name` | `vend_name` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:15` |
| `ship_qty` | `f.ship_qty` | `ship_qty` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:16` |
| `base_cost` | `f.base_cost` | `base_cost` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:17` |
| `extend_base_cost` | `f.extend_base_cost` | `extend_base_cost` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:18` |
| `bill_to_cust_no` | `f.bill_to_cust_no` | `bill_to_cust_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:19` |
| `bill_to_cust_name` | `f.bill_to_cust_name` | `bill_to_cust_name` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:20` |
| `bill_to_cust_zip` | `f.bill_to_cust_zip` | `bill_to_cust_zip` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:21` |
| `bill_to_cust_city` | `f.bill_to_cust_city` | `bill_to_cust_city` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:22` |
| `bill_to_cust_state` | `f.bill_to_cust_state` | `bill_to_cust_state` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:23` |
| `sold_to_cust_name` | `f.sold_to_cust_name` | `sold_to_cust_name` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:24` |
| `customer_po_no` | `f.cpo_no` | `cpo_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:25` |
| `sales_terr` | `f.sales_terr` | `sales_terr` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:26` |
| `terr_name` | `f.terr_name` | `terr_name` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:27` |
| `ship_to_name` | `f.ship_to_name` | `ship_to_name` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:28` |
| `ship_to_city` | `f.ship_to_city` | `ship_to_city` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:29` |
| `ship_to_zip` | `f.ship_to_zip` | `ship_to_zip` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:30` |
| `ship_to_state` | `f.ship_to_state` | `ship_to_state` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:31` |
| `end_user_name` | `f.eu_company_name` | `eu_company_name` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:32` |
| `end_user_city` | `f.eu_city` | `eu_city` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:33` |
| `end_user_state` | `f.eu_state` | `eu_state` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:34` |
| `from_loc_no` | `f.from_loc_no` | `from_loc_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:35` |
| `part_no` | `p.part_no` | `part_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:36` |
| `mfg_partno` | `p.mfg_partno` | `mfg_partno` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:37` |
| `part_desc` | `f.part_desc` | `part_desc` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:38` |
| `synnex_po` | `f.synnex_po_no` | `synnex_po_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:39` |
| `vpl_code` | `f.vpl_code` | `vpl_code` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:40` |
| `track_no` | `e.track_no` | `track_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:41` |
| `mcust_no` | `f.master_cust_no` | `master_cust_no` | `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info_rt`, `dw_us.dwd_pub_common_history_header_extend`, `dim_us.dim_pub_order_type`, `table_final_data_us_18213`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `rds_scm_us_18213`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql:42` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `pos` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |
| `dim_us.dim_pub_part_info_rt` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |
| `dw_us.dwd_pub_common_history_header_extend` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |
| `dim_us.dim_pub_order_type` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |
| `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_pos/etl/pos_spa_scm_horizontal_rds_18213.sql` (source_kind: rds_report_sql).*
