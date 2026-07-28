# Examples index — `starrocks_vpo`

- artifact_type: examples-index
- artifact_id: rds/starrocks_vpo/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical StarRocks VPO example reports

1. typical_vpo_inventory_open_po_eta_rio_runrate_rds_7806.txt
   Source: US/run/rds_7806_rtv.sp
   Use when the request asks for inventory plus VPO/open PO ETA monthly buckets, order_type = 2 ETA detail, location-specific ETA splits, inventory aging, RIO hold quantity, allocation adjustment, runrate, and StarRocks tempdb primary key / distributed table style.

2. typical_vpo_cpo_mso_vpo_sso_contract_ot125_rds_17067.txt
   Source: US/run/rds_17067_rtv.sp
   Use when the request asks for CPO to MSO/VPO/SSO chained order linkage, VPO order_type = 2 int_ref relationships, drop-ship flags, RESERVEVPO profile, CONTRNO profile, OT125 billing entry, VPC group/VPG enrichment, EU common fallback, and gross margin from order or billing amounts.

3. typical_vpo_open_po_vendor_so_quote_etasrc_rds_18013.txt
   Source: US/run/rds_18013_rtv.sp
   Use when the request asks for open VPO lines from order_header/order_detail, open_qty = order_qty - rec_qty, vendor buyer from vend_user_matrix, Vendor SO fallback from SAPID profile or ETA code vend_so_no, Vendor Quote ID from CEDM EU custom, and ETA source from ETASRC profile plus SRC list box.

4. typical_vpo_simple_open_po_customer_rds_19380.txt
   Source: US/run/rds_19380_rtv.sp
   Use when the request asks for a compact open VPO extract with order_type = 2, delete filters, order_qty/rec_qty/open_qty, product filtering by vendor, CPO/customer PO fallback from int_ref, and customer name enrichment.

5. typical_vpo_current_history_open_po_vendor_so_rds_19401.txt
   Source: US/run/rds_19401_rtv.sp
   Use when the request asks for current plus history VPO open order union, vendor buyer enrichment, Vendor SO fallback from current/history SAPID profile and ETA code tables, CPO/customer enrichment, and fixed date-window filtering.

6. typical_vpo_eta_detail_current_history_region_rds_100791.txt
   Source: UK/run/rds_100791_rtv.sp
   Use when the request asks for regional/non-RT order ETA detail, current plus history ETA union, order_type = 2, order detail to part master lookup, manager/login enrichment, tracking number, and lightweight VPO ETA output.
```
