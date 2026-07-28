-- Typical POS example: sales summary with order_type 114 credit/protection exception.
-- Source: CA/run/rds_7720_rtv.sp

drop table if exists table_ca7720_order;
create local temporary table table_ca7720_order on commit preserve rows as 
select a.vend_no ,
	a.vend_segment ,
	a.vend_name ,
	a.vpl_no ,
	a.vpl_code ,
	b.global_family_desc ,
	b.global_cat_desc ,
	b.global_sub_desc ,
	b.pcode ,
	b.pcode_desc ,
	sum(case when order_type=114 and cpo_no in ('SONY-TRAILLINGCREDIT','SONY-PRICEPROTECTION') then 0 else extend_net_price end) as ext_net_price
from dw_ca.dwd_disty_common_pos_di a
left join dim_ca.dim_pub_part_info b on a.sku_no=b.sku_no
where b.vend_segment = 'SHF'
and a.date_flag >= DATE_TRUNC('MONTH',current_date()-1)
and a.date_flag < CURRENT_DATE() 
and a.order_line_type in ('Single','Kit')
group by a.vend_no ,
	a.vend_segment ,
	a.vend_name ,
	a.vpl_no ,
	a.vpl_code ,
	b.global_family_desc ,
	b.global_cat_desc ,
	b.global_sub_desc ,
	b.pcode ,
	b.pcode_desc 
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as 
select *
from table_ca7720_order
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
