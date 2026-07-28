# -*- coding: utf-8 -*-
# @Time : 3/29/2024 4:43 PM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):

    run_sql("""
    with
    table_dt_month as (
    select
        cust_no,
        mcust_no,
        cust_terr,
        cust_type,
        division,
        terr_sub_group,
        terr_group,
        sales_rep_id,
        sales_sup_id,
        sales_mgr_id,
        sales_dir_id,
        sales_vp_id,
        sku_no,
        vpl_no,
        vpc_group_id,
        vend_no,
        master_vend_no,
        group_id,
        seg_code,
        pm_id,
        pm_mgr_id,
        pm_dir_id,
        pm_vp_id,
        buyer_id,
        buyer_mgr_id,
        buyer_dir_id,
        buyer_vp_id,
        nvl(company_no,1) as company_no,
        sum(net_sales ) as m_sales,
        sum(net_cost ) as m_cost,
        sum(total_unit ) as m_unit,
        sum(gm_amt ) as m_gm,
        sum(ngm_amt ) as m_ngm,
        sum(oplgm_amt ) as m_opl,
        sum(oplgm_plus_amt) as m_oplgm_plus_amt,
        sum(scm_usage ) as m_scm_usage,
        sum(tgm_amt ) as m_tgm,
        sum(scm_disc ) as m_scm_disc,
        sum(scm_ndisc ) as m_scm_ndisc,
        sum(ds_sales ) as m_ds_sales,
        sum(stock_sales ) as m_stock_sales,
        sum(ds_cost ) as m_ds_cost,
        sum(stock_cost ) as m_stock_cost,
        sum(ds_scm_usage ) as m_ds_scm_usage,
        sum(stock_scm_usage ) as m_stock_scm_usage,
        sum(cgp ) as m_cgp,
        sum(total_btl ) as m_total_btl,
        sum(fx_cost ) as m_fx_cost,

        sum(rr_unit ) as rr_unit,
        sum(rr_sales ) as rr_sales,
        sum(rr_cost ) as rr_cost,
        sum(rr_gm ) as rr_gm,
        sum(rr_ngm ) as rr_ngm,
        sum(rr_opl ) as rr_opl,
        sum(rr_oplgm_plus_amt ) as rr_oplgm_plus_amt,
        sum(rr_cgp ) as rr_cgp,
        sum(rr_total_btl ) as rr_total_btl,
        sum(rr_tgm ) as rr_tgm,
        sum(p91_cost) as p91_cost,
        
        sum(bo_gross_sales ) as bo_gross_sales,
        sum(bo_gross_cost ) as bo_gross_cost,
        sum(bo_total_unit ) as bo_total_unit,
        sum(bo_gm_amt ) as bo_gm_amt,
        sum(so_gross_sales ) as so_gross_sales,
        sum(so_gross_cost ) as so_gross_cost,
        sum(so_total_unit ) as so_total_unit,
        sum(so_gm_amt ) as so_gm_amt,
        sum(bo_age0_7 ) as bo_age0_7,
        sum(bo_age8_14 ) as bo_age8_14,
        sum(bo_age15_21 ) as bo_age15_21,
        sum(bo_age21_up ) as bo_age21_up,
        sum(so_age0_7 ) as so_age0_7,
        sum(so_age8_14 ) as so_age8_14,
        sum(so_age15_21 ) as so_age15_21,
        sum(so_age21_up ) as so_age21_up,
        sum(fx_cost ) as fx_cost,
        sum(pdt) as m_pdt
    from dw_${country}.dws_disty_brpt_pl_extend_mtd
    where date_flag = '${date_flag}'
    group by
        cust_no,
        mcust_no,
        cust_terr,
        cust_type,
        division,
        terr_sub_group,
        terr_group,
        sales_rep_id,
        sales_sup_id,
        sales_mgr_id,
        sales_dir_id,
        sales_vp_id,
        sku_no,
        vpl_no,
        vpc_group_id,
        vend_no,
        master_vend_no,
        group_id,
        seg_code,
        pm_id,
        pm_mgr_id,
        pm_dir_id,
        pm_vp_id,
        buyer_id,
        buyer_mgr_id,
        buyer_dir_id,
        buyer_vp_id,
        nvl(company_no,1) ),

    table_last_dt_month as (
    select
        sku_no,
        vpl_no,
        vend_no,
        seg_code,
        cust_no,
        cust_terr,
        cust_type,
        nvl(company_no,1) as company_no,
        sum(case when date_flag = '${end_day_of_last_month}' then net_sales else 0 end) as pm_sales,
        sum(case when date_flag = '${end_day_of_last_month}' then net_cost else 0 end) as pm_cost,
        sum(case when date_flag = '${end_day_of_last_month}' then total_unit else 0 end) as pm_unit,
        sum(case when date_flag = '${end_day_of_last_month}' then gm_amt else 0 end) as pm_gm,
        sum(case when date_flag = '${end_day_of_last_month}' then ngm_amt else 0 end) as pm_ngm,
        sum(case when date_flag = '${end_day_of_last_month}' then oplgm_amt else 0 end) as pm_opl,
        sum(case when date_flag = '${end_day_of_last_month}' then oplgm_plus_amt else 0 end) as pm_oplgm_plus_amt,
        sum(case when date_flag = '${end_day_of_last_month}' then scm_usage else 0 end) as pm_scm_usage,
        sum(case when date_flag = '${end_day_of_last_month}' then tgm_amt else 0 end) as pm_tgm,
        sum(case when date_flag = '${end_day_of_last_month}' then scm_disc else 0 end) as pm_scm_disc,
        sum(case when date_flag = '${end_day_of_last_month}' then scm_ndisc else 0 end) as pm_scm_ndisc,
        sum(case when date_flag = '${end_day_of_last_month}' then ds_sales else 0 end) as pm_ds_sales,
        sum(case when date_flag = '${end_day_of_last_month}' then stock_sales else 0 end) as pm_stock_sales,
        sum(case when date_flag = '${end_day_of_last_month}' then ds_cost else 0 end) as pm_ds_cost,
        sum(case when date_flag = '${end_day_of_last_month}' then stock_cost else 0 end) as pm_stock_cost,
        sum(case when date_flag = '${end_day_of_last_month}' then ds_scm_usage else 0 end) as pm_ds_scm_usage,
        sum(case when date_flag = '${end_day_of_last_month}' then stock_scm_usage else 0 end) as pm_stock_scm_usage,
        sum(case when date_flag = '${end_day_of_last_month}' then cgp else 0 end) as pm_cgp,
        sum(case when date_flag = '${end_day_of_last_month}' then total_btl else 0 end) as pm_total_btl,
        sum(case when date_flag = '${end_day_of_last_month}' then fx_cost else 0 end) as pm_fx_cost,

        sum(case when date_flag = '${end_day_of_last_2month}' then net_sales else 0 end) as ppm_sales,
        sum(case when date_flag = '${end_day_of_last_2month}' then net_cost else 0 end) as ppm_cost,
        sum(case when date_flag = '${end_day_of_last_2month}' then total_unit else 0 end) as ppm_unit,
        sum(case when date_flag = '${end_day_of_last_2month}' then gm_amt else 0 end) as ppm_gm,
        sum(case when date_flag = '${end_day_of_last_2month}' then ngm_amt else 0 end) as ppm_ngm,
        sum(case when date_flag = '${end_day_of_last_2month}' then oplgm_amt else 0 end) as ppm_opl,
        sum(case when date_flag = '${end_day_of_last_2month}' then oplgm_plus_amt else 0 end) as ppm_oplgm_plus_amt,
        sum(case when date_flag = '${end_day_of_last_2month}' then scm_usage else 0 end) as ppm_scm_usage,
        sum(case when date_flag = '${end_day_of_last_2month}' then tgm_amt else 0 end) as ppm_tgm,
        sum(case when date_flag = '${end_day_of_last_2month}' then scm_disc else 0 end) as ppm_scm_disc,
        sum(case when date_flag = '${end_day_of_last_2month}' then scm_ndisc else 0 end) as ppm_scm_ndisc,
        sum(case when date_flag = '${end_day_of_last_2month}' then ds_sales else 0 end) as ppm_ds_sales,
        sum(case when date_flag = '${end_day_of_last_2month}' then stock_sales else 0 end) as ppm_stock_sales,
        sum(case when date_flag = '${end_day_of_last_2month}' then ds_cost else 0 end) as ppm_ds_cost,
        sum(case when date_flag = '${end_day_of_last_2month}' then stock_cost else 0 end) as ppm_stock_cost,
        sum(case when date_flag = '${end_day_of_last_2month}' then ds_scm_usage else 0 end) as ppm_ds_scm_usage,
        sum(case when date_flag = '${end_day_of_last_2month}' then stock_scm_usage else 0 end) as ppm_stock_scm_usage,
        sum(case when date_flag = '${end_day_of_last_2month}' then cgp else 0 end) as ppm_cgp,
        sum(case when date_flag = '${end_day_of_last_2month}' then total_btl else 0 end) as ppm_total_btl,
        sum(case when date_flag = '${end_day_of_last_2month}' then fx_cost else 0 end) as ppm_fx_cost
    from dw_${country}.dws_disty_brpt_pl_extend_mtd
    where date_flag in ('${end_day_of_last_2month}','${end_day_of_last_month}')
    group by
        sku_no,
        vpl_no,
        vend_no,
        seg_code,
        cust_no,
        cust_terr,
        cust_type,
        nvl(company_no,1) ),

    table_dt_month_last_year as (
    select
        sku_no,
        vpl_no,
        vend_no,
        seg_code,
        cust_no,
        cust_terr,
        cust_type,
        nvl(company_no,1) as company_no,
        sum(net_sales) as lm_sales,
        sum(net_cost) as lm_cost,
        sum(total_unit) as lm_unit,
        sum(gm_amt) as lm_gm,
        sum(ngm_amt) as lm_ngm,
        sum(oplgm_amt) as lm_opl,
        sum(oplgm_plus_amt) as lm_oplgm_plus_amt,
        sum(scm_usage) as lm_scm_usage,
        sum(tgm_amt) as lm_tgm,
        sum(scm_disc) as lm_scm_disc,
        sum(scm_ndisc) as lm_scm_ndisc,
        sum(ds_sales) as lm_ds_sales,
        sum(stock_sales) as lm_stock_sales,
        sum(ds_cost) as lm_ds_cost,
        sum(stock_cost) as lm_stock_cost,
        sum(ds_scm_usage) as lm_ds_scm_usage,
        sum(stock_scm_usage) as lm_stock_scm_usage,
        sum(cgp) as lm_cgp,
        sum(total_btl) as lm_total_btl,
        sum(fx_cost) as lm_fx_cost
    from dw_${country}.dws_disty_brpt_pl_extend_mtd
    where date_flag = '${end_day_of_same_month_of_last_year}'
    group by
        sku_no,
        vpl_no,
        vend_no,
        seg_code,
        cust_no,
        cust_terr,
        cust_type,
        nvl(company_no,1) ),

    table_1d as (
    select
        sku_no,
        vpl_no,
        vend_no,
        seg_code,
        cust_no,
        cust_terr,
        cust_type,
        nvl(company_no,1) as company_no,
        sum(case when date_flag = '${date_flag}' then net_sales else 0 end) as d_sales,
        sum(case when date_flag = '${date_flag}' then net_cost else 0 end) as d_cost,
        sum(case when date_flag = '${date_flag}' then total_unit else 0 end) as d_unit,
        sum(case when date_flag = '${date_flag}' then gm_amt else 0 end) as d_gm,
        sum(case when date_flag = '${date_flag}' then ngm_amt else 0 end) as d_ngm,
        sum(case when date_flag = '${date_flag}' then oplgm_amt else 0 end) as d_opl,
        sum(case when date_flag = '${date_flag}' then oplgm_plus_amt else 0 end) as d_oplgm_plus_amt,
        sum(case when date_flag = '${date_flag}' then scm_usage else 0 end) as d_scm_usage,
        sum(case when date_flag = '${date_flag}' then tgm_amt else 0 end) as d_tgm,
        sum(case when date_flag = '${date_flag}' then cgp else 0 end) as d_cgp,
        sum(case when date_flag = '${date_flag}' then total_btl else 0 end) as d_total_btl,
        sum(case when date_flag = '${date_flag}' then fx_cost else 0 end) as d_fx_cost,

        sum(net_sales) as w_sales,
        sum(net_cost) as w_cost,
        sum(total_unit) as w_unit,
        sum(gm_amt) as w_gm,
        sum(ngm_amt) as w_ngm,
        sum(oplgm_amt) as w_opl,
        sum(oplgm_plus_amt) as w_oplgm_plus_amt,
        sum(scm_usage) as w_scm_usage,
        sum(tgm_amt) as w_tgm,
        sum(cgp) as w_cgp,
        sum(total_btl) as w_total_btl,
        sum(fx_cost) as w_fx_cost
    from dw_${country}.dws_disty_brpt_pl_extend_1d
    where date_flag between '${week_begin_of_dateflag}' and '${date_flag}'
    group by
        sku_no,
        vpl_no,
        vend_no,
        seg_code,
        cust_no,
        cust_terr,
        cust_type,
        nvl(company_no,1) )

    insert overwrite table dw_${country}.dws_disty_brpt_pl_extend_comb_mtd partition(date_flag = '${date_flag}')
    select
        ${month_no},
        coalesce(table_dt_month.cust_no, table_last_dt_month.cust_no, table_dt_month_last_year.cust_no,table_1d.cust_no) as cust_no,
        null as cust_name,
        table_dt_month.mcust_no,
        null as mcust_name,
        coalesce(table_dt_month.cust_terr, table_last_dt_month.cust_terr, table_dt_month_last_year.cust_terr,table_1d.cust_terr) as cust_terr,
        null as terr_name,
        coalesce(table_dt_month.cust_type, table_last_dt_month.cust_type, table_dt_month_last_year.cust_type,table_1d.cust_type) as cust_type,
        null as cust_type_desc,
        table_dt_month.division,
        null as division_desc,
        table_dt_month.terr_sub_group,
        null as sub_group_desc,
        table_dt_month.terr_group,
        null as terr_group_desc,
        table_dt_month.sales_rep_id,
        table_dt_month.sales_sup_id,
        table_dt_month.sales_mgr_id,
        table_dt_month.sales_dir_id,
        table_dt_month.sales_vp_id,
        coalesce(table_dt_month.sku_no, table_last_dt_month.sku_no, table_dt_month_last_year.sku_no,table_1d.sku_no) as sku_no,
        null as part_no,
        null as mfg_partno,
        coalesce(table_dt_month.vpl_no, table_last_dt_month.vpl_no, table_dt_month_last_year.vpl_no,table_1d.vpl_no) as vpl_no,
        null as vpl_code,
        table_dt_month.vpc_group_id,
        null as vpc_group_desc,
        coalesce(table_dt_month.vend_no, table_last_dt_month.vend_no, table_dt_month_last_year.vend_no,table_1d.vend_no) as vend_no,
        null as vend_name,
        table_dt_month.master_vend_no,
        null as master_vend_name,
        table_dt_month.group_id,
        coalesce(table_dt_month.seg_code, table_last_dt_month.seg_code, table_dt_month_last_year.seg_code,table_1d.seg_code) as seg_code,
        table_dt_month.pm_id,
        table_dt_month.pm_mgr_id,
        table_dt_month.pm_dir_id,
        table_dt_month.pm_vp_id,
        table_dt_month.buyer_id,
        table_dt_month.buyer_mgr_id,
        table_dt_month.buyer_dir_id,
        table_dt_month.buyer_vp_id,
        coalesce(table_dt_month.company_no, table_last_dt_month.company_no, table_dt_month_last_year.company_no,table_1d.company_no) as company_no,

        table_1d.d_sales,
        table_1d.d_cost,
        table_1d.d_unit,
        table_1d.d_gm,
        table_1d.d_ngm,
        table_1d.d_opl,
        table_1d.d_scm_usage,
        table_1d.d_tgm,
        table_1d.d_cgp,
        table_1d.d_total_btl,

        table_1d.w_sales,
        table_1d.w_cost,
        table_1d.w_unit,
        table_1d.w_gm,
        table_1d.w_ngm,
        table_1d.w_opl,
        table_1d.w_scm_usage,
        table_1d.w_tgm,
        table_1d.w_cgp,
        table_1d.w_total_btl,

        table_dt_month.m_sales,
        table_dt_month.m_cost,
        table_dt_month.m_unit,
        table_dt_month.m_gm,
        table_dt_month.m_ngm,
        table_dt_month.m_opl,
        table_dt_month.m_scm_usage,
        table_dt_month.m_tgm,
        table_dt_month.m_scm_disc,
        table_dt_month.m_scm_ndisc,
        table_dt_month.m_ds_sales,
        table_dt_month.m_stock_sales,
        table_dt_month.m_ds_cost,
        table_dt_month.m_stock_cost,
        table_dt_month.m_ds_scm_usage,
        table_dt_month.m_stock_scm_usage,
        table_dt_month.m_cgp,
        table_dt_month.m_total_btl,

        table_last_dt_month.pm_sales,
        table_last_dt_month.pm_cost,
        table_last_dt_month.pm_unit,
        table_last_dt_month.pm_gm,
        table_last_dt_month.pm_ngm,
        table_last_dt_month.pm_opl,
        table_last_dt_month.pm_scm_usage,
        table_last_dt_month.pm_tgm,
        table_last_dt_month.pm_scm_disc,
        table_last_dt_month.pm_scm_ndisc,
        table_last_dt_month.pm_ds_sales,
        table_last_dt_month.pm_stock_sales,
        table_last_dt_month.pm_ds_cost,
        table_last_dt_month.pm_stock_cost,
        table_last_dt_month.pm_ds_scm_usage,
        table_last_dt_month.pm_stock_scm_usage,
        table_last_dt_month.pm_cgp,
        table_last_dt_month.pm_total_btl,

        table_last_dt_month.ppm_sales,
        table_last_dt_month.ppm_cost,
        table_last_dt_month.ppm_unit,
        table_last_dt_month.ppm_gm,
        table_last_dt_month.ppm_ngm,
        table_last_dt_month.ppm_opl,
        table_last_dt_month.ppm_scm_usage,
        table_last_dt_month.ppm_tgm,
        table_last_dt_month.ppm_scm_disc,
        table_last_dt_month.ppm_scm_ndisc,
        table_last_dt_month.ppm_ds_sales,
        table_last_dt_month.ppm_stock_sales,
        table_last_dt_month.ppm_ds_cost,
        table_last_dt_month.ppm_stock_cost,
        table_last_dt_month.ppm_ds_scm_usage,
        table_last_dt_month.ppm_stock_scm_usage,
        table_last_dt_month.ppm_cgp,
        table_last_dt_month.ppm_total_btl,

        table_dt_month_last_year.lm_sales,
        table_dt_month_last_year.lm_cost,
        table_dt_month_last_year.lm_unit,
        table_dt_month_last_year.lm_gm,
        table_dt_month_last_year.lm_ngm,
        table_dt_month_last_year.lm_opl,
        table_dt_month_last_year.lm_scm_usage,
        table_dt_month_last_year.lm_tgm,
        table_dt_month_last_year.lm_scm_disc,
        table_dt_month_last_year.lm_scm_ndisc,
        table_dt_month_last_year.lm_ds_sales,
        table_dt_month_last_year.lm_stock_sales,
        table_dt_month_last_year.lm_ds_cost,
        table_dt_month_last_year.lm_stock_cost,
        table_dt_month_last_year.lm_ds_scm_usage,
        table_dt_month_last_year.lm_stock_scm_usage,
        table_dt_month_last_year.lm_cgp,
        table_dt_month_last_year.lm_total_btl,

        table_dt_month.bo_gross_sales,
        table_dt_month.bo_gross_cost,
        table_dt_month.bo_total_unit,
        table_dt_month.bo_gm_amt,
        table_dt_month.so_gross_sales,
        table_dt_month.so_gross_cost,
        table_dt_month.so_total_unit,
        table_dt_month.so_gm_amt,
        table_dt_month.bo_age0_7,
        table_dt_month.bo_age8_14,
        table_dt_month.bo_age15_21,
        table_dt_month.bo_age21_up,
        table_dt_month.so_age0_7,
        table_dt_month.so_age8_14,
        table_dt_month.so_age15_21,
        table_dt_month.so_age21_up,

        table_dt_month.rr_unit,
        table_dt_month.rr_sales,
        table_dt_month.rr_cost,
        table_dt_month.rr_gm,
        table_dt_month.rr_ngm,
        table_dt_month.rr_opl,
        table_dt_month.rr_cgp,
        table_dt_month.rr_total_btl,
        table_dt_month.rr_tgm,
        '${etl_timestamp}',
        table_dt_month.p91_cost as m_p91_cost,
        table_1d.d_fx_cost,
        table_1d.w_fx_cost,
        table_dt_month.m_fx_cost,
        table_last_dt_month.pm_fx_cost,
        table_last_dt_month.ppm_fx_cost,
        table_dt_month_last_year.lm_fx_cost,
        table_dt_month.m_pdt,
        
        table_1d.d_oplgm_plus_amt,
        table_1d.w_oplgm_plus_amt,
        table_dt_month.m_oplgm_plus_amt,
        table_last_dt_month.pm_oplgm_plus_amt,
        table_last_dt_month.ppm_oplgm_plus_amt,
        table_dt_month_last_year.lm_oplgm_plus_amt,
        table_dt_month.rr_oplgm_plus_amt
    from table_dt_month
    full join table_last_dt_month
    on table_dt_month.sku_no = table_last_dt_month.sku_no
    and table_dt_month.vpl_no = table_last_dt_month.vpl_no
    and table_dt_month.vend_no = table_last_dt_month.vend_no
    and table_dt_month.seg_code = table_last_dt_month.seg_code
    and table_dt_month.cust_no = table_last_dt_month.cust_no
    and table_dt_month.cust_terr = table_last_dt_month.cust_terr
    and table_dt_month.cust_type = table_last_dt_month.cust_type
    and table_dt_month.company_no = table_last_dt_month.company_no

    full join table_dt_month_last_year
    on  nvl(table_dt_month.sku_no    ,table_last_dt_month.sku_no    ) = table_dt_month_last_year.sku_no
    and nvl(table_dt_month.vpl_no    ,table_last_dt_month.vpl_no    ) = table_dt_month_last_year.vpl_no
    and nvl(table_dt_month.vend_no   ,table_last_dt_month.vend_no   ) = table_dt_month_last_year.vend_no
    and nvl(table_dt_month.seg_code  ,table_last_dt_month.seg_code  ) = table_dt_month_last_year.seg_code
    and nvl(table_dt_month.cust_no   ,table_last_dt_month.cust_no   ) = table_dt_month_last_year.cust_no
    and nvl(table_dt_month.cust_terr ,table_last_dt_month.cust_terr ) = table_dt_month_last_year.cust_terr
    and nvl(table_dt_month.cust_type ,table_last_dt_month.cust_type ) = table_dt_month_last_year.cust_type
    and nvl(table_dt_month.company_no,table_last_dt_month.company_no) = table_dt_month_last_year.company_no

    full join table_1d
    on  coalesce(table_dt_month.sku_no    ,table_last_dt_month.sku_no    ,table_dt_month_last_year.sku_no    ) = table_1d.sku_no
    and coalesce(table_dt_month.vpl_no    ,table_last_dt_month.vpl_no    ,table_dt_month_last_year.vpl_no    ) = table_1d.vpl_no
    and coalesce(table_dt_month.vend_no   ,table_last_dt_month.vend_no   ,table_dt_month_last_year.vend_no   ) = table_1d.vend_no
    and coalesce(table_dt_month.seg_code  ,table_last_dt_month.seg_code  ,table_dt_month_last_year.seg_code  ) = table_1d.seg_code
    and coalesce(table_dt_month.cust_no   ,table_last_dt_month.cust_no   ,table_dt_month_last_year.cust_no   ) = table_1d.cust_no
    and coalesce(table_dt_month.cust_terr ,table_last_dt_month.cust_terr ,table_dt_month_last_year.cust_terr ) = table_1d.cust_terr
    and coalesce(table_dt_month.cust_type ,table_last_dt_month.cust_type ,table_dt_month_last_year.cust_type ) = table_1d.cust_type
    and coalesce(table_dt_month.company_no,table_last_dt_month.company_no,table_dt_month_last_year.company_no) = table_1d.company_no
    """)

    ################################################################################# enrich after full join
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

    run_sql("""
    insert overwrite table dw_${country}.dws_disty_brpt_pl_extend_comb_mtd partition(date_flag = '${date_flag}')
    select 
    table_dwd.month_no,
    
    nvl(table_dwd.cust_no,-3),
    table_customer.cust_name_replace,
    coalesce(table_dwd.mcust_no,cxc.cust_no, dbp.icode1, cx.xref_no, table_customer.mcust_no, -3) as mcust_no,--特殊逻辑和pl_extend_comb一致
    table_mcustomer.cust_name_replace                                       as mcust_name,
    nvl(table_dwd.cust_terr,-3)                                             as cust_terr, 
    table_terr.terr_name                                                    as terr_name,
    nvl(table_dwd.cust_type,-3)                                             as cust_type,
    table_cust_type.cust_type_descr                                         as cust_type_desc,
    coalesce(table_dwd.division,table_cust_type.division,-3)                as division,
    table_div.division_desc                                                 as division_desc,
    coalesce(table_dwd.terr_sub_group,table_terr.sub_group_id,-3)           as terr_sub_group,
    table_sub_group.sub_group_desc                                          as terr_sub_group_desc,
    coalesce(table_dwd.terr_group,table_terr.group_id,-3)                   as terr_group,
    table_group.group_desc                                                  as terr_group_desc,

    coalesce(table_dwd.sales_rep_id,table1.sales_rep_id,-3)        as sales_rep_id,
    coalesce(table_dwd.sales_sup_id,table2.manager_id,  -3)          as sales_sup_id,
    coalesce(table_dwd.sales_mgr_id,table3.manager_id,  -3)          as sales_mgr_id,
    coalesce(table_dwd.sales_dir_id,table4.manager_id,  -3)          as sales_dir_id,
    coalesce(table_dwd.sales_vp_id ,table5.manager_id,  -3)          as sales_vp_id,
    
    nvl(table_dwd.sku_no,-3)                                            as sku_no,
    table_part.part_no                                                  as part_no,
    table_part.mfg_partno                                               as mfg_partno,
    nvl(table_dwd.vpl_no,-3)                                            as vpl_no, --特殊逻辑和pl_extend_comb一致
    table_vpl.vpl_code                                                  as vpl_code,
    coalesce(table_dwd.vpc_group_id,table_vpl.vpc_group_id,-3)          as vpc_group_id, --特殊逻辑和pl_extend_comb一致
    table_vpl.vpc_group_desc                                            as vpc_group_desc,
    nvl(table_dwd.vend_no,-3)                                           as vend_no, --特殊逻辑和pl_extend_comb一致
    table_vend.vend_name                                                as vend_name,
    coalesce(table_dwd.master_vend_no,table_vend.master_vend_no,-3)     as master_vend_no,
    table_mvend.cis_mk_name                                             as master_vend_name,
    coalesce(table_dwd.group_id,table_part.group_id,-3)                 as group_id,
    table_dwd.seg_code                                                  as seg_code, --特殊逻辑和pl_extend_comb一致

    coalesce(table_dwd.pm_id,table_vpl_hierarchy.pm_id,table_vend_hierarchy.pm_id,-3)                           as pm_id,
    coalesce(table_dwd.pm_mgr_id,table_vpl_hierarchy.pm_manager_id,table_vend_hierarchy.pm_mgr_id,-3)           as pm_mgr_id,
    coalesce(table_dwd.pm_dir_id,table_vpl_hierarchy.pm_director_id,table_vend_hierarchy.pm_dir_id,-3)          as pm_dir_id,
    coalesce(table_dwd.pm_vp_id,table_vpl_hierarchy.pm_vp_id,table_vend_hierarchy.pm_vp_id,-3)                  as pm_vp_id,
    coalesce(table_dwd.buyer_id,table_vpl_hierarchy.buyer_id,table_vpl_hierarchy.pana_id,-3)                            as buyer_id,
    coalesce(table_dwd.buyer_mgr_id,table_vpl_hierarchy.buyer_manager_id,table_vpl_hierarchy.pana_manager_id,-3)        as buyer_mgr_id,
    coalesce(table_dwd.buyer_dir_id,table_vpl_hierarchy.buyer_director_id,table_vpl_hierarchy.pana_director_id-3)       as buyer_dir_id,
    coalesce(table_dwd.buyer_vp_id,table_vpl_hierarchy.buyer_vp_id,table_vpl_hierarchy.pana_vp_id,-3)                   as buyer_vp_id,
    table_dwd.company_no,
    
    nvl(table_dwd.d_sales,0),
    nvl(table_dwd.d_cost,0),
    nvl(table_dwd.d_unit,0),
    nvl(table_dwd.d_gm,0),
    nvl(table_dwd.d_ngm,0),
    nvl(table_dwd.d_opl,0),
    nvl(table_dwd.d_scm_usage,0),
    nvl(table_dwd.d_tgm,0),
    nvl(table_dwd.d_cgp,0),
    nvl(table_dwd.d_total_btl,0),
    nvl(table_dwd.w_sales,0),
    nvl(table_dwd.w_cost,0),
    nvl(table_dwd.w_unit,0),
    nvl(table_dwd.w_gm,0),
    nvl(table_dwd.w_ngm,0),
    nvl(table_dwd.w_opl,0),
    nvl(table_dwd.w_scm_usage,0),
    nvl(table_dwd.w_tgm,0),
    nvl(table_dwd.w_cgp,0),
    nvl(table_dwd.w_total_btl,0),
    nvl(table_dwd.m_sales,0),
    nvl(table_dwd.m_cost,0),
    nvl(table_dwd.m_unit,0),
    nvl(table_dwd.m_gm,0),
    nvl(table_dwd.m_ngm,0),
    nvl(table_dwd.m_opl,0),
    nvl(table_dwd.m_scm_usage,0),
    nvl(table_dwd.m_tgm,0),
    nvl(table_dwd.m_scm_disc,0),
    nvl(table_dwd.m_scm_ndisc,0),
    nvl(table_dwd.m_ds_sales,0),
    nvl(table_dwd.m_stock_sales,0),
    nvl(table_dwd.m_ds_cost,0),
    nvl(table_dwd.m_stock_cost,0),
    nvl(table_dwd.m_ds_scm_usage,0),
    nvl(table_dwd.m_stock_scm_usage,0),
    nvl(table_dwd.m_cgp,0),
    nvl(table_dwd.m_total_btl,0),
    nvl(table_dwd.pm_sales,0),
    nvl(table_dwd.pm_cost,0),
    nvl(table_dwd.pm_unit,0),
    nvl(table_dwd.pm_gm,0),
    nvl(table_dwd.pm_ngm,0),
    nvl(table_dwd.pm_opl,0),
    nvl(table_dwd.pm_scm_usage,0),
    nvl(table_dwd.pm_tgm,0),
    nvl(table_dwd.pm_scm_disc,0),
    nvl(table_dwd.pm_scm_ndisc,0),
    nvl(table_dwd.pm_ds_sales,0),
    nvl(table_dwd.pm_stock_sales,0),
    nvl(table_dwd.pm_ds_cost,0),
    nvl(table_dwd.pm_stock_cost,0),
    nvl(table_dwd.pm_ds_scm_usage,0),
    nvl(table_dwd.pm_stock_scm_usage,0),
    nvl(table_dwd.pm_cgp,0),
    nvl(table_dwd.pm_total_btl,0),
    nvl(table_dwd.ppm_sales,0),
    nvl(table_dwd.ppm_cost,0),
    nvl(table_dwd.ppm_unit,0),
    nvl(table_dwd.ppm_gm,0),
    nvl(table_dwd.ppm_ngm,0),
    nvl(table_dwd.ppm_opl,0),
    nvl(table_dwd.ppm_scm_usage,0),
    nvl(table_dwd.ppm_tgm,0),
    nvl(table_dwd.ppm_scm_disc,0),
    nvl(table_dwd.ppm_scm_ndisc,0),
    nvl(table_dwd.ppm_ds_sales,0),
    nvl(table_dwd.ppm_stock_sales,0),
    nvl(table_dwd.ppm_ds_cost,0),
    nvl(table_dwd.ppm_stock_cost,0),
    nvl(table_dwd.ppm_ds_scm_usage,0),
    nvl(table_dwd.ppm_stock_scm_usage,0),
    nvl(table_dwd.ppm_cgp,0),
    nvl(table_dwd.ppm_total_btl,0),
    nvl(table_dwd.lm_sales,0),
    nvl(table_dwd.lm_cost,0),
    nvl(table_dwd.lm_unit,0),
    nvl(table_dwd.lm_gm,0),
    nvl(table_dwd.lm_ngm,0),
    nvl(table_dwd.lm_opl,0),
    nvl(table_dwd.lm_scm_usage,0),
    nvl(table_dwd.lm_tgm,0),
    nvl(table_dwd.lm_scm_disc,0),
    nvl(table_dwd.lm_scm_ndisc,0),
    nvl(table_dwd.lm_ds_sales,0),
    nvl(table_dwd.lm_stock_sales,0),
    nvl(table_dwd.lm_ds_cost,0),
    nvl(table_dwd.lm_stock_cost,0),
    nvl(table_dwd.lm_ds_scm_usage,0),
    nvl(table_dwd.lm_stock_scm_usage,0),
    nvl(table_dwd.lm_cgp,0),
    nvl(table_dwd.lm_total_btl,0),
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
    table_dwd.etl_timestamp,
    nvl(table_dwd.m_p91_cost,0),
    nvl(table_dwd.d_fx_cost,0),
    nvl(table_dwd.w_fx_cost,0),
    nvl(table_dwd.m_fx_cost,0),
    nvl(table_dwd.pm_fx_cost,0),
    nvl(table_dwd.ppm_fx_cost,0),
    nvl(table_dwd.lm_fx_cost,0),
    nvl(table_dwd.m_pdt,0),
    
    nvl(table_dwd.d_oplgm_plus_amt,0),
    nvl(table_dwd.w_oplgm_plus_amt,0),
    nvl(table_dwd.m_oplgm_plus_amt,0),
    nvl(table_dwd.pm_oplgm_plus_amt,0),
    nvl(table_dwd.ppm_oplgm_plus_amt,0),
    nvl(table_dwd.lm_oplgm_plus_amt,0),
    nvl(table_dwd.rr_oplgm_plus_amt,0)
    from (select * from dw_${country}.dws_disty_brpt_pl_extend_comb_mtd
          where date_flag = '${date_flag}') as table_dwd
    left join (select *,replace(cust_name,'\\\\','/') as cust_name_replace
               from dim_${country}.dim_pub_customer_info_df
               where date_flag = '${date_flag}') as table_customer                     -- unique id: cust_no
    on table_dwd.cust_no = table_customer.cust_no
    
    left join temp_mcust_no_clean cx
    on table_dwd.cust_no = cx.cust_no
    left join (select profile_i as icode,cast(profile_f as int) as icode1
                from ods_${country}.ods_breport_mydaas_breport_parameter
               where param_type='Consolidated_report' 
                 and param_cat='Consolidated Mcust' 
                 and param_sub_cat='Consolidated Mcust' 
			     and profile_i <> cast(profile_f as int)) as dbp
    on table_customer.mcust_no = dbp.icode
    left join (select * from temp_cust_xref_company
               where company_no is not null) as cxc
    on table_dwd.cust_no = cxc.xref_no
    
    left join (select *,replace(cust_name,'\\\\','/') as cust_name_replace
               from dim_${country}.dim_pub_customer_info_df
               where date_flag = '${date_flag}') as table_mcustomer                     -- unique id: cust_no
    on coalesce(table_dwd.mcust_no,cxc.cust_no, dbp.icode1, cx.xref_no, table_customer.mcust_no) = table_mcustomer.cust_no
    
    left join ods_${country}.ods_cis_corp_cust_type as table_cust_type      --unique id: cust_type
    on table_dwd.cust_type = table_cust_type.cust_type
    
    left join ods_${country}.ods_cis_corp_division as table_div
    on nvl(table_dwd.division,table_cust_type.division) =  table_div.division
    
    left join (select * from dim_${country}.dim_pub_sales_territory_df where date_flag = '${date_flag}') as table_terr
    on table_dwd.cust_terr = table_terr.sales_terr
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_rep_terr_df
               where date_flag = '${date_flag}' and is_primary_rep = 'Y'
               and (end_date is null or end_date > current_timestamp()) ) as table1 --unique id : sales_terr
    on table_dwd.cust_terr = table1.sales_terr
    
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
    on table_dwd.cust_type = table4.dept_no
    
    left join (select
               *
               from dim_${country}.dim_pub_sales_mgr_dept_df
               where date_flag = '${date_flag}' and dept_level = 'DIVISION'
               and seq_id = 0
               and (end_date is null or end_date > current_timestamp()) ) as table5  --unique id : dept_no
    on nvl(table_dwd.division,table_cust_type.division) = table5.dept_no
    
    left join ods_${country}.ods_cis_corp_territory_sub_group as table_sub_group
    on nvl(table_dwd.terr_sub_group,table_terr.sub_group_id) = table_sub_group.sub_group_id
    
    left join ods_${country}.ods_cis_corp_territory_group as table_group
    on nvl(table_dwd.terr_group,table_terr.group_id) = table_group.group_id

    --
    left join (select *
               from dim_${country}.dim_pub_part_info_df
               where date_flag = '${date_flag}') as table_part
    on table_dwd.sku_no = table_part.sku_no

    left join (select *
               from dim_${country}.dim_pub_vpl_info_df
               where date_flag = '${date_flag}') as table_vpl
    on table_dwd.vpl_no = table_vpl.vpl_no
    
    left join (select *
               from dim_${country}.dim_pub_vendor_info_df
               where date_flag = '${date_flag}') as table_vend
    on table_dwd.vend_no = table_vend.vend_no
    
    left join (select *
               from dim_${country}.dim_pub_vendor_info_df
               where date_flag = '${date_flag}') as table_mvend
    on nvl(table_dwd.master_vend_no,table_vend.master_vend_no) = table_mvend.vend_no
    
    left join (select *
               from dim_${country}.dim_pub_vpl_hierarchy_info_df
               where date_flag = '${date_flag}') as table_vpl_hierarchy
    on table_dwd.vpl_no = table_vpl_hierarchy.vpl_no
    
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
    """)


main()
