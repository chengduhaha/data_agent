# -*- coding: utf-8 -*-
# @Time : 9/12/2023 2:45 PM
# @Author : Marvin Ma


from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql
# dw_{country}.dws_disty_brpt_bd_proj_task_mtd
# dw_{country}.dws_disty_brpt_bd_proj_task_1d
# dim_{country}.dim_pub_date
#
# dw_{country}.dwd_disty_brpt_orders_pl_mi



def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)
    exec_newest_hierarchy(country, date_flag, dt_month)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):
    end_day_of_last_month = conf.get("end_day_of_last_month")
    end_day_of_last_2month = conf.get("end_day_of_last_2month")
    end_day_of_same_month_of_last_year = conf.get("end_day_of_same_month_of_last_year")
    week_begin_of_dateflag = conf.get("week_begin_of_dateflag")
    month_no = conf.get("month_no")
    first_biz_date = conf.get("first_biz_date")
    


    main_sql = r"""
    with
    table_dt_month as (
    select
    project_no,
    task_no,
    nvl(company_no,1) as company_no,
    
    sum(case when date_flag = '{date_flag}' then goal_nsales else 0 end) as goal_nsales,
    sum(case when date_flag = '{date_flag}' then goal_gm else 0 end) as goal_gm,
    sum(case when date_flag = '{date_flag}' then goal_ngm else 0 end) as goal_ngm,
    sum(case when date_flag = '{date_flag}' then goal_opl_gm else 0 end) as goal_opl_gm,
    sum(case when date_flag = '{date_flag}' then goal_oplgm_plus_amt else 0 end) as goal_oplgm_plus_amt,
    sum(case when date_flag = '{date_flag}' then goal_tgm else 0 end) as goal_tgm,
    sum(case when date_flag = '{date_flag}' then goal_dos else 0 end) as goal_dos,
    sum(case when date_flag = '{date_flag}' then goal_pdt else 0 end) as goal_pdt,
    sum(case when date_flag = '{date_flag}' then goal_total_btl else 0 end) as goal_total_btl,
    sum(case when date_flag = '{date_flag}' then goal_cust_cnt else 0 end) as goal_cust_cnt,
    
    sum(case when date_flag = '{date_flag}' then net_sales else 0 end) as m_sales,
    sum(case when date_flag = '{date_flag}' then net_cost else 0 end) as m_cost,
    sum(case when date_flag = '{date_flag}' then total_unit else 0 end) as m_unit,
    sum(case when date_flag = '{date_flag}' then gm_amt else 0 end) as m_gm,
    sum(case when date_flag = '{date_flag}' then ngm_amt else 0 end) as m_ngm,
    sum(case when date_flag = '{date_flag}' then oplgm_amt else 0 end) as m_opl,
    sum(case when date_flag = '{date_flag}' then oplgm_plus_amt else 0 end) as m_oplgm_plus_amt,
    sum(case when date_flag = '{date_flag}' then scm_usage else 0 end) as m_scm_usage,
    sum(case when date_flag = '{date_flag}' then tgm_amt else 0 end) as m_tgm,
    sum(case when date_flag = '{date_flag}' then scm_disc else 0 end) as m_scm_disc,
    sum(case when date_flag = '{date_flag}' then scm_ndisc else 0 end) as m_scm_ndisc,
    sum(case when date_flag = '{date_flag}' then ds_sales else 0 end) as m_ds_sales,
    sum(case when date_flag = '{date_flag}' then stock_sales else 0 end) as m_stock_sales,
    sum(case when date_flag = '{date_flag}' then ds_cost else 0 end) as m_ds_cost,
    sum(case when date_flag = '{date_flag}' then stock_cost else 0 end) as m_stock_cost,
    sum(case when date_flag = '{date_flag}' then ds_scm_usage else 0 end) as m_ds_scm_usage,
    sum(case when date_flag = '{date_flag}' then stock_scm_usage else 0 end) as m_stock_scm_usage,
    sum(case when date_flag = '{date_flag}' then cgp else 0 end) as m_cgp,
    sum(case when date_flag = '{date_flag}' then total_btl else 0 end) as m_total_btl,
    sum(case when date_flag = '{date_flag}' then fx_cost else 0 end) as m_fx_cost,

    sum(case when date_flag = '{date_flag}' then bo_gross_sales else 0 end) as bo_gross_sales,
    sum(case when date_flag = '{date_flag}' then bo_gross_cost else 0 end) as bo_gross_cost,
    sum(case when date_flag = '{date_flag}' then bo_total_unit else 0 end) as bo_total_unit,
    sum(case when date_flag = '{date_flag}' then bo_gm_amt else 0 end) as bo_gm_amt,
    sum(case when date_flag = '{date_flag}' then so_gross_sales else 0 end) as so_gross_sales,
    sum(case when date_flag = '{date_flag}' then so_gross_cost else 0 end) as so_gross_cost,
    sum(case when date_flag = '{date_flag}' then so_total_unit else 0 end) as so_total_unit,
    sum(case when date_flag = '{date_flag}' then so_gm_amt else 0 end) as so_gm_amt,
    sum(case when date_flag = '{date_flag}' then bo_age0_7 else 0 end) as bo_age0_7,
    sum(case when date_flag = '{date_flag}' then bo_age8_14 else 0 end) as bo_age8_14,
    sum(case when date_flag = '{date_flag}' then bo_age15_21 else 0 end) as bo_age15_21,
    sum(case when date_flag = '{date_flag}' then bo_age21_up else 0 end) as bo_age21_up,
    sum(case when date_flag = '{date_flag}' then so_age0_7 else 0 end) as so_age0_7,
    sum(case when date_flag = '{date_flag}' then so_age8_14 else 0 end) as so_age8_14,
    sum(case when date_flag = '{date_flag}' then so_age15_21 else 0 end) as so_age15_21,
    sum(case when date_flag = '{date_flag}' then so_age21_up else 0 end) as so_age21_up,

    sum(case when date_flag = '{date_flag}' then rr_unit else 0 end) as rr_unit,
    sum(case when date_flag = '{date_flag}' then rr_sales else 0 end) as rr_sales,
    sum(case when date_flag = '{date_flag}' then rr_cost else 0 end) as rr_cost,
    sum(case when date_flag = '{date_flag}' then rr_gm else 0 end) as rr_gm,
    sum(case when date_flag = '{date_flag}' then rr_ngm else 0 end) as rr_ngm,
    sum(case when date_flag = '{date_flag}' then rr_opl else 0 end) as rr_opl,
    sum(case when date_flag = '{date_flag}' then rr_oplgm_plus_amt else 0 end) as rr_oplgm_plus_amt,
    sum(case when date_flag = '{date_flag}' then rr_cgp else 0 end) as rr_cgp,
    sum(case when date_flag = '{date_flag}' then rr_total_btl else 0 end) as rr_total_btl,
    sum(case when date_flag = '{date_flag}' then rr_tgm else 0 end) as rr_tgm
    from dw_{country}.dws_disty_brpt_bd_proj_task_mtd
    where date_flag = '{date_flag}'
    group by
    project_no,
    task_no,
    nvl(company_no,1)),
    
    table_last_dt_month as (
    select 
        project_no,
        task_no,
        nvl(company_no,1) as company_no,
        sum(case when date_flag = '{end_day_of_last_month}' then net_sales else 0 end) as pm_sales,
        sum(case when date_flag = '{end_day_of_last_month}' then net_cost else 0 end) as pm_cost,
        sum(case when date_flag = '{end_day_of_last_month}' then total_unit else 0 end) as pm_unit,
        sum(case when date_flag = '{end_day_of_last_month}' then gm_amt else 0 end) as pm_gm,
        sum(case when date_flag = '{end_day_of_last_month}' then ngm_amt else 0 end) as pm_ngm,
        sum(case when date_flag = '{end_day_of_last_month}' then oplgm_amt else 0 end) as pm_opl,
        sum(case when date_flag = '{end_day_of_last_month}' then oplgm_plus_amt else 0 end) as pm_oplgm_plus_amt,
        sum(case when date_flag = '{end_day_of_last_month}' then scm_usage else 0 end) as pm_scm_usage,
        sum(case when date_flag = '{end_day_of_last_month}' then tgm_amt else 0 end) as pm_tgm,
        sum(case when date_flag = '{end_day_of_last_month}' then scm_disc else 0 end) as pm_scm_disc,
        sum(case when date_flag = '{end_day_of_last_month}' then scm_ndisc else 0 end) as pm_scm_ndisc,
        sum(case when date_flag = '{end_day_of_last_month}' then ds_sales else 0 end) as pm_ds_sales,
        sum(case when date_flag = '{end_day_of_last_month}' then stock_sales else 0 end) as pm_stock_sales,
        sum(case when date_flag = '{end_day_of_last_month}' then ds_cost else 0 end) as pm_ds_cost,
        sum(case when date_flag = '{end_day_of_last_month}' then stock_cost else 0 end) as pm_stock_cost,
        sum(case when date_flag = '{end_day_of_last_month}' then ds_scm_usage else 0 end) as pm_ds_scm_usage,
        sum(case when date_flag = '{end_day_of_last_month}' then stock_scm_usage else 0 end) as pm_stock_scm_usage,
        sum(case when date_flag = '{end_day_of_last_month}' then cgp else 0 end) as pm_cgp,
        sum(case when date_flag = '{end_day_of_last_month}' then total_btl else 0 end) as pm_total_btl,
        sum(case when date_flag = '{end_day_of_last_month}' then fx_cost else 0 end) as pm_fx_cost,
        
        sum(case when date_flag = '{end_day_of_last_2month}' then net_sales else 0 end) as ppm_sales,
        sum(case when date_flag = '{end_day_of_last_2month}' then net_cost else 0 end) as ppm_cost,
        sum(case when date_flag = '{end_day_of_last_2month}' then total_unit else 0 end) as ppm_unit,
        sum(case when date_flag = '{end_day_of_last_2month}' then gm_amt else 0 end) as ppm_gm,
        sum(case when date_flag = '{end_day_of_last_2month}' then ngm_amt else 0 end) as ppm_ngm,
        sum(case when date_flag = '{end_day_of_last_2month}' then oplgm_amt else 0 end) as ppm_opl,
        sum(case when date_flag = '{end_day_of_last_2month}' then oplgm_plus_amt else 0 end) as ppm_oplgm_plus_amt,
        sum(case when date_flag = '{end_day_of_last_2month}' then scm_usage else 0 end) as ppm_scm_usage,
        sum(case when date_flag = '{end_day_of_last_2month}' then tgm_amt else 0 end) as ppm_tgm,
        sum(case when date_flag = '{end_day_of_last_2month}' then scm_disc else 0 end) as ppm_scm_disc,
        sum(case when date_flag = '{end_day_of_last_2month}' then scm_ndisc else 0 end) as ppm_scm_ndisc,
        sum(case when date_flag = '{end_day_of_last_2month}' then ds_sales else 0 end) as ppm_ds_sales,
        sum(case when date_flag = '{end_day_of_last_2month}' then stock_sales else 0 end) as ppm_stock_sales,
        sum(case when date_flag = '{end_day_of_last_2month}' then ds_cost else 0 end) as ppm_ds_cost,
        sum(case when date_flag = '{end_day_of_last_2month}' then stock_cost else 0 end) as ppm_stock_cost,
        sum(case when date_flag = '{end_day_of_last_2month}' then ds_scm_usage else 0 end) as ppm_ds_scm_usage,
        sum(case when date_flag = '{end_day_of_last_2month}' then stock_scm_usage else 0 end) as ppm_stock_scm_usage,
        sum(case when date_flag = '{end_day_of_last_2month}' then cgp else 0 end) as ppm_cgp,
        sum(case when date_flag = '{end_day_of_last_2month}' then total_btl else 0 end) as ppm_total_btl,
        sum(case when date_flag = '{end_day_of_last_2month}' then fx_cost else 0 end) as ppm_fx_cost
    from dw_{country}.dws_disty_brpt_bd_proj_task_mtd
    where date_flag in ('{end_day_of_last_2month}','{end_day_of_last_month}')
    group by 
        project_no,
        task_no,
        nvl(company_no,1) ),

    table_dt_month_last_year as (
    select
    project_no,
    task_no,
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
    from dw_{country}.dws_disty_brpt_bd_proj_task_mtd
    where date_flag = '{end_day_of_same_month_of_last_year}'
    group by
    project_no,
    task_no,
    nvl(company_no,1) ),

    table_1d as (
    select
    project_no,
    task_no,
    nvl(company_no,1) as company_no,
    sum(case when date_flag = '{date_flag}' then net_sales else 0 end) as d_sales,
    sum(case when date_flag = '{date_flag}' then net_cost else 0 end) as d_cost,
    sum(case when date_flag = '{date_flag}' then total_unit else 0 end) as d_unit,
    sum(case when date_flag = '{date_flag}' then gm_amt else 0 end) as d_gm,
    sum(case when date_flag = '{date_flag}' then ngm_amt else 0 end) as d_ngm,
    sum(case when date_flag = '{date_flag}' then oplgm_amt else 0 end) as d_opl,
    sum(case when date_flag = '{date_flag}' then oplgm_plus_amt else 0 end) as d_oplgm_plus_amt,
    sum(case when date_flag = '{date_flag}' then scm_usage else 0 end) as d_scm_usage,
    sum(case when date_flag = '{date_flag}' then tgm_amt else 0 end) as d_tgm,
    sum(case when date_flag = '{date_flag}' then cgp else 0 end) as d_cgp,
    sum(case when date_flag = '{date_flag}' then total_btl else 0 end) as d_total_btl,
    sum(case when date_flag = '{date_flag}' then fx_cost else 0 end) as d_fx_cost,

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
    from dw_{country}.dws_disty_brpt_bd_proj_task_1d
    where date_flag between '{week_begin_of_dateflag}' and '{date_flag}'
    group by
    project_no,
    task_no,
    nvl(company_no,1) ),

    table_b33 as (
    SELECT project_no
    FROM ods_{country}.ods_cis_corp_bd_project
    WHERE project_type = 1
         AND prod_group IS not NULL
         AND b33_flag = 'APPROVED'
         AND (close_date IS NULL OR close_date > '{date_flag}')
    )

    insert overwrite table dw_{country}.dws_disty_brpt_bd_proj_task_comb_mtd partition(date_flag = '{date_flag}')
    select
        {month_no},
        coalesce(table_dt_month.project_no,table_last_dt_month.project_no,table_dt_month_last_year.project_no,table_1d.project_no),
        table_project.project_desc as project_name,
        coalesce(table_dt_month.task_no,table_last_dt_month.task_no,table_dt_month_last_year.task_no,table_1d.task_no),
        t.task_name,
        coalesce(table_dt_month.company_no,table_last_dt_month.company_no,table_dt_month_last_year.company_no,table_1d.company_no) as company_no,
        t.bd_rep_id,
        t.bd_rep_name,
        t.bd_mgr_id,
        t.bd_mgr_name,
        t.bd_dir_id,
        t.bd_dir_name,
        t.bd_vp_id,
        t.bd_vp_name,
        
        table_dt_month.goal_nsales  ,
        table_dt_month.goal_gm      ,
        table_dt_month.goal_ngm     ,
        table_dt_month.goal_opl_gm  ,
        table_dt_month.goal_tgm     ,
        table_dt_month.goal_dos     ,
        table_dt_month.goal_pdt     ,
        table_dt_month.goal_total_btl,
        table_dt_month.goal_cust_cnt,

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
        '{etl_timestamp}',
        
        null as pm_sales_2            ,
        null as pm_cost_2             ,
        null as pm_unit_2             ,
        null as pm_gm_2               ,
        null as pm_ngm_2              ,
        null as pm_opl_2              ,
        null as pm_scm_usage_2        ,
        null as pm_tgm_2              ,
        null as pm_scm_disc_2         ,
        null as pm_scm_ndisc_2        ,
        null as pm_ds_sales_2         ,
        null as pm_stock_sales_2      ,
        null as pm_ds_cost_2          ,
        null as pm_stock_cost_2       ,
        null as pm_ds_scm_usage_2     ,
        null as pm_stock_scm_usage_2  ,
        null as pm_cgp_2              ,
        null as pm_total_btl_2        ,
        null as ppm_sales_2           ,
        null as ppm_cost_2            ,
        null as ppm_unit_2            ,
        null as ppm_gm_2              ,
        null as ppm_ngm_2             ,
        null as ppm_opl_2             ,
        null as ppm_scm_usage_2       ,
        null as ppm_tgm_2             ,
        null as ppm_scm_disc_2        ,
        null as ppm_scm_ndisc_2       ,
        null as ppm_ds_sales_2        ,
        null as ppm_stock_sales_2     ,
        null as ppm_ds_cost_2         ,
        null as ppm_stock_cost_2      ,
        null as ppm_ds_scm_usage_2    ,
        null as ppm_stock_scm_usage_2 ,
        null as ppm_cgp_2             ,
        null as ppm_total_btl_2       ,
        null as lm_sales_2            ,
        null as lm_cost_2             ,
        null as lm_unit_2             ,
        null as lm_gm_2               ,
        null as lm_ngm_2              ,
        null as lm_opl_2              ,
        null as lm_scm_usage_2        ,
        null as lm_tgm_2              ,
        null as lm_scm_disc_2         ,
        null as lm_scm_ndisc_2        ,
        null as lm_ds_sales_2         ,
        null as lm_stock_sales_2      ,
        null as lm_ds_cost_2          ,
        null as lm_stock_cost_2       ,
        null as lm_ds_scm_usage_2     ,
        null as lm_stock_scm_usage_2  ,
        null as lm_cgp_2              ,
        null as lm_total_btl_2        ,
        if( table_b33.project_no is not null, 1, 0 ) as b33_flag,
        table_1d.d_fx_cost,
        table_1d.w_fx_cost,
        table_dt_month.m_fx_cost,
        table_last_dt_month.pm_fx_cost,
        table_last_dt_month.ppm_fx_cost,
        table_dt_month_last_year.lm_fx_cost,
        
        t.bd_svp_id,
        t.bd_svp_name,
        
        table_1d.d_oplgm_plus_amt  ,
        table_1d.w_oplgm_plus_amt  ,
        table_dt_month.m_oplgm_plus_amt  ,
        table_last_dt_month.pm_oplgm_plus_amt ,
        table_last_dt_month.ppm_oplgm_plus_amt,
        table_dt_month_last_year.lm_oplgm_plus_amt ,
        table_dt_month.rr_oplgm_plus_amt,
        table_dt_month.goal_oplgm_plus_amt
    from table_dt_month
    full join table_last_dt_month
    on table_dt_month.project_no = table_last_dt_month.project_no
    and table_dt_month.task_no = table_last_dt_month.task_no
    and table_dt_month.company_no = table_last_dt_month.company_no

    full join table_dt_month_last_year
    on  nvl(table_dt_month.project_no,table_last_dt_month.project_no) = table_dt_month_last_year.project_no
    and nvl(table_dt_month.task_no,table_last_dt_month.task_no) = table_dt_month_last_year.task_no
    and nvl(table_dt_month.company_no,table_last_dt_month.company_no) = table_dt_month_last_year.company_no

    full join table_1d
    on  coalesce(table_dt_month.project_no,table_last_dt_month.project_no,table_dt_month_last_year.project_no) = table_1d.project_no
    and coalesce(table_dt_month.task_no,table_last_dt_month.task_no,table_dt_month_last_year.task_no) = table_1d.task_no
    and coalesce(table_dt_month.company_no,table_last_dt_month.company_no,table_dt_month_last_year.company_no) = table_1d.company_no

    left join table_b33
    on coalesce(table_dt_month.project_no,table_last_dt_month.project_no,table_dt_month_last_year.project_no,table_1d.project_no) = table_b33.project_no
    
    left join (select * from dim_{country}.dim_disty_bd_project_user_df where date_flag = '{first_biz_date}') as t
    on coalesce(table_dt_month.project_no,table_last_dt_month.project_no,table_dt_month_last_year.project_no,table_1d.project_no) = t.project_no
    and coalesce(table_dt_month.task_no,table_last_dt_month.task_no,table_dt_month_last_year.task_no,table_1d.task_no) = t.task_no
    
    left join ods_{country}.ods_cis_corp_bd_project as table_project
    on coalesce(table_dt_month.project_no,table_last_dt_month.project_no,table_dt_month_last_year.project_no,table_1d.project_no)  = table_project.project_no;
    """.format(country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp=etl_timestamp,
               end_day_of_last_month=end_day_of_last_month,
               end_day_of_last_2month=end_day_of_last_2month,
               end_day_of_same_month_of_last_year=end_day_of_same_month_of_last_year,
               week_begin_of_dateflag=week_begin_of_dateflag,
               month_no=month_no,
               first_biz_date=first_biz_date)
    run_sql(main_sql)


def exec_newest_hierarchy(country, date_flag, dt_month):
    """
    非_2字段： 从业务id来看，pm想按照最新的hierarchy 看现在归属自己的vpl，在历史上数据。
    _2字段:  join 人员id，纯粹看人员id， pm1去年卖了100万 今年卖了80万， 整合成一条数据：100万、80万。
    """
    end_day_of_last_month = conf.get("end_day_of_last_month")
    end_day_of_last_2month = conf.get("end_day_of_last_2month")
    end_day_of_same_month_of_last_year = conf.get("end_day_of_same_month_of_last_year")
    week_begin_of_dateflag = conf.get("week_begin_of_dateflag")
    month_no = conf.get("month_no")
    sql = """
    with
    table_last_dt_month as (
    select
    project_no  ,
    task_no     ,
    bd_rep_id   ,
    bd_mgr_id   ,
    bd_dir_id   ,
    bd_vp_id,
    nvl(company_no,1) as company_no,
    sum(case when date_flag = '{end_day_of_last_month}' then net_sales else 0 end) as pm_sales_2,
    sum(case when date_flag = '{end_day_of_last_month}' then net_cost else 0 end) as pm_cost_2,
    sum(case when date_flag = '{end_day_of_last_month}' then total_unit else 0 end) as pm_unit_2,
    sum(case when date_flag = '{end_day_of_last_month}' then gm_amt else 0 end) as pm_gm_2,
    sum(case when date_flag = '{end_day_of_last_month}' then ngm_amt else 0 end) as pm_ngm_2,
    sum(case when date_flag = '{end_day_of_last_month}' then oplgm_amt else 0 end) as pm_opl_2,
    sum(case when date_flag = '{end_day_of_last_month}' then scm_usage else 0 end) as pm_scm_usage_2,
    sum(case when date_flag = '{end_day_of_last_month}' then tgm_amt else 0 end) as pm_tgm_2,
    sum(case when date_flag = '{end_day_of_last_month}' then scm_disc else 0 end) as pm_scm_disc_2,
    sum(case when date_flag = '{end_day_of_last_month}' then scm_ndisc else 0 end) as pm_scm_ndisc_2,
    sum(case when date_flag = '{end_day_of_last_month}' then ds_sales else 0 end) as pm_ds_sales_2,
    sum(case when date_flag = '{end_day_of_last_month}' then stock_sales else 0 end) as pm_stock_sales_2,
    sum(case when date_flag = '{end_day_of_last_month}' then ds_cost else 0 end) as pm_ds_cost_2,
    sum(case when date_flag = '{end_day_of_last_month}' then stock_cost else 0 end) as pm_stock_cost_2,
    sum(case when date_flag = '{end_day_of_last_month}' then ds_scm_usage else 0 end) as pm_ds_scm_usage_2,
    sum(case when date_flag = '{end_day_of_last_month}' then stock_scm_usage else 0 end) as pm_stock_scm_usage_2,
    sum(case when date_flag = '{end_day_of_last_month}' then cgp else 0 end) as pm_cgp_2,
    sum(case when date_flag = '{end_day_of_last_month}' then total_btl else 0 end) as pm_total_btl_2,

    sum(case when date_flag = '{end_day_of_last_2month}' then net_sales else 0 end) as ppm_sales_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then net_cost else 0 end) as ppm_cost_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then total_unit else 0 end) as ppm_unit_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then gm_amt else 0 end) as ppm_gm_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then ngm_amt else 0 end) as ppm_ngm_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then oplgm_amt else 0 end) as ppm_opl_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then scm_usage else 0 end) as ppm_scm_usage_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then tgm_amt else 0 end) as ppm_tgm_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then scm_disc else 0 end) as ppm_scm_disc_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then scm_ndisc else 0 end) as ppm_scm_ndisc_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then ds_sales else 0 end) as ppm_ds_sales_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then stock_sales else 0 end) as ppm_stock_sales_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then ds_cost else 0 end) as ppm_ds_cost_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then stock_cost else 0 end) as ppm_stock_cost_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then ds_scm_usage else 0 end) as ppm_ds_scm_usage_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then stock_scm_usage else 0 end) as ppm_stock_scm_usage_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then cgp else 0 end) as ppm_cgp_2,
    sum(case when date_flag = '{end_day_of_last_2month}' then total_btl else 0 end) as ppm_total_btl_2
    from dw_{country}.dws_disty_brpt_bd_proj_task_mtd
    where date_flag in ('{end_day_of_last_2month}','{end_day_of_last_month}')
    group by
    project_no  ,
    task_no     ,
    bd_rep_id   ,
    bd_mgr_id   ,
    bd_dir_id   ,
    bd_vp_id,
    nvl(company_no,1) ),

    table_dt_month_last_year as (
    select
    project_no  ,
    task_no     ,
    bd_rep_id   ,
    bd_mgr_id   ,
    bd_dir_id   ,
    bd_vp_id,
    nvl(company_no,1) as company_no,
    sum(net_sales) as lm_sales_2,
    sum(net_cost) as lm_cost_2,
    sum(total_unit) as lm_unit_2,
    sum(gm_amt) as lm_gm_2,
    sum(ngm_amt) as lm_ngm_2,
    sum(oplgm_amt) as lm_opl_2,
    sum(scm_usage) as lm_scm_usage_2,
    sum(tgm_amt) as lm_tgm_2,
    sum(scm_disc) as lm_scm_disc_2,
    sum(scm_ndisc) as lm_scm_ndisc_2,
    sum(ds_sales) as lm_ds_sales_2,
    sum(stock_sales) as lm_stock_sales_2,
    sum(ds_cost) as lm_ds_cost_2,
    sum(stock_cost) as lm_stock_cost_2,
    sum(ds_scm_usage) as lm_ds_scm_usage_2,
    sum(stock_scm_usage) as lm_stock_scm_usage_2,
    sum(cgp) as lm_cgp_2,
    sum(total_btl) as lm_total_btl_2
    from dw_{country}.dws_disty_brpt_bd_proj_task_mtd
    where date_flag = '{end_day_of_same_month_of_last_year}'
    group by
    project_no  ,
    task_no     ,
    bd_rep_id   ,
    bd_mgr_id   ,
    bd_dir_id   ,
    bd_vp_id,
    nvl(company_no,1) )
    
    insert overwrite dw_{country}.dws_disty_brpt_bd_proj_task_comb_mtd partition(date_flag = '{date_flag}')
    select
        table_dm.month_no,
        table_dm.project_no,
        table_dm.project_name,
        table_dm.task_no,
        table_dm.task_name,
        table_dm.company_no,
        table_dm.bd_rep_id,
        table_dm.bd_rep_name,
        table_dm.bd_mgr_id,
        table_dm.bd_mgr_name,
        table_dm.bd_dir_id,
        table_dm.bd_dir_name,
        table_dm.bd_vp_id,
        table_dm.bd_vp_name,
        
        nvl(table_dm.goal_nsales,0),
        nvl(table_dm.goal_gm,0),
        nvl(table_dm.goal_ngm,0),
        nvl(table_dm.goal_opl_gm,0),
        nvl(table_dm.goal_tgm,0),
        nvl(table_dm.goal_dos,0),
        nvl(table_dm.goal_pdt,0),
        nvl(table_dm.goal_total_btl,0),
        nvl(table_dm.goal_cust_cnt,0),
        nvl(table_dm.d_sales,0),
        nvl(table_dm.d_cost,0),
        nvl(table_dm.d_unit,0),
        nvl(table_dm.d_gm,0),
        nvl(table_dm.d_ngm,0),
        nvl(table_dm.d_opl,0),
        nvl(table_dm.d_scm_usage,0),
        nvl(table_dm.d_tgm,0),
        nvl(table_dm.d_cgp,0),
        nvl(table_dm.d_total_btl,0),
        nvl(table_dm.w_sales,0),
        nvl(table_dm.w_cost,0),
        nvl(table_dm.w_unit,0),
        nvl(table_dm.w_gm,0),
        nvl(table_dm.w_ngm,0),
        nvl(table_dm.w_opl,0),
        nvl(table_dm.w_scm_usage,0),
        nvl(table_dm.w_tgm,0),
        nvl(table_dm.w_cgp,0),
        nvl(table_dm.w_total_btl,0),
        nvl(table_dm.m_sales,0),
        nvl(table_dm.m_cost,0),
        nvl(table_dm.m_unit,0),
        nvl(table_dm.m_gm,0),
        nvl(table_dm.m_ngm,0),
        nvl(table_dm.m_opl,0),
        nvl(table_dm.m_scm_usage,0),
        nvl(table_dm.m_tgm,0),
        nvl(table_dm.m_scm_disc,0),
        nvl(table_dm.m_scm_ndisc,0),
        nvl(table_dm.m_ds_sales,0),
        nvl(table_dm.m_stock_sales,0),
        nvl(table_dm.m_ds_cost,0),
        nvl(table_dm.m_stock_cost,0),
        nvl(table_dm.m_ds_scm_usage,0),
        nvl(table_dm.m_stock_scm_usage,0),
        nvl(table_dm.m_cgp,0),
        nvl(table_dm.m_total_btl,0),
        nvl(table_dm.pm_sales,0),
        nvl(table_dm.pm_cost,0),
        nvl(table_dm.pm_unit,0),
        nvl(table_dm.pm_gm,0),
        nvl(table_dm.pm_ngm,0),
        nvl(table_dm.pm_opl,0),
        nvl(table_dm.pm_scm_usage,0),
        nvl(table_dm.pm_tgm,0),
        nvl(table_dm.pm_scm_disc,0),
        nvl(table_dm.pm_scm_ndisc,0),
        nvl(table_dm.pm_ds_sales,0),
        nvl(table_dm.pm_stock_sales,0),
        nvl(table_dm.pm_ds_cost,0),
        nvl(table_dm.pm_stock_cost,0),
        nvl(table_dm.pm_ds_scm_usage,0),
        nvl(table_dm.pm_stock_scm_usage,0),
        nvl(table_dm.pm_cgp,0),
        nvl(table_dm.pm_total_btl,0),
        nvl(table_dm.ppm_sales,0),
        nvl(table_dm.ppm_cost,0),
        nvl(table_dm.ppm_unit,0),
        nvl(table_dm.ppm_gm,0),
        nvl(table_dm.ppm_ngm,0),
        nvl(table_dm.ppm_opl,0),
        nvl(table_dm.ppm_scm_usage,0),
        nvl(table_dm.ppm_tgm,0),
        nvl(table_dm.ppm_scm_disc,0),
        nvl(table_dm.ppm_scm_ndisc,0),
        nvl(table_dm.ppm_ds_sales,0),
        nvl(table_dm.ppm_stock_sales,0),
        nvl(table_dm.ppm_ds_cost,0),
        nvl(table_dm.ppm_stock_cost,0),
        nvl(table_dm.ppm_ds_scm_usage,0),
        nvl(table_dm.ppm_stock_scm_usage,0),
        nvl(table_dm.ppm_cgp,0),
        nvl(table_dm.ppm_total_btl,0),
        nvl(table_dm.lm_sales,0),
        nvl(table_dm.lm_cost,0),
        nvl(table_dm.lm_unit,0),
        nvl(table_dm.lm_gm,0),
        nvl(table_dm.lm_ngm,0),
        nvl(table_dm.lm_opl,0),
        nvl(table_dm.lm_scm_usage,0),
        nvl(table_dm.lm_tgm,0),
        nvl(table_dm.lm_scm_disc,0),
        nvl(table_dm.lm_scm_ndisc,0),
        nvl(table_dm.lm_ds_sales,0),
        nvl(table_dm.lm_stock_sales,0),
        nvl(table_dm.lm_ds_cost,0),
        nvl(table_dm.lm_stock_cost,0),
        nvl(table_dm.lm_ds_scm_usage,0),
        nvl(table_dm.lm_stock_scm_usage,0),
        nvl(table_dm.lm_cgp,0),
        nvl(table_dm.lm_total_btl,0),
        nvl(table_dm.bo_gross_sales,0),
        nvl(table_dm.bo_gross_cost,0),
        nvl(table_dm.bo_total_unit,0),
        nvl(table_dm.bo_gm_amt,0),
        nvl(table_dm.so_gross_sales,0),
        nvl(table_dm.so_gross_cost,0),
        nvl(table_dm.so_total_unit,0),
        nvl(table_dm.so_gm_amt,0),
        nvl(table_dm.bo_age0_7,0),
        nvl(table_dm.bo_age8_14,0),
        nvl(table_dm.bo_age15_21,0),
        nvl(table_dm.bo_age21_up,0),
        nvl(table_dm.so_age0_7,0),
        nvl(table_dm.so_age8_14,0),
        nvl(table_dm.so_age15_21,0),
        nvl(table_dm.so_age21_up,0),
        nvl(table_dm.rr_unit,0),
        nvl(table_dm.rr_sales,0),
        nvl(table_dm.rr_cost,0),
        nvl(table_dm.rr_gm,0),
        nvl(table_dm.rr_ngm,0),
        nvl(table_dm.rr_opl,0),
        nvl(table_dm.rr_cgp,0),
        nvl(table_dm.rr_total_btl,0),
        nvl(table_dm.rr_tgm,0),
        table_dm.etl_timestamp,
    
        nvl(table_last_dt_month.pm_sales_2,0),
        nvl(table_last_dt_month.pm_cost_2,0),
        nvl(table_last_dt_month.pm_unit_2,0),
        nvl(table_last_dt_month.pm_gm_2,0),
        nvl(table_last_dt_month.pm_ngm_2,0),
        nvl(table_last_dt_month.pm_opl_2,0),
        nvl(table_last_dt_month.pm_scm_usage_2,0),
        nvl(table_last_dt_month.pm_tgm_2,0),
        nvl(table_last_dt_month.pm_scm_disc_2,0),
        nvl(table_last_dt_month.pm_scm_ndisc_2,0),
        nvl(table_last_dt_month.pm_ds_sales_2,0),
        nvl(table_last_dt_month.pm_stock_sales_2,0),
        nvl(table_last_dt_month.pm_ds_cost_2,0),
        nvl(table_last_dt_month.pm_stock_cost_2,0),
        nvl(table_last_dt_month.pm_ds_scm_usage_2,0),
        nvl(table_last_dt_month.pm_stock_scm_usage_2,0),
        nvl(table_last_dt_month.pm_cgp_2,0),
        nvl(table_last_dt_month.pm_total_btl_2,0),
        nvl(table_last_dt_month.ppm_sales_2,0),
        nvl(table_last_dt_month.ppm_cost_2,0),
        nvl(table_last_dt_month.ppm_unit_2,0),
        nvl(table_last_dt_month.ppm_gm_2,0),
        nvl(table_last_dt_month.ppm_ngm_2,0),
        nvl(table_last_dt_month.ppm_opl_2,0),
        nvl(table_last_dt_month.ppm_scm_usage_2,0),
        nvl(table_last_dt_month.ppm_tgm_2,0),
        nvl(table_last_dt_month.ppm_scm_disc_2,0),
        nvl(table_last_dt_month.ppm_scm_ndisc_2,0),
        nvl(table_last_dt_month.ppm_ds_sales_2,0),
        nvl(table_last_dt_month.ppm_stock_sales_2,0),
        nvl(table_last_dt_month.ppm_ds_cost_2,0),
        nvl(table_last_dt_month.ppm_stock_cost_2,0),
        nvl(table_last_dt_month.ppm_ds_scm_usage_2,0),
        nvl(table_last_dt_month.ppm_stock_scm_usage_2,0),
        nvl(table_last_dt_month.ppm_cgp_2,0),
        nvl(table_last_dt_month.ppm_total_btl_2,0),
        nvl(table_dt_month_last_year.lm_sales_2,0),
        nvl(table_dt_month_last_year.lm_cost_2,0),
        nvl(table_dt_month_last_year.lm_unit_2,0),
        nvl(table_dt_month_last_year.lm_gm_2,0),
        nvl(table_dt_month_last_year.lm_ngm_2,0),
        nvl(table_dt_month_last_year.lm_opl_2,0),
        nvl(table_dt_month_last_year.lm_scm_usage_2,0),
        nvl(table_dt_month_last_year.lm_tgm_2,0),
        nvl(table_dt_month_last_year.lm_scm_disc_2,0),
        nvl(table_dt_month_last_year.lm_scm_ndisc_2,0),
        nvl(table_dt_month_last_year.lm_ds_sales_2,0),
        nvl(table_dt_month_last_year.lm_stock_sales_2,0),
        nvl(table_dt_month_last_year.lm_ds_cost_2,0),
        nvl(table_dt_month_last_year.lm_stock_cost_2,0),
        nvl(table_dt_month_last_year.lm_ds_scm_usage_2,0),
        nvl(table_dt_month_last_year.lm_stock_scm_usage_2,0),
        nvl(table_dt_month_last_year.lm_cgp_2,0),
        nvl(table_dt_month_last_year.lm_total_btl_2,0),
        nvl(table_dm.b33_flag,0),
        nvl(table_dm.d_fx_cost,0),
        nvl(table_dm.w_fx_cost,0),
        nvl(table_dm.m_fx_cost,0),
        nvl(table_dm.pm_fx_cost,0),
        nvl(table_dm.ppm_fx_cost,0),
        nvl(table_dm.lm_fx_cost,0),
        table_dm.bd_svp_id,
        table_dm.bd_svp_name,
        nvl(table_dm.d_oplgm_plus_amt   ,0),
        nvl(table_dm.w_oplgm_plus_amt   ,0),
        nvl(table_dm.m_oplgm_plus_amt   ,0),
        nvl(table_dm.pm_oplgm_plus_amt  ,0),
        nvl(table_dm.ppm_oplgm_plus_amt ,0),
        nvl(table_dm.lm_oplgm_plus_amt  ,0),
        nvl(table_dm.rr_oplgm_plus_amt  ,0),
        nvl(table_dm.goal_oplgm_plus_amt,0)
    from (select *
          from dw_{country}.dws_disty_brpt_bd_proj_task_comb_mtd
          where date_flag = '{date_flag}') as table_dm
    left join table_last_dt_month
    on table_dm.project_no = table_last_dt_month.project_no
    and table_dm.task_no = table_last_dt_month.task_no
    and table_dm.bd_rep_id = table_last_dt_month.bd_rep_id
    and table_dm.bd_mgr_id = table_last_dt_month.bd_mgr_id
    and table_dm.bd_dir_id = table_last_dt_month.bd_dir_id
    and table_dm.bd_vp_id = table_last_dt_month.bd_vp_id
    and table_dm.company_no = table_last_dt_month.company_no
    
    left join table_dt_month_last_year
    on table_dm.project_no = table_dt_month_last_year.project_no
    and table_dm.task_no = table_dt_month_last_year.task_no
    and table_dm.bd_rep_id = table_dt_month_last_year.bd_rep_id
    and table_dm.bd_mgr_id = table_dt_month_last_year.bd_mgr_id
    and table_dm.bd_dir_id = table_dt_month_last_year.bd_dir_id
    and table_dm.bd_vp_id = table_dt_month_last_year.bd_vp_id
    and table_dm.company_no = table_dt_month_last_year.company_no
    """.format(country=country,dt_month=dt_month,date_flag=date_flag,
               end_day_of_last_month=end_day_of_last_month,
               end_day_of_last_2month=end_day_of_last_2month,
               end_day_of_same_month_of_last_year=end_day_of_same_month_of_last_year,
               week_begin_of_dateflag=week_begin_of_dateflag)
    run_sql(sql)


main()