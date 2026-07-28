
drop table if exists tempdb.temp_que_nos_7026;
create table tempdb.temp_que_nos_7026 as
 select a.mt_que_no  as que_no
 from ods_ca.ods_cis_corp_consignment_mt_que_rt a
 inner join ods_ca.ods_cis_corp_part_master_rt c
	on a.sku_no = c.sku_no
 inner join  ods_ca.ods_cis_corp_order_header_rt d
	on  a.int_ref_no = d.order_no
    and d.order_type = a.int_ref_type
where d.delete_id is null
 and a.cust_no= 1055308
 and a.from_ref_type=81
 and 1=2
 ;



    insert into tempdb.temp_que_nos_7026

    select a.mt_que_no  as que_no
     from ods_ca.ods_cis_corp_consignment_mt_que_rt a
 inner join ods_ca.ods_cis_corp_part_master_rt c
	on a.sku_no = c.sku_no
 left join  ods_ca.ods_cis_corp_order_header_rt d
	on  a.int_ref_no = d.order_no
    and a.int_ref_type = d.order_type
	and d.delete_id is null
	 where a.cust_no=1055308
	  and a.from_ref_type=81
    and a.entry_datetime >= DATE_FORMAT( DATE_SUB(CURRENT_DATE(), interval (dayofmonth(current_date())-1)day), '%Y-%m-01')
      and a.entry_datetime <  DATE_FORMAT( current_date(), '%Y-%m-%d')
      order by  a.cust_no asc, a.cust_po_no asc, a.cust_loc_no asc, a.sku_no asc, a.mt_que_no asc
    ;




drop table if exists tempdb.consign_batch_tmp_7026;
create table tempdb.consign_batch_tmp_7026 PRIMARY KEY(id) DISTRIBUTED BY HASH(id) as

select
uuid_numeric() as id,
a.mt_que_no,
a.from_ref_type,
a.cust_no,
a.cust_loc_no,
a.sku_no,
a.po_qty,
a.fullfill_qty,
a.cust_po_no,
a.batch_no,
a.seq_no,
a.entry_id,
a.entry_datetime,
a.status,
a.int_ref_type,
a.int_ref_no,
a.int_ref_line_no,
a.issue_date,
a.receiving_date,
a.kill_id,
a.kill_date,
a.int_ref_type2,
a.int_ref_no2,
a.int_ref_line_no2,
a.cust_inv_qty  ,
cast(b.loc_no as int) as loc_no,
c.part_no ,
c.abc_code,
case when d.entry_datetime is null then (select entry_datetime from ods_ca.ods_cis_corp_history_header_rt hh
										where hh.order_no = a.int_ref_no and hh.order_type = a.int_ref_type)
										else d.entry_datetime end as order_entry_datetime,
c.vend_no,
vm.vend_name,
case when d.from_loc_no is null then
	(select from_loc_no
	 from ods_ca.ods_cis_corp_history_header_rt hh
	 where hh.order_no = a.int_ref_no
	 and hh.order_type = a.int_ref_type)
	 else d.from_loc_no end as from_loc_no,
b.loc_name as cust_loc_name,
case when d.ship_date is null then
			(select ship_date from ods_ca.ods_cis_corp_history_header_rt hh
			 where hh.order_no = a.int_ref_no
			 and hh.order_type = a.int_ref_type)
			 else d.ship_date end as ship_date,
case when d.credit_rel_date is null
                   then (select credit_rel_date from ods_ca.ods_cis_corp_history_header_rt hh
				   where hh.order_no = a.int_ref_no
				   and hh.order_type = a.int_ref_type)
				   else d.credit_rel_date end as credit_rel_date,
c.active_status,
c.avail_to_sell,
case when d.invoice_date is null
     then (select invoice_date from ods_ca.ods_cis_corp_history_header_rt hh
	 where hh.order_no = a.int_ref_no
	 and hh.order_type = a.int_ref_type)
	 else d.invoice_date
	 end as invoice_date,
case when d.ship_to_state is null
	 then (select ship_to_state
		   from ods_ca.ods_cis_corp_history_header_rt hh
		   where hh.order_no = a.int_ref_no
		   and hh.order_type = a.int_ref_type)
		   else d.ship_to_state end as ship_to_prov,
ifnull(ap.profile_i,-1)  as default_loc,
ifnull(h.loc_char,'Default') as default_loc_char,
-- primary_wh  = convert(varchar(10),null)
 null as master_cust_no,
 null as primary_loc_no,
 ad.addr_no as addr_no
 -- primary_loc_char=convert(varchar(50),null)
from ods_ca.ods_cis_corp_consignment_mt_que_rt a
  inner join tempdb.temp_que_nos_7026 e
	on a.mt_que_no=e.que_no
  inner join ods_ca.ods_cis_corp_location_info_rt b
	on a.cust_no = b.ext_no
  inner join ods_ca.ods_cis_corp_part_master_rt c
  	on a.sku_no = c.sku_no
  left  join ods_ca.ods_cis_corp_order_header_rt d
  	on a.int_ref_no =d.order_no
  	and d.order_type = a.int_ref_type	and d.order_type in (48,148) and d.delete_id is null
  inner join ods_ca.ods_cis_corp_vend_master_rt vm
  	on c.vend_no = vm.vend_no
  left join ods_ca.ods_cis_corp_addr_xref_rt ax
	on a.cust_no = ax.xref_no
   and a.cust_loc_no =ax.xref_seq
   and ax.xref_type = 'ADDR_CUST'
   and ax.active='Y'
left join ods_ca.ods_cis_corp_address_rt ad
	on ad.addr_no = ax.addr_no
left join ods_ca.ods_cis_corp_addr_profile_rt ap
	  on ad.addr_no  = ap.addr_no
	 and ap.profile_type ='DEF_WH'
	 and ap.active = 'Y'
left join ods_ca.ods_cis_corp_location_info_rt h
		on ifnull(ap.profile_i,-1) = h.loc_no
		where   b.ext_loc_no = 1

;



 update tempdb.consign_batch_tmp_7026
 set cust_loc_name = ca.addr_name1a
 from ods_ca.ods_cis_corp_customer_header_rt ch
 ,ods_ca.ods_cis_corp_address_rt ca
 ,ods_ca.ods_cis_corp_addr_xref_rt ax
 where ch.cust_no =  (SELECT xref_no
					 FROM ods_ca.ods_cis_corp_cust_xref_rt
					 WHERE xref_type = 'MASTER_SUB'
                     AND cust_no = 1055308
                     AND active IN ('Y','y'))
 and ch.cust_no = ax.xref_no
 and cast(ax.xref_seq as int )= consign_batch_tmp_7026.cust_loc_no
 and ax.xref_type = 'ADDR_CUST'
 and ca.addr_no = ax.addr_no
 and ax.active='Y'
 ;

 update tempdb.consign_batch_tmp_7026
 set master_cust_no = x.xref_no
 from ods_ca.ods_cis_corp_cust_profile_rt p
 ,ods_ca.ods_cis_corp_cust_xref_rt x
 where consign_batch_tmp_7026.cust_no=p.cust_no
 and p.profile_type='CSGN_1VLOC'
 and p.profile_cat='OTHE'
 and p.active in ('Y','y')
 and p.cust_no=x.cust_no
 and x.xref_type ='MASTER_SUB'
 and x.active in ('Y','y')
;


 update tempdb.consign_batch_tmp_7026
 set cust_loc_name = b.addr_name1a
 from ods_ca.ods_cis_corp_customer_header_rt a
 ,ods_ca.ods_cis_corp_address_rt b
 ,ods_ca.ods_cis_corp_addr_xref_rt c
 where a.cust_no =consign_batch_tmp_7026.master_cust_no
 and a.cust_no = c.xref_no
 and c.xref_seq = consign_batch_tmp_7026.cust_loc_no
 and c.xref_type = 'ADDR_CUST'
 and b.addr_no = c.addr_no
 and c.active = 'Y'
;

 update tempdb.consign_batch_tmp_7026
 set ship_to_prov = f.state
 from ods_ca.ods_cis_corp_addr_xref_rt e
 ,ods_ca.ods_cis_corp_address_rt f
 where e.addr_no = f.addr_no
 and consign_batch_tmp_7026.cust_no = e.xref_no
 and e.xref_type = 'ADDR_CUST'
 and e.xref_seq = consign_batch_tmp_7026.cust_loc_no
 and e.active = 'Y'
 ;


 update tempdb.consign_batch_tmp_7026
 set primary_loc_no = ( select ifnull(g.profile_i,-1)
                        from ods_ca.ods_cis_corp_addr_xref_rt e
						,ods_ca.ods_cis_corp_address_rt f
						,ods_ca.ods_cis_corp_addr_profile_rt g
                        where e.xref_no =  consign_batch_tmp_7026.cust_no
                        and e.xref_type  = 'ADDR_CUST'
                        and e.addr_no = f.addr_no
                        and e.addr_no = g.addr_no
                        and g.profile_type ='DEF_WH'
                        and e.active = 'Y' and g.active = 'Y' )
 from ods_ca.ods_cis_corp_cust_profile_rt p
 where consign_batch_tmp_7026.cust_no=p.cust_no
 and p.profile_type='CSGN_1VLOC'
 and p.profile_cat='OTHE'
 and p.active in ('Y','y')
 ;


 drop table if exists tempdb.tmp;
 create table tempdb.tmp PRIMARY KEY(id) DISTRIBUTED BY HASH(id) as

 with min_eta as
( select
		sku_no,
		eta_code,
		date_format(min(eta),'%m/%d/%Y') as min_eta
   from dm_ca.dm_pur_unieta_boso_detail_rt eta
   group by sku_no
)
   select uuid_numeric() as id,
	a.mt_que_no,
	a.cust_no,
	a.cust_loc_name,
	a.cust_loc_no,
	a.ship_to_prov,
	a.cust_po_no,
	a.sku_no,
	a.part_no  ,
	a.abc_code,
	a.po_qty,
	a.fullfill_qty,
	a.from_loc_no ,
	a.primary_loc_no ,
	a.int_ref_type ,
	a.int_ref_no ,
	a.status,
	a.issue_date,
	a.ship_date,
	a.receiving_date,
	b.loginid,
	a.entry_datetime,
	a.kill_id ,
    a.kill_date,
    a.vend_no,
    a.vend_name,
    cast(0 as int) as DMH_RIO,
    cast(0 as int) as DHA_RIO,
    cast(0 as int) as DGU_RIO,
    cast(0 as int) as DCG_RIO,
    cast(0 as int) as DRN_RIO,
    cast(0 as int) as DMS_RIO,
    cast(0 as int) as DMH_AVAILABLE,
    cast(0 as int) as DHA_AVAILABLE,
    cast(0 as int) as DGU_AVAILABLE,
    cast(0 as int) as DCG_AVAILABLE,
    cast(0 as int) as DRN_AVAILABLE,
    cast(0 as int) as DMS_AVAILABLE,
    cast(0 as int) as Avai_stock,
    cast(0 as int) as On_Order_Stock,
    eta.min_eta as ETA_Date,
    eta_code as ETA_Code
    from tempdb.consign_batch_tmp_7026 a
	left join ods_ca.ods_cis_corp_manager_rt b
		on a.entry_id = b.userid
	left join ods_ca.ods_cis_corp_manager_rt c
		on a.kill_id = c.userid
	left join min_eta eta
		on a.sku_no=eta.sku_no
	  -- and a.order_no = eta.order_no
	--	 and a.order_type = eta.order_type
	--	 and b.order_line_no = eta.order_line_no

	order by  sku_no
	;


	drop table if exists tempdb.sku_avail;
    create table tempdb.sku_avail as
	SELECT b.sku_no
	      ,sum(a.on_order_qty) as oo
	      ,sum(a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty) as avail
	FROM dw_ca.dwd_disty_inv_qty_df a
	    ,(SELECT DISTINCT sku_no FROM tempdb.tmp) b
	WHERE a.date_flag = date_format(date_add( CURRENT_DATE(), INTERVAL -1 DAY), '%Y-%m-%d')
	        AND a.sku_no = b.sku_no
	        AND a.inv_type IN (1,300)
	GROUP BY b.sku_no
	;

	UPDATE tempdb.tmp
	SET Avai_stock = b.avail
	   ,On_Order_Stock = b.oo
	FROM tempdb.sku_avail b
	where tmp.sku_no = b.sku_no
	;


	-- rio

	drop table if exists tempdb.rds_rio_7026;
    create table tempdb.rds_rio_7026 as
	SELECT rrh.sku_no
	      ,rrh.cust_no
	      ,sum(CASE WHEN loc_no = 57 THEN rrd.hold_qty ELSE 0 END) as DMH_RIO
	      ,sum(CASE WHEN loc_no = 26 THEN rrd.hold_qty ELSE 0 END) DHA_RIO
	      ,sum(CASE WHEN loc_no = 29 THEN rrd.hold_qty ELSE 0 END) DGU_RIO
	      ,sum(CASE WHEN loc_no = 31 THEN rrd.hold_qty ELSE 0 END) DCG_RIO
	      ,sum(CASE WHEN loc_no = 81 THEN rrd.hold_qty ELSE 0 END) DRN_RIO
	      ,sum(CASE WHEN loc_no = 80 THEN rrd.hold_qty ELSE 0 END) DMS_RIO
	FROM ods_ca.ods_cis_corp_rio_request_header_rt rrh
	inner join ods_ca.ods_cis_corp_rio_req_detail_rt rrd
		 on rrh.rio_req_no = rrd.rio_req_no
	    AND rrh.cust_no IN (select DISTINCT cust_no from tempdb.tmp)
	    AND rrd.inproc_ref_type = 18
	GROUP BY rrh.sku_no,rrh.cust_no
	;

	UPDATE tempdb.tmp
	SET DMH_RIO = b.DMH_RIO
	   ,DHA_RIO = b.DHA_RIO
	   ,DGU_RIO = b.DGU_RIO
	   ,DCG_RIO = b.DCG_RIO
	   ,DRN_RIO = b.DRN_RIO
	   ,DMS_RIO = b.DMS_RIO
	FROM  tempdb.rds_rio_7026 b
	where tmp.sku_no = b.sku_no
	;


	drop table if exists tempdb.rds_inv_7026;
    create table tempdb.rds_inv_7026 as
	SELECT sku_no
	      ,sum(CASE WHEN loc_no = 57 THEN a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty ELSE 0 END) DMH_AVAILABLE
	      ,sum(CASE WHEN loc_no = 26 THEN a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty ELSE 0 END) DHA_AVAILABLE
	      ,sum(CASE WHEN loc_no = 29 THEN a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty ELSE 0 END) DGU_AVAILABLE
	      ,sum(CASE WHEN loc_no = 31 THEN a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty ELSE 0 END) DCG_AVAILABLE
	      ,sum(CASE WHEN loc_no = 81 THEN a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty ELSE 0 END) DRN_AVAILABLE
	      ,sum(CASE WHEN loc_no = 80 THEN a.on_hand_qty - a.bo_qty + a.intran_in - a.intran_out - a.alloc_qty ELSE 0 END) DMS_AVAILABLE
	FROM ods_ca.ods_cis_corp_inv_qty_rt a
	WHERE inv_type IN ( 1 ,200)
	GROUP BY sku_no
	;

	UPDATE tempdb.tmp
	SET DMH_AVAILABLE = b.DMH_AVAILABLE
	    ,DHA_AVAILABLE = b.DHA_AVAILABLE
	    ,DGU_AVAILABLE = b.DGU_AVAILABLE
	    ,DCG_AVAILABLE = b.DCG_AVAILABLE
	    ,DRN_AVAILABLE = b.DRN_AVAILABLE
	    ,DMS_AVAILABLE = b.DMS_AVAILABLE
	FROM tempdb.rds_inv_7026 b
	WHERE tmp.sku_no = b.sku_no
	;


 drop table if exists tempdb.rds_tmp;
 create table tempdb.rds_tmp as
   select
	mt_que_no,
	cust_no,
	cust_loc_name,
	cust_loc_no,
	ship_to_prov,
	cust_po_no,
	sku_no,
	part_no,
	abc_code,
	po_qty,
	fullfill_qty,
	from_loc_no ,
	primary_loc_no ,
	int_ref_type ,
	int_ref_no ,
	status,
	date_format(issue_date,'%m/%d/%Y') as issue_date,
	date_format(ship_date,'%m/%d/%Y') as ship_date,
	date_format(receiving_date,'%m/%d/%Y') as receiving_date,
	loginid,
	date_format(entry_datetime,'%m/%d/%Y') as entry_datetime,
	kill_id ,
    date_format(kill_date,'%m/%d/%Y') as kill_date,
    vend_no,
    vend_name,
    DMH_RIO,
    DHA_RIO,
    DGU_RIO,
    DCG_RIO,
    DRN_RIO,
    DMS_RIO,
    DMH_AVAILABLE,
    DHA_AVAILABLE,
    DGU_AVAILABLE,
    DCG_AVAILABLE,
    DRN_AVAILABLE,
    DMS_AVAILABLE,
    Avai_stock,
    On_Order_Stock,
    ETA_Date,
    ETA_Code
    from tempdb.tmp
    ;

drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;

