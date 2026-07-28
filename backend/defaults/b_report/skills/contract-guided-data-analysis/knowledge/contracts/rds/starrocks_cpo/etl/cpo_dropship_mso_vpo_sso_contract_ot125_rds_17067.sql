drop table if exists tempdb.req_us17067;

create table tempdb.req_us17067 (
  `cpo_id` int(11) null,
  `Calendar_Day` varchar(10) null,
  `Sold_To_Party` varchar(200) null,
  `Region` varchar(200) null,
  `End_Customer` varchar(200) null,
  `Drop_Ship_Flag` varchar(1) null,
  `Reservation_Flag` varchar(1) null,
  `cpo_line_seq` int(11) null,
  `MSO` int(11) null,
  `VPO` int(11) null,
  `SSO` int(11) null,
  `contract_no` int(11) null,
  `OT125` int(11) null,
  `vend_no` int(11) null,
  `vpl_no` int(11) null,
  `vend_name` varchar(80) null,
  `Customer_PO_Number` varchar(200) null,
  `pcode` varchar(80) null,
  `pcode_desc` varchar(80) null,
  `category` varchar(80) null,
  `global_cat_type` varchar(80) null,
  `VPG` varchar(80) null,
  `VPG_DESC` varchar(80) null,
  `End_User_State` varchar(80) null
)
;

insert into tempdb.req_us17067
select
	distinct
    ch.cpo_id,
    date_format(ch.convert_datetime ,'%m/%d/%Y')as Calendar_Day,
    cth.cust_name as Sold_To_Party,
    adr.state as Region,
    case
        when cec.eu_company_name is null then cec1.eu_company_name
        else cec.eu_company_name
    end as End_Customer,
    case when (oh.order_no is not null) or (cp.profile_i is not null or hcp.profile_i is not null) then 'Y' ELSE 'N' END as Drop_Ship_Flag,
    case when op.order_no is not null then 'Y' ELSE 'N' END as Reservation_Flag,
    cd.cpo_line_seq,
    oh.order_no as MSO,
    vpo.order_no as VPO,
    sso.order_no as SSO,
	case when cp.profile_i is null then hcp.profile_i else cp.profile_i end as contract_no,
    case when obe.order_no is null then obe1.order_no else obe.order_no end as OT125,
    pm.vend_no,
    pm.vpl_no,
    pm.vend_name,
    ch.cpo_no as Customer_PO_Number,
    pm.pcode as pcode,
    pm.pcode_desc as pcode_desc,
    pm.category as category,
    pm.global_cat_type as global_cat_type,
    pm.vpl_code as VPG,
    vpg.vpc_group_desc as VPG_DESC,
    case when cec.eu_loc_state is null then cec1.eu_loc_state else cec.eu_loc_state end as End_User_State
from
    ods_us.ods_cis_corp_cpo_header_rt ch
join
    ods_us.ods_cis_corp_cpo_detail_rt cd
    on ch.cpo_id = cd.cpo_id
left join
	   ods_us.ods_cis_corp_cpo_eu_common_rt	cec
    on ch.cpo_id = cec.cpo_id
left join
    ods_us.ods_cis_corp_history_cpo_eu_common_rt cec1
    on ch.cpo_id = cec1.cpo_id
join
    dim_us.dim_pub_part_info pm
    on cd.cpo_sku_no = pm.sku_no
join
    ods_us.ods_cis_corp_customer_header cth
    on ch.reseller_cust_no = cth.cust_no
left join ods_us.ods_cis_corp_order_detail_rt oh
on oh.order_type = 1 and oh.int_ref_no = ch.cpo_id and oh.delete_date is null and oh.int_ref_line_no = cd.cpo_line_seq
left join ods_us.ods_cis_corp_order_detail_rt vpo
on vpo.order_type = 2 and vpo.int_ref_type = 1 and oh.order_no = vpo.int_ref_no and vpo.int_ref_line_no = oh.order_line_no
left join ods_us.ods_cis_corp_order_detail_rt sso
on sso.order_type = 1 and sso.int_ref_type = 2 and sso.int_ref_no = vpo.order_no and sso.int_ref_line_no = vpo.order_line_no
left join ods_us.ods_cis_corp_order_profile_rt op
on oh.order_no = op.order_no and op.order_type = 1 and op.profile_cat = 'ORDR' and op.profile_type = 'RESERVEVPO'
left join ods_us.ods_cis_corp_cpo_profile_rt cp
on ch.cpo_id = cp.cpo_id and cd.cpo_line_no = cp.cpo_line_seq and cp.profile_type = 'CONTRNO' and cp.profile_cat = 'CPOL'
left join ods_us.ods_cis_corp_history_cpo_profile_rt hcp
on ch.cpo_id = hcp.cpo_id and cd.cpo_line_no = hcp.cpo_line_seq and hcp.profile_type = 'CONTRNO' and hcp.profile_cat = 'CPOL'
left join ods_us.ods_cis_corp_ot125_billing_entry obe
on cp.profile_i = obe.contract_no and cp.cpo_line_seq = obe.contract_line_no
left join ods_us.ods_cis_corp_ot125_billing_entry obe1
on hcp.profile_i = obe1.contract_no  and hcp.cpo_line_seq = obe1.contract_line_no
left join ods_us.ods_cis_corp_addr_xref_rt ax
on ch.reseller_cust_no = ax.xref_no and ax.xref_seq = 1 and ax.xref_type = 'ADDR_CUST'
left join ods_us.ods_cis_corp_address_rt adr
on adr.addr_no = ax.addr_no
left join ods_us.ods_cis_corp_vpc_group_xref_rt vpx
on pm.vpl_no = vpx.vpl_no
left join ods_us.ods_cis_corp_vpc_group_rt vpg
on vpx.vpc_group_id = vpg.vpc_group_id and vpg.group_code = 'BRPT'
where
    ch.convert_datetime between DATE_FORMAT(date_add(current_date(),interval -1 day), '%Y-%m-01') AND  current_date()
    and pm.vend_no in (96378,75432,75062,54254,74771,75063,96248,96432,96273,95764,96420,96072,96403,96438,75596,96380,96378,96378)
    and ch.cpo_sales_terr in (4404, 4405)
UNION
select
    ch.cpo_id,
    date_format(ch.convert_datetime ,'%m/%d/%Y') as Calendar_Day,
    cth.cust_name as Sold_To_Party,
    adr.state as Region,
    case
        when cec.eu_company_name is null then cec1.eu_company_name
        else cec.eu_company_name
    end as End_Customer,
    case when (oh.order_no is not null) or (cp.profile_i is not null or hcp.profile_i is not null) then 'Y' ELSE 'N' END as Drop_Ship_Flag,
    case when op.order_no is not null then 'Y' ELSE 'N' END as Reservation_Flag,
    cd.cpo_line_seq,
    oh.order_no as MSO,
    vpo.order_no as VPO,
    sso.order_no as SSO,
	case when cp.profile_i is null then hcp.profile_i else cp.profile_i end as contract_no,
    case when obe.order_no is null then obe1.order_no else obe.order_no end as OT125,
    pm.vend_no,
    pm.vpl_no,
    pm.vend_name,
    ch.cpo_no as Customer_PO_Number,
    pm.pcode as pcode,
    pm.pcode_desc as pcode_desc,
    pm.category as category,
    pm.global_cat_type as global_cat_type,
    pm.vpl_code as VPG,
    vpg.vpc_group_desc as VPG_DESC,
    case when cec.eu_loc_state is null then cec1.eu_loc_state else cec.eu_loc_state end as End_User_State
from
    ods_us.ods_cis_corp_history_cpo_header_rt ch
join
    ods_us.ods_cis_corp_history_cpo_detail_rt cd
    on ch.cpo_id = cd.cpo_id
left join
	   ods_us.ods_cis_corp_cpo_eu_common_rt	cec
    on ch.cpo_id = cec.cpo_id
left join
    ods_us.ods_cis_corp_history_cpo_eu_common_rt cec1
    on ch.cpo_id = cec1.cpo_id
join
    dim_us.dim_pub_part_info pm
    on cd.cpo_sku_no = pm.sku_no
join
    ods_us.ods_cis_corp_customer_header cth
    on ch.reseller_cust_no = cth.cust_no
left join ods_us.ods_cis_corp_history_detail_rt oh
on oh.order_type = 1 and oh.int_ref_no = ch.cpo_id and oh.delete_date is null and oh.int_ref_line_no = cd.cpo_line_seq
left join ods_us.ods_cis_corp_history_detail_rt vpo
on vpo.order_type = 2 and vpo.int_ref_type = 1 and oh.order_no = vpo.int_ref_no and vpo.int_ref_line_no = oh.order_line_no
left join ods_us.ods_cis_corp_history_detail_rt sso
on sso.order_type = 1 and sso.int_ref_type = 2 and sso.int_ref_no = vpo.order_no and sso.int_ref_line_no = vpo.order_line_no
left join ods_us.ods_cis_corp_history_profile_rt op
on oh.order_no = op.order_no and op.order_type = 1 and op.profile_cat = 'ORDR' and op.profile_type = 'RESERVEVPO'
left join ods_us.ods_cis_corp_cpo_profile_rt cp
on ch.cpo_id = cp.cpo_id and cd.cpo_line_no = cp.cpo_line_seq and cp.profile_type = 'CONTRNO' and cp.profile_cat = 'CPOL'
left join ods_us.ods_cis_corp_history_cpo_profile_rt hcp
on ch.cpo_id = hcp.cpo_id and cd.cpo_line_no = hcp.cpo_line_seq and hcp.profile_type = 'CONTRNO' and hcp.profile_cat = 'CPOL'
left join ods_us.ods_cis_corp_ot125_billing_entry obe
on cp.profile_i = obe.contract_no and cp.cpo_line_seq = obe.contract_line_no
left join ods_us.ods_cis_corp_ot125_billing_entry obe1
on hcp.profile_i = obe1.contract_no  and hcp.cpo_line_seq = obe1.contract_line_no
left join ods_us.ods_cis_corp_addr_xref_rt ax
on ch.reseller_cust_no = ax.xref_no and ax.xref_seq = 1 and ax.xref_type = 'ADDR_CUST'
left join ods_us.ods_cis_corp_address_rt adr
on adr.addr_no = ax.addr_no
left join ods_us.ods_cis_corp_vpc_group_xref_rt vpx
on pm.vpl_no = vpx.vpl_no
left join ods_us.ods_cis_corp_vpc_group_rt vpg
on vpx.vpc_group_id = vpg.vpc_group_id and vpg.group_code = 'BRPT'
where
    ch.convert_datetime between DATE_FORMAT(date_add(current_date(),interval -1 day), '%Y-%m-01') AND  current_date()
    and pm.vend_no in (96378,75432,75062,54254,74771,75063,96248,96432,96273,95764,96420,96072,96403,96438,75596,96380,96378,96378)
    and ch.cpo_sales_terr in (4404, 4405)
;

drop table if exists tempdb.rds_tmp;

create table tempdb.rds_tmp (
  `cpo_id` int(11) null,
  `Calendar_Day` varchar(10) null,
  `Sold_To_Party` varchar(200) null,
  `Region` varchar(200) null,
  `End_Customer` varchar(200) null,
  `Drop_Ship_Flag` varchar(1) null,
  `Reservation_Flag` varchar(1) null,
  `cpo_line_seq` int(11) null,
  `MSO` int(11) null,
  `VPO` int(11) null,
  `SSO` int(11) null,
  `contract_no` int(11) null,
  `OT125` int(11) null,
  `vend_no` int(11) null,
  `vpl_no` int(11) null,
  `vend_name` varchar(80) null,
  `Customer_PO_Number` varchar(200) null,
  `pcode` varchar(80) null,
  `pcode_desc` varchar(80) null,
  `category` varchar(80) null,
  `global_cat_type` varchar(80) null,
  `VPG` varchar(80) null,
  `VPG_DESC` varchar(80) null,
  `End_User_State` varchar(80) null,
  `Extended_Cost_DC` varchar(80) null,
  `Extended_Resales_in_DC` varchar(80) null,
  `line_gm` varchar(80) null
);

insert into tempdb.rds_tmp
select
a.cpo_id,a.Calendar_Day,a.Sold_To_Party,a.Region,a.End_Customer,a.Drop_Ship_Flag,a.Reservation_Flag,a.cpo_line_seq,a.MSO,a.VPO,a.SSO,a.contract_no,a.OT125,a.vend_no,a.vpl_no,a.vend_name,a.Customer_PO_Number,a.pcode,a.pcode_desc,a.category,a.global_cat_type,a.VPG,a.VPG_DESC,a.End_User_State,
od.unit_cost * od.order_qty as Extended_Cost_DC,
od.unit_price * od.order_qty as Extended_Resales_in_DC,
case when od.unit_price  = 0 then 0 else
((od.unit_price   - od.unit_cost )) / (od.unit_price )* 100
END as line_gm
from tempdb.req_us17067 a
join ods_us.ods_cis_corp_order_detail_rt od
on a.MSO = od.order_no and od.order_type = 1  and a.cpo_line_seq = od.int_ref_line_no
where a.contract_no is null
order by cpo_id;

insert into tempdb.rds_tmp
select
a.cpo_id,a.Calendar_Day,a.Sold_To_Party,a.Region,a.End_Customer,a.Drop_Ship_Flag,a.Reservation_Flag,a.cpo_line_seq,a.MSO,a.VPO,a.SSO,a.contract_no,a.OT125,a.vend_no,a.vpl_no,a.vend_name,a.Customer_PO_Number,a.pcode,a.pcode_desc,a.category,a.global_cat_type,a.VPG,a.VPG_DESC,a.End_User_State,
od.unit_cost * od.order_qty as Extended_Cost_DC,
od.unit_price * od.order_qty as Extended_Resales_in_DC,
case when od.unit_price  = 0 then 0 else
((od.unit_price   - od.unit_cost )) / (od.unit_price )* 100
END as line_gm
from tempdb.req_us17067 a
join ods_us.ods_cis_corp_history_detail_rt od
on a.MSO = od.order_no and od.order_type = 1  and a.cpo_line_seq = od.int_ref_line_no
where a.contract_no is null
order by cpo_id;

insert into tempdb.rds_tmp
select
a.cpo_id,a.Calendar_Day,a.Sold_To_Party,a.Region,a.End_Customer,a.Drop_Ship_Flag,a.Reservation_Flag,a.cpo_line_seq,a.MSO,a.VPO,a.SSO,a.contract_no,a.OT125,a.vend_no,a.vpl_no,a.vend_name,a.Customer_PO_Number,a.pcode,a.pcode_desc,a.category,a.global_cat_type,a.VPG,a.VPG_DESC,a.End_User_State,
obe.bill_cost * obe.bill_qty as Extended_Cost_DC,
obe.bill_price * obe.bill_qty as Extended_Resales_in_DC,
case when obe.bill_price  = 0 then 0 else
((obe.bill_price   - obe.bill_cost )) / (obe.bill_price )* 100
END as line_gm
from tempdb.req_us17067 a
left join ods_us.ods_cis_corp_ot125_billing_entry obe
on a.contract_no = obe.contract_no and a.cpo_line_seq = obe.contract_line_no
where a.contract_no is not null
order by cpo_id;

create table if not exists tempdb.rds_tmp_body (
body_type varchar(10) null,
cnt int null
)
;

insert into tempdb.rds_tmp_body(body_type,cnt)
select 'Standard', count(*) from tempdb.rds_tmp
;


