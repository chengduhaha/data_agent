


drop table if exists tempdb.rds_sku_14053;
create table tempdb.rds_sku_14053 as
select b.vend_no,
       d.vend_name,
       a.sku_no,
       b.mfg_partno,
       b.short_desc as short_desc,
       c.vpl_code
  from ods_us.ods_cis_corp_sku_profile_rt a
  inner join ods_us.ods_cis_corp_part_master_rt b
	on a.sku_no = b.sku_no
  inner join ods_us.ods_cis_corp_dw_vend_pl_rt c
	on b.vpl_no = c.vpl_no
  inner join ods_us.ods_cis_corp_vend_master_rt d
	on  b.vend_no = d.vend_no
 where a.profile_type = 'CUST_SKU'
   and a.profile_cat = 'CUST'
   and a.active = 'Y'
   and a.profile_i = 116405
   and b.vend_no in (73885, 74418, 74417)
;


drop table if exists tempdb.rds_ord_14053;
create table tempdb.rds_ord_14053 as
select distinct d.vend_no,
       d.vend_name,
       d.sku_no,
       d.mfg_partno,
       d.short_desc,
       d.vpl_code,
       -- vpo = convert(int, null),
       b.ext_ref as cust_po,
       b.order_type,
       b.order_no,
       c.order_line_no,
       date_format(c.entry_datetime,'%m/%d/%Y') as entry_datetime,
       b.from_loc_no,
       l.loc_char as loc,
       b.to_acct_no as bill_to_cust_no,
       ch.cust_name as bill_to_cust_name,
       b.ship_to_name,
       b.ship_to_addr,
       b.ship_to_city,
       b.ship_to_state,
       b.ship_to_zip,
       c.order_qty - ifnull(c.ship_qty,0)  as Open_Qty,
       c.unit_price
       -- unit_usum=convert(money,null),
       -- extended_price=convert(money,null),
       -- expected_date = convert(varchar(10), null),
       -- oh = convert(int, null),
       -- oo = convert(int, null),
       -- alloc_qty = convert(int, null),
       -- serial_no = convert(varchar(1000), null),
       -- end_user_po = convert(varchar(40), null)
  from tempdb.rds_sku_14053 d
  inner join ods_us.ods_cis_corp_order_detail_rt c
  on c.sku_no = d.sku_no
  inner join ods_us.ods_cis_corp_order_header_rt b
   on b.order_no = c.order_no
   and b.order_type = c.order_type
  left join ods_us.ods_cis_corp_location_info_rt l
	on l.loc_no = b.from_loc_no
 left join ods_us.ods_cis_corp_customer_header_rt ch
	on ch.cust_no = b.to_acct_no
   where b.delete_date is null
   and c.delete_date is null
   and b.order_type in (1, 8)
;


drop table if exists tempdb.rds_sum_expense_14053;
create table tempdb.rds_sum_expense_14053 as
select a.order_type,
       a.order_no,
	   a.order_line_no,
	   sum(ifnull(b.unit_exp,0)) as unit_usum
from tempdb.rds_ord_14053 a
inner join ods_us.ods_cis_corp_order_exp_rt b
on a.order_type = b.order_type
  and a.order_no = b.order_no
  and a.order_line_no = b.order_line_no
  and b.order_exp_type = 'DP'
  and b.delete_date is null
group by a.order_type, a.order_no, a.order_line_no
;


drop table if exists tempdb.rds_usum_14053;
create table tempdb.rds_usum_14053 as
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
select distinct
       a.vend_no,
       a.vend_name,
       a.sku_no,
       a.mfg_partno,
       a.short_desc,
       a.vpl_code,
       -- vpo = convert(int, null),
       a.cust_po,
       a.order_type,
       a.order_no,
       a.order_line_no,
       a.entry_datetime,
       a.from_loc_no,
       a.loc,
       a.bill_to_cust_no,
       a.bill_to_cust_name,
       a.ship_to_name,
       a.ship_to_addr,
       a.ship_to_city,
       a.ship_to_state,
       a.ship_to_zip,
       a.Open_Qty,
       (a.unit_price+ifnull(b.unit_usum,0)) as unit_price,
       ifnull(b.unit_usum,0) as  unit_usum,
       (a.unit_price+ifnull(b.unit_usum,0)) * a.Open_Qty as extended_price,
        eta.min_eta as expected_date,
       c.on_hand_qty as oh,
       c.on_order_qty as oo,
       c.alloc_qty as alloc_qty,
       -- serial_no = convert(varchar(1000), null),
       d.end_user_po as end_user_po
  from tempdb.rds_ord_14053 a
  left join tempdb.rds_sum_expense_14053 b
	on a.order_no = b.order_no
	and a.order_type = b.order_type
	and a.order_line_no = b.order_line_no
  left join min_eta eta
   on a.sku_no=eta.sku_no
   and a.order_no = eta.order_no
   and a.order_type = eta.order_type
   and a.order_line_no = eta.order_line_no
  left join dw_us.dwd_disty_inv_qty_df c
	on a.sku_no = c.sku_no
   and a.from_loc_no = c.loc_no
   and c.date_flag = date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%m/%d/%Y')
   and c.inv_type = 1
  left join ods_us.ods_cis_corp_order_soldto_rt d
  on a.order_no = d.order_no
   and a.order_type = d.order_type
;







-- ser_no start
drop table if exists tempdb.rds_ser_no1_14053;
create table tempdb.rds_ser_no1_14053 as
select distinct a.order_no,
       a.order_type,
       a.order_line_no,
       b.ser_no
  from ods_us.ods_cis_corp_history_serial_nbr_rt b
  inner join tempdb.rds_usum_14053 a
 where a.order_no = b.order_no
   and a.order_type = b.order_type
   and a.order_line_no = b.order_line_no
   and b.ser_no is not null
union
select distinct a.order_no,
       a.order_type,
       a.order_line_no,
       b.ser_no
  from ods_us.ods_cis_corp_serial_nbr_rt b
  inner join tempdb.rds_usum_14053 a
 where a.order_no = b.order_no
   and a.order_type = b.order_type
   and a.order_line_no = b.order_line_no
   and b.ser_no is not null
;


drop table if exists tempdb.rds_final_14053;
create table tempdb.rds_final_14053 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
select distinct
	   uuid_numeric() as id,
       a.vend_no,
       a.vend_name,
       a.sku_no,
       a.mfg_partno,
       a.short_desc,
       a.vpl_code,
       null as vpo,
       a.cust_po,
       a.order_type,
       a.order_no,
       a.order_line_no,
       a.entry_datetime,
       a.from_loc_no,
       a.loc,
       a.bill_to_cust_no,
       a.bill_to_cust_name,
       a.ship_to_name,
       a.ship_to_addr,
       a.ship_to_city,
       a.ship_to_state,
       a.ship_to_zip,
       a.Open_Qty,
       a.unit_price,
       a.unit_usum,
       a.extended_price,
       a.expected_date,
       a.oh,
       a.oo,
       a.alloc_qty,
       b.ser_no as serial_no,
       a.end_user_po
  from tempdb.rds_usum_14053 a
  left join tempdb.rds_ser_no1_14053 b
	on a.order_no = b.order_no
	and a.order_type = b.order_type
	and a.order_line_no= b.order_line_no
 ;






update tempdb.rds_final_14053
set vpo=b.int_ref_no
from ods_us.ods_cis_corp_order_header_rt b
where rds_final_14053.order_no=b.order_no
and rds_final_14053.order_type=b.order_type
and b.int_ref_type=2
;


update tempdb.rds_final_14053
set vpo=b.int_ref_no
from ods_us.ods_cis_corp_history_header_rt b
where rds_final_14053.order_no=b.order_no
and rds_final_14053.order_type=b.order_type
and b.int_ref_type=2
and rds_final_14053.vpo is null
;

update tempdb.rds_final_14053
set vpo=b.order_no
from ods_us.ods_cis_corp_order_header_rt b
where rds_final_14053.order_no=b.int_ref_no
and rds_final_14053.order_type=b.int_ref_type
and b.order_type=2
and rds_final_14053.vpo is null
;


update tempdb.rds_final_14053
set vpo=b.order_no
from ods_us.ods_cis_corp_history_header_rt b
where rds_final_14053.order_no=b.int_ref_no
and rds_final_14053.order_type=b.int_ref_type
and b.order_type=2
and rds_final_14053.vpo is null
;

update tempdb.rds_final_14053
set vpo=b.int_ref_no
from ods_us.ods_cis_corp_history_header_rt b
where rds_final_14053.order_no=b.order_no
and rds_final_14053.order_type=b.order_type
and b.int_ref_type=2
and rds_final_14053.vpo is null
;


update tempdb.rds_final_14053
set vpo=b.int_ref_no
from ods_us.ods_cis_corp_mc_order_ref_rt b
where rds_final_14053.order_no=b.order_no
and rds_final_14053.order_type=b.order_type
and b.int_ref_type=2
and rds_final_14053.vpo is null
;


drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select distinct
       -- vend_no as 'Group#',
       -- vend_name as 'Group',
       -- sku_no as 'Item#',
       mfg_partno as 'MANPart#',
       short_desc as 'ItemDescription',
       -- vpl_code as 'P/Line',
       vpo as 'Vendor PO#',
       cust_po as 'Customer PO',
       -- order_type as 'Sales Order Type',
       order_no as 'Sales Order#',
       expected_date as 'Estimated Ship Date',
       -- order_line_no as 'Order Line#',
       entry_datetime as 'Created On Date',
       loc as 'Plant',
       -- bill_to_cust_no as 'Bill To Cust#',
       -- bill_to_cust_name as 'Bill To Cust Name',
       ship_to_name as 'Ship To Name',
       -- ship_to_addr as 'Ship To Street',
       -- ship_to_city as 'Ship To City',
       -- ship_to_state as 'Ship To Region',
       -- ship_to_zip as 'Ship To Zip Code',
       Open_Qty as 'Open Quantity',
       unit_price as 'Unit Net Price',
       extended_price as 'Extended Net Price',
       oh as 'O/H',
       alloc_qty as 'Total Alloc.',
       oo as 'O/O',
       serial_no as 'SerialNoProfile',
       end_user_po as 'End User PO'
  from tempdb.rds_final_14053
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;
