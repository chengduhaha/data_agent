# Examples index — `vertica_vpo`

- artifact_type: examples-index
- artifact_id: rds/vertica_vpo/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical Vertica VPO example reports

1. typical_vpo_recent_closed_po_prodcode_rds_9751.txt
   Source: US/run/rds_9751_rtv.sp
   Use when the request asks for recently closed PO/VPO rows from dwd_disty_common_po_basic, prod_code-specific PO extracts, closed_date rolling windows with month-start exception, payment/currency/confirmation fields, and simple rdsetl output.

2. typical_vpo_ap_balance_open_po_rds_16242.txt
   Source: US/run/rds_16242_rtv.sp
   Use when the request asks for vendor AP balance, AP aging by sum_level and terms_no, analyst enrichment, AP hold/payment-hold fields, open PO exposure by vendor, accrual/debit balance formulas, and AP/vendor financial filtering.

3. typical_vpo_open_po_status_customer_part_carton_rds_16874.txt
   Source: US/run/rds_16874_rtv.sp
   Use when the request asks for open VPO/order_type 2 detail, order_qty vs rec_qty, order status from order header dates, scheduled/actual ship and arrival dates, customer part number, carton/tracking context, ship-to fields, and vendor-specific open PO output.

4. typical_vpo_open_po_scm_spa_ref_rds_17736.txt
   Source: US/run/rds_17736_rtv.sp
   Use when the request asks for current-month VPO release detail, line_delete_date filtering, SCM/SPA reference lookup from shipped order SCM/SPA detail, and keeping only the first SPA/SCM row per PO line with row_number().

5. typical_vpo_pos_doc_fallback_cedm_serial_rds_610.txt
   Source: MX/run/rds_610_rtv.sp
   Use when the request asks for shipped POS rows tied to VPO, CEDM DEAL ID from EU custom map/list box, customer address/contact de-duplication, SCM/SPA lookup, multi-step vend_inv_no fallback through PO basic/AP hold/vend_doc, serial/asset-tag branching, and region-specific WCLA schema logic.

6. typical_vpo_inventory_open_dropship_pos_qty_rds_18517.txt
   Source: US/run/rds_18517_rtv.sp
   Use when the request asks for SKU/vendor inventory comparison, on-hand/on-order quantity and extended value, open dropship PO quantity from to_loc_no = 98, prior/month-to-date/year-to-date POS shipped quantities, and product-list filtering by mfg_partno.
```
