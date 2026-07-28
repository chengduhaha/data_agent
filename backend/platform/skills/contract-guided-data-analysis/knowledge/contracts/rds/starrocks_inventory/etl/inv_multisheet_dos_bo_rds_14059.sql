
drop table if exists tempdb.rds_tmp_sheet_config;
create table tempdb.rds_tmp_sheet_config(
    sheet_name varchar(50) null,
    title_active varchar(1) null,
    date_pattern varchar(50) null
   )
;

insert into tempdb.rds_tmp_sheet_config values('US - Apple OnHand Inventory',null,null);
insert into tempdb.rds_tmp_sheet_config values('Back Orders',null,null);

-- part1
drop table if exists tempdb.temp_14059_vend;
create table tempdb.temp_14059_vend as
select distinct c.vend_no
      ,c.mfg_partno as  VendPart
	  ,c.sku_no as TDMat
	  ,c.short_desc as MatDesc
	  ,b.vpl_code as LMan
	  ,c.pur_comment as Red_Notes_1
	  ,c.mar_comment as Red_Notes_2
	  ,ifnull(c.po_cost,c.ave_cost) as MAV
	  ,c.abc_code
from  ods_us.ods_cis_corp_dw_vend_pl_rt b
inner join ods_us.ods_cis_corp_part_master_rt c
on b.vpl_no=c.vpl_no
and b.vend_no=c.vend_no
where b.vend_no in (73885, 74417, 74418,75078)
and b.active='Y'
;



drop table if exists tempdb.temp_14059_sku;
create table tempdb.temp_14059_sku PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
select
	   uuid_numeric() as id,
       a.LMan
      ,a.VendPart
      ,a.TDMat
	  ,a.MatDesc
      ,sum(ifnull(b.on_hand_qty,0)) AS OnHand
      ,sum(ifnull(b.on_hand_qty-b.bo_qty-b.alloc_qty-b.wip_qty-b.intran_out,0)) AS AvailQty
      ,sum(ifnull(b.on_hand_qty,0) + ifnull(b.intran_in,0)) total_inv
	  ,sum(ifnull(b.on_order_qty,0)) AS OnPO
	  ,sum(case when loc_no = 3 then b.on_order_qty else 0 end) DFR_on_order
	  ,sum(case when loc_no = 7 then b.on_order_qty else 0 end) DTN_on_order
	  ,sum(case when loc_no = 8 then b.on_order_qty else 0 end) DNJ_on_order
	  ,sum(case when loc_no = 50 then b.on_order_qty else 0 end) DCO_on_order
	  ,sum(case when loc_no = 99 then b.on_order_qty else 0 end) D99_on_order
	  ,sum(case when loc_no = 502 then b.on_order_qty else 0 end) DGA_on_order
	  ,sum(case when loc_no = 503 then b.on_order_qty else 0 end) DSW_on_order
	  ,sum(case when loc_no = 504 then b.on_order_qty else 0 end) DIN_on_order
	  ,sum(case when loc_no = 505 then b.on_order_qty else 0 end) DFW_on_order
	  ,sum(case when loc_no = 506 then b.on_order_qty else 0 end) DFO_on_order

	  ,sum(ifnull(b.rio_qty,0)) as rio_qty
	  ,sum(case when loc_no = 3 then b.on_hand_qty else 0 end) DFR
	  ,sum(case when loc_no = 7 then b.on_hand_qty else 0 end) DTN
	  ,sum(case when loc_no = 8 then b.on_hand_qty else 0 end) DNJ
	  ,sum(case when loc_no = 50 then b.on_hand_qty else 0 end) DCO
	  ,sum(case when loc_no = 99 then b.on_hand_qty else 0 end) D99
	  ,sum(case when loc_no = 502 then b.on_hand_qty else 0 end) DGA
	  ,sum(case when loc_no = 503 then b.on_hand_qty else 0 end) DSW
	  ,sum(case when loc_no = 504 then b.on_hand_qty else 0 end) DIN
	  ,sum(case when loc_no = 505 then b.on_hand_qty else 0 end) DFW
	  ,sum(case when loc_no = 506 then b.on_hand_qty else 0 end) DFO
	  ,null as other
	  ,null as DOS1
	  ,b.inv_type
	  ,a.Red_Notes_1
	  ,a.Red_Notes_2
	  ,a.MAV
	  ,a.abc_code
from tempdb.temp_14059_vend a
inner join dw_us.dwd_disty_inv_qty_df b
on a.TDMat = b.sku_no
and b.date_flag =  date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
where b.inv_type = 1
group by a.LMan,a.VendPart,a.TDMat,a.MatDesc,b.inv_type,a.Red_Notes_1,a.Red_Notes_2,a.MAV,a.abc_code
;





drop table if exists tempdb.temp_14059_maxweek;
create table tempdb.temp_14059_maxweek as
select a.sku_no,
	   max(week) as max_week
from dw_us.dws_disty_pur_ips_runrate_1w a
inner join tempdb.temp_14059_sku b
on a.inv_type = b.inv_type
and a.sku_no=b.TDMat
where a.sum_type ='WITYPESTU'
group by a.sku_no
;

drop table if exists tempdb.temp_14059_dos;
create table tempdb.temp_14059_dos as
select a.sku_no,
	   sum(case when b.max_week-4 < a.week and b.max_week>a.week then a.runrate_qty else 0 end ) as q4w
from dw_us.dws_disty_pur_ips_runrate_1w a
inner join tempdb.temp_14059_maxweek b
	on a.sku_no = b.sku_no
;





update tempdb.temp_14059_sku
set DOS1 = temp_14059_sku.AvailQty*20/(case when b.q4w=0 then null else b.q4w end)
from tempdb.temp_14059_dos b
where temp_14059_sku.TDMat=b.sku_no
;

update tempdb.temp_14059_sku
set other = total_inv - DFR - DTN - DNJ- DCO- D99- DGA - DSW - DIN - DFW - DFO
;


drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select LMan as VPC
      ,VendPart as 'MFG Part'
      ,TDMat as SKU
	  ,abc_code as 'ABC code'
      ,MatDesc as Description
	  ,MAV as 'Base Cost'
      ,OnHand
      ,AvailQty
      ,OnPO as 'On Order'
	  , DFR_on_order
	  , DTN_on_order
	  , DNJ_on_order
	  , DCO_on_order
	  , D99_on_order
	  , DGA_on_order
	  , DSW_on_order
	  , DIN_on_order
	  , DFW_on_order
	  , DFO_on_order
	  ,rio_qty as 'RIO qty'
--      ,Red_Notes_1 as SlsBlock
	  ,other as 'Others-OH'
	  ,DFR as '3-DFR-OH'
	  ,DTN as '7-DTN-OH'
	  ,DNJ as '8-DNJ-OH'
	  ,DCO as '50-DCO-OH'
	  ,D99 as '99-D99-OH'
	  ,DGA as '502-DGA-OH'
	  ,DSW as '503-DSW-OH'
	  ,DIN as '504-DIN-OH'
	  ,DFW as '505-DFW-OH'
	  ,DFO as '506-DFO-OH'
      ,Red_Notes_2 as SlsBlkDesc
from tempdb.temp_14059_sku
;


select * from tempdb.rds_tmp
;

-- part2


drop table if exists tempdb.rds_order_14059;
create table tempdb.rds_order_14059 as
with min_eta as
( select
		order_no,
		order_type,
		order_line_no,
		sku_no,
		date_format(min(eta),'%m/%d/%Y') as min_eta
   from dm_us.dm_pur_unieta_boso_detail_rt eta
   group by order_no, order_type, order_line_no,sku_no
)
select bo.order_type,
       bo.order_no,
       bo.order_line_no,
       null as synnex_po,
       ifnull(hh.ext_ref,oh.ext_ref) as cpo,
       bo.cust_no,
       ch.cust_name as cust_name,
       bo.cust_terr,
       t.terr_name as terr_name,
       bo.sku_no,
       pm.part_no as part_no,
       bo.unit_cost as unit_price,
       bo.order_qty,
       bo.unit_cost * bo.order_qty as total_amount,
       eta.min_eta as ETA,
       exp_ship_date,
       date_format( bo.order_entry_datetime, '%m/%d/%Y') as entry_datetime,
       bo.loc_no,
       l.loc_name as loc_name
  from dw_us.dwd_disty_brpt_bo_detail_df bo
  left join ods_us.ods_cis_corp_order_header_rt oh
	on bo.order_no = oh.order_no
   and bo.order_type = oh.order_type
  left join ods_us.ods_cis_corp_history_header_rt hh
	on bo.order_no = hh.order_no
   and bo.order_type = hh.order_type
  left join ods_us.ods_cis_corp_customer_header_rt ch
	on bo.cust_no = ch.cust_no
  left join ods_us.ods_cis_corp_territory_rt t
	on bo.cust_terr = t.sales_terr
  left join ods_us.ods_cis_corp_part_master_rt pm
	on bo.sku_no = pm.sku_no
  left join ods_us.ods_cis_corp_location_info_rt l
	on bo.loc_no = l.loc_no
  left join min_eta eta
   on bo.sku_no=eta.sku_no
   and bo.order_no = eta.order_no
   and bo.order_type = eta.order_type
   and bo.order_line_no = eta.order_line_no
 where bo.vend_no in (73885, 74417, 74418,75078)
 and bo.date_flag =  date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
;



drop table if exists tempdb.rds_tmp_1;
create table tempdb.rds_tmp_1 as
select order_type as 'Order Type',
       order_no as 'Order #',
       order_line_no as 'Line #',
       synnex_po as 'SYNNEX PO#',
       cpo as 'Customer PO',
       cust_no as 'Cust #',
       cust_name as 'Cust Name',
       cust_terr as 'Terr #',
       terr_name as 'Terr Name',
       sku_no as 'SKU #',
       part_no as 'Part #',
       unit_price as 'Net Price',
       order_qty as 'Order Quantity',
       total_amount as 'Total Amount',
       ETA as 'ETA Date Time',
       exp_ship_date as 'Expected Ship Date',
       entry_datetime as 'Entry Date Time',
       loc_no as 'Location #',
       loc_name as 'Location Name'
  from tempdb.rds_order_14059
 where order_type = 8
;


drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;

insert into tempdb.rds_tmp_body
select 2 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp_1
;
