drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists table_us_sku_18517;
create local temporary table table_us_sku_18517 on commit preserve rows as
select distinct
  sku_no,
  part_no,
  mfg_partno,
  po_cost as base_cost
from dim_us.dim_pub_part_info_rt
where vend_no = 69888
and mfg_partno in (
'VP0N3100',
'VP7541',
'VP9562',
'VP9563',
'VP9567',
'VP9571A',
'VA4N11A0',
'VA4N21A0',
'VP4N30AH',
'VP4N30AM',
'VP4N30AN',
'VP4N30AP',
'VP4N32A0',
'VP4N60AE',
'VP7N30AP',
'VP7N30AQ',
'VP7N31A1',
'VP7N32A0',
'VP5N11A0',
'VP5N20A4',
'VP5N21A1',
'VP5N30A5',
'VP5N30AU',
'VP5N31A0',
'VP5N31A1'
)
;

-- select * from table_us_sku_18517 where mfg_partno = 'VP0N3100'

drop table if exists table_us_inv_18517;
create local temporary table table_us_inv_18517 on commit preserve rows as
select
  a.sku_no,
  b.part_no,
  b.mfg_partno,
  ifnull(a.base_cost,0) as base_cost,
  sum(a.on_hand_qty) as on_hand_qty,
  sum(ifnull(a.base_cost,0) * a.on_hand_qty) as extended_oh,
  sum(a.on_order_qty) as on_order_qty,
  sum(ifnull(a.base_cost,0) * a.on_order_qty) as extended_oo
from dw_us.dwd_disty_inv_qty_df a
inner join table_us_sku_18517 b on a.sku_no = b.sku_no
where a.date_flag = current_date()-1
--and a.inv_type in (1,300)
group by
  a.sku_no,
  b.part_no,
  b.mfg_partno,
  ifnull(a.base_cost,0)
;

delete from table_us_inv_18517
where on_hand_qty = 0
and on_order_qty = 0
;

--select * from table_us_inv_18517 a where sku_no = 14575231 limit 1
--select * from dw_us.dwd_disty_inv_qty_df a where sku_no = 14575231 limit 1

drop table if exists table_us_qty_sold_18517;
create local temporary table table_us_qty_sold_18517 on commit preserve rows as
select
  a.sku_no,
  sum(ifnull(a.ship_qty,0)) as ytd_qty,
  sum(case when a.date_flag >= cast(timestampadd(mm, -1, trunc(timestampadd (dd, -1, getdate()), 'month')) as date)
           and a.date_flag < cast(trunc(getdate(), 'month') as date)
           then ifnull(a.ship_qty,0)
           else 0
      end) as prior_qty,
  sum(case when a.date_flag >= cast(trunc(timestampadd (dd, -1, getdate()), 'month') as date)
           and a.date_flag < current_date()
           then ifnull(a.ship_qty,0)
           else 0
      end) as mtd_qty
from dw_us.dwd_disty_common_pos_di a
inner join table_us_sku_18517 b on a.sku_no = b.sku_no
where a.date_flag >= cast(trunc(timestampadd (dd, -1, getdate()), 'year') as date)
and a.date_flag < current_date()
and a.order_line_type != 'Comp'
and a.order_type > 0
group by
  a.sku_no
;

drop table if exists table_us_open_ds_18517;
create local temporary table table_us_open_ds_18517 on commit preserve rows as
select
 a.sku_no,
 sum(a.open_qty) as open_qty
from dw_us.dwd_disty_common_po_basic a
where a.order_type = 2
and a.to_loc_no = 98
and a.delete_date is null
and a.line_delete_date is null
group by
 a.sku_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
  a.sku_no as 'SKU',
  a.part_no as 'Part#',
  a.mfg_partno as 'Vertiv SKU',
  a.base_cost as 'Curernt Base Cost',
  a.on_hand_qty as 'Stocking On Hand',
  a.extended_oh as 'OH $ Extended',
  a.on_order_qty as 'Stocking On Order',
  a.extended_oo as 'OO $ Extended',
  b.open_qty as 'Open Dropship QTY ',
  a.base_cost * b.open_qty as 'Open Dropship $ Extended',
  ifnull(c.prior_qty,0) as 'Prior Month Unit QTY Sold',
  ifnull(c.mtd_qty,0) as 'Current MTD Unit QTY Sold',
  ifnull(c.ytd_qty,0) as 'YTD QTY Sold '
from table_us_inv_18517 a
left join table_us_open_ds_18517 b on a.sku_no = b.sku_no
left join table_us_qty_sold_18517 c on a.sku_no = c.sku_no
order by a.mfg_partno
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;
