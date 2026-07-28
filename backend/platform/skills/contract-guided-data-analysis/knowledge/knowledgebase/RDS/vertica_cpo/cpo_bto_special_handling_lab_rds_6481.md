# REPORT: Open order */ (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_cpo.cpo_bto_special_handling_lab_rds_6481
- domain: RDS/vertica_cpo
- one_line_purpose: RDS cpo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_cpo/cpo_bto_special_handling_lab_rds_6481.md
- ref_evidence: source/ref/RDS/vertica_cpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `cpo` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_cpo` |
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
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_cpo cpo_bto_special_handling_lab_rds_6481" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_ca.ods_cis_corp_order_header` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_detail` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_soldto` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_profile` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `dim_ca.dim_pub_location_info` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_wms_mywms_cws_bto_lab` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `dm_ca.dm_disty_sales_open_cpo` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_cis_corp_history_header` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_cis_corp_history_detail` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **upstream:** `ods_ca.ods_cis_corp_history_soldto` — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`
- **downstream:** `rdsetl.rds_tmp_sheet_config` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `cpo` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_cpo/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `cpo` |
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

- **Source:** [source/contracts/rds/vertica_cpo/metric-index.md](../../../../source/contracts/rds/vertica_cpo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |

### Key filters and ETL business logic
- `a.to_acct_no = 1055050 and a.order_type in(1,8) and a.ship_date is null and a.delete_date is null and b.delete_date is null and b.order_qty - ifnull(b.ship_qty,0) <> 0 ; drop table…`
- `a.to_acct_no = 1055050 and a.order_type = 1 and a.ship_date >= current_date()-1 and a.ship_date < current_date() ; drop table if exists rds_6481_rtv_13; create LOCAL TEMPORARY TABL…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (12 objects).
2. Build staging temps (24 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_ca.ods_cis_corp_order_header"]
  P1["ods_ca.ods_cis_corp_order_detail"]
  P2["ods_ca.ods_cis_corp_order_soldto"]
  P3["ods_ca.ods_cis_corp_order_profile"]
  P4["dim_ca.dim_pub_location_info"]
  P5["ods_ca.ods_wms_mywms_cws_bto_lab"]
  P6["dm_ca.dm_disty_sales_open_cpo"]
  P7["ods_ca.ods_cis_corp_history_header"]
  T0["rds_6481_rtv"]
  T1["rds_6481_rtv_2"]
  T2["special_handle_6481"]
  T3["rds_6481_rtv_3"]
  T4["rds_6481_rtv_4"]
  T5["rds_6481_rtv_5"]
  T6["rds_6481_rtv_6"]
  T7["rds_6481_rtv_7"]
  T8["rds_6481_rtv_8"]
  T9["rds_6481_rtv_9"]
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
| `ods_ca.ods_cis_corp_order_header` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_detail` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_soldto` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_profile` | Permanent warehouse source |
| `dim_ca.dim_pub_location_info` | Permanent warehouse source |
| `ods_ca.ods_wms_mywms_cws_bto_lab` | Permanent warehouse source |
| `dm_ca.dm_disty_sales_open_cpo` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_header` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_detail` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_soldto` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_carton_header` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_asset_tag` | Permanent warehouse source |
| `rds_6481_rtv` | Report staging / temp table |
| `rds_6481_rtv_2` | Report staging / temp table |
| `special_handle_6481` | Report staging / temp table |
| `rds_6481_rtv_3` | Report staging / temp table |
| `rds_6481_rtv_4` | Report staging / temp table |
| `rds_6481_rtv_5` | Report staging / temp table |
| `rds_6481_rtv_6` | Report staging / temp table |
| `rds_6481_rtv_7` | Report staging / temp table |
| `rds_6481_rtv_8` | Report staging / temp table |
| `rds_6481_rtv_9` | Report staging / temp table |
| `rds_6481_rtv_final_1` | Report staging / temp table |
| `rds_6481_rtv_12` | Report staging / temp table |
| `rds_6481_rtv_13` | Report staging / temp table |
| `special_handle_6481_2` | Report staging / temp table |
| `rds_6481_rtv_14` | Report staging / temp table |
| `rds_6481_rtv_15` | Report staging / temp table |
| `rds_6481_rtv_16` | Report staging / temp table |
| `rds_6481_track_distinct` | Report staging / temp table |
| `rds_6481_track_no` | Report staging / temp table |
| `rds_6481_rtv_final_2` | Report staging / temp table |
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
**Source:** `ods_ca.ods_cis_corp_order_header`, `ods_ca.ods_cis_corp_order_detail`, `ods_ca.ods_cis_corp_order_soldto`, `ods_ca.ods_cis_corp_order_profile`, `dim_ca.dim_pub_location_info`, `ods_ca.ods_wms_mywms_cws_bto_lab`, `dm_ca.dm_disty_sales_open_cpo`, `ods_ca.ods_cis_corp_history_header`, `ods_ca.ods_cis_corp_history_detail`, `ods_ca.ods_cis_corp_history_soldto`, `ods_ca.ods_cis_corp_carton_header`, `ods_ca.ods_cis_corp_asset_tag`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_6481_rtv`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_6481_rtv_2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `special_handle_6481`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_6481_rtv_3`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rds_6481_rtv_4`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rds_6481_rtv_5`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rds_6481_rtv_6`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rds_6481_rtv_7`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `rds_6481_rtv_8`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rds_6481_rtv_9`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `rds_6481_rtv_final_1`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `rds_6481_rtv_12`
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
| `flag` | `2` | — | `rdsetl.rds_tmp_2` | rename | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql:2` |
| `body_type` | `'Standard'` | `Standard` | `rdsetl.rds_tmp_2` | literal | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql:403` |
| `cnt` | `count(*)` | — | `rdsetl.rds_tmp_2` | agg | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql:404` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `cpo` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_ca.ods_cis_corp_order_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_order_soldto` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_order_profile` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `dim_ca.dim_pub_location_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_wms_mywms_cws_bto_lab` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `dm_ca.dm_disty_sales_open_cpo` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_history_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_history_detail` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_history_soldto` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_carton_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |
| `ods_ca.ods_cis_corp_asset_tag` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_cpo/etl/cpo_bto_special_handling_lab_rds_6481.sql` (source_kind: rds_report_sql).*
