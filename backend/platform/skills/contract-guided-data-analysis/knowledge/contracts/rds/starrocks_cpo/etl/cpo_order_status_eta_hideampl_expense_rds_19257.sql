drop table if exists tempdb.rds_tmp;
drop table if exists tempdb.rds_tmp_body;

drop table if exists tempdb.us_report_19257;
create table tempdb.us_report_19257
(   id bigint auto_increment,
    cpo_no varchar(50) null,
    end_user_po varchar(40) null,
    to_acct_no int null,
    cpo_id int null,
    vpo_no int null,
    mso_no int null,
    po_date varchar(10) null,
    po_total decimal(12,4) null,
    order_type int null,
    order_no int null,
    order_date varchar(10) null,
    total_order decimal(12,4) null,
    ship_date varchar(10) null,
    ship_method varchar(50) null,
    order_status varchar(50) null,
    order_type_desc varchar(50) null,
    order_line_no int null,
    sku_no int null,
    order_line_qty int null,
    order_line_price decimal(12,4) null,
    unit_usum decimal(12,4) null,
    net_sales decimal(12,4) null,
    mfg_partno varchar(80) null,
    part_descr varchar(200) null,
    eta varchar(20) null
)
primary key (id)
distributed by hash (id)
;

insert into tempdb.us_report_19257(
    cpo_no,
    end_user_po,
    to_acct_no,
    cpo_id,
    vpo_no,
    mso_no,
    po_date,
    po_total,
    order_type,
    order_no,
    order_date,
    total_order,
    ship_date,
    ship_method,
    order_status,
    order_type_desc,
    order_line_no,
    sku_no,
    order_line_qty,
    order_line_price,
    unit_usum,
    net_sales,
    mfg_partno,
    part_descr,
    eta)
with max_eta as
(select
     order_no,
     order_type,
     order_line_no,
     sku_no,
     date_format(max(eta),'%m/%d/%Y') as max_eta
 from dm_us.dm_pur_unieta_boso_detail_rt eta
 -- where order_no = 172910055
 group by order_no, order_type, order_line_no,sku_no
)
select
  a.ext_ref as cpo_no,
  cast(null as varchar(40)) end_user_po,
  a.to_acct_no,
  case when a.order_type = 8 then a.int_ref_no
       when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type != 2 then a.int_ref_no
  end as cpo_id,
  case when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type = 2 then a.int_ref_no
       else null
  end as vpo_no,
  cast(null as int) mso_no,
  cast(null as varchar(10)) po_date,
  cast(null as decimal(12,4)) po_total,
  a.order_type,
  a.order_no,
  date_format(a.entry_datetime, '%m/%d/%Y') as order_date,
  a.total_order,
  date_format(a.ship_date, '%m/%d/%Y') as ship_date,
  a.ship_method,
  case when a.delete_date is not null then 'Cancelled'
       when a.order_type = 8 then 'Back Order'
       when a.closed_date is not null then 'Closed'
       when a.schedule_date is not null then 'Expired'
       when a.invoice_date is not null then 'Invoiced'
       when a.ship_date is not null then 'Shipped'
       when a.qc_date is not null then 'QCDate'
       when a.pick_date is not null then 'Picked'
       when a.credit_rel_date is not null then 'Credit Released'
       when a.sales_rel_date is not null then 'Sales Released'
       when a.issue_date is not null then 'Queued'
       else 'Open Order'
  end as order_status,
  case when a.order_type = 8 then 'Back Order'
       when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type != 2 then 'Sales Order(Master)'
       when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type = 2 then 'Sales Order(Ship)'
       else c.order_type_descr
  end as order_type_desc,
  b.order_line_no,
  b.sku_no,
  b.order_qty as order_line_qty,
  b.unit_price as order_line_price,
  cast(null as decimal(12,4)) unit_usum,
  cast(null as decimal(12,4)) net_sales,
  cast(null as varchar(80)) mfg_partno,
  cast(null as varchar(200)) part_descr,
  eta.max_eta as eta_date
from ods_us.ods_cis_corp_history_header_rt a
inner join ods_us.ods_cis_corp_history_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type
inner join ods_us.ods_cis_corp_order_type_rt c on a.order_type = c.order_type
left join max_eta eta
    on b.sku_no=eta.sku_no
    and a.order_no = eta.order_no
    and a.order_type = eta.order_type
    and b.order_line_no = eta.order_line_no
where a.order_type in (1,8)
and a.to_acct_no = 686022
and a.entry_datetime >= '2025-01-01'
and a.entry_datetime < current_date()
-- and a.order_no = 172910055

union

select
  a.ext_ref as cpo_no,
  cast(null as varchar(40)) end_user_po,
  a.to_acct_no,
  case when a.order_type = 8 then a.int_ref_no
       when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type != 2 then a.int_ref_no
  end as cpo_id,
  case when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type = 2 then a.int_ref_no
       else null
  end as vpo_no,
  cast(null as int) mso_no,
  cast(null as varchar(10)) po_date,
  cast(null as decimal(12,4)) po_total,
  a.order_type,
  a.order_no,
  date_format(a.entry_datetime, '%m/%d/%Y') as order_date,
  a.total_order,
  date_format(a.ship_date, '%m/%d/%Y') as ship_date,
  a.ship_method,
  case when a.delete_date is not null then 'Cancelled'
       when a.order_type = 8 then 'Back Order'
       when a.closed_date is not null then 'Closed'
       when a.schedule_date is not null then 'Expired'
       when a.invoice_date is not null then 'Invoiced'
       when a.ship_date is not null then 'Shipped'
       when a.qc_date is not null then 'QCDate'
       when a.pick_date is not null then 'Picked'
       when a.credit_rel_date is not null then 'Credit Released'
       when a.sales_rel_date is not null then 'Sales Released'
       when a.issue_date is not null then 'Queued'
       else 'Open Order'
  end as order_status,
  case when a.order_type = 8 then 'Back Order'
       when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type != 2 then 'Sales Order(Master)'
       when a.order_type = 1 and a.from_loc_no = 98 and a.int_ref_type = 2 then 'Sales Order(Ship)'
       else c.order_type_descr
  end as order_type_desc,
  b.order_line_no,
  b.sku_no,
  b.order_qty as order_line_qty,
  b.unit_price as order_line_price,
  cast(null as decimal(12,4)) unit_usum,
  cast(null as decimal(12,4)) net_sales,
  cast(null as varchar(80)) mfg_partno,
  cast(null as varchar(200)) part_descr,
  eta.max_eta as eta_date
from ods_us.ods_cis_corp_order_header_rt a
inner join ods_us.ods_cis_corp_order_detail_rt b on a.order_no = b.order_no and a.order_type = b.order_type
inner join ods_us.ods_cis_corp_order_type_rt c on a.order_type = c.order_type
left join max_eta eta
    on b.sku_no=eta.sku_no
    and a.order_no = eta.order_no
    and a.order_type = eta.order_type
    and b.order_line_no = eta.order_line_no
where a.order_type in (1,8)
and a.to_acct_no = 686022
and a.entry_datetime >= '2025-01-01'
and a.entry_datetime < current_date()
-- and a.order_no = 172910055
;

-- select * from tempdb.us_report_19257 where order_type_desc = 'Back Order'
-- select * from tempdb.us_report_19257 a where a.order_no = 172557166
-- select * from ods_us.ods_cis_corp_history_header_rt a where a.order_no = 174335844
-- select * from ods_us.ods_cis_corp_history_detail_rt a where a.order_no = 174335844

drop table if exists us_exp_9185;
drop table if exists us_exp_temp_9185;

create table us_exp_temp_9185 as
select a.order_no
	,a.order_line_no
	,a.order_type
	,sum(ifnull(b.unit_exp,0)) as u_sum_expense
from tempdb.us_report_19257 a
inner join ods_us.ods_cis_corp_order_exp_rt b on a.order_no = b.order_no and a.order_type = b.order_type
	and a.order_line_no = b.order_line_no
	and b.order_exp_type = 'DP'
	and b.delete_id is null
group by a.order_no
	,a.order_line_no
	,a.order_type
union
select a.order_no
	,a.order_line_no
	,a.order_type
	,sum(ifnull(b.unit_exp,0)) as u_sum_expense
from tempdb.us_report_19257 a
inner join ods_us.ods_cis_corp_order_exp_rt b on a.order_no = b.order_no and a.order_type = b.order_type
	and a.order_line_no = b.order_line_no
	and b.exp_code = 'AMPL'
	and exists (select 1
	            from ods_us.ods_cis_corp_order_profile_rt op
                where op.order_type = b.order_type
                and op.order_no = b.order_no
                and op.profile_type = 'HIDEAMPL'
                and op.profile_cat  = 'AMPL'
                and op.profile_c = 'Y'
                )
	and b.delete_id is null
group by a.order_no
	,a.order_line_no
	,a.order_type
union
select a.order_no
	,a.order_line_no
	,a.order_type
	,sum(ifnull(b.unit_exp,0)) as u_sum_expense
from tempdb.us_report_19257 a
inner join ods_us.ods_cis_corp_history_exp_rt b on a.order_no = b.order_no and a.order_type = b.order_type
	and a.order_line_no = b.order_line_no
	and b.order_exp_type = 'DP'
	and b.delete_id is null
group by a.order_no
	,a.order_line_no
	,a.order_type
union
select a.order_no
	,a.order_line_no
	,a.order_type
	,sum(ifnull(b.unit_exp,0)) as u_sum_expense
from tempdb.us_report_19257 a
inner join ods_us.ods_cis_corp_history_exp_rt b on a.order_no = b.order_no and a.order_type = b.order_type
	and a.order_line_no = b.order_line_no
	and b.exp_code = 'AMPL'
	and exists (select 1
	            from ods_us.ods_cis_corp_history_profile_rt op
                where op.order_type = b.order_type
                and op.order_no = b.order_no
                and op.profile_type = 'HIDEAMPL'
                and op.profile_cat  = 'AMPL'
                and op.profile_c = 'Y'
                )
	and b.delete_id is null
group by a.order_no
	,a.order_line_no
	,a.order_type
;

create table us_exp_9185 as
select a.order_no
	,a.order_line_no
	,a.order_type
	,sum(ifnull(a.u_sum_expense,0)) as u_sum_expense
from us_exp_temp_9185 a
group by a.order_no
	,a.order_line_no
	,a.order_type
;

update tempdb.us_report_19257
set unit_usum = ifnull((
	select b.u_sum_expense
	from us_exp_9185 b
	where tempdb.us_report_19257.order_no = b.order_no
		and tempdb.us_report_19257.order_line_no = b.order_line_no
		and tempdb.us_report_19257.order_type = b.order_type
    ), 0)
;

update tempdb.us_report_19257
set net_sales = order_line_price + ifnull(unit_usum, 0)
;

-- select * from us_report_19257 where order_no = 174335844

update tempdb.us_report_19257
set end_user_po = b.end_user_po
from ods_us.ods_cis_corp_order_soldto_rt b
where tempdb.us_report_19257.order_type = b.order_type
and tempdb.us_report_19257.order_no = b.order_no
;

update tempdb.us_report_19257
set end_user_po = b.end_user_po
from ods_us.ods_cis_corp_history_soldto_rt b
where tempdb.us_report_19257.order_type = b.order_type
and tempdb.us_report_19257.order_no = b.order_no
and tempdb.us_report_19257.end_user_po is null
;

update tempdb.us_report_19257
set mso_no = b.int_ref_no
from ods_us.ods_cis_corp_order_header_rt b
where 2 = b.order_type
and tempdb.us_report_19257.vpo_no = b.order_no
;

update tempdb.us_report_19257
set mso_no = b.int_ref_no
from ods_us.ods_cis_corp_history_header_rt b
where 2 = b.order_type
and tempdb.us_report_19257.vpo_no = b.order_no
and tempdb.us_report_19257.mso_no is null
;

update tempdb.us_report_19257
set cpo_id = b.int_ref_no
from ods_us.ods_cis_corp_order_header_rt b
where 1 = b.order_type
and tempdb.us_report_19257.mso_no = b.order_no
;

update tempdb.us_report_19257
set cpo_id = b.int_ref_no
from ods_us.ods_cis_corp_history_header_rt b
where 1 = b.order_type
and tempdb.us_report_19257.mso_no = b.order_no
and tempdb.us_report_19257.cpo_id is null
;

update tempdb.us_report_19257
set po_date = date_format(b.cpo_date, '%m/%d/%Y'),
    po_total = b.po_total
from ods_us.ods_cis_corp_cpo_header_rt b
where tempdb.us_report_19257.cpo_id = b.cpo_id
and tempdb.us_report_19257.po_date is null
;

update tempdb.us_report_19257
set po_date = date_format(b.cpo_date, '%m/%d/%Y'),
    po_total = b.po_total
from ods_us.ods_cis_corp_history_cpo_header_rt b
where tempdb.us_report_19257.cpo_id = b.cpo_id
and tempdb.us_report_19257.po_date is null
;

update tempdb.us_report_19257
set mfg_partno = b.mfg_partno,
    part_descr = b.short_desc
from ods_us.ods_cis_corp_part_master_rt b
where tempdb.us_report_19257.sku_no = b.sku_no
;


drop table if exists rds_tmp;
create table rds_tmp as
select
  cpo_no as 'PO#',
  end_user_po as 'End_Customer_PO#',
  -- to_acct_no as 'Bill_To',
  po_date as 'PO_Date',
  po_total as 'PO_Total',
  -- order_type as 'Order_Type',
  order_no as 'Order#',
  order_date as 'Order_Date',
  total_order as 'Total_Order',
  ship_date as 'Ship_Date',
  -- ship_method as 'Ship_Method',
  order_status as 'Order_Status',
  order_type_desc as 'Order_Type_Desc',
  order_line_no as 'Order LN#',
  sku_no as 'SKU#',
  order_line_qty as 'Line_QTY',
  net_sales as 'Unit_Price',
  (net_sales * order_line_qty) as 'EXT_Net_Price',
  mfg_partno as 'Mft_P/N',
  part_descr as 'Mft_P/N_Desc',
  eta as 'ETA'
from tempdb.us_report_19257
order by order_type, order_no, order_line_no
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from tempdb.rds_tmp
;

drop table if exists tempdb.us_report_19257;
