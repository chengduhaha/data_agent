
drop table if exists tempdb.rds_sku_6302;
create table tempdb.rds_sku_6302 as
select
a.sku_no,
a.short_desc,
b.vpl_code,
a.part_no,
a.mfg_partno,
a.abc_code,
a.po_cost
from ods_ca.ods_cis_corp_part_master_rt a
inner join ods_ca.ods_cis_corp_dw_vend_pl_rt b
	on a.vpl_no=b.vpl_no
and b.vend_no in(16996)
;



drop table if exists tempdb.temp_6302;
create table tempdb.temp_6302 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
SELECT
uuid_numeric() as id,
b.sku_no,
a.from_loc_no,
ifnull(a.order_type,null) as order_type,
a.to_acct_no as CUST_NUM,
cast(null as varchar(100)) as CUST_NAME,

cast(null as int) as RIO_Req_No,
cast(null as varchar(10)) as RIO_Request_Date,
cast(null as int) as RIO_No,
cast(null as varchar(200)) as Ref_No,
cast(null as varchar(200)) as Ref_No_Description,
cast(null as varchar(10)) as RIO_Approve_Date,
cast(null as varchar(10)) as RIO_Expiration_Date,
cast(null as varchar(80)) as RIO_Approved,

date_format(a.entry_datetime,'%m/%d/%Y') as ORDR_ENTRY_DATE,
cast(null as int) as REP_ID,
a.sales_terr as TERR,
cast(null as varchar(100)) as SALES_REP_NME,
ifnull(a.order_no,null) as order_no,
ifnull(b.order_line_no,null) as LINE_NO,
cast(null as varchar(50)) as WH,
a.ext_ref as CUSTOMER_PO,
cast(null as varchar(60)) as END_USER_PO,
c.short_desc,
ifnull(c.vpl_code,null) as PLINE,
c.part_no as PART_NO,
c.mfg_partno as VNDR_PROD_NO,
b.order_qty as QTY_ORD,
case when b.order_type = 8 then b.order_qty else 0 end as QTY_BO,
case when b.order_type = 1 then b.order_qty else 0 end as QTY_ALLOC,

cast(null as int) as RIO_Req_Qty,
cast(null as int) as RIO_Reserved_Orders,
cast(null as int) as RIO_PO_MT_Qty,
cast(null as int) as RIO_Open_Qty,
cast(null as int) as Consumed_Qty,

(b.ship_qty * b.unit_price) as EXTND_PRICE,
c.abc_code as STAT_CODE,
a.ship_method as SHIP_VIA,
a.ship_to_addr as SHIP_TO_ADDR_LINE,
a.ship_to_city as SHIP_TO_CITY_NAME,
a.ship_to_state as SHIP_TO_STATE,
a.ship_to_zip as SHIP_TO_POSTAL_CODE,
date_format(a.ship_date,'%m/%d/%Y') as CUST_AVAIL_SHIP_DATE,
null as ETA,
cast(null as int) as VEN_PO,
a.ship_to_name as SHIP_TO_NAME,
c.po_cost as Base_Cost,
(b.order_qty*c.po_cost) as Ext_Base_Cost_ORD,
case when b.order_type = 8 then (b.order_qty*c.po_cost) else 0 end as Ext_Base_Cost_BO,
case when b.order_type = 1 then (b.order_qty*c.po_cost) else 0 end as Ext_Base_Cost_ALLOC

FROM ods_ca.ods_cis_corp_order_header_rt a
inner join ods_ca.ods_cis_corp_order_detail_rt b
	on a.order_no=b.order_no
	and a.order_type=b.order_type
inner join tempdb.rds_sku_6302 c
	on b.sku_no=c.sku_no
where a.order_type in(1,8)
and a.ship_date is null
and a.delete_date is null
and b.delete_date is null
and b.order_qty - ifnull(b.ship_qty,0) <> 0
;




drop table if exists tempdb.rds_inv_rio_6302;
create table tempdb.rds_inv_rio_6302 as
select distinct
c.sku_no,
rrh.cust_no,
rrh.rio_req_no,
date_format(rrh.entry_datetime,'%m/%d/%Y') as entry_datetime,
rd.inproc_ref_no as inproc_ref_no ,
rrh.hold_auth_no,
rrh.ref_descr as ref_no_description,
date_format(rrh.approve_datetime,'%m/%d/%Y') as approve_datetime,
date_format(rrh.end_date,'%m/%d/%Y') as end_date,
rrh.approve_id,
m.loginid as approve_name,
rrh.loc_no,
-- loc_char = convert(varchar(50),null),
c.part_no,
c.mfg_partno,
ifnull(rrh.kit_flag, 'S') as kit_flag,
pm.ave_cost as unit_cost,
-- ext_base_cost_ord = convert(money,null),
-- ext_base_cost_bo = convert(money,null),
-- ext_base_cost_alloc = convert(money,null),
rrh.req_qty,
(	select sum(ifnull(hold_qty, 0))
	from ods_ca.ods_cis_corp_rio_req_detail_rt rrd
	where rrd.rio_req_no = rrh.rio_req_no
	and rrd.inproc_ref_type = 18) as rio_reserved_qty,
(   select sum(ifnull(hold_qty, 0))
    from ods_ca.ods_cis_corp_rio_req_detail_rt rrd
    where rrd.rio_req_no = rrh.rio_req_no
    and rrd.inproc_ref_type in (2,4)) as  rio_po_mt_qty,
-- rio_open_qty = convert(int,null),
(
  select ifnull(sum(ifnull(c.to_order_qty, 0)), 0)
  from ods_ca.ods_cis_corp_rio_req_consumed_rt c
  where c.rio_req_no = rrh.rio_req_no
  and c.to_order_no != - 1
  and c.to_order_type in (select cast(code_value as int)
                          from ods_ca.ods_cis_corp_list_box_detail_rt
                          where list_box_code = 'RCT'
                          )
                        ) as rio_consumed_qty

from ods_ca.ods_cis_corp_rio_request_header_rt rrh
inner join tempdb.rds_sku_6302 c
	on rrh.sku_no = c.sku_no
left join ods_ca.ods_cis_corp_manager_rt m
	on m.userid = rrh.approve_id
left join ods_ca.ods_cis_corp_rio_req_detail_rt rd
	on rrh.rio_req_no = rd.rio_req_no
	and rd.inproc_ref_type = 18
left join ods_ca.ods_cis_corp_part_master_rt pm
	on c.sku_no = pm.sku_no
where rrh.status = 'A' --and rrh.status <> 'D'
and ((rrh.type = 'F' and rrh.approved_qty > 0) or rrh.type = 'R')
and rrh.company_no = 1
;



drop table if exists tempdb.rds_inv_rio1_6302;
create table tempdb.rds_inv_rio1_6302 PRIMARY KEY(id) DISTRIBUTED BY HASH(id)  as
select distinct
uuid_numeric() as id,
a.sku_no,
a.cust_no,
a.rio_req_no,
a.entry_datetime,
a.inproc_ref_no ,
a.hold_auth_no,
a.ref_no_description,
a.approve_datetime,
a.end_date,
a.approve_id,
a.approve_name,
a.loc_no,
-- loc_char = convert(varchar(50),null),
a.part_no,
a.mfg_partno,
a.kit_flag,
a.unit_cost,
null as ext_base_cost_ord,
null as ext_base_cost_bo,
null as ext_base_cost_alloc,
a.req_qty,
a.rio_reserved_qty,
a.rio_po_mt_qty,
(a.req_qty - ifnull(a.rio_reserved_qty, 0) - ifnull(a.rio_consumed_qty, 0) - ifnull(a.rio_po_mt_qty, 0)) as rio_open_qty,
a.rio_consumed_qty
from tempdb.rds_inv_rio_6302 a
;





drop table if exists tempdb.sku_6302;
create table tempdb.sku_6302 as
select distinct sku_no
from tempdb.rds_inv_rio1_6302
where kit_flag != 'S'
;

drop table if exists tempdb.var_6302;
create table tempdb.var_6302 as
select t.sku_no
        ,ifnull(sum(bcv.cost_variance), 0) as cost
from ods_ca.ods_cis_corp_bom_cost_var_rt bcv
inner join ods_ca.ods_cis_corp_exp_codes_rt ec
        on bcv.exp_code = ec.exp_code
inner join tempdb.sku_6302 t
        on t.sku_no = bcv.sku_no
where (ec.start_date is null or ec.start_date <= current_date())
and ( ec.end_date is null or ec.end_date >= current_date())
group by t.sku_no
;


drop table if exists tempdb.base_6302;
create table tempdb.base_6302 as
select t.sku_no
      ,sum(pm.po_cost * bm.comp_qty) as cost
from ods_ca.ods_cis_corp_bom_rt bm
inner join tempdb.sku_6302 t
	on bm.sku_no = t.sku_no
inner join ods_ca.ods_cis_corp_part_master_rt pm
    on bm.comp_no = pm.sku_no
-- where t.flag = 'P'
group by t.sku_no
;



update tempdb.rds_inv_rio1_6302
set unit_cost = t.cost
from tempdb.base_6302 t
where rds_inv_rio1_6302.sku_no = t.sku_no
;

update tempdb.rds_inv_rio1_6302
set unit_cost = unit_cost + ifnull(t.cost, 0)
from tempdb.var_6302 t
where rds_inv_rio1_6302.sku_no = t.sku_no
;

update tempdb.rds_inv_rio1_6302
set ext_base_cost_ord = unit_cost * ifnull(rio_reserved_qty, 0),
    ext_base_cost_bo = unit_cost * ifnull(rio_open_qty, 0),
    ext_base_cost_alloc = unit_cost * ifnull(rio_reserved_qty, 0)
;



insert into tempdb.temp_6302 (
id,sku_no, CUST_NUM, RIO_Req_No, RIO_Request_Date, RIO_No, Ref_No, Ref_No_Description, RIO_Approve_Date, RIO_Expiration_Date, RIO_Approved, from_loc_no,
PART_NO, VNDR_PROD_NO,
RIO_Req_Qty, RIO_Reserved_Orders, RIO_PO_MT_Qty, RIO_Open_Qty, Consumed_Qty,
Base_Cost ,Ext_Base_Cost_ORD, Ext_Base_Cost_BO, Ext_Base_Cost_ALLOC
)
select
id,sku_no, cust_no, rio_req_no, entry_datetime, inproc_ref_no, hold_auth_no, ref_no_description, approve_datetime, end_date, approve_name, loc_no,
part_no, mfg_partno,
req_qty, rio_reserved_qty, rio_po_mt_qty, rio_open_qty, rio_consumed_qty,
unit_cost, ext_base_cost_ord, ext_base_cost_bo, ext_base_cost_alloc
from tempdb.rds_inv_rio1_6302
;


-- VEN_PO



update tempdb.temp_6302
set VEN_PO=b.order_no
from ods_ca.ods_cis_corp_order_header_rt b
where temp_6302.order_no = b.int_ref_no
and temp_6302.order_type = b.int_ref_type
and b.order_type = 1
;

     --for backorders--

update tempdb.temp_6302
set VEN_PO = b.int_ref_no
from ods_ca.ods_cis_corp_mc_order_ref_rt b
where b.order_no = temp_6302.order_no
and b.order_type = temp_6302.order_type
and b.order_line_no = temp_6302.LINE_NO
and temp_6302.order_type = 8
and b.int_ref_type = 2
and ifnull(b.status,'A') != 'E'
;



update tempdb.temp_6302
set CUST_NAME=b.cust_name
from ods_ca.ods_cis_corp_customer_header_rt b
where temp_6302.CUST_NUM=b.cust_no
;


-- EndUserPurchaseOrderNo
update tempdb.temp_6302
set END_USER_PO=b.end_user_po
from ods_ca.ods_cis_corp_order_soldto_rt b
where temp_6302.order_no=b.order_no
and temp_6302.order_type=b.order_type
;

update tempdb.temp_6302
set END_USER_PO=b.end_user_po
from ods_ca.ods_cis_corp_history_soldto_rt b
where temp_6302.order_no=b.order_no
and temp_6302.order_type=b.order_type
;


-- REP_ID and SALES_REP_NME
update tempdb.temp_6302
set REP_ID = b.primary_id
from ods_ca.ods_cis_corp_territory_rt b
where temp_6302.TERR=b.sales_terr
;

update tempdb.temp_6302
set SALES_REP_NME = concat(b.firstname ,' ', b.lastname)
from ods_ca.ods_cis_corp_manager_rt b
where temp_6302.REP_ID=b.userid
;

-- WH
UPDATE tempdb.temp_6302
SET WH = b.loc_char
FROM ods_ca.ods_cis_corp_location_info_rt b
WHERE temp_6302.from_loc_no = b.loc_no
;

-- ETA

drop table if exists tempdb.eta_ca6302;
create table tempdb.eta_ca6302 as
select
		order_no,
		order_type,
		order_line_no,
		sku_no,
		date_format(min(eta),'%m/%d/%Y') as min_eta
   from dm_ca.dm_pur_unieta_boso_detail_rt eta
   group by order_no, order_type, order_line_no,sku_no
   ;

 update  tempdb.temp_6302
 set ETA = b.min_eta
 from tempdb.eta_ca6302 b
 where temp_6302.sku_no=b.sku_no
 and temp_6302.order_no = b.order_no
 and temp_6302.order_type = b.order_type
 and temp_6302.sku_no=b.sku_no
;


drop table if exists tempdb.rds_tmp;
create table tempdb.rds_tmp as
select
CUST_NUM,
CUST_NAME,

RIO_Req_No,
RIO_Request_Date,
RIO_No,
Ref_No,
Ref_No_Description,
RIO_Approve_Date,
RIO_Expiration_Date,
RIO_Approved,

ORDR_ENTRY_DATE,
REP_ID,
TERR,
SALES_REP_NME,
order_no as 'ORDER',
LINE_NO,
WH,
CUSTOMER_PO,
END_USER_PO,
short_desc as 'DESC',
PLINE,
PART_NO,
VNDR_PROD_NO,
QTY_ORD,
QTY_ALLOC,
QTY_BO,

RIO_Req_Qty,
RIO_Reserved_Orders,
RIO_PO_MT_Qty,
RIO_Open_Qty,
Consumed_Qty,

EXTND_PRICE,
STAT_CODE,
SHIP_VIA,
SHIP_TO_ADDR_LINE,
SHIP_TO_CITY_NAME,
SHIP_TO_STATE,
SHIP_TO_POSTAL_CODE,
CUST_AVAIL_SHIP_DATE,
ETA,
VEN_PO,
SHIP_TO_NAME,
Base_Cost,
Ext_Base_Cost_ORD,
Ext_Base_Cost_BO,
Ext_Base_Cost_ALLOC
from tempdb.temp_6302
order by order_no,LINE_NO,PART_NO
;


drop table if exists tempdb.rds_tmp_body;
create table tempdb.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from tempdb.rds_tmp
;