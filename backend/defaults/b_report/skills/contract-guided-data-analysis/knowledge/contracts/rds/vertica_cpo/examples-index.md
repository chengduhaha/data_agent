# Examples index — `vertica_cpo`

- artifact_type: examples-index
- artifact_id: rds/vertica_cpo/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Vertica CPO typical examples index

Use these examples as implementation references when generating Vertica CPO SQL. Load the CPO reference files first, then open the closest example only when the requested report matches the business pattern.

1. typical_cpo_open_emailquote_cart_inventory_rds_14943.txt
   Source: US/run/rds_14943_rtv.sp
   Use when the request needs open CPO lines enriched with product/customer/contact fields, EMAILQUOTE profile logic, e-commerce cart current/history linkage, or CPO-to-cart matching.

2. typical_cpo_pos_open_close_vendor_quote_rds_18556.txt
   Source: US/run/rds_18556_rtv.sp
   Use when the request compares shipped POS/order data with open and closed CPO facts, includes SPA fields, or extracts Vendor Quote ID from order extended/custom fields.

3. typical_cpo_bto_special_handling_lab_rds_6481.txt
   Source: CA/run/rds_6481_rtv.sp
   Use when the request needs order/CPO linkage through CIS order header/detail, BTO special handling flags, CWS lab hold or inbound timestamps, or multi-sheet RDS output.

4. typical_cpo_order_eu_custom_bom_vpo_rds_14893.txt
   Source: US/run/rds_14893_rtv.sp
   Use when the request links CPO to sales orders and EU custom fields, especially DPAS/custom data, BOM/VPO-style enrichment, or open plus closed CPO union logic by order reference.

5. typical_cpo_deleted_cancelled_comments_rds_9874.txt
   Source: US/run/rds_9874_rtv.sp
   Use when the request focuses on deleted/cancelled closed CPO lines, delete user/date, cancellation comments, or recent deletion windows.

6. typical_cpo_recent_open_customer_product_rds_10295.txt
   Source: US/run/rds_10295_rtv.sp
   Use when the request is a simpler recent open CPO extract with product/customer enrichment and order reference fields.

7. typical_cpo_order_profile_expected_dates_rds_9676.txt
   Source: US/run/rds_9676_rtv.sp
   Use when the request needs expected ship or delivery dates from current/history CPO profile tables, CPO ship quantity, and order linkage.
```
