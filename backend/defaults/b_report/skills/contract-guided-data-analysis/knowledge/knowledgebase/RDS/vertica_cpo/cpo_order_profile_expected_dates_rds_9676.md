# REPORT: RDS cpo report SQL — cpo order profile expected dates rds 9676 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_cpo.cpo_order_profile_expected_dates_rds_9676
- domain: RDS/vertica_cpo
- one_line_purpose: RDS cpo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_cpo/cpo_order_profile_expected_dates_rds_9676.md
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
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_cpo cpo_order_profile_expected_dates_rds_9676" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_common_dw_orders_pl_extend_di` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `dim_us.dim_pub_location_info` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `dim_us.dim_pub_customer_info` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `dim_us.dim_pub_vpl_hierarchy_info` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `ods_us.ods_cis_corp_history_cpo_profile` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `ods_us.ods_cis_corp_cpo_profile` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `dm_us.dm_disty_sales_close_cpo_di` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **upstream:** `ods_us.ods_cis_corp_carton_header` — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **downstream:** `rdsetl.rds_tmp_3` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |

### Key filters and ETL business logic
- `a.cust_no in (430592, 124254, 430594) and a.date_flag >= DATE_TRUNC('MONTH',ADD_MONTHS(current_date(),-1)) and a.date_flag < current_date() ; drop table if exists table_9676_order;…`
- `a.order_line_type != 'Comp' and a.bill_to_cust_no in (430592,124254) and a.date_flag>=DATE_TRUNC('MONTH',ADD_MONTHS(current_date(),-1)) and a.date_flag<current_date() and a.ship_qt…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (11 objects).
2. Build staging temps (11 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_common_dw_orders_pl_extend_di"]
  P1["dim_us.dim_pub_part_info"]
  P2["ods_us.ods_cis_corp_history_header"]
  P3["dim_us.dim_pub_location_info"]
  P4["dim_us.dim_pub_customer_info"]
  P5["dim_us.dim_pub_vpl_hierarchy_info"]
  P6["ods_us.ods_cis_corp_history_cpo_profile"]
  P7["ods_us.ods_cis_corp_cpo_profile"]
  T0["table_9676_order_mid"]
  T1["table_9676_order"]
  T2["table_9676_track"]
  T3["table_9676_tab1"]
  T4["table_9676_tab2"]
  T5["table_9676_tab3"]
  T6["rdsetl.rds_tmp"]
  T7["rdsetl.rds_tmp_2"]
  T8["rdsetl.rds_tmp_3"]
  T9["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_2"]
  O2["rdsetl.rds_tmp_3"]
  O3["rdsetl.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_common_dw_orders_pl_extend_di` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header` | Permanent warehouse source |
| `dim_us.dim_pub_location_info` | Permanent warehouse source |
| `dim_us.dim_pub_customer_info` | Permanent warehouse source |
| `dim_us.dim_pub_vpl_hierarchy_info` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_profile` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_profile` | Permanent warehouse source |
| `dm_us.dm_disty_sales_close_cpo_di` | Permanent warehouse source |
| `ods_us.ods_cis_corp_carton_header` | Permanent warehouse source |
| `dw_us.dwd_disty_common_pos_di` | Permanent warehouse source |
| `table_9676_order_mid` | Report staging / temp table |
| `table_9676_order` | Report staging / temp table |
| `table_9676_track` | Report staging / temp table |
| `table_9676_tab1` | Report staging / temp table |
| `table_9676_tab2` | Report staging / temp table |
| `table_9676_tab3` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_2` | Report staging / temp table |
| `rdsetl.rds_tmp_3` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp_sheet_config` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_2` | Final report output object |
| `rdsetl.rds_tmp_3` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |
| `rdsetl.rds_tmp_sheet_config` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_us.dwd_disty_common_dw_orders_pl_extend_di`, `dim_us.dim_pub_part_info`, `ods_us.ods_cis_corp_history_header`, `dim_us.dim_pub_location_info`, `dim_us.dim_pub_customer_info`, `dim_us.dim_pub_vpl_hierarchy_info`, `ods_us.ods_cis_corp_history_cpo_profile`, `ods_us.ods_cis_corp_cpo_profile`, `dm_us.dm_disty_sales_close_cpo_di`, `ods_us.ods_cis_corp_carton_header`, `dw_us.dwd_disty_common_pos_di`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_9676_order_mid`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `table_9676_order`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `table_9676_track`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `table_9676_tab1`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `table_9676_tab2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `table_9676_tab3`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rdsetl.rds_tmp_2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `rdsetl.rds_tmp_3`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `rdsetl.rds_tmp_sheet_config`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 14 -- finalize `rdsetl.rds_tmp_2`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `rdsetl.rds_tmp_3`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 16 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `flag` | `2` | — | `rdsetl.rds_tmp_2`, `rdsetl.rds_tmp_3` | rename | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql:45` |
| `body_type` | `'Standard'` | `Standard` | `rdsetl.rds_tmp_2`, `rdsetl.rds_tmp_3` | literal | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql:300` |
| `cnt` | `count(*)` | — | `rdsetl.rds_tmp_2`, `rdsetl.rds_tmp_3` | agg | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql:301` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` | no |

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
-- See full script: source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_common_dw_orders_pl_extend_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `ods_us.ods_cis_corp_history_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `dim_us.dim_pub_location_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `dim_us.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `dim_us.dim_pub_vpl_hierarchy_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `ods_us.ods_cis_corp_history_cpo_profile` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `ods_us.ods_cis_corp_cpo_profile` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `dm_us.dm_disty_sales_close_cpo_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `ods_us.ods_cis_corp_carton_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |
| `dw_us.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_cpo/etl/cpo_order_profile_expected_dates_rds_9676.sql` (source_kind: rds_report_sql).*
