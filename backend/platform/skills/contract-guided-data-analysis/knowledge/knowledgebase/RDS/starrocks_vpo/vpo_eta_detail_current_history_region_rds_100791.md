# REPORT: RDS vpo report SQL — vpo eta detail current history region rds 100791 (`tempdb.rds_tmp_body`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_vpo.vpo_eta_detail_current_history_region_rds_100791
- domain: RDS/starrocks_vpo
- one_line_purpose: RDS vpo report SQL on StarRocks producing `tempdb.rds_tmp_body`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_vpo/vpo_eta_detail_current_history_region_rds_100791.md
- ref_evidence: source/ref/RDS/starrocks_vpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp_body`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `vpo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp_body` | Evidence SQL pack `starrocks_vpo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp_body` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 15 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_vpo vpo_eta_detail_current_history_region_rds_100791" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_hyuk.ods_cis_corp_order_eta_detail` — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **upstream:** `ods_hyuk.ods_cis_corp_order_detail` — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **upstream:** `ods_hyuk.ods_cis_corp_part_master` — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **upstream:** `ods_hyuk.ods_cis_corp_manager` — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **upstream:** `ods_hyuk.ods_cis_corp_history_eta_detail` — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **upstream:** `ods_hyuk.ods_cis_corp_history_detail` — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `vpo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_vpo/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `vpo` |
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

- **Source:** [source/contracts/rds/starrocks_vpo/metric-index.md](../../../../source/contracts/rds/starrocks_vpo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |

### Key filters and ETL business logic
- `a.entry_datetime >= date_add(CURRENT_DATE () ,interval - 1 MONTH) AND a.entry_datetime < CURRENT_DATE () AND a.order_type = 2 ; insert into rds_t_hyuk_tmp_100791 select a.source, a…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (6 objects).
2. Build staging temps (3 objects).
3. Materialize final output `tempdb.rds_tmp_body`.

```mermaid
flowchart LR
  P0["ods_hyuk.ods_cis_corp_order_eta_detail"]
  P1["ods_hyuk.ods_cis_corp_order_detail"]
  P2["ods_hyuk.ods_cis_corp_part_master"]
  P3["ods_hyuk.ods_cis_corp_manager"]
  P4["ods_hyuk.ods_cis_corp_history_eta_detail"]
  P5["ods_hyuk.ods_cis_corp_history_detail"]
  T0["rds_t_hyuk_tmp_100791"]
  T1["rds_tmp"]
  T2["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp_body"]
  O1["tempdb.rds_tmp"]
  P0 --> T0
  T2 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_hyuk.ods_cis_corp_order_eta_detail` | Permanent warehouse source |
| `ods_hyuk.ods_cis_corp_order_detail` | Permanent warehouse source |
| `ods_hyuk.ods_cis_corp_part_master` | Permanent warehouse source |
| `ods_hyuk.ods_cis_corp_manager` | Permanent warehouse source |
| `ods_hyuk.ods_cis_corp_history_eta_detail` | Permanent warehouse source |
| `ods_hyuk.ods_cis_corp_history_detail` | Permanent warehouse source |
| `rds_t_hyuk_tmp_100791` | Report staging / temp table |
| `rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Final report output object |
| `tempdb.rds_tmp` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_hyuk.ods_cis_corp_order_eta_detail`, `ods_hyuk.ods_cis_corp_order_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_t_hyuk_tmp_100791`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 6 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `source` | `a.source` | `source` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:4` |
| `order_type` | `a.order_type` | `order_type` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:5` |
| `order_no` | `a.order_no` | `order_no` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:6` |
| `order_line_no` | `a.order_line_no` | `order_line_no` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:7` |
| `vend_no` | `p.vend_no` | `vend_no` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:8` |
| `sku_no` | `b.sku_no` | `sku_no` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:9` |
| `part_no` | `p.part_no` | `part_no` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:10` |
| `ship_date` | `cast(a.ship_date as date)` | `ship_date` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | cast | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:11` |
| `eta_qty` | `a.eta_qty` | `eta_qty` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:12` |
| `eta_code` | `a.eta_code` | `eta_code` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:13` |
| `eta_date` | `cast(a.eta_date as date)` | `eta_date` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | cast | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:14` |
| `entry_id` | `a.entry_id` | `entry_id` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:15` |
| `loginid` | `m.loginid` | `loginid` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:16` |
| `tracking_no` | `a.tracking_no` | `tracking_no` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:17` |
| `entry_datetime` | `a.entry_datetime` | `entry_datetime` | `ods_hyuk.ods_cis_corp_history_eta_detail`, `ods_hyuk.ods_cis_corp_history_detail`, `ods_hyuk.ods_cis_corp_part_master`, `ods_hyuk.ods_cis_corp_manager`, `rds_t_hyuk_tmp_100791`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql:18` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` — Not documented as Azkaban partition |

**Plain language:** This is on-demand report SQL. Date windows come from the script body or runtime parameters, not from warehouse ETL bootstrap jobs.

### Data quality checks
- Row counts on `tempdb.rds_tmp_body` after report execution
- Spot-check measure totals vs source fact tables listed in L1 lineage

### Validation SQL
<!-- sql-artifact snippet_type: illustrative intent: audit -->
```sql
-- 1) row count on final output (session)
-- SELECT COUNT(*) FROM tempdb.rds_tmp_body;

-- 2) metric sum by a key dimension (replace <dim> / <metric> from final SELECT)
-- SELECT <dim>, SUM(<metric>) FROM tempdb.rds_tmp_body GROUP BY 1;

-- 3) grain duplicate check when natural key is known from SQL
-- SELECT <key_cols>, COUNT(*) FROM tempdb.rds_tmp_body GROUP BY <key_cols> HAVING COUNT(*) > 1;
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
| Report output | N/A | `tempdb.rds_tmp_body` (StarRocks) | on-demand | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `vpo` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_hyuk.ods_cis_corp_order_eta_detail` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |
| `ods_hyuk.ods_cis_corp_order_detail` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |
| `ods_hyuk.ods_cis_corp_part_master` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |
| `ods_hyuk.ods_cis_corp_manager` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |
| `ods_hyuk.ods_cis_corp_history_eta_detail` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |
| `ods_hyuk.ods_cis_corp_history_detail` | FROM/JOIN source | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp_body` final report result | `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_vpo/etl/vpo_eta_detail_current_history_region_rds_100791.sql` (source_kind: rds_report_sql).*
