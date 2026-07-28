drop table if exists temp_data_mx_1241;
create local temporary table temp_data_mx_1241 on commit preserve rows as
select
     sum(ocche.extended_exp) as scm
    ,dspc.claim_type
    ,dppct.descr
    ,ocche.order_no
    ,ocche.order_type
    ,ocche.order_line_no
    ,ocche.project_no
    ,occh.company_no
from ods_wcla.ods_cis_corp_history_exp ocche
inner join ods_wcla.ods_cis_corp_history_header occh
    on occh.order_no = ocche.order_no
    and occh.order_type = ocche.order_type
left join (
    select distinct claim_type
        ,project_no
    from dw_wcla.dwd_disty_scm_pm_claim
) dspc on ocche.project_no = dspc.project_no
left join dim_wcla.dim_pub_pm_claim_type dppct
    on dspc.claim_type = dppct.claim_type
where ocche.delete_date is null
    and ocche.order_line_no is not null
    and ocche.project_no is not null
group by
     dspc.claim_type
    ,dppct.descr
    ,ocche.order_no
    ,ocche.order_type
    ,ocche.order_line_no
    ,ocche.project_no
    ,occh.company_no
;

drop table if exists rds_mx1241_report;
create local temporary table rds_mx1241_report on commit preserve rows as
select
     dcsd.company_no
    ,hst.reseller_cust_no
    ,ch.cust_name as reseller_cust_name
    ,coalesce(
        (
        select avg((1 - cpo_unit_cost / cpo_unit_price))
        from dw_wcla.dwd_disty_sales_open_cpo_detail_extend cd
        where cd.cpo_id = hd.int_ref_no
            and cd.cpo_sku_no = pl.sku_no
            and cpo_unit_price > 0
        ),
        0) * 100 as quote_margin
    ,case scm.claim_type
        when 31 then scm.scm
        else 0
     end as POS_Rebate_SCM
    ,case scm.claim_type
        when 59 then scm.scm
        else 0
     end as Back_Commission
    ,case scm.claim_type
        when 5001 then scm.scm
        else 0
     end as Vendor_Rebate
    ,case scm.claim_type
        when 5002 then scm.scm
        else 0
     end as Marketing_Rebate
    ,case
        when scm.claim_type not in (5002, 5001, 31, 59) then scm.scm
        else 0
     end as Others_SCM
    ,case
        when c.cust_acct_type = 'EU' then 'Y'
        else 'N'
     end as bill_end_user
    ,dv.division_desc as salesdivision
    ,ch.resale_no
    ,pl.date_flag
    ,pl.order_type
    ,pl.order_no
    ,pl.order_line_no
    ,pl.cust_no
    ,pl.mcust_no
    ,c.cust_name
    ,pl.cust_terr
    ,sht.terr_name
    ,pl.sales_rep
    ,pl.sku_no
    ,pl.prod_code
    ,pl.vend_no
    ,dpvi.vend_name
    ,dpvi.universal_vend_name
    ,pl.from_loc_no
    ,pl.inv_type
    ,pl.ship_qty
    ,pl.u_price
    ,pl.u_cost
    ,dcsd.spec_cost
    ,pl.u_sum_expense
    ,pl.terms
    ,pl.cust_segment
    ,pl.cust_exclude
    ,pl.part_segment
    ,pl.btl
    ,pl.btl_sales
    ,pl.cust_rebate
    ,pl.frt_out_exp
    ,pl.whoh_pack
    ,pl.inv_cost
    ,pl.inv_reserve
    ,pl.ap_finance
    ,pl.cust_pmt_disc
    ,pl.cust_finance
    ,pl.cr_risk_cterm
    ,pl.scm_cost
    ,pl.scm_risk
    ,pl.rma
    ,pl.infrastructure
    ,pl.cust_type
    ,pl.one_time_btl
    ,pl.marketing
    ,pl.hc_pm
    ,pl.hc_sales
    ,pl.cvr_rm
    ,pl.pm_code
    ,pl.oplgm_amt
    ,pl.ngm_amt
    ,pl.csc_amt
    ,pl.ppc_amt
    ,pl.gv_user_type
    ,pl.sales_cost
    ,pl.hbtl
    ,pl.hc_bd
    ,pl.scm_profit_adj
    ,pl.corporate
    ,pl.base_cost
    ,pl.cust_finance_sales
    ,pl.u_sum_expense as unit_exp
    ,(pl.u_sum_expense * pl.ship_qty) as extended_exp
    ,case
        when pl.order_type = 125
            or cloudprofile.order_no is not null then 'Cloud'
        else 'Other'
     end as cloud
    ,coalesce(legacyinvoiceno.profile_c, (cast(pl.order_type as varchar) || '-' || cast(pl.order_no as varchar))) as invoicenumber
    ,scm.claim_type
from dw_wcla.dwd_disty_common_dw_orders_pl_extend_di pl
left join dw_wcla.dwd_disty_common_sales_detail_di dcsd
    on dcsd.order_no = pl.order_no
    and dcsd.order_type = pl.order_type
    and dcsd.order_line_no = pl.order_line_no
left join dim_wcla.dim_pub_sales_hierarchy_primary_role_by_terr_view sht
    on pl.cust_terr = sht.sales_terr
left join dim_wcla.dim_pub_sales_cust_type cty
    on sht.cust_type = cty.cust_type
left join dim_wcla.dim_pub_sales_division dv
    on cty.division = dv.division
left outer join ods_wcla.ods_cis_corp_history_profile cloudprofile
    on pl.order_type = cloudprofile.order_type
    and pl.order_no = cloudprofile.order_no
    and cloudprofile.profile_type = 'ACQCLOUD'
    and cloudprofile.active = 'Y'
left outer join ods_wcla.ods_cis_corp_history_profile legacyinvoiceno
    on pl.order_type = legacyinvoiceno.order_type
    and pl.order_no = legacyinvoiceno.order_no
    and legacyinvoiceno.profile_type = 'ACQINVNO'
    and legacyinvoiceno.active = 'Y'
left join ods_wcla.ods_cis_corp_history_header hd
    on hd.order_type = pl.order_type
    and hd.order_no = pl.order_no
left join dim_wcla.dim_pub_customer_info c
    on hd.to_acct_no = c.cust_no
left outer join ods_wcla.ods_cis_corp_history_soldto hst
    on hst.order_no = pl.order_no
    and hst.order_type = pl.order_type
left outer join dim_wcla.dim_pub_customer_info ch
    on ch.cust_no = hst.reseller_cust_no
left join dim_wcla.dim_pub_vendor_info dpvi
    on pl.vend_no = dpvi.vend_no
left join temp_data_mx_1241 scm
    on pl.order_no = scm.order_no
    and pl.order_type = scm.order_type
    and pl.order_line_no = scm.order_line_no
where pl.date_flag > ADD_MONTHS(CURRENT_TIMESTAMP, -2)
    and pl.order_type > 0
    and dcsd.company_no = 428
    and pl.order_type in (1, 11, 14, 16, 20, 101, 114, 125, 127, 128)
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_mx1241_report
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;
-- 1
