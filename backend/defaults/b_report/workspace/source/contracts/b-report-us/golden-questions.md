# Golden Questions Contract Header

- contract_version: v2.0.0
- artifact_type: golden-questions
- artifact_id: b-report-us
# Golden Questions - b-report-us

- Q: What is the NGM amount for 2026 Jan and Feb?
  - id: ngm-jan-feb-2026
  - A: Jan=70,272,093.1676; Feb=64,652,614.6147
  - intent: metric_comparison
  - table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - grain: date_flag_month_end company total
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-24
  - verified_shape: rows=2; columns=period_label,ngm_amt
- Q: Please show net sales YoY% for 2026 Jan.
  - id: net-sales-yoy-jan-2026
  - A: 15%
  - intent: metric_comparison
  - table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - grain: date_flag_month_end company total
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-24
  - verified_shape: rows=1; columns=yoy_pct
- Q: Top 5 vendors ranking by net sales for 2026 Jan.
  - id: jan-vendor-top5-ranking
  - A: vend_no month-end 2026-01-31 top 5 = 64956, 13208, 96432, 64036, 19534 (52390 ranks 6)
  - intent: ranking
  - table_fqn: dw_us.dws_disty_brpt_vend_mtd
  - grain: date_flag_month_end + vend_no
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-23
  - verified_shape: rows=5; columns=vend_no,vendor_name,net_sales
- Q: Revenue under PM id 735781 in 2026 Jan.
  - id: pm-735781-revenue-jan-2026
  - A: 638940.6584
  - intent: metric_lookup
  - table_fqn: dm_us.dm_disty_brpt_pm_mtd
  - grain: date_flag_month_end + pm_id
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-24
  - verified_shape: rows=1; columns=revenue
- Q: Show me negative NGM orders processed on 2026-04-30. list top 10.
  - id: negative-ngm-orders-top10
  - A: ranking intent; top 10 order lines with ngm_amt < 0 on 2026-04-30
  - intent: ranking
  - table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi
  - grain: order_no + order_line_no + date_flag
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-24
  - verified_shape: rows<=10; columns=order_no,order_line_no,cust_no,ngm_amt,date_flag
- Q: if current month is 2026-05. For master customer CDW LOGISTICS, what is net sales by each sub-customer for last month? List the top 20.
  - id: cdw-sub-customer-ranking
  - A: 16 sub-customers (April 2026 month-end); GROUP BY cust_no not cust_name
  - intent: ranking
  - table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - grain: date_flag_month_end + cust_no
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-23
  - verified_shape: rows=16; columns=cust_no,sub_customer,net_sales
- Q: tell me the revenue/margin for Part ENN-525
  - id: part-enn-525-revenue-margin
  - A: latest open month revenue and margin for part identifier ENN-525 (exact or ILIKE on part_no/mfg_partno)
  - intent: metric_lookup
  - table_fqn: dw_us.dws_disty_brpt_part_mtd
  - grain: latest month MTD through max date_flag + sku_no
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-25
  - verified_shape: rows=1; columns=revenue,margin_amt,margin_pct,period_label
- Q: tell me the revenue/margin for VPC Scanners
  - id: vpc-scanners-revenue-margin
  - A: latest open month revenue and margin for VPC/VPL label "VPC Scanners" (Phase-1 dim_pub_vpl_info then dws_disty_brpt_vpl_mtd)
  - intent: metric_lookup
  - table_fqn: dw_us.dws_disty_brpt_vpl_mtd
  - grain: latest month MTD through max date_flag + vpl_no
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-25
  - verified_shape: rows=1; columns=revenue,margin_amt,margin_pct,period_label
- Q: 请给我看一下 2026 年 CISCO 的月度销售趋势数据。
  - id: cisco-vendor-net-sales-trend-2026
  - A: monthly net_sales by period_label for CISCO vendor scope across 2026 calendar months (month-end date_flag per dim_pub_date)
  - intent: trend
  - table_fqn: dw_us.dws_disty_brpt_vend_mtd
  - grain: date_flag_month_end + vend_no (dim-scoped)
  - assembly: dim_scope_calendar_month_ends + Phase-1 dim_us.dim_pub_vendor_info vendor_scope
  - status: routing-certified
  - verified_engine: vertica
  - verified_at: 2026-06-26
  - verified_shape: rows>=1; columns=period_label,net_sales

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_comparison
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: date_flag_month_end company total
golden_ref: b-report-us#ngm-jan-feb-2026
verified_at: 2026-06-24
verified_engine: vertica
verified_shape: rows=2; columns=period_label,ngm_amt
anti_use: do not sum multiple date_flag rows within one month
-->
```sql
SELECT 'Jan-2026' AS period_label, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN (
  SELECT MAX(date_flag) AS date_flag
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
) d ON t.date_flag = d.date_flag
UNION ALL
SELECT 'Feb-2026', SUM(t.ngm_amt)
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN (
  SELECT MAX(date_flag) AS date_flag
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-02-01' AND date_flag < '2026-03-01'
) d ON t.date_flag = d.date_flag;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_comparison
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: date_flag_month_end company total
golden_ref: b-report-us#net-sales-yoy-jan-2026
verified_at: 2026-06-24
verified_engine: vertica
verified_shape: rows=1; columns=yoy_pct
anti_use: do not use order-line DWD for company YoY
-->
```sql
WITH month_ends AS (
  SELECT MAX(CASE WHEN date_flag >= '2026-01-01' AND date_flag < '2026-02-01' THEN date_flag END) AS jan26_end,
         MAX(CASE WHEN date_flag >= '2025-01-01' AND date_flag < '2025-02-01' THEN date_flag END) AS jan25_end
  FROM dim_us.dim_pub_date
)
SELECT ROUND(
  (
    SUM(CASE WHEN t.date_flag = m.jan26_end THEN t.net_sales END)
    / NULLIFZERO(SUM(CASE WHEN t.date_flag = m.jan25_end THEN t.net_sales END))
    - 1
  ) * 100,
  0
) AS yoy_pct
FROM dw_us.dws_disty_brpt_cust_mtd t
CROSS JOIN month_ends m
WHERE t.date_flag IN (m.jan26_end, m.jan25_end);
```

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_lookup
table_fqn: dm_us.dm_disty_brpt_pm_mtd
grain: date_flag_month_end + pm_id
golden_ref: b-report-us#pm-735781-revenue-jan-2026
verified_at: 2026-06-24
verified_engine: vertica
verified_shape: rows=1; columns=revenue
anti_use: do not use comb_mtd unless multi-period columns required
-->
```sql
SELECT SUM(t.net_sales) AS revenue
FROM dm_us.dm_disty_brpt_pm_mtd t
JOIN (
  SELECT MAX(date_flag) AS date_flag
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-01-01'
    AND date_flag < '2026-02-01'
) d ON t.date_flag = d.date_flag
WHERE t.pm_id = 735781;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: ranking
table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi
grain: order_line + date_flag
golden_ref: b-report-us#negative-ngm-orders-top10
verified_at: 2026-06-24
verified_engine: vertica
verified_shape: rows<=10
anti_use: order-line only; no MTD serving tables
-->
```sql
SELECT order_no, order_line_no, cust_no, ngm_amt, date_flag
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag = '2026-04-30'
  AND ngm_amt < 0
ORDER BY ngm_amt ASC
LIMIT 10;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: ranking
table_fqn: dw_us.dws_disty_brpt_cust_mtd
grain: date_flag_month_end + cust_no
golden_ref: b-report-us#cdw-sub-customer-ranking
verified_at: 2026-06-23
verified_engine: vertica
verified_shape: rows=16; columns=cust_no,sub_customer,net_sales
anti_use: do not GROUP BY cust_name; no DWD order-line for this ranking
-->
```sql
SELECT t.cust_no,
       MAX(t.cust_name) AS sub_customer,
       SUM(t.net_sales) AS net_sales
FROM dw_us.dws_disty_brpt_cust_mtd t
JOIN (
  SELECT date_flag,
         ROW_NUMBER() OVER (ORDER BY date_flag DESC) AS rn
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-04-01' AND date_flag < '2026-05-01'
) d ON t.date_flag = d.date_flag AND d.rn = 1
WHERE t.mcust_name = 'CDW LOGISTICS'
GROUP BY t.cust_no
ORDER BY net_sales DESC
LIMIT 20;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: ranking
table_fqn: dw_us.dws_disty_brpt_vend_mtd
grain: date_flag_month_end + vend_no
golden_ref: b-report-us#jan-vendor-top5-ranking
verified_at: 2026-06-23
verified_engine: vertica
verified_shape: rows=5; columns=vend_no,vendor_name,net_sales
anti_use: do not GROUP BY vend_name; month-end date_flag only
-->
```sql
SELECT t.vend_no,
       MAX(t.vend_name) AS vendor_name,
       SUM(t.net_sales) AS net_sales
FROM dw_us.dws_disty_brpt_vend_mtd t
WHERE t.date_flag = '2026-01-31'
GROUP BY t.vend_no
ORDER BY net_sales DESC
LIMIT 5;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_lookup
table_fqn: dw_us.dws_disty_brpt_part_mtd
grain: date_flag_month_start_through_latest + sku_no
golden_ref: b-report-us#part-enn-525-revenue-margin
verified_at: 2026-06-25
verified_engine: vertica
verified_shape: rows=1; columns=revenue,margin_amt,margin_pct,period_label
anti_use: do not filter sku_no with alphanumeric strings; do not use dim_sku; do not filter DWD by part_no
-->
```sql
WITH latest_period AS (
  SELECT DATE_TRUNC('MONTH', MAX(date_flag)) AS month_start
  FROM dim_us.dim_pub_date
),
part_scope AS (
  SELECT sku_no, part_no, mfg_partno
  FROM dim_us.dim_pub_part_info
  WHERE part_no = 'ENN-525'
     OR mfg_partno = 'ENN-525'
     OR part_no ILIKE '%ENN-525%'
     OR mfg_partno ILIKE '%ENN-525%'
  LIMIT 20
)
SELECT SUM(t.net_sales) AS revenue,
       SUM(t.ngm_amt) AS margin_amt,
       ROUND(SUM(t.ngm_amt) / NULLIFZERO(SUM(t.net_sales)) * 100, 2) AS margin_pct,
       TO_CHAR(MAX(t.date_flag), 'YYYY-MM') AS period_label
FROM dw_us.dws_disty_brpt_part_mtd t
JOIN part_scope p ON t.sku_no = p.sku_no
CROSS JOIN latest_period lp
WHERE t.date_flag >= lp.month_start;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_lookup
table_fqn: dw_us.dws_disty_brpt_vpl_mtd
grain: date_flag_month_start_through_latest + vpl_no
golden_ref: b-report-us#vpc-scanners-revenue-margin
verified_at: 2026-06-25
verified_engine: vertica
verified_shape: rows=1; columns=revenue,margin_amt,margin_pct,period_label
anti_use: do not join dim_pub_vpl_hierarchy_info; do not use vpl_id or vpl_name; do not filter vpl_no with alphanumeric strings
-->
```sql
WITH latest_period AS (
  SELECT DATE_TRUNC('MONTH', MAX(date_flag)) AS month_start
  FROM dw_us.dws_disty_brpt_vpl_mtd
),
vpl_scope AS (
  SELECT vpl_no, vpl_code, vpl_desc, vpc_group_desc
  FROM dim_us.dim_pub_vpl_info
  WHERE vpc_group_desc ILIKE '%Scanner%'
     OR vpl_desc ILIKE '%Scanner%'
     OR vpl_code ILIKE '%Scanner%'
     OR vpc_group_desc ILIKE '%VPC Scanners%'
     OR vpl_desc ILIKE '%VPC Scanners%'
  LIMIT 200
)
SELECT SUM(t.net_sales) AS revenue,
       SUM(t.ngm_amt) AS margin_amt,
       ROUND(SUM(t.ngm_amt) / NULLIFZERO(SUM(t.net_sales)) * 100, 2) AS margin_pct,
       TO_CHAR(MAX(t.date_flag), 'YYYY-MM') AS period_label
FROM dw_us.dws_disty_brpt_vpl_mtd t
JOIN vpl_scope v ON t.vpl_no = v.vpl_no
CROSS JOIN latest_period lp
WHERE t.date_flag >= lp.month_start;
```

<!-- sql-artifact
snippet_type: routing_certified
intent: trend
table_fqn: dw_us.dws_disty_brpt_vend_mtd
grain: date_flag_month_end + vend_no (dim-scoped)
golden_ref: b-report-us#cisco-vendor-net-sales-trend-2026
verified_at: 2026-06-26
verified_engine: vertica
verified_shape: rows>=1; columns=period_label,net_sales
anti_use: do not filter month_no as YYYYMM; do not LIMIT 1 vendor row; do not sum multiple date_flag within one month
-->
```sql
WITH month_ends AS (
  SELECT MAX(date_flag) AS date_flag
  FROM dim_us.dim_pub_date
  WHERE date_flag >= '2026-01-01' AND date_flag <= '2026-12-31'
  GROUP BY DATE_TRUNC('month', date_flag)
),
vendor_scope AS (
  SELECT vend_no, vend_name, master_vend_name, universal_vend_name, cis_mk_name, pur_vend_name
  FROM dim_us.dim_pub_vendor_info
  WHERE vend_name = 'CISCO'
     OR vend_name ILIKE '%CISCO%'
     OR master_vend_name = 'CISCO'
     OR master_vend_name ILIKE '%CISCO%'
     OR universal_vend_name ILIKE '%CISCO%'
     OR cis_mk_name ILIKE '%CISCO%'
     OR pur_vend_name ILIKE '%CISCO%'
  ORDER BY CASE WHEN UPPER(vend_name) = UPPER('CISCO') THEN 0 ELSE 1 END,
           CASE WHEN UPPER(master_vend_name) = UPPER('CISCO') THEN 0 ELSE 1 END,
           CASE WHEN UPPER(universal_vend_name) = UPPER('CISCO') THEN 0 ELSE 1 END,
           CASE WHEN UPPER(cis_mk_name) = UPPER('CISCO') THEN 0 ELSE 1 END,
           CASE WHEN UPPER(pur_vend_name) = UPPER('CISCO') THEN 0 ELSE 1 END
  LIMIT 200
)
SELECT TO_CHAR(t.date_flag, 'YYYY-MM') AS period_label,
       SUM(t.net_sales) AS net_sales
FROM dw_us.dws_disty_brpt_vend_mtd t
JOIN vendor_scope s ON t.vend_no = s.vend_no
JOIN month_ends m ON t.date_flag = m.date_flag
GROUP BY period_label
ORDER BY period_label;
```
