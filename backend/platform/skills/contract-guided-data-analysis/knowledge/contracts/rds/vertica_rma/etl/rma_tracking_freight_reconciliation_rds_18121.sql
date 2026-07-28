set time zone to 'America/Los_Angeles';

drop table if exists rds_us18121_rma_track_no;
create local temporary table rds_us18121_rma_track_no on commit preserve rows as
select distinct rma_track_no
from dw_us.dwd_disty_cs_rma_info
where vend_segment = 'SHF'
;

drop table if exists rds_us18121_track;
create local temporary table rds_us18121_track on commit preserve rows as
select distinct a.report_no
    ,a.carrier_code
    ,a.invoice_no
    ,a.invoice_date
    ,a.line_no
    ,a.track_no
    ,a.cust_ref_no
    ,a.weight
    ,a.dimweight
    ,a.order_type
    ,a.order_no
    ,a.bill_to_acct
    ,a.bill_to_name
    ,a.paid_amount
    ,a.edi_charge
    ,a.doc_no
    ,a.shipper_address1
    ,a.shipper_name
    ,a.shipper_state
    ,a.shipper_city
    ,a.shipper_zip
    ,a.shipper_company
    ,a.recv_address1
    ,a.recv_name
    ,a.recv_state
    ,a.recv_city
    ,a.recv_zip
    ,a.recv_company
    ,a.FRT_amt_edi
    ,a.FRT_disc_edi
    ,a.FRT_amt_plus_disc_edi
    ,a.FRT_sur_edi
    ,a.FRT_IVACCT
    ,a.FRT_SP
    ,a.FRT_OUTDEL
    ,a.FRT_res_edi
    ,a.FRT_addcr_edi
    ,a.FRT_sec_edi
    ,a.FRT_IDL_edi
    ,a.FRT_LFT_edi
    ,a.FRT_OVR_edi
    ,a.FRT_OVR_edi1
    ,a.FRT_SCC_edi
    ,a.FRT_BYD
    ,a.FRT_NA
    ,a.WTV
    ,a.Others
    ,a.length
    ,a.width
    ,a.height
    ,a.charge_desc
    ,a.gl_type
    ,a.report_week
    ,a.dataset_snapshot
    ,substr(a.track_no,2) as track_no_like
from dw_us.dwd_disty_ap_freight_none_order_view a
where a.report_week = current_date()-8
;

DROP TABLE IF EXISTS rdsetl.rds_tmp;
CREATE TABLE IF NOT EXISTS rdsetl.rds_tmp as
select distinct a.report_no
    ,a.carrier_code
    ,a.invoice_no
    ,a.invoice_date
    ,a.line_no
    ,a.track_no
    ,a.cust_ref_no
    ,a.weight
    ,a.dimweight
    ,a.order_type
    ,a.order_no
    ,a.bill_to_acct
    ,a.bill_to_name
    ,a.paid_amount
    ,a.edi_charge
    ,a.doc_no
    ,a.shipper_address1
    ,a.shipper_name
    ,a.shipper_state
    ,a.shipper_city
    ,a.shipper_zip
    ,a.shipper_company
    ,a.recv_address1
    ,a.recv_name
    ,a.recv_state
    ,a.recv_city
    ,a.recv_zip
    ,a.recv_company
    ,a.FRT_amt_edi
    ,a.FRT_disc_edi
    ,a.FRT_amt_plus_disc_edi
    ,a.FRT_sur_edi
    ,a.FRT_IVACCT
    ,a.FRT_SP
    ,a.FRT_OUTDEL
    ,a.FRT_res_edi
    ,a.FRT_addcr_edi
    ,a.FRT_sec_edi
    ,a.FRT_IDL_edi
    ,a.FRT_LFT_edi
    ,a.FRT_OVR_edi
    ,a.FRT_OVR_edi1
    ,a.FRT_SCC_edi
    ,a.FRT_BYD
    ,a.FRT_NA
    ,a.WTV
    ,a.Others
    ,a.length
    ,a.width
    ,a.height
    ,a.charge_desc
    ,a.gl_type
    ,a.report_week
    ,a.dataset_snapshot
from rds_us18121_rma_track_no b
inner join rds_us18121_track a
on b.rma_track_no like '%'||a.track_no_like||'%'
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
-- 2
