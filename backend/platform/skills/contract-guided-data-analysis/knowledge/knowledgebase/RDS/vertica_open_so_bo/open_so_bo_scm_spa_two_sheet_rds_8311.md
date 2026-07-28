# REPORT: RDS open_so_bo report SQL — open so bo scm spa two sheet rds 8311 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_open_so_bo.open_so_bo_scm_spa_two_sheet_rds_8311
- domain: RDS/vertica_open_so_bo
- one_line_purpose: RDS open_so_bo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_scm_spa_two_sheet_rds_8311.md
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
| **column_count** | 3 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_open_so_bo open_so_bo_scm_spa_two_sheet_rds_8311" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_ca.dwd_disty_sales_open_order_detail` — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`
- **upstream:** `dim_ca.dim_pub_location_info` — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`
- **upstream:** `dw_ca.dwd_disty_scm_open_order_spa_df` — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`
- **downstream:** `rdsetl.rds_tmp_sheet_config` (report output) — `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` |

### Key filters and ETL business logic
- `a.vend_no = 40279 and a.order_delete_date is null and a.order_line_delete_date is null ; drop table if exists rdsetl.rds_tmp; create table rdsetl.rds_tmp as select * from rds_us713…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (3 objects).
2. Build staging temps (5 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_ca.dwd_disty_sales_open_order_detail"]
  P1["dim_ca.dim_pub_location_info"]
  P2["dw_ca.dwd_disty_scm_open_order_spa_df"]
  T0["rds_us7130_order"]
  T1["rdsetl.rds_tmp"]
  T2["rdsetl.rds_tmp_2"]
  T3["rdsetl.rds_tmp_body"]
  T4["rdsetl.rds_tmp_sheet_config"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_2"]
  O2["rdsetl.rds_tmp_body"]
  O3["rdsetl.rds_tmp_sheet_config"]
  P0 --> T0
  T4 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_ca.dwd_disty_sales_open_order_detail` | Permanent warehouse source |
| `dim_ca.dim_pub_location_info` | Permanent warehouse source |
| `dw_ca.dwd_disty_scm_open_order_spa_df` | Permanent warehouse source |
| `rds_us7130_order` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_2` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp_sheet_config` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_2` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |
| `rdsetl.rds_tmp_sheet_config` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_ca.dwd_disty_sales_open_order_detail`, `dim_ca.dim_pub_location_info`, `dw_ca.dwd_disty_scm_open_order_spa_df`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_us7130_order`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rdsetl.rds_tmp_2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rdsetl.rds_tmp_sheet_config`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 8 -- finalize `rdsetl.rds_tmp_2`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 9 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 10 -- finalize `rdsetl.rds_tmp_sheet_config`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `flag` | `2` | — | `rdsetl.rds_tmp_2` | rename | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql:35` |
| `body_type` | `'Standard'` | `Standard` | `rdsetl.rds_tmp_2` | literal | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql:57` |
| `cnt` | `count(*)` | — | `rdsetl.rds_tmp_2` | agg | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql:58` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` | no |

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
-- See full script: source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_ca.dwd_disty_sales_open_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` |
| `dim_ca.dim_pub_location_info` | FROM/JOIN source | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` |
| `dw_ca.dwd_disty_scm_open_order_spa_df` | FROM/JOIN source | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_scm_spa_two_sheet_rds_8311.sql` (source_kind: rds_report_sql).*
