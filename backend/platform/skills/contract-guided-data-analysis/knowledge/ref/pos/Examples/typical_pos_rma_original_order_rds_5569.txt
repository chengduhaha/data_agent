-- Typical POS example: RMA and original SO tracing by int_ref_type/int_ref_no.
-- Source: CA/run/rds_5569_rtv.sp

drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists rds_5569_info;
create LOCAL TEMPORARY TABLE rds_5569_info ON COMMIT PRESERVE ROWS AS
select 
b.order_no,
b.order_type,
b.order_line_no,
b.date_flag as ship_date,
b.ship_qty,
b.sku_no,
b.part_no,
b.ship_to_name,
b.ship_to_addr,
b.ship_to_city,
b.ship_to_state,
b.ship_to_zip,
b.cpo_no as cust_po,
min(case when a.rma_no is not null then a.so_no
     when b.int_ref_type = 1 then b.int_ref_no
	 else null
 end) original_so_no,
b.end_user_po,
case when b.int_ref_type = 9 then b.int_ref_no else null end as rma_no
from dw_ca.dwd_disty_common_pos_di b
left join ods_ca.ods_cis_corp_rma_details a
on case when b.int_ref_type = 9 then b.int_ref_no else null end = a.rma_no
and a.delete_date is null
where b.bill_to_cust_no = 1159669
and b.order_type in (14,16)
and b.order_entry_datetime >= trunc(sysdate()-1, 'month')
and b.order_entry_datetime< current_date()
group by b.order_no,
b.order_type,
b.order_line_no,
b.date_flag,
b.ship_qty,
b.sku_no,
b.part_no,
b.ship_to_name,
b.ship_to_addr,
b.ship_to_city,
b.ship_to_state,
b.ship_to_zip,
b.cpo_no,
b.end_user_po,
case when b.int_ref_type = 9 then b.int_ref_no else null end
;

drop table if exists rds_5569_final;
create LOCAL TEMPORARY TABLE rds_5569_final ON COMMIT PRESERVE ROWS AS
select 
		a.order_no,
		a.order_type,
		to_char(a.ship_date,'MM/DD/YYYY') AS ship_date,
		a.ship_qty,
		a.sku_no,
		a.part_no,
		a.ship_to_name,
		a.ship_to_addr,
		a.ship_to_city,
		a.ship_to_state,
		a.ship_to_zip,
		a.cust_po,
		a.original_so_no,
		b.ext_ref as original_cust_po,
		to_char(b.invoice_date,'MM/DD/YYYY')  as original_invoice_date,
		a.end_user_po,
		a.rma_no
from rds_5569_info a  
left join ods_ca.ods_cis_corp_history_header b
on
a.original_so_no = b.order_no and b.order_type = 1
;

CREATE TABLE rdsetl.rds_tmp AS 
select *
from rds_5569_final
;

CREATE TABLE rdsetl.rds_tmp_body AS 
select 'Standard' as body_type
	,0 as acct_no
	,count(*) as cnt
from rdsetl.rds_tmp
;
