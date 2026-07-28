set time zone='America/Los_Angeles';

drop table if exists rds_us11417_date;
create local temporary table rds_us11417_date on commit preserve rows as
select m
	,max(date_flag) as month_end_12
from dim_us.dim_pub_date
where date_flag >= add_months(current_date()-1,-11)
and date_flag < current_date()
group by m
;

drop table if exists rds_us11417_sales;
create local temporary table rds_us11417_sales on commit preserve rows as
select a.cust_no
	,sum(ifnull(a.net_sales,0)) as net_sales
	,sum(ifnull(a.gross_sales,0)) as gross_sales
	,sum(ifnull(a.gross_cost,0)) as gross_cost
	,sum(ifnull(a.ngm_amt,0)) as ngm_amt
from dw_us.dws_disty_brpt_cust_mtd a
inner join rds_us11417_date b
on a.date_flag = b.month_end_12
group by a.cust_no
having sum(ifnull(a.gross_sales,0)) <> 0
;

drop table if exists rds_us11417_sales_60_days;
create local temporary table rds_us11417_sales_60_days on commit preserve rows as
select bill_to_cust_no as cust_no
	,sum(ifnull(extend_net_price,0)) as net_sales_60
from dw_us.dwd_disty_common_pos_di
where order_line_type != 'Comp'
and date_flag >= current_date()-60
and date_flag < current_date()
group by bill_to_cust_no
;

drop table if exists rds_us11417_doc;
create local temporary table rds_us11417_doc on commit preserve rows as
select cust_no
	,order_type
	,to_char(due_date,'mm/dd/yyyy') as due_date
	,to_char(doc_date,'mm/dd/yyyy') as doc_date
	,case when amount > 0 then 'DR' when amount < 0 then 'CR' end as cmdm_flag
	,sum(case when due_date_agedays < 1 then amount - ifnull(applied,0) else 0 end) as age0
	,sum(case when due_date_agedays >= 1 and due_date_agedays < 31 then amount - ifnull(applied,0) else 0 end) as age1_30
	,sum(case when due_date_agedays >= 31 and due_date_agedays < 61 then amount - ifnull(applied,0) else 0 end) as age31_60
	,sum(case when due_date_agedays >= 61 and due_date_agedays < 91 then amount - ifnull(applied,0) else 0 end) as age61_90
	,sum(case when due_date_agedays >= 91 and due_date_agedays < 121 then amount - ifnull(applied,0) else 0 end) as age91_120
	,sum(case when due_date_agedays >= 121 then amount - ifnull(applied,0) else 0 end) as age120_plus
	,sum(case when due_date_agedays >= 91 and due_date_agedays < 181 then amount - ifnull(applied,0) else 0 end) as age91_180
	,sum(case when due_date_agedays >= 181 then amount - ifnull(applied,0) else 0 end) as age180_plus
	,count(distinct order_no) as doc_count
	,sum(amount - ifnull(applied,0)) as open_ar
	,due_date_agedays
from dw_us.dwd_disty_ar_cust_doc_df
where date_flag = current_date()-1
and amount - ifnull(applied,0) <> 0
and close_date is null
group by cust_no
	,order_type
	,to_char(due_date,'mm/dd/yyyy')
	,to_char(doc_date,'mm/dd/yyyy')
	,case when amount > 0 then 'DR' when amount < 0 then 'CR' end
	,due_date_agedays
;

drop table if exists rds_us11417_cust_list;
create local temporary table rds_us11417_cust_list on commit preserve rows as
select cust_no
from rds_us11417_sales
union
select cust_no
from rds_us11417_doc
;

drop table if exists rds_us11417_final;
create local temporary table rds_us11417_final on commit preserve rows as
select to_char(getdate(), 'YYYY-MM-DD') as date_flag
	,'SNX US' as org
	,d.collector_supervisor_name
	,d.collector_manager_name
	,d.collector_director_name
	,d.collector_vp_name
	,d.credit_analyst_manager_name
	,d.credit_analyst_director_name
	,d.credit_analyst_vp_name
	,e.mgr_name AS sales_rep_manager_name
	,e.dir_name AS sales_rep_director_name
	,e.vp_name AS sales_rep_vp_name
	,d.credit_analyst
	,d.credit_analyst_name
	,d.collector_id
	,d.collector_name
	,d.cust_type
	,d.cust_type_descr
	,d.cust_name
	,ifnull(d.finance_master, d.cust_no) as finance_master
	,d.cust_no
	,d.default_terms
	,d.is_discontinued
	,f.terms_desc
	,f.terms_days
	,f.disc_percent
	,f.disc_days
	,d.sales_terr
	,e.sales_rep_name
	,cast(null as varchar(100)) as address
	,cast(null as varchar(200)) as city
	,cast(null as varchar(200)) as state
	,cast(null as varchar(200)) as zip
	,cast(null as varchar(200)) as ap_contact_name
	,cast(null as varchar(200)) as ap_title
	,cast(null as varchar(200)) as ap_phone_no
	,cast(null as varchar(200)) as ap_email_address
	,b.net_sales
	,b.gross_sales
	,b.gross_sales - b.gross_cost as gross_profit_amt
	,(b.gross_sales - b.gross_cost)*100/nullif(b.net_sales,0) as gross_profit
	,b.ngm_amt
	,b.ngm_amt*100/nullif(b.net_sales,0) as ngm_amt_pct
	,d.currency
	,d.credit_limit
	,to_char(d.next_review,'mm/dd/yyyy') as next_review
	,'USD' as ar_currency
	,d.pending_amt
	,c.cmdm_flag
	,c.due_date
	,c.due_date_agedays
	,c.doc_count
	,c.open_ar
	,c.age0
	,c.age1_30
	,c.age31_60
	,c.age61_90
	,c.age91_120
	,c.age120_plus
	,c.age91_180
	,c.age180_plus
	,g.net_sales_60
	,c.open_ar*60/nullif(g.net_sales_60,0) as dso
	,c.doc_date
	,c.order_type
	,d.sales_terr as territory
	,d.division_desc
from rds_us11417_cust_list a
inner join dim_us.dim_pub_customer_info d
on a.cust_no = d.cust_no
left join rds_us11417_sales b
on a.cust_no = b.cust_no
left join rds_us11417_doc c
on a.cust_no = c.cust_no
left join dim_us.dim_pub_sales_hierarchy_primary_role_by_terr_view e
on d.sales_terr = e.sales_terr
left join dim_us.dim_pub_terms_file_view f
on d.default_terms = f.doc_terms
left join rds_us11417_sales_60_days g
on a.cust_no = g.cust_no
where d.default_terms <> 'DRM'
;


drop table if exists cust_limit_us11417;
create local temporary table cust_limit_us11417 on commit preserve rows as
select distinct
       a.cust_no,
       a.default_terms,
       a.finance_master,
       case when n.doc_char is not null then 'Y' else ifnull(cp.profile_c, 'N') end AS exclued
from rds_us11417_final a
LEFT JOIN dim_us.dim_pub_terms_file_view tf on a.default_terms = tf.doc_terms
LEFT JOIN dim_us.dim_pub_cust_profile_all cp on a.cust_no = cp.cust_no
                                           and cp.profile_type = 'E_SUM_LMT'
                                           and cp.profile_cat = 'CRED'
                                           and cp.active = 'Y'
LEFT JOIN ods_us.ods_cis_corp_no_ctrl n on tf.terms_group = n.doc_char
                                      and n.kind = 'AUTOCRED_CREDIT_LIMIT_AGGREGATE_EXCLUDE_TERMS_GROUP'
                                      and n.active_flag = 'Y'
where ifnull(a.is_discontinued, 'N') = 'N'
;

drop table if exists cust_master_limit_us11417;
create local temporary table cust_master_limit_us11417 on commit preserve rows as
select distinct
       a.finance_master,
       cc.credit_limit
from cust_limit_us11417 a
INNER JOIN dim_us.dim_pub_customer_info cc on a.finance_master = cc.cust_no
where a.exclued <> 'Y'
  and not exists (
      select 1
      from cust_limit_us11417 c
      where c.cust_no = a.finance_master
        and c.exclued = 'Y'
  )
;

update rds_us11417_final a
set credit_limit = t.credit_limit
from cust_master_limit_us11417 t
where a.finance_master = t.finance_master
;


update rds_us11417_final a
set address = b.address1a,
    city = b.city1a,
    state = b.state,
    zip = b.zip_code
from dim_us.dim_pub_customer_address_contacts_info b
where a.cust_no = b.xref_no
and b.addr_xref_seq = 1
;

update rds_us11417_final a
set ap_contact_name = b.contact_name,
    ap_title = b.title,
	ap_phone_no = b.phone_no,
	ap_email_address = b.email_address
from dim_us.dim_pub_customer_address_contacts_info b
where a.cust_no = b.xref_no
and b.active_flag_contact = 'Y'
and b.delete_datetime_contact is null
and b.contact_name is not null
;

drop table if exists rds_us11417_format;
create local temporary table rds_us11417_format on commit preserve rows as
select date_flag as 'date_flag'
	,org as 'ORG'
	,collector_supervisor_name as 'Collectors Supervisor Name'
	,collector_manager_name as 'Collectors Manager name'
	,collector_director_name as 'Collectors Director name'
	,collector_vp_name as 'Collectors VP name'
	,credit_analyst_manager_name as 'Credit Analysts Manager name'
	,credit_analyst_director_name as 'Credit Analysts Director name'
	,credit_analyst_vp_name as 'Credit Analysts VP name'
	,sales_rep_manager_name as 'Sales Reps Manager name'
	,sales_rep_director_name as 'Sales Reps Director name'
	,sales_rep_vp_name as 'Sales Reps VP name'
	,credit_analyst as 'cred_analyst'
	,credit_analyst_name as 'cred_analyst_name'
	,collector_id as 'collector'
	,collector_name as 'collector_name'
	,cust_type as 'cust_type'
	,cust_type_descr as 'cust_type_descr'
	,cust_name as 'cust_name'
	,finance_master as 'mcust'
	,cust_no as 'cust_no'
	,default_terms as 'terms'
	,terms_desc as 'terms_desc'
	,terms_days as 'terms_days'
	,disc_percent as 'disc_percent'
	,disc_days as 'disc_days'
	,sales_terr as 'sales_terr'
	,sales_rep_name as 'rep_name'
	,address as 'address'
	,city as 'city'
	,state as 'state'
	,zip as 'zip'
	,ap_contact_name as 'ap_contact'
	,ap_email_address as 'ap_email_address'
	,ap_title as 'ap_title'
	,ap_phone_no as 'ap_phone'
	,round(net_sales,4)::NUMERIC(26,4) as 'nsales_12mths'
	,round(gross_sales,4)::NUMERIC(26,4) as 'Gross Sales 12mths $'
	,round(gross_profit_amt,4)::NUMERIC(26,4) as 'Gross Profit 12mths $'
	,to_char(gross_profit, 'FM999999999999999990.00')||'%' as 'Gross Profit 12mths %'
	,round(ngm_amt,4)::NUMERIC(26,4) as 'Net Gross Margin 12mths $'
	,to_char(ngm_amt_pct, 'FM999999999999999990.00')||'%' as 'Net Gross Margin 12mths %'
	,currency as 'CL Currency'
	,round(credit_limit,4)::NUMERIC(26,4) as 'credit_limit'
	,next_review as 'review_date'
	,ar_currency as 'A/R Currency'
	,round(pending_amt,4)::NUMERIC(26,4) as 'pending_amt'
	,cmdm_flag as 'cmdm_flag'
	,due_date as 'due_date'
	,due_date_agedays as 'age_days'
	,doc_count as 'doc_count'
	,round(open_ar,4)::NUMERIC(26,4) as 'total'
	,round(age0,4)::NUMERIC(26,4) as 'current'
	,round(age1_30,4)::NUMERIC(26,4) as ' 1-30'
	,round(age31_60,4)::NUMERIC(26,4) as '31-60'
	,round(age61_90,4)::NUMERIC(26,4) as '61-90'
	,round(age91_120,4)::NUMERIC(26,4) as '91-120'
	,round(age120_plus,4)::NUMERIC(26,4) as '>120+ '
	,round(age91_180,4)::NUMERIC(26,4) as '91-180'
	,round(age180_plus,4)::NUMERIC(26,4) as '>180+ '
	,round(net_sales_60,4)::NUMERIC(26,4) as 'nsales_60d'
	,round(dso,4)::NUMERIC(26,4) as 'DSO'
	,doc_date as 'Doc_date'
	,order_type as 'Order Type'
	,territory as 'Territory'
	,division_desc as 'Customer Div'
from rds_us11417_final
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_us11417_format
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag, 'Standard' as body_type, count(*) as cnt
from rdsetl.rds_tmp
;