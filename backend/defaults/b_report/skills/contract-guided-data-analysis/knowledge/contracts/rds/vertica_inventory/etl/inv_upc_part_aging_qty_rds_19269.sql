drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists table_upc_code_us_19269;
create local temporary table table_upc_code_us_19269 on commit preserve rows as
select distinct upc_code
from dim_us.dim_pub_part_info_rt b
where b.part_no like 'PCW-%'
or b.part_no like 'SNO-%'
;

drop table if exists table_sku_us_19269;
create local temporary table table_sku_us_19269 on commit preserve rows as
select
  b.mfg_partno,
  b.sku_no,
  b.part_no,
  b.upc_code,
  b.vpl_no,
  b.vend_no,
  b.vend_name,
  cast(null as money) as grid_price,
  cast(null as money) as net_price,
  b.po_cost,
  sum(ifnull(c.on_hand_qty,0)) as oh,
  sum(ifnull(c.on_order_qty,0)) as oo,
  cast(null as varchar(80)) as pm_name,
  b.company_no,
  b.long_desc
from table_upc_code_us_19269 a
inner join dim_us.dim_pub_part_info_rt b on a.upc_code = b.upc_code
left join dw_us.dwd_disty_inv_qty_df c on b.sku_no = c.sku_no and c.date_flag = current_date()-1 and c.inv_type in (1,300)
group by
  b.mfg_partno,
  b.sku_no,
  b.part_no,
  b.upc_code,
  b.vpl_no,
  b.vend_no,
  b.vend_name,
  b.po_cost,
  b.company_no,
  b.long_desc
;

update table_sku_us_19269 a
set pm_name = b.pm_name
from dim_us.dim_pub_vpl_pm_hierarchy_info b
where a.vend_no = b.vend_no
and a.vpl_no = b.vpl_no
;

drop table if exists table_sku_list_us_19269;
create local temporary table table_sku_list_us_19269 on commit preserve rows as
select distinct
    a.company_no,
    a.sku_no
from table_sku_us_19269 a
;

drop table if exists rdsetl.rds_tmp_p1_price_input
;
drop table if exists rdsetl.rds_tmp_p1_price_output
;

create table rdsetl.rds_tmp_p1_price_input (
    caller varchar(255) null,
    companyNo integer not null,
    custNo integer not null,
    priceType varchar(20) not null,
    skuNo integer not null,
    currencyType varchar(20) not null
)
;
create table rdsetl.rds_tmp_p1_price_output (
    custNo integer not null,
    skuNo integer not null,
    companyNo integer not null,
    gridPrice decimal(19, 4) null,
    netPrice decimal(19, 4) null,
    unitCost decimal(19, 4) null,
    poCost decimal(19, 4) null,
    retail decimal(19, 4) null,
    cisUnitCost decimal(19, 4) null,
    companyCurrency varchar(255) null,
    custCurrency varchar(255) null,
    vendCurrency varchar(255) null,
    comments varchar(4000) null,
    spaComments varchar(4000) null
)
;

insert into rdsetl.rds_tmp_p1_price_input (caller, companyNo, custNo, priceType, skuNo, currencyType)
select
    'RDS_CALL_PRICE_API' as caller,
    a.company_no as companyNo,
    462198 as custNo,
    'QI' as priceType,
    a.sku_no as skuNo,
    'companyCurrency' as currencyType
from table_sku_list_us_19269 a
;

[PRICE_API_DATA_FETCH]
;

drop table if exists rds_us_report_19269;
create local temporary table rds_us_report_19269 on commit preserve rows as
select distinct
  b.mfg_partno,
  b.sku_no,
  b.part_no,
  b.upc_code,
  b.vend_no,
  b.vend_name,
  case when a.custNo = 462198 then a.gridPrice else null end as grid_price,
  case when a.custNo = 462198 then a.netPrice else null end as net_price,
  b.po_cost,
  b.oh,
  b.oo,
  b.pm_name,
  b.long_desc
from table_sku_us_19269 b
left join rdsetl.rds_tmp_p1_price_output a
    on a.skuNo = b.sku_no
    and a.companyNo = b.company_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
  mfg_partno as 'MFR PART',
  sku_no as 'SKU',
  part_no as 'PART',
  upc_code as 'UPC',
  vend_no as 'Vendor #',
  vend_name as 'Vendor Name',
  max(grid_price) as 'GRID PRICE$ (use C#462198)',
  max(net_price) as 'NET PRICE$ (use C#462198)',
  po_cost as 'BASE COST$',
  oh as 'OnHand QTY',
  oo as 'OnOrder QTY',
  pm_name as 'PM Name',
  long_desc as 'Long Description'
from rds_us_report_19269 b
group by
  mfg_partno,
  sku_no,
  part_no,
  upc_code,
  vend_no,
  vend_name,
  po_cost,
  oh,
  oo,
  pm_name,
  long_desc
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select
    1 as flag,
    'Standard' as body_type,
    count(*) as cnt
from rdsetl.rds_tmp
;
