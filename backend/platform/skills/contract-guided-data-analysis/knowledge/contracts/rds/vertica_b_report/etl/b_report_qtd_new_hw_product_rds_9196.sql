drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists tmp_ca_report_9196;
create local temporary table tmp_ca_report_9196 on commit preserve rows as
with fiscal_qtr as (
  select
    case
      when month(current_date()) = 12 then add_months(date_trunc('year', current_date()), 11)
      when month(current_date()) in (1, 2) then add_months(date_trunc('year', current_date()), -1)
      when month(current_date()) in (3, 4, 5) then add_months(date_trunc('year', current_date()), 2)
      when month(current_date()) in (6, 7, 8) then add_months(date_trunc('year', current_date()), 5)
      else add_months(date_trunc('year', current_date()), 8)
    end as fq_start
),

qtd_range as (
  select
    fq_start as qtd_start,
    add_months(fq_start, 3) as fq_end_exclusive,
    current_date() as qtd_end
  from fiscal_qtr
),

month_flag as (
  select distinct d.date_flag
  from dim_ca.dim_pub_date d
  cross join qtd_range q
  where d.date_flag between q.qtd_start and q.qtd_end
)

select
  pm.vend_name,
  fact.sku_no,
  case
    when pm.entry_datetime >= q.qtd_start and pm.entry_datetime < q.fq_end_exclusive
      then to_date(to_char(pm.entry_datetime, 'MM-DD-YYYY'), 'MM-DD-YYYY')
  end as new_part_create_date,
  pm.part_no,
  pm.short_desc,
  pm.long_desc,
  pm.vend_no,
  pm.vpl_no,
  pm.vpl_code,
  h.pm_name,
  pm.vpl_desc,
  fact.pm_code,
  sum(fact.net_sales) as total_net_sales,
  sum((ifnull(fact.sales_cost, fact.u_cost) + ifnull(fact.u_sum_expense, 0)) * fact.ship_qty) as total_net_cost,
  pm.group_id,
  pm.family,
  pm.category as cat,
  pm.sub_category as subcat,
  pm.global_cat_type as category_type,
  pm.asc606,
  pm.renewal_flag
from dw_ca.dwd_disty_common_dw_orders_pl_extend_di fact
inner join dim_ca.dim_pub_part_info pm on fact.sku_no = pm.sku_no
left join dim_ca.dim_pub_vpl_hierarchy_info h on pm.vpl_no = h.vpl_no
inner join month_flag m on fact.date_flag = m.date_flag
cross join qtd_range q
where fact.date_flag between q.qtd_start and q.qtd_end
  and fact.segment_exclude = 'N'
  and pm.global_cat_type in ('HW')
  and (pm.vend_name not like '%SYNNEX%' or pm.vend_name = 'SYNNEX WW VENDOR GROUP')
group by
  pm.vend_name,
  fact.sku_no,
  case
    when pm.entry_datetime >= q.qtd_start and pm.entry_datetime < q.fq_end_exclusive
      then to_date(to_char(pm.entry_datetime, 'MM-DD-YYYY'), 'MM-DD-YYYY')
  end,
  pm.part_no,
  pm.short_desc,
  pm.long_desc,
  pm.vend_no,
  pm.vpl_no,
  pm.vpl_code,
  h.pm_name,
  pm.group_id,
  pm.family,
  pm.category,
  pm.sub_category,
  pm.global_cat_type,
  pm.asc606,
  pm.renewal_flag,
  pm.vpl_desc,
  fact.pm_code
order by fact.sku_no
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from tmp_ca_report_9196
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
    ,'Standard' as body_type
    ,count(*) as cnt
from rdsetl.rds_tmp
;

drop table if exists tmp_ca_report_9196;
