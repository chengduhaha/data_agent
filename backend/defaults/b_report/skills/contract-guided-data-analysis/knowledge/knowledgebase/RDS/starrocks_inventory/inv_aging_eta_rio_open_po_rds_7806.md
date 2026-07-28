# REPORT: Drop existing tables if they exist (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_inventory.inv_aging_eta_rio_open_po_rds_7806
- domain: RDS/starrocks_inventory
- one_line_purpose: RDS inventory report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_inventory/inv_aging_eta_rio_open_po_rds_7806.md
- ref_evidence: source/ref/RDS/starrocks_inventory/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `inventory` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_inventory` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 34 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_inventory inv_aging_eta_rio_open_po_rds_7806" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_us.ods_cis_corp_inv_qty_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_vend_master_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `dw_us.dwd_disty_inv_aging_df` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_order_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_order_eta_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_order_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_rio_request_header_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `ods_us.ods_cis_corp_rio_req_detail_rt` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **upstream:** `dw_us.dws_disty_pur_ips_runrate_1w` — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `inventory` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_inventory/special_logic.txt` — do not invent.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **RDS developers** | Reuse proven report patterns for `inventory` |
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

- **Source:** [source/contracts/rds/starrocks_inventory/metric-index.md](../../../../source/contracts/rds/starrocks_inventory/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |

### Key filters and ETL business logic
- `a.sku_no = c.sku_no AND b.vend_no = c.vend_no AND c.vend_no IN (13439, 50633) AND inv_type IN (1, 300)`
- `a.sku_no = b.sku_no and b.inv_type in (1, 300) and b.view_level = 'IT_PART' and b.date_flag = date_add(current_date(),interval -1 day)`
- `rds_tmp.sku_no = a.sku_no ; -- Create table for order ETA details (location 310) CREATE TABLE tempdb.rds_oo_7806 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS SELECT uuid_numeric() as…`
- `rds_tmp.sku_no = b.sku_no; -- Create table for order ETA details (location 312) CREATE TABLE tempdb.rds_oo312_7806 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS SELECT uuid_numeric() …`
- `rds_tmp.sku_no = b.sku_no; -- Create RIO inventory table CREATE TABLE tempdb.rds_inv_rio_7806 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS SELECT uuid_numeric() as id , c.sku_no, loc…`
- `rds_tmp.sku_no = b.sku_no; -- Update alloc_qty UPDATE tempdb.rds_tmp SET alloc_qty = IFNULL(total_Alloc_qty - IFNULL(rio_qty, 0), total_Alloc_qty); -- Delete rows with zero quantit…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (10 objects).
2. Build staging temps (10 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_us.ods_cis_corp_inv_qty_rt"]
  P1["ods_us.ods_cis_corp_vend_master_rt"]
  P2["ods_us.ods_cis_corp_part_master_rt"]
  P3["dw_us.dwd_disty_inv_aging_df"]
  P4["ods_us.ods_cis_corp_order_header_rt"]
  P5["ods_us.ods_cis_corp_order_eta_detail_rt"]
  P6["ods_us.ods_cis_corp_order_detail_rt"]
  P7["ods_us.ods_cis_corp_rio_request_header_rt"]
  T0["tempdb.rds_tmp"]
  T1["tempdb.t_inv_aging_7806"]
  T2["for"]
  T3["tempdb.rds_oo_7806"]
  T4["tempdb.rds_oo312_7806"]
  T5["tempdb.rds_inv_rio_7806"]
  T6["tempdb.rds_rio_7806"]
  T7["tempdb.tmp_date_flag"]
  T8["tempdb.rds_rr_7806"]
  T9["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  P0 --> T0
  T9 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_us.ods_cis_corp_inv_qty_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_vend_master_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `dw_us.dwd_disty_inv_aging_df` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_eta_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_order_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_rio_request_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_rio_req_detail_rt` | Permanent warehouse source |
| `dw_us.dws_disty_pur_ips_runrate_1w` | Permanent warehouse source |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.t_inv_aging_7806` | Report staging / temp table |
| `for` | Report staging / temp table |
| `tempdb.rds_oo_7806` | Report staging / temp table |
| `tempdb.rds_oo312_7806` | Report staging / temp table |
| `tempdb.rds_inv_rio_7806` | Report staging / temp table |
| `tempdb.rds_rio_7806` | Report staging / temp table |
| `tempdb.tmp_date_flag` | Report staging / temp table |
| `tempdb.rds_rr_7806` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_us.ods_cis_corp_inv_qty_rt`, `ods_us.ods_cis_corp_vend_master_rt`, `ods_us.ods_cis_corp_part_master_rt`, `dw_us.dwd_disty_inv_aging_df`, `ods_us.ods_cis_corp_order_header_rt`, `ods_us.ods_cis_corp_order_eta_detail_rt`, `ods_us.ods_cis_corp_order_detail_rt`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `dw_us.dws_disty_pur_ips_runrate_1w`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.t_inv_aging_7806`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `for`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.rds_oo_7806`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.rds_oo312_7806`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.rds_inv_rio_7806`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- `tempdb.rds_rio_7806`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 9 -- `tempdb.tmp_date_flag`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 10 -- `tempdb.rds_rr_7806`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 11 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 12 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 13 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `id` | `uuid_numeric()` | `uuid_numeric` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | udf | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:16` |
| `sku_no` | `c.sku_no` | `sku_no` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:17` |
| `vend_no` | `b.vend_no` | `vend_no` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:18` |
| `part_no` | `c.part_no` | `part_no` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:19` |
| `mfg_partno` | `c.mfg_partno` | `mfg_partno` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:20` |
| `abc_code` | `c.abc_code` | `abc_code` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:21` |
| `mar_comment` | `c.mar_comment` | `mar_comment` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | passthrough | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:22` |
| `base_cost` | `c.po_cost` | `po_cost` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | rename | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:23` |
| `runrate13w` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `runrate52w` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OH` | `SUM(on_hand_qty)` | `on_hand_qty` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:26` |
| `IT` | `SUM(intran_in)` | `intran_in` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:27` |
| `BO` | `SUM(bo_qty)` | `bo_qty` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:28` |
| `total_Alloc_qty` | `SUM(alloc_qty)` | `alloc_qty` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:29` |
| `rio_qty` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `alloc_qty` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO` | `SUM(on_order_qty)` | `on_order_qty` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | agg | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:32` |
| `OO_DEX` | `SUM(CASE WHEN loc_no = 310 THEN on_order_qty ELSE 0 END)` | `loc_no`, `on_order_qty` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | case | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:33` |
| `OO_DEX_curr_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_DEX_second_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_DEX_third_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_DEX_fourth_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_DEX_fifth_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_DEX_sixth_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_LOC312` | `SUM(CASE WHEN loc_no = 312 THEN on_order_qty ELSE 0 END)` | `loc_no`, `on_order_qty` | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | case | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:40` |
| `OO_LOC312_curr_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_LOC312_second_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_LOC312_third_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_LOC312_fourth_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_LOC312_fifth_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `OO_LOC312_sixth_mth` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `age61_90` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `age90plus` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |
| `age180plus` | `CAST(NULL AS INT)` | — | `ods_us.ods_cis_corp_inv_qty_rt`, `tempdb.rds_tmp`, `tempdb.t_inv_aging_7806`, `ods_us.ods_cis_corp_order_header_rt`, `tempdb.rds_oo_7806`, `tempdb.rds_oo312_7806`, `ods_us.ods_cis_corp_rio_request_header_rt`, `ods_us.ods_cis_corp_rio_req_detail_rt`, `tempdb.rds_inv_rio_7806`, `tempdb.rds_rio_7806`, `dw_us.dws_disty_pur_ips_runrate_1w`, `tmp_date_flag` | cast | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:24` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` | no |

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
| Knowledgebase / agents | Lineage and filter documentation for `inventory` |

### Representative query patterns
<!-- sql-artifact snippet_type: routing_certified -->
```sql
-- See full script: source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_us.ods_cis_corp_inv_qty_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_vend_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `dw_us.dwd_disty_inv_aging_df` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_order_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_order_eta_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_order_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_rio_request_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `ods_us.ods_cis_corp_rio_req_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |
| `dw_us.dws_disty_pur_ips_runrate_1w` | FROM/JOIN source | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` (source_kind: rds_report_sql).*
