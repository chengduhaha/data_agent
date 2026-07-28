drop table if exists tempdb.rds_order_us19137;
create table tempdb.rds_order_us19137 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) as  
select
    uuid_numeric() as id,
    a.order_no,
    a.order_type,
    b.order_line_no,
    a.to_acct_no,
    a.from_loc_no,
    cast(null as char(4)) as loc_char, 
    date_format(a.entry_datetime,'%m/%d/%Y') as created_date ,
    date_format(a.ship_date,'%m/%d/%Y') as ship_date,
    date_format(a.printed_date,'%m/%d/%Y') as printed_date,
    date_format(a.pick_date,'%m/%d/%Y') as pick_date,
    date_format(a.qc_date,'%m/%d/%Y') as qc_date,
    b.sku_no,     
    c.vpl_no,
    a.sales_terr, 
	cast(null as int) as sold_to_acct,
    cast(null as varchar(60)) as sold_to_cust_name,
    a.ship_to_name,
    date_format(a.delete_date,'%m/%d/%Y') as deleted,
    date_format(a.sales_rel_date,'%m/%d/%Y') as sales_rel,
    date_format(a.credit_rel_date,'%m/%d/%Y') as credit_rel, 
    cast(null as int) as primary_id,
    cast(null as varchar(80)) as pm,
    cast('N' as varchar(10)) as order_ship_complete,
    cast('N' as varchar(10)) as pm_queue, 
    a.issue_date,
    a.ship_method,
    cast(null as varchar(200)) as  comments,
    c.vend_no,
    b.inv_type,
    cast(null as int) as on_hand
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type
inner join dim_us.dim_pub_part_info c on b.sku_no = c.sku_no
where a.order_type in (1, 8)
and a.delete_date is null
and b.delete_date is null
and a.ship_date is null
and b.order_qty - ifnull(b.ship_qty,0) <> 0 
and c.vend_no in (13208	,81051,22084,81551,16176,77294,19534,83561 )
and a.sales_terr in (7350,7351,7352,7353,7354,7355,7356,7357,7358,7359,
7360,7361,7362,7363,7364,7365,7366,7367,7368,7369,7370,7371,7372,7373,316,7014,1010,301	)
;

update tempdb.rds_order_us19137
   set sold_to_cust_name = c.cust_name,
       sold_to_acct = b.to_acct_no 
  from   ods_us.ods_cis_corp_order_soldto_rt b
  inner join ods_us.ods_cis_corp_customer_header_rt c
    on b.to_acct_no = c.cust_no
	where   rds_order_us19137.order_no = b.order_no
   and rds_order_us19137.order_type = b.order_type
;
  

update tempdb.rds_order_us19137
set primary_id = b.primary_id
from ods_us.ods_cis_corp_vend_user_matrix_rt b
where tempdb.rds_order_us19137.vpl_no = b.vpl_no
and tempdb.rds_order_us19137.vend_no = b.vend_no
and b.profile_type = 'PM'
;

update tempdb.rds_order_us19137
set primary_id = b.primary_id
from ods_us.ods_cis_corp_vend_user_matrix_rt b
where -1 = b.vpl_no
and tempdb.rds_order_us19137.vend_no = b.vend_no
and b.profile_type = 'PM'
and tempdb.rds_order_us19137.primary_id is null
;

update tempdb.rds_order_us19137
   set pm = concat(c.firstname,' ',c.lastname)
 from dim_us.dim_pub_manager c
where tempdb.rds_order_us19137.primary_id = c.userid
;

update tempdb.rds_order_us19137
   set loc_char = b.loc_char
  from ods_us.ods_cis_corp_location_info_rt b
 where rds_order_us19137.from_loc_no = b.loc_no
;
  

update tempdb.rds_order_us19137
   set order_ship_complete = 'Y'
  from ods_us.ods_cis_corp_order_profile_rt a
 where tempdb.rds_order_us19137.order_no = a.order_no
 and a.order_type IN (1,8)
 and a.profile_cat = 'ORDR'
 and a.profile_type = 'SHIP_CPLE'
 and a.active = 'Y'
;

drop table if exists tempdb.pm_queue_us19137;
create table tempdb.pm_queue_us19137 as
select distinct
  q.order_no,
  q.order_type
from ods_us.ods_cis_corp_sales_que_rt q
inner join ods_us.ods_cis_corp_order_header_rt h on q.order_no = h.order_no and q.order_type = h.order_type
where q.rule_id in (23,35)
  and q.approve_date is null
  and q.delete_date is null
  and h.issue_date is not null
  and h.sales_rel_date is null
  and h.delete_date is null
  and h.closed_date is null
;

update tempdb.rds_order_us19137
   set pm_queue = 'Y'
  from tempdb.pm_queue_us19137 a
 where tempdb.rds_order_us19137.order_no = a.order_no
 and tempdb.rds_order_us19137.order_type = a.order_type
;

update tempdb.rds_order_us19137
   set comments = a.comment
  from ods_us.ods_cis_corp_sales_que_rt a
 where tempdb.rds_order_us19137.order_no = a.order_no
 and a.order_type IN (1,8)
 and a.delete_date is null
;

update tempdb.rds_order_us19137
   set on_hand = ifnull(b.on_hand_qty,0)
  from dw_us.dwd_disty_inv_qty_df b
 where rds_order_us19137.sku_no = b.sku_no
   and rds_order_us19137.inv_type = b.inv_type
   and b.date_flag = DATE_ADD(CURRENT_DATE(),INTERVAL -1 DAY)
;

update tempdb.rds_order_us19137
   set on_hand = ifnull(b.on_hand_qty,0)
  from dw_us.dwd_disty_inv_qty_df b
 where rds_order_us19137.sku_no = b.sku_no
   and rds_order_us19137.inv_type = b.inv_type
   and b.date_flag = DATE_ADD(CURRENT_DATE(),INTERVAL -2 DAY)
   and rds_order_us19137.on_hand is null
;


drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select distinct order_type as 'Order Sales type Number',
       order_no as 'Order #', 
       to_acct_no as 'Customer Number',
       loc_char as Warehouse,
       sold_to_cust_name as 'Sold-to (Customer Name)',   
       created_date as 'Created Date',
	   issue_date as 'Queued',
	   sales_rel as 'SO Sales Released',
       credit_rel as 'SO Credit Released',
	   printed_date as 'Printed',
       pick_date as 'Pick Completed',
       qc_date as 'QC Date',
       ship_date as 'Ship Date',
       order_ship_complete as 'Order Ship Complete',
       pm_queue as 'PM QUEUE',
       sales_terr as 'Sales Terr#',
       pm as 'Primary PM',
       ship_method	, 
	   comments as 'Sales Released Comments',
       vend_no as 'Vendor Number',
       sku_no as 'SKU',
       on_hand as 'ON HAND',
       inv_type as 'INVENTORY TYPE',
       ship_to_name as 'Ship To'
  from tempdb.rds_order_us19137
;
  
drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;


drop table if exists tempdb.rds_order_us19137; 
drop table if exists tempdb.pm_queue_us19137;