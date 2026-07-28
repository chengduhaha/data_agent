drop table if exists table_us16483_tab1;
create local temporary table table_us16483_tab1 on commit preserve rows as
select to_char(rma_issue_date,'mm/dd/yyyy') as rma_issue_date
    ,rma_no
    ,rma_line_no
    ,part_no
    ,original_so_no
    ,original_so_line_no
    ,original_so_cpo_no
    ,so_days
    ,original_so_ship_qty
    ,auth_qty
    ,rec_qty
    ,so_price
    ,price_adj
    ,incident_no
    ,rma_status
from dw_us.dwd_disty_cs_rma_info
where sku_no in (9472517,9472519,9472518,9472534,9472520,9472531,9472530,9472526,9472528,9472527,9472529,9472537,9472538,9472525,9472533)
;

drop table if exists table_us16483_tab2;
create local temporary table table_us16483_tab2 on commit preserve rows as
select distinct a.cust_no
    ,a.order_type
    ,a.vend_no
    ,a.order_no
    ,b.ext_ref as cpo_no
    ,a.ship_method
    ,to_char(a.order_date,'mm/dd/yyyy') as created_date
    ,to_char(a.issue_date,'mm/dd/yyyy') as queued
    ,to_char(a.sales_rel_date,'mm/dd/yyyy') as sales_released
    ,to_char(a.credit_rel_date,'mm/dd/yyyy') as credit_released
    ,to_char(b.printed_date,'mm/dd/yyyy') as printed
    ,to_char(a.pick_date,'mm/dd/yyyy') as pick_completed
    ,to_char(a.qc_date,'mm/dd/yyyy') as qc_date
from dw_us.dwd_disty_sales_open_order_detail a
left join ods_us.ods_cis_corp_order_header b
on a.order_no = b.order_no
and a.order_type = b.order_type
-- and b.delete_date is null
where a.cust_no=436785
and a.vend_no=75897
and a.order_delete_date is null
and a.order_line_delete_date is null
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from table_us16483_tab1
;
drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from table_us16483_tab2
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
insert into rdsetl.rds_tmp_sheet_config select 1,'RMA',null,null;
insert into rdsetl.rds_tmp_sheet_config select 2,'Shipment Status',null,null;
-- 2
