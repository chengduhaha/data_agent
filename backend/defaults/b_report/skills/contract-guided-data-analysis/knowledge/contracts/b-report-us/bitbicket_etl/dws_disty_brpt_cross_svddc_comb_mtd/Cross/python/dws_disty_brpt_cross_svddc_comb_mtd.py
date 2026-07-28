# -*- coding: utf-8 -*-
# @Time : 10/11/2023 1:45 PM
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

# dw_{country}.dws_disty_brpt_cross_svddc_mtd
# dw_{country}.dws_disty_brpt_cross_svddc_1d


def main():
    country = conf.get("country")
    date_flag = conf.get("date_flag")  # date_flag = yesterday = @process_date
    dt_month = conf.get("dt_month")  # date_flag format to 'yyyy-MM'
    etl_timestamp = conf.get("etl_timestamp")

    exec_main_sql(country, date_flag, dt_month, etl_timestamp)


def exec_main_sql(country, date_flag, dt_month, etl_timestamp):
    end_day_of_last_month = conf.get("end_day_of_last_month")
    end_day_of_last_2month = conf.get("end_day_of_last_2month")
    end_day_of_same_month_of_last_year = conf.get("end_day_of_same_month_of_last_year")
    week_begin_of_dateflag = conf.get("week_begin_of_dateflag")
    month_no = conf.get("month_no")

    main_sql = r"""
    with
    table_dt_month as (
    select
        cust_type          ,
        division           ,
    
        pm_dir_id	       ,
        pm_vp_id	       ,
        seg_code           ,
        nvl(company_no,1) as company_no         ,
        
        sum(net_sales) as m_sales,
        sum(net_cost) as m_cost,
        sum(total_unit) as m_unit,
        sum(gm_amt) as m_gm,
        sum(ngm_amt) as m_ngm,
        sum(oplgm_amt) as m_opl,
        sum(oplgm_plus_amt) as m_oplgm_plus_amt,
        sum(scm_usage) as m_scm_usage,
        sum(tgm_amt) as m_tgm,
        sum(scm_disc) as m_scm_disc,
        sum(scm_ndisc) as m_scm_ndisc,
        sum(ds_sales) as m_ds_sales,
        sum(stock_sales) as m_stock_sales,
        sum(ds_cost) as m_ds_cost,
        sum(stock_cost) as m_stock_cost,
        sum(ds_scm_usage) as m_ds_scm_usage,
        sum(stock_scm_usage) as m_stock_scm_usage,
        sum(cgp) as m_cgp,
        sum(total_btl) as m_total_btl,
        sum(fx_cost) as m_fx_cost,
    
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
        sum(rr_oplgm_plus_amt) as rr_oplgm_plus_amt,
        sum(rr_cgp) as rr_cgp,
        sum(rr_total_btl) as rr_total_btl,
        sum(rr_tgm) as rr_tgm
    from dw_{country}.dws_disty_brpt_cross_svddc_mtd
    where date_flag = '{date_flag}'
    group by
        cust_type          ,
        division           ,
    
        pm_dir_id	       ,
        pm_vp_id	       ,
        seg_code           ,
        nvl(company_no,1)         ),

    table_last_dt_month as (
    select
        cust_type,
        pm_dir_id,
        pm_vp_id,
        seg_code,
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
    from dw_{country}.dws_disty_brpt_cross_svddc_mtd
    where date_flag in ('{end_day_of_last_2month}','{end_day_of_last_month}')
    group by
        cust_type,
        pm_dir_id,
        pm_vp_id,
        seg_code,
        nvl(company_no,1) ),

    table_dt_month_last_year as (
    select
        cust_type,
        pm_dir_id,
        pm_vp_id,
        seg_code,
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
    from dw_{country}.dws_disty_brpt_cross_svddc_mtd
    where date_flag = '{end_day_of_same_month_of_last_year}'
    group by
        cust_type,
        pm_dir_id,
        pm_vp_id,
        seg_code,
        nvl(company_no,1) ),

    table_1d as (
    select
        cust_type,
        pm_dir_id,
        pm_vp_id,
        seg_code,
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
    from dw_{country}.dws_disty_brpt_cross_svddc_1d
    where date_flag between '{week_begin_of_dateflag}' and '{date_flag}'
    group by
        cust_type,
        pm_dir_id,
        pm_vp_id,
        seg_code,
        nvl(company_no,1) )

    insert overwrite table dw_{country}.dws_disty_brpt_cross_svddc_comb_mtd partition(date_flag = '{date_flag}')
    select
        {month_no},

        coalesce(table_dt_month.cust_type, table_last_dt_month.cust_type, table_dt_month_last_year.cust_type,table_1d.cust_type) as cust_type,
        null as cust_type_desc,
        table_dt_month.division,
        null as division_desc,

        coalesce(table_dt_month.pm_dir_id, table_last_dt_month.pm_dir_id, table_dt_month_last_year.pm_dir_id,table_1d.pm_dir_id) as pm_dir_id,
        null as pm_director_name	    ,
        coalesce(table_dt_month.pm_vp_id, table_last_dt_month.pm_vp_id, table_dt_month_last_year.pm_vp_id,table_1d.pm_vp_id) as pm_vp_id,
        null as pm_vp_name	        ,
        coalesce(table_dt_month.seg_code, table_last_dt_month.seg_code, table_dt_month_last_year.seg_code,table_1d.seg_code) as seg_code,
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
        '{etl_timestamp}',
        table_1d.d_fx_cost,
        table_1d.w_fx_cost,
        table_dt_month.m_fx_cost,
        table_last_dt_month.pm_fx_cost,
        table_last_dt_month.ppm_fx_cost,
        table_dt_month_last_year.lm_fx_cost,
        table_1d.d_oplgm_plus_amt  ,
        table_1d.w_oplgm_plus_amt  ,
        table_dt_month.m_oplgm_plus_amt  ,
        table_last_dt_month.pm_oplgm_plus_amt ,
        table_last_dt_month.ppm_oplgm_plus_amt,
        table_dt_month_last_year.lm_oplgm_plus_amt ,
        table_dt_month.rr_oplgm_plus_amt
    from table_dt_month
    full join table_last_dt_month
    on table_dt_month.cust_type = table_last_dt_month.cust_type
    and table_dt_month.pm_dir_id = table_last_dt_month.pm_dir_id
    and table_dt_month.pm_vp_id = table_last_dt_month.pm_vp_id
    and table_dt_month.seg_code = table_last_dt_month.seg_code
    and table_dt_month.company_no = table_last_dt_month.company_no

    full join table_dt_month_last_year
    on  nvl(table_dt_month.cust_type ,table_last_dt_month.cust_type ) = table_dt_month_last_year.cust_type
    and nvl(table_dt_month.pm_dir_id ,table_last_dt_month.pm_dir_id ) = table_dt_month_last_year.pm_dir_id
    and nvl(table_dt_month.pm_vp_id  ,table_last_dt_month.pm_vp_id  ) = table_dt_month_last_year.pm_vp_id
    and nvl(table_dt_month.seg_code  ,table_last_dt_month.seg_code  ) = table_dt_month_last_year.seg_code
    and nvl(table_dt_month.company_no,table_last_dt_month.company_no) = table_dt_month_last_year.company_no

    full join table_1d
    on  coalesce(table_dt_month.cust_type ,table_last_dt_month.cust_type ,table_dt_month_last_year.cust_type ) = table_1d.cust_type
    and coalesce(table_dt_month.pm_dir_id ,table_last_dt_month.pm_dir_id ,table_dt_month_last_year.pm_dir_id ) = table_1d.pm_dir_id
    and coalesce(table_dt_month.pm_vp_id  ,table_last_dt_month.pm_vp_id  ,table_dt_month_last_year.pm_vp_id  ) = table_1d.pm_vp_id
    and coalesce(table_dt_month.seg_code  ,table_last_dt_month.seg_code  ,table_dt_month_last_year.seg_code  ) = table_1d.seg_code
    and coalesce(table_dt_month.company_no,table_last_dt_month.company_no,table_dt_month_last_year.company_no) = table_1d.company_no
    """.format(country=country, date_flag=date_flag, dt_month=dt_month, etl_timestamp=etl_timestamp, month_no=month_no,
               end_day_of_last_month=end_day_of_last_month,
               end_day_of_last_2month=end_day_of_last_2month,
               end_day_of_same_month_of_last_year=end_day_of_same_month_of_last_year,
               week_begin_of_dateflag=week_begin_of_dateflag)
    run_sql(main_sql)

    run_sql("""
    insert overwrite table dw_${country}.dws_disty_brpt_cross_svddc_comb_mtd partition(date_flag = '${date_flag}')
    select
    table_dwd.month_no,
    
    coalesce(table_dwd.cust_type,-3),
    table_cust_type.cust_type_descr                                 as cust_type_desc,
    coalesce(table_dwd.division, table_cust_type.division,-3)               as division,
    table_div.division_desc                                         as division_desc,

    nvl(table_dwd.pm_dir_id,-3),
    concat_ws(' ', table_manager3.firstname, table_manager3.lastname)       as pm_director_name,
    nvl(table_dwd.pm_vp_id,-3),
    concat_ws(' ', table_manager4.firstname, table_manager4.lastname)       as pm_vp_name,
    table_dwd.seg_code,
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
    nvl(table_dwd.d_fx_cost,0),
    nvl(table_dwd.w_fx_cost,0),
    nvl(table_dwd.m_fx_cost,0),
    nvl(table_dwd.pm_fx_cost,0),
    nvl(table_dwd.ppm_fx_cost,0),
    nvl(table_dwd.lm_fx_cost,0),
    nvl(table_dwd.d_oplgm_plus_amt,0),
    nvl(table_dwd.w_oplgm_plus_amt,0),
    nvl(table_dwd.m_oplgm_plus_amt,0),
    nvl(table_dwd.pm_oplgm_plus_amt,0),
    nvl(table_dwd.ppm_oplgm_plus_amt,0),
    nvl(table_dwd.lm_oplgm_plus_amt,0),
    nvl(table_dwd.rr_oplgm_plus_amt,0)
    from (select *
          from dw_${country}.dws_disty_brpt_cross_svddc_comb_mtd
          where date_flag = '${date_flag}') as table_dwd
    left join ods_${country}.ods_cis_corp_cust_type as table_cust_type
    on table_dwd.cust_type = table_cust_type.cust_type
    
    left join ods_${country}.ods_cis_corp_division as table_div
    on nvl(table_dwd.division, table_cust_type.division) = table_div.division
    
    left join ods_${country}.ods_cis_corp_manager as table_manager3   --unique id : userid
    on table_dwd.pm_dir_id = table_manager3.userid
    left join ods_${country}.ods_cis_corp_manager as table_manager4   --unique id : userid
    on table_dwd.pm_vp_id = table_manager4.userid
    """)


main()