DROP TABLE IF EXISTS rds_9163_month;
CREATE LOCAL TEMPORARY TABLE rds_9163_month ON COMMIT PRESERVE ROWS AS
SELECT add_months(date_trunc('month', current_date)::date, -1) AS month_start,
       (date_trunc('month', current_date)::date - 1) AS month_end,
       DAY((date_trunc('month', current_date)::date - 1)) AS days_in_month
;

DROP TABLE IF EXISTS rdsetl.rds_tmp;
CREATE TABLE rdsetl.rds_tmp AS
SELECT a.vend_no AS "Vendor Number",
       b.vend_name AS "Vendor Name",
       ROUND(SUM(a.total) / MAX(m.days_in_month), 2) AS "AP Balance"
  FROM dw_ca.dws_disty_ap_vend_aging_df a
 INNER JOIN dim_ca.dim_pub_vendor_info b
    ON a.vend_no = b.vend_no
 CROSS JOIN rds_9163_month m
 WHERE (1=1
       AND (a.date_flag >= m.month_start AND a.date_flag <= m.month_end)
       )
 GROUP BY a.vend_no, b.vend_name
 ORDER BY 1
;

DROP TABLE IF EXISTS rdsetl.rds_tmp_2;
CREATE TABLE rdsetl.rds_tmp_2 AS
SELECT a.cust_no AS "Customer Number",
       a.cust_name AS "Customer Name",
       ROUND(SUM(a.total) / MAX(m.days_in_month), 2) AS "AR Balance"
  FROM dw_ca.dws_disty_ar_cust_sum_age_df a
 CROSS JOIN rds_9163_month m
 WHERE (1=1
       AND (a.date_flag >= m.month_start AND a.date_flag <= m.month_end)
       )
   AND a.data_period = 'D'
   AND a.view_level = 'CUST_COM'
 GROUP BY a.cust_no, a.cust_name
 ORDER BY 1, 2
;

DROP TABLE IF EXISTS rdsetl.rds_tmp_3;
CREATE TABLE rdsetl.rds_tmp_3 AS
SELECT a.vend_no AS "Vendor Number",
       b.vend_name AS "Vendor Name",
       a.sku_no AS "SKU Number",
       SUM(a.age1_30 + (COALESCE(a.intran_in, 0) * a.ave_cost)) / MAX(m.days_in_month) AS "Age 1",
       SUM(a.age31_60) / MAX(m.days_in_month) AS "Age 2",
       SUM(a.age61_90) / MAX(m.days_in_month) AS "Age 3",
       SUM(a.age91_120) / MAX(m.days_in_month) AS "Age 5e",
       SUM(a.age121_150) / MAX(m.days_in_month) AS "Age 6e",
       SUM(a.age151_180) / MAX(m.days_in_month) AS "Age 7e",
       SUM(a.age181_210) / MAX(m.days_in_month) AS "Age 8e1",
       SUM(a.age211_240) / MAX(m.days_in_month) AS "Age 8e2",
       SUM(a.age241_270) / MAX(m.days_in_month) AS "Age 9e1",
       SUM(a.age271_300) / MAX(m.days_in_month) AS "Age 9e2",
       SUM(a.age301_330) / MAX(m.days_in_month) AS "Age 9e3",
       SUM(a.age331_360) / MAX(m.days_in_month) AS "Age 9e4",
       SUM(a.age360_up) / MAX(m.days_in_month) AS "Age 10e"
  FROM dw_ca.dwd_disty_inv_aging_df a
 INNER JOIN dim_ca.dim_pub_vendor_info b
    ON a.vend_no = b.vend_no
 CROSS JOIN rds_9163_month m
 WHERE (1=1
       AND (a.date_flag >= m.month_start AND a.date_flag <= m.month_end)
       )
   AND a.view_level = 'IT_PART'
   AND a.inv_type != 6
 GROUP BY a.vend_no, b.vend_name, a.sku_no
 ORDER BY 1, 2
;

DROP TABLE IF EXISTS rdsetl.rds_tmp_body;
CREATE TABLE rdsetl.rds_tmp_body AS
SELECT 1 AS flag,
       'Standard' AS body_type,
       COUNT(*) AS cnt
  FROM rdsetl.rds_tmp
;

INSERT INTO rdsetl.rds_tmp_body
SELECT 2 AS flag,
       'Standard' AS body_type,
       COUNT(*) AS cnt
  FROM rdsetl.rds_tmp_2
;

INSERT INTO rdsetl.rds_tmp_body
SELECT 3 AS flag,
       'Standard' AS body_type,
       COUNT(*) AS cnt
  FROM rdsetl.rds_tmp_3
;

DROP TABLE IF EXISTS rdsetl.rds_tmp_sheet_config;
CREATE TABLE rdsetl.rds_tmp_sheet_config (
    sheet_index int,
    sheet_name varchar(50),
    title_active varchar(1),
    date_pattern varchar(50)
)
;

INSERT INTO rdsetl.rds_tmp_sheet_config SELECT 1, 'AP Balance', NULL, 'MM/dd/yyyy';
INSERT INTO rdsetl.rds_tmp_sheet_config SELECT 2, 'AR Balance', NULL, 'MM/dd/yyyy';
INSERT INTO rdsetl.rds_tmp_sheet_config SELECT 3, 'Inventory', NULL, NULL;

DROP TABLE IF EXISTS rds_9163_month;
