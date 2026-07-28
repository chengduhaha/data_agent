# -*- coding: utf-8 -*-
# @Time : 9/11/2023 5:32 PM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql
# dw_{country}.dws_disty_brpt_bd_mtd
#
# ods_{country}.ods_cis_corp_bd_task_goal


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):

    month_no = conf.get("month_no")
    first_biz_date = conf.get("first_biz_date")


    main_sql = r"""
    with
    table_goal as (
    select
        date_flag,
        project_no,
        task_no,
        company_no,
        sales                          as goal_nsales,
        (sales * gm_percent) /100      as goal_gm,
        (sales * ngm_percent) / 100    as goal_ngm,
        (sales * opl_gm_percent) / 100 as goal_opl_gm,
        null                           as goal_oplgm_plus_amt,
        (sales * tgm_percent) / 100    as goal_tgm,
        null                           as goal_dos,
        null                           as goal_pdt,
        null                           as goal_total_btl,
        new_cust                       as goal_cust_cnt
    from ods_{country}.ods_cis_corp_bd_task_goal         -- unique id : date_flag + project_no + task_no
    where date_flag = date_trunc('MM', '{dt_month}')
    and (sales <> 0 or new_cust <> 0)
    ),
    
    table_dwd as (
    select
        project_no,
        task_no,
        b33_flag,
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
        sum(cgp) as cgp,
        sum(total_btl) as total_btl,
        sum(tgm_amt) as tgm_amt,
        sum(gm_amt) as gm_amt,
        sum(ngm_amt) as ngm_amt,
        sum(oplgm_amt) as oplgm_amt,
        sum(oplgm_plus_amt) as oplgm_plus_amt,

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
        
        sum(rr_unit) as rr_unit,
        sum(rr_sales) as rr_sales,
        sum(rr_cost) as rr_cost,
        sum(rr_gm) as rr_gm,
        sum(rr_ngm) as rr_ngm,
        sum(rr_opl) as rr_opl,
        sum(rr_oplgm_plus_amt) as rr_oplgm_plus_amt,
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
        
        sum(btl_sales_for_opl         ) as btl_sales_for_opl         ,
        sum(trans_btl_sales_for_opl   ) as trans_btl_sales_for_opl   ,
        sum(pdt_for_opl               ) as pdt_for_opl               ,
        sum(cust_rebate_for_opl       ) as cust_rebate_for_opl       ,
        sum(cvr_rm_for_opl            ) as cvr_rm_for_opl            ,
        sum(btl_backout_for_opl       ) as btl_backout_for_opl       ,
        sum(cust_pmt_disc_for_opl     ) as cust_pmt_disc_for_opl     ,
        sum(cust_finance_sales_for_opl) as cust_finance_sales_for_opl,
        sum(rma_for_opl               ) as rma_for_opl               ,
        sum(ar_fin_recovery_for_opl   ) as ar_fin_recovery_for_opl   ,
        sum(order_overhead_for_opl    ) as order_overhead_for_opl    ,
        sum(frt_out_exp_for_opl       ) as frt_out_exp_for_opl       ,
        sum(frt_ob_recovery_for_opl   ) as frt_ob_recovery_for_opl   ,
        sum(fx_cost) as fx_cost
    from dw_{country}.dws_disty_brpt_bd_mtd
    where date_flag = '{date_flag}'
    group by
        project_no,
        task_no,
        b33_flag,
        nvl(company_no,1) )

    insert overwrite table dw_{country}.dws_disty_brpt_bd_proj_task_mtd partition(date_flag = '{date_flag}')
    select
    {month_no},
    nvl(table_dwd.project_no,g.project_no),
    table_project.project_desc as project_name,
    nvl(table_dwd.task_no,g.task_no),
    t.task_name,
    nvl(table_dwd.company_no,
        if(g.company_no = -1,1,g.company_no) ) as company_no,  --只有goal 没有sales的project，插入本表时:company_no为1

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    nvl(g.goal_nsales  ,0),
    nvl(g.goal_gm      ,0),
    nvl(g.goal_ngm     ,0),
    nvl(g.goal_opl_gm  ,0),
    nvl(g.goal_tgm     ,0),
    nvl(g.goal_dos     ,0),
    nvl(g.goal_pdt     ,0),
    nvl(g.goal_total_btl,0),
    nvl(g.goal_cust_cnt,0),

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
    
    nvl(table_dwd.rr_unit     ,0),
    nvl(table_dwd.rr_sales    ,0),
    nvl(table_dwd.rr_cost     ,0),
    nvl(table_dwd.rr_gm       ,0),
    nvl(table_dwd.rr_ngm      ,0),
    nvl(table_dwd.rr_opl      ,0),
    nvl(table_dwd.rr_cgp      ,0),
    nvl(table_dwd.rr_total_btl,0),
    nvl(table_dwd.rr_tgm      ,0),

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
    
    '{etl_timestamp}',
    
    nvl(table_dwd.btl_sales_for_opl         ,0),
    nvl(table_dwd.trans_btl_sales_for_opl   ,0),
    nvl(table_dwd.pdt_for_opl               ,0),
    nvl(table_dwd.cust_rebate_for_opl       ,0),
    nvl(table_dwd.cvr_rm_for_opl            ,0),
    nvl(table_dwd.btl_backout_for_opl       ,0),
    nvl(table_dwd.cust_pmt_disc_for_opl     ,0),
    nvl(table_dwd.cust_finance_sales_for_opl,0),
    nvl(table_dwd.rma_for_opl               ,0),
    nvl(table_dwd.ar_fin_recovery_for_opl   ,0),
    nvl(table_dwd.order_overhead_for_opl    ,0),
    nvl(table_dwd.frt_out_exp_for_opl       ,0),
    nvl(table_dwd.frt_ob_recovery_for_opl   ,0),
    nvl(table_dwd.b33_flag,0),
    nvl(table_dwd.fx_cost,0),
    t.bd_svp_id,
    t.bd_svp_name,
    nvl(table_dwd.oplgm_plus_amt     ,0),
    nvl(table_dwd.rr_oplgm_plus_amt  ,0),
    nvl(g.goal_oplgm_plus_amt,0)
    from table_dwd
    full join table_goal as g           -- unique id : date_flag + project_no + task_no
    on table_dwd.project_no = g.project_no
    and table_dwd.task_no = g.task_no
    and (table_dwd.company_no = g.company_no or g.company_no = -1)
    
    left join (select * from dim_{country}.dim_disty_bd_project_user_df where date_flag = '{first_biz_date}') as t
    on nvl(table_dwd.project_no,g.project_no) = t.project_no
    and nvl(table_dwd.task_no,g.task_no) = t.task_no
    
    left join ods_{country}.ods_cis_corp_bd_project as table_project
    on nvl(table_dwd.project_no,g.project_no) = table_project.project_no;
    """.format(country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp=etl_timestamp,
               month_no=month_no,
               first_biz_date=first_biz_date)
    run_sql(main_sql)


main()