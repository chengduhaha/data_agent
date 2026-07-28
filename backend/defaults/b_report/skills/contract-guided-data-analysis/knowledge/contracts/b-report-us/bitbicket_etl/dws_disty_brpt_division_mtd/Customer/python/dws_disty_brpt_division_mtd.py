# -*- coding: utf-8 -*-
# @Time : 9/28/2023 10:09 AM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

""" 
    生成上月分区，from mtd, 使用的是上月底的层次关系 得到的terr_sub_group terr_group sales PM
    生成本月分区，from 1d，使用当天最新的层次关系 得到的terr_sub_group terr_group sales PM   1d.date_flag=dim.date_flag
"""
# dw_{country}.dws_disty_brpt_cust_type_mtd


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
        division,
        company_no,
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
    and cust_terr = 0
    and terr_sub_group = 0
    and terr_group = 0
    and cust_type = 0
    and division <> 0
    group by
        division,
        company_no
    having goal_nsales <> 0
    or goal_cust_cnt <> 0
    or goal_soft_sales <> 0),
        
    table_dws as (
    select 
        division       ,
        nvl(company_no,1) as company_no     ,

        sum(gross_sales        ) as gross_sales     ,
        sum(net_sales          ) as net_sales       ,
        sum(gross_cost         ) as gross_cost      ,
        sum(net_cost           ) as net_cost        ,
        sum(scm_usage          ) as scm_usage       ,
        sum(ds_sales           ) as ds_sales        ,
        sum(stock_sales        ) as stock_sales     ,
        sum(ds_cost            ) as ds_cost         ,
        sum(stock_cost         ) as stock_cost      ,
        sum(ds_scm_usage       ) as ds_scm_usage    ,
        sum(stock_scm_usage    ) as stock_scm_usage ,
        sum(total_unit         ) as total_unit      ,
        sum(total_weight       ) as total_weight    ,

        sum(net_income         ) as net_income      ,
        sum(invest_capital     ) as invest_capital  ,

        sum(cgp                ) as cgp         ,
        sum(total_btl          ) as total_btl   ,
        sum(tgm_amt            ) as tgm_amt     ,
        sum(gm_amt             ) as gm_amt      ,
        sum(ngm_amt            ) as ngm_amt     ,
        sum(oplgm_amt          ) as oplgm_amt   ,

        sum(bo_gross_sales     ) as bo_gross_sales,
        sum(bo_gross_cost      ) as bo_gross_cost ,
        sum(bo_total_unit      ) as bo_total_unit ,
        sum(bo_gm_amt          ) as bo_gm_amt     ,
        sum(so_gross_sales     ) as so_gross_sales,
        sum(so_gross_cost      ) as so_gross_cost ,
        sum(so_total_unit      ) as so_total_unit ,
        sum(so_gm_amt          ) as so_gm_amt     ,
        sum(bo_age0_7          ) as bo_age0_7     ,
        sum(bo_age8_14         ) as bo_age8_14    ,
        sum(bo_age15_21        ) as bo_age15_21   ,
        sum(bo_age21_up        ) as bo_age21_up   ,
        sum(so_age0_7          ) as so_age0_7     ,
        sum(so_age8_14         ) as so_age8_14    ,
        sum(so_age15_21        ) as so_age15_21   ,
        sum(so_age21_up        ) as so_age21_up   ,

        sum(rr_unit            ) as rr_unit     ,
        sum(rr_sales           ) as rr_sales    ,
        sum(rr_cost            ) as rr_cost     ,
        sum(rr_gm              ) as rr_gm       ,
        sum(rr_ngm             ) as rr_ngm      ,
        sum(rr_opl             ) as rr_opl      ,
        sum(rr_cgp             ) as rr_cgp      ,
        sum(rr_total_btl       ) as rr_total_btl,
        sum(rr_tgm             ) as rr_tgm      ,

        sum(ap_finance         ) as ap_finance        ,
        sum(inv_cost           ) as inv_cost          ,
        sum(inv_reserve        ) as inv_reserve       ,
        sum(cr_risk_cterm      ) as cr_risk_cterm     ,
        sum(flr_synnex         ) as flr_synnex        ,
        sum(direct_credit      ) as direct_credit     ,
        sum(csgn_edi_fee       ) as csgn_edi_fee      ,
        sum(corporate          ) as corporate         ,
        sum(sfs                ) as sfs               ,
        sum(scm_risk           ) as scm_risk          ,
        sum(flr_vendor         ) as flr_vendor        ,
        sum(cust_finance_sales ) as cust_finance_sales,
        sum(cust_pmt_disc      ) as cust_pmt_disc     ,
        sum(cvr_rm             ) as cvr_rm            ,
        sum(ar_fin_recovery    ) as ar_fin_recovery   ,
        sum(mfg_oh             ) as mfg_oh            ,
        sum(cust_finance       ) as cust_finance      ,
        sum(rma                ) as rma               ,
        sum(hc_sales           ) as hc_sales          ,
        sum(order_overhead     ) as order_overhead    ,
        sum(margin_share       ) as margin_share      ,
        sum(ap_adj             ) as ap_adj            ,
        sum(pdt                ) as pdt               ,
        sum(scm_cost           ) as scm_cost          ,
        sum(infrastructure     ) as infrastructure    ,
        sum(marketing          ) as marketing         ,
        sum(coop               ) as coop              ,
        sum(one_time_btl       ) as one_time_btl      ,
        sum(hbtl               ) as hbtl              ,
        sum(scm_profit_adj     ) as scm_profit_adj    ,
        sum(hc_pm              ) as hc_pm             ,
        sum(hc_bd              ) as hc_bd             ,
        sum(btl                ) as btl               ,
        sum(btl_sales          ) as btl_sales         ,
        sum(btl_backout        ) as btl_backout       ,
        sum(cust_rebate        ) as cust_rebate       ,
        sum(mof                ) as mof               ,
        sum(frt_out_load       ) as frt_out_load      ,
        sum(frt_out_exp        ) as frt_out_exp       ,
        sum(whoh_pack          ) as whoh_pack         ,
        sum(frt_ob_recovery    ) as frt_ob_recovery   ,
        sum(frt_ib_recovery    ) as frt_ib_recovery   ,
        sum(others             ) as others            ,
        sum(others_sales       ) as others_sales      ,
        sum(scm_disc           ) as scm_disc          ,
        sum(scm_ndisc          ) as scm_ndisc         ,
        sum(frt_in             ) as frt_in            ,
        sum(trans_btl          ) as trans_btl         ,
        sum(trans_btl_sales    ) as trans_btl_sales   ,

        sum(btl_sales_for_opl          ) as btl_sales_for_opl          ,
        sum(trans_btl_sales_for_opl    ) as trans_btl_sales_for_opl    ,
        sum(pdt_for_opl                ) as pdt_for_opl                ,
        sum(cust_rebate_for_opl        ) as cust_rebate_for_opl        ,
        sum(cvr_rm_for_opl             ) as cvr_rm_for_opl             ,
        sum(btl_backout_for_opl        ) as btl_backout_for_opl        ,
        sum(cust_pmt_disc_for_opl      ) as cust_pmt_disc_for_opl      ,
        sum(cust_finance_sales_for_opl ) as cust_finance_sales_for_opl ,
        sum(rma_for_opl                ) as rma_for_opl                ,
        sum(ar_fin_recovery_for_opl    ) as ar_fin_recovery_for_opl    ,
        sum(order_overhead_for_opl     ) as order_overhead_for_opl     ,
        sum(frt_out_exp_for_opl        ) as frt_out_exp_for_opl        ,
        sum(frt_ob_recovery_for_opl    ) as frt_ob_recovery_for_opl    ,
        sum(fx_cost) as fx_cost,
        sum(oplgm_plus_amt   ) as oplgm_plus_amt   ,
        sum(rr_oplgm_plus_amt) as rr_oplgm_plus_amt
    from dw_${country}.dws_disty_brpt_cust_type_mtd
    where date_flag = '${date_flag}'
    group by 
        division       ,
        nvl(company_no,1) )
    
    insert overwrite table dw_${country}.dws_disty_brpt_division_mtd partition(date_flag = '${date_flag}')
    select
        ${month_no},
        coalesce(table_dws.division,table_goal.division,-3),
        table_div.division_desc,
        coalesce(table_dws.company_no,table_goal.company_no) as company_no,
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
        nvl(table_goal.goal_nsales,0),
        nvl(table_goal.goal_gm,0),
        nvl(table_goal.goal_ngm,0),
        nvl(table_goal.goal_opl_gm,0),
        nvl(table_goal.goal_tgm,0),
        nvl(table_goal.goal_dos,0),
        nvl(table_goal.goal_pdt,0),
        nvl(table_goal.goal_total_btl,0),
        nvl(table_goal.goal_cust_cnt,0),
        nvl(table_dws.fx_cost,0),
        nvl(table_goal.goal_soft_sales,0),
        nvl(table_dws.oplgm_plus_amt      ,0),
        nvl(table_dws.rr_oplgm_plus_amt   ,0),
        nvl(table_goal.goal_oplgm_plus_amt,0)
    from table_dws 
    full join table_goal
    on table_dws.division = table_goal.division
    and (table_dws.company_no = table_goal.company_no or table_goal.company_no = -1)
    
    left join ods_${country}.ods_cis_corp_division as table_div
    on nvl(table_dws.division,table_goal.division) = table_div.division
    """)


main()