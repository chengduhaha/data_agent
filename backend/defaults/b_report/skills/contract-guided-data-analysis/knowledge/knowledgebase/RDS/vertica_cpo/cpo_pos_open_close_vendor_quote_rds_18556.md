# REPORT: RDS cpo report SQL — cpo pos open close vendor quote rds 18556 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_cpo.cpo_pos_open_close_vendor_quote_rds_18556
- domain: RDS/vertica_cpo
- one_line_purpose: RDS cpo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_cpo/cpo_pos_open_close_vendor_quote_rds_18556.md
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
| **column_count** | 12 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_cpo cpo_pos_open_close_vendor_quote_rds_18556" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_us.dwd_disty_common_pos_di` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `dw_us.dwd_disty_scm_shipped_order_spa_di` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `ods_us.ods_cis_corp_history_eu_custom` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `ods_us.ods_cis_corp_eu_custom_map` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `ods_us.ods_cis_corp_list_box_detail` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `dm_us.dm_disty_sales_open_cpo` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **upstream:** `dm_us.dm_disty_sales_close_cpo_di` — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`
- **downstream:** `rdsetl.rds_tmp_sheet_config` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |

### Key filters and ETL business logic
- `a.order_line_type != 'Comp' and a.date_flag>= DATE_TRUNC('month',current_date()-1) and a.date_flag<current_date() and a.vend_no=77105 ; update table_us18556_order x set total_order…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (10 objects).
2. Build staging temps (8 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_us.dwd_disty_common_pos_di"]
  P1["dw_us.dwd_disty_scm_shipped_order_spa_di"]
  P2["ods_us.ods_cis_corp_order_header"]
  P3["ods_us.ods_cis_corp_history_header"]
  P4["ods_us.ods_cis_corp_history_eu_custom"]
  P5["ods_us.ods_cis_corp_eu_custom_map"]
  P6["ods_us.ods_cis_corp_list_box_detail"]
  P7["dm_us.dm_disty_sales_open_cpo"]
  T0["table_us18556_order"]
  T1["table_us18556_tab1"]
  T2["table_us18556_cpo"]
  T3["table_us18556_tab2"]
  T4["rdsetl.rds_tmp"]
  T5["rdsetl.rds_tmp_2"]
  T6["rdsetl.rds_tmp_body"]
  T7["rdsetl.rds_tmp_sheet_config"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_2"]
  O2["rdsetl.rds_tmp_body"]
  O3["rdsetl.rds_tmp_sheet_config"]
  P0 --> T0
  T7 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_common_pos_di` | Permanent warehouse source |
| `dw_us.dwd_disty_scm_shipped_order_spa_di` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_eu_custom` | Permanent warehouse source |
| `ods_us.ods_cis_corp_eu_custom_map` | Permanent warehouse source |
| `ods_us.ods_cis_corp_list_box_detail` | Permanent warehouse source |
| `dm_us.dm_disty_sales_open_cpo` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dm_us.dm_disty_sales_close_cpo_di` | Permanent warehouse source |
| `table_us18556_order` | Report staging / temp table |
| `table_us18556_tab1` | Report staging / temp table |
| `table_us18556_cpo` | Report staging / temp table |
| `table_us18556_tab2` | Report staging / temp table |
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
**Source:** `dw_us.dwd_disty_common_pos_di`, `dw_us.dwd_disty_scm_shipped_order_spa_di`, `ods_us.ods_cis_corp_order_header`, `ods_us.ods_cis_corp_history_header`, `ods_us.ods_cis_corp_history_eu_custom`, `ods_us.ods_cis_corp_eu_custom_map`, `ods_us.ods_cis_corp_list_box_detail`, `dm_us.dm_disty_sales_open_cpo`, `dim_us.dim_pub_part_info`, `dm_us.dm_disty_sales_close_cpo_di`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_us18556_order`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `table_us18556_tab1`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `table_us18556_cpo`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `table_us18556_tab2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rdsetl.rds_tmp_2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rdsetl.rds_tmp_sheet_config`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 11 -- finalize `rdsetl.rds_tmp_2`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 12 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `rdsetl.rds_tmp_sheet_config`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cpo_id` | `a.cpo_id` | `cpo_id` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:84` |
| `cpo_no` | `a.cpo_no` | `cpo_no` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:6` |
| `cpo_cust_no` | `a.cpo_cust_no` | `cpo_cust_no` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:86` |
| `cpo_cust_name` | `a.cpo_cust_name` | `cpo_cust_name` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:87` |
| `quote_amount` | `round(a.cpo_unit_price * a.cpo_line_qty, 2)` | `cpo_unit_price`, `cpo_line_qty` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | arithmetic | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:88` |
| `eu_name` | `a.eu_company_name` | `eu_company_name` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | rename | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:89` |
| `expire_date` | `a.expected_close_date` | `expected_close_date` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | rename | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:90` |
| `vpl_code` | `b.vpl_code` | `vpl_code` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:91` |
| `cpo_entry_datetime` | `a.cpo_entry_datetime` | `cpo_entry_datetime` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:92` |
| `term_dates` | `''` | — | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | literal | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:93` |
| `vend_quote_id` | `a.vend_quote_id` | `vend_quote_id` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:94` |
| `spa_no` | `a.spa_no` | `spa_no` | `dm_us.dm_disty_sales_close_cpo_di`, `dim_us.dim_pub_part_info`, `table_us18556_cpo`, `table_us18556_tab1`, `table_us18556_tab2`, `rdsetl.rds_tmp`, `rdsetl.rds_tmp_2` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:95` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` | no |

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
-- See full script: source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `dw_us.dwd_disty_scm_shipped_order_spa_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `ods_us.ods_cis_corp_order_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `ods_us.ods_cis_corp_history_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `ods_us.ods_cis_corp_history_eu_custom` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `ods_us.ods_cis_corp_eu_custom_map` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `ods_us.ods_cis_corp_list_box_detail` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `dm_us.dm_disty_sales_open_cpo` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |
| `dm_us.dm_disty_sales_close_cpo_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` (source_kind: rds_report_sql).*
