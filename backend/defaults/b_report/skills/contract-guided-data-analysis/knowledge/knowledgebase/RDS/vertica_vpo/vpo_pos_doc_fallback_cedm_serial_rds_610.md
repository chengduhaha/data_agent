# REPORT: RDS vpo report SQL — vpo pos doc fallback cedm serial rds 610 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_vpo.vpo_pos_doc_fallback_cedm_serial_rds_610
- domain: RDS/vertica_vpo
- one_line_purpose: RDS vpo report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_vpo/vpo_pos_doc_fallback_cedm_serial_rds_610.md
- ref_evidence: source/ref/RDS/vertica_vpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `rdsetl.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `vpo` domain report on Vertica
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Vertica | yes | `rdsetl.rds_tmp` | Evidence SQL pack `vertica_vpo` |
| StarRocks | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `rdsetl.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 57 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_vpo vpo_pos_doc_fallback_cedm_serial_rds_610" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_wcla.dwd_disty_common_pos_di` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dim_wcla.dim_pub_customer_address_contacts_info` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dw_wcla.dwd_pub_common_shipped_order_scm_spa_detail_di` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dw_wcla.dwd_disty_sales_eu_custom_di` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dim_wcla.dim_pub_eu_custom_map_view` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dim_wcla.dim_pub_list_box_detail` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dw_wcla.dwd_disty_sales_open_order_detail` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dw_wcla.dwd_pub_common_history_header_extend` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `dw_wcla.dwd_disty_common_po_basic` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **upstream:** `ods_wcla.ods_cis_corp_vend_doc` — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `vpo` curated example report SQL for Vertica. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/vertica_vpo/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/vertica_vpo/metric-index.md](../../../../source/contracts/rds/vertica_vpo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |

### Key filters and ETL business logic
- `a.date_flag >= CURRENT_DATE() - 7 AND a.date_flag < CURRENT_DATE() AND a.order_line_type NOT IN ('Comp') AND a.vend_no IN (32991, 30040, 30060, 30070, 33001, 30068) AND a.order_typ…`
- `l.list_box_code = 'CEDM' AND l.code_desc = 'DEAL ID' ) c ON a.order_no = c.order_no AND a.order_type = c.order_type; UPDATE rds_wcla610_t2 SET doc_no_order = b.order_no FROM dw_wcl…`
- `ABS(a.ship_qty) > b.cnt ; insert into rds_wcla610_final SELECT a.order_no ,a.order_type ,a.order_line_no ,sku_no ,EU_company_name ,EU_address1 ,EU_address2 ,EU_city ,EU_state ,EU_z…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (12 objects).
2. Build staging temps (7 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_wcla.dwd_disty_common_pos_di"]
  P1["dim_wcla.dim_pub_customer_address_contacts_info"]
  P2["dw_wcla.dwd_pub_common_shipped_order_scm_spa_detail_di"]
  P3["dw_wcla.dwd_disty_sales_eu_custom_di"]
  P4["dim_wcla.dim_pub_eu_custom_map_view"]
  P5["dim_wcla.dim_pub_list_box_detail"]
  P6["dw_wcla.dwd_disty_sales_open_order_detail"]
  P7["dw_wcla.dwd_pub_common_history_header_extend"]
  T0["rds_wcla610_t1"]
  T1["rds_wcla610_t2"]
  T2["rds_wcla610_ser"]
  T3["rds_wcla610_ser_count"]
  T4["rds_wcla610_final"]
  T5["rdsetl.rds_tmp"]
  T6["rdsetl.rds_tmp_body"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T6 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_wcla.dwd_disty_common_pos_di` | Permanent warehouse source |
| `dim_wcla.dim_pub_customer_address_contacts_info` | Permanent warehouse source |
| `dw_wcla.dwd_pub_common_shipped_order_scm_spa_detail_di` | Permanent warehouse source |
| `dw_wcla.dwd_disty_sales_eu_custom_di` | Permanent warehouse source |
| `dim_wcla.dim_pub_eu_custom_map_view` | Permanent warehouse source |
| `dim_wcla.dim_pub_list_box_detail` | Permanent warehouse source |
| `dw_wcla.dwd_disty_sales_open_order_detail` | Permanent warehouse source |
| `dw_wcla.dwd_pub_common_history_header_extend` | Permanent warehouse source |
| `dw_wcla.dwd_disty_common_po_basic` | Permanent warehouse source |
| `ods_wcla.ods_cis_corp_vend_doc` | Permanent warehouse source |
| `dw_wcla.dwd_disty_ap_hold_df` | Permanent warehouse source |
| `dw_wcla.dwd_disty_common_order_serial_no_di` | Permanent warehouse source |
| `rds_wcla610_t1` | Report staging / temp table |
| `rds_wcla610_t2` | Report staging / temp table |
| `rds_wcla610_ser` | Report staging / temp table |
| `rds_wcla610_ser_count` | Report staging / temp table |
| `rds_wcla610_final` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_wcla.dwd_disty_common_pos_di`, `dim_wcla.dim_pub_customer_address_contacts_info`, `dw_wcla.dwd_pub_common_shipped_order_scm_spa_detail_di`, `dw_wcla.dwd_disty_sales_eu_custom_di`, `dim_wcla.dim_pub_eu_custom_map_view`, `dim_wcla.dim_pub_list_box_detail`, `dw_wcla.dwd_disty_sales_open_order_detail`, `dw_wcla.dwd_pub_common_history_header_extend`, `dw_wcla.dwd_disty_common_po_basic`, `ods_wcla.ods_cis_corp_vend_doc`, `dw_wcla.dwd_disty_ap_hold_df`, `dw_wcla.dwd_disty_common_order_serial_no_di`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `rds_wcla610_t1`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_wcla610_t2`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_wcla610_ser`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_wcla610_ser_count`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rds_wcla610_final`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rdsetl.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rdsetl.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 10 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_no` | `a.order_no` | `order_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:57` |
| `order_type` | `a.order_type` | `order_type` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:5` |
| `order_line_no` | `a.order_line_no` | `order_line_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:6` |
| `sku_no` | `sku_no` | `sku_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:7` |
| `EU_company_name` | `EU_company_name` | `EU_company_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:8` |
| `EU_address1` | `EU_address1` | `EU_address1` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:9` |
| `EU_address2` | `EU_address2` | `EU_address2` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:10` |
| `EU_city` | `EU_city` | `EU_city` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:11` |
| `EU_state` | `EU_state` | `EU_state` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:12` |
| `EU_zip` | `EU_zip` | `EU_zip` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:13` |
| `EU_country` | `EU_country` | `EU_country` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:14` |
| `EU_contact_name` | `EU_contact_name` | `EU_contact_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:15` |
| `EU_phone` | `a.eu_contact_phone` | `eu_contact_phone` | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:16` |
| `ship_to_name` | `ship_to_name` | `ship_to_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:17` |
| `ship_to_addr` | `ship_to_addr` | `ship_to_addr` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:18` |
| `ship_to_city` | `ship_to_city` | `ship_to_city` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:19` |
| `ship_to_state` | `ship_to_state` | `ship_to_state` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:20` |
| `ship_to_zip` | `ship_to_zip` | `ship_to_zip` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:21` |
| `ship_to_country` | `ship_to_country` | `ship_to_country` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:22` |
| `sold_to_cust_no` | `sold_to_cust_no` | `sold_to_cust_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:23` |
| `sold_to_cust_name` | `sold_to_cust_name` | `sold_to_cust_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:24` |
| `sold_to_addr` | `sold_to_addr` | `sold_to_addr` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:78` |
| `sold_to_city` | `sold_to_city` | `sold_to_city` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:79` |
| `sold_to_state` | `sold_to_state` | `sold_to_state` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:80` |
| `sold_to_zip` | `sold_to_zip` | `sold_to_zip` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:81` |
| `sold_to_country` | `sold_to_country` | `sold_to_country` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:82` |
| `sold_to_contact_name` | `sold_to_contact_name` | `sold_to_contact_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:83` |
| `sold_to_contact_phone` | `sold_to_contact_phone` | `sold_to_contact_phone` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:84` |
| `bill_to_cust_no` | `bill_to_cust_no` | `bill_to_cust_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:25` |
| `bill_to_cust_name` | `bill_to_cust_name` | `bill_to_cust_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:26` |
| `bill_to_address` | `a.bill_to_cust_addr` | `bill_to_cust_addr` | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:27` |
| `bill_to_address2` | `CAST(NULL AS VARCHAR(60))` | — | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:28` |
| `bill_to_cust_city` | `bill_to_cust_city` | `bill_to_cust_city` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:29` |
| `bill_to_cust_state` | `bill_to_cust_state` | `bill_to_cust_state` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:30` |
| `bill_to_cust_zip` | `bill_to_cust_zip` | `bill_to_cust_zip` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:31` |
| `bill_to_cust_country` | `bill_to_cust_country` | `bill_to_cust_country` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:32` |
| `bill_to_contact_name` | `bill_to_contact_name` | `bill_to_contact_name` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:33` |
| `bill_to_contact_phone` | `bill_to_contact_phone` | `bill_to_contact_phone` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:34` |
| `sales_terr` | `sales_terr` | `sales_terr` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:35` |
| `terr_manager` | `CAST(NULL AS VARCHAR(60))` | — | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:28` |
| `ship_qty` | `a.ship_qty - b.cnt * SIGN(a.ship_qty)` | `ship_qty`, `cnt`, `SIGN` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | arithmetic | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:375` |
| `vend_part_no` | `a.mfg_partno` | `mfg_partno` | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:38` |
| `invoice_date` | `invoice_date` | `invoice_date` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:39` |
| `u_price` | `a.unit_price` | `unit_price` | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | rename | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:40` |
| `extended_unit_price` | `a.unit_price - a.unit_sum_exp` | `unit_price`, `unit_sum_exp` | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | arithmetic | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:41` |
| `drop_ship_flag` | `CASE WHEN a.from_loc_no = 98 THEN 'DROP' ELSE 'STCK' END` | `from_loc_no`, `DROP`, `STCK` | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | case | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:42` |
| `int_ref_no` | `int_ref_no` | `int_ref_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:43` |
| `int_ref_type` | `int_ref_type` | `int_ref_type` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:44` |
| `from_loc_no` | `from_loc_no` | `from_loc_no` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:42` |
| `inv_type` | `inv_type` | `inv_type` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:46` |
| `scm_no_1` | `scm_no_1` | `scm_no_1` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:139` |
| `spa_no1` | `spa_no1` | `spa_no1` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:140` |
| `deal_id` | `deal_id` | `deal_id` | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:141` |
| `ser_no` | `''` | — | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | literal | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:255` |
| `asset_tag` | `''` | — | `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | literal | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:255` |
| `doc_no_order` | `CAST(NULL AS INT)` | — | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:47` |
| `vend_inv_no` | `CAST(NULL AS VARCHAR(200))` | — | `temp_t1`, `rds_wcla610_t2`, `rds_wcla610_ser_count`, `rds_wcla610_final`, `Name`, `ID`, `Tax`, `Address`, `City`, `State`, `Postal`, `Country`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:48` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` | no |

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
-- See full script: source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_wcla.dwd_disty_common_pos_di` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dim_wcla.dim_pub_customer_address_contacts_info` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_pub_common_shipped_order_scm_spa_detail_di` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_disty_sales_eu_custom_di` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dim_wcla.dim_pub_eu_custom_map_view` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dim_wcla.dim_pub_list_box_detail` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_disty_sales_open_order_detail` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_pub_common_history_header_extend` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_disty_common_po_basic` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `ods_wcla.ods_cis_corp_vend_doc` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_disty_ap_hold_df` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |
| `dw_wcla.dwd_disty_common_order_serial_no_di` | FROM/JOIN source | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` (source_kind: rds_report_sql).*
