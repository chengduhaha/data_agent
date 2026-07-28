
DROP TABLE IF EXISTS rds_t_hyuk_tmp_100791;
create table rds_t_hyuk_tmp_100791 as      
select a.source,
a.order_type,
a.order_no,
a.order_line_no,
p.vend_no ,
b.sku_no,
p.part_no,
cast(a.ship_date as date) as  ship_date,
a.eta_qty,
a.eta_code,
cast(a.eta_date as date) as  eta_date,
a.entry_id,
m.loginid,
a.tracking_no,
a.entry_datetime  
from ods_hyuk.ods_cis_corp_order_eta_detail  a
 left join ods_hyuk.ods_cis_corp_order_detail  b
 on  a.order_no = b.order_no    
	and a.order_type = b.order_type    
	and a.order_line_no = b.order_line_no   
 left join ods_hyuk.ods_cis_corp_part_master  p on b.sku_no = p.sku_no
 left join ods_hyuk.ods_cis_corp_manager  m on  a.entry_id = m.userid
 where a.entry_datetime >= date_add(CURRENT_DATE () ,interval - 1 MONTH)
	AND a.entry_datetime < CURRENT_DATE ()
	AND a.order_type = 2 
;

insert  into rds_t_hyuk_tmp_100791     
select a.source,
a.order_type,
a.order_no,
a.order_line_no,
p.vend_no ,
b.sku_no,
p.part_no,
cast(a.ship_date as date) as  ship_date,
a.eta_qty,
a.eta_code,
cast(a.eta_date as date) as  eta_date,
a.entry_id,
m.loginid,
a.tracking_no,
a.entry_datetime
 from ods_hyuk.ods_cis_corp_history_eta_detail  a
 left join ods_hyuk.ods_cis_corp_history_detail  b
 on  a.order_no = b.order_no    
	and a.order_type = b.order_type    
	and a.order_line_no = b.order_line_no   
 left join ods_hyuk.ods_cis_corp_part_master  p on b.sku_no = p.sku_no
 left join ods_hyuk.ods_cis_corp_manager m on  a.entry_id = m.userid
 where a.entry_datetime >= date_add(CURRENT_DATE(), interval - 1 MONTH)
	AND a.entry_datetime < CURRENT_DATE ()
	AND a.order_type = 2 

;  

DROP TABLE IF EXISTS rds_tmp;
create table rds_tmp as 
select * from  rds_t_hyuk_tmp_100791
;


drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;
 
DROP TABLE IF EXISTS rds_t_hyuk_tmp_100791;
 