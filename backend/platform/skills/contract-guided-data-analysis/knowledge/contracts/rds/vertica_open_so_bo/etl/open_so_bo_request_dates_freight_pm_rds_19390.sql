drop table if exists t_orders_19390;
create local temporary table t_orders_19390 on commit preserve rows as
select
  a.order_type,
  a.order_no,
  a.from_loc_no,
  a.from_loc_char,
  a.inv_type,
  a.sales_terr,
  a.terr_name,
  a.sales_rep_id,
  a.sales_rep_name,
  a.ship_method,
  b.service_days,
  a.expected_date,
  a.request_delivery_date,
  a.requested_ship_date,
  a.cust_no as bill_to_cust_no,
  a.cust_name as bill_to_cust_name,
  a.bill_to_cust_addr,
  a.bill_to_cust_zip,
  a.bill_to_cust_city,
  a.bill_to_cust_state,
  a.bill_to_cust_country,
  a.bill_to_contact_name,
  a.bill_to_contact_email,
  a.bill_to_contact_phone,
  a.order_date,
  a.sales_rel_date,
  a.credit_rel_date,
  a.sku_no,
  a.vpl_no,
  a.vend_no,
  a.part_no,
  a.mfg_partno,
  a.order_qty,
  a.ship_qty,
  a.base_cost,
  a.eta_code,
  a.eta_date,
  a.est_delivery_date,
  cast(null as varchar(80)) pm_name, -- Primary Procurement Analyst
  cast(null as varchar(80)) pm_manager_name, -- Primary Procurement Analyst Manager
  cast(null as varchar(80)) pm_director_name -- Primary Procurement Analyst Director
from dw_us.dwd_disty_sales_open_order_detail a
left join ods_us.ods_cis_corp_order_frt_detail b on a.order_type = b.order_type and a.order_no = b.order_no and a.ship_method = b.ship_method
where a.request_delivery_date is not null
or a.requested_ship_date is not null
;


update t_orders_19390 a
set pm_name = b.pm_name,
    pm_manager_name = b.pm_manager_name,
    pm_director_name = b.pm_director_name
from dim_us.dim_pub_vpl_pm_hierarchy_info b
where a.vend_no = b.vend_no
and a.vpl_no = b.vpl_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
  a.order_no as 'SO#',
  a.from_loc_no as 'Loc#',
  a.from_loc_char as 'Loc Name',
  a.inv_type as 'Inv Type',
  a.sales_terr as 'Sales Territory',
  a.terr_name as 'Sales Territory Name',
  a.sales_rep_name as 'Sales Rep',
  a.ship_method as 'Ship Method',
  a.service_days as 'Service Days',
  a.expected_date as 'Expect Date',
  a.request_delivery_date as 'Request Delivery Date',
  a.requested_ship_date as 'Request Ship Date',
  a.bill_to_cust_no as 'Bill To Cust#',
  a.bill_to_cust_name as 'Bill To Cust Name',
  a.bill_to_cust_addr as 'Bill To Cust Addr',
  a.bill_to_cust_zip as 'Bill To Cust Zip',
  a.bill_to_cust_city as 'Bill To Cust City',
  a.bill_to_cust_state as 'Bill To Cust State',
  a.bill_to_cust_country as 'Bill To Cust Country',
  a.bill_to_contact_name as 'Bill To Contact Name',
  a.bill_to_contact_email as 'Bill To Contact Email',
  a.bill_to_contact_phone as 'Bill To ontact Phone',
  a.order_date as 'SO Created Date',
  a.sales_rel_date as 'Sales Release Date',
  a.credit_rel_date as 'Credit Release Date',
  a.sku_no as 'SKU#',
  a.part_no as 'Part#',
  a.mfg_partno as 'MFG Part#',
  a.order_qty as 'Qty',
  a.ship_qty as 'Ship Qty',
  a.base_cost as 'Base Cost',
  a.eta_code as 'ETA Code',
  a.eta_date as 'Est. Ship Date',
  a.est_delivery_date as 'Est. Delivery Date',
  a.pm_name as 'PP Analyst',
  a.pm_manager_name as 'PP Analyst Manager',
  a.pm_director_name as 'PP Analyst Director'
from t_orders_19390 a
--where order_no = 139170373
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

drop table if exists t_orders_19390;
