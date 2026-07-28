drop table if exists us_back_orders_19082;
create local temporary table us_back_orders_19082 on commit preserve rows as
select distinct
  a.order_no,
  to_char(a.order_date, 'mm/dd/yyyy') as order_date,
  a.cpo_id,
  a.cpo_no,
  a.sold_to_cust_name,
  a.eu_company_name,
  a.mfg_partno,
  a.order_qty,
  to_char(a.expected_date, 'mm/dd/yyyy') as expected_date
from dw_us.dwd_disty_sales_open_order_detail a
where a.order_type = 8
and a.vend_no = 64036
;

--select * from us_back_orders_19082

drop table if exists us_t_cpo_dis_19082;
create local temporary table us_t_cpo_dis_19082 on commit preserve rows as
select distinct cpo_id
from us_back_orders_19082
;

drop table if exists us_t_cpo_eu_19082;
create local temporary table us_t_cpo_eu_19082 on commit preserve rows as
select
  a.cpo_id,
  l.code_desc,
  c.data_c
from us_t_cpo_dis_19082 a
inner join ods_us.ods_cis_corp_cpo_eu_custom c on a.cpo_id=c.cpo_id
inner join dim_us.dim_pub_eu_custom_map_view m on c.eu_map_id = m.eu_map_id and c.eu_map_line_no = m.eu_map_line_no
inner join dim_us.dim_pub_list_box_detail l on l.code_value = m.map_data_desc
where l.list_box_code = 'CEDM'
and l.code_desc in('Vendor Quote ID')
union
select
  a.cpo_id,
  l.code_desc,
  c.data_c
from us_t_cpo_dis_19082 a
inner join ods_us.ods_cis_corp_history_cpo_eu_custom c	on a.cpo_id=c.cpo_id
inner join dim_us.dim_pub_eu_custom_map_view m on c.eu_map_id = m.eu_map_id and c.eu_map_line_no = m.eu_map_line_no
inner join dim_us.dim_pub_list_box_detail l	on l.code_value = m.map_data_desc
where l.list_box_code = 'CEDM'
and l.code_desc in('Vendor Quote ID')
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select distinct
  a.order_no as 'BO#',
  a.order_date as 'SO Date',
  a.cpo_id as 'TD SYNNEX PO ID',
  a.cpo_no as 'Partner PO',
  a.sold_to_cust_name as 'Sold To Partner',
  a.eu_company_name as 'EU Biz Name',
  b.data_c  as 'Vendor Quote #',
  a.mfg_partno as 'MFGPart#',
  a.order_qty as 'Qty',
  a.expected_date as 'Est Arrival'
from us_back_orders_19082 a
left join us_t_cpo_eu_19082 b on a.cpo_id = b.cpo_id
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;
