# -*- coding: utf-8 -*-
# @Time : 9/12/2023 2:33 PM
# @Author : Marvin Ma


from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql
# dw_{country}.dws_disty_brpt_bd_proj_task_mtd


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):
    main_sql = r"""
    insert overwrite table dm_{country}.dm_disty_brpt_bd_rep_mtd partition(date_flag = '{date_flag}')
    select
        month_no,
        bd_rep_id,
        bd_rep_name,
        bd_mgr_id,
        bd_mgr_name,
        bd_dir_id,
        bd_dir_name,
        bd_vp_id,
        bd_vp_name,
        company_no,

        sum(goal_nsales),
        sum(goal_gm),
        sum(goal_ngm),
        sum(goal_opl_gm),
        sum(goal_tgm),
        sum(goal_dos),
        sum(goal_pdt),
        sum(goal_total_btl),
        sum(goal_cust_cnt),

        sum(gross_sales),
        sum(net_sales),
        sum(gross_cost),
        sum(net_cost),
        sum(scm_usage),
        sum(ds_sales),
        sum(stock_sales),
        sum(ds_cost),
        sum(stock_cost),
        sum(ds_scm_usage),
        sum(stock_scm_usage),
        sum(total_unit),
        sum(total_weight),

        sum(cgp),
        sum(total_btl),
        sum(tgm_amt),
        sum(gm_amt),
        sum(ngm_amt),
        sum(oplgm_amt),

        sum(bo_gross_sales),
        sum(bo_gross_cost),
        sum(bo_total_unit),
        sum(bo_gm_amt),
        sum(so_gross_sales),
        sum(so_gross_cost),
        sum(so_total_unit),
        sum(so_gm_amt),
        sum(bo_age0_7),
        sum(bo_age8_14),
        sum(bo_age15_21),
        sum(bo_age21_up),
        sum(so_age0_7),
        sum(so_age8_14),
        sum(so_age15_21),
        sum(so_age21_up),
        
        sum(rr_unit) as rr_unit,
        sum(rr_sales) as rr_sales,
        sum(rr_cost) as rr_cost,
        sum(rr_gm) as rr_gm,
        sum(rr_ngm) as rr_ngm,
        sum(rr_opl) as rr_opl,
        sum(rr_cgp) as rr_cgp,
        sum(rr_total_btl) as rr_total_btl,
        sum(rr_tgm) as rr_tgm,

        sum(ap_finance),
        sum(inv_cost),
        sum(inv_reserve),
        sum(cr_risk_cterm),
        sum(flr_synnex),
        sum(direct_credit),
        sum(csgn_edi_fee),
        sum(corporate),
        sum(sfs),
        sum(scm_risk),
        sum(flr_vendor),
        sum(cust_finance_sales),
        sum(cust_pmt_disc),
        sum(cvr_rm),
        sum(ar_fin_recovery),
        sum(mfg_oh),
        sum(cust_finance),
        sum(rma),
        sum(hc_sales),
        sum(order_overhead),
        sum(margin_share),
        sum(ap_adj),
        sum(pdt),
        sum(scm_cost),
        sum(infrastructure),
        sum(marketing),
        sum(coop),
        sum(one_time_btl),
        sum(hbtl),
        sum(scm_profit_adj),
        sum(hc_pm),
        sum(hc_bd),
        sum(btl),
        sum(btl_sales),
        sum(btl_backout),
        sum(cust_rebate),
        sum(mof),
        sum(frt_out_load),
        sum(frt_out_exp),
        sum(whoh_pack),
        sum(frt_ob_recovery),
        sum(frt_ib_recovery),
        sum(others),
        sum(others_sales),
        sum(scm_disc),
        sum(scm_ndisc),
        sum(frt_in),
        sum(trans_btl),
        sum(trans_btl_sales),
        '{etl_timestamp}',
        
        sum(btl_sales_for_opl         ),
        sum(trans_btl_sales_for_opl   ),
        sum(pdt_for_opl               ),
        sum(cust_rebate_for_opl       ),
        sum(cvr_rm_for_opl            ),
        sum(btl_backout_for_opl       ),
        sum(cust_pmt_disc_for_opl     ),
        sum(cust_finance_sales_for_opl),
        sum(rma_for_opl               ),
        sum(ar_fin_recovery_for_opl   ),
        sum(order_overhead_for_opl    ),
        sum(frt_out_exp_for_opl       ),
        sum(frt_ob_recovery_for_opl   ),
        b33_flag,
        sum(fx_cost),
        bd_svp_id,
        bd_svp_name,
        sum(oplgm_plus_amt     ),
        sum(rr_oplgm_plus_amt  ),
        sum(goal_oplgm_plus_amt)
    from dw_{country}.dws_disty_brpt_bd_proj_task_mtd
    where date_flag = '{date_flag}'
    group by
        month_no,
        b33_flag,
        bd_rep_id,
        bd_rep_name,
        bd_mgr_id,
        bd_mgr_name,
        bd_dir_id,
        bd_dir_name,
        bd_vp_id,
        bd_vp_name,
        bd_svp_id,
        bd_svp_name,
        company_no
    """.format(country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp=etl_timestamp)
    run_sql(main_sql)


main()