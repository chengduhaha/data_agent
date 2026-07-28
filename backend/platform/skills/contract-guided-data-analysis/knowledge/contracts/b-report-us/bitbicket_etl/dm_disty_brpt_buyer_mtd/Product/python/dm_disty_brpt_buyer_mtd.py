# -*- coding: utf-8 -*-
# @Time : 9/25/2023 3:12 PM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

""" 
    生成上月分区，from mtd, 使用的是上月底的层次关系 得到的terr_sub_group terr_group sales PM
    生成本月分区，from 1d，使用当天最新的层次关系 得到的terr_sub_group terr_group sales PM   1d.date_flag=dim.date_flag
"""
# dw_{country}.dws_disty_brpt_part_mtd
# ods_{country}.ods_cis_corp_manager


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):
    main_sql = r"""
    with
    table_dws as (
    select
        month_no,
        buyer_id,
        buyer_mgr_id,
        buyer_dir_id,
        buyer_vp_id,
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
        sum(oplgm_plus_amt) as oplgm_plus_amt,
    
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
    
        sum(reg_inv) as reg_inv,
        sum(reg_inv_age0_30) as reg_inv_age0_30,
        sum(reg_inv_age31_60) as reg_inv_age31_60,
        sum(reg_inv_age61_90) as reg_inv_age61_90,
        sum(reg_inv_age90_up) as reg_inv_age90_up,
        sum(rma_inv) as rma_inv,
        sum(rma_inv_age0_30) as rma_inv_age0_30,
        sum(rma_inv_age31_60) as rma_inv_age31_60,
        sum(rma_inv_age61_90) as rma_inv_age61_90,
        sum(rma_inv_age90_up) as rma_inv_age90_up,
        sum(oh_cost) as oh_cost,
        sum(oo_cost) as oo_cost,
        sum(oh_qty) as oh_qty,
        sum(oo_qty) as oo_qty,
        
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
        sum(p91_cost) as p91_cost,
        sum(fx_cost) as fx_cost
    from dw_{country}.dws_disty_brpt_part_mtd
    where date_flag = '{date_flag}'
    group by
        month_no,
        buyer_id,
        buyer_mgr_id,
        buyer_dir_id,
        buyer_vp_id,
        nvl(company_no,1) )
    
    insert overwrite table dm_{country}.dm_disty_brpt_buyer_mtd partition(date_flag = '{date_flag}')
    select
        table_dws.month_no,
        coalesce(table_dws.buyer_id,-3),
        concat_ws(' ', table_manager.firstname, table_manager.lastname) as buyer_name,
        coalesce(table_dws.buyer_mgr_id,-3),
        concat_ws(' ', table_manager2.firstname, table_manager2.lastname) as buyer_mgr_name,
        coalesce(table_dws.buyer_dir_id,-3),
        concat_ws(' ', table_manager3.firstname, table_manager3.lastname) as buyer_dir_name,
        coalesce(table_dws.buyer_vp_id,-3),
        concat_ws(' ', table_manager4.firstname, table_manager4.lastname) as buyer_vp_name,
        table_dws.company_no,
    
        gross_sales,
        net_sales,
        gross_cost,
        net_cost,
        scm_usage,
        ds_sales,
        stock_sales,
        ds_cost,
        stock_cost,
        ds_scm_usage,
        stock_scm_usage,
        total_unit,
        total_weight,
        
        net_income,
        invest_capital,
    
        cgp,
        total_btl,
        tgm_amt,
        gm_amt,
        ngm_amt,
        oplgm_amt,
    
        bo_gross_sales,
        bo_gross_cost,
        bo_total_unit,
        bo_gm_amt,
        so_gross_sales,
        so_gross_cost,
        so_total_unit,
        so_gm_amt,
        bo_age0_7,
        bo_age8_14,
        bo_age15_21,
        bo_age21_up,
        so_age0_7,
        so_age8_14,
        so_age15_21,
        so_age21_up,
    
        reg_inv,
        reg_inv_age0_30,
        reg_inv_age31_60,
        reg_inv_age61_90,
        reg_inv_age90_up,
        rma_inv,
        rma_inv_age0_30,
        rma_inv_age31_60,
        rma_inv_age61_90,
        rma_inv_age90_up,
        oh_cost,
        oo_cost,
        oh_qty,
        oo_qty,
        
        rr_unit,
        rr_sales,
        rr_cost,
        rr_gm,
        rr_ngm,
        rr_opl,
        rr_cgp,
        rr_total_btl,
        rr_tgm,
    
        ap_finance,
        inv_cost,
        inv_reserve,
        cr_risk_cterm,
        flr_synnex,
        direct_credit,
        csgn_edi_fee,
        corporate,
        sfs,
        scm_risk,
        flr_vendor,
        cust_finance_sales,
        cust_pmt_disc,
        cvr_rm,
        ar_fin_recovery,
        mfg_oh,
        cust_finance,
        rma,
        hc_sales,
        order_overhead,
        margin_share,
        ap_adj,
        pdt,
        scm_cost,
        infrastructure,
        marketing,
        coop,
        one_time_btl,
        hbtl,
        scm_profit_adj,
        hc_pm,
        hc_bd,
        btl,
        btl_sales,
        btl_backout,
        cust_rebate,
        mof,
        frt_out_load,
        frt_out_exp,
        whoh_pack,
        frt_ob_recovery,
        frt_ib_recovery,
        others,
        others_sales,
        scm_disc,
        scm_ndisc,
        frt_in,
        trans_btl,
        trans_btl_sales,
        
        btl_sales_for_opl,
        trans_btl_sales_for_opl,
        pdt_for_opl,
        cust_rebate_for_opl,
        cvr_rm_for_opl,
        btl_backout_for_opl,
        cust_pmt_disc_for_opl,
        cust_finance_sales_for_opl,
        rma_for_opl,
        ar_fin_recovery_for_opl,
        order_overhead_for_opl,
        frt_out_exp_for_opl,
        frt_ob_recovery_for_opl,
    
        '{etl_timestamp}',
        table_dws.p91_cost,
        table_dws.fx_cost,
        table_dws.oplgm_plus_amt,
        table_dws.rr_oplgm_plus_amt
    from table_dws
    left join ods_{country}.ods_cis_corp_manager as table_manager   --unique id : userid
    on table_dws.buyer_id = table_manager.userid
    left join ods_{country}.ods_cis_corp_manager as table_manager2   --unique id : userid
    on table_dws.buyer_mgr_id = table_manager2.userid
    left join ods_{country}.ods_cis_corp_manager as table_manager3   --unique id : userid
    on table_dws.buyer_dir_id = table_manager3.userid
    left join ods_{country}.ods_cis_corp_manager as table_manager4   --unique id : userid
    on table_dws.buyer_vp_id = table_manager4.userid
    """.format(country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp= etl_timestamp)
    run_sql(main_sql)


main()