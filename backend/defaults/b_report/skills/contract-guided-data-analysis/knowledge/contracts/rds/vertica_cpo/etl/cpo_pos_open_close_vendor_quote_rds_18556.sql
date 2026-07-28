DROP TABLE IF EXISTS table_us18556_order;
CREATE LOCAL TEMPORARY TABLE table_us18556_order ON COMMIT PRESERVE ROWS AS
select a.order_no ,
	a.order_type ,
	a.bill_to_cust_no ,
	a.cpo_no ,
	a.bill_to_cust_name ,
	a.ship_date ,
	a.order_line_no ,
	a.part_no ,
	a.vpl_code ,
	a.ship_qty ,
	a.unit_net_price ,
	cast (null as money) as total_order,
	cast (null as varchar(200)) as Vendor_Quote_ID,
	b.spa_no
from dw_us.dwd_disty_common_pos_di a
left join dw_us.dwd_disty_scm_shipped_order_spa_di b
on a.order_no=b.order_no
and a.order_type=b.order_type
and a.order_line_no=b.order_line_no
and a.date_flag=b.date_flag
where a.order_line_type != 'Comp'
and a.date_flag>= DATE_TRUNC('month',current_date()-1)
and a.date_flag<current_date()
and a.vend_no=77105
;

update table_us18556_order x
set total_order = a.total_order
from ods_us.ods_cis_corp_order_header a
where x.order_no = a.order_no
and x.order_type=a.order_type
and a.delete_date is null
;

update table_us18556_order x
set total_order = a.total_order
from ods_us.ods_cis_corp_history_header a
where x.order_no = a.order_no
and x.order_type=a.order_type
and a.delete_date is null
and x.total_order is null
;

update table_us18556_order x
set Vendor_Quote_ID=a.data_c
from ods_us.ods_cis_corp_history_eu_custom a
inner join ods_us.ods_cis_corp_eu_custom_map b
on a.eu_map_id = b.eu_map_id
and a.eu_map_line_no = b.eu_map_line_no
inner join ods_us.ods_cis_corp_list_box_detail c
on c.code_value = b.map_data_desc
and c.list_box_code ='CEDM'
and c.code_desc = 'Vendor Quote ID'
where x.order_no = a.order_no
and x.order_type=a.order_type
and a.order_line_no=0
and a.delete_date is null
and x.Vendor_Quote_ID is null
;

DROP TABLE IF EXISTS table_us18556_tab1;
CREATE LOCAL TEMPORARY TABLE table_us18556_tab1 ON COMMIT PRESERVE ROWS AS
select order_no as 'Order #',
	bill_to_cust_no as 'Customer#',
	cpo_no as 'Cust PO',
	bill_to_cust_name as 'Cust Name',
	ship_date as 'Ship Date',
	order_line_no as 'Order Line#',
	part_no as 'Part#',
	vpl_code as 'VPC Code',
	ship_qty as 'Qty',
	unit_net_price as 'Net Price',
	total_order as 'Total Order',
	Vendor_Quote_ID as 'Vendor Quote ID',
	spa_no as 'SPA# Applied'
from table_us18556_order
;

--tab 2
DROP TABLE IF EXISTS table_us18556_cpo;
CREATE LOCAL TEMPORARY TABLE table_us18556_cpo ON COMMIT PRESERVE ROWS AS
select a.cpo_id
	,a.cpo_no
	,a.cpo_cust_no
	,a.cpo_cust_name
	,round(a.cpo_unit_price * a.cpo_line_qty, 2) as quote_amount
	,a.eu_company_name as eu_name
	,a.expected_close_date as expire_date
	,b.vpl_code
	,a.cpo_entry_datetime
	,'' as term_dates
	,a.vend_quote_id
	,a.spa_no
from dm_us.dm_disty_sales_open_cpo a
inner join dim_us.dim_pub_part_info b
on a.cpo_sku_no=b.sku_no
where a.cpo_entry_datetime>= DATE_TRUNC('month',current_date()-1)
and a.cpo_entry_datetime<current_date()
and a.cpo_delete_datetime is null
and a.cpo_line_delete_datetime is null
and b.vend_no=77105
;

insert into table_us18556_cpo
select a.cpo_id
	,a.cpo_no
	,a.cpo_cust_no
	,a.cpo_cust_name
	,round(a.cpo_unit_price * a.cpo_line_qty, 2) as quote_amount
	,a.eu_company_name as eu_name
	,a.expected_close_date as expire_date
	,b.vpl_code
	,a.cpo_entry_datetime
	,'' as term_dates
	,a.vend_quote_id
	,a.spa_no
from dm_us.dm_disty_sales_close_cpo_di a
inner join dim_us.dim_pub_part_info b
on a.cpo_sku_no=b.sku_no
where a.cpo_entry_datetime>= DATE_TRUNC('month',current_date()-1)
and a.cpo_entry_datetime<current_date()
and a.cpo_delete_datetime is null
and a.cpo_line_delete_datetime is null
and b.vend_no=77105
;

DROP TABLE IF EXISTS table_us18556_tab2;
CREATE LOCAL TEMPORARY TABLE table_us18556_tab2 ON COMMIT PRESERVE ROWS AS
select distinct cpo_id               as 'Quote#'
	,cpo_no               as 'WQ CPO#'
	,cpo_cust_no		  as 'Cust #'
	,cpo_cust_name	 	  as 'Customer Name'
	,quote_amount 		  as 'Quote Amount'
	,eu_name 			  as 'EU Name'
	,expire_date 		  as 'Expire Date'
	,vpl_code
	,cpo_entry_datetime	  as 'CPO Entry Date'
	,vend_quote_id		  as 'Vendor Quote ID'
	,spa_no 			  as 'SPA# Applied'
from table_us18556_cpo
;

-- RDS tables
drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from table_us18556_tab1
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from table_us18556_tab2
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
insert into rdsetl.rds_tmp_sheet_config select 1,'Invoiced Orders',null,'MM/dd/yyyy';
insert into rdsetl.rds_tmp_sheet_config select 2,'Quotes',null,'MM/dd/yyyy';