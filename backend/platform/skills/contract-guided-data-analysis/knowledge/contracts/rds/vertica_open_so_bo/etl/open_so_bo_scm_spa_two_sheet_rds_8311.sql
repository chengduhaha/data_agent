set time zone to 'America/Toronto';

drop table if exists rds_us7130_order;
create local temporary table rds_us7130_order on commit preserve rows as
select a.order_type as 'Order Type'
    ,a.order_no as 'Order #'
    ,a.order_line_no as 'Line #'
    ,a.synnex_po_no as 'SYNNEX PO #'
    ,a.cpo_no as 'CUSTOMER PO'
    ,a.cust_no as 'Cust #'
    ,a.cust_name as 'Cust Name'
    ,a.sales_terr as 'Terr #'
    ,a.terr_name as 'Terr Name'
    ,a.sku_no as 'SKU #'
    ,a.part_no as 'Part #'
    ,a.unit_price + ifnull(a.unit_sum_expense,0) as 'Net Price'
    ,a.order_qty as 'Order Quantity'
    ,a.extend_net_price as 'Total Amount'
    ,a.eta_date as 'ETA Date Time'
    ,a.requested_ship_date as 'Expected Ship Date'
    ,a.order_date as 'Entry Date Time'
    ,a.from_loc_no as 'Location #'
    ,b.loc_name as 'Location Name'
    ,a.eu_company_name as 'End User'
    ,a.eu_state as 'EU State'
    ,c.spa_ref_no as 'SPA'
from dw_ca.dwd_disty_sales_open_order_detail a
left join dim_ca.dim_pub_location_info b
on a.from_loc_no = b.loc_no
left join dw_ca.dwd_disty_scm_open_order_spa_df c
on a.order_type = c.order_type
and a.order_no = c.order_no
and a.order_line_no = c.order_line_no
and c.date_flag = current_date()-1
where a.vend_no = 40279
and a.order_delete_date is null
and a.order_line_delete_date is null
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_us7130_order
where "Order Type" = 8
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from rds_us7130_order
where "Order Type" = 1
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
insert into rdsetl.rds_tmp_sheet_config select 1,'BO',null,null;
insert into rdsetl.rds_tmp_sheet_config select 2,'Pending Orders',null,null;
-- 1