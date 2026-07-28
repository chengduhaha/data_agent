drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_2;
drop table if exists rdsetl.rds_tmp_body;
drop table if exists rdsetl.rds_tmp_sheet_config;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
	sheet_index int,
	sheet_name varchar(50),
	title_active varchar(1),
	date_pattern varchar(50)
);

insert into rdsetl.rds_tmp_sheet_config values(1,'Summary',null,null);
insert into rdsetl.rds_tmp_sheet_config values(2,'Detail',null,null);

drop table if exists t_disc_orders_19383;
drop table if exists t_cust_19383;
drop table if exists t_19383;
drop table if exists t_discount_order_19383;
drop table if exists t_discount_19383;
drop table if exists t_all_19383;
drop table if exists t_total_19383;

create local temporary table t_disc_orders_19383 on commit preserve rows as
with params as
(
    select
        cast(timestampadd(dd, -day(getdate()), getdate()) as date) as date_flag,
        cast(code_value as int) as grace_period
    from dim_us.dim_pub_list_box_detail
    where list_box_code = 'GRAC'
      and delete_datetime is null
)
select
    hc.cust_no,
    hc.order_no,
    hc.order_type,
    hc.terms,
    tf.terms_desc,
    to_char(hc.doc_date, 'MM/DD/YYYY') as doc_date,
    datediff('day', hc.doc_date, params.date_flag) as age_days,
    params.grace_period as Grace,
    tf.terms_days,
    tf.disc_days,
    tf.disc_days + params.grace_period as max_disc_days,
    tf.terms_days + params.grace_period as max_terms_days,
    tf.disc_percent,
    hc.amount,
    cast(null as varchar(60)) as cust_name,
    case
        when datediff('day', hc.doc_date, params.date_flag) <= tf.disc_days + params.grace_period
        then (tf.disc_percent / 100) * hc.amount
        else null
    end as disc_amt
from dw_us.dwd_disty_ar_cust_doc_df hc
inner join dim_us.dim_pub_terms_file_view tf on hc.terms = tf.doc_terms
cross join params
where hc.date_flag = params.date_flag
and hc.close_date is null
and tf.disc_percent <> 0
and hc.order_type = 1
;

update t_disc_orders_19383 t
set cust_name = ch.cust_name
from dim_us.dim_pub_customer_info_rt ch
where t.cust_no = ch.cust_no
;

create table rdsetl.rds_tmp_2 as
select *
from t_disc_orders_19383
;

create local temporary table t_cust_19383 on commit preserve rows as
select distinct
    ch.cust_no,
    ch.cust_name,
    cx.xref_no as master_acct,
    ch.default_terms,
    tf.terms_desc,
    tf.terms_days,
    tf.disc_percent,
    tf.disc_days,
    tf.credit_risk
from dim_us.dim_pub_customer_info_rt ch
inner join dim_us.dim_pub_terms_file_view tf on ch.default_terms = tf.doc_terms
left join dim_us.dim_pub_cust_xref_all cx on ch.cust_no = cx.cust_no and cx.xref_type = 'FINAN_SUB' and cx.active = 'Y'
where tf.terms_group = 'D'
and tf.active = 'Y'
and ch.is_discontinued = 'N'
;

--select count(*) from t_cust_19383

drop table if exists t_19383;

create local temporary table t_19383(
    date_flag varchar(6),
    cust_no int,
    net_sales numeric(18, 2)
) on commit preserve rows
;

insert into t_19383 (date_flag, cust_no, net_sales)
select
    to_char(a.date_flag, 'YYYYMM') as date_flag,
    a.bill_to_cust_no as cust_no,
    sum((coalesce(a.unit_price, 0) + coalesce(a.unit_sum_exp, 0)) * a.ship_qty) as net_sales
from t_cust_19383 t
inner join dw_us.dwd_disty_common_pos_di a on t.cust_no = a.bill_to_cust_no
where a.date_flag >= cast(timestampadd(year, -1, timestampadd(dd, 1-day(getdate()), getdate())) as date)
and a.date_flag < cast(timestampadd(dd, 1-day(getdate()), getdate()) as date)
and a.order_line_type != 'Comp'
group by
    to_char(a.date_flag, 'YYYYMM'),
    a.bill_to_cust_no
;

-- select date_flag, count(*) from t_19383 group by date_flag

create local temporary table t_discount_order_19383
(
    date_flag varchar(6),
    cust_no int,
    order_no int,
    order_type int,
    pay_amt numeric(18, 2),
    disc_taken_amt numeric(18, 2),
    doc_date_flag varchar(6)
) on commit preserve rows
;

insert into t_discount_order_19383
select
    to_char(cp.batch_date, 'YYYYMM') as date_flag,
    t.cust_no,
    ca.order_no,
    ca.order_type,
    ca.pay_amt,
    ca.disc_amt_taken,
    to_char(cd.doc_date, 'YYYYMM') as doc_date_flag
from t_cust_19383 t
inner join dw_us.dwd_disty_ar_payment_cust_payment cp on t.cust_no = cp.cust_no
inner join dw_us.dwd_disty_ar_payment_cust_application ca on cp.pay_no = ca.pay_no
--left join dw_us.dwd_disty_ar_his_cust_doc_di cd on ca.order_no = cd.order_no and ca.order_type = cd.order_type
left join dw_us.dwd_disty_ar_cust_doc_df cd on ca.order_no = cd.order_no and ca.order_type = cd.order_type and cd.date_flag = cast(timestampadd(dd, -day(getdate()), getdate()) as date)
where cp.batch_date >= cast(timestampadd(year, -1, timestampadd(dd, 1-day(getdate()), getdate())) as date)
and cp.batch_date < cast(timestampadd(dd, 1-day(getdate()), getdate()) as date)
;

-- select count(*) from t_discount_order_19383

create local temporary table t_discount_19383 on commit preserve rows as
select
    date_flag,
    cust_no,
    sum(pay_amt) as pay_amt,
    sum(disc_taken_amt) as disc_taken_amt
from t_discount_order_19383
where doc_date_flag <> date_flag
group by
    date_flag,
    cust_no
;

create local temporary table t_all_19383 on commit preserve rows as
select
    date_flag,
    cust_no,
    net_sales,
    cast(null as numeric(18, 2)) as pay_amt,
    cast(null as numeric(18, 2)) as disc_taken_amt
from t_19383
union all
select
    date_flag,
    cust_no,
    cast(null as numeric(18, 2)) as net_sales,
    pay_amt,
    disc_taken_amt
from t_discount_19383
;

create local temporary table t_total_19383 on commit preserve rows as
select
    date_flag,
    cust_no,
    sum(net_sales) as net_sales,
    sum(pay_amt) as pay_amt,
    sum(disc_taken_amt) as disc_taken_amt
from t_all_19383
group by
    date_flag,
    cust_no
;

create table rdsetl.rds_tmp as
select
    t.date_flag,
    tc.default_terms,
    coalesce(sum(t.net_sales), 0) as net_sales,
    coalesce(sum(t.pay_amt), 0) as pay_amt_pre_month_o,
    coalesce(sum(t.disc_taken_amt), 0) as disc_taken_amt_pre_month_o
from t_total_19383 t
inner join t_cust_19383 tc on t.cust_no = tc.cust_no
group by
    t.date_flag,
    tc.default_terms
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

insert into rdsetl.rds_tmp_body
select 2 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp_2
;

drop table if exists t_disc_orders_19383;
drop table if exists t_cust_19383;
drop table if exists t_19383;
drop table if exists t_discount_order_19383;
drop table if exists t_discount_19383;
drop table if exists t_all_19383;
drop table if exists t_total_19383;
