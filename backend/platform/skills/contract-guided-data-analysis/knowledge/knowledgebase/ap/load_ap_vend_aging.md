# load_ap_vend_aging

- artifact_type: etl_table
- artifact_id: ${literal_target_db}.dws_disty_ap_vend_aging_df
- domain: ap
- one_line_purpose: This job summarizes detailed AP vendor document and AP hold lines into vendor aging reporting buckets. It produces AP aging by vendor, product, terms, order/claim classifications, auto-deduct status, SKU, VPL, and company-level rollups.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `${literal_target_db}.dws_disty_ap_vend_aging_df`
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
| Hive | yes | `${literal_target_db}.dws_disty_ap_vend_aging_df` | ETL target / intermediate per evidence script |
| Vertica | pending | `${literal_target_db}.dws_disty_ap_vend_aging_df` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `${literal_target_db}.dws_disty_ap_vend_aging_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "ap load_ap_vend_aging schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `${literal_target_db}.dwd_disty_ap_vdah_lines_di` | Source detailed AP aging lines. |
| 2 | `${literal_source_db}.ods_cis_corp_part_master` | Source SKU-to-vendor/product/VPL enrichment. |
| 3 | `${literal_source_db}.ods_cis_corp_debit_note_header` | Source auto-deduct and non-auto-deduct debit note classification. |
| 4 | `${literal_target_db}.dwd_disty_ap_inv_sum_temp` | Source inventory cost summary. |
| 5 | `${literal_source_db}.ods_cis_corp_vend_master` | Source vendor name and AP clerk. |
| 6 | `${literal_target_db}.dws_disty_ap_vend_aging_df` | Target AP vendor aging summary table. |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This job summarizes detailed AP vendor document and AP hold lines into vendor aging reporting buckets. It produces AP aging by vendor, product, terms, order/claim classifications, auto-deduct status, SKU, VPL, and company-level rollups.

It helps AP, finance, vendor management, and reporting teams monitor outstanding vendor exposure, past-due balances, inventory cost context, and aging trends in both local and USD amounts.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (ap)** | Uses `${literal_target_db}.dws_disty_ap_vend_aging_df` for operational and reporting workflows documented below. |

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py` |

### Key filters and ETL business logic
### Sources and joins
The job reads `${literal_target_db}.dwd_disty_ap_vdah_lines_di` for the configured date and company list, then derives local and USD aging bucket amounts from `days`, `amt`, AP hold line amount, and vendor document line amount. It joins distinct SKUs to part master for vendor/product/VPL enrichment.

The script builds many summary levels from the detailed line table, including terms/vendor/product, vendor credit/debit direction, unmatched and vendor-document hold categories, order type categories, marketing group categories, auto-deduct categories, vendor/product rollups, company/product rollups, terms rollups, SKU rollups, and VPL rollups. It enriches vendor-facing output with vendor name and AP clerk from vendor master.

Inventory cost from `${literal_target_db}.dwd_disty_ap_inv_sum_temp` is joined into vendor/product rows and then rolled into higher-level summaries. Vendor-level inventory cost is also propagated into selected vendor summary levels.

### Filters and business rules
The source line extract is filtered to `date_flag = '${literal_date_flag}'` and configured companies. Aging buckets are calculated with sign-based expressions over `days`, separating negative/early buckets, short-term buckets, and longer past-due ranges.

Rows are excluded from the final output when all local and USD amount fields, inventory fields, and cost fields round to zero at four decimals. Auto-deduct and non-auto-deduct groups are identified by existence in `${literal_source_db}.ods_cis_corp_debit_note_header` with `auto_deduct = 'Y'` or `auto_deduct = 'N'`.

### Grain and deduplication
The target grain depends on `sum_level`. Common keys are `date_flag`, `sum_level`, `terms_no`, `vend_no`, `prod_code`, `vpl_no`, and `company_no`. The script uses grouped aggregations and `UNION ALL` to produce multiple business summary grains from the same detailed AP line source.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sum_level` | Business summary grain. | Assigned by each aggregation block, such as vendor/product, terms/vendor, SKU, VPL, auto-deduct, or order-type grouping. |
| `terms_no` | Terms or category value for the row. | Comes from source terms or category labels such as `ALL`, `AA`, `CR`, `DR`, or claim/order values. |
| `vend_no` | Vendor or company rollup identifier. | Uses vendor number for vendor rows and company number for company-level rollups. |
| `prod_code` | Product, SKU, or rollup product identifier depending on `sum_level`. | Derived from detailed AP line product code, SKU, part master, or fixed rollup values. |
| `age1_30`, `age31_60`, `age91_120`, and other aging columns | AP balance in aging buckets. | Summed from calculated bucket fields based on `days` and line amounts. |
| `total_doc_amt` | Total vendor document amount in the row. | Aggregated from detailed line `vd_line_amt`. |
| `total_po_cost` | Total AP hold or PO-cost amount in the row. | Aggregated from AP hold or vendor document cost components. |
| `inv_cost`, `cinv_cost` | Inventory and consignment inventory cost. | Joined from inventory summary or accumulated from consignment-related history. |
| `vend_name`, `ap_clerk` | Vendor descriptive fields. | Joined from vendor master for applicable summary levels. |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM ${literal_target_db}.dws_disty_ap_vend_aging_df
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
The job reads `${literal_target_db}.dwd_disty_ap_vdah_lines_di` for the configured date and company list, then derives local and USD aging bucket amounts from `days`, `amt`, AP hold line amount, and vendor document line amount. It joins distinct SKUs to part master for vendor/product/VPL enrichment.

The script builds many summary levels from the detailed line table, including terms/vendor/product, vendor credit/debit direction, unmatched and vendor-document hold categories, order type categories, marketing group categories, auto-deduct categories, vendor/product rollups, company/product rollups, terms rollups, SKU rollups, and VPL rollups. It enriches vendor-facing output with vendor name and AP clerk from vendor master.

Inventory cost from `${literal_target_db}.dwd_disty_ap_inv_sum_temp` is joined into vendor/product rows and then rolled into higher-level summaries. Vendor-level inventory cost is also propagated into selected vendor summary levels.

### Filters and business rules
The source line extract is filtered to `date_flag = '${literal_date_flag}'` and configured companies. Aging buckets are calculated with sign-based expressions over `days`, separating negative/early buckets, short-term buckets, and longer past-due ranges.

Rows are excluded from the final output when all local and USD amount fields, inventory fields, and cost fields round to zero at four decimals. Auto-deduct and non-auto-deduct groups are identified by existence in `${literal_source_db}.ods_cis_corp_debit_note_header` with `auto_deduct = 'Y'` or `auto_deduct = 'N'`.

### Grain and deduplication
The target grain depends on `sum_level`. Common keys are `date_flag`, `sum_level`, `terms_no`, `vend_no`, `prod_code`, `vpl_no`, and `company_no`. The script uses grouped aggregations and `UNION ALL` to produce multiple business summary grains from the same detailed AP line source.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sum_level` | Business summary grain. | Assigned by each aggregation block, such as vendor/product, terms/vendor, SKU, VPL, auto-deduct, or order-type grouping. |
| `terms_no` | Terms or category value for the row. | Comes from source terms or category labels such as `ALL`, `AA`, `CR`, `DR`, or claim/order values. |
| `vend_no` | Vendor or company rollup identifier. | Uses vendor number for vendor rows and company number for company-level rollups. |
| `prod_code` | Product, SKU, or rollup product identifier depending on `sum_level`. | Derived from detailed AP line product code, SKU, part master, or fixed rollup values. |
| `age1_30`, `age31_60`, `age91_120`, and other aging columns | AP balance in aging buckets. | Summed from calculated bucket fields based on `days` and line amounts. |
| `total_doc_amt` | Total vendor document amount in the row. | Aggregated from detailed line `vd_line_amt`. |
| `total_po_cost` | Total AP hold or PO-cost amount in the row. | Aggregated from AP hold or vendor document cost components. |
| `inv_cost`, `cinv_cost` | Inventory and consignment inventory cost. | Joined from inventory summary or accumulated from consignment-related history. |
| `vend_name`, `ap_clerk` | Vendor descriptive fields. | Joined from vendor master for applicable summary levels. |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[load_ap_vend_aging]
  JOB --> TGT[${literal_target_db}.dws_disty_ap_vend_aging_df]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `${literal_target_db}.dwd_disty_ap_vdah_lines_di` | Source detailed AP aging lines. |
| 2 | `${literal_source_db}.ods_cis_corp_part_master` | Source SKU-to-vendor/product/VPL enrichment. |
| 3 | `${literal_source_db}.ods_cis_corp_debit_note_header` | Source auto-deduct and non-auto-deduct debit note classification. |
| 4 | `${literal_target_db}.dwd_disty_ap_inv_sum_temp` | Source inventory cost summary. |
| 5 | `${literal_source_db}.ods_cis_corp_vend_master` | Source vendor name and AP clerk. |
| 6 | `${literal_target_db}.dws_disty_ap_vend_aging_df` | Target AP vendor aging summary table. |

### Step-by-step logic
### Sources and joins
The job reads `${literal_target_db}.dwd_disty_ap_vdah_lines_di` for the configured date and company list, then derives local and USD aging bucket amounts from `days`, `amt`, AP hold line amount, and vendor document line amount. It joins distinct SKUs to part master for vendor/product/VPL enrichment.

The script builds many summary levels from the detailed line table, including terms/vendor/product, vendor credit/debit direction, unmatched and vendor-document hold categories, order type categories, marketing group categories, auto-deduct categories, vendor/product rollups, company/product rollups, terms rollups, SKU rollups, and VPL rollups. It enriches vendor-facing output with vendor name and AP clerk from vendor master.

Inventory cost from `${literal_target_db}.dwd_disty_ap_inv_sum_temp` is joined into vendor/product rows and then rolled into higher-level summaries. Vendor-level inventory cost is also propagated into selected vendor summary levels.

### Filters and business rules
The source line extract is filtered to `date_flag = '${literal_date_flag}'` and configured companies. Aging buckets are calculated with sign-based expressions over `days`, separating negative/early buckets, short-term buckets, and longer past-due ranges.

Rows are excluded from the final output when all local and USD amount fields, inventory fields, and cost fields round to zero at four decimals. Auto-deduct and non-auto-deduct groups are identified by existence in `${literal_source_db}.ods_cis_corp_debit_note_header` with `auto_deduct = 'Y'` or `auto_deduct = 'N'`.

### Grain and deduplication
The target grain depends on `sum_level`. Common keys are `date_flag`, `sum_level`, `terms_no`, `vend_no`, `prod_code`, `vpl_no`, and `company_no`. The script uses grouped aggregations and `UNION ALL` to produce multiple business summary grains from the same detailed AP line source.

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sum_level` | Business summary grain. | Assigned by each aggregation block, such as vendor/product, terms/vendor, SKU, VPL, auto-deduct, or order-type grouping. |
| `terms_no` | Terms or category value for the row. | Comes from source terms or category labels such as `ALL`, `AA`, `CR`, `DR`, or claim/order values. |
| `vend_no` | Vendor or company rollup identifier. | Uses vendor number for vendor rows and company number for company-level rollups. |
| `prod_code` | Product, SKU, or rollup product identifier depending on `sum_level`. | Derived from detailed AP line product code, SKU, part master, or fixed rollup values. |
| `age1_30`, `age31_60`, `age91_120`, and other aging columns | AP balance in aging buckets. | Summed from calculated bucket fields based on `days` and line amounts. |
| `total_doc_amt` | Total vendor document amount in the row. | Aggregated from detailed line `vd_line_amt`. |
| `total_po_cost` | Total AP hold or PO-cost amount in the row. | Aggregated from AP hold or vendor document cost components. |
| `inv_cost`, `cinv_cost` | Inventory and consignment inventory cost. | Joined from inventory summary or accumulated from consignment-related history. |
| `vend_name`, `ap_clerk` | Vendor descriptive fields. | Joined from vendor master for applicable summary levels. |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `${literal_source_db}.ods_cis_corp_part_master` | `temp_d_sku` | many:1 | `a.sku_no = b.sku_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:95) |
| `temp_dw_vend_aging_3` | `temp_dw_inv_sum` | many:1 | `a.vend_no = s.vend_no AND a.prod_code = s.prod_code AND a.company_no = s.company_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1235) |
| `temp_dw_vend_aging_11` | `${literal_source_db}.ods_cis_corp_vend_master` | many:1 | `t.vend_no = m.vend_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1742) |
| `temp_vdal_ln` | `temp_sku` | many:1 | `l.sku_no = pm.sku_no and l.company_no = pm.company_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1742) |
| `temp_sku` | `${literal_source_db}.ods_cis_corp_vend_master` | many:1 | `nvl(nullif(pm.vend_no,0),l.vend_no) = m.vend_no` | etl_sql (source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1742) |

`source/ref/ap/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `sum_level` | `sum_level` | `sum_level` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:104` |
| `terms_no` | `terms_no` | `terms_no` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:14` |
| `vend_no` | `vend_no` | `vend_no` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:9` |
| `prod_code` | `prod_code` | `prod_code` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:13` |
| `vend_name` | `vend_name` | `vend_name` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1748` |
| `vpl_no` | `vpl_no` | `vpl_no` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:18` |
| `ap_clerk` | `ap_clerk` | `ap_clerk` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1752` |
| `age29_up` | `age29_up` | `age29_up` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:23` |
| `age22_28` | `age22_28` | `age22_28` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:24` |
| `age15_21` | `age15_21` | `age15_21` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:25` |
| `age8_14` | `age8_14` | `age8_14` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:26` |
| `age1_7` | `age1_7` | `age1_7` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:27` |
| `age1_30` | `age1_30` | `age1_30` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:28` |
| `age31_60` | `age31_60` | `age31_60` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:29` |
| `age61_90` | `age61_90` | `age61_90` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:30` |
| `age91_120` | `age91_120` | `age91_120` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:31` |
| `total_doc_amt` | `total_doc_amt` | `total_doc_amt` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:61` |
| `total_po_cost` | `total_po_cost` | `total_po_cost` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:62` |
| `total` | `total` | `total` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:61` |
| `inv_cost_reg` | `inv_cost_reg` | `inv_cost_reg` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:123` |
| `inv_cost_rma` | `inv_cost_rma` | `inv_cost_rma` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:124` |
| `inv_cost` | `inv_cost` | `inv_cost` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:123` |
| `entry_id` | `entry_id` | `entry_id` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:146` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:147` |
| `usd29_up` | `usd29_up` | `usd29_up` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:65` |
| `usd_age22_28` | `usd_age22_28` | `usd_age22_28` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:66` |
| `usd_age15_21` | `usd_age15_21` | `usd_age15_21` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:67` |
| `usd_age8_14` | `usd_age8_14` | `usd_age8_14` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:68` |
| `usd_age1_7` | `usd_age1_7` | `usd_age1_7` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:69` |
| `usd_age1_30` | `usd_age1_30` | `usd_age1_30` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:70` |
| `usd_age31_60` | `usd_age31_60` | `usd_age31_60` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:71` |
| `usd_age61_90` | `usd_age61_90` | `usd_age61_90` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:72` |
| `usd_age91_120` | `usd_age91_120` | `usd_age91_120` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:36` |
| `usd_total_doc_amt` | `usd_total_doc_amt` | `usd_total_doc_amt` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:77` |
| `usd_total_po_cost` | `usd_total_po_cost` | `usd_total_po_cost` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:78` |
| `usd_total` | `usd_total` | `usd_total` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:77` |
| `usd_inv_cost_reg` | `usd_inv_cost_reg` | `usd_inv_cost_reg` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:142` |
| `usd_inv_cost_rma` | `usd_inv_cost_rma` | `usd_inv_cost_rma` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:143` |
| `usd_inv_cost` | `usd_inv_cost` | `usd_inv_cost` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:142` |
| `cinv_cost` | `cinv_cost` | `cinv_cost` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:126` |
| `usd_cinv_cost` | `usd_cinv_cost` | `usd_cinv_cost` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:145` |
| `age121_180` | `age121_180` | `age121_180` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:32` |
| `usd_age121_180` | `usd_age121_180` | `usd_age121_180` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:74` |
| `age181_365` | `age181_365` | `age181_365` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:33` |
| `usd_age181_365` | `usd_age181_365` | `usd_age181_365` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:75` |
| `age365_up` | `age365_up` | `age365_up` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:34` |
| `usd_age365_up` | `usd_age365_up` | `usd_age365_up` | `temp_final_ap_aging` | passthrough | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:76` |
| `date_flag` | `to_date(date_flag)` | `date_flag` | `temp_final_ap_aging` | udf | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:2080` |
| `company_no` | `cast(company_no as int)` | `company_no` | `temp_final_ap_aging` | cast | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:2232` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM ${literal_target_db}.dws_disty_ap_vend_aging_df WHERE partition_col = '${partition_value}' GROUP BY 1;
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
| `${literal_target_db}.dwd_disty_ap_vdah_lines_di` | Source AP detailed aging lines. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:82` |
| `${literal_source_db}.ods_cis_corp_part_master` | Enriches SKU rows with vendor, product, and VPL values. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:97` |
| `${literal_source_db}.ods_cis_corp_debit_note_header` | Classifies auto-deduct and non-auto-deduct debit note amounts. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:828`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1010` |
| `${literal_target_db}.dwd_disty_ap_inv_sum_temp` | Supplies vendor/product inventory cost summary. | `s

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM ${literal_target_db}.dws_disty_ap_vend_aging_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `${literal_target_db}.dwd_disty_ap_vdah_lines_di` | Source AP detailed aging lines. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:82` |
| `${literal_source_db}.ods_cis_corp_part_master` | Enriches SKU rows with vendor, product, and VPL values. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:97` |
| `${literal_source_db}.ods_cis_corp_debit_note_header` | Classifies auto-deduct and non-auto-deduct debit note amounts. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:828`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1010` |
| `${literal_target_db}.dwd_disty_ap_inv_sum_temp` | Supplies vendor/product inventory cost summary. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1224` |
| `${literal_source_db}.ods_cis_corp_vend_master` | Supplies vendor name and AP clerk. | `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1796`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:1854` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `sync_dws_disty_ap_vend_aging_df` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:264` |
| `hive2starrocks-dws_disty_ap_vend_aging_df` job | `source/etl/flows/data_service/ap/ap_aging_load_us.flow:316` |
| `source/etl/sql/vendor/data_service/vpl_extract/python/load_dws_disty_brpt_extract_vpl_di.py` | `source/etl/sql/vendor/data_service/vpl_extract/python/load_dws_disty_brpt_extract_vpl_di.py:258`, `source/etl/sql/vendor/data_service/vpl_extract/python/load_dws_disty_brpt_extract_vpl_di.py:274` |
| `source/etl/sql/vendor/data_service/vpl_extract/python/load_dim_disty_brpt_extract_vpl_pm_vend.py` | `source/etl/sql/vendor/data_service/vpl_extract/python/load_dim_disty_brpt_extract_vpl_pm_vend.py:66` |

### Operational detail (verified)
- The AP aging flow runs this script as a `livy32` Python job named `load_ap_vend_aging`. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:214`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:228`.
- The flow declares `load_ap_vend_aging` depends on `load_ap_vdah_lines` and `get_params`. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:229`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:231`.
- The target partition is dropped before insert overwrite. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:2181`, `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:2182`.
- Hive-to-Vertica sync jobs for AP vendor document, hold, detailed lines, and vendor aging depend on `load_ap_vend_aging` in the AP aging flow. Evidence: `source/etl/flows/data_service/ap/ap_aging_load_us.flow:234`, `source/etl/flows/data_service/ap/ap_aging_load_us.flow:267`.

### Not documented in repository
- Owner, SLA, and schedule are not documented in the reviewed files.
- Physical DDL for `${literal_target_db}.dws_disty_ap_vend_aging_df` is not documented in the reviewed files.
- Business definitions for each `sum_level` code are inferred from SQL grouping labels only; no external business glossary was found in the reviewed files.

### Related scripts (verified)
- `load_ap_vdah_lines.py` — produces `${literal_target_db}.dwd_disty_ap_vdah_lines_di` consumed by this job — `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py:82`
- `load_ap_vend_doc.py` — upstream of `load_ap_vdah_lines` in the AP aging flow — `source/etl/flows/data_service/ap/ap_aging_load_us.flow:207`
- `load_ap_hold.py` — upstream of `load_ap_vdah_lines` in the AP aging flow — `source/etl/flows/data_service/ap/ap_aging_load_us.flow:208`

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/ap/data_service/ap/python/load_ap_vend_aging.py`.*
