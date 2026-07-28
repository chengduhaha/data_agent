DROP TABLE IF EXISTS rds_us19106_rtv;
CREATE LOCAL TEMPORARY TABLE rds_us19106_rtv ON COMMIT PRESERVE ROWS AS
select a.order_no,
	a.order_type,
	a.order_line_no,
	a.part_no,
	p.mfg_partno,
	sum(d.on_hand_qty - d.bo_qty + d.intran_in - d.intran_out - d.alloc_qty) as avail
from dw_us.dwd_disty_ap_hold_df a
inner join ods_us.ods_cis_corp_part_master p
on a.sku_no = p.sku_no
left join dw_us.dwd_disty_inv_qty_df d
on a.sku_no = d.sku_no
where a.rec_datetime >= current_date() - 7
and a.rec_datetime <= current_date()
and a.vend_no in (74552)
and p.vpl_no in (100240)
and d.date_flag = current_date() - 1
and d.inv_type in (1, 300)
and a.part_no in ('TDX-21R1002SUS-AP-NT', 'TDX-40AY0090US-NT', 'TDX-GW2790-NT', 'TDX-920-002714-NT', 'TDX-F8E089-BLK-NT')
group by a.order_no,
	a.order_type,
	a.order_line_no,
	a.part_no,
	p.mfg_partno
;

drop table if exists rdsetl.rds_tmp;
CREATE TABLE rdsetl.rds_tmp AS
select order_no as "Order#",
	order_type as "Order Type",
	order_line_no as "Order Line",
	part_no as "Part Number",
	mfg_partno as "Mfg Part",
	avail as "Current Availability"
from rds_us19106_rtv
;

drop table if exists rdsetl.rds_tmp_body;
CREATE TABLE rdsetl.rds_tmp_body AS
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp
;
