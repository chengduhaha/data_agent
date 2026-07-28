# Examples index — `vertica_rma`

- artifact_type: examples-index
- artifact_id: rds/vertica_rma/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical Vertica RMA example reports

1. typical_rma_gfs_prophet_sitetran_repair_movement_rds_1214.txt
   Source: MX/run/rds_1214_rtv.sp
   Use when the request asks for Prophet SITETRAN, GFS defective inventory return movement, repair yield, defective-to-repair transaction history, forced repair-center site logic, monthly transaction output, or SF_ORD_NO profile linkage.

2. typical_rma_detail_shipment_status_multisheet_rds_16483.txt
   Source: US/run/rds_16483_rtv.sp
   Use when the request asks for RMA authorization/receipt detail, original SO and CPO fields, hardcoded SKU-list RMA extracts, shipment status as a second worksheet, or rdsetl multi-sheet output using rdsetl.rds_tmp_2 and rdsetl.rds_tmp_sheet_config.

3. typical_rma_tracking_freight_reconciliation_rds_18121.txt
   Source: US/run/rds_18121_rtv.sp
   Use when the request asks for RMA tracking reconciliation, freight/non-order freight detail, vend_segment-based RMA tracking filters, report_week freight snapshots, or fuzzy tracking matching using rma_track_no LIKE '%' || track_no_like || '%'.
```
