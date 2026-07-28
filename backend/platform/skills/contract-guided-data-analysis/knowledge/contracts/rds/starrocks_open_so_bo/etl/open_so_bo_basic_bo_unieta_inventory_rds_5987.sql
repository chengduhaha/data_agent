
drop table if exists tempdb.t_backorder_5987;
create table tempdb.t_backorder_5987 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
select
uuid_numeric() as id,
a.order_no,
a.order_type,
b.order_line_no,
c.vend_no,
cast(null as varchar(1)) as ready_flag,
from_loc_no,
from_inv_type,
a.entry_datetime,
a.ext_ref cust_po,
a.ship_to_name,
c.part_no,
c.mfg_partno,
b.sku_no,
c.upc_code,
b.order_qty demand,
cast(null as int) as on_order_qty,
cast(null as varchar(20)) as eta_date,
a.to_acct_no,
cast(null as varchar(60)) as Reseller_Name
from ods_ca.ods_cis_corp_order_header_rt a
inner join ods_ca.ods_cis_corp_order_detail_rt b
        on a.order_no = b.order_no
        and a.order_type = b.order_type
inner join ods_ca.ods_cis_corp_part_master_rt c
        on b.sku_no = c.sku_no
where a.order_type = 8
and a.delete_date is null
and b.delete_date is null
and a.to_acct_no in ( 1212575,1214882,1039266)
and c.vend_no in (29357,40373)
;

update tempdb.t_backorder_5987
set Reseller_Name = b.cust_name
from ods_ca.ods_cis_corp_customer_header_rt b
where t_backorder_5987.to_acct_no = b.cust_no
;


update tempdb.t_backorder_5987
set on_order_qty = b.on_order_qty
from ods_ca.ods_cis_corp_inv_qty_rt b
where t_backorder_5987.sku_no = b.sku_no
and t_backorder_5987.from_loc_no = b.loc_no
and t_backorder_5987.from_inv_type = b.inv_type
;

	
  update tempdb.t_backorder_5987
  set eta_date = date_format(b.eta,'%m/%d/%y')
    --  on_order_qty = b.on_order_qty
  from dm_ca.dm_pur_unieta_boso_detail_rt b
  where t_backorder_5987.sku_no=b.sku_no
  and t_backorder_5987.order_no = b.order_no
  and t_backorder_5987.order_type = b.order_type
  and t_backorder_5987.sku_no=b.sku_no
  ;
	        
	
	drop table if exists tempdb.rds_tmp;
	create table tempdb.rds_tmp as
	select vend_no 'Vendor #',
	order_no 'Order#',
	ready_flag 'Ready Flag',
	date_format(entry_datetime,'%m/%d/%y') as 'Entry Date',
	cust_po 'Reseller PO#',
	ship_to_name 'Ship To',
	part_no 'Part#',
	mfg_partno 'MFG Part#',
	sku_no as 'SKU#',
	upc_code 'UPC',
	demand 'Demand',
	on_order_qty 'On Order',
	eta_date 'ETA Date',
	Reseller_Name
	from tempdb.t_backorder_5987
	order by date_format(entry_datetime,'%Y/%m/%d') desc
	;
	
	drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;
	
