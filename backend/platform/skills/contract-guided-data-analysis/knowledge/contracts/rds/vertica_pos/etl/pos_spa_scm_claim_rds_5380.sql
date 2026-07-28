-- Typical POS example: SPA/SCM claim detail with ROW_NUMBER grain control.
-- Source: CA/run/rds_5380_rtv.sp

drop table if exists rds_5380_rtv;
create LOCAL TEMPORARY TABLE rds_5380_rtv ON COMMIT PRESERVE ROWS AS
select
a.order_no,
a.order_type,
a.order_line_no,
to_char(a.invoice_date,'mm-dd-yyyy') as invoice_date,
a.mfg_partno,
a.part_desc as short_desc,
a.bill_to_cust_name,
a.ship_to_name,
(a.unit_price + a.unit_sum_exp) * a.ship_qty as extend_net_price,
a.ship_qty,
a.unit_cost,
a.sku_no,
a.vend_no,
b.exp_code ,
b.claim_type,
b.scm_no,
b.unit_exp,
b.extended_exp,
b.spa_no,
nvl(b.spa_ref_no,d.spa_ref_no) as spa_ref_no,
b.approved_cost ,
b.rebate_amt,
c.order_expense_line_no,
row_number() over(partition by a.order_no,a.order_type,a.order_line_no order by b.scm_no) as rn
from dw_ca.dwd_disty_common_pos_di a
left join dw_ca.dwd_disty_scm_shipped_order_spa_di b
on a.order_type = b.order_type
and a.order_no = b.order_no
and a.order_line_no = b.order_line_no
left join ods_ca.ods_cis_corp_history_exp c
on a.order_no = c.order_no
and a.order_type = c.order_type
and a.order_line_no = c.order_line_no
and c.delete_date is null
left join ods_ca.ods_cis_corp_spa_header d
on b.scm_no=d.scm_no
where a.vend_no in (8707,19173)
and a.date_flag >= trunc(add_months(sysdate(), -1), 'month')
and a.date_flag < trunc(sysdate(), 'month')
and a.order_line_type != 'Comp'
order by a.date_flag
;

drop table if exists rds_5380_rtv_2;
create LOCAL TEMPORARY TABLE rds_5380_rtv_2 ON COMMIT PRESERVE ROWS AS
select
a.order_no,
a.order_type,
a.order_line_no,
a.order_expense_line_no,
a.invoice_date,
a.mfg_partno,
a.short_desc,
a.bill_to_cust_name,
a.ship_to_name,
a.extend_net_price,
a.ship_qty,
a.unit_cost as u_cost,
a.sku_no,
a.vend_no,
a.exp_code,
a.claim_type,
f.claim_no,
a.scm_no,
a.unit_exp,
a.extended_exp,
a.spa_no,
c.marketing_comment as internal_comment,
a.spa_ref_no,
a.approved_cost,
a.rebate_amt
from rds_5380_rtv a
left join ods_ca.ods_cis_corp_spa_detail c
on a.spa_no = c.spa_no
and a.sku_no = c.sku_no
left join ods_ca.ods_cis_corp_scm_auto_claim_log f
on a.order_no = f.order_no
and a.order_type = f.order_type
and a.order_line_no = f.order_line_no
and a.order_expense_line_no = f.order_expense_line_no
where rn=1
;

drop table if exists rds_5380_rtv_3;
create LOCAL TEMPORARY TABLE rds_5380_rtv_3 ON COMMIT PRESERVE ROWS AS
select
		'SYNNEX' as 'Distributor_Name',								
		a.order_no as 'Distributor Invoice #',								
		invoice_date as 'Invoice Date',								
		mfg_partno as 'Material',								
		short_desc as 'Material Description',								
		bill_to_cust_name as 'Reseller Name',								
		ship_to_name as 'Ship to Name',								
		internal_comment as 'Promo ID',								
		extend_net_price as 'Total Sales $',								
		ship_qty as 'Shipped QTY',								
		u_cost as 'unit cost',								
		unit_exp as 'Rebate',								
		extended_exp as 'Extended Rebate',								
		sku_no as 'SKU #',								
		to_char(scm_no) || '-' || nvl(to_char(claim_no),' ') as 'SCM # posted',								
		spa_ref_no as 'SPA ref #',								
		vend_no as 'Vendor #'
from 
rds_5380_rtv_2 a
where claim_no is not null;

drop table if exists rdsetl.rds_tmp; 
CREATE TABLE rdsetl.rds_tmp AS 
select * from rds_5380_rtv_3;
 
drop table if exists rdsetl.rds_tmp_body;
CREATE TABLE rdsetl.rds_tmp_body AS 
select 
		 1 as flag
		,'Standard' as body_type
		,count(*) as cnt
from rdsetl.rds_tmp
;
