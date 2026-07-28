# REPORT: RDS ap report SQL — ap month end position terms bucket rds 3977 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_ap.ap_month_end_position_terms_bucket_rds_3977
- domain: RDS/vertica_ap
- one_line_purpose: RDS ap report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_ap/ap_month_end_position_terms_bucket_rds_3977.md
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
| **column_count** | 1 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_ap ap_month_end_position_terms_bucket_rds_3977" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_ca.dws_disty_ap_vend_aging_df` — `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql`
- **upstream:** `dm_ca.dm_ap_aging_header_df` — `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql`
- **upstream:** `dim_ca.dim_pub_vendor_profile` — `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` |

### Key filters and ETL business logic
- `date_flag < date_trunc('month', current_date())::date ; create local temporary table rds_3977_main on commit preserve rows as select h.vend_no, h.vend_name, h.vend_type, cast(null …`
- `h.date_flag = c.dt and h.sum_level in ('UOT', 'UOTC') and cast(h.terms_no as varchar(10)) in ('3', '12', '27', '126', '1127')`
- `h.date_flag = c.dt and h.sum_level = 'VVU' and cast(h.terms_no as varchar(10)) = 'V'`
- `h.date_flag = c.dt and h.sum_level in ('UOT', 'UOTC') and cast(h.terms_no as varchar(10)) in ('2', '362', '125', '1125', '363')`
- `m.vend_no = u.vend_no ; update rds_3977_main m set uvdebits_cdn = u.amt from rds_3977_uv_cdn u where m.vend_no = u.vend_no ; update rds_3977_main m set tb_usd = t.amt from rds_3977…`
- `m.vend_no = p.vend_no ; drop table if exists rdsetl.rds_tmp; create table rdsetl.rds_tmp as select date_flag, vend_currency, vend_no, vend_name, vend_type, old_comp, uvdebits_usd, …`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (3 objects).
2. Build staging temps (10 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_ca.dws_disty_ap_vend_aging_df"]
  P1["dm_ca.dm_ap_aging_header_df"]
  P2["dim_ca.dim_pub_vendor_profile"]
  T0["rds_3977_run_ctx"]
  T1["rds_3977_main"]
  T2["rds_3977_uv_usd"]
  T3["rds_3977_uv_cdn"]
  T4["rds_3977_tb_usd"]
  T5["rds_3977_tb_cdn"]
  T6["rds_3977_acc_usd"]
  T7["rds_3977_acc_cdn"]
  T8["rdsetl.rds_tmp"]
  T9["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_ca.dws_disty_ap_vend_aging_df` | Permanent warehouse source |
| `dm_ca.dm_ap_aging_header_df` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_profile` | Permanent warehouse source |
| `rds_3977_run_ctx` | Report staging / temp table |
| `rds_3977_main` | Report staging / temp table |
| `rds_3977_uv_usd` | Report staging / temp table |
| `rds_3977_uv_cdn` | Report staging / temp table |
| `rds_3977_tb_usd` | Report staging / temp table |
| `rds_3977_tb_cdn` | Report staging / temp table |
| `rds_3977_acc_usd` | Report staging / temp table |
| `rds_3977_acc_cdn` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_ca.dws_disty_ap_vend_aging_df`, `dm_ca.dm_ap_aging_header_df`, `dim_ca.dim_pub_vendor_profile`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_3977_run_ctx`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_3977_main`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_3977_uv_usd`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_3977_uv_cdn`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rds_3977_tb_usd`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rds_3977_tb_cdn`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rds_3977_acc_usd`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `rds_3977_acc_cdn`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `dt` | `max(date_flag)` | `date_flag` | `dw_ca.dws_disty_ap_vend_aging_df`, `dm_ca.dm_ap_aging_header_df`, `rds_3977_run_ctx`, `rds_3977_uv_usd`, `rds_3977_uv_cdn`, `rds_3977_tb_usd`, `rds_3977_tb_cdn`, `rds_3977_acc_usd`, `rds_3977_acc_cdn`, `dim_ca.dim_pub_vendor_profile`, `rds_3977_main`, `rdsetl.rds_tmp` | agg | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql:13` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` | no |

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
-- See full script: source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_ca.dws_disty_ap_vend_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` |
| `dm_ca.dm_ap_aging_header_df` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` |
| `dim_ca.dim_pub_vendor_profile` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_ap/etl/ap_month_end_position_terms_bucket_rds_3977.sql` (source_kind: rds_report_sql).*
