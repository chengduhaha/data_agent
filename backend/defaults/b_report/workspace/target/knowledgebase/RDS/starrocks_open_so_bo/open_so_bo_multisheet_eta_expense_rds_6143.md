# REPORT: RDS open_so_bo report SQL — open so bo multisheet eta expense rds 6143 (`tempdb.rds_tmp_sheet_config`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_open_so_bo.open_so_bo_multisheet_eta_expense_rds_6143
- domain: RDS/starrocks_open_so_bo
- one_line_purpose: RDS open_so_bo report SQL on StarRocks producing `tempdb.rds_tmp_sheet_config`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_multisheet_eta_expense_rds_6143.md
- ref_evidence: source/ref/RDS/starrocks_open_so_bo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp_sheet_config`
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
| StarRocks | yes | `tempdb.rds_tmp_sheet_config` | Evidence SQL pack `starrocks_open_so_bo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp_sheet_config` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 3 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_open_so_bo open_so_bo_multisheet_eta_expense_rds_6143" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_ca.ods_cis_corp_customer_header` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_territory_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_cust_type_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `dm_ca.dm_pur_unieta_boso_detail_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_vend_master_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_order_exp_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **upstream:** `ods_ca.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **downstream:** `tempdb.rds_tmp_sheet_config` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **downstream:** `tempdb.rds_tmp_two` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`
- **downstream:** `tempdb.rds_tmp_2` (report output) — `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |

### Key filters and ETL business logic
- `a.cust_no in (1208695,1207991,1209317,1210017,1210172,1211745,1230183,1241238,1243713,1253947) ; -- TAB 1 drop table if exists tempdb.rds_tmp1; create table tempdb.rds_tmp1 PRIMARY…`
- `h.order_type in ( 1,8) and h.delete_date is null and h.closed_date is null and d.delete_date is null and d.order_qty -ifnull(d.ship_qty,0) <>0 ; drop table if exists tempdb.rds_sum…`
- `h.order_type = 1 and h.int_ref_type = 2 and h.from_loc_no = 98 and h.ship_date >= date_trunc('month',CURRENT_DATE()) and h.ship_date < CURRENT_DATE() and h.delete_date is null and …`
- `h.order_type = 1 and h.from_loc_no <> 98 and h.ship_date >= date_trunc('month',CURRENT_DATE()) and h.ship_date < CURRENT_DATE() and h.delete_date is null and d.delete_date is null`
- `h.order_type = 1 and h.from_loc_no <> 98 and h.ship_date >= date_trunc('month',CURRENT_DATE()) and h.ship_date < CURRENT_DATE() and h.delete_date is null and d.delete_date is null …`
- `h.order_type = 1 and h.delete_date is null and h.invoice_date >= date_add(current_date(), interval -17 month) and h.invoice_date < current_date()`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (12 objects).
2. Build staging temps (10 objects).
3. Materialize final output `tempdb.rds_tmp_sheet_config`.

```mermaid
flowchart LR
  P0["ods_ca.ods_cis_corp_customer_header"]
  P1["ods_ca.ods_cis_corp_territory_rt"]
  P2["ods_ca.ods_cis_corp_cust_type_rt"]
  P3["dm_ca.dm_pur_unieta_boso_detail_rt"]
  P4["ods_ca.ods_cis_corp_order_header_rt"]
  P5["ods_ca.ods_cis_corp_order_detail_rt"]
  P6["ods_ca.ods_cis_corp_part_master_rt"]
  P7["ods_ca.ods_cis_corp_vend_master_rt"]
  T0["tempdb.rds_tmp_sheet_config"]
  T1["tempdb.acct_6143"]
  T2["tempdb.rds_tmp1"]
  T3["tempdb.rds_sum_expense_6143"]
  T4["tempdb.rds_tmp"]
  T5["tempdb.rds_tmp_two"]
  T6["tempdb.rds_tmp_2"]
  T7["tempdb.rds_tmp_three"]
  T8["tempdb.rds_tmp_3"]
  T9["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp_sheet_config"]
  O1["tempdb.rds_tmp"]
  O2["tempdb.rds_tmp_two"]
  O3["tempdb.rds_tmp_2"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_ca.ods_cis_corp_customer_header` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_territory_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_cust_type_rt` | Permanent warehouse source |
| `dm_ca.dm_pur_unieta_boso_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_vend_master_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_order_exp_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_detail_rt` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_history_exp_rt` | Permanent warehouse source |
| `tempdb.rds_tmp_sheet_config` | Report staging / temp table |
| `tempdb.acct_6143` | Report staging / temp table |
| `tempdb.rds_tmp1` | Report staging / temp table |
| `tempdb.rds_sum_expense_6143` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_two` | Report staging / temp table |
| `tempdb.rds_tmp_2` | Report staging / temp table |
| `tempdb.rds_tmp_three` | Report staging / temp table |
| `tempdb.rds_tmp_3` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp_sheet_config` | Final report output object |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_two` | Final report output object |
| `tempdb.rds_tmp_2` | Final report output object |
| `tempdb.rds_tmp_three` | Final report output object |
| `tempdb.rds_tmp_3` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_ca.ods_cis_corp_customer_header`, `ods_ca.ods_cis_corp_territory_rt`, `ods_ca.ods_cis_corp_cust_type_rt`, `dm_ca.dm_pur_unieta_boso_detail_rt`, `ods_ca.ods_cis_corp_order_header_rt`, `ods_ca.ods_cis_corp_order_detail_rt`, `ods_ca.ods_cis_corp_part_master_rt`, `ods_ca.ods_cis_corp_vend_master_rt`, `ods_ca.ods_cis_corp_order_exp_rt`, `ods_ca.ods_cis_corp_history_header_rt`, `ods_ca.ods_cis_corp_history_detail_rt`, `ods_ca.ods_cis_corp_history_exp_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.rds_tmp_sheet_config`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.acct_6143`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.rds_tmp1`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.rds_sum_expense_6143`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.rds_tmp_two`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `tempdb.rds_tmp_2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `tempdb.rds_tmp_three`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `tempdb.rds_tmp_3`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- finalize `tempdb.rds_tmp_sheet_config`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 14 -- finalize `tempdb.rds_tmp_two`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `tempdb.rds_tmp_2`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `flag` | `3` | — | `tempdb.rds_tmp_3` | rename | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql:14` |
| `body_type` | `'Standard'` | `Standard` | `tempdb.rds_tmp_3` | literal | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql:420` |
| `cnt` | `count(*)` | — | `tempdb.rds_tmp_3` | agg | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql:421` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` — Not documented as Azkaban partition |

**Plain language:** This is on-demand report SQL. Date windows come from the script body or runtime parameters, not from warehouse ETL bootstrap jobs.

### Data quality checks
- Row counts on `tempdb.rds_tmp_sheet_config` after report execution
- Spot-check measure totals vs source fact tables listed in L1 lineage

### Validation SQL
<!-- sql-artifact snippet_type: illustrative intent: audit -->
```sql
-- 1) row count on final output (session)
-- SELECT COUNT(*) FROM tempdb.rds_tmp_sheet_config;

-- 2) metric sum by a key dimension (replace <dim> / <metric> from final SELECT)
-- SELECT <dim>, SUM(<metric>) FROM tempdb.rds_tmp_sheet_config GROUP BY 1;

-- 3) grain duplicate check when natural key is known from SQL
-- SELECT <key_cols>, COUNT(*) FROM tempdb.rds_tmp_sheet_config GROUP BY <key_cols> HAVING COUNT(*) > 1;
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
| Report output | N/A | `tempdb.rds_tmp_sheet_config` (StarRocks) | on-demand | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` | no |

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
-- See full script: source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_ca.ods_cis_corp_customer_header` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_territory_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_cust_type_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `dm_ca.dm_pur_unieta_boso_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_vend_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_order_exp_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_history_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |
| `ods_ca.ods_cis_corp_history_exp_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp_sheet_config` final report result | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` (source_kind: rds_report_sql).*
