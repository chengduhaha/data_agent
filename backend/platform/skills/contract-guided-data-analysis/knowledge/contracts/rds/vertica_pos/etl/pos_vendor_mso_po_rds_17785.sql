drop table if exists rds_us_sku_17785;
create local temporary table rds_us_sku_17785 on commit preserve rows as
select
  vend_no,
  vend_name,
  sku_no,
  mfg_partno
from dim_us.dim_pub_part_info
where vend_no = 48620
;

drop table if exists rds_us_report_17785;
create local temporary table rds_us_report_17785 on commit preserve rows as
select
  a.order_no,
  a.order_type,
  a.order_line_no,
  a.mso_no,
  a.synnex_po_no,
  a.cpo_no,
  a.ship_date,
  a.vend_no,
  a.vend_name,
  a.sku_no,
  a.part_no,
  a.mfg_partno,
  a.part_desc,
  a.ship_qty,
  a.base_cost,
  a.extend_base_cost,
  a.prod_code,
  a.sales_terr,
  a.terr_name,
  a.from_loc_no,
  a.from_loc_char,
  a.ship_method,
  a.master_cust_no,
  a.master_cust_name,
  a.bill_to_cust_no,
  a.bill_to_cust_name,
  a.sold_to_cust_no,
  a.sold_to_cust_name,
  a.ship_to_name,
  a.ship_to_addr,
  a.ship_to_city,
  a.ship_to_zip,
  a.ship_to_state,
  a.bill_to_cust_zip,
  a.bill_to_cust_state,
  a.bill_to_cust_city,
  a.bill_to_cust_addr,
  a.order_entry_datetime,
  a.serial_no
 from dw_us.dwd_disty_common_pos_di a
inner join rds_us_sku_17785 b on a.sku_no = b.sku_no
where a.date_flag >= cast(trunc(timestampadd (dd, -1, getdate()), 'year') as date)
  and a.date_flag < current_date()
  and a.order_line_type != 'Comp'
  and a.order_type <> 114
;

drop table if exists rds_us_order_info_17785;
create local temporary table rds_us_order_info_17785 on commit preserve rows as
select distinct
  a.order_no,
  a.order_type,
  a.order_line_no
from rds_us_report_17785 a
;

drop table if exists rds_us_spa_17785;
create local temporary table rds_us_spa_17785 on commit preserve rows as
select
       a.order_no,
       a.order_type,
       a.order_line_no,
       listagg(distinct ifnull(a.spa_no, -scm_no) using PARAMETERS max_length=4096, separator=', ', on_overflow='TRUNCATE') as spa_no
from dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di a
inner join rds_us_order_info_17785 b on a.order_no = b.order_no and a.order_type = b.order_type and a.order_line_no = b.order_line_no
group by
       a.order_no,
       a.order_type,
       a.order_line_no
;

--select * from rds_us_spa_17785
drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
  a.order_no,
  a.order_type,
  a.order_line_no,
  a.mso_no,
  a.synnex_po_no,
  a.cpo_no,
  a.ship_date,
  a.vend_no,
  a.vend_name,
  a.sku_no,
  a.part_no,
  a.mfg_partno,
  a.part_desc,
  a.ship_qty,
  a.base_cost,
  a.extend_base_cost,
  a.prod_code,
  a.sales_terr,
  a.terr_name,
  a.from_loc_no,
  a.from_loc_char,
  a.ship_method,
  a.master_cust_no,
  a.master_cust_name,
  a.bill_to_cust_no,
  a.bill_to_cust_name,
  a.sold_to_cust_no,
  a.sold_to_cust_name,
  a.ship_to_name,
  a.ship_to_addr,
  a.ship_to_city,
  a.ship_to_zip,
  a.ship_to_state,
  a.bill_to_cust_zip,
  a.bill_to_cust_state,
  a.bill_to_cust_city,
  a.bill_to_cust_addr,
  a.order_entry_datetime,
  a.serial_no,
  b.spa_no
from rds_us_report_17785 a
left join rds_us_spa_17785 b on a.order_no = b.order_no and a.order_type = b.order_type and a.order_line_no = b.order_line_no
order by
  a.order_no,
  a.order_type,
  a.order_line_no
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

drop table if exists rds_us_sku_17785;
drop table if exists rds_us_report_17785;
drop table if exists rds_us_order_info_17785;
drop table if exists rds_us_spa_17785;
