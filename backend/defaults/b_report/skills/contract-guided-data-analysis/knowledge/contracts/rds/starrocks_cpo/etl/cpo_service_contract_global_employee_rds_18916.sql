drop table if exists tempdb.rds_tmp;
drop table if exists tempdb.rds_tmp_body;

drop table if exists rds_us_customers_18916;
create table rds_us_customers_18916 as
select distinct
  division,
  division_desc as division_descr,
  cust_type,
  cust_type_descr,
  sales_terr,
  sales_terr_name as terr_name,
  cust_no,
  cust_name
from dim_us.dim_pub_customer_info
;

-- select count(*) from rds_us_customers_18916

drop table if exists rds_us_users_18916;
create table rds_us_users_18916 as
select distinct
  m.userid as cis_id,
  m.name as cis_name,
  m.title as biz_title,
  loc.local_loc_no as loc_no,
  loc.loc_name,
  concat(m.firstname,' ',m.lastname) as rep_name
from dim_us.dim_pub_manager m
inner join ods_gbl.ods_cis_mygbl_global_employee e on m.global_id = e.globalemployeeid
left join ods_gbl.ods_cis_mygbl_global_location_rt loc on e.userloc = loc.global_loc_id
where ifnull(m.title,'') <> 'Buyer'
;

-- select count(*) from rds_us_users_18916

drop table if exists rds_us_orders_18916;
create table rds_us_orders_18916 as
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
left join ods_us.ods_cis_corp_order_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 8
union
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_history_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
left join ods_us.ods_cis_corp_history_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 8
;

insert into rds_us_orders_18916
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
inner join ods_us.ods_cis_corp_inv_tran_rt d on a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42)
left join ods_us.ods_cis_corp_order_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 1
and ifnull(a.int_ref_type,0) <> 2
union
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
inner join ods_us.ods_cis_corp_history_inv_tran_rt d on a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42)
left join ods_us.ods_cis_corp_order_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 1
and ifnull(a.int_ref_type,0) <> 2
union
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_history_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
inner join ods_us.ods_cis_corp_history_inv_tran_rt d on a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42)
left join ods_us.ods_cis_corp_history_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 1
and ifnull(a.int_ref_type,0) <> 2
union
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_history_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
inner join ods_us.ods_cis_corp_inv_tran_rt d on a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42)
left join ods_us.ods_cis_corp_history_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 1
and ifnull(a.int_ref_type,0) <> 2
;

insert into rds_us_orders_18916
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
left join ods_us.ods_cis_corp_order_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 1
and ifnull(a.int_ref_type,0) <> 2
and not exists (select 1 from ods_us.ods_cis_corp_inv_tran_rt d where a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42))
and not exists (select 1 from ods_us.ods_cis_corp_history_inv_tran_rt d where a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42))
union
select
  a.order_type,
  a.order_no,
  trim(a.ext_ref) as cpo_no,
  b.order_line_no,
  a.delete_date as order_delete_date,
  b.delete_date as order_line_delete_date,
  a.entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  c.from_ref_type,
  a.int_ref_no as cpo_id,
  a.int_ref_type as cpo_type,
  a.from_loc_no
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_history_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type and b.kit_line_no is null
inner join ods_us.ods_cis_corp_part_master_rt bb on b.sku_no = bb.sku_no and bb.vend_no in (311,6771,64565,64956,76922,64460,68194,76819,64222)
left join ods_us.ods_cis_corp_history_soldto_rt c on a.order_no = c.order_no and a.order_type = c.order_type
where a.entry_datetime >= date_add(current_date(), interval -1 month)
and a.entry_datetime < date_add(current_date(), interval -0 day)
and a.order_type = 1
and ifnull(a.int_ref_type,0) <> 2
and not exists (select 1 from ods_us.ods_cis_corp_inv_tran_rt d where a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42))
and not exists (select 1 from ods_us.ods_cis_corp_history_inv_tran_rt d where a.order_no = d.doc_no and a.order_type = d.order_type and d.trans_type in (41,42))
;

drop table if exists rds_us_orders_125_18916;
create table rds_us_orders_125_18916 as
select
  a.contract_type,
  a.contract_no,
  sum(ifnull(b.unit_price,0) * ifnull(b.qty,0)) as total_order
from ods_us.ods_cis_corp_service_contract_header a
left join ods_us.ods_cis_corp_service_contract_line_sum b on a.contract_no = b.contract_no and a.contract_type = b.contract_type and b.delete_datetime is null
where a.entry_date >= date_add(current_date(), interval -1 month)
and a.entry_date < date_add(current_date(), interval -0 day)
and a.contract_type = 1
and a.vendor_no = 64956
group by
  a.contract_type,
  a.contract_no
;

insert into rds_us_orders_18916
select distinct
  ifnull(b.ot_type,0) as order_type,
  a.contract_no as order_no,
  trim(a.reseller_po_no) as cpo_no,
  b.line_no as order_line_no,
  a.delete_date as order_delete_date,
  b.delete_datetime as order_line_delete_date,
  a.entry_date as entry_datetime,
  c.total_order,
  a.entry_id,
  a.reseller_no as to_acct_no,
  -888888 as from_ref_type,
  -888888 as cpo_id,
  -888888 as cpo_type,
  -888888 as from_loc_no
from ods_us.ods_cis_corp_service_contract_header a
inner join rds_us_orders_125_18916 c on a.contract_no = c.contract_no and a.contract_type = c.contract_type
left join ods_us.ods_cis_corp_service_contract_line_sum b on a.contract_no = b.contract_no and a.contract_type = b.contract_type
where a.entry_date >= date_add(current_date(), interval -1 month)
and a.entry_date < date_add(current_date(), interval -0 day)
and a.contract_type = 1
and a.vendor_no = 64956
;

-- select count(*) from rds_us_orders_18916 where order_type = 125

drop table if exists tempdb.rds_us_report_18916;
create table tempdb.rds_us_report_18916
(   id bigint auto_increment,
    order_type int(11) null,
    order_no int(11) null,
    cpo_no varchar(80) null,
    cnt_order_line int(11) null,
    cnt_delete_order_line int(11) null,
    order_delete_date varchar(20) null,
    entry_datetime varchar(20) null,
    total_order decimal(18,4) null,
    entry_id int(11) null,
    to_acct_no int(11) null,
    from_ref_type int(11) null,
    from_ref_type_desc varchar(100) null,
    from_type varchar(100) null,
    loc_no int(11) null,
    office_location varchar(100) null,
    rep_name varchar(100) null,
    cpo_id int(11) null,
    cpo_type int(11) null,
    cpo_entry_id int(11) null,
    cpo_rep_name varchar(100) null,
    cpo_loc_no int(11) null,
    from_loc_no int(11) null,
    from_loc_char varchar(80) null,
    rn int(11) null
)
primary key (id)
distributed by hash (id)
;

insert into tempdb.rds_us_report_18916 (order_type, order_no, cpo_no, cnt_order_line, cnt_delete_order_line, order_delete_date, entry_datetime,
                                        total_order, entry_id, to_acct_no, from_ref_type, from_ref_type_desc, from_type, loc_no, office_location,
                                        rep_name, cpo_id, cpo_type, cpo_entry_id, cpo_rep_name,from_loc_no,rn)
select
  a.order_type,
  a.order_no,
  a.cpo_no,
  sum(case when a.order_line_delete_date is null then 1 else 0 end) as cnt_order_line,
  sum(case when a.order_line_delete_date is not null then 1 else 0 end) as cnt_delete_order_line,
  date_format(a.order_delete_date,'%d/%m/%Y') as order_delete_date,
  date_format(a.entry_datetime,'%d/%m/%Y') as entry_datetime,
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  ifnull(a.from_ref_type,-999) as from_ref_type,
  ifnull(b.from_ref_type_desc,'N/A') as from_ref_type_desc,
  cast('AUTO-EDI' as varchar(80)) as from_type,
  c.loc_no,
  ifnull(c.loc_name, cast(c.loc_no as varchar(20))) as office_location,
  c.rep_name,
  a.cpo_id,
  a.cpo_type,
  null,
  null,
  a.from_loc_no,
  row_number() over(order by a.order_no, a.order_type) rn
from rds_us_orders_18916 a
left join ods_us.ods_cis_corp_from_ref_type_rt b on a.from_ref_type = b.from_ref_type
inner join rds_us_users_18916 c on a.entry_id = c.cis_id
group by
  a.order_type,
  a.order_no,
  a.cpo_no,
  date_format(a.order_delete_date,'%d/%m/%Y'),
  date_format(a.entry_datetime,'%d/%m/%Y'),
  a.total_order,
  a.entry_id,
  a.to_acct_no,
  ifnull(a.from_ref_type,-999),
  ifnull(b.from_ref_type_desc,'N/A'),
  cast('AUTO-EDI' as varchar(80)),
  c.loc_no,
  ifnull(c.loc_name, cast(c.loc_no as varchar(20))),
  c.rep_name,
  a.cpo_id,
  a.cpo_type,
  null,
  null,
  a.from_loc_no
;


update tempdb.rds_us_report_18916
set cpo_id = b.int_ref_no
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_history_header_rt b on a.int_ref_type = b.order_type and a.int_ref_no = b.order_no
where tempdb.rds_us_report_18916.cpo_type = 2
and tempdb.rds_us_report_18916.from_loc_no = 98
and tempdb.rds_us_report_18916.cpo_id = a.order_no
and a.order_type = 2
;
update tempdb.rds_us_report_18916
set cpo_id = b.int_ref_no
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_order_header_rt b on a.int_ref_type = b.order_type and a.int_ref_no = b.order_no
where tempdb.rds_us_report_18916.cpo_type = 2
and tempdb.rds_us_report_18916.from_loc_no = 98
and tempdb.rds_us_report_18916.cpo_id = a.order_no
and a.order_type = 2
;

update tempdb.rds_us_report_18916
set cpo_id = b.int_ref_no
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_history_header_rt b on a.int_ref_type = b.order_type and a.int_ref_no = b.order_no
where tempdb.rds_us_report_18916.cpo_type = 2
and tempdb.rds_us_report_18916.from_loc_no = 98
and tempdb.rds_us_report_18916.cpo_id = a.order_no
and a.order_type = 2
;
update tempdb.rds_us_report_18916
set cpo_id = b.int_ref_no
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_header_rt b on a.int_ref_type = b.order_type and a.int_ref_no = b.order_no
where tempdb.rds_us_report_18916.cpo_type = 2
and tempdb.rds_us_report_18916.from_loc_no = 98
and tempdb.rds_us_report_18916.cpo_id = a.order_no
and a.order_type = 2
;

update tempdb.rds_us_report_18916
set cpo_entry_id = a.cpo_entry_id
from ods_us.ods_cis_corp_cpo_header_rt a
where tempdb.rds_us_report_18916.cpo_id = a.cpo_id
;
update tempdb.rds_us_report_18916
set cpo_entry_id = a.cpo_entry_id
from ods_us.ods_cis_corp_history_cpo_header_rt a
where tempdb.rds_us_report_18916.cpo_id = a.cpo_id
and tempdb.rds_us_report_18916.cpo_entry_id is null
;

update tempdb.rds_us_report_18916
set cpo_rep_name = c.rep_name,
    cpo_loc_no = c.loc_no
from rds_us_users_18916 c
where tempdb.rds_us_report_18916.cpo_entry_id = c.cis_id
;

update tempdb.rds_us_report_18916
set from_loc_char = c.loc_char
from ods_us.ods_cis_corp_location_info_rt c
where tempdb.rds_us_report_18916.from_loc_no = c.loc_no
;

update tempdb.rds_us_report_18916
set from_loc_char = 'N/A'
where from_loc_char is null
;

-- select count(*) from tempdb.rds_us_report_18916
-- select * from tempdb.rds_us_report_18916 where from_loc_char is null

-------- updated from_type start --------

drop table if exists rds_us_rds_bjrep_18916;
create table rds_us_rds_bjrep_18916 as
select a.userid
from ods_us.ods_cis_corp_manager_rt a
    ,ods_us.ods_cis_corp_location_info_rt b
where a.user_loc = b.loc_no
    and loc_city in ('Beijing', 'Chengdu')
    and country_code = 'CN'
;

drop table if exists rds_us_rds_phrep_18916;
create table rds_us_rds_phrep_18916 as
select a.userid
from ods_us.ods_cis_corp_manager_rt a
    ,ods_us.ods_cis_corp_location_info_rt b
where a.user_loc = b.loc_no
    and (
        loc_city in ('Kwun Tong, Kowloon')
        or country_code = 'PH'
        )
;

drop table if exists rds_us_rds_indrep_18916;
create table rds_us_rds_indrep_18916 as
select userid
  from ods_us.ods_cis_corp_manager_rt a, ods_gbl.ods_cis_mygbl_global_job_code b
   where a.job_code = b.jobcodeid
   and lower(b.jobcodetitle) like '%sales%'
   and company_no = 5143
union
select userid
from ods_us.ods_cis_corp_manager_rt
where userid = 738084
;

drop table if exists rds_us_rds_usrep_18916;

create table rds_us_rds_usrep_18916
(   userid int(11)
)
primary key (userid)
distributed by hash (userid)
;

insert into rds_us_rds_usrep_18916 (userid)
select userid
from ods_us.ods_cis_corp_manager_rt
where (
        cost_center in (200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 220, 221,
        222, 223, 224, 225, 226, 227, 228, 229, 23, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244,
        245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268,
        269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292,
        293, 294, 295, 296, 297, 298, 299, 420, 450, 490, 709, 711, 8103)
        or deptid = 60
        )
    and userid > 0
;

delete from rds_us_rds_usrep_18916
where rds_us_rds_usrep_18916.userid in (select b.userid from rds_us_rds_bjrep_18916 b)
;
delete from rds_us_rds_usrep_18916
where rds_us_rds_usrep_18916.userid in (select b.userid from rds_us_rds_phrep_18916 b)
;
delete from rds_us_rds_usrep_18916
where rds_us_rds_usrep_18916.userid in (select b.userid from rds_us_rds_indrep_18916 b)
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when from_ref_type in (null,1,41,87,65,67)
                then 'CN-MANUAL'
            else 'CN-EDI'
            end
        )
from rds_us_rds_bjrep_18916 s
where tempdb.rds_us_report_18916.entry_id = s.userid
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when from_ref_type in (null,1,41,87,65,67)
                then 'PH-MANUAL'
            else 'PH-EDI'
            end
        )
from rds_us_rds_phrep_18916 s
where tempdb.rds_us_report_18916.entry_id = s.userid;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when from_ref_type in (null,1,41,87,65,67)
                then 'IND-MANUAL'
            else 'EDI/IND Sales'
            end
        )
from rds_us_rds_indrep_18916 s
where tempdb.rds_us_report_18916.entry_id = s.userid
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when from_ref_type in (null,1,41,87,65,67)
                then 'US-MANUAL'
            else 'US-EDI'
            end
        )
from rds_us_rds_usrep_18916 s
where tempdb.rds_us_report_18916.entry_id = s.userid
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when from_ref_type in (null,1,41,87,65,67)
                then 'US-MANUAL'
            else 'US-EDI'
            end
        )
where entry_id > 0
    and from_type = 'AUTO-EDI'
;

update tempdb.rds_us_report_18916
set from_type = 'AUTO-EDI'
where entry_id = 602583
;

update tempdb.rds_us_report_18916
set from_type = 'NIFI-MANUAL'
where from_ref_type = 68
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when rep_name = 'RPA CN Sales'
                then 'CN-RPA-EDI'
            when rep_name = 'RPA PH Sales'
                then 'PH RPA'
            when rep_name = 'RPA US Sales'
                then 'US-RPA-EDI'
            else from_type
            end
        )
where rep_name like 'RPA%'
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when cpo_rep_name = 'RPA CN Sales'
                then 'CN-RPA-MANUAL'
            else from_type
            end
        )
;

update tempdb.rds_us_report_18916
set from_type = (
        case
            when rep_name = 'RPA CN Sales'
                and from_ref_type = 68
                then 'NIFI-MANUAL'
            else from_type
            end
        )
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type in ('US-MANUAL','CN-MANUAL')
            then 'US Sales-RPA'
        when from_type in ('US-EDI','CN-EDI')
            then 'US-RPA-EDI'
        else from_type
        end
where entry_id = 703826
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type = 'US-EDI'
            then 'IND-QUATTRO-EDI'
        when from_type = 'US-MANUAL'
            then 'IND-QUATTRO-MANUAL'
        else from_type
        end
where office_location like '%Quattro- India - Delhi%'
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type = 'US-EDI'
            and loc_no = 5632
            then 'IND-CHENNAI-EDI'
        when from_type = 'US-MANUAL'
            and loc_no = 5632
            then 'IND-CHENNAI-MANUAL'
        else from_type
        end
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type = 'IND-EDI'
            and loc_no = 5632
            then 'IND-CHENNAI-EDI'
        when from_type = 'IND-MANUAL'
            and loc_no = 5632
            then 'IND-CHENNAI-MANUAL'
        else from_type
        end
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type = 'US-EDI'
            and loc_no = 6742
            then 'IND-KOLKATA-EDI'
        when from_type = 'US-MANUAL'
            and loc_no = 6742
            then 'IND-KOLKATA-MANUAL'
        else from_type
        end
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type = 'US-EDI'
            and loc_no = 6014
            then 'TDCR-EDI'
        when from_type = 'US-MANUAL'
            and loc_no = 6014
            then 'TDCR-MANUAL'
        else from_type
        end
;

update tempdb.rds_us_report_18916
set from_type = case
        when from_type in ('US-MANUAL')
            then 'CN-MANUAL'
        when from_type in ('US-EDI')
            then 'CN-EDI'
        else from_type
        end
where office_location like '%Beijing Office%'
or office_location like '%Chengdu Office%'
;

update tempdb.rds_us_report_18916
set from_type = 'Service Billing'
where order_type = 125
;

update tempdb.rds_us_report_18916
set from_type =  replace(from_type,'-EDI','-MANUAL')
where from_ref_type_desc = 'WebQuote'
and from_type like '%-EDI%'
;

update tempdb.rds_us_report_18916
set from_type = case when loc_no in (76,78) or cpo_loc_no in (76,78) then replace(from_type,'US-','CN-')
                     when loc_no in (5632,6742) or cpo_loc_no in (5632,6742) then replace(from_type,'US-','IND-')
                     else from_type
                end
where from_type like 'US-%'
and ((loc_no in (76,78,5632,6742) and locate('RPA', rep_name) = 0) or (cpo_loc_no in (76,78,5632,6742) and locate('RPA', cpo_rep_name) = 0 and locate('Auto', cpo_rep_name) = 0))
;

update tempdb.rds_us_report_18916
set from_type = case when loc_no in (76,78) or cpo_loc_no in (76,78) and from_type like 'IND-KOLKATA-%' then replace(from_type,'IND-KOLKATA-','CN-')
                     when loc_no in (76,78) or cpo_loc_no in (76,78) and from_type like 'IND-CHENNAI-%' then replace(from_type,'IND-CHENNAI-','CN-')
                     when loc_no in (76,78) or cpo_loc_no in (76,78) then replace(from_type,'IND-','CN-')
                     when loc_no in (5632,6742) or cpo_loc_no in (5632,6742) then replace(from_type,'IND-','IND-')
                     else from_type
                end
where from_type like 'IND-%'
and ((loc_no in (76,78,5632,6742) and locate('RPA', rep_name) = 0) or (cpo_loc_no in (76,78,5632,6742) and locate('RPA', cpo_rep_name) = 0 and locate('Auto', cpo_rep_name) = 0))
;

update tempdb.rds_us_report_18916
set from_type = case when entry_id in (select userid from rds_us_rds_bjrep_18916) or cpo_entry_id in (select userid from rds_us_rds_bjrep_18916) then replace(from_type,'AUTO-','CN-')
                     when entry_id in (select userid from rds_us_rds_indrep_18916) or cpo_entry_id in (select userid from rds_us_rds_indrep_18916) then replace(from_type,'AUTO-','IND-')
                     when entry_id in (select userid from rds_us_rds_usrep_18916) or cpo_entry_id in (select userid from rds_us_rds_usrep_18916) then replace(from_type,'AUTO-','US-')
                     when entry_id in (select userid from rds_us_rds_phrep_18916) or cpo_entry_id in (select userid from rds_us_rds_phrep_18916) then replace(from_type,'AUTO-','PH-')
                     else from_type
                end
where from_type like '%AUTO-MANUAL%'
;

update tempdb.rds_us_report_18916
set from_type = case when loc_no in (6742) or cpo_loc_no in (6742) then replace(from_type,'IND-','IND-KOLKATA-')
                     when loc_no in (5632) or cpo_loc_no in (5632) then replace(from_type,'IND-','IND-CHENNAI-')
                     else from_type
                end
where from_type like '%IND-MANUAL%'
;

-------- updated from_type end --------

drop table if exists rds_us_dim_18916;
create table rds_us_dim_18916 as
select distinct
  a.to_acct_no,
  a.entry_id,
  a.from_ref_type,
  a.from_ref_type_desc,
  a.from_type,
  a.cpo_entry_id
from rds_us_report_18916 a
;

-- select * from rds_us_report_18916 where cnt_order_line <> 0 and cnt_delete_order_line = 0
-- select * from rds_us_report_18916 where cnt_order_line = 0 and cnt_delete_order_line <> 0
-- select * from rds_us_report_18916 where cnt_order_line <> 0 and cnt_delete_order_line <> 0

drop table if exists rds_us_orders_sum_18916;
create table rds_us_orders_sum_18916 as
select
  a.entry_id,
  a.to_acct_no,
  a.from_ref_type,
  a.from_type,
  a.cpo_entry_id,
  sum(a.total_order) as total_order,
  count(distinct a.cpo_id) as cnt_po,
  count(distinct a.order_no) as cnt_so_bo,
  sum(a.cnt_order_line) as cnt_order_line
from rds_us_report_18916 a
where cnt_order_line <> 0
and cnt_delete_order_line = 0
group by
  a.entry_id,
  a.to_acct_no,
  a.from_ref_type,
  a.from_type,
  a.cpo_entry_id
;

drop table if exists rds_us_orders_delete_18916;
create table rds_us_orders_delete_18916 as
select
  a.entry_id,
  a.to_acct_no,
  a.from_ref_type,
  a.from_type,
  a.cpo_entry_id,
  count(distinct a.cpo_id) as del_po,
  count(distinct a.order_no) as del_so_bo,
  sum(a.cnt_delete_order_line) as cnt_order_line
from rds_us_report_18916 a
where cnt_order_line = 0
and cnt_delete_order_line <> 0
group by
  a.entry_id,
  a.to_acct_no,
  a.from_ref_type,
  a.from_type,
  a.cpo_entry_id
;

drop table if exists rds_us_orders_delete_partial_18916;
create table rds_us_orders_delete_partial_18916 as
select
  a.entry_id,
  a.to_acct_no,
  a.from_ref_type,
  a.from_type,
  a.cpo_entry_id,
  count(distinct a.order_no) as partial_del_so_bo,
  count(distinct a.cpo_id) as partial_del_po,
  sum(a.cnt_order_line + a.cnt_delete_order_line) as cnt_order_line
from rds_us_report_18916 a
where cnt_order_line <> 0
and cnt_delete_order_line <> 0
group by
  a.entry_id,
  a.to_acct_no,
  a.from_ref_type,
  a.from_type,
  a.cpo_entry_id
;

drop table if exists rds_tmp;
create table rds_tmp as
select
  b.division,
  b.division_descr,
  b.cust_type,
  b.cust_type_descr,
  b.sales_terr,
  b.terr_name,
  a.to_acct_no as cust_no,
  b.cust_name,
  a.entry_id as cis_id,
  c.cis_name,
  c.biz_title,
  c.loc_no,
  c.loc_name,
  d.cis_name as cpo_rep_name,
  a.from_ref_type_desc as from_ref_type,
  a.from_type,
  a1.total_order,
  ifnull(a1.cnt_po,0) as cnt_po,
  ifnull(a1.cnt_so_bo,0) as cnt_so_bo,
  ifnull(a1.cnt_order_line,0) + ifnull(a2.cnt_order_line,0) + ifnull(a3.cnt_order_line,0) as cnt_order_line,
  ifnull(a2.del_po,0) as del_po,
  ifnull(a2.del_so_bo,0) as del_so_bo,
  ifnull(a3.partial_del_so_bo,0) as partial_del_so_bo,
  ifnull(a3.partial_del_po,0) as partial_del_po
from rds_us_dim_18916 a
left join rds_us_orders_sum_18916 a1 on a.to_acct_no = a1.to_acct_no and a.entry_id = a1.entry_id and a.from_ref_type = a1.from_ref_type and a.from_type = a1.from_type and ifnull(a.cpo_entry_id,0) = ifnull(a1.cpo_entry_id,0)
left join rds_us_orders_delete_18916 a2 on a.to_acct_no = a2.to_acct_no and a.entry_id = a2.entry_id and a.from_ref_type = a2.from_ref_type and a.from_type = a2.from_type and ifnull(a.cpo_entry_id,0) = ifnull(a2.cpo_entry_id,0)
left join rds_us_orders_delete_partial_18916 a3 on a.to_acct_no = a3.to_acct_no and a.entry_id = a3.entry_id and a.from_ref_type = a3.from_ref_type and a.from_type = a3.from_type and ifnull(a.cpo_entry_id,0) = ifnull(a3.cpo_entry_id,0)
left join rds_us_customers_18916 b on a.to_acct_no = b.cust_no
left join rds_us_users_18916 c on a.entry_id = c.cis_id
left join rds_us_users_18916 d on a.cpo_entry_id = d.cis_id
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;
