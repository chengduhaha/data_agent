# REPORT: RDS cpo report SQL — cpo open emailquote cart inventory rds 14943 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_cpo.cpo_open_emailquote_cart_inventory_rds_14943
- domain: RDS/vertica_cpo
- one_line_purpose: RDS cpo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_cpo/cpo_open_emailquote_cart_inventory_rds_14943.md
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
| **column_count** | 4 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_cpo cpo_open_emailquote_cart_inventory_rds_14943" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_us.dim_pub_part_info` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `dm_us.dm_disty_sales_open_cpo` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `ods_us.ods_cis_corp_cpo_profile` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `dim_us.dim_pub_customer_info` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `ods_us.ods_etl_ec_cart_current` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `ods_us.ods_cis_corp_ec_user` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `dim_us.dim_pub_customer_address_contacts_info` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **upstream:** `ods_us.ods_cis_corp_history_header` — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **downstream:** `rdsetl.rds_tmp_2` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`
- **downstream:** `rdsetl.rds_tmp_sheet_config` (report output) — `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |

### Key filters and ETL business logic
- `a.cpo_delete_datetime is null and a.cpo_line_delete_datetime is null and a.convert_datetime is null and c.data_source='CIS' and c.vend_no in (select vend_no from ods_gbl.ods_daas_m…`
- `a.rn=1 ; -- tab 2 drop table if exists table_us14943_ec; create local temporary table table_us14943_ec on commit preserve rows as select a.vend_no ,a.vend_name ,b.entry_datetime as…`
- `a.vend_no in (select vend_no from ods_gbl.ods_daas_mygbldaas_smb_vend_image_config where e_catalog_source ='GCC' and active = 'Y' and country_code = 'US') and a.data_source = 'CIS'…`
- `b.entry_datetime>=current_date()-24 and b.cpo_id>0 and b.status='SUBMITTED' ; insert into table_us14943_add_order select a.sku_no ,a.cust_no ,b.cpo_id ,c.entry_datetime ,c.order_no…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (15 objects).
2. Build staging temps (16 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dim_us.dim_pub_part_info"]
  P1["dm_us.dm_disty_sales_open_cpo"]
  P2["ods_us.ods_cis_corp_cpo_profile"]
  P3["dim_us.dim_pub_customer_info"]
  P4["ods_us.ods_etl_ec_cart_current"]
  P5["ods_us.ods_cis_corp_ec_user"]
  P6["ods_gbl.ods_daas_mygbldaas_smb_vend_image_config"]
  P7["dim_us.dim_pub_customer_address_contacts_info"]
  T0["table_us14943_cpo"]
  T1["table_us14943_add_addr"]
  T2["table_us14943_add_order_info"]
  T3["table_us14943_add_order_info_2"]
  T4["table_us14943_add_qty"]
  T5["table_us14943_tab1"]
  T6["table_us14943_ec"]
  T7["table_us14943_add_order"]
  T8["table_us14943_add_cpo"]
  T9["table_us14943_final"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_2"]
  O2["rdsetl.rds_tmp_body"]
  O3["rdsetl.rds_tmp_sheet_config"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_part_info` | Permanent warehouse source |
| `dm_us.dm_disty_sales_open_cpo` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_profile` | Permanent warehouse source |
| `dim_us.dim_pub_customer_info` | Permanent warehouse source |
| `ods_us.ods_etl_ec_cart_current` | Permanent warehouse source |
| `ods_us.ods_cis_corp_ec_user` | Permanent warehouse source |
| `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | Permanent warehouse source |
| `dim_us.dim_pub_customer_address_contacts_info` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_header` | Permanent warehouse source |
| `ods_us.ods_cis_corp_inv_qty` | Permanent warehouse source |
| `ods_us.ods_etl_ec_cart_history` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_detail` | Permanent warehouse source |
| `dm_us.dm_disty_sales_close_cpo_di` | Permanent warehouse source |
| `table_us14943_cpo` | Report staging / temp table |
| `table_us14943_add_addr` | Report staging / temp table |
| `table_us14943_add_order_info` | Report staging / temp table |
| `table_us14943_add_order_info_2` | Report staging / temp table |
| `table_us14943_add_qty` | Report staging / temp table |
| `table_us14943_tab1` | Report staging / temp table |
| `table_us14943_ec` | Report staging / temp table |
| `table_us14943_add_order` | Report staging / temp table |
| `table_us14943_add_cpo` | Report staging / temp table |
| `table_us14943_final` | Report staging / temp table |
| `table_us14943_add_qty2` | Report staging / temp table |
| `table_us14943_tab2` | Report staging / temp table |
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
**Source:** `dim_us.dim_pub_part_info`, `dm_us.dm_disty_sales_open_cpo`, `ods_us.ods_cis_corp_cpo_profile`, `dim_us.dim_pub_customer_info`, `ods_us.ods_etl_ec_cart_current`, `ods_us.ods_cis_corp_ec_user`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `dim_us.dim_pub_customer_address_contacts_info`, `ods_us.ods_cis_corp_order_header`, `ods_us.ods_cis_corp_history_header`, `ods_us.ods_cis_corp_inv_qty`, `ods_us.ods_etl_ec_cart_history`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_us14943_cpo`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `table_us14943_add_addr`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `table_us14943_add_order_info`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `table_us14943_add_order_info_2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `table_us14943_add_qty`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `table_us14943_tab1`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `table_us14943_ec`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `table_us14943_add_order`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `table_us14943_add_cpo`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `table_us14943_final`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `table_us14943_add_qty2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `table_us14943_tab2`
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

#### Step 16 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 17 -- finalize `rdsetl.rds_tmp_sheet_config`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cpo_id` | `a.cpo_id` | `cpo_id` | `table_us14943_cpo`, `ods_us.ods_cis_corp_history_header`, `table_us14943_add_order_info`, `ods_us.ods_cis_corp_inv_qty`, `table_us14943_add_addr`, `table_us14943_add_order_info_2`, `table_us14943_add_qty`, `dim_us.dim_pub_part_info`, `ods_us.ods_etl_ec_cart_history`, `ods_us.ods_cis_corp_ec_user`, `dim_us.dim_pub_customer_info`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql:4` |
| `order_no` | `b.order_no` | `order_no` | `table_us14943_cpo`, `ods_us.ods_cis_corp_history_header`, `table_us14943_add_order_info`, `ods_us.ods_cis_corp_inv_qty`, `table_us14943_add_addr`, `table_us14943_add_order_info_2`, `table_us14943_add_qty`, `dim_us.dim_pub_part_info`, `ods_us.ods_etl_ec_cart_history`, `ods_us.ods_cis_corp_ec_user`, `dim_us.dim_pub_customer_info`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql:75` |
| `order_type` | `b.order_type` | `order_type` | `table_us14943_cpo`, `ods_us.ods_cis_corp_history_header`, `table_us14943_add_order_info`, `ods_us.ods_cis_corp_inv_qty`, `table_us14943_add_addr`, `table_us14943_add_order_info_2`, `table_us14943_add_qty`, `dim_us.dim_pub_part_info`, `ods_us.ods_etl_ec_cart_history`, `ods_us.ods_cis_corp_ec_user`, `dim_us.dim_pub_customer_info`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql:76` |
| `entry_datetime` | `b.entry_datetime` | `entry_datetime` | `table_us14943_cpo`, `ods_us.ods_cis_corp_history_header`, `table_us14943_add_order_info`, `ods_us.ods_cis_corp_inv_qty`, `table_us14943_add_addr`, `table_us14943_add_order_info_2`, `table_us14943_add_qty`, `dim_us.dim_pub_part_info`, `ods_us.ods_etl_ec_cart_history`, `ods_us.ods_cis_corp_ec_user`, `dim_us.dim_pub_customer_info`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | passthrough | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql:77` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` | no |

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
-- See full script: source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_part_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `dm_us.dm_disty_sales_open_cpo` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_cpo_profile` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `dim_us.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_etl_ec_cart_current` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_ec_user` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `dim_us.dim_pub_customer_address_contacts_info` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_order_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_history_header` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_inv_qty` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_etl_ec_cart_history` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `ods_us.ods_cis_corp_history_detail` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |
| `dm_us.dm_disty_sales_close_cpo_di` | FROM/JOIN source | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_cpo/etl/cpo_open_emailquote_cart_inventory_rds_14943.sql` (source_kind: rds_report_sql).*
