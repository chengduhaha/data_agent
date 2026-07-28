drop table if exists tempdb.rds_sales_us17797;
create table tempdb.rds_sales_us17797 as
select DISTINCT 
	 a.order_type 										 as 'Order Sales type Number'
	,ot.order_type_descr 								 as 'Order Sales type Name'
	,a.order_no                                       	 as 'ORDER SSO#'
	,a.date_flag                                         as 'Ship Date'
	,a.cust_no											 as 'Customer Number'
	,ch.cust_name										 as 'Sold-to (Customer name)'
	,pm.part_no 										 as 'SNX Part#'
	,a.sku_no											 as 'SKU#'
	,a.cust_terr    									 as 'Sales Terr Number'
	,a.ship_qty 										 as 'Ship Qty'
	,c.profile_f                                         as 'Spec Cost'
	,hp.profile_i                                        as 'SPA#'
	,hp.profile_c                                        as 'SPA Ref#'
	,sp.spa_desc    									 as 'SPA Desc'
	,SIGN(a.btl_sales) * ABS(IFNULL(a.btl_sales * 100 / IFNULL(NULLIF(a.net_sales, 0), 100), 0))	as 'BTL-SALES %'
from dw_us.dwd_disty_common_dw_orders_pl_extend_di a
left join ods_us.ods_cis_corp_order_type_rt ot on a.order_type = ot.order_type
left join ods_us.ods_cis_corp_customer_header_rt ch on a.cust_no = ch.cust_no 
left join ods_us.ods_cis_corp_part_master_rt pm on a.sku_no = pm.sku_no 
left join ods_us.ods_cis_corp_history_profile_rt c on a.order_no = c.order_no and a.order_type = c.order_type and a.order_line_no = c.order_line_no and c.profile_type='SYNPOPRICE' and c.active='Y'
left join ods_us.ods_cis_corp_history_exp_rt he on he.order_type = a.order_type and he.order_no = a.order_no and he.order_line_no = a.order_line_no and he.delete_date is null
left join ods_us.ods_cis_corp_history_profile_rt hp on he.order_no = hp.order_no and he.order_type = hp.order_type and he.order_line_no = hp.order_line_no and he.order_expense_line_no = hp.profile_no and hp.profile_type = 'REBATE_ADJ' and hp.active = 'Y'
left join ods_us.ods_his_corp_history_spa_header sp on hp.profile_i = sp.spa_no 
where a.vend_no IN (81051, 83561)
and a.date_flag >= date_add(current_date(),interval -7 day)
and a.date_flag < current_date()
and a.order_type >0
UNION
select 
	a.order_type 										 as 'Order Sales type Number'
	,ot.order_type_descr 								 as 'Order Sales type Name'
	,a.order_no                                       	 as 'ORDER SSO#'
	,a.date_flag                                         as 'Ship Date'
	,a.cust_no											 as 'Customer Number'
	,ch.cust_name										 as 'Sold-to (Customer name)'
	,pm.part_no 										 as 'SNX Part#'
	,a.sku_no											 as 'SKU#'
	,a.cust_terr    									 as 'Sales Terr Number'
	,a.ship_qty 										 as 'Ship Qty'
	,c.profile_f                                         as 'Spec Cost'
	,hp.profile_i                                        as 'SPA#'
	,hp.profile_c                                        as 'SPA Ref#'
	,sp.spa_desc    									 as 'SPA Desc'
	,SIGN(a.btl_sales) * ABS(IFNULL(a.btl_sales * 100 / IFNULL(NULLIF(a.net_sales, 0), 100), 0))	as 'BTL-SALES %'
from dw_us.dwd_disty_common_dw_orders_pl_extend_di a
left join ods_us.ods_cis_corp_order_type_rt ot on a.order_type = ot.order_type
left join ods_us.ods_cis_corp_customer_header_rt ch on a.cust_no = ch.cust_no 
left join ods_us.ods_cis_corp_part_master_rt pm on a.sku_no = pm.sku_no 
left join ods_us.ods_cis_corp_order_profile_rt c on a.order_no = c.order_no and a.order_type = c.order_type and a.order_line_no = c.order_line_no and c.profile_type='SYNPOPRICE' and c.active='Y'
left join ods_us.ods_cis_corp_order_exp_rt he on he.order_type = a.order_type and he.order_no = a.order_no and he.order_line_no = a.order_line_no and he.delete_date is null
left join ods_us.ods_cis_corp_order_profile_rt hp on he.order_no = hp.order_no and he.order_type = hp.order_type and he.order_line_no = hp.order_line_no and he.order_expense_line_no = hp.profile_no and hp.profile_type = 'REBATE_ADJ' and hp.active = 'Y'
left join ods_us.ods_cis_corp_spa_header_rt sp on hp.profile_i = sp.spa_no 
where a.vend_no IN (81051, 83561)
and a.date_flag >= date_add(current_date(),interval -7 day)
and a.date_flag < current_date()
and a.order_type >0
;

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select *
from tempdb.rds_sales_us17797
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;
