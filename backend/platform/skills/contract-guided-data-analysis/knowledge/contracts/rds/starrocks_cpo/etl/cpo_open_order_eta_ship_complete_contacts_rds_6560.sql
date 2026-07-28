drop table if exists sku_list_ca6560;
create table sku_list_ca6560 as
select  sku_no,
		short_desc,
		part_no,
		mfg_partno,
		cast(vpl_code as varchar(60)) as vpl_code,
		vpl_desc,
		pm.vend_no,
		abc_code
  from ods_ca.ods_cis_corp_part_master_rt pm 
 inner join ods_ca.ods_cis_corp_dw_vend_pl_rt b 
    on pm.vpl_no = b.vpl_no
 where pm.vend_no = 50535
;
  
  
drop table if exists order_list_ca6560;
create table order_list_ca6560 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
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
select uuid_numeric() as id,
       a.entry_datetime,
       eta.min_eta as eta,
       a.order_no,
       a.order_type,
       ot.order_type_descr as order_type_descr,
       b.order_line_no,
       a.to_acct_no as cust_no,
       ch.cust_name as bill_to_name,
       case when a.invoice_date is not null then 'Invoiced'
                        when a.ship_date is not null then 'Shipped'
                        when a.qc_date is not null then 'QC Date'
                        when a.pick_date is not null then 'Picked'
                        when a.credit_rel_date is not null then 'Credit Released'
                        when a.sales_rel_date is not null then 'Sales Released'
                        when a.issue_date is not null then 'Queued'
                        when a.entry_datetime is not null then 'Created Date'
                    end as so_status,
       ifnull(op.profile_c, 'N') as ship_complete,
       a.int_ref_no as cpo_id,
       b.int_ref_line_no as cpo_line_seq,
           a.ext_ref,
           os.end_user_po as eu_po,
           c.vend_no,
           vm.vend_name as vend_name,
           ship_to_name,
           ship_to_addr,
           ship_to_city ,       
           ship_to_state,       
           ship_to_zip,
           order_qty,
           rec_qty,
       cpod.cpo_line_qty as po_qty,
       case when a.order_type = 1 and a.pick_date is null then 'Y' else 'N' end as on_hold,
           b.sku_no,
           short_desc,
           part_no,
           mfg_partno,
           vpl_code,
           vpl_desc,
           unit_cost,
           unit_price,
           from_loc_no,
           concat(l.loc_city , ', ' , l.loc_state) as loc_name,
      case when from_loc_no = 98 then 98
	        when (ship_to_zip like 'A%'
OR ship_to_zip like 'B%'
OR ship_to_zip like 'C%'
OR ship_to_zip like 'D%'
OR ship_to_zip like 'E%'
OR ship_to_zip like 'F%'
OR ship_to_zip like 'G%'
OR ship_to_zip like 'H%'
OR ship_to_zip like 'I%'
OR ship_to_zip like 'J%'
OR ship_to_zip like 'K%'
OR ship_to_zip like 'L%'
OR ship_to_zip like 'M%'
OR ship_to_zip like 'N%'
OR ship_to_zip like 'O%'
OR ship_to_zip like 'P%'
OR ship_to_zip like 'Q%'
OR ship_to_zip like 'R%') then 29

	        when (ship_to_zip like 'S%'
OR ship_to_zip like 'T%'
OR ship_to_zip like 'U%'
OR ship_to_zip like 'V%'
OR ship_to_zip like 'W%'
OR ship_to_zip like 'X%'
OR ship_to_zip like 'Y%'
OR ship_to_zip like 'Z%'
) then 81
	        end as preferred_whs_ship,
       case when from_loc_no = 98 then 'Drop Ship'
	        when (ship_to_zip like 'A%'
OR ship_to_zip like 'B%'
OR ship_to_zip like 'C%'
OR ship_to_zip like 'D%'
OR ship_to_zip like 'E%'
OR ship_to_zip like 'F%'
OR ship_to_zip like 'G%'
OR ship_to_zip like 'H%'
OR ship_to_zip like 'I%'
OR ship_to_zip like 'J%'
OR ship_to_zip like 'K%'
OR ship_to_zip like 'L%'
OR ship_to_zip like 'M%'
OR ship_to_zip like 'N%'
OR ship_to_zip like 'O%'
OR ship_to_zip like 'P%'
OR ship_to_zip like 'Q%'
OR ship_to_zip like 'R%') then 'Guelph,ON'
	        when (ship_to_zip like 'S%'
OR ship_to_zip like 'T%'
OR ship_to_zip like 'U%'
OR ship_to_zip like 'V%'
OR ship_to_zip like 'W%'
OR ship_to_zip like 'X%'
OR ship_to_zip like 'Y%'
OR ship_to_zip like 'Z%'
) then 'Richmond,BC' 
	        end as preferred_whs_ship_desc,
           abc_code,
       lbd.code_desc as abc_desc,
           a.sales_terr,
           d.division_desc as division,
		   ax.addr_no,
       -- custdes = convert(int,null),
       -- custdeshold = convert(int,null),
       -- date_alloc = convert(varchar(10),null),
       -- RIO_desc = convert(varchar(60),null),
       -- order_source = convert(varchar(30), null),
       null as sales_rep,
        null as manager
       
       -- request_delivery = convert(varchar(10),null)
  from ods_ca.ods_cis_corp_order_header_rt a
 inner join ods_ca.ods_cis_corp_order_detail_rt b
    on a.order_no = b.order_no 
   and a.order_type = b.order_type
 inner join sku_list_ca6560 c
    on b.sku_no = c.sku_no
left join ods_ca.ods_cis_corp_order_type_rt ot 
	on a.order_type = ot.order_type
left join min_eta eta
	on b.sku_no=eta.sku_no
	and a.order_no = eta.order_no
	and a.order_type = eta.order_type
	and b.order_line_no = eta.order_line_no
left join ods_ca.ods_cis_corp_customer_header_rt ch 
	on a.to_acct_no = ch.cust_no
left join ods_ca.ods_cis_corp_cpo_header_rt cpoh
	    on a.int_ref_no = cpoh.cpo_id
left join ods_ca.ods_cis_corp_cpo_detail_rt cpod
	    on a.int_ref_no = cpod.cpo_id
	   and b.int_ref_line_no = cpod.cpo_line_seq
left join ods_ca.ods_cis_corp_order_profile_rt op 
	   on a.order_type = op.order_type
	   and a.order_no = op.order_no
	   and op.profile_type = 'SHIP_CPLE'
left join ods_ca.ods_cis_corp_order_soldto_rt os 
	on a.order_type = os.order_type
	and a.order_no = os.order_no
left join ods_ca.ods_cis_corp_vend_master_rt vm 
	on c.vend_no = vm.vend_no
left join ods_ca.ods_cis_corp_list_box_detail_rt lbd 
	on c.abc_code = trim(lbd.code_value)
	and lbd.list_box_code = 'SABC'
left join ods_ca.ods_cis_corp_location_info_rt l 
	on a.from_loc_no = l.loc_no
left join ods_ca.ods_cis_corp_territory_rt t 
	on a.sales_terr = t.sales_terr
left join ods_ca.ods_cis_corp_territory_group_rt tg
	on t.group_id = tg.group_id
left join ods_ca.ods_cis_corp_cust_type_rt cty
	on tg.cust_type = cty.cust_type
left join ods_ca.ods_cis_corp_division_rt d
	on cty.division = d.division
left join ods_ca.ods_cis_corp_addr_xref_rt ax
		on a.to_acct_no =ax.xref_no
	   and ax.xref_seq = 1
	   and ax.xref_type = 'ADDR_CUST'
	   and ax.active = 'Y'  
 where a.delete_date is null
   and b.delete_date is null
   and a.ship_date is null
   and b.close_date is null
   and b.order_qty - ifnull(b.ship_qty,0) <> 0
   and a.order_type in (1,8)
   and a.sales_terr <> 6100
;
  
 update order_list_ca6560
	   set manager = ct.contact_name
	  from ods_ca.ods_cis_corp_contact_xref_rt cx
      inner join ods_ca.ods_cis_corp_contacts_rt ct
	 	where  order_list_ca6560.addr_no = cx.xref_no
	   and cx.contact_no = ct.contact_no
	   and cx.xref_type = 'CONT_ADDR'
	   and cx.active = 'Y'
	   and cx.delete_id is null
	   and ct.title = 'Sony Manager'
	;
	  
	update order_list_ca6560
	   set sales_rep = ct.contact_name
	 from ods_ca.ods_cis_corp_contact_xref_rt cx
      inner join ods_ca.ods_cis_corp_contacts_rt ct
	 	where  order_list_ca6560.addr_no = cx.xref_no
	   and cx.contact_no = ct.contact_no
	   and cx.xref_type = 'CONT_ADDR'
	   and cx.active = 'Y'
	   and cx.delete_id is null
	   and ct.title = 'Sony Rep'
   ;

	drop table if exists order_rio_ca6560;
	create table order_rio_ca6560 as  
	select a.sku_no,
	       c.rio_req_no,
	       c.to_order_no,
	       c.to_order_line_no,
	       c.to_order_qty,
	       b.ref_descr,
	       date_format( c.entry_datetime, '%m/%d/%Y') as entry_datetime
	  from order_list_ca6560 a
	  left join ods_ca.ods_cis_corp_rio_request_header_rt b
	    on a.sku_no = b.sku_no
	   and a.cust_no = b.cust_no
	  left join ods_ca.ods_cis_corp_rio_req_consumed_rt c
	    on b.rio_req_no = c.rio_req_no
	;
	  

	  
	
drop table if exists order_list1_ca6560;
create table order_list1_ca6560 as
select a.entry_datetime,
       a.eta,
       a.order_no,
       a.order_type,
       a.order_type_descr,
       a.order_line_no,
       a.cust_no,
       a.bill_to_name,
       a.so_status,
       a.ship_complete,
       a.cpo_id,
       a.cpo_line_seq,
       a.ext_ref,
       a.eu_po,
       a.vend_no,
       a.vend_name,
       a.ship_to_name,
       a.ship_to_addr,
       a.ship_to_city ,       
       a.ship_to_state,       
       a.ship_to_zip,
       a.order_qty,
       a.rec_qty,
       a.po_qty,
       a.on_hold,
       a.sku_no,
       a.short_desc,
       a.part_no,
       a.mfg_partno,
       a.vpl_code,
       a.vpl_desc,
       a.unit_cost,
       a.unit_price,
       a.from_loc_no,
       a.loc_name,
       a.preferred_whs_ship,
       a.preferred_whs_ship_desc,
       a.abc_code,
       a.abc_desc,
       a.sales_terr,
       a.division,
	   a.addr_no,
       b.rio_req_no as custdes,
       b.to_order_qty as custdeshold,
       b.entry_datetime as date_alloc,
       b.ref_descr as RIO_desc,
       frt.from_ref_type_desc as order_source,
       a.sales_rep,
       a.manager,
       cast(op.profile_d as varchar(10)) as request_delivery
  from order_list_ca6560 a   
  left join order_rio_ca6560 b 
	 on a.order_no = b.to_order_no
	and a.order_line_no = b.to_order_line_no
	and a.sku_no = b.sku_no
  left join ods_ca.ods_cis_corp_order_soldto_rt os 
	on a.order_no = os.order_no
   and a.order_type = os.order_type
  left join ods_ca.ods_cis_corp_from_ref_type_rt frt 
	on os.from_ref_type = frt.from_ref_type
  left join ods_ca.ods_cis_corp_order_profile_rt op
	on  a.order_type = op.order_type
	and a.order_no = op.order_no
	and op.order_line_no is null
	and op.profile_type = 'EXPDELSTAR'
	and op.profile_cat = 'SHIP'

;
	 
    
	drop table if exists exp_ca6560;
	create table exp_ca6560 as
	select  a.order_no,
			a.order_type,
			a.order_line_no,
			sum(ifnull(a.unit_exp,0)) as u_sum_expense                                                   
	from ods_ca.ods_cis_corp_history_exp_rt a
	inner join order_list1_ca6560 b                               
		on a.order_no=b.order_no                             
		and a.order_type=b.order_type                           
		and a.order_line_no=b.order_line_no                             
		and a.order_exp_type='DP'                               
		and a.delete_date is null                               
	group by a.order_no,a.order_type,a.order_line_no                                
	union                           
	select  a.order_no,
			a.order_type,
			a.order_line_no,
			sum(ifnull(a.unit_exp,0)) as u_sum_expense                                  
	from ods_ca.ods_cis_corp_order_exp_rt a
	inner join order_list1_ca6560 b                                 
		 on a.order_no=b.order_no                             
		and a.order_type=b.order_type                           
		and a.order_line_no=b.order_line_no                             
		and a.order_exp_type='DP'                               
		and a.delete_date is null                               
	group by a.order_no,a.order_type,a.order_line_no                                
	;



drop table if exists order_list2_ca6560;
create table order_list2_ca6560 as
select distinct a.entry_datetime,
       a.eta,
       a.order_no,
       a.order_type,
       a.order_type_descr,
       a.order_line_no,
       a.cust_no,
       a.bill_to_name,
       a.so_status,
       a.ship_complete,
       a.cpo_id,
       a.cpo_line_seq,
       a.ext_ref,
       a.eu_po,
       a.vend_no,
       a.vend_name,
       a.ship_to_name,
       a.ship_to_addr,
       a.ship_to_city ,       
       a.ship_to_state,       
       a.ship_to_zip,
       a.order_qty,
       a.rec_qty,
       a.po_qty,
       a.on_hold,
       a.sku_no,
       a.short_desc,
       a.part_no,
       a.mfg_partno,
       a.vpl_code,
       a.vpl_desc,
       a.unit_cost,
       a.unit_price,
       a.from_loc_no,
       a.loc_name,
       a.preferred_whs_ship,
       a.preferred_whs_ship_desc,
       a.abc_code,
       a.abc_desc,
       a.sales_terr,
       a.division,
	   a.addr_no,
       a.custdes,
       a.custdeshold,
       a.date_alloc,
       a.RIO_desc,
       a.order_source,
       a.sales_rep,
       a.manager,
       a.request_delivery,
	   b.u_sum_expense as u_sum_expense
  from order_list1_ca6560 a 
  left join exp_ca6560 b 
	 on a.order_no=b.order_no                             
	and a.order_type=b.order_type                           
	and a.order_line_no=b.order_line_no


;


    drop table if exists rds_tmp;
	create table rds_tmp as
	select date_format(current_date(),'%m/%d/%Y') as 'ImpDate',
	       date_format(entry_datetime,'%m/%d/%Y') as 'order Entry Date',
	       eta as 'Cust ETA Ship Date',
	       cust_no as 'Customer Number',
	       bill_to_name as 'Customer Name',
	       division as 'Sales Division',
	       division as 'Sales Team',
	       concat(cast(order_type as varchar(5)) , ' - ' , order_type_descr) as 'Order Type',
	       so_status as 'SO Status',
	       ship_complete as 'Ship Complete',
	       cpo_id as 'PO ID',
	       order_no as 'Sales order Number',
	       order_line_no as 'Sales order Line Number',
	       ext_ref as 'Customer PO',
	       eu_po as 'End User PO',
	       vend_no as 'primary Vendor #',
	       vend_name as 'primary Vendor Name',
	       vpl_code as 'VPC Code',
	       -- vpl_desc as 'Product Line Name',
	       sku_no as 'Item Number',
	       short_desc as 'Item Name',
	       mfg_partno as 'Vendor Part Number',
	       -- abc_code as 'Item Status Code',
	       abc_desc as 'Item Status Desc',
	       from_loc_no as 'Warehouse',
	       loc_name as 'Warehouse Name',
	       preferred_whs_ship as 'Preferred Warehouse',
	       preferred_whs_ship_desc as 'Preferred Warehouse Desc',
	       order_qty as 'Ordered Quantity',    
	       case when order_type = 8 then order_qty else 0 end as 'Order Backorder Qty',
	       case when order_type = 1 then order_qty else 0 end as 'Available Qty',
	       case when order_source = 'TD migrate order' then order_qty else po_qty end as 'Original Order Qty',
	       case when from_loc_no = 98 then order_qty else 0 end as 'Drop Ship Order Qty',
	       (unit_price+ ifnull(u_sum_expense,0)) as 'Unit Net Price',
	       order_qty * (unit_price+ ifnull(u_sum_expense,0)) as 'Extended Net Price',
	       on_hold as 'On Hold',
	       custdes as 'RIO#',
	       custdeshold as 'RIO Consumed Qty',
	       date_alloc as 'Date Allocated',
	       RIO_desc as 'RIO Description',
	       order_source as 'OrdSrc',                             
	       manager as Manager,
	       sales_rep as Rep,
	       ship_to_name as 'Ship To Name',
	       ship_to_addr as 'Ship To Addr Line 1',
	       ship_to_city as 'Ship To City',
	       ship_to_state as 'Ship To State',
	       ship_to_zip as 'Ship To Postal Code',
	       request_delivery as 'Req Del Date'
	  from order_list2_ca6560
	 where case when order_source = 'TD migrate order' then order_qty else po_qty end >= 50
	 order by order_no
	;

drop table if exists rds_tmp_body;
create table rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rds_tmp
;

drop table if exists sku_list_ca6560;
drop table if exists order_list_ca6560;
drop table if exists order_rio_ca6560;
drop table if exists order_list1_ca6560;
drop table if exists exp_ca6560;
drop table if exists order_list2_ca6560;