drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists table_14893_cpo;
create local temporary table table_14893_cpo on commit preserve rows as 
select
 ch.cpo_id, ch.cpo_no
from ods_us.ods_cis_corp_order_header oh 
inner join dm_us.dm_disty_sales_open_cpo ch on oh.int_ref_no = ch.cpo_id and oh.int_ref_type in (1,8)
where oh.order_type in (1,8)
and oh.sales_terr in (4404 , 4405)
and oh.delete_date is null
union
select
 ch.cpo_id, ch.cpo_no
from ods_us.ods_cis_corp_order_header oh 
inner join dm_us.dm_disty_sales_close_cpo_di ch on oh.int_ref_no = ch.cpo_id and oh.int_ref_type in (1,8)
where oh.order_type in (1,8)
and oh.sales_terr in (4404 , 4405)
and oh.delete_date is null
;

create table rdsetl.rds_tmp as
select
  oh.order_no,
  oh.order_type,
  oh.entry_datetime,
  m1.firstname||' '||m1.lastname as Created_By,
  oh.sales_terr,
  oec.data_c as DPAS_Value,
  oec2.data_d as Quote_Expiration_Date,
  pm.part_no,
  pm.mfg_partno,
  od.sku_no,
  od.order_qty,
  pm.vend_no,
  pm.vend_name,
  oh.total_order,
  oh.expected_date,
  ch.cpo_no,
  pm1.sku_no as Kit_Parts,
  bom.bom_line_no as kit_line_no,
  bom.comp_no as comp_sku,
  pm2.part_no as comp_partno,
  pm2.mfg_partno as comp_mfgpart,
  null as VPO
from ods_us.ods_cis_corp_order_header oh
inner join ods_us.ods_cis_corp_order_detail od on oh.order_type = od.order_type and oh.order_no = od.order_no 
left join ods_us.ods_cis_corp_order_eu_custom oec on oh.order_type = oec.order_type and oh.order_no = oec.order_no  and oec.eu_map_id = 300 and oec.eu_map_line_no = 4
left join ods_us.ods_cis_corp_order_eu_custom oec2 on oh.order_type = oec2.order_type and oh.order_no = oec2.order_no  and oec2.eu_map_id = 300 and oec2.eu_map_line_no = 5
left join ods_us.ods_cis_corp_order_soldto os on os.order_type = oh.order_type and os.order_no = oh.order_no 
left join dim_us.dim_pub_manager m1 on m1.userid = oh.entry_id
left join dim_us.dim_pub_part_info pm on od.sku_no = pm.sku_no 
left join dim_us.dim_pub_part_info pm1 on od.sku_no = pm1.sku_no and pm1.prod_type = 'K'
left join ods_us.ods_cis_corp_bom bom on pm1.sku_no = bom.sku_no
left join dim_us.dim_pub_part_info pm2 on pm2.sku_no = bom.comp_no
left join table_14893_cpo ch on oh.int_ref_no = ch.cpo_id and oh.int_ref_type in (1,8)
where oh.order_type = 8
and oh.sales_terr in (4404 , 4405)
and oh.delete_date is null

union

select
  oh.order_no,
  oh.order_type,
  oh.entry_datetime,
  m1.firstname||' '||m1.lastname as Created_By,
  oh.sales_terr,
  oec.data_c as DPAS_Value,
  oec2.data_d as Quote_Expiration_Date,
  pm.part_no,
  pm.mfg_partno,
  od.sku_no,
  od.order_qty,
  pm.vend_no,
  pm.vend_name,
  oh.total_order,
  oh.expected_date,
  ch.cpo_no,
  pm1.sku_no as Kit_Parts,
  bom.bom_line_no as kit_line_no,
  bom.comp_no as comp_sku,
  pm2.part_no,
  pm2.mfg_partno,
  ohv.order_no as VPO
from ods_us.ods_cis_corp_order_header oh
join ods_us.ods_cis_corp_order_detail od on oh.order_type = od.order_type and oh.order_no = od.order_no 
left join ods_us.ods_cis_corp_order_eu_custom oec on oh.order_type = oec.order_type and oh.order_no = oec.order_no  and oec.eu_map_id = 300 and oec.eu_map_line_no = 4
left join ods_us.ods_cis_corp_order_eu_custom oec2 on oh.order_type = oec2.order_type and oh.order_no = oec2.order_no  and oec2.eu_map_id = 300 and oec2.eu_map_line_no = 5
left join ods_us.ods_cis_corp_order_soldto os on os.order_type = oh.order_type and os.order_no = oh.order_no 
left join dim_us.dim_pub_manager m1 on m1.userid = oh.entry_id
left join dim_us.dim_pub_part_info pm on od.sku_no = pm.sku_no 
left join dim_us.dim_pub_part_info pm1 on od.sku_no = pm1.sku_no and pm1.prod_type = 'K'
left join ods_us.ods_cis_corp_bom bom on pm1.sku_no = bom.sku_no
left join dim_us.dim_pub_part_info pm2 on pm2.sku_no = bom.comp_no
left join table_14893_cpo ch on oh.int_ref_no = ch.cpo_id and oh.int_ref_type in (1,8)
left join ods_us.ods_cis_corp_order_header ohv on oh.order_type = ohv.int_ref_type and oh.order_no = ohv.int_ref_no and ohv.order_type = 2 and ohv.delete_date is null 
where oh.order_type = 1
and oh.sales_terr in (4404, 4405)
and oh.from_loc_no = 98
and oh.delete_date is null
;

create table rdsetl.rds_tmp_body as 
select 'Standard' as body_type
	,0 as acct_no
	,count(*) as cnt
from rdsetl.rds_tmp
;
