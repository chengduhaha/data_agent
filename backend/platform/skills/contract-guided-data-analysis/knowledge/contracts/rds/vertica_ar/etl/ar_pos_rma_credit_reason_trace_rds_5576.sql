
drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists rds_5576_rtv;
create LOCAL TEMPORARY TABLE rds_5576_rtv ON COMMIT PRESERVE ROWS AS 
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
	 else null end) original_so_no,					
b.end_user_po,					
case when b.int_ref_type = 9 then b.int_ref_no else null end as rma_no				
from dw_ca.dwd_disty_common_pos_di b
left join ods_ca.ods_cis_corp_rma_details a
on case when b.int_ref_type = 9 then b.int_ref_no else null end = a.rma_no
and a.delete_date is null			
where 
b.bill_to_cust_no in (1200548)   					
and b.order_type in (14,16)										
and b.order_entry_datetime >= trunc(current_date()-1, 'month')
and b.order_entry_datetime< current_date()-1
group BY 
b.order_no,					
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



drop table if exists rds_5576_rtv_2;
create LOCAL TEMPORARY TABLE rds_5576_rtv_2 ON COMMIT PRESERVE ROWS AS 
SELECT 
a.order_type,
a.order_no,										
to_char(a.ship_date,'MM/DD/YYYY') AS ship_date,					
a.ship_qty,
a.part_no,
a.sku_no,							
a.ship_to_name,					
a.ship_to_addr,					
a.ship_to_city,					
a.ship_to_state,					
a.ship_to_zip,					
a.cust_po,					
a.original_so_no,
b.ext_ref as original_cust_po,					
to_char(b.invoice_date,'MM/DD/YYYY')  as original_invoice_date,										
a.end_user_po
from rds_5576_rtv a  
left join ods_ca.ods_cis_corp_history_header b
on
a.original_so_no = b.order_no and b.order_type = 1
;


drop table if exists rds_5576_rtv_3;
create LOCAL TEMPORARY TABLE rds_5576_rtv_3 ON COMMIT PRESERVE ROWS AS 
SELECT 
a.order_type,
a.order_no,										
a.ship_date,					
a.ship_qty,
a.part_no,
a.sku_no,							
a.ship_to_name,					
a.ship_to_addr,					
a.ship_to_city,					
a.ship_to_state,					
a.ship_to_zip,					
a.cust_po,					
a.original_so_no,
a.original_cust_po,					
a.original_invoice_date,	
b.reference as credit_reason,
a.end_user_po
from rds_5576_rtv_2 a  
left join dw_ca.dwd_disty_ar_cust_doc_df b
on
 a.order_no = b.order_no 					
and  a.order_type = b.order_type
and b.date_flag  = current_date()-1
;



CREATE TABLE rdsetl.rds_tmp AS 
select *
from rds_5576_rtv_3
;


CREATE TABLE rdsetl.rds_tmp_body AS 
select 'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
