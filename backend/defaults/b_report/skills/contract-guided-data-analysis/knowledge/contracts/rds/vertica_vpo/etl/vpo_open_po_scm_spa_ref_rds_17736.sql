drop table if exists rdsetl.rds_tmp;
drop table if exists rdsetl.rds_tmp_body;

drop table if exists us_rds_17736_po;
create local temporary table us_rds_17736_po on commit preserve rows as
select to_loc_no 	as "CM#",
	order_type,	order_no  , order_line_no,-- order_qty,
	sku_no, part_no as  "Part#",
	ifnull(order_qty,0)*ifnull(unit_cost ,0)as "Base Cost Total",
	sales_rel_date 	as "Release Date",
	ship_to_name ,
    ship_to_addr,
    ship_to_city,
    ship_to_zip,
    ship_to_state,
    ship_to_country
from dw_us.dwd_disty_common_po_basic
where  order_type = 2  
	and entry_datetime >=  date_trunc('month',current_date()-1)
	and entry_datetime < current_date()
	and line_delete_date is null
	and vend_no = 34038
;
 

DROP TABLE IF EXISTS rds_us_17736_spa;
CREATE LOCAL TEMPORARY TABLE rds_us_17736_spa ON COMMIT PRESERVE ROWS AS
select a.order_no
	,a.order_type
	,a.order_line_no
	,b.scm_no
	,b.spa_no
	,b.spa_ref_no
	,row_number() over(partition by a.order_no,a.order_type,a.order_line_no order by b.scm_no) as rn
from us_rds_17736_po a
inner join dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di b
on a.order_no=b.order_no
and a.order_type=b.order_type
and a.order_line_no=b.order_line_no
;

create table rdsetl.rds_tmp as
select      "CM#",
            a.order_no as "PO#",
         	sku_no,
         	"Part#",
         	"Base Cost Total",
         	"Release Date",
         	ship_to_name ,
             ship_to_addr,
             ship_to_city,
             ship_to_zip,
             ship_to_state,
             ship_to_country,
--	    	max(b.scm_no ) as scm_no,
--	    	max(b.spa_no ) as spa_no,
	    	max(b.spa_ref_no ) as spa_ref_no
from us_rds_17736_po a
left join rds_us_17736_spa b
on a.order_no=b.order_no
and a.order_type=b.order_type
and a.order_line_no=b.order_line_no
and b.rn = 1
group by
           "CM#",
            a.order_no,
         	sku_no,
         	"Part#",
         	"Base Cost Total",
         	"Release Date",
         	ship_to_name ,
            ship_to_addr,
            ship_to_city,
            ship_to_zip,
            ship_to_state,
            ship_to_country
;

create table rdsetl.rds_tmp_body as
select 'standard' as body_type
    ,0 as acct_no
    ,count(*) as cnt
from rdsetl.rds_tmp
;