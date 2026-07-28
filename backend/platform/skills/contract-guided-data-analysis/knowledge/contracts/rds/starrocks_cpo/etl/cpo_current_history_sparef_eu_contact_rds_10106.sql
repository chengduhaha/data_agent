
use tempdb;

DROP TABLE IF EXISTS tempdb.rds_tmp;
DROP TABLE IF EXISTS tempdb.rds_tmp_body;


DROP TABLE IF EXISTS tempdb.temp_10106;
			
create table tempdb.temp_10106  as 			
SELECT  b.vend_no				
	,c.cpo_cust_no as cust_no			
	,cast(null as int ) as mcust_no 			
	,cast(null as varchar(60)) as cust_name			
	,a.cpo_id as qute_no			
	,a.cpo_entry_datetime as  entry_datetime			
	,c.cpo_sales_terr as sales_terr			
	,cast(null as varchar(60)) as terr_name		
	,c.cpo_no as customer_po			
	,a.cpo_sku_no as sku_no			
	,dpl.vpl_code			
	,b.mfg_partno  			
	,b.short_desc as vendor_part_descr			
	,a.cpo_line_qty as order_qty			
	,b.po_cost as base_cost			
	,b.po_cost *a.cpo_line_qty	as extended_base_cost
	,cast(null as varchar(60))	as sales_terr_email		
	,e.profile_c as  vend_spa			
	,cast(null as varchar(60)) as addr_no 			
	,cast(null as varchar(60))  as reseller_city			
	,cast(null as varchar(60))	as reseller_state		
	,cast(null as varchar(60))	as reseller_email_address		
	,cast(null as varchar(60))	as reseller_contact_name		
	,d.probability
	,cast(null as varchar(60)) as end_user_name
    ,cast(null as varchar(60)) as end_user_address
    ,cast(null as varchar(60)) as end_user_contact_name
	,cast(null as varchar(60)) as end_user_email

FROM ods_us.ods_cis_corp_cpo_detail_rt a				
inner join ods_us.ods_cis_corp_part_master_rt b on	a.cpo_sku_no=b.sku_no		
inner join ods_us.ods_cis_corp_cpo_header_rt c	on a.cpo_id = c.cpo_id		
left join ods_us.ods_cis_corp_spl_open_rt d on   a.cpo_id = d.int_ref_no 			
left join ods_us.ods_cis_corp_cpo_profile_rt e 			
on  a.cpo_id = e.cpo_id			
and e.profile_type='SPAREF#'	
and e.active='Y'	
left join ods_us.ods_cis_corp_dw_vend_pl_rt dpl on b.vpl_no = dpl.vpl_no			
where b.vend_no=70425 				
and a.cpo_entry_datetime >= DATE_ADD(CURRENT_DATE(),INTERVAL -7 DAY)			
and a.cpo_delete_datetime is null  				
union 							
SELECT b.vend_no					
	,c.cpo_cust_no as cust_no			
	,cast(null as int ) as mcust_no 			
	,cast(null as varchar(60)) as cust_name			
	,a.cpo_id as qute_no			
	,a.cpo_entry_datetime as  entry_datetime			
	,c.cpo_sales_terr as sales_terr			
	,cast(null as varchar(60)) as terr_name		
	,c.cpo_no as customer_po			
	,a.cpo_sku_no as sku_no			
	,dpl.vpl_code			
	,b.mfg_partno  			
	,b.short_desc as vendor_part_descr			
	,a.cpo_line_qty as order_qty			
	,b.po_cost as base_cost			
	,b.po_cost *a.cpo_line_qty	as extended_base_cost
	,cast(null as varchar(60))	as sales_terr_email		
	,e.profile_c as  vend_spa			
	,cast(null as varchar(60)) as addr_no 			
	,cast(null as varchar(60))  as reseller_city			
	,cast(null as varchar(60))	as reseller_state		
	,cast(null as varchar(60))	as reseller_email_address		
	,cast(null as varchar(60))	as reseller_contact_name		
	,d.probability
	,cast(null as varchar(60)) as end_user_name
    ,cast(null as varchar(60)) as end_user_address
    ,cast(null as varchar(60)) as end_user_contact_name
	,cast(null as varchar(60)) as end_user_email
FROM ods_us.ods_cis_corp_history_cpo_detail_rt a				
inner join ods_us.ods_cis_corp_part_master_rt b	on a.cpo_sku_no=b.sku_no		
inner join ods_us.ods_cis_corp_history_cpo_header_rt c	on a.cpo_id = c.cpo_id			
left join ods_us.ods_cis_corp_spl_open_rt d on   a.cpo_id = d.int_ref_no 			
left join ods_us.ods_cis_corp_history_cpo_profile_rt e 			
on  a.cpo_id = e.cpo_id			
and e.profile_type='SPAREF#'	
and e.active='Y'	
left join ods_us.ods_cis_corp_dw_vend_pl_rt dpl on b.vpl_no = dpl.vpl_no			
where b.vend_no=70425 				
and a.cpo_entry_datetime >=DATE_ADD(CURRENT_DATE(),INTERVAL -7 DAY)
and a.cpo_delete_datetime is null  				
;				


create table tempdb.rds_tmp PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
select uuid_numeric() as id, a.*
from tempdb.temp_10106 a
;

drop table if exists tempdb.t1_10106;

create table tempdb.t1_10106 as
select distinct a.cust_no, ifnull(b.xref_no,a.cust_no)  as mcust_no
from tempdb.rds_tmp a
left join ods_us.ods_cis_corp_cust_xref_rt b
on a.cust_no = b.cust_no
and b.xref_type = 'MASTER_SUB'
and ifnull(b.active,'Y')= 'Y'
;

update tempdb.rds_tmp 	
set mcust_no  = (select b.mcust_no
                   from tempdb.t1_10106 b
                   where b.cust_no = tempdb.rds_tmp.cust_no)
where tempdb.rds_tmp.cust_no is not null
;

				
update tempdb.rds_tmp  			
set cust_name = (select cust_name from ods_us.ods_cis_corp_customer_header_rt b where tempdb.rds_tmp.cust_no = b.cust_no)	
where tempdb.rds_tmp.cust_no is not null
;			

update tempdb.rds_tmp 			
set terr_name = (select terr_name from ods_us.ods_cis_corp_territory_rt b where tempdb.rds_tmp.sales_terr = b.sales_terr)	
where tempdb.rds_tmp.sales_terr is not null
; 				


update tempdb.rds_tmp 				
set sales_terr_email= 
(select c.email 				
from  ods_us.ods_cis_corp_manager_rt b, ods_us.ods_cis_corp_employee_contacts_rt c  				
where tempdb.rds_tmp.terr_name = concat(b.firstname,' ',b.lastname)                                            				
and b.userid = c.user_id)	
where tempdb.rds_tmp.terr_name is not null
;		
 
				
update tempdb.rds_tmp                                      				
set   sales_terr_email = concat('sales',cast(sales_terr as varchar(60)),'@synnex.com')		
where sales_terr_email is null  				
;			

update tempdb.rds_tmp			
set  reseller_city			
= (select b.city1a			
     from ods_us.ods_cis_corp_address_rt b,ods_us.ods_cis_corp_addr_xref_rt c  				
    where tempdb.rds_tmp.cust_no =c.xref_no				
      and c.xref_seq=1				
      and b.addr_no=c.addr_no				
      and c.xref_type='ADDR_CUST')	
where tempdb.rds_tmp.cust_no is not null
;		

update tempdb.rds_tmp			
set  reseller_state				
= (select  b.state			
     from ods_us.ods_cis_corp_address_rt b,ods_us.ods_cis_corp_addr_xref_rt c  				
    where tempdb.rds_tmp.cust_no =c.xref_no				
      and c.xref_seq=1				
      and b.addr_no=c.addr_no				
      and c.xref_type='ADDR_CUST')	
where tempdb.rds_tmp.cust_no is not null
;				

update tempdb.rds_tmp			
set addr_no	
= (select b.addr_no 				
     from ods_us.ods_cis_corp_address_rt b,ods_us.ods_cis_corp_addr_xref_rt c  				
    where tempdb.rds_tmp.cust_no =c.xref_no				
      and c.xref_seq=1				
      and b.addr_no=c.addr_no				
      and c.xref_type='ADDR_CUST')	
where tempdb.rds_tmp.cust_no is not null
;			

drop table if exists tempdb.t2_10106;

create table tempdb.t2_10106 as
select a.addr_no,min(d.contact_no) as contact_no		
from tempdb.rds_tmp a,ods_us.ods_cis_corp_contact_xref_rt d				
where a.addr_no =d.xref_no 				
and d.xref_type='CONT_ADDR'				
and d.xref_seq=1			
group by a.addr_no
;


update tempdb.rds_tmp 			
set reseller_contact_name				
  = (select e.contact_name				
       from tempdb.t2_10106 a,ods_us.ods_cis_corp_contacts_rt e 				
      where tempdb.rds_tmp.addr_no =a.addr_no							
        and a.contact_no = e.contact_no)
where tempdb.rds_tmp.addr_no is not null  
;						

update tempdb.rds_tmp 			
set reseller_email_address				
  = (select e.email_address				
       from tempdb.t2_10106 a,ods_us.ods_cis_corp_contacts_rt e 				
      where tempdb.rds_tmp.addr_no =a.addr_no							
        and a.contact_no = e.contact_no)
where tempdb.rds_tmp.addr_no is not null  
;				


drop table if exists tempdb.t3_10106;

create table tempdb.t3_10106 as
select a.qute_no,
       b.eu_company_name,
       b.eu_loc_address1,
       b.eu_loc_contact,
       b.eu_contact_email
from tempdb.rds_tmp  a , ods_us.ods_cis_corp_cpo_eu_common_rt b
where a.qute_no=b.cpo_id
and b.cpo_line_seq = 0
UNION 
select a.qute_no,
       b.eu_company_name,
       b.eu_loc_address1,
       b.eu_loc_contact,
       b.eu_contact_email
from tempdb.rds_tmp  a , ods_us.ods_cis_corp_history_cpo_eu_common_rt b
where a.qute_no=b.cpo_id
and b.cpo_line_seq = 0
;

update tempdb.rds_tmp 
set end_user_name = (select b.eu_company_name from tempdb.t3_10106 b where tempdb.rds_tmp.qute_no=b.qute_no),
    end_user_address = (select b.eu_loc_address1 from tempdb.t3_10106 b where tempdb.rds_tmp.qute_no=b.qute_no),
    end_user_contact_name = (select b.eu_loc_contact from tempdb.t3_10106 b where tempdb.rds_tmp.qute_no=b.qute_no),
    end_user_email = (select b.eu_contact_email from tempdb.t3_10106 b where tempdb.rds_tmp.qute_no=b.qute_no)
where tempdb.rds_tmp.qute_no is not null
;


CREATE TABLE tempdb.rds_tmp_body as 
SELECT 'standard' as body_type
,count(*) as cnt
FROM tempdb.rds_tmp
;

