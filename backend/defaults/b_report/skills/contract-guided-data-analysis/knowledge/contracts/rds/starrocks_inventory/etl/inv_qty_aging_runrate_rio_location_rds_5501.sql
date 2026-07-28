/*Please correct the attached Inventory Report.  US Report 5501.
Please make sure to report all product ON HAND and ON ORDER.
Currently, if i do not have product on hand, it will not show that i have product on order for that same product.
It does not give my "Vendor a true picture of what I have on order.
Time frame and recipients will all stay the same.
*/

-- Drop existing tables if they exist
DROP TABLE IF EXISTS tempdb.rds_tmp;
DROP TABLE IF EXISTS tempdb.rds_tmp_body;
DROP TABLE IF EXISTS tempdb.t_loc_5501;
DROP TABLE IF EXISTS tempdb.t_bom_5501;
DROP TABLE IF EXISTS tempdb.t_kit_5501;
DROP TABLE IF EXISTS tempdb.t_rr_5501;
DROP TABLE IF EXISTS tempdb.t_var_5501;
DROP TABLE IF EXISTS tempdb.t_sku_5501;
DROP TABLE IF EXISTS tempdb.t_rio_5501;
DROP TABLE IF EXISTS tempdb.t_total_qty_rio_5501;
DROP TABLE IF EXISTS tempdb.t_rr_5501_max_week;

-- Create main temporary table with primary key
CREATE TABLE tempdb.rds_tmp
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    b.abc_code,
    b.prod_type,
    CAST(NULL AS INT) as pp,
    CAST(NULL AS INT) as pur_vend_no,
    b.vend_no,
    b.prod_code,
    b.vpl_no,
    CAST(NULL AS VARCHAR(40)) as vpl_code,
    b.part_no,
    b.sku_no,
    1 as inv_type,
    COALESCE(b.po_cost, 0) as base_cost,
    CAST(NULL AS DECIMAL(18,2)) as bom_base_cost,
    CAST(NULL AS DECIMAL(18,2)) as bom_system_cost,
    CAST(NULL AS INT) as it_qty1,
    CAST(NULL AS INT) as it_qty2,
    CAST(NULL AS INT) as it_qty3,
    CAST(NULL AS INT) as it_qty4,
    CAST(NULL AS INT) as it_qty5e,
    CAST(NULL AS INT) as it_qty6e,
    CAST(NULL AS INT) as it_qty7e,
    CAST(NULL AS INT) as it_qty8e,
    CAST(NULL AS INT) as it_qty9e,
    CAST(NULL AS INT) as it_qty8e1,
    CAST(NULL AS INT) as it_qty8e2,
    CAST(NULL AS INT) as it_qty9e1,
    CAST(NULL AS INT) as it_qty9e2,
    CAST(NULL AS INT) as it_qty9e3,
    CAST(NULL AS INT) as it_qty9e4,
    CAST(NULL AS INT) as it_qty10e,
    CAST(NULL AS INT) as oh,
    SUM(a.on_order_qty) as oo,
    SUM(a.bo_qty) as bo,
    SUM(a.alloc_qty) as alloc,
    SUM(a.intran_in) as it,
    SUM(a.wip_qty) as wip,
    SUM(a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty) as avail,
    SUM(COALESCE(on_hand_qty, 0) + COALESCE(intran_in, 0)) as total,
    SUM(COALESCE(on_hand_qty, 0) + COALESCE(intran_in, 0)) * COALESCE(b.po_cost, 0) as ext_amt,
    CAST(0 AS INT) as other,
    SUM(CASE WHEN loc_no = 3 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DFR,
    SUM(CASE WHEN loc_no = 4 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DAT,
    SUM(CASE WHEN loc_no = 502 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DGA,
    SUM(CASE WHEN loc_no = 503 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DSW,
    SUM(CASE WHEN loc_no = 504 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DIN,
    SUM(CASE WHEN loc_no = 505 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DFW,
    SUM(CASE WHEN loc_no = 506 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DFO,
    SUM(CASE WHEN loc_no = 507 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DGR,
    SUM(CASE WHEN loc_no = 6 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DCH,
    SUM(CASE WHEN loc_no = 7 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DTN,
    SUM(CASE WHEN loc_no = 9 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DDC,
    SUM(CASE WHEN loc_no = 10 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DOR,
    SUM(CASE WHEN loc_no = 12 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DON,
    SUM(CASE WHEN loc_no = 14 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DOH,
    SUM(CASE WHEN loc_no = 16 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DFL,
    SUM(CASE WHEN loc_no = 27 THEN COALESCE(a.on_hand_qty, 0) + COALESCE(a.intran_in, 0) ELSE 0 END) as DNW,
    CAST(0 AS INT) as rr10,
    CAST(0 AS INT) as rr4,
    CAST(0 AS INT) as rr2,
    CAST(0 AS INT) as rr1,
    CAST(0 AS INT) as wtd,
    b.mfg_partno,
    CAST(NULL AS VARCHAR(60)) as pur_vend_name,
    CAST(NULL AS VARCHAR(60)) as vend_name,
    SUM(on_hand_qty) as on_hand,
    CAST(NULL AS VARCHAR(50)) as us_buyer,
    CAST(NULL AS VARCHAR(50)) as us_manager,
    CAST(NULL AS VARCHAR(50)) as PM,
    CAST(NULL AS INT) as qty60up,
    CAST(NULL AS DECIMAL(18,2)) as age60up,
    CAST(NULL AS DECIMAL(18,2)) as age90up,
    CAST(NULL AS INT) as qty270up,
    CAST(NULL AS DECIMAL(18,2)) as age270up,
    b.short_desc,
    b.long_desc,
    CAST(NULL AS INT) as total_qty_rio,
    CAST(NULL AS INT) as Other_RIO,
    CAST(NULL AS INT) as DFR_RIO,
    CAST(NULL AS INT) as DAT_RIO,
    CAST(NULL AS INT) as DGA_RIO,
    CAST(NULL AS INT) as DSW_RIO,
    CAST(NULL AS INT) as DIN_RIO,
    CAST(NULL AS INT) as DFW_RIO,
    CAST(NULL AS INT) as DFO_RIO,
    CAST(NULL AS INT) as DGR_RIO,
    CAST(NULL AS INT) as DCH_RIO,
    CAST(NULL AS INT) as DTN_RIO,
    CAST(NULL AS INT) as DDC_RIO,
    CAST(NULL AS INT) as DOR_RIO,
    CAST(NULL AS INT) as DON_RIO,
    CAST(NULL AS INT) as DOH_RIO,
    CAST(NULL AS INT) as DFL_RIO,
    CAST(NULL AS INT) as DNW_RIO
FROM  ods_us.ods_cis_corp_part_master_rt b
LEFT JOIN dw_us.dwd_disty_inv_qty_df a
ON b.sku_no = a.sku_no
AND a.inv_type = 1
AND a.date_flag = cast(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) as date)
WHERE b.prod_type IN ('A', 'K', 'R', 'S')
AND b.abc_code IN ('A', 'B', 'C', 'T', 'E')
AND b.vend_no IN (13439, 50633)
GROUP BY b.abc_code,
    b.prod_type,
    b.vend_no,
    b.prod_code,
    b.vpl_no,
    b.part_no,
    b.sku_no,
    a.inv_type,
    COALESCE(b.po_cost, 0),
    b.mfg_partno,
    b.short_desc,
    b.long_desc;

-- Create sku table
CREATE TABLE tempdb.t_sku_5501
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    sku_no
FROM tempdb.rds_tmp
GROUP BY sku_no;

-- Create RIO table
CREATE TABLE tempdb.t_rio_5501
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    cws.sku_no,
    cws.inv_type,
    SUM(CASE WHEN loc_no = 3 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DFR_RIO,
    SUM(CASE WHEN loc_no = 4 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DAT_RIO,
    SUM(CASE WHEN loc_no = 502 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DGA_RIO,
    SUM(CASE WHEN loc_no = 503 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DSW_RIO,
    SUM(CASE WHEN loc_no = 504 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DIN_RIO,
    SUM(CASE WHEN loc_no = 505 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DFW_RIO,
    SUM(CASE WHEN loc_no = 506 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DFO_RIO,
    SUM(CASE WHEN loc_no = 507 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DGR_RIO,
    SUM(CASE WHEN loc_no = 6 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DCH_RIO,
    SUM(CASE WHEN loc_no = 7 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DTN_RIO,
    SUM(CASE WHEN loc_no = 9 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DDC_RIO,
    SUM(CASE WHEN loc_no = 10 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DOR_RIO,
    SUM(CASE WHEN loc_no = 12 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DON_RIO,
    SUM(CASE WHEN loc_no = 14 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DOH_RIO,
    SUM(CASE WHEN loc_no = 16 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DFL_RIO,
    SUM(CASE WHEN loc_no = 27 THEN COALESCE(cws.order_qty, 0) ELSE 0 END) as DNW_RIO
FROM ods_us.ods_cis_corp_cws_cop_ship_progress cws
INNER JOIN tempdb.t_sku_5501 t ON cws.sku_no = t.sku_no
WHERE cws.order_type = 18
GROUP BY cws.sku_no, cws.inv_type;

-- Update main table with RIO data
UPDATE tempdb.rds_tmp
SET DFR_RIO = b.DFR_RIO,
    DAT_RIO = b.DAT_RIO,
    DGA_RIO = b.DGA_RIO,
    DSW_RIO = b.DSW_RIO,
    DIN_RIO = b.DIN_RIO,
    DFW_RIO = b.DFW_RIO,
    DFO_RIO = b.DFO_RIO,
    DGR_RIO = b.DGR_RIO,
    DCH_RIO = b.DCH_RIO,
    DTN_RIO = b.DTN_RIO,
    DDC_RIO = b.DDC_RIO,
    DOR_RIO = b.DOR_RIO,
    DON_RIO = b.DON_RIO,
    DOH_RIO = b.DOH_RIO,
    DFL_RIO = b.DFL_RIO,
    DNW_RIO = b.DNW_RIO
FROM tempdb.t_rio_5501 b
WHERE rds_tmp.sku_no = b.sku_no
    AND rds_tmp.inv_type = b.inv_type;


create table tempdb.t_total_qty_rio_5501 as
SELECT sku_no, inv_type, SUM(COALESCE(cws.order_qty, 0)) as total_qty_rio
FROM tempdb.ods_cis_corp_cws_cop_ship_progress cws
WHERE cws.order_type = 18
GROUP BY cws.sku_no, cws.inv_type;

-- Update total_qty_rio
UPDATE tempdb.rds_tmp
SET total_qty_rio = b.total_qty_rio
FROM tempdb.t_total_qty_rio_5501 b
WHERE rds_tmp.sku_no = b.sku_no
    AND rds_tmp.inv_type = b.inv_type;

-- Update Other_RIO
UPDATE tempdb.rds_tmp
SET Other_RIO = total_qty_rio
    - DFR_RIO
    - DAT_RIO
    - DGA_RIO
    - DSW_RIO
    - DIN_RIO
    - DFW_RIO
    - DFO_RIO
    - DGR_RIO
    - DCH_RIO
    - DTN_RIO
    - DDC_RIO
    - DOR_RIO
    - DON_RIO
    - DOH_RIO
    - DFL_RIO
    - DNW_RIO;

-- Update inventory aging data
UPDATE tempdb.rds_tmp
SET it_qty1 = CAST(ROUND(COALESCE(a.age1_30 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty2 = CAST(ROUND(COALESCE(a.age31_60 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty3 = CAST(ROUND(COALESCE(a.age61_90 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty4 = CAST(ROUND(COALESCE(a.age90_up / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty5e = CAST(ROUND(COALESCE(a.age91_120 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty6e = CAST(ROUND(COALESCE(a.age121_150 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty7e = CAST(ROUND(COALESCE(a.age151_180 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty8e = CAST(ROUND(COALESCE(a.age180_up / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty9e = CAST(ROUND(COALESCE(a.age240_up / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty8e1 = CAST(ROUND(COALESCE(a.age181_210 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty8e2 = CAST(ROUND(COALESCE(a.age211_240 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty9e1 = CAST(ROUND(COALESCE(a.age241_270 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty9e2 = CAST(ROUND(COALESCE(a.age271_300 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty9e3 = CAST(ROUND(COALESCE(a.age301_330 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty9e4 = CAST(ROUND(COALESCE(a.age331_360 / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    it_qty10e = CAST(ROUND(COALESCE(a.age360_up / NULLIF(COALESCE(a.ave_cost, 0), 0), 0), 0) AS INT),
    oh = COALESCE(a.on_hand_qty, 0)
FROM dw_us.dwd_disty_inv_aging_df a
WHERE a.sku_no = rds_tmp.sku_no
    AND a.date_flag = cast(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) as date)
    AND a.view_level = 'IT_PART'
    AND a.inv_type = 1;

CREATE TABLE tempdb.t_rr_5501_max_week PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id, max(week) as max_week
FROM dw_us.dws_disty_pur_ips_runrate_1w
WHERE sum_type = 'WITYPESTD';

-- Create runrate table
CREATE TABLE tempdb.t_rr_5501
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    b.sku_no,
    b.inv_type
   ,SUM(CASE WHEN b.week=c.max_week THEN b.runrate_qty ELSE 0 END) AS wtd
    ,SUM(CASE WHEN b.week=c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr1
    ,SUM(CASE WHEN b.week BETWEEN c.max_week-2  AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr2
    ,SUM(CASE WHEN b.week BETWEEN c.max_week-4  AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr4
    ,SUM(CASE WHEN b.week BETWEEN c.max_week-10 AND c.max_week-1 THEN b.runrate_qty ELSE 0 END) AS rr10
FROM
    dw_us.dws_disty_pur_ips_runrate_1w b
JOIN
    ods_us.ods_cis_corp_part_master_rt a
ON
    a.sku_no = b.sku_no
JOIN tempdb.t_rr_5501_max_week c
ON
    1=1
WHERE c.max_week-10 <= b.week
AND
    b.sum_type = 'WITYPESTD'
GROUP BY
    b.sku_no, b.inv_type;


-- Update main table with runrate data
UPDATE tempdb.rds_tmp
SET rr10 = b.rr10,
    rr4 = b.rr4,
    rr2 = b.rr2,
    rr1 = b.rr1,
    wtd = b.wtd
FROM tempdb.t_rr_5501 b
WHERE rds_tmp.sku_no = b.sku_no
    AND rds_tmp.inv_type = b.inv_type;

-- Create BOM table
CREATE TABLE tempdb.t_bom_5501
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    a.sku_no,
    b.comp_no,
    b.comp_qty,
    b.bom_line_no,
    CAST(NULL AS DECIMAL(18,2)) as ave_cost,
    CAST(NULL AS DECIMAL(18,2)) as po_cost
FROM tempdb.rds_tmp a
JOIN ods_us.ods_cis_corp_bom_rt b ON a.sku_no = b.sku_no
WHERE a.prod_type IN ('K', 'A');

-- Update BOM table with costs
UPDATE tempdb.t_bom_5501
SET ave_cost = COALESCE(COALESCE(b.ave_cost, b.po_cost), 0),
    po_cost = COALESCE(b.po_cost, 0)
FROM ods_us.ods_cis_corp_part_master_rt b
WHERE t_bom_5501.comp_no = b.sku_no;

-- Create cost variance table
CREATE TABLE tempdb.t_var_5501
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    a.sku_no,
    SUM(b.cost_variance) as cost_variance
FROM tempdb.rds_tmp a
JOIN ods_us.ods_cis_corp_bom_cost_var_rt b ON a.sku_no = b.sku_no
WHERE a.prod_type IN ('K', 'A')
GROUP BY a.sku_no;

-- Create kit table
CREATE TABLE tempdb.t_kit_5501
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    sku_no,
    SUM(comp_qty * ave_cost) as bom_system_cost,
    SUM(comp_qty * po_cost) as bom_base_cost,
    CAST(NULL AS DECIMAL(18,2)) as cost_variance
FROM tempdb.t_bom_5501
GROUP BY sku_no;

-- Update kit table with cost variance
UPDATE tempdb.t_kit_5501
SET cost_variance = b.cost_variance
FROM tempdb.t_var_5501 b
WHERE t_kit_5501.sku_no = b.sku_no;

-- Update main table with BOM costs
UPDATE tempdb.rds_tmp
SET bom_system_cost = b.bom_system_cost + COALESCE(b.cost_variance, 0),
    bom_base_cost = b.bom_base_cost + COALESCE(b.cost_variance, 0)
FROM tempdb.t_kit_5501 b
WHERE rds_tmp.sku_no = b.sku_no;

-- Update inventory quantities with aging logic
UPDATE tempdb.rds_tmp
SET it_qty1 = CASE WHEN on_hand < it_qty1 THEN on_hand ELSE it_qty1 END,
    on_hand = on_hand - it_qty1;

UPDATE tempdb.rds_tmp
SET it_qty2 = CASE WHEN on_hand < it_qty2 THEN on_hand ELSE it_qty2 END,
    on_hand = on_hand - it_qty2;

UPDATE tempdb.rds_tmp
SET it_qty3 = CASE WHEN on_hand < it_qty3 THEN on_hand ELSE it_qty3 END,
    on_hand = on_hand - it_qty3;

UPDATE tempdb.rds_tmp
SET it_qty4 = on_hand;

UPDATE tempdb.rds_tmp
SET it_qty5e = CASE WHEN on_hand < it_qty5e THEN on_hand ELSE it_qty5e END,
    on_hand = on_hand - it_qty5e;

UPDATE tempdb.rds_tmp
SET it_qty6e = CASE WHEN on_hand < it_qty6e THEN on_hand ELSE it_qty6e END,
    on_hand = on_hand - it_qty6e;

UPDATE tempdb.rds_tmp
SET it_qty7e = CASE WHEN on_hand < it_qty7e THEN on_hand ELSE it_qty7e END,
    on_hand = on_hand - it_qty7e;

UPDATE tempdb.rds_tmp
SET it_qty8e1 = CASE WHEN on_hand < it_qty8e1 THEN on_hand ELSE it_qty8e1 END,
    on_hand = on_hand - it_qty8e1;

UPDATE tempdb.rds_tmp
SET it_qty8e2 = CASE WHEN on_hand < it_qty8e2 THEN on_hand ELSE it_qty8e2 END,
    on_hand = on_hand - it_qty8e2;

UPDATE tempdb.rds_tmp
SET it_qty9e1 = CASE WHEN on_hand < it_qty9e1 THEN on_hand ELSE it_qty9e1 END,
    on_hand = on_hand - it_qty9e1;

UPDATE tempdb.rds_tmp
SET it_qty9e2 = CASE WHEN on_hand < it_qty9e2 THEN on_hand ELSE it_qty9e2 END,
    on_hand = on_hand - it_qty9e2;

UPDATE tempdb.rds_tmp
SET it_qty9e3 = CASE WHEN on_hand < it_qty9e3 THEN on_hand ELSE it_qty9e3 END,
    on_hand = on_hand - it_qty9e3;

UPDATE tempdb.rds_tmp
SET it_qty9e4 = CASE WHEN on_hand < it_qty9e4 THEN on_hand ELSE it_qty9e4 END,
    on_hand = on_hand - it_qty9e4;

UPDATE tempdb.rds_tmp
SET it_qty10e = CASE WHEN on_hand < it_qty10e THEN on_hand ELSE it_qty10e END,
    on_hand = on_hand - it_qty10e;

-- Update other quantity
UPDATE tempdb.rds_tmp
SET other = total
    - DFR
    - DAT
    - DGA
    - DSW
    - DIN
    - DFW
    - DFO
    - DGR
    - DCH
    - DTN
    - DDC
    - DOR
    - DON
    - DOH
    - DFL
    - DNW;

-- Update product detail
UPDATE tempdb.rds_tmp
SET pp = ppd.data_no
FROM ods_us.ods_cis_corp_part_prod_detail_rt ppd
WHERE rds_tmp.sku_no = ppd.sku_no
    AND ppd.prod_code = 0
    AND ppd.col_no = 1;

-- Update VPL code
UPDATE tempdb.rds_tmp
SET vpl_code = dvp.vpl_code
FROM ods_us.ods_cis_corp_dw_vend_pl_rt dvp
WHERE rds_tmp.vpl_no = dvp.vpl_no;

-- Update vendor name
UPDATE tempdb.rds_tmp
SET vend_name = dvp.vend_name
FROM ods_us.ods_cis_corp_vend_master_rt dvp
WHERE rds_tmp.vend_no = dvp.vend_no;


-- Update purchase vendor number
UPDATE tempdb.rds_tmp
SET pur_vend_no = x.xref_no
FROM ods_us.ods_cis_corp_vendor_xref_rt x
WHERE rds_tmp.vend_no = x.vend_no
    AND x.xref_type = 'VEND_PURCH'
    AND x.active = 'Y';

-- Set default purchase vendor number
UPDATE tempdb.rds_tmp
SET pur_vend_no = COALESCE(pur_vend_no, vend_no);

-- Update purchase vendor name
UPDATE tempdb.rds_tmp
SET pur_vend_name = dvp.vend_name
FROM ods_us.ods_cis_corp_vend_master_rt dvp
WHERE rds_tmp.pur_vend_no = dvp.vend_no;


-- Update US buyer
UPDATE tempdb.rds_tmp
SET us_buyer = CONCAT(c.firstname, c.lastname)
FROM ods_us.ods_cis_corp_vend_user_matrix_rt b
JOIN dim_us.dim_pub_manager c ON CAST(b.primary_id AS INT) = c.userid
WHERE rds_tmp.vpl_no = b.vpl_no
    AND rds_tmp.vend_no = b.vend_no
    AND b.profile_type = 'BUYR';

UPDATE tempdb.rds_tmp
SET us_buyer = CONCAT(c.firstname, c.lastname)
FROM ods_us.ods_cis_corp_vend_user_matrix_rt b
JOIN dim_us.dim_pub_manager c ON CAST(b.primary_id AS INT) = c.userid
WHERE -1 = b.vpl_no
    AND rds_tmp.vend_no = b.vend_no
    AND b.profile_type = 'BUYR'
    AND rds_tmp.us_buyer IS NULL;

-- Update US manager
UPDATE tempdb.rds_tmp
SET us_manager = CONCAT(c.firstname, c.lastname)
FROM ods_us.ods_cis_corp_vend_user_matrix_rt b
JOIN dim_us.dim_pub_manager c ON CAST(b.manager_id AS INT) = c.userid
WHERE rds_tmp.vpl_no = b.vpl_no
    AND rds_tmp.vend_no = b.vend_no
    AND b.profile_type = 'BUYR';

UPDATE tempdb.rds_tmp
SET us_manager = CONCAT(c.firstname, c.lastname)
FROM ods_us.ods_cis_corp_vend_user_matrix_rt b
JOIN dim_us.dim_pub_manager c ON CAST(b.manager_id AS INT) = c.userid
WHERE -1 = b.vpl_no
    AND rds_tmp.vend_no = b.vend_no
    AND b.profile_type = 'BUYR'
    AND rds_tmp.us_manager IS NULL;

-- Update PM
UPDATE tempdb.rds_tmp
SET PM = CONCAT(c.firstname, c.lastname)
FROM ods_us.ods_cis_corp_vend_user_matrix_rt b
JOIN dim_us.dim_pub_manager c ON CAST(b.primary_id AS INT) = c.userid
WHERE rds_tmp.vpl_no = b.vpl_no
    AND rds_tmp.vend_no = b.vend_no
    AND b.profile_type = 'PM';

UPDATE tempdb.rds_tmp
SET PM = CONCAT(c.firstname, c.lastname)
FROM ods_us.ods_cis_corp_vend_user_matrix_rt b
JOIN dim_us.dim_pub_manager c ON CAST(b.primary_id AS INT) = c.userid
WHERE -1 = b.vpl_no
    AND rds_tmp.vend_no = b.vend_no
    AND b.profile_type = 'PM'
    AND rds_tmp.PM IS NULL;

-- Update aging calculations
UPDATE tempdb.rds_tmp
SET qty60up = it_qty3 + it_qty4,
    age60up = (it_qty3 + it_qty4) * base_cost,
    age90up = it_qty4 * base_cost,
    qty270up = it_qty9e2 + it_qty9e3 + it_qty9e4 + it_qty10e,
    age270up = (it_qty9e2 + it_qty9e3 + it_qty9e4 + it_qty10e) * base_cost
    where 1=1;

-- Delete specific part numbers
DELETE FROM tempdb.rds_tmp WHERE part_no LIKE 'XERX-%';
DELETE FROM tempdb.rds_tmp WHERE part_no LIKE '%-DE';

-- Create body table
CREATE TABLE tempdb.rds_tmp_body
PRIMARY KEY(id) DISTRIBUTED BY HASH(id) AS
SELECT uuid_numeric() as id,
    vend_no,
    vend_name,
    'standard' as body_type,
    COUNT(*) as cnt,
    vend_name as sub_name
FROM tempdb.rds_tmp
GROUP BY vend_no, vend_name;

-- Clean up temporary tables
DROP TABLE IF EXISTS tempdb.t_loc_5501;
DROP TABLE IF EXISTS tempdb.t_bom_5501;
DROP TABLE IF EXISTS tempdb.t_kit_5501;
DROP TABLE IF EXISTS tempdb.t_rr_5501;
DROP TABLE IF EXISTS tempdb.t_var_5501;
DROP TABLE IF EXISTS tempdb.t_sku_5501;
DROP TABLE IF EXISTS tempdb.t_rio_5501;
DROP TABLE IF EXISTS tempdb.t_total_qty_rio_5501;
DROP TABLE IF EXISTS tempdb.t_rr_5501_max_week;
