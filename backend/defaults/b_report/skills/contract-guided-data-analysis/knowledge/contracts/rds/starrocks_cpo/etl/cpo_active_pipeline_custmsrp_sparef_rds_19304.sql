drop table if exists tempdb.rds_us_cpo_tmp_19304;
create table tempdb.rds_us_cpo_tmp_19304 as
select distinct a.cpo_id,
       a.cpo_no,
       b.cpo_line_no,	
       a.cpo_cust_no,
       d.cust_name,
       c.part_no,
       c.short_desc,
       c.prod_type,
       b.cpo_unit_price,
       b.cpo_unit_cost,
       b.cpo_unit_cost * b.cpo_so_qty as extended_price_quoted,
       c.vpl_no,
       e.vpl_code,
       c.vend_no,
       a.cpo_sales_terr,
       f.terr_name,
       case when a.cpo_ship_loc_type = 'EU' then a.ship_name1 else null end as end_user_name,
       g.close_date,
       concat(g.probability, '-', ifnull(g.quote_stage, 'Not Pipelined')) as quote_stage,
       concat(h.firstname, ' ', h.lastname) as Primary_Rep,
       a.cpo_total_notax,
       a.cpo_entry_datetime,
       ct.cust_type_descr as customer_type,
       b.cpo_sku_no,
       b.cpo_line_seq,
       (b.cpo_line_qty - b.cpo_del_qty) as quoted_qty
  from ods_us.ods_cis_corp_cpo_header_rt a
 inner join ods_us.ods_cis_corp_cpo_detail_rt b
    on a.cpo_id = b.cpo_id
   and b.cpo_delete_datetime is null
 inner join ods_us.ods_cis_corp_part_master_rt c
    on b.cpo_sku_no = c.sku_no
  left join ods_us.ods_cis_corp_customer_header_rt d
    on a.cpo_cust_no = d.cust_no
 inner join ods_us.ods_cis_corp_dw_vend_pl_rt e
    on c.vpl_no = e.vpl_no
   and e.vpl_code in ('Apstra Intent-based System', 'QFX Series Switches')
  left join ods_us.ods_cis_corp_territory_rt f
    on a.cpo_sales_terr = f.sales_terr
  left join ods_us.ods_cis_corp_cust_type_rt ct
    on f.cust_type = ct.cust_type
  left join ods_us.ods_snx_crm_mycrm_pipeline_header_rt g
    on a.cpo_id = g.cpo_id
  left join ods_us.ods_cis_corp_manager_rt h
    on f.primary_id = h.userid
 where a.cpo_delete_datetime is null
   and a.cpo_status in ('QUOTESHEET', 'QUOTEPO', 'ALOCQTYERR', 'CONVERTOK', 'EFPRERR', 'EUACCTERR', 'EUINFOCHCK', 'EUSUBMIT',
                        'HOLDPO', 'MAXPOAMT', 'MULTIFIX', 'NOCPOPAF', 'OKACPOPMAX', 'OKCOMMENTS', 'OKNOACPOP', 'OKOLDGRID',
                        'OKSKUSTOP', 'OLV2QUOTE', 'POCHANGE', 'POLINEQC', 'READYAF', 'SHIPCUTOFF', 'SHIPMETHOD', 'SHIPTOFIX', 'TERMSFIX')
   and a.cpo_entry_datetime >= DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -12 MONTH)
   and a.cpo_entry_datetime < current_date()
;

drop table if exists tempdb.rds_us_cpo_custmsrp_tmp_19304_part1;
create table tempdb.rds_us_cpo_custmsrp_tmp_19304_part1 as
with temporary_table_p1 as (
select distinct cpo_id from tempdb.rds_us_cpo_tmp_19304 
where cpo_entry_datetime >= DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -12 MONTH)
and cpo_entry_datetime < DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -6 MONTH)
)
select a.cpo_id, c.cpo_line_seq,
       c.profile_f
  from temporary_table_p1 a
  inner join ods_us.ods_cis_corp_cpo_profile_rt c
    on a.cpo_id = c.cpo_id
   and c.profile_cat = 'CPOL'
   and c.profile_type = 'CUSTMSRP'
 group by a.cpo_id
; 

drop table if exists tempdb.rds_us_cpo_custmsrp_tmp_19304_part2;
create table tempdb.rds_us_cpo_custmsrp_tmp_19304_part2 as
with temporary_table_p2 as (
select distinct cpo_id from tempdb.rds_us_cpo_tmp_19304 
where cpo_entry_datetime >= DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -6 MONTH)
)
select a.cpo_id,c.cpo_line_seq,
       c.profile_f
  from temporary_table_p2 a
  inner join ods_us.ods_cis_corp_cpo_profile_rt c
    on a.cpo_id = c.cpo_id
   and c.profile_cat = 'CPOL'
   and c.profile_type = 'CUSTMSRP'
 group by a.cpo_id
; 

drop table if exists tempdb.rds_us_cpo_custmsrp_tmp_19304;
create table tempdb.rds_us_cpo_custmsrp_tmp_19304 as
select a.cpo_id, sum(b.profile_f * a.quoted_qty) as ext_list_price 
from tempdb.rds_us_cpo_tmp_19304 a
inner join tempdb.rds_us_cpo_custmsrp_tmp_19304_part1 b 
on a.cpo_id = b.cpo_id and a.cpo_line_seq = b.cpo_line_seq
group by a.cpo_id
union
select a.cpo_id, sum(b.profile_f * a.quoted_qty) as ext_list_price 
from tempdb.rds_us_cpo_tmp_19304 a
INNER  join tempdb.rds_us_cpo_custmsrp_tmp_19304_part2 b 
on a.cpo_id = b.cpo_id and a.cpo_line_seq = b.cpo_line_seq
group by a.cpo_id;

drop table if exists tempdb.rds_us_cpo_sparef_tmp_19304;
create table tempdb.rds_us_cpo_sparef_tmp_19304 as
with temporary_table_p3 as (
select distinct cpo_id from tempdb.rds_us_cpo_tmp_19304 
where cpo_entry_datetime >= DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -12 MONTH)
and cpo_entry_datetime < DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -6 MONTH)
)
select distinct a.cpo_id,
	c.profile_f as spa_ref_no
  from temporary_table_p3 a
  inner join ods_us.ods_cis_corp_cpo_profile_rt c
    on a.cpo_id = c.cpo_id
   and c.profile_cat = 'CPOH'
   and c.profile_type = 'SPAREF#'
;

insert into tempdb.rds_us_cpo_sparef_tmp_19304
with temporary_table_p4 as (
select distinct cpo_id from tempdb.rds_us_cpo_tmp_19304 
where cpo_entry_datetime >= DATE_ADD(DATE_FORMAT(current_date(), '%Y-%m-01'), INTERVAL -6 MONTH)
) 
select distinct a.cpo_id,
	c.profile_f as spa_ref_no
  from temporary_table_p4 a
  inner join ods_us.ods_cis_corp_cpo_profile_rt c
    on a.cpo_id = c.cpo_id
   and c.profile_cat = 'CPOH'
   and c.profile_type = 'SPAREF#'
; 

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select a.cpo_id,
       a.cpo_no,
       c.spa_ref_no as "SPA REF#",
       b.ext_list_price as "Ext List Price",
       a.cpo_total_notax as "N sales Total",
       a.cpo_line_no,
       DATE_FORMAT(a.cpo_entry_datetime, '%Y-%m-%d %H:%i:%s') as cpo_entry_datetime,
       a.cpo_sku_no,
       a.part_no,
       a.short_desc,
       a.prod_type,
       a.quoted_qty as "Quoted Quantity",
       a.cpo_unit_price,
       a.cpo_unit_cost,
       a.extended_price_quoted as 'Extended Price Quoted',
       a.cpo_cust_no,
       a.cust_name,
       a.vpl_no,
       a.vpl_code,
       a.vend_no,
       a.end_user_name as "End User Company Name",
       a.close_date,
       a.quote_stage,
       a.customer_type as cust_type,
       a.cpo_sales_terr,
       a.terr_name,
       a.Primary_Rep
  from tempdb.rds_us_cpo_tmp_19304 a
  left join tempdb.rds_us_cpo_custmsrp_tmp_19304 b
    on a.cpo_id = b.cpo_id
  left join tempdb.rds_us_cpo_sparef_tmp_19304 c
    on a.cpo_id = c.cpo_id
 order by a.cpo_id
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag,
       'Standard' as body_type,
       count(*) as cnt
  from tempdb.rds_tmp
;
