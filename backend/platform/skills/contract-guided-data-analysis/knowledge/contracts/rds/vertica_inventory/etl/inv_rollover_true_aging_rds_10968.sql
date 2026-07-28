set time zone='America/Los_Angeles';

drop table if exists report_us10968;
create local temporary table report_us10968 on commit preserve rows as
select
    b.date_flag as date_flag
    ,b.vend_no as vend_no
    ,cast(null as varchar(60)) as vend_name
    ,b.vpl_no as vpl_no
    ,cast(null as varchar(60)) as vpc_code
    ,sum(ifnull(b.rollover, 0) * ifnull(b.ave_cost, 0)) as all_rollover_amount_240_up
    ,sum(case when b.inv_type = 2 then ifnull(b.rollover, 0) * ifnull(b.ave_cost, 0) else 0 end) as type_2_rollover_240_up
    ,cast(null as numeric(19, 4)) as all_true_240_up
    ,cast(null as numeric(19, 4)) as all_aging_360_up
    ,cast(null as varchar(60)) as us_buyer
    ,cast(null as varchar(60)) as us_buyer_email
    ,cast(null as varchar(60)) as us_buyer_manager
    ,cast(null as varchar(60)) as us_buyer_manager_email
    ,cast(null as varchar(60)) as us_buyer_director
    ,cast(null as varchar(60)) as us_buyer_director_email
    ,cast(null as varchar(60)) as pm
    ,cast(null as varchar(60)) as pm_email
    ,cast(null as varchar(60)) as pm_manager
    ,cast(null as varchar(60)) as pm_manager_email
    ,cast(null as varchar(600)) as additional_pm
    ,cast(null as varchar(600)) as additional_pm_email
    ,cast(null as varchar(60)) as pm_director
    ,cast(null as varchar(60)) as pm_director_email
    ,cast(null as varchar(60)) as pm_vp
    ,cast(null as varchar(60)) as pm_vp_email
    ,cast(null as varchar(60)) as vcm
    ,cast(null as numeric(19, 4)) as total_oh_amt
from dw_us.dwd_disty_inv_aging_rollover_rtv2_df b
where b.date_flag = current_date() - 1
    and b.report_type = 240
    and b.inv_type in (1, 2, 300)
group by
    b.date_flag
    ,b.vend_no
    ,b.vpl_no
;

drop table if exists aging_us10968;
create local temporary table aging_us10968 on commit preserve rows as
select
    b.date_flag as date_flag
    ,c.vend_no as vend_no
    ,c.vpl_no as vpl_no
    ,sum(
        ifnull(b.age241_270, 0) + ifnull(b.age271_300, 0) + ifnull(b.age301_330, 0) + ifnull(b.age331_360, 0)
    ) as amt_241_360
    ,sum(ifnull(b.age360_up, 0)) as amt_360_up
from dw_us.dwd_disty_inv_aging_df b
inner join dim_us.dim_pub_part_info c
    on b.sku_no = c.sku_no
where b.view_level = 'IT_PART'
    and b.date_flag = current_date() - 1
    and b.inv_type in (1, 2, 300)
group by
    b.date_flag
    ,c.vend_no
    ,c.vpl_no
;

drop table if exists true_aging_us10968;
create local temporary table true_aging_us10968 on commit preserve rows as
select
    b.date_flag as date_flag
    ,c.vend_no as vend_no
    ,c.vpl_no as vpl_no
    ,sum(ifnull(b.true_age360, 0)) as true_360_up
from dw_us.dwd_disty_inv_true_aging_df b
inner join dim_us.dim_pub_part_info c
    on b.sku_no = c.sku_no
where b.date_flag = current_date() - 1
    and b.inv_type in (1, 2, 300)
group by
    b.date_flag
    ,c.vend_no
    ,c.vpl_no
;

drop table if exists metrics_upd_us10968;
create local temporary table metrics_upd_us10968 on commit preserve rows as
select
    k.date_flag as date_flag
    ,k.vend_no as vend_no
    ,k.vpl_no as vpl_no
    ,coalesce(ag.amt_241_360, 0) + coalesce(ta.true_360_up, 0) as all_true_240_up
    ,ta.true_360_up as all_aging_360_up
from report_us10968 k
left outer join aging_us10968 ag
    on ag.date_flag = k.date_flag
    and ag.vend_no = k.vend_no
    and ag.vpl_no = k.vpl_no
left outer join true_aging_us10968 ta
    on ta.date_flag = k.date_flag
    and ta.vend_no = k.vend_no
    and ta.vpl_no = k.vpl_no
;

update report_us10968 a
set
    all_true_240_up = m.all_true_240_up
    ,all_aging_360_up = m.all_aging_360_up
from metrics_upd_us10968 m
where a.date_flag = m.date_flag
    and a.vend_no = m.vend_no
    and a.vpl_no = m.vpl_no
;

update report_us10968 a
set vend_name = b.vend_name
from dim_us.dim_pub_vendor_info b
where a.vend_no = b.vend_no
;

update report_us10968 a
set vpc_code = b.vpl_code
from dim_us.dim_pub_vpl_info b
where a.vpl_no = b.vpl_no
;

delete from report_us10968
where vpc_code in ('NONSTOCK', 'nonstock', 'APT', 'APT-CIS')
;

update report_us10968 a
set
    us_buyer = trim(c.firstname) || ' ' || trim(c.lastname)
    ,us_buyer_email = e.email
    ,us_buyer_manager = trim(d.firstname) || ' ' || trim(d.lastname)
    ,us_buyer_manager_email = f.email
from dim_us.dim_pub_vend_user_matrix b
inner join dim_us.dim_pub_manager c
    on b.primary_id = c.userid
inner join dim_us.dim_pub_manager d
    on b.manager_id = d.userid
inner join dim_us.dim_pub_manager e
    on b.primary_id = e.userid
inner join dim_us.dim_pub_manager f
    on b.manager_id = f.userid
where a.vend_no = b.vend_no
    and b.vpl_no = -1
    and b.profile_type = 'BUYR'
;

update report_us10968 a
set
    us_buyer_director = trim(c.firstname) || ' ' || trim(c.lastname)
    ,us_buyer_director_email = e.email
from dim_us.dim_pub_vend_user_matrix b
inner join dim_us.dim_pub_manager c
    on b.other_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.other_id = e.userid
where a.vend_no = b.vend_no
    and b.vpl_no = -1
    and b.profile_type = 'BUYR'
;

update report_us10968 a
set
    us_buyer = trim(c.firstname) || ' ' || trim(c.lastname)
    ,us_buyer_email = e.email
    ,us_buyer_manager = trim(d.firstname) || ' ' || trim(d.lastname)
    ,us_buyer_manager_email = f.email
from dim_us.dim_pub_vend_user_matrix b
inner join dim_us.dim_pub_manager c
    on b.primary_id = c.userid
inner join dim_us.dim_pub_manager d
    on b.manager_id = d.userid
inner join dim_us.dim_pub_manager e
    on b.primary_id = e.userid
inner join dim_us.dim_pub_manager f
    on b.manager_id = f.userid
where a.vend_no = b.vend_no
    and a.vpl_no = b.vpl_no
    and b.profile_type = 'BUYR'
;

update report_us10968 a
set
    us_buyer_director = trim(c.firstname) || ' ' || trim(c.lastname)
    ,us_buyer_director_email = e.email
from dim_us.dim_pub_vend_user_matrix b
inner join dim_us.dim_pub_manager c
    on b.other_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.other_id = e.userid
where a.vend_no = b.vend_no
    and a.vpl_no = b.vpl_no
    and b.profile_type = 'BUYR'
;

update report_us10968 a
set
    pm = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_email = d.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager d
    on b.pm_id = d.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'PM'
    and b.vpl_no = -1
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_email = d.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager d
    on b.pm_id = d.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'PM'
    and a.vpl_no = b.vpl_no
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm_manager = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_manager_email = f.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager f
    on b.pm_id = f.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'MGR'
    and b.vpl_no = -1
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm_manager = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_manager_email = f.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager f
    on b.pm_id = f.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'MGR'
    and a.vpl_no = b.vpl_no
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm_director = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_director_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'DIR'
    and b.vpl_no = -1
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm_director = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_director_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'DIR'
    and a.vpl_no = b.vpl_no
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm_vp = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_vp_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'VP'
    and b.vpl_no = -1
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

update report_us10968 a
set
    pm_vp = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_vp_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and b.pm_role = 'VP'
    and a.vpl_no = b.vpl_no
    and b.is_primary = 'Y'
    and b.is_backup <> 'Y'
;

-- Additional PM / backup PM: Sybase builds from pm_vpc_matrix and row-wise concat
-- Vertica uses listagg (max_length raised, on_overflow TRUNCATE) then substr to 600 to match column width and avoid default 1024-byte listagg limit.
drop table if exists add_pm_rows_us10968;
create local temporary table add_pm_rows_us10968 on commit preserve rows as
select distinct
    b.vend_no as vend_no
    ,b.vpl_no as vpl_no
    ,b.pm_id as pm_id
    ,trim(ifnull(m.firstname, '')) || ' ' || trim(ifnull(m.lastname, '')) as pm_display_name
    ,trim(ifnull(ec.email, '')) as pm_email_addr
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager m
    on b.pm_id = m.userid
left join dim_us.dim_pub_manager ec
    on b.pm_id = ec.userid
where b.pm_role = 'PM'
    and b.is_primary = 'N'
    and b.is_backup = 'N'
;

drop table if exists add_pm_agg_us10968;
create local temporary table add_pm_agg_us10968 on commit preserve rows as
select
    r.vend_no as vend_no
    ,r.vpl_no as vpl_no
    ,cast(
        substr(
            listagg(p.pm_display_name using parameters separator = '*', max_length = 8192, on_overflow = 'TRUNCATE')
            , 1
            , 600
        ) as varchar(600)
    ) as additional_pm
    ,cast(
        substr(
            listagg(p.pm_email_addr using parameters separator = '*', max_length = 8192, on_overflow = 'TRUNCATE')
            , 1
            , 600
        ) as varchar(600)
    ) as additional_pm_email
from report_us10968 r
inner join add_pm_rows_us10968 p
    on r.vend_no = p.vend_no
    and r.vpl_no = p.vpl_no
group by
    r.vend_no
    ,r.vpl_no
;

update report_us10968 a
set
    additional_pm = g.additional_pm
    ,additional_pm_email = g.additional_pm_email
from add_pm_agg_us10968 g
where a.vend_no = g.vend_no
    and a.vpl_no = g.vpl_no
;

update report_us10968 a
set
    pm_director = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_director_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and b.vpl_no = -1
    and b.pm_role = 'DIR'
    and b.is_primary = 'Y'
    and b.is_backup = 'N'
    and b.vend_discontinued = 'N'
    and b.vend_restricted = 'N'
;

update report_us10968 a
set
    pm_director = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_director_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and a.vpl_no = b.vpl_no
    and b.pm_role = 'DIR'
    and b.is_primary = 'Y'
    and b.is_backup = 'N'
    and b.vend_discontinued = 'N'
    and b.vend_restricted = 'N'
;

update report_us10968 a
set
    pm_vp = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_vp_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and b.vpl_no = -1
    and b.pm_role = 'VP'
    and b.is_primary = 'Y'
    and b.is_backup = 'N'
    and b.vend_discontinued = 'N'
    and b.vend_restricted = 'N'
;

update report_us10968 a
set
    pm_vp = trim(c.firstname) || ' ' || trim(c.lastname)
    ,pm_vp_email = e.email
from dim_us.dim_disty_v_pm_vpc_matrix_view b
inner join dim_us.dim_pub_manager c
    on b.pm_id = c.userid
inner join dim_us.dim_pub_manager e
    on b.pm_id = e.userid
where a.vend_no = b.vend_no
    and a.vpl_no = b.vpl_no
    and b.pm_role = 'VP'
    and b.is_primary = 'Y'
    and b.is_backup = 'N'
    and b.vend_discontinued = 'N'
    and b.vend_restricted = 'N'
;

update report_us10968 a
set vcm = trim(c.firstname) || ' ' || trim(c.lastname)
from dim_us.dim_pub_vend_user_matrix b
inner join dim_us.dim_pub_manager c
    on b.primary_id = c.userid
where a.vend_no = b.vend_no
    and b.vpl_no = -1
    and b.profile_type = 'VCM'
;

update report_us10968 a
set vcm = trim(c.firstname) || ' ' || trim(c.lastname)
from dim_us.dim_pub_vend_user_matrix b
inner join dim_us.dim_pub_manager c
    on b.primary_id = c.userid
where a.vend_no = b.vend_no
    and a.vpl_no = b.vpl_no
    and b.profile_type = 'VCM'
;

drop table if exists report_us10968_vend;
create local temporary table report_us10968_vend on commit preserve rows as
select distinct
    b.vend_no as vend_no
    ,b.sku_no as sku_no
from dw_us.dwd_disty_inv_aging_rollover_rtv2_df b
where b.date_flag = current_date() - 1
    and b.report_type = 240
    and b.inv_type in (1, 2, 300)
;

drop table if exists sku_oh_us10968;
create local temporary table sku_oh_us10968 on commit preserve rows as
select
    c.vend_no as vend_no
    ,c.vpl_no as vpl_no
    ,sum(ifnull(b.on_hand_qty, 0) * ifnull(c.ave_cost, 0)) as total_oh_amt
from report_us10968_vend a
inner join dim_us.dim_pub_part_info c
    on a.vend_no = c.vend_no
    and a.sku_no = c.sku_no
inner join dw_us.dwd_disty_inv_qty_df b
    on b.sku_no = c.sku_no
    and b.inv_type in (1, 2)
    and b.date_flag = current_date() - 1
group by
    c.vend_no
    ,c.vpl_no
;

update report_us10968 a
set total_oh_amt = b.total_oh_amt
from sku_oh_us10968 b
where b.vend_no = a.vend_no
    and b.vpl_no = a.vpl_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select distinct
    to_char(a.date_flag, 'mm/dd/yyyy') as date_flag
    ,a.vend_no as vend_no
    ,a.vend_name as vend_name
    ,a.vpc_code as vpc_code
    ,a.total_oh_amt as 'Total OH Amount'
    ,a.all_rollover_amount_240_up as 'All_rollover_amount_240_up'
    ,a.type_2_rollover_240_up as 'Type_2_rollover_240_up'
    ,a.all_true_240_up as 'All_True_240_up'
    ,a.all_aging_360_up as 'All_Aging_360_up'
    ,l.terms as terms
    ,replace(
        replace(
            replace(
                replace(
                    replace(ifnull(b.terms_desc, ''), chr(9), '')
                    , chr(10), '')
                , chr(13), '')
            , chr(160), '')
        , chr(34), '') as terms_desc
    ,a.us_buyer as 'US_buyer'
    ,a.us_buyer_email as 'US_buyer_email'
    ,a.us_buyer_manager as 'US_buyer_manager'
    ,a.us_buyer_manager_email as 'US_buyer_manager_email'
    ,a.us_buyer_director as 'US_buyer_director'
    ,a.us_buyer_director_email as 'US_buyer_director_email'
    ,a.pm as 'PM'
    ,a.pm_email as 'PM_email'
    ,a.pm_manager as 'PM_manager'
    ,a.pm_manager_email as 'PM_manager_email'
    ,a.additional_pm as 'Additional_PM'
    ,a.additional_pm_email as 'Additional_PM_email'
    ,a.pm_director as 'PM_director'
    ,a.pm_director_email as 'PM_director_email'
    ,a.pm_vp as 'PM_VP'
    ,a.pm_vp_email as 'PM_VP_email'
    ,a.vcm as 'VCM'
from report_us10968 a
inner join dim_us.dim_pub_vendor_info v
    on v.vend_no = a.vend_no
inner join dim_us.dim_pub_vend_location_view l
    on l.vend_no = v.vend_no
    and l.loc_no = v.primary_loc
inner join dim_us.dim_pub_terms_file_view b
    on l.terms = b.doc_terms
where ifnull(b.active, 'Y') = 'Y'
    and b.usage = 'P'
;


drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select
    1 as flag
    ,'standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;
-- 2