/*
Transactions (SITETRAN)
Description:  Provides current values that describe the current inventory transactions needed by Prophet
			  A history of transactions related to defective inventory returns to CSL and the repair of said defective inventory
RDS# 1214
*/


DROP table if exists rds_gfs1214_report;
CREATE local temporary TABLE rds_gfs1214_report
(Material_Code int null,
 Region_Code varchar(15) null,
 Site_Code int null,
 Transaction_Code varchar(20) null,
 Date varchar(8) null,
 Quantity int null)
    ON COMMIT PRESERVE ROWS
;


-- Get Site codes to use later in the logic.  this will match the logic from the SITE file logic
drop table if exists rds_gfs1214_site_code;
create local temporary table rds_gfs1214_site_code on commit preserve rows as
select
    a.loc_no as Site_Code
     ,concat(concat('SHYFT-', case when a.server_ip = 'CSL' then 'DC-' else 'FLD-' end), case when a.company_no = 2203 then 'US' else 'CA' end) as 'Region_Code'
from
    dim_gfs.dim_pub_location_info a
        inner join dim_wcla.dim_gfs_location_info b
                   on a.loc_no = b.loc_no
where
    a.company_no in (2302, 2203)
  and a.server_ip in ('CSL','FSL')		--> FE locations not in scope
  and b.active_flag = 'Y'
;


-- Force repair center PRISM (5079) A 8WIP (3301) into the SITE feed
-- this will be needed for the DEF_TO_REPAIR_INT section further below
insert into rds_gfs1214_site_code
select
    loc_no as Site_Code
     ,case when company_no = 2203 then 'SHYFT-FLD-US' else 'SHYFT-FLD-CA' end as 'Region_Code'
from dim_gfs.dim_pub_location_info
where
    loc_no in (5079, 3301)
  and company_no in (2203, 2302)
;



/* ***   Part 1   *** */
/*
SITETRAN Transaction_Code: DEF_RETURN
Shyft Data Source (From Call): SP07 or second part of a CAP (MRA)
Generic Description : Transaction history of defective inventories moving from the field to defective holding area. By default, Prophet assumes the holding area is the central DC for the network.
*/


/* RMA CAP orders */
-- SP01 CAP RMA are tied to an OT11 and only these records with an OT11 are needed
-- SP13 Returns (Cuat --> FE) need to be exluded and they will NOT have an OT tied to them

insert into rds_gfs1214_report
select
    a.sku_no as 'Material_Code'
    ,d.Region_code
    ,d.Site_Code
    ,'DEF_RETURN' as 'Transaction_Code'
    ,TO_CHAR(DATE_TRUNC('month', a.rma_entry_datetime), 'YYYYMMDD') as 'Date'
    ,sum(rec_qty) as 'Quantity'
from
    dw_gfs.dwd_disty_cs_rma_info a
        inner join dim_gfs.dim_pub_location_info b
                   on a.loc_no = b.loc_no
        inner join dim_wcla.dim_pub_part_info c
                   on a.sku_no = c.sku_no
        inner join rds_gfs1214_site_code d
                   on a.loc_no = d.Site_Code
where
    a.company_no in (2203, 2302)
  and c.vend_no in (22822, 22823)
  and a.vend_segment = 'GFS'
  and a.delete_id is NULL
  and a.rma_status = 'Received'
  and a.rma_type = 'A'							--> A = Advanced Exchange
  and b.server_ip in ('CSL')
  and a.rma_entry_datetime > DATE_TRUNC('MONTH',TIMESTAMPADD(month,-11,current_date()))
group by
     a.sku_no
    ,d.Region_code
    ,d.Site_Code
    ,TO_CHAR(DATE_TRUNC('month', a.rma_entry_datetime), 'YYYYMMDD')
;



/* MT4 SP07 FE Returns */
-- Defective returns from the FE back to the warehouse (CSL)

insert into rds_gfs1214_report
select distinct
    a.sku_no as 'Material_Code'
    ,d.Region_Code
    ,d.Site_Code
    ,'DEF_RETURN' as 'Transaction_Code'
    ,TO_CHAR(DATE_TRUNC('month', a.closed_date), 'YYYYMMDD') as 'Date'
    ,sum(a.rec_qty) as 'Quantity'
from
    dw_gfs.dwd_gfs_pur_mt_detail a
        inner join dim_wcla.dim_pub_part_info b
                   on a.sku_no = b.sku_no
        inner join rds_gfs1214_site_code d
                   on a.to_loc_no = d.Site_Code
where
    a.company_no in (2203, 2302)
  and b.vend_no in (22822, 22823)
  and a.order_type = 4
  and a.gfs_order_type in ('SP07')
  and a.to_loc_type in ('CSL', 'FSL')
  and a.closed_date > DATE_TRUNC('MONTH', TIMESTAMPADD(month, -11, current_date()))
group by
     a.sku_no
    ,d.Region_Code
    ,d.Site_Code
    ,TO_CHAR(DATE_TRUNC('month', a.closed_date), 'YYYYMMDD')
    ;



/* ***   Part 2   *** */
/*
SITETRAN Transaction_Code:  REPAIR_YIELD_INT
Generic Description: Transaction history of defective units that were successfully repaired during the repair process

OT4 from "PRSM" to CSL as a Type 1 inventory (Good)
*/

-- Also missong the profile that connects the OT4 to 8WIP to the OT4 return from 8WIP

drop table if exists rds_gfs1214_temp1;
create local temporary table rds_gfs1214_temp1 on commit preserve rows as
select distinct
     a.sku_no
    ,a.order_type, a.order_no, a.order_line_no
    ,a.from_loc_no
    ,a.to_loc_no
    ,a.to_loc_type
    ,a.rec_qty
    ,cast(b.profile_c as integer) as profile_c
    ,d.Region_Code
    ,d.Site_code
    ,'REPAIR_YIELD_INT' as 'Transaction_Code'
    ,TO_CHAR(DATE_TRUNC('month', a.closed_date), 'YYYYMMDD') as 'Date'
from
    dw_gfs.dwd_gfs_pur_mt_detail a
    left join dw_wcla.dwd_pub_common_order_profile_lightweight b
              on a.order_no = b.order_no and
                 a.order_type = b.order_type
                  and b.profile_type = 'SF_ORD_NO'
                  and b.active = 'Y'
    inner join dim_wcla.dim_pub_part_info c
               on a.sku_no = c.sku_no
    inner join rds_gfs1214_site_code d
               on a.to_loc_no = d.Site_Code
where
--   a.company_no in (2203, 2302)				-- REmoved CA frpom this for now as the profle SF_ORD_NO to link the order from 33-->8WIP and 8WIP-->33 does NOt exist
    a.company_no in (2203)				-- 2203 = US ONLY
  and c.vend_no in (22822, 22823)
  and a.order_type = 4
--   and a.from_loc_no in (5079,3301)			-- REmoved CA frpom this for now as the profle SF_ORD_NO to link the order from 33-->8WIP and 8WIP-->33 does NOt exist
  and a.from_loc_no in (5079)			-- 5079 = US PRISM ONLY
  and a.from_inv_type = 2
  and a.to_inv_type = 1
  and a.rec_qty is not null					--> to be removed and fixed for delete date when Dean fixes the Vertica Data issue
  and a.closed_date > DATE_TRUNC('MONTH',TIMESTAMPADD(month, -11, current_date()))
;


insert into rds_gfs1214_report
select distinct
    sku_no as 'Material_Code'
    ,Region_Code
    ,Site_Code
    ,Transaction_Code
    ,Date
    ,sum(rec_qty) as 'Quantity'
from rds_gfs1214_temp1
group by
     sku_no
    ,Region_Code
    ,Site_Code
    ,Transaction_Code
    ,Date
;



/* ***   Part 3   *** */
/*
SITETRAN Transaction_Code:  DEF_TO_REPAIR_INT
Generic Description: Transaction history of defective units sent to repair, regardless of the outcome of the repair.

OT4 from CSL to "PRSM" destination (DEFECTIVE)
*/

-- NOTES
-- only send DEF TO repair when there is a return from PRISM
-- shift the date on the order to PRISM to match the date on the return from PRISM
-- expand the 3 month look back to capture long repairs

-- only SEND COMPLETED CASES ?????

drop table if exists rds_gfs1214_temp2;
create local temporary table rds_gfs1214_temp2 on commit preserve rows as
select distinct
     a.sku_no
    ,a.order_type, a.order_no, a.order_line_no
    ,a.from_loc_no
    ,a.to_loc_no
    ,a.ship_qty
    ,x.profile_c
    ,b.Region_Code
    ,b.Site_Code
    ,'DEF_TO_REPAIR_INT' as 'Transaction_Code'
    ,x.Date
from
    rds_gfs1214_temp1 x
    inner join dw_gfs.dwd_gfs_pur_mt_detail a
               on x.order_type = a.order_type and
                  x.profile_c = a.order_no and
                  x.sku_no = a.sku_no
    inner join rds_gfs1214_site_code b
               on a.to_loc_no = b.Site_Code
where
--   a.company_no in (2203, 2302)				-- REmoved CA frpom this for now as the profle SF_ORD_NO to link the order from 33-->8WIP and 8WIP-->33 does NOt exist
    a.company_no in (2203)				-- 2203 = US ONLY
  and a.order_type = 4
--   and a.to_loc_no in (5079,3301)			-- REmoved CA frpom this for now as the profle SF_ORD_NO to link the order from 33-->8WIP and 8WIP-->33 does NOt exist
  and a.to_loc_no in (5079)			-- 5079 = US PRISM ONLY
  and a.from_inv_type = 2
  and a.rec_qty is not null					--> to be removed and fixed for delete date when Dean fixes the Vertica Data issue
;


insert into rds_gfs1214_report
select
    sku_no as 'Material_Code'
    ,Region_Code
    ,Site_Code
    ,Transaction_Code
    ,Date
    ,sum(ship_qty) as 'Quantity'
from rds_gfs1214_temp2
group by
     sku_no
    ,Region_Code
    ,Site_Code
    ,Transaction_Code
    ,Date
;



-- select * from rds_gfs1214_report;



drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select *
from rds_gfs1214_report
;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
     ,'Standard' as body_type
     ,count(*) as cnt
from rdsetl.rds_tmp
;



drop table if exists rds_gfs1214_report;
drop table if exists rds_gfs1214_site_code;

