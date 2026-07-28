drop table if exists table_us_sku_17345;

create local temporary table table_us_sku_17345 on commit preserve rows as
select distinct
  a.vend_no,
  a.vend_name,
  isnull(b.pur_vend_no,b.vend_no) as  pur_vend_no,
  isnull(b.pur_vend_name,b.vend_name) as pur_vend_name,
  a.sku_no,
  a.vpl_code,
  a.part_no,
  a.mfg_partno,
  a.short_desc,
  a.mar_comment,
  isnull(a.po_cost,0) as base_cost
from dim_us.dim_pub_part_info a
left join dim_us.dim_pub_vendor_info_rt b on a.vend_no = b.vend_no
where a.vend_no in (18549, 69632)
and a.data_source = 'CIS'
-- and a.sku_no = 5334044
;

drop table if exists table_us_aging_17345;

create local temporary table table_us_aging_17345 on commit preserve rows as
select
  a.sku_no,
  sum(isnull(c.qty1_30,0))    as qty_0_30,
  sum(isnull(c.qty31_60,0))   as qty_31_60,
  sum(isnull(c.qty61_90,0))   as qty_61_90,
  sum(isnull(c.qty90_up,0))   as qty_90_plus,
  sum(isnull(c.qty91_120,0))  as qty_91_120,
  sum(isnull(c.qty121_150,0)) as qty_121_150,
  sum(isnull(c.qty151_180,0)) as qty_151_180,
  sum(isnull(c.qty181_210,0)) as qty_181_210,
  sum(isnull(c.qty211_240,0)) as qty_211_240,
  sum(isnull(c.qty240_up,0))  as qty_240_plus
from table_us_sku_17345 a
left join dw_us.dwd_disty_inv_aging_df c on a.sku_no = c.sku_no and c.date_flag = current_date()-1 and c.inv_type in (1,300) and c.view_level = 'IT_PART'
group by
  a.sku_no
;

-- Runrate --DWS上以周六作为一周第一天，Vertica上是以周日第一天

drop table if exists table_us17345_max_week;

create local temporary table table_us17345_max_week on commit preserve rows as
select max(week) as max_week
from dw_us.dws_disty_pur_ips_runrate_1w
where sum_type = 'WITYPESTD'
and inv_type in (1,300)
;

drop table if exists table_us_runrate_17345;

create local temporary table table_us_runrate_17345 on commit preserve rows as
select
   a.sku_no
  ,sum(case when c.week=b.max_week then c.runrate_qty else 0 end) as wtd_qty
  ,sum(case when c.week=b.max_week-1 then c.runrate_qty else 0 end) as rr1_qty
  ,sum(case when c.week between b.max_week-2  and b.max_week-1 then c.runrate_qty else 0 end) as rr2_qty
  ,sum(case when c.week between b.max_week-4  and b.max_week-1 then c.runrate_qty else 0 end) as rr4_qty
  ,sum(case when c.week between b.max_week-10 and b.max_week-1 then c.runrate_qty else 0 end) as rr10_qty
from table_us_sku_17345 a
cross join table_us17345_max_week b
left join dw_us.dws_disty_pur_ips_runrate_1w c on b.max_week - 10 <= c.week and a.sku_no = c.sku_no and c.inv_type in (1, 300) and c.sum_type = 'WITYPESTD'
group by a.sku_no
;

drop table if exists table_us_so_alloc_qty_17345;

create local temporary table table_us_so_alloc_qty_17345 on commit preserve rows as
select
   a.sku_no
  -- ,b.from_loc_no
  -- ,b.from_inv_type
  ,sum(isnull(b.order_qty, 0) - isnull(b.ship_qty, 0)) as so_alloc_qty
from table_us_sku_17345 a
inner join dw_us.dwd_disty_sales_open_order_detail b on a.sku_no = b.sku_no
where b.ship_date is null
and b.order_type in (1,10,11)
and b.from_inv_type in (1,300)
group by
   a.sku_no
  -- ,b.from_loc_no
  -- ,b.from_inv_type
;

drop table if exists table_us_inv_17345;

create local temporary table table_us_inv_17345 on commit preserve rows as
select
  a.vend_no,
  a.vpl_code,
  a.mfg_partno,
  a.sku_no,
  a.base_cost,
  c.qty_0_30,
  c.qty_31_60,
  c.qty_61_90,
  c.qty_90_plus,
  c.qty_91_120,
  c.qty_121_150,
  c.qty_151_180,
  c.qty_181_210,
  c.qty_211_240,
  c.qty_240_plus,
  sum(isnull(b.on_hand_qty,0)) as oh,
  sum(isnull(b.on_order_qty,0)) as oo,
  sum(isnull(b.bo_qty,0)) as bo,
  sum(isnull(b.alloc_qty,0)) as alloc,
  sum(isnull(b.rio_qty,0)) as rio_qty,
  e.so_alloc_qty,
  sum(isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0)) as avail_qty,
  sum(isnull(b.on_hand_qty,0)+isnull(b.intran_in,0)) as total,
  sum(case when b.loc_no = 3   then isnull(b.on_hand_qty,0) else 0 end)  as DFR_oh,
  sum(case when b.loc_no = 6   then isnull(b.on_hand_qty,0) else 0 end)  as DCH_oh,
  sum(case when b.loc_no = 7   then isnull(b.on_hand_qty,0) else 0 end)  as DTN_oh,
  sum(case when b.loc_no = 12  then isnull(b.on_hand_qty,0) else 0 end)  as DON_oh,
  sum(case when b.loc_no = 50  then isnull(b.on_hand_qty,0) else 0 end)  as DCO_oh,
  sum(case when b.loc_no = 502 then isnull(b.on_hand_qty,0) else 0 end)  as DGA_oh,
  sum(case when b.loc_no = 503 then isnull(b.on_hand_qty,0) else 0 end)  as DSW_oh,
  sum(case when b.loc_no = 504 then isnull(b.on_hand_qty,0) else 0 end)  as DIN_oh,
  sum(case when b.loc_no = 505 then isnull(b.on_hand_qty,0) else 0 end)  as DFW_oh,
  sum(case when b.loc_no = 506 then isnull(b.on_hand_qty,0) else 0 end)  as DFO_oh,
  sum(case when b.loc_no = 3   then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DFR_avail,
  sum(case when b.loc_no = 6   then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DCH_avail,
  sum(case when b.loc_no = 7   then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DTN_avail,
  sum(case when b.loc_no = 12  then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DON_avail,
  sum(case when b.loc_no = 50  then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DCO_avail,
  sum(case when b.loc_no = 502 then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DGA_avail,
  sum(case when b.loc_no = 503 then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DSW_avail,
  sum(case when b.loc_no = 504 then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DIN_avail,
  sum(case when b.loc_no = 505 then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DFW_avail,
  sum(case when b.loc_no = 506 then isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0) else 0 end)  as DFO_avail,
  d.rr10_qty,
  d.rr4_qty,
  d.rr2_qty,
  a.vend_name,
  a.short_desc
from table_us_sku_17345 a
left join dw_us.dwd_disty_inv_qty_df b on a.sku_no = b.sku_no and b.date_flag = current_date()-1 and b.inv_type in (1,300)
left join table_us_aging_17345 c on a.sku_no = c.sku_no
left join table_us_runrate_17345 d on a.sku_no = d.sku_no
left join table_us_so_alloc_qty_17345 e on a.sku_no = e.sku_no
group by
  a.vend_no,
  a.vpl_code,
  a.mfg_partno,
  a.sku_no,
  a.base_cost,
  c.qty_0_30,
  c.qty_31_60,
  c.qty_61_90,
  c.qty_90_plus,
  c.qty_91_120,
  c.qty_121_150,
  c.qty_151_180,
  c.qty_181_210,
  c.qty_211_240,
  c.qty_240_plus,
  e.so_alloc_qty,
  d.rr10_qty,
  d.rr4_qty,
  d.rr2_qty,
  a.vend_name,
  a.short_desc
;

drop table if exists rdsetl.rds_tmp;

create table rdsetl.rds_tmp as
select distinct
  a.vend_no as 'Vend#',
  a.vpl_code as 'VPC',
  a.mfg_partno as 'MFGPart#',
  a.sku_no as 'SKU#',
  a.base_cost as 'BaseCost($)',
  a.qty_0_30 as '0-30',
  a.qty_31_60 as '31-60',
  a.qty_61_90 as '61-90',
  a.qty_90_plus as '90+',
  a.qty_91_120 as '91-120',
  a.qty_121_150 as '121-150',
  a.qty_151_180 as '151-180',
  a.qty_181_210 as '181-210',
  a.qty_211_240 as '211-240',
  a.qty_240_plus as '241+',
  a.oh as 'O/H',
  a.oo as 'O/O',
  a.bo as 'B/O',
  a.alloc as 'AllocQty',
  a.rio_qty as 'RIOQty',
  a.so_alloc_qty as 'SO AllocQty',
  a.avail_qty as 'Avail Qty',
  a.total as 'Total',
  a.DFR_oh as '3-DFR-OH',
  a.DCH_oh as '6-DCH-OH',
  a.DTN_oh as '7-DTN-OH',
  a.DON_oh as '12-DON-OH',
  a.DCO_oh as '50-DCO-OH',
  a.DGA_oh as '502-DGA-OH',
  a.DSW_oh as '503-DSW-OH',
  a.DIN_oh as '504-DIN-OH',
  a.DFW_oh as '505-DFW-OH',
  a.DFO_oh as '506-DFO-OH',
  a.DFR_avail as '3-DFR-Avail',
  a.DCH_avail as '6-DCH-Avail',
  a.DTN_avail as '7-DTN-Avail',
  a.DON_avail as '12-DON-Avail',
  a.DCO_avail as '50-DCO-Avail',
  a.DGA_avail as '502-DGA-Avail',
  a.DSW_avail as '503-DSW-Avail',
  a.DIN_avail as '504-DIN-Avail',
  a.DFW_avail as '505-DFW-Avail',
  a.DFO_avail as '506-DFO-Avail',
  a.rr10_qty as '10W',
  a.rr4_qty as '4W',
  a.rr2_qty as '2W',
  a.vend_name as 'Vendor Name',
  a.short_desc as 'Short Desc'
from table_us_inv_17345 a
order by
  a.vend_no,
  a.vpl_code,
  a.total desc
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

drop table if exists table_us_sku_17345;
drop table if exists table_us_aging_17345;
drop table if exists table_us17345_max_week;
drop table if exists table_us_runrate_17345;
drop table if exists table_us_so_alloc_qty_17345;
drop table if exists table_us_inv_17345;
