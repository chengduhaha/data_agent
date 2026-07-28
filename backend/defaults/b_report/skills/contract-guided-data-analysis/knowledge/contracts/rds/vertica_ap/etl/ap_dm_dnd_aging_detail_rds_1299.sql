set time zone='America/Toronto';

drop table if exists rds_ca1299_debit_all;
create local temporary table rds_ca1299_debit_all on commit preserve rows as
select
    h.vend_no,
    h.vend_name,
    h.discontinued,
    h.vend_type,
    h.ap_hold_flag,
    h.analyst_id,
    ifnull(h.age3, 0) + ifnull(h.age8, 0) AS total_dm_60,
    h.total_amt AS total_dm_all,
    h.vend_currency,
    h.pas_code,
    h.terms_desc
from dm_ca.dm_ap_aging_header_df h
where h.date_flag = current_date() - 1
  and h.sum_level = 'VCD'
  and cast(h.terms_no AS varchar(10)) = 'DR'
;

drop table if exists rds_ca1299_vcm_27;
create local temporary table rds_ca1299_vcm_27 on commit preserve rows as
select
    h.vend_no,
    ifnull(h.age3, 0) + ifnull(h.age8, 0) AS vcm_dm_60,
    h.total_amt AS vcm_dm_all
from dm_ca.dm_ap_aging_header_df h
where h.date_flag = current_date() - 1
  and h.sum_level = 'OT'
  and cast(h.terms_no AS varchar(10)) = '27'
;

drop table if exists rds_ca1299_dm_vend;
create local temporary table rds_ca1299_dm_vend on commit preserve rows as
select distinct
    p.vend_no
from dim_ca.dim_disty_ap_dnd_profile p
where trim(p.profile_type) = 'DM'
  and trim(p.status) = 'A'
;

drop table if exists rds_ca1299_dnd_vend;
create local temporary table rds_ca1299_dnd_vend on commit preserve rows as
select distinct
    p.vend_no
from dim_ca.dim_disty_ap_dnd_profile p
where trim(p.profile_type) = 'DND'
  and trim(p.status) = 'A'
;

drop table if exists rds_ca1299_old_comp;
create local temporary table rds_ca1299_old_comp on commit preserve rows as
select
    p.vend_no,
    max(p.profile_c) AS profile_c
from dim_ca.dim_pub_vendor_profile p
where trim(p.profile_type) = 'OLD_COMP'
  and trim(p.profile_cat) = 'AP'
  and ifnull(trim(p.active), 'Y') = 'Y'
group by
    p.vend_no
;

drop table if exists rds_ca1299_final;
create local temporary table rds_ca1299_final on commit preserve rows as
select
    a.vend_no,
    a.vend_name,
    a.discontinued,
    a.vend_type,
    a.ap_hold_flag,
    case when dm.vend_no is null then 'N' else 'Y' end AS dm_flag,
    case when dnd.vend_no is null then 'N' else 'Y' end AS dnd_flag,
    a.analyst_id,
    m.name AS analyst_name,
    ifnull(a.total_dm_60, 0) - ifnull(v.vcm_dm_60, 0) AS ap_dm_60,
    ifnull(v.vcm_dm_60, 0) AS vcm_dm_60,
    ifnull(a.total_dm_60, 0) AS total_dm_60,
    ifnull(a.total_dm_all, 0) - ifnull(v.vcm_dm_all, 0) AS ap_dm_all,
    ifnull(v.vcm_dm_all, 0) AS vcm_dm_all,
    ifnull(a.total_dm_all, 0) AS total_dm_all,
    a.vend_currency,
    a.pas_code,
    a.terms_desc,
    trim(o.profile_c) AS old_comp
from rds_ca1299_debit_all a
left join rds_ca1299_vcm_27 v
    on a.vend_no = v.vend_no
left join dim_ca.dim_pub_manager m
    on a.analyst_id = m.userid
left join rds_ca1299_dm_vend dm
    on a.vend_no = dm.vend_no
left join rds_ca1299_dnd_vend dnd
    on a.vend_no = dnd.vend_no
left join rds_ca1299_old_comp o
    on a.vend_no = o.vend_no
;

drop table if exists rds_ca1299_detail_base;
create local temporary table rds_ca1299_detail_base on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    ifnull(v.vend_currency, 'CAD') AS vend_curr,
    d.doc_no,
    case
        when d.uv_type = 'U' then cast(d.order_type AS varchar(60))
        else cast(d.doc_type AS varchar(60))
    end AS doc_ord_type,
    case
        when d.uv_type = 'U' then d.rec_datetime::date
        else d.doc_date::date
    end AS dm_date,
    case
        when d.uv_type = 'V' then cast(d.vend_inv_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type = 27 then cast(d.order_no AS varchar(60)) || '-' || cast(d.order_line_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type in (3, 12) then cast(d.order_no AS varchar(60)) || '/' || cast(d.doc_ref AS varchar(60))
    end AS invoice_order,
    current_date() - 1 - case when d.uv_type = 'U' then d.rec_datetime::date else d.doc_date::date end AS age,
    cast(null AS numeric(20, 8)) AS usd_amt,
    d.amt AS cdn_amt,
    d.doc_type,
    d.doc_date,
    d.doc_entry_datetime::date AS doc_entry_datetime,
    d.vend_inv_no,
    d.order_no,
    d.rec_datetime,
    d.amt,
    d.ap_cnanalyst_id,
    m.name AS analyst_name
from dm_ca.dm_ap_aging_detail_df d
left join dim_ca.dim_pub_vendor_info v
    on d.vend_no = v.vend_no
left join dim_ca.dim_pub_manager m
    on v.ap_clerk = m.userid
where d.date_flag = current_date() - 1
  and ifnull(d.entry_id, 0) = 0
  and ifnull(d.amt, 0) < 0
;

delete from rds_ca1299_detail_base where age < 61;

drop table if exists rds_ca1299_usd_base;
create local temporary table rds_ca1299_usd_base on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    ifnull(v.vend_currency, 'CAD') AS vend_curr,
    d.doc_no,
    case
        when d.uv_type = 'U' then cast(d.order_type AS varchar(60))
        else cast(d.doc_type AS varchar(60))
    end AS doc_ord_type,
    case
        when d.uv_type = 'U' then d.rec_datetime::date
        else d.doc_date::date
    end AS dm_date,
    case
        when d.uv_type = 'V' then cast(d.vend_inv_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type = 27 then cast(d.order_no AS varchar(60)) || '-' || cast(d.order_line_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type in (3, 12) then cast(d.order_no AS varchar(60)) || '/' || cast(d.doc_ref AS varchar(60))
    end AS invoice_order,
    current_date() - 1 - case when d.uv_type = 'U' then d.rec_datetime::date else d.doc_date::date end AS age,
    ifnull(d.usd_amt, d.amt) AS usd_amt,
    cast(null AS numeric(20, 8)) AS cdn_amt,
    d.doc_type,
    d.doc_date,
    d.doc_entry_datetime::date AS doc_entry_datetime,
    d.vend_inv_no,
    d.order_no,
    d.rec_datetime,
    ifnull(d.usd_amt, d.amt) AS amt,
    d.ap_cnanalyst_id,
    m.name AS analyst_name
from dm_ca.dm_ap_aging_detail_df d
left join dim_ca.dim_pub_vendor_info v
    on d.vend_no = v.vend_no
left join dim_ca.dim_pub_manager m
    on v.ap_clerk = m.userid
where d.date_flag = current_date() - 1
  and ifnull(d.entry_id, 0) = 0
  and ifnull(d.usd_amt, d.amt) < 0
;

delete from rds_ca1299_usd_base where age < 61;

drop table if exists rds_ca1299_usd_sum;
create local temporary table rds_ca1299_usd_sum on commit preserve rows as
select
    u.vend_no,
    u.vend_name,
    u.vend_curr,
    u.analyst_name,
    u.doc_ord_type,
    u.doc_no,
    u.dm_date,
    u.invoice_order,
    u.age,
    u.doc_entry_datetime,
    sum(ifnull(u.usd_amt, 0)) AS usd_amt,
    sum(ifnull(u.cdn_amt, 0)) AS cdn_amt
from rds_ca1299_usd_base u
group by
    u.vend_no,
    u.vend_name,
    u.vend_curr,
    u.analyst_name,
    u.doc_ord_type,
    u.doc_no,
    u.dm_date,
    u.invoice_order,
    u.age,
    u.doc_entry_datetime
;

drop table if exists rds_ca1299_usd_order_sum;
create local temporary table rds_ca1299_usd_order_sum on commit preserve rows as
select
    u.vend_no,
    u.order_no,
    sum(ifnull(u.usd_amt, 0)) AS usd_amt
from rds_ca1299_usd_base u
where u.doc_no is null
   or u.doc_no < 0
group by
    u.vend_no,
    u.order_no
;

drop table if exists rds_ca1299_detail_sum;
create local temporary table rds_ca1299_detail_sum on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    d.doc_ord_type,
    d.doc_no,
    d.dm_date,
    d.invoice_order,
    d.age,
    d.doc_entry_datetime,
    ifnull(max(d.usd_amt), max(o.usd_amt)) AS usd_amt,
    sum(ifnull(d.cdn_amt, 0)) AS cdn_amt
from rds_ca1299_detail_base d
left join rds_ca1299_usd_order_sum o
    on d.vend_no = o.vend_no
   and d.order_no = o.order_no
   and (d.doc_no is null or d.doc_no < 0)
group by
    d.vend_no,
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    d.doc_ord_type,
    d.doc_no,
    d.dm_date,
    d.invoice_order,
    d.age,
    d.doc_entry_datetime
;

drop table if exists rds_ca1299_detail_sum_final;
create local temporary table rds_ca1299_detail_sum_final on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    d.doc_ord_type,
    d.doc_no,
    d.dm_date,
    d.invoice_order,
    d.age,
    d.doc_entry_datetime,
    ifnull(d.usd_amt, u.usd_amt) AS usd_amt,
    d.cdn_amt
from rds_ca1299_detail_sum d
left join rds_ca1299_usd_sum u
    on d.vend_no = u.vend_no
   and d.vend_name = u.vend_name
   and d.vend_curr = u.vend_curr
   and d.analyst_name = u.analyst_name
   and d.doc_ord_type = u.doc_ord_type
   and d.doc_no = u.doc_no
   and d.dm_date = u.dm_date
   and d.invoice_order = u.invoice_order
   and d.age = u.age
   and d.doc_entry_datetime = u.doc_entry_datetime
;

drop table if exists rds_ca1299_audit_detail_base;
create local temporary table rds_ca1299_audit_detail_base on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    ifnull(v.vend_currency, 'CAD') AS vend_curr,
    d.doc_no,
    case
        when d.uv_type = 'U' then cast(d.order_type AS varchar(60))
        else cast(d.doc_type AS varchar(60))
    end AS doc_ord_type,
    case
        when d.uv_type = 'U' then d.rec_datetime::date
        else d.doc_date::date
    end AS dm_date,
    case
        when d.uv_type = 'V' then cast(d.vend_inv_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type = 27 then cast(d.order_no AS varchar(60)) || '-' || cast(d.order_line_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type in (3, 12) then cast(d.order_no AS varchar(60)) || '/' || cast(d.doc_ref AS varchar(60))
    end AS invoice_order,
    current_date() - 1 - case when d.uv_type = 'U' then d.rec_datetime::date else d.doc_date::date end AS age,
    cast(null AS numeric(20, 8)) AS usd_amt,
    d.amt AS cdn_amt,
    d.doc_entry_datetime::date AS doc_entry_datetime,
    d.order_no,
    m.name AS analyst_name
from dm_ca.dm_ap_aging_detail_df d
left join dim_ca.dim_pub_vendor_info v
    on d.vend_no = v.vend_no
left join dim_ca.dim_pub_manager m
    on v.ap_clerk = m.userid
where d.date_flag = current_date() - 1
  and ifnull(d.entry_id, 0) = 0
  and ifnull(d.amt, 0) < 0
;

delete from rds_ca1299_audit_detail_base where age < 61;

drop table if exists rds_ca1299_audit_usd_base;
create local temporary table rds_ca1299_audit_usd_base on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    ifnull(v.vend_currency, 'CAD') AS vend_curr,
    d.doc_no,
    case
        when d.uv_type = 'U' then cast(d.order_type AS varchar(60))
        else cast(d.doc_type AS varchar(60))
    end AS doc_ord_type,
    case
        when d.uv_type = 'U' then d.rec_datetime::date
        else d.doc_date::date
    end AS dm_date,
    case
        when d.uv_type = 'V' then cast(d.vend_inv_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type = 27 then cast(d.order_no AS varchar(60)) || '-' || cast(d.order_line_no AS varchar(60))
        when d.uv_type = 'U' and d.order_type in (3, 12) then cast(d.order_no AS varchar(60)) || '/' || cast(d.doc_ref AS varchar(60))
    end AS invoice_order,
    current_date() - 1 - case when d.uv_type = 'U' then d.rec_datetime::date else d.doc_date::date end AS age,
    ifnull(d.usd_amt, d.amt) AS usd_amt,
    cast(null AS numeric(20, 8)) AS cdn_amt,
    d.doc_entry_datetime::date AS doc_entry_datetime,
    d.order_no,
    m.name AS analyst_name
from dm_ca.dm_ap_aging_detail_df d
left join dim_ca.dim_pub_vendor_info v
    on d.vend_no = v.vend_no
left join dim_ca.dim_pub_manager m
    on v.ap_clerk = m.userid
where d.date_flag = current_date() - 1
  and ifnull(d.entry_id, 0) = 0
  and ifnull(d.usd_amt, d.amt) < 0
;

delete from rds_ca1299_audit_usd_base where age < 61;

drop table if exists rds_ca1299_audit_usd_sum;
create local temporary table rds_ca1299_audit_usd_sum on commit preserve rows as
select
    u.vend_no,
    u.vend_name,
    u.vend_curr,
    u.analyst_name,
    u.doc_ord_type,
    u.doc_no,
    u.dm_date,
    u.invoice_order,
    u.age,
    u.doc_entry_datetime,
    sum(ifnull(u.usd_amt, 0)) AS usd_amt,
    sum(ifnull(u.cdn_amt, 0)) AS cdn_amt
from rds_ca1299_audit_usd_base u
group by
    u.vend_no,
    u.vend_name,
    u.vend_curr,
    u.analyst_name,
    u.doc_ord_type,
    u.doc_no,
    u.dm_date,
    u.invoice_order,
    u.age,
    u.doc_entry_datetime
;

drop table if exists rds_ca1299_audit_usd_order_sum;
create local temporary table rds_ca1299_audit_usd_order_sum on commit preserve rows as
select
    u.vend_no,
    u.order_no,
    sum(ifnull(u.usd_amt, 0)) AS usd_amt
from rds_ca1299_audit_usd_base u
where u.doc_no is null
   or u.doc_no < 0
group by
    u.vend_no,
    u.order_no
;

drop table if exists rds_ca1299_detail_sum_audit;
create local temporary table rds_ca1299_detail_sum_audit on commit preserve rows as
select
    d.vend_no,
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    d.doc_ord_type,
    d.doc_no,
    d.dm_date,
    d.invoice_order,
    d.age,
    d.doc_entry_datetime,
    ifnull(ifnull(max(d.usd_amt), max(o.usd_amt)), max(u.usd_amt)) AS usd_amt,
    sum(ifnull(d.cdn_amt, 0)) AS cdn_amt
from rds_ca1299_audit_detail_base d
left join rds_ca1299_audit_usd_order_sum o
    on d.vend_no = o.vend_no
   and d.order_no = o.order_no
   and (d.doc_no is null or d.doc_no < 0)
left join rds_ca1299_audit_usd_sum u
    on d.vend_no = u.vend_no
   and d.vend_name = u.vend_name
   and d.vend_curr = u.vend_curr
   and d.analyst_name = u.analyst_name
   and d.doc_ord_type = u.doc_ord_type
   and d.doc_no = u.doc_no
   and d.dm_date = u.dm_date
   and d.invoice_order = u.invoice_order
   and d.age = u.age
   and d.doc_entry_datetime = u.doc_entry_datetime
group by
    d.vend_no,
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    d.doc_ord_type,
    d.doc_no,
    d.dm_date,
    d.invoice_order,
    d.age,
    d.doc_entry_datetime
;

drop table if exists rds_ca1299_final_totals;
create local temporary table rds_ca1299_final_totals on commit preserve rows as
select
    sum(ifnull(f.ap_dm_60, 0)) AS sum_ap_dm_60,
    sum(ifnull(f.vcm_dm_60, 0)) AS sum_vcm_dm_60,
    sum(ifnull(f.total_dm_60, 0)) AS sum_total_dm_60,
    sum(ifnull(f.ap_dm_all, 0)) AS sum_ap_dm_all,
    sum(ifnull(f.vcm_dm_all, 0)) AS sum_vcm_dm_all,
    sum(ifnull(f.total_dm_all, 0)) AS sum_total_dm_all
from rds_ca1299_final f
;

drop table if exists rds_ca1299_sec1_vendors;
create local temporary table rds_ca1299_sec1_vendors on commit preserve rows as
select
    max(f.analyst_name) AS analyst_name,
    f.vend_no,
    max(f.vend_name) AS vend_name,
    max(f.discontinued) AS discontinued,
    max(f.ap_hold_flag) AS ap_hold_flag,
    f.old_comp,
    max(f.terms_desc) AS terms_desc,
    max(f.vend_currency) AS vend_currency,
    max(f.pas_code) AS pas_code,
    max(f.dm_flag) AS dm_flag,
    max(f.dnd_flag) AS dnd_flag,
    max(f.ap_dm_60) AS ap_dm_60,
    max(f.vcm_dm_60) AS vcm_dm_60,
    max(f.total_dm_60) AS total_dm_60
from rds_ca1299_final f
where f.total_dm_60 <> 0
group by
    f.vend_no,
    f.old_comp
;

drop table if exists rds_ca1299_t1;
create local temporary table rds_ca1299_t1 on commit preserve rows as
select
    'Total:' AS name,
    sum(ifnull(v.ap_dm_60, 0)) AS ap_dm_60,
    sum(ifnull(v.vcm_dm_60, 0)) AS vcm_dm_60,
    sum(ifnull(v.total_dm_60, 0)) AS total_dm_60
from rds_ca1299_sec1_vendors v
;

drop table if exists rds_ca1299_t4;
create local temporary table rds_ca1299_t4 on commit preserve rows as
select
    d.analyst_name,
    sum(ifnull(case when d.doc_ord_type in ('16', '17', '19') then d.cdn_amt else 0 end, 0)) AS dm_amt,
    sum(ifnull(case when d.doc_ord_type in ('3', '5', '6', '12') then d.cdn_amt else 0 end, 0)) AS v_returns,
    sum(ifnull(case when d.doc_ord_type in ('25') then d.cdn_amt else 0 end, 0)) AS ap_ar_offset,
    sum(ifnull(case when d.doc_ord_type in ('2', '125', '126') then d.cdn_amt else 0 end, 0)) AS cons_cloud_bill,
    sum(ifnull(case when d.doc_ord_type in ('22', '362', '363') then d.cdn_amt else 0 end, 0)) AS expense,
    sum(ifnull(case when d.doc_ord_type not in ('16', '17', '19', '3', '5', '6', '12', '25', '2', '125', '126', '22', '362', '363', '4', '8', '9', '15', '18', '21', '27') then d.cdn_amt else 0 end, 0)) AS other,
    sum(ifnull(case when d.doc_ord_type in ('4', '8', '9', '15', '18', '21', '27') then d.cdn_amt else 0 end, 0)) AS vcm
from rds_ca1299_detail_sum_final d
group by
    d.analyst_name
;

drop table if exists rds_ca1299_t5;
create local temporary table rds_ca1299_t5 on commit preserve rows as
select
    'Total:' AS name,
    sum(ifnull(case when d.doc_ord_type in ('16', '17', '19') then d.cdn_amt else 0 end, 0)) AS dm_amt,
    sum(ifnull(case when d.doc_ord_type in ('3', '5', '6', '12') then d.cdn_amt else 0 end, 0)) AS v_returns,
    sum(ifnull(case when d.doc_ord_type in ('25') then d.cdn_amt else 0 end, 0)) AS ap_ar_offset,
    sum(ifnull(case when d.doc_ord_type in ('2', '125', '126') then d.cdn_amt else 0 end, 0)) AS cons_cloud_bill,
    sum(ifnull(case when d.doc_ord_type in ('22', '362', '363') then d.cdn_amt else 0 end, 0)) AS expense,
    sum(ifnull(case when d.doc_ord_type not in ('16', '17', '19', '3', '5', '6', '12', '25', '2', '125', '126', '22', '362', '363', '4', '8', '9', '15', '18', '21', '27') then d.cdn_amt else 0 end, 0)) AS other,
    sum(ifnull(case when d.doc_ord_type in ('4', '8', '9', '15', '18', '21', '27') then d.cdn_amt else 0 end, 0)) AS vcm
from rds_ca1299_detail_sum_final d
;

drop table if exists rds_ca1299_t6;
create local temporary table rds_ca1299_t6 on commit preserve rows as
select
    f.analyst_name,
    sum(ifnull(f.ap_dm_60, 0)) AS ap_dm_60,
    sum(ifnull(f.vcm_dm_60, 0)) AS vcm_dm_60,
    sum(ifnull(f.total_dm_60, 0)) AS total_dm_60
from rds_ca1299_final f
where f.total_dm_60 <> 0
group by
    f.analyst_name
;

drop table if exists rds_ca1299_t7;
create local temporary table rds_ca1299_t7 on commit preserve rows as
select
    'Total:' AS name,
    sum(ifnull(f.ap_dm_60, 0)) AS ap_dm_60,
    sum(ifnull(f.vcm_dm_60, 0)) AS vcm_dm_60,
    sum(ifnull(f.total_dm_60, 0)) AS total_dm_60
from rds_ca1299_final f
where f.total_dm_60 <> 0
;

drop table if exists rds_ca1299_sec3_pivot;
create local temporary table rds_ca1299_sec3_pivot on commit preserve rows as
select
    t4.analyst_name,
    t4.dm_amt,
    t4.v_returns,
    t4.ap_ar_offset,
    t4.cons_cloud_bill,
    t4.expense,
    t4.other,
    t4.vcm,
    t6.ap_dm_60,
    t6.vcm_dm_60,
    t6.total_dm_60
from rds_ca1299_t4 t4
inner join rds_ca1299_t6 t6
    on t4.analyst_name = t6.analyst_name
;

drop table if exists rds_ca1299_recap;
create local temporary table rds_ca1299_recap on commit preserve rows as
select
    1 AS id,
    'Total Debits over 60 days' AS s1,
    sum(ifnull(f.ap_dm_60, 0)) AS ap_amt,
    sum(ifnull(f.vcm_dm_60, 0)) AS vcm_amt,
    sum(ifnull(f.total_dm_60, 0)) AS total_amt,
    sum(ifnull(f.total_dm_60, 0)) AS pct_base
from rds_ca1299_final f
union all
select
    2 AS id,
    'Total outstanding Debits' AS s1,
    sum(ifnull(f.ap_dm_all, 0)) AS ap_amt,
    sum(ifnull(f.vcm_dm_all, 0)) AS vcm_amt,
    sum(ifnull(f.total_dm_all, 0)) AS total_amt,
    sum(ifnull(f.total_dm_all, 0)) AS pct_base
from rds_ca1299_final f
union all
select
    3 AS id,
    'Percent of Debits Over 60 days Vs Total Debits' AS s1,
    cast(null AS numeric(20, 8)) AS ap_amt,
    cast(null AS numeric(20, 8)) AS vcm_amt,
    cast(null AS numeric(20, 8)) AS total_amt,
    cast(null AS numeric(20, 8)) AS pct_base
;

drop table if exists rds_ca1299_audit_pick;
create local temporary table rds_ca1299_audit_pick on commit preserve rows as
select
    d.doc_no,
    d.vend_no
from rds_ca1299_detail_sum_final d
where d.cdn_amt = (
    select max(m.cdn_amt)
    from rds_ca1299_detail_sum_final m
)
order by
    d.vend_name,
    d.vend_no,
    d.doc_ord_type,
    d.dm_date + 1,
    d.invoice_order
limit 1
;

drop table if exists rds_ca1299_detail_audit_stats;
create local temporary table rds_ca1299_detail_audit_stats on commit preserve rows as
select
    count(*) AS rds_cnt,
    sum(ifnull(d.cdn_amt, 0)) AS rds_cdn
from rds_ca1299_detail_sum_final d
;

drop table if exists rds_ca1299_detail_audit_stats_it;
create local temporary table rds_ca1299_detail_audit_stats_it on commit preserve rows as
select
    count(*) AS it_cnt,
    sum(ifnull(d.cdn_amt, 0)) AS it_cdn
from rds_ca1299_detail_sum_audit d
;

drop table if exists rds_ca1299_audit_pick_stats;
create local temporary table rds_ca1299_audit_pick_stats on commit preserve rows as
select
    sum(ifnull(d.usd_amt, 0)) AS rds_usd,
    sum(ifnull(d.cdn_amt, 0)) AS rds_cdn
from rds_ca1299_detail_sum_final d
inner join rds_ca1299_audit_pick p
    on d.doc_no = p.doc_no
   and d.vend_no = p.vend_no
;

drop table if exists rds_ca1299_audit_pick_stats_it;
create local temporary table rds_ca1299_audit_pick_stats_it on commit preserve rows as
select
    sum(ifnull(d.usd_amt, 0)) AS it_usd,
    sum(ifnull(d.cdn_amt, 0)) AS it_cdn
from rds_ca1299_detail_sum_audit d
inner join rds_ca1299_audit_pick p
    on d.doc_no = p.doc_no
   and d.vend_no = p.vend_no
;

drop table if exists rds_ca1299_tab1;
create local temporary table rds_ca1299_tab1 (
    id int,
    s1 varchar(100),
    s2 varchar(100),
    s3 varchar(100),
    s4 varchar(100),
    s5 varchar(100),
    s6 varchar(100),
    s7 varchar(100),
    s8 varchar(100),
    s9 varchar(100),
    s10 varchar(100),
    s11 varchar(100),
    s12 varchar(100),
    s13 varchar(100),
    s14 varchar(100),
    s15 varchar(100),
    s16 varchar(100),
    s17 varchar(100)
) on commit preserve rows
;

insert into rds_ca1299_tab1 (id, s1)
select 1, 'Aged Debits on Aging ' || to_char(current_date() - 1, 'MM/DD/YYYY')
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17)
select 2, 'Analyst', 'vend_no', 'vend_name', 'Disco', 'Pmt_Hold', 'Old Comp', 'Pmt_Terms', 'vend_curr', 'PAS', 'DM', 'DND', 'AP', 'AP%', 'VCM', 'VCM%', 'total_over_60', 'Total%'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17)
select
    3,
    v.analyst_name,
    cast(v.vend_no AS varchar(100)),
    v.vend_name,
    v.discontinued,
    v.ap_hold_flag,
    v.old_comp,
    v.terms_desc,
    v.vend_currency,
    v.pas_code,
    v.dm_flag,
    v.dnd_flag,
    '$' || to_char(round(ifnull(v.ap_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(v.ap_dm_60 * 100 / nullif(ft.sum_ap_dm_60, 0), 0), 2), 'FM999999990.00') || '%',
    '$' || to_char(round(ifnull(v.vcm_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(v.vcm_dm_60 * 100 / nullif(ft.sum_vcm_dm_60, 0), 0), 2), 'FM999999990.00') || '%',
    '$' || to_char(round(ifnull(v.total_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(v.total_dm_60 * 100 / nullif(ft.sum_total_dm_60, 0), 0), 2), 'FM999999990.00') || '%'
from rds_ca1299_sec1_vendors v
cross join rds_ca1299_final_totals ft
;

insert into rds_ca1299_tab1 (id, s2, s12, s13, s14, s15, s16, s17)
select
    4,
    t.name,
    '$' || to_char(round(ifnull(t.ap_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(t.ap_dm_60 * 100 / nullif(t.total_dm_60, 0), 0), 2), 'FM999999990.00') || '%',
    '$' || to_char(round(ifnull(t.vcm_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(t.vcm_dm_60 * 100 / nullif(t.total_dm_60, 0), 0), 2), 'FM999999990.00') || '%',
    '$' || to_char(round(ifnull(t.total_dm_60, 0), 4), 'FM999999999999990.0000'),
    '100.00%'
from rds_ca1299_t1 t
;

insert into rds_ca1299_tab1 (id, s1)
select 5, 'detail'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12)
select 6, 'analyst_name', 'Vend_No', 'Vend_Name', 'vend_curr', 'doc/ord_type', 'Doc No', 'DM_date', 'Invoice No/Order No', 'age', 'Doc Entry Date', 'Usd_amt', 'Cdn_amt'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12)
select
    7,
    d.analyst_name,
    cast(d.vend_no AS varchar(100)),
    d.vend_name,
    d.vend_curr,
    cast(d.doc_ord_type AS varchar(100)),
    cast(d.doc_no AS varchar(100)),
    to_char(d.dm_date, 'MM/DD/YYYY'),
    cast(d.invoice_order AS varchar(100)),
    cast(d.age AS varchar(100)),
    to_char(d.doc_entry_datetime, 'MM/DD/YYYY'),
    '$' || to_char(round(ifnull(d.usd_amt, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(d.cdn_amt, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_detail_sum_final d
;

insert into rds_ca1299_tab1 (id, s1)
select 8, ''
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15)
select 9, 'analyst_name', 'DM', 'V RETURNS', 'AP/AR OFFSET', 'CONS/CLOUD BILL', 'EXPENSE', 'OTHER', 'VCM', 'analyst_name', 'AP', 'AP%', 'VCM', 'VCM%', 'total_over_60', 'Total%'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s8)
select 10, 'Ord/Doc Type', 'DT-16,19,17', 'OT-3,12 & DT-5,6', 'DT-25', 'OT-2,125, 126', 'OT-362, 363 & DT-22', 'OT-27 & DT-4,8,9,11,15,18,21'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15)
select
    11,
    p.analyst_name,
    '$' || to_char(round(ifnull(p.dm_amt, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(p.v_returns, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(p.ap_ar_offset, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(p.cons_cloud_bill, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(p.expense, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(p.other, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(p.vcm, 0), 4), 'FM999999999999990.0000'),
    p.analyst_name,
    '$' || to_char(round(ifnull(p.ap_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(p.ap_dm_60 * 100 / nullif(ft.sum_ap_dm_60, 0), 0), 2), 'FM999999990.00') || '%',
    '$' || to_char(round(ifnull(p.vcm_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(p.vcm_dm_60 * 100 / nullif(ft.sum_vcm_dm_60, 0), 0), 2), 'FM999999990.00') || '%',
    '$' || to_char(round(ifnull(p.total_dm_60, 0), 4), 'FM999999999999990.0000'),
    to_char(round(ifnull(p.total_dm_60 * 100 / nullif(ft.sum_total_dm_60, 0), 0), 2), 'FM999999990.00') || '%'
from rds_ca1299_sec3_pivot p
cross join rds_ca1299_final_totals ft
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15)
select
    12,
    t5.name,
    '$' || to_char(round(ifnull(t5.dm_amt, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(t5.v_returns, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(t5.ap_ar_offset, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(t5.cons_cloud_bill, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(t5.expense, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(t5.other, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(t5.vcm, 0), 4), 'FM999999999999990.0000'),
    t7.name,
    '$' || to_char(round(ifnull(t7.ap_dm_60, 0), 4), 'FM999999999999990.0000'),
    '100.00%',
    '$' || to_char(round(ifnull(t7.vcm_dm_60, 0), 4), 'FM999999999999990.0000'),
    '100.00%',
    '$' || to_char(round(ifnull(t7.total_dm_60, 0), 4), 'FM999999999999990.0000'),
    '100.00%'
from rds_ca1299_t5 t5
cross join rds_ca1299_t7 t7
;

insert into rds_ca1299_tab1 (id, s1)
select 13, ''
;

insert into rds_ca1299_tab1 (id, s10, s11, s12, s13, s14, s15)
select 14, 'AP', 'AP%', 'VCM', 'VCM%', 'total_over_60', 'Total%'
;

insert into rds_ca1299_tab1 (id, s1, s10, s11, s12, s13, s14, s15)
select
    15,
    r.s1,
    case when r.id = 3 then null else '$' || to_char(round(ifnull(r.ap_amt, 0), 4), 'FM999999999999990.0000') end,
    case
        when r.id = 1 then to_char(round(ifnull(r.ap_amt * 100 / nullif(r.pct_base, 0), 0), 2), 'FM999999990.00') || '%'
        when r.id = 2 then to_char(round(ifnull(r.ap_amt * 100 / nullif(r.pct_base, 0), 0), 2), 'FM999999990.00') || '%'
        else to_char(round(ifnull(ft.sum_ap_dm_60 * 100 / nullif(ft.sum_ap_dm_all, 0), 0), 2), 'FM999999990.00') || '%'
    end,
    case when r.id = 3 then null else '$' || to_char(round(ifnull(r.vcm_amt, 0), 4), 'FM999999999999990.0000') end,
    case
        when r.id = 1 then to_char(round(ifnull(r.vcm_amt * 100 / nullif(r.pct_base, 0), 0), 2), 'FM999999990.00') || '%'
        when r.id = 2 then to_char(round(ifnull(r.vcm_amt * 100 / nullif(r.pct_base, 0), 0), 2), 'FM999999990.00') || '%'
        else to_char(round(ifnull(ft.sum_vcm_dm_60 * 100 / nullif(ft.sum_vcm_dm_all, 0), 0), 2), 'FM999999990.00') || '%'
    end,
    case when r.id = 3 then null else '$' || to_char(round(ifnull(r.total_amt, 0), 4), 'FM999999999999990.0000') end,
    case
        when r.id = 1 then to_char(round(ifnull(r.total_amt * 100 / nullif(r.pct_base, 0), 0), 2), 'FM999999990.00') || '%'
        when r.id = 2 then to_char(round(ifnull(r.total_amt * 100 / nullif(r.pct_base, 0), 0), 2), 'FM999999990.00') || '%'
        else to_char(round(ifnull(ft.sum_total_dm_60 * 100 / nullif(ft.sum_total_dm_all, 0), 0), 2), 'FM999999990.00') || '%'
    end
from rds_ca1299_recap r
cross join rds_ca1299_final_totals ft
;

insert into rds_ca1299_tab1 (id, s1)
select 16, null
;

insert into rds_ca1299_tab1 (id, s1)
select 17, 'Audit COMPLETENESS Testing(Detail)'
;

insert into rds_ca1299_tab1 (id, s2, s3, s4)
select 18, 'Original RDS Report Data', 'IT Extracted Summary/Completeness Query Result ', 'Reconciliation'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4)
select 19, 'Field', 'Amount', 'Amount', 'Difference in Amount'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4)
select
    20,
    'Record Count',
    cast(r.rds_cnt AS varchar(100)),
    cast(i.it_cnt AS varchar(100)),
    cast(r.rds_cnt - i.it_cnt AS varchar(100))
from rds_ca1299_detail_audit_stats r
cross join rds_ca1299_detail_audit_stats_it i
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4)
select
    21,
    'Total Cdn_amt',
    '$' || to_char(round(ifnull(r.rds_cdn, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(i.it_cdn, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(r.rds_cdn - i.it_cdn, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_detail_audit_stats r
cross join rds_ca1299_detail_audit_stats_it i
;

insert into rds_ca1299_tab1 (id, s1)
select 22, null
;

insert into rds_ca1299_tab1 (id, s1)
select 23, 'Audit ACCURACY Testing(Detail )'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13)
select 24, 'Source', 'Vend_No', 'Vend_Name', 'vend_curr', 'analyst_name', 'doc/ord_type', 'Doc No', 'DM_date', 'Invoice No/Order No', 'age', 'Doc Entry Date', 'Usd_amt', 'Cdn_amt'
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13)
select
    25,
    'RDS report',
    cast(d.vend_no AS varchar(100)),
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    cast(d.doc_ord_type AS varchar(100)),
    cast(d.doc_no AS varchar(100)),
    to_char(d.dm_date, 'MM/DD/YYYY'),
    cast(d.invoice_order AS varchar(100)),
    cast(d.age AS varchar(100)),
    to_char(d.doc_entry_datetime, 'MM/DD/YYYY'),
    '$' || to_char(round(ifnull(d.usd_amt, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(d.cdn_amt, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_detail_sum_final d
inner join rds_ca1299_audit_pick p
    on d.doc_no = p.doc_no
   and d.vend_no = p.vend_no
;

insert into rds_ca1299_tab1 (id, s1, s12, s13)
select
    26,
    'total',
    '$' || to_char(round(ifnull(s.rds_usd, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(s.rds_cdn, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_audit_pick_stats s
;

insert into rds_ca1299_tab1 (id, s1)
select 27, null
;

insert into rds_ca1299_tab1 (id, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13)
select
    28,
    'IT Extracted from Accuracy Query',
    cast(d.vend_no AS varchar(100)),
    d.vend_name,
    d.vend_curr,
    d.analyst_name,
    cast(d.doc_ord_type AS varchar(100)),
    cast(d.doc_no AS varchar(100)),
    to_char(d.dm_date, 'MM/DD/YYYY'),
    cast(d.invoice_order AS varchar(100)),
    cast(d.age AS varchar(100)),
    to_char(d.doc_entry_datetime, 'MM/DD/YYYY'),
    '$' || to_char(round(ifnull(d.usd_amt, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(d.cdn_amt, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_detail_sum_audit d
inner join rds_ca1299_audit_pick p
    on d.doc_no = p.doc_no
   and d.vend_no = p.vend_no
;

insert into rds_ca1299_tab1 (id, s1, s12, s13)
select
    29,
    'total',
    '$' || to_char(round(ifnull(s.it_usd, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(s.it_cdn, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_audit_pick_stats_it s
;

insert into rds_ca1299_tab1 (id, s1)
select 30, null
;

insert into rds_ca1299_tab1 (id, s1, s12, s13)
select
    31,
    'difference',
    '$' || to_char(round(ifnull(r.rds_usd - i.it_usd, 0), 4), 'FM999999999999990.0000'),
    '$' || to_char(round(ifnull(r.rds_cdn - i.it_cdn, 0), 4), 'FM999999999999990.0000')
from rds_ca1299_audit_pick_stats r
cross join rds_ca1299_audit_pick_stats_it i
;

drop table if exists rds_ca1299_tab2;
create local temporary table rds_ca1299_tab2 (
    id int,
    audit_notes varchar(200)
) on commit preserve rows
;

insert into rds_ca1299_tab2 (id, audit_notes)
select 1, 'This report extracts data based on below criteria'
;

insert into rds_ca1299_tab2 (id, audit_notes)
select 2, 'entry_id = 0'
;

insert into rds_ca1299_tab2 (id, audit_notes)
select 3, 'total_dm over 60 days <> 0'
;

insert into rds_ca1299_tab2 (id, audit_notes)
select 4, 'View of category: Debit'
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_ca1299_tab1
;

drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as
select *
from rds_ca1299_tab2
;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
sheet_index int,
sheet_name varchar(50),
title_active varchar(1),
date_pattern varchar(50)
);
insert into rdsetl.rds_tmp_sheet_config select 1,'Report data',null,null;
insert into rdsetl.rds_tmp_sheet_config select 2,'Notes for Synnex Audit',null,null;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select
    1 AS flag,
    'standard' AS body_type,
    count(*) AS cnt
from rdsetl.rds_tmp
;
insert into rdsetl.rds_tmp_body (flag, body_type, cnt)
select
    2 AS flag,
    'standard' AS body_type,
    count(*) AS cnt
from rdsetl.rds_tmp_2
;
