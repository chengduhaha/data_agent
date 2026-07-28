drop table if exists table_us17956_order;
create local temporary table table_us17956_order on commit preserve rows as
select a.order_no as 'BO#/MSO#',
  a.order_type,
  cast(a.order_date as date)  as 'Order_Entry_Date',
  a.cust_no as 'Cust#',
  a.cust_name as 'Cust_Name',
  a.sku_no as 'SKU#',
  a.part_no as 'Part#',
  a.order_qty as 'Order_Quantity',
  ship_qty as 'Ship_Quantity',
  open_qty as 'Open_Quantity',
  extend_base_cost,
  ifnull(d.spa_no,e.spa_no) as spa_no,
  ifnull(d.spa_ref_no,e.spa_ref_no) as spa_ref_no,
  synnex_po_no as VPO,
  a.sold_to_cust_name as reseller,
  a.cpo_no
from dw_us.dwd_disty_sales_open_order_detail a
left join dw_us.dwd_disty_brpt_bo_detail_df b
       on a.order_type = b.order_type
      and a.order_no = b.order_no
      and a.order_line_no = a.order_line_no
      and b.date_flag = current_date()-1
left join dw_us.dwd_disty_scm_shipped_order_spa_di d
on a.order_no = d.order_no
and a.order_type = d.order_type
and a.order_line_no = d.order_line_no
left join dw_us.dwd_disty_scm_open_order_spa_df e
on a.order_no = e.order_no
and a.order_type = e.order_type
and a.order_line_no = e.order_line_no
where a.vend_no = 3493
and a.order_type =8
and a.order_date >= trunc(current_date()-1,'Year')
and a.order_date < current_date()
and a.order_delete_date is null
and a.order_line_delete_date is null

UNION


select a.order_no,a.order_type,
  cast(a.order_date as date) as 'Order_Entry_Date',
  a.cust_no as 'Cust#',
  a.cust_name as 'Cust_Name',
  a.sku_no as 'SKU#',
  a.part_no as 'Part#',
  a.order_qty as 'Order_Quantity',
  ship_qty as 'Ship_Quantity',
  open_qty as 'Open_Quantity',
  extend_base_cost,
  ifnull(d.spa_no,e.spa_no) as spa_no,
  ifnull(d.spa_ref_no,e.spa_ref_no) as spa_ref_no,
  synnex_po_no as VPO,
  a.sold_to_cust_name as reseller,
  a.cpo_no
from dw_us.dwd_disty_sales_open_order_detail a
left join dw_us.dwd_disty_brpt_bo_detail_df b
       on a.order_type = b.order_type
      and a.order_no = b.order_no
      and a.order_line_no = a.order_line_no
      and b.date_flag = current_date()-1
left join dw_us.dwd_disty_scm_shipped_order_spa_di d
on a.order_no = d.order_no
and a.order_type = d.order_type
and a.order_line_no = d.order_line_no
left join dw_us.dwd_disty_scm_open_order_spa_df e
on a.order_no = e.order_no
and a.order_type = e.order_type
and a.order_line_no = e.order_line_no
where a.vend_no = 3493
and a.order_type =1
and a.drop_ship ='Y'
and a.order_date >= trunc(current_date()-1,'Year')
and a.order_date < current_date()
and a.order_delete_date is null
and a.order_line_delete_date is null

;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from table_us17956_order
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
