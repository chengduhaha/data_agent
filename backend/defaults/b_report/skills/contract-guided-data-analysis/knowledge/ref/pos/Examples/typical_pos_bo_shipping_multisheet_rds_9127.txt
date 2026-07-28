-- Typical POS example: multi-sheet BO status plus prior-day shipping.
-- Source: CA/run/rds_9127_rtv.sp

-- tab 1 Daily BO Status
DROP TABLE IF EXISTS table_9127_bo;
CREATE LOCAL TEMPORARY TABLE table_9127_bo ON COMMIT PRESERVE ROWS AS
select a.order_no,
       a.order_type,
       a.order_line_no,
       cast(a.order_date as date) as order_entry_date,
       a.cust_no,
       a.cust_name,
       a.sales_terr,
       a.terr_name,
       a.sku_no,
       a.part_no,
       a.order_qty,
       a.ship_qty,
       a.open_qty,
       a.extend_base_cost,
       a.unit_price + ifnull(a.extend_net_price,0) as net_price,
       a.extend_net_price,
       a.eta_date,
       b.exp_ship_date,
       a.order_date,
       a.from_loc_no,
       a.from_loc_char,
       a.synnex_po_no,
       a.cpo_no,
       a.sold_to_cust_name as reseller,
       ifnull(d.spa_no,e.spa_no) as spa_no,
       ifnull(d.spa_ref_no,e.spa_ref_no) as spa_ref_no,
       a.eu_company_name,
       a.eu_country,
       a.eu_city,
       a.eu_state,
       a.eu_zip,
       a.eu_address1
  from dw_ca.dwd_disty_sales_open_order_detail a
  left join dw_ca.dwd_disty_brpt_bo_detail_df b
         on a.order_type = b.order_type
        and a.order_no = b.order_no
        and a.order_line_no = b.order_line_no
        and b.date_flag >= current_date()-1
        and b.date_flag < current_date()
  left join dw_ca.dwd_disty_scm_shipped_order_spa_di d
    on a.order_no = d.order_no
   and a.order_type = d.order_type
   and a.order_line_no = d.order_line_no
  left join dw_ca.dwd_disty_scm_open_order_spa_df e
    on a.order_no = e.order_no
   and a.order_type = e.order_type
   and a.order_line_no = e.order_line_no
 where a.master_cust_no in (1051212)
   and a.order_type = 8
   and a.order_delete_date is null
   and a.order_line_delete_date is null
;

DROP TABLE IF EXISTS table_9127_tab1;
CREATE LOCAL TEMPORARY TABLE table_9127_tab1 ON COMMIT PRESERVE ROWS AS
select order_no              as 'BO#/MSO#'
      ,order_type            as 'Order_Type'
      ,order_entry_date      as 'Order_Entry_Date'
      ,order_no              as 'Order#'
      ,order_line_no         as 'Line#'
      ,synnex_po_no          as 'SYNNEX_PO#'
      ,cpo_no                as 'Customer_PO'
      ,cust_no               as 'Cust#'
      ,cust_name             as 'Cust_Name'
      ,sales_terr            as 'Terr#'
      ,terr_name             as 'Terr_Name'
      ,sku_no                as 'SKU#'
      ,part_no               as 'Part#'
      ,net_price             as 'Net_Price'
      ,order_qty             as 'Order_Quantity'
      ,ship_qty              as 'Ship_Quantity'
      ,open_qty              as 'Open_Quantity'
      ,extend_net_price      as 'Total_Amount'
      ,extend_base_cost      as 'Extend_Base_Cost'
      ,eta_date              as 'ETA_Date_Time'
      ,exp_ship_date         as 'Expected_Ship_Date'
      ,order_date            as 'Entry_Date_Time'
      ,from_loc_no           as 'Location#'
      ,from_loc_char         as 'Location Name'
      ,spa_no                as 'SPA#'
      ,spa_ref_no            as 'SPA_Ref#'
      ,synnex_po_no          as 'VPO'
      ,reseller              as 'Reseller'
      ,eu_company_name       as 'EU_Company_Name'
      ,eu_country            as 'EU_Country'
      ,eu_city               as 'EU_City'
      ,eu_state              as 'EU_State'
      ,eu_zip                as 'EU_Zip'
      ,eu_address1           as 'EU_Address1'
  from table_9127_bo
;

-- tab 2 Prior Day Shipping
DROP TABLE IF EXISTS table_9127_order_mid;
CREATE LOCAL TEMPORARY TABLE table_9127_order_mid ON COMMIT PRESERVE ROWS AS
select a.order_no,
       a.order_type,
       a.bill_to_cust_no,
       a.bill_to_cust_name,
       a.ship_to_name,
       a.cpo_no,
       a.end_user_po,
       to_char(a.date_flag,'yyyy-mm-dd') as ship_date,
       a.ship_to_addr,
       a.order_line_no,
       a.mfg_partno,
       a.part_desc,
       a.ship_qty,
       a.unit_net_price,
       a.serial_no,
       a.ship_method,
       a.vend_name,
       a.sku_no,
       a.vpl_desc,
       a.synnex_po_no
  from dw_ca.dwd_disty_common_pos_di a
 where order_line_type != 'Comp'
 and a.master_cust_no in (1051212)
and a.date_flag>=CURRENT_DATE()-1
and a.date_flag<current_date()
;

DROP TABLE IF EXISTS table_9127_order;
CREATE LOCAL TEMPORARY TABLE table_9127_order ON COMMIT PRESERVE ROWS AS
select a.order_no,
       a.order_type,
       a.bill_to_cust_no,
       a.bill_to_cust_name,
       a.ship_to_name,
       a.cpo_no,
       a.end_user_po,
       LISTAGG(DISTINCT c.track_no USING PARAMETERS max_length=2048,separator='*',on_overflow='TRUNCATE') as track_no,
       a.ship_date,
       a.ship_to_addr,
       a.order_line_no,
       a.mfg_partno,
       a.part_desc,
       a.ship_qty,
       a.unit_net_price,
       a.serial_no,
       b.total_order,
       a.ship_method,
       a.vend_name,
       a.sku_no,
       a.vpl_desc,
       a.synnex_po_no
  from table_9127_order_mid a
 inner join ods_ca.ods_cis_corp_history_header b
    on a.order_no = b.order_no
   and a.order_type = b.order_type
   and b.delete_date is null
  left join ods_ca.ods_cis_corp_carton_header c
    on a.order_no = c.order_no
   and a.order_type = c.order_type
 group by a.order_no,a.order_type,a.bill_to_cust_no,a.bill_to_cust_name,a.ship_to_name,a.cpo_no,
          a.end_user_po,a.ship_date,a.ship_to_addr,a.order_line_no,a.mfg_partno,a.part_desc,
          a.ship_qty,a.unit_net_price,a.serial_no,b.total_order,a.ship_method,a.vend_name,a.sku_no,a.vpl_desc,a.synnex_po_no
;

DROP TABLE IF EXISTS table_9127_tab2;
CREATE LOCAL TEMPORARY TABLE table_9127_tab2 ON COMMIT PRESERVE ROWS AS
select order_no           as 'Order #'
      ,cpo_no             as 'Cust PO'
      ,bill_to_cust_name  as 'Cust Name'
      ,synnex_po_no       as 'PO#'
      ,track_no           as 'Tracking #'
      ,ship_date          as 'Ship Date'
      ,order_type         as 'Order Type'
      ,bill_to_cust_no    as 'Customer #'
      ,ship_to_addr       as 'Ship To Address'
      ,order_line_no      as 'Order Line#'
      ,mfg_partno         as 'MFG Part#'
      ,sku_no             as 'SKU#'
      ,vend_name          as 'Vendor Name'
      ,vpl_desc           as 'VPC Desc'
      ,ship_method        as 'Ship Method'
      ,ship_qty           as 'QTY'
      ,unit_net_price     as 'Net Price'
      ,serial_no          as 'Serial#'
      ,total_order        as 'Total Order'
  from table_9127_order
;

-- RDS tables
drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from table_9127_tab1
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from table_9127_tab2
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
      ,'Standard' as body_type
      ,count(*) as cnt
from rdsetl.rds_tmp
;
insert into rdsetl.rds_tmp_body
select 2 as flag
      ,'Standard' as body_type
      ,count(*) as cnt
from rdsetl.rds_tmp_2
;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
sheet_index int,
sheet_name varchar(50),
title_active varchar(1),
date_pattern varchar(50)
);
insert into rdsetl.rds_tmp_sheet_config select 1,'Daily BO Status',null,'MM/dd/yyyy';
insert into rdsetl.rds_tmp_sheet_config select 2,'Prior Day Shipping',null,'MM/dd/yyyy';
