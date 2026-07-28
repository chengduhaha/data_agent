drop table if exists tempdb.rds_tmp;
drop table if exists tempdb.rds_tmp_body;

drop table if exists tempdb.rds_us_sku_18013;
create table tempdb.rds_us_sku_18013 as
select
  a.vend_no,
  a.vend_name,
  a.prod_code,
  a.vpl_no,
  a.sku_no,
  a.part_no,
  a.mfg_partno,
  a.ave_cost as sys_cost,
  a.po_cost,
  a.abc_code
from dim_us.dim_pub_part_info a
where a.vend_no = 65505
-- and a.sku_no = 14781378
;

drop table if exists tempdb.rds_us_orders_18013;
create table tempdb.rds_us_orders_18013 as
select
  a.to_inv_type as inv_type,
  a.to_loc_no as loc_no,
  c.vend_no,
  c.vend_name,
  c.prod_code,
  c.vpl_no,
  a.int_ref_no as mso,
  a.order_no as po_no,
  b.order_line_no as po_ln_no,
  c.sku_no,
  c.part_no,
  c.mfg_partno,
  c.sys_cost,
  b.unit_cost as base_cost,
  b.order_qty,
  b.order_qty - ifnull(b.rec_qty, 0) as open_qty,
  ifnull(b.rec_qty, 0) as rec_qty,
  c.abc_code,
  a.entry_datetime as entry_date,
  a.entry_id as entry_id,
  concat(d.firstname, ' ', d.lastname) as entry_name,
  concat(m.firstname, ' ', m.lastname) as buyer,
  date_format(a.sales_rel_date, '%m/%d/%Y') as sales_rel_date,
  date_format(a.expected_date, '%m/%d/%Y') as expected_date,
  date_format(b.prod_exp_date, '%m/%d/%Y') as ship_date,
  date_format(b.expected_date, '%m/%d/%Y') as eta_date,
  g.eta_code,
  cast(null as varchar(360)) as vendor_quote_id,
  aa.ext_ref as cpo,
  a.to_acct_no as cust_no,
  e.cust_name,
  a.sales_terr,
  f.terr_name,
  a.ship_to_name as end_user_name
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b
        on a.order_no = b.order_no
       and a.order_type = b.order_type
       and b.delete_date is null
       and b.order_qty > ifnull(b.rec_qty, 0)
inner join tempdb.rds_us_sku_18013 c
        on b.sku_no = c.sku_no
 left join ods_us.ods_cis_corp_order_header_rt aa
        on a.int_ref_no = aa.order_no
       and a.int_ref_type = aa.order_type = 1
       and aa.from_loc_no = 98
 left join ods_us.ods_cis_corp_manager_rt d
        on a.entry_id = d.userid
 left join ods_us.ods_cis_corp_customer_header_rt e
        on a.to_acct_no = e.cust_no
 left join ods_us.ods_cis_corp_territory_rt f
        on a.sales_terr = f.sales_terr
 left join ods_us.ods_cis_corp_order_eta_code_rt g
        on b.order_no = g.order_no
       and b.order_type = g.order_type
       and b.order_line_no = g.order_line_no
 left join ods_us.ods_cis_corp_vend_user_matrix_rt vum
        on c.vend_no = vum.vend_no
       and (c.vpl_no = vum.vpl_no or vum.vpl_no = -1)
       and vum.profile_type = 'BUYR'
 left join ods_us.ods_cis_corp_manager_rt m
        on vum.primary_id = m.userid
where a.order_type = 2
and a.delete_date is null
-- and a.order_no = 37938104
;

drop table if exists tempdb.rds_us_vendor_mso_18013;
create table tempdb.rds_us_vendor_mso_18013 as
select
b.order_no,
b.profile_c
from tempdb.rds_us_orders_18013 a
inner join ods_us.ods_cis_corp_history_profile b on b.order_no = a.mso and b.order_type = 1
where a.mso is not null
and b.profile_type = 'SAPID'
and b.profile_cat = 'ORDR'
and b.profile_c is not null
union
select
b.order_no,
b.profile_c
from tempdb.rds_us_orders_18013 a
inner join ods_us.ods_cis_corp_order_profile b on b.order_no = a.mso and b.order_type = 1
where a.mso is not null
and b.profile_type = 'SAPID'
and b.profile_cat = 'ORDR'
and b.profile_c is not null
;

drop table if exists tempdb.rds_us_vendor_po_18013;
create table tempdb.rds_us_vendor_po_18013 as
select
b.order_no,
b.vend_so_no as profile_c
from tempdb.rds_us_orders_18013 a
inner join ods_us.ods_cis_corp_order_eta_code_rt b on b.order_no = a.po_no and b.order_type = 2
where b.vend_so_no is not null
union
select
b.order_no,
b.vend_so_no as profile_c
from tempdb.rds_us_orders_18013 a
inner join ods_us.ods_cis_corp_history_eta_code_rt b on b.order_no = a.po_no and b.order_type = 2
where b.vend_so_no is not null
;

drop table if exists tempdb.rds_us_orders_2_18013;
create table tempdb.rds_us_orders_2_18013 as
select distinct
  a.inv_type,
  a.loc_no,
  a.vend_no,
  a.vend_name,
  a.prod_code,
  a.vpl_no,
  a.mso,
  a.po_no,
  a.po_ln_no,
  a.sku_no,
  a.part_no,
  a.mfg_partno,
  a.sys_cost,
  a.base_cost,
  a.order_qty,
  a.open_qty,
  a.rec_qty,
  a.abc_code,
  a.entry_date,
  a.entry_id,
  a.entry_name,
  a.buyer,
  a.sales_rel_date,
  a.expected_date,
  a.ship_date,
  a.eta_date,
  a.eta_code,
  a.vendor_quote_id,
  ifnull(b.profile_c, c.profile_c) as vendor_so,
  a.cpo,
  a.cust_no,
  a.cust_name,
  a.sales_terr,
  a.terr_name,
  a.end_user_name
from tempdb.rds_us_orders_18013 a
left join tempdb.rds_us_vendor_mso_18013 b on a.mso = b.order_no
left join tempdb.rds_us_vendor_po_18013 c on a.po_no = c.order_no
;

-- select * from tempdb.rds_us_orders_2_18013 where po_no = 38764085

drop table if exists tempdb.rds_us_report_18013;
create table tempdb.rds_us_report_18013 as
with vendor_quote as (
    select
        order_no,
        max(data_c) as vendor_quote_id
    from (
        select
            b.order_no,
            b.data_c
        from ods_us.ods_cis_corp_order_eu_custom_rt b
        join ods_us.ods_cis_corp_eu_custom_map_rt c
          on b.eu_map_id = c.eu_map_id
         and b.eu_map_line_no = c.eu_map_line_no
        join dim_us.dim_pub_list_box_detail d
          on c.map_data_desc = d.code_value
         and d.list_box_code = 'CEDM'
         and d.code_desc = 'Vendor Quote ID'
        where b.order_type = 1
          and b.delete_date is null
    ) x
    group by order_no
),
eta_src_profile as (
    select
        order_no,
        profile_no,
        max(profile_i) as profile_i
    from ods_us.ods_cis_corp_order_profile_rt
    where order_type = 2
      and profile_type = 'ETASRC'
    group by
        order_no,
        profile_no
),
src_list as (
    select
        cast(code_value as int) as code_value_int,
        max(code_desc) as code_desc
    from dim_us.dim_pub_list_box_detail
    where list_box_code = 'SRC'
    group by cast(code_value as int)
)
select
  a.inv_type,
  a.loc_no,
  a.vend_no,
  a.vend_name,
  a.prod_code,
  a.vpl_no,
  a.mso,
  a.po_no,
  a.po_ln_no,
  a.sku_no,
  a.part_no,
  a.mfg_partno,
  a.sys_cost,
  a.base_cost,
  a.order_qty,
  a.open_qty,
  a.rec_qty,
  a.abc_code,
  a.entry_date,
  a.entry_id,
  a.entry_name,
  a.buyer,
  a.sales_rel_date,
  a.expected_date,
  a.ship_date,
  a.eta_date,
  a.eta_code,
  l.code_desc,
  vq.vendor_quote_id,
  a.vendor_so,
  a.cpo,
  a.cust_no,
  a.cust_name,
  a.sales_terr,
  a.terr_name,
  a.end_user_name
from tempdb.rds_us_orders_2_18013 a
left join vendor_quote vq
  on a.mso = vq.order_no
left join eta_src_profile p
  on a.po_no = p.order_no
 and a.po_ln_no = p.profile_no
left join src_list l
  on p.profile_i = l.code_value_int
;


drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select
 a.inv_type as 'Inv Type',
 a.loc_no as 'Loc#',
 a.vend_no as 'Vend#',
 a.vend_name as 'Vend Name',
 a.prod_code as 'PM Code',
 a.vpl_no as 'VPL#',
 a.mso as 'MSO# / B2B BO#',
 a.po_no as 'PO#',
 a.po_ln_no as 'PO LN#',
 a.sku_no as 'SKU#',
 a.part_no as 'Part',
 a.mfg_partno as 'Mfg#',
 a.sys_cost as 'Sys Cost',
 a.base_cost as 'Base Cost',
 a.order_qty as 'Order Qty',
 a.open_qty as 'Open Qty',
 a.rec_qty as 'Rec Qty',
 a.abc_code as 'ABC',
 a.entry_date as 'Entry Date',
 a.entry_id as 'Entry ID',
 a.entry_name as 'Entry Name',
 a.buyer as 'Buyer',
 a.sales_rel_date as 'PO Rel Date',
 a.expected_date as 'Request ETA',
 a.ship_date as 'Ship Date',
 a.eta_date as 'ETA Date',
 a.eta_code as 'ETA Code',
 a.code_desc as 'ETA Source',
 a.vendor_quote_id as 'Vendor Quote ID',
 a.vendor_so as 'Vendor SO#',
 a.cpo as 'Cust PO',
 a.cust_no as 'Cust#',
 a.cust_name as 'Reseller Name',
 a.end_user_name as 'End User Name',
 a.sales_terr as 'sales_terr',
 a.terr_name as 'terr_name'
from tempdb.rds_us_report_18013 a
order by a.po_no, a.po_ln_no
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;

drop table if exists tempdb.rds_us_sku_18013;
drop table if exists tempdb.rds_us_orders_18013;
drop table if exists tempdb.rds_us_vendor_mso_18013;
drop table if exists tempdb.rds_us_vendor_po_18013;
drop table if exists tempdb.rds_us_orders_2_18013;
drop table if exists tempdb.rds_us_report_18013;
