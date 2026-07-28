# -*- coding: utf-8 -*-
# @Time : 8/28/2023 10:25 AM
# @Author : Marvin Ma
# @File : dws_disty_brpt_cust_mtd.py

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

""" 
    生成上月分区，from mtd, 使用的是上月底的层次关系 得到的terr_sub_group terr_group sales PM
    生成本月分区，from 1d，使用当天最新的层次关系 得到的terr_sub_group terr_group sales PM   1d.date_flag=dim.date_flag
"""
# dw_{country}.dws_disty_brpt_pl_extend_mtd
# dw_{country}.dws_disty_brpt_bo_aging_df


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):
    run_sql("""
    with
    table_goal as (
    select
        company_no,
        cust_no,
        cust_terr,
        cust_type,
        division,
        sum(net_sales_local_currency)                     as goal_nsales,
        sum(gm * net_sales_local_currency / 100)          as goal_gm,
        sum(ngm * net_sales_local_currency / 100)         as goal_ngm,
        sum(oplgm * net_sales_local_currency / 100)       as goal_opl_gm,
        sum(tgm * net_sales_local_currency / 100)         as goal_tgm,
        null             as goal_dos,
        null             as goal_pdt,
        null             as goal_total_btl,
        sum(cust_cnt)    as goal_cust_cnt,
        sum(soft_local_currency)                          as goal_soft_sales,
        sum(opl_plus * net_sales_local_currency / 100)    as goal_oplgm_plus_amt
    from dw_${country}.dwd_disty_sales_report_goal_view  -- unique id：period,goal_type,division,cust_type,terr_group,terr_sub_group,cust_terr,cust_no,master_cust_no [when cust_terr is not null]
    where period = ${month_no} and goal_type = 'NORMAL'
    and cust_no <> 0
    group by
        company_no,
        cust_no,
        cust_terr,
        cust_type,
        division
    having goal_nsales <> 0
    or goal_cust_cnt <> 0
    or goal_soft_sales <> 0 ),

    table_dwd as (
    select
    cust_no        ,
    mcust_no       ,
    cust_terr      ,
    cust_type      ,
    division       ,
    terr_sub_group ,
    terr_group     ,
    sales_rep_id   ,
    sales_sup_id   ,
    sales_mgr_id   ,
    sales_dir_id   ,
    sales_vp_id    ,
    nvl(company_no,1) as company_no,
    sum(gross_sales) as gross_sales,
    sum(net_sales) as net_sales,
    sum(gross_cost) as gross_cost,
    sum(net_cost) as net_cost,
    sum(scm_usage) as scm_usage,
    sum(ds_sales) as ds_sales,
    sum(stock_sales) as stock_sales,
    sum(ds_cost) as ds_cost,
    sum(stock_cost) as stock_cost,
    sum(ds_scm_usage) as ds_scm_usage,
    sum(stock_scm_usage) as stock_scm_usage,
    sum(total_unit) as total_unit,
    sum(total_weight) as total_weight,

    sum(net_income) as net_income,
    sum(invest_capital) as invest_capital,

    sum(cgp) as cgp,
    sum(total_btl) as total_btl,
    sum(tgm_amt) as tgm_amt,
    sum(gm_amt) as gm_amt,
    sum(ngm_amt) as ngm_amt,
    sum(oplgm_amt) as oplgm_amt,

    sum(rr_unit) as rr_unit,
    sum(rr_sales) as rr_sales,
    sum(rr_cost) as rr_cost,
    sum(rr_gm) as rr_gm,
    sum(rr_ngm) as rr_ngm,
    sum(rr_opl) as rr_opl,
    sum(rr_cgp) as rr_cgp,
    sum(rr_total_btl) as rr_total_btl,
    sum(rr_tgm) as rr_tgm,
    
    sum(ap_finance) as ap_finance,
    sum(inv_cost) as inv_cost,
    sum(inv_reserve) as inv_reserve,
    sum(cr_risk_cterm) as cr_risk_cterm,
    sum(flr_synnex) as flr_synnex,
    sum(direct_credit) as direct_credit,
    sum(csgn_edi_fee) as csgn_edi_fee,
    sum(corporate) as corporate,
    sum(sfs) as sfs,
    sum(scm_risk) as scm_risk,
    sum(flr_vendor) as flr_vendor,
    sum(cust_finance_sales) as cust_finance_sales,
    sum(cust_pmt_disc) as cust_pmt_disc,
    sum(cvr_rm) as cvr_rm,
    sum(ar_fin_recovery) as ar_fin_recovery,
    sum(mfg_oh) as mfg_oh,
    sum(cust_finance) as cust_finance,
    sum(rma) as rma,
    sum(hc_sales) as hc_sales,
    sum(order_overhead) as order_overhead,
    sum(margin_share) as margin_share,
    sum(ap_adj) as ap_adj,
    sum(pdt) as pdt,
    sum(scm_cost) as scm_cost,
    sum(infrastructure) as infrastructure,
    sum(marketing) as marketing,
    sum(coop) as coop,
    sum(one_time_btl) as one_time_btl,
    sum(hbtl) as hbtl,
    sum(scm_profit_adj) as scm_profit_adj,
    sum(hc_pm) as hc_pm,
    sum(hc_bd) as hc_bd,
    sum(btl) as btl,
    sum(btl_sales) as btl_sales,
    sum(btl_backout) as btl_backout,
    sum(cust_rebate) as cust_rebate,
    sum(mof) as mof,
    sum(frt_out_load) as frt_out_load,
    sum(frt_out_exp) as frt_out_exp,
    sum(whoh_pack) as whoh_pack,
    sum(frt_ob_recovery) as frt_ob_recovery,
    sum(frt_ib_recovery) as frt_ib_recovery,
    sum(others) as others,
    sum(others_sales) as others_sales,
    sum(scm_disc) as scm_disc,
    sum(scm_ndisc) as scm_ndisc,
    sum(frt_in) as frt_in,
    sum(trans_btl) as trans_btl,
    sum(trans_btl_sales) as trans_btl_sales,

    sum(btl_sales_for_opl) as btl_sales_for_opl,
    sum(trans_btl_sales_for_opl) as trans_btl_sales_for_opl,
    sum(pdt_for_opl) as pdt_for_opl,
    sum(cust_rebate_for_opl) as cust_rebate_for_opl,
    sum(cvr_rm_for_opl) as cvr_rm_for_opl,
    sum(btl_backout_for_opl) as btl_backout_for_opl,
    sum(cust_pmt_disc_for_opl) as cust_pmt_disc_for_opl,
    sum(cust_finance_sales_for_opl) as cust_finance_sales_for_opl,
    sum(rma_for_opl) as rma_for_opl,
    sum(ar_fin_recovery_for_opl) as ar_fin_recovery_for_opl,
    sum(order_overhead_for_opl) as order_overhead_for_opl,
    sum(frt_out_exp_for_opl) as frt_out_exp_for_opl,
    sum(frt_ob_recovery_for_opl) as frt_ob_recovery_for_opl,
    
    SUM(bo_gross_sales) as bo_gross_sales,
    SUM(bo_gross_cost) as bo_gross_cost,
    SUM(bo_total_unit) as bo_total_unit,
    SUM(bo_gm_amt) as bo_gm_amt,
    SUM(so_gross_sales) as so_gross_sales,
    SUM(so_gross_cost) as so_gross_cost,
    SUM(so_total_unit) as so_total_unit,
    SUM(so_gm_amt) as so_gm_amt,
    SUM(bo_age0_7) as bo_age0_7,
    SUM(bo_age8_14) as bo_age8_14,
    SUM(bo_age15_21) as bo_age15_21,
    SUM(bo_age21_up) as bo_age21_up,
    SUM(so_age0_7) as so_age0_7,
    SUM(so_age8_14) as so_age8_14,
    SUM(so_age15_21) as so_age15_21,
    SUM(so_age21_up) as so_age21_up,
    sum(fx_cost) as fx_cost,
    sum(oplgm_plus_amt   ) as oplgm_plus_amt   ,
    sum(rr_oplgm_plus_amt) as rr_oplgm_plus_amt
    from dw_${country}.dws_disty_brpt_pl_extend_mtd
    where date_flag = '${date_flag}'
    group by
    cust_no        ,
    mcust_no       ,
    cust_terr      ,
    cust_type      ,
    division       ,
    terr_sub_group ,
    terr_group     ,
    sales_rep_id   ,
    sales_sup_id   ,
    sales_mgr_id   ,
    sales_dir_id   ,
    sales_vp_id    ,
    nvl(company_no,1) )

    insert overwrite table dw_${country}.dws_disty_brpt_cust_mtd partition (date_flag = '${date_flag}')
    select
        ${month_no},
        coalesce(table_dwd.cust_no,table_goal.cust_no,-3)                   as cust_no,
        table_customer.cust_name_replace                                    as cust_name,
        coalesce(table_dwd.mcust_no,table_customer.mcust_no,-3)             as mcust_no, -- table_goal的mcust_no不准，所以 以cust_info表为准
        table_mcust.cust_name_replace                                       as mcust_name,
        coalesce(table_dwd.cust_terr,table_goal.cust_terr,-3)               as cust_terr,
        table_terr.terr_name                                                as terr_name,
        coalesce(table_dwd.cust_type,table_goal.cust_type,-3)               as cust_type,
        table_cust_type.cust_type_descr                                     as cust_type_desc ,
        coalesce(table_dwd.division,table_goal.division,-3)                 as division,
        table_div.division_desc                                             as division_desc,
        coalesce(table_dwd.terr_sub_group, table_terr.sub_group_id,-3)      as terr_sub_group,
        table_sub_group.sub_group_desc                                      as sub_group_desc,
        coalesce(table_dwd.terr_group,table_terr.group_id,-3)               as terr_group,
        table_group.group_desc                                              as terr_group_desc,
        coalesce(table_dwd.sales_rep_id   ,table1.sales_rep_id, -3),
        coalesce(table_dwd.sales_sup_id   ,table2.manager_id,   -3),
        coalesce(table_dwd.sales_mgr_id   ,table3.manager_id,   -3),
        coalesce(table_dwd.sales_dir_id   ,table4.manager_id,   -3),
        coalesce(table_dwd.sales_vp_id    ,table5.manager_id,   3),
        coalesce(table_dwd.company_no,table_goal.company_no)                 as company_no,

        nvl(table_dwd.gross_sales,0),
        nvl(table_dwd.net_sales,0),
        nvl(table_dwd.gross_cost,0),
        nvl(table_dwd.net_cost,0),
        nvl(table_dwd.scm_usage,0),
        nvl(table_dwd.ds_sales,0),
        nvl(table_dwd.stock_sales,0),
        nvl(table_dwd.ds_cost,0),
        nvl(table_dwd.stock_cost,0),
        nvl(table_dwd.ds_scm_usage,0),
        nvl(table_dwd.stock_scm_usage,0),
        nvl(table_dwd.total_unit,0),
        nvl(table_dwd.total_weight,0),

        nvl(table_dwd.net_income,0),
        nvl(table_dwd.invest_capital,0),

        nvl(table_dwd.cgp,0),
        nvl(table_dwd.total_btl,0),
        nvl(table_dwd.tgm_amt,0),
        nvl(table_dwd.gm_amt,0),
        nvl(table_dwd.ngm_amt,0),
        nvl(table_dwd.oplgm_amt,0),

        nvl(table_dwd.bo_gross_sales,0),
        nvl(table_dwd.bo_gross_cost,0),
        nvl(table_dwd.bo_total_unit,0),
        nvl(table_dwd.bo_gm_amt,0),
        nvl(table_dwd.so_gross_sales,0),
        nvl(table_dwd.so_gross_cost,0),
        nvl(table_dwd.so_total_unit,0),
        nvl(table_dwd.so_gm_amt,0),
        nvl(table_dwd.bo_age0_7,0),
        nvl(table_dwd.bo_age8_14,0),
        nvl(table_dwd.bo_age15_21,0),
        nvl(table_dwd.bo_age21_up,0),
        nvl(table_dwd.so_age0_7,0),
        nvl(table_dwd.so_age8_14,0),
        nvl(table_dwd.so_age15_21,0),
        nvl(table_dwd.so_age21_up,0),

        nvl(table_dwd.rr_unit,0),
        nvl(table_dwd.rr_sales,0),
        nvl(table_dwd.rr_cost,0),
        nvl(table_dwd.rr_gm,0),
        nvl(table_dwd.rr_ngm,0),
        nvl(table_dwd.rr_opl,0),
        nvl(table_dwd.rr_cgp,0),
        nvl(table_dwd.rr_total_btl,0),
        nvl(table_dwd.rr_tgm,0),

        nvl(table_dwd.ap_finance,0),
        nvl(table_dwd.inv_cost,0),
        nvl(table_dwd.inv_reserve,0),
        nvl(table_dwd.cr_risk_cterm,0),
        nvl(table_dwd.flr_synnex,0),
        nvl(table_dwd.direct_credit,0),
        nvl(table_dwd.csgn_edi_fee,0),
        nvl(table_dwd.corporate,0),
        nvl(table_dwd.sfs,0),
        nvl(table_dwd.scm_risk,0),
        nvl(table_dwd.flr_vendor,0),
        nvl(table_dwd.cust_finance_sales,0),
        nvl(table_dwd.cust_pmt_disc,0),
        nvl(table_dwd.cvr_rm,0),
        nvl(table_dwd.ar_fin_recovery,0),
        nvl(table_dwd.mfg_oh,0),
        nvl(table_dwd.cust_finance,0),
        nvl(table_dwd.rma,0),
        nvl(table_dwd.hc_sales,0),
        nvl(table_dwd.order_overhead,0),
        nvl(table_dwd.margin_share,0),
        nvl(table_dwd.ap_adj,0),
        nvl(table_dwd.pdt,0),
        nvl(table_dwd.scm_cost,0),
        nvl(table_dwd.infrastructure,0),
        nvl(table_dwd.marketing,0),
        nvl(table_dwd.coop,0),
        nvl(table_dwd.one_time_btl,0),
        nvl(table_dwd.hbtl,0),
        nvl(table_dwd.scm_profit_adj,0),
        nvl(table_dwd.hc_pm,0),
        nvl(table_dwd.hc_bd,0),
        nvl(table_dwd.btl,0),
        nvl(table_dwd.btl_sales,0),
        nvl(table_dwd.btl_backout,0),
        nvl(table_dwd.cust_rebate,0),
        nvl(table_dwd.mof,0),
        nvl(table_dwd.frt_out_load,0),
        nvl(table_dwd.frt_out_exp,0),
        nvl(table_dwd.whoh_pack,0),
        nvl(table_dwd.frt_ob_recovery,0),
        nvl(table_dwd.frt_ib_recovery,0),
        nvl(table_dwd.others,0),
        nvl(table_dwd.others_sales,0),
        nvl(table_dwd.scm_disc,0),
        nvl(table_dwd.scm_ndisc,0),
        nvl(table_dwd.frt_in,0),
        nvl(table_dwd.trans_btl,0),
        nvl(table_dwd.trans_btl_sales,0),

        nvl(table_dwd.btl_sales_for_opl,0),
        nvl(table_dwd.trans_btl_sales_for_opl,0),
        nvl(table_dwd.pdt_for_opl,0),
        nvl(table_dwd.cust_rebate_for_opl,0),
        nvl(table_dwd.cvr_rm_for_opl,0),
        nvl(table_dwd.btl_backout_for_opl,0),
        nvl(table_dwd.cust_pmt_disc_for_opl,0),
        nvl(table_dwd.cust_finance_sales_for_opl,0),
        nvl(table_dwd.rma_for_opl,0),
        nvl(table_dwd.ar_fin_recovery_for_opl,0),
        nvl(table_dwd.order_overhead_for_opl,0),
        nvl(table_dwd.frt_out_exp_for_opl,0),
        nvl(table_dwd.frt_ob_recovery_for_opl,0),
        '${etl_timestamp}',
        nvl(table_goal.goal_nsales,0),
        nvl(table_goal.goal_gm,0),
        nvl(table_goal.goal_ngm,0),
        nvl(table_goal.goal_opl_gm,0),
        nvl(table_goal.goal_tgm,0),
        nvl(table_goal.goal_dos,0),
        nvl(table_goal.goal_pdt,0),
        nvl(table_goal.goal_total_btl,0),
        nvl(table_goal.goal_cust_cnt,0),
        nvl(table_dwd.fx_cost,0),
        nvl(table_goal.goal_soft_sales,0),
        nvl(table_dwd.oplgm_plus_amt      ,0),
        nvl(table_dwd.rr_oplgm_plus_amt   ,0),
        nvl(table_goal.goal_oplgm_plus_amt,0)
    from table_dwd

    full join table_goal
    on table_dwd.cust_no = table_goal.cust_no
    and table_dwd.cust_terr = table_goal.cust_terr
    and table_dwd.cust_type = table_goal.cust_type
    and table_dwd.division = table_goal.division
    and (table_dwd.company_no = table_goal.company_no or table_goal.company_no = -1)
    
    left join (select *,replace(cust_name,'\\\\','/') as cust_name_replace
               from dim_${country}.dim_pub_customer_info_df
               where date_flag = '${date_flag}') as table_customer                     -- unique id: cust_no
    on nvl(table_dwd.cust_no,table_goal.cust_no) = table_customer.cust_no
    
    left join (select *,replace(cust_name,'\\\\','/') as cust_name_replace
               from dim_${country}.dim_pub_customer_info_df
               where date_flag = '${date_flag}') as table_mcust
    on nvl(table_dwd.mcust_no,table_customer.mcust_no) = table_mcust.cust_no
    

    left join ods_${country}.ods_cis_corp_cust_type as table_cust_type    
    on nvl(table_dwd.cust_type,table_goal.cust_type) = table_cust_type.cust_type

    left join ods_${country}.ods_cis_corp_division as table_div
    on nvl(table_dwd.division,table_goal.division) =  table_div.division
    
    left join (select * from dim_${country}.dim_pub_sales_territory_df where date_flag = '${date_flag}') as table_terr
    on nvl(table_dwd.cust_terr,table_goal.cust_terr) = table_terr.sales_terr
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_rep_terr_df
               where date_flag = '${date_flag}' and is_primary_rep = 'Y'
               and (end_date is null or end_date > current_timestamp()) ) as table1 --unique id : sales_terr
    on nvl(table_dwd.cust_terr,table_goal.cust_terr) = table1.sales_terr
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'TERR_SUB_GROUP'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table2  --unique id : dept_no
    on table_terr.sub_group_id = table2.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'TERR_GROUP'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table3  --unique id : dept_no
    on table_terr.group_id = table3.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'CUST_TYPE'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table4  --unique id : dept_no
    on nvl(table_dwd.cust_type,table_goal.cust_type) = table4.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'DIVISION'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table5  --unique id : dept_no
    on nvl(table_dwd.division,table_goal.division) = table5.dept_no
    
    left join ods_${country}.ods_cis_corp_territory_sub_group as table_sub_group
    on nvl(table_dwd.terr_sub_group,table_terr.sub_group_id) = table_sub_group.sub_group_id
    
    left join ods_${country}.ods_cis_corp_territory_group as table_group
    on nvl(table_dwd.terr_group,table_terr.group_id) = table_group.group_id
    """)

    # goal表有脏数据的情况： goal表的terr_sub_group terr_group为0， dwd表不为0。
    # 这样就导致同一个cust_terr有两行数据，在生成comb_mtd表时会笛卡尔积
    # 所以join goal表时，不再on terr_sub_group terr_group



main()