set time zone to 'America/Los_Angeles';

DROP TABLE IF EXISTS t_report_16874;
create LOCAL TEMPORARY table t_report_16874 ON COMMIT PRESERVE ROWS AS  
select  
order_no,
order_type,
order_line_no, 
sku_no,
part_no,
mfg_partno, 
vpl_no,
vpl_code,
vpl_desc,
vend_no,
vend_name, 
universal_vend_no,
universal_vend_name,
order_qty,
rec_qty,
open_qty,
unit_cost,
unit_price, 
po_cost,
ave_cost,
total_cost,
entry_datetime,
issue_date,
credit_rel_date,
sales_rel_date,
expected_date,
receiving_date,
printed_date,
closed_date,
delete_date,
line_expected_date,
eta_code,
request_eta_date,
line_rec_date,
po_ship_date,
line_delete_date, 
ext_ref,
mso_no,
mso_line_no,
bo_no,
cust_no,
cust_name,
ship_method, 
internal_comments 
from dw_us.dwd_disty_common_po_basic  
where order_type =2  
and order_qty<>rec_qty 
and vend_no in (104257,
104258,
104259,
104260,
104261,
75877,
76042
) 
; 
DROP TABLE IF EXISTS t_final_16874;
create LOCAL TEMPORARY table t_final_16874 ON COMMIT PRESERVE ROWS AS  
select  DISTINCT a.cust_no
	,a.cust_name
	,b.ship_to_name
	,a.order_no
	,a.order_type
	,a.order_line_no
	,mfg_partno AS Manufacturer_Part_No
	,c.cust_part_no
	,a.sku_no
	,a.part_no
	,a.vpl_no
	,a.vpl_code
	,a.vpl_desc
	,a.vend_no
	,a.vend_name
	,a.order_qty
	,a.rec_qty
	,a.open_qty
	,(case when b.delete_date is not null then 'Cancelled'
                     when b.schedule_date is not null then 'Expired'
                     when b.invoice_date is not null then 'Invoiced'
                     when b.ship_date is not null then 'Shipped'
                     when b.qc_date is not null then 'QCDate'
                     when b.pick_date is not null then 'Picked'
                     when b.credit_rel_date is not null then 'CreditRel'
                     when b.sales_rel_date is not null then 'SalesRel'
                     when b.issue_date is not null then 'Queued'
                     else 'Open'
                     end) as status 
	,request_eta_date AS Scheduled_Ship_Date
	,b.ship_date AS Actual_Ship_Date
	,a.expected_date AS Scheduled_Arrival_Date
	,a.receiving_date AS Actual_Arrival_Date
	,line_expected_date
	,a.eta_code
	,line_rec_date
	,po_ship_date
	,a.ext_ref
	,d.track_no
	,a.internal_comments
	,b.ship_to_addr
	,a.unit_cost
	,a.total_cost
	,a.entry_datetime AS Entered_Date
	,a.ship_method
FROM t_report_16874 a
LEFT JOIN ods_us.ods_cis_corp_order_header b ON a.order_no = b.order_no
	AND a.order_type = b.order_type
LEFT JOIN ods_us.ods_cis_corp_cust_part_no c ON a.sku_no = c.synnex_sku_no
LEFT JOIN ods_us.ods_cis_corp_carton_header d ON a.order_no = d.order_no
	AND a.order_type = d.order_type
;
DROP TABLE IF EXISTS rdsetl.rds_tmp;
CREATE TABLE rdsetl.rds_tmp AS
select * from t_final_16874;


DROP TABLE IF EXISTS rdsetl.rds_tmp_body;
CREATE TABLE rdsetl.rds_tmp_body AS
select
		1 as flag
		,'Standard' as body_type
		,count(*) as cnt
from rdsetl.rds_tmp
;


DROP TABLE IF EXISTS t_report_16874;
DROP TABLE IF EXISTS t_final_16874;