set time zone='America/Toronto';

drop table if exists brpt_ca5540_date_list;
create local temporary table brpt_ca5540_date_list on commit preserve rows as
select 3-b.fyear+a.fyear as sheet_index
    ,a.fyear
    ,a.m
    ,max(a.date_flag) as date_flag
from dim_ca.dim_pub_date a
cross join (select fyear from dim_ca.dim_pub_date where date_flag=current_date()-1) b
where a.fyear between b.fyear-2 and b.fyear
and a.date_flag < current_date()
group by 3-b.fyear+a.fyear
    ,a.fyear
    ,a.m
;

drop table if exists brpt_ca5540_final;
create local temporary table brpt_ca5540_final on commit preserve rows as
select dl.sheet_index
    ,to_char(a.date_flag, 'yyyymm') as month
    ,a.division_desc as Sales_Division
    ,sales_dir.name as Sales_Director
    ,a.cust_terr as sales_terr
    ,a.terr_name
    ,a.cust_type
    ,a.cust_type_desc as cust_type_descr
    ,a.vend_no
    ,a.vend_name
    ,pm.name as PM_name
    ,pm_mgr.name as PM_Manager
    ,pm_vp.name as PMVP
    ,sum(ifnull(a.net_sales, 0)) as Net_Sales
    ,sum(ifnull(a.ngm_amt, 0)) as NGM
    ,sum(ifnull(a.tgm_amt, 0)) as TGM
    ,sum(ifnull(a.oplgm_amt, 0)) as OPL
    ,sum(ifnull(a.gm_amt, 0)) as GM
from dw_ca.dws_disty_brpt_pl_extend_mtd a
inner join brpt_ca5540_date_list dl
    on a.date_flag = dl.date_flag
left join dim_ca.dim_pub_manager sales_dir
    on a.sales_dir_id = sales_dir.userid
left join dim_ca.dim_pub_manager pm
    on a.pm_id = pm.userid
left join dim_ca.dim_pub_manager pm_mgr
    on a.pm_mgr_id = pm_mgr.userid
left join dim_ca.dim_pub_manager pm_vp
    on a.pm_vp_id = pm_vp.userid
where a.pm_vp_id = 26109
group by dl.sheet_index
    ,to_char(a.date_flag, 'yyyymm')
    ,a.division_desc
    ,a.cust_terr
    ,a.terr_name
    ,a.cust_type
    ,a.cust_type_desc
    ,a.vend_no
    ,a.vend_name
    ,a.sales_dir_id
    ,a.pm_id
    ,a.pm_mgr_id
    ,a.pm_vp_id
    ,sales_dir.name
    ,pm.name
    ,pm_mgr.name
    ,pm_vp.name
having not (
    sum(ifnull(a.net_sales, 0)) = 0
    and sum(ifnull(a.ngm_amt, 0)) = 0
    and sum(ifnull(a.tgm_amt, 0)) = 0
    and sum(ifnull(a.oplgm_amt, 0)) = 0
    and sum(ifnull(a.gm_amt, 0)) = 0
)
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select f.month
    ,f.Sales_Division
    ,f.Sales_Director
    ,f.sales_terr
    ,f.terr_name
    ,f.cust_type
    ,f.cust_type_descr
    ,f.vend_no
    ,f.vend_name
    ,f.PM_name
    ,f.PM_Manager
    ,f.PMVP
    ,f.Net_Sales
    ,f.NGM
    ,f.TGM
    ,f.OPL
    ,f.GM
from brpt_ca5540_final f
where f.sheet_index = 1
order by f.month
    ,f.Sales_Division
    ,f.sales_terr
    ,f.cust_type
    ,f.vend_no
    ,f.PMVP
    ,f.PM_Manager
    ,f.PM_name
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select f.month
    ,f.Sales_Division
    ,f.Sales_Director
    ,f.sales_terr
    ,f.terr_name
    ,f.cust_type
    ,f.cust_type_descr
    ,f.vend_no
    ,f.vend_name
    ,f.PM_name
    ,f.PM_Manager
    ,f.PMVP
    ,f.Net_Sales
    ,f.NGM
    ,f.TGM
    ,f.OPL
    ,f.GM
from brpt_ca5540_final f
where f.sheet_index = 2
order by f.month
    ,f.Sales_Division
    ,f.sales_terr
    ,f.cust_type
    ,f.vend_no
    ,f.PMVP
    ,f.PM_Manager
    ,f.PM_name
;

drop table if exists rdsetl.rds_tmp_3;
create table rdsetl.rds_tmp_3 as
select f.month
    ,f.Sales_Division
    ,f.Sales_Director
    ,f.sales_terr
    ,f.terr_name
    ,f.cust_type
    ,f.cust_type_descr
    ,f.vend_no
    ,f.vend_name
    ,f.PM_name
    ,f.PM_Manager
    ,f.PMVP
    ,f.Net_Sales
    ,f.NGM
    ,f.TGM
    ,f.OPL
    ,f.GM
from brpt_ca5540_final f
where f.sheet_index = 3
order by f.month
    ,f.Sales_Division
    ,f.sales_terr
    ,f.cust_type
    ,f.vend_no
    ,f.PMVP
    ,f.PM_Manager
    ,f.PM_name
;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
    sheet_index int,
    sheet_name varchar(50),
    title_active varchar(1),
    date_pattern varchar(50)
);

insert into rdsetl.rds_tmp_sheet_config values(1, 'Fiscal LLY', null, null);
insert into rdsetl.rds_tmp_sheet_config values(2, 'Fiscal LY', null, null);
insert into rdsetl.rds_tmp_sheet_config values(3, 'Fiscal CY', null, null);

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

insert into rdsetl.rds_tmp_body
select 2 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp_2
;

insert into rdsetl.rds_tmp_body
select 3 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp_3
;

