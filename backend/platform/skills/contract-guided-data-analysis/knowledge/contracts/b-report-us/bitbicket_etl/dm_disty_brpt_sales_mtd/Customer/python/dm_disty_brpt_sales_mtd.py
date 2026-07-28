# -*- coding: utf-8 -*-
# @Time : 9/20/2023 10:12 AM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

""" 
    cust_terr      & sales_req_id
    terr_sub_group & sales_sup_id
    terr_group     & sales_mgr_id
    cust_type      & sales_dir_id
    division       & sales_vp_id
"""
"""
先决知识点：
1、数据发生时（月中）的terr 和type的对应关系  和  月底时的terr 和type的对应关系，可能不一致。
2、有两种对应关系：terr与type的归属  type与dir的对应

月中的order 一一join方式得到的是  :  terr3  月中归属的type4   及type4【月底】对应的dir4
dim_df 分区=月底 是存储的        :  terr3  月底归属的type5   及type5【月底】对应的dir5

一一join写，目的是要忠于order发生时的数据，并且得到月底的type 与dir的对应关系：
    比如1-10号的订单是我拿下的，20-30号的订单是你拿下的，需要按照事实来汇总数据、获得销售奖金。


"""
# dw_{country}.dws_disty_brpt_cust_mtd
# dw_{country}.dwd_disty_sales_report_goal_view
# ods_{country}.ods_cis_corp_sales_rep_terr
# ods_{country}.ods_cis_corp_sales_mgr_dept
# ods_{country}.ods_cis_corp_manager


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    flow_run_type = conf.get("flow_run_type")
    month_no = conf.get("month_no")
    exec_everyday(country, date_flag, dt_month, etl_timestamp, month_no)


def exec_everyday(country, date_flag, dt_month, etl_timestamp,month_no):
    run_sql("""
    with
    table_goal as (
    select
        company_no,
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
    and cust_no = 0
    and cust_terr <> 0
    group by
        company_no,
        cust_terr,
        cust_type,
        division
    having goal_nsales <> 0
    or goal_cust_cnt <> 0
    or goal_soft_sales <> 0),
    
    table_dws as (
    select
        sales_rep_id,
        sales_sup_id,
        sales_mgr_id,
        sales_dir_id,
        sales_vp_id,
        cust_terr,
        terr_sub_group,
        terr_group,
        cust_type,
        division,
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
    
        sum(bo_gross_sales) as bo_gross_sales,
        sum(bo_gross_cost) as bo_gross_cost,
        sum(bo_total_unit) as bo_total_unit,
        sum(bo_gm_amt) as bo_gm_amt,
        sum(so_gross_sales) as so_gross_sales,
        sum(so_gross_cost) as so_gross_cost,
        sum(so_total_unit) as so_total_unit,
        sum(so_gm_amt) as so_gm_amt,
        sum(bo_age0_7) as bo_age0_7,
        sum(bo_age8_14) as bo_age8_14,
        sum(bo_age15_21) as bo_age15_21,
        sum(bo_age21_up) as bo_age21_up,
        sum(so_age0_7) as so_age0_7,
        sum(so_age8_14) as so_age8_14,
        sum(so_age15_21) as so_age15_21,
        sum(so_age21_up) as so_age21_up,
    
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
        sum(fx_cost) as fx_cost,
        sum(oplgm_plus_amt   ) as oplgm_plus_amt   ,
        sum(rr_oplgm_plus_amt) as rr_oplgm_plus_amt
    from dw_${country}.dws_disty_brpt_cust_mtd
    where date_flag = '${date_flag}'
    group by
        sales_rep_id,
        sales_sup_id,
        sales_mgr_id,
        sales_dir_id,
        sales_vp_id,
        cust_terr,
        terr_sub_group,
        terr_group,
        cust_type,
        division,
        nvl(company_no,1) )
    
    insert overwrite table dm_${country}.dm_disty_brpt_sales_mtd partition(date_flag = '${date_flag}')
    select
        ${month_no},
    
        coalesce(table_dws.sales_rep_id,table1.sales_rep_id,-3)         as sales_rep_id,
        concat_ws(' ', table_manager.firstname, table_manager.lastname) as sales_rep_name,
        coalesce(table_dws.sales_sup_id,table2.manager_id,-3)             as sales_sup_id,
        concat_ws(' ', table_manager2.firstname, table_manager2.lastname) as sales_sup_name,
        coalesce(table_dws.sales_mgr_id,table3.manager_id,-3)             as sales_mgr_id,
        concat_ws(' ', table_manager3.firstname, table_manager3.lastname) as sales_mgr_name,
        coalesce(table_dws.sales_dir_id,table4.manager_id)                as sales_dir_id,
        concat_ws(' ', table_manager4.firstname, table_manager4.lastname) as sales_dir_name,
        coalesce(table_dws.sales_vp_id,table5.manager_id)                 as sales_vp_id,
        concat_ws(' ', table_manager5.firstname, table_manager5.lastname) as sales_vp_name,
        coalesce(table_dws.company_no,table_goal.company_no)              as company_no,
    
        coalesce(table_dws.cust_terr,table_goal.cust_terr,-3)              as cust_terr,
        coalesce(table_dws.terr_sub_group,table_terr.sub_group_id,-3)      as terr_sub_group,
        coalesce(table_dws.terr_group,table_terr.group_id,-3)              as terr_group,
        coalesce(table_dws.cust_type,table_goal.cust_type,-3)              as cust_type,
        coalesce(table_dws.division,table_goal.division,-3)                as division,
    
        nvl(table_goal.goal_nsales,0),
        nvl(table_goal.goal_gm,0),
        nvl(table_goal.goal_ngm,0),
        nvl(table_goal.goal_opl_gm,0),
        nvl(table_goal.goal_tgm,0),
        nvl(table_goal.goal_dos,0),
        nvl(table_goal.goal_pdt,0),
        nvl(table_goal.goal_total_btl,0),
        nvl(table_goal.goal_cust_cnt,0),
    
        nvl(table_dws.gross_sales,0),
        nvl(table_dws.net_sales,0),
        nvl(table_dws.gross_cost,0),
        nvl(table_dws.net_cost,0),
        nvl(table_dws.scm_usage,0),
        nvl(table_dws.ds_sales,0),
        nvl(table_dws.stock_sales,0),
        nvl(table_dws.ds_cost,0),
        nvl(table_dws.stock_cost,0),
        nvl(table_dws.ds_scm_usage,0),
        nvl(table_dws.stock_scm_usage,0),
        nvl(table_dws.total_unit,0),
        nvl(table_dws.total_weight,0),
    
        nvl(table_dws.net_income,0),
        nvl(table_dws.invest_capital,0),
    
        nvl(table_dws.cgp,0),
        nvl(table_dws.total_btl,0),
        nvl(table_dws.tgm_amt,0),
        nvl(table_dws.gm_amt,0),
        nvl(table_dws.ngm_amt,0),
        nvl(table_dws.oplgm_amt,0),
    
        nvl(table_dws.bo_gross_sales,0),
        nvl(table_dws.bo_gross_cost,0),
        nvl(table_dws.bo_total_unit,0),
        nvl(table_dws.bo_gm_amt,0),
        nvl(table_dws.so_gross_sales,0),
        nvl(table_dws.so_gross_cost,0),
        nvl(table_dws.so_total_unit,0),
        nvl(table_dws.so_gm_amt,0),
        nvl(table_dws.bo_age0_7,0),
        nvl(table_dws.bo_age8_14,0),
        nvl(table_dws.bo_age15_21,0),
        nvl(table_dws.bo_age21_up,0),
        nvl(table_dws.so_age0_7,0),
        nvl(table_dws.so_age8_14,0),
        nvl(table_dws.so_age15_21,0),
        nvl(table_dws.so_age21_up,0),
    
        nvl(table_dws.rr_unit,0),
        nvl(table_dws.rr_sales,0),
        nvl(table_dws.rr_cost,0),
        nvl(table_dws.rr_gm,0),
        nvl(table_dws.rr_ngm,0),
        nvl(table_dws.rr_opl,0),
        nvl(table_dws.rr_cgp,0),
        nvl(table_dws.rr_total_btl,0),
        nvl(table_dws.rr_tgm,0),
    
        nvl(table_dws.ap_finance,0),
        nvl(table_dws.inv_cost,0),
        nvl(table_dws.inv_reserve,0),
        nvl(table_dws.cr_risk_cterm,0),
        nvl(table_dws.flr_synnex,0),
        nvl(table_dws.direct_credit,0),
        nvl(table_dws.csgn_edi_fee,0),
        nvl(table_dws.corporate,0),
        nvl(table_dws.sfs,0),
        nvl(table_dws.scm_risk,0),
        nvl(table_dws.flr_vendor,0),
        nvl(table_dws.cust_finance_sales,0),
        nvl(table_dws.cust_pmt_disc,0),
        nvl(table_dws.cvr_rm,0),
        nvl(table_dws.ar_fin_recovery,0),
        nvl(table_dws.mfg_oh,0),
        nvl(table_dws.cust_finance,0),
        nvl(table_dws.rma,0),
        nvl(table_dws.hc_sales,0),
        nvl(table_dws.order_overhead,0),
        nvl(table_dws.margin_share,0),
        nvl(table_dws.ap_adj,0),
        nvl(table_dws.pdt,0),
        nvl(table_dws.scm_cost,0),
        nvl(table_dws.infrastructure,0),
        nvl(table_dws.marketing,0),
        nvl(table_dws.coop,0),
        nvl(table_dws.one_time_btl,0),
        nvl(table_dws.hbtl,0),
        nvl(table_dws.scm_profit_adj,0),
        nvl(table_dws.hc_pm,0),
        nvl(table_dws.hc_bd,0),
        nvl(table_dws.btl,0),
        nvl(table_dws.btl_sales,0),
        nvl(table_dws.btl_backout,0),
        nvl(table_dws.cust_rebate,0),
        nvl(table_dws.mof,0),
        nvl(table_dws.frt_out_load,0),
        nvl(table_dws.frt_out_exp,0),
        nvl(table_dws.whoh_pack,0),
        nvl(table_dws.frt_ob_recovery,0),
        nvl(table_dws.frt_ib_recovery,0),
        nvl(table_dws.others,0),
        nvl(table_dws.others_sales,0),
        nvl(table_dws.scm_disc,0),
        nvl(table_dws.scm_ndisc,0),
        nvl(table_dws.frt_in,0),
        nvl(table_dws.trans_btl,0),
        nvl(table_dws.trans_btl_sales,0),
    
        nvl(table_dws.btl_sales_for_opl,0),
        nvl(table_dws.trans_btl_sales_for_opl,0),
        nvl(table_dws.pdt_for_opl,0),
        nvl(table_dws.cust_rebate_for_opl,0),
        nvl(table_dws.cvr_rm_for_opl,0),
        nvl(table_dws.btl_backout_for_opl,0),
        nvl(table_dws.cust_pmt_disc_for_opl,0),
        nvl(table_dws.cust_finance_sales_for_opl,0),
        nvl(table_dws.rma_for_opl,0),
        nvl(table_dws.ar_fin_recovery_for_opl,0),
        nvl(table_dws.order_overhead_for_opl,0),
        nvl(table_dws.frt_out_exp_for_opl,0),
        nvl(table_dws.frt_ob_recovery_for_opl,0),
    
        '${etl_timestamp}',
        table_terr.terr_name,
        table_sub_group.sub_group_desc,
        table_group.group_desc,
        table_cust_type.cust_type_descr,
        table_div.division_desc,
        nvl(table_dws.fx_cost,0),
        nvl(table_goal.goal_soft_sales,0),
        nvl(table_dws.oplgm_plus_amt      ,0),
        nvl(table_dws.rr_oplgm_plus_amt   ,0),
        nvl(table_goal.goal_oplgm_plus_amt,0)
    from table_dws
    
    full join table_goal
    on table_dws.cust_terr = table_goal.cust_terr
    and table_dws.cust_type = table_goal.cust_type
    and table_dws.division = table_goal.division
    and (table_dws.company_no = table_goal.company_no or table_goal.company_no = -1)
    
    left join (select * from dim_${country}.dim_pub_sales_territory_df where date_flag = '${date_flag}') as table_terr
    on nvl(table_dws.cust_terr,table_goal.cust_terr) = table_terr.sales_terr
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_rep_terr_df
               where date_flag = '${date_flag}' and is_primary_rep = 'Y'
               and (end_date is null or end_date > current_timestamp()) ) as table1 --unique id : sales_terr
    on nvl(table_dws.cust_terr,table_goal.cust_terr) = table1.sales_terr
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'TERR_SUB_GROUP'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table2  --unique id : dept_no
    on nvl(table_dws.terr_sub_group,table_terr.sub_group_id) = table2.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'TERR_GROUP'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table3  --unique id : dept_no
    on nvl(table_dws.terr_sub_group,table_terr.group_id) = table3.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'CUST_TYPE'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table4  --unique id : dept_no
    on nvl(table_dws.cust_type,table_goal.cust_type) = table4.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'DIVISION'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table5  --unique id : dept_no
    on nvl(table_dws.division,table_goal.division) = table5.dept_no
    
    left join ods_${country}.ods_cis_corp_territory_sub_group as table_sub_group
    on nvl(table_dws.terr_sub_group,table_terr.sub_group_id) = table_sub_group.sub_group_id
    
    left join ods_${country}.ods_cis_corp_territory_group as table_group
    on nvl(table_dws.terr_group,table_terr.group_id) = table_group.group_id
    
    left join ods_${country}.ods_cis_corp_cust_type as table_cust_type
    on nvl(table_dws.cust_type,table_goal.cust_type) = table_cust_type.cust_type

    left join ods_${country}.ods_cis_corp_division as table_div
    on nvl(table_dws.division,table_goal.division) =  table_div.division
    
    left join ods_${country}.ods_cis_corp_manager as table_manager   --unique id : userid
    on nvl(table_dws.sales_rep_id,table1.sales_rep_id)    = table_manager.userid
    left join ods_${country}.ods_cis_corp_manager as table_manager2   --unique id : userid
    on nvl(table_dws.sales_sup_id,table2.manager_id)    = table_manager2.userid
    left join ods_${country}.ods_cis_corp_manager as table_manager3   --unique id : userid
    on nvl(table_dws.sales_mgr_id,table3.manager_id)    = table_manager3.userid
    left join ods_${country}.ods_cis_corp_manager as table_manager4   --unique id : userid
    on nvl(table_dws.sales_dir_id,table4.manager_id)    = table_manager4.userid
    left join ods_${country}.ods_cis_corp_manager as table_manager5   --unique id : userid
    on nvl(table_dws.sales_vp_id,table5.manager_id)     = table_manager5.userid
    """)


main()