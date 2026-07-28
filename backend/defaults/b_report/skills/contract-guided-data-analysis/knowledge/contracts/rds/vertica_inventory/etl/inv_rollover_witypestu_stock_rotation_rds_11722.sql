set time zone='America/Los_Angeles';

drop table if exists dates_us11722;
create local temporary table dates_us11722 on commit preserve rows as
select
    (select w from dim_us.dim_pub_date where date_flag = current_date() - 1 limit 1) as w_y
    ,(select m from dim_us.dim_pub_date where date_flag = current_date() limit 1) as m_t
    ,current_date() - 2 as rollover_date_flag
;

drop table if exists win_us11722;
create local temporary table win_us11722 on commit preserve rows as
select
    (select min(cal.date_flag) from dim_us.dim_pub_date cal where cal.w = (select w_y from dates_us11722 limit 1) - 4) as d_4w_begin
    ,(select min(cal.date_flag) from dim_us.dim_pub_date cal where cal.w = (select w_y from dates_us11722 limit 1)) as d_4w_end
    ,(select min(cal.date_flag) from dim_us.dim_pub_date cal where cal.w = (select w_y from dates_us11722 limit 1) - 13) as d_13w_begin
    ,(select min(cal.date_flag) from dim_us.dim_pub_date cal where cal.m = (select m_t from dates_us11722 limit 1)) as d_mtd_begin
    ,(select min(cal.date_flag) from dim_us.dim_pub_date cal where cal.m = (select m_t from dates_us11722 limit 1) - 1) as d_pmon_begin
    ,(select min(cal.date_flag) from dim_us.dim_pub_date cal where cal.m = (select m_t from dates_us11722 limit 1) - 2) as d_ppmon_begin
;

drop table if exists t_vpl_us11722;
-- Sybase #t_vpl_11722: CIS..part_master where vend_no > 0 only (no active_status filter). Match that grain so #t_res / final row counts align.
create local temporary table t_vpl_us11722 on commit preserve rows as
select
    a.vend_no as vend_no
    ,a.prod_code as prod_code
    ,a.vpl_no as vpl_no
    ,count(*) as cnt
from dim_us.dim_pub_part_info a
where a.vend_no > 0
group by
    a.vend_no
    ,a.prod_code
    ,a.vpl_no
;

drop table if exists t_res_us11722;
create local temporary table t_res_us11722 on commit preserve rows as
select
    a.vend_no as vend_no
    ,a.prod_code as prod_code
    ,a.vpl_no as vpl_no
    ,cast(null as numeric(19, 4)) as oh
    ,cast(null as numeric(19, 4)) as it
    ,cast(null as numeric(19, 4)) as oo
    ,cast(null as numeric(19, 4)) as bo
    ,cast(null as numeric(19, 4)) as age30
    ,cast(null as numeric(19, 4)) as age60
    ,cast(null as numeric(19, 4)) as age90
    ,cast(null as numeric(19, 4)) as age90p
    ,cast(null as numeric(19, 4)) as age120
    ,cast(null as numeric(19, 4)) as age150
    ,cast(null as numeric(19, 4)) as age180
    ,cast(null as numeric(19, 4)) as age210
    ,cast(null as numeric(19, 4)) as age240
    ,cast(null as numeric(19, 4)) as age270
    ,cast(null as numeric(19, 4)) as age300
    ,cast(null as numeric(19, 4)) as age330
    ,cast(null as numeric(19, 4)) as age360
    ,cast(null as numeric(19, 4)) as age360p
    ,cast(null as numeric(19, 4)) as ppmon_reg
    ,cast(null as numeric(19, 4)) as ppmon_ds
    ,cast(null as numeric(19, 4)) as ppmon_all
    ,cast(null as numeric(19, 4)) as pmon_reg
    ,cast(null as numeric(19, 4)) as pmon_ds
    ,cast(null as numeric(19, 4)) as pmon_all
    ,cast(null as numeric(19, 4)) as mtd_reg
    ,cast(null as numeric(19, 4)) as mtd_ds
    ,cast(null as numeric(19, 4)) as mtd_all
    ,cast(null as numeric(19, 4)) as s4w_reg
    ,cast(null as numeric(19, 4)) as s4w_ds
    ,cast(null as numeric(19, 4)) as s13w_reg
    ,cast(null as numeric(19, 4)) as s13w_ds
    ,cast(null as numeric(19, 4)) as ap_ttl
    ,cast(null as numeric(19, 4)) as rec_mtd
    ,cast(null as numeric(19, 4)) as so_alo_amt
    ,cast(null as numeric(19, 4)) as age90roll_amt
    ,cast(null as numeric(19, 4)) as monroll_amt
    ,cast(null as numeric(19, 4)) as wr_amt
from t_vpl_us11722 a
inner join dim_us.dim_pub_vendor_info b
    on a.vend_no = b.vend_no
where b.discontinued in ('N', 'n')
;

drop table if exists t_inv_us11722;
create local temporary table t_inv_us11722 on commit preserve rows as
select
    b.prod_code as prod_code
    ,b.vpl_no as vpl_no
    ,sum(ifnull(a.on_order_qty, 0) * ifnull(a.ave_cost, 0)) as oo
    ,sum(ifnull(a.bo_qty, 0) * ifnull(a.ave_cost, 0)) as bo
from dw_us.dwd_disty_inv_qty_df a
inner join dim_us.dim_pub_part_info b
    on a.sku_no = b.sku_no
where a.date_flag = current_date() - 1
    and a.inv_type in (1, 32, 300)
    and abs(ifnull(a.on_order_qty, 0)) + abs(ifnull(a.bo_qty, 0)) > 0
group by
    b.prod_code
    ,b.vpl_no
;

update t_res_us11722 a
set
    oo = b.oo
    ,bo = b.bo
from t_inv_us11722 b
where a.prod_code = b.prod_code
    and a.vpl_no = b.vpl_no
;

drop table if exists t_aging_us11722;
create local temporary table t_aging_us11722 on commit preserve rows as
select
    b.prod_code as prod_code
    ,b.vpl_no as vpl_no
    ,sum(ifnull(a.on_hand_qty, 0) * ifnull(a.ave_cost, 0)) as oh
    ,sum(ifnull(a.intran_in, 0) * ifnull(a.ave_cost, 0)) as it
    ,sum(ifnull(a.age1_30, 0)) as age30
    ,sum(ifnull(a.age31_60, 0)) as age60
    ,sum(ifnull(a.age61_90, 0)) as age90
    ,sum(ifnull(a.age90_up, 0)) as age90p
    ,sum(ifnull(a.age91_120, 0)) as age120
    ,sum(ifnull(a.age121_150, 0)) as age150
    ,sum(ifnull(a.age151_180, 0)) as age180
    ,sum(ifnull(a.age181_210, 0)) as age210
    ,sum(ifnull(a.age211_240, 0)) as age240
    ,sum(ifnull(a.age241_270, 0)) as age270
    ,sum(ifnull(a.age271_300, 0)) as age300
    ,sum(ifnull(a.age301_330, 0)) as age330
    ,sum(ifnull(a.age331_360, 0)) as age360
    ,sum(ifnull(a.age360_up, 0)) as age360p
from dw_us.dwd_disty_inv_aging_df a
inner join dim_us.dim_pub_part_info b
    on a.sku_no = b.sku_no
where a.date_flag = current_date() - 1
    and a.inv_type in (1, 7, 32, 300)
    and a.view_level = 'IT_PART'
group by
    b.prod_code
    ,b.vpl_no
;

update t_res_us11722 a
set
    oh = b.oh
    ,it = b.it
    ,age30 = b.age30
    ,age60 = b.age60
    ,age90 = b.age90
    ,age90p = b.age90p
    ,age120 = b.age120
    ,age150 = b.age150
    ,age180 = b.age180
    ,age210 = b.age210
    ,age240 = b.age240
    ,age270 = b.age270
    ,age300 = b.age300
    ,age330 = b.age330
    ,age360 = b.age360
    ,age360p = b.age360p
from t_aging_us11722 b
where a.prod_code = b.prod_code
    and a.vpl_no = b.vpl_no
;

drop table if exists t_sales_us11722;
create local temporary table t_sales_us11722 (
    sku_no int
    ,active_status varchar(20)
    ,vend_no int
    ,prod_code int
    ,vpl_no int
    ,s4w_reg numeric(19, 4)
    ,s4w_ds numeric(19, 4)
    ,s4w_all numeric(19, 4)
    ,s13w_reg numeric(19, 4)
    ,s13w_ds numeric(19, 4)
    ,s13w_all numeric(19, 4)
    ,pmon_reg numeric(19, 4)
    ,pmon_ds numeric(19, 4)
    ,pmon_all numeric(19, 4)
    ,ppmon_reg numeric(19, 4)
    ,ppmon_ds numeric(19, 4)
    ,ppmon_all numeric(19, 4)
    ,mtd_reg numeric(19, 4)
    ,mtd_ds numeric(19, 4)
    ,mtd_all numeric(19, 4)
) on commit preserve rows
;
-- t_sales_us11722: inv_type (1, 7, 32, 100, 200, 300) matches Sybase v_comp_orders in rds_11722.
insert into t_sales_us11722
select
    a.sku_no as sku_no
    ,cast(null as varchar(20)) as active_status
    ,a.vend_no as vend_no
    ,cast(null as int) as prod_code
    ,cast(null as int) as vpl_no
    ,sum(
        case
            when a.date_flag >= w.d_4w_begin
                and a.date_flag < w.d_4w_end
                and a.from_loc_no <> 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as s4w_reg
    ,sum(
        case
            when a.date_flag >= w.d_4w_begin
                and a.date_flag < w.d_4w_end
                and a.from_loc_no = 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as s4w_ds
    ,sum(
        case
            when a.date_flag >= w.d_4w_begin
                and a.date_flag < w.d_4w_end
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as s4w_all
    ,sum(
        case
            when a.date_flag >= w.d_13w_begin
                and a.date_flag < w.d_4w_end
                and a.from_loc_no <> 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as s13w_reg
    ,sum(
        case
            when a.date_flag >= w.d_13w_begin
                and a.date_flag < w.d_4w_end
                and a.from_loc_no = 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as s13w_ds
    ,sum(
        case
            when a.date_flag >= w.d_13w_begin
                and a.date_flag < w.d_4w_end
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as s13w_all
    ,sum(
        case
            when a.date_flag >= w.d_pmon_begin
                and a.date_flag < w.d_mtd_begin
                and a.from_loc_no <> 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as pmon_reg
    ,sum(
        case
            when a.date_flag >= w.d_pmon_begin
                and a.date_flag < w.d_mtd_begin
                and a.from_loc_no = 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as pmon_ds
    ,sum(
        case
            when a.date_flag >= w.d_pmon_begin
                and a.date_flag < w.d_mtd_begin
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as pmon_all
    ,sum(
        case
            when a.date_flag >= w.d_ppmon_begin
                and a.date_flag < w.d_pmon_begin
                and a.from_loc_no <> 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as ppmon_reg
    ,sum(
        case
            when a.date_flag >= w.d_ppmon_begin
                and a.date_flag < w.d_pmon_begin
                and a.from_loc_no = 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as ppmon_ds
    ,sum(
        case
            when a.date_flag >= w.d_ppmon_begin
                and a.date_flag < w.d_pmon_begin
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as ppmon_all
    ,sum(
        case
            when a.date_flag >= w.d_mtd_begin
                and a.date_flag < current_date()
                and a.from_loc_no <> 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as mtd_reg
    ,sum(
        case
            when a.date_flag >= w.d_mtd_begin
                and a.date_flag < current_date()
                and a.from_loc_no = 98
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as mtd_ds
    ,sum(
        case
            when a.date_flag >= w.d_mtd_begin
                and a.date_flag < current_date()
                then ifnull(a.ship_qty * a.unit_cost, 0)
            else 0
        end
    ) as mtd_all
from dw_us.dwd_disty_common_pos_di a
cross join win_us11722 w
where a.date_flag >= w.d_13w_begin
    and a.date_flag < current_date()
    and a.inv_type in (1, 7, 32, 100, 200, 300)
group by
    a.sku_no
    ,a.vend_no
;

update t_sales_us11722 a
set
    prod_code = b.prod_code
    ,vpl_no = b.vpl_no
    ,active_status = b.active_status
from dim_us.dim_pub_part_info b
where a.sku_no = b.sku_no
    and a.prod_code is null
;

drop table if exists t_sales_2_us11722;
create local temporary table t_sales_2_us11722 on commit preserve rows as
select
    prod_code as prod_code
    ,vpl_no as vpl_no
    ,sum(ifnull(s4w_reg, 0)) as s4w_reg
    ,sum(ifnull(s4w_ds, 0)) as s4w_ds
    ,sum(ifnull(s4w_all, 0)) as s4w_all
    ,sum(ifnull(s13w_reg, 0)) as s13w_reg
    ,sum(ifnull(s13w_ds, 0)) as s13w_ds
    ,sum(ifnull(s13w_all, 0)) as s13w_all
    ,sum(ifnull(pmon_reg, 0)) as pmon_reg
    ,sum(ifnull(pmon_ds, 0)) as pmon_ds
    ,sum(ifnull(pmon_all, 0)) as pmon_all
    ,sum(ifnull(ppmon_reg, 0)) as ppmon_reg
    ,sum(ifnull(ppmon_ds, 0)) as ppmon_ds
    ,sum(ifnull(ppmon_all, 0)) as ppmon_all
    ,sum(ifnull(mtd_reg, 0)) as mtd_reg
    ,sum(ifnull(mtd_ds, 0)) as mtd_ds
    ,sum(ifnull(mtd_all, 0)) as mtd_all
from t_sales_us11722
group by
    prod_code
    ,vpl_no
;

update t_res_us11722 a
set
    s4w_reg = b.s4w_reg
    ,s4w_ds = b.s4w_ds
    ,s13w_reg = b.s13w_reg
    ,s13w_ds = b.s13w_ds
    ,pmon_reg = b.pmon_reg
    ,pmon_ds = b.pmon_ds
    ,pmon_all = b.pmon_all
    ,ppmon_reg = b.ppmon_reg
    ,ppmon_ds = b.ppmon_ds
    ,ppmon_all = b.ppmon_all
    ,mtd_reg = b.mtd_reg
    ,mtd_ds = b.mtd_ds
    ,mtd_all = b.mtd_all
from t_sales_2_us11722 b
where a.prod_code = b.prod_code
    and a.vpl_no = b.vpl_no
;

drop table if exists t_rec_mtd_us11722;
create local temporary table t_rec_mtd_us11722 on commit preserve rows as
select
    prod_code as prod_code
    ,vpl_no as vpl_no
    ,sum(ifnull(ap_ttl, 0)) as ap_ttl
    ,sum(ifnull(rec_mtd, 0)) as rec_mtd
from dm_us.dm_disty_pur_purch_forecast461_rtv2
where date_flag = current_date() - 1
group by
    prod_code
    ,vpl_no
;

update t_res_us11722 a
set
    ap_ttl = b.ap_ttl
    ,rec_mtd = b.rec_mtd
from t_rec_mtd_us11722 b
where a.prod_code = b.prod_code
    and a.vpl_no = b.vpl_no
;

drop table if exists so_alo_us11722;
create local temporary table so_alo_us11722 on commit preserve rows as
select
    sum(ifnull(od.order_qty, 0) * ifnull(od.unit_cost, 0)) as so_alo_amt
    ,pm.prod_code as prod_code
    ,pm.vpl_no as vpl_no
from dw_us.dwd_pub_common_order_header_extend oh
inner join dw_us.dwd_disty_sales_open_order_detail od
    on oh.order_no = od.order_no
    and oh.order_type = od.order_type
inner join dim_us.dim_pub_part_info pm
    on od.sku_no = pm.sku_no
where oh.order_type in (1, 11)
    and oh.ship_date is null
    and oh.delete_date is null
    and (od.order_delete_date is null or od.order_delete_date <= cast('1900-01-02' as date))
    and oh.from_inv_type not in (100, 200)
group by
    pm.prod_code
    ,pm.vpl_no
;

update t_res_us11722 a
set so_alo_amt = b.so_alo_amt
from so_alo_us11722 b
where a.prod_code = b.prod_code
    and a.vpl_no = b.vpl_no
;

drop table if exists t_roll_us11722;
-- Rollover fact dwd_disty_inv_aging_rollover_rtv2_df: date_flag = dates_us11722.rollover_date_flag (see file header). age90p = 90+ dollars (not age90_up on dwd_disty_inv_aging_df).
create local temporary table t_roll_us11722 on commit preserve rows as
select
    a.sku_no as sku_no
    ,sum(ifnull(a.rollover, 0) - ifnull(a.age90p, 0)) as age90roll_qty
    ,cast(null as numeric(19, 4)) as age90roll_amt
    ,sum(ifnull(a.rollover, 0)) as monroll_qty
    ,cast(null as numeric(19, 4)) as monroll_amt
    ,cast(null as int) as wr_qty
    ,cast(null as numeric(19, 4)) as wr_amt
from dw_us.dwd_disty_inv_aging_rollover_rtv2_df a
where a.date_flag = (select d.rollover_date_flag from dates_us11722 d limit 1)
    and a.report_type = 90
    and a.inv_type in (1, 7, 32, 300)
group by
    a.sku_no
;

drop table if exists max_week_us11722;
create local temporary table max_week_us11722 on commit preserve rows as
select
    max(week) as max_week
from dw_us.dws_disty_pur_ips_runrate_1w
where sum_type = 'WITYPESTU'
    and inv_type = 1
;

drop table if exists t_w4rr_us11722;
-- w4rr: sum runrate_qty for weeks max_week-4..max_week-1, sku driver from rollover grain, loc_no replaces Sybase region (colleague pattern).
create local temporary table t_w4rr_us11722 on commit preserve rows as
select
    a.sku_no as sku_no
    ,cast(sum(
        case
            when c.week between b.max_week - 4 and b.max_week - 1
                then ifnull(c.runrate_qty, 0)
            else 0
        end
    ) as int) as w4rr
from (
    select distinct
        sku_no as sku_no
    from t_roll_us11722
) a
cross join max_week_us11722 b
left join dw_us.dws_disty_pur_ips_runrate_1w c
    on b.max_week - 10 <= c.week
    and c.week <= b.max_week
    and a.sku_no = c.sku_no
    and c.inv_type in (1, 7, 32, 300)
    and c.sum_type = 'WITYPESTU'
    and c.loc_no < 300
    and c.loc_no <> 98
group by
    a.sku_no
;

drop table if exists eom_us11722;
create local temporary table eom_us11722 on commit preserve rows as
select
    count(*) as weekday_eom
from dim_us.dim_pub_date cal
where cal.m = (
        select m
        from dim_us.dim_pub_date
        where date_flag = current_date()
        limit 1
    )
    and cal.day >= dayofmonth(current_date())
    and cal.weekday = 1
;

-- w4rr: Sybase only updates rows with a runrate row, missing w4rr must use 0 so wr_qty and wr_amt compute (same formula with w4rr=0).
update t_roll_us11722 a
set wr_qty = case
        when cast(round((
            ifnull(a.monroll_qty, 0)
            - (
                cast(ifnull((
                    select max(w.w4rr)
                    from t_w4rr_us11722 w
                    where w.sku_no = a.sku_no
                ), 0) as float)
                * cast((select e.weekday_eom from eom_us11722 e limit 1) as float)
            ) / 20
        ), 0) as int) < 0
            then 0
        else cast(round((
            ifnull(a.monroll_qty, 0)
            - (
                cast(ifnull((
                    select max(w.w4rr)
                    from t_w4rr_us11722 w
                    where w.sku_no = a.sku_no
                ), 0) as float)
                * cast((select e.weekday_eom from eom_us11722 e limit 1) as float)
            ) / 20
        ), 0) as int)
    end
;

update t_roll_us11722 a
set
    age90roll_amt = ifnull(a.age90roll_qty, 0) * ifnull(pm.ave_cost, 0)
    ,monroll_amt = ifnull(a.monroll_qty, 0) * ifnull(pm.ave_cost, 0)
    ,wr_amt = ifnull(a.wr_qty, 0) * ifnull(pm.ave_cost, 0)
from dim_us.dim_pub_part_info pm
where a.sku_no = pm.sku_no
;

drop table if exists t_roll_2_us11722;
create local temporary table t_roll_2_us11722 on commit preserve rows as
select
    pm.prod_code as prod_code
    ,pm.vpl_no as vpl_no
    ,sum(ifnull(a.age90roll_amt, 0)) as age90roll_amt
    ,sum(ifnull(a.monroll_amt, 0)) as monroll_amt
    ,sum(ifnull(a.wr_amt, 0)) as wr_amt
from t_roll_us11722 a
inner join dim_us.dim_pub_part_info pm
    on a.sku_no = pm.sku_no
group by
    pm.prod_code
    ,pm.vpl_no
;

update t_res_us11722 a
set
    age90roll_amt = b.age90roll_amt
    ,monroll_amt = b.monroll_amt
    ,wr_amt = b.wr_amt
from t_roll_2_us11722 b
where a.prod_code = b.prod_code
    and a.vpl_no = b.vpl_no
;

drop table if exists rds_11722_final_us;
create local temporary table rds_11722_final_us on commit preserve rows as
select
    1 as sum_level
    ,cast(null as varchar(120)) as primary_id
    ,cast(null as varchar(120)) as backup_id
    ,cast(null as varchar(120)) as manager_id
    ,cast(null as varchar(120)) as other_id
    ,cast(null as varchar(120)) as pm_id
    ,cast(null as varchar(120)) as pm_manager_id
    ,cast(null as varchar(120)) as pm_dir_id
    ,cast(null as varchar(120)) as pm_vp_id
    ,cast(null as int) as vend_no
    ,cast(null as varchar(120)) as vend_name
    ,cast(null as int) as master_vend_no
    ,cast(null as varchar(200)) as master_vend_name
    ,cast(null as varchar(20)) as vend_segment
    ,a.prod_code as prod_code
    ,a.vpl_no as vpl_no
    ,cast(null as varchar(150)) as vpc
    ,cast(null as varchar(150)) as vpc_desc
    ,a.oh as oh
    ,a.oo as oo
    ,a.bo as bo
    ,a.age30 as age30
    ,a.age60 as age31_60
    ,a.age90 as age61_90
    ,a.age90p as age90p
    ,a.age120 as age120
    ,a.age150 as age150
    ,a.age180 as age180
    ,a.age210 as age210
    ,a.age240 as age240
    ,a.age270 as age270
    ,a.age300 as age300
    ,a.age330 as age330
    ,a.age360 as age360
    ,a.age360p as age360p
    ,(ifnull(a.age90p, 0) - ifnull(a.age360p, 0)) as age91_360
    ,(ifnull(a.age180, 0) + ifnull(a.age210, 0) + ifnull(a.age240, 0) + ifnull(a.age270, 0) + ifnull(a.age300, 0) + ifnull(a.age330, 0) + ifnull(a.age360, 0) + ifnull(a.age360p, 0)) as age150p
    ,(ifnull(a.age270, 0) + ifnull(a.age300, 0) + ifnull(a.age330, 0) + ifnull(a.age360, 0) + ifnull(a.age360p, 0)) as age240p
    ,(ifnull(a.age300, 0) + ifnull(a.age330, 0) + ifnull(a.age360, 0) + ifnull(a.age360p, 0)) as age270p
    ,cast(0 as float) as age30_percent
    ,cast(0 as float) as age31_60_percent
    ,cast(0 as float) as age61_90_percent
    ,cast(0 as float) as age91_360_percent
    ,cast(0 as float) as age90p_percent
    ,cast(0 as float) as age150p_percent
    ,cast(0 as float) as age240p_percent
    ,cast(0 as float) as age270p_percent
    ,cast(0 as float) as age360p_percent
    ,a.ppmon_reg as ppmon_reg
    ,a.ppmon_ds as ppmon_ds
    ,a.ppmon_all as ppmon_all
    ,a.pmon_reg as pmon_reg
    ,a.pmon_ds as pmon_ds
    ,a.pmon_all as pmon_all
    ,a.mtd_reg as mtd_reg
    ,a.mtd_ds as mtd_ds
    ,a.mtd_all as mtd_all
    ,case when ifnull(a.s4w_reg, 0) <> 0 then a.oh / a.s4w_reg * 4 else 0 end as ohrr_4w
    ,case when ifnull(a.s4w_reg, 0) <> 0 then (a.oh + a.oo) / a.s4w_reg * 4 else 0 end as ohoorr_4w
    ,case when ifnull(a.s13w_reg, 0) <> 0 then a.oh / a.s13w_reg * 13 else 0 end as ohrr_13w
    ,case when ifnull(a.s13w_reg, 0) <> 0 then (a.oh + a.oo) / a.s13w_reg * 13 else 0 end as ohoorr_13w
    ,a.s4w_reg as s4w_reg
    ,a.s4w_ds as s4w_ds
    ,a.s13w_reg as s13w_reg
    ,a.s13w_ds as s13w_ds
    ,cast(null as varchar(60)) as stock_rotation
    ,cast(null as int) as sr_frequency
    ,cast(null as numeric(19, 4)) as sr_per_con
    ,cast(null as numeric(19, 4)) as sr_per_openbox
    ,cast(null as numeric(19, 4)) as sr_per_combine
    ,cast(null as int) as pp_type
    ,cast(null as varchar(120)) as pp_type_desc
    ,a.ap_ttl as ap_ttl
    ,a.rec_mtd as rec_mtd
    ,a.so_alo_amt as so_alo_amt
    ,a.age90roll_amt as age90roll_amt
    ,a.monroll_amt as monroll_amt
    ,a.wr_amt as wr_amt
    ,cast(null as varchar(2)) as day_eom
from t_res_us11722 a
;

update rds_11722_final_us
set
    age30_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age30 / oh
    end
    ,age31_60_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age31_60 / oh
    end
    ,age61_90_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age61_90 / oh
    end
    ,age91_360_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age91_360 / oh
    end
    ,age90p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age90p / oh
    end
    ,age150p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age150p / oh
    end
    ,age240p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age240p / oh
    end
    ,age270p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age270p / oh
    end
    ,age360p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age360p / oh
    end
;

-- Remove VPC rows with no inventory, no sales dollars in checked buckets, and no AP/rec/so/roll (same predicate list as Sybase tempdb..rds_11722_final delete in New_RDS rds_11722_rtv.sp).
delete from rds_11722_final_us
where ifnull(oh, 0) = 0
    and ifnull(oo, 0) = 0
    and ifnull(bo, 0) = 0
    and ifnull(age30, 0) = 0
    and ifnull(age30_percent, 0) = 0
    and ifnull(age31_60, 0) = 0
    and ifnull(age31_60_percent, 0) = 0
    and ifnull(age61_90, 0) = 0
    and ifnull(age61_90_percent, 0) = 0
    and ifnull(age91_360, 0) = 0
    and ifnull(age91_360_percent, 0) = 0
    and ifnull(age150p, 0) = 0
    and ifnull(age150p_percent, 0) = 0
    and ifnull(age240p, 0) = 0
    and ifnull(age240p_percent, 0) = 0
    and ifnull(age270p, 0) = 0
    and ifnull(age270p_percent, 0) = 0
    and ifnull(age360p, 0) = 0
    and ifnull(age360p_percent, 0) = 0
    and ifnull(age90roll_amt, 0) = 0
    and ifnull(monroll_amt, 0) = 0
    and ifnull(wr_amt, 0) = 0
    and ifnull(ppmon_reg, 0) = 0
    and ifnull(ppmon_ds, 0) = 0
    and ifnull(ppmon_all, 0) = 0
    and ifnull(pmon_reg, 0) = 0
    and ifnull(pmon_ds, 0) = 0
    and ifnull(pmon_all, 0) = 0
    and ifnull(mtd_reg, 0) = 0
    and ifnull(mtd_ds, 0) = 0
    and ifnull(mtd_all, 0) = 0
    and ifnull(ohrr_4w, 0) = 0
    and ifnull(ohoorr_4w, 0) = 0
    and ifnull(s4w_reg, 0) = 0
    and ifnull(s4w_ds, 0) = 0
    and ifnull(ap_ttl, 0) = 0
    and ifnull(rec_mtd, 0) = 0
    and ifnull(so_alo_amt, 0) = 0
;

update rds_11722_final_us a
set
    vend_no = b.vend_no
    ,vpc = b.vpl_code
from dim_us.dim_pub_vpl_info b
where a.vpl_no = b.vpl_no
;

update rds_11722_final_us a
set
    pm_id = cast(trim(ifnull(p.pm_name, '')) as varchar(120))
    ,pm_manager_id = cast(trim(ifnull(p.pm_manager_name, '')) as varchar(120))
    ,pm_dir_id = cast(trim(ifnull(p.pm_director_name, '')) as varchar(120))
    ,pm_vp_id = cast(trim(ifnull(p.pm_vp_name, '')) as varchar(120))
    ,primary_id = cast(trim(ifnull(h.buyer_name, '')) as varchar(120))
    ,backup_id = cast(trim(ifnull(h.buyer_primary_backup_name, '')) as varchar(120))
    ,manager_id = cast(trim(ifnull(h.buyer_manager_name, '')) as varchar(120))
    ,other_id = cast(trim(ifnull(h.buyer_director_name, '')) as varchar(120))
from dim_us.dim_pub_vpl_hierarchy_info h
left outer join dim_us.dim_pub_vpl_pm_hierarchy_info p
    on p.vend_no = h.vend_no
    and p.vpl_no = h.vpl_no
where a.vend_no = h.vend_no
    and a.vpl_no = h.vpl_no
;

update rds_11722_final_us a
set
    pm_id = coalesce(nullif(trim(a.pm_id), ''), cast(trim(ifnull(p.pm_name, '')) as varchar(120)))
    ,pm_manager_id = coalesce(nullif(trim(a.pm_manager_id), ''), cast(trim(ifnull(p.pm_manager_name, '')) as varchar(120)))
    ,pm_dir_id = coalesce(nullif(trim(a.pm_dir_id), ''), cast(trim(ifnull(p.pm_director_name, '')) as varchar(120)))
    ,pm_vp_id = coalesce(nullif(trim(a.pm_vp_id), ''), cast(trim(ifnull(p.pm_vp_name, '')) as varchar(120)))
    ,primary_id = coalesce(a.primary_id, cast(trim(ifnull(h.buyer_name, '')) as varchar(120)))
    ,backup_id = coalesce(a.backup_id, cast(trim(ifnull(h.buyer_primary_backup_name, '')) as varchar(120)))
    ,manager_id = coalesce(a.manager_id, cast(trim(ifnull(h.buyer_manager_name, '')) as varchar(120)))
    ,other_id = coalesce(a.other_id, cast(trim(ifnull(h.buyer_director_name, '')) as varchar(120)))
from dim_us.dim_pub_vpl_hierarchy_info h
left outer join dim_us.dim_pub_vpl_pm_hierarchy_info p
    on p.vend_no = h.vend_no
    and p.vpl_no = h.vpl_no
where a.vend_no = h.vend_no
    and h.vpl_no = -1
    and (
        a.primary_id is null
        or a.backup_id is null
        or a.manager_id is null
        or a.other_id is null
        or trim(a.pm_id) is null
        or trim(a.pm_id) = ''
    )
;

update rds_11722_final_us a
set vend_name = v.vend_name
from dim_us.dim_pub_vendor_info v
where a.vend_no = v.vend_no
;

-- Sybase: master_vend_no from vendor_xref with outer join (a.vend_no *= b.vend_no): use xref when present, else vend_no for every row.
update rds_11722_final_us a
set master_vend_no = coalesce(b.xref_no, a.vend_no)
from dim_us.dim_pub_vendor_xref b
where a.vend_no = b.vend_no
    and b.xref_type = 'VEND_PURCH'
    and b.active = 'Y'
;

update rds_11722_final_us
set master_vend_no = vend_no
where master_vend_no is null
    and vend_no is not null
;

insert into rds_11722_final_us (
    sum_level
    ,primary_id
    ,backup_id
    ,manager_id
    ,other_id
    ,pm_id
    ,pm_manager_id
    ,pm_dir_id
    ,pm_vp_id
    ,master_vend_no
    ,prod_code
    ,vpl_no
    ,vpc
    ,vpc_desc
    ,oh
    ,oo
    ,bo
    ,age30
    ,age30_percent
    ,age31_60
    ,age31_60_percent
    ,age61_90
    ,age61_90_percent
    ,age91_360
    ,age91_360_percent
    ,age90p
    ,age90p_percent
    ,age150p
    ,age150p_percent
    ,age240p
    ,age240p_percent
    ,age270p
    ,age270p_percent
    ,age360p
    ,age360p_percent
    ,ppmon_reg
    ,ppmon_ds
    ,ppmon_all
    ,pmon_reg
    ,pmon_ds
    ,pmon_all
    ,mtd_reg
    ,mtd_ds
    ,mtd_all
    ,ohrr_4w
    ,ohoorr_4w
    ,ohrr_13w
    ,ohoorr_13w
    ,s4w_reg
    ,s4w_ds
    ,s13w_reg
    ,s13w_ds
    ,stock_rotation
    ,sr_frequency
    ,sr_per_con
    ,sr_per_openbox
    ,sr_per_combine
    ,pp_type
    ,pp_type_desc
    ,ap_ttl
    ,rec_mtd
    ,so_alo_amt
    ,age90roll_amt
    ,monroll_amt
    ,wr_amt
    ,day_eom
)
select
    2 as sum_level
    ,cast(null as varchar(120)) as primary_id
    ,cast(null as varchar(120)) as backup_id
    ,cast(null as varchar(120)) as manager_id
    ,cast(null as varchar(120)) as other_id
    ,cast(null as varchar(120)) as pm_id
    ,cast(null as varchar(120)) as pm_manager_id
    ,cast(null as varchar(120)) as pm_dir_id
    ,cast(null as varchar(120)) as pm_vp_id
    ,master_vend_no as master_vend_no
    ,cast(null as int) as prod_code
    ,cast(null as int) as vpl_no
    ,cast(null as varchar(150)) as vpc
    ,cast(null as varchar(150)) as vpc_desc
    ,sum(ifnull(oh, 0)) as oh
    ,sum(ifnull(oo, 0)) as oo
    ,sum(ifnull(bo, 0)) as bo
    ,sum(ifnull(age30, 0)) as age30
    ,cast(null as float) as age30_percent
    ,sum(ifnull(age31_60, 0)) as age31_60
    ,cast(null as float) as age31_60_percent
    ,sum(ifnull(age61_90, 0)) as age61_90
    ,cast(null as float) as age61_90_percent
    ,sum(ifnull(age91_360, 0)) as age91_360
    ,cast(null as float) as age91_360_percent
    ,sum(ifnull(age90p, 0)) as age90p
    ,cast(null as float) as age90p_percent
    ,sum(ifnull(age150p, 0)) as age150p
    ,cast(null as float) as age150p_percent
    ,sum(ifnull(age240p, 0)) as age240p
    ,cast(null as float) as age240p_percent
    ,sum(ifnull(age270p, 0)) as age270p
    ,cast(null as float) as age270p_percent
    ,sum(ifnull(age360p, 0)) as age360p
    ,cast(null as float) as age360p_percent
    ,sum(ifnull(ppmon_reg, 0)) as ppmon_reg
    ,sum(ifnull(ppmon_ds, 0)) as ppmon_ds
    ,sum(ifnull(ppmon_all, 0)) as ppmon_all
    ,sum(ifnull(pmon_reg, 0)) as pmon_reg
    ,sum(ifnull(pmon_ds, 0)) as pmon_ds
    ,sum(ifnull(pmon_all, 0)) as pmon_all
    ,sum(ifnull(mtd_reg, 0)) as mtd_reg
    ,sum(ifnull(mtd_ds, 0)) as mtd_ds
    ,sum(ifnull(mtd_all, 0)) as mtd_all
    ,case sum(ifnull(s4w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0)) / sum(ifnull(s4w_reg, 0)) * 4 end as ohrr_4w
    ,case sum(ifnull(s4w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0) + ifnull(oo, 0)) / sum(ifnull(s4w_reg, 0)) * 4 end as ohoorr_4w
    ,case sum(ifnull(s13w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0)) / sum(ifnull(s13w_reg, 0)) * 13 end as ohrr_13w
    ,case sum(ifnull(s13w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0) + ifnull(oo, 0)) / sum(ifnull(s13w_reg, 0)) * 13 end as ohoorr_13w
    ,sum(ifnull(s4w_reg, 0)) as s4w_reg
    ,sum(ifnull(s4w_ds, 0)) as s4w_ds
    ,sum(ifnull(s13w_reg, 0)) as s13w_reg
    ,sum(ifnull(s13w_ds, 0)) as s13w_ds
    ,cast(null as varchar(60)) as stock_rotation
    ,cast(null as int) as sr_frequency
    ,cast(null as numeric(19, 4)) as sr_per_con
    ,cast(null as numeric(19, 4)) as sr_per_openbox
    ,cast(null as numeric(19, 4)) as sr_per_combine
    ,cast(null as int) as pp_type
    ,cast(null as varchar(120)) as pp_type_desc
    ,sum(ifnull(ap_ttl, 0)) as ap_ttl
    ,sum(ifnull(rec_mtd, 0)) as rec_mtd
    ,sum(ifnull(so_alo_amt, 0)) as so_alo_amt
    ,sum(ifnull(age90roll_amt, 0)) as age90roll_amt
    ,sum(ifnull(monroll_amt, 0)) as monroll_amt
    ,sum(ifnull(wr_amt, 0)) as wr_amt
    ,cast(null as varchar(2)) as day_eom
from rds_11722_final_us
where sum_level = 1
group by
    master_vend_no
;

update rds_11722_final_us
set
    age30_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age30 / oh
    end
    ,age31_60_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age31_60 / oh
    end
    ,age61_90_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age61_90 / oh
    end
    ,age91_360_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age91_360 / oh
    end
    ,age90p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age90p / oh
    end
    ,age150p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age150p / oh
    end
    ,age240p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age240p / oh
    end
    ,age270p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age270p / oh
    end
    ,age360p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age360p / oh
    end
where sum_level = 2
;

insert into rds_11722_final_us (
    sum_level
    ,primary_id
    ,backup_id
    ,manager_id
    ,other_id
    ,pm_id
    ,pm_manager_id
    ,pm_dir_id
    ,pm_vp_id
    ,master_vend_no
    ,prod_code
    ,vpl_no
    ,vpc
    ,vpc_desc
    ,oh
    ,oo
    ,bo
    ,age30
    ,age30_percent
    ,age31_60
    ,age31_60_percent
    ,age61_90
    ,age61_90_percent
    ,age91_360
    ,age91_360_percent
    ,age90p
    ,age90p_percent
    ,age150p
    ,age150p_percent
    ,age240p
    ,age240p_percent
    ,age270p
    ,age270p_percent
    ,age360p
    ,age360p_percent
    ,ppmon_reg
    ,ppmon_ds
    ,ppmon_all
    ,pmon_reg
    ,pmon_ds
    ,pmon_all
    ,mtd_reg
    ,mtd_ds
    ,mtd_all
    ,ohrr_4w
    ,ohoorr_4w
    ,ohrr_13w
    ,ohoorr_13w
    ,s4w_reg
    ,s4w_ds
    ,s13w_reg
    ,s13w_ds
    ,stock_rotation
    ,sr_frequency
    ,sr_per_con
    ,sr_per_openbox
    ,sr_per_combine
    ,pp_type
    ,pp_type_desc
    ,ap_ttl
    ,rec_mtd
    ,so_alo_amt
    ,age90roll_amt
    ,monroll_amt
    ,wr_amt
    ,day_eom
)
select
    3 as sum_level
    -- Normalize buyer keys so NULL/blank/whitespace variants roll into one sum_level 3 bucket (reduces extra Vend-Buyer Total rows vs Sybase).
    ,nullif(trim(ifnull(primary_id, '')), '') as primary_id
    ,nullif(trim(ifnull(backup_id, '')), '') as backup_id
    ,nullif(trim(ifnull(manager_id, '')), '') as manager_id
    ,nullif(trim(ifnull(other_id, '')), '') as other_id
    -- Sybase sum_level 3 insert groups by buyer keys + master_vend_no only (not PM_*). PM columns are non-aggregated in Sybase (one row per group picked by engine). Vertica: MAX picks one value per group (ANY_VALUE not available for varchar on this cluster).
    ,max(pm_id) as pm_id
    ,max(pm_manager_id) as pm_manager_id
    ,max(pm_dir_id) as pm_dir_id
    ,max(pm_vp_id) as pm_vp_id
    ,master_vend_no as master_vend_no
    ,cast(null as int) as prod_code
    ,cast(null as int) as vpl_no
    ,cast(null as varchar(150)) as vpc
    ,cast(null as varchar(150)) as vpc_desc
    ,sum(ifnull(oh, 0)) as oh
    ,sum(ifnull(oo, 0)) as oo
    ,sum(ifnull(bo, 0)) as bo
    ,sum(ifnull(age30, 0)) as age30
    ,cast(null as float) as age30_percent
    ,sum(ifnull(age31_60, 0)) as age31_60
    ,cast(null as float) as age31_60_percent
    ,sum(ifnull(age61_90, 0)) as age61_90
    ,cast(null as float) as age61_90_percent
    ,sum(ifnull(age91_360, 0)) as age91_360
    ,cast(null as float) as age91_360_percent
    ,sum(ifnull(age90p, 0)) as age90p
    ,cast(null as float) as age90p_percent
    ,sum(ifnull(age150p, 0)) as age150p
    ,cast(null as float) as age150p_percent
    ,sum(ifnull(age240p, 0)) as age240p
    ,cast(null as float) as age240p_percent
    ,sum(ifnull(age270p, 0)) as age270p
    ,cast(null as float) as age270p_percent
    ,sum(ifnull(age360p, 0)) as age360p
    ,cast(null as float) as age360p_percent
    ,sum(ifnull(ppmon_reg, 0)) as ppmon_reg
    ,sum(ifnull(ppmon_ds, 0)) as ppmon_ds
    ,sum(ifnull(ppmon_all, 0)) as ppmon_all
    ,sum(ifnull(pmon_reg, 0)) as pmon_reg
    ,sum(ifnull(pmon_ds, 0)) as pmon_ds
    ,sum(ifnull(pmon_all, 0)) as pmon_all
    ,sum(ifnull(mtd_reg, 0)) as mtd_reg
    ,sum(ifnull(mtd_ds, 0)) as mtd_ds
    ,sum(ifnull(mtd_all, 0)) as mtd_all
    ,case sum(ifnull(s4w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0)) / sum(ifnull(s4w_reg, 0)) * 4 end as ohrr_4w
    ,case sum(ifnull(s4w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0) + ifnull(oo, 0)) / sum(ifnull(s4w_reg, 0)) * 4 end as ohoorr_4w
    ,case sum(ifnull(s13w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0)) / sum(ifnull(s13w_reg, 0)) * 13 end as ohrr_13w
    ,case sum(ifnull(s13w_reg, 0)) when 0 then 0 else sum(ifnull(oh, 0) + ifnull(oo, 0)) / sum(ifnull(s13w_reg, 0)) * 13 end as ohoorr_13w
    ,sum(ifnull(s4w_reg, 0)) as s4w_reg
    ,sum(ifnull(s4w_ds, 0)) as s4w_ds
    ,sum(ifnull(s13w_reg, 0)) as s13w_reg
    ,sum(ifnull(s13w_ds, 0)) as s13w_ds
    ,cast(null as varchar(60)) as stock_rotation
    ,cast(null as int) as sr_frequency
    ,cast(null as numeric(19, 4)) as sr_per_con
    ,cast(null as numeric(19, 4)) as sr_per_openbox
    ,cast(null as numeric(19, 4)) as sr_per_combine
    ,cast(null as int) as pp_type
    ,cast(null as varchar(120)) as pp_type_desc
    ,sum(ifnull(ap_ttl, 0)) as ap_ttl
    ,sum(ifnull(rec_mtd, 0)) as rec_mtd
    ,sum(ifnull(so_alo_amt, 0)) as so_alo_amt
    ,sum(ifnull(age90roll_amt, 0)) as age90roll_amt
    ,sum(ifnull(monroll_amt, 0)) as monroll_amt
    ,sum(ifnull(wr_amt, 0)) as wr_amt
    ,cast(null as varchar(2)) as day_eom
from rds_11722_final_us
where sum_level = 1
group by
    nullif(trim(ifnull(primary_id, '')), '')
    ,nullif(trim(ifnull(backup_id, '')), '')
    ,nullif(trim(ifnull(manager_id, '')), '')
    ,nullif(trim(ifnull(other_id, '')), '')
    ,master_vend_no
;

update rds_11722_final_us
set
    age30_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age30 / oh
    end
    ,age31_60_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age31_60 / oh
    end
    ,age61_90_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age61_90 / oh
    end
    ,age91_360_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age91_360 / oh
    end
    ,age90p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age90p / oh
    end
    ,age150p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age150p / oh
    end
    ,age240p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age240p / oh
    end
    ,age270p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age270p / oh
    end
    ,age360p_percent = case
        when ifnull(oh, 0) = 0 then 0
        else age360p / oh
    end
where sum_level = 3
;

update rds_11722_final_us dw
set master_vend_name = case
        when dw.sum_level = 1 then vm.vend_name
        when dw.sum_level = 2 then 'Vend Total_' || vm.vend_name
        when dw.sum_level = 3 then 'Vend-Buyer Total_' || vm.vend_name || '(' || ifnull(dw.primary_id, '') || ')'
        else null
    end
    ,vend_segment = vm.vend_seg_code
from dim_us.dim_pub_vendor_info vm
where dw.master_vend_no = vm.vend_no
;

update rds_11722_final_us a
set vpc_desc = b.vpl_desc
from dim_us.dim_pub_vpl_info b
where a.vpl_no = b.vpl_no
;

-- Sybase: CIS..vend_master_etc + list_box_detail (SSR) + prod_code_detail / pp_type=100 override + dw_calendar day_eom.
-- Vertica: CIS..vend_master_etc -> ods_us.ods_cis_corp_vend_master_etc (Sybase column names: stock_rotation_opt, sr_freq, sr_per_*, pp_type).
update rds_11722_final_us a
set stock_rotation = c.code_desc
from ods_us.ods_cis_corp_vend_master_etc b
inner join dim_us.dim_pub_list_box_detail c
    on trim(cast(b.stock_rotation_opt as varchar(50))) = trim(cast(c.code_value as varchar(50)))
    and c.list_box_code = 'SSR'
    and c.delete_datetime is null
where a.vend_no = b.vend_no
;

-- Sybase: update from CIS..vend_master_etc (New_RDS rds_11722 lines 1355-1359, same block in corporate rds_11470_rtv.sp as Sybase).
update rds_11722_final_us a
set
    sr_frequency = b.sr_freq
    ,sr_per_con = b.sr_per_con
    ,sr_per_openbox = b.sr_per_openbox
    ,sr_per_combine = b.sr_per_combine
    ,pp_type = b.pp_type
from ods_us.ods_cis_corp_vend_master_etc b
where a.vend_no = b.vend_no
;

update rds_11722_final_us a
set pp_type_desc = cast(s.desc_val as varchar(120))
from (
    select
        pcd.data_no as data_no
        ,max(pcd.data_value) as desc_val
    from ods_us.ods_cis_corp_prod_code_detail pcd
    where pcd.prod_code = 0
        and pcd.col_no = 1
    group by
        pcd.data_no
) s
where a.pp_type = s.data_no
;

update rds_11722_final_us a
set pp_type_desc = 'Scale 100 (Multiple  Price protection)'
where a.pp_type = 100
;

-- Sybase: day_eom = convert(varchar(2), 91 - @day_eom) with @day_eom = datediff(day, getdate(), max(date_flag for current month)) + 1. Vertica: (max(date)::date - current_date::date) matches SS datediff for calendar dates, use +1 only.
update rds_11722_final_us
set day_eom = cast(
    91 - (
        (
            (
                select max(cal.date_flag)
                from dim_us.dim_pub_date cal
                where cal.m = (
                    select sub.m
                    from dim_us.dim_pub_date sub
                    where sub.date_flag = current_date()
                    limit 1
                )
            )::date
            - current_date()::date
        ) + 1
    ) as varchar(2)
)
;

delete from rds_11722_final_us
where master_vend_name like 'Vend-Buyer Total%'
;

drop table if exists rds_tmp_11722_us;
create local temporary table rds_tmp_11722_us on commit preserve rows as
select
    vend_no as "Vendor#"
    ,vend_name as "Vend Name"
    ,master_vend_no as "Master Vendor#"
    ,master_vend_name as "Master Vend Name"
    ,vend_segment as "Vend Seg"
    ,prod_code as "PM"
    ,vpc as "VPC"
    ,vpc_desc as "VPC description"
    ,cast(oh as decimal(20, 0)) as "OH Amt"
    ,cast(oo as decimal(20, 0)) as "OO Amt"
    ,cast(bo as decimal(20, 0)) as "BO Amt"
    ,cast(age30 as decimal(20, 0)) as "Age 0-30"
    ,cast(age30_percent * 100 as decimal(15, 2)) as "Age 0-30 Percent(%)"
    ,cast(age31_60 as decimal(20, 0)) as "Age 31-60"
    ,cast(age31_60_percent * 100 as decimal(15, 2)) as "Age 31-60 Percent(%)"
    ,cast(age61_90 as decimal(20, 0)) as "Age 61-90"
    ,cast(age61_90_percent * 100 as decimal(15, 2)) as "Age 61-90 Percent(%)"
    ,cast(age91_360 as decimal(20, 0)) as "Age 91-360"
    ,cast(age91_360_percent * 100 as decimal(15, 2)) as "Age 91-360 Percent(%)"
    ,cast(age90p as decimal(20, 0)) as "Age 90+"
    ,cast(age90p_percent * 100 as decimal(15, 2)) as "Age 90+ Percent(%)"
    ,cast(age150p as decimal(20, 0)) as "Age 150+"
    ,cast(age150p_percent * 100 as decimal(15, 2)) as "Age 150+ Percent(%)"
    ,cast(age240p as decimal(20, 0)) as "Age 240+"
    ,cast(age240p_percent * 100 as decimal(15, 2)) as "Age 240+ Percent(%)"
    ,cast(age270p as decimal(20, 0)) as "Age 270+"
    ,cast(age270p_percent * 100 as decimal(15, 2)) as "Age 270+ Percent(%)"
    ,cast(age360p as decimal(20, 0)) as "Age 361+"
    ,cast(age360p_percent * 100 as decimal(15, 2)) as "Age 360+ Percent(%)"
    ,cast(ppmon_reg as decimal(20, 0)) as "PP Mon Reg"
    ,cast(ppmon_ds as decimal(20, 0)) as "PP Mon DS"
    ,cast(ppmon_all as decimal(20, 0)) as "PP Mon Sales"
    ,cast(pmon_reg as decimal(20, 0)) as "P Mon Reg"
    ,cast(pmon_ds as decimal(20, 0)) as "P Mon DS"
    ,cast(pmon_all as decimal(20, 0)) as "P Mon Sales"
    ,cast(mtd_reg as decimal(20, 0)) as "MTD Reg"
    ,cast(mtd_ds as decimal(20, 0)) as "MTD DS"
    ,cast(mtd_all as decimal(20, 0)) as "MTD Sales"
    ,cast(ohrr_4w as decimal(20, 1)) as "OHRR Week 4wk"
    ,cast(ohoorr_4w as decimal(20, 1)) as "OHOORR Week 4wk"
    ,cast(ohrr_13w as decimal(20, 1)) as "OHRR Week 13wk"
    ,cast(ohoorr_13w as decimal(20, 1)) as "OHOORR Week 13wk"
    ,cast(s4w_reg as decimal(20, 0)) as "Last 4wk Stocking Sales"
    ,cast(s4w_ds as decimal(20, 0)) as "Last 4wk DS Sales"
    ,cast(s13w_reg as decimal(20, 0)) as "Last 13wk Stocking Sales"
    ,cast(s13w_ds as decimal(20, 0)) as "Last 13wk DS Sales"
    ,cast(so_alo_amt as decimal(20, 0)) as "SO Allocated Amt"
    ,cast(age90roll_amt as decimal(20, 0)) as "Age91roll Amt"
    ,cast(monroll_amt as decimal(20, 0)) as "MTD Roll+ Ext"
    ,cast(wr_amt as decimal(20, 0)) as "MTD Roll+ w/r Ext"
    ,day_eom as "Days"
    ,stock_rotation as "Stock Rotation Terms"
    ,sr_frequency as "Frequency(months)"
    ,sr_per_con as "Concealed %"
    ,sr_per_openbox as "Open Box %"
    ,sr_per_combine as "Combined %"
    ,cast(pp_type as varchar(10)) || ' ' || pp_type_desc as "Price Protection"
    ,pm_id as "Product Manager(Primary)"
    ,pm_manager_id as "Product Manager(Manager)"
    ,pm_dir_id as "Product Manager(Director)"
    ,pm_vp_id as "Product Manager(VP)"
    ,primary_id as "US Buyer"
    ,backup_id as "US Buyer backup"
    ,manager_id as "US Buyer Mgr"
    ,other_id as "US Buyer Dir/VP"
from rds_11722_final_us
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_tmp_11722_us
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
-- 2