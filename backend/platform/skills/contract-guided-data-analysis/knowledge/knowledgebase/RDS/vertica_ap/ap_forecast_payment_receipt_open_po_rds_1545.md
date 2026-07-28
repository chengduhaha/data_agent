# REPORT: RDS ap report SQL — ap forecast payment receipt open po rds 1545 (`rdsetl.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.vertica_ap.ap_forecast_payment_receipt_open_po_rds_1545
- domain: RDS/vertica_ap
- one_line_purpose: RDS ap report SQL on Vertica producing `rdsetl.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql
- knowledgebase_path: target/knowledgebase/RDS/vertica_ap/ap_forecast_payment_receipt_open_po_rds_1545.md
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
| **column_count** | 23 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS vertica_ap ap_forecast_payment_receipt_open_po_rds_1545" --intent find_table_schema` |

### Lineage
- **upstream:** `dw_ca.dws_disty_brpt_vend_comb_mtd` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dim_ca.dim_pub_vendor_info` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dim_ca.dim_pub_vend_location_view` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dim_ca.dim_pub_terms_file_view` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `ods_ca.ods_cis_corp_vend_payments` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dw_ca.dws_disty_ap_vend_aging_df` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dw_ca.dwd_disty_pm_report_goal` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dw_ca.dwd_disty_ap_ap_hold` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dw_ca.dwd_disty_ap_vend_doc_df` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **upstream:** `dim_ca.dim_pub_date` — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **downstream:** `rdsetl.rds_tmp` (report output) — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`
- **downstream:** `rdsetl.rds_tmp_body` (report output) — `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql`

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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |

### Key filters and ETL business logic
- `date_flag = current_date()-1`
- `(mtd_sales!=0 and mtd_cost!=0 and qtd_sales!=0 and qtd_cost!=0) ; drop table if exists rds_vend_ca1545; create local temporary table rds_vend_ca1545 on commit preserve rows as sele…`
- `a.vend_no=b.vend_no and b.loc_no=1 and b.terms=c.doc_terms and exists (select 1 from rds_sales_qtr_ca1545 d where a.vend_no=d.vend_no) ; --actual payment drop table if exists rds_a…`
- `date_flag = current_date()-1 and sum_level='V'`
- `period = (DATEDIFF('month', DATE '1993-01-01', current_date()) + 1) and vpl_no = 0 and vend_no != 0`
- `a.vend_no=b.vend_no and ifnull(b.mtd_sales,0)<>0 ; --MTD receipt drop table if exists TEMP_DATE; create local temporary table TEMP_DATE on commit preserve rows as SELECT CASE WHEN …`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (10 objects).
2. Build staging temps (25 objects).
3. Materialize final output `rdsetl.rds_tmp`.

```mermaid
flowchart LR
  P0["dw_ca.dws_disty_brpt_vend_comb_mtd"]
  P1["dim_ca.dim_pub_vendor_info"]
  P2["dim_ca.dim_pub_vend_location_view"]
  P3["dim_ca.dim_pub_terms_file_view"]
  P4["ods_ca.ods_cis_corp_vend_payments"]
  P5["dw_ca.dws_disty_ap_vend_aging_df"]
  P6["dw_ca.dwd_disty_pm_report_goal"]
  P7["dw_ca.dwd_disty_ap_ap_hold"]
  T0["temp_rds_sales_qtr_ca1545"]
  T1["rds_sales_qtr_ca1545"]
  T2["rds_vend_ca1545"]
  T3["rds_actual_pay_ca1545"]
  T4["rds_ap_total_ca1545"]
  T5["rds_goal_ca1545"]
  T6["rds_sales_ca1545"]
  T7["TEMP_DATE"]
  T8["TEMP_QTR_DATE"]
  T9["rds_rec_pool_ca1545"]
  O0["rdsetl.rds_tmp"]
  O1["rdsetl.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_ca.dws_disty_brpt_vend_comb_mtd` | Permanent warehouse source |
| `dim_ca.dim_pub_vendor_info` | Permanent warehouse source |
| `dim_ca.dim_pub_vend_location_view` | Permanent warehouse source |
| `dim_ca.dim_pub_terms_file_view` | Permanent warehouse source |
| `ods_ca.ods_cis_corp_vend_payments` | Permanent warehouse source |
| `dw_ca.dws_disty_ap_vend_aging_df` | Permanent warehouse source |
| `dw_ca.dwd_disty_pm_report_goal` | Permanent warehouse source |
| `dw_ca.dwd_disty_ap_ap_hold` | Permanent warehouse source |
| `dw_ca.dwd_disty_ap_vend_doc_df` | Permanent warehouse source |
| `dim_ca.dim_pub_date` | Permanent warehouse source |
| `temp_rds_sales_qtr_ca1545` | Report staging / temp table |
| `rds_sales_qtr_ca1545` | Report staging / temp table |
| `rds_vend_ca1545` | Report staging / temp table |
| `rds_actual_pay_ca1545` | Report staging / temp table |
| `rds_ap_total_ca1545` | Report staging / temp table |
| `rds_goal_ca1545` | Report staging / temp table |
| `rds_sales_ca1545` | Report staging / temp table |
| `TEMP_DATE` | Report staging / temp table |
| `TEMP_QTR_DATE` | Report staging / temp table |
| `rds_rec_pool_ca1545` | Report staging / temp table |
| `rds_qtd_pool_ca1545` | Report staging / temp table |
| `rds_rec_ca1545` | Report staging / temp table |
| `rds_rec_qtd_ca1545` | Report staging / temp table |
| `rds_open_pay_ca1545` | Report staging / temp table |
| `rds_open_spay_ca1545` | Report staging / temp table |
| `rds_open_po1_ca1545` | Report staging / temp table |
| `rds_open_po1_ca1545_filtered` | Report staging / temp table |
| `rds_open_po_ca1545` | Report staging / temp table |
| `rds_day_ca1545` | Report staging / temp table |
| `rds_cogs_left_ca1545` | Report staging / temp table |
| `rds_forecast_pay_ca1545` | Report staging / temp table |
| `rds_merge_ca1545` | Report staging / temp table |
| `rds_ca1545_final` | Report staging / temp table |
| `rdsetl.rds_tmp` | Report staging / temp table |
| `rdsetl.rds_tmp_body` | Report staging / temp table |
| `rdsetl.rds_tmp` | Final report output object |
| `rdsetl.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `dw_ca.dws_disty_brpt_vend_comb_mtd`, `dim_ca.dim_pub_vendor_info`, `dim_ca.dim_pub_vend_location_view`, `dim_ca.dim_pub_terms_file_view`, `ods_ca.ods_cis_corp_vend_payments`, `dw_ca.dws_disty_ap_vend_aging_df`, `dw_ca.dwd_disty_pm_report_goal`, `dw_ca.dwd_disty_ap_ap_hold`, `dw_ca.dwd_disty_ap_vend_doc_df`, `dim_ca.dim_pub_date`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `temp_rds_sales_qtr_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `rds_sales_qtr_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `rds_vend_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `rds_actual_pay_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `rds_ap_total_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `rds_goal_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `rds_sales_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `TEMP_DATE`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `TEMP_QTR_DATE`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `rds_rec_pool_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- `rds_qtd_pool_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 13 -- `rds_rec_ca1545`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 14 -- finalize `rdsetl.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 15 -- finalize `rdsetl.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no_str` | `CAST(vend_no AS VARCHAR(100))` | `vend_no` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:582` |
| `vend_name_str` | `CAST(vend_name AS VARCHAR(100))` | `vend_name` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:583` |
| `disc_percent_str` | `CAST(disc_percent AS VARCHAR(100))` | `disc_percent` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:584` |
| `disc_days_str` | `CAST(disc_days AS VARCHAR(100))` | `disc_days` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:585` |
| `net_days_str` | `CAST(net_days AS VARCHAR(100))` | `net_days` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:586` |
| `forecast_payment_str` | `TO_CHAR(forecast_payment, '999,999,999,999.99')` | `TO_CHAR`, `forecast_payment` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:588` |
| `actual_payment_str` | `TO_CHAR(ifnull(actual_payment,0.00), '999,999,999,999.99')` | `TO_CHAR`, `actual_payment` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | coalesce | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:589` |
| `payment_due_str` | `TO_CHAR(payment_due, '999,999,999,999.99')` | `TO_CHAR`, `payment_due` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:590` |
| `day_str` | `CAST(Day AS VARCHAR(100))` | `Day` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:592` |
| `days_str` | `CAST(Days AS VARCHAR(100))` | `Days` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:593` |
| `vend_type_str` | `CAST(vend_type AS VARCHAR(100))` | `vend_type` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | cast | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:594` |
| `AP_Total_str` | `TO_CHAR(AP_Total, '999,999,999,999.99')` | `TO_CHAR`, `AP_Total` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:596` |
| `Forecast_AP_Total_str` | `TO_CHAR(Forecast_AP_Total, '999,999,999,999.99')` | `TO_CHAR`, `Forecast_AP_Total` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:597` |
| `sales_goal_str` | `TO_CHAR(sales_goal, '999,999,999,999.99')` | `TO_CHAR`, `sales_goal` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:598` |
| `MTD_sales_str` | `TO_CHAR(MTD_sales, '999,999,999,999.99')` | `TO_CHAR`, `MTD_sales` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:599` |
| `QTD_sales_str` | `TO_CHAR(QTD_sales, '999,999,999,999.99')` | `TO_CHAR`, `QTD_sales` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:600` |
| `COGS_goal_str` | `TO_CHAR(COGS_goal, '999,999,999,999.99')` | `TO_CHAR`, `COGS_goal` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:602` |
| `Daily_COGS_goal_str` | `TO_CHAR(Daily_COGS_goal, '999,999,999,999.99')` | `TO_CHAR`, `Daily_COGS_goal` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:603` |
| `MTD_COGS_str` | `TO_CHAR(MTD_COGS, '999,999,999,999.99')` | `TO_CHAR`, `MTD_COGS` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:604` |
| `QTD_COGS_str` | `TO_CHAR(QTD_COGS, '999,999,999,999.99')` | `TO_CHAR`, `QTD_COGS` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:605` |
| `MTD_receipts_str` | `TO_CHAR(MTD_receipts, '999,999,999,999.99')` | `TO_CHAR`, `MTD_receipts` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:607` |
| `QTD_receipts_str` | `TO_CHAR(QTD_receipts, '999,999,999,999.99')` | `TO_CHAR`, `QTD_receipts` | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | udf | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:608` |
| `14` | `14` | — | `rds_merge_ca1545`, `rds_ca1545_final`, `rdsetl.rds_tmp` | passthrough | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql:425` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `rdsetl.rds_tmp` (Vertica) | on-demand | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` | no |

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
-- See full script: source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_ca.dws_disty_brpt_vend_comb_mtd` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dim_ca.dim_pub_vendor_info` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dim_ca.dim_pub_vend_location_view` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dim_ca.dim_pub_terms_file_view` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `ods_ca.ods_cis_corp_vend_payments` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dw_ca.dws_disty_ap_vend_aging_df` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dw_ca.dwd_disty_pm_report_goal` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dw_ca.dwd_disty_ap_ap_hold` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dw_ca.dwd_disty_ap_vend_doc_df` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |
| `dim_ca.dim_pub_date` | FROM/JOIN source | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `rdsetl.rds_tmp` final report result | `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/vertica_ap/etl/ap_forecast_payment_receipt_open_po_rds_1545.sql` (source_kind: rds_report_sql).*
