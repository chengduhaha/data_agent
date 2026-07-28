# -*- coding: utf-8 -*-
# @Time : 8/4/2023 11:04 AM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql
from util.get_parameter_util import get_parameter, get_last_month_parameter
from util.time_util import yyyymmdd_to_date
from datetime import timedelta

""" 
    生成上月分区，from dwd_mi，使用的是上月底的层次关系 得到的terr_sub_group terr_group sales PM
    生成本月分区，from dwd_di，使用每天最新的层次关系 得到的terr_sub_group terr_group sales PM    dwd_di.date_flag=dim.date_flag
"""
"""
# sys.path.append(os.path.abspath((os.path.join(os.path.dirname(__file__), '../../'))))
# if lastrow is comment state: Azkaban-flow failed cause by [no module named Customer]
# if lastrow is not comment state: Azkaban-flow failed cause by [__file__ is not defined]
# So: should use [script.deps.python.path: "./py_module"]
"""

# dw_${country}.dwd_disty_brpt_orders_pl_di
# dim_${country}.dim_pub_part_info
# dim_${country}.dim_pub_vpl_info
# ods_${country}.ods_cis_corp_dw_vend_pl
# dim_${country}.dim_pub_customer_info
# ods_${country}.ods_cis_corp_cust_type
#
# dim_${country}.dim_pub_vpl_hierarchy_info
# ods_${country}.ods_cis_corp_vpc_group_xref
# ods_${country}.ods_cis_corp_vpc_group
# dim_${country}.dim_pub_vendor_info
#
# ods_${country}.ods_cis_corp_vendor_segment
# ods_${country}.ods_cis_corp_pl_code
#
#
#################################################### exec_1st_to_9th_per_month
# dw_${country}.dwd_disty_brpt_orders_pl_mi
# dim_{country}.dim_pub_sales_hierarchy_by_terr_user_role_df
# ods_{country}.ods_cis_corp_comm_tran_rules
#
# dim_${country}.dim_pub_part_info_df
# dim_${country}.dim_pub_vpl_info_df
# dim_${country}.dim_pub_customer_info_df
# dim_${country}.dim_pub_vpl_hierarchy_info_df
# dim_${country}.dim_pub_vendor_info_df


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    firstday_of_month = conf.get("firstday_of_month")  # firstday_of_month = date_flag's first day of month
    beg_date = conf.get("beg_date")  # beg_date = date_flag - 29
    flow_run_type = conf.get("flow_run_type")

    if flow_run_type == "1":
        (cur_mon, days, days_mtd, days_m, fin_cost_rate,
         gap_rate, after_tax_rate, invc, cfin, apfi,
         scma, emi, total_unvouch, total_intran_inv) = get_parameter(country, date_flag)
        where_condition_preposition = r"""
        from dw_{country}.dwd_disty_brpt_orders_pl_di
        where date_flag BETWEEN '{beg_date}' AND '{date_flag}'
        """.format(country=country, beg_date=beg_date, date_flag=date_flag)
        total_nsales, total_fin_cost, total_ap_finance, total_inv_cost = get_last_month_parameter(where_condition_preposition)

        source_table = "dw_{country}.dwd_disty_brpt_orders_pl_di".format(country=country)
        where_condition = "date_flag between '{firstday_of_month}' and '{date_flag}'".format(firstday_of_month=firstday_of_month, date_flag=date_flag)
        opl_columns = """
        sum( nvl(btl_sales,0) ) as btl_sales_for_opl,
        sum( nvl(trans_btl_sales,0) ) as trans_btl_sales_for_opl,
        sum( nvl(pdt,0) ) as pdt_for_opl,
        sum( nvl(cust_rebate,0) ) as cust_rebate_for_opl,
        sum( nvl(cvr_rm,0) ) as cvr_rm_for_opl,
        sum( nvl(btl_backout,0) ) as btl_backout_for_opl,
        sum( nvl(cust_pmt_disc,0) ) as cust_pmt_disc_for_opl,
        sum( nvl(cust_finance_sales,0) ) as cust_finance_sales_for_opl,
        sum( nvl(rma,0) ) as rma_for_opl,
        sum( nvl(ar_fin_recovery,0) ) as ar_fin_recovery_for_opl,
        sum( nvl(order_overhead,0) ) as order_overhead_for_opl,
        sum( nvl(frt_out_exp,0) ) as frt_out_exp_for_opl,
        sum( nvl(frt_ob_recovery,0) ) as frt_ob_recovery_for_opl"""

    elif flow_run_type == "11" or flow_run_type == "12":
        (cur_mon, days, days_mtd, days_m, fin_cost_rate,
         gap_rate, after_tax_rate, invc, cfin, apfi,
         scma, emi, total_unvouch, total_intran_inv) = get_parameter(country, date_flag)
        where_condition_preposition = r"""
        from dw_{country}.dwd_disty_brpt_orders_pl_mi
        where dt_month = '{dt_month}'
        """.format(country=country, dt_month=dt_month)
        (total_nsales, total_fin_cost, total_ap_finance, total_inv_cost) = get_last_month_parameter(where_condition_preposition)

        source_table = "dw_{country}.dwd_disty_brpt_orders_pl_mi".format(country=country)
        where_condition = "dt_month = '{dt_month}'".format(dt_month=dt_month)
        opl_columns = """
        sum( nvl(btl_sales_for_opl,0) ) as btl_sales_for_opl,
        sum( nvl(trans_btl_sales_for_opl,0) ) as trans_btl_sales_for_opl,
        sum( nvl(pdt_for_opl,0) ) as pdt_for_opl,
        sum( nvl(cust_rebate_for_opl,0) ) as cust_rebate_for_opl,
        sum( nvl(cvr_rm_for_opl,0) ) as cvr_rm_for_opl,
        sum( nvl(btl_backout_for_opl,0) ) as btl_backout_for_opl,
        sum( nvl(cust_pmt_disc_for_opl,0) ) as cust_pmt_disc_for_opl,
        sum( nvl(cust_finance_sales_for_opl,0) ) as cust_finance_sales_for_opl,
        sum( nvl(rma_for_opl,0) ) as rma_for_opl,
        sum( nvl(ar_fin_recovery_for_opl,0) ) as ar_fin_recovery_for_opl,
        sum( nvl(order_overhead_for_opl,0) ) as order_overhead_for_opl,
        sum( nvl(frt_out_exp_for_opl,0) ) as frt_out_exp_for_opl,
        sum( nvl(frt_ob_recovery_for_opl,0) ) as frt_ob_recovery_for_opl"""

    ###### 弃用非df表，全部使用df表。重跑不影响维度状态
    dim_pub_part_info = """
            (select *
            from dim_{country}.dim_pub_part_info_df
            where date_flag = '{date_flag}')""".format(country=country, date_flag=date_flag)
    dim_pub_vpl_info = """
            (select *
            from dim_{country}.dim_pub_vpl_info_df
            where date_flag = '{date_flag}')""".format(country=country, date_flag=date_flag)
    dim_pub_vpl_hierarchy_info = """
            (select *
            from dim_{country}.dim_pub_vpl_hierarchy_info_df
            where date_flag = '{date_flag}')""".format(country=country, date_flag=date_flag)
    dim_pub_vendor_info = """
            (select *
            from dim_{country}.dim_pub_vendor_info_df
            where date_flag = '{date_flag}')""".format(country=country, date_flag=date_flag)

    dim_pub_customer_info = r"""
            (select *,replace(cust_name,'\\\\','/') as cust_name_replace
            from dim_{country}.dim_pub_customer_info_df
            where date_flag = '{date_flag}')""".format(country=country,date_flag=date_flag)



    ####################################################################################### main sql begin at there
    run_sql("""
    create temporary table  temp_cust_xref_company stored as orc as
    select
    cx1.xref_no,
    cx1.cust_no,
        (
        select
        parameter_value
        from
            ods_${country}.ods_cis_corp_parameters
        where
            parameter_name = 'COMPANY_NO'
            and parameter_value = 1
            limit 1
            ) as company_no
    from (select * from ods_${country}.ods_etl_cust_xref_all_df
          where xref_type = 'AGENT_NO'
          and nvl(active,'Y') = 'Y' 
          and date_flag = '${date_flag}') as cx1
    --inner join (select * from ods_${country}.ods_breport_mydaas_breport_parameter
    --            where id = 'Apptis Customers') as dbp1
    --on cx1.cust_no = dbp1.icode
    where 1=2
    ;

    create temporary table  temp_mcust_no_clean stored as orc as
    select * from (
        select 
        cx.cust_no,cx.xref_no, 
        ROW_NUMBER () over (partition by cx.cust_no order by cx.entry_datetime desc) as r_no
        from ods_${country}.ods_etl_cust_xref_all_df cx
        where cx.xref_type = 'MASTER_SUB'
        and nvl(cx.active,'Y') = 'Y'
        and date_flag = '${date_flag}') t
    where t.r_no=1;
    """)
    ################################################################################ get alt_vpl_no
    run_sql("""
    with
    table_tmp as (
    select
        *,
        -- common & reusable logic. write here, used below.
        nvl(ship_qty,0) * (nvl(u_price,0) + nvl(u_sum_expense,0)) as net_sales,
        nvl(ship_qty,0) * (coalesce(sales_cost,u_cost,0) + nvl(u_sum_expense,0)) as net_cost,
        nvl(ship_qty,0) * (nvl(u_price,0) - coalesce(sales_cost,u_cost,0)) as gm_amt,
    
        nvl(ship_qty,0) * (nvl(u_price,0) - coalesce(sales_cost,u_cost,0))
        + nvl(btl,0)
        + nvl(one_time_btl,0)
        + nvl(hbtl,0)
        + nvl(scm_profit_adj,0)
        + nvl(btl_backout,0)
        + nvl(pdt,0) as cgp,
    
        nvl(btl, 0)
        + nvl(one_time_btl, 0)
        + nvl(btl_backout, 0)
        + nvl(hbtl, 0)
        + nvl(scm_profit_adj, 0) as total_btl,
    
        -- logic from https://git.synnex.org/users/marvin.ma_tdsynnex.com/repos/pub_dw/browse/public_order_dw/script/dws_disty_common_pl_ofcs_1d.sql#1
        (nvl(u_price,0) - coalesce(sales_cost,u_cost,0)) * nvl(ship_qty,0)
         + nvl(btl,0) + nvl(one_time_btl,0) + nvl(hbtl,0) + nvl(scm_profit_adj,0)
         + nvl(btl_backout,0) + nvl(pdt,0) + nvl(inv_reserve,0) + nvl(mof,0)
         + nvl(marketing,0) + nvl(frt_out_load,0) + nvl(frt_out_exp,0) + nvl(frt_ob_recovery,0)
         + nvl(frt_ib_recovery,0) + nvl(cust_pmt_disc,0) + nvl(cust_rebate,0) + nvl(cvr_rm,0)
         + nvl(ap_adj,0) + nvl(others,0)
         + (coalesce(sales_cost,u_cost,0) - nvl(u_cost,0)) * nvl(ship_qty,0) as tgm_amt
    from ${source_table}
    where ${where_condition}),
    
    table_dwd as (
    select
        nvl(cust_no,-3) as cust_no,
        nvl(cust_terr,-3) as cust_terr,
        nvl(cust_type,-3) as cust_type,
        nvl(sku_no,-3) as sku_no,
        nvl(vpl_no,-3) as vpl_no,
        nvl(vend_no,-3) as vend_no,
        nvl(company_no,1) as company_no,
    
        sum( nvl(ship_qty,0) * nvl(u_price,0) ) as gross_sales,
        sum( net_sales ) as net_sales,
        sum( nvl(ship_qty,0) * coalesce(sales_cost,u_cost,0) ) as gross_cost,
        sum( net_cost ) as net_cost,
        sum( nvl(ship_qty,0) * nvl(u_sum_expense,0) ) as scm_usage,
        sum(case when from_loc_no = 98 and inv_type in (100,200)      then nvl(ship_qty,0) * coalesce(sales_cost,u_cost,0) else 0 end) as ds_cost,
        sum(case when from_loc_no != 98 and inv_type not in (100,200) then nvl(ship_qty,0) * coalesce(sales_cost,u_cost,0) else 0 end) as stock_cost,
        sum(case when from_loc_no = 98 and inv_type in (100,200)      then nvl(ship_qty,0) * nvl(u_price,0)                else 0 end) as ds_sales,
        sum(case when from_loc_no != 98 and inv_type not in (100,200) then nvl(ship_qty,0) * nvl(u_price,0)                else 0 end) as stock_sales,
        sum(case when from_loc_no = 98 and inv_type in (100,200)      then nvl(ship_qty,0) * nvl(u_sum_expense,0)          else 0 end) as ds_scm_usage,
        sum(case when from_loc_no != 98 and inv_type not in (100,200) then nvl(ship_qty,0) * nvl(u_sum_expense,0)          else 0 end) as stock_scm_usage,
        sum(case when order_type = 114 then 0 else nvl(ship_qty,0) end ) as total_unit,
        sum( nvl(ship_qty,0) * nvl(l_weight,0) ) as total_weight,
        sum( nvl(ship_qty,0) * (coalesce(sales_cost,u_cost,0) - nvl(u_cost,0)) ) as fx_cost,
    
            ----------------------------------------------------------------------- from procedure ： load_b_report_fact
            sum( (nvl(ngm_amt, 0)
                  + nvl( ${fin_cost_rate}
                         * ${total_nsales}
                         * ( nvl(cust_finance, 0) + nvl(ar_fin_recovery, 0) + nvl(inv_cost, 0) + nvl(ap_finance, 0) + nvl(scm_cost, 0) )
                         / nvl(${total_fin_cost}, 0), 0)
                  + ${gap_rate} * (nvl(u_price,0) + nvl(u_sum_expense, 0)) * nvl(ship_qty,0) )
                  * ${after_tax_rate} )
            * 365 / ${days} as net_income,
            sum( nvl(CUST_FINANCE / nvl(${cfin}, 0), 0)
                 + nvl(AR_FIN_RECOVERY / nvl(${cfin}, 0), 0)
                 + nvl(INV_COST / nvl(${invc}, 0), 0)
                 - nvl(AP_FINANCE / nvl(${apfi}, 0), 0)
                 + nvl(SCM_COST / nvl(${scma}, 0), 0)
                 - nvl(${total_unvouch} * AP_FINANCE / nvl(${total_ap_finance}, 0), 0)
                 + nvl(${total_intran_inv}  * INV_COST / nvl(${total_inv_cost}, 0), 0)
                 + nvl(${emi} / nvl(${total_nsales}, 0) * (u_price + nvl(u_sum_expense, 0)) * ship_qty, 0) )
            * ${days_m} / ${days_mtd} as invest_capital,
            -----------------------------------------------------------------------
    
        sum( cgp ) as cgp,
        sum( total_btl ) as total_btl,
        sum( tgm_amt ) as tgm_amt,
        sum( gm_amt ) as gm_amt,
        sum( nvl(ngm_amt,0) ) as ngm_amt,
        sum( nvl(oplgm_amt,0) ) as oplgm_amt,
        sum( nvl(oplgm_plus_amt,0) ) as oplgm_plus_amt,
    
            sum(nvl(ship_qty,0)) * ${days_m} / ${days_mtd}  as rr_unit,
            ( sum(if(order_type <> 125, net_sales, 0)) * ${days_m} / ${days_mtd} 
                + sum(if(order_type = 125, net_sales, 0)) ) as rr_sales,
            sum(net_cost) * ${days_m} / ${days_mtd}         as rr_cost,
            sum(gm_amt) * ${days_m} / ${days_mtd}           as rr_gm,
            sum(nvl(ngm_amt,0)) * ${days_m} / ${days_mtd}   as rr_ngm,
            sum(nvl(oplgm_amt,0)) * ${days_m} / ${days_mtd} as rr_opl,
            sum(cgp) * ${days_m} / ${days_mtd}              as rr_cgp,
            sum(total_btl) * ${days_m} / ${days_mtd}        as rr_total_btl,
            sum(tgm_amt) * ${days_m} / ${days_mtd}          as rr_tgm,
            sum(oplgm_plus_amt) * ${days_m} / ${days_mtd}   as rr_oplgm_plus_amt,
    
        sum( nvl(ap_finance,0) ) as ap_finance,
        sum( nvl(inv_cost,0) ) as inv_cost,
        sum( nvl(inv_reserve,0) ) as inv_reserve,
        sum( nvl(cr_risk_cterm,0) ) as cr_risk_cterm,
        sum( nvl(flr_synnex,0) ) as flr_synnex,
        sum( nvl(direct_credit,0) ) as direct_credit,
        sum( nvl(csgn_edi_fee,0) ) as csgn_edi_fee,
        sum( nvl(corporate,0) ) as corporate,
        sum( nvl(sfs,0) ) as sfs,
        sum( nvl(scm_risk,0) ) as scm_risk,
        sum( nvl(flr_vendor,0) ) as flr_vendor,
        sum( nvl(cust_finance_sales,0) ) as cust_finance_sales,
        sum( nvl(cust_pmt_disc,0) ) as cust_pmt_disc,
        sum( nvl(cvr_rm,0) ) as cvr_rm,
        sum( nvl(ar_fin_recovery,0) ) as ar_fin_recovery,
        sum( nvl(mfg_oh,0) ) as mfg_oh,
        sum( nvl(cust_finance,0) ) as cust_finance,
        sum( nvl(rma,0) ) as rma,
        sum( nvl(hc_sales,0) ) as hc_sales,
        sum( nvl(order_overhead,0) ) as order_overhead,
        sum( nvl(margin_share,0) ) as margin_share,
        sum( nvl(ap_adj,0) ) as ap_adj,
        sum( nvl(pdt,0) ) as pdt,
        sum( nvl(scm_cost,0) ) as scm_cost,
        sum( nvl(infrastructure,0) ) as infrastructure,
        sum( nvl(marketing,0) ) as marketing,
        sum( nvl(coop,0) ) as coop,
        sum( nvl(one_time_btl,0) ) as one_time_btl,
        sum( nvl(hbtl,0) ) as hbtl,
        sum( nvl(scm_profit_adj,0) ) as scm_profit_adj,
        sum( nvl(hc_pm,0) ) as hc_pm,
        sum( nvl(hc_bd,0) ) as hc_bd,
        sum( nvl(btl,0) ) as btl,
        sum( nvl(btl_sales,0) ) as btl_sales,
        sum( nvl(btl_backout,0) ) as btl_backout,
        sum( nvl(cust_rebate,0) ) as cust_rebate,
        sum( nvl(mof,0) ) as mof,
        sum( nvl(frt_out_load,0) ) as frt_out_load,
        sum( nvl(frt_out_exp,0) ) as frt_out_exp,
        sum( nvl(whoh_pack,0) ) as whoh_pack,
        sum( nvl(frt_ob_recovery,0) ) as frt_ob_recovery,
        sum( nvl(frt_ib_recovery,0) ) as frt_ib_recovery,
        sum( nvl(others,0) ) as others,
        sum( nvl(others_sales,0) ) as others_sales,
        sum( nvl(scm_disc,0) ) as scm_disc,
        sum( nvl(scm_ndisc,0) ) as scm_ndisc,
        sum( nvl(frt_in,0) ) as frt_in,
        sum( nvl(trans_btl,0) ) as trans_btl,
        sum( nvl(trans_btl_sales,0) ) as trans_btl_sales,
            ${opl_columns}
    from table_tmp
    group by
        nvl(cust_no,-3),
        nvl(cust_terr,-3),
        nvl(cust_type,-3),
        nvl(sku_no,-3),
        nvl(vpl_no,-3),
        nvl(vend_no,-3),
        nvl(company_no,1) )

    insert overwrite table dw_${country}.dws_disty_brpt_pl_extend_mtd partition(date_flag = '${date_flag}')
    select
        ${month_no},

        nvl(table_dwd.cust_no,table_aging.cust_no)                             as cust_no,
        table_customer.cust_name_replace,
        coalesce(cxc.cust_no, dbp.icode1, cx.xref_no, table_customer.mcust_no) as mcust_no,
        null as mcust_name,
        nvl(table_dwd.cust_terr,table_aging.cust_terr)                         as cust_terr,
        table_terr.terr_name                                                   as terr_name,
        nvl(table_dwd.cust_type,table_aging.cust_type)                         as cust_type,
        table_cust_type.cust_type_descr as cust_type_desc,
        table_cust_type.division,
        table_div.division_desc,
        table_terr.sub_group_id           as terr_sub_group,
        table_terr.sub_group_desc         as terr_sub_group_desc,
        table_terr.group_id               as terr_group         ,
        table_terr.group_desc             as terr_group_desc    ,
    
        nvl(table1.sales_rep_id,-3)     as sales_rep_id,
        nvl(table2.manager_id,  -3)       as sales_sup_id,
        nvl(table3.manager_id,  -3)       as sales_mgr_id,
        nvl(table4.manager_id,  -3)       as sales_dir_id,
        nvl(table5.manager_id,  -3)       as sales_vp_id,
    
        coalesce(table_dwd.sku_no,table_aging.sku_no)         as sku_no,
        table_part.part_no,
        table_part.mfg_partno,
        case when coalesce(table_dwd.sku_no,table_aging.sku_no) >=0                                                        -- sku_no >= 0的情况，走普通的alt逻辑
             then nvl(table_part_vpl.alt_vpl_no,table_part.vpl_no)  
             when coalesce(table_dwd.sku_no,table_aging.sku_no) < 0 and table_dwd.vpl_no >= 0                              --sku_no<0,且vpl>=0的情况
             then nvl(table_vpl.alt_vpl_no,table_dwd.vpl_no)
             when coalesce(table_dwd.sku_no,table_aging.sku_no) < 0 and (table_dwd.vpl_no < 0 or table_dwd.vpl_no is null) --sku_no<0,且vpl<0或null的情况
             then -3
             else -3 end as vpl_no,  --alt之后的vpl_no
        null as vpl_code,
        null as vpc_group_id,
        null as vpc_group_desc,
        case when coalesce(table_dwd.sku_no,table_aging.sku_no) >=0                                                        -- sku_no >= 0的情况，走普通的alt逻辑
             then nvl(table_part_vpl.alt_vend_no,table_part_vpl.vend_no)
             when coalesce(table_dwd.sku_no,table_aging.sku_no) < 0 and table_dwd.vpl_no >= 0                              --sku_no<0,且vpl>=0 
             then nvl(table_vpl.alt_vend_no,table_dwd.vend_no)
             when coalesce(table_dwd.sku_no,table_aging.sku_no) < 0 and (table_dwd.vpl_no < 0 or table_dwd.vpl_no is null)  --sku_no<0,且vpl_no<0或null
             then table_dwd.vend_no
             else -3 end as vend_no, --alt之后的vend_no
        null as vend_name,
        null as master_vend_no,
        null as master_vend_name,
        table_part.group_id,
        nullif(table_part_vpl2.alt_seg_code, '') as seg_code,

        null as pm_id,
        null as pm_mgr_id,
        null as pm_dir_id,
        null as pm_vp_id,

        null as buyer_id,
        null as buyer_mgr_id,
        null as buyer_dir_id,
        null as buyer_vp_id,
    
        coalesce(table_dwd.company_no,table_aging.company_no) as company_no,
    
        table_dwd.gross_sales,
        table_dwd.net_sales,
        table_dwd.gross_cost,
        table_dwd.net_cost,
        table_dwd.scm_usage,
        table_dwd.ds_cost,
        table_dwd.stock_cost,
        table_dwd.ds_sales,
        table_dwd.stock_sales,
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
    
        '${etl_timestamp}',
        0 as p91_cost,-- p91_cost 应从sku vpl vend系列表中取，从cust+sku粒度的本表sum取是错的

        table_aging.bo_gross_sales,
        table_aging.bo_gross_cost,
        table_aging.bo_total_unit,
        table_aging.bo_gm_amt,
        table_aging.so_gross_sales,
        table_aging.so_gross_cost,
        table_aging.so_total_unit,
        table_aging.so_gm_amt,
        table_aging.bo_age0_7,
        table_aging.bo_age8_14,
        table_aging.bo_age15_21,
        table_aging.bo_age21_up,
        table_aging.so_age0_7,
        table_aging.so_age8_14,
        table_aging.so_age15_21,
        table_aging.so_age21_up,
        table_dwd.fx_cost,
        table_dwd.oplgm_plus_amt,
        table_dwd.rr_oplgm_plus_amt
    from table_dwd
    full join (select -- full join: 左表(月初至今日的汇总)是已发货的order,右表是未发货的order.有可能二者存在差集 所以要用fulljoin
               nvl(sku_no,-3) as sku_no,
               nvl(cust_no,-3) as cust_no,
               nvl(cust_terr,-3) as cust_terr,
               nvl(cust_type,-3) as cust_type,
               nvl(company_no, 1) as company_no,
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
               SUM(so_age21_up) as so_age21_up
               from dw_${country}.dws_disty_brpt_bo_aging_df
               where date_flag = '${date_flag}'
               group by
               nvl(sku_no,-3),
               nvl(cust_no,-3),
               nvl(cust_terr,-3),
               nvl(cust_type,-3),
               nvl(company_no,1) ) as table_aging
    on table_dwd.sku_no = table_aging.sku_no
    and table_dwd.cust_no = table_aging.cust_no
    and table_dwd.cust_terr = table_aging.cust_terr
    and table_dwd.cust_type = table_aging.cust_type
    and table_dwd.company_no = table_aging.company_no

    left join ${dim_pub_part_info} as table_part
    on coalesce(table_dwd.sku_no,table_aging.sku_no) = table_part.sku_no

    left join ${dim_pub_vpl_info} as table_part_vpl
    on table_part.vpl_no = table_part_vpl.vpl_no
    
    left join (select * from ods_${country}.ods_etl_dw_vend_pl_df where date_flag = '${date_flag}') as table_part_vpl2
    on table_part.vpl_no = table_part_vpl2.vpl_no

    left join ${dim_pub_vpl_info} as table_vpl
    on table_dwd.vpl_no = table_vpl.vpl_no

    --
    left join ${dim_pub_customer_info} as table_customer       -- unique id: cust_no
    on nvl(table_dwd.cust_no,table_aging.cust_no) = table_customer.cust_no

    left join ods_${country}.ods_cis_corp_cust_type as table_cust_type      --unique id: cust_type
    on nvl(table_dwd.cust_type,table_aging.cust_type) = table_cust_type.cust_type
    
    left join ods_${country}.ods_cis_corp_division as table_div
    on table_cust_type.division =  table_div.division
    
    
    left join (select * from dim_${country}.dim_pub_sales_territory_df where date_flag = '${date_flag}') as table_terr
    on nvl(table_dwd.cust_terr,table_aging.cust_terr) = table_terr.sales_terr
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_rep_terr_df
               where date_flag = '${date_flag}' and is_primary_rep = 'Y'
               and (end_date is null or end_date > current_timestamp()) ) as table1 --unique id : sales_terr
    on nvl(table_dwd.cust_terr,table_aging.cust_terr) = table1.sales_terr
    
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
    on nvl(table_dwd.cust_type,table_aging.cust_type) = table4.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'DIVISION'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table5  --unique id : dept_no
    on table_cust_type.division = table5.dept_no
    
    left join temp_mcust_no_clean cx
    on nvl(table_dwd.cust_no,table_aging.cust_no) = cx.cust_no
    left join (select profile_i as icode,cast(profile_f as int) as icode1
                from ods_${country}.ods_breport_mydaas_breport_parameter
               where param_type='Consolidated_report' 
                 and param_cat='Consolidated Mcust' 
                 and param_sub_cat='Consolidated Mcust' 
			     and profile_i <> cast(profile_f as int)) as dbp
    on table_customer.mcust_no = dbp.icode
    left join (select * from temp_cust_xref_company
               where company_no is not null) as cxc
    on nvl(table_dwd.cust_no,table_aging.cust_no) = cxc.xref_no
    """, country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp=etl_timestamp,
               fin_cost_rate=fin_cost_rate, total_nsales=total_nsales, total_fin_cost=total_fin_cost,
               gap_rate=gap_rate, after_tax_rate=after_tax_rate, days=days,
               days_m=days_m, days_mtd=days_mtd, cfin=cfin,
               invc=invc, apfi=apfi, scma=scma,
               total_unvouch=total_unvouch, total_ap_finance=total_ap_finance,
               total_intran_inv=total_intran_inv, total_inv_cost=total_inv_cost, emi=emi,
            source_table=source_table,
            where_condition=where_condition,
            opl_columns=opl_columns,
            dim_pub_part_info=dim_pub_part_info,
            dim_pub_vpl_info=dim_pub_vpl_info,
            dim_pub_vpl_hierarchy_info=dim_pub_vpl_hierarchy_info,
            dim_pub_vendor_info=dim_pub_vendor_info,
            dim_pub_customer_info=dim_pub_customer_info)

    ################################################################################# use alt_vpl_no to enrich dimension
    run_sql("""
    insert overwrite table dw_${country}.dws_disty_brpt_pl_extend_mtd partition(date_flag = '${date_flag}')
    select
    table_dwd.month_no,

    table_dwd.cust_no,
    table_dwd.cust_name,
    table_dwd.mcust_no,
    table_m_customer.cust_name_replace  as mcust_name,
    table_dwd.cust_terr,
    table_dwd.terr_name,
    table_dwd.cust_type,
    table_dwd.cust_type_desc,
    table_dwd.division,
    table_dwd.division_desc,
    table_dwd.terr_sub_group,
    table_dwd.sub_group_desc,
    table_dwd.terr_group,
    table_dwd.terr_group_desc,

    table_dwd.sales_rep_id,
    table_dwd.sales_sup_id,
    table_dwd.sales_mgr_id,
    table_dwd.sales_dir_id,
    table_dwd.sales_vp_id,

    table_dwd.sku_no,
    table_dwd.part_no,
    table_dwd.mfg_partno,
    table_dwd.vpl_no,
    table_vpl.vpl_code,
    table_vpl.vpc_group_id,
    table_vpl.vpc_group_desc,
    table_dwd.vend_no,
    table_vend.vend_name,
    table_vend.master_vend_no,
    table_master_vend.cis_mk_name as master_vend_name,
    table_dwd.group_id,
    coalesce(table_dwd.seg_code, nullif(table_vpl2.alt_seg_code,''), table_vend.vend_seg_code) as seg_code,

    nvl(table_vpl_hierarchy.pm_id,         table_vend_hierarchy.pm_id)       as pm_id,
    nvl(table_vpl_hierarchy.pm_manager_id, table_vend_hierarchy.pm_mgr_id)   as pm_mgr_id,
    nvl(table_vpl_hierarchy.pm_director_id,table_vend_hierarchy.pm_dir_id)   as pm_dir_id,
    nvl(table_vpl_hierarchy.pm_vp_id,      table_vend_hierarchy.pm_vp_id)    as pm_vp_id,
    nvl(table_vpl_hierarchy.buyer_id         ,table_vpl_hierarchy.pana_id )          as buyer_id,
    nvl(table_vpl_hierarchy.buyer_manager_id ,table_vpl_hierarchy.pana_manager_id )  as buyer_mgr_id,
    nvl(table_vpl_hierarchy.buyer_director_id,table_vpl_hierarchy.pana_director_id ) as buyer_dir_id,
    nvl(table_vpl_hierarchy.buyer_vp_id      ,table_vpl_hierarchy.pana_vp_id )       as buyer_vp_id,
    table_dwd.company_no,

    table_dwd.gross_sales,
    table_dwd.net_sales,
    table_dwd.gross_cost,
    table_dwd.net_cost,
    table_dwd.scm_usage,
    table_dwd.ds_cost,
    table_dwd.stock_cost,
    table_dwd.ds_sales,
    table_dwd.stock_sales,
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
    table_dwd.fx_cost,
    table_dwd.oplgm_plus_amt,
    table_dwd.rr_oplgm_plus_amt
    from (select * from dw_${country}.dws_disty_brpt_pl_extend_mtd
          where date_flag = '${date_flag}') as table_dwd

    left join ${dim_pub_vpl_info} as table_vpl
    on table_dwd.vpl_no = table_vpl.vpl_no
    
    left join (select * from ods_${country}.ods_etl_dw_vend_pl_df where date_flag = '${date_flag}') as table_vpl2
    on table_dwd.vpl_no = table_vpl2.vpl_no

    left join ${dim_pub_vpl_hierarchy_info} as table_vpl_hierarchy
    on table_dwd.vpl_no = table_vpl_hierarchy.vpl_no

    left join ${dim_pub_vendor_info} as table_vend
    on table_dwd.vend_no = table_vend.vend_no
    
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
    on table_dwd.vend_no = table_vend_hierarchy.vend_no
    
    left join ${dim_pub_vendor_info} as table_master_vend
    on table_vend.master_vend_no = table_master_vend.vend_no
    
    left join ${dim_pub_customer_info} as table_m_customer 
    on table_dwd.mcust_no = table_m_customer.cust_no
    """, source_table=source_table,
            where_condition=where_condition,
            opl_columns=opl_columns,
            dim_pub_part_info=dim_pub_part_info,
            dim_pub_vpl_info=dim_pub_vpl_info,
            dim_pub_vpl_hierarchy_info=dim_pub_vpl_hierarchy_info,
            dim_pub_vendor_info=dim_pub_vendor_info,
            dim_pub_customer_info=dim_pub_customer_info)

    ########################################################################################################## modify seg_code
    run_sql("""
    insert overwrite table dw_${country}.dws_disty_brpt_pl_extend_mtd partition(date_flag = '${date_flag}')
    select
    table_dwd.month_no,
    nvl(table_dwd.cust_no,-3),
    table_dwd.cust_name,
    nvl(table_dwd.mcust_no,-3),
    table_dwd.mcust_name,
    nvl(table_dwd.cust_terr,-3),
    table_dwd.terr_name,
    nvl(table_dwd.cust_type,-3),
    table_dwd.cust_type_desc,
    nvl(table_dwd.division,-3),
    table_dwd.division_desc,
    nvl(table_dwd.terr_sub_group,-3),
    table_dwd.sub_group_desc,
    nvl(table_dwd.terr_group,-3),
    table_dwd.terr_group_desc,
    nvl(table_dwd.sales_rep_id,-3),
    nvl(table_dwd.sales_sup_id,-3),
    nvl(table_dwd.sales_mgr_id,-3),
    nvl(table_dwd.sales_dir_id,-3),
    nvl(table_dwd.sales_vp_id,-3),
    
    nvl(table_dwd.sku_no,-3),
    table_dwd.part_no,
    table_dwd.mfg_partno,
    nvl(table_dwd.vpl_no,-3),
    table_dwd.vpl_code,
    nvl(table_dwd.vpc_group_id,-3),
    table_dwd.vpc_group_desc,
    nvl(table_dwd.vend_no,-3),
    table_dwd.vend_name,
    nvl(table_dwd.master_vend_no,-3),
    table_dwd.master_vend_name,
    nvl(table_dwd.group_id,-3),
    if(table_dim2.ccode is null,'OTH',table_dwd.seg_code) as seg_code,
    nvl(table_dwd.pm_id,-3),
    nvl(table_dwd.pm_mgr_id,-3),
    nvl(table_dwd.pm_dir_id,-3),
    nvl(table_dwd.pm_vp_id,-3),
    nvl(table_dwd.buyer_id,-3),
    nvl(table_dwd.buyer_mgr_id,-3),
    nvl(table_dwd.buyer_dir_id,-3),
    nvl(table_dwd.buyer_vp_id,-3),
    table_dwd.company_no,
    
    nvl(table_dwd.gross_sales,0),
    nvl(table_dwd.net_sales,0),
    nvl(table_dwd.gross_cost,0),
    nvl(table_dwd.net_cost,0),
    nvl(table_dwd.scm_usage,0),
    nvl(table_dwd.ds_cost,0),
    nvl(table_dwd.stock_cost,0),
    nvl(table_dwd.ds_sales,0),
    nvl(table_dwd.stock_sales,0),
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
    nvl(table_dwd.fx_cost,0),
    nvl(table_dwd.oplgm_plus_amt,0),
    nvl(table_dwd.rr_oplgm_plus_amt,0)
    from (select *
          from dw_${country}.dws_disty_brpt_pl_extend_mtd
          where date_flag = '${date_flag}'
          and (seg_code not in (select seg_code
                               from ods_${country}.ods_cis_corp_vendor_segment
                               where type_code = 'EXP/SER')
               or seg_code is null)) as table_dwd
    left join (select *
               from ods_${country}.ods_cis_corp_pl_code
               where code_type = 'VSEG') as table_dim2
    on table_dwd.seg_code = table_dim2.ccode
    """)


main()