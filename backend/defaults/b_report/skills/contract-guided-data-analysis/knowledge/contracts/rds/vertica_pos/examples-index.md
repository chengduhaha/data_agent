# Examples index — `vertica_pos`

- artifact_type: examples-index
- artifact_id: rds/vertica_pos/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Vertica POS typical examples index

Use these examples as implementation references when generating Vertica POS SQL. Load the POS reference files first, then open the closest example only when the requested report matches the business pattern.

1. typical_pos_spa_scm_claim_rds_5380.txt
   Source: US/run/rds_5380_rtv.sp
   Use when the request needs POS lines with SPA/SCM expense, claim logic, or multi-expense enrichment on shipped order lines.

2. typical_pos_serial_authorization_rds_5378.txt
   Source: US/run/rds_5378_rtv.sp
   Use when the request needs serial number, authorization, or shipped-line detail enrichment on POS output.

3. typical_pos_rma_original_order_rds_5569.txt
   Source: US/run/rds_5569_rtv.sp
   Use when the request links RMA or return POS activity back to the original order and order-line context.

4. typical_pos_sales_credit_protection_rds_7720.txt
   Source: US/run/rds_7720_rtv.sp
   Use when the request needs sales credit protection, customer credit context, or related POS/customer enrichment.

5. typical_pos_bo_shipping_multisheet_rds_9127.txt
   Source: US/run/rds_9127_rtv.sp
   Use when the request combines POS/shipping context with backorder or multi-sheet RDS output patterns.

6. typical_pos_spa_horizontal_rds_16358.txt
   Source: US/run/rds_16358_rtv.sp
   Use when the request needs POS order lines with up to three SPA groups horizontally expanded into repeated column groups.

7. typical_pos_spa_scm_horizontal_rds_18213.txt
   Source: US/run/rds_18213_rtv.sp
   Use when the request needs POS order lines with multiple SPA/SCM expense groups horizontally expanded on the same line.

8. typical_pos_scm_reference_hierarchy_rds_17482.txt
   Source: US/run/rds_17482_rtv.sp
   Use when the request needs POS output filtered by sales/PM/BD hierarchy and enriched with SCM reference logic.

9. typical_pos_vendor_mso_po_rds_17785.txt
   Source: US/run/rds_17785_rtv.sp
   Use when the request needs vendor-filtered POS output with MSO/PO/CPO linkage fields.

10. typical_pos_scm_reference_hierarchy_rds_8329.txt
    Source: CA/run/rds_8329_rtv.sp
    Use when the request needs CA POS output filtered by sales/PM/BD hierarchy and enriched with SCM reference logic.
```
