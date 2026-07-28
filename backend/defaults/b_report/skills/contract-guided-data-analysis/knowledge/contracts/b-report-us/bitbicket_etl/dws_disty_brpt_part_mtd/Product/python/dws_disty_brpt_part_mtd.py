# -*- coding: utf-8 -*-
# @Time : 8/23/2023 10:37 AM
# @Author : Marvin Ma
# @File : dws_disty_brpt_part_mtd.py

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql


""" 
    生成上月分区，from mtd, 使用的是上月底的层次关系 得到的terr_sub_group terr_group sales PM
    生成本月分区，from 1d，使用当天最新的层次关系 得到的terr_sub_group terr_group sales PM   1d.date_flag=dim.date_flag
"""
# dw_{country}.dws_disty_brpt_pl_extend_mtd
# dw_{country}.dws_disty_brpt_bo_aging_df
# dw_{country}.dwd_disty_inv_aging_df
# ods_{country}.ods_breport_mydaas_dw_inv_type
# dw_{country}.dwd_disty_inv_qty_df


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):
    month_no = conf.get("month_no")
    main_sql = r"""
    with
    table_dwd as (
    select
    sku_no	        ,
    vpl_no	        ,
    vpc_group_id	,
    vend_no	        ,
    master_vend_no	,
    group_id	    ,
    seg_code	    ,
    nvl(company_no,1) as company_no,
    pm_id	        ,
    pm_mgr_id	    ,
    pm_dir_id	    ,
    pm_vp_id	    ,
    buyer_id	    ,
    buyer_mgr_id    ,
    buyer_dir_id    ,
    buyer_vp_id	    ,
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
    sum(fx_cost) as fx_cost
    from dw_{country}.dws_disty_brpt_pl_extend_mtd
    where date_flag = '{date_flag}'
    group by
    sku_no	        ,
    vpl_no	        ,
    vpc_group_id	,
    vend_no	        ,
    master_vend_no	,
    group_id	    ,
    seg_code	    ,
    nvl(company_no,1),
    pm_id	        ,
    pm_mgr_id	    ,
    pm_dir_id	    ,
    pm_vp_id	    ,
    buyer_id	    ,
    buyer_mgr_id    ,
    buyer_dir_id    ,
    buyer_vp_id	    ),

    table_tmp_inv as (
    select
    table_inv.sku_no,
    nvl(table_inv.company_no,1) as company_no,
    sum(case when nvl(table_inv_group.inv_group,'REG') = 'REG' then table_inv.ext_oh_cost + table_inv.ext_it_cost else 0 end) as reg_inv,
    sum(case when nvl(table_inv_group.inv_group,'REG') = 'REG' then table_inv.age1_30 else 0 end) as reg_inv_age0_30,
    sum(case when nvl(table_inv_group.inv_group,'REG') = 'REG' then table_inv.age31_60 else 0 end) as reg_inv_age31_60,
    sum(case when nvl(table_inv_group.inv_group,'REG') = 'REG' then table_inv.age61_90 else 0 end) as reg_inv_age61_90,
    sum(case when nvl(table_inv_group.inv_group,'REG') = 'REG' then table_inv.age90_up else 0 end) as reg_inv_age90_up,

    sum(case when table_inv_group.inv_group = 'RMA' then table_inv.ext_oh_cost + table_inv.ext_it_cost else 0 end) as rma_inv,
    sum(case when table_inv_group.inv_group = 'RMA' then table_inv.age1_30 else 0 end) as rma_inv_age0_30,
    sum(case when table_inv_group.inv_group = 'RMA' then table_inv.age31_60 else 0 end) as rma_inv_age31_60,
    sum(case when table_inv_group.inv_group = 'RMA' then table_inv.age61_90 else 0 end) as rma_inv_age61_90,
    sum(case when table_inv_group.inv_group = 'RMA' then table_inv.age90_up else 0 end) as rma_inv_age90_up
    from (select
          *
          from dw_{country}.dwd_disty_brpt_inv_aging_extend_df
          where date_flag = '{date_flag}') as table_inv
    inner join ods_{country}.ods_breport_mydaas_dw_inv_type as table_inv_group
    on table_inv.inv_type = table_inv_group.inv_type
    group by
    table_inv.sku_no,
    nvl(table_inv.company_no,1) ),

    table_tmp_inv2 as (
    select
        sku_no,
        nvl(company_no,1) as company_no,
        sum(oh_cost) as oh_cost,
        sum(oh_qty)  as oh_qty,
        sum(oo_cost) as oo_cost,
        sum(oo_qty)  as oo_qty,
        sum(p91_cost) as p91_cost
    from dw_{country}.dwd_disty_brpt_inv_aging_extend_df
    where date_flag = '{date_flag}'
    group by 
        sku_no,
        nvl(company_no,1) )

    insert overwrite table dw_{country}.dws_disty_brpt_part_mtd partition (date_flag = '{date_flag}')
    select
        {month_no},

        coalesce(table_dwd.sku_no,table_tmp_inv.sku_no,table_tmp_inv2.sku_no) as sku_no,
        null as part_no	        ,
        null as mfg_partno	    ,
        table_dwd.vpl_no,
        null as vpl_code	        ,
        table_dwd.vpc_group_id,
        null as vpc_group_desc	,
        table_dwd.vend_no,
        null as vend_name	        ,
        table_dwd.master_vend_no	,
        null as master_vend_name  ,
        table_dwd.group_id	        ,
        table_dwd.seg_code,
        coalesce(table_dwd.company_no,table_tmp_inv.company_no,table_tmp_inv2.company_no) as company_no        ,
        table_dwd.pm_id	            ,
        table_dwd.pm_mgr_id	        ,
        table_dwd.pm_dir_id	        ,
        table_dwd.pm_vp_id	        ,
        table_dwd.buyer_id	        ,
        table_dwd.buyer_mgr_id      ,
        table_dwd.buyer_dir_id      ,
        table_dwd.buyer_vp_id	    ,

        table_dwd.gross_sales,
        table_dwd.net_sales,
        table_dwd.gross_cost,
        table_dwd.net_cost,
        table_dwd.scm_usage,
        table_dwd.ds_sales,
        table_dwd.stock_sales,
        table_dwd.ds_cost,
        table_dwd.stock_cost,
        table_dwd.ds_scm_usage,
        table_dwd.stock_scm_usage,
        table_dwd.total_unit,
        table_dwd.total_weight,

        table_dwd.net_income,
        table_dwd.invest_capital,

        table_dwd.cgp,
        table_dwd.total_btl,
        table_dwd.tgm_amt,
        table_dwd.gm_amt,
        table_dwd.ngm_amt,
        table_dwd.oplgm_amt,

        table_dwd.bo_gross_sales,
        table_dwd.bo_gross_cost,
        table_dwd.bo_total_unit,
        table_dwd.bo_gm_amt,
        table_dwd.so_gross_sales,
        table_dwd.so_gross_cost,
        table_dwd.so_total_unit,
        table_dwd.so_gm_amt,
        table_dwd.bo_age0_7,
        table_dwd.bo_age8_14,
        table_dwd.bo_age15_21,
        table_dwd.bo_age21_up,
        table_dwd.so_age0_7,
        table_dwd.so_age8_14,
        table_dwd.so_age15_21,
        table_dwd.so_age21_up,

        table_tmp_inv.reg_inv,
        table_tmp_inv.reg_inv_age0_30,
        table_tmp_inv.reg_inv_age31_60,
        table_tmp_inv.reg_inv_age61_90,
        table_tmp_inv.reg_inv_age90_up,
        table_tmp_inv.rma_inv,
        table_tmp_inv.rma_inv_age0_30,
        table_tmp_inv.rma_inv_age31_60,
        table_tmp_inv.rma_inv_age61_90,
        table_tmp_inv.rma_inv_age90_up,
        table_tmp_inv2.oh_cost,
        table_tmp_inv2.oo_cost,
        table_tmp_inv2.oh_qty,
        table_tmp_inv2.oo_qty,

        table_dwd.rr_unit,
        table_dwd.rr_sales,
        table_dwd.rr_cost,
        table_dwd.rr_gm,
        table_dwd.rr_ngm,
        table_dwd.rr_opl,
        table_dwd.rr_cgp,
        table_dwd.rr_total_btl,
        table_dwd.rr_tgm,

        table_dwd.ap_finance,
        table_dwd.inv_cost,
        table_dwd.inv_reserve,
        table_dwd.cr_risk_cterm,
        table_dwd.flr_synnex,
        table_dwd.direct_credit,
        table_dwd.csgn_edi_fee,
        table_dwd.corporate,
        table_dwd.sfs,
        table_dwd.scm_risk,
        table_dwd.flr_vendor,
        table_dwd.cust_finance_sales,
        table_dwd.cust_pmt_disc,
        table_dwd.cvr_rm,
        table_dwd.ar_fin_recovery,
        table_dwd.mfg_oh,
        table_dwd.cust_finance,
        table_dwd.rma,
        table_dwd.hc_sales,
        table_dwd.order_overhead,
        table_dwd.margin_share,
        table_dwd.ap_adj,
        table_dwd.pdt,
        table_dwd.scm_cost,
        table_dwd.infrastructure,
        table_dwd.marketing,
        table_dwd.coop,
        table_dwd.one_time_btl,
        table_dwd.hbtl,
        table_dwd.scm_profit_adj,
        table_dwd.hc_pm,
        table_dwd.hc_bd,
        table_dwd.btl,
        table_dwd.btl_sales,
        table_dwd.btl_backout,
        table_dwd.cust_rebate,
        table_dwd.mof,
        table_dwd.frt_out_load,
        table_dwd.frt_out_exp,
        table_dwd.whoh_pack,
        table_dwd.frt_ob_recovery,
        table_dwd.frt_ib_recovery,
        table_dwd.others,
        table_dwd.others_sales,
        table_dwd.scm_disc,
        table_dwd.scm_ndisc,
        table_dwd.frt_in,
        table_dwd.trans_btl,
        table_dwd.trans_btl_sales,

        table_dwd.btl_sales_for_opl,
        table_dwd.trans_btl_sales_for_opl,
        table_dwd.pdt_for_opl,
        table_dwd.cust_rebate_for_opl,
        table_dwd.cvr_rm_for_opl,
        table_dwd.btl_backout_for_opl,
        table_dwd.cust_pmt_disc_for_opl,
        table_dwd.cust_finance_sales_for_opl,
        table_dwd.rma_for_opl,
        table_dwd.ar_fin_recovery_for_opl,
        table_dwd.order_overhead_for_opl,
        table_dwd.frt_out_exp_for_opl,
        table_dwd.frt_ob_recovery_for_opl,
        '{etl_timestamp}',
        table_tmp_inv2.p91_cost,
        table_dwd.fx_cost,
        table_dwd.oplgm_plus_amt,
        table_dwd.rr_oplgm_plus_amt
    from table_dwd
    full join table_tmp_inv
    on table_dwd.sku_no = table_tmp_inv.sku_no
    and table_dwd.company_no = table_tmp_inv.company_no

    full join table_tmp_inv2
    on  nvl(table_dwd.sku_no    ,table_tmp_inv.sku_no    ) = table_tmp_inv2.sku_no
    and nvl(table_dwd.company_no,table_tmp_inv.company_no) = table_tmp_inv2.company_no
    """.format(country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp=etl_timestamp,month_no=month_no)
    run_sql(main_sql)

    ############################################################# enrich after full join
    # 先用左表的维度补，如果左表的维度补不上，再走扩维那一套。
    run_sql("""
    insert overwrite table dw_${country}.dws_disty_brpt_part_mtd partition (date_flag = '${date_flag}')
    select 
        table_dwd.month_no,
        table_dwd.sku_no,
        table_dwd.part_no,
        table_dwd.mfg_partno,
        table_dwd.vpl_no,
        nvl(table_dwd.vpl_code,table_old_vpl.vpl_code),
        nvl(table_dwd.vpc_group_id,table_old_vpl.vpc_group_id),
        nvl(table_dwd.vpc_group_desc,table_old_vpl.vpc_group_desc),
        table_dwd.vend_no,
        nvl(table_dwd.vend_name,table_old_vend.vend_name),
        nvl(table_dwd.master_vend_no,table_old_vend.master_vend_no),
        nvl(table_dwd.master_vend_name,table_old_vend.master_vend_name),
        table_dwd.group_id,
        nvl(table_dwd.seg_code,table_old_vpl.seg_code),
        table_dwd.company_no,
        nvl(table_dwd.pm_id,table_old_vpl.pm_id),
        nvl(table_dwd.pm_mgr_id,table_old_vpl.pm_mgr_id),
        nvl(table_dwd.pm_dir_id,table_old_vpl.pm_dir_id),
        nvl(table_dwd.pm_vp_id,table_old_vpl.pm_vp_id),
        table_dwd.buyer_id,
        table_dwd.buyer_mgr_id,
        table_dwd.buyer_dir_id,
        table_dwd.buyer_vp_id,
        table_dwd.gross_sales,
        table_dwd.net_sales,
        table_dwd.gross_cost,
        table_dwd.net_cost,
        table_dwd.scm_usage,
        table_dwd.ds_sales,
        table_dwd.stock_sales,
        table_dwd.ds_cost,
        table_dwd.stock_cost,
        table_dwd.ds_scm_usage,
        table_dwd.stock_scm_usage,
        table_dwd.total_unit,
        table_dwd.total_weight,
        table_dwd.net_income,
        table_dwd.invest_capital,
        table_dwd.cgp,
        table_dwd.total_btl,
        table_dwd.tgm_amt,
        table_dwd.gm_amt,
        table_dwd.ngm_amt,
        table_dwd.oplgm_amt,
        table_dwd.bo_gross_sales,
        table_dwd.bo_gross_cost,
        table_dwd.bo_total_unit,
        table_dwd.bo_gm_amt,
        table_dwd.so_gross_sales,
        table_dwd.so_gross_cost,
        table_dwd.so_total_unit,
        table_dwd.so_gm_amt,
        table_dwd.bo_age0_7,
        table_dwd.bo_age8_14,
        table_dwd.bo_age15_21,
        table_dwd.bo_age21_up,
        table_dwd.so_age0_7,
        table_dwd.so_age8_14,
        table_dwd.so_age15_21,
        table_dwd.so_age21_up,
        table_dwd.reg_inv,
        table_dwd.reg_inv_age0_30,
        table_dwd.reg_inv_age31_60,
        table_dwd.reg_inv_age61_90,
        table_dwd.reg_inv_age90_up,
        table_dwd.rma_inv,
        table_dwd.rma_inv_age0_30,
        table_dwd.rma_inv_age31_60,
        table_dwd.rma_inv_age61_90,
        table_dwd.rma_inv_age90_up,
        table_dwd.oh_cost,
        table_dwd.oo_cost,
        table_dwd.oh_qty,
        table_dwd.oo_qty,
        table_dwd.rr_unit,
        table_dwd.rr_sales,
        table_dwd.rr_cost,
        table_dwd.rr_gm,
        table_dwd.rr_ngm,
        table_dwd.rr_opl,
        table_dwd.rr_cgp,
        table_dwd.rr_total_btl,
        table_dwd.rr_tgm,
        table_dwd.ap_finance,
        table_dwd.inv_cost,
        table_dwd.inv_reserve,
        table_dwd.cr_risk_cterm,
        table_dwd.flr_synnex,
        table_dwd.direct_credit,
        table_dwd.csgn_edi_fee,
        table_dwd.corporate,
        table_dwd.sfs,
        table_dwd.scm_risk,
        table_dwd.flr_vendor,
        table_dwd.cust_finance_sales,
        table_dwd.cust_pmt_disc,
        table_dwd.cvr_rm,
        table_dwd.ar_fin_recovery,
        table_dwd.mfg_oh,
        table_dwd.cust_finance,
        table_dwd.rma,
        table_dwd.hc_sales,
        table_dwd.order_overhead,
        table_dwd.margin_share,
        table_dwd.ap_adj,
        table_dwd.pdt,
        table_dwd.scm_cost,
        table_dwd.infrastructure,
        table_dwd.marketing,
        table_dwd.coop,
        table_dwd.one_time_btl,
        table_dwd.hbtl,
        table_dwd.scm_profit_adj,
        table_dwd.hc_pm,
        table_dwd.hc_bd,
        table_dwd.btl,
        table_dwd.btl_sales,
        table_dwd.btl_backout,
        table_dwd.cust_rebate,
        table_dwd.mof,
        table_dwd.frt_out_load,
        table_dwd.frt_out_exp,
        table_dwd.whoh_pack,
        table_dwd.frt_ob_recovery,
        table_dwd.frt_ib_recovery,
        table_dwd.others,
        table_dwd.others_sales,
        table_dwd.scm_disc,
        table_dwd.scm_ndisc,
        table_dwd.frt_in,
        table_dwd.trans_btl,
        table_dwd.trans_btl_sales,
        table_dwd.btl_sales_for_opl,
        table_dwd.trans_btl_sales_for_opl,
        table_dwd.pdt_for_opl,
        table_dwd.cust_rebate_for_opl,
        table_dwd.cvr_rm_for_opl,
        table_dwd.btl_backout_for_opl,
        table_dwd.cust_pmt_disc_for_opl,
        table_dwd.cust_finance_sales_for_opl,
        table_dwd.rma_for_opl,
        table_dwd.ar_fin_recovery_for_opl,
        table_dwd.order_overhead_for_opl,
        table_dwd.frt_out_exp_for_opl,
        table_dwd.frt_ob_recovery_for_opl,
        table_dwd.etl_timestamp,
        table_dwd.p91_cost,
        table_dwd.fx_cost,
        table_dwd.oplgm_plus_amt,
        table_dwd.rr_oplgm_plus_amt
    from (select *
          from dw_${country}.dws_disty_brpt_part_mtd 
          where date_flag = '${date_flag}') as table_dwd
    left join (select *
               from dim_${country}.dim_pub_part_info_df
               where date_flag = '${date_flag}') as table_part
    on table_dwd.sku_no = table_part.sku_no
    
    left join (select *
               from dim_${country}.dim_pub_vpl_info_df
               where date_flag = '${date_flag}') as table_vpl_tmp
    on table_part.vpl_no = table_vpl_tmp.vpl_no
    
    --
    left join (select *
                from (select
                          vend_no,
                          vend_name,
                          master_vend_no,
                          master_vend_name,
                          row_number() over(partition by vend_no order by master_vend_no) as rank --假如dave的表中存在一对多的情况，随便选一个
                      from dw_${country}.dws_disty_brpt_pl_extend_mtd
                      where date_flag = '${date_flag}'
                      group by
                          vend_no,
                          vend_name,
                          master_vend_no,
                          master_vend_name)
                where rank = 1) as table_old_vend
    on coalesce(table_dwd.vend_no,table_vpl_tmp.alt_vend_no,table_part.vend_no) = table_old_vend.vend_no
    
    left join (select *
                from (select
                          vpl_no,
                          vpl_code,
                          vpc_group_id,
                          vpc_group_desc,
                          pm_id,
                          pm_mgr_id,
                          pm_dir_id,
                          pm_vp_id,
                          seg_code,
                          row_number() over(partition by vpl_no order by vpc_group_id) as rank --假如dave的表中存在一对多的情况，随便选一个
                      from dw_${country}.dws_disty_brpt_pl_extend_mtd
                      where date_flag = '${date_flag}'
                      group by
                          vpl_no,
                          vpl_code,
                          vpc_group_id,
                          vpc_group_desc,
                          pm_id,
                          pm_mgr_id,
                          pm_dir_id,
                          pm_vp_id,
                          seg_code)
                where rank = 1) as table_old_vpl
    on coalesce(table_dwd.vpl_no,table_vpl_tmp.alt_vpl_no,table_part.vpl_no) = table_old_vpl.vpl_no
    """)

    run_sql("""
    insert overwrite table dw_${country}.dws_disty_brpt_part_mtd partition (date_flag = '${date_flag}')
    select 
        table_dwd.month_no,
        
        coalesce(table_dwd.sku_no,-3),
        table_part.part_no,
        table_part.mfg_partno,
        coalesce(table_dwd.vpl_no,table_vpl_tmp.alt_vpl_no,table_part.vpl_no,-3)  as vpl_no, --特殊逻辑和pl_extend_comb一致
        table_vpl.vpl_code,
        coalesce(table_dwd.vpc_group_id,table_vpl.vpc_group_id,-3)                as vpc_group_id, --特殊逻辑和pl_extend_comb一致
        table_vpl.vpc_group_desc,
        coalesce(table_dwd.vend_no,table_vpl_tmp.alt_vend_no,table_part.vend_no,-3) as vend_no, --特殊逻辑和pl_extend_comb一致
        table_vend.vend_name,
        coalesce(table_dwd.master_vend_no,table_vend.master_vend_no,-3)             as master_vend_no,
        table_mvend.cis_mk_name                                                     as master_vend_name,
        coalesce(table_dwd.group_id,table_part.group_id,-3)                         as group_id,
        coalesce(table_dwd.seg_code,  if(table_dim2.ccode is null,'OTH',nvl(table_vpl_tmp.alt_seg_code,table_vend.vend_seg_code)))                  as seg_code, --特殊逻辑和pl_extend_comb一致
        table_dwd.company_no,

        coalesce(table_dwd.pm_id,table_vpl_hierarchy.pm_id,table_vend_hierarchy.pm_id,-3)                           as pm_id,
        coalesce(table_dwd.pm_mgr_id,table_vpl_hierarchy.pm_manager_id,table_vend_hierarchy.pm_mgr_id,-3)           as pm_mgr_id,
        coalesce(table_dwd.pm_dir_id,table_vpl_hierarchy.pm_director_id,table_vend_hierarchy.pm_dir_id,-3)          as pm_dir_id,
        coalesce(table_dwd.pm_vp_id,table_vpl_hierarchy.pm_vp_id,table_vend_hierarchy.pm_vp_id,-3)                  as pm_vp_id,
        coalesce(table_dwd.buyer_id,table_vpl_hierarchy.buyer_id,table_vpl_hierarchy.pana_id,-3)                        as buyer_id,
        coalesce(table_dwd.buyer_mgr_id,table_vpl_hierarchy.buyer_manager_id,table_vpl_hierarchy.pana_manager_id,-3)    as buyer_mgr_id,
        coalesce(table_dwd.buyer_dir_id,table_vpl_hierarchy.buyer_director_id,table_vpl_hierarchy.pana_director_id,-3)  as buyer_dir_id,
        coalesce(table_dwd.buyer_vp_id,table_vpl_hierarchy.buyer_vp_id,table_vpl_hierarchy.pana_vp_id,-3)               as buyer_vp_id,

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
        nvl(table_dwd.reg_inv,0),
        nvl(table_dwd.reg_inv_age0_30,0),
        nvl(table_dwd.reg_inv_age31_60,0),
        nvl(table_dwd.reg_inv_age61_90,0),
        nvl(table_dwd.reg_inv_age90_up,0),
        nvl(table_dwd.rma_inv,0),
        nvl(table_dwd.rma_inv_age0_30,0),
        nvl(table_dwd.rma_inv_age31_60,0),
        nvl(table_dwd.rma_inv_age61_90,0),
        nvl(table_dwd.rma_inv_age90_up,0),
        nvl(table_dwd.oh_cost,0),
        nvl(table_dwd.oo_cost,0),
        nvl(table_dwd.oh_qty,0),
        nvl(table_dwd.oo_qty,0),
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
        table_dwd.etl_timestamp,
        nvl(table_dwd.p91_cost,0),
        nvl(table_dwd.fx_cost,0),
        table_dwd.oplgm_plus_amt,
        table_dwd.rr_oplgm_plus_amt
    from (select *
          from dw_${country}.dws_disty_brpt_part_mtd 
          where date_flag = '${date_flag}') as table_dwd
    left join (select *
               from dim_${country}.dim_pub_part_info_df
               where date_flag = '${date_flag}') as table_part
    on table_dwd.sku_no = table_part.sku_no
    
    left join (select *
               from dim_${country}.dim_pub_vpl_info_df
               where date_flag = '${date_flag}') as table_vpl_tmp
    on table_part.vpl_no = table_vpl_tmp.vpl_no
    
    left join (select *
               from dim_${country}.dim_pub_vpl_info_df
               where date_flag = '${date_flag}') as table_vpl
    on coalesce(table_dwd.vpl_no,table_vpl_tmp.alt_vpl_no,table_part.vpl_no) = table_vpl.vpl_no
    
    left join (select *
               from dim_${country}.dim_pub_vendor_info_df
               where date_flag = '${date_flag}') as table_vend
    on coalesce(table_dwd.vend_no,table_vpl_tmp.alt_vend_no,table_part.vend_no) = table_vend.vend_no
    
    left join (select *
               from dim_${country}.dim_pub_vendor_info_df
               where date_flag = '${date_flag}') as table_mvend
    on nvl(table_dwd.master_vend_no,table_vend.master_vend_no) = table_mvend.vend_no
    
    left join (select *
               from dim_${country}.dim_pub_vpl_hierarchy_info_df
               where date_flag = '${date_flag}') as table_vpl_hierarchy
    on coalesce(table_dwd.vpl_no,table_vpl_tmp.alt_vpl_no,table_part.vpl_no) = table_vpl_hierarchy.vpl_no
    
    left join (SELECT
                   vend_no,
                   MAX(CASE WHEN pm_dna_role = 'PM' AND in_vend_matrix = 'P' THEN pm_id ELSE - 3 END)              as pm_id,
                   MAX(CASE WHEN pm_dna_role = 'PM Team Manager' AND in_vend_matrix = 'M' THEN pm_id ELSE - 3 END) as pm_mgr_id,
                   MAX(CASE WHEN pm_dna_role = 'PM Director' AND in_vend_matrix = 'D' THEN pm_id ELSE - 3 END)     as pm_dir_id ,
                   MAX(CASE WHEN pm_dna_role = 'PM VP' AND in_vend_matrix = 'O' THEN pm_id ELSE - 3 END)           as pm_vp_id
               FROM ods_${country}.ods_etl_pm_vpc_matrix_df 
               where date_flag = '${date_flag}'
               and vpl_no = -1
               GROUP BY
                   vend_no) as table_vend_hierarchy
    on coalesce(table_dwd.vend_no,table_vpl_tmp.alt_vend_no,table_part.vend_no) = table_vend_hierarchy.vend_no
    
    left join (select *
               from ods_${country}.ods_cis_corp_pl_code
               where code_type = 'VSEG') as table_dim2
    on nvl(table_vpl_tmp.alt_seg_code,table_vend.vend_seg_code) = table_dim2.ccode
    """)


main()