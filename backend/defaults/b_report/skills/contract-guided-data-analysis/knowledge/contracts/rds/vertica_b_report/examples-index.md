# Examples index — `vertica_b_report`

- artifact_type: examples-index
- artifact_id: rds/vertica_b_report/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical Vertica B REPORT example reports

1. typical_b_report_vpc_vpl_pl_profit_rds_802.txt
   Source: CA/run/rds_802_rtv.sp
   Use when the request asks for VPC/VPL product-line population logic, VPC group and VPL union rules, BRPT group-style product filters, PL order-line sales, net sales from ship quantity and unit price/expense, NGM/OPLGM amount and percentage, customer/product/vendor/VPL profitability, or curated vendor/product-line inclusion and exclusion rules.

2. typical_b_report_monthly_pl_summary_rds_5540.txt
   Source: CA/run/rds_5540_rtv.sp
   Use when the request asks for monthly or MTD B REPORT PL summary from dws_disty_brpt_pl_extend_mtd, date-list driven monthly aggregation, sales/PM/territory hierarchy enrichment, GM/TGM/NGM/OPL metrics, or summarized B REPORT output rather than order-line detail.

3. typical_b_report_ai_recommendation_attribution_rds_8328.txt
   Source: CA/run/rds_8328_rtv.sp
   Use when the request asks for AI/e-catalog recommendation attribution, SMB recommendation source, pre/post email sales windows, customer/SKU exclusion based on prior sales, BY AI prioritization, row_number de-duplication by order line, recommendation source parsing, or attributed sales and NGM reporting.

4. typical_b_report_qtd_new_hw_product_rds_9196.txt
   Source: CA/run/rds_9196_rtv.sp
   Use when the request asks for QTD new hardware product reporting, fiscal-quarter date window logic, new part create date rules, hardware-only filters, SYNNEX vendor exclusions with SYNNEX WW exception, ASC606 and renewal flags, product hierarchy, or QTD PL sales/cost by SKU.

5. typical_b_report_acq_cloud_legacy_invoice_rds_1241.txt
   Source: MX/run/rds_1241_rtv.sp
   Use when the request asks for acquisition/cloud order reporting, ACQCLOUD profile logic, legacy invoice number from ACQINVNO, Cloud classification using order_type 125 or profile rows, WCLA/MX regional PL detail, sales detail enrichment, sales hierarchy/customer/vendor context, or SCM claim type enrichment.

6. typical_b_report_lightweight_orders_inventory_rio_rds_7500.txt
   Source: US/run/rds_7500_rtv.sp
   Use when the request asks for lightweight order extension from dwd_disty_pub_dw_orders_extend_di, recent order runrate, stocking versus drop-ship split by from_loc_no, inventory aging and inventory quantity context, RIO request demand, Dell/runrate style SKU metrics, or cross-domain B REPORT inventory/RIO output.
```
