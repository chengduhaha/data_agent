drop table if exists tempdb.t_7522;
create table tempdb.t_7522 as
select order_type,
       order_line_no,
       cast(null as varchar(100)) as cust_po_no,
       order_no,
       sku_no,
       cast(null as varchar(60)) as part_no,
       cast(null as varchar(500)) part_description,
       (unit_price+ifnull(unit_sum_expense,0)) as unit_net_price,
       ship_qty*(unit_price+ifnull(unit_sum_expense,0)) as extend_net_price,
       cast(null as char(10)) as invoice_date,
       cast(null as varchar(10)) as exp_ship_date,
       cast(null as char(10)) as ship_date,
       cast(null as int) as order_qty,
       ship_qty,
       cast(null as varchar(60)) as ship_to_name,
       cast(null as varchar(60)) as ship_to_addr,
       cast(null as int) as from_loc_no,
       cast(null as varchar(60)) as from_loc_name,
       cast(null as varchar(30)) as ship_method,
       cast(null as varchar(60)) as ship_desc,
       cast(null as varchar(2000)) as tracking_no,
       cast(null as varchar(8000)) as serial_no,
       cast(null as int) as avail,
       cast(null as int) as on_hand,
       cast(null as int) as on_order,
       cast(null as varchar(10)) as ETA,
       cast(null as varchar(60)) as ETA_code,
       cast(null as varchar(255)) as marketing_comments
  from dw_ca.dwd_disty_pub_dw_orders_extend_di
 where date_flag >= date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
   and date_flag < date_format(current_date(),'%Y-%m-%d')
   and cust_no in (1057431,1240353 )
;

insert into tempdb.t_7522
select order_type,
       order_line_no,
       cast(null as varchar(100)) as cust_po_no,
       order_no,
       sku_no,
       cast(null as varchar(60)) as part_no,
       cast(null as varchar(500)) as part_description,
       unit_price as unit_net_price,
       order_qty*unit_cost as extend_net_price,
       cast(null as varchar(10)) as invoice_date,
       exp_ship_date,
       cast(null as varchar(10)) as ship_date,
       order_qty,
       cast(null as int) as ship_qty,
       cast(null as varchar(60)) as ship_to_name,
       cast(null as varchar(60)) as ship_to_addr,
       cast(null as int) as from_loc_no,
       cast(null as varchar(60)) as from_loc_name,
       cast(null as varchar(30)) as ship_method,
       cast(null as varchar(60)) as ship_desc,
       cast(null as varchar(2000)) as tracking_no,
       cast(null as varchar(8000)) as serial_no,
       cast(null as int) as avail,
       cast(null as int) as on_hand,
       cast(null as int) as on_order,
       cast(null as varchar(10)) as ETA,
       cast(null as char(3)) as ETA_code,
       cast(null as varchar(255)) as marketing_comments
  from dw_ca.dwd_disty_brpt_bo_detail_df
 where order_type = 8
   and cust_no in (1057431,1240353 )
   and date_flag = date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
;

drop table if exists tempdb.t1_7522;
create table tempdb.t1_7522 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) as
select uuid_numeric() as id,
       a.order_type,
       a.order_line_no,
       oh.ext_ref as cust_po_no,
       a.order_no,
       a.sku_no,
       pm.part_no,
       pm.short_desc as part_description,
       a.unit_net_price,
       a.extend_net_price,
       date_format(oh.invoice_date,'%m/%d/%Y') as invoice_date,
       ifnull(oh.expected_date,a.exp_ship_date) as exp_ship_date,
       a.ship_date,
       a.order_qty,
       a.ship_qty,
       oh.ship_to_name as ship_to_name,
       oh.ship_to_addr as ship_to_addr,
       oh.from_loc_no as from_loc_no,
       a.from_loc_name,
       oh.ship_method as ship_method,
       a.ship_desc,
       a.tracking_no,
       a.serial_no,
       a.avail,
       a.on_hand,
       a.on_order,
       a.ETA,
       a.ETA_code,
       pm.mar_comment as marketing_comments
  from tempdb.t_7522 a
  left join ods_ca.ods_cis_corp_part_master_rt pm
	on a.sku_no = pm.sku_no
  left join ods_ca.ods_cis_corp_order_header_rt oh
	on a.order_no = oh.order_no
   and a.order_type = oh.order_type
;




 update tempdb.t1_7522
    set invoice_date = date_format(b.invoice_date,'%m/%d/%Y'),
        cust_po_no = b.ext_ref,
        ship_to_addr = b.ship_to_addr,
        ship_to_name = b.ship_to_name,
        ship_method = b.ship_method,
        from_loc_no = b.from_loc_no,
        exp_ship_date = date_format(b.expected_date,'%m/%d/%Y')
   from ods_ca.ods_cis_corp_history_header_rt b
  where t1_7522.order_no = b.order_no
    and t1_7522.order_type = b.order_type
 ;

update tempdb.t1_7522
   set from_loc_name = b.loc_name
  from ods_ca.ods_cis_corp_location_info_rt b
 where t1_7522.from_loc_no = b.loc_no
;

update tempdb.t1_7522
   set ship_desc = b.ship_desc
  from ods_ca.ods_cis_corp_ship_method b
 where t1_7522.ship_method = b.ship_method
;


drop table if exists tempdb.eta;
create table tempdb.eta as
select  a.order_type,
		a.order_no,
		max(est_ship_date) as est_ship_date
from ods_ca.ods_cis_corp_uni_eta_log_rt a
inner join tempdb.t1_7522 b
	on a.order_type = b.order_type
	and a.order_no = b.order_no
	and a.order_type =8
group by a.order_type,a.order_no
;

update tempdb.t1_7522
set exp_ship_date = date_format(b.est_ship_date,'%m/%d/%Y')
from tempdb.eta b
where b.order_no=b.order_no
and  b.order_type = b.order_type
;

drop table if exists tempdb.t_ser_no_7522;
create table tempdb.t_ser_no_7522 as
SELECT distinct  b.order_no,
				 b.order_type,
				 a.sku_no,
				 a.ser_no
FROM ods_ca.ods_cis_corp_serial_nbr_rt a
inner join tempdb.t1_7522 b
	 on a.order_no=b.order_no
	AND a.order_type=b.order_type
	AND a.sku_no=b.sku_no
UNION
SELECT  b.order_no,
		b.order_type,
		a.sku_no,
		a.ser_no
FROM ods_ca.ods_cis_corp_history_serial_nbr_rt a
inner join tempdb.t1_7522 b
	on a.order_no=b.order_no
	AND a.order_type=b.order_type
	AND a.sku_no=b.sku_no
;



drop table if exists tempdb.ser_no;
create table tempdb.ser_no as
select *
from tempdb.t_ser_no_7522
order by order_no,order_type,sku_no
;


drop table if exists tempdb.ser_no_2;
create table tempdb.ser_no_2 as
select  order_no,
		order_type,
		sku_no,
		group_concat(ser_no,',') as all_comment
from tempdb.ser_no
group by order_no,order_type, sku_no
;

update tempdb.t1_7522
set serial_no = all_comment
from tempdb.ser_no_2 b
where t1_7522.order_no = b.order_no
and t1_7522.order_type = b.order_type
and t1_7522.sku_no = b.sku_no
;

drop table if exists tempdb.track_7522;
create table tempdb.track_7522 as
select distinct b.order_type,b.order_no,ifnull(b.track_no,'') as track_no
 from  tempdb.t1_7522 a
 inner join ods_ca.ods_cis_corp_carton_header_rt b
	on a.order_no = b.order_no
   and a.order_type = b.order_type
  ;

delete from tempdb.track_7522
where track_no = ''
;


drop table if exists tempdb.track_7522_group;
create table tempdb.track_7522_group as
select  a.order_type,a.order_no,GROUP_CONCAT(a.track_no,'/') as track_no
 from tempdb.track_7522 a
group by a.order_type,a.order_no
  ;



 update tempdb.t1_7522
   set tracking_no = ifnull(b.track_no,'') -- combine
  from tempdb.track_7522_group b
 where t1_7522.order_type = b.order_type
   and t1_7522.order_no = b.order_no
;


drop table if exists tempdb.rds_inv_qty_7522;
create table tempdb.rds_inv_qty_7522 as
select sku_no,
       loc_no,
       sum(on_hand_qty) as on_hand_qty,
       sum(bo_qty) as bo_qty,
       sum(alloc_qty) as alloc_qty,
       sum(wip_qty) as wip_qty,
       sum(intran_out) as intran_out,
       sum(on_order_qty) as on_order_qty
  from ods_ca.ods_cis_corp_inv_qty_rt ciq
 where inv_type in (1, 300)
 group by sku_no, loc_no
;



update tempdb.t1_7522
   set avail = b.on_hand_qty-b.bo_qty-b.alloc_qty-b.wip_qty-b.intran_out,
       on_hand = b.on_hand_qty,
       on_order = b.on_order_qty
  from tempdb.rds_inv_qty_7522 b
 where t1_7522.sku_no = b.sku_no
   and t1_7522.from_loc_no = b.loc_no
;

-- update ETA&ETA_code
drop table if exists tempdb.inv_eta;
create table tempdb.inv_eta as
 select
		-- order_no,
		-- order_type,
		-- order_line_no,
		sku_no,
		loc_no ,
		inv_type,
		eta_code,
		date_format(min(eta),'%Y/%m/%d') as min_eta
   from dm_ca.dm_pur_unieta_sku_detail_rt eta
   group by sku_no, loc_no,inv_type,eta_code
;


  update tempdb.t1_7522
	   set ETA = b.min_eta,
	       ETA_code = b.eta_code
	  from tempdb.inv_eta b
	 where t1_7522.sku_no = b.sku_no
	   and t1_7522.from_loc_no = b.loc_no
	   and b.inv_type = 1
	   ;


drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select cust_po_no,
       order_type,
       order_no,
       order_line_no,
       sku_no,
       part_no,
       part_description,
       unit_net_price,
       extend_net_price,
       exp_ship_date,
       invoice_date,
       ship_date,
       order_qty,
       ship_qty,
       ship_to_name,
       ship_to_addr,
       from_loc_name,
       ship_method,
       ship_desc,
       ifnull(concat('"','=',tracking_no,'=','"'),'"=="') as tracking_no,
       ifnull(concat('"','=',serial_no,'=','"'),'"=="') as serial_no,
       avail,
       on_hand,
       on_order,
       ETA,
       ETA_code,
       marketing_comments
  from tempdb.t1_7522
 order by order_type,order_no,order_line_no
 ;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;

select * from tempdb.rds_tmp;
