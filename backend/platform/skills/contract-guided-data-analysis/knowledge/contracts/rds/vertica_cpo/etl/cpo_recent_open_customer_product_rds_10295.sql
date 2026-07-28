	
		
drop table if exists rds_10295_rtv;
create LOCAL TEMPORARY TABLE rds_10295_rtv ON COMMIT PRESERVE ROWS AS 	
select distinct a.cpo_id,
       a.cpo_no as webq_no,
       to_char(a.cpo_entry_datetime,'MM-DD-YYYY') as cpo_entry_datetime,
       a.cpo_cust_name as cust_name,
       a.ship_to_name as ship_to,
       c.part_no,
       a.cpo_line_qty,
	   a.cpo_line_qty * a.cpo_unit_price as cpo_amount,
       cast(round(100*(a.cpo_unit_price - a.cpo_unit_cost)/nullif(a.cpo_unit_price,0),4) as varchar(10)) || '%' as gm,
       e.order_no as order_no,
       to_char(e.entry_datetime,'MM-DD-YYYY') as order_entry_date,
	   a.spa_ref_no,
	   a.cpo_sales_terr as sales_terr ,
	   a.reseller_cust_no ,
	   isnull(d.email,'sales'||to_char(a.cpo_sales_terr)||'@tdsynnex.com') as sales_terr_email
from dm_us.dm_disty_sales_open_cpo a
inner join dim_us.dim_pub_part_info c
on a.cpo_sku_no=c.sku_no
left join ods_us.ods_cis_corp_order_header e
on a.cpo_id = e.int_ref_no
and e.ext_ref=a.cpo_no
left join dim_us.dim_pub_sales_hierarchy_by_terr_user_role b
on a.cpo_sales_terr=b.sales_terr
left join dim_us.dim_pub_manager d
on b.terr_name=d.name
where c.vend_no=17516
and a.cpo_entry_datetime >=current_date()-30
and a.cpo_entry_datetime < CURRENT_DATE()
;

insert into rds_10295_rtv
select distinct a.cpo_id,
       a.cpo_no as webq_no,
       to_char(a.cpo_entry_datetime,'MM-DD-YYYY') as cpo_entry_datetime,
       a.cpo_cust_name as cust_name,
       a.ship_to_name as ship_to,
       c.part_no,
       a.cpo_line_qty,
	   a.cpo_line_qty * a.cpo_unit_price as cpo_amount,
       cast(round(100*(a.cpo_unit_price - a.cpo_unit_cost)/nullif(a.cpo_unit_price,0),4) as varchar(10)) || '%' as gm,
       e.order_no as order_no,
       to_char(e.entry_datetime,'MM-DD-YYYY') as order_entry_date,
	   a.spa_ref_no,
	   a.cpo_sales_terr as sales_terr   ,
	   a.reseller_cust_no ,
	   isnull(d.email,'sales'||to_char(a.cpo_sales_terr)||'@tdsynnex.com') as sales_terr_email
from dm_us.dm_disty_sales_open_cpo a
inner join dim_us.dim_pub_part_info c
on a.cpo_sku_no=c.sku_no
left join ods_us.ods_cis_corp_history_header e
on a.cpo_id = e.int_ref_no
and e.ext_ref=a.cpo_no
left join dim_us.dim_pub_sales_hierarchy_by_terr_user_role b
on a.cpo_sales_terr=b.sales_terr
left join dim_us.dim_pub_manager d
on b.terr_name=d.name
where c.vend_no=17516
and a.cpo_entry_datetime >=current_date()-30
and a.cpo_entry_datetime < CURRENT_DATE()
and a.cpo_id not in (select cpo_id from rds_10295_rtv)
;

drop table if exists rdsetl.rds_tmp; 
CREATE TABLE rdsetl.rds_tmp AS
select * from rds_10295_rtv;


drop table if exists rdsetl.rds_tmp_body;
CREATE TABLE rdsetl.rds_tmp_body AS 
select 
		 1 as flag
		,'Standard' as body_type
		,count(*) as cnt
from rdsetl.rds_tmp
;