# REPORT: RDS pos report SQL — pos scm reference hierarchy rds 17482 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_pos.pos_scm_reference_hierarchy_rds_17482
- domain: RDS/vertica_pos
- one_line_purpose: RDS pos report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md
- ref_evidence: source/ref/RDS/vertica_pos/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `pos` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_pos` |
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
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_pos pos_scm_reference_hierarchy_rds_17482" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_sales_hierarchy_by_terr_user_role` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_pub_manager` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_pub_pm_vpc_matrix` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_pub_bd_hierarchy` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_disty_bd_project_cust` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_disty_bd_project_sku` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dw_us.dwd_disty_common_pos_di` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dim_us.dim_pub_order_type` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **upstream:** `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `pos` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_pos/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/vertica_pos/metric-index.md](../../../../source/contracts/rds/vertica_pos/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |

### Key filters and ETL business logic
- `m.loginid = 'sandra.macdonald' ) ,pm_hierarchy as ( select distinct pm.vend_no ,pm.vpl_no from dim_us.dim_pub_pm_vpc_matrix pm inner join dim_us.dim_pub_manager m on pm.pm_id = m.u…`
- `1 = 1 and fact.order_line_type in ('Kit','Single') and fact.date_flag >= case when date_part('day',getdate()) = 5 then timestampadd(month, -1, cast(timestampadd(dd, 22-day(getdate(…`
- `m.loginid = 'sandra.macdonald') ,pm_hierarchy as ( select distinct pm.vend_no ,pm.vpl_no from dim_us.dim_pub_pm_vpc_matrix pm inner join dim_us.dim_pub_manager m on pm.pm_id = m.us…`
- `1 = 1 and fact.company_no in (1) and fact.order_line_type in ('Kit','Single') and fact.date_flag >= case when date_part('day',getdate()) = 5 then timestampadd(month, -1, cast(times…`
- `1 = 2 ) ,ser_number_list as ( select fd.order_type as ser_order_type ,fd.order_no as ser_order_no ,fd.order_line_no as ser_order_line_no ,ser.ser_no ,case when fd.ship_qty > 0 then…`
- `p.ser_qty <> 0 and abs(b.ship_qty) <> abs(p.ser_qty) ) select fd.order_no ,fd.order_type ,fd.order_line_no ,to_date(to_char(fd.ship_date, 'MM/DD/YYYY'), 'MM/DD/YYYY') as Ship_Date …`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (17 objects).
2. Build staging temps (4 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_sales_hierarchy_by_terr_user_role"]
  P1["dim_us.dim_pub_manager"]
  P2["dim_us.dim_pub_pm_vpc_matrix"]
  P3["dim_us.dim_pub_bd_hierarchy"]
  P4["dim_us.dim_disty_bd_project_cust"]
  P5["dim_us.dim_disty_bd_project_sku"]
  P6["dw_us.dwd_disty_common_pos_di"]
  P7["dim_us.dim_pub_part_info"]
  T0["table_us_scm_reference_17482"]
  T1["table_us_pos_17482"]
  T2["rdsetl.rds_tmp"]
  T3["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T3 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_sales_hierarchy_by_terr_user_role` | Permanent warehouse source |
| `dim_us.dim_pub_manager` | Permanent warehouse source |
| `dim_us.dim_pub_pm_vpc_matrix` | Permanent warehouse source |
| `dim_us.dim_pub_bd_hierarchy` | Permanent warehouse source |
| `dim_us.dim_disty_bd_project_cust` | Permanent warehouse source |
| `dim_us.dim_disty_bd_project_sku` | Permanent warehouse source |
| `dw_us.dwd_disty_common_pos_di` | Permanent warehouse source |
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dim_us.dim_pub_order_type` | Permanent warehouse source |
| `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` | Permanent warehouse source |
| `dim_us.dim_pub_vpc_group_xref_view` | Permanent warehouse source |
| `dim_us.dim_pub_vpc_group_view` | Permanent warehouse source |
| `dim_us.dim_pub_customer_info` | Permanent warehouse source |
| `dim_us.dim_pub_sku_profile_extend` | Permanent warehouse source |
| `dw_us.dwd_stellr_billing_history_di` | Permanent warehouse source |
| `dm_us.dm_disty_pos_order_kit_di` | Permanent warehouse source |
| `dw_us.dwd_disty_common_order_serial_no_di` | Permanent warehouse source |
| `table_us_scm_reference_17482` | Report staging / temp table |
| `table_us_pos_17482` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dim_us.dim_pub_sales_hierarchy_by_terr_user_role`, `dim_us.dim_pub_manager`, `dim_us.dim_pub_pm_vpc_matrix`, `dim_us.dim_pub_bd_hierarchy`, `dim_us.dim_disty_bd_project_cust`, `dim_us.dim_disty_bd_project_sku`, `dw_us.dwd_disty_common_pos_di`, `dim_us.dim_pub_part_info`, `dim_us.dim_pub_order_type`, `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di`, `dim_us.dim_pub_vpc_group_xref_view`, `dim_us.dim_pub_vpc_group_view`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_us_scm_reference_17482`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `table_us_pos_17482`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 7 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `flag` | `1` | — | `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql:4` |
| `body_type` | `'Standard'` | `Standard` | `rdsetl.rds_tmp` | literal | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql:554` |
| `cnt` | `count(*)` | — | `rdsetl.rds_tmp` | agg | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql:555` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` | no |

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
-- See full script: source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_sales_hierarchy_by_terr_user_role` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_pm_vpc_matrix` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_bd_hierarchy` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_disty_bd_project_cust` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_disty_bd_project_sku` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dw_us.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_order_type` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_vpc_group_xref_view` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_vpc_group_view` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dim_us.dim_pub_sku_profile_extend` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |
| `dw_us.dwd_stellr_billing_history_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` (source_kind: rds_report_sql).*
