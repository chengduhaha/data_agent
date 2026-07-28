drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists rds_9751_po;
create local temporary table rds_9751_po on commit preserve rows as
select order_no,
       sku_no,
       part_no,
       vend_no,
       rtrim(ltrim(vpl_code)) || '--' || rtrim(ltrim(vpl_desc)) as vend_name,
       to_char(entry_datetime,'MM/DD/YYYY HH24:MI:SS') as entry_datetime,
       to_char(closed_date,'MM/DD/YYYY HH24:MI:SS') as closed_date,
       total_cost,
       a_amount as amount,
       currency_type,
       pay_method,
       po_confirmation as confirmation,
       entry_id,
       entry_name,
       internal_comments
  from dw_us.dwd_disty_common_po_basic
 where prod_code = 6900
   and closed_date >= case when date_part('day',current_date()) = 1 then cast(trunc(add_months(current_date(), -1), 'month') as date) else cast(current_date()-7 as date) end
   and closed_date < current_date()
;

create table rdsetl.rds_tmp as
select *
from rds_9751_po
;

create table rdsetl.rds_tmp_body as
select 'standard' as body_type
    ,0 as acct_no
    ,count(*) as cnt
from rdsetl.rds_tmp
;