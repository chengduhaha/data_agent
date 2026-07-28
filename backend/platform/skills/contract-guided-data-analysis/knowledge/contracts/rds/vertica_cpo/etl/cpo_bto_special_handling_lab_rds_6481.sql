drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_2;
drop table if exists rdsetl.rds_tmp_body;
drop table if exists rdsetl.rds_tmp_sheet_config;



/* Open order */

drop table if exists rds_6481_rtv;
create LOCAL TEMPORARY TABLE rds_6481_rtv ON COMMIT PRESERVE ROWS AS
select distinct
   a.order_type,
   a.order_no,
   a.from_loc_no,
   a.ext_ref as cpo,
   a.ship_to_name,   
   a.ship_to_addr,
   a.ship_to_city,
   a.ship_to_state,
   a.ship_to_zip,
   a.ship_to_country,
   a.int_ref_type,
   a.int_ref_no,
   case when a.int_ref_type = 8 then a.int_ref_no else null end cpo_id,
   a.issue_date as sales_rel_date,
   a.credit_rel_date,
   a.pick_date
from ods_ca.ods_cis_corp_order_header a
inner join ods_ca.ods_cis_corp_order_detail b on a.order_no = b.order_no and a.order_type = b.order_type
where a.to_acct_no = 1055050
and a.order_type in(1,8)
and a.ship_date is null
and a.delete_date is null
and b.delete_date is null
and b.order_qty - ifnull(b.ship_qty,0) <> 0
;



drop table if exists rds_6481_rtv_2;
create LOCAL TEMPORARY TABLE rds_6481_rtv_2 ON COMMIT PRESERVE ROWS AS
select  a.*,
		p.special_handle as bto_order_flag,
		p.end_user_po as end_user_po
from rds_6481_rtv a
left join  ods_ca.ods_cis_corp_order_soldto p
on a.order_no = p.order_no
and a.order_type= p.order_type
and p.special_handle = 1
;



drop table if exists special_handle_6481;
create LOCAL TEMPORARY TABLE special_handle_6481 ON COMMIT PRESERVE ROWS AS
select distinct a.order_type, a.order_no, p.profile_c
from rds_6481_rtv_2 a, ods_ca.ods_cis_corp_order_profile p
where a.order_no = p.order_no
and a.order_type = p.order_type
and p.profile_type = 'SPEC_HANDL'
and p.active = 'Y'
and p.profile_c = 1
;



drop table if exists rds_6481_rtv_3;
create LOCAL TEMPORARY TABLE rds_6481_rtv_3 ON COMMIT PRESERVE ROWS AS
select  
   a.order_no,
   a.order_type,
   a.from_loc_no,
   a.cpo,
   a.ship_to_name,   
   a.ship_to_addr,
   a.ship_to_city,
   a.ship_to_state,
   a.ship_to_zip,
   a.ship_to_country,
   a.int_ref_type,
   a.int_ref_no,
   case when a.int_ref_type = 8 then a.int_ref_no else null end cpo_id,
   a.sales_rel_date,
   a.credit_rel_date,
   a.pick_date,
   case when a.bto_order_flag is null then a.bto_order_flag 
	    	 else p.profile_c end bto_order_flag,
	a.end_user_po
from rds_6481_rtv_2 a
left join special_handle_6481 p
on a.order_no = p.order_no
and a.order_type = p.order_type
;




drop table if exists rds_6481_rtv_4;
create LOCAL TEMPORARY TABLE rds_6481_rtv_4 ON COMMIT PRESERVE ROWS AS
select *
from rds_6481_rtv_3
where bto_order_flag = 1
;


drop table if exists rds_6481_rtv_5;
create LOCAL TEMPORARY TABLE rds_6481_rtv_5 ON COMMIT PRESERVE ROWS AS
select  a.*,
		b.loc_char as from_loc_char
from rds_6481_rtv_4	a
left join dim_ca.dim_pub_location_info b 
on b.loc_no = a.from_loc_no
;



drop table if exists rds_6481_rtv_6;
create LOCAL TEMPORARY TABLE rds_6481_rtv_6 ON COMMIT PRESERVE ROWS AS
select a.*,
	   b.qc_out_pass_datetime as rf_pick_complete_time,
	   b.lab_hold_datetime as lab_hold_date
from rds_6481_rtv_5 a
left join ods_ca.ods_wms_mywms_cws_bto_lab b 
on a.order_no = b.order_no
and a.order_type = b.order_type
;


drop table if exists rds_6481_rtv_7;
create LOCAL TEMPORARY TABLE rds_6481_rtv_7 ON COMMIT PRESERVE ROWS AS
select a.*,
		b.qc_in_pass_datetime as bto_inbound_time
from rds_6481_rtv_6 a
left join ods_ca.ods_wms_mywms_cws_bto_lab b
on a.order_no = b.order_no
and a.order_type = b.order_type
;




drop table if exists rds_6481_rtv_8;
create LOCAL TEMPORARY TABLE rds_6481_rtv_8 ON COMMIT PRESERVE ROWS AS
select a.order_no,
		a.order_type,
   a.from_loc_no,
   a.cpo,
   a.ship_to_name,   
   a.ship_to_addr,
   a.ship_to_city,
   a.ship_to_state,
   a.ship_to_zip,
   a.ship_to_country,
   a.int_ref_type,
   a.int_ref_no,
   a.sales_rel_date,
   a.credit_rel_date,
   a.pick_date,
   a.end_user_po,
	a.from_loc_char,
	a.rf_pick_complete_time,
	a.lab_hold_date,
	a.bto_inbound_time,
   a.bto_order_flag,
   case when a.cpo_id is null then c.int_ref_no else a.cpo_id end as cpo_id
from rds_6481_rtv_7 a
left join ods_ca.ods_cis_corp_order_header b  
on a.int_ref_no = b.order_no
and a.int_ref_type = b.order_type
and b.order_type = 2
left join ods_ca.ods_cis_corp_order_header c
on b.int_ref_no = c.order_no
and b.int_ref_type = c.order_type
and b.int_ref_type = 1
and c.int_ref_type = 8
;



drop table if exists rds_6481_rtv_9;
create LOCAL TEMPORARY TABLE rds_6481_rtv_9 ON COMMIT PRESERVE ROWS AS
select a.*,
		b.cpo_entry_datetime as cpo_date
from rds_6481_rtv_8 a
left join dm_ca.dm_disty_sales_open_cpo b
on a.cpo_id = b.cpo_id
;



drop table if exists rds_6481_rtv_final_1;
create LOCAL TEMPORARY TABLE rds_6481_rtv_final_1 ON COMMIT PRESERVE ROWS AS
select
 distinct 
 order_type,
 order_no,
 from_loc_no,
 from_loc_char,
 cpo,
 end_user_po,
 ship_to_name,
 ship_to_addr,
 ship_to_city,
 ship_to_state,
 ship_to_zip,
 ship_to_country,
 cpo_id,
 cpo_date,
 sales_rel_date,
 credit_rel_date,
 pick_date,
 rf_pick_complete_time,
 bto_inbound_time,
 lab_hold_date,
 null as bto_outbound_time
from rds_6481_rtv_9 a
order by order_type, order_no
;





/* shipped order */

drop table if exists rds_6481_rtv_12;
create LOCAL TEMPORARY TABLE rds_6481_rtv_12 ON COMMIT PRESERVE ROWS AS
select distinct
   a.order_type,
   a.order_no,
   a.from_loc_no,
   a.ext_ref as cpo,
   a.ship_to_name,   
   a.ship_to_addr,
   a.ship_to_city,
   a.ship_to_state,
   a.ship_to_zip,
   a.ship_to_country,
   a.ship_date as ship_time,
   a.ship_method
from ods_ca.ods_cis_corp_history_header a
inner join ods_ca.ods_cis_corp_history_detail b on a.order_no = b.order_no and a.order_type = b.order_type
where a.to_acct_no = 1055050
and a.order_type = 1
and a.ship_date >= current_date()-1 
and a.ship_date < current_date() 
;


drop table if exists rds_6481_rtv_13;
create LOCAL TEMPORARY TABLE rds_6481_rtv_13 ON COMMIT PRESERVE ROWS AS
select a.*,
		p.special_handle as bto_order_flag,
		p.end_user_po as  end_user_po
from rds_6481_rtv_12 a
left join ods_ca.ods_cis_corp_history_soldto p 
on a.order_no = p.order_no
and a.order_type= p.order_type
and p.special_handle = 1
;



drop table if exists special_handle_6481_2;
create LOCAL TEMPORARY TABLE special_handle_6481_2 ON COMMIT PRESERVE ROWS AS
select distinct a.order_type, a.order_no, p.profile_c
from rds_6481_rtv_13 a, ods_ca.ods_cis_corp_order_profile p
where a.order_no = p.order_no
and a.order_type = p.order_type
and p.profile_type = 'SPEC_HANDL'
and p.active = 'Y'
and p.profile_c = 1
;


drop table if exists rds_6481_rtv_14;
create LOCAL TEMPORARY TABLE rds_6481_rtv_14 ON COMMIT PRESERVE ROWS AS
SELECT 
		a.order_type,
   a.order_no,
   a.from_loc_no,
   a.cpo,
   a.ship_to_name,   
   a.ship_to_addr,
   a.ship_to_city,
   a.ship_to_state,
   a.ship_to_zip,
   a.ship_to_country,
   a.ship_time,
   a.ship_method,
   case when a.bto_order_flag is null then a.bto_order_flag 
	    	 else p.profile_c end bto_order_flag,
	  a.end_user_po
from rds_6481_rtv_13 a
left join special_handle_6481_2 p
on a.order_no = p.order_no
and a.order_type = p.order_type
;


drop table if exists rds_6481_rtv_15;
create LOCAL TEMPORARY TABLE rds_6481_rtv_15 ON COMMIT PRESERVE ROWS AS
select *
from rds_6481_rtv_14 a
where bto_order_flag = 1
;


drop table if exists rds_6481_rtv_16;
create LOCAL TEMPORARY TABLE rds_6481_rtv_16 ON COMMIT PRESERVE ROWS AS
select a.*,
		b.loc_char as from_loc_char
from rds_6481_rtv_15 a
left join dim_ca.dim_pub_location_info b
on b.loc_no = a.from_loc_no
;



drop table if exists rds_6481_track_distinct;
create LOCAL TEMPORARY TABLE rds_6481_track_distinct ON COMMIT PRESERVE ROWS AS
select distinct a.order_no,a.order_type,a.track_no
from ods_ca.ods_cis_corp_carton_header a
inner join rds_6481_rtv_16 b 
on a.order_no=b.order_no
and a.order_type=b.order_type
;

drop table if exists rds_6481_track_no;
create LOCAL TEMPORARY TABLE rds_6481_track_no ON COMMIT PRESERVE ROWS AS
select a.order_no
,a.order_type
,listagg(b.track_no using parameters max_length=1024, on_overflow='TRUNCATE') as track_no
from rds_6481_rtv_16 a
left join rds_6481_track_distinct b 
on a.order_no=b.order_no
and a.order_type=b.order_type
group by a.order_no
,a.order_type
;



drop table if exists rds_6481_rtv_final_2;
create LOCAL TEMPORARY TABLE rds_6481_rtv_final_2 ON COMMIT PRESERVE ROWS AS
select
 a.order_type,
 a.order_no,
 a.from_loc_no,
 a.from_loc_char,
 a.cpo,
 a.end_user_po,
 a.ship_to_name,
 a.ship_to_addr,
 a.ship_to_city,
 a.ship_to_state,
 a.ship_to_zip,
 a.ship_to_country,
 a.ship_time,
 a.ship_method,
 c.track_no as tracking_no,
 b.part_no,
 b.sku_no,
 b.serial_no,
 b.tag_no,
 b.mac_address,
 b.item_no,
 null as pkid
 from rds_6481_rtv_16 a
left join rds_6481_track_no c
on a.order_no = c.order_no
and a.order_type= c.order_type
left join ods_ca.ods_cis_corp_asset_tag b
on a.order_type = b.order_type
and a.order_no= b.order_no
and b.serial_no is not null
and b.tag_no is not null
order by order_type, order_no
;

CREATE TABLE rdsetl.rds_tmp AS 
select * from rds_6481_rtv_final_1;

CREATE TABLE rdsetl.rds_tmp_2 AS 
select * from rds_6481_rtv_final_2;


create table rdsetl.rds_tmp_sheet_config(
sheet_index int,
sheet_name varchar(50),
title_active varchar(1),
date_pattern varchar(50)
)
;

insert into rdsetl.rds_tmp_sheet_config values(1,'Open order',null,null);
insert into rdsetl.rds_tmp_sheet_config values(2,'shipped',null,null);


CREATE TABLE rdsetl.rds_tmp_body AS 
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;

Insert into rdsetl.rds_tmp_body
select 2 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp_2
;