drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists table_us_scm_reference_17482;
create local temporary table table_us_scm_reference_17482 on commit preserve rows as
with sales_hierarchy
as (
    select distinct
         s.sales_terr
    from dim_us.dim_pub_sales_hierarchy_by_terr_user_role s
    inner join dim_us.dim_pub_manager m
            on s.user_id = m.userid
    where m.loginid = 'sandra.macdonald'
    )
    ,pm_hierarchy
as (
    select distinct
         pm.vend_no
        ,pm.vpl_no
    from dim_us.dim_pub_pm_vpc_matrix pm
    inner join dim_us.dim_pub_manager m
            on pm.pm_id = m.userid
    where m.loginid = 'sandra.macdonald'
    )
    ,bd_hierarchy_c
as (
    select distinct
         b.cust_no
    from dim_us.dim_pub_bd_hierarchy a
    inner join dim_us.dim_disty_bd_project_cust b
            on a.project_no = b.project_no
           and a.task_no = b.task_no
    where a.loginid = 'sandra.macdonald'
      and a.project_no = -1
    )
    ,bd_hierarchy_v
as (
    select distinct b.sku_no
    from dim_us.dim_pub_bd_hierarchy a
    inner join dim_us.dim_disty_bd_project_sku b
            on a.project_no = b.project_no
    where a.loginid = 'sandra.macdonald'
      and a.project_no = -1
    )
    ,all_list
as (
    select row_number() over (
            order by fact.order_type
                ,fact.order_no
                ,fact.order_line_no
            ) as row_number
        ,fact.order_type
        ,fact.order_no
        ,fact.order_line_no
        ,- 1 as sub_line_no
        ,fact.prod_type
        ,fact.company_no
    from dw_us.dwd_disty_common_pos_di fact
    left join dim_us.dim_pub_part_info part
           on fact.sku_no = part.sku_no
    where 1 = 1
      and fact.order_line_type in ('Kit','Single')
      and fact.date_flag >= case when date_part('day',getdate()) = 5 then timestampadd(month, -1, cast(timestampadd(dd, 22-day(getdate()), getdate()) as date))
                                 when date_part('day',getdate()) = 22 then cast(timestampadd(dd, 5-day(getdate()), getdate()) as date)
                                 else current_date()+1
                             end
      and fact.date_flag < current_date()
      and fact.order_type not in (
            select distinct order_type
            from dim_us.dim_pub_order_type
            where ship_tran_no is null
            )
      and fact.vend_no in (95920,96273)
    )
    ,com_list
as (
    select
         al.row_number
        ,com.order_type
        ,com.order_no
        ,com.kit_line_no as order_line_no
        ,com.order_line_no as sub_line_no
    from all_list al
    inner join dw_us.dwd_disty_common_pos_di com
            on al.order_type = com.order_type
           and al.order_no = com.order_no
           and al.order_line_no = com.kit_line_no
    where al.prod_type in ('A','K')
    )
    ,final_order_list
as (
    select
         al.order_type
        ,al.order_no
        ,al.order_line_no
        ,al.sub_line_no
    from all_list al
    )
    ,final_data
as (
    select
         al.order_type
        ,al.order_no
        ,al.order_line_no
        ,al.sub_line_no
    from all_list al
    inner join final_order_list fol
            on al.order_type = fol.order_type
           and al.order_no = fol.order_no
           and al.order_line_no = fol.order_line_no
    )
select
     he.order_type
    ,he.order_no
    ,he.order_line_no
    ,he.exp_code
    ,he.claim_type
    ,he.scm_no as project_no
    ,he.unit_exp as scm_unit_exp
    ,he.extend_exp as extended_exp
    ,he.spa_no
    ,he.spa_ref_no
    ,he.vendor_appr_ref_no as pri_approv_ref_no
    ,row_number() over (
        partition by he.order_type
        ,he.order_no
        ,he.order_line_no order by he.spa_no
        ) scm_row
from final_data fd
inner join dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di he
        on fd.order_no = he.order_no
       and fd.order_type = he.order_type
       and fd.order_line_no = he.order_line_no
;

drop table if exists table_us_pos_17482;
create local temporary table table_us_pos_17482 on commit preserve rows as
with sales_hierarchy as (
        select distinct
             s.sales_terr
        from dim_us.dim_pub_sales_hierarchy_by_terr_user_role s
        inner join dim_us.dim_pub_manager m
                on s.user_id = m.userid
        where m.loginid = 'sandra.macdonald')
    ,pm_hierarchy as (
        select distinct
             pm.vend_no
            ,pm.vpl_no
        from dim_us.dim_pub_pm_vpc_matrix pm
        inner join dim_us.dim_pub_manager m
                on pm.pm_id = m.userid
        where m.loginid = 'sandra.macdonald'
        )
    ,bd_hierarchy_c as (
        select distinct
             b.cust_no
        from dim_us.dim_pub_bd_hierarchy a
        inner join dim_us.dim_disty_bd_project_cust b
                on a.project_no = b.project_no
               and a.task_no = b.task_no
        where a.loginid = 'sandra.macdonald'
          and a.project_no = - 1
        )
    ,bd_hierarchy_v as (
        select distinct
             b.sku_no
        from dim_us.dim_pub_bd_hierarchy a
        inner join dim_us.dim_disty_bd_project_sku b
                on a.project_no = b.project_no
        where a.loginid = 'sandra.macdonald'
          and a.project_no = -1
        )
    ,all_vpg as (
        select distinct
             b.vpl_no
            ,a.vpc_group_id || '-' || a.vpc_group_desc as vpc_group_desc
        from dim_us.dim_pub_vpc_group_xref_view b
        inner join dim_us.dim_pub_vpc_group_view a
                on b.vpc_group_id = a.vpc_group_id
        where a.group_code = 'BRPT'
          and a.active = 'Y'
          and a.vpc_group_desc is not null
        )
    ,all_list as (
        select row_number() over (
                order by fact.order_no
                    ,fact.order_type
                    ,fact.order_line_no
                ) as row_number
            ,fact.order_type
            ,fact.order_no
            ,fact.order_line_no
            ,-1 as sub_line_no
            ,fact.ship_date
            ,fact.ship_qty
            ,-1 as sub_qty
            ,fact.part_no as part_no_ori
            ,'-1' as sub_part
            ,fact.sku_no
            ,-1 as sub_sku
            ,fact.unit_price
            ,fact.extend_price
            ,fact.unit_sum_exp as unit_exp
            ,fact.extend_sum_exp as extend_exp
            ,fact.unit_net_price
            ,fact.extend_net_price
            ,fact.vend_name
            ,fact.bill_to_cust_no
            ,fact.ngm_amt as NGM_amt
            ,fact.big_deal_no
            ,fact.eu_company_name as company_name
            ,fact.auth_no as auth_id
            ,fact.prod_type
            ,'S' as sub_prod
            ,fact.vend_no
            ,fact.date_flag
            ,case
                when fact.extend_net_price = 0
                    then 0
                else fact.ngm_amt / fact.extend_net_price
                end as ngm_percent
        from dw_us.dwd_disty_common_pos_di fact
        inner join dim_us.dim_pub_part_info part
                on fact.sku_no = part.sku_no
        inner join dim_us.dim_pub_customer_info cust
                on fact.bill_to_cust_no = cust.cust_no
        left join dim_us.dim_pub_sku_profile_extend sku_profile
               on fact.sku_no = sku_profile.sku_no
        where 1 = 1
          and fact.company_no in (1)
          and fact.order_line_type in ('Kit','Single')
          and fact.date_flag >= case when date_part('day',getdate()) = 5 then timestampadd(month, -1, cast(timestampadd(dd, 22-day(getdate()), getdate()) as date))
                                     when date_part('day',getdate()) = 22 then cast(timestampadd(dd, 5-day(getdate()), getdate()) as date)
                                     else current_date()+1
                                end
          and fact.date_flag< current_date()
          and fact.order_type not in (
                select distinct order_type
                from dim_us.dim_pub_order_type
                where ship_tran_no is null
                )
          and fact.vend_no in (95920,96273)
        )
    ,com_list as (
        select
             al.row_number
            ,com.order_type
            ,com.order_no
            ,com.kit_line_no as order_line_no
            ,com.order_line_no as sub_line_no
            ,al.ship_date
            ,com.ship_qty
            ,com.ship_qty as sub_qty
            ,al.part_no_ori
            ,com.part_no as sub_part
            ,al.sku_no
            ,com.sku_no as sub_sku
            ,com.unit_price
            ,com.extend_price
            ,com.unit_sum_exp as unit_exp
            ,com.extend_sum_exp as extend_exp
            ,com.unit_net_price
            ,com.extend_net_price as extend_net_price
            ,com.vend_name
            ,com.bill_to_cust_no
            ,com.ngm_amt as NGM_amt
            ,com.big_deal_no
            ,com.eu_company_name as company_name
            ,com.auth_no as auth_id
            ,al.prod_type
            ,'S' as sub_prod
            ,com.vend_no
            ,com.date_flag
            ,case
                when com.extend_net_price = 0
                    then 0
                else com.ngm_amt / com.extend_net_price
                end as ngm_percent
        from all_list al
        inner join dw_us.dwd_disty_common_pos_di com
                on al.order_type = com.order_type
               and al.order_no = com.order_no
               and al.order_line_no = com.kit_line_no
               and com.company_no in (1)
        left join dim_us.dim_pub_part_info part
               on com.sku_no = part.sku_no
        left join dim_us.dim_pub_sku_profile_extend sku_profile
               on com.sku_no = sku_profile.sku_no
        where al.prod_type in ('A','K')
        )
    ,final_order_list as (
        select
             al.order_type
            ,al.order_no
            ,al.order_line_no
            ,al.sub_line_no
            ,al.extend_net_price
            ,al.prod_type
            ,al.ship_qty
            ,(
                select max(row_number)
                from all_list
                ) + 0 as max_row
            ,(
                select sum(ship_qty)
                from all_list
                ) as total_qty
        from all_list al
        )
    ,contract_list as (
        select
             order_type
            ,order_no
            ,order_line_no
            ,contract_no as cmt_contract_no
        from dw_us.dwd_stellr_billing_history_di
        where order_type = 125
        )
    ,recalculate_exp as (
        select
             al.order_type
            ,al.order_no
            ,al.order_line_no
            ,sum(scm.unit_exp) as unit_exp
            ,sum(scm.extend_exp) as extend_exp
        from all_list al
        inner join dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di scm
                on al.order_type = scm.order_type
               and al.order_no = scm.order_no
               and al.order_line_no = scm.order_line_no
        where 1 = 1
        group by al.order_type
            ,al.order_no
            ,al.order_line_no

        union all

        select al.order_type
            ,al.order_no
            ,al.sub_line_no as order_line_no
            ,sum(scm.unit_exp) as unit_exp
            ,sum(scm.extend_exp) as extend_exp
        from com_list al
        inner join dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di scm
                on al.order_type = scm.order_type
               and al.order_no = scm.order_no
               and al.sub_line_no = scm.order_line_no
        where 1 = 1
        group by al.order_type
            ,al.order_no
            ,al.sub_line_no
        )
    ,final_data as (
        select
             fol.max_row
            ,fol.total_qty
            ,al.row_number
            ,al.order_type
            ,al.order_no
            ,al.order_line_no
            ,al.sub_line_no
            ,al.ship_date
            ,al.ship_qty
            ,al.sub_qty
            ,al.part_no_ori
            ,null as sub_part
            ,al.sku_no
            ,null as sub_sku
            ,al.unit_price
            ,al.extend_price
            ,case
                when re.order_line_no is null
                    then 0
                else re.Unit_Exp
                end as Unit_Exp
            ,case
                when re.order_line_no is null
                    then 0
                else re.extend_exp
                end as extend_exp
            ,al.unit_net_price
            ,al.extend_net_price
            ,al.vend_name
            ,al.bill_to_cust_no
            ,case
                when al.prod_type = 'A'
                    or al.prod_type = 'K'
                    then rc.ngm_amt
                else al.ngm_amt
                end as NGM_amt
            ,al.big_deal_no
            ,al.company_name
            ,al.auth_id
            ,al.prod_type
            ,null as sub_prod
            ,al.vend_no
            ,al.date_flag
            ,case
                when al.prod_type = 'A'
                    or al.prod_type = 'K'
                    then rc.ngm_percent
                else al.ngm_percent
                end as ngm_percent
        from all_list al
        inner join final_order_list fol
                on al.order_type = fol.order_type
               and al.order_no = fol.order_no
               and al.order_line_no = fol.order_line_no
        left join dm_us.dm_disty_pos_order_kit_di rc
               on al.order_type = rc.order_type
              and al.order_no = rc.order_no
              and al.order_line_no = rc.order_line_no
        left join recalculate_exp re
               on al.order_type = re.order_type
              and al.order_no = re.order_no
              and al.order_line_no = re.order_line_no
        )
    ,final_ser_order_list as (
        select order_type
            ,order_no
            ,order_line_no
            ,ship_qty
            ,prod_type
        from final_data
        where 1 = 2
        )
    ,ser_number_list as (
        select fd.order_type as ser_order_type
            ,fd.order_no as ser_order_no
            ,fd.order_line_no as ser_order_line_no
            ,ser.ser_no
            ,case
                when fd.ship_qty > 0
                    then 1
                when fd.ship_qty < 0
                    then - 1
                else 0
                end as ser_qty
            ,case
                when fd.ship_qty > 0
                    then - 1
                when fd.ship_qty < 0
                    then 1
                else 0
                end as neg_qty
            ,ser.asset_tag
            ,ser.mac_address
            ,ser.imei_no
            ,ser.iccid_no
        from final_ser_order_list fd
        inner join dw_us.dwd_disty_common_order_serial_no_di ser
                on fd.order_type = ser.order_type
               and fd.order_no = ser.order_no
               and fd.order_line_no = ser.order_line_no
        where 1 = 1
        )
    ,final_ser_list as (
        select snl.ser_order_type
            ,snl.ser_order_no
            ,snl.ser_order_line_no
            ,snl.ser_no
            ,snl.ser_qty
            ,snl.neg_qty
            ,snl.asset_tag
            ,snl.mac_address
            ,snl.imei_no
            ,snl.iccid_no
        from ser_number_list snl

        union all

        select b.order_type
            ,b.order_no
            ,b.order_line_no
            ,null
            ,b.ship_qty - p.ser_qty
            ,0
            ,null
            ,null
            ,null
            ,null
        from final_ser_order_list b
        inner join (
            select ser_order_type
                ,ser_order_no
                ,ser_order_line_no
                ,sum(ser_qty) as ser_qty
            from ser_number_list
            group by ser_order_type
                ,ser_order_no
                ,ser_order_line_no
            ) p on b.order_type = p.ser_order_type
            and b.order_no = p.ser_order_no
            and b.order_line_no = p.ser_order_line_no
        where p.ser_qty <> 0
          and abs(b.ship_qty) <> abs(p.ser_qty)
        )
select
     fd.order_no
    ,fd.order_type
    ,fd.order_line_no
    ,to_date(to_char(fd.ship_date, 'MM/DD/YYYY'), 'MM/DD/YYYY') as Ship_Date
    ,fd.sku_no
    ,fd.part_no_ori as part_no
    ,fd.prod_type
    ,fd.ship_qty as Ship_Qty
    ,fd.unit_price as Unit_Price
    ,fd.extend_price as Extend_Price
    ,fd.Unit_Exp
    ,fd.Extend_Exp
    ,fd.unit_net_price as Net_Price
    ,fd.extend_net_price as Extend_Net_Price
    ,fd.vend_no
    ,fd.vend_name as Vend_Name
    ,fd.bill_to_cust_no
    ,fd.NGM_amt
    ,fd.ngm_percent as 'NGM%'
    ,fd.big_deal_no
    ,fd.company_name as 'EU Company Name'
    ,fd.auth_id
from final_data fd
order by fd.row_number
    ,fd.order_no
    ,fd.order_type
    ,fd.order_line_no
    ,fd.sub_line_no
;


drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select
  a.*,
  b.exp_code,
  b.claim_type,
  b.project_no,
  b.scm_unit_exp,
  b.extended_exp,
  b.spa_no,
  b.spa_ref_no,
  b.pri_approv_ref_no
from table_us_pos_17482 a
left join table_us_scm_reference_17482 b
       on a.order_no = b.order_no
      and a.order_type = b.order_type
      and a.order_line_no = b.order_line_no
--where a.order_no = 160228614
order by a.order_no, a.order_type, a.order_line_no
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

drop table if exists table_us_scm_reference_17482;
drop table if exists table_us_pos_17482;
