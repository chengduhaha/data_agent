# REPORT: Typical POS example: serial LISTAGG plus authority program enrichment. (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_pos.pos_serial_authorization_rds_5378
- domain: RDS/vertica_pos
- one_line_purpose: RDS pos report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_pos/pos_serial_authorization_rds_5378.md
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
| **column_count** | 23 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_pos pos_serial_authorization_rds_5378" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_ca.dwd_disty_common_pos_di` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **upstream:** `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **upstream:** `ods_ca.ods_cis_corp_spa_detail` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **upstream:** `dw_ca.dwd_disty_common_order_serial_no_di` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **upstream:** `dim_ca.dim_disty_pm_authority_program_sku` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **upstream:** `dim_ca.dim_pub_customer_info` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **upstream:** `dim_ca.dim_disty_pm_authority_program_cust` — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |

### Key filters and ETL business logic
- `a.order_line_type != 'Comp' and a.vend_no in (8707,19173) and a.date_flag >= trunc(current_date()-1,'month') and a.date_flag < current_date() ; DROP TABLE IF EXISTS table_5378_ser_…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (7 objects).
2. Build staging temps (5 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_ca.dwd_disty_common_pos_di"]
  P1["dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di"]
  P2["ods_ca.ods_cis_corp_spa_detail"]
  P3["dw_ca.dwd_disty_common_order_serial_no_di"]
  P4["dim_ca.dim_disty_pm_authority_program_sku"]
  P5["dim_ca.dim_pub_customer_info"]
  P6["dim_ca.dim_disty_pm_authority_program_cust"]
  T0["table_5378_order"]
  T1["table_5378_ser_number_list"]
  T2["table_5378_final"]
  T3["rdsetl.rds_tmp"]
  T4["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T4 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_ca.dwd_disty_common_pos_di` | Permanent warehouse source |
| `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_spa_detail` | Permanent warehouse source |
| `dw_ca.dwd_disty_common_order_serial_no_di` | Permanent warehouse source |
| `dim_ca.dim_disty_pm_authority_program_sku` | Permanent warehouse source |
| `dim_ca.dim_pub_customer_info` | Permanent warehouse source |
| `dim_ca.dim_disty_pm_authority_program_cust` | Permanent warehouse source |
| `table_5378_order` | Report staging / temp table |
| `table_5378_ser_number_list` | Report staging / temp table |
| `table_5378_final` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `table_5378_order`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `table_5378_ser_number_list`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `table_5378_final`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 8 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `distributor_name` | `'Synnex Canada'` | `Synnex`, `Canada` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | literal | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:9` |
| `distributor_invoice_no` | `a.order_no` | `order_no` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:10` |
| `invoice_date` | `to_char(a.invoice_date,'mm/dd/yyyy')` | `to_char`, `invoice_date`, `mm`, `dd`, `yyyy` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | arithmetic | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:11` |
| `promotion_start_date` | `to_char(c.begin_date,'mm/dd/yyyy')` | `to_char`, `begin_date`, `mm`, `dd`, `yyyy` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | arithmetic | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:12` |
| `promotion_end_date` | `to_char(c.expire_date,'mm/dd/yyyy')` | `to_char`, `expire_date`, `mm`, `dd`, `yyyy` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | arithmetic | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:13` |
| `brother_promo_id` | `trim(c.marketing_comment)` | `marketing_comment` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:14` |
| `valid_brother_material` | `a.mfg_partno` | `mfg_partno` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:15` |
| `quantity_sold` | `a.ship_qty` | `ship_qty` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:16` |
| `end_user_price` | `a.ship_qty * (a.unit_price + isnull(a.unit_sum_exp,0))` | `ship_qty`, `unit_price`, `unit_sum_exp` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | coalesce | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:17` |
| `bill_to_name` | `a.bill_to_cust_name` | `bill_to_cust_name` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:18` |
| `bill_to_addr` | `a.bill_to_cust_addr` | `bill_to_cust_addr` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:19` |
| `bill_to_city` | `a.bill_to_cust_city` | `bill_to_cust_city` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:20` |
| `bill_to_zip` | `a.bill_to_cust_zip` | `bill_to_cust_zip` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:21` |
| `bill_to_state` | `a.bill_to_cust_state` | `bill_to_cust_state` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:22` |
| `ship_to_name` | `a.ship_to_name` | `ship_to_name` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:23` |
| `ship_to_zip` | `a.ship_to_zip` | `ship_to_zip` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:24` |
| `ship_to_state` | `a.ship_to_state` | `ship_to_state` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:25` |
| `invoice_amount` | `a.ship_qty * (a.unit_price + isnull(a.unit_sum_exp,0))` | `ship_qty`, `unit_price`, `unit_sum_exp` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | coalesce | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:17` |
| `spa_ref_no` | `b.spa_ref_no` | `spa_ref_no` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:27` |
| `order_line_no` | `a.order_line_no` | `order_line_no` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:28` |
| `order_type` | `a.order_type` | `order_type` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:29` |
| `sku_no` | `a.sku_no` | `sku_no` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:30` |
| `bill_to_cust_no` | `a.bill_to_cust_no` | `bill_to_cust_no` | `dw_ca.dwd_disty_common_pos_di`, `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di`, `ods_ca.ods_cis_corp_spa_detail`, `table_5378_order`, `dw_ca.dwd_disty_common_order_serial_no_di`, `dim_ca.dim_disty_pm_authority_program_sku`, `dim_ca.dim_pub_customer_info`, `dim_ca.dim_disty_pm_authority_program_cust`, `table_5378_ser_number_list`, `table_5378_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:31` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` | no |

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
-- See full script: source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_ca.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| `dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| `ods_ca.ods_cis_corp_spa_detail` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| `dw_ca.dwd_disty_common_order_serial_no_di` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| `dim_ca.dim_disty_pm_authority_program_sku` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| `dim_ca.dim_pub_customer_info` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |
| `dim_ca.dim_disty_pm_authority_program_cust` | FROM/JOIN source | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` (source_kind: rds_report_sql).*
