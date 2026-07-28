-- tab 1
drop table if exists table_9676_order_mid;
create local temporary table table_9676_order_mid on commit preserve rows as
select distinct b.from_loc_no,
       c.loc_char as from_loc_name,
       a.order_no,
       a.order_type,
       b.ext_ref as customer_po_no,
       a.sku_no,
       d.part_no,
       d.mfg_partno,
       a.u_price as unit_price,
       d.vend_segment as vend_seg_code,
       d.vend_no,
       d.vend_name,
       a.cust_no as bill_to_cust,
       e.cust_name as bill_to_cust_name,
       b.ship_to_name,
       e.sales_terr,
       e.sales_terr_name as terr_name,
       f.buyer_name as primary_buyer,
       f.pm_name as primary_pm,
       b.entry_datetime as so_entry_date,
       a.date_flag as shiped_date,
       a.ship_qty,
       a.ship_qty * (a.u_price+ifnull(a.u_sum_expense,0)) as sales_revenue,
       b.ship_method,
       a.order_line_no,
       b.int_ref_no
  from dw_us.dwd_disty_common_dw_orders_pl_extend_di a
 inner join dim_us.dim_pub_part_info d
    on a.sku_no = d.sku_no
   and d.data_source = 'CIS'
 inner join ods_us.ods_cis_corp_history_header b
    on a.order_no = b.order_no
   and a.order_type = b.order_type
   and b.delete_date is null
  left join dim_us.dim_pub_location_info c
    on b.from_loc_no = c.loc_no
  left join dim_us.dim_pub_customer_info e
    on a.cust_no = e.cust_no
  left join dim_us.dim_pub_vpl_hierarchy_info f
    on d.vend_no = f.vend_no
   and d.vpl_no = f.vpl_no
 where a.cust_no in (430592, 124254, 430594)
   and a.date_flag >= DATE_TRUNC('MONTH',ADD_MONTHS(current_date(),-1))
   and a.date_flag < current_date()
;

drop table if exists table_9676_order;
create local temporary table table_9676_order on commit preserve rows as
select a.from_loc_no,
       a.from_loc_name,
       a.order_no,
       a.order_type,
       a.customer_po_no,
       a.sku_no,
       a.part_no,
       a.mfg_partno,
       a.unit_price,
       a.vend_seg_code,
       a.vend_no,
       a.vend_name,
       a.bill_to_cust,
       a.bill_to_cust_name,
       a.ship_to_name,
       a.sales_terr,
       a.terr_name,
       a.primary_buyer,
       a.primary_pm,
       a.so_entry_date,
       a.shiped_date,
       a.ship_qty,
       a.sales_revenue,
       a.ship_method,
       a.order_line_no,
       isnull(g.profile_d,g1.profile_d) as request_ship_date,
       isnull(h.profile_d,h1.profile_d) as request_delivery_date,
       i.cpo_ship_qty,
       row_number() over(partition by a.order_no,a.order_type,a.order_line_no) rn
  from table_9676_order_mid a
  left join ods_us.ods_cis_corp_history_cpo_profile g
    on a.int_ref_no = g.cpo_id
   and g.profile_type = 'EXPSHIPDAY'
   and g.profile_cat = 'SHIP'
   and g.active = 'Y'
  left join ods_us.ods_cis_corp_cpo_profile g1
    on a.int_ref_no = g1.cpo_id
   and g1.profile_type = 'EXPSHIPDAY'
   and g1.profile_cat = 'SHIP'
   and g1.active = 'Y'
  left join ods_us.ods_cis_corp_history_cpo_profile h
    on a.int_ref_no = h.cpo_id
   and h.profile_type = 'EXPDELDAY'
   and h.profile_cat = 'SHIP'
   and h.active = 'Y'
  left join ods_us.ods_cis_corp_cpo_profile h1
    on a.int_ref_no = h1.cpo_id
   and h1.profile_type = 'EXPDELDAY'
   and h1.profile_cat = 'SHIP'
   and h1.active = 'Y'
  left join dm_us.dm_disty_sales_close_cpo_di i
    on a.int_ref_no = i.cpo_id
   and a.sku_no = i.cpo_sku_no
   and i.cpo_delete_datetime is null
   and i.cpo_line_delete_datetime is null
;

drop table if exists table_9676_track;
create local temporary table table_9676_track on commit preserve rows as
select a.from_loc_no
	,a.from_loc_name
	,a.order_no
	,a.order_type
	,a.customer_po_no
	,a.sku_no
	,a.part_no
	,a.mfg_partno
	,a.unit_price
	,a.vend_seg_code
	,a.vend_no
	,a.vend_name
	,a.bill_to_cust
	,a.bill_to_cust_name
	,a.ship_to_name
	,a.sales_terr
	,a.terr_name
	,a.primary_buyer
	,a.primary_pm
	,a.request_ship_date
	,a.request_delivery_date
	,a.so_entry_date
	,a.shiped_date
	,a.ship_qty
	,a.cpo_ship_qty
	,a.sales_revenue
	,a.ship_method
	,a.order_line_no
	,max(b.track_no) as track_no
	,count(b.carton_no) as carton_cnt
from table_9676_order a
left join ods_us.ods_cis_corp_carton_header b
on a.order_no=b.order_no
and a.order_type=b.order_type
where a.rn=1
group by a.from_loc_no
	,a.from_loc_name
	,a.order_no
	,a.order_type
	,a.customer_po_no
	,a.sku_no
	,a.part_no
	,a.mfg_partno
	,a.unit_price
	,a.vend_seg_code
	,a.vend_no
	,a.vend_name
	,a.bill_to_cust
	,a.bill_to_cust_name
	,a.ship_to_name
	,a.sales_terr
	,a.terr_name
	,a.primary_buyer
	,a.primary_pm
	,a.request_ship_date
	,a.request_delivery_date
	,a.so_entry_date
	,a.shiped_date
	,a.ship_qty
	,a.cpo_ship_qty
	,a.sales_revenue
	,a.ship_method
	,a.order_line_no
;

drop table if exists table_9676_tab1;
create local temporary table table_9676_tab1 on commit preserve rows as
select from_loc_no
	,from_loc_name
	,order_no as 'so#'
	,order_type
	,customer_po_no
	,sku_no
	,part_no
	,mfg_partno
	,unit_price
	,vend_seg_code
	,vend_no
	,vend_name
	,bill_to_cust
	,bill_to_cust_name
	,ship_to_name
	,sales_terr
	,terr_name
	,primary_buyer
	,primary_pm
	,request_ship_date
	,request_delivery_date
	,so_entry_date
	,shiped_date
	,ship_qty
	,cpo_ship_qty as po_qty
	,sales_revenue
	,ship_method
	,track_no
	,carton_cnt
from table_9676_track
;

-- tab 2
drop table if exists table_9676_tab2;
create local temporary table table_9676_tab2 on commit preserve rows as 
select a.from_loc_no
	,a.from_loc_char as from_loc_name
	,a.order_no
	,b.total_order
	,b.total_cost
	,b.sales_total
	,(b.sales_total-b.total_cost)*100/nullif(b.sales_total,0) as 'GM%'
	,a.ship_to_city
	,a.ship_to_state
	,a.ship_to_zip
	,a.ship_to_country
	,c.sales_terr
	,c.sales_terr_name as terr_name
	,a.bill_to_cust_no as bill_to_cust
	,a.bill_to_cust_name
	,a.date_flag as date_yyyymm
	,sum(a.ship_qty*(a.unit_price+ifnull(a.unit_sum_exp,0))) as sales_revenue
from dw_us.dwd_disty_common_pos_di a
inner join ods_us.ods_cis_corp_history_header b
on a.order_no=b.order_no
and a.order_type=b.order_type
and b.delete_date is null
inner join dim_us.dim_pub_customer_info c
on a.bill_to_cust_no=c.cust_no
where a.order_line_type != 'Comp'
and a.bill_to_cust_no in (430592,124254)
and a.date_flag>=DATE_TRUNC('MONTH',ADD_MONTHS(current_date(),-1))
and a.date_flag<current_date()
and a.ship_qty <>0
group by a.from_loc_no
	,a.from_loc_char
	,a.order_no
	,b.total_order
	,b.total_cost
	,b.sales_total
	,(b.sales_total-b.total_cost)*100/nullif(b.sales_total,0)
	,a.ship_to_city
	,a.ship_to_state
	,a.ship_to_zip
	,a.ship_to_country
	,c.sales_terr
	,c.sales_terr_name
	,a.bill_to_cust_no
	,a.bill_to_cust_name
	,a.date_flag
;

-- tab 3
drop table if exists table_9676_tab3;
create local temporary table table_9676_tab3 on commit preserve rows as 
select a.bill_to_cust_no as bill_to_cust
	,a.bill_to_cust_name
	,to_char(a.date_flag,'mm/dd/yyyy') as date_yyyymm
	,count(distinct order_no) as order_cnts
from dw_us.dwd_disty_common_pos_di a
where a.order_line_type != 'Comp'
and a.bill_to_cust_no in (430592,124254)
and a.date_flag>=DATE_TRUNC('MONTH',ADD_MONTHS(current_date(),-1))
and a.date_flag<current_date()
and a.ship_qty <>0
and a.order_type>0
group by a.bill_to_cust_no
	,a.bill_to_cust_name
	,to_char(a.date_flag,'mm/dd/yyyy')
;


-- RDS tables
drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as 
select *
from table_9676_tab1
;
drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as 
select *
from table_9676_tab2
;
drop table if exists rdsetl.rds_tmp_3;
create table rdsetl.rds_tmp_3 as 
select *
from table_9676_tab3
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
insert into rdsetl.rds_tmp_body
select 3 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp_3
;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
sheet_index int,
sheet_name varchar(50),
title_active varchar(1),
date_pattern varchar(50)
);
insert into rdsetl.rds_tmp_sheet_config select 1,'POS_Sku_Level',null,'MM/dd/yyyy';
insert into rdsetl.rds_tmp_sheet_config select 2,'POS_Order_Level',null,'MM/dd/yyyy';
insert into rdsetl.rds_tmp_sheet_config select 3,'Order Counts',null,'MM/dd/yyyy';