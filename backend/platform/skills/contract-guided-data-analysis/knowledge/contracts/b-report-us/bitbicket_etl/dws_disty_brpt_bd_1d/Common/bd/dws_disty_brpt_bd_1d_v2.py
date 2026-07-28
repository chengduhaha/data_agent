# -*- coding: utf-8 -*-
# @Time : 2025/3/10 15:44
# @Author : Marvin Ma

from synnex.bigdata import conf
from synnex.bigdata.pyspark import run_sql

""" comment on bd_1d&bd_mtd
[sku_no = -1]  project which can sell all sku
[cust_no = -1] project which can sell to all customer
[C 0 2] + [C 1 2] + [C 2 2] = total 4 case. 
"""



run_sql(r"""
create temporary table table_mi_dws2 stored as orc as
select
    date_flag,
    nvl(company_no,1) as company_no,

    cust_no,
    cust_name,
    mcust_no,
    mcust_name,
    cust_terr,
    terr_name,
    cust_type,
    cust_type_desc,
    division,
    division_desc,
    terr_sub_group,
    sub_group_desc,
    terr_group,
    terr_group_desc,

    sku_no,
    part_no,
    mfg_partno,
    vpl_no,
    vpl_code,
    vpc_group_id,
    vpc_group_desc,
    vend_no,
    vend_name,
    master_vend_no,
    master_vend_name,
    group_id,
    seg_code,

    sum( nvl(gross_sales,0) ) as gross_sales,
    sum( nvl(net_sales,0) ) as net_sales,
    sum( nvl(gross_cost,0) ) as gross_cost,
    sum( nvl(net_cost,0) ) as net_cost,
    sum( nvl(scm_usage,0) ) as scm_usage,
    sum( nvl(ds_cost, 0) ) as ds_cost,
    sum( nvl(stock_cost, 0) ) as stock_cost,
    sum( nvl(ds_sales, 0) ) as ds_sales,
    sum( nvl(stock_sales, 0) ) as stock_sales,
    sum( nvl(ds_scm_usage, 0) ) as ds_scm_usage,
    sum( nvl(stock_scm_usage, 0) ) as stock_scm_usage,
    sum( nvl(total_unit,0) ) as total_unit,
    sum( nvl(total_weight,0) ) as total_weight,

    sum( nvl(cgp,0) ) as cgp,
    sum( nvl(total_btl,0) ) as total_btl,
    sum( nvl(tgm_amt,0) ) as tgm_amt,
    sum( nvl(gm_amt,0) ) as gm_amt,
    sum( nvl(ngm_amt,0) ) as ngm_amt,
    sum( nvl(oplgm_amt,0) ) as oplgm_amt,

    sum( nvl(bo_gross_sales,0)  ) as bo_gross_sales,
    sum( nvl(bo_gross_cost ,0)  ) as bo_gross_cost,
    sum( nvl(bo_total_unit ,0)  ) as bo_total_unit,
    sum( nvl(bo_gm_amt     ,0)  ) as bo_gm_amt,
    sum( nvl(so_gross_sales,0)  ) as so_gross_sales,
    sum( nvl(so_gross_cost ,0)  ) as so_gross_cost,
    sum( nvl(so_total_unit ,0)  ) as so_total_unit,
    sum( nvl(so_gm_amt     ,0)  ) as so_gm_amt,
    sum( nvl(bo_age0_7     ,0)  ) as bo_age0_7,
    sum( nvl(bo_age8_14    ,0)  ) as bo_age8_14,
    sum( nvl(bo_age15_21   ,0)  ) as bo_age15_21,
    sum( nvl(bo_age21_up   ,0)  ) as bo_age21_up,
    sum( nvl(so_age0_7     ,0)  ) as so_age0_7,
    sum( nvl(so_age8_14    ,0)  ) as so_age8_14,
    sum( nvl(so_age15_21   ,0)  ) as so_age15_21,
    sum( nvl(so_age21_up   ,0)  ) as so_age21_up,

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
    sum( nvl(fx_cost,0) ) as fx_cost,
    sum( nvl(btl_sales_for_opl	        ,0) ) as btl_sales_for_opl	        ,
    sum( nvl(trans_btl_sales_for_opl	,0) ) as trans_btl_sales_for_opl	,
    sum( nvl(pdt_for_opl         	    ,0) ) as pdt_for_opl         	    ,
    sum( nvl(cust_rebate_for_opl	    ,0) ) as cust_rebate_for_opl	    ,
    sum( nvl(cvr_rm_for_opl	            ,0) ) as cvr_rm_for_opl	            ,
    sum( nvl(btl_backout_for_opl	    ,0) ) as btl_backout_for_opl	    ,
    sum( nvl(cust_pmt_disc_for_opl	    ,0) ) as cust_pmt_disc_for_opl	    ,
    sum( nvl(cust_finance_sales_for_opl	,0) ) as cust_finance_sales_for_opl	,
    sum( nvl(rma_for_opl             	,0) ) as rma_for_opl             	,
    sum( nvl(ar_fin_recovery_for_opl 	,0) ) as ar_fin_recovery_for_opl 	,
    sum( nvl(order_overhead_for_opl  	,0) ) as order_overhead_for_opl  	,
    sum( nvl(frt_out_exp_for_opl     	,0) ) as frt_out_exp_for_opl     	,
    sum( nvl(frt_ob_recovery_for_opl 	,0) ) as frt_ob_recovery_for_opl 	,
    sum( nvl(oplgm_plus_amt             ,0) ) as oplgm_plus_amt
from dw_${country}.dws_disty_brpt_pl_extend_1d
where date_flag between '${firstday_of_month}' and '${date_flag}'
group by
    date_flag,
    cust_no,
    cust_name,
    mcust_no,
    mcust_name,
    cust_terr,
    terr_name,
    cust_type,
    cust_type_desc,
    division,
    division_desc,
    terr_sub_group,
    sub_group_desc,
    terr_group,
    terr_group_desc,

    sku_no,
    part_no,
    mfg_partno,
    vpl_no,
    vpl_code,
    vpc_group_id,
    vpc_group_desc,
    vend_no,
    vend_name,
    master_vend_no,
    master_vend_name,
    group_id,
    seg_code,
    nvl(company_no,1)
""")

################################################################## prod definition
run_sql("""
--'VEND','VPC','SKU'
create temporary table bdprj_prod_def as
select
    p.project_no,
    d.prod_level,
    d.prod_id
from (select * from ods_${country}.ods_etl_prog_prod_detail_df
      where date_flag = '${first_biz_date}' 
      and prod_level in ('VEND','VPC','SKU') ) as d
inner join (select * from ods_${country}.ods_etl_bd_project_df
            where (close_date is null or close_date > '${date_flag}')
            and date_flag = '${first_biz_date}') as p
on p.prod_group = d.group_id;

-- ALL
insert into bdprj_prod_def
select
    p.project_no,
    d.prod_level,
    null as prod_id
from (select * from ods_${country}.ods_etl_prog_prod_detail_df
      where date_flag = '${first_biz_date}' 
      and prod_level = 'ALL' ) as d
inner join (select * from ods_${country}.ods_etl_bd_project_df
            where (close_date is null or close_date > '${date_flag}')
            and date_flag = '${first_biz_date}') as p
on p.prod_group = d.group_id
group by 
    p.project_no,
    d.prod_level;
""")

run_sql("""
create temporary table t_prod_vend as 
SELECT 
    project_no,
    prod_id
FROM bdprj_prod_def
WHERE prod_level = 'VEND'
group by 
    project_no,
    prod_id;

create temporary table t_prod_vpc as 
SELECT 
    project_no,
    prod_id
FROM bdprj_prod_def
WHERE prod_level = 'VPC'
group by 
    project_no,
    prod_id;

create temporary table t_prod_sku as 
SELECT
    a.project_no,
    a.prod_id
FROM (select * from bdprj_prod_def WHERE prod_level = 'SKU') as a
join(select sku_no from table_mi_dws2 group by sku_no) as b 
on a.prod_id = b.sku_no
group by 
    a.project_no,
    a.prod_id;
""")
################################################################### cust definition
run_sql("""
--'DIV','CTYP','TERR','CUST'
create temporary table bdprj_cust_def as
select
p.project_no,
p.task_no,
d.cust_level,
d.cust_id
from (select * from ods_${country}.ods_etl_prog_cust_detail_df
      where inc_flag = 'Y'
      and cust_level in ('DIV','CTYP','TERR','CUST')
      and date_flag = '${first_biz_date}' ) as d
inner join (select * from ods_${country}.ods_etl_bd_project_task_df
            where (close_date is null or close_date > '${date_flag}')
            and date_flag = '${first_biz_date}') as p
on p.cust_group = d.group_id;

-- 寻找cust_no的 子cust_no
insert into bdprj_cust_def
select
table_tmp.project_no,
table_tmp.task_no,
table_tmp.cust_level,
x.cust_no
from (select * from bdprj_cust_def where cust_level = 'CUST') as table_tmp
inner join (select * from ods_${country}.ods_etl_cust_xref_all_df
            where date_flag = '${first_biz_date}'
            and data_source = 'ods_cis_corp_cust_xref'
            and xref_type = 'MASTER_SUB'
            AND active = 'Y'
            AND cust_no != xref_no) as x
on table_tmp.cust_id = x.xref_no;

-- state level
create temporary table table_state_temp as 
select 
    t.project_no,
    t.task_no,
    b.state_code
from (select * from ods_${country}.ods_etl_bd_project_task_df
      where (close_date is null or close_date > '${date_flag}')
      and date_flag = '${first_biz_date}') t
join (select * from ods_${country}.ods_etl_prog_cust_detail_df
      where inc_flag = 'Y'
      and cust_level = 'STAT'
      and date_flag = '${first_biz_date}') a
on t.cust_group = a.group_id
join (select * from ods_${country}.ods_cis_corp_state_code
      where active = 'Y'
      and country_code = upper('${country}') ) as b
on concat(chr(a.cust_id/100) , chr(a.cust_id%100)) = b.state_code;

insert into  bdprj_cust_def
select 
s.project_no,
s.task_no,
'CUST' as cust_level,
ch.cust_no
from (select * from ods_${country}.ods_cis_corp_customer_header
      where delete_datetime IS NULL
      and restricted <> 'Y'
      and discontinued <> 'Y') as ch
inner join (select * from ods_${country}.ods_cis_corp_addr_xref
            where xref_type = 'ADDR_CUST'
            and active = 'Y') as ax
ON ch.cust_no = ax.xref_no
INNER JOIN (select * from ods_${country}.ods_cis_corp_address
            where delete_id IS NULL
            and delete_datetime IS NULL) as  cd
ON ax.addr_no = cd.addr_no
RIGHT JOIN (select * from ods_${country}.ods_cis_corp_addr_profile
            where profile_type = 'CMLT'
            and profile_cat = 'LOCA'
            and profile_c = 'BT') ap
ON ax.addr_no = ap.addr_no
INNER JOIN table_state_temp s
ON cd.state = s.state_code;

-- all level
insert into bdprj_cust_def
select
    p.project_no,
    p.task_no,
    'ALL' as cust_level,
    null as cust_id
from (select * from ods_${country}.ods_etl_prog_cust_detail_df
      where inc_flag = 'Y'
      and cust_level = 'ALL'
      and date_flag = '${first_biz_date}') as d
inner join (select * from ods_${country}.ods_etl_bd_project_task_df
            where (close_date is null or close_date > '${date_flag}')
            and date_flag = '${first_biz_date}') as p
on p.cust_group = d.group_id
group by 
    p.project_no,
    p.task_no;
""")

run_sql("""
create temporary table t_cust_division as 
SELECT 
    project_no,
    task_no,
    cust_id
FROM bdprj_cust_def
WHERE cust_level = 'DIV'
group by 
    project_no,
    task_no,
    cust_id;

create temporary table t_cust_ctyp as 
SELECT 
    project_no,
    task_no,
    cust_id
FROM bdprj_cust_def
WHERE cust_level = 'CTYP'
group by 
    project_no,
    task_no,
    cust_id;

create temporary table t_cust_terr as
SELECT
    project_no,
    task_no,
    cust_id
FROM bdprj_cust_def
WHERE cust_level = 'TERR'
group by 
    project_no,
    task_no,
    cust_id;

create temporary table t_cust_no as
SELECT
    a.project_no,
    a.task_no,
    a.cust_id
FROM (select * from bdprj_cust_def WHERE cust_level = 'CUST') as a
join(select cust_no from table_mi_dws2 group by cust_no) as b 
on a.cust_id = b.cust_no
group by 
    a.project_no,
    a.task_no,
    a.cust_id;
""")

################################################################ cust exclude definition
run_sql("""
-- exclude 只有cust level
create temporary table t_cust_exclude as
select
p.project_no,
p.task_no,
d.cust_id as cust_no
from (select * from ods_${country}.ods_etl_prog_cust_detail_df
      where inc_flag = 'N'
      and cust_level = 'CUST'
      and date_flag = '${first_biz_date}') as d
inner join (select * from ods_${country}.ods_etl_bd_project_task_df
            where (close_date is null or close_date > '${date_flag}')
            and date_flag = '${first_biz_date}') as p
on p.cust_group = d.group_id;

-- 寻找cust_no的 子cust_no
insert into t_cust_exclude
select
table_tmp.project_no,
table_tmp.task_no,
x.cust_no
from t_cust_exclude as table_tmp
inner join (select * from ods_${country}.ods_etl_cust_xref_all_df
            where date_flag = '${first_biz_date}'
            and data_source = 'ods_cis_corp_cust_xref'
            and xref_type = 'MASTER_SUB'
            AND active = 'Y'
            AND cust_no != xref_no) as x
on table_tmp.cust_no = x.xref_no;
""")
###################################################################### table_b33: project_no of b33
run_sql("""
create temporary table table_b33 as
SELECT project_no
FROM ods_${country}.ods_etl_bd_project_df
WHERE project_type = 1
     AND prod_group IS not NULL
     AND b33_flag = 'APPROVED'
     AND (close_date IS NULL OR close_date > '${date_flag}')
     and date_flag = '${first_biz_date}'
""")

###################################################################################################### TODO 分割线
# 1.filter project:[cust_no != -1 and sku_no = -1]  project which can sell all sku to specified customer
# 1.1 All SKU + Division
# 1.2 All SKU + CustType
# 1.3 All SKU + Terr
# 1.4 All SKU + Cust(+State)
############# 1.1 prod_level = ALL & cust_level = DIV
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from (select *
         from bdprj_prod_def
         where prod_level = 'ALL') as table_sku
join t_cust_division as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert overwrite dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}' as etl_timestamp,
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    1 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.division = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")
#################### 1.2 prod_level = ALL & cust_level = CTYP
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from (select *
         from bdprj_prod_def
         where prod_level = 'ALL') as table_sku
join t_cust_ctyp as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    1 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.cust_type = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")
################ 1.3 prod_level = ALL & cust_level = TERR
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from (select *
         from bdprj_prod_def
         where prod_level = 'ALL') as table_sku
join t_cust_terr as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    1 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.cust_terr = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")
############# 1.4 prod_level = ALL & cust_level = CUST
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from (select *
         from bdprj_prod_def
         where prod_level = 'ALL') as table_sku
join t_cust_no as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    1 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.cust_no = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")
########################################################################################## TODO 分割线
# 2. filter project:[cust_no != -1 and sku_no != -1]  project which can sell specified sku to specified customer
# 2.1 Vend + Division
# 2.2 VPC + Division
# 2.3 SKU + Division
# 2.4 Vend + CustType
# 2.5 VPC + CustType
# 2.6 SKU + CustType
# 2.7 Vend + Terr
# 2.8 VPC + Terr
# 2.9 SKU + Terr
# 2.10 Vend + Cust
# 2.11 VPC + Cust
# 2.12 SKU + Cust

######################### 2.1 prod_level = Vend & cust_level = Division
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vend as table_sku
join t_cust_division as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vend_no = table_filter_cust_sku.prod_id
and table_mi_tmp.division = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.2 prod_level = VPC & cust_level = Division
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vpc as table_sku
join t_cust_division as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vpl_no = table_filter_cust_sku.prod_id
and table_mi_tmp.division = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.3 prod_level = SKU & cust_level = Division
run_sql("""
with
table_filter_cust_sku  as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_sku as table_sku
join t_cust_division as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.sku_no = table_filter_cust_sku.prod_id
and table_mi_tmp.division = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.4 prod_level = VEND & cust_level = CustType
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vend as table_sku
join t_cust_ctyp as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vend_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_type = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.5 prod_level = VPC & cust_level = CustType
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vpc as table_sku
join t_cust_ctyp as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vpl_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_type = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.6 prod_level = sku & cust_level = CustType
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_sku as table_sku
join t_cust_ctyp as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.sku_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_type = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.7 prod_level = vend & cust_level = TERR
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vend as table_sku
join t_cust_terr as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vend_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_terr = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.8 prod_level = vpc & cust_level = TERR
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vpc as table_sku
join t_cust_terr as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vpl_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_terr = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.9 prod_level = sku & cust_level = TERR
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_sku as table_sku
join t_cust_terr as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.sku_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_terr = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.10 prod_level = vend & cust_level = cust_no
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vend as table_sku
join t_cust_no as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vend_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_no = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.11 prod_level = vpc & cust_level = cust_no
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_vpc as table_sku
join t_cust_no as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.vpl_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_no = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

######################### 2.12 prod_level = sku & cust_level = cust_no
run_sql("""
with 
table_filter_cust_sku as (
select
    a.project_no,
    a.task_no,
    table_sku.prod_id,
    a.cust_id,
    if( table_b33.project_no is not null,1,0 ) as b33_flag
from t_prod_sku as table_sku
join t_cust_no as a
on table_sku.project_no = a.project_no
left join table_b33
on table_sku.project_no = table_b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_tmp.cust_no                    ,
    table_mi_tmp.cust_name                  ,
    table_mi_tmp.mcust_no                   ,
    table_mi_tmp.mcust_name                 ,
    table_mi_tmp.cust_terr                  ,
    table_mi_tmp.terr_name                  ,
    table_mi_tmp.cust_type                  ,
    table_mi_tmp.cust_type_desc             ,
    table_mi_tmp.division                   ,
    table_mi_tmp.division_desc              ,
    table_mi_tmp.terr_sub_group             ,
    table_mi_tmp.sub_group_desc             ,
    table_mi_tmp.terr_group                 ,
    table_mi_tmp.terr_group_desc            ,

    table_mi_tmp.sku_no                     ,
    table_mi_tmp.part_no                    ,
    table_mi_tmp.mfg_partno                 ,
    table_mi_tmp.vpl_no                     ,
    table_mi_tmp.vpl_code                   ,
    table_mi_tmp.vpc_group_id               ,
    table_mi_tmp.vpc_group_desc             ,
    table_mi_tmp.vend_no                    ,
    table_mi_tmp.vend_name                  ,
    table_mi_tmp.master_vend_no             ,
    table_mi_tmp.master_vend_name           ,
    table_mi_tmp.group_id                   ,
    table_mi_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_tmp.fx_cost,
    2 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_tmp.date_flag
from table_mi_dws2 as table_mi_tmp
join table_filter_cust_sku
on table_mi_tmp.sku_no = table_filter_cust_sku.prod_id
and table_mi_tmp.cust_no = table_filter_cust_sku.cust_id

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

################################################################################### TODO 分割线
# 3. filter project:[cust_no = -1 and sku_no != -1]  project which can sell specified sku to all customer(exclude)
# 3.1 Vend + ALL Cust
# 3.2 VPC + ALL Cust
# 3.3 SKU + ALL Cust
#########################  # 3.1 Vend + ALL Cust
run_sql("""
with
table_filter_cust_sku as (
select
    table_cust.project_no,
    table_cust.task_no,
    if( b33.project_no is not null, 1, 0 ) as b33_flag,
    table_sku.prod_id
from (select *
     from bdprj_cust_def
     where cust_level = 'ALL') as table_cust
join t_prod_vend as table_sku
on table_sku.project_no = table_cust.project_no
left join table_b33 as b33
on table_cust.project_no = b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_dws_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_dws_tmp.cust_no                    ,
    table_mi_dws_tmp.cust_name                  ,
    table_mi_dws_tmp.mcust_no                   ,
    table_mi_dws_tmp.mcust_name                 ,
    table_mi_dws_tmp.cust_terr                  ,
    table_mi_dws_tmp.terr_name                  ,
    table_mi_dws_tmp.cust_type                  ,
    table_mi_dws_tmp.cust_type_desc             ,
    table_mi_dws_tmp.division                   ,
    table_mi_dws_tmp.division_desc              ,
    table_mi_dws_tmp.terr_sub_group             ,
    table_mi_dws_tmp.sub_group_desc             ,
    table_mi_dws_tmp.terr_group                 ,
    table_mi_dws_tmp.terr_group_desc            ,

    table_mi_dws_tmp.sku_no                     ,
    table_mi_dws_tmp.part_no                    ,
    table_mi_dws_tmp.mfg_partno                 ,
    table_mi_dws_tmp.vpl_no                     ,
    table_mi_dws_tmp.vpl_code                   ,
    table_mi_dws_tmp.vpc_group_id               ,
    table_mi_dws_tmp.vpc_group_desc             ,
    table_mi_dws_tmp.vend_no                    ,
    table_mi_dws_tmp.vend_name                  ,
    table_mi_dws_tmp.master_vend_no             ,
    table_mi_dws_tmp.master_vend_name           ,
    table_mi_dws_tmp.group_id                   ,
    table_mi_dws_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_dws_tmp.fx_cost,
    3 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_dws_tmp.date_flag
from from table_mi_dws2 as table_mi_dws_tmp
join table_filter_cust_sku
on table_mi_dws_tmp.vend_no = table_filter_cust_sku.prod_id  

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

#########################  # 3.2 VPC + ALL Cust
run_sql("""
with
table_filter_cust_sku as (
select
    table_cust.project_no,
    table_cust.task_no,
    if( b33.project_no is not null, 1, 0 ) as b33_flag,
    table_sku.prod_id
from (select *
     from bdprj_cust_def
     where cust_level = 'ALL') as table_cust
join t_prod_vpc as table_sku
on table_sku.project_no = table_cust.project_no
left join table_b33 as b33
on table_cust.project_no = b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_dws_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_dws_tmp.cust_no                    ,
    table_mi_dws_tmp.cust_name                  ,
    table_mi_dws_tmp.mcust_no                   ,
    table_mi_dws_tmp.mcust_name                 ,
    table_mi_dws_tmp.cust_terr                  ,
    table_mi_dws_tmp.terr_name                  ,
    table_mi_dws_tmp.cust_type                  ,
    table_mi_dws_tmp.cust_type_desc             ,
    table_mi_dws_tmp.division                   ,
    table_mi_dws_tmp.division_desc              ,
    table_mi_dws_tmp.terr_sub_group             ,
    table_mi_dws_tmp.sub_group_desc             ,
    table_mi_dws_tmp.terr_group                 ,
    table_mi_dws_tmp.terr_group_desc            ,

    table_mi_dws_tmp.sku_no                     ,
    table_mi_dws_tmp.part_no                    ,
    table_mi_dws_tmp.mfg_partno                 ,
    table_mi_dws_tmp.vpl_no                     ,
    table_mi_dws_tmp.vpl_code                   ,
    table_mi_dws_tmp.vpc_group_id               ,
    table_mi_dws_tmp.vpc_group_desc             ,
    table_mi_dws_tmp.vend_no                    ,
    table_mi_dws_tmp.vend_name                  ,
    table_mi_dws_tmp.master_vend_no             ,
    table_mi_dws_tmp.master_vend_name           ,
    table_mi_dws_tmp.group_id                   ,
    table_mi_dws_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_dws_tmp.fx_cost,
    3 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_dws_tmp.date_flag
from from table_mi_dws2 as table_mi_dws_tmp
join table_filter_cust_sku
on table_mi_dws_tmp.vpl_no = table_filter_cust_sku.prod_id  

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

#########################  # 3.3 sku + ALL Cust
run_sql("""
with
table_filter_cust_sku as (
select
    table_cust.project_no,
    table_cust.task_no,
    if( b33.project_no is not null, 1, 0 ) as b33_flag,
    table_sku.prod_id
from (select *
     from bdprj_cust_def
     where cust_level = 'ALL') as table_cust
join t_prod_sku as table_sku
on table_sku.project_no = table_cust.project_no
left join table_b33 as b33
on table_cust.project_no = b33.project_no)

insert into dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
    table_filter_cust_sku.project_no,
    table_project.project_desc as project_name,
    table_filter_cust_sku.task_no,
    t.task_name,
    table_mi_dws_tmp.company_no,

    t.bd_rep_id,
    t.bd_rep_name,
    t.bd_mgr_id,
    t.bd_mgr_name,
    t.bd_dir_id,
    t.bd_dir_name,
    t.bd_vp_id,
    t.bd_vp_name,

    table_mi_dws_tmp.cust_no                    ,
    table_mi_dws_tmp.cust_name                  ,
    table_mi_dws_tmp.mcust_no                   ,
    table_mi_dws_tmp.mcust_name                 ,
    table_mi_dws_tmp.cust_terr                  ,
    table_mi_dws_tmp.terr_name                  ,
    table_mi_dws_tmp.cust_type                  ,
    table_mi_dws_tmp.cust_type_desc             ,
    table_mi_dws_tmp.division                   ,
    table_mi_dws_tmp.division_desc              ,
    table_mi_dws_tmp.terr_sub_group             ,
    table_mi_dws_tmp.sub_group_desc             ,
    table_mi_dws_tmp.terr_group                 ,
    table_mi_dws_tmp.terr_group_desc            ,

    table_mi_dws_tmp.sku_no                     ,
    table_mi_dws_tmp.part_no                    ,
    table_mi_dws_tmp.mfg_partno                 ,
    table_mi_dws_tmp.vpl_no                     ,
    table_mi_dws_tmp.vpl_code                   ,
    table_mi_dws_tmp.vpc_group_id               ,
    table_mi_dws_tmp.vpc_group_desc             ,
    table_mi_dws_tmp.vend_no                    ,
    table_mi_dws_tmp.vend_name                  ,
    table_mi_dws_tmp.master_vend_no             ,
    table_mi_dws_tmp.master_vend_name           ,
    table_mi_dws_tmp.group_id                   ,
    table_mi_dws_tmp.seg_code                   ,

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

    '${etl_timestamp}',
    table_filter_cust_sku.b33_flag,
    table_mi_dws_tmp.fx_cost,
    3 as project_source_flag,
    t.bd_svp_id,
    t.bd_svp_name,
    btl_sales_for_opl	        ,
    trans_btl_sales_for_opl	    ,
    pdt_for_opl         	    ,
    cust_rebate_for_opl	        ,
    cvr_rm_for_opl	            ,
    btl_backout_for_opl	        ,
    cust_pmt_disc_for_opl	    ,
    cust_finance_sales_for_opl	,
    rma_for_opl             	,
    ar_fin_recovery_for_opl 	,
    order_overhead_for_opl  	,
    frt_out_exp_for_opl     	,
    frt_ob_recovery_for_opl 	,
    oplgm_plus_amt,
    table_mi_dws_tmp.date_flag
from from table_mi_dws2 as table_mi_dws_tmp
join table_filter_cust_sku
on table_mi_dws_tmp.sku_no = table_filter_cust_sku.prod_id  

left join (select * from dim_${country}.dim_disty_bd_project_user_df where date_flag = '${first_biz_date}') as t     --unique id: project_no+task_no
on table_filter_cust_sku.project_no = t.project_no
and table_filter_cust_sku.task_no = t.task_no

left join (select * from ods_${country}.ods_etl_bd_project_df where date_flag = '${first_biz_date}') as table_project
on table_filter_cust_sku.project_no = table_project.project_no;
""")

# ignore the 4th case:
# 4. filter project:[cust_no = -1 and sku_no = -1]  project which can sell all sku to all customer
# join condition is item which [!= -1]: None


################################################################################# TODO 分割线 排除逻辑 + 最终的去重
# 去重（因为可能重复定义,举例：一个project 定义了terr后 还可能重复定义某些cust_no）
run_sql("""
with
table_tmp as (
select
table_left.*
from (select *
      from dw_${country}.dws_disty_brpt_bd_1d
      where date_flag between '${firstday_of_month}' and '${date_flag}') as table_left
left join t_cust_exclude
on table_left.project_no = t_cust_exclude.project_no
and table_left.task_no = t_cust_exclude.task_no
and table_left.cust_no = t_cust_exclude.cust_no

where t_cust_exclude.project_no is null
and t_cust_exclude.task_no is null
and t_cust_exclude.cust_no is null),

table_tmp2 as (
select
*,
row_number() over(partition by date_flag,project_no,task_no,
                               sku_no,vpl_no,vend_no,
                               cust_no,cust_terr,cust_type
                  order by date_flag) as rank
from table_tmp)

insert overwrite table dw_${country}.dws_disty_brpt_bd_1d partition(date_flag)
select
project_no,
project_name,
task_no,
task_name,
company_no,
bd_rep_id,
bd_rep_name,
bd_mgr_id,
bd_mgr_name,
bd_dir_id,
bd_dir_name,
bd_vp_id,
bd_vp_name,
cust_no,
cust_name,
mcust_no,
mcust_name,
cust_terr,
terr_name,
cust_type,
cust_type_desc,
division,
division_desc,
terr_sub_group,
sub_group_desc,
terr_group,
terr_group_desc,
sku_no,
part_no,
mfg_partno,
vpl_no,
vpl_code,
vpc_group_id,
vpc_group_desc,
vend_no,
vend_name,
master_vend_no,
master_vend_name,
group_id,
seg_code,
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
etl_timestamp,
b33_flag,
fx_cost,
project_source_flag,
bd_svp_id,
bd_svp_name,
btl_sales_for_opl	        ,
trans_btl_sales_for_opl	    ,
pdt_for_opl         	    ,
cust_rebate_for_opl	        ,
cvr_rm_for_opl	            ,
btl_backout_for_opl	        ,
cust_pmt_disc_for_opl	    ,
cust_finance_sales_for_opl	,
rma_for_opl             	,
ar_fin_recovery_for_opl 	,
order_overhead_for_opl  	,
frt_out_exp_for_opl     	,
frt_ob_recovery_for_opl 	,
oplgm_plus_amt,
date_flag
from table_tmp2
where rank = 1;
""")

