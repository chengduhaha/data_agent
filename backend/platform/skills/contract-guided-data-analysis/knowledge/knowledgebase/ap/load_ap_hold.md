# load_ap_hold

- artifact_type: etl_table
- artifact_id: ${literal_target_db}.dwd_disty_ap_hold_df
- domain: ap
- one_line_purpose: This job builds the daily accounts payable hold snapshot from AP receiving hold records. It keeps open AP hold activity as of the run date and removes offsetting duplicate order or receipt lines that net to zero.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/ap/data_service/ap/python/load_ap_hold.py

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `${literal_target_db}.dwd_disty_ap_hold_df`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one AP hold receipt line per `date_flag` and company, keyed by receipt and line-level fields such as `rec_no` and `rec_line_no`
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository


### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `${literal_target_db}.dwd_disty_ap_hold_df` | ETL target / intermediate per evidence script |
| Vertica | pending | `${literal_target_db}.dwd_disty_ap_hold_df` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `${literal_target_db}.dwd_disty_ap_hold_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dw_us_dwd_disty_ap_hold_df.json` |
| **column_count** | 33 |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "ap load_ap_hold schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `${literal_source_db}.ods_cis_corp_ap_hold` | Source AP hold receipt records. |
| 2 | `temp_ap_hold`, `temp_dup_order`, `temp_ap_hold2`, `temp_dup_rec`, `temp_ap_hold3` | Temporary filtering and duplicate-removal objects. |
| 3 | `${literal_target_db}.dwd_disty_ap_hold_df` | Target daily AP hold table. |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This job builds the daily accounts payable hold snapshot from AP receiving hold records. It keeps open AP hold activity as of the run date and removes offsetting duplicate order or receipt lines that net to zero.

It helps AP and operations teams review unresolved receiving or invoice-hold exposure before the vendor aging line and summary jobs allocate amounts downstream.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (ap)** | Uses `${literal_target_db}.dwd_disty_ap_hold_df` for operational and reporting workflows documented below. |

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
| P&L adjustment / measure | `ext_cost` | `ext_cost` | ext_cost at unspecified grain |
| Governed metric | `inventory_cost` | `inventory_cost` | inventory_cost at unspecified grain |
| P&L adjustment / measure | `invoice_cost` | `invoice_cost` | invoice_cost at unspecified grain |
| P&L adjustment / measure | `po_cost` | `po_cost` | po_cost at unspecified grain |
| P&L adjustment / measure | `usd_ext_cost` | `usd_ext_cost` | usd_ext_cost at unspecified grain |
| P&L adjustment / measure | `usd_po_cost` | `usd_po_cost` | usd_po_cost at unspecified grain |

### Metric serving map

**Formula authority:** [`source/contracts/ap/metric-index.md`](../../source/contracts/ap/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `ext_cost` | unspecified | `ext_cost` | Not in metric-index.md |
| `inventory_cost` | unspecified | `inventory_cost` | `source/contracts/ap/metric-index.md#inventory_cost` |
| `invoice_cost` | unspecified | `invoice_cost` | Not in metric-index.md |
| `po_cost` | unspecified | `po_cost` | Not in metric-index.md |
| `usd_ext_cost` | unspecified | `usd_ext_cost` | Not in metric-index.md |
| `usd_po_cost` | unspecified | `usd_po_cost` | Not in metric-index.md |

### etl_metrics

Formulas below are sourced from [`source/contracts/ap/metric-index.md`](../../source/contracts/ap/metric-index.md) for logical metrics present on this table.
Index formulas are canonical: this enricher copies them into KB and never overwrites `final_effective_formula_sql` in the metric-index.

#### `inventory_cost`
- **Source:** [metric-index.md](../../source/contracts/ap/metric-index.md#inventory_cost)
- **Business definition:** Compare AP exposure against inventory on hand.
```sql
Regular, RMA, and combined inventory cost attached to vendor/product rows.
```

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py` |

### Key filters and ETL business logic
### Sources and joins
The job reads `${literal_source_db}.ods_cis_corp_ap_hold` twice: once for rows with a document number and an open period crossing the run date, and once for rows without a document number that remain open. It then derives duplicate candidate groups from the temporary AP hold population.

Duplicate order groups are identified by vendor, order type, order number, order line, and document number where local and USD extended values net close to zero. Duplicate receipt pairs for order type `27` are identified by matching vendor, order, document, date, and offsetting positive/negative costs.

### Filters and business rules
Rows with `doc_no IS NOT NULL` must have `rec_close_date >= '${literal_run_date}'`, `rec_datetime < '${literal_run_date}'`, and `gl_acct_no IS NULL`. Rows with `doc_no IS NULL` must have `rec_close_date IS NULL`, `rec_datetime < '${literal_run_date}'`, and `gl_acct_no IS NULL`. Both extracts are limited to configured companies.

The job removes duplicate order groups whose summed local and USD costs are within `0.005`, and removes both sides of qualifying offsetting receipt pairs for order type `27`.

### Grain and deduplication
The output grain is one AP hold receipt line per `date_flag` and company, keyed by receipt and line-level fields such as `rec_no` and `rec_line_no`. Deduplication is implemented through exclusion tables for net-zero order groups and offsetting receipt pairs.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `rec_no` | Receipt number. | Carried from AP hold source rows that survive duplicate filtering. |
| `rec_line_no` | Receipt line number. | Carried from AP hold source rows. |
| `vend_no` | Vendor associated with the held receipt. | Carried from AP hold source rows. |
| `po_cost` | Purchase order unit cost. | Carried from AP hold source rows and used for duplicate cost checks. |
| `usd_po_cost` | USD purchase order unit cost. | Nulls are converted to zero before target insert. |
| `snap_date` | ETL snapshot timestamp. | Set from `${etl_timestamp}` during insert. |
| `date_flag` | Snapshot partition date. | Set from `${literal_date_flag}`. |
| `company_no` | Company partition. | Carried from the AP hold source. |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM ${literal_target_db}.dwd_disty_ap_hold_df
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
The job reads `${literal_source_db}.ods_cis_corp_ap_hold` twice: once for rows with a document number and an open period crossing the run date, and once for rows without a document number that remain open. It then derives duplicate candidate groups from the temporary AP hold population.

Duplicate order groups are identified by vendor, order type, order number, order line, and document number where local and USD extended values net close to zero. Duplicate receipt pairs for order type `27` are identified by matching vendor, order, document, date, and offsetting positive/negative costs.

### Filters and business rules
Rows with `doc_no IS NOT NULL` must have `rec_close_date >= '${literal_run_date}'`, `rec_datetime < '${literal_run_date}'`, and `gl_acct_no IS NULL`. Rows with `doc_no IS NULL` must have `rec_close_date IS NULL`, `rec_datetime < '${literal_run_date}'`, and `gl_acct_no IS NULL`. Both extracts are limited to configured companies.

The job removes duplicate order groups whose summed local and USD costs are within `0.005`, and removes both sides of qualifying offsetting receipt pairs for order type `27`.

### Grain and deduplication
The output grain is one AP hold receipt line per `date_flag` and company, keyed by receipt and line-level fields such as `rec_no` and `rec_line_no`. Deduplication is implemented through exclusion tables for net-zero order groups and offsetting receipt pairs.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `rec_no` | Receipt number. | Carried from AP hold source rows that survive duplicate filtering. |
| `rec_line_no` | Receipt line number. | Carried from AP hold source rows. |
| `vend_no` | Vendor associated with the held receipt. | Carried from AP hold source rows. |
| `po_cost` | Purchase order unit cost. | Carried from AP hold source rows and used for duplicate cost checks. |
| `usd_po_cost` | USD purchase order unit cost. | Nulls are converted to zero before target insert. |
| `snap_date` | ETL snapshot timestamp. | Set from `${etl_timestamp}` during insert. |
| `date_flag` | Snapshot partition date. | Set from `${literal_date_flag}`. |
| `company_no` | Company partition. | Carried from the AP hold source. |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[load_ap_hold]
  JOB --> TGT[${literal_target_db}.dwd_disty_ap_hold_df]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `${literal_source_db}.ods_cis_corp_ap_hold` | Source AP hold receipt records. |
| 2 | `temp_ap_hold`, `temp_dup_order`, `temp_ap_hold2`, `temp_dup_rec`, `temp_ap_hold3` | Temporary filtering and duplicate-removal objects. |
| 3 | `${literal_target_db}.dwd_disty_ap_hold_df` | Target daily AP hold table. |

### Step-by-step logic
### Sources and joins
The job reads `${literal_source_db}.ods_cis_corp_ap_hold` twice: once for rows with a document number and an open period crossing the run date, and once for rows without a document number that remain open. It then derives duplicate candidate groups from the temporary AP hold population.

Duplicate order groups are identified by vendor, order type, order number, order line, and document number where local and USD extended values net close to zero. Duplicate receipt pairs for order type `27` are identified by matching vendor, order, document, date, and offsetting positive/negative costs.

### Filters and business rules
Rows with `doc_no IS NOT NULL` must have `rec_close_date >= '${literal_run_date}'`, `rec_datetime < '${literal_run_date}'`, and `gl_acct_no IS NULL`. Rows with `doc_no IS NULL` must have `rec_close_date IS NULL`, `rec_datetime < '${literal_run_date}'`, and `gl_acct_no IS NULL`. Both extracts are limited to configured companies.

The job removes duplicate order groups whose summed local and USD costs are within `0.005`, and removes both sides of qualifying offsetting receipt pairs for order type `27`.

### Grain and deduplication
The output grain is one AP hold receipt line per `date_flag` and company, keyed by receipt and line-level fields such as `rec_no` and `rec_line_no`. Deduplication is implemented through exclusion tables for net-zero order groups and offsetting receipt pairs.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `rec_no` | Receipt number. | Carried from AP hold source rows that survive duplicate filtering. |
| `rec_line_no` | Receipt line number. | Carried from AP hold source rows. |
| `vend_no` | Vendor associated with the held receipt. | Carried from AP hold source rows. |
| `po_cost` | Purchase order unit cost. | Carried from AP hold source rows and used for duplicate cost checks. |
| `usd_po_cost` | USD purchase order unit cost. | Nulls are converted to zero before target insert. |
| `snap_date` | ETL snapshot timestamp. | Set from `${etl_timestamp}` during insert. |
| `date_flag` | Snapshot partition date. | Set from `${literal_date_flag}`. |
| `company_no` | Company partition. | Carried from the AP hold source. |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `—` | `temp_ap_hold2` | many:1 | `a.vend_no = b.vend_no AND a.order_type = b.order_type AND a.order_no = b.order_no AND nvl(a.order_line_no, - 9999) = nvl(b.order_line_no, - 9999) AND a.doc_n...` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:106) |

`source/ref/ap/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `rec_no` | `a.rec_no` | `rec_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:107` |
| `rec_line_no` | `a.rec_line_no` | `rec_line_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:108` |
| `unknown` | `'!'` | — | `temp_ap_hold3` | literal | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:146` |
| `rec_type` | `a.rec_type` | `rec_type` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:147` |
| `rec_loc` | `a.rec_loc` | `rec_loc` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:148` |
| `sku_no` | `a.sku_no` | `sku_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:149` |
| `vend_no` | `a.vend_no` | `vend_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:99` |
| `vend_loc_no` | `a.vend_loc_no` | `vend_loc_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:151` |
| `part_no` | `a.part_no` | `part_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:152` |
| `order_type` | `a.order_type` | `order_type` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:100` |
| `order_no` | `a.order_no` | `order_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:101` |
| `order_line_no` | `a.order_line_no` | `order_line_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:102` |
| `order_exp_line_no` | `a.order_exp_line_no` | `order_exp_line_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:156` |
| `inventory_cost` | `a.inventory_cost` | `inventory_cost` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:157` |
| `invoice_cost` | `NULL` | — | `temp_ap_hold3` | rename | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:32` |
| `po_cost` | `a.po_cost` | `po_cost` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:121` |
| `rec_qty` | `a.rec_qty` | `rec_qty` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:121` |
| `rec_datetime` | `a.rec_datetime` | `rec_datetime` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:118` |
| `doc_date` | `NULL` | — | `temp_ap_hold3` | rename | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:32` |
| `doc_no` | `NULL` | — | `temp_ap_hold3` | rename | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:32` |
| `entry_datetime` | `a.entry_datetime` | `entry_datetime` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:164` |
| `entry_id` | `a.entry_id` | `entry_id` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:165` |
| `hold` | `a.hold` | `hold` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:166` |
| `accept` | `NULL` | — | `temp_ap_hold3` | rename | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:32` |
| `packing_list_no` | `a.packing_list_no` | `packing_list_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:168` |
| `rec_close_date` | `NULL` | — | `temp_ap_hold3` | rename | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:32` |
| `ext_cost` | `a.ext_cost` | `ext_cost` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:170` |
| `gl_acct_no` | `a.gl_acct_no` | `gl_acct_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:171` |
| `usd_po_cost` | `a.usd_po_cost` | `usd_po_cost` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:122` |
| `usd_ext_cost` | `a.usd_ext_cost` | `usd_ext_cost` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:173` |
| `snap_date` | `'${etl_timestamp}'` | `etl_timestamp` | `temp_ap_hold3` | literal | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:174` |
| `date_flag` | `to_date('${literal_date_flag}')` | `literal_date_flag` | `temp_ap_hold3` | udf | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:175` |
| `company_no` | `company_no` | `company_no` | `temp_ap_hold3` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:29` |

### Sentinel and code values
None identified in repository

---


### POS bitbucket-etl mirror

- Also packaged under POS contract pack: source/contracts/pos/bitbucket-etl/dwd_disty_ap_hold_df/load_ap_hold.py
- Table-level POS KB (when applicable): see 	arget/knowledgebase/pos/readme.md § Bitbucket-etl

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM ${literal_target_db}.dwd_disty_ap_hold_df WHERE partition_col = '${partition_value}' GROUP BY 1;
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
| `${literal_source_db}.ods_cis_corp_ap_hold` | Source for open AP hold records with and without document numbers. | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:31`, `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:66` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `load_ap_vdah_lines` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:207` |
| `sync_dwd_disty_ap_hold_df` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:244` |
| `${target_db}.dwd_disty_ap_hold_df` read by `load_ap_vdah_lines.py` | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:65` |

### Operational detail (verifie

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM ${literal_target_db}.dwd_disty_ap_hold_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `${literal_source_db}.ods_cis_corp_ap_hold` | Source for open AP hold records with and without document numbers. | `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:31`, `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:66` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `load_ap_vdah_lines` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:207` |
| `sync_dwd_disty_ap_hold_df` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:244` |
| `${target_db}.dwd_disty_ap_hold_df` read by `load_ap_vdah_lines.py` | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:65` |

### Operational detail (verified)
- The AP aging flow runs this script as a `livy32` Python job named `load_ap_hold`. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:164`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:176`.
- The target partition is dropped before insert overwrite. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:141`, `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py:142`.

### Not documented in repository
- Owner, SLA, and schedule are not documented in the reviewed files.
- Physical table DDL and storage format for `${literal_target_db}.dwd_disty_ap_hold_df` are not documented in the reviewed files.

### Related scripts (verified)
- `load_ap_vend_doc.py` — runs before `load_ap_vdah_lines` along with `load_ap_hold` — `source/etl/flows/data_service/ap/ap_aging_load_us.flow:207`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:208`
- `load_ap_vdah_lines.py` — consumes `${target_db}.dwd_disty_ap_hold_df` — `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:65`

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_hold.py`.*
