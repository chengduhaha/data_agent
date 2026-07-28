# REPORT: RDS cpo report SQL — cpo order status eta hideampl expense rds 19257 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_cpo.cpo_order_status_eta_hideampl_expense_rds_19257
- domain: RDS/starrocks_cpo
- one_line_purpose: RDS cpo report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_cpo/cpo_order_status_eta_hideampl_expense_rds_19257.md
- ref_evidence: source/ref/RDS/starrocks_cpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `cpo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_cpo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 3 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_cpo cpo_order_status_eta_hideampl_expense_rds_19257" --intent find_table_schema` |

### Lineage
- **upstream:** `dm_us.dm_pur_unieta_boso_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_history_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_order_type_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_order_exp_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_order_profile_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_history_exp_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **upstream:** `ods_us.ods_cis_corp_history_profile_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`
- **downstream:** `tempdb.us_report_19257` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `cpo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_cpo/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/starrocks_cpo/metric-index.md](../../../../source/contracts/rds/starrocks_cpo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |

### Key filters and ETL business logic
- `order_no = 172910055`
- `a.order_type in (1,8) and a.to_acct_no = 686022 and a.entry_datetime >= '2025-01-01' and a.entry_datetime < current_date() -- and a.order_no = 172910055`
- `a.order_type in (1,8) and a.to_acct_no = 686022 and a.entry_datetime >= '2025-01-01' and a.entry_datetime < current_date() -- and a.order_no = 172910055 ; -- select * from tempdb.u…`
- `op.order_type = b.order_type and op.order_no = b.order_no and op.profile_type = 'HIDEAMPL' and op.profile_cat = 'AMPL' and op.profile_c = 'Y' ) and b.delete_id is null`
- `tempdb.us_report_19257.order_no = b.order_no and tempdb.us_report_19257.order_line_no = b.order_line_no and tempdb.us_report_19257.order_type = b.order_type ), 0) ; update tempdb.u…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (15 objects).
2. Build staging temps (5 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["dm_us.dm_pur_unieta_boso_detail_rt"]
  P1["ods_us.ods_cis_corp_history_header_rt"]
  P2["ods_us.ods_cis_corp_history_detail_rt"]
  P3["ods_us.ods_cis_corp_order_type_rt"]
  P4["ods_us.ods_cis_corp_order_header_rt"]
  P5["ods_us.ods_cis_corp_order_detail_rt"]
  P6["ods_us.ods_cis_corp_order_exp_rt"]
  P7["ods_us.ods_cis_corp_order_profile_rt"]
  T0["tempdb.us_report_19257"]
  T1["us_exp_temp_9185"]
  T2["us_exp_9185"]
  T3["rds_tmp"]
  T4["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  O2["tempdb.us_report_19257"]
  P0 --> T0
  T4 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_pur_unieta_boso_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_type_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_exp_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_profile_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_exp_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_profile_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_soldto_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_soldto_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `tempdb.us_report_19257` | Report staging / temp table |
| `us_exp_temp_9185` | Report staging / temp table |
| `us_exp_9185` | Report staging / temp table |
| `rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |
| `tempdb.us_report_19257` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dm_us.dm_pur_unieta_boso_detail_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_detail_rt`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_order_exp_rt`, `ods_us.ods_cis_corp_order_profile_rt`, `ods_us.ods_cis_corp_history_exp_rt`, `ods_us.ods_cis_corp_history_profile_rt`, `ods_us.ods_cis_corp_order_soldto_rt`, `ods_us.ods_cis_corp_history_soldto_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.us_report_19257`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `us_exp_temp_9185`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `us_exp_9185`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 8 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 9 -- finalize `tempdb.us_report_19257`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `flag` | `1` | — | `tempdb.rds_tmp` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql:4` |
| `body_type` | `'Standard'` | `Standard` | `tempdb.rds_tmp` | literal | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql:402` |
| `cnt` | `count(*)` | — | `tempdb.rds_tmp` | agg | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql:403` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` | no |

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
-- See full script: source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dm_us.dm_pur_unieta_boso_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_history_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_order_type_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_order_exp_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_order_profile_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_history_exp_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_history_profile_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_order_soldto_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_history_soldto_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_cpo_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_history_cpo_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |
| `ods_us.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` (source_kind: rds_report_sql).*
