# Extract: load_ap_vend_aging.py (gap-fill)

Provenance: `BAF/data_service_b_report/disty_common/ap/python/load_ap_vend_aging.py` (master).

## Role
Buckets AP open amounts by aging windows into `dws_disty_ap_vend_aging_df` (feeds P&L `AP_FINANCE` / `AP_ADJ` pre_* nodes).

## Key upstream (ETL-proven)
- `\.dwd_disty_ap_vdah_lines_di` — line source with `days`, `amt`, `ah_type`, `vd_type` (filter `date_flag = '\'`)
- `\.ods_cis_corp_part_master` — SKU/vend enrichment via `temp_sku`

## Technical filters
- `date_flag = '\'`
- `company_no in (\)` on vdah lines

## Compass process
- `tdsynnex/azkabanprocess/data_service_b_report/ap_aging_load_us/load_ap_vend_aging`
