set time zone='America/Toronto';

drop table if exists rds_3977_run_ctx;
drop table if exists rds_3977_uv_usd;
drop table if exists rds_3977_uv_cdn;
drop table if exists rds_3977_tb_usd;
drop table if exists rds_3977_tb_cdn;
drop table if exists rds_3977_acc_usd;
drop table if exists rds_3977_acc_cdn;
drop table if exists rds_3977_main;

create local temporary table rds_3977_run_ctx on commit preserve rows as
select max(date_flag) as dt
from dw_ca.dws_disty_ap_vend_aging_df
where date_flag < date_trunc('month', current_date())::date
;

create local temporary table rds_3977_main on commit preserve rows as
select
    h.vend_no,
    h.vend_name,
    h.vend_type,
    cast(null as varchar(60)) as old_comp,
    h.discontinued,
    h.restricted,
    h.analyst_id,
    h.analyst_loginid,
    h.cn_analyst_id,
    h.cn_analyst_loginid,
    h.master_vend_flag,
    h.master_vend_no,
    h.vend_company,
    h.vend_currency,
    h.vend_segment,
    h.pas_code,
    h.date_flag,
    cast(null as numeric(20, 8)) as uvdebits_usd,
    cast(null as numeric(20, 8)) as uvdebits_cdn,
    cast(null as numeric(20, 8)) as tb_usd,
    cast(null as numeric(20, 8)) as tb_cdn,
    cast(null as numeric(20, 8)) as accruals_usd,
    cast(null as numeric(20, 8)) as accruals_cdn,
    cast(null as numeric(20, 8)) as subtotal_usd,
    cast(null as numeric(20, 8)) as subtotal_cdn,
    cast(null as numeric(20, 8)) as ap_total_usd,
    cast(null as numeric(20, 8)) as ap_total_cdn
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level = 'V'
;

create local temporary table rds_3977_uv_usd on commit preserve rows as
select
    h.vend_no,
    sum(coalesce(h.usd_total_amt, h.usd_unvouched_amt, 0)) as amt
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level in ('UOT', 'UOTC')
  and cast(h.terms_no as varchar(10)) in ('3', '12', '27', '126', '1127')
group by h.vend_no
;

create local temporary table rds_3977_uv_cdn on commit preserve rows as
select
    h.vend_no,
    sum(coalesce(h.total_amt, h.unvouched_amt, 0)) as amt
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level in ('UOT', 'UOTC')
  and cast(h.terms_no as varchar(10)) in ('3', '12', '27', '126', '1127')
group by h.vend_no
;

create local temporary table rds_3977_tb_usd on commit preserve rows as
select
    h.vend_no,
    sum(coalesce(h.usd_total_amt, h.usd_total_doc_amt, 0)) as amt
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level = 'VVU'
  and cast(h.terms_no as varchar(10)) = 'V'
group by h.vend_no
;

create local temporary table rds_3977_tb_cdn on commit preserve rows as
select
    h.vend_no,
    sum(coalesce(h.total_amt, h.total_doc_amt, 0)) as amt
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level = 'VVU'
  and cast(h.terms_no as varchar(10)) = 'V'
group by h.vend_no
;

create local temporary table rds_3977_acc_usd on commit preserve rows as
select
    h.vend_no,
    sum(coalesce(h.usd_total_amt, h.usd_unvouched_amt, 0)) as amt
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level in ('UOT', 'UOTC')
  and cast(h.terms_no as varchar(10)) in ('2', '362', '125', '1125', '363')
group by h.vend_no
;

create local temporary table rds_3977_acc_cdn on commit preserve rows as
select
    h.vend_no,
    sum(coalesce(h.total_amt, h.unvouched_amt, 0)) as amt
from dm_ca.dm_ap_aging_header_df h
cross join rds_3977_run_ctx c
where h.date_flag = c.dt
  and h.sum_level in ('UOT', 'UOTC')
  and cast(h.terms_no as varchar(10)) in ('2', '362', '125', '1125', '363')
group by h.vend_no
;

update rds_3977_main m
set uvdebits_usd = u.amt
from rds_3977_uv_usd u
where m.vend_no = u.vend_no
;

update rds_3977_main m
set uvdebits_cdn = u.amt
from rds_3977_uv_cdn u
where m.vend_no = u.vend_no
;

update rds_3977_main m
set tb_usd = t.amt
from rds_3977_tb_usd t
where m.vend_no = t.vend_no
;

update rds_3977_main m
set tb_cdn = t.amt
from rds_3977_tb_cdn t
where m.vend_no = t.vend_no
;

update rds_3977_main m
set accruals_usd = a.amt
from rds_3977_acc_usd a
where m.vend_no = a.vend_no
;

update rds_3977_main m
set accruals_cdn = a.amt
from rds_3977_acc_cdn a
where m.vend_no = a.vend_no
;

update rds_3977_main
set subtotal_usd = coalesce(uvdebits_usd, 0) + coalesce(tb_usd, 0),
    subtotal_cdn = coalesce(uvdebits_cdn, 0) + coalesce(tb_cdn, 0),
    ap_total_usd = coalesce(uvdebits_usd, 0) + coalesce(tb_usd, 0) + coalesce(accruals_usd, 0),
    ap_total_cdn = coalesce(uvdebits_cdn, 0) + coalesce(tb_cdn, 0) + coalesce(accruals_cdn, 0)
;

update rds_3977_main m
set old_comp = trim(p.profile_c)
from (
    select
        vend_no,
        max(profile_c) as profile_c
    from dim_ca.dim_pub_vendor_profile
    where profile_type = 'OLD_COMP'
      and profile_cat = 'AP'
      and coalesce(active, 'Y') = 'Y'
    group by vend_no
) p
where m.vend_no = p.vend_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
    date_flag,
    vend_currency,
    vend_no,
    vend_name,
    vend_type,
    old_comp,
    uvdebits_usd,
    uvdebits_cdn,
    tb_usd,
    tb_cdn,
    subtotal_usd,
    subtotal_cdn,
    accruals_usd,
    accruals_cdn,
    ap_total_usd,
    ap_total_cdn
from rds_3977_main
union all
select
    null as date_flag,
    null as vend_currency,
    null as vend_no,
    'Total Sum      ' as vend_name,
    null as vend_type,
    null as old_comp,
    sum(uvdebits_usd),
    sum(uvdebits_cdn),
    sum(tb_usd),
    sum(tb_cdn),
    sum(subtotal_usd),
    sum(subtotal_cdn),
    sum(accruals_usd),
    sum(accruals_cdn),
    sum(ap_total_usd),
    sum(ap_total_cdn)
from rds_3977_main
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag,
    'standard' as body_type,
    count(*) as cnt
from rdsetl.rds_tmp
;
