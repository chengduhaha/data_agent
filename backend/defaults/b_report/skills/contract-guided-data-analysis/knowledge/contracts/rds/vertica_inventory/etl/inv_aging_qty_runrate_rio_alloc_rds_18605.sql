drop table if exists table_us_sku_18605;
create local temporary table table_us_sku_18605 on commit preserve rows as
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
  a.long_desc,
  a.mar_comment,
  isnull(a.po_cost,0) as base_cost
from dim_us.dim_pub_part_info a
left join dim_us.dim_pub_vendor_info_rt b on a.vend_no = b.vend_no
where a.vend_no in (81051)
and a.data_source = 'CIS'
;

drop table if exists table_us_aging_18605;
create local temporary table table_us_aging_18605 on commit preserve rows as
select
  a.sku_no,
  c.inv_type,
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
from table_us_sku_18605 a
inner join dw_us.dwd_disty_inv_aging_df c on a.sku_no = c.sku_no and c.date_flag = current_date()-1 and c.inv_type in (1,300) and c.view_level = 'IT_PART'
group by
  a.sku_no,
  c.inv_type
;

-- Runrate --DWS上以周六作为一周第一天，Vertica上是以周日第一天

drop table if exists table_us18605_max_week;
create local temporary table table_us18605_max_week on commit preserve rows as
select max(week) as max_week
from dw_us.dws_disty_pur_ips_runrate_1w
where sum_type = 'WITYPESTD'
and inv_type in (1,300)
;

drop table if exists table_us_runrate_18605;
create local temporary table table_us_runrate_18605 on commit preserve rows as
select
   a.sku_no
  ,c.inv_type
  ,sum(case when c.week=b.max_week then c.runrate_qty else 0 end) as wtd_qty
  ,sum(case when c.week=b.max_week-1 then c.runrate_qty else 0 end) as rr1_qty
  ,sum(case when c.week between b.max_week-2  and b.max_week-1 then c.runrate_qty else 0 end) as rr2_qty
  ,sum(case when c.week between b.max_week-4  and b.max_week-1 then c.runrate_qty else 0 end) as rr4_qty
  ,sum(case when c.week between b.max_week-10 and b.max_week-1 then c.runrate_qty else 0 end) as rr10_qty
from table_us_sku_18605 a
cross join table_us18605_max_week b
inner join dw_us.dws_disty_pur_ips_runrate_1w c on b.max_week - 10 <= c.week and a.sku_no = c.sku_no and c.inv_type in (1, 300) and c.sum_type = 'WITYPESTD'
group by a.sku_no, c.inv_type
;

drop table if exists table_us_alloc_qty_18605;
create local temporary table table_us_alloc_qty_18605 on commit preserve rows as
select
   ril.sku_no
  ,ril.inv_type
  ,sum(ril.alloc_so) as alloc_so
  ,sum(ril.alloc_rio) as alloc_rio
  ,sum(ril.alloc_kwo) as alloc_kwo
  ,sum(ril.avail_qty) as avail_qty
  ,sum(ril.rio_qty) as rio_qty
from dm_us.dm_disty_sales_rio_sku_inv_loc ril
inner join table_us_sku_18605 part on ril.sku_no = part.sku_no
where ril.prod_type = 'K'
and ril.bundle_kit = 'Y'
group by
   ril.sku_no
  ,ril.inv_type
union
select
   ril.sku_no
  ,ril.inv_type
  ,sum(ril.alloc_so) as alloc_so
  ,sum(ril.alloc_rio) as alloc_rio
  ,sum(ril.alloc_kwo) as alloc_kwo
  ,sum(ril.avail_qty) as avail_qty
  ,sum(ril.rio_qty) as rio_qty
from dm_us.dm_disty_sales_rio_sku_inv_loc ril
inner join table_us_sku_18605 part on ril.sku_no = part.sku_no
where ril.prod_type = 'S'
and ril.bundle_kit is null
group by
   ril.sku_no
  ,ril.inv_type
;

drop table if exists table_us_inv_qty_temp_18605;
create local temporary table table_us_inv_qty_temp_18605 on commit preserve rows as
select
  b.sku_no,
  b.ave_cost,
  a.base_cost,
  a.vend_no,
  a.vpl_code,
  a.part_no,
  a.mfg_partno,
  a.pur_vend_name,
  a.vend_name,
  a.short_desc,
  a.long_desc,
  a.mar_comment,
  b.inv_type,
  sum(isnull(b.on_hand_qty,0)) as oh,
  sum(isnull(b.on_order_qty,0)) as oo,
  sum(isnull(b.bo_qty,0)) as bo,
  sum(isnull(b.alloc_qty,0)) as alloc,
  sum(isnull(b.intran_in,0)) as it,
  sum(isnull(b.wip_qty,0)) as wip_qty,
  sum(isnull(b.on_hand_qty,0)-isnull(b.bo_qty,0)+isnull(b.intran_in,0)-isnull(b.intran_out,0)-isnull(b.alloc_qty,0)) as avail,
  sum(isnull(b.on_hand_qty,0)+isnull(b.intran_in,0)) as total,
  sum(isnull(b.on_hand_qty,0)+isnull(b.intran_in,0))*isnull(a.base_cost,0) as ext_amt,
  sum(isnull(b.on_hand_qty,0)) - sum(case when b.loc_no in (3,6,7,12,16,50,502,503,504,505,506) then isnull(b.on_hand_qty,0) else 0 end) as others_oh,
  sum(case when b.loc_no = 3   then isnull(b.on_hand_qty,0) else 0 end)  as DFR_oh,
  sum(case when b.loc_no = 6   then isnull(b.on_hand_qty,0) else 0 end)  as DCH_oh,
  sum(case when b.loc_no = 7   then isnull(b.on_hand_qty,0) else 0 end)  as DTN_oh,
  sum(case when b.loc_no = 12  then isnull(b.on_hand_qty,0) else 0 end)  as DON_oh,
  sum(case when b.loc_no = 16  then isnull(b.on_hand_qty,0) else 0 end)  as DFL_oh,
  sum(case when b.loc_no = 50  then isnull(b.on_hand_qty,0) else 0 end)  as DCO_oh,
  sum(case when b.loc_no = 502 then isnull(b.on_hand_qty,0) else 0 end)  as DGA_oh,
  sum(case when b.loc_no = 503 then isnull(b.on_hand_qty,0) else 0 end)  as DSW_oh,
  sum(case when b.loc_no = 504 then isnull(b.on_hand_qty,0) else 0 end)  as DIN_oh,
  sum(case when b.loc_no = 505 then isnull(b.on_hand_qty,0) else 0 end)  as DFW_oh,
  sum(case when b.loc_no = 506 then isnull(b.on_hand_qty,0) else 0 end)  as DFO_oh
from table_us_sku_18605 a
inner join dw_us.dwd_disty_inv_qty_df b on a.sku_no = b.sku_no and b.date_flag = current_date()-1 and b.inv_type in (1,300)
group by
  b.sku_no,
  b.ave_cost,
  a.base_cost,
  a.vend_no,
  a.vpl_code,
  a.part_no,
  a.mfg_partno,
  a.pur_vend_name,
  a.vend_name,
  a.short_desc,
  a.long_desc,
  a.mar_comment,
  b.inv_type
;

drop table if exists table_us_inv_qty_18605;
create local temporary table table_us_inv_qty_18605 on commit preserve rows as
select distinct
  a.sku_no,
  a.ave_cost,
  a.base_cost,
  a.vend_no,
  a.vpl_code,
  a.part_no,
  a.mfg_partno,
  a.pur_vend_name,
  a.vend_name,
  a.short_desc,
  a.long_desc,
  a.mar_comment,
  a.inv_type,
  a.oh,
  a.oo,
  a.bo,
  case when b.sku_no is not null then ifnull(b.alloc_kwo,0) + ifnull(b.alloc_rio,0) + ifnull(b.alloc_so,0) else a.alloc end as alloc_qty,
  ifnull(b.alloc_rio, 0) as alloc_rio,
  ifnull(b.alloc_kwo, 0) as alloc_kwo,
  ifnull(b.alloc_so, 0) as alloc_so,
  a.it,
  a.wip_qty,
  case when b.sku_no is not null then b.avail_qty else a.avail end as avail_qty,
  a.total,
  a.ext_amt,
  a.others_oh,
  a.DFR_oh,
  a.DCH_oh,
  a.DTN_oh,
  a.DON_oh,
  a.DFL_oh,
  a.DCO_oh,
  a.DGA_oh,
  a.DSW_oh,
  a.DIN_oh,
  a.DFW_oh,
  a.DFO_oh
from table_us_inv_qty_temp_18605 a
left join table_us_alloc_qty_18605 b on a.sku_no = b.sku_no and a.inv_type = b.inv_type
;

-- select * from table_us_inv_qty_18605 where sku_no = 13580143

drop table if exists table_us_report_18605;
create local temporary table table_us_report_18605 on commit preserve rows as
select
  b.vend_no,
  b.inv_type,
  b.vpl_code,
  b.part_no,
  b.sku_no,
  b.base_cost,
  b.ave_cost,
  ifnull(c.qty_0_30,0) as qty_0_30,
  ifnull(c.qty_31_60,0) as qty_31_60,
  ifnull(c.qty_61_90,0) as qty_61_90,
  ifnull(c.qty_90_plus,0) as qty_90_plus,
  ifnull(c.qty_91_120,0) as qty_91_120,
  ifnull(c.qty_121_150,0) as qty_121_150,
  ifnull(c.qty_151_180,0) as qty_151_180,
  ifnull(c.qty_181_210,0) as qty_181_210,
  ifnull(c.qty_211_240,0) as qty_211_240,
  ifnull(c.qty_240_plus,0) as qty_240_plus,
  ifnull(c.qty_241_270,0) as qty_241_270,
  ifnull(c.qty_271_300,0) as qty_271_300,
  ifnull(c.qty_301_330,0) as qty_301_330,
  ifnull(c.qty_331_360,0) as qty_331_360,
  ifnull(c.qty_360_plus,0) as qty_360_plus,
  b.oh,
  b.oo,
  b.bo,
  b.alloc_qty,
  b.alloc_rio,
  b.alloc_kwo,
  b.alloc_so,
  b.it,
  b.wip_qty,
  b.avail_qty,
  b.total,
  b.ext_amt,
  b.others_oh,
  b.DFR_oh,
  b.DCH_oh,
  b.DTN_oh,
  b.DON_oh,
  b.DFL_oh,
  b.DCO_oh,
  b.DGA_oh,
  b.DSW_oh,
  b.DIN_oh,
  b.DFW_oh,
  b.DFO_oh,
  ifnull(d.rr10_qty,0) as rr10_qty,
  ifnull(d.rr4_qty,0) as rr4_qty,
  ifnull(d.rr2_qty,0) as rr2_qty,
  ifnull(d.rr1_qty,0) as rr1_qty,
  ifnull(d.wtd_qty,0) as wtd_qty,
  b.mfg_partno,
  b.pur_vend_name,
  b.vend_name,
  b.short_desc,
  b.long_desc,
  b.mar_comment
from table_us_inv_qty_18605 b
left join table_us_aging_18605 c on b.sku_no = c.sku_no and b.inv_type = c.inv_type
left join table_us_runrate_18605 d on b.sku_no = d.sku_no and b.inv_type = d.inv_type
;

--select count(*) from table_us_sku_18605

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select distinct
  a.vend_no as 'Vend#',
  a.vpl_code as 'VPC',
  a.part_no as 'Part#',
  a.sku_no as 'SKU#',
  a.inv_type as 'InvType',
  a.oh as 'O/H',
  a.oo as 'O/O',
  a.bo as 'B/O',
  a.alloc_qty as 'Alloc Qty',
  a.alloc_rio as 'RIO Qty',
  a.alloc_kwo as 'KWO Alloc Qty',
  a.alloc_so as 'SO Alloc Qty',
  a.it as 'I/T',
  a.wtd_qty as 'WTD',
  a.avail_qty as 'Avail Qty',
  a.total as 'Total',
  a.ext_amt as 'Ext Amt($)',
  a.DFL_oh as '16-DFL_OH',
  a.DGA_oh as '502-DGA-OH',
  a.DFW_oh as '505-DFW-OH',
  a.rr10_qty as '10W',
  a.rr4_qty as '4W',
  a.mfg_partno as 'MFGPart#',
  a.vend_name as 'Vendor Name',
  a.long_desc as 'Long Desc'
from table_us_report_18605 a
order by
  a.vpl_code,
  a.sku_no desc
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

drop table if exists table_us_sku_18605;
drop table if exists table_us_aging_18605;
drop table if exists table_us18605_max_week;
drop table if exists table_us_runrate_18605;
drop table if exists table_us_alloc_qty_18605;
drop table if exists table_us_inv_qty_temp_18605;
drop table if exists table_us_inv_qty_18605;
drop table if exists table_us_report_18605;
