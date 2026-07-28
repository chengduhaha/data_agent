set time_zone = 'America/Los_Angeles';

drop table if exists tempdb.rds_staging_sku_cpo_17362;
create table tempdb.rds_staging_sku_cpo_17362 as
select distinct ch.cpo_id,
       ch.reseller_cust_no as cpo_sold_to,
       ss.part_no,
       ss.sku_no,
       ss.short_desc,
       ss.vend_no,
       cd.cis_unit_cost as base_cost_cpo,
       cp.profile_f as list_price_cpo
  from ods_us.ods_cis_corp_cpo_header_rt ch
 inner join ods_us.ods_cis_corp_cpo_detail_rt cd
    on ch.cpo_id = cd.cpo_id
 inner join ods_us.ods_part_mymdm_sku_staging_rt ss
    on cd.cpo_sku_no = ss.sku_no
   and ss.vend_no in (73779, 72030)
   and ss.status = 'STAGING'
  left join ods_us.ods_cis_corp_cpo_profile_rt cp
    on cd.cpo_id = cp.cpo_id
   and cd.cpo_line_seq = cp.cpo_line_seq
   and cp.profile_type = 'CUSTMSRP'
   and cp.active = 'Y'
;

drop table if exists tempdb.rds_quote_expire_date_17362;
create table tempdb.rds_quote_expire_date_17362 as
select distinct a.cpo_id,
       eu.data_d as quote_expire_date
  from tempdb.rds_staging_sku_cpo_17362 a
 inner join ods_us.ods_cis_corp_cpo_eu_custom_rt eu
    on a.cpo_id = eu.cpo_id
 inner join ods_us.ods_cis_corp_eu_custom_map_rt eumap
    on eu.eu_map_id = eumap.eu_map_id
   and eu.eu_map_line_no = eumap.eu_map_line_no
   and eu.data_d is not null
   and eu.delete_date is null
 inner join ods_us.ods_cis_corp_list_box_detail_rt lbd
    on eumap.map_data_desc = lbd.code_value
   and lbd.list_box_code = 'CEDM'
   and lbd.code_desc in ('Quote Expire Date')
;

drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select a.cpo_id as 'PO ID',
       a.cpo_sold_to as 'Sold To',
       a.part_no as 'Part#',
       a.sku_no as 'SKU#',
       a.short_desc as 'Description',
       a.vend_no as 'Vendor#',
       a.base_cost_cpo as 'Base Cost',
       a.list_price_cpo as 'List Price',
       b.quote_expire_date as 'Quote Expire Date'
  from tempdb.rds_staging_sku_cpo_17362 a
  left join tempdb.rds_quote_expire_date_17362 b
    on a.cpo_id = b.cpo_id
;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as 
select  1 as flag,
        'standard' as body_type,
        count(*) as cnt
  from tempdb.rds_tmp
;