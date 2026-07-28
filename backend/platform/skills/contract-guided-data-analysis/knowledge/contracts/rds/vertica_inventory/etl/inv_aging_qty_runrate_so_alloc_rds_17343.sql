-- Typical Inventory example: aging/qty/runrate/SO allocation with location pivots.
-- Source: US/run/rds_17343_rtv.sp

drop table if exists table_us_sku_17343;

create local temporary table table_us_sku_17343 on commit preserve rows as
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

drop table if exists table_us_aging_17343;

create local temporary table table_us_aging_17343 on commit preserve rows as
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
  sum(isnull(c.qty240_up,0))  as qty_240_plus,
  sum(isnull(c.qty241_270,0)) as qty_241_270,
  sum(isnull(c.qty271_300,0)) as qty_271_300,
  sum(isnull(c.qty301_330,0)) as qty_301_330,
  sum(isnull(c.qty331_360,0)) as qty_331_360,
  sum(isnull(c.qty360_up,0))  as qty_360_plus
from table_us_sku_17343 a
left join dw_us.dwd_disty_inv_aging_df c on a.sku_no = c.sku_no and c.date_flag = current_date()-1 and c.inv_type in (1,300) and c.view_level = 'IT_PART'
group by
  a.sku_no
;

-- Runrate --DWS上以周六作为一周第一天，Vertica上是以周日第一天

drop table if exists table_us17343_max_week;
create local temporary table table_us17343_max_week on commit preserve rows as
select max(week) as max_week
from dw_us.dws_disty_pur_ips_runrate_1w
where sum_type = 'WITYPESTD'
and inv_type in (1,300)
;

drop table if exists table_us_runrate_17343;

create local temporary table table_us_runrate_17343 on commit preserve rows as
select
   a.sku_no
  ,sum(case when c.week=b.max_week then c.runrate_qty else 0 end) as wtd_qty
  ,sum(case when c.week=b.max_week-1 then c.runrate_qty else 0 end) as rr1_qty
  ,sum(case when c.week between b.max_week-2  and b.max_week-1 then c.runrate_qty else 0 end) as rr2_qty
  ,sum(case when c.week between b.max_week-4  and b.max_week-1 then c.runrate_qty else 0 end) as rr4_qty
  ,sum(case when c.week between b.max_week-10 and b.max_week-1 then c.runrate_qty else 0 end) as rr10_qty
from table_us_sku_17343 a
cross join table_us17343_max_week b
left join dw_us.dws_disty_pur_ips_runrate_1w c on b.max_week - 10 <= c.week and a.sku_no = c.sku_no and c.inv_type in (1, 300) and c.sum_type = 'WITYPESTD'
group by a.sku_no
;

drop table if exists table_us_inv_17343;

create local temporary table table_us_inv_17343 on commit preserve rows as
select
  a.vend_no,
  a.vpl_code,
  a.part_no,
  a.sku_no,
  a.base_cost,
  b.ave_cost,
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
  c.qty_241_270,
  c.qty_271_300,
  c.qty_301_330,
  c.qty_331_360,
  c.qty_360_plus,
  sum(isnull(b.on_hand_qty,0)) as oh,
  sum(isnull(b.on_order_qty,0)) as oo,
  sum(isnull(b.bo_qty,0)) as bo,
  sum(isnull(b.alloc_qty,0)) as alloc,
  sum(isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0)) as avail,
  sum(isnull(b.on_hand_qty,0)+isnull(b.intran_in,0)) as total,
  sum(isnull(b.on_hand_qty,0)+isnull(b.intran_in,0))*isnull(a.base_cost,0) as ext_amt,
  sum(isnull(b.on_hand_qty,0)) - sum(case when b.loc_no in (3,6,7,12,50,502,503,504,505,506) then isnull(b.on_hand_qty,0) else 0 end) as others_oh,
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
  d.rr10_qty,
  d.rr4_qty,
  d.rr2_qty,
  d.rr1_qty,
  d.wtd_qty,
  a.mfg_partno,
  a.pur_vend_name,
  a.vend_name,
  a.short_desc,
  a.mar_comment
from table_us_sku_17343 a
left join dw_us.dwd_disty_inv_qty_df b on a.sku_no = b.sku_no and b.date_flag = current_date()-1 and b.inv_type in (1,300)
left join table_us_aging_17343 c on a.sku_no = c.sku_no
left join table_us_runrate_17343 d on a.sku_no = d.sku_no
group by
  a.vend_no,
  a.vpl_code,
  a.part_no,
  a.sku_no,
  a.base_cost,
  b.ave_cost,
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
  c.qty_241_270,
  c.qty_271_300,
  c.qty_301_330,
  c.qty_331_360,
  c.qty_360_plus,
  d.rr10_qty,
  d.rr4_qty,
  d.rr2_qty,
  d.rr1_qty,
  d.wtd_qty,
  a.mfg_partno,
  a.pur_vend_name,
  a.vend_name,
  a.short_desc,
  a.mar_comment
;

drop table if exists rdsetl.rds_tmp;

create table rdsetl.rds_tmp as
select distinct
  a.vend_no as 'Vend#',
  a.vpl_code as 'VPC',
  a.part_no as 'Part#',
  a.sku_no as 'SKU#',
  a.base_cost as 'BaseCost($)',
  a.ave_cost as 'SysCost($)',
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
  a.qty_241_270 as '241-270',
  a.qty_271_300 as '271-300',
  a.qty_301_330 as '301-330',
  a.qty_331_360 as '331-360',
  a.qty_360_plus as '360+',

  a.oh as 'O/H',
  a.oo as 'O/O',
  a.bo as 'B/O',
  a.alloc as 'Alloc Qty',
  a.avail as 'Avail Qty',
  a.total as 'Total',
  a.ext_amt as 'Ext Amt($)',
  a.others_oh as 'Others-OH',
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
  a.rr10_qty as '10W',
  a.rr4_qty as '4W',
  a.rr2_qty as '2W',
  a.rr1_qty as '1W',
  a.wtd_qty as 'WTD',
  a.mfg_partno as 'MFGPart#',
  a.pur_vend_name as 'Pur Vend Name',
  a.vend_name as 'Vendor Name',
  a.short_desc as 'Short Desc',
  a.mar_comment as 'Mkting Comm'
from table_us_inv_17343 a
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
