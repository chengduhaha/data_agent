  
drop table if exists tempdb.rds_order_8700;
create table tempdb.rds_order_8700 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
with min_eta as
( select
		order_no,
		order_type,
		order_line_no,
		sku_no,
		eta_code,
		date_format(min(eta),'%m/%d/%Y') as min_eta
   from dm_ca.dm_pur_unieta_boso_detail_rt eta
   group by order_no, order_type, order_line_no,sku_no,eta_code
)
select uuid_numeric() as id,
       a.order_type,
       a.order_no,
       a.order_line_no,
      cast(null as  int) as  synnex_po,
       a.cust_no,
       ch.cust_name as cust_name,
	   a.loc_no,
       l.loc_char as loc ,
	   oh.ship_method ,
       date_format(a.order_entry_datetime, '%m/%d/%Y') as entry_datetime ,
	   oh.ext_ref as cpo,
	   oh.ship_to_name ,
	   st.end_user_po ,
       a.unit_price * a.order_qty as total_amount,
	   cast(null as  varchar(60)) as spa_no,
	   cast(null as  varchar(60)) as spa_ref_no,
	   eta_code,
	   eta.min_eta as ETA ,
	   a.exp_ship_date,
	   b.part_no ,
	   b.mfg_partno ,
	   a.sku_no,
	   v.vpl_code,
	   a.seg_code,
       a.unit_price,
       a.order_qty
FROM dw_ca.dwd_disty_brpt_bo_detail_df a
LEFT JOIN ods_ca.ods_cis_corp_order_header_rt oh ON a.order_no = oh.order_no
	AND a.order_type = oh.order_type
LEFT JOIN ods_ca.ods_cis_corp_order_soldto_rt st ON a.order_no = st.order_no
	AND a.order_type = st.order_type
LEFT JOIN ods_ca.ods_cis_corp_part_master_rt b ON a.sku_no = b.sku_no
LEFT JOIN ods_ca.ods_cis_corp_customer_header_rt ch ON a.cust_no = ch.cust_no
LEFT JOIN ods_ca.ods_cis_corp_location_info_rt l ON a.loc_no = l.loc_no
LEFT JOIN min_eta eta ON a.sku_no = eta.sku_no
	AND a.order_no = eta.order_no
	AND a.order_type = eta.order_type
	AND a.order_line_no = eta.order_line_no
LEFT JOIN ods_ca.ods_cis_corp_dw_vend_pl_rt v ON b.vpl_no = v.vpl_no
WHERE a.cust_no = 1241432
	AND a.order_type = 8
	AND a.date_flag =date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
;

update tempdb.rds_order_8700
   set synnex_po = b.order_no
  from ods_ca.ods_cis_corp_order_header_rt b
 where rds_order_8700.order_no = b.int_ref_no
   and b.order_type = 2
; 

UPDATE tempdb.rds_order_8700
	SET spa_no = b.profile_i
	, spa_ref_no = b.profile_c
FROM ods_ca.ods_cis_corp_order_exp_rt a 
INNER join ods_ca.ods_cis_corp_order_profile_rt b 
on a.order_no = b.order_no and 
     a.order_type = b.order_type and 
     a.order_line_no = b.order_line_no and 
     a.order_expense_line_no = b.profile_no  AND
     b.profile_type = 'REBATE_ADJ' AND 
     b.active = 'Y'
WHERE rds_order_8700.order_no = a.order_no
AND rds_order_8700.order_type = a.order_type
AND rds_order_8700.order_line_no = a.order_line_no

;
  
drop table if exists tempdb.rds_sku_8700;
create table tempdb.rds_sku_8700   as
select distinct sku_no from   tempdb.rds_order_8700
 ;

   
drop table if exists tempdb.rds_inv_8700;
create table tempdb.rds_inv_8700    as
select a.sku_no 
	,SUM(b.on_hand_qty) as on_hand_qty	
	,SUM(b.on_order_qty) as on_order_qty
	,SUM(b.rio_qty) as rio_qty
	,SUM(b.on_hand_qty - b.bo_qty + b.intran_in - b.intran_out - b.alloc_qty) as avail_qty
from tempdb.rds_sku_8700 a 
inner join dw_ca.dwd_disty_inv_qty_df b on a.sku_no=b.sku_no
WHERE  b.date_flag =  date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
and b.inv_type in (1,200)
group by a.sku_no
;
drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select  order_type,	order_no,	order_line_no,	cust_name,loc,	ship_method	,entry_datetime,	cpo as reseller_po,
ship_to_name,	end_user_po	,total_amount,	spa_no,	spa_ref_no,	eta_code,	ETA	,exp_ship_date,	part_no,	mfg_partno,	a.sku_no	,vpl_code	,seg_code,
unit_price	,order_qty as demand,
b.avail_qty,b.on_hand_qty,b.on_order_qty,b.rio_qty
from tempdb.rds_order_8700 a 
left join tempdb.rds_inv_8700 b on a.sku_no=b.sku_no
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;

drop table if exists tempdb.rds_inv_8700;
drop table if exists tempdb.rds_sku_8700;
drop table if exists tempdb.rds_order_8700;