# REPORT: RDS inventory report SQL — inv aging qty vendor filter rds 17484 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_inventory.inv_aging_qty_vendor_filter_rds_17484
- domain: RDS/vertica_inventory
- one_line_purpose: RDS inventory report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_vendor_filter_rds_17484.md
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
| **column_count** | 44 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_inventory inv_aging_qty_vendor_filter_rds_17484" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql`
- **upstream:** `dim_us.dim_pub_vendor_info_rt` — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql`
- **upstream:** `dw_us.dwd_disty_inv_qty_df` — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |

### Key filters and ETL business logic
- `a.vend_no in (13529, 74688, 70654, 75429, 61682, 55907) and a.data_source = 'CIS' ; drop table if exists table_us_aging_17484; create local temporary table table_us_aging_17484 on …`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (4 objects).
2. Build staging temps (5 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_part_info"]
  P1["dim_us.dim_pub_vendor_info_rt"]
  P2["dw_us.dwd_disty_inv_aging_df"]
  P3["dw_us.dwd_disty_inv_qty_df"]
  T0["table_us_sku_17484"]
  T1["table_us_aging_17484"]
  T2["table_us_inv_17484"]
  T3["rdsetl.rds_tmp"]
  T4["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T4 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dim_us.dim_pub_vendor_info_rt` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_qty_df` | Permanent warehouse source |
| `table_us_sku_17484` | Report staging / temp table |
| `table_us_aging_17484` | Report staging / temp table |
| `table_us_inv_17484` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_us.dim_pub_part_info`, `dim_us.dim_pub_vendor_info_rt`, `dw_us.dwd_disty_inv_aging_df`, `dw_us.dwd_disty_inv_qty_df`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_us_sku_17484`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `table_us_aging_17484`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `table_us_inv_17484`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 8 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `id` | `a.vend_no` | `vend_no` | `table_us_inv_17484`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:4` |
| `name` | `a.vend_name` | `vend_name` | `table_us_inv_17484`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:5` |
| `vend_no` | `a.vend_no` | `vend_no` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:4` |
| `vend_name` | `a.vend_name` | `vend_name` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:5` |
| `vpl_code` | `a.vpl_code` | `vpl_code` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:7` |
| `mfg_partno` | `a.mfg_partno` | `mfg_partno` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:9` |
| `base_cost` | `a.base_cost` | `base_cost` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:71` |
| `qty_0_30` | `a.qty_0_30` | `qty_0_30` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:164` |
| `qty_31_60` | `a.qty_31_60` | `qty_31_60` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:165` |
| `qty_61_90` | `a.qty_61_90` | `qty_61_90` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:166` |
| `qty_90_plus` | `a.qty_90_plus` | `qty_90_plus` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:167` |
| `qty_91_120` | `a.qty_91_120` | `qty_91_120` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:168` |
| `qty_121_150` | `a.qty_121_150` | `qty_121_150` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:169` |
| `qty_151_180` | `a.qty_151_180` | `qty_151_180` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:170` |
| `qty_181_210` | `a.qty_181_210` | `qty_181_210` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:171` |
| `qty_211_240` | `a.qty_211_240` | `qty_211_240` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:172` |
| `qty_240_plus` | `a.qty_240_plus` | `qty_240_plus` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:173` |
| `qty_241_270` | `a.qty_241_270` | `qty_241_270` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:174` |
| `qty_271_300` | `a.qty_271_300` | `qty_271_300` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:175` |
| `qty_301_330` | `a.qty_301_330` | `qty_301_330` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:176` |
| `qty_331_360` | `a.qty_331_360` | `qty_331_360` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:177` |
| `qty_360_plus` | `a.qty_360_plus` | `qty_360_plus` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:178` |
| `age_0_30` | `a.age_0_30` | `age_0_30` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:179` |
| `age_31_60` | `a.age_31_60` | `age_31_60` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:180` |
| `age_61_90` | `a.age_61_90` | `age_61_90` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:181` |
| `age_90_plus` | `a.age_90_plus` | `age_90_plus` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:182` |
| `age_91_120` | `a.age_91_120` | `age_91_120` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:183` |
| `age_121_150` | `a.age_121_150` | `age_121_150` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:184` |
| `age_151_180` | `a.age_151_180` | `age_151_180` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:185` |
| `age_181_210` | `a.age_181_210` | `age_181_210` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:186` |
| `age_211_240` | `a.age_211_240` | `age_211_240` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:187` |
| `age_240_plus` | `a.age_240_plus` | `age_240_plus` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:188` |
| `age_241_270` | `a.age_241_270` | `age_241_270` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:189` |
| `age_271_300` | `a.age_271_300` | `age_271_300` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:190` |
| `age_301_330` | `a.age_301_330` | `age_301_330` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:191` |
| `age_331_360` | `a.age_331_360` | `age_331_360` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:192` |
| `age_360_plus` | `a.age_360_plus` | `age_360_plus` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:193` |
| `oh` | `a.oh` | `oh` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:194` |
| `oo` | `a.oo` | `oo` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:195` |
| `bo` | `a.bo` | `bo` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:196` |
| `alloc` | `a.alloc` | `alloc` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:197` |
| `avail` | `a.avail` | `avail` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:198` |
| `total` | `a.total` | `total` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:199` |
| `ext_amt` | `a.ext_amt` | `ext_amt` | `table_us_inv_17484`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:200` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` | no |

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
-- See full script: source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |
| `dim_us.dim_pub_vendor_info_rt` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |
| `dw_us.dwd_disty_inv_qty_df` | FROM/JOIN source | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` (source_kind: rds_report_sql).*
