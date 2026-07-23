# REPORT: RDS open_so_bo report SQL — open so bo rio allocation inventory rds 6302 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_open_so_bo.open_so_bo_rio_allocation_inventory_rds_6302
- domain: RDS/starrocks_open_so_bo
- one_line_purpose: RDS open_so_bo report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_rio_allocation_inventory_rds_6302.md
- ref_evidence: source/ref/RDS/starrocks_open_so_bo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `open_so_bo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_open_so_bo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 7 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_open_so_bo open_so_bo_rio_allocation_inventory_rds_6302" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_ca.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_dw_vend_pl_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_rio_req_detail_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_rio_req_consumed_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_list_box_detail_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_rio_request_header_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_manager_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **upstream:** `ods_ca.ods_cis_corp_bom_cost_var_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`
- **downstream:** `tempdb.temp_6302` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `open_so_bo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_open_so_bo/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/starrocks_open_so_bo/metric-index.md](../../../../source/contracts/rds/starrocks_open_so_bo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |

### Key filters and ETL business logic
- `a.order_type in(1,8) and a.ship_date is null and a.delete_date is null and b.delete_date is null and b.order_qty - ifnull(b.ship_qty,0) <> 0 ; drop table if exists tempdb.rds_inv_r…`
- `t.flag = 'P'`
- `rds_inv_rio1_6302.sku_no = t.sku_no ; update tempdb.rds_inv_rio1_6302 set unit_cost = unit_cost + ifnull(t.cost, 0) from tempdb.var_6302 t where rds_inv_rio1_6302.sku_no = t.sku_no…`
- `temp_6302.sku_no=b.sku_no and temp_6302.order_no = b.order_no and temp_6302.order_type = b.order_type and temp_6302.sku_no=b.sku_no ; drop table if exists tempdb.rds_tmp; create ta…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (19 objects).
2. Build staging temps (10 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_ca.ods_cis_corp_part_master_rt"]
  P1["ods_ca.ods_cis_corp_dw_vend_pl_rt"]
  P2["ods_ca.ods_cis_corp_order_header_rt"]
  P3["ods_ca.ods_cis_corp_order_detail_rt"]
  P4["ods_ca.ods_cis_corp_rio_req_detail_rt"]
  P5["ods_ca.ods_cis_corp_rio_req_consumed_rt"]
  P6["ods_ca.ods_cis_corp_list_box_detail_rt"]
  P7["ods_ca.ods_cis_corp_rio_request_header_rt"]
  T0["tempdb.rds_sku_6302"]
  T1["tempdb.temp_6302"]
  T2["tempdb.rds_inv_rio_6302"]
  T3["tempdb.rds_inv_rio1_6302"]
  T4["tempdb.sku_6302"]
  T5["tempdb.var_6302"]
  T6["tempdb.base_6302"]
  T7["tempdb.eta_ca6302"]
  T8["tempdb.rds_tmp"]
  T9["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  O2["tempdb.temp_6302"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_ca.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_dw_vend_pl_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_rio_req_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_rio_req_consumed_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_list_box_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_rio_request_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_manager_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_bom_cost_var_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_exp_codes_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_bom_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_mc_order_ref_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_customer_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_soldto_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_soldto_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_territory_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_location_info_rt` | Permanent warehouse source |
| `dm_ca.dm_pur_unieta_boso_detail_rt` | Permanent warehouse source |
| `tempdb.rds_sku_6302` | Report staging / temp table |
| `tempdb.temp_6302` | Report staging / temp table |
| `tempdb.rds_inv_rio_6302` | Report staging / temp table |
| `tempdb.rds_inv_rio1_6302` | Report staging / temp table |
| `tempdb.sku_6302` | Report staging / temp table |
| `tempdb.var_6302` | Report staging / temp table |
| `tempdb.base_6302` | Report staging / temp table |
| `tempdb.eta_ca6302` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |
| `tempdb.temp_6302` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `ods_ca.ods_cis_corp_bom_cost_var_rt`, `ods_ca.ods_cis_corp_exp_codes_rt`, `ods_ca.ods_cis_corp_bom_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.rds_sku_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.temp_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.rds_inv_rio_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.rds_inv_rio1_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.sku_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.var_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `tempdb.base_6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `tempdb.eta_ca6302`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `tempdb.rds_tmp`
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

#### Step 14 -- finalize `tempdb.temp_6302`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `sku_no` | `a.sku_no` | `sku_no` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:5` |
| `short_desc` | `a.short_desc` | `short_desc` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:6` |
| `vpl_code` | `b.vpl_code` | `vpl_code` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:7` |
| `part_no` | `a.part_no` | `part_no` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:8` |
| `mfg_partno` | `a.mfg_partno` | `mfg_partno` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:9` |
| `abc_code` | `a.abc_code` | `abc_code` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:10` |
| `po_cost` | `a.po_cost` | `po_cost` | `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_dw_vend_pl_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `tempdb.rds_sku_6302`, `ods_ca.ods_cis_corp_rio_req_detail_rt`, `ods_ca.ods_cis_corp_rio_req_consumed_rt`, `ods_ca.ods_cis_corp_list_box_detail_rt`, `ods_ca.ods_cis_corp_rio_request_header_rt`, `ods_ca.ods_cis_corp_manager_rt`, `tempdb.rds_inv_rio_6302`, `tempdb.rds_inv_rio1_6302` | passthrough | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:11` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` | no |

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
-- See full script: source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_ca.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_dw_vend_pl_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_rio_req_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_rio_req_consumed_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_list_box_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_rio_request_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_manager_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_bom_cost_var_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_exp_codes_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_bom_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_mc_order_ref_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_customer_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |
| `ods_ca.ods_cis_corp_order_soldto_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` (source_kind: rds_report_sql).*
