# Examples index — `starrocks_open_so_bo`

- artifact_type: examples-index
- artifact_id: rds/starrocks_open_so_bo/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
﻿Typical StarRocks OPEN_SO_BO example reports

1. typical_open_so_bo_basic_bo_unieta_inventory_rds_5987.txt
   Source: CA/run/rds_5987_rtv.sp
   Use when the request asks for a compact open BO extract with order_type = 8, current order header/detail, product master, customer name enrichment, inventory on-order lookup, UniETA ETA update, and StarRocks tempdb primary-key staging style.

2. typical_open_so_bo_multisheet_eta_expense_rds_6143.txt
   Source: CA/run/rds_6143_rtv.sp
   Use when the request asks for multi-sheet Open_SO_BO output, open orders with ETA, shipped current month, invoiced rolling history, customer/account staging, open quantity = order_qty - ifnull(ship_qty,0), UniETA min ETA, and order_exp DP expense aggregation.

3. typical_open_so_bo_rio_allocation_inventory_rds_6302.txt
   Source: CA/run/rds_6302_rtv.sp
   Use when the request asks for SKU/VPL filtered open SO/BO demand, order_type 1 allocation versus order_type 8 BO quantities, RIO request/detail/consumed quantities, RCT list-box order types, manager approval name, inventory and allocation style calculations.

4. typical_open_so_bo_customer_sku_serial_inventory_rds_14053.txt
   Source: US/run/rds_14053_rtv.sp
   Use when the request asks for customer-specific SKU selection via SKU profile CUST_SKU, open SO/BO detail with order expense aggregation, UniETA, daily inventory snapshot, sold-to/end-user PO, and serial-number style enrichment.

5. typical_open_so_bo_status_eu_custom_vpo_chain_rds_17936.txt
   Source: US/run/rds_17936_rtv.sp
   Use when the request asks for status/current queue derivation from operational dates, current plus dropship/VPO-related branches, CEDM EU custom field extraction such as Multiterm Billing, VPO number fallback through mc_order_ref or order header int_ref, and technical note enrichment.

6. typical_open_so_bo_open_shipped_tracking_rds_8775.txt
   Source: CA/run/rds_8775_rtv.sp
   Use when the request asks for open SO/BO rows plus recent shipped rows, status OPENED/RELEASED from pick_date, order comments and EU common contact filters, shipped tracking from current/history carton headers, and multi-tab output.

7. typical_open_so_bo_pm_queue_ship_complete_rds_19137.txt
   Source: US/run/rds_19137_rtv.sp
   Use when the request asks for PM/vendor ownership, vend_user_matrix PM fallback by VPL or vendor, SHIP_CPLE order profile flag, PM queue from sales_que, sales territory filters, comments, and inventory on-hand fallback across prior-day snapshots.

8. typical_open_so_bo_brpt_snapshot_profile_rds_8700.txt
   Source: CA/run/rds_8700_rtv.sp
   Use when the request asks for BRPT BO current snapshot context, open order enrichment from order header/sold-to/location/customer/territory/product, profile or SPA/rebate style enrichment, and snapshot date_flag handling alongside StarRocks output tables.
```
