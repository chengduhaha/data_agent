# Examples index — `vertica_open_so_bo`

- artifact_type: examples-index
- artifact_id: rds/vertica_open_so_bo/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
﻿Typical Vertica OPEN_SO_BO example reports

1. typical_open_so_bo_request_dates_freight_pm_rds_19390.txt
   Source: US/run/rds_19390_rtv.sp
   Use when the request asks for a straightforward open SO/BO extract from dwd_disty_sales_open_order_detail with requested delivery/request ship dates, freight service days, customer and sales fields, and VPL/PM hierarchy enrichment.

2. typical_open_so_bo_scm_spa_two_sheet_rds_8311.txt
   Source: CA/run/rds_8311_rtv.sp
   Use when the request asks for active open order detail with order_delete_date/order_line_delete_date filters, location enrichment, SCM/SPA lookup from dwd_disty_scm_open_order_spa_df using current snapshot date_flag, split outputs for order_type 8 BO and order_type 1 pending orders, plus rds_tmp_sheet_config.

3. typical_open_so_bo_inventory_rio_runrate_rds_7500.txt
   Source: US/run/rds_7500_rtv.sp
   Use when the request asks for customer hierarchy expansion, runrate weekly buckets, current inventory, inventory aging, RIO allocation/on-order quantities, suggested-buy style calculations, location 98 dropship separation, and multi-stage SKU aggregation before output.

4. typical_open_so_bo_cpo_vendor_quote_eu_custom_rds_19082.txt
   Source: US/run/rds_19082_rtv.sp
   Use when the request asks for order_type 8 backorders tied to CPO, Vendor Quote ID from CEDM EU custom mapping, and current/history CPO EU custom union through cpo_id, eu_map_id, eu_map_line_no, and list_box_code = 'CEDM'.

5. typical_open_so_bo_eta_sapid_shipped_open_rds_17695.txt
   Source: US/run/rds_17695_rtv.sp
   Use when the request asks for both awaiting-to-ship open orders and recent shipped/invoiced rows, ETA from dm_pur_unieta_boso_detail_rt, SAPID/vendor SO from order_profile, tracking and ship method enrichment, component-line exclusion, and two output sheets.

6. typical_open_so_bo_union_brpt_scm_spa_rds_17956.txt
   Source: US/run/rds_17956_rtv.sp
   Use when the request asks for year-to-date BO/MSO output that unions order_type 8 BO with order_type 1 dropship rows, uses BRPT BO current snapshot detail, and falls back between shipped SCM/SPA and open SCM/SPA values.

7. typical_open_so_bo_open_pos_status_rds_18245.txt
   Source: US/run/rds_18245_rtv.sp
   Use when the request asks to combine shipped POS and open order populations, derive status from order/header date precedence, use quarter-to-date windows, and output a single order status report with rds_tmp_body.
```
