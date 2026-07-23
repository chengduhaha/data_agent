# load_ap_vend_doc

- artifact_type: etl_table
- artifact_id: ${literal_target_db}.dwd_disty_ap_vend_doc_df
- domain: ap
- one_line_purpose: This job builds the daily accounts payable vendor document snapshot. It keeps open vendor documents and documents that closed after the run date, then adjusts applied amounts for payments posted after the snapshot date.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `${literal_target_db}.dwd_disty_ap_vend_doc_df`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per vendor document and company in a `date_flag` partition
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository


### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `${literal_target_db}.dwd_disty_ap_vend_doc_df` | ETL target / intermediate per evidence script |
| Vertica | pending | `${literal_target_db}.dwd_disty_ap_vend_doc_df` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `${literal_target_db}.dwd_disty_ap_vend_doc_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "ap load_ap_vend_doc schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `${literal_source_db}.ods_cis_corp_vend_doc` | Source for vendor document header/detail rows. |
| 2 | `${literal_source_db}.ods_cis_corp_vend_applications` | Source for later payment and discount applications. |
| 3 | `${source_db}.ods_cis_corp_no_ctrl` | Source for adjustment vendor number control values. |
| 4 | `temp_ap_det_dec`, `temp_va_dec`, `temp_ap_det_dec2`, `temp_adj_vd`, `temp_doc_ori_vd` | Temporary processing objects. |
| 5 | `${literal_target_db}.dwd_disty_ap_vend_doc_df` | Target daily AP vendor document table. |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This job builds the daily accounts payable vendor document snapshot. It keeps open vendor documents and documents that closed after the run date, then adjusts applied amounts for payments posted after the snapshot date.

It helps AP reporting, vendor aging, and downstream finance consumers understand outstanding vendor document balances by company and date.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (ap)** | Uses `${literal_target_db}.dwd_disty_ap_vend_doc_df` for operational and reporting workflows documented below. |

### Fact key resolution
- Natural key: Not documented in repository
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** Not documented in repository
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/ap/metric-index.md`](../../source/contracts/ap/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/ap/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py` |

### Key filters and ETL business logic
### Sources and joins
The job reads vendor documents from `${literal_source_db}.ods_cis_corp_vend_doc` for two populations: documents closed on or after the run date and open documents with entry or document dates before the run date. It aggregates `${literal_source_db}.ods_cis_corp_vend_applications` by `doc_no` for applications entered on or after the run date, then left joins those totals back to document rows to reverse later applied amounts from the snapshot.

Adjustment vendor handling is driven by `${source_db}.ods_cis_corp_no_ctrl`, filtered to `site = 16` and `kind = 'AP_Adjustment_Vend_NO'`. Documents whose vendor number is in that control list are joined back to vendor document details to derive `from_vend_no` from the `vend_inv_no` pattern.

### Filters and business rules
The source extract is restricted to configured companies through `company_no in (${literal_company_no})`. Closed documents must have `entry_datetime < '${literal_run_date}'`, `doc_close_date >= '${literal_run_date}'`, and a non-null `doc_close_date`; open documents require `doc_close_date IS NULL` and `NVL(entry_datetime, doc_date) < '${literal_run_date}'`.

Payment applications entered after the snapshot date reduce `new_applied` and `new_usd_applied`, so the target reflects the document state as of the run date rather than the current fully applied state.

### Grain and deduplication
The output grain is one row per vendor document and company in a `date_flag` partition. No explicit rank-based deduplication is present; rows are shaped by the source document records and joined payment/application summaries.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `doc_no` | Vendor document identifier. | Selected from the vendor document source and used as the join key. |
| `new_applied` | Snapshot-applied amount. | Current applied amount minus payments entered after the run date when later applications exist. |
| `new_usd_applied` | Snapshot-applied amount in USD. | Current USD applied amount minus later USD payment and discount applications. |
| `from_vend_no` | Original vendor for adjustment documents. | Parsed from `vend_inv_no` for adjustment vendor records matching the `/DOC#` pattern. |
| `date_flag` | Snapshot partition date. | Set from `${literal_date_flag}`. |
| `company_no` | Company partition. | Carried from the vendor document source. |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM ${literal_target_db}.dwd_disty_ap_vend_doc_df
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
The job reads vendor documents from `${literal_source_db}.ods_cis_corp_vend_doc` for two populations: documents closed on or after the run date and open documents with entry or document dates before the run date. It aggregates `${literal_source_db}.ods_cis_corp_vend_applications` by `doc_no` for applications entered on or after the run date, then left joins those totals back to document rows to reverse later applied amounts from the snapshot.

Adjustment vendor handling is driven by `${source_db}.ods_cis_corp_no_ctrl`, filtered to `site = 16` and `kind = 'AP_Adjustment_Vend_NO'`. Documents whose vendor number is in that control list are joined back to vendor document details to derive `from_vend_no` from the `vend_inv_no` pattern.

### Filters and business rules
The source extract is restricted to configured companies through `company_no in (${literal_company_no})`. Closed documents must have `entry_datetime < '${literal_run_date}'`, `doc_close_date >= '${literal_run_date}'`, and a non-null `doc_close_date`; open documents require `doc_close_date IS NULL` and `NVL(entry_datetime, doc_date) < '${literal_run_date}'`.

Payment applications entered after the snapshot date reduce `new_applied` and `new_usd_applied`, so the target reflects the document state as of the run date rather than the current fully applied state.

### Grain and deduplication
The output grain is one row per vendor document and company in a `date_flag` partition. No explicit rank-based deduplication is present; rows are shaped by the source document records and joined payment/application summaries.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `doc_no` | Vendor document identifier. | Selected from the vendor document source and used as the join key. |
| `new_applied` | Snapshot-applied amount. | Current applied amount minus payments entered after the run date when later applications exist. |
| `new_usd_applied` | Snapshot-applied amount in USD. | Current USD applied amount minus later USD payment and discount applications. |
| `from_vend_no` | Original vendor for adjustment documents. | Parsed from `vend_inv_no` for adjustment vendor records matching the `/DOC#` pattern. |
| `date_flag` | Snapshot partition date. | Set from `${literal_date_flag}`. |
| `company_no` | Company partition. | Carried from the vendor document source. |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[load_ap_vend_doc]
  JOB --> TGT[${literal_target_db}.dwd_disty_ap_vend_doc_df]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `${literal_source_db}.ods_cis_corp_vend_doc` | Source for vendor document header/detail rows. |
| 2 | `${literal_source_db}.ods_cis_corp_vend_applications` | Source for later payment and discount applications. |
| 3 | `${source_db}.ods_cis_corp_no_ctrl` | Source for adjustment vendor number control values. |
| 4 | `temp_ap_det_dec`, `temp_va_dec`, `temp_ap_det_dec2`, `temp_adj_vd`, `temp_doc_ori_vd` | Temporary processing objects. |
| 5 | `${literal_target_db}.dwd_disty_ap_vend_doc_df` | Target daily AP vendor document table. |

### Step-by-step logic
### Sources and joins
The job reads vendor documents from `${literal_source_db}.ods_cis_corp_vend_doc` for two populations: documents closed on or after the run date and open documents with entry or document dates before the run date. It aggregates `${literal_source_db}.ods_cis_corp_vend_applications` by `doc_no` for applications entered on or after the run date, then left joins those totals back to document rows to reverse later applied amounts from the snapshot.

Adjustment vendor handling is driven by `${source_db}.ods_cis_corp_no_ctrl`, filtered to `site = 16` and `kind = 'AP_Adjustment_Vend_NO'`. Documents whose vendor number is in that control list are joined back to vendor document details to derive `from_vend_no` from the `vend_inv_no` pattern.

### Filters and business rules
The source extract is restricted to configured companies through `company_no in (${literal_company_no})`. Closed documents must have `entry_datetime < '${literal_run_date}'`, `doc_close_date >= '${literal_run_date}'`, and a non-null `doc_close_date`; open documents require `doc_close_date IS NULL` and `NVL(entry_datetime, doc_date) < '${literal_run_date}'`.

Payment applications entered after the snapshot date reduce `new_applied` and `new_usd_applied`, so the target reflects the document state as of the run date rather than the current fully applied state.

### Grain and deduplication
The output grain is one row per vendor document and company in a `date_flag` partition. No explicit rank-based deduplication is present; rows are shaped by the source document records and joined payment/application summaries.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `doc_no` | Vendor document identifier. | Selected from the vendor document source and used as the join key. |
| `new_applied` | Snapshot-applied amount. | Current applied amount minus payments entered after the run date when later applications exist. |
| `new_usd_applied` | Snapshot-applied amount in USD. | Current USD applied amount minus later USD payment and discount applications. |
| `from_vend_no` | Original vendor for adjustment documents. | Parsed from `vend_inv_no` for adjustment vendor records matching the `/DOC#` pattern. |
| `date_flag` | Snapshot partition date. | Set from `${literal_date_flag}`. |
| `company_no` | Company partition. | Carried from the vendor document source. |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `temp_ap_det_dec` | `${literal_source_db}.ods_cis_corp_vend_applications` | many:1 | `t.doc_no = va.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:51) |
| `temp_ap_det_dec` | `temp_va_dec` | many:1 | `ad.doc_no = va.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:64) |
| `temp_ap_det_dec2` | `${literal_source_db}.ods_cis_corp_vend_doc` | many:1 | `a.doc_no = b.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:100) |
| `${literal_source_db}.ods_cis_corp_vend_doc` | `temp_adj_vd` | many:1 | `b.vend_no = c.vend_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:100) |
| `temp_ap_det_dec2` | `temp_doc_ori_vd` | many:1 | `a.doc_no = c.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:116) |

`source/ref/ap/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `doc_no` | `b.doc_no` | `doc_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:106` |
| `H` | `'H'` | `H` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | literal | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:119` |
| `doc_amt` | `b.doc_amt` | `doc_amt` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:120` |
| `doc_date` | `b.doc_date` | `doc_date` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:121` |
| `vend_no` | `b.vend_no` | `vend_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:108` |
| `loc_no` | `b.loc_no` | `loc_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:123` |
| `inv_disc_date` | `b.inv_disc_date` | `inv_disc_date` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:124` |
| `inv_disc_percent` | `b.inv_disc_percent` | `inv_disc_percent` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:125` |
| `inv_disc_amt` | `b.inv_disc_amt` | `inv_disc_amt` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:126` |
| `doc_type` | `b.doc_type` | `doc_type` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:127` |
| `entry_datetime` | `b.entry_datetime` | `entry_datetime` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:128` |
| `entry_id` | `b.entry_id` | `entry_id` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:129` |
| `doc_close_date` | `a.doc_close_date` | `doc_close_date` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:130` |
| `new_applied` | `a.new_applied` | `new_applied` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:131` |
| `doc_due_date` | `b.doc_due_date` | `doc_due_date` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:132` |
| `doc_ref` | `b.doc_ref` | `doc_ref` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:133` |
| `doc_terms` | `b.doc_terms` | `doc_terms` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:134` |
| `ap_hold_hold` | `b.ap_hold_hold` | `ap_hold_hold` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:135` |
| `check_hold` | `b.check_hold` | `check_hold` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:136` |
| `vend_inv_no` | `b.vend_inv_no` | `vend_inv_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:103` |
| `reason_id` | `b.reason_id` | `reason_id` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:138` |
| `vend_doc` | `b.vend_doc` | `vend_doc` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:139` |
| `usd_doc_amt` | `b.usd_doc_amt` | `usd_doc_amt` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:140` |
| `usd_disc_amt` | `b.usd_disc_amt` | `usd_disc_amt` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:141` |
| `new_usd_applied` | `a.new_usd_applied` | `new_usd_applied` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:142` |
| `etl_timestamp` | `'${etl_timestamp}'` | `etl_timestamp` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | literal | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:143` |
| `initiator_id` | `b.initiator_id` | `initiator_id` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:144` |
| `approver_id` | `b.approver_id` | `approver_id` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:145` |
| `exp_po_no` | `b.exp_po_no` | `exp_po_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:146` |
| `doc_pay_date` | `b.doc_pay_date` | `doc_pay_date` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:147` |
| `disc_taken` | `b.disc_taken` | `disc_taken` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:148` |
| `usd_disc_taken` | `b.usd_disc_taken` | `usd_disc_taken` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:149` |
| `doc_comments` | `b.doc_comments` | `doc_comments` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:150` |
| `from_vend_no` | `c.from_vend_no` | `from_vend_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:151` |
| `literal_date_flag` | `to_date('${literal_date_flag}')` | `literal_date_flag` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | udf | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:152` |
| `company_no` | `b.company_no` | `company_no` | `temp_ap_det_dec2`, `${literal_source_db}.ods_cis_corp_vend_doc`, `temp_doc_ori_vd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:153` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM ${literal_target_db}.dwd_disty_ap_vend_doc_df WHERE partition_col = '${partition_value}' GROUP BY 1;
-- 2) metric sum by dimension (top N) - replace metric/dim from L2
-- 3) grain duplicate check on natural keys
```


### Caveats for interpretation
None identified in repository

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Not in Vertica** | *See script lineage* | *No Vertica mapping identified in repository* | - | *Add flow evidence when found* | no |

No queryable Vertica table has been confirmed for this script from current repository evidence.

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | unknown |
| scan_risk_tier | high |

---

## L6 Access and Consumption

### Primary consumers and use cases
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `${literal_source_db}.ods_cis_corp_vend_doc` | Reads source AP vendor documents and joins document attributes for the target insert. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:20`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:155` |
| `${literal_source_db}.ods_cis_corp_vend_applications` | Aggregates payment and discount applications by `doc_no`. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:56` |
| `${source_db}.ods_cis_corp_no_ctrl` | Gets AP adjustment vendor numbers. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:96` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `lo

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM ${literal_target_db}.dwd_disty_ap_vend_doc_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `${literal_source_db}.ods_cis_corp_vend_doc` | Reads source AP vendor documents and joins document attributes for the target insert. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:20`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:155` |
| `${literal_source_db}.ods_cis_corp_vend_applications` | Aggregates payment and discount applications by `doc_no`. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:56` |
| `${source_db}.ods_cis_corp_no_ctrl` | Gets AP adjustment vendor numbers. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:96` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `load_ap_vdah_lines` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:207` |
| `sync_dwd_disty_ap_vend_doc_df` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:234` |
| `hive2starrocks-dwd_disty_ap_vend_doc_df` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:324` |
| `${target_db}.dwd_disty_ap_vend_doc_df` read by `load_ap_vdah_lines.py` | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:105` |

### Operational detail (verified)
- The AP aging flow runs this script as a `livy32` Python job named `load_ap_vend_doc`. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:148`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:160`.
- The target partition is dropped before insert overwrite. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:115`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py:116`.

### Not documented in repository
- Owner, SLA, and schedule are not documented in the reviewed files.
- Physical table DDL and partition definitions beyond the script's `date_flag` and `company_no` write are not documented in the reviewed files.

### Related scripts (verified)
- `load_ap_vdah_lines.py` — consumes `${target_db}.dwd_disty_ap_vend_doc_df` — `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:105`
- `load_ap_vend_aging.py` — runs after `load_ap_vdah_lines` in the AP aging flow — `source/etl/flows/data_service/ap/ap_aging_load_us.flow:214`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:229`

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vend_doc.py`.*
