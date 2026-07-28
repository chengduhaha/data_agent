DROP TABLE IF EXISTS inv_qty_sum_12980;
create table inv_qty_sum_12980 as
select sku_no
    ,inv_type
    ,sum(on_hand_qty) as on_hand_ttl
    ,sum(on_order_qty) as on_order_ttl
    ,sum(alloc_qty) as allocated_stock
from ods_us.ods_cis_corp_inv_qty_rt
where inv_type in (1,2,3,4,7,32,33,37,40,68,100,200,300)
group by sku_no,inv_type
;

DROP TABLE IF EXISTS inv_qty_all_12980;
create table inv_qty_all_12980 as
select s.sku_no
    ,v.vend_no
    ,v.vend_name
    ,p.mfg_partno
    ,s.dg_code
    ,p.short_desc
    ,p.long_desc
    ,p.usage_type
    ,p.abc_code
    ,p.active_status
    ,a.vpl_code
    ,p.entry_datetime
    ,p.group_id
    ,b.family_id
    ,c.cat_desc as family_desc
    ,b.cat_id
    ,d.cat_desc
    ,b.subcat_id
    ,e.cat_desc as subcat_desc
    ,i.inv_type
    ,f.inv_type_descr
    ,i.on_hand_ttl
    ,i.on_order_ttl
    ,i.allocated_stock
    ,p.part_no
    ,row_number() over(order by s.sku_no) as id
from ods_us.ods_cis_corp_sku_extension_rt s
inner join inv_qty_sum_12980 i
on s.sku_no = i.sku_no
inner join ods_us.ods_cis_corp_part_master_rt p
on s.sku_no = p.sku_no
inner join ods_us.ods_cis_corp_vend_master_rt v
on p.vend_no = v.vend_no
left join ods_us.ods_cis_corp_dw_vend_pl_rt a
on p.vpl_no = a.vpl_no
left join ods_us.ods_cis_corp_part_cat_rt b
on p.group_id = b.group_id
left join ods_us.ods_cis_corp_pco_cat_id_rt c
on b.family_id = c.cat_id
left join ods_us.ods_cis_corp_pco_cat_id_rt d
on b.cat_id = d.cat_id
left join ods_us.ods_cis_corp_pco_cat_id_rt e
on b.subcat_id = e.cat_id
left join ods_us.ods_cis_corp_inv_type_rt f
on i.inv_type = f.inv_type
where p.active_status = 'A'
and p.avail_to_sell = 'Y'
and (s.dg_code in ('HAZRV','HAZDS','HAZLG','HAZOB','HAZIT')
     or s.dg_code is null)
;

delete from inv_qty_all_12980 where on_hand_ttl = 0 and on_order_ttl = 0
;

DROP TABLE IF EXISTS rds_tmp;
create table rds_tmp as
select *
from inv_qty_all_12980
where id<=150000
;

DROP TABLE IF EXISTS rds_tmp_2;
create table rds_tmp_2 as
select *
from inv_qty_all_12980
where id>150000 and id<=300000
;

DROP TABLE IF EXISTS rds_tmp_3;
create table rds_tmp_3 as
select *
from inv_qty_all_12980
where id>300000 and id<=450000
;

drop table if exists rds_tmp_body;
create table rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rds_tmp
;
insert into rds_tmp_body
select 2 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rds_tmp_2
;
insert into rds_tmp_body
select 3 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rds_tmp_3
;

-- 1
DROP TABLE IF EXISTS inv_qty_sum_12980;
DROP TABLE IF EXISTS inv_qty_all_12980;