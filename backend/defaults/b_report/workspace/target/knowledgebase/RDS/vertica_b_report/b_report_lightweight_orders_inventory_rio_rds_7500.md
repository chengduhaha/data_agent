# REPORT: Drop temporary tables if they exist (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_b_report.b_report_lightweight_orders_inventory_rio_rds_7500
- domain: RDS/vertica_b_report
- one_line_purpose: RDS b_report report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_b_report/b_report_lightweight_orders_inventory_rio_rds_7500.md
- ref_evidence: source/ref/RDS/vertica_b_report/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `b_report` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_b_report` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 2 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_b_report b_report_lightweight_orders_inventory_rio_rds_7500" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_customer_info` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dim_us.dim_pub_cust_xref_all` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dw_us.dwd_disty_pub_dw_orders_extend_di` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dw_us.dwd_pub_common_history_header_extend` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dw_us.dwd_disty_sales_open_order_detail` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dim_us.dim_pub_vpl_info` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dw_us.dwd_disty_inv_qty_df` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **upstream:** `dw_us.dws_disty_pur_ips_runrate_1w` — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`
- **downstream:** `rdsetl.rds_tmp_sheet_config` (report output) — `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `b_report` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_b_report/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `b_report` |
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

- **Source:** [source/contracts/rds/vertica_b_report/metric-index.md](../../../../source/contracts/rds/vertica_b_report/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |

### Key filters and ETL business logic
- `cust_no IN (124858, 613402); UPDATE t_cust_7500 SET mcust_no = COALESCE(b.xref_no, t_cust_7500.cust_no) FROM dim_us.dim_pub_cust_xref_all b WHERE t_cust_7500.cust_no = b.cust_no AN…`
- `date_flag >= current_date() - 70 AND date_flag < current_date(); UPDATE rds_ord_7500 SET from_loc_no = b.from_loc_no FROM dw_us.dwd_pub_common_history_header_extend b WHERE rds_ord…`
- `a.date_flag = current_date() - 1 AND a.view_level = 'IT_PART' AND a.inv_type = 1; UPDATE tmp_inv_us7500 SET aging_90_plus = b.aging_90_plus FROM inv_aging b WHERE tmp_inv_us7500.sk…`
- `tmp_inv_us7500.sku_no = b.sku_no; UPDATE tmp_inv_us7500 SET vend_no = b.vend_no, vpl_no = b.vpl_no, short_desc = b.short_desc, part_no = b.part_no, abc_code = b.abc_code, source_st…`
- `tmp_inv_us7500.sku_no = b.sku_no; CREATE LOCAL TEMP TABLE t_rr_7500_max_week ON COMMIT PRESERVE ROWS AS SELECT max(week) as max_week FROM dw_us.dws_disty_pur_ips_runrate_1w WHERE s…`
- `tmp_inv_us7500.sku_no = b.sku_no; UPDATE tmp_inv_us7500 SET spike_check = (b.rr4 * 1.00 / 4) / (b.rr10 * 1.00 / 10) FROM t_rr_7500 b WHERE tmp_inv_us7500.sku_no = b.sku_no AND b.rr…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (18 objects).
2. Build staging temps (17 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_customer_info"]
  P1["dim_us.dim_pub_cust_xref_all"]
  P2["dw_us.dwd_disty_pub_dw_orders_extend_di"]
  P3["dw_us.dwd_pub_common_history_header_extend"]
  P4["dw_us.dwd_disty_inv_aging_df"]
  P5["dw_us.dwd_disty_sales_open_order_detail"]
  P6["dim_us.dim_pub_part_info"]
  P7["dim_us.dim_pub_vpl_info"]
  T0["t_cust_7500"]
  T1["t_all_cust_7500"]
  T2["rds_ord_7500"]
  T3["tmp_inv_us7500"]
  T4["sku"]
  T5["inv_aging"]
  T6["Dell_BO_QTY_7500"]
  T7["inv_7500"]
  T8["t_rr_7500_max_week"]
  T9["t_rr_7500"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_2"]
  O2["rdsetl.rds_tmp_body"]
  O3["rdsetl.rds_tmp_sheet_config"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_customer_info` | Permanent warehouse source |
| `dim_us.dim_pub_cust_xref_all` | Permanent warehouse source |
| `dw_us.dwd_disty_pub_dw_orders_extend_di` | Permanent warehouse source |
| `dw_us.dwd_pub_common_history_header_extend` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `dw_us.dwd_disty_sales_open_order_detail` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_info` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `dw_us.dws_disty_pur_ips_runrate_1w` | Permanent warehouse source |
| `dim_us.dim_disty_pur_vendor_dna_matrix` | Permanent warehouse source |
| `dim_us.dim_pub_manager` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_rio_req_header` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_rio_req_detail` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_info` | Permanent warehouse source |
| `dim_us.dim_pub_sku_profile_rt` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_rio_req_consumed` | Permanent warehouse source |
| `dim_us.dim_pub_list_box_detail` | Permanent warehouse source |
| `t_cust_7500` | Report staging / temp table |
| `t_all_cust_7500` | Report staging / temp table |
| `rds_ord_7500` | Report staging / temp table |
| `tmp_inv_us7500` | Report staging / temp table |
| `sku` | Report staging / temp table |
| `inv_aging` | Report staging / temp table |
| `Dell_BO_QTY_7500` | Report staging / temp table |
| `inv_7500` | Report staging / temp table |
| `t_rr_7500_max_week` | Report staging / temp table |
| `t_rr_7500` | Report staging / temp table |
| `rio_7500` | Report staging / temp table |
| `rds_rio_on_order` | Report staging / temp table |
| `loc_qty` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_2` | Report staging / temp table |
| `rdsetl.rds_tmp_sheet_config` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_2` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |
| `rdsetl.rds_tmp_sheet_config` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_us.dim_pub_customer_info`, `dim_us.dim_pub_cust_xref_all`, `dw_us.dwd_disty_pub_dw_orders_extend_di`, `dw_us.dwd_pub_common_history_header_extend`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dwd_disty_sales_open_order_detail`, `dim_us.dim_pub_part_info`, `dim_us.dim_pub_vpl_info`, `dw_us.dwd_disty_inv_qty_df`, `dw_us.dws_disty_pur_ips_runrate_1w`, `dim_us.dim_disty_pur_vendor_dna_matrix`, `dim_us.dim_pub_manager`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `t_cust_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `t_all_cust_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_ord_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tmp_inv_us7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `sku`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `inv_aging`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `Dell_BO_QTY_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `inv_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `t_rr_7500_max_week`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `t_rr_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `rio_7500`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `rds_rio_on_order`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 14 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `rdsetl.rds_tmp_2`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 16 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 17 -- finalize `rdsetl.rds_tmp_sheet_config`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `sku_no` | `inv.sku_no` | `sku_no` | `dw_us.dwd_disty_inv_rio_req_header`, `rds_rio_on_order`, `loc_qty`, `dw_us.dwd_disty_inv_rio_req_detail`, `dw_us.dwd_disty_inv_rio_req_consumed`, `dim_us.dim_pub_list_box_detail`, `tmp_inv_us7500`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql:322` |
| `req_qty` | `SUM(rh.req_qty)` | `req_qty` | `dw_us.dwd_disty_inv_rio_req_header`, `rds_rio_on_order`, `loc_qty`, `dw_us.dwd_disty_inv_rio_req_detail`, `dw_us.dwd_disty_inv_rio_req_consumed`, `dim_us.dim_pub_list_box_detail`, `tmp_inv_us7500`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | agg | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql:322` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `b_report` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dim_us.dim_pub_cust_xref_all` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_disty_pub_dw_orders_extend_di` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_pub_common_history_header_extend` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_disty_sales_open_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dim_us.dim_pub_vpl_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dws_disty_pur_ips_runrate_1w` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dim_us.dim_disty_pur_vendor_dna_matrix` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_disty_inv_rio_req_header` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dw_us.dwd_disty_inv_rio_req_detail` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |
| `dim_us.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` (source_kind: rds_report_sql).*
