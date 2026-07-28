-- tab 1
drop table if exists table_us14943_cpo;
create local temporary table table_us14943_cpo on commit preserve rows as 
select a.cpo_id
	,a.cpo_line_no
	,a.cpo_entry_datetime
	,a.cpo_status
	,c.vend_no
	,c.vend_name
	,c.vpl_code
	,a.cpo_sku_no
	,c.short_desc
	,a.cpo_cust_no
	,d.mcust_no as mast_cust
	,a.reseller_cust_no
	,d.cust_name
	,d.sales_terr
	,d.sales_terr_name as terr_name
	,d.cust_type_descr as cust_type_desc
	,e.user_id
	,d.stop_mailing
	,e.source
	,a.cpo_from_ref_type as from_ref_type
	,c.abc_code
	,c.long_desc
	,c.mar_comment
	,'http://oneapiprod.synnex.com/image_technote/' as product_image_link
	,f.contact_no
from dim_us.dim_pub_part_info c
inner join dm_us.dm_disty_sales_open_cpo a
on c.sku_no=a.cpo_sku_no
inner join ods_us.ods_cis_corp_cpo_profile b
on a.cpo_id=b.cpo_id
and b.profile_type = 'EMAILQUOTE'
and b.active='Y'
inner join dim_us.dim_pub_customer_info d
on a.cpo_cust_no=d.cust_no
left join ods_us.ods_etl_ec_cart_current e
on a.cpo_cust_no=e.cust_no
and a.cpo_sku_no=e.sku_no
left join ods_us.ods_cis_corp_ec_user f
on e.user_id=f.user_id
and f.delete_date is null
where a.cpo_delete_datetime is null
and a.cpo_line_delete_datetime is null
and a.convert_datetime is null
and c.data_source='CIS'
and c.vend_no in (select vend_no from ods_gbl.ods_daas_mygbldaas_smb_vend_image_config where e_catalog_source ='GCC' and active = 'Y' and country_code = 'US')
and d.cust_type in (245, 137, 246, 247, 244, 231)
and a.cpo_entry_datetime>=current_date()-7
and a.cpo_entry_datetime<current_date()
-- and a.cpo_entry_datetime>='2023-08-28'
-- and a.cpo_entry_datetime<'2023-09-04'
;

drop table if exists table_us14943_add_addr;
create local temporary table table_us14943_add_addr on commit preserve rows as 
select a.*
	,g.contact_name
	,g.title
	,g.phone_no
	,g.state
	,g.stop_call
	,g.email_address
	,g.stop_email
	,row_number() over(partition by a.cpo_id,a.cpo_line_no order by g.addr_no desc) as rn
from table_us14943_cpo a
left join dim_us.dim_pub_customer_address_contacts_info g
on a.contact_no=g.contact_no
;

drop table if exists table_us14943_add_order_info;
create local temporary table table_us14943_add_order_info on commit preserve rows as 
select a.cpo_id
	,b.order_no
	,b.order_type
	,b.entry_datetime
from table_us14943_cpo a
inner join ods_us.ods_cis_corp_order_header b
on a.cpo_id = b.int_ref_no
and b.order_type <> 2
;

insert into table_us14943_add_order_info
select a.cpo_id
	,b.order_no
	,b.order_type
	,b.entry_datetime
from table_us14943_cpo a
inner join ods_us.ods_cis_corp_history_header b
on a.cpo_id = b.int_ref_no
and b.order_type <> 2
;

drop table if exists table_us14943_add_order_info_2;
create local temporary table table_us14943_add_order_info_2 on commit preserve rows as 
select cpo_id
	,order_no
	,order_type
	,entry_datetime
	,row_number() over(partition by cpo_id order by entry_datetime desc) as rn
from table_us14943_add_order_info
;

drop table if exists table_us14943_add_qty;
create local temporary table table_us14943_add_qty on commit preserve rows as 
select a.cpo_sku_no
	,sum(b.on_hand_qty) as on_hand
	,sum(b.on_order_qty) as on_order
from (select distinct cpo_sku_no
		from table_us14943_cpo
	  ) a
inner join ods_us.ods_cis_corp_inv_qty b
on a.cpo_sku_no = b.sku_no
and b.inv_type = 1
group by a.cpo_sku_no
;


drop table if exists table_us14943_tab1;
create local temporary table table_us14943_tab1 on commit preserve rows as 
select a.cpo_id
	,a.cpo_entry_datetime
	,a.cpo_status
	,a.vend_no
	,a.vend_name
	,a.vpl_code
	,a.cpo_sku_no
	,a.short_desc
	,a.cpo_cust_no
	,a.mast_cust
	,a.reseller_cust_no
	,a.cust_name
	,a.sales_terr
	,a.terr_name
	,a.cust_type_desc
	,a.user_id
	,a.contact_name 
	,a.title        
	,a.phone_no     
	,a.state        
	,a.stop_call    
	,a.email_address
	,a.stop_email   
	,a.stop_mailing
	,b.entry_datetime
	,b.order_no
	,a.source
	,a.from_ref_type
	,a.abc_code
	,a.long_desc
	,a.mar_comment as marketing_comment
	,a.product_image_link
	,c.on_hand
	,c.on_order
	-- ,a.cpo_line_no
from table_us14943_add_addr a
left join table_us14943_add_order_info_2 b
on a.cpo_id=b.cpo_id
and b.rn=1
left join table_us14943_add_qty c
on a.cpo_sku_no=c.cpo_sku_no
where a.rn=1
;


-- tab 2
drop table if exists table_us14943_ec;
create local temporary table table_us14943_ec on commit preserve rows as 
select a.vend_no
	,a.vend_name
	,b.entry_datetime as abandonment_date
	,b.status
	,a.vpl_no
	,a.vpl_code
	,a.sku_no
	,a.short_desc
	,d.mcust_no
	,b.cust_no
	,d.cust_name
	,d.sales_terr
	,d.sales_terr_name as terr_name
	,d.cust_type_descr as cust_type_desc
	,b.user_id
	,d.stop_mailing
	,b.source
	,a.abc_code
	,a.long_desc
	,a.mar_comment
	,'http://oneapiprod.synnex.com/image_technote/' as product_image_link
	,f.contact_no
from dim_us.dim_pub_part_info a
inner join ods_us.ods_etl_ec_cart_history b
on a.sku_no=b.sku_no
inner join ods_us.ods_cis_corp_ec_user f
on b.user_id=f.user_id
and f.delete_date is null
inner join dim_us.dim_pub_customer_info d
on b.cust_no=d.cust_no
where a.vend_no in (select vend_no from ods_gbl.ods_daas_mygbldaas_smb_vend_image_config where e_catalog_source ='GCC' and active = 'Y' and country_code = 'US')
and a.data_source = 'CIS'
and d.cust_type in (245, 137, 246, 247, 244, 231)
and b.entry_datetime>=current_date()-7
and b.entry_datetime<current_date()
and b.status in ('DELETED','SAVED','SAVE4LATER','ACTIVE','FAVORITES')

union

select a.vend_no
	,a.vend_name
	,b.entry_datetime as abandonment_date
	,b.status
	,a.vpl_no
	,a.vpl_code
	,a.sku_no
	,a.short_desc
	,d.mcust_no
	,b.cust_no
	,d.cust_name
	,d.sales_terr
	,d.sales_terr_name as terr_name
	,d.cust_type_descr as cust_type_desc
	,b.user_id
	,d.stop_mailing
	,b.source
	,a.abc_code
	,a.long_desc
	,a.mar_comment
	,'http://oneapiprod.synnex.com/image_technote/' as product_image_link
	,f.contact_no
from dim_us.dim_pub_part_info a
inner join ods_us.ods_etl_ec_cart_current b
on a.sku_no=b.sku_no
inner join ods_us.ods_cis_corp_ec_user f
on b.user_id=f.user_id
and f.delete_date is null
inner join dim_us.dim_pub_customer_info d
on b.cust_no=d.cust_no
where a.vend_no in (select vend_no from ods_gbl.ods_daas_mygbldaas_smb_vend_image_config where e_catalog_source ='GCC' and active = 'Y' and country_code = 'US')
and a.data_source = 'CIS'
and d.cust_type in (245, 137, 246, 247, 244, 231)
and b.entry_datetime>=current_date()-7
and b.entry_datetime<current_date()
and b.status in ('DELETED','SAVED','SAVE4LATER','ACTIVE','FAVORITES')
;

drop table if exists table_us14943_add_addr;
create local temporary table table_us14943_add_addr on commit preserve rows as 
select a.*
	,g.contact_name
	,g.title
	,g.phone_no
	,g.state
	,g.stop_call
	,g.email_address
	,g.stop_email
	,g.addr_no
	,row_number() over(partition by a.sku_no,a.cust_no,a.contact_no,a.user_id order by g.addr_no desc) as rn
from table_us14943_ec a
inner join dim_us.dim_pub_customer_address_contacts_info g
on a.contact_no=g.contact_no
;

drop table if exists table_us14943_add_order;
create local temporary table table_us14943_add_order on commit preserve rows as 
select a.sku_no
	,a.cust_no
	,b.cpo_id
	,c.entry_datetime
	,c.order_no
	,c.order_type
	,d.order_line_no
	,d.entry_datetime as line_create_date
from table_us14943_ec a
inner join ods_us.ods_etl_ec_cart_history b
on a.sku_no=b.sku_no
and a.cust_no=b.cust_no
left join ods_us.ods_cis_corp_order_header c 
on b.cpo_id = c.int_ref_no 
and c.order_type<>2
and c.delete_date is null
left join ods_us.ods_cis_corp_order_detail d
on c.order_no=d.order_no
and c.order_type=d.order_type
and d.delete_date is null
where b.entry_datetime>=current_date()-24
and b.cpo_id>0
and b.status='SUBMITTED'
;

insert into table_us14943_add_order
select a.sku_no
	,a.cust_no
	,b.cpo_id
	,c.entry_datetime
	,c.order_no
	,c.order_type
	,d.order_line_no
	,d.entry_datetime as line_create_date
from table_us14943_ec a
inner join ods_us.ods_etl_ec_cart_history b
on a.sku_no=b.sku_no
and a.cust_no=b.cust_no
left join ods_us.ods_cis_corp_history_header c 
on b.cpo_id = c.int_ref_no 
and c.order_type<>2
and c.delete_date is null
left join ods_us.ods_cis_corp_history_detail d
on c.order_no=d.order_no
and c.order_type=d.order_type
and d.delete_date is null
where b.entry_datetime>=current_date()-24
and b.cpo_id>0
and b.status='SUBMITTED'
;

drop table if exists table_us14943_add_cpo;
create local temporary table table_us14943_add_cpo on commit preserve rows as 
select a.order_no
	,a.sku_no
	,a.cust_no
	,a.entry_datetime
	,max(isnull(b.cpo_id,c.cpo_id)) as cpo_id
	,max(isnull(b.cpo_from_ref_type,c.cpo_from_ref_type)) as cpo_from_ref_type
from (select sku_no
			,cust_no
			,cpo_id
			,entry_datetime
			,order_no
			,order_type
			,order_line_no
			,row_number() over(partition by order_no,order_type order by line_create_date desc) as rn
		from table_us14943_add_order
		) a
left join dm_us.dm_disty_sales_open_cpo b
on a.cpo_id=b.cpo_id
left join dm_us.dm_disty_sales_close_cpo_di c
on a.cpo_id=c.cpo_id
where a.rn=1
group by a.order_no
	,a.sku_no
	,a.cust_no
	,a.entry_datetime
;


drop table if exists table_us14943_final;
create local temporary table table_us14943_final on commit preserve rows as 
select a.vend_no
	,a.vend_name
	,a.abandonment_date
	,a.status
	,a.vpl_no
	,a.vpl_code
	,a.sku_no
	,a.short_desc
	,a.mcust_no
	,a.cust_no
	,a.cust_name
	,a.sales_terr
	,a.terr_name
	,a.cust_type_desc
	,a.user_id
	,a.contact_name 
	,a.title        
	,a.phone_no     
	,a.state        
	,a.stop_call    
	,a.email_address
	,a.stop_email   
	,a.stop_mailing
	,max(b.entry_datetime) as entry_datetime
	,max(b.order_no      ) as order_no      
	,max(b.cpo_id        ) as cpo_id        
	,a.source
	,max(b.cpo_from_ref_type) as from_ref_type
	,a.addr_no
	,a.abc_code
	,a.long_desc
	,a.mar_comment
	,a.product_image_link
from table_us14943_add_addr a
left join table_us14943_add_cpo b
on a.sku_no=b.sku_no
and a.cust_no=b.cust_no
where a.rn=1
group by a.vend_no
	,a.vend_name
	,a.abandonment_date
	,a.status
	,a.vpl_no
	,a.vpl_code
	,a.sku_no
	,a.short_desc
	,a.mcust_no
	,a.cust_no
	,a.cust_name
	,a.sales_terr
	,a.terr_name
	,a.cust_type_desc
	,a.user_id
	,a.contact_name 
	,a.title        
	,a.phone_no     
	,a.state        
	,a.stop_call    
	,a.email_address
	,a.stop_email   
	,a.stop_mailing
	,a.source
	,a.addr_no
	,a.abc_code
	,a.long_desc
	,a.mar_comment
	,a.product_image_link
;


drop table if exists table_us14943_add_qty2;
create local temporary table table_us14943_add_qty2 on commit preserve rows as 
select a.sku_no
	,sum(b.on_hand_qty) as on_hand
	,sum(b.on_order_qty) as on_order
from (select distinct sku_no
		from table_us14943_final
	  ) a
inner join ods_us.ods_cis_corp_inv_qty b
on a.sku_no = b.sku_no
and b.inv_type = 1
group by a.sku_no
;

drop table if exists table_us14943_tab2;
create local temporary table table_us14943_tab2 on commit preserve rows as 
select a.vend_no
	,a.vend_name
	,a.abandonment_date
	,a.status
	,a.vpl_no
	,a.vpl_code
	,a.sku_no
	,a.short_desc
	,a.mcust_no
	,a.cust_no
	,a.cust_name
	,a.sales_terr
	,a.terr_name
	,a.cust_type_desc
	,a.user_id
	,a.contact_name
	,a.title
	,a.phone_no
	,a.state
	,a.stop_call
	,a.email_address
	,a.stop_email
	,a.stop_mailing
	,a.entry_datetime
	,a.order_no      
	,a.cpo_id        
	,a.source
	,a.from_ref_type
	,a.addr_no
	,a.abc_code
	,a.long_desc
	,a.mar_comment as marketing_comment
	,a.product_image_link
	,c.on_hand
	,c.on_order
from table_us14943_final a
left join table_us14943_add_qty2 c
on a.sku_no=c.sku_no
;

-- RDS tables
drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as 
select *
from table_us14943_tab1
;
drop table if exists rdsetl.rds_tmp_2;
create table rdsetl.rds_tmp_2 as 
select *
from table_us14943_tab2
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
insert into rdsetl.rds_tmp_body
select 2 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp_2
;

drop table if exists rdsetl.rds_tmp_sheet_config;
create table rdsetl.rds_tmp_sheet_config(
sheet_index int,
sheet_name varchar(50),
title_active varchar(1),
date_pattern varchar(50)
);
insert into rdsetl.rds_tmp_sheet_config select 1,'Open CPO-Weekly Report',null,'yyyy-MM-dd';
insert into rdsetl.rds_tmp_sheet_config select 2,'Campaign Report',null,'yyyy-MM-dd';

-- 1