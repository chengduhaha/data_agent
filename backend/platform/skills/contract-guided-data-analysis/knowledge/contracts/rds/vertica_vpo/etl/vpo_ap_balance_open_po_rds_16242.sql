drop table if exists rds_us16242_ap;
create local temporary table rds_us16242_ap on commit preserve rows as 
select b.name as analyst_name
	,a.vend_no
	,a.vend_name
	,a.vend_type
	,a.discontinued 
	,ifnull(a.ap_hold_flag,'N') as ap_hold_flag
	,a.old_comp 
	,a.terms_desc
	,a.vend_currency 
	,a.pas_code 
	-- DM
	,a.a_is_dnd as DND
	,ifnull(a.total_doc_amt,0) as vouched_usd
	,cast(0 as decimal(20,8)) as unvouched_debit_usd
	,cast(0 as decimal(20,8)) as total_ap_usd
	,cast(0 as decimal(20,8)) as accruals_usd
	,ifnull(a.inv_cost,0) as inventory_usd
	,cast(0 as decimal(20,8)) as balance_usd
	,cast(0 as decimal(20,8)) as open_po
from dm_us.dm_ap_aging_header_df a
left join dim_us.dim_pub_manager b
on a.analyst_id = b.userid
where a.date_flag = current_date()-1
-- where a.date_flag = '2025-03-31'
and a.sum_level = 'V'
;

	-- ,CASE
		-- WHEN EXISTS (
				-- SELECT 1
				-- FROM CIS..ap_dnd_profile z
				-- WHERE a.vend_no = z.vend_no
					-- AND z.profile_type ='DM'
					-- AND z.status = 'A'
				-- )
			-- THEN 'Y'
		-- ELSE 'N'
		-- END
	-- ,CASE
		-- WHEN EXISTS (
				-- SELECT 1
				-- FROM CIS..ap_dnd_profile z
				-- WHERE a.vend_no = z.vend_no
					-- AND z.profile_type ='DND'
					-- AND z.status = 'A'
				-- )
			-- THEN 'Y'
		-- ELSE 'N'
		-- END

drop table if exists rds_us16242_debit;
create local temporary table rds_us16242_debit on commit preserve rows as 
select vend_no
	,sum(ifnull(unvouched_amt,0)) as unvouched_amt
from dm_us.dm_ap_aging_header_df
where date_flag = current_date()-1
-- where date_flag = '2025-03-31'
and sum_level = 'OT'
and terms_no in ('3','12','27')
group by vend_no
;

update rds_us16242_ap a
set unvouched_debit_usd = b.unvouched_amt
from rds_us16242_debit b
where a.vend_no=b.vend_no
;

update rds_us16242_ap
set total_ap_usd = vouched_usd + unvouched_debit_usd
;

drop table if exists rds_us16242_credit;
create local temporary table rds_us16242_credit on commit preserve rows as 
select vend_no
	,sum(ifnull(unvouched_amt,0)) as unvouched_amt
from dm_us.dm_ap_aging_header_df
where date_flag = current_date()-1
-- where date_flag = '2025-03-31'
and ((sum_level = 'VCD' and terms_no = 'CR')
	 or (sum_level = 'OT' and terms_no = '2'))
group by vend_no
;

update rds_us16242_ap a
set accruals_usd = b.unvouched_amt
from rds_us16242_credit b
where a.vend_no=b.vend_no
;

update rds_us16242_ap
set balance_usd = total_ap_usd + accruals_usd - inventory_usd
;

drop table if exists rds_us16242_open_po;
create local temporary table rds_us16242_open_po on commit preserve rows as 
select vend_no
	,sum(open_qty*ifnull(unit_cost,0)) as open_po
from dw_us.dwd_disty_common_po_basic
where delete_date is null
and line_delete_date is null
and closed_date is null
and open_qty <> 0
and ifnull(order_qty,0) <> ifnull(rec_qty,0)
and vend_no in (select vend_no from rds_us16242_ap)
group by vend_no
;

update rds_us16242_ap a
set open_po = b.open_po
from rds_us16242_open_po b
where a.vend_no=b.vend_no
;

-- remove some lines
delete from rds_us16242_ap
where total_ap_usd >= 0
;

delete from rds_us16242_ap
where vouched_usd=0
and unvouched_debit_usd=0
and total_ap_usd=0
and accruals_usd=0
and inventory_usd=0
and balance_usd=0
and open_po=0
;

drop table if exists rds_us16242_final;
create local temporary table rds_us16242_final on commit preserve rows as 
select analyst_name as Analyst
	,vend_no
	,vend_name
	,vend_type
	,discontinued as Disco
	,ap_hold_flag as Pmt_Hold
	,old_comp as Old_Comp
	,terms_desc as Pmt_Terms
	,vend_currency as Vend_Curr
	,pas_code as PAS
	,DND
	,vouched_usd as Vouched_USD
	,unvouched_debit_usd as Unvouched_Debit_USD
	,total_ap_usd as Debit_Balance_USD
	,accruals_usd as 'Unvouched Credit(accrual)'
	,inventory_usd as Inventory_USD
	,balance_usd as APP_USD
	,open_po as Open_PO
from rds_us16242_ap
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as 
select *
from rds_us16242_final
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
-- 3