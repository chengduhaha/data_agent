# B Report US Golden Evaluation Cases

**Source:** `source/contracts/b-report-us/eval/golden_cases.yaml`

## Dataset metadata

| Field | Value |
|-------|-------|
| contract_version | v1 |
| knowledge_pack | b-report-us |
| dataset_name | b-report-us-golden-v2 |
| case_count | 31 |

## Case index

| ID | Intent | Status | Table FQN | Question |
|----|--------|--------|-----------|----------|
| ngm-jan-feb-2026 | metric_comparison | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | What is the NGM amount for 2026 Jan and Feb? |
| net-sales-yoy-jan-2026 | metric_comparison | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Please show net sales YoY% for 2026 Jan. |
| jan-vendor-top5-ranking | ranking | routing-certified | `dw_us.dws_disty_brpt_vend_mtd` | Top 5 vendors ranking by net sales for 2026 Jan. |
| pm-735781-revenue-jan-2026 | metric_lookup | routing-certified | `dm_us.dm_disty_brpt_pm_mtd` | What is the revenue under pm id 735781 in 2026 Jan |
| negative-ngm-orders-top10 | ranking | routing-certified | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | Show me negative NGM orders processed on 2026-04-30. list top 10. |
| cdw-sub-customer-ranking | ranking | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | if current month is 2026-05.For master customer: CDW LOGISTICS, what is net s... |
| part-enn-525-revenue-margin | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_part_mtd` | tell me the revenue/margin for Part ENN-525 |
| vpc-scanners-revenue-margin | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_vpl_mtd` | tell me the revenue/margin for VPC Scanners |
| cisco-vendor-net-sales-trend-2026 | trend | routing-certified | `dw_us.dws_disty_brpt_vend_mtd` | 请给我看一下 2026 年 CISCO 的月度销售趋势数据。 |
| retail-scanner-margin-holdout | metric_lookup | hold-out | `dw_us.dws_disty_brpt_vpl_mtd` | what is the margin for Retail Scanner |
| vpl-code-scan-holdout | metric_lookup | hold-out | `dw_us.dws_disty_brpt_vpl_mtd` | revenue for vpl code SCAN |
| net-sales-feb-2026-scalar | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | What is net sales for Feb 2026? |
| ngm-mar-2026-scalar | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | NGM for March 2026? |
| gross-sales-q1-2026 | metric_comparison | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Gross sales for Q1 2026? |
| vendor-top3-feb-2026 | ranking | routing-certified | `dw_us.dws_disty_brpt_vend_mtd` | Top 3 vendors by net sales in Feb 2026 |
| customer-top5-feb-2026 | ranking | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Top 5 customers by net sales Feb 2026 |
| pm-top5-ngm-feb-2026 | ranking | routing-certified | `dw_us.dm_disty_brpt_pm_mtd` | Top 5 PM by NGM Feb 2026 |
| dell-vendor-sales-feb-2026 | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_vend_mtd` | Dell net sales Feb 2026 |
| hp-vendor-ngm-feb-2026 | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_vend_mtd` | HP NGM Feb 2026 |
| trend-net-sales-2026 | trend | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Monthly net sales trend for 2026 |
| trend-ngm-2026 | trend | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Monthly NGM trend 2026 |
| yoy-net-sales-feb-2026 | metric_comparison | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Net sales YoY for Feb 2026 |
| margin-pct-feb-2026 | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Margin percent Feb 2026 |
| vpc-breakdown-feb-2026 | diagnostic_slice | routing-certified | `dw_us.dws_disty_brpt_vpl_mtd` | Net sales by VPC group Feb 2026 |
| vpl-breakdown-feb-2026 | diagnostic_slice | routing-certified | `dw_us.dws_disty_brpt_vpl_mtd` | Net sales by VPL Feb 2026 |
| territory-top5-feb-2026 | ranking | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Top 5 territories by net sales Feb 2026 |
| part-top5-sales-feb-2026 | ranking | routing-certified | `dw_us.dws_disty_brpt_part_mtd` | Top 5 parts by net sales Feb 2026 |
| order-line-ngm-negative | ranking | routing-certified | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | Orders with negative NGM Feb 2026 top 10 |
| cisco-trend-2026-holdout | trend | routing-certified | `dw_us.dws_disty_brpt_vend_mtd` | CISCO monthly revenue trend 2026 |
| scanner-category-lookup | metric_lookup | routing-certified | `dw_us.dws_disty_brpt_vpl_mtd` | VPC Scanners revenue Feb 2026 |
| unsupported-forecast | unsupported | routing-certified | `dw_us.dws_disty_brpt_cust_mtd` | Forecast next year revenue without data |

## Case details

### ngm-jan-feb-2026

| Field | Value |
|-------|-------|
| question | What is the NGM amount for 2026 Jan and Feb? |
| intent | metric_comparison |
| golden_ref | b-report-us#ngm-jan-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_cust_mtd`, `ngm_amt`, `dim_pub_date`

**Certified SQL**

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

### net-sales-yoy-jan-2026

| Field | Value |
|-------|-------|
| question | Please show net sales YoY% for 2026 Jan. |
| intent | metric_comparison |
| golden_ref | b-report-us#net-sales-yoy-jan-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-01-31 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_cust_mtd`, `net_sales`, `yoy_pct`
- sql_shape.must_not_contain: `dwd_disty_brpt_orders_pl_etl_mi`

**Certified SQL**

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

### jan-vendor-top5-ranking

| Field | Value |
|-------|-------|
| question | Top 5 vendors ranking by net sales for 2026 Jan. |
| intent | ranking |
| golden_ref | b-report-us#jan-vendor-top5-ranking |
| table_fqn | dw_us.dws_disty_brpt_vend_mtd |
| status | routing-certified |
| snapshot_date | 2026-01-31 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_vend_mtd`, `vend_no`, `GROUP BY`
- sql_shape.must_not_contain: `GROUP BY vend_name`
- sql_shape.group_by_key: `vend_no`
- result_shape: min_rows=1, max_rows=5

**Certified SQL**

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

### pm-735781-revenue-jan-2026

| Field | Value |
|-------|-------|
| question | What is the revenue under pm id 735781 in 2026 Jan |
| intent | metric_lookup |
| golden_ref | b-report-us#pm-735781-revenue-jan-2026 |
| table_fqn | dm_us.dm_disty_brpt_pm_mtd |
| status | routing-certified |
| snapshot_date | 2026-01-31 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`
- entity_filters:
  - pm_id: `735781`

**Assertions**

- sql_shape.must_contain: `dm_disty_brpt_pm_mtd`, `pm_id`, `735781`
- numeric: column=`revenue`, expected=`638940.6584`, tolerance=`0.01`

**Certified SQL**

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

### negative-ngm-orders-top10

| Field | Value |
|-------|-------|
| question | Show me negative NGM orders processed on 2026-04-30. list top 10. |
| intent | ranking |
| golden_ref | b-report-us#negative-ngm-orders-top10 |
| table_fqn | dw_us.dwd_disty_brpt_orders_pl_etl_mi |
| status | routing-certified |
| snapshot_date | 2026-04-30 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `dwd_disty_brpt_orders_pl_etl_mi`, `ngm_amt`, `< 0`, `LIMIT 10`, `2026-04-30`
- result_shape: min_rows=1, max_rows=10

**Certified SQL**

```sql
SELECT order_no, order_line_no, cust_no, ngm_amt, date_flag
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag = '2026-04-30'
  AND ngm_amt < 0
ORDER BY ngm_amt ASC
LIMIT 10;
```

### cdw-sub-customer-ranking

| Field | Value |
|-------|-------|
| question | if current month is 2026-05.For master customer: CDW LOGISTICS, what is net sales by each sub-customer for last month? List the top 20 |
| intent | ranking |
| golden_ref | b-report-us#cdw-sub-customer-ranking |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-04-30 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_cust_mtd`, `mcust_name`, `GROUP BY`
- sql_shape.must_not_contain: `GROUP BY cust_name`, `dwd_disty_brpt_orders_pl_etl_mi`
- sql_shape.group_by_key: `cust_no`
- result_shape: min_rows=1, max_rows=20

**Certified SQL**

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

### part-enn-525-revenue-margin

| Field | Value |
|-------|-------|
| question | tell me the revenue/margin for Part ENN-525 |
| intent | metric_lookup |
| golden_ref | b-report-us#part-enn-525-revenue-margin |
| table_fqn | dw_us.dws_disty_brpt_part_mtd |
| status | routing-certified |
| snapshot_date | 2026-06-20 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`, `ngm_amt`
- entity_filters:
  - part_identifier: `ENN-525`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_part_mtd`, `dim_pub_part_info`, `part_no`, `net_sales`, `ngm_amt`, `ILIKE`
- sql_shape.must_not_contain: `dim_sku`, `sku_no = 'ENN-525'`, `sku_no::varchar`

**Certified SQL**

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

### vpc-scanners-revenue-margin

| Field | Value |
|-------|-------|
| question | tell me the revenue/margin for VPC Scanners |
| intent | metric_lookup |
| golden_ref | b-report-us#vpc-scanners-revenue-margin |
| table_fqn | dw_us.dws_disty_brpt_vpl_mtd |
| status | routing-certified |
| snapshot_date | 2026-06-23 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`, `ngm_amt`
- entity_filters:
  - vpc_group_label: `Scanners`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_vpl_mtd`, `dim_pub_vpl_info`, `net_sales`, `ngm_amt`, `latest_period`
- sql_shape.must_not_contain: `vpl_id`, `vpl_name`, `dim_pub_vpl_hierarchy_info`

**Certified SQL**

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

### cisco-vendor-net-sales-trend-2026

| Field | Value |
|-------|-------|
| question | 请给我看一下 2026 年 CISCO 的月度销售趋势数据。 |
| intent | trend |
| golden_ref | b-report-us#cisco-vendor-net-sales-trend-2026 |
| table_fqn | dw_us.dws_disty_brpt_vend_mtd |
| status | routing-certified |
| snapshot_date | 2026-06-26 |
| eval_mode | mock |
| agent_test_level | full |

**Retrieval**

- resolved_metrics: `net_sales`
- entity_filters:
  - vendor_label: `CISCO`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_vend_mtd`, `dim_pub_vendor_info`, `month_ends`, `vendor_scope`, `period_label`, `net_sales`, `GROUP BY`, `ORDER BY period_label`
- sql_shape.must_not_contain: `month_no`, `LIMIT 1`, `202601`
- result_shape: min_rows=1

**Certified SQL**

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

### retail-scanner-margin-holdout

| Field | Value |
|-------|-------|
| question | what is the margin for Retail Scanner |
| intent | metric_lookup |
| table_fqn | dw_us.dws_disty_brpt_vpl_mtd |
| status | hold-out |
| snapshot_date | 2026-06-23 |
| eval_mode | mock |
| agent_test_level | retrieval |

**Retrieval**

- resolved_metrics: `ngm_amt`
- entity_filters:
  - vpc_group_label: `Retail Scanner`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_vpl_mtd`, `dim_pub_vpl_info`, `ngm_amt`
- sql_shape.must_not_contain: `vpl_id`, `vpl_name`, `dim_pub_vpl_hierarchy_info`

### vpl-code-scan-holdout

| Field | Value |
|-------|-------|
| question | revenue for vpl code SCAN |
| intent | metric_lookup |
| table_fqn | dw_us.dws_disty_brpt_vpl_mtd |
| status | hold-out |
| snapshot_date | 2026-06-23 |
| eval_mode | mock |
| agent_test_level | retrieval |

**Retrieval**

- resolved_metrics: `net_sales`
- entity_filters:
  - vpl_code: `SCAN`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_vpl_mtd`, `dim_pub_vpl_info`, `vpl_code`
- sql_shape.must_not_contain: `vpl_id`, `vpl_name`

### net-sales-feb-2026-scalar

| Field | Value |
|-------|-------|
| question | What is net sales for Feb 2026? |
| intent | metric_lookup |
| golden_ref | b-report-us#net-sales-feb-2026-scalar |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_cust_mtd`, `net_sales`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### ngm-mar-2026-scalar

| Field | Value |
|-------|-------|
| question | NGM for March 2026? |
| intent | metric_lookup |
| golden_ref | b-report-us#ngm-mar-2026-scalar |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `dws_disty_brpt_cust_mtd`, `ngm_amt`

**Certified SQL**

```sql
SELECT 1 AS ngm_amt LIMIT 1
```

### gross-sales-q1-2026

| Field | Value |
|-------|-------|
| question | Gross sales for Q1 2026? |
| intent | metric_comparison |
| golden_ref | b-report-us#gross-sales-q1-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `gross_sales`

**Assertions**

- sql_shape.must_contain: `gross_sales`

**Certified SQL**

```sql
SELECT 1 AS gross_sales LIMIT 1
```

### vendor-top3-feb-2026

| Field | Value |
|-------|-------|
| question | Top 3 vendors by net sales in Feb 2026 |
| intent | ranking |
| golden_ref | b-report-us#vendor-top3-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_vend_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `vend_no`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### customer-top5-feb-2026

| Field | Value |
|-------|-------|
| question | Top 5 customers by net sales Feb 2026 |
| intent | ranking |
| golden_ref | b-report-us#customer-top5-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `cust_no`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### pm-top5-ngm-feb-2026

| Field | Value |
|-------|-------|
| question | Top 5 PM by NGM Feb 2026 |
| intent | ranking |
| golden_ref | b-report-us#pm-top5-ngm-feb-2026 |
| table_fqn | dw_us.dm_disty_brpt_pm_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `pm_id`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS ngm_amt LIMIT 1
```

### dell-vendor-sales-feb-2026

| Field | Value |
|-------|-------|
| question | Dell net sales Feb 2026 |
| intent | metric_lookup |
| golden_ref | b-report-us#dell-vendor-sales-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_vend_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `vend_name`, `net_sales`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### hp-vendor-ngm-feb-2026

| Field | Value |
|-------|-------|
| question | HP NGM Feb 2026 |
| intent | metric_lookup |
| golden_ref | b-report-us#hp-vendor-ngm-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_vend_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `ngm_amt`

**Certified SQL**

```sql
SELECT 1 AS ngm_amt LIMIT 1
```

### trend-net-sales-2026

| Field | Value |
|-------|-------|
| question | Monthly net sales trend for 2026 |
| intent | trend |
| golden_ref | b-report-us#trend-net-sales-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `period_label`, `net_sales`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### trend-ngm-2026

| Field | Value |
|-------|-------|
| question | Monthly NGM trend 2026 |
| intent | trend |
| golden_ref | b-report-us#trend-ngm-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `ngm_amt`

**Certified SQL**

```sql
SELECT 1 AS ngm_amt LIMIT 1
```

### yoy-net-sales-feb-2026

| Field | Value |
|-------|-------|
| question | Net sales YoY for Feb 2026 |
| intent | metric_comparison |
| golden_ref | b-report-us#yoy-net-sales-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `yoy`, `net_sales`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### margin-pct-feb-2026

| Field | Value |
|-------|-------|
| question | Margin percent Feb 2026 |
| intent | metric_lookup |
| golden_ref | b-report-us#margin-pct-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `ngm_amt`, `net_sales`

**Certified SQL**

```sql
SELECT 1 AS ngm_amt LIMIT 1
```

### vpc-breakdown-feb-2026

| Field | Value |
|-------|-------|
| question | Net sales by VPC group Feb 2026 |
| intent | diagnostic_slice |
| golden_ref | b-report-us#vpc-breakdown-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_vpl_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `vpc_group_desc`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### vpl-breakdown-feb-2026

| Field | Value |
|-------|-------|
| question | Net sales by VPL Feb 2026 |
| intent | diagnostic_slice |
| golden_ref | b-report-us#vpl-breakdown-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_vpl_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `vpl_code`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### territory-top5-feb-2026

| Field | Value |
|-------|-------|
| question | Top 5 territories by net sales Feb 2026 |
| intent | ranking |
| golden_ref | b-report-us#territory-top5-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `cust_terr`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### part-top5-sales-feb-2026

| Field | Value |
|-------|-------|
| question | Top 5 parts by net sales Feb 2026 |
| intent | ranking |
| golden_ref | b-report-us#part-top5-sales-feb-2026 |
| table_fqn | dw_us.dws_disty_brpt_part_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `sku_no`, `GROUP BY`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### order-line-ngm-negative

| Field | Value |
|-------|-------|
| question | Orders with negative NGM Feb 2026 top 10 |
| intent | ranking |
| golden_ref | b-report-us#order-line-ngm-negative |
| table_fqn | dw_us.dwd_disty_brpt_orders_pl_etl_mi |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `ngm_amt`

**Assertions**

- sql_shape.must_contain: `order_no`, `ngm_amt`

**Certified SQL**

```sql
SELECT 1 AS ngm_amt LIMIT 1
```

### cisco-trend-2026-holdout

| Field | Value |
|-------|-------|
| question | CISCO monthly revenue trend 2026 |
| intent | trend |
| golden_ref | b-report-us#cisco-trend-2026-holdout |
| table_fqn | dw_us.dws_disty_brpt_vend_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `period_label`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### scanner-category-lookup

| Field | Value |
|-------|-------|
| question | VPC Scanners revenue Feb 2026 |
| intent | metric_lookup |
| golden_ref | b-report-us#scanner-category-lookup |
| table_fqn | dw_us.dws_disty_brpt_vpl_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | metric_index |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**

- sql_shape.must_contain: `vpc_group_desc`

**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

### unsupported-forecast

| Field | Value |
|-------|-------|
| question | Forecast next year revenue without data |
| intent | unsupported |
| golden_ref | b-report-us#unsupported-forecast |
| table_fqn | dw_us.dws_disty_brpt_cust_mtd |
| status | routing-certified |
| snapshot_date | 2026-02-28 |
| eval_mode | mock |
| agent_test_level | full |
| semantic_layer_path | n/a |

**Retrieval**

- resolved_metrics: `net_sales`

**Assertions**


**Certified SQL**

```sql
SELECT 1 AS net_sales LIMIT 1
```

