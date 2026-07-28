# REPORT: RDS ap report SQL — ap dm dnd aging detail rds 1299 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_ap.ap_dm_dnd_aging_detail_rds_1299
- domain: RDS/vertica_ap
- one_line_purpose: RDS ap report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_ap/ap_dm_dnd_aging_detail_rds_1299.md
- ref_evidence: source/ref/RDS/vertica_ap/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `ap` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_ap` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 9 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_ap ap_dm_dnd_aging_detail_rds_1299" --intent find_table_schema` |

### Lineage
- **upstream:** `dm_ca.dm_ap_aging_header_df` — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **upstream:** `dim_ca.dim_disty_ap_dnd_profile` — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **upstream:** `dim_ca.dim_pub_vendor_profile` — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **upstream:** `dim_ca.dim_pub_manager` — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **upstream:** `dm_ca.dm_ap_aging_detail_df` — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **upstream:** `dim_ca.dim_pub_vendor_info` — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **downstream:** `rdsetl.rds_tmp_sheet_config` (report output) — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `ap` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_ap/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `ap` |
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

- **Source:** [source/contracts/rds/vertica_ap/metric-index.md](../../../../source/contracts/rds/vertica_ap/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |

### Key filters and ETL business logic
- `h.date_flag = current_date() - 1 and h.sum_level = 'VCD' and cast(h.terms_no AS varchar(10)) = 'DR' ; drop table if exists rds_ca1299_vcm_27; create local temporary table rds_ca129…`
- `d.date_flag = current_date() - 1 and ifnull(d.entry_id, 0) = 0 and ifnull(d.amt, 0) < 0 ; delete from rds_ca1299_detail_base where age < 61; drop table if exists rds_ca1299_usd_bas…`
- `u.doc_no is null or u.doc_no < 0`
- `d.date_flag = current_date() - 1 and ifnull(d.entry_id, 0) = 0 and ifnull(d.amt, 0) < 0 ; delete from rds_ca1299_audit_detail_base where age < 61; drop table if exists rds_ca1299_a…`
- `f.total_dm_60 <> 0`
- `f.total_dm_60 <> 0 ; drop table if exists rds_ca1299_sec3_pivot; create local temporary table rds_ca1299_sec3_pivot on commit preserve rows as select t4.analyst_name, t4.dm_amt, t4…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (6 objects).
2. Build staging temps (37 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dm_ca.dm_ap_aging_header_df"]
  P1["dim_ca.dim_disty_ap_dnd_profile"]
  P2["dim_ca.dim_pub_vendor_profile"]
  P3["dim_ca.dim_pub_manager"]
  P4["dm_ca.dm_ap_aging_detail_df"]
  P5["dim_ca.dim_pub_vendor_info"]
  T0["rds_ca1299_debit_all"]
  T1["rds_ca1299_vcm_27"]
  T2["rds_ca1299_dm_vend"]
  T3["rds_ca1299_dnd_vend"]
  T4["rds_ca1299_old_comp"]
  T5["rds_ca1299_final"]
  T6["rds_ca1299_detail_base"]
  T7["rds_ca1299_usd_base"]
  T8["rds_ca1299_usd_sum"]
  T9["rds_ca1299_usd_order_sum"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_2"]
  O2["rdsetl.rds_tmp_sheet_config"]
  O3["rdsetl.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dm_ca.dm_ap_aging_header_df` | Permanent warehouse source |
| `dim_ca.dim_disty_ap_dnd_profile` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_profile` | Permanent warehouse source |
| `dim_ca.dim_pub_manager` | Permanent warehouse source |
| `dm_ca.dm_ap_aging_detail_df` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_info` | Permanent warehouse source |
| `rds_ca1299_debit_all` | Report staging / temp table |
| `rds_ca1299_vcm_27` | Report staging / temp table |
| `rds_ca1299_dm_vend` | Report staging / temp table |
| `rds_ca1299_dnd_vend` | Report staging / temp table |
| `rds_ca1299_old_comp` | Report staging / temp table |
| `rds_ca1299_final` | Report staging / temp table |
| `rds_ca1299_detail_base` | Report staging / temp table |
| `rds_ca1299_usd_base` | Report staging / temp table |
| `rds_ca1299_usd_sum` | Report staging / temp table |
| `rds_ca1299_usd_order_sum` | Report staging / temp table |
| `rds_ca1299_detail_sum` | Report staging / temp table |
| `rds_ca1299_detail_sum_final` | Report staging / temp table |
| `rds_ca1299_audit_detail_base` | Report staging / temp table |
| `rds_ca1299_audit_usd_base` | Report staging / temp table |
| `rds_ca1299_audit_usd_sum` | Report staging / temp table |
| `rds_ca1299_audit_usd_order_sum` | Report staging / temp table |
| `rds_ca1299_detail_sum_audit` | Report staging / temp table |
| `rds_ca1299_final_totals` | Report staging / temp table |
| `rds_ca1299_sec1_vendors` | Report staging / temp table |
| `rds_ca1299_t1` | Report staging / temp table |
| `rds_ca1299_t4` | Report staging / temp table |
| `rds_ca1299_t5` | Report staging / temp table |
| `rds_ca1299_t6` | Report staging / temp table |
| `rds_ca1299_t7` | Report staging / temp table |
| `rds_ca1299_sec3_pivot` | Report staging / temp table |
| `rds_ca1299_recap` | Report staging / temp table |
| `rds_ca1299_audit_pick` | Report staging / temp table |
| `rds_ca1299_detail_audit_stats` | Report staging / temp table |
| `rds_ca1299_detail_audit_stats_it` | Report staging / temp table |
| `rds_ca1299_audit_pick_stats` | Report staging / temp table |
| `rds_ca1299_audit_pick_stats_it` | Report staging / temp table |
| `rds_ca1299_tab1` | Report staging / temp table |
| `rds_ca1299_tab2` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_2` | Report staging / temp table |
| `rdsetl.rds_tmp_sheet_config` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_2` | Final report output object |
| `rdsetl.rds_tmp_sheet_config` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dm_ca.dm_ap_aging_header_df`, `dim_ca.dim_disty_ap_dnd_profile`, `dim_ca.dim_pub_vendor_profile`, `dim_ca.dim_pub_manager`, `dm_ca.dm_ap_aging_detail_df`, `dim_ca.dim_pub_vendor_info`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_ca1299_debit_all`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_ca1299_vcm_27`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_ca1299_dm_vend`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_ca1299_dnd_vend`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rds_ca1299_old_comp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rds_ca1299_final`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rds_ca1299_detail_base`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rds_ca1299_usd_base`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `rds_ca1299_usd_sum`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rds_ca1299_usd_order_sum`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `rds_ca1299_detail_sum`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `rds_ca1299_detail_sum_final`
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

#### Step 16 -- finalize `rdsetl.rds_tmp_sheet_config`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 17 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `1` | `1` | — | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:3` |
| `data` | `'Report data'` | `Report`, `data` | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | literal | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:1018` |
| `null` | `null` | — | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:12` |
| `2` | `null; insert into rdsetl.rds_tmp_sheet_config select` | `insert`, `into`, `rds_tmp_sheet_config` | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | partial | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:1018` |
| `Audit` | `'Notes for Synnex Audit'` | `Notes`, `for`, `Synnex`, `Audit` | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | literal | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:1019` |
| `null` | `null` | — | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:12` |
| `flag` | `null; drop table if exists rdsetl.rds_tmp_body; create table rdsetl.rds_tmp_body as select 1` | `drop`, `table`, `exists`, `rds_tmp_body`, `create` | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | partial | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:1018` |
| `body_type` | `'standard'` | `standard` | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | literal | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:1025` |
| `cnt` | `count(*)` | — | `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | agg | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql:627` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `ap` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dm_ca.dm_ap_aging_header_df` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |
| `dim_ca.dim_disty_ap_dnd_profile` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |
| `dim_ca.dim_pub_vendor_profile` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |
| `dim_ca.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |
| `dm_ca.dm_ap_aging_detail_df` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |
| `dim_ca.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_ap/etl/ap_dm_dnd_aging_detail_rds_1299.sql` (source_kind: rds_report_sql).*
