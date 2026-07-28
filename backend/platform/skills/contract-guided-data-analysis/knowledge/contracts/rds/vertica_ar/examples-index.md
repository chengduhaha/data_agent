# Examples index — `vertica_ar`

- artifact_type: examples-index
- artifact_id: rds/vertica_ar/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
Typical Vertica AR example reports

1. typical_ar_open_aging_customer_activity_credit_limit_rds_11417.txt
   Source: US/run/rds_11417_rtv.sp
   Use when the request asks for comprehensive open AR aging by customer, current open AR from dwd_disty_ar_cust_doc_df, 12-month customer sales, recent 60-day POS sales/DSO, collector hierarchy, customer terms, customer contact enrichment, finance master, credit limit aggregation, or credit-limit exclusion rules.

2. typical_ar_long_aged_365_500_multisheet_rds_9041.txt
   Source: CA/run/rds_9041_rtv.sp
   Use when the request asks for long-aged AR, 365+ aging detail, 500+ aging detail, collector and sales territory exclusions, open/full-short open document status, document reference fields, or multi-sheet AR output using rdsetl.rds_tmp and rdsetl.rds_tmp_2.

3. typical_ar_customer_balance_30day_average_rds_18804.txt
   Source: US/run/rds_18804_rtv.sp
   Use when the request asks for customer total AR balance from ODS customer documents plus last 30 days average AR balance from dws_disty_ar_cust_sum_age_df, customer-level AR summary, view_level/data_period filters, or simple customer balance output.

4. typical_ar_discount_payment_timing_rds_19383.txt
   Source: US/run/rds_19383_rtv.sp
   Use when the request asks for early payment discount, discount eligibility, grace period from list box, terms discount days/percent, payment/application joins, payment month versus document month comparison, or summary/detail two-sheet discount reporting.

5. typical_ar_pos_rma_credit_reason_trace_rds_5576.txt
   Source: CA/run/rds_5576_rtv.sp
   Use when the request asks for POS/RMA credit tracing, original SO and original customer PO recovery, RMA reference through int_ref_type = 9, history header enrichment, AR customer document credit reason, or order-level AR credit context.
```
