drop table if exists table_9874_cpo;
create local temporary table table_9874_cpo on commit preserve rows as 
select a.cpo_no
	,b.part_no
	,a.cpo_status
	,a.cpo_line_no
	,a.cpo_line_status
	,c.cpo_comment as line_cancellation_info
	,a.cpo_entry_datetime as create_date
	,a.cpo_delete_datetime
	,d.name as delete_user
from dm_us.dm_disty_sales_close_cpo_di a
left join dim_us.dim_pub_part_info b
on a.cpo_sku_no=b.sku_no
left join ods_us.ods_cis_corp_history_cpo_comments c
on a.cpo_id=c.cpo_id
and a.cpo_line_seq=c.cpo_line_seq
and c.cpo_comment_type='OX'
left join dim_us.dim_pub_manager d
on a.cpo_delete_id=d.userid
where a.cpo_cust_no in (124254,430592)
and a.cpo_delete_datetime>=current_date()-30
and a.cpo_delete_datetime<current_date()

union

select a.cpo_no
	,b.part_no
	,a.cpo_status
	,a.cpo_line_no
	,a.cpo_line_status
	,c.cpo_comment as line_cancellation_info
	,a.cpo_entry_datetime as create_date
	,a.cpo_delete_datetime
	,d.name as delete_user
from dm_us.dm_disty_sales_open_cpo a
left join dim_us.dim_pub_part_info b
on a.cpo_sku_no=b.sku_no
left join ods_us.ods_cis_corp_cpo_comments c
on a.cpo_id=c.cpo_id
and a.cpo_line_seq=c.cpo_line_seq
and c.cpo_comment_type='OX'
left join dim_us.dim_pub_manager d
on a.cpo_delete_id=d.userid
where a.cpo_cust_no in (124254,430592)
and a.cpo_delete_datetime>=current_date()-30
and a.cpo_delete_datetime<current_date()
;


drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as 
select *
from table_9874_cpo
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;