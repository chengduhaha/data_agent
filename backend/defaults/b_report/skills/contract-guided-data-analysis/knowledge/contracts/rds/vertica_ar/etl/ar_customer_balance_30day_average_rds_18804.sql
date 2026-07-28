drop table if exists table_us_18804_data;
create local temporary table table_us_18804_data on commit preserve rows as
select a.cust_no,
		b.cust_name,
		round(sum(amount-applied), 2) as total_ar_balance,
		cast(null as float) as last_30D_avg_ar_balance
from ods_us.ods_cis_corp_cust_doc a
inner join ods_us.ods_cis_corp_customer_header b
on a.cust_no = b.cust_no
group by a.cust_no , b.cust_name
;

drop table if exists table_us_18804_data_t1;
create local temporary table table_us_18804_data_t1 (
	cust_no int,
	ar_bal float null
) on commit preserve rows ;

insert into table_us_18804_data_t1
select cust_no, round(ar_bal_total/30, 2) as ar_bal
from
(
	select cust_no, sum(total) as ar_bal_total
	from dw_us.dws_disty_ar_cust_sum_age_df
	where view_level = 'CUST_COM'
	and data_period='D'
	and date_flag between (current_date() - 30) and current_date()
	group by cust_no
) temp
;

update table_us_18804_data x
set last_30D_avg_ar_balance=a.ar_bal
from table_us_18804_data_t1 a
where x.cust_no = a.cust_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select cust_no as 'Cust No.',
	   cust_name as 'Cust Name',
	   total_ar_balance as 'Cust.Total AR Balance',
	   last_30D_avg_ar_balance	as 'Cust. Last 30 Days Average AR Balance'
from table_us_18804_data
order by 1;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;