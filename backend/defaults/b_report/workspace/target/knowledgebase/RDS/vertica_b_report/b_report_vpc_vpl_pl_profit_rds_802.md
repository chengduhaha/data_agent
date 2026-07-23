# REPORT: Drop temp tables if they exist (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_b_report.b_report_vpc_vpl_pl_profit_rds_802
- domain: RDS/vertica_b_report
- one_line_purpose: RDS b_report report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_b_report/b_report_vpc_vpl_pl_profit_rds_802.md
- ref_evidence: source/ref/RDS/vertica_b_report/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `b_report` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_b_report` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 2 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_b_report b_report_vpc_vpl_pl_profit_rds_802" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_ca.dim_pub_vpc_group_view` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_vpc_group_xref_view` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_vpl_info` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_date` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dw_ca.dwd_disty_common_dw_orders_pl_extend_di` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dw_ca.dwd_pub_common_history_header_extend` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_part_info` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_customer_info` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_vendor_info` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **upstream:** `dim_ca.dim_pub_cust_xref_all` — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `b_report` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_b_report/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `b_report` |
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

- **Source:** [source/contracts/rds/vertica_b_report/metric-index.md](../../../../source/contracts/rds/vertica_b_report/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |

### Key filters and ETL business logic
- `vpc_group_id IN (120, 119, 118) OR vpc_group_desc LIKE '%Audio/Video - Projector%'; -- ============================================================ -- t_vpl_802: vendor product lin…`
- `a.vpl_no = 15844`
- `a.vpl_no IN ( 14806, 14807, 14808, 14809, 14810, 14998, 14999, 15000, 15001, 15002, 15012, 15013, 15014, 15015, 15016, 15020, 15021, 15022, 15023, 15024, 15028, 15029, 15030, 15031…`
- `a.vpl_code IN ('TVLCDsmall', 'TVLCD', 'ACC-LG', 'Medical') AND a.active = 'Y'`
- `a.vpl_code IN ('PJONLINE', 'PJVAR') AND a.active = 'Y'`
- `COALESCE(a.alt_vend_no, a.vend_no) = 33449`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (10 objects).
2. Build staging temps (6 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_ca.dim_pub_vpc_group_view"]
  P1["dim_ca.dim_pub_vpc_group_xref_view"]
  P2["dim_ca.dim_pub_vpl_info"]
  P3["dim_ca.dim_pub_date"]
  P4["dw_ca.dwd_disty_common_dw_orders_pl_extend_di"]
  P5["dw_ca.dwd_pub_common_history_header_extend"]
  P6["dim_ca.dim_pub_part_info"]
  P7["dim_ca.dim_pub_customer_info"]
  T0["t_vpg_802"]
  T1["t_vpl_802"]
  T2["t_sls_802"]
  T3["rds_pl_ca802"]
  T4["rdsetl.rds_tmp"]
  T5["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T5 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_ca.dim_pub_vpc_group_view` | Permanent warehouse source |
| `dim_ca.dim_pub_vpc_group_xref_view` | Permanent warehouse source |
| `dim_ca.dim_pub_vpl_info` | Permanent warehouse source |
| `dim_ca.dim_pub_date` | Permanent warehouse source |
| `dw_ca.dwd_disty_common_dw_orders_pl_extend_di` | Permanent warehouse source |
| `dw_ca.dwd_pub_common_history_header_extend` | Permanent warehouse source |
| `dim_ca.dim_pub_part_info` | Permanent warehouse source |
| `dim_ca.dim_pub_customer_info` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_info` | Permanent warehouse source |
| `dim_ca.dim_pub_cust_xref_all` | Permanent warehouse source |
| `t_vpg_802` | Report staging / temp table |
| `t_vpl_802` | Report staging / temp table |
| `t_sls_802` | Report staging / temp table |
| `rds_pl_ca802` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_ca.dim_pub_vpc_group_view`, `dim_ca.dim_pub_vpc_group_xref_view`, `dim_ca.dim_pub_vpl_info`, `dim_ca.dim_pub_date`, `dw_ca.dwd_disty_common_dw_orders_pl_extend_di`, `dw_ca.dwd_pub_common_history_header_extend`, `dim_ca.dim_pub_part_info`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_pub_vendor_info`, `dim_ca.dim_pub_cust_xref_all`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `t_vpg_802`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `t_vpl_802`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `t_sls_802`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_pl_ca802`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 9 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `body_type` | `'standard'` | `standard` | `rdsetl.rds_tmp` | literal | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql:520` |
| `cnt` | `COUNT(*)` | — | `rdsetl.rds_tmp` | agg | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql:521` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `b_report` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_ca.dim_pub_vpc_group_view` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_vpc_group_xref_view` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_vpl_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_date` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dw_ca.dwd_disty_common_dw_orders_pl_extend_di` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dw_ca.dwd_pub_common_history_header_extend` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |
| `dim_ca.dim_pub_cust_xref_all` | FROM/JOIN source | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_b_report/etl/b_report_vpc_vpl_pl_profit_rds_802.sql` (source_kind: rds_report_sql).*
