DROP TABLE IF EXISTS rds_wcla610_t1;
CREATE LOCAL TEMPORARY TABLE rds_wcla610_t1 ON COMMIT PRESERVE ROWS AS 
WITH temp_t1 AS (
    SELECT order_no
        ,a.order_type
        ,a.order_line_no
        ,a.sku_no
        ,a.eu_company_name AS EU_company_name
        ,a.eu_address1 AS EU_address1
        ,a.eu_address2 AS EU_address2
        ,a.eu_city AS EU_city
        ,a.eu_state AS EU_state
        ,a.eu_zip AS EU_zip
        ,a.eu_country AS EU_country
        ,a.eu_contact_name AS EU_contact_name
        ,a.eu_contact_phone AS EU_phone
        ,a.ship_to_name
        ,a.ship_to_addr
        ,a.ship_to_city
        ,a.ship_to_state
        ,a.ship_to_zip
        ,a.ship_to_country
        ,a.sold_to_cust_no
        ,a.sold_to_cust_name
        ,a.bill_to_cust_no
        ,a.bill_to_cust_name
        ,a.bill_to_cust_addr AS bill_to_address
        ,CAST(NULL AS VARCHAR(60)) AS bill_to_address2
        ,a.bill_to_cust_city
        ,a.bill_to_cust_state
        ,a.bill_to_cust_zip
        ,a.bill_to_cust_country
        ,a.bill_to_contact_name
        ,a.bill_to_contact_phone
        ,a.sales_terr
        ,CAST(NULL AS VARCHAR(60)) AS terr_manager
        ,a.ship_qty
        ,a.mfg_partno AS vend_part_no
        ,a.invoice_date
        ,a.unit_price AS u_price
        ,a.unit_price - a.unit_sum_exp AS extended_unit_price
        ,CASE WHEN a.from_loc_no = 98 THEN 'DROP' ELSE 'STCK' END AS drop_ship_flag
        ,a.int_ref_no
        ,a.int_ref_type
        ,a.from_loc_no
        ,a.inv_type
        ,CAST(NULL AS INT) AS doc_no_order
        ,CAST(NULL AS VARCHAR(200)) AS vend_inv_no
    FROM dw_wcla.dwd_disty_common_pos_di a
    WHERE a.date_flag >= CURRENT_DATE() - 7
        AND a.date_flag < CURRENT_DATE()
        AND a.order_line_type NOT IN ('Comp')
        AND a.vend_no IN (32991, 30040, 30060, 30070, 33001, 30068)
        AND a.order_type = 1
        AND UPPER(a.mfg_partno) NOT LIKE 'ARUBA%'
)
SELECT a.order_no
    ,a.order_type
    ,a.order_line_no
    ,a.sku_no
    ,a.EU_company_name
    ,a.EU_address1
    ,a.EU_address2
    ,a.EU_city
    ,a.EU_state
    ,a.EU_zip
    ,a.EU_country
    ,a.EU_contact_name
    ,a.EU_phone
    ,a.ship_to_name
    ,a.ship_to_addr
    ,a.ship_to_city
    ,a.ship_to_state
    ,a.ship_to_zip
    ,a.ship_to_country
    ,a.sold_to_cust_no
    ,a.sold_to_cust_name
    ,b.address1a AS sold_to_addr
    ,b.city1a AS sold_to_city
    ,b.state AS sold_to_state
    ,b.zip_code AS sold_to_zip
    ,b.country AS sold_to_country
    ,b.contact_name AS sold_to_contact_name
    ,b.phone_no AS sold_to_contact_phone
    ,a.bill_to_cust_no
    ,a.bill_to_cust_name
    ,a.bill_to_address
    ,a.bill_to_address2
    ,a.bill_to_cust_city
    ,a.bill_to_cust_state
    ,a.bill_to_cust_zip
    ,a.bill_to_cust_country
    ,a.bill_to_contact_name
    ,a.bill_to_contact_phone
    ,a.sales_terr
    ,a.terr_manager
    ,a.ship_qty
    ,a.vend_part_no
    ,a.invoice_date
    ,a.u_price
    ,a.extended_unit_price
    ,a.drop_ship_flag
    ,a.int_ref_no
    ,a.int_ref_type
    ,a.from_loc_no
    ,a.inv_type
    ,a.doc_no_order
    ,a.vend_inv_no
FROM temp_t1 a
LEFT JOIN (
    SELECT b.*
        ,ROW_NUMBER() OVER(PARTITION BY b.cust_no ORDER BY b.entry_datetime_contact DESC) AS rn1
    FROM temp_t1 a
    INNER JOIN dim_wcla.dim_pub_customer_address_contacts_info b
        ON a.sold_to_cust_no = b.cust_no
        AND b.xref_seq = 1
) b
    ON a.sold_to_cust_no = b.cust_no
    AND b.rn1 = 1
ORDER BY order_no, order_type, order_line_no;


DROP TABLE IF EXISTS rds_wcla610_t2;
CREATE LOCAL TEMPORARY TABLE rds_wcla610_t2 ON COMMIT PRESERVE ROWS AS 
WITH temp_spa AS (
    SELECT a.order_no
        ,a.order_type
        ,a.order_line_no
        ,b.scm_no
        ,b.spa_no
        ,ROW_NUMBER() OVER(PARTITION BY a.order_no, a.order_type, a.order_line_no ORDER BY b.scm_no) AS rn
    FROM rds_wcla610_t1 a
    INNER JOIN dw_wcla.dwd_pub_common_shipped_order_scm_spa_detail_di b
        ON a.order_no = b.order_no
        AND a.order_type = b.order_type
        AND a.order_line_no = b.order_line_no
)
SELECT a.*
    ,b.scm_no AS scm_no_1
    ,b.spa_no AS spa_no1
    ,c.deal_id
FROM rds_wcla610_t1 a
LEFT JOIN temp_spa b
    ON a.order_no = b.order_no
    AND a.order_type = b.order_type
    AND a.order_line_no = b.order_line_no
    AND b.rn = 1
LEFT JOIN (
    SELECT DISTINCT a.order_no
        ,a.order_type
        ,b.data_c AS deal_id
    FROM rds_wcla610_t1 a
    INNER JOIN dw_wcla.dwd_disty_sales_eu_custom_di b
        ON a.order_no = b.order_no
        AND a.order_type = b.order_type
        AND b.order_line_no = 0
    INNER JOIN dim_wcla.dim_pub_eu_custom_map_view m
        ON b.eu_map_id = m.eu_map_id
        AND b.eu_map_line_no = m.eu_map_line_no
        AND m.delete_date IS NULL
    INNER JOIN dim_wcla.dim_pub_list_box_detail l
        ON l.code_value = m.map_data_desc
        AND l.delete_datetime IS NULL
    WHERE l.list_box_code = 'CEDM'
        AND l.code_desc = 'DEAL ID'
) c
    ON a.order_no = c.order_no
    AND a.order_type = c.order_type;

UPDATE rds_wcla610_t2
SET doc_no_order = b.order_no
FROM dw_wcla.dwd_disty_sales_open_order_detail b
WHERE rds_wcla610_t2.order_no = b.int_ref_no;


UPDATE rds_wcla610_t2
SET doc_no_order = b.order_no
FROM dw_wcla.dwd_pub_common_history_header_extend b
WHERE rds_wcla610_t2.order_no = b.int_ref_no
    AND rds_wcla610_t2.doc_no_order IS NULL;


UPDATE rds_wcla610_t2
SET vend_inv_no = c.vend_inv_no
FROM dw_wcla.dwd_disty_common_po_basic b
    ,ods_wcla.ods_cis_corp_vend_doc c
WHERE rds_wcla610_t2.doc_no_order = b.order_no
    AND rds_wcla610_t2.sku_no = b.sku_no
    AND b.doc_no = c.doc_no
    AND rds_wcla610_t2.vend_inv_no IS NULL;


UPDATE rds_wcla610_t2
SET vend_inv_no = c.vend_inv_no
FROM dw_wcla.dwd_disty_ap_hold_df b
    ,ods_wcla.ods_cis_corp_vend_doc c
WHERE rds_wcla610_t2.doc_no_order = b.order_no
    AND rds_wcla610_t2.sku_no = b.sku_no
    AND b.doc_no = c.doc_no
    AND rds_wcla610_t2.vend_inv_no IS NULL;


UPDATE rds_wcla610_t2
SET vend_inv_no = c.vend_inv_no
FROM dw_wcla.dwd_disty_common_po_basic b
    ,ods_wcla.ods_cis_corp_vend_doc c
WHERE rds_wcla610_t2.order_no = b.order_no
    AND rds_wcla610_t2.sku_no = b.sku_no
    AND b.doc_no = c.doc_no
    AND rds_wcla610_t2.vend_inv_no IS NULL;


UPDATE rds_wcla610_t2
SET vend_inv_no = c.vend_inv_no
FROM dw_wcla.dwd_disty_ap_hold_df b
    ,ods_wcla.ods_cis_corp_vend_doc c
WHERE rds_wcla610_t2.order_no = b.order_no
    AND rds_wcla610_t2.sku_no = b.sku_no
    AND b.doc_no = c.doc_no
    AND rds_wcla610_t2.vend_inv_no IS NULL;


UPDATE rds_wcla610_t2
SET vend_inv_no = c.vend_inv_no
FROM dw_wcla.dwd_disty_common_po_basic b
    ,ods_wcla.ods_cis_corp_vend_doc c
WHERE rds_wcla610_t2.int_ref_no = b.order_no
    AND rds_wcla610_t2.sku_no = b.sku_no
    AND b.doc_no = c.doc_no
    AND rds_wcla610_t2.vend_inv_no IS NULL;


UPDATE rds_wcla610_t2
SET vend_inv_no = c.vend_inv_no
FROM dw_wcla.dwd_disty_ap_hold_df b
    ,ods_wcla.ods_cis_corp_vend_doc c
WHERE rds_wcla610_t2.int_ref_no = b.order_no
    AND rds_wcla610_t2.sku_no = b.sku_no
    AND b.doc_no = c.doc_no
    AND rds_wcla610_t2.vend_inv_no IS NULL;


DROP TABLE IF EXISTS rds_wcla610_ser;
CREATE LOCAL TEMPORARY TABLE rds_wcla610_ser ON COMMIT PRESERVE ROWS AS 
SELECT a.order_no
    ,a.order_type
    ,a.order_line_no
    ,b.ser_no
    ,b.asset_tag
FROM rds_wcla610_t2 a
INNER JOIN dw_wcla.dwd_disty_common_order_serial_no_di b
    ON a.order_no = b.order_no
    AND a.order_type = b.order_type
    AND a.order_line_no = b.order_line_no
    AND IFNULL(TRIM(b.ser_no), '') <> '';


DROP TABLE IF EXISTS rds_wcla610_ser_count;
CREATE LOCAL TEMPORARY TABLE rds_wcla610_ser_count ON COMMIT PRESERVE ROWS AS 
SELECT a.order_no
    ,a.order_type
    ,a.order_line_no
    ,COUNT(*) AS cnt
FROM rds_wcla610_ser a
GROUP BY a.order_no, a.order_type, a.order_line_no;


DROP TABLE IF EXISTS rds_wcla610_final;
CREATE LOCAL TEMPORARY TABLE rds_wcla610_final ON COMMIT PRESERVE ROWS AS 
SELECT a.order_no
    ,a.order_type
    ,a.order_line_no
    ,sku_no
    ,EU_company_name
    ,EU_address1
    ,EU_address2
    ,EU_city
    ,EU_state
    ,EU_zip
    ,EU_country
    ,EU_contact_name
    ,EU_phone
    ,ship_to_name
    ,ship_to_addr
    ,ship_to_city
    ,ship_to_state
    ,ship_to_zip
    ,ship_to_country
    ,sold_to_cust_no
    ,sold_to_cust_name
    ,sold_to_addr
    ,sold_to_city
    ,sold_to_state
    ,sold_to_zip
    ,sold_to_country
    ,sold_to_contact_name
    ,sold_to_contact_phone
    ,bill_to_cust_no
    ,bill_to_cust_name
    ,bill_to_address
    ,bill_to_address2
    ,bill_to_cust_city
    ,bill_to_cust_state
    ,bill_to_cust_zip
    ,bill_to_cust_country
    ,bill_to_contact_name
    ,bill_to_contact_phone
    ,sales_terr
    ,terr_manager
    ,1 * SIGN(a.ship_qty) AS ship_qty
    ,vend_part_no
    ,invoice_date
    ,u_price
    ,extended_unit_price
    ,drop_ship_flag
    ,int_ref_no
    ,int_ref_type
    ,from_loc_no
    ,inv_type
    ,scm_no_1
    ,spa_no1
    ,deal_id
    ,b.ser_no AS ser_no
    ,b.asset_tag AS asset_tag
    ,doc_no_order
    ,vend_inv_no
FROM rds_wcla610_t2 a
INNER JOIN rds_wcla610_ser b
    ON a.order_no = b.order_no
    AND a.order_type = b.order_type
    AND a.order_line_no = b.order_line_no
;

insert into rds_wcla610_final
SELECT a.order_no
    ,a.order_type
    ,a.order_line_no
    ,sku_no
    ,EU_company_name
    ,EU_address1
    ,EU_address2
    ,EU_city
    ,EU_state
    ,EU_zip
    ,EU_country
    ,EU_contact_name
    ,EU_phone
    ,ship_to_name
    ,ship_to_addr
    ,ship_to_city
    ,ship_to_state
    ,ship_to_zip
    ,ship_to_country
    ,sold_to_cust_no
    ,sold_to_cust_name
    ,sold_to_addr
    ,sold_to_city
    ,sold_to_state
    ,sold_to_zip
    ,sold_to_country
    ,sold_to_contact_name
    ,sold_to_contact_phone
    ,bill_to_cust_no
    ,bill_to_cust_name
    ,bill_to_address
    ,bill_to_address2
    ,bill_to_cust_city
    ,bill_to_cust_state
    ,bill_to_cust_zip
    ,bill_to_cust_country
    ,bill_to_contact_name
    ,bill_to_contact_phone
    ,sales_terr
    ,terr_manager
    ,a.ship_qty - b.cnt * SIGN(a.ship_qty) AS ship_qty
    ,vend_part_no
    ,invoice_date
    ,u_price
    ,extended_unit_price
    ,drop_ship_flag
    ,int_ref_no
    ,int_ref_type
    ,from_loc_no
    ,inv_type
    ,scm_no_1
    ,spa_no1
    ,deal_id
    ,'' AS ser_no
    ,'' AS asset_tag
    ,doc_no_order
    ,vend_inv_no
FROM rds_wcla610_t2 a
INNER JOIN rds_wcla610_ser_count b
    ON a.order_no = b.order_no
    AND a.order_type = b.order_type
    AND a.order_line_no = b.order_line_no
WHERE ABS(a.ship_qty) > b.cnt
;


insert into rds_wcla610_final
SELECT a.order_no
    ,a.order_type
    ,a.order_line_no
    ,sku_no
    ,EU_company_name
    ,EU_address1
    ,EU_address2
    ,EU_city
    ,EU_state
    ,EU_zip
    ,EU_country
    ,EU_contact_name
    ,EU_phone
    ,ship_to_name
    ,ship_to_addr
    ,ship_to_city
    ,ship_to_state
    ,ship_to_zip
    ,ship_to_country
    ,sold_to_cust_no
    ,sold_to_cust_name
    ,sold_to_addr
    ,sold_to_city
    ,sold_to_state
    ,sold_to_zip
    ,sold_to_country
    ,sold_to_contact_name
    ,sold_to_contact_phone
    ,bill_to_cust_no
    ,bill_to_cust_name
    ,bill_to_address
    ,bill_to_address2
    ,bill_to_cust_city
    ,bill_to_cust_state
    ,bill_to_cust_zip
    ,bill_to_cust_country
    ,bill_to_contact_name
    ,bill_to_contact_phone
    ,sales_terr
    ,terr_manager
    ,ship_qty
    ,vend_part_no
    ,invoice_date
    ,u_price
    ,extended_unit_price
    ,drop_ship_flag
    ,int_ref_no
    ,int_ref_type
    ,from_loc_no
    ,inv_type
    ,scm_no_1
    ,spa_no1
    ,deal_id
    ,'' AS ser_no
    ,'' AS asset_tag
    ,doc_no_order
    ,vend_inv_no
FROM rds_wcla610_t2 a
WHERE NOT EXISTS (
    SELECT 1
    FROM rds_wcla610_final b
    WHERE a.order_no = b.order_no
        AND a.order_type = b.order_type
        AND a.order_line_no = b.order_line_no
);


DROP TABLE IF EXISTS rdsetl.rds_tmp;
CREATE TABLE rdsetl.rds_tmp AS 
SELECT 'USD' AS 'Resale Currency Code'
    ,NULL AS 'Partner Internal Transaction ID'
    ,'1000827613' AS 'Partner Party-id'
    ,'COMM' AS 'Partner reporting type'
    ,'WETSCON MEXICO SA DE CV' AS 'Partner name'
    ,EU_company_name AS 'End Customer Name'
    ,NULL AS 'End Customer ID'
    ,NULL AS 'End Customer Tax ID'
    ,EU_address1 AS 'End Customer Address 1'
    ,EU_address2 AS 'End Customer Address 2'
    ,EU_city AS 'End Customer City'
    ,EU_state AS 'End Customer State/Province'
    ,EU_zip AS 'End Customer Postal Cd'
    ,EU_country AS 'End Customer Country Code'
    ,EU_contact_name AS 'End Customer Contact Name'
    ,EU_phone AS 'End Customer Contact Phone'
    ,ship_to_name AS 'Ship To Name'
    ,NULL AS 'Ship To ID'
    ,NULL AS 'Ship To Tax ID'
    ,ship_to_addr AS 'Ship To Address 1'
    ,NULL AS 'Ship To Address 2'
    ,ship_to_city AS 'Ship To City'
    ,ship_to_state AS 'Ship To State/Province'
    ,ship_to_zip AS 'Ship To Postal Cd'
    ,ship_to_country AS 'Ship To Country Cd'
    ,sold_to_cust_name AS 'Sold To Name'
    ,NULL AS 'Sold To ID'
    ,NULL AS 'Sold To Tax ID'
    ,sold_to_addr AS 'Sold To Address 1'
    ,NULL AS 'Sold To Address 2'
    ,sold_to_city AS 'Sold To City'
    ,sold_to_state AS 'Sold To State/Province'
    ,sold_to_zip AS 'Sold To Postal Cd'
    ,sold_to_country AS 'Sold To Country Cd'
    ,bill_to_cust_name AS 'Bill To Name'
    ,NULL AS 'Bill To ID'
    ,NULL AS 'Bill To Tax ID'
    ,bill_to_address AS 'Bill To Address 1'
    ,bill_to_address2 AS 'Bill To Address 2'
    ,bill_to_cust_city AS 'Bill To City'
    ,bill_to_cust_state AS 'Bill To State/Province'
    ,bill_to_cust_zip AS 'Bill To Postal Cd'
    ,bill_to_cust_country AS 'Bill To Country Cd'
    ,ship_qty AS 'Quantity'
    ,vend_part_no AS 'HPE Part Number'
    ,NULL AS 'Partner Product Number'
    ,NULL AS 'Bundle ID'
    ,TO_CHAR(invoice_date, 'mm/dd/YYYY') AS 'Invoice Date/Reported Period '
    ,u_price AS 'Unit Resale Price'
    ,(ship_qty * u_price) AS 'Net Purchase Price After Rebate Deduction'
    ,NULL AS 'Partner Purchase Price'
    ,'USD' AS 'Partner Purchase Price Currency Cd'
    ,SUBSTRING(deal_id, 1, 8) AS 'Upfront Deal #1'
    ,NULL AS 'Upfront Deal #2'
    ,NULL AS 'Upfront Deal #3'
    ,NULL AS 'Back-end Deal #1'
    ,NULL AS 'Back-end Deal #2'
    ,NULL AS 'Back-end Deal #3'
    ,NULL AS 'Back-end Deal #4'
    ,NULL AS 'Deal Reg#1'
    ,NULL AS 'Deal Reg#2'
    ,NULL AS 'Partner Purchase order'
    ,vend_inv_no AS 'HPE Invoice number'
    ,order_no AS 'Partner to Cust Invoice No'
    ,ISNULL(REPLACE(ser_no, ' ', NULL), 'ZZLABNCCS') AS 'Serial Number'
    ,'HPE' AS 'Product Origin'
    ,'MX' AS 'Country of Origin'
    ,drop_ship_flag AS 'Drop Ship Flag'
    ,'WETSCON MEXICO SA DE CV' AS 'Sell-From Name'
    ,NULL AS 'Sell-From ID'
    ,'WME000218GK3' AS 'Sell-From Tax ID'
    ,'AV. INSURGENTES SUR 730. PISO 11' AS 'Sell-From Address 1'
    ,NULL AS 'Sell-From Address 2'
    ,'CIUDAD DE MEXICO' AS 'Sell-From City'
    ,'DF' AS 'Sell-From State/Province'
    ,'03100' AS 'Sell-From Postal Cd'
    ,'MX' AS 'Sell-From Country Cd'
    ,NULL AS 'Entitled Party Name'
    ,NULL AS 'Entitled Party  ID'
    ,NULL AS 'Entitled Party  Tax ID'
    ,NULL AS 'Entitled Party Address 1'
    ,NULL AS 'Entitled Party  Address 2'
    ,NULL AS 'Entitled Party  City'
    ,NULL AS 'Entitled Party  State/Province'
    ,NULL AS 'Entitled Party Postal Cd'
    ,NULL AS 'Entitled Party Country Code'
    ,NULL AS 'Entitled Party Contact Name'
    ,NULL AS 'Entitled Party Contact Phone'
FROM rds_wcla610_final
;


DROP TABLE IF EXISTS rdsetl.rds_tmp_body;
CREATE TABLE rdsetl.rds_tmp_body AS 
SELECT 1 AS flag
    ,'Standard' AS body_type
    ,COUNT(*) AS cnt
FROM rdsetl.rds_tmp;
