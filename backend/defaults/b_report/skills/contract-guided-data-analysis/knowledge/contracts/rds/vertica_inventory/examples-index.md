# Examples index — `vertica_inventory`

- artifact_type: examples-index
- artifact_id: rds/vertica_inventory/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical Vertica Inventory example reports

1. typical_inv_aging_qty_runrate_so_alloc_rds_17345.txt
   Source: US/run/rds_17345_rtv.sp
   Use when the request asks for SKU/vendor inventory aging quantity buckets, on-hand/on-order/BO/allocation, available quantity, runrate, SO allocated quantity, and location pivot columns.

2. typical_inv_rollover_true_aging_rds_10968.txt
   Source: US/run/rds_10968_rtv.sp
   Use when the request asks for vendor/VPL level rollover aging, true aging, 240+/360+ metrics, cost amount metrics, and ownership hierarchy enrichment.

3. typical_inv_rio_cws_location_rds_6800.txt
   Source: CA/run/rds_6800_rtv.sp
   Use when the request asks for a comprehensive inventory availability report with RIO/CWS committed quantity, location-level quantity, kit/S&A handling, and CA-style location mapping.

4. typical_inv_ap_hold_availability_rds_19106.txt
   Source: US/run/rds_19106_rtv.sp
   Use when the request asks for AP hold or blocked PO lines with current availability from inventory quantity.

5. typical_inv_rollover_witypestu_stock_rotation_rds_11722.txt
   Source: US/run/rds_11722_rtv.sp
   Use when the request asks for 90+ rollover aging, WITYPESTU runrate, stock rotation/list-box lookup, or special location-filtered runrate logic.

6. typical_inv_aging_qty_runrate_so_alloc_rds_17343.txt
   Source: US/run/rds_17343_rtv.sp
   Use when the request asks for SKU/vendor inventory aging quantity buckets, on-hand/on-order/BO/allocation, available quantity, runrate, and location pivot columns similar to report 17345.

7. typical_inv_aging_qty_vendor_filter_rds_17484.txt
   Source: US/run/rds_17484_rtv.sp
   Use when the request asks for vendor-filtered inventory aging quantity with SKU list and location-level quantity aggregation.

8. typical_inv_upc_part_aging_qty_rds_19269.txt
   Source: US/run/rds_19269_rtv.sp
   Use when the request asks for UPC/part-prefix driven SKU selection and inventory aging quantity output.

9. typical_inv_aging_qty_runrate_rio_alloc_rds_18605.txt
   Source: US/run/rds_18605_rtv.sp
   Use when the request asks for inventory aging quantity, runrate, RIO allocation quantity, and available quantity at SKU/inv_type grain.

10. typical_inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.txt
    Source: user-provided US inventory example (vendor 13208)
    Use when the request asks for comprehensive US inventory quantity, aging, runrate, RIO allocation, customer enrichment, and location pivot output without a single historical RTV source file in-repo.
```
