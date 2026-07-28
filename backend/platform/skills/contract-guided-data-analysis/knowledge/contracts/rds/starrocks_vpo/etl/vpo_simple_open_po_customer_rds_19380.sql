drop table if exists tempdb.rds_tmp;
drop table if exists tempdb.rds_tmp_body;

drop table if exists tempdb.rds_us_sku_19380;
create table tempdb.rds_us_sku_19380 as
select
  a.vend_no,
  a.sku_no,
  a.mfg_partno,
  a.po_cost as base_cost
from dim_us.dim_pub_part_info a
where a.vend_no = 36035
;

drop table if exists tempdb.rds_us_orders_19380;
create table tempdb.rds_us_orders_19380 as
select
  a.order_no as po_no,
  b.order_line_no as po_ln_no,
  c.mfg_partno,
  b.order_qty,
  b.order_qty - ifnull(b.rec_qty, 0) as open_qty,
  ifnull(b.rec_qty, 0) as rec_qty,
  date_format(a.sales_rel_date, '%m/%d/%Y') as sales_rel_date,
  aa.ext_ref as cpo,
  a.to_acct_no as cust_no,
  e.cust_name,
  c.base_cost
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b
        on a.order_no = b.order_no
       and a.order_type = b.order_type
       and b.delete_date is null
       and b.order_qty > ifnull(b.rec_qty, 0)
inner join tempdb.rds_us_sku_19380 c
        on b.sku_no = c.sku_no
 left join ods_us.ods_cis_corp_order_header_rt aa
        on a.int_ref_no = aa.order_no
       and a.int_ref_type = aa.order_type = 1
       and aa.from_loc_no = 98
 left join ods_us.ods_cis_corp_customer_header_rt e
        on a.to_acct_no = e.cust_no
where a.order_type = 2
  and a.delete_date is null
;

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select
  a.po_no as 'PO#',
  a.mfg_partno as 'MFG#',
  a.order_qty as 'Order qty',
  a.open_qty as 'Open QTY',
  a.rec_qty as 'Rec QTY',
  a.sales_rel_date as 'PO release date',
  a.cpo as 'Customer PO#',
  a.cust_name as 'Customer Name'
from tempdb.rds_us_orders_19380 a
order by a.po_no, a.po_ln_no
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;

drop table if exists tempdb.rds_us_sku_19380;
drop table if exists tempdb.rds_us_orders_19380;
