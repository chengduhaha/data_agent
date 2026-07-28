# -*- coding: utf-8 -*-
# @Time : 2025/12/23 10:53
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

run_sql("""
insert overwrite table dw_${country}.dwd_disty_brpt_orders_pl_etl_mi partition(dt_month = '${dt_month}')
select 
    date_flag,
    virtual_type,
    order_type,
    order_no,
    order_line_no,
    cust_no,
    mcust_no,
    cust_terr,
    cust_type,
    sales_rep,
    from_loc_no,
    terms,
    gv_user_type,
    sku_no,
    prod_code,
    vpl_no,
    vend_no,
    inv_type,
    base_cost,
    sales_cost,
    ship_qty,
    u_price,
    u_cost,
    u_sum_expense,
    l_weight,
    sales_total,
    cust_program_id,
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
    ngm_amt,
    oplgm_amt,
    ap_finance_calcproc,
    inv_cost_calcproc,
    inv_reserve_calcproc,
    cr_risk_cterm_calcproc,
    flr_synnex_calcproc,
    direct_credit_calcproc,
    csgn_edi_fee_calcproc,
    corporate_calcproc,
    sfs_calcproc,
    scm_risk_calcproc,
    flr_vendor_calcproc,
    cust_finance_sales_calcproc,
    cust_pmt_disc_calcproc,
    cvr_rm_calcproc,
    ar_fin_recovery_calcproc,
    mfg_oh_calcproc,
    cust_finance_calcproc,
    rma_calcproc,
    hc_sales_calcproc,
    order_overhead_calcproc,
    margin_share_calcproc,
    ap_adj_calcproc,
    pdt_calcproc,
    scm_cost_calcproc,
    infrastructure_calcproc,
    marketing_calcproc,
    coop_calcproc,
    one_time_btl_calcproc,
    hbtl_calcproc,
    scm_profit_adj_calcproc,
    hc_pm_calcproc,
    hc_bd_calcproc,
    btl_calcproc,
    btl_sales_calcproc,
    btl_backout_calcproc,
    cust_rebate_calcproc,
    mof_calcproc,
    frt_out_load_calcproc,
    frt_out_exp_calcproc,
    whoh_pack_calcproc,
    frt_ob_recovery_calcproc,
    frt_ib_recovery_calcproc,
    others_calcproc,
    others_sales_calcproc,
    scm_disc_calcproc,
    scm_ndisc_calcproc,
    frt_in_calcproc,
    trans_btl_calcproc,
    trans_btl_sales_calcproc,
    ngm_amt_calcproc,
    oplgm_amt_calcproc,
    company_no,
    etl_timestamp,
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
    adjust_group,
    dim_division,
    dim_cust_type,
    dim_terr_sub_group,
    dim_terr_group,
    dim_mcust_no,
    dim_seg_code,
    dim_master_vend_no,
    dim_vend_no,
    dim_vpc_group_id,
    dim_vpl_no,
    dim_group_id,
    dim_pm_id,
    dim_pm_mgr_id,
    dim_pm_dir_id,
    dim_pm_vp_id,
    dim_buyer_id,
    dim_buyer_mgr_id,
    dim_buyer_dir_id,
    dim_buyer_vp_id,
    segment_exclude,
    fx_cost,
    integrated_order_flag,
    biz_solution_flag,
    eu_loc_id,

    ( ( nvl(ship_qty,0) * (nvl(u_price,0) - coalesce(sales_cost,u_cost,0)) ) +
          nvl(btl,0) +
          nvl(hbtl,0) +
          nvl(one_time_btl,0) +
          nvl(btl_backout,0) +
          nvl(scm_profit_adj,0) +
          nvl(pdt,0) +
          nvl(frt_out_load,0) +
          nvl(frt_out_exp,0) +
          nvl(frt_ib_recovery,0) +
          nvl(ap_finance,0) +
          nvl(whoh_pack,0) +
          nvl(csgn_edi_fee,0) +
          (  nvl(cust_finance,0) * nvl(p.mcode * 1.0,0)/nvl((case when p.icode2=0 then 1 else p.icode2 end),0)  ) +
          nvl(cr_risk_cterm,0) +
          nvl(cust_pmt_disc,0) +
          nvl(cust_rebate,0) + nvl(cvr_rm,0) +
          nvl(rma,0) +
          nvl(mof,0) +
          nvl(order_overhead,0) +
          nvl(direct_credit,0) +
          nvl(flr_synnex,0) +
          nvl(others_sales,0) +
          nvl(others,0) ) as oplgm_plus_amt,
        '' as oplgm_plus_amt_calcproc
from (select * from dw_${country}.dwd_disty_brpt_orders_pl_etl_mi
      where dt_month = '${dt_month}') as a

left join (Select
             max(mcode) as mcode,
             max(icode2) as icode2
             from ods_${country}.ods_cis_corp_pl_code 
             where code_type = 'CFNR' and ccode = 'NGM' 
             and '${date_flag}' between nvl(start_date,'${date_flag}') and nvl(end_date,'${date_flag}') ) p
on  1 = 1
""")