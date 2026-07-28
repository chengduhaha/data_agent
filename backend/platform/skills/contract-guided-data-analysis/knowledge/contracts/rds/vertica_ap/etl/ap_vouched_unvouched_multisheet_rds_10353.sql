-- unvouched
drop table if exists rds_br10353_tab1;
create local temporary table rds_br10353_tab1 on commit preserve rows as
select distinct a.date_flag,
a.rec_no,
a.rec_line_no,
b.rec_datetime,
b.order_type,
b.order_no,
b.order_line_no,
terms_no,
b.vend_no,
b.sku_no,
b.doc_no,
c.item_type,
c.vend_inv_no,
ah_usd_line_amt unvouched,
cast(c.doc_due_date as date) doc_due_date,
terms_days
FROM dw_br.dwd_disty_ap_vdah_lines_di a
inner join ods_br.ods_cis_corp_ap_hold b
	on a.rec_no = b.rec_no
	and a.rec_line_no = b.rec_line_no
left join ods_br.ods_cis_corp_vend_doc c
	on b.doc_no = c.doc_no
inner join ods_br.ods_cis_corp_v_vend_currency z
	on a.vend_no = z.vend_no and z.vend_currency = 'USD'
WHERE a.date_flag = CURRENT_DATE()-1
and a.vd_type = 'U'
and a.usd_amt > 0
;

-- vouched
drop table if exists rds_br10353_tab2;
create local temporary table rds_br10353_tab2 on commit preserve rows as
select distinct a.date_flag,
a.vend_no,
c.vend_name,
b.doc_no,
doc_type,
vend_inv_no,
vd_usd_line_amt vouched,
cast(doc_date as date) doc_date,
item_type,
cast(b.doc_due_date as date) doc_due_date
FROM dw_br.dwd_disty_ap_vdah_lines_di a
left join ods_br.ods_cis_corp_vend_doc b
	on a.doc_no = b.doc_no
inner join dim_br.dim_pub_vendor_info c
	on a.vend_no = c.vend_no
inner join ods_br.ods_cis_corp_v_vend_currency z
	on a.vend_no = z.vend_no and z.vend_currency = 'USD'
WHERE a.date_flag = CURRENT_DATE()-1
and a.vd_type != 'U'
and a.usd_amt > 0
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_br10353_tab1
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from rds_br10353_tab2
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
insert into rdsetl.rds_tmp_sheet_config select 1,'unvouched',null,null;
insert into rdsetl.rds_tmp_sheet_config select 2,'vouched',null,null;