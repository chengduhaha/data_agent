drop table if exists table_us_sku_17484;
create local temporary table table_us_sku_17484 on commit preserve rows as
select distinct
  a.vend_no,
  a.vend_name,
  a.sku_no,
  a.vpl_code,
  a.part_no,
  a.mfg_partno,
  a.short_desc,
  isnull(a.po_cost,0) as base_cost
from dim_us.dim_pub_part_info a
left join dim_us.dim_pub_vendor_info_rt b on a.vend_no = b.vend_no
where a.vend_no in (13529, 74688, 70654, 75429, 61682, 55907)
and a.data_source = 'CIS'
;

drop table if exists table_us_aging_17484;
create local temporary table table_us_aging_17484 on commit preserve rows as
select
  a.sku_no,
  sum(isnull(c.age1_30,0))    as age_0_30,
  sum(isnull(c.age31_60,0))   as age_31_60,
  sum(isnull(c.age61_90,0))   as age_61_90,
  sum(isnull(c.age90_up,0))   as age_90_plus,
  sum(isnull(c.age91_120,0))  as age_91_120,
  sum(isnull(c.age121_150,0)) as age_121_150,
  sum(isnull(c.age151_180,0)) as age_151_180,
  sum(isnull(c.age181_210,0)) as age_181_210,
  sum(isnull(c.age211_240,0)) as age_211_240,
  sum(isnull(c.age240_up,0))  as age_240_plus,
  sum(isnull(c.age241_270,0)) as age_241_270,
  sum(isnull(c.age271_300,0)) as age_271_300,
  sum(isnull(c.age301_330,0)) as age_301_330,
  sum(isnull(c.age331_360,0)) as age_331_360,
  sum(isnull(c.age360_up,0))  as age_360_plus,
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
from table_us_sku_17484 a
left join dw_us.dwd_disty_inv_aging_df c
       on a.sku_no = c.sku_no
      and c.date_flag = current_date()-1
      and c.inv_type in (1,300)
      and c.view_level = 'IT_PART'
group by
  a.sku_no
;

drop table if exists table_us_inv_17484;
create local temporary table table_us_inv_17484 on commit preserve rows as
select
  a.vend_no,
  a.vend_name,
  a.vpl_code,
  a.mfg_partno,
  a.part_no,
  a.sku_no,
  a.base_cost,
  b.ave_cost,
  c.age_0_30,
  c.age_31_60,
  c.age_61_90,
  c.age_90_plus,
  c.age_91_120,
  c.age_121_150,
  c.age_151_180,
  c.age_181_210,
  c.age_211_240,
  c.age_240_plus,
  c.age_241_270,
  c.age_271_300,
  c.age_301_330,
  c.age_331_360,
  c.age_360_plus,
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
  sum(isnull(b.on_hand_qty,0)+isnull(b.intran_in,0))*isnull(a.base_cost,0) as ext_amt
from table_us_sku_17484 a
left join dw_us.dwd_disty_inv_qty_df b on a.sku_no = b.sku_no and b.date_flag = current_date()-1 and b.inv_type in (1,300)
left join table_us_aging_17484 c on a.sku_no = c.sku_no
group by
  a.vend_no,
  a.vend_name,
  a.vpl_code,
  a.mfg_partno,
  a.part_no,
  a.sku_no,
  a.base_cost,
  b.ave_cost,
  c.age_0_30,
  c.age_31_60,
  c.age_61_90,
  c.age_90_plus,
  c.age_91_120,
  c.age_121_150,
  c.age_151_180,
  c.age_181_210,
  c.age_211_240,
  c.age_240_plus,
  c.age_241_270,
  c.age_271_300,
  c.age_301_330,
  c.age_331_360,
  c.age_360_plus,
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
  c.qty_360_plus
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
  0 as id,
  cast('All Vendors' as varchar(80)) as name,
  a.vend_no,
  a.vend_name,
  a.vpl_code,
  a.mfg_partno,
  a.base_cost,
  a.qty_0_30,
  a.qty_31_60,
  a.qty_61_90,
  a.qty_90_plus,
  a.qty_91_120,
  a.qty_121_150,
  a.qty_151_180,
  a.qty_181_210,
  a.qty_211_240,
  a.qty_240_plus,
  a.qty_241_270,
  a.qty_271_300,
  a.qty_301_330,
  a.qty_331_360,
  a.qty_360_plus,
  a.age_0_30,
  a.age_31_60,
  a.age_61_90,
  a.age_90_plus,
  a.age_91_120,
  a.age_121_150,
  a.age_151_180,
  a.age_181_210,
  a.age_211_240,
  a.age_240_plus,
  a.age_241_270,
  a.age_271_300,
  a.age_301_330,
  a.age_331_360,
  a.age_360_plus,
  a.oh,
  a.oo,
  a.bo,
  a.alloc,
  a.avail,
  a.total,
  a.ext_amt
from table_us_inv_17484 a
order by
  a.vend_no,
  a.vend_name,
  a.vpl_code,
  a.total desc
;

insert into rdsetl.rds_tmp
select
  a.vend_no as id,
  a.vend_name as name,
  a.vend_no,
  a.vend_name,
  a.vpl_code,
  a.mfg_partno,
  a.base_cost,
  a.qty_0_30,
  a.qty_31_60,
  a.qty_61_90,
  a.qty_90_plus,
  a.qty_91_120,
  a.qty_121_150,
  a.qty_151_180,
  a.qty_181_210,
  a.qty_211_240,
  a.qty_240_plus,
  a.qty_241_270,
  a.qty_271_300,
  a.qty_301_330,
  a.qty_331_360,
  a.qty_360_plus,
  a.age_0_30,
  a.age_31_60,
  a.age_61_90,
  a.age_90_plus,
  a.age_91_120,
  a.age_121_150,
  a.age_151_180,
  a.age_181_210,
  a.age_211_240,
  a.age_240_plus,
  a.age_241_270,
  a.age_271_300,
  a.age_301_330,
  a.age_331_360,
  a.age_360_plus,
  a.oh,
  a.oo,
  a.bo,
  a.alloc,
  a.avail,
  a.total,
  a.ext_amt
from table_us_inv_17484 a
order by
  a.vend_no,
  a.vend_name,
  a.vpl_code,
  a.total desc
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,id
    ,'Standard' as body_type
    ,count(*) as cnt
    ,name as sub_name
from rdsetl.rds_tmp
group by id, name
;
