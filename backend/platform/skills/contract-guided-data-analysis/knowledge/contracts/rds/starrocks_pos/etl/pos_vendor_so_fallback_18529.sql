drop table if exists tempdb.rds_tmp;
drop table if exists tempdb.rds_tmp_body;

drop table if exists rds_us_order_18529;
create table rds_us_order_18529 as
select distinct
    date(c.credit_rel_date) as create_date,
    date(a.ship_date) as ship_date,
    a.cust_no,
    a.order_no,
    a.order_type,
    a.cust_po_no,
    a.mso_no,
    a.synnex_po_no,
    b.order_type_descr,
    a.loc_name
from dw_us.dwd_disty_pub_dw_orders_extend_di a
left join ods_us.ods_cis_corp_order_type_rt b on a.order_type = b.order_type
left join ods_us.ods_cis_corp_history_header_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.date_flag >= date_add(current_date(), interval -7 month)
and a.date_flag < current_date()
and a.order_type = 1
and a.cust_no = 657888
and a.vend_no = 64956
;

-- select count(*) from ods_us.ods_cis_corp_history_profile where mso_no is not null
-- select * from rds_us_order_18529 where order_no = 167433219
-- select * from dw_us.dwd_disty_pub_dw_orders_extend_di where order_no = 163211292

drop table if exists rds_us_vendor_so_18529;
create table rds_us_vendor_so_18529 as
select distinct
  b.order_no,
  b.profile_c
from rds_us_order_18529 a
inner join ods_us.ods_cis_corp_history_profile b on a.order_no = b.order_no and b.order_type = a.order_type
where a.order_no is not null
and b.profile_type = 'SAPID'
and b.profile_cat = 'ORDR'
and b.profile_c is not null
union
select distinct
  b.order_no,
  b.profile_c
from rds_us_order_18529 a
inner join ods_us.ods_cis_corp_order_profile b on a.order_no = b.order_no and b.order_type = a.order_type
where a.order_no is not null
and b.profile_type = 'SAPID'
and b.profile_cat = 'ORDR'
and b.profile_c is not null
;

drop table if exists rds_us_vendor_mso_18529;
create table rds_us_vendor_mso_18529 as
select
  b.order_no,
  b.profile_c
from rds_us_order_18529 a
inner join ods_us.ods_cis_corp_history_profile b on b.order_no = a.mso_no and b.order_type = a.order_type
where a.mso_no is not null
and b.profile_type = 'SAPID'
and b.profile_cat = 'ORDR'
and b.profile_c is not null
union
select
  b.order_no,
  b.profile_c
from rds_us_order_18529 a
inner join ods_us.ods_cis_corp_order_profile b on b.order_no = a.mso_no and b.order_type = a.order_type
where a.mso_no is not null
and b.profile_type = 'SAPID'
and b.profile_cat = 'ORDR'
and b.profile_c is not null
;

drop table if exists rds_us_vendor_po_18529;
create table rds_us_vendor_po_18529 as
select
  b.order_no,
  b.vend_so_no as profile_c
from rds_us_order_18529 a
inner join ods_us.ods_cis_corp_order_eta_code_rt b on b.order_no = a.synnex_po_no and b.order_type = 2
where b.vend_so_no is not null
union
select
  b.order_no,
  b.vend_so_no as profile_c
from rds_us_order_18529 a
inner join ods_us.ods_cis_corp_history_eta_code_rt b on b.order_no = a.synnex_po_no and b.order_type = 2
where b.vend_so_no is not null
;

-- select * from rds_us_vendor_po_18529 where order_no = 38473907

drop table if exists rds_tmp;
create table rds_tmp as
select distinct
    a.create_date as 'Create_Date',
    a.ship_date as 'Ship Date',
    a.cust_no as 'Customer#',
    a.order_no as 'order_no',
    a.cust_po_no as 'cpo_no',
    a.mso_no as 'mso_no',
    a.synnex_po_no as 'synnex_po_no',
    coalesce(b.profile_c, c.profile_c, d.profile_c) as 'Vendor SO',
    a.order_type_descr as 'Order Type',
    a.loc_name as 'Loc Char'
from rds_us_order_18529 a
left join rds_us_vendor_so_18529 b on a.order_no = b.order_no
left join rds_us_vendor_mso_18529 c on a.mso_no = c.order_no
left join rds_us_vendor_po_18529 d on a.synnex_po_no = d.order_no
order by a.order_no
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;

drop table if exists rds_us_order_18529;
drop table if exists rds_us_vendor_so_18529;
drop table if exists rds_us_vendor_mso_18529;
drop table if exists rds_us_vendor_po_18529;
