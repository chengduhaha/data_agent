drop table if exists table_us17695_order;
create local temporary table table_us17695_order on commit preserve rows as
select distinct
	a.order_no as 'Order#',
	a.order_type as 'Order Type',
	a.order_line_no as 'Order Line#',
	a.cpo_no as 'Customer PO#',
	a.total_order as 'PO Total',
	a.unit_price as 'Unit Price',
	a.extend_net_price as 'Extended Price',
	a.sales_total as 'Order Total',
	a.sku_no as 'SKU#',
	a.mfg_partno as 'MFG#',
	a.vend_no as 'Vendor#',
	a.cpo_line_status as 'Order Status',
	min(eta) as 'Estimated Ship Date.',
	expected_date as 'Estimated Delivery Date',
	a.part_desc as 'Product Description',
	c.profile_c as 'Vendor SO#'
from dw_us.dwd_disty_sales_open_order_detail a
left join dm_us.dm_pur_unieta_boso_detail_rt b
on a.order_no = b.order_no and a.order_type = b.order_type and a.sku_no = b.sku_no
left join ods_us.ods_cis_corp_order_profile c on a.order_no =c.order_no and c.profile_type ='SAPID' and c.profile_cat='ORDR'
where (a.cust_no = 472684 or a.master_cust_no = 472684)
group by a.order_no,
	a.order_type,
	a.order_line_no,
	a.cpo_no,
	a.total_order,
	a.unit_price,
	a.extend_net_price,
	a.sales_total,
	a.sku_no,
	a.mfg_partno,
	a.vend_no,
	a.cpo_line_status,
	expected_date,
	a.part_desc,
	c.profile_c
;

drop table if exists table_us17695_shipped;
create local temporary table table_us17695_shipped on commit preserve rows as
select distinct a.order_no as 'Order#',
	a.order_qty as 'Order Quantity',
	a.sku_no as 'SKU#',
	a.unit_net_price as 'Unit Price',
	a.extend_net_price as 'Extended Price',
	hh.total_order as 'PO Total',
	a.cpo_no as 'Customer PO#',
	hh.entry_datetime as 'Order Date',
	hh.sales_total as 'Order Total',
	a.mfg_partno as 'MFG#',
	a.vend_no as 'Vendor#',
	a.vend_name as 'Vendor Name',
	a.ship_date as 'Ship Date',
	sm.ship_desc as 'Ship via',
	a.ship_qty as 'Ship Quantity',
	c.track_no as 'Tracking #',
	a.serial_no as 'Serial#''s',
	a.part_desc as 'Product Description',
	b.profile_c as 'Vendor SO#'
from dw_us.dwd_disty_common_pos_di a
left join ods_us.ods_cis_corp_order_profile b on a.order_no =b.order_no and b.profile_type ='SAPID' and b.profile_cat='ORDR'
left join dw_us.dwd_pub_common_history_header_extend c on a.order_no = c.order_no and a.order_type = c.order_type
left join dim_us.dim_pub_ship_method sm on a.ship_method = sm.ship_method
left join ods_us.ods_cis_corp_history_header hh on a.order_no = hh.order_no and a.order_type = hh.order_type
where a.order_type not in (14,114)
and (a.bill_to_cust_no = 472684 or a.master_cust_no = 472684)
and a.sales_terr = 6260
and a.date_flag >= current_date() - 10
and a.date_flag <  current_date()
and a.order_line_type != 'Comp'
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select * from table_us17695_shipped
;

drop table if exists rdsetl.rds_tmp_2;
CREATE TABLE rdsetl.rds_tmp_2 AS
select *
from table_us17695_order
;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
sheet_index int,
sheet_name varchar(50),
title_active varchar(1),
date_pattern varchar(50)
);

insert into rdsetl.rds_tmp_sheet_config select 1,'Shipped/Invoiced',null,null;
insert into rdsetl.rds_tmp_sheet_config select 2,'Awaiting To Ship',null,null;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;

Insert into rdsetl.rds_tmp_body
select 	2 as flag
		,'Standard' as body_type
		,count(*) as cnt
from rdsetl.rds_tmp_2
;