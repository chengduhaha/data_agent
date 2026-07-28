drop table if exists tempdb.tmp_us_report_17251;
create table tempdb.tmp_us_report_17251 as
select a.order_no as 'Order #',
    b.entry_datetime as 'Order Date',
    a.order_type as 'Order type',
    a.order_line_no as 'Order Line#',
    a1.to_acct_no as 'Cust',
    f.cust_name as 'Cust Name',
    b.order_qty as 'Qty',
    a.int_ref_no as 'Synnex PO#',
    a.entry_datetime as 'PO Created Date',
    b.sku_no as 'SKU',
    c.mfg_partno as 'MFG Part#',
    c.part_no as 'Part#',
    a1.from_loc_no as 'Warehouse',
    concat(d.firstname, ' ', d.lastname) as 'Creator',
    a1.sales_terr as 'Sales Terr#',
    e.terr_name as 'Sales Terr Name',
--     case when a1.ship_date is not null
--          then 'Yes'
--          else 'No'
--      end as 'ORDER STATUS SHIP COMPLETE',
    h.profile_c as 'ORDER STATUS SHIP COMPLETE',
    case when a1.delete_date is not null
         then 'Yes'
         else 'No'
     end as 'ORDER Delete Status',
    a1.ship_method as 'Ship Method Status',
    a1.invoice_date as 'Invoice Date',
    concat(g.firstname, ' ', g.lastname) as 'SALES ORDER CREATOR',
    a1.ext_ref as 'Customer PO#'
from ods_us.ods_cis_corp_mc_order_ref_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b
        on a.order_no = b.order_no
       and a.order_type = b.order_type
       and a.order_line_no = b.order_line_no
       and b.delete_date is null
inner join dim_us.dim_pub_part_info c
        on c.sku_no = b.sku_no
inner join ods_us.ods_cis_corp_order_header_rt a1
        on b.order_no = a1.order_no
       and b.order_type = a1.order_type
       and a1.delete_date is null
inner join ods_us.ods_cis_corp_manager_rt d
        on a.entry_id = d.userid
inner join ods_us.ods_cis_corp_territory_rt e
        on a1.sales_terr = e.sales_terr
inner join ods_us.ods_customer_mymdm_customer_header_rt f
        on a1.to_acct_no = f.cust_no
inner join ods_us.ods_cis_corp_manager_rt g
        on a1.entry_id = g.userid
left join ods_us.ods_cis_corp_order_profile_rt h
		on a.order_no = h.order_no and h.order_type IN (1,8) and h.profile_type = 'SHIP_CPLE' and h.active = 'Y'
where c.vend_no IN (81051)

union

select a.order_no as 'Order #',
    b.entry_datetime as 'Order Date',
    a.order_type as 'Order type',
    a.order_line_no as 'Order Line#',
    a1.to_acct_no as 'Cust',
    f.cust_name as 'Cust Name',
    b.order_qty as 'Qty',
    a.int_ref_no as 'Synnex PO#',
    a.entry_datetime as 'PO Created Date',
    b.sku_no as 'SKU',
    c.mfg_partno as 'MFG Part#',
    c.part_no as 'Part#',
    a1.from_loc_no as 'Warehouse',
    concat(d.firstname, ' ', d.lastname) as 'Creator',
    a1.sales_terr as 'Sales Terr#',
    e.terr_name as 'Sales Terr Name',
    --     case when a1.ship_date is not null
--          then 'Yes'
--          else 'No'
--      end as 'ORDER STATUS SHIP COMPLETE',
    h.profile_c as 'ORDER STATUS SHIP COMPLETE',
    case when a1.delete_date is not null
         then 'Yes'
         else 'No'
     end as 'ORDER Delete Status',
    a1.ship_method as 'Ship Method Status',
    a1.invoice_date as 'Invoice Date',
    concat(g.firstname, ' ', g.lastname) as 'SALES ORDER CREATOR',
    a1.ext_ref as 'Customer PO#'
from ods_us.ods_cis_corp_mc_order_ref_rt a
inner join ods_us.ods_cis_corp_history_detail_rt b
        on a.order_no = b.order_no
       and a.order_type = b.order_type
       and a.order_line_no = b.order_line_no
       and b.delete_date is null
inner join dim_us.dim_pub_part_info c
        on c.sku_no = b.sku_no
inner join ods_us.ods_cis_corp_history_header_rt a1
        on b.order_no = a1.order_no
       and b.order_type = a1.order_type
       and a1.delete_date is null
inner join ods_us.ods_cis_corp_manager_rt d
        on a.entry_id = d.userid
inner join ods_us.ods_cis_corp_territory_rt e
        on a1.sales_terr = e.sales_terr
inner join ods_us.ods_customer_mymdm_customer_header_rt f
        on a1.to_acct_no = f.cust_no
inner join ods_us.ods_cis_corp_manager_rt g
        on a1.entry_id = g.userid
left join ods_us.ods_cis_corp_order_profile_rt h
		on a.order_no = h.order_no and h.order_type IN (1,8) and h.profile_type = 'SHIP_CPLE' and h.active = 'Y'
where c.vend_no IN (81051)
;

drop table if exists tempdb.tmp_us_sku_17251;
create table tempdb.tmp_us_sku_17251  as
select distinct SKU as sku_no
from tempdb.tmp_us_report_17251
;

drop table if exists tempdb.tmp_us_oh_17251;
create table tempdb.tmp_us_oh_17251  as
select a.sku_no,inv_type
    ,sum(on_hand_qty) as on_hand
    ,sum(on_hand_qty - bo_qty + intran_in - intran_out - alloc_qty) as avail
from tempdb.tmp_us_sku_17251 a
inner join ods_us.ods_dw_prod_dws_dw_inv_qty b on a.sku_no = b.sku_no
    and b.inv_type = 1
    and b.date_flag = date_add(current_date(), interval -1 day)
group by a.sku_no,inv_type
;

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select a.*,
    ifnull(on_hand,0) as 'On Hand',
    ifnull(avail,0) as 'UNITS AVAILABLE'
from tempdb.tmp_us_report_17251 a
left join  tempdb.tmp_us_oh_17251 b  ON a.SKU = b.sku_no
;

-- 1
drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;