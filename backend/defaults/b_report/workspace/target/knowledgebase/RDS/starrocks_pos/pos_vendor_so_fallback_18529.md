# REPORT: select count(*) from ods_us.ods_cis_corp_history_profile where mso_no is not null (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_pos.pos_vendor_so_fallback_18529
- domain: RDS/starrocks_pos
- one_line_purpose: RDS pos report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_pos/pos_vendor_so_fallback_18529.md
- ref_evidence: source/ref/RDS/starrocks_pos/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `pos` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_pos` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 10 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_pos pos_vendor_so_fallback_18529" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_pub_dw_orders_extend_di` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **upstream:** `ods_us.ods_cis_corp_order_type_rt` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header_rt` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **upstream:** `ods_us.ods_cis_corp_history_profile` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **upstream:** `ods_us.ods_cis_corp_order_profile` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **upstream:** `ods_us.ods_cis_corp_order_eta_code_rt` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **upstream:** `ods_us.ods_cis_corp_history_eta_code_rt` — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `pos` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_pos/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `pos` |
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

- **Source:** [source/contracts/rds/starrocks_pos/metric-index.md](../../../../source/contracts/rds/starrocks_pos/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |

### Key filters and ETL business logic
- `a.date_flag >= date_add(current_date(), interval -7 month) and a.date_flag < current_date() and a.order_type = 1 and a.cust_no = 657888 and a.vend_no = 64956 ; -- select count(*) f…`
- `a.order_no is not null and b.profile_type = 'SAPID' and b.profile_cat = 'ORDR' and b.profile_c is not null ; drop table if exists rds_us_vendor_mso_18529; create table rds_us_vendo…`
- `a.mso_no is not null and b.profile_type = 'SAPID' and b.profile_cat = 'ORDR' and b.profile_c is not null ; drop table if exists rds_us_vendor_po_18529; create table rds_us_vendor_p…`
- `b.vend_so_no is not null ; -- select * from rds_us_vendor_po_18529 where order_no = 38473907 drop table if exists rds_tmp; create table rds_tmp as select distinct a.create_date as …`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (7 objects).
2. Build staging temps (6 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_pub_dw_orders_extend_di"]
  P1["ods_us.ods_cis_corp_order_type_rt"]
  P2["ods_us.ods_cis_corp_history_header_rt"]
  P3["ods_us.ods_cis_corp_history_profile"]
  P4["ods_us.ods_cis_corp_order_profile"]
  P5["ods_us.ods_cis_corp_order_eta_code_rt"]
  P6["ods_us.ods_cis_corp_history_eta_code_rt"]
  T0["rds_us_order_18529"]
  T1["rds_us_vendor_so_18529"]
  T2["rds_us_vendor_mso_18529"]
  T3["rds_us_vendor_po_18529"]
  T4["rds_tmp"]
  T5["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  P0 --> T0
  T5 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_pub_dw_orders_extend_di` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_type_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_profile` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_profile` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_eta_code_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_eta_code_rt` | Permanent warehouse source |
| `rds_us_order_18529` | Report staging / temp table |
| `rds_us_vendor_so_18529` | Report staging / temp table |
| `rds_us_vendor_mso_18529` | Report staging / temp table |
| `rds_us_vendor_po_18529` | Report staging / temp table |
| `rds_tmp` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_us_order_18529`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_us_vendor_so_18529`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_us_vendor_mso_18529`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_us_vendor_po_18529`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 9 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `create_date` | `date(c.credit_rel_date)` | `credit_rel_date` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | udf | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:7` |
| `ship_date` | `date(a.ship_date)` | `ship_date` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | udf | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:8` |
| `cust_no` | `a.cust_no` | `cust_no` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:9` |
| `order_no` | `a.order_no` | `order_no` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:10` |
| `order_type` | `a.order_type` | `order_type` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:11` |
| `cust_po_no` | `a.cust_po_no` | `cust_po_no` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:12` |
| `mso_no` | `a.mso_no` | `mso_no` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:13` |
| `synnex_po_no` | `a.synnex_po_no` | `synnex_po_no` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:14` |
| `order_type_descr` | `b.order_type_descr` | `order_type_descr` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:15` |
| `loc_name` | `a.loc_name` | `loc_name` | `dw_us.dwd_disty_pub_dw_orders_extend_di`, `ods_us.ods_cis_corp_order_type_rt`, `ods_us.ods_cis_corp_history_header_rt`, `rds_us_order_18529`, `ods_us.ods_cis_corp_history_profile`, `ods_us.ods_cis_corp_order_profile`, `ods_us.ods_cis_corp_order_eta_code_rt`, `ods_us.ods_cis_corp_history_eta_code_rt`, `rds_us_vendor_so_18529`, `rds_us_vendor_mso_18529`, `rds_us_vendor_po_18529`, `tempdb.rds_tmp` | passthrough | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql:16` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `pos` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_pub_dw_orders_extend_di` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| `ods_us.ods_cis_corp_order_type_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| `ods_us.ods_cis_corp_history_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| `ods_us.ods_cis_corp_history_profile` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| `ods_us.ods_cis_corp_order_profile` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| `ods_us.ods_cis_corp_order_eta_code_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |
| `ods_us.ods_cis_corp_history_eta_code_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_pos/etl/pos_vendor_so_fallback_18529.sql` (source_kind: rds_report_sql).*
