-- Drop temporary tables if they exist
DROP TABLE IF EXISTS rdsetl.rds_tmp;
DROP TABLE IF EXISTS rdsetl.rds_tmp_2;
DROP TABLE IF EXISTS rdsetl.rds_tmp_body;
DROP TABLE IF EXISTS rdsetl.rds_tmp_sheet_config;
DROP TABLE IF EXISTS tmp_inv_us7500;
DROP TABLE IF EXISTS rds_ord_7500;
DROP TABLE IF EXISTS t_vpl_7500;
DROP TABLE IF EXISTS t_cust_7500;
DROP TABLE IF EXISTS t_all_cust_7500;
DROP TABLE IF EXISTS rio_7500;
DROP TABLE IF EXISTS t_rr_7500;
DROP TABLE IF EXISTS inv_7500;
DROP TABLE IF EXISTS sku;
DROP TABLE IF EXISTS inv_aging;
DROP TABLE IF EXISTS Dell_BO_QTY_7500;
DROP TABLE IF EXISTS rds_rio_on_order;
DROP TABLE IF EXISTS loc_qty;
DROP TABLE IF EXISTS t_rr_7500_max_week;

-- Create LOCAL TEMPORARY tables with PRESERVE ROWS
CREATE LOCAL TEMPORARY TABLE t_cust_7500 ON COMMIT PRESERVE ROWS AS
SELECT cust_no, CAST(NULL AS INT) AS mcust_no
FROM dim_us.dim_pub_customer_info
WHERE cust_no IN (124858, 613402);

UPDATE t_cust_7500
SET mcust_no = COALESCE(b.xref_no, t_cust_7500.cust_no)
FROM dim_us.dim_pub_cust_xref_all b
WHERE t_cust_7500.cust_no = b.cust_no
    AND b.xref_type = 'MASTER_SUB'
    AND b.active = 'Y';

CREATE LOCAL TEMPORARY TABLE t_all_cust_7500 ON COMMIT PRESERVE ROWS AS
SELECT a.cust_no, a.xref_no AS mcust_no
FROM dim_us.dim_pub_cust_xref_all a
JOIN t_cust_7500 b ON a.xref_no = b.mcust_no
WHERE a.xref_type = 'MASTER_SUB'
    AND a.active = 'Y'
UNION
SELECT cust_no, mcust_no
FROM t_cust_7500;

CREATE LOCAL TEMPORARY TABLE rds_ord_7500 ON COMMIT PRESERVE ROWS AS
SELECT order_no,
    order_type,
    order_line_no,
    date_flag AS ship_date,
    a.sku_no,
    CAST(NULL AS VARCHAR(60)) AS part_no,
    CAST(NULL AS VARCHAR(60)) AS mfg_partno,
    CAST(NULL AS VARCHAR(60)) AS short_desc,
    a.ship_qty,
    CASE
        WHEN date_flag >= current_date() - 28
            AND date_flag < current_date() - 21
            THEN 'LLLLW'
        WHEN date_flag >= current_date() - 21
            AND date_flag < current_date() - 14
            THEN 'LLLW'
        WHEN date_flag >= current_date() - 14
            AND date_flag < current_date() - 7
            THEN 'LLW'
        WHEN date_flag >= current_date() - 7
            AND date_flag < current_date()
            THEN 'LW'
        ELSE NULL
    END AS wk,
    (COALESCE(unit_sum_expense, 0) + unit_price) * a.ship_qty AS sales,
    a.cust_terr AS sales_terr,
    CAST(NULL AS VARCHAR(60)) AS terr_name,
    a.cust_no AS billto_cust,
    CAST(NULL AS VARCHAR(60)) AS billto_name,
    CAST(NULL AS INT) AS from_loc_no
FROM dw_us.dwd_disty_pub_dw_orders_extend_di a
JOIN t_all_cust_7500 c ON a.cust_no = c.cust_no
WHERE date_flag >= current_date() - 70
AND date_flag < current_date();

UPDATE rds_ord_7500
SET from_loc_no = b.from_loc_no
FROM dw_us.dwd_pub_common_history_header_extend b
WHERE rds_ord_7500.order_no = b.order_no
    AND rds_ord_7500.order_type = b.order_type;

CREATE LOCAL TEMPORARY TABLE tmp_inv_us7500 ON COMMIT PRESERVE ROWS AS
SELECT CAST(NULL AS INT) AS vend_no,
    CAST(NULL AS VARCHAR(100)) AS vend_name,
    CAST(NULL AS VARCHAR(100)) AS part_no,
    CAST(NULL AS VARCHAR(100)) AS mfg_partno,
    sku_no,
    CAST(NULL AS VARCHAR(100)) AS abc_code,
    CAST(NULL AS VARCHAR(100)) AS source_status,
    CAST(NULL AS NUMERIC(19,4)) AS base_cost,
    CAST(NULL AS VARCHAR(200)) AS short_desc,
    CAST(NULL AS INT) AS on_hand,
    CAST(NULL AS INT) AS avail,
    CAST(NULL AS INT) AS on_order,
    CAST(NULL AS INT) AS bo_qty,
    CAST(NULL AS INT) AS Dell_BO_QTY,
    CAST(NULL AS INT) AS aging_90_plus,
    CAST(NULL AS INT) AS rio_qty_for_dell,
    CAST(NULL AS INT) AS rio_on_order_qty_for_dell,
    CAST(NULL AS INT) AS total_rio_oh_oo_for_dell,
    CAST(NULL AS INT) AS sugg_buy,
    CAST(NULL AS INT) AS rr_4,
    CAST(NULL AS INT) AS rr_10,
    CAST(NULL AS NUMERIC(19,4)) AS weekly_avg,
    CAST(NULL AS NUMERIC(19,4)) AS spike_check,
    CAST(NULL AS NUMERIC(19,4)) AS wk_of_cal,
    SUM(CASE WHEN ship_date >= current_date() - 28 THEN ship_qty ELSE 0 END) AS rr_4_dell,
    SUM(ship_qty) AS rr_10_dell,
    SUM(CASE WHEN wk = 'LW' THEN ship_qty ELSE 0 END) AS LW_Qty,
    SUM(CASE WHEN wk = 'LLW' THEN ship_qty ELSE 0 END) AS LLW_Qty,
    SUM(CASE WHEN wk = 'LLLW' THEN ship_qty ELSE 0 END) AS LLLW_Qty,
    SUM(CASE WHEN wk = 'LLLLW' THEN ship_qty ELSE 0 END) AS LLLLW_Qty,
    SUM(CASE WHEN wk = 'LW' THEN sales ELSE 0 END) AS LW_Sales,
    SUM(CASE WHEN wk = 'LLW' THEN sales ELSE 0 END) AS LLW_Sales,
    SUM(CASE WHEN wk = 'LLLW' THEN sales ELSE 0 END) AS LLLW_Sales,
    SUM(CASE WHEN wk = 'LLLLW' THEN sales ELSE 0 END) AS LLLLW_Sales,
    SUM(CASE WHEN ship_date >= current_date() - 28 AND from_loc_no <> 98 THEN ship_qty ELSE 0 END) AS rr_4_stocking_dell,
    SUM(CASE WHEN ship_date >= current_date() - 28 AND from_loc_no = 98 THEN ship_qty ELSE 0 END) AS rr_4_dds_dell,
    SUM(CASE WHEN from_loc_no <> 98 THEN ship_qty ELSE 0 END) AS rr_10_stocking_dell,
    SUM(CASE WHEN from_loc_no = 98 THEN ship_qty ELSE 0 END) AS rr_10_dds_dell,
    CAST(NULL AS NUMERIC(19,4)) AS WOS_for_dell,
    CAST(NULL AS NUMERIC(19,4)) AS WOS_for_all,
    CAST(NULL AS VARCHAR(60)) AS street_date,
    CAST(NULL AS INT) AS vpl_no,
    CAST(NULL AS VARCHAR(60)) AS vpc_code,
    CAST(NULL AS VARCHAR(60)) AS us_buyer,
    CAST(NULL AS INT) AS pm_code
FROM rds_ord_7500
GROUP BY sku_no;

CREATE LOCAL TEMPORARY TABLE sku ON COMMIT PRESERVE ROWS AS
SELECT DISTINCT sku_no
FROM tmp_inv_us7500;

CREATE LOCAL TEMPORARY TABLE inv_aging ON COMMIT PRESERVE ROWS AS
SELECT a.sku_no,
    CAST(ROUND(COALESCE(a.age90_up / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT) AS aging_90_plus
FROM dw_us.dwd_disty_inv_aging_df a
JOIN sku b ON a.sku_no = b.sku_no
WHERE a.date_flag = current_date() - 1
    AND a.view_level = 'IT_PART'
    AND a.inv_type = 1;

UPDATE tmp_inv_us7500
SET aging_90_plus = b.aging_90_plus
FROM inv_aging b
WHERE tmp_inv_us7500.sku_no = b.sku_no;

CREATE LOCAL TEMPORARY TABLE Dell_BO_QTY_7500 ON COMMIT PRESERVE ROWS AS
SELECT a.sku_no,
    SUM(order_qty) AS dell_bo_qty
FROM dw_us.dwd_disty_sales_open_order_detail a
WHERE a.cust_no IN (124858, 613402)
    AND a.order_type = 8
GROUP BY a.sku_no;

UPDATE tmp_inv_us7500
SET Dell_BO_QTY = b.dell_bo_qty
FROM Dell_BO_QTY_7500 b
WHERE tmp_inv_us7500.sku_no = b.sku_no;

UPDATE tmp_inv_us7500
SET vend_no = b.vend_no,
    vpl_no = b.vpl_no,
    short_desc = b.short_desc,
    part_no = b.part_no,
    abc_code = b.abc_code,
    source_status = b.source_status,
    base_cost = b.po_cost,
    pm_code = b.prod_code,
    mfg_partno = b.mfg_partno
FROM dim_us.dim_pub_part_info b
WHERE tmp_inv_us7500.sku_no = b.sku_no;

UPDATE tmp_inv_us7500
SET vpc_code = dvp.vpl_code
FROM dim_us.dim_pub_vpl_info dvp
WHERE tmp_inv_us7500.vpl_no = dvp.vpl_no;

CREATE LOCAL TEMPORARY TABLE inv_7500 ON COMMIT PRESERVE ROWS AS
SELECT a.sku_no,
    SUM(on_hand_qty) AS on_hand,
    SUM(a.on_order_qty) AS on_order,
    SUM(a.bo_qty) AS bo_qty,
    SUM(a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty) AS avail
FROM dw_us.dwd_disty_inv_qty_df a
JOIN tmp_inv_us7500 b ON a.sku_no = b.sku_no
WHERE inv_type = 1
    AND a.date_flag = current_date() - 1
GROUP BY a.sku_no;

UPDATE tmp_inv_us7500
SET on_hand = b.on_hand,
    avail = b.avail,
    on_order = b.on_order,
    bo_qty = b.bo_qty
FROM inv_7500 b
WHERE tmp_inv_us7500.sku_no = b.sku_no;


CREATE LOCAL TEMP TABLE t_rr_7500_max_week ON COMMIT PRESERVE ROWS AS
SELECT max(week) as max_week
FROM dw_us.dws_disty_pur_ips_runrate_1w
WHERE sum_type = 'WITYPESTD'
AND inv_type = 1;

CREATE LOCAL TEMP TABLE t_rr_7500 ON COMMIT PRESERVE ROWS AS
SELECT b.sku_no
      ,b.inv_type
      ,SUM(CASE WHEN b.week=c.max_week THEN b.runrate_qty ELSE 0 END) AS wtd
      ,SUM(CASE WHEN b.week=c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr1
      ,SUM(CASE WHEN b.week BETWEEN c.max_week-2  AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr2
      ,SUM(CASE WHEN b.week BETWEEN c.max_week-4  AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr4
      ,SUM(CASE WHEN b.week BETWEEN c.max_week-10 AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr10
FROM dw_us.dws_disty_pur_ips_runrate_1w b
JOIN t_rr_7500_max_week c ON 1=1
WHERE c.max_week-10 <= b.week
     AND b.inv_type= 1
     AND b.sum_type='WITYPESTD'
GROUP BY b.sku_no, b.inv_type;


UPDATE tmp_inv_us7500
SET rr_10 = b.rr10,
    rr_4 = b.rr4,
    weekly_avg = (b.rr4 * 1.00 / 4) * 0.80 + (b.rr10 * 1.00 / 10) * 0.20
FROM t_rr_7500 b
WHERE tmp_inv_us7500.sku_no = b.sku_no;

UPDATE tmp_inv_us7500
SET spike_check = (b.rr4 * 1.00 / 4) / (b.rr10 * 1.00 / 10)
FROM t_rr_7500 b
WHERE tmp_inv_us7500.sku_no = b.sku_no
    AND b.rr10 <> 0;

UPDATE tmp_inv_us7500
SET wk_of_cal = CASE
        WHEN spike_check >= 1.7 THEN 2
        WHEN spike_check >= 1.5 AND spike_check < 1.7 THEN 3
        WHEN spike_check >= 1.1 AND spike_check < 1.5 THEN 3.50
        WHEN spike_check >= 0.9 AND spike_check < 1.1 THEN 4
        WHEN spike_check >= 0.7 AND spike_check < 0.9 THEN 3
        WHEN spike_check >= 0.5 AND spike_check < 0.7 THEN 2
        WHEN spike_check >= 0.3 AND spike_check < 0.5 THEN 1.5
        ELSE 0
    END;

UPDATE tmp_inv_us7500
SET us_buyer = c.firstname || ' ' || c.lastname
FROM dim_us.dim_disty_pur_vendor_dna_matrix b
JOIN dim_us.dim_pub_manager c
ON b.member_id = c.userid AND member_role = 'primary' and primary_flag = 'Y'
WHERE tmp_inv_us7500.vpl_no = b.vpl_no
    AND tmp_inv_us7500.vend_no = b.vend_no
    AND b.department_type = 'BUYR';

UPDATE tmp_inv_us7500
SET us_buyer = c.firstname || ' ' || c.lastname
FROM dim_us.dim_disty_pur_vendor_dna_matrix b
JOIN dim_us.dim_pub_manager c
ON b.member_id = c.userid AND member_role = 'primary' and primary_flag = 'Y'
WHERE -1 = b.vpl_no
    AND tmp_inv_us7500.vend_no = b.vend_no
    AND b.department_type = 'BUYR'
    AND tmp_inv_us7500.us_buyer IS NULL;

CREATE LOCAL TEMPORARY TABLE rio_7500 ON COMMIT PRESERVE ROWS AS
SELECT c.sku_no,
    COALESCE(SUM(rrd.hold_qty), 0) AS RIO_cust_qty
FROM dw_us.dwd_disty_inv_rio_req_header rrh
JOIN dw_us.dwd_disty_inv_rio_req_detail rrd ON rrh.rio_req_no = rrd.rio_req_no
JOIN tmp_inv_us7500 c ON rrh.sku_no = c.sku_no
WHERE rrd.inproc_ref_type = 18
    AND rrh.cust_no IN (124858, 613402)
    AND rrh.type = 'R'
GROUP BY c.sku_no;

UPDATE tmp_inv_us7500
SET rio_qty_for_dell = RIO_cust_qty
FROM rio_7500 b
WHERE tmp_inv_us7500.sku_no = b.sku_no;

UPDATE tmp_inv_us7500
SET vend_name = b.vend_name
FROM dim_us.dim_pub_vendor_info b
WHERE tmp_inv_us7500.vend_no = b.vend_no;

UPDATE tmp_inv_us7500
SET WOS_for_dell = (COALESCE(avail, 0) + COALESCE(on_order, 0) + COALESCE(rio_qty_for_dell, 0)) / NULLIF((COALESCE(rr_4_stocking_dell, 0) / 4.00), 0);

UPDATE tmp_inv_us7500
SET WOS_for_all = (COALESCE(avail, 0) + COALESCE(on_order, 0) + COALESCE(rio_qty_for_dell, 0)) / NULLIF((COALESCE(rr_4, 0) / 4.00 * 0.8 + COALESCE(rr_10, 0) / 10.00 * 0.2), 0);

UPDATE tmp_inv_us7500
SET street_date = TO_CHAR(p.profile_d, 'YYYYMMDD')
FROM dim_us.dim_pub_sku_profile_rt p
WHERE tmp_inv_us7500.sku_no = p.sku_no
    AND p.profile_type = 'STREETDATE'
    AND p.active = 'Y';

CREATE LOCAL TEMPORARY TABLE rds_rio_on_order ON COMMIT PRESERVE ROWS AS
SELECT sku_no,
    CAST(NULL AS INT) AS req_qty,
    CAST(NULL AS INT) AS hold_qty,
    CAST(NULL AS INT) AS consumed_qty,
    CAST(NULL AS INT) AS rio_on_order_qty_for_dell
FROM tmp_inv_us7500;

CREATE LOCAL TEMPORARY TABLE loc_qty (
    sku_no INT,
    qty INT
) ON COMMIT PRESERVE ROWS;

-- Get req_qty
DELETE FROM loc_qty;

INSERT INTO loc_qty
SELECT inv.sku_no, SUM(rh.req_qty)
FROM dw_us.dwd_disty_inv_rio_req_header rh
JOIN rds_rio_on_order inv ON inv.sku_no = rh.sku_no
    AND rh.cust_no IN (124858, 613402)
WHERE rh.status = 'A'
GROUP BY inv.sku_no;

UPDATE rds_rio_on_order
SET req_qty = q.qty
FROM loc_qty q
WHERE rds_rio_on_order.sku_no = q.sku_no;

-- Get hold qty
DELETE FROM loc_qty;

INSERT INTO loc_qty
SELECT inv.sku_no, SUM(rd.hold_qty)
FROM dw_us.dwd_disty_inv_rio_req_header rh
JOIN dw_us.dwd_disty_inv_rio_req_detail rd ON rh.rio_req_no = rd.rio_req_no
JOIN rds_rio_on_order inv ON inv.sku_no = rh.sku_no
    AND rh.cust_no IN (124858, 613402)
WHERE rh.status = 'A'
    AND rd.inproc_ref_type IN (4, 18)
GROUP BY inv.sku_no;

UPDATE rds_rio_on_order
SET hold_qty = q.qty
FROM loc_qty q
WHERE rds_rio_on_order.sku_no = q.sku_no;

-- Get consumed_qty
DELETE FROM loc_qty;

INSERT INTO loc_qty
SELECT inv.sku_no, SUM(COALESCE(rc.to_order_qty, 0))
FROM dw_us.dwd_disty_inv_rio_req_header rh
JOIN rds_rio_on_order inv ON inv.sku_no = rh.sku_no
    AND rh.cust_no IN (124858, 613402)
JOIN dw_us.dwd_disty_inv_rio_req_consumed rc ON rc.rio_req_no = rh.rio_req_no
WHERE EXISTS (
        SELECT 1
        FROM dim_us.dim_pub_list_box_detail l
        WHERE list_box_code = 'RCT'
            AND l.code_value != '-1'
            AND CAST(l.code_value AS INT) = rc.to_order_type
    )
GROUP BY inv.sku_no;

UPDATE rds_rio_on_order
SET consumed_qty = q.qty
FROM loc_qty q
WHERE rds_rio_on_order.sku_no = q.sku_no;

-- Get open_rio_qty
UPDATE rds_rio_on_order
SET rio_on_order_qty_for_dell = req_qty - COALESCE(hold_qty, 0) - COALESCE(consumed_qty, 0);

UPDATE tmp_inv_us7500
SET rio_on_order_qty_for_dell = b.rio_on_order_qty_for_dell
FROM rds_rio_on_order b
WHERE tmp_inv_us7500.sku_no = b.sku_no;

UPDATE tmp_inv_us7500
SET total_rio_oh_oo_for_dell = COALESCE(rio_qty_for_dell, 0) + COALESCE(rio_on_order_qty_for_dell, 0);

UPDATE tmp_inv_us7500
SET sugg_buy = weekly_avg * wk_of_cal - (COALESCE(avail, 0) + COALESCE(on_order, 0) + COALESCE(rio_qty_for_dell, 0));

CREATE TABLE rdsetl.rds_tmp AS
select * from tmp_inv_us7500;

CREATE TABLE rdsetl.rds_tmp_2 AS
SELECT rh.sku_no,
    rh.rio_req_no,
    rd.inproc_ref_no AS PO_no,
    rd.hold_qty
FROM dw_us.dwd_disty_inv_rio_req_header rh
JOIN dw_us.dwd_disty_inv_rio_req_detail rd ON rh.rio_req_no = rd.rio_req_no
WHERE rh.status = 'A'
    AND rd.inproc_ref_type = 2
    AND rh.cust_no IN (124858, 613402);

CREATE TABLE rdsetl.rds_tmp_sheet_config AS
SELECT 'report' AS sheet_name, NULL AS title_active, NULL AS date_pattern
UNION ALL
SELECT 'tied PO' AS sheet_name, NULL AS title_active, NULL AS date_pattern;

CREATE TABLE rdsetl.rds_tmp_body AS
SELECT 'standard' AS body_type,
       COUNT(*) AS cnt
  FROM rdsetl.rds_tmp;

insert into rdsetl.rds_tmp_body
SELECT 'standard' AS body_type,
       COUNT(*) AS cnt
  FROM rdsetl.rds_tmp_2;
