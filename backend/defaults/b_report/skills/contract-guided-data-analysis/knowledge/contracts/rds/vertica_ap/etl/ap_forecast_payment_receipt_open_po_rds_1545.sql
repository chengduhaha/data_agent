drop table if exists temp_rds_sales_qtr_ca1545;
create local temporary table temp_rds_sales_qtr_ca1545 on commit preserve rows as 
select vend_no,
       sum(m_sales) as mtd_sales, 
	   sum(m_cost) mtd_cost,			
       sum(m_sales+pm_sales+ppm_sales) as qtd_sales,		
	   sum(m_cost+pm_cost+ppm_cost) as qtd_cost			
from dw_ca.dws_disty_brpt_vend_comb_mtd		
where date_flag = current_date()-1
group by vend_no
;		



drop table if exists rds_sales_qtr_ca1545;
create local temporary table rds_sales_qtr_ca1545 on commit preserve rows as 
select vend_no,
       mtd_sales, 
	   mtd_cost,			
       qtd_sales,		
	   qtd_cost			
from temp_rds_sales_qtr_ca1545		
where (mtd_sales!=0 and mtd_cost!=0 and qtd_sales!=0 and qtd_cost!=0)
;

drop table if exists rds_vend_ca1545;
create local temporary table rds_vend_ca1545 on commit preserve rows as 
select  a.vend_no,
		a.vend_name,		
		b.terms,		
		c.disc_days, 
		c.disc_percent,		
		c.terms_days				
from dim_ca.dim_pub_vendor_info a,
	 dim_ca.dim_pub_vend_location_view b,
	 dim_ca.dim_pub_terms_file_view c		
where a.vend_no=b.vend_no		
and b.loc_no=1		
and b.terms=c.doc_terms		
and a.discontinued='N'		
union
select  a.vend_no,
        a.vend_name,		
		b.terms,		
		c.disc_days, 
		c.disc_percent,		
		c.terms_days		
from dim_ca.dim_pub_vendor_info a,
     dim_ca.dim_pub_vend_location_view b,
	 dim_ca.dim_pub_terms_file_view c 
where a.vend_no=b.vend_no		
and b.loc_no=1		
and b.terms=c.doc_terms		
and exists (select 1 from rds_sales_qtr_ca1545 d where a.vend_no=d.vend_no)
;		
		


--actual payment
drop table if exists rds_actual_pay_ca1545;
create local temporary table rds_actual_pay_ca1545 on commit preserve rows as 		
select vend_no,
       sum(pay_amt) as pay_amt				
from ods_ca.ods_cis_corp_vend_payments  		
where TO_CHAR(pay_date,'yyyymmdd') >= CASE WHEN DATE_PART('day', current_date()) = 1 THEN 
						  TO_CHAR(ADD_MONTHS(current_date(), -1), 'yyyymmdd')
					 ELSE
                          TO_CHAR(DATE_TRUNC('month', current_date()), 'yyyymmdd')
                  END	
and TO_CHAR(pay_date,'yyyymmdd') < CASE WHEN DATE_PART('day', current_date()) = 1 THEN 
				   TO_CHAR(current_date(), 'yyyymmdd')
                   ELSE
                   TO_CHAR(current_date(), 'yyyymmdd')
                END		
group by vend_no		
;
--AP Total		
       	

drop table if exists rds_ap_total_ca1545;
create local temporary table rds_ap_total_ca1545 on commit preserve rows as 
select vend_no,
       sum(total) total				
from dw_ca.dws_disty_ap_vend_aging_df		
where date_flag = current_date()-1
and sum_level='V'		
group by vend_no		
;		



--sales goal		
drop table if exists rds_goal_ca1545;
create local temporary table rds_goal_ca1545 on commit preserve rows as 
select  vend_no		
	   ,sum(net_sales_local_currency) as sls_goal
	   ,cast(0 as float) as cogs_goal	
from dw_ca.dwd_disty_pm_report_goal	
where period = (DATEDIFF('month', DATE '1993-01-01', current_date()) + 1) 	
and vpl_no = 0	
and vend_no != 0 	
group by vend_no		
having sum(net_sales_local_currency) !=0	
;

-- MTD sales & MTD cogs		

drop table if exists rds_sales_ca1545;
create local temporary table rds_sales_ca1545 on commit preserve rows as 
select vend_no,
       sum(m_sales) as mtd_sales, sum(m_cost) mtd_cost				
from dw_ca.dws_disty_brpt_vend_comb_mtd		
where date_flag = current_date()-1
group by vend_no		
;		



update rds_goal_ca1545	a	
set cogs_goal=a.sls_goal- (a.sls_goal*(b.mtd_sales - b.mtd_cost )/b.mtd_sales )		
from rds_sales_ca1545 b		
where a.vend_no=b.vend_no		
and ifnull(b.mtd_sales,0)<>0		
;		



--MTD receipt		


drop table if exists TEMP_DATE;
create local temporary table TEMP_DATE on commit preserve rows as
SELECT CASE WHEN DATE_PART('day', current_date()) = 1 THEN current_date() ELSE DATE_TRUNC('month', current_date()) END AS st_date,
    current_date() AS en_date
;



drop table if exists TEMP_QTR_DATE;
create local temporary table TEMP_QTR_DATE on commit preserve rows as
SELECT ADD_MONTHS(st_date, -2) AS qtr_st_date
FROM TEMP_DATE
;


-- Insert data into rds_rec_pool_1545
drop table if exists rds_rec_pool_ca1545;
create local temporary table rds_rec_pool_ca1545 on commit preserve rows as
SELECT vend_no, SUM(ext_cost) AS ext_cost
FROM (
    SELECT vend_no, ext_cost, rec_datetime
    FROM dw_ca.dwd_disty_ap_ap_hold 
    WHERE rec_datetime >= (SELECT st_date FROM TEMP_DATE)
      AND rec_datetime < (SELECT en_date FROM TEMP_DATE)
) AS subquery
GROUP BY vend_no
;



-- Insert data into rds_qtd_pool_1545
drop table if exists rds_qtd_pool_ca1545;
create local temporary table rds_qtd_pool_ca1545 on commit preserve rows as
SELECT vend_no, SUM(ext_cost) AS ext_cost
FROM (
    SELECT vend_no, ext_cost, rec_datetime
    FROM dw_ca.dwd_disty_ap_ap_hold 
    WHERE rec_datetime >= (SELECT qtr_st_date FROM TEMP_QTR_DATE)
      AND rec_datetime < (SELECT en_date FROM TEMP_DATE)
) AS subquery
GROUP BY vend_no
;


drop table if exists rds_rec_ca1545;
create local temporary table rds_rec_ca1545 on commit preserve rows as
select vend_no,
       sum(ext_cost) as ext_cost
from rds_rec_pool_ca1545
group by vend_no
;


drop table if exists rds_rec_qtd_ca1545;
create local temporary table rds_rec_qtd_ca1545 on commit preserve rows as
select vend_no,
       sum(ext_cost) as ext_cost
from rds_qtd_pool_ca1545
group by vend_no
;




---Forecast payment		

--Open payment		
drop table if exists rds_open_pay_ca1545;
create local temporary table rds_open_pay_ca1545 on commit preserve rows as    	
select 	vend_no,
        sum(ifnull(doc_amt,0) - ifnull( inv_disc_amt,0) - ifnull(doc_applied,0) - ifnull(disc_taken,0)) doc_amt 
from dw_ca.dwd_disty_ap_vend_doc_df
where date_flag = current_date()-1
and TO_CHAR(doc_pay_date,'yyyymmdd' ) < TO_CHAR(current_date(), 'yyyymmdd')
and doc_close_date is null	
group by vend_no	
;


drop table if exists rds_open_spay_ca1545;
create local temporary table rds_open_spay_ca1545 on commit preserve rows as        		
select  vend_no,
        sum(doc_amt) doc_amt			
from rds_open_pay_ca1545		
group by vend_no		
;
	

---Open PO		
drop table if exists rds_open_po1_ca1545;
create local temporary table rds_open_po1_ca1545 on commit preserve rows as
select a.vend_no		
	  ,sum(ifnull(a.ext_cost,0)) as open_amt
	  ,date(a.entry_datetime) as tol_date		
from dw_ca.dwd_disty_ap_ap_hold  a,
     rds_vend_ca1545 b		
 where order_type=2		
 and rec_close_date is null		
 and doc_no is null		
 and a.vend_no=b.vend_no		
group by a.vend_no,date(a.entry_datetime)		
;

 		
DROP TABLE IF EXISTS rds_open_po1_ca1545_filtered;
CREATE LOCAL TEMPORARY TABLE rds_open_po1_ca1545_filtered ON COMMIT PRESERVE ROWS AS
SELECT b.*
FROM rds_open_po1_ca1545 b
LEFT JOIN rds_vend_ca1545 a ON a.vend_no = b.vend_no
WHERE b.tol_date + ifnull(a.disc_days, 0) < current_date()
;	


drop table if exists rds_open_po_ca1545;
create local temporary table rds_open_po_ca1545 on commit preserve rows as
select vend_no,
       sum(open_amt) open_amt
from rds_open_po1_ca1545_filtered
group by vend_no
     ;
  		
  		
DROP TABLE IF EXISTS rds_day_ca1545;
CREATE LOCAL TEMPORARY TABLE rds_day_ca1545 ON COMMIT PRESERVE ROWS AS
SELECT 
    COUNT(*) AS days,
    SUM(CASE WHEN date_flag < current_date() THEN 1 ELSE 0 END) AS day
FROM dim_ca.dim_pub_date
WHERE date_flag >= DATE_TRUNC('MONTH',current_date()-1)
AND date_flag < ADD_MONTHS(DATE_TRUNC('MONTH',current_date()-1),1)
;




drop table if exists rds_cogs_left_ca1545;
create local temporary table rds_cogs_left_ca1545 on commit preserve rows as
select a.vend_no,
      (case when days-day >= disc_days then disc_days* cogs_goal/nullif(days,0) else 0 end) as cogs_left			
from rds_vend_ca1545 a,
     rds_goal_ca1545 b,
	 rds_day_ca1545 c		
where a.vend_no=b.vend_no		
;		


drop table if exists rds_forecast_pay_ca1545;
create local temporary table rds_forecast_pay_ca1545 on commit preserve rows as
select a.vend_no,
      (case when ifnull(b.pay_amt,0)+ifnull(c.doc_amt,0)+ ifnull(d.open_amt,0) + ifnull(e.cogs_left,0)<0 then 0 else 		
       ifnull(b.pay_amt,0)+ifnull(c.doc_amt,0)+ ifnull(d.open_amt,0) + ifnull(e.cogs_left,0) end)		
       as forecast_payment			
from rds_vend_ca1545 a
left join rds_actual_pay_ca1545 b
	on a.vend_no=b.vend_no
left join rds_open_spay_ca1545 c
	on a.vend_no=c.vend_no
left join rds_open_po_ca1545 d
	on a.vend_no=d.vend_no
left join rds_cogs_left_ca1545 e		
	on a.vend_no=e.vend_no		
;		
	 	

drop table if exists rds_merge_ca1545;
create local temporary table rds_merge_ca1545 on commit preserve rows as
select 
vend_no,
cast(null as varchar(100)) as vend_name,		
disc_percent,
disc_days,		
terms_days as net_days,		
cast(null as float) as forecast_payment,		
cast(null as float) as actual_payment,		
cast(null as float) as payment_due,		
cast(null as int) as Day,		
cast(null as int) as Days,		
cast(null as varchar(100)) as vend_type,		
cast(null as float) as AP_Total,		
cast(null as float) as Forecast_AP_Total,		
cast(null as float) as sales_goal,		
cast(null as float) as MTD_sales,		
cast(null as float) as QTD_sales,		
cast(null as float) as COGS_goal,		
cast(null as float) as Daily_COGS_goal,		
cast(null as float) as MTD_COGS,		
cast(null as float) as QTD_COGS,		
cast(null as float) as MTD_receipts,		
cast(null as float) as QTD_receipts			
from rds_vend_ca1545		
   ;		


update rds_merge_ca1545		
set Day=b.day,Days=b.days		
from rds_day_ca1545 b		
   ;		



update rds_merge_ca1545	a	
set actual_payment= b.pay_amt 	
from rds_actual_pay_ca1545 b		
where a.vend_no=b.vend_no		
  ;		



update rds_merge_ca1545	a	
set forecast_payment=b.forecast_payment, 
    payment_due=case when ifnull(b.forecast_payment,0)-ifnull(actual_payment,0)<0 then 0 
	            else ifnull(b.forecast_payment,0)-ifnull(actual_payment,0) end		
from rds_forecast_pay_ca1545 b		
where a.vend_no=b.vend_no		
;		


update rds_merge_ca1545	a	
set AP_Total=b.total		
from rds_ap_total_ca1545 b		
where a.vend_no=b.vend_no		
;		


update rds_merge_ca1545	a	
set  sales_goal=b.sls_goal, 
     COGS_goal=b.cogs_goal		
from rds_goal_ca1545 b		
where a.vend_no=b.vend_no		
;		


update rds_merge_ca1545	a	
set QTD_sales=b.qtd_sales,		
MTD_sales=b.mtd_sales,		
MTD_COGS=b.mtd_cost,		
QTD_COGS=b.qtd_cost		
from rds_sales_qtr_ca1545 b		
where a.vend_no=b.vend_no		
;		


update rds_merge_ca1545		
set Daily_COGS_goal=COGS_goal/Days			
;		

update rds_merge_ca1545		
set  Forecast_AP_Total=ifnull(AP_Total,0) - ifnull(payment_due,0) + ifnull(Daily_COGS_goal,0)*ifnull(Days-Day,0)				
;		



update rds_merge_ca1545	a	
set QTD_receipts=b.ext_cost		
from rds_rec_qtd_ca1545 b		
where a.vend_no=b.vend_no 		
;

	

update rds_merge_ca1545	a	
set MTD_receipts=b.ext_cost		
from rds_rec_ca1545 b		
where a.vend_no=b.vend_no 		
 ;		



update rds_merge_ca1545	a	
set vend_name=b.vend_name,
    vend_type=b.vend_type		
from dim_ca.dim_pub_vendor_info b		
where a.vend_no=b.vend_no		
;		


-- select * from rds_merge_ca1545;


drop table if exists rds_ca1545_final;
create local temporary table rds_ca1545_final (
  s1  VARCHAR(100),
  s2  VARCHAR(100),
  s3  VARCHAR(100),
  s4  VARCHAR(100),
  s5  VARCHAR(100),
  s6  VARCHAR(100),
  s7  VARCHAR(100),
  s8  VARCHAR(100),
  s9  VARCHAR(100),
  s10 VARCHAR(100),
  s11 VARCHAR(100),
  s12 VARCHAR(100),
  s13 VARCHAR(100),
  s14 VARCHAR(100),
  s15 VARCHAR(100),
  s16 VARCHAR(100),
  s17 VARCHAR(100),
  s18 VARCHAR(100),
  s19 VARCHAR(100),
  s20 VARCHAR(100),
  s21 VARCHAR(100),
  s22 VARCHAR(100),
  id int
)on commit preserve rows;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
select 'DPO REPORT'
	,TO_CHAR(current_date(), 'yyyymmdd')	
	,'DPO(monthly):'
	,SPLIT_PART(
        TO_CHAR(SUM(AP_Total) / (nullif(SUM(MTD_COGS),0) * 12) * 365, '999999999999.99'),
        '.',
        1)
	,1
from rds_merge_ca1545		
 ;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
select null
	,null
	,'DPO(quarterly):'
	,SPLIT_PART(
        TO_CHAR(SUM(AP_Total) / (nullif(SUM(QTD_COGS),0) * 4) * 365, '999999999999.99'),
        '.',
        1)
	,2
from rds_merge_ca1545		
;		


insert into rds_ca1545_final		
(s1,id)		
values('',3)		
;		

insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
values		
(
'MTD Sales',		
'MTD COGS',		
'Forecast COGS',		
'AP Total',
4
)		
;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
select		
TO_CHAR(SUM(MTD_sales), '999,999,999,999.99') AS MTD_sales_formatted,
TO_CHAR(SUM(MTD_COGS), '999,999,999,999.99') AS MTD_COGS_formatted,
TO_CHAR(SUM(COGS_goal), '999,999,999,999.99') AS COGS_goal_formatted,
TO_CHAR(SUM(AP_Total), '999,999,999,999.99') AS AP_Total_formatted,
5
from rds_merge_ca1545		
;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
values		
('QTD Sales',		
'QTD COGS',		
'RunRate COGS',		
'Forecast AP Total'	,
6
)		
;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
select 		
TO_CHAR(SUM(QTD_sales), '999,999,999,999.99') AS QTD_sales_formatted,
    TO_CHAR(SUM(QTD_COGS), '999,999,999,999.99') AS QTD_COGS_formatted,
    TO_CHAR(SUM((MTD_COGS / ifnull(Day,0)) * Days), '999,999,999,999.99') AS MTD_COGS_days_formatted,
    TO_CHAR(SUM(Forecast_AP_Total), '999,999,999,999.99') AS Forecast_AP_Total_formatted,
    7
from rds_merge_ca1545		
;


insert into rds_ca1545_final		
(s1,id)		
values('',8)		
;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
values		
(		
'Report',		
'DPO Per Actual COGS',		
'DPO Per Forecast COGS',		
'DPO Per Runrate COGS',
9
)		
;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
select 'Actual AP',		
 TO_CHAR( NVL(SUM(AP_Total) / DECODE(SUM(MTD_COGS * 12), 0, NULL, SUM(MTD_COGS * 12)) * 365, 0),
        '999,999,999,999.99') AS AP_Total_MTD_COGS_formatted,
 TO_CHAR( SUM(AP_Total) / SUM(COGS_goal * 12) * 365,
        '999,999,999,999.99') AS AP_Total_COGS_goal_formatted,
 TO_CHAR( NVL(SUM(AP_Total) / DECODE(SUM((MTD_COGS / Day) * Days * 12), 0, NULL, SUM((MTD_COGS / Day) * Days * 12)) * 365, 0),
        '999,999,999,999.99') AS AP_Total_MTD_COGS_Days_formatted,
        10
from rds_merge_ca1545		
;		


insert into rds_ca1545_final		
(s1,s2,s3,s4,id)		
select 'Forecast AP',		
TO_CHAR( NVL(SUM(Forecast_AP_Total) / DECODE(SUM(MTD_COGS * 12), 0, NULL, SUM(MTD_COGS * 12)) * 365, 0),
        '999,999,999,999.99' ) AS Forecast_AP_Total_MTD_COGS_formatted,  
TO_CHAR(SUM(Forecast_AP_Total) / SUM(COGS_goal * 12) * 365,
    '999,999,999,999.99') AS Forecast_AP_Total_COGS_goal_formatted,
TO_CHAR( NVL(SUM(Forecast_AP_Total) / DECODE(SUM((MTD_COGS / Day) * Days * 12), 0, NULL, SUM((MTD_COGS / Day) * Days * 12)) * 365, 0),
    '999,999,999,999.99') AS Forecast_AP_Total_MTD_COGS_Days_formatted,
    11
from rds_merge_ca1545		
;	

				 
insert into rds_ca1545_final		
(s1,id)		
values('',12)		
;		



insert into rds_ca1545_final		
values('vend_no','vend_name','disc_percent','disc_days','net_days','forecat_payment','actual_payment','payment_due','Day','Days','vend_type','AP_Total','Forecast_AP_Total','sales_goal','MTD_sales','QTD_sales','COGS_goal','Daily_COGS_goal','MTD_COGS','QTD_COGS','MTD_receipts','QTD_receipts',13		
)		
;

		
insert into rds_ca1545_final		
select		
    CAST(vend_no AS VARCHAR(100)) AS vend_no_str,
    CAST(vend_name AS VARCHAR(100)) AS vend_name_str,
    CAST(disc_percent AS VARCHAR(100)) AS disc_percent_str,
    CAST(disc_days AS VARCHAR(100)) AS disc_days_str,
    CAST(net_days AS VARCHAR(100)) AS net_days_str,
    
    TO_CHAR(forecast_payment, '999,999,999,999.99') AS forecast_payment_str,
    TO_CHAR(ifnull(actual_payment,0.00), '999,999,999,999.99') AS actual_payment_str,
    TO_CHAR(payment_due, '999,999,999,999.99') AS payment_due_str,
    
    CAST(Day AS VARCHAR(100)) AS day_str,
    CAST(Days AS VARCHAR(100)) AS days_str,
    CAST(vend_type AS VARCHAR(100)) AS vend_type_str,
    
    TO_CHAR(AP_Total, '999,999,999,999.99') AS AP_Total_str,
    TO_CHAR(Forecast_AP_Total, '999,999,999,999.99') AS Forecast_AP_Total_str,
    TO_CHAR(sales_goal, '999,999,999,999.99') AS sales_goal_str,
    TO_CHAR(MTD_sales, '999,999,999,999.99') AS MTD_sales_str,
    TO_CHAR(QTD_sales, '999,999,999,999.99') AS QTD_sales_str,
    
    TO_CHAR(COGS_goal, '999,999,999,999.99') AS COGS_goal_str,
    TO_CHAR(Daily_COGS_goal, '999,999,999,999.99') AS Daily_COGS_goal_str,
    TO_CHAR(MTD_COGS, '999,999,999,999.99') AS MTD_COGS_str,
    TO_CHAR(QTD_COGS, '999,999,999,999.99') AS QTD_COGS_str,
    
    TO_CHAR(MTD_receipts, '999,999,999,999.99') AS MTD_receipts_str,
    TO_CHAR(QTD_receipts, '999,999,999,999.99') AS QTD_receipts_str,
    14
from rds_merge_ca1545		
order by vend_no		
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select id,
	s1,
	s2,
	s3,
	s4,
	s5,
	s6,
	s7,
	s8,
	s9,
	s10,
	s11,
	s12,
	s13,
	s14,
	s15,
	s16,
	s17,
	s18,
	s19,
	s20,
	s21,
	s22
from rds_ca1545_final 
;

create table rdsetl.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
