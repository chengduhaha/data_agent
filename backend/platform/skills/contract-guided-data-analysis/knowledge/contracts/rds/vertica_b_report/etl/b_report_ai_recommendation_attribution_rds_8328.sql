drop table if exists rds_ca8328_sku_list;
create local temporary table rds_ca8328_sku_list on commit preserve rows as
SELECT DISTINCT pm.sku_no
	,pm.mfg_partno
	,pm.long_desc
	,pm.vpl_no
	,pm.vend_no
	,pm.vend_name
	,pm.vpl_code
	,pm.vpl_desc
	,vpl.vpc_group_id
	,vpl.vpc_group_desc
	,smb.cust_no
	,date(smb.report_date) AS email_date
	,date(smb.report_date) - 30 AS pre_date
	,date(smb.report_date) + 30 AS post_date
	,smb.email_address
	,CASE WHEN smb.recommend_source = 'BY CART' THEN 'BY RDS' ELSE smb.recommend_source END AS recommend_source
	,smb.recommend_source_detail
	,smb.e_catalog_source
FROM dim_ca.dim_pub_part_info pm
INNER JOIN ods_gbl.ods_daas_mygbldaas_smb_auto_recommend smb
ON pm.sku_no = smb.recommend_sku_no
left join dim_ca.dim_pub_vpl_info vpl
on pm.vpl_no = vpl.vpl_no
where (smb.country_code= 'CA' OR smb.country_code IS NULL)
and date(smb.report_date) >= DATE_TRUNC('year',ADD_MONTHS(current_date(),-1))
and date(smb.report_date) < DATE_TRUNC('MONTH',current_date())
and smb.report_date not in ('2025-02-26','2025-04-21')
;

drop table if exists rds_ca8328_exclude_cust_sku;
create local temporary table rds_ca8328_exclude_cust_sku on commit preserve rows as
SELECT DISTINCT dw.mcust_no
	,dw.sku_no
FROM dw_ca.dwd_disty_common_dw_orders_pl_extend_di dw
INNER JOIN rds_ca8328_sku_list sl
ON dw.mcust_no = sl.cust_no
AND dw.sku_no = sl.sku_no
AND dw.date_flag >= sl.pre_date
and dw.date_flag <= sl.email_date
where dw.order_type > 0
AND dw.net_sales > 0
;


drop table if exists rds_ca8328_rn;
create local temporary table rds_ca8328_rn on commit preserve rows as
SELECT sl.email_date
	,dw.order_no
	,dw.order_line_no
	,dw.mcust_no
	,ch.cust_name
	,dw.vend_no
	,sl.vend_name
	,dw.sku_no
	,ship_qty
	,sl.vpl_no
	,sl.vpl_desc
	,sl.vpc_group_id
	,sl.vpc_group_desc
	,dw.date_flag
	,dw.net_sales
	,dw.net_cost
	,dw.ngm_amt
	,round(COALESCE(dw.ngm_amt / NULLIF(dw.net_sales,0), 0),2) as NGM_Percent
	,ch.sales_terr
	,ch.sales_terr_name
	,'(' || ch.cust_type || ')' || ch.cust_type_descr as Cust_Type
	,sl.mfg_partno
	,sl.recommend_source
	,sl.recommend_source_detail
	,sl.e_catalog_source
	,row_number() over(partition by dw.order_no,dw.order_line_no order by sl.email_date desc,case when sl.recommend_source='BY AI' then 1 else 2 end) as rn
FROM dw_ca.dwd_disty_common_dw_orders_pl_extend_di dw
INNER JOIN dim_ca.dim_pub_customer_info ch
ON dw.mcust_no = ch.cust_no
INNER JOIN rds_ca8328_sku_list sl
ON dw.mcust_no = sl.cust_no
AND dw.sku_no = sl.sku_no
AND dw.date_flag >= sl.email_date
AND dw.date_flag <= sl.post_date
where dw.order_type > 0
and dw.net_sales > 0
and ch.sales_terr not in (12,126,131,135,136,149,153,154,157,160,179,181,191,228,237,240,250,47)
and ch.cust_type in (199,200)
and NOT EXISTS (SELECT 1 FROM rds_ca8328_exclude_cust_sku cs WHERE cs.mcust_no = dw.mcust_no AND cs.sku_no = dw.sku_no)
;

drop table if exists rds_ca8328_final;
create local temporary table rds_ca8328_final on commit preserve rows as
select email_date            as 'Email Date'
    ,TO_CHAR(email_date, 'Mon') as 'Email Month'
    ,order_no                as 'Order#'
    ,order_line_no           as 'Order Line#'
    ,mcust_no                as 'Cust#'
    ,cust_name               as 'Cust Name'
    ,vend_no                 as 'Vend#'
    ,vend_name               as 'Vend Name'
    ,sku_no                  as 'SKU#'
    ,ship_qty                as 'Ship Qty'
    ,vpl_no                  as 'VPL Number'
    ,vpl_desc                as 'VPL Desc'
	,vpc_group_id            as 'VPC Group ID'
	,vpc_group_desc          as 'Group Name'
    ,date_flag               as 'Order Date'
    ,net_sales               as 'Net Sales'
    ,net_cost                as 'Cost'
    ,ngm_amt                 as 'NGM'
    ,NGM_Percent             as 'NGM Percent'
    ,sales_terr              as 'Sales Terr'
    ,sales_terr_name         as 'Terr Name'
    ,Cust_Type               as 'Cust Type'
    ,mfg_partno              as 'MFG Part#'
    ,recommend_source        as 'Recommend Source'
    ,COALESCE(REGEXP_SUBSTR(recommend_source, '^[^,]+'), recommend_source) as 'Initial Recommend Source'
    ,recommend_source_detail as 'Recommend Source Detail'
    ,COALESCE(REGEXP_SUBSTR(recommend_source_detail, '^[^,]+'), recommend_source_detail) as 'Initial Recommend Source Detail'
    ,e_catalog_source        as 'E Catalog Source'
from rds_ca8328_rn
where rn = 1
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_ca8328_final
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
-- 1