-- Typical POS example: serial LISTAGG plus authority program enrichment.
-- Source: CA/run/rds_5378_rtv.sp

DROP TABLE IF EXISTS rdsetl.rds_tmp;
DROP TABLE IF EXISTS rdsetl.rds_tmp_body;

DROP TABLE IF EXISTS table_5378_order;
CREATE LOCAL TEMPORARY TABLE table_5378_order ON COMMIT PRESERVE ROWS AS
select 'Synnex Canada' as distributor_name
    ,a.order_no as distributor_invoice_no
    ,to_char(a.invoice_date,'mm/dd/yyyy') as invoice_date
    ,to_char(c.begin_date,'mm/dd/yyyy') as promotion_start_date
    ,to_char(c.expire_date,'mm/dd/yyyy') as promotion_end_date
    ,trim(c.marketing_comment) as brother_promo_id
    ,a.mfg_partno as valid_brother_material
    ,a.ship_qty as quantity_sold
    ,a.ship_qty * (a.unit_price + isnull(a.unit_sum_exp,0)) as end_user_price
    ,a.bill_to_cust_name as bill_to_name
    ,a.bill_to_cust_addr as bill_to_addr
    ,a.bill_to_cust_city as bill_to_city
    ,a.bill_to_cust_zip as bill_to_zip
    ,a.bill_to_cust_state as bill_to_state
    ,a.ship_to_name
    ,a.ship_to_zip
    ,a.ship_to_state
    ,a.ship_qty * (a.unit_price + isnull(a.unit_sum_exp,0)) as invoice_amount
    ,b.spa_ref_no
    ,a.order_line_no
    ,a.order_type
    ,a.sku_no
    ,a.bill_to_cust_no
from dw_ca.dwd_disty_common_pos_di a
left join dw_ca.dwd_pub_common_shipped_order_scm_spa_detail_di b on a.order_no=b.order_no and a.order_type=b.order_type and a.order_line_no=b.order_line_no
left join ods_ca.ods_cis_corp_spa_detail c on a.sku_no=c.sku_no and b.spa_no=c.spa_no
where a.order_line_type != 'Comp'
and a.vend_no in (8707,19173)
and a.date_flag >= trunc(current_date()-1,'month')
and a.date_flag < current_date()
;

DROP TABLE IF EXISTS table_5378_ser_number_list;
CREATE LOCAL TEMPORARY TABLE table_5378_ser_number_list ON COMMIT PRESERVE ROWS AS
select
     fd.order_type
    ,fd.distributor_invoice_no
    ,fd.order_line_no
    ,LISTAGG(DISTINCT ser.ser_no USING PARAMETERS max_length=22048,separator=',',on_overflow='TRUNCATE') as ser_no
from table_5378_order fd
inner join dw_ca.dwd_disty_common_order_serial_no_di ser on fd.order_type=ser.order_type and fd.distributor_invoice_no=ser.order_no and fd.order_line_no=ser.order_line_no
where 1=1
group by
     fd.order_type
    ,fd.distributor_invoice_no
    ,fd.order_line_no
;

DROP TABLE IF EXISTS table_5378_final;
CREATE LOCAL TEMPORARY TABLE table_5378_final ON COMMIT PRESERVE ROWS AS
select a.distributor_name
    ,a.distributor_invoice_no
    ,a.invoice_date
    ,a.promotion_start_date
    ,a.promotion_end_date
    ,a.brother_promo_id
    ,a.valid_brother_material
    ,a.quantity_sold
    ,a.end_user_price
    ,a.bill_to_name
    ,a.bill_to_addr
    ,a.bill_to_city
    ,a.bill_to_zip
    ,a.bill_to_state
    ,a.ship_to_name
    ,a.ship_to_zip
    ,a.ship_to_state
    ,a.invoice_amount
    ,a.spa_ref_no
    ,max(isnull(d.auth_no,d1.auth_no)) as authorization_id
    ,a.order_line_no
    ,a.order_type
    ,snl.ser_no
from table_5378_order a
left join dim_ca.dim_disty_pm_authority_program_sku b on a.sku_no=b.sku_no
left join dim_ca.dim_pub_customer_info c on a.bill_to_cust_no=c.cust_no
left join dim_ca.dim_disty_pm_authority_program_cust d on c.mcust_no=d.cust_no and b.program_id=d.program_id
left join dim_ca.dim_disty_pm_authority_program_cust d1 on a.bill_to_cust_no=d1.cust_no and b.program_id=d1.program_id
left join table_5378_ser_number_list snl on snl.order_type = a.order_type and snl.distributor_invoice_no = a.distributor_invoice_no and snl.order_line_no = a.order_line_no
group by a.distributor_name
    ,a.distributor_invoice_no
    ,a.invoice_date
    ,a.promotion_start_date
    ,a.promotion_end_date
    ,a.brother_promo_id
    ,a.valid_brother_material
    ,a.quantity_sold
    ,a.end_user_price
    ,a.bill_to_name
    ,a.bill_to_addr
    ,a.bill_to_city
    ,a.bill_to_zip
    ,a.bill_to_state
    ,a.ship_to_name
    ,a.ship_to_zip
    ,a.ship_to_state
    ,a.invoice_amount
    ,a.spa_ref_no
    ,a.order_line_no
    ,a.order_type
    ,snl.ser_no
;

CREATE TABLE rdsetl.rds_tmp AS
select distributor_name
    ,distributor_invoice_no
    ,invoice_date
    ,promotion_start_date
    ,promotion_end_date
    ,brother_promo_id
    ,valid_brother_material
    ,quantity_sold
    ,end_user_price
    ,bill_to_name
    ,bill_to_addr
    ,bill_to_city
    ,bill_to_zip
    ,bill_to_state
    ,ship_to_name
    ,ship_to_zip
    ,ship_to_state
    ,invoice_amount
    ,spa_ref_no
    ,authorization_id
    ,ser_no
from table_5378_final
;

CREATE TABLE rdsetl.rds_tmp_body AS
select 'Standard' as body_type
    ,0 as acct_no
    ,count(*) as cnt
from rdsetl.rds_tmp
;
