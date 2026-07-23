# load_ap_vdah_lines

- artifact_type: etl_table
- artifact_id: ${target_db}.dwd_disty_ap_vdah_lines_di
- domain: ap
- one_line_purpose: This job creates detailed AP vendor document and AP hold aging lines. It combines vendor document balances, receiving hold lines, inventory cost summaries, terms, vendor profiles, project and claim information, and currency-rate handling in...
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `${target_db}.dwd_disty_ap_vdah_lines_di`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** Not documented in repository
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository


### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `${target_db}.dwd_disty_ap_vdah_lines_di` | ETL target / intermediate per evidence script |
| Vertica | pending | `${target_db}.dwd_disty_ap_vdah_lines_di` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `${target_db}.dwd_disty_ap_vdah_lines_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "ap load_ap_vdah_lines schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `${target_db}.dwd_disty_ap_hold_df` | Source AP hold snapshot. |
| 2 | `${target_db}.dwd_disty_ap_vend_doc_df` | Source AP vendor document snapshot. |
| 3 | `${source_db}.ods_cis_corp_ap_hold` | Source receipt-level AP hold detail. |
| 4 | `${target_db}.dwd_disty_inv_qty_df` and `${source_db}.ods_cis_corp_part_master` | Sources for inventory quantity, vendor, and product attributes. |
| 5 | `${target_db}.dws_disty_ap_vend_aging_df` | Source prior-month consignment inventory cost. |
| 6 | `${target_db}.dwd_disty_ap_inv_sum_temp` | Intermediate inventory summary target used by the aging summary job. |
| 7 | `${target_db}.dwd_disty_ap_vdah_lines_di` | Target detailed AP aging line table. |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This job creates detailed AP vendor document and AP hold aging lines. It combines vendor document balances, receiving hold lines, inventory cost summaries, terms, vendor profiles, project and claim information, and currency-rate handling into a line-level AP aging dataset.

It helps AP, finance, and operations users analyze outstanding AP exposure by vendor, SKU, product code, claim/project attributes, document, receipt, and aging bucket inputs.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (ap)** | Uses `${target_db}.dwd_disty_ap_vdah_lines_di` for operational and reporting workflows documented below. |

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py` |

### Key filters and ETL business logic
### Sources and joins
The job starts from the AP hold snapshot and AP vendor document snapshot for the configured `a_date` and companies. It joins vendor documents to AP hold source detail to calculate document hold sums, and joins vendor documents to vendor master data for tolerance and document type logic.

Inventory valuation is built from `${target_db}.dwd_disty_inv_qty_df`, part master, vendor currency, SKU cost, inventory type group metadata, exchange rates, and consignment inventory. The script writes those values into `${target_db}.dwd_disty_ap_inv_sum_temp`, which is later consumed by the vendor aging summary job.

For line construction, the job combines unmatched AP hold orders and matched vendor document hold lines, enriches order details from order headers, terms, part master, PM claims, claim types, project info, AP do-not-deduct profiles, vendor profiles, vendor location terms, and adjustment vendor controls.

### Filters and business rules
The script filters AP hold and vendor document snapshots to `date_flag = '${a_date}'` and configured companies. Inventory quantity is filtered to the same snapshot date and company list, excludes DSL-profile locations, and keeps rows with a non-null inventory group.

Line amount allocation divides vendor document amounts across AP hold lines by each line's share of AP hold amount when possible. Aging days are calculated from discount dates, due dates, receipt dates, terms days, tolerance, and special order type `27` do-not-deduct profile rules. If `age_auto_deduct == 1`, negative amounts for active AP `AUTO_DE` vendor profiles are forced to zero aging days.

### Grain and deduplication
The final output grain is one detailed AP document/hold aging line per date, company, document, receipt line, vendor, product/SKU, and order context. The script uses grouped temporary tables for inventory summaries and AP hold/document sums, and keeps line-level rows for final AP aging detail.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `doc_no` | AP vendor document identifier. | Comes from vendor document snapshot or the AP hold line context. |
| `rec_no`, `rec_line_no` | Receipt and receipt line identifiers. | Used to retain receiving-line detail for AP hold exposure. |
| `vd_type` | Vendor document type classification. | Set to `V` when AP hold detail exists for a document, otherwise `R` for remaining document balance. |
| `ah_type` | AP hold line type. | Set to `U` for unmatched AP hold orders and `V` for vendor-document-linked hold lines. |
| `amt` | Local AP line amount. | Uses AP hold line amount for unmatched holds or allocated vendor document amount for document lines. |
| `usd_amt` | USD AP line amount. | Uses USD AP hold or allocated USD vendor document amount. |
| `days` | Aging-days input. | Calculated from due/discount/receipt dates, terms, tolerance, and order type `27` DND rules. |
| `var_no`, `claim_type` | Project/claim attributes. | Enriched from project info and PM claim data for order type `27`. |
| `org_vend_no` | Original vendor number for adjustment documents. | Derived from vendor invoice text when adjustment vendor controls match. |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM ${target_db}.dwd_disty_ap_vdah_lines_di
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
The job starts from the AP hold snapshot and AP vendor document snapshot for the configured `a_date` and companies. It joins vendor documents to AP hold source detail to calculate document hold sums, and joins vendor documents to vendor master data for tolerance and document type logic.

Inventory valuation is built from `${target_db}.dwd_disty_inv_qty_df`, part master, vendor currency, SKU cost, inventory type group metadata, exchange rates, and consignment inventory. The script writes those values into `${target_db}.dwd_disty_ap_inv_sum_temp`, which is later consumed by the vendor aging summary job.

For line construction, the job combines unmatched AP hold orders and matched vendor document hold lines, enriches order details from order headers, terms, part master, PM claims, claim types, project info, AP do-not-deduct profiles, vendor profiles, vendor location terms, and adjustment vendor controls.

### Filters and business rules
The script filters AP hold and vendor document snapshots to `date_flag = '${a_date}'` and configured companies. Inventory quantity is filtered to the same snapshot date and company list, excludes DSL-profile locations, and keeps rows with a non-null inventory group.

Line amount allocation divides vendor document amounts across AP hold lines by each line's share of AP hold amount when possible. Aging days are calculated from discount dates, due dates, receipt dates, terms days, tolerance, and special order type `27` do-not-deduct profile rules. If `age_auto_deduct == 1`, negative amounts for active AP `AUTO_DE` vendor profiles are forced to zero aging days.

### Grain and deduplication
The final output grain is one detailed AP document/hold aging line per date, company, document, receipt line, vendor, product/SKU, and order context. The script uses grouped temporary tables for inventory summaries and AP hold/document sums, and keeps line-level rows for final AP aging detail.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `doc_no` | AP vendor document identifier. | Comes from vendor document snapshot or the AP hold line context. |
| `rec_no`, `rec_line_no` | Receipt and receipt line identifiers. | Used to retain receiving-line detail for AP hold exposure. |
| `vd_type` | Vendor document type classification. | Set to `V` when AP hold detail exists for a document, otherwise `R` for remaining document balance. |
| `ah_type` | AP hold line type. | Set to `U` for unmatched AP hold orders and `V` for vendor-document-linked hold lines. |
| `amt` | Local AP line amount. | Uses AP hold line amount for unmatched holds or allocated vendor document amount for document lines. |
| `usd_amt` | USD AP line amount. | Uses USD AP hold or allocated USD vendor document amount. |
| `days` | Aging-days input. | Calculated from due/discount/receipt dates, terms, tolerance, and order type `27` DND rules. |
| `var_no`, `claim_type` | Project/claim attributes. | Enriched from project info and PM claim data for order type `27`. |
| `org_vend_no` | Original vendor number for adjustment documents. | Derived from vendor invoice text when adjustment vendor controls match. |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[load_ap_vdah_lines]
  JOB --> TGT[${target_db}.dwd_disty_ap_vdah_lines_di]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `${target_db}.dwd_disty_ap_hold_df` | Source AP hold snapshot. |
| 2 | `${target_db}.dwd_disty_ap_vend_doc_df` | Source AP vendor document snapshot. |
| 3 | `${source_db}.ods_cis_corp_ap_hold` | Source receipt-level AP hold detail. |
| 4 | `${target_db}.dwd_disty_inv_qty_df` and `${source_db}.ods_cis_corp_part_master` | Sources for inventory quantity, vendor, and product attributes. |
| 5 | `${target_db}.dws_disty_ap_vend_aging_df` | Source prior-month consignment inventory cost. |
| 6 | `${target_db}.dwd_disty_ap_inv_sum_temp` | Intermediate inventory summary target used by the aging summary job. |
| 7 | `${target_db}.dwd_disty_ap_vdah_lines_di` | Target detailed AP aging line table. |

### Step-by-step logic
### Sources and joins
The job starts from the AP hold snapshot and AP vendor document snapshot for the configured `a_date` and companies. It joins vendor documents to AP hold source detail to calculate document hold sums, and joins vendor documents to vendor master data for tolerance and document type logic.

Inventory valuation is built from `${target_db}.dwd_disty_inv_qty_df`, part master, vendor currency, SKU cost, inventory type group metadata, exchange rates, and consignment inventory. The script writes those values into `${target_db}.dwd_disty_ap_inv_sum_temp`, which is later consumed by the vendor aging summary job.

For line construction, the job combines unmatched AP hold orders and matched vendor document hold lines, enriches order details from order headers, terms, part master, PM claims, claim types, project info, AP do-not-deduct profiles, vendor profiles, vendor location terms, and adjustment vendor controls.

### Filters and business rules
The script filters AP hold and vendor document snapshots to `date_flag = '${a_date}'` and configured companies. Inventory quantity is filtered to the same snapshot date and company list, excludes DSL-profile locations, and keeps rows with a non-null inventory group.

Line amount allocation divides vendor document amounts across AP hold lines by each line's share of AP hold amount when possible. Aging days are calculated from discount dates, due dates, receipt dates, terms days, tolerance, and special order type `27` do-not-deduct profile rules. If `age_auto_deduct == 1`, negative amounts for active AP `AUTO_DE` vendor profiles are forced to zero aging days.

### Grain and deduplication
The final output grain is one detailed AP document/hold aging line per date, company, document, receipt line, vendor, product/SKU, and order context. The script uses grouped temporary tables for inventory summaries and AP hold/document sums, and keeps line-level rows for final AP aging detail.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `doc_no` | AP vendor document identifier. | Comes from vendor document snapshot or the AP hold line context. |
| `rec_no`, `rec_line_no` | Receipt and receipt line identifiers. | Used to retain receiving-line detail for AP hold exposure. |
| `vd_type` | Vendor document type classification. | Set to `V` when AP hold detail exists for a document, otherwise `R` for remaining document balance. |
| `ah_type` | AP hold line type. | Set to `U` for unmatched AP hold orders and `V` for vendor-document-linked hold lines. |
| `amt` | Local AP line amount. | Uses AP hold line amount for unmatched holds or allocated vendor document amount for document lines. |
| `usd_amt` | USD AP line amount. | Uses USD AP hold or allocated USD vendor document amount. |
| `days` | Aging-days input. | Calculated from due/discount/receipt dates, terms, tolerance, and order type `27` DND rules. |
| `var_no`, `claim_type` | Project/claim attributes. | Enriched from project info and PM claim data for order type `27`. |
| `org_vend_no` | Original vendor number for adjustment documents. | Derived from vendor invoice text when adjustment vendor controls match. |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `temp_hvd` | `ods_xx.ods_cis_corp_ap_hold` | many:1 | `a.doc_no = v.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:109) |
| `temp_hvd` | `ods_xx.ods_cis_corp_vend_master` | many:1 | `v.vend_no=m.vend_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:119) |
| `temp_hvd` | `temp_dw_ah_sum` | many:1 | `v.doc_no=a.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:119) |
| `temp_currency` | `${literal_source_db}.ods_cis_corp_company_profile` | many:1 | `a.company_no = b.company_no and b.profile_type = 'CURRENCY' AND b.company_no in (${company_no}))` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:144) |
| `temp_currency` | `${literal_source_db}.ods_cis_corp_exchange_rate` | many:1 | `a.currency = b.currency AND date <= '${a_date}' AND base = '${base}') e` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:144) |
| `dw_xx.dwd_disty_inv_qty_df` | `ods_xx.ods_cis_corp_part_master` | many:1 | `a.sku_no = c.sku_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:184) |
| `temp_inv_qty1` | `ods_xx.ods_cis_corp_v_vend_currency` | many:1 | `a.vend_no = b.vend_no AND a.company_no = b.company_no ), inv_qty_po AS (` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:203) |
| `temp_inv_qty1` | `ods_xx.ods_cis_corp_sku_cost` | many:1 | `a.sku_no = b.sku_no AND a.company_no = b.company_no)` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:203) |
| `temp_inv_qty3` | `temp_rate` | many:1 | `a.company_no = b.company_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:286) |
| `temp_csgn_ah` | `ods_xx.ods_cis_corp_part_master` | many:1 | `a.sku_no = b.sku_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:320) |
| `temp_dw_inv_sum_1` | `temp_csgn_inv` | many:1 | `a.vend_no = b.vend_no and a.prod_code = b.prod_code and a.company_no = b.company_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:364) |
| `temp_csgn_inv` | `temp_rate` | many:1 | `a.company_no = r.company_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:364) |
| `temp_hah` | `temp_dw_ah_sum` | many:1 | `o.doc_no = a.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `temp_dw_ah_sum` | `temp_dw_vd_sum` | many:1 | `o.doc_no = v.doc_no), ah_od_3 AS (` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `temp_dw_ah_sum` | `ods_xx.ods_etl_order_header_all` | many:1 | `o.order_type = h.order_type and o.order_no = h.order_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `temp_dw_ah_sum` | `ods_xx.ods_cis_corp_part_master` | many:1 | `o.sku_no = p.sku_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `ods_xx.ods_etl_order_header_all` | `ods_xx.ods_cis_corp_terms_file` | many:1 | `trim(h.terms_no) = trim(t.doc_terms)), ah_od_5 AS (` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `temp_dw_ah_sum` | `ods_xx.ods_cis_corp_pm_claim` | many:1 | `o.order_no = c.project_no and o.order_line_no = c.claim_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `ods_xx.ods_cis_corp_pm_claim` | `ods_xx.ods_cis_corp_pm_claim_type` | many:1 | `c.claim_type = ct.claim_type` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `ods_xx.ods_cis_corp_pm_claim` | `ods_xx.ods_cis_corp_terms_file` | many:1 | `trim(c.doc_terms) = trim(t.doc_terms))` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:414) |
| `temp_dw_vdah_ln_2` | `ods_xx.ods_cis_corp_project_info` | many:1 | `a.order_no = b.proj_no), order_27_3 AS (` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `temp_dw_vdah_ln_2` | `ods_xx.ods_cis_corp_ap_dnd_profile` | many:1 | `a.vend_no = b.vend_no and b.profile_type = 'DND' and b.profile_cond_i = 27 and b.status = 'A' and b.start_var_no <= a.var_no and b.end_var_no >= a.var_no and...` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `temp_dw_vdah_ln_2` | `ods_xx.ods_cis_corp_ap_dnd_profile` | many:1 | `a.vend_no = b.vend_no and b.profile_type = 'DND' and b.profile_cond_i = 0 and b.status = 'A' and a.hold_day is null` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `ods_xx.ods_cis_corp_vend_master` | `ods_xx.ods_cis_corp_vend_location` | many:1 | `l.vend_no = v.vend_no and l.loc_no = v.pay_to_loc` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `ods_xx.ods_cis_corp_vend_location` | `ods_xx.ods_cis_corp_terms_file` | many:1 | `trim(t.doc_terms) = trim(l.terms)) v on v.vend_no = a.vend_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `temp_dw_vdah_ln_2` | `ods_xx.ods_cis_corp_project_info` | many:1 | `a.order_no = c.proj_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `temp_dw_vdah_ln_2` | `ods_xx.ods_cis_corp_pm_claim` | many:1 | `a.order_no = d.project_no and a.order_line_no = d.claim_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:831) |
| `temp_dw_vdah_ln_3` | `ods_xx.ods_cis_corp_vendor_profile` | many:1 | `a.vend_no = b.vend_no and b.profile_type = 'AUTO_DE' and b.profile_cat = 'AP' and b.active = 'Y'` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1021) |
| `temp_dw_vdah_ln` | `temp_adj_vd` | many:1 | `a.vend_no = b.vend_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1081) |
| `temp_dw_vdah_ln` | `temp_hvd` | many:1 | `a.doc_no = c.doc_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1081) |

`source/ref/ap/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `doc_no` | `a.doc_no` | `doc_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:110` |
| `rec_no` | `a.rec_no` | `rec_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:417` |
| `rec_line_no` | `a.rec_line_no` | `rec_line_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:418` |
| `vd_type` | `a.vd_type` | `vd_type` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:560` |
| `ah_type` | `a.ah_type` | `ah_type` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:540` |
| `order_type` | `a.order_type` | `order_type` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:420` |
| `order_no` | `a.order_no` | `order_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:421` |
| `order_line_no` | `a.order_line_no` | `order_line_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:422` |
| `terms_no` | `trim(a.terms_no)` | `terms_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | udf | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1090` |
| `prod_code` | `a.prod_code` | `prod_code` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:230` |
| `vpl_no` | `(select max(pm.vpl_no) from ${source_db}.ods_cis_corp_part_master pm where pm.sku_no= a.sku_no)` | `vpl_no`, `source_db`, `ods_cis_corp_part_master`, `pm`, `sku_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | agg | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1092` |
| `vend_no` | `a.vend_no` | `vend_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:216` |
| `ah_vend_no` | `a.ah_vend_no` | `ah_vend_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:544` |
| `sku_no` | `a.sku_no` | `sku_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:185` |
| `ah_sum` | `a.ah_sum` | `ah_sum` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:461` |
| `vd_sum` | `a.vd_sum` | `vd_sum` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:561` |
| `ah_line_amt` | `a.ah_line_amt` | `ah_line_amt` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:548` |
| `vd_line_amt` | `a.vd_line_amt` | `vd_line_amt` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:738` |
| `amt` | `a.amt` | `amt` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:739` |
| `revenue_acct_no` | `a.revenue_acct_no` | `revenue_acct_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:555` |
| `tolerance` | `a.tolerance` | `tolerance` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:563` |
| `inv_disc_date` | `a.inv_disc_date` | `inv_disc_date` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:564` |
| `doc_due_date` | `a.doc_due_date` | `doc_due_date` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:565` |
| `terms_days` | `a.terms_days` | `terms_days` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:550` |
| `disc_days` | `a.disc_days` | `disc_days` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:551` |
| `rec_datetime` | `a.rec_datetime` | `rec_datetime` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:425` |
| `days` | `a.days` | `days` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:760` |
| `inv_type` | `a.inv_type` | `inv_type` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:189` |
| `reason_code` | `a.reason_code` | `reason_code` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:762` |
| `ah_usd_sum` | `a.ah_usd_sum` | `ah_usd_sum` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:462` |
| `vd_usd_sum` | `a.vd_usd_sum` | `vd_usd_sum` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:562` |
| `ah_usd_line_amt` | `a.ah_usd_line_amt` | `ah_usd_line_amt` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:557` |
| `vd_usd_line_amt` | `a.vd_usd_line_amt` | `vd_usd_line_amt` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:768` |
| `usd_amt` | `a.usd_amt` | `usd_amt` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:769` |
| `var_no` | `a.var_no` | `var_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:770` |
| `claim_type` | `a.claim_type` | `claim_type` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:771` |
| `org_vend_no` | `case when b.vend_no is not null and c.doc_no is not null and upper(c.vend_inv_no) rlike '[0-9]/DOC#[0-9]' and SUBSTR(...` | `vend_no`, `doc_no`, `vend_inv_no`, `rlike`, `DOC`, `INSTR`, `org_vend_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | case | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1118` |
| `date_flag` | `to_date(a.date_flag)` | `date_flag` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | udf | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1124` |
| `company_no` | `a.company_no` | `company_no` | `temp_dw_vdah_ln`, `temp_adj_vd`, `temp_hvd` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:146` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM ${target_db}.dwd_disty_ap_vdah_lines_di WHERE partition_col = '${partition_value}' GROUP BY 1;
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
| `${target_db}.dwd_disty_ap_hold_df` | Reads AP hold snapshot. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:65` |
| `${target_db}.dwd_disty_ap_vend_doc_df` | Reads AP vendor document snapshot. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:105` |
| `${source_db}.ods_cis_corp_ap_hold` | Reads AP hold source detail for document sums and order lines. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:115`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:451` |
| `${source_db}.ods_cis_corp_vend_master` | Reads vendor tolerance, terms, and vendor name attributes. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:137`,

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM ${target_db}.dwd_disty_ap_vdah_lines_di
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `${target_db}.dwd_disty_ap_hold_df` | Reads AP hold snapshot. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:65` |
| `${target_db}.dwd_disty_ap_vend_doc_df` | Reads AP vendor document snapshot. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:105` |
| `${source_db}.ods_cis_corp_ap_hold` | Reads AP hold source detail for document sums and order lines. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:115`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:451` |
| `${source_db}.ods_cis_corp_vend_master` | Reads vendor tolerance, terms, and vendor name attributes. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:137`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:925` |
| `${literal_source_db}.ods_cis_corp_company_profile` | Reads company currency profile. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:149` |
| `${literal_source_db}.ods_cis_corp_exchange_rate` | Reads exchange rate for configured base currency. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:161` |
| `${target_db}.dwd_disty_inv_qty_df` | Reads inventory quantity snapshot. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:196` |
| `${source_db}.ods_cis_corp_part_master` | Reads part, vendor, product, and VPL attributes. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:197`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1092` |
| `${source_db}.ods_cis_corp_v_vend_currency` | Reads vendor currency flags. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:215` |
| `${source_db}.ods_cis_corp_sku_cost` | Reads SKU cost values. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:249` |
| `${source_db}.ods_breport_mydaas_dw_inv_type` | Maps inventory type to inventory group. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:246` |
| `${source_db}.ods_cis_corp_vend_profile` | Excludes DSL locations. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:273` |
| `${target_db}.dws_disty_ap_vend_aging_df` | Reads prior-month consignment inventory cost. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:341` |
| `${source_db}.ods_etl_order_header_all` | Reads order terms and inventory type context. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:488` |
| `${source_db}.ods_cis_corp_terms_file` | Reads terms and discount days. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:493` |
| `${source_db}.ods_cis_corp_pm_claim` | Reads PM claim terms, product manager code, and claim type. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:533`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1016` |
| `${source_db}.ods_cis_corp_pm_claim_type` | Reads revenue account for PM claim type. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:536` |
| `${source_db}.ods_cis_corp_vendor_profile` | Reads AP default product manager and AUTO_DE profiles. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:713`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1064` |
| `${source_db}.ods_cis_corp_project_info` | Reads project variable number for order type `27`. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:858`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1014` |
| `${source_db}.ods_cis_corp_ap_dnd_profile` | Reads do-not-deduct hold-day rules. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:879`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:904` |
| `${source_db}.ods_cis_corp_no_ctrl` | Reads AP adjustment vendor numbers. | `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1076` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `load_ap_vend_aging` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:214`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:229` |
| `${literal_target_db}.dwd_disty_ap_vdah_lines_di` read by `load_ap_vend_aging.py` | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:82` |
| `sync_dwd_disty_ap_vdah_lines_di` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:254` |

### Operational detail (verified)
- The AP aging flow runs this script as a `livy32` Python job named `load_ap_vdah_lines`. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:180`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:206`.
- The flow declares dependencies on `load_ap_vend_doc`, `load_ap_hold`, `get_params`, `azk_inv_aging_load`, and `relyon_ods_etl_order_header_all`. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:207`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:212`.
- The target `dwd_disty_ap_vdah_lines_di` partition is dropped before insert overwrite. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1080`, `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:1081`.
- The intermediate `${target_db}.dwd_disty_ap_inv_sum_temp` is inserted before the line target is built. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:364`.

### Not documented in repository
- Owner, SLA, and schedule are not documented in the reviewed files.
- Physical DDL for `${target_db}.dwd_disty_ap_inv_sum_temp` and `${target_db}.dwd_disty_ap_vdah_lines_di` is not documented in the reviewed files.

### Related scripts (verified)
- `load_ap_vend_doc.py` — produces `${target_db}.dwd_disty_ap_vend_doc_df` consumed by this job — `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:105`
- `load_ap_hold.py` — produces `${target_db}.dwd_disty_ap_hold_df` consumed by this job — `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py:65`
- `load_ap_vend_aging.py` — consumes `${literal_target_db}.dwd_disty_ap_vdah_lines_di` — `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:82`

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vdah_lines.py`.*
