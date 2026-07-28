# REPORT: RDS cpo report SQL — cpo current history sparef eu contact rds 10106 (`tempdb.rds_tmp`)

- artifact_type: rds_report
- artifact_id: rds.starrocks_cpo.cpo_current_history_sparef_eu_contact_rds_10106
- domain: RDS/starrocks_cpo
- one_line_purpose: RDS cpo report SQL on StarRocks producing `tempdb.rds_tmp`
- layer_type: REPORT
- source_kind: rds_report_sql
- evidence_source: source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql
- knowledgebase_path: target/knowledgebase/RDS/starrocks_cpo/cpo_current_history_sparef_eu_contact_rds_10106.md
- ref_evidence: source/ref/RDS/starrocks_cpo/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `tempdb.rds_tmp`
- **Layer type:** REPORT
- **Canonical / derived:** Report SQL output (temporary / session result), not a warehouse load target
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (infer from final SELECT in evidence SQL)
- **Scope:** `cpo` domain report on StarRocks
- **Partition:** Not documented in repository — report SQL uses session/date filters (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| StarRocks | yes | `tempdb.rds_tmp` | Evidence SQL pack `starrocks_cpo` |
| Vertica | unknown | — | Sister pack may exist under the other engine prefix |

### Physical schema reference

Pointer block only — report outputs are session temps; no warehouse L1 catalog unless separately seeded.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | Not documented in repository (report temp output) |
| **entity_id** | `tempdb.rds_tmp` |
| **l1_catalog_seed** | Not documented in repository |
| **column_count** | 28 |
| **partition_keys** | Not documented in repository |
| **ddl_source** | Report SQL — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "RDS starrocks_cpo cpo_current_history_sparef_eu_contact_rds_10106" --intent find_table_schema` |

### Lineage
- **upstream:** `ods_us.ods_cis_corp_cpo_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_part_master_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_cpo_header_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_spl_open_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_cpo_profile_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_dw_vend_pl_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_history_cpo_detail_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_history_cpo_header_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_history_cpo_profile_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **upstream:** `ods_us.ods_cis_corp_cust_xref_rt` — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **downstream:** `tempdb.rds_tmp` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`
- **downstream:** `tempdb.rds_tmp_body` (report output) — `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | On-demand report SQL (not Azkaban warehouse load) |
| Schedule | Not documented in repository |
| Parameters | Session / report parameters in SQL (if any) |

---

## L2 Declarative Knowledge

### Business purpose
RDS `cpo` curated example report SQL for StarRocks. Documents how the report stages data into temporary tables and projects the final result set used by RDS tooling. Business filters and measure formulas must be taken from the evidence SQL and `source/ref/RDS/starrocks_cpo/special_logic.txt` — do not invent.

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

- **Source:** [source/contracts/rds/starrocks_cpo/metric-index.md](../../../../source/contracts/rds/starrocks_cpo/metric-index.md)
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
| See SQL JOIN list | Not documented in repository | Dimension enrichment in report | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |

### Key filters and ETL business logic
- `b.vend_no=70425 and a.cpo_entry_datetime >= DATE_ADD(CURRENT_DATE(),INTERVAL -7 DAY) and a.cpo_delete_datetime is null`
- `b.vend_no=70425 and a.cpo_entry_datetime >=DATE_ADD(CURRENT_DATE(),INTERVAL -7 DAY) and a.cpo_delete_datetime is null ; create table tempdb.rds_tmp PRIMARY KEY(id) DISTRIBUTED BY H…`
- `tempdb.rds_tmp.addr_no =a.addr_no and a.contact_no = e.contact_no) where tempdb.rds_tmp.addr_no is not null ; update tempdb.rds_tmp set reseller_email_address = (select e.email_add…`
- `a.qute_no=b.cpo_id and b.cpo_line_seq = 0 ; update tempdb.rds_tmp set end_user_name = (select b.eu_company_name from tempdb.t3_10106 b where tempdb.rds_tmp.qute_no=b.qute_no), end_…`

### Standard time-filter SQL
<!-- sql-artifact snippet_type: time_filter_pattern -->
```sql
-- Use date predicates from source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql; do not invent partition values.
```

### End-to-end flow
1. Read permanent sources (20 objects).
2. Build staging temps (6 objects).
3. Materialize final output `tempdb.rds_tmp`.

```mermaid
flowchart LR
  P0["ods_us.ods_cis_corp_cpo_detail_rt"]
  P1["ods_us.ods_cis_corp_part_master_rt"]
  P2["ods_us.ods_cis_corp_cpo_header_rt"]
  P3["ods_us.ods_cis_corp_spl_open_rt"]
  P4["ods_us.ods_cis_corp_cpo_profile_rt"]
  P5["ods_us.ods_cis_corp_dw_vend_pl_rt"]
  P6["ods_us.ods_cis_corp_history_cpo_detail_rt"]
  P7["ods_us.ods_cis_corp_history_cpo_header_rt"]
  T0["tempdb.temp_10106"]
  T1["tempdb.rds_tmp"]
  T2["tempdb.t1_10106"]
  T3["tempdb.t2_10106"]
  T4["tempdb.t3_10106"]
  T5["tempdb.rds_tmp_body"]
  O0["tempdb.rds_tmp"]
  O1["tempdb.rds_tmp_body"]
  P0 --> T0
  T5 --> O0
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_us.ods_cis_corp_cpo_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_part_master_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_spl_open_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_profile_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_dw_vend_pl_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_detail_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_profile_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cust_xref_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_customer_header_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_territory_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_manager_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_employee_contacts_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_address_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_addr_xref_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_contact_xref_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_contacts_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_cpo_eu_common_rt` | Permanent warehouse source |
| `ods_us.ods_cis_corp_history_cpo_eu_common_rt` | Permanent warehouse source |
| `tempdb.temp_10106` | Report staging / temp table |
| `tempdb.rds_tmp` | Report staging / temp table |
| `tempdb.t1_10106` | Report staging / temp table |
| `tempdb.t2_10106` | Report staging / temp table |
| `tempdb.t3_10106` | Report staging / temp table |
| `tempdb.rds_tmp_body` | Report staging / temp table |
| `tempdb.rds_tmp` | Final report output object |
| `tempdb.rds_tmp_body` | Final report output object |

### Step-by-step logic
#### Step 1 -- read warehouse sources
**Source:** `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `ods_us.ods_cis_corp_cust_xref_rt`, `ods_us.ods_cis_corp_customer_header_rt`, `ods_us.ods_cis_corp_territory_rt`  
**Filter:** see Key filters  
**Join keys:** Not documented in repository (see SQL)

#### Step 2 -- `tempdb.temp_10106`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 3 -- `tempdb.rds_tmp`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 4 -- `tempdb.t1_10106`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 5 -- `tempdb.t2_10106`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 6 -- `tempdb.t3_10106`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 7 -- `tempdb.rds_tmp_body`
**Source:** prior step / permanent tables  
**Filter:** report-specific predicates in SQL  
**Join keys:** Not documented in repository (see SQL)

#### Step 8 -- finalize `tempdb.rds_tmp`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A

#### Step 9 -- finalize `tempdb.rds_tmp_body`
**Source:** last staging temp  
**Filter:** final SELECT projection  
**Join keys:** N/A


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `b.vend_no` | `vend_no` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:11` |
| `cust_no` | `c.cpo_cust_no` | `cpo_cust_no` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:12` |
| `mcust_no` | `cast(null as int )` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:13` |
| `cust_name` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `qute_no` | `a.cpo_id` | `cpo_id` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:15` |
| `entry_datetime` | `a.cpo_entry_datetime` | `cpo_entry_datetime` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:16` |
| `sales_terr` | `c.cpo_sales_terr` | `cpo_sales_terr` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:17` |
| `terr_name` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `customer_po` | `c.cpo_no` | `cpo_no` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:19` |
| `sku_no` | `a.cpo_sku_no` | `cpo_sku_no` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:20` |
| `vpl_code` | `dpl.vpl_code` | `vpl_code` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:21` |
| `mfg_partno` | `b.mfg_partno` | `mfg_partno` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:22` |
| `vendor_part_descr` | `b.short_desc` | `short_desc` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:23` |
| `order_qty` | `a.cpo_line_qty` | `cpo_line_qty` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:24` |
| `base_cost` | `b.po_cost` | `po_cost` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:25` |
| `extended_base_cost` | `b.po_cost *a.cpo_line_qty` | `po_cost`, `cpo_line_qty` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | arithmetic | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:26` |
| `sales_terr_email` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `vend_spa` | `e.profile_c` | `profile_c` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | rename | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:28` |
| `addr_no` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `reseller_city` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `reseller_state` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `reseller_email_address` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `reseller_contact_name` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `probability` | `d.probability` | `probability` | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | passthrough | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:34` |
| `end_user_name` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `end_user_address` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `end_user_contact_name` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |
| `end_user_email` | `cast(null as varchar(60))` | — | `ods_us.ods_cis_corp_cpo_detail_rt`, `ods_us.ods_cis_corp_part_master_rt`, `ods_us.ods_cis_corp_cpo_header_rt`, `ods_us.ods_cis_corp_spl_open_rt`, `ods_us.ods_cis_corp_cpo_profile_rt`, `ods_us.ods_cis_corp_dw_vend_pl_rt`, `ods_us.ods_cis_corp_history_cpo_detail_rt`, `ods_us.ods_cis_corp_history_cpo_header_rt`, `ods_us.ods_cis_corp_history_cpo_profile_rt`, `tempdb.temp_10106`, `tempdb.rds_tmp`, `ods_us.ods_cis_corp_cust_xref_rt` | cast | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql:14` |

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| None identified in repository | — | — |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition/date is determined |
|------|--------|----------------------------------|
| 1 | Report SQL | Session/current_date or explicit literals in `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` — Not documented as Azkaban partition |

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
| Report output | N/A | `tempdb.rds_tmp` (StarRocks) | on-demand | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` | no |

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
-- See full script: source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql
```

### Dependencies and notes
#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_us.ods_cis_corp_cpo_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_part_master_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_cpo_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_spl_open_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_cpo_profile_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_dw_vend_pl_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_history_cpo_detail_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_history_cpo_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_history_cpo_profile_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_cust_xref_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_customer_header_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_territory_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_manager_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_employee_contacts_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |
| `ods_us.ods_cis_corp_address_rt` | FROM/JOIN source | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `tempdb.rds_tmp` final report result | `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` |

#### Not documented in repository
- Schedule, owner, SLA
- Production Azkaban flow binding for this report example

---

*Document generated from `source/contracts/rds/starrocks_cpo/etl/cpo_current_history_sparef_eu_contact_rds_10106.sql` (source_kind: rds_report_sql).*
