-- ============================================================
-- Drop temp tables if they exist
-- ============================================================
DROP TABLE IF EXISTS rdsetl.rds_tmp;
DROP TABLE IF EXISTS rdsetl.rds_tmp_body;
DROP TABLE IF EXISTS t_vpg_802;
DROP TABLE IF EXISTS t_vpl_802;
DROP TABLE IF EXISTS t_sls_802;

-- ============================================================
-- t_vpg_802: vendor product group filter
-- ============================================================
CREATE LOCAL TEMPORARY TABLE t_vpg_802 (
    vpc_group_id   INT,
    vpc_group_desc VARCHAR(200)
) ON COMMIT PRESERVE ROWS;

INSERT INTO t_vpg_802 (vpc_group_id, vpc_group_desc)
SELECT vpc_group_id, vpc_group_desc
FROM dim_ca.dim_pub_vpc_group_view
WHERE vpc_group_id IN (120, 119, 118)
   OR vpc_group_desc LIKE '%Audio/Video - Projector%';

-- ============================================================
-- t_vpl_802: vendor product line filter (multi-criteria UNION)
-- ============================================================
CREATE LOCAL TEMPORARY TABLE t_vpl_802 (
    vpl_no   INT,
    vpl_code VARCHAR(60),
    vpl_desc VARCHAR(200),
    vend_no  INT
) ON COMMIT PRESERVE ROWS;

INSERT INTO t_vpl_802 (vpl_no, vpl_code, vpl_desc, vend_no)

-- From vpc_group cross-reference
SELECT c.vpl_no, c.vpl_code, c.vpl_desc, c.vend_no
FROM t_vpg_802 a
JOIN dim_ca.dim_pub_vpc_group_xref_view b ON a.vpc_group_id = b.vpc_group_id
JOIN dim_ca.dim_pub_vpl_info            c ON b.vpl_no = c.vpl_no

UNION

-- HP BO
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_no = 15844

UNION

-- Explicit vpl_no list
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_no IN (
    14806, 14807, 14808, 14809, 14810, 14998, 14999, 15000,
    15001, 15002, 15012, 15013, 15014, 15015, 15016, 15020,
    15021, 15022, 15023, 15024, 15028, 15029, 15030, 15031, 15032,
    15033, 15034, 15035, 15036, 15037, 15038, 15039, 15040, 15041,
    15042, 15043, 15046, 15047, 15048, 15049, 15050, 15051, 15052,
    15053, 15054, 15055, 15056, 15057, 15058, 15059, 15060, 15061,
    15062, 15063, 15064, 15065, 15066, 15067, 16082, 16083, 16084,
    17647, 17648, 1146, 34696, 34697, 23814, 71601, 71602, 71603
)

UNION

-- TVLCDsmall, TVLCD, ACC-LG, Medical vpl codes (active only)
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
JOIN dim_ca.dim_pub_vpc_group_xref_view c ON a.vpl_no = c.vpl_no
JOIN dim_ca.dim_pub_vpc_group_view      b ON b.vpc_group_id = c.vpc_group_id
WHERE a.vpl_code IN ('TVLCDsmall', 'TVLCD', 'ACC-LG', 'Medical')
  AND a.active = 'Y'

UNION

-- PJONLINE, PJVAR vpl codes (active only)
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
JOIN dim_ca.dim_pub_vpc_group_xref_view c ON a.vpl_no = c.vpl_no
JOIN dim_ca.dim_pub_vpc_group_view      b ON b.vpc_group_id = c.vpc_group_id
WHERE a.vpl_code IN ('PJONLINE', 'PJVAR')
  AND a.active = 'Y'

UNION

-- vend_no 33449
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 33449

UNION

-- vend_no 6443, specific vpl codes
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 6443
  AND UPPER(a.vpl_code) IN ('LCDMONITORS', 'NMSO', 'LFD')

UNION

-- vend_no 1122, excluding specific vpl_no list
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 1122
  AND a.vpl_no NOT IN (
      18424, 20068, 13035, 20504, 20503, 1933,
      20502, 21338, 21339, 21568, 22212, 20497
  )

UNION

-- vend_no 8711, specific vpl codes
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 8711
  AND a.vpl_code IN ('10LCD', '15Interactiv', '20Projectors', '25Acces')

UNION

-- vend_no 100, LED/LCD specific codes
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 100
  AND a.vpl_code IN ('LCD21-22-B2B', 'LCD21-30-B2C', 'LCD24-30-B2B', 'LED SIGNAGE')

UNION

-- vend_no 35738
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 35738
  AND a.vpl_code IN ('LCD19-30-B2C', 'LCD21-30-B2C')

UNION

-- vend_no 36498
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 36498
  AND a.vpl_code IN ('OPENFRAME', 'SLIMLINE', 'DSKTOP MONIT', 'ANDROID', 'DIGITALSIGNA')

UNION

-- vend_no 29447
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 29447
  AND a.vpl_code IN ('DISPLAY-NUL', 'DISPLAY', 'PRJCTR')

UNION

-- Explicit vpl_no list (second group)
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_no IN (
    21320, 19048, 18014, 22044, 22039, 22046, 22043,
    22040, 22045, 22038, 22042, 22041, 22047
)

UNION

-- vend_no 36056
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE COALESCE(a.alt_vend_no, a.vend_no) = 36056

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'PROJECTOR'   AND COALESCE(a.alt_vend_no, a.vend_no) = 35819

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'INSTALLPJ'   AND COALESCE(a.alt_vend_no, a.vend_no) = 773

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'InstallPJ'   AND COALESCE(a.alt_vend_no, a.vend_no) = 2761

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'PRO-AV'      AND COALESCE(a.alt_vend_no, a.vend_no) = 2655

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'PJ-DLP'      AND COALESCE(a.alt_vend_no, a.vend_no) = 36056

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'PJ-LCD'      AND COALESCE(a.alt_vend_no, a.vend_no) = 36056

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'INS PROJ'    AND COALESCE(a.alt_vend_no, a.vend_no) = 2706

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'INSTALLPJ'   AND COALESCE(a.alt_vend_no, a.vend_no) = 21558

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'ProScenePJ'  AND COALESCE(a.alt_vend_no, a.vend_no) = 29798

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'LrgVenuePJ'  AND COALESCE(a.alt_vend_no, a.vend_no) = 29798

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'Installation' AND COALESCE(a.alt_vend_no, a.vend_no) = 12371

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code = 'IC-PJ'        AND COALESCE(a.alt_vend_no, a.vend_no) = 8711

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_code IN ('MONITOR', 'PROJECTOR')
  AND COALESCE(a.alt_vend_no, a.vend_no) = 36259

UNION

-- Explicit vpl_no list (third group)
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vpl_no IN (14484, 22663, 21148, 22147, 23256, 23885, 23056, 24209, 19944, 22025, 24210)

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 36558

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 36751

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 36759

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 8793

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 33411
  AND a.vpl_no  = 24227

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 36829

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 2706
  AND a.vpl_no  = 32440

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 100
  AND a.vpl_no  = 32424

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 773
  AND a.vpl_no  IN (32441, 35108)

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no IN (39776, 40048, 1215)

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 29798
  AND a.vpl_no  = 32233

UNION

-- vend_no 40406 - Daniel, Michelle Support Email Added
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 40406

UNION

-- req# 117610
SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 40509

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 35827

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no = 39407

UNION

SELECT a.vpl_no, a.vpl_code, a.vpl_desc, a.vend_no
FROM dim_ca.dim_pub_vpl_info a
WHERE a.vend_no  = 16996
  AND a.vpl_code IN ('BO', 'BO-SB', 'TB', 'TB-SB');

-- ============================================================
-- t_sls_802: monthly sales by vpl/sku/customer
-- ============================================================
CREATE LOCAL TEMPORARY TABLE t_sls_802 (
    year        INT,
    month       INT,
    cust_no     INT,
    ship_to_name VARCHAR(100),
    vpl_no      INT,
    vend_no     INT,
    sku_no      INT,
    cost        NUMERIC(20,8),
    unit        INT,
    net_sales   NUMERIC(20,8),
    NGM_amt     NUMERIC(20,8),
    OPLGM_amt   NUMERIC(20,8)
) ON COMMIT PRESERVE ROWS;

-- Consolidated insert for the full previous month
-- (replaces the three 10-day chunked inserts in Sybase)
INSERT INTO t_sls_802 (year, month, cust_no, ship_to_name, vpl_no, vend_no, sku_no,
                       cost, unit, net_sales, NGM_amt, OPLGM_amt)
WITH date_range AS (
    SELECT
        MIN(CASE WHEN d.m = cal.cur_m - 1 THEN d.date_flag ELSE NULL END) AS dt_start,
        MIN(CASE WHEN d.m = cal.cur_m     THEN d.date_flag ELSE NULL END) AS dt_end
    FROM dim_ca.dim_pub_date d
    CROSS JOIN (
        SELECT m AS cur_m
        FROM dim_ca.dim_pub_date
        WHERE date_flag = current_date()
        LIMIT 1
    ) cal
)
SELECT
    YEAR(a.date_flag),
    MONTH(a.date_flag),
    a.cust_no,
    c.ship_to_name,
    a.pm_code                                          AS vpl_no,
    b.vend_no,
    a.sku_no,
    SUM(a.u_cost * a.ship_qty)                         AS cost,
    SUM(a.ship_qty)                                    AS unit,
    SUM(a.ship_qty * (a.u_price + COALESCE(a.u_sum_expense, 0))) AS net_sales,
    SUM(a.NGM_amt)                                     AS NGM_amt,
    SUM(a.OPLGM_amt)                                   AS OPLGM_amt
FROM dw_ca.dwd_disty_common_dw_orders_pl_extend_di a
JOIN t_vpl_802                            b  ON a.pm_code    = b.vpl_no
JOIN dw_ca.dwd_pub_common_history_header_extend c  ON a.order_no   = c.order_no
                                            AND a.order_type = c.order_type
CROSS JOIN date_range dr
WHERE a.date_flag >= dr.dt_start
  AND a.date_flag <  dr.dt_end
GROUP BY
    YEAR(a.date_flag),
    MONTH(a.date_flag),
    a.cust_no,
    c.ship_to_name,
    a.pm_code,
    b.vend_no,
    a.sku_no;

-- ============================================================
-- rds_tmp: aggregate by year/month/cust/vend/vpl/sku
-- ============================================================
CREATE LOCAL TEMPORARY TABLE rds_pl_ca802 ON COMMIT PRESERVE ROWS AS
SELECT
    year,
    month,
    cust_no                      AS master_acct,
    cust_no,
    CAST(NULL AS VARCHAR(60))    AS cust_name,
    ship_to_name,
    vend_no,
    CAST(NULL AS VARCHAR(60))    AS vend_name,
    vpl_no,
    CAST(NULL AS VARCHAR(60))    AS vpl_code,
    CAST(NULL AS VARCHAR(60))    AS vpl_desc,
    sku_no,
    CAST(NULL AS VARCHAR(60))    AS part_no,
    SUM(cost)                    AS cost,
    SUM(unit)                    AS units,
    SUM(net_sales)               AS net_sales,
    SUM(NGM_amt)                 AS NGM_amt,
    CAST(NULL AS VARCHAR(60))    AS NGM_pct,
    SUM(OPLGM_amt)               AS OPLGM_amt,
    CAST(NULL AS VARCHAR(60))    AS OPL_pct
FROM t_sls_802
GROUP BY year, month, cust_no, vend_no, vpl_no, ship_to_name, sku_no;

-- ============================================================
-- Remove zero-cost zero-unit rows
-- ============================================================
DELETE FROM rds_pl_ca802
WHERE cost  = 0
  AND units = 0;

-- ============================================================
-- Update percentage columns where net_sales is non-zero
-- ============================================================
UPDATE rds_pl_ca802
SET NGM_pct = CAST(100 * NGM_amt   / net_sales AS VARCHAR(60)) || '%',
    OPL_pct = CAST(100 * OPLGM_amt / net_sales AS VARCHAR(60)) || '%'
WHERE net_sales <> 0;

-- ============================================================
-- Update part_no from part_master
-- ============================================================
UPDATE rds_pl_ca802
SET part_no = b.part_no
FROM dim_ca.dim_pub_part_info b
WHERE rds_pl_ca802.sku_no = b.sku_no;

-- ============================================================
-- Update cust_name from customer_header
-- ============================================================
UPDATE rds_pl_ca802
SET cust_name = b.cust_name
FROM dim_ca.dim_pub_customer_info b
WHERE rds_pl_ca802.cust_no = b.cust_no;

-- ============================================================
-- Update vend_name from vend_master
-- ============================================================
UPDATE rds_pl_ca802
SET vend_name = b.vend_name
FROM dim_ca.dim_pub_vendor_info b
WHERE rds_pl_ca802.vend_no = b.vend_no;

-- ============================================================
-- Update vpl_code and vpl_desc from dw_vend_pl
-- ============================================================
UPDATE rds_pl_ca802
SET vpl_code = b.vpl_code,
    vpl_desc = b.vpl_desc
FROM dim_ca.dim_pub_vpl_info b
WHERE rds_pl_ca802.vpl_no = b.vpl_no;

-- ============================================================
-- Set master_acct to cust_no (default)
-- ============================================================
UPDATE rds_pl_ca802
SET master_acct = cust_no;

-- ============================================================
-- Override master_acct with xref parent account where applicable
-- ============================================================
UPDATE rds_pl_ca802
SET master_acct = b.xref_no
FROM dim_ca.dim_pub_cust_xref_all b
WHERE rds_pl_ca802.cust_no   = b.cust_no
  AND b.xref_type       = 'MASTER_SUB'
  AND b.active          = 'Y';
  
create table rdsetl.rds_tmp as
select * from rds_pl_ca802;

-- ============================================================
-- rds_tmp_body: email body metadata
-- ============================================================
create table rdsetl.rds_tmp_body as
SELECT 'standard' AS body_type,
       COUNT(*) AS cnt
  FROM rdsetl.rds_tmp;

-- ============================================================
-- Cleanup intermediate tables
-- ============================================================
DROP TABLE IF EXISTS t_vpg_802;
DROP TABLE IF EXISTS t_vpl_802;
DROP TABLE IF EXISTS t_sls_802;
DROP TABLE IF EXISTS rds_pl_ca802;
