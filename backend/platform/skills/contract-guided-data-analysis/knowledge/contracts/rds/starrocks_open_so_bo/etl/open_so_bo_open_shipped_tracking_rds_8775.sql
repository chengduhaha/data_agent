
drop table if exists tempdb.temp_ca_8775_open_boso;
create table tempdb.temp_ca_8775_open_boso as
with min_eta as
( select
		order_no,
		order_type,
		order_line_no,
		sku_no,
		date_format(min(eta),'%m/%d/%Y') as min_eta
   from dm_ca.dm_pur_unieta_boso_detail_rt eta
   group by order_no, order_type, order_line_no,sku_no
)
select
   oh.order_type,
   oh.order_no,
   od.order_line_no,
   oh.entry_datetime as order_date,
   od.sku_no,

   od.order_qty,
   od.order_qty - (case when od.ship_qty is null then 0 else od.ship_qty end) open_qty,
   od.unit_price,
   eta.min_eta as  expected_date ,
   null reserved_qty,
   case when oh.pick_date is null then 'OPENED' else 'RELEASED' end as order_status,
   oh.ext_ref as cpo,
   os.end_user_po as epo,
   case when od.order_type = 8 then order_qty else null end as bo_qty,
   ship_to_name,
   oc.comment as ship_to_contact,
   ship_to_addr,
   ship_to_city,
   ship_to_state,
   ship_to_zip,
   ship_to_po_box,
   short_desc,
   mfg_partno,
   ec.res_contact as res_contact
   from ods_ca.ods_cis_corp_order_header_rt oh
   inner join ods_ca.ods_cis_corp_order_detail_rt od
       on oh.order_no = od.order_no
	  and oh.order_type = od.order_type
   inner join ods_ca.ods_cis_corp_part_master_rt pm
      on od.sku_no = pm.sku_no
	left join ods_ca.ods_cis_corp_order_eu_common_rt ec
		on  oh.order_no = ec.order_no
		and oh.order_type = ec.order_type
		and ec.delete_date is null
        and lower(ec.res_contact) like '%desjardin%'
	left join ods_ca.ods_cis_corp_order_comments_rt oc
		on oh.order_no = oc.order_no
		and oh.order_type = oc.order_type
	    and oc.comment_type = 'SA'
		and oc.comment_loc = 'N'
	left join ods_ca.ods_cis_corp_order_soldto_rt os
	    on oh.order_no = os.order_no
		and oh.order_type = os.order_type
	left join min_eta eta
		on od.sku_no=eta.sku_no
		and oh.order_no = eta.order_no
		and oh.order_type = eta.order_type
		and od.order_line_no = eta.order_line_no
   where oh.order_type in (1,8)
   and oh.to_acct_no in (1208530, 1255400, 1255400)
   and od.order_qty - ifnull(od.ship_qty,0) <> 0
   and oh.delete_date is null
   and od.delete_date is null
   and od.close_date is null
   and ec.res_contact is not null
;

-- tab1

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
	Select
	   order_status as 'Status',
	   date_format(order_date,'%m/%d/%Y') as 'Order Date',
   	   date_format(order_date,'%h:%m:%s') as 'Order Time',
	   order_no as 'Order',
	   epo as 'End User PO#',
	   cpo as 'Customer PO',
	   order_line_no as 'Line Number',
	   mfg_partno as 'Manufacture #',
	   short_desc as 'Description',
	   sum(order_qty) as 'Order QTY',
	   case when order_type = 1 then sum(order_qty) else 0 end  as 'Reserved Qty',
	   sum(bo_qty) as 'BackOrder Qty',
	   case when order_type = 8 then expected_date else null end  as 'BackOrder ETA',
	   ship_to_name as 'Ship To Name',
	   ship_to_contact as 'Ship To Attention',
	   ship_to_addr as 'Ship To Address 1',
	   ship_to_po_box as 'Ship To Address 2',
	   ship_to_city as 'Ship To City',
	   ship_to_state as 'Ship To Province',
	   ship_to_zip as 'Ship To PostalCode'
	FROM tempdb.temp_ca_8775_open_boso
	group by
	   order_status, order_no, epo,cpo, order_line_no, mfg_partno, short_desc, order_type, expected_date,
	   ship_to_name, ship_to_contact, ship_to_addr, ship_to_city, ship_to_state, ship_to_zip, ship_to_po_box
	order by order_type, order_no, order_line_no
	;


-- tab2
drop table if exists sales_ca_8775;
create table sales_ca_8775 as
SELECT
    oh.order_type
   ,oh.order_no
   ,od.order_line_no
   ,oh.to_acct_no  as cust_no
   ,ch.cust_name
   ,od.sku_no
   ,oh.invoice_date
   ,oh.ship_method
   ,oh.ext_ref as reseller_po_no

   ,oh.ship_to_name
   ,oh.ship_to_addr
   ,oh.ship_to_city
   ,oh.ship_to_state
   ,oh.ship_to_zip
FROM ods_ca.ods_cis_corp_order_header_rt oh
inner join ods_ca.ods_cis_corp_order_detail_rt od
   on oh.order_no = od.order_no
  and oh.order_type = od.order_type
left join ods_ca.ods_cis_corp_customer_header_rt ch on  oh.to_acct_no =ch.cust_no
where oh.ship_date>= date_add(current_date() , interval -7 day)
and oh.ship_date <  current_date()
and oh.to_acct_no  in(1208530, 1255400, 1255400)
and oh.order_type=1
union
SELECT
    oh.order_type
   ,oh.order_no
   ,od.order_line_no
   ,oh.to_acct_no  as cust_no
   ,ch.cust_name
   ,od.sku_no
   ,oh.invoice_date
   ,oh.ship_method
   ,oh.ext_ref as reseller_po_no

   ,oh.ship_to_name
   ,oh.ship_to_addr
   ,oh.ship_to_city
   ,oh.ship_to_state
   ,oh.ship_to_zip
FROM ods_ca.ods_cis_corp_history_header_rt oh
inner join ods_ca.ods_cis_corp_history_detail_rt od
   on oh.order_no = od.order_no
  and oh.order_type = od.order_type
left join ods_ca.ods_cis_corp_customer_header_rt ch on  oh.to_acct_no =ch.cust_no
where oh.ship_date>= date_add(current_date() , interval -7 day)
and oh.ship_date <  current_date()
and oh.to_acct_no  in(1208530, 1255400, 1255400)
and oh.order_type=1
;
drop table if exists sales_ca_8775_track_no;
create table sales_ca_8775_track_no as
select a.order_no
    ,a.order_type
    ,b.track_no
from sales_ca_8775 a
inner join ods_ca.ods_cis_corp_carton_header_rt b
on a.order_no = b.order_no
and a.order_type = b.order_type
union
select a.order_no
    ,a.order_type
    ,b.track_no
from sales_ca_8775 a
inner join ods_ca.ods_cis_corp_history_carton_header b
on a.order_no = b.order_no
and a.order_type = b.order_type
;

drop table if exists sales_ca_8775_track_no_listagg;
create table sales_ca_8775_track_no_listagg as
select order_no
    ,order_type
    ,group_concat(track_no,'*') as track_no
from sales_ca_8775_track_no
group by order_no
    ,order_type
;

drop table if exists rds_tmp_2;
create table rds_tmp_2 as
select distinct
    a.cust_no as 'Customer Number'
   ,a.cust_name as 'Customer Name'
   ,a.invoice_date as 'Invoice Date'
   ,a.order_no as 'Sales Order Number'
   ,a.reseller_po_no as 'Customer Purchase Order Number'
   ,ifnull(c.end_user_po ,c2.end_user_po) as 'EndUser Purchase Order Number'
   ,b.track_no as 'Tracking Container Number'
   ,a.ship_method as 'Ship Via Code'
   ,a.ship_to_name as 'Ship To Name'
   ,a.ship_to_addr as 'Ship To Address'
   ,a.ship_to_city as 'Ship To City'
   ,a.ship_to_state as 'Ship To State'
   ,a.ship_to_zip as 'Ship To Postal Code'
from sales_ca_8775 a
left join sales_ca_8775_track_no_listagg b
on a.order_no = b.order_no
and a.order_type = b.order_type
left join ods_ca.ods_cis_corp_order_soldto_rt c
on a.order_no = c.order_no
and a.order_type = c.order_type
left join ods_ca.ods_cis_corp_history_soldto_rt c2
on a.order_no = c2.order_no
and a.order_type = c2.order_type

;
drop table if exists rds_tmp_sheet_config;
CREATE TABLE rds_tmp_sheet_config(
	sheet_index int null,
	sheet_name varchar(50) null,
	title_active varchar(1) null,
	date_pattern varchar(50) null
);

insert into rds_tmp_sheet_config values(1,'BO',null,null);
insert into rds_tmp_sheet_config values(2,'Invoiced',null,null);

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;
insert into tempdb.rds_tmp_body
select 2 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp_2
;

drop table if exists tempdb.temp_ca_8775_open_boso;
drop table if exists tempdb.sales_ca_8775;
drop table if exists tempdb.sales_ca_8775_track_no;
drop table if exists tempdb.sales_ca_8775_track_no_listagg;

