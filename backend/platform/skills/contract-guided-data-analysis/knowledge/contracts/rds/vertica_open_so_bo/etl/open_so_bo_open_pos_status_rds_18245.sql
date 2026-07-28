drop table if exists orders_us18245_table;
create LOCAL TEMPORARY TABLE orders_us18245_table ON COMMIT PRESERVE ROWS AS
select
	a.synnex_po_no as 'PO#',
	a.bill_to_cust_no,
	a.bill_to_cust_name,
	concat(concat(concat(concat(bill_to_cust_addr, ' '), bill_to_cust_city), bill_to_cust_state), bill_to_cust_zip) as bill_to_address,
	a.ship_to_name,
	concat(concat(concat(concat(a.ship_to_addr, ' '), a.ship_to_city), a.ship_to_state), a.ship_to_zip) as ship_to_address,
	mfg_partno as 'MFG Part#',
	a.part_desc as Description,
	a.cpo_no as 'Quote #',
	a.order_no,
	a.order_type,
	a.mso_no,
	a.ship_date,
	a.order_entry_datetime as 'Order submission Date',
	a.invoice_date as 'Order Completion Date',
	b.total_order as 'total value',
	case when b.delete_date is not null then 'Deleted'
                    when b.schedule_date is not null then 'Expired'
                    when b.invoice_date is not null then 'Invoiced'
                    when b.ship_date is not null then 'Shipped'
                    when b.qc_date is not null then 'QCDate'
                    when b.pick_date is not null then 'Picked'
                    when b.credit_rel_date is not null then 'CreditRel'
                    when b.sales_rel_date is not null then 'SalesRel'
                    when b.issue_date is not null then 'Queued'
                    else 'Open'
                 end as status
from dw_us.dwd_disty_common_pos_di a
left join dw_us.dwd_pub_common_history_header_extend b on a.order_no = b.order_no and a.order_type = b.order_type
where a.vend_no in (59566  )
and a.bill_to_cust_no= 622647
and a.date_flag  >= DATE_TRUNC('QUARTER',CURRENT_DATE() - 1)  -- QTD
and a.date_flag  < CURRENT_DATE()
and a.order_type not in (14,16,114)
;

insert into orders_us18245_table
select distinct
	a.synnex_po_no as 'PO#',
	a.cust_no,
	a.cust_name,
	concat(concat(concat(concat(bill_to_cust_addr, ' '), bill_to_cust_city), bill_to_cust_state), bill_to_cust_zip) as bill_to_address,
	a.ship_to_name,
	concat(concat(concat(concat(a.ship_to_addr, ' '), a.ship_to_city), a.ship_to_state), a.ship_to_zip) as ship_to_address,
	mfg_partno as 'MFG Part#',
	a.part_desc as Description,
	a.cpo_no as 'Quote #',
	a.order_no,
	a.order_type,
	a.mso_no,
	a.ship_date ,
	a.order_date as 'Order submission Date',
	null  as 'Order Completion Date',
    a.total_order as 'total value',
    case when b.delete_date is not null then 'Deleted'
                     when b.schedule_date is not null then 'Expired'
                     when b.invoice_date is not null then 'Invoiced'
                     when b.ship_date is not null then 'Shipped'
                     when b.qc_date is not null then 'QCDate'
                     when b.pick_date is not null then 'Picked'
                     when b.credit_rel_date is not null then 'CreditRel'
                     when b.sales_rel_date is not null then 'SalesRel'
                     when b.issue_date is not null then 'Queued'
                     else 'Open'
                  end as status
from dw_us.dwd_disty_sales_open_order_detail a
left join dw_us.dwd_pub_common_history_header_extend b on a.order_no = b.order_no and a.order_type = b.order_type
where a.vend_no = 59566
and a.cust_no= 622647
and a.order_date  >= DATE_TRUNC('QUARTER',CURRENT_DATE() - 1)  -- QTD
and a.order_date  < CURRENT_DATE()
and a.order_type not in (14,16,114)
;

drop table if exists rdsetl.rds_tmp ;
CREATE TABLE rdsetl.rds_tmp AS
select  * from  orders_us18245_table ;


create table rdsetl.rds_tmp_body as
select 'Standard' as body_type,
       count(*) as cnt
  from rdsetl.rds_tmp
;

drop table if exists orders_us18245_table;