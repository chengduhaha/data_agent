drop table if exists tempdb.rds_us17936_order;
create table tempdb.rds_us17936_order primary key(id) distributed by hash(id) as
select
     uuid_numeric() as id
    ,a.sales_terr
    ,a.to_acct_no
    ,c.cust_name as cust_name
    ,date_format(a.entry_datetime,'%m/%d/%Y') as po_date
    ,a.ext_ref
    ,a.order_no
    ,b.order_type
    ,b.order_line_no
    ,b.sku_no
    ,b.order_qty
    ,ifnull(b.unit_price,0) as Revenue
    ,a.from_loc_no
    ,case when a.from_loc_no = 98 and a.order_type = 1 and a.int_ref_type = 2 then a.int_ref_no else null end as vpo_no
    ,cast(null as datetime) as po_date_time
    ,cast(null as varchar(5700)) as license_type
    ,cast(null as varchar(5700)) as service_duration
    ,case when a.delete_date is not null then 'Deleted'
          when a.schedule_date is not null then 'Closed Date'
          when a.invoice_date is not null then 'Expired'
          when a.ship_date is not null then 'Invoiced'
          when a.qc_date is not null then 'Shipped'
          when a.pick_date is not null then 'QC Date'
          when a.credit_rel_date is not null then 'Picked'
          when a.sales_rel_date is not null then 'Credit Released'
          when a.issue_date is not null then 'Sales Released'
          else 'Queued'
     end current_queue
    ,case when a.delete_date is not null then 'Deleted'
          when a.schedule_date is not null then 'Expired'
          when a.invoice_date is not null then 'Invoiced'
          when a.ship_date is not null then 'Shipped'
          when a.qc_date is not null then 'QC Date'
          when a.pick_date is not null then 'Picked'
          when a.credit_rel_date is not null then 'Credit Released'
          when a.sales_rel_date is not null then 'Sales Released'
          when a.issue_date is not null then 'Queued'
          else 'Created Date'
     end last_completed_queue
    ,case when a.delete_date is not null then a.delete_date
          when a.schedule_date is not null then a.schedule_date
          when a.invoice_date is not null then a.invoice_date
          when a.ship_date is not null then a.ship_date
          when a.qc_date is not null then a.qc_date
          when a.pick_date is not null then a.pick_date
          when a.credit_rel_date is not null then a.credit_rel_date
          when a.sales_rel_date is not null then a.sales_rel_date
          when a.issue_date is not null then a.issue_date
          else a.entry_datetime
     end date_timestamp,
     concat(d.firstname, ' ', d.lastname) as entry_name,
     cast(null as varchar(360)) as multiterm_billing
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type
left join ods_us.ods_cis_corp_customer_header_rt c on a.to_acct_no=c.cust_no
left join ods_us.ods_cis_corp_manager_rt d on a.entry_id = d.userid
where a.sales_terr in (4404,4405)
and a.delete_date is null
and b.delete_date is null
and a.order_type in (1,8,148)
and ifnull(b.ship_qty,0)<>b.order_qty
and a.from_loc_no <> 98
union
select
     uuid_numeric() as id
    ,a.sales_terr
    ,a.to_acct_no
    ,c.cust_name as cust_name
    ,date_format(a.entry_datetime,'%m/%d/%Y') as po_date
    ,a.ext_ref
    ,a.order_no
    ,b.order_type
    ,b.order_line_no
    ,b.sku_no
    ,b.order_qty
    ,ifnull(b.unit_price,0) as Revenue
    ,a.from_loc_no
    ,case when a.from_loc_no = 98 and a.order_type = 1 and a.int_ref_type = 2 then a.int_ref_no else null end as vpo_no
    ,cast(null as datetime) as po_date_time
    ,cast(null as varchar(5700)) as license_type
    ,cast(null as varchar(5700)) as service_duration
    ,case when a.delete_date is not null then 'Deleted'
          when a.qc_date is not null then 'Completed'
          when a.credit_rel_date is not null then 'VPO Released'
          when a.sales_rel_date is not null then 'Credit Released'
          when a.issue_date is not null then 'Sales Released'
          else 'Queued'
     end current_queue
    ,case when a.delete_date is not null then 'Deleted'
          when a.closed_date is not null then 'Completed'
          when a.qc_date is not null then 'VPO Released'
          when a.credit_rel_date is not null then 'Credit Released'
          when a.sales_rel_date is not null then 'Sales Released'
          when a.issue_date is not null then 'Queued'
          else 'Created Date'
     end last_completed_queue
    ,case when a.delete_date is not null then a.delete_date
          when a.closed_date is not null then a.closed_date
          when a.qc_date is not null then a.qc_date
          when a.credit_rel_date is not null then a.credit_rel_date
          when a.sales_rel_date is not null then a.sales_rel_date
          when a.issue_date is not null then a.issue_date
          else a.entry_datetime
     end date_timestamp,
     concat(d.firstname, ' ', d.lastname) as entry_name,
     cast(null as varchar(360)) as multiterm_billing
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type
left join ods_us.ods_cis_corp_customer_header_rt c on a.to_acct_no=c.cust_no
left join ods_us.ods_cis_corp_manager_rt d on a.entry_id = d.userid
where a.sales_terr in (4404,4405)
and a.delete_date is null
and b.delete_date is null
and a.order_type in (1,8,148)
and a.from_loc_no = 98
and a.int_ref_type = 8
;

update tempdb.rds_us17936_order
set multiterm_billing = a.data_c
from ods_us.ods_cis_corp_order_eu_custom_rt a, ods_us.ods_cis_corp_eu_custom_map_rt b, ods_us.ods_cis_corp_list_box_detail_rt c
where a.order_type = tempdb.rds_us17936_order.order_type
and a.order_no = tempdb.rds_us17936_order.order_no
and a.eu_map_id = b.eu_map_id
and a.eu_map_line_no = b.eu_map_line_no
and c.code_value = b.map_data_desc
and c.list_box_code = 'CEDM'
and c.code_desc in ('Multiterm Billing')
;

update tempdb.rds_us17936_order
set vpo_no = b.int_ref_no,
    po_date_time = b.entry_datetime
from ods_us.ods_cis_corp_mc_order_ref_rt b
where rds_us17936_order.order_no = b.order_no
and rds_us17936_order.order_type = b.order_type
and rds_us17936_order.order_line_no = b.order_line_no
and rds_us17936_order.vpo_no
and b.delete_id is null
and b.order_type = 8
;
update tempdb.rds_us17936_order
set vpo_no = b.order_no,
    po_date_time = b.entry_datetime
from ods_us.ods_cis_corp_order_header_rt b
where rds_us17936_order.order_no = b.int_ref_no
and rds_us17936_order.order_type = b.int_ref_type
and b.delete_id is null
and b.order_type = 2
;

update tempdb.rds_us17936_order
set license_type = a.content
from ods_us.ods_cis_corp_tc_value_en a, ods_us.ods_cis_corp_tc_part_technotes_en b, ods_us.ods_cis_corp_tc_attribute_en c
where tempdb.rds_us17936_order.sku_no = b.sku_no
and a.id = b.value_id
and b.attribute_id = c.id
and c.content = 'License Type'
;

update tempdb.rds_us17936_order
set service_duration = a.content
from ods_us.ods_cis_corp_tc_value_en a, ods_us.ods_cis_corp_tc_part_technotes_en b, ods_us.ods_cis_corp_tc_attribute_en c
where tempdb.rds_us17936_order.sku_no = b.sku_no
and a.id = b.value_id
and b.attribute_id = c.id
and c.content = 'Service Duration'
;

drop table if exists tempdb.rds_us17936_temp1;
create table tempdb.rds_us17936_temp1 as
select a.sales_terr
    ,a.to_acct_no
    ,a.cust_name
    ,a.po_date
    ,a.ext_ref
    ,a.order_no
    ,a.sku_no
    ,b.mfg_partno as mfg_partno
    ,b.short_desc as short_desc
    ,a.order_qty
    ,a.Revenue
    ,a.order_type
    ,a.order_line_no
    ,a.from_loc_no
    ,l.loc_char as loc_char
    ,b.vend_no as vend_no
    ,vm.vend_name as vend_name
    ,a.vpo_no
    ,po_date_time
    ,license_type
    ,service_duration
    ,current_queue
    ,last_completed_queue
    ,date_timestamp
    ,entry_name
    ,multiterm_billing
from tempdb.rds_us17936_order a
left join ods_us.ods_cis_corp_part_master_rt b on a.sku_no=b.sku_no
left join ods_us.ods_cis_corp_vend_master_rt vm on b.vend_no=vm.vend_no
left join ods_us.ods_cis_corp_location_info_rt l on a.from_loc_no=l.loc_no
;


drop table if exists tempdb.rds_us17936_exp;
create table tempdb.rds_us17936_exp as
select a.order_no
    ,a.order_type
    ,a.order_line_no
    ,sum(ifnull(unit_exp,0)) as exp_amt
from tempdb.rds_us17936_temp1 a
inner join ods_us.ods_cis_corp_order_exp_rt b
on b.order_no=a.order_no
and b.order_type=a.order_type
and b.order_line_no=a.order_line_no
and b.delete_date is null
group by a.order_no,a.order_type,a.order_line_no
;

drop table if exists tempdb.rds_us17936_temp2;
create table tempdb.rds_us17936_temp2 as
with min_eta as
( select
        order_no,
        order_type,
        order_line_no,
        date_format(min(eta),'%m/%d/%Y') as min_eta
   from dm_us.dm_pur_unieta_boso_detail_rt eta
   group by order_no, order_type, order_line_no
)
select a.sales_terr
    ,a.to_acct_no
    ,a.cust_name
    ,a.po_date
    ,a.ext_ref
    ,a.order_no
    ,a.sku_no
    ,a.mfg_partno
    ,a.short_desc
    ,c.min_eta as ETA_date
    ,a.order_qty
    ,(a.Revenue+ifnull(b.exp_amt,0))*order_qty as Revenue
    ,a.order_type
    ,a.order_line_no
    ,a.from_loc_no
    ,a.loc_char
    ,a.vend_no
    ,a.vend_name
    ,a.vpo_no
    ,a.po_date_time
    ,a.license_type
    ,a.service_duration
    ,a.current_queue
    ,a.last_completed_queue
    ,a.date_timestamp
    ,a.entry_name
    ,a.multiterm_billing
from tempdb.rds_us17936_temp1 a
left join tempdb.rds_us17936_exp b on b.order_no=a.order_no and b.order_type=a.order_type and b.order_line_no=a.order_line_no
left join min_eta c on a.order_no = c.order_no and a.order_type = c.order_type and a.order_line_no = c.order_line_no
;

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select sales_terr
    ,to_acct_no as cust_no
    ,cust_name
    ,po_date
    ,ext_ref as CPO_no
    ,order_no
    ,order_type
    ,order_line_no
    ,sku_no
    ,mfg_partno
    ,short_desc
    ,ETA_date
    ,order_qty
    ,Revenue
    ,from_loc_no as loc_no
    ,loc_char as loc_name
    ,vend_no
    ,vend_name
    ,vpo_no as TDS_PO_no
    ,po_date_time as 'TDS PO Date'
    ,license_type as 'License Type'
    ,service_duration as 'Service Duration'
    ,current_queue as 'Current Queue'
    ,last_completed_queue as 'Last Completed Queue'
    ,date_timestamp as 'Date/Timestamp'
    ,entry_name as 'Order Creator'
    ,multiterm_billing as 'Multiterm Billing'
from tempdb.rds_us17936_temp2
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;

-- 2
drop table if exists tempdb.rds_us17936_order;
drop table if exists tempdb.rds_us17936_temp1;
drop table if exists tempdb.rds_us17936_exp;
drop table if exists tempdb.rds_us17936_temp2;
