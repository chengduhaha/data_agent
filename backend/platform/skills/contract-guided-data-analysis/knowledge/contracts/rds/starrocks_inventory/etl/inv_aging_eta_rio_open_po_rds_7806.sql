set time_zone = 'America/Los_Angeles';

-- Drop existing tables if they exist
DROP TABLE IF EXISTS tempdb.rds_oo_7806;
DROP TABLE IF EXISTS tempdb.rds_rr_7806;
DROP TABLE IF EXISTS tempdb.rds_tmp;
DROP TABLE IF EXISTS tempdb.rds_tmp_body;
DROP TABLE IF EXISTS tempdb.rds_inv_rio_7806;
DROP TABLE IF EXISTS tempdb.rds_rio_7806;
DROP TABLE IF EXISTS tempdb.rds_oo312_7806;
DROP TABLE IF EXISTS tempdb.tmp_date_flag;

-- Create main temporary table with primary key
CREATE TABLE tempdb.rds_tmp
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    c.sku_no,
    b.vend_no,
    c.part_no,
    c.mfg_partno,
    c.abc_code,
    c.mar_comment,
    c.po_cost as base_cost,
    CAST(NULL AS INT) as runrate13w,
    CAST(NULL AS INT) as runrate52w,
    SUM(on_hand_qty) as OH,
    SUM(intran_in) as IT,
    SUM(bo_qty) as BO,
    SUM(alloc_qty) as total_Alloc_qty,
    CAST(NULL AS INT) as rio_qty,
    CAST(NULL AS INT) as alloc_qty,
    SUM(on_order_qty) as OO,
    SUM(CASE WHEN loc_no = 310 THEN on_order_qty ELSE 0 END) as OO_DEX,
    CAST(NULL AS INT) as OO_DEX_curr_mth,
    CAST(NULL AS INT) as OO_DEX_second_mth,
    CAST(NULL AS INT) as OO_DEX_third_mth,
    CAST(NULL AS INT) as OO_DEX_fourth_mth,
    CAST(NULL AS INT) as OO_DEX_fifth_mth,
    CAST(NULL AS INT) as OO_DEX_sixth_mth,
    SUM(CASE WHEN loc_no = 312 THEN on_order_qty ELSE 0 END) as OO_LOC312,
    CAST(NULL AS INT) as OO_LOC312_curr_mth,
    CAST(NULL AS INT) as OO_LOC312_second_mth,
    CAST(NULL AS INT) as OO_LOC312_third_mth,
    CAST(NULL AS INT) as OO_LOC312_fourth_mth,
    CAST(NULL AS INT) as OO_LOC312_fifth_mth,
    CAST(NULL AS INT) as OO_LOC312_sixth_mth,
    CAST(NULL AS INT) as age61_90,
    CAST(NULL AS INT) as age90plus,
    CAST(NULL AS INT) as age180plus
FROM ods_us.ods_cis_corp_inv_qty_rt a
, ods_us.ods_cis_corp_vend_master_rt b 
, ods_us.ods_cis_corp_part_master_rt c  
WHERE 
a.sku_no = c.sku_no AND b.vend_no = c.vend_no AND
c.vend_no IN (13439, 50633)
    AND inv_type IN (1, 300)
GROUP BY  b.vend_no,
    c.part_no,
    c.mfg_partno, 
    c.po_cost,
    c.abc_code,
    c.mar_comment
;

-- Update inventory aging data
drop table if exists tempdb.t_inv_aging_7806;
create table tempdb.t_inv_aging_7806 as
select a.sku_no,
       sum(b.qty61_90) as age61_90,
       sum(b.qty90_up) as age90plus,
       sum(b.qty180_up) as age180plus
  from tempdb.rds_tmp a, dw_us.dwd_disty_inv_aging_df b
 where a.sku_no = b.sku_no
   and b.inv_type in (1, 300)
   and b.view_level = 'IT_PART'
   and b.date_flag = date_add(current_date(),interval -1 day)
 group by a.sku_no
;
update tempdb.rds_tmp
   set age61_90 = a.age61_90,
       age90plus = a.age90plus,
       age180plus = a.age180plus
  from tempdb.t_inv_aging_7806 a
 where rds_tmp.sku_no = a.sku_no
;

-- Create table for order ETA details (location 310)
CREATE TABLE tempdb.rds_oo_7806
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    c.sku_no,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 0 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 1 MONTH))
        THEN eta_qty ELSE 0 END) as OO_DEX_curr_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 1 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 2 MONTH))
        THEN eta_qty ELSE 0 END) as OO_DEX_second_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 2 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 3 MONTH))
        THEN eta_qty ELSE 0 END) as OO_DEX_third_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 3 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 4 MONTH))
        THEN eta_qty ELSE 0 END) as OO_DEX_fourth_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 4 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 5 MONTH))
        THEN eta_qty ELSE 0 END) as OO_DEX_fifth_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 5 MONTH))
        THEN eta_qty ELSE 0 END) as OO_DEX_sixth_mth
FROM ods_us.ods_cis_corp_order_header_rt a
, ods_us.ods_cis_corp_order_eta_detail_rt b 
, tempdb.rds_tmp c 
, ods_us.ods_cis_corp_order_detail_rt d 
   where a.order_no=b.order_no
       and a.order_type=b.order_type
       and d.sku_no=c.sku_no
       and a.to_loc_no=310
       and a.delete_date is null
       and b.order_no=d.order_no
       and b.order_type=d.order_type
       and b.order_line_no=d.order_line_no
       and a.order_type=2
       and d.delete_date is null
     group by c.sku_no;

-- Update main table with order ETA details (location 310)
UPDATE tempdb.rds_tmp
SET OO_DEX_curr_mth = b.OO_DEX_curr_mth,
    OO_DEX_second_mth = b.OO_DEX_second_mth,
    OO_DEX_third_mth = b.OO_DEX_third_mth,
    OO_DEX_fourth_mth = b.OO_DEX_fourth_mth,
    OO_DEX_fifth_mth = b.OO_DEX_fifth_mth,
    OO_DEX_sixth_mth = b.OO_DEX_sixth_mth
FROM tempdb.rds_oo_7806 b
WHERE rds_tmp.sku_no = b.sku_no;

-- Create table for order ETA details (location 312)
CREATE TABLE tempdb.rds_oo312_7806
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id ,
    c.sku_no,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 0 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 1 MONTH))
        THEN eta_qty ELSE 0 END) as OO_LOC312_curr_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 1 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 2 MONTH))
        THEN eta_qty ELSE 0 END) as OO_LOC312_second_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 2 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 3 MONTH))
        THEN eta_qty ELSE 0 END) as OO_LOC312_third_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 3 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 4 MONTH))
        THEN eta_qty ELSE 0 END) as OO_LOC312_fourth_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 4 MONTH))
        AND CAST(b.eta_date AS DATE) < date_trunc('month',date_add(CURDATE(), INTERVAL 5 MONTH))
        THEN eta_qty ELSE 0 END) as OO_LOC312_fifth_mth,
    SUM(CASE WHEN CAST(b.eta_date AS DATE) >= date_trunc('month',date_add(CURDATE(), INTERVAL 5 MONTH))
        THEN eta_qty ELSE 0 END) as OO_LOC312_sixth_mth
FROM ods_us.ods_cis_corp_order_header_rt a
, ods_us.ods_cis_corp_order_eta_detail_rt b 
, tempdb.rds_tmp c 
, ods_us.ods_cis_corp_order_detail_rt d 
   where a.order_no=b.order_no
       and a.order_type=b.order_type
       and d.sku_no=c.sku_no
       and a.to_loc_no=312
       and a.delete_date is null
       and b.order_no=d.order_no
       and b.order_type=d.order_type
       and b.order_line_no=d.order_line_no
       and a.order_type=2
       and d.delete_date is null
     group by c.sku_no;

-- Update main table with order ETA details (location 312)
UPDATE tempdb.rds_tmp
SET OO_LOC312_curr_mth = b.OO_LOC312_curr_mth,
    OO_LOC312_second_mth = b.OO_LOC312_second_mth,
    OO_LOC312_third_mth = b.OO_LOC312_third_mth,
    OO_LOC312_fourth_mth = b.OO_LOC312_fourth_mth,
    OO_LOC312_fifth_mth = b.OO_LOC312_fifth_mth,
    OO_LOC312_sixth_mth = b.OO_LOC312_sixth_mth
FROM tempdb.rds_oo312_7806 b
WHERE rds_tmp.sku_no = b.sku_no;

-- Create RIO inventory table
CREATE TABLE tempdb.rds_inv_rio_7806
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id ,
    c.sku_no,
    loc_no,
    SUM(IFNULL(rrd.hold_qty, 0)) as RIO_qty
FROM ods_us.ods_cis_corp_rio_request_header_rt rrh
JOIN ods_us.ods_cis_corp_rio_req_detail_rt rrd ON rrh.rio_req_no = rrd.rio_req_no
JOIN tempdb.rds_tmp c ON rrh.sku_no = c.sku_no
GROUP BY c.sku_no, loc_no;

-- Create aggregated RIO table
CREATE TABLE tempdb.rds_rio_7806
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    sku_no,
    SUM(RIO_qty) as rio_qty
FROM tempdb.rds_inv_rio_7806
GROUP BY sku_no;

-- Update main table with RIO quantity
UPDATE tempdb.rds_tmp
SET rio_qty = b.rio_qty
FROM tempdb.rds_rio_7806 b
WHERE rds_tmp.sku_no = b.sku_no;

-- Update alloc_qty
UPDATE tempdb.rds_tmp
SET alloc_qty = IFNULL(total_Alloc_qty - IFNULL(rio_qty, 0), total_Alloc_qty);

-- Delete rows with zero quantities
DELETE FROM tempdb.rds_tmp
WHERE IFNULL(OH, 0) = 0
    AND IFNULL(BO, 0) = 0
    AND IFNULL(IT, 0) = 0
    AND IFNULL(alloc_qty, 0) = 0
    AND IFNULL(rio_qty, 0) = 0;

CREATE TABLE tempdb.tmp_date_flag
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id ,
max(week) as max_week
FROM dw_us.dws_disty_pur_ips_runrate_1w
WHERE sum_type = 'WITYPESTD'
AND inv_type in (1,300);

-- Create runrate table
CREATE TABLE tempdb.rds_rr_7806
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id ,
    b.sku_no
    ,b.inv_type
    ,SUM(CASE WHEN b.week BETWEEN c.max_week-13 AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS wk13_qty
    ,SUM(CASE WHEN b.week BETWEEN c.max_week-52 AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS wk52_qty
FROM dw_us.dws_disty_pur_ips_runrate_1w b
JOIN tmp_date_flag c ON 1=1
WHERE c.max_week-52 <= b.week
     AND b.inv_type in (1,300)
     AND b.sum_type='WITYPESTD'
GROUP BY b.sku_no, b.inv_type;

-- Update main table with runrate13w
UPDATE tempdb.rds_tmp
SET runrate13w = (SELECT SUM(b.wk13_qty) FROM tempdb.rds_rr_7806 b WHERE rds_tmp.sku_no = b.sku_no);

-- Update main table with runrate52w
UPDATE tempdb.rds_tmp
SET runrate52w = (SELECT SUM(b.wk52_qty) FROM tempdb.rds_rr_7806 b WHERE rds_tmp.sku_no = b.sku_no);

-- Create body table
CREATE TABLE tempdb.rds_tmp_body
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
       'standard' as body_type,
       COUNT(*) as cnt
FROM tempdb.rds_tmp;

-- Clean up temporary tables
DROP TABLE IF EXISTS tempdb.rds_oo_7806;
DROP TABLE IF EXISTS tempdb.rds_rr_7806;
DROP TABLE IF EXISTS tempdb.rds_oo312_7806;
DROP TABLE IF EXISTS tempdb.t_date_var_7806;
DROP TABLE IF EXISTS tempdb.tmp_date_flag;