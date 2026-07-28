drop table if exists rds_ca9041_doc;
create local temporary table rds_ca9041_doc on commit preserve rows as
select b.mcust_no
    ,b.mcust_name
    ,a.cust_no
    ,a.cust_name
    ,a.order_type
    ,a.order_no
    ,a.terms as doc_terms
    ,a.doc_date
    ,a.due_date
    ,a.due_date_agedays
    ,ifnull(a.amount,0) as doc_amount
    ,ifnull(a.amount,0) - ifnull(a.applied,0) as open_amount
    ,a.reference
    ,a.reference2
    ,case when ifnull(a.applied,0) = 0 then 'Full Open' else 'Short Open' end as full_short_open
    ,a.credit_code as reason_code
-- Text_Box_Note
    ,a.sales_terr
    ,a.collector_id
    ,a.collector_name
from dw_ca.dwd_disty_ar_cust_doc_df a
left join dim_ca.dim_pub_customer_info b
on a.cust_no = b.cust_no
where a.date_flag in (select max(date_flag) from dw_ca.dwd_disty_ar_cust_doc_df)
and a.due_date_agedays >= 365
and a.collector_id <> 621252
and a.sales_terr not in (2000, 2910, 8058, 8888)
;

-- update tempdb..rds_tmp
-- set Text_Box_Note=  b.profile_c
-- from tempdb..rds_tmp  a, CIS..cust_doc_profile b
-- where a.order_no = b.order_no
-- and a.order_type = b.order_type
-- and b.profile_cat = 'AR'
-- and b.profile_type = 'TEXT_NOTE'

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_ca9041_doc
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from rds_ca9041_doc
where due_date_agedays >= 500
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
insert into rdsetl.rds_tmp_sheet_config select 1,'365+ Aging',null,null;
insert into rdsetl.rds_tmp_sheet_config select 2,'500+ Aging',null,null;