
drop table if exists tempdb.rds_tmp_sheet_config;
create table tempdb.rds_tmp_sheet_config
(
sheet_index int not null,
sheet_name varchar(50) null,
title_active varchar(1) null,
date_pattern varchar(50) null
)
;

insert into tempdb.rds_tmp_sheet_config values(1,'open orders with ETA',null,null);
insert into tempdb.rds_tmp_sheet_config values(2,'Shipped current month',null,null);
insert into tempdb.rds_tmp_sheet_config values(3,'invoiced rolling 17 months',null,null);




drop table if exists tempdb.acct_6143;
create table tempdb.acct_6143 as
select a.cust_no as acct_no ,b.cust_type , c.cust_type_descr
from   ods_ca.ods_cis_corp_customer_header a
inner join ods_ca.ods_cis_corp_territory_rt  b on a.sales_terr =b.sales_terr
inner join ods_ca.ods_cis_corp_cust_type_rt  c on b.cust_type =c.cust_type
where a.cust_no in (1208695,1207991,1209317,1210017,1210172,1211745,1230183,1241238,1243713,1253947)
;



-- TAB 1
drop table if exists tempdb.rds_tmp1;
create table tempdb.rds_tmp1 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
with min_eta as
( select
		order_no,
		order_type,
		order_line_no,
		sku_no,
		date_format(min(eta),'%Y/%m/%d') as min_eta
   from dm_ca.dm_pur_unieta_boso_detail_rt eta
   group by order_no, order_type, order_line_no,sku_no
)
select uuid_numeric() as id
   , h.order_type
   , h.order_no
   , date_format( h.entry_datetime, '%m/%d/%Y') as entry_date
   , h.ext_ref as reseller_po
   , h.ship_to_name
   , h.sales_total
   , null as net_sales
   , p.vend_no
   , vm.vend_name as vend_name
   , d.order_line_no
   , p.sku_no
   , p.mfg_partno
   , d.order_qty
   , d.ship_qty
   , d.unit_price
   , null as unit_usum
   , eta.min_eta
from ods_ca.ods_cis_corp_order_header_rt h
inner join ods_ca.ods_cis_corp_order_detail_rt d
		on h.order_no = d.order_no
		and h.order_type = d.order_type
inner join ods_ca.ods_cis_corp_part_master_rt p
	on d.sku_no = p.sku_no
inner join tempdb.acct_6143 a
	on  h.to_acct_no = a.acct_no
left join min_eta eta
	on p.sku_no=eta.sku_no
	and h.order_no = eta.order_no
	and h.order_type = eta.order_type
	and d.order_line_no = eta.order_line_no
left join ods_ca.ods_cis_corp_vend_master_rt vm
	on p.vend_no = vm.vend_no
where h.order_type in ( 1,8)
and h.delete_date is null
and h.closed_date is null
and d.delete_date is null
and d.order_qty -ifnull(d.ship_qty,0) <>0
;



drop table if exists tempdb.rds_sum_expense_6143;
create table tempdb.rds_sum_expense_6143 as
select  a.order_type,
		a.order_no,
		a.order_line_no,
		sum(ifnull(b.unit_exp,0)) as unit_usum
from tempdb.rds_tmp1 a
inner join ods_ca.ods_cis_corp_order_exp_rt b
	 on a.order_type = b.order_type
	and a.order_no = b.order_no
	and a.order_line_no = b.order_line_no
	and b.order_exp_type = 'DP'
	and b.delete_date is null
group by a.order_type, a.order_no, a.order_line_no
;

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select
     h.order_type
   , h.order_no
   , h.entry_date
   , h.reseller_po
   , h.ship_to_name
   , h.sales_total
   , (ifnull(se.unit_usum,0) + h.unit_price)* h.order_qty as net_sales
   , h.vend_no
   , h.vend_name
   , h.order_line_no
   , h.sku_no
   , h.mfg_partno
   , h.order_qty
   , h.ship_qty
   , h.unit_price
   , ifnull(se.unit_usum,0) as unit_usum
   , h.min_eta as eta
from tempdb.rds_tmp1 h
left join tempdb.rds_sum_expense_6143 se
	on h.order_no = se.order_no
	and h.order_type = se.order_type
	and h.order_line_no = se.order_line_no

;



	-- TAB 2

	drop table if exists tempdb.rds_tmp_two;
	create table tempdb.rds_tmp_two as
	select
	     h.order_type
	   , h.order_no
	   , date_format(h.entry_datetime, '%m/%d/%Y') as entry_date
	   , h.ext_ref as reseller_po
	   , h.ship_to_name
	   , h.sales_total
	   -- , net_sales=convert(money,null)
	   , p.vend_no
	   -- , vend_name=convert(varchar(80),null)
	   , d.order_line_no
	   , p.sku_no
	   , p.mfg_partno
	   , d.order_qty
	   , d.ship_qty
	   , d.unit_price
	   -- , unit_usum=convert(money,null)
	   ,  date_format(h.ship_date,'%m/%d/%Y') as ship_date
	from ods_ca.ods_cis_corp_order_header_rt h
	inner join  ods_ca.ods_cis_corp_order_detail_rt d
		on h.order_no = d.order_no
	   and h.order_type = d.order_type
	inner join ods_ca.ods_cis_corp_part_master_rt p
		on d.sku_no = p.sku_no
	inner join tempdb.acct_6143 a
		on h.to_acct_no = a.acct_no
	where h.order_type = 1
	   and h.int_ref_type = 2
	   and h.from_loc_no = 98
	   and h.ship_date >= date_trunc('month',CURRENT_DATE())
	   and h.ship_date <  CURRENT_DATE()
	   and h.delete_date is null
	   and d.delete_date is null
	union
	select
	     h.order_type
	   , h.order_no
	   , date_format( h.entry_datetime, '%m/%d/%Y') as entry_date
	   , h.ext_ref as reseller_po
	   , h.ship_to_name
	   , h.sales_total
	   -- , net_sales=convert(money,null)
	   , p.vend_no
	   -- , vend_name=convert(varchar(80),null)
	   , d.order_line_no
	   , p.sku_no
	   , p.mfg_partno
	   , d.order_qty
	   , d.ship_qty
	   , d.unit_price
	   -- , unit_usum=convert(money,null)
	   , date_format(h.ship_date,'%m/%d/%Y') as ship_date
	from ods_ca.ods_cis_corp_order_header_rt h
	inner join  ods_ca.ods_cis_corp_order_detail_rt d
		on h.order_no = d.order_no
	   and h.order_type = d.order_type
	inner join  ods_ca.ods_cis_corp_part_master_rt p
		on d.sku_no = p.sku_no
	inner join  tempdb.acct_6143 a
		on h.to_acct_no = a.acct_no
	where  h.order_type = 1
	   and h.from_loc_no <> 98
	   and h.ship_date >= date_trunc('month',CURRENT_DATE())
       and h.ship_date < CURRENT_DATE()
	   and h.delete_date is null
	   and d.delete_date is null
	union
	select
	     h.order_type
	   , h.order_no
	   , date_format( h.entry_datetime, '%m/%d/%Y') as entry_date
	   , h.ext_ref as reseller_po
	   , h.ship_to_name
	   , h.sales_total
	  -- , net_sales=convert(money,null)
	   , p.vend_no
	   -- , vend_name=convert(varchar(80),null)
	   , d.order_line_no
	   , p.sku_no
	   , p.mfg_partno
	   , d.order_qty
	   , d.ship_qty
	   , d.unit_price
	   -- , unit_usum=convert(money,null)
	   , date_format(h.ship_date,'%m/%d/%Y') as ship_date
	from ods_ca.ods_cis_corp_history_header_rt h
	inner join ods_ca.ods_cis_corp_history_detail_rt d
		on h.order_no = d.order_no
	   and h.order_type = d.order_type
    inner join ods_ca.ods_cis_corp_part_master_rt p
		on d.sku_no = p.sku_no
	inner join tempdb.acct_6143 a
		on h.to_acct_no = a.acct_no
	where  h.order_type = 1
	   and h.int_ref_type = 2
	   and h.from_loc_no = 98
	   and h.ship_date >= date_trunc('month',CURRENT_DATE())
       and h.ship_date < CURRENT_DATE()
	   and h.delete_date is null
	   and d.delete_date is null
	union
	select
	     h.order_type
	   , h.order_no
	   , date_format(h.entry_datetime, '%m/%d/%Y') as entry_date
	   , h.ext_ref as reseller_po
	   , h.ship_to_name
	   , h.sales_total
	   -- , net_sales=convert(money,null)
	   , p.vend_no
	   -- , vend_name=convert(varchar(80),null)
	   , d.order_line_no
	   , p.sku_no
	   , p.mfg_partno
	   , d.order_qty
	   , d.ship_qty
	   , d.unit_price
	   -- , unit_usum=convert(money,null)
	   , date_format(h.ship_date,'%m/%d/%Y') as ship_date
	from ods_ca.ods_cis_corp_history_header_rt h
	inner join ods_ca.ods_cis_corp_history_detail_rt d
		on h.order_no = d.order_no
	   and h.order_type = d.order_type
	inner join ods_ca.ods_cis_corp_part_master_rt p
		on d.sku_no = p.sku_no
	inner join tempdb.acct_6143 a
		on h.to_acct_no = a.acct_no
	 where h.order_type = 1
	   and h.from_loc_no <> 98
	   and h.ship_date >= date_trunc('month',CURRENT_DATE())
       and h.ship_date < CURRENT_DATE()
	   and h.delete_date is null
	   and d.delete_date is null
	;



	drop table if exists tempdb.rds_sum_expense_6143;
	create table tempdb.rds_sum_expense_6143 as
	select a.order_type, a.order_no, a.order_line_no, sum(ifnull(b.unit_exp,0)) as unit_usum
	from tempdb.rds_tmp_two a
	inner join ods_ca.ods_cis_corp_history_exp_rt b
	where a.order_type = b.order_type
	  and a.order_no = b.order_no
	  and a.order_line_no = b.order_line_no
	  and b.order_exp_type = 'DP'
	  and b.delete_date is null
	group by a.order_type, a.order_no, a.order_line_no
	;


	drop table if exists tempdb.rds_tmp_2;
	create table tempdb.rds_tmp_2 as
	select
	     a.order_type
	   , a.order_no
	   , a.entry_date
	   , a.reseller_po
	   , a.ship_to_name
	   , a.sales_total
	   , (ifnull(b.unit_usum,0) + a.unit_price)*a.order_qty as net_sales
	   , a.vend_no
	   , vm.vend_name as vend_name
	   , a.order_line_no
	   , a.sku_no
	   , a.mfg_partno
	   , a.order_qty
	   , a.ship_qty
	   , a.unit_price
	   , ifnull(b.unit_usum,0) as unit_usum
	   ,a.ship_date
	from tempdb.rds_tmp_two a
	left join tempdb.rds_sum_expense_6143 b
		on a.order_no = b.order_no
		and a.order_type = b.order_type
		and a.order_line_no = b.order_line_no
	left join ods_ca.ods_cis_corp_vend_master_rt vm
		on a.vend_no = vm.vend_no
;



	-- TAB 3
      drop table if exists tempdb.rds_tmp_three;
	create table tempdb.rds_tmp_three    as
	select
	     h.order_type
	   , h.order_no
	   , d.order_line_no
	   , cast(h.invoice_date as date) as invoice_date
	   , d.ship_qty
	   , d.unit_price
	   , p.vend_no
	   , vm.vend_name
	   , a.cust_type
	   , a.cust_type_descr
	from ods_ca.ods_cis_corp_order_header_rt h
	inner join ods_ca.ods_cis_corp_order_detail_rt d
		on h.order_no = d.order_no
	   and h.order_type = d.order_type
	inner join ods_ca.ods_cis_corp_part_master_rt p
		on  d.sku_no = p.sku_no
	inner join ods_ca.ods_cis_corp_vend_master_rt vm on p.vend_no = vm.vend_no
	inner join tempdb.acct_6143 a
		on h.to_acct_no = a.acct_no
	 where h.order_type = 1
	   and h.delete_date  is null
       and h.invoice_date  >= date_add(current_date(), interval -17 month)
       and h.invoice_date < current_date()
	union
	select
	     h.order_type
	   , h.order_no
	   , d.order_line_no
	   , cast(h.invoice_date as date) as invoice_date
	   , d.ship_qty
	   , d.unit_price
	   , p.vend_no
	   , vm.vend_name
	   , a.cust_type
	   , a.cust_type_descr
	from ods_ca.ods_cis_corp_history_header_rt h
	inner join ods_ca.ods_cis_corp_history_detail_rt d
		on h.order_no = d.order_no
	   and h.order_type = d.order_type
	inner join ods_ca.ods_cis_corp_part_master_rt p
		on d.sku_no = p.sku_no
	inner join ods_ca.ods_cis_corp_vend_master_rt vm on p.vend_no = vm.vend_no
	inner join tempdb.acct_6143 a
		on h.to_acct_no = a.acct_no
	where  h.order_type = 1
	   and h.delete_date  is null
       and h.invoice_date  >= date_add(current_date(), interval -17 month)
       and h.invoice_date < current_date()
	;

	drop table if exists tempdb.rds_sum_expense_6143;
	create table tempdb.rds_sum_expense_6143 as
	select a.order_type, a.order_no, a.order_line_no, sum(ifnull(b.unit_exp,0)) as unit_usum
	from tempdb.rds_tmp_three a
	inner join ods_ca.ods_cis_corp_order_exp_rt b
	  on  a.order_type = b.order_type
	  and a.order_no = b.order_no
	  and a.order_line_no = b.order_line_no
	  and b.order_exp_type = 'DP'
	  -- and b.delete_date is null
	group by a.order_type, a.order_no, a.order_line_no
	union
	select a.order_type, a.order_no, a.order_line_no, sum(ifnull(b.unit_exp,0)) as unit_usum
	from tempdb.rds_tmp_three a
	inner join ods_ca.ods_cis_corp_history_exp_rt b
	   on a.order_type = b.order_type
	  and a.order_no = b.order_no
	  and a.order_line_no = b.order_line_no
	  and b.order_exp_type = 'DP'
	  -- and b.delete_date is null
	group by a.order_type, a.order_no, a.order_line_no
	;


	drop table if exists tempdb.rds_tmp_3;
	create table tempdb.rds_tmp_3 as
	select
	     a.cust_type
	   , a.cust_type_descr
	   , a.vend_no
	   , a.vend_name
	   , DATE_FORMAT(date_trunc('month',a.invoice_date),'%M %Y')  As  months
	   , (ifnull(b.unit_usum,0) + a.unit_price)*a.ship_qty as net_sales

	from tempdb.rds_tmp_three a
	left join tempdb.rds_sum_expense_6143 b
		on a.order_no = b.order_no
		and a.order_type = b.order_type
		and a.order_line_no = b.order_line_no
	group by   a.cust_type
	   , a.cust_type_descr
	   , a.vend_no
	   , a.vend_name
	   , DATE_FORMAT(date_trunc('month',a.invoice_date),'%M %Y')
	;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
union all
select 2 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp_2
union all
select 3 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp_3
;

