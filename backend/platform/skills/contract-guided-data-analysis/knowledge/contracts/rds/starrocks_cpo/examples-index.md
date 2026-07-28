# Examples index — `starrocks_cpo`

- artifact_type: examples-index
- artifact_id: rds/starrocks_cpo/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical StarRocks CPO example reports

1. typical_cpo_open_order_eta_ship_complete_contacts_rds_6560.txt
   Source: CA/run/rds_6560_rtv.sp
   Use when the request asks for open order lines tied to CPO, UniETA min ETA, ship-complete order profile, order type/status, customer address/contact enrichment, territory/division lookup, VPL/vendor filters, and location/preferred warehouse logic.

2. typical_cpo_current_history_sparef_eu_contact_rds_10106.txt
   Source: US/run/rds_10106_rtv.sp
   Use when the request asks for current plus history CPO union, SPAREF# profile, SPL/open probability, VPL/vendor enrichment, master customer fallback, reseller address/contact/email enrichment, sales territory email fallback, and EU common end-user fields.

3. typical_cpo_dropship_mso_vpo_sso_contract_ot125_rds_17067.txt
   Source: US/run/rds_17067_rtv.sp
   Use when the request asks for drop-ship CPO logic, MSO/VPO/SSO chained order linkage, RESERVEVPO reservation flag, CONTRNO profile, OT125 billing entry, service-contract-like CPO lines, VPC group/VPG enrichment, EU common fallback, and gross margin calculations from order or billing amounts.

4. typical_cpo_cedm_quote_expire_custmsrp_rds_17362.txt
   Source: US/run/rds_17362_rtv.sp
   Use when the request asks for CUSTMSRP line profile, Quote Expire Date from CPO EU custom tables, CEDM list-box mapping through EU custom map, staging SKU/vendor filters, and compact quote output.

5. typical_cpo_active_pipeline_custmsrp_sparef_rds_19304.txt
   Source: US/run/rds_19304_rtv.sp
   Use when the request asks for active quote pipeline filters using cpo_status, CRM pipeline quote stage, VPL/product/customer/territory enrichment, extended quoted cost, CUSTMSRP extended list price, SPAREF# SPA reference, and split profile extraction over long date windows.

6. typical_cpo_order_status_eta_hideampl_expense_rds_19257.txt
   Source: US/run/rds_19257_rtv.sp
   Use when the request asks for order/history union around CPO-backed order status, drop-ship order type labeling, max UniETA per order line, HIDEAMPL-controlled AMPL expense inclusion, DP expense aggregation, net sales recalculation, end-user PO fallback, and backfilling CPO from VPO/MSO references.

7. typical_cpo_service_contract_global_employee_rds_18916.txt
   Source: US/run/rds_18916_rtv.sp
   Use when the request asks for service contract / type 125 logic, global employee and global location enrichment, current/history order unions, inventory transaction-based order inclusion, sentinel placeholder values for non-order contract rows, from_ref_type descriptions, rep grouping by location/job/cost center, and CPO entry user fallback.
```
