# Examples index — `vertica_ap`

- artifact_type: examples-index
- artifact_id: rds/vertica_ap/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical Vertica AP example reports

1. typical_ap_vouched_unvouched_multisheet_rds_10353.txt
   Source: BR/run/rds_10353_rtv.sp
   Use when the request asks for AP vouched versus unvouched separation, VDAH line detail, USD-only AP detail, ODS AP hold / vendor document enrichment, or multi-sheet AP output using rdsetl.rds_tmp_2 and rdsetl.rds_tmp_sheet_config.

2. typical_ap_dm_dnd_aging_detail_rds_1299.txt
   Source: CA/run/rds_1299_rtv.sp
   Use when the request asks for AP debit memo / VCM debit memo separation, DND or DM vendor flags, OLD_COMP profile enrichment, AP aging detail, negative aged AP detail, uv_type-based invoice/order display logic, or order_type = 27 claim fields.

3. typical_ap_forecast_payment_receipt_open_po_rds_1545.txt
   Source: CA/run/rds_1545_rtv.sp
   Use when the request asks for AP forecast payment, actual payment MTD, open payment, open PO, receipt/QTD receipt, AP total, sales goal, MTD sales/cost, first-day-of-month payment window logic, or vendor-level forecast staging.

4. typical_ap_month_end_position_terms_bucket_rds_3977.txt
   Source: CA/run/rds_3977_rtv.sp
   Use when the request asks for prior-month AP position, latest snapshot before current month, AP total split into unvouched debits, TB, accruals, USD/CAD parallel calculations, or terms_no / sum_level based AP bucket construction.

5. typical_ap_multiregion_aging_detail_rds_8443.txt
   Source: HY/run/rds_8443_rtv.sp
   Use when the request asks for multi-region AP aging across HYUS/HYUK/HYCN/HYWW, Region-discriminated UNION ALL logic, AP aging header and detail together, vendor xref relationship mapping, payment/application adjustment by doc_no, local versus FX amount mode, or AP detail de-duplication.

6. typical_ap_average_balance_multisheet_rds_9163.txt
   Source: CA/run/rds_9163_rtv.sp
   Use when the request asks for monthly average AP balance, daily snapshot average divided by days in month, AP/AR/Inventory workbook tabs, inventory aging by vendor/SKU, or cross-domain multi-sheet output where AP, AR, and inventory grains remain separate.
```
