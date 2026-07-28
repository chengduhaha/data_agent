# Examples index — `starrocks_inventory`

- artifact_type: examples-index
- artifact_id: rds/starrocks_inventory/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical StarRocks Inventory example reports

1. typical_inv_qty_aging_runrate_rio_location_rds_5501.txt
   Source: US/run/rds_5501_rtv.sp
   Use when the request asks for vendor/SKU inventory quantity, aging buckets, runrate, RIO/CWS committed quantity, BOM/cost variance, and location pivot columns in StarRocks tempdb output style.

2. typical_inv_aging_eta_rio_open_po_rds_7806.txt
   Source: US/run/rds_7806_rtv.sp
   Use when the request asks for inventory aging plus open PO ETA monthly buckets, specific location ETA splits, runrate, and RIO request allocation logic.

3. typical_inv_order_history_union_ods_qty_rds_17251.txt
   Source: US/run/rds_17251_rtv.sp
   Use when the request asks for order/current-history union logic, ship complete profile lookup, order creator/territory/customer enrichment, and ODS DW inventory quantity availability.

4. typical_inv_consignment_address_default_wh_rds_7026.txt
   Source: CA/run/rds_7026_rtv.sp
   Use when the request asks for consignment queue logic, current-vs-history order fallback, customer address lookup, default warehouse profile, and customer location handling.

5. typical_inv_dg_broad_invtype_paged_output_rds_12980.txt
   Source: US/run/rds_12980_rtv.sp
   Use when the request asks for hazardous/DG inventory extracts, broad inventory type lists, product category hierarchy, and paged output across multiple rds_tmp tables.

6. typical_inv_multisheet_dos_bo_rds_14059.txt
   Source: US/run/rds_14059_rtv.sp
   Use when the request asks for multi-sheet output, vendor on-hand/on-order inventory, BO detail, runrate-derived DOS, location pivots, and sheet config.

7. typical_inv_ship_bo_detail_serial_tracking_rds_6525.txt
   Source: CA/run/rds_6525_rtv.sp
   Use when the request asks for shipped order plus backorder detail, serial/tracking/order enrichment, customer-specific order lines, and availability fields.
```
