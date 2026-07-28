# REPORT: RDS inventory report SQL — inv rio cws location rds 6800 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_inventory.inv_rio_cws_location_rds_6800
- domain: RDS/vertica_inventory
- one_line_purpose: RDS inventory report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_inventory/inv_rio_cws_location_rds_6800.md
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
| **column_count** | 3 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_inventory inv_rio_cws_location_rds_6800" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_ca.dwd_disty_inv_qty_df` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `ods_ca.ods_cis_corp_inv_qty` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `dim_ca.dim_pub_part_info` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `dim_ca.dim_pub_vendor_info` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `ods_ca.ods_cis_corp_sku_cost` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `dw_ca.dws_disty_pur_ips_runrate_1w` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `dim_ca.dim_pub_location_info` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `dim_ca.dim_pub_vendor_xref` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `ods_ca.ods_cis_corp_v_vend_currency` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **upstream:** `ods_ca.ods_cis_corp_pdss_prod_profile` — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |

### Key filters and ETL business logic
- `date_flag = CURRENT_DATE()-1`
- `b.date_flag =CURRENT_DATE()-1 ; DROP TABLE IF EXISTS inv_qty_temp; CREATE LOCAL TEMPORARY TABLE inv_qty_temp ON COMMIT PRESERVE ROWS AS SELECT CURRENT_DATE()-1 AS date_flag ,diq.lo…`
- `1 = 2 AND (pm.vend_no IN (1301,17832,22354,29357,29447,29716,31106,31503,32328,33410,33411,35876,35916,35988,36665,39177,39321,40090) OR pvi.pur_vend_no IN (1301,17832,22354,29357,…`
- `on_hand_qty > 0`
- `a1.on_hand_qty > 0 ) a WHERE iq.sku_no = a.sku_no AND iq.sku_no IN ( SELECT sku_no FROM ( SELECT sku_no ,count(DISTINCT ave_cost) icount FROM inv_qty_temp`
- `iq.sku_no = sc.sku_no AND iq.sku_no IN ( SELECT sku_no FROM ( SELECT sku_no ,count(DISTINCT ave_cost) icount FROM inv_qty_temp`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (17 objects).
2. Build staging temps (8 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_ca.dwd_disty_inv_qty_df"]
  P1["ods_ca.ods_cis_corp_inv_qty"]
  P2["dim_ca.dim_pub_part_info"]
  P3["dim_ca.dim_pub_vendor_info"]
  P4["ods_ca.ods_cis_corp_sku_cost"]
  P5["dw_ca.dws_disty_pur_ips_runrate_1w"]
  P6["dim_ca.dim_pub_location_info"]
  P7["dim_ca.dim_pub_vendor_xref"]
  T0["sku_inv_loc"]
  T1["inv_qty_temp"]
  T2["max_week"]
  T3["only_runrate_skus"]
  T4["aging_data"]
  T5["rds_6800_final"]
  T6["rdsetl.rds_tmp"]
  T7["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T7 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_ca.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_inv_qty` | Permanent warehouse source |
| `dim_ca.dim_pub_part_info` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_info` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_sku_cost` | Permanent warehouse source |
| `dw_ca.dws_disty_pur_ips_runrate_1w` | Permanent warehouse source |
| `dim_ca.dim_pub_location_info` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_xref` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_v_vend_currency` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_pdss_prod_profile` | Permanent warehouse source |
| `dw_ca.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_prod_code_detail` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_part_prod_detail` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_detail` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_header` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_cws_cop_ship_progress` | Permanent warehouse source |
| `dim_ca.dim_pub_customer_info` | Permanent warehouse source |
| `sku_inv_loc` | Report staging / temp table |
| `inv_qty_temp` | Report staging / temp table |
| `max_week` | Report staging / temp table |
| `only_runrate_skus` | Report staging / temp table |
| `aging_data` | Report staging / temp table |
| `rds_6800_final` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_ca.dwd_disty_inv_qty_df`, `ods_ca.ods_cis_corp_inv_qty`, `dim_ca.dim_pub_part_info`, `dim_ca.dim_pub_vendor_info`, `ods_ca.ods_cis_corp_sku_cost`, `dw_ca.dws_disty_pur_ips_runrate_1w`, `dim_ca.dim_pub_location_info`, `dim_ca.dim_pub_vendor_xref`, `ods_ca.ods_cis_corp_v_vend_currency`, `ods_ca.ods_cis_corp_pdss_prod_profile`, `dw_ca.dwd_disty_inv_aging_df`, `ods_ca.ods_cis_corp_prod_code_detail`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `sku_inv_loc`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `inv_qty_temp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `max_week`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `only_runrate_skus`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `aging_data`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rds_6800_final`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 11 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `flag` | `1` | — | `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql:7` |
| `body_type` | `'Standard'` | `Standard` | `rdsetl.rds_tmp` | literal | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql:1065` |
| `cnt` | `count(*)` | — | `rdsetl.rds_tmp` | agg | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql:1066` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` | no |

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
-- See full script: source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_ca.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_inv_qty` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `dim_ca.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `dim_ca.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_sku_cost` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `dw_ca.dws_disty_pur_ips_runrate_1w` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `dim_ca.dim_pub_location_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `dim_ca.dim_pub_vendor_xref` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_v_vend_currency` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_pdss_prod_profile` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `dw_ca.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_prod_code_detail` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_part_prod_detail` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |
| `ods_ca.ods_cis_corp_order_header` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` (source_kind: rds_report_sql).*
