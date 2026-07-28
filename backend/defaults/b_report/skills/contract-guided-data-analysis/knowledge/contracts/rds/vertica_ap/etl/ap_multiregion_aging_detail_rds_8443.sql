
DROP TABLE IF EXISTS rds_hyve_report_8443;
CREATE LOCAL TEMPORARY TABLE rds_hyve_report_8443 ON COMMIT PRESERVE ROWS AS
SELECT  'HYUS'  as Region,
    date_flag,
    vend_no,
    vend_name,
    vend_type,
    ap_hold_flag,
    vend_currency,
    pas_code,
    total_doc_amt AS vouched_amt,
    unvouched_amt,
    total_amt AS ap_total_amt,
    inv_cost,
    COALESCE(ap_position, total_amt - inv_cost) AS ap_position,
    terms_desc,
    current_amt,
    age1  AS "1-30",
    age2  AS "31-60",
    age3  AS "61-90",
    age4  AS "91-180",
    age5  AS "181-365",
    age6  AS "> 90",
    age7  AS ">180",
    age8  AS "> 365",
    week1	as '1-7',
 	week2	as '8-14',
 	week3	as '15-21',
 	week4	as '22-28',
 	week5	as '>28',
    discontinued,
    restricted,
    vend_segmen_desc,
    cn_analyst_loginid as CN_Analyst,
    analyst_loginid as AP_Analyst
FROM dm_hyus.dm_ap_aging_header_df
WHERE date_flag = CURRENT_DATE() - INTERVAL '1' DAY
  AND sum_level = 'V'

 UNION ALl
 SELECT  'HYUK'  as Region,
    date_flag,
    vend_no,
    vend_name,
    vend_type,
    ap_hold_flag,
    vend_currency,
    pas_code,
    total_doc_amt AS vouched_amt,
    unvouched_amt,
    total_amt AS ap_total_amt,
    inv_cost,
    COALESCE(ap_position, total_amt - inv_cost) AS ap_position,
    terms_desc,
    current_amt,
    age1  AS "1-30",
    age2  AS "31-60",
    age3  AS "61-90",
    age4  AS "91-180",
    age5  AS "181-365",
    age6  AS "> 90",
    age7  AS ">180",
    age8  AS "> 365",
    week1	as '1-7',
 	week2	as '8-14',
 	week3	as '15-21',
 	week4	as '22-28',
 	week5	as '>28',
    discontinued,
    restricted,
    vend_segmen_desc,
    cn_analyst_loginid as CN_Analyst,
    analyst_loginid as AP_Analyst
FROM dm_hyuk.dm_ap_aging_header_df
WHERE date_flag = CURRENT_DATE() - INTERVAL '1' DAY
  AND sum_level = 'V'

 UNION ALl

 SELECT  'HYCN'  as Region,
    date_flag,
    vend_no,
    vend_name,
    vend_type,
    ap_hold_flag,
    vend_currency,
    pas_code,
    total_doc_amt AS vouched_amt,
    unvouched_amt,
    total_amt AS ap_total_amt,
    inv_cost,
    COALESCE(ap_position, total_amt - inv_cost) AS ap_position,
    terms_desc,
    current_amt,
    age1  AS "1-30",
    age2  AS "31-60",
    age3  AS "61-90",
    age4  AS "91-180",
    age5  AS "181-365",
    age6  AS "> 90",
    age7  AS ">180",
    age8  AS "> 365",
    week1	as '1-7',
 	week2	as '8-14',
 	week3	as '15-21',
 	week4	as '22-28',
 	week5	as '>28',
    discontinued,
    restricted,
    vend_segmen_desc,
    cn_analyst_loginid as CN_Analyst,
    analyst_loginid as AP_Analyst
FROM dm_hycn.dm_ap_aging_header_df
WHERE date_flag = CURRENT_DATE() - INTERVAL '1' DAY
  AND sum_level = 'V'

 UNION ALl

 SELECT  'HYWW'  as Region,
    date_flag,
    vend_no,
    vend_name,
    vend_type,
    ap_hold_flag,
    vend_currency,
    pas_code,
    total_doc_amt AS vouched_amt,
    unvouched_amt,
    total_amt AS ap_total_amt,
    inv_cost,
    COALESCE(ap_position, total_amt - inv_cost) AS ap_position,
    terms_desc,
    current_amt,
    age1  AS "1-30",
    age2  AS "31-60",
    age3  AS "61-90",
    age4  AS "91-180",
    age5  AS "181-365",
    age6  AS "> 90",
    age7  AS ">180",
    age8  AS "> 365",
    week1	as '1-7',
 	week2	as '8-14',
 	week3	as '15-21',
 	week4	as '22-28',
 	week5	as '>28',
    discontinued,
    restricted,
    vend_segmen_desc,
    cn_analyst_loginid as CN_Analyst,
    analyst_loginid as AP_Analyst
FROM dm_hyww.dm_ap_aging_header_df
WHERE date_flag = CURRENT_DATE() - INTERVAL '1' DAY
  AND sum_level = 'V'

  ;


DROP TABLE IF EXISTS rds_hyve_ap_aging_detail_8443;
CREATE LOCAL TEMPORARY TABLE rds_hyve_ap_aging_detail_8443 ON COMMIT PRESERVE ROWS AS
WITH temp_detail_report AS (
    WITH temp_tt_rel_ved_pre AS (
        SELECT t.Region,t.vend_no,
               MAX(t.xref_no) AS xref_no,
               CASE
                   WHEN t.xref_type = 'VEND_PURCH' THEN 'PURCHASE'
                   WHEN t.xref_type = 'SRef' THEN 'MARKETING'
                   ELSE NULL
               END AS rel_type
        FROM (
            SELECT DISTINCT vend_no, xref_no, xref_type,Region
            FROM (
                SELECT * , 'HYUS' AS Region FROM dim_hyus.dim_pub_ap_aging_vendor_xref
                UNION ALL
                SELECT * , 'HYUK' AS Region FROM dim_hyuk.dim_pub_ap_aging_vendor_xref
                UNION ALL
                SELECT * , 'HYCN' AS Region FROM dim_hycn.dim_pub_ap_aging_vendor_xref
                UNION ALL
                SELECT * , 'HYWW' AS Region FROM dim_hyww.dim_pub_ap_aging_vendor_xref
            ) vxf
            WHERE xref_type IN ('VEND_PURCH','SRef')
              AND active = 'Y'
              AND vend_no <> xref_no
        ) t
        GROUP BY t.Region,t.vend_no, t.xref_type
    ),
    temp_tt_rel_vd AS (
        SELECT Region,vend_no, xref_no, rel_type
        FROM temp_tt_rel_ved_pre
        UNION ALL
        SELECT Region,xref_no AS vend_no, xref_no, rel_type
        FROM temp_tt_rel_ved_pre
    ),
    temp_tt_vend_ls AS (
        SELECT DISTINCT vi.vend_no, vi.vend_name, 'HYUS' AS Region
        FROM dim_hyus.dim_pub_vendor_info vi
        UNION ALL
        SELECT DISTINCT vi.vend_no, vi.vend_name, 'HYUK' AS Region
        FROM dim_hyuk.dim_pub_vendor_info vi
        UNION ALL
        SELECT DISTINCT vi.vend_no, vi.vend_name, 'HYCN' AS Region
        FROM dim_hycn.dim_pub_vendor_info vi
        UNION ALL
        SELECT DISTINCT vi.vend_no, vi.vend_name, 'HYWW' AS Region
        FROM dim_hyww.dim_pub_vendor_info vi

    )
    SELECT dvl.*
    FROM temp_tt_vend_ls vendf
    INNER JOIN (
        SELECT *, 'HYUS' AS Region FROM dm_hyus.dm_ap_aging_detail_df where  company_no IN (1)
        UNION ALL
        SELECT *, 'HYUK' AS Region FROM dm_hyuk.dm_ap_aging_detail_df where  company_no IN (1)
        UNION ALL
        SELECT *, 'HYCN' AS Region FROM dm_hycn.dm_ap_aging_detail_df where  company_no IN (1)
        UNION ALL
        SELECT *, 'HYWW' AS Region FROM dm_hyww.dm_ap_aging_detail_df -- where  company_no IN (1)
    ) dvl
        ON vendf.vend_no = dvl.vend_no and vendf.Region = dvl.Region
    WHERE dvl.date_flag = CURRENT_DATE() - INTERVAL '1' DAY
      -- AND dvl.company_no IN (1)
),
temp_tt_applied AS (
    SELECT va.Region,va.doc_no,
           SUM(COALESCE(usd_pay_amt, 0) + COALESCE(usd_disc_amt, 0)) AS fx_doc_paid,
           SUM(COALESCE(pay_amt, 0) + COALESCE(disc_amt_taken, 0)) AS doc_paid
    FROM (
        SELECT *,'HYUS' AS Region  FROM ods_hyus.ods_cis_corp_ap_vend_applications
        UNION ALL
        SELECT *,'HYUK' AS Region FROM ods_hyuk.ods_cis_corp_ap_vend_applications
        UNION ALL
        SELECT *,'HYCN' AS Region FROM ods_hycn.ods_cis_corp_ap_vend_applications
        UNION ALL
        SELECT *,'HYWW' AS Region  FROM ods_hyww.ods_cis_corp_ap_vend_applications
    ) va
    WHERE va.doc_no > 0
      AND va.entry_datetime < CURRENT_DATE()
    GROUP BY va.Region,va.doc_no
),
temp_detail_report_rm_dup as(
  select t.* from (
   select dvl.Region
		,dvl.doc_no
		,dvl.vend_no
		,dvl.uv_type
		,dvl.ah_type
		,dvl.vd_type
		,dvl.doc_type
		,dvl.doc_date
		,dvl.doc_due_date
		,dvl.doc_entry_datetime
		,dvl.doc_terms
		,dvl.doc_ref
		,dvl.vend_inv_no
		,dvl.doc_applied
		,dvl.days
		,dvl.inv_disc_date
		,dvl.order_no
		,dvl.order_type
		,dvl.rec_datetime
		,dvl.terms_no
		,dvl.order_line_no
		,dvl.ln
		,dvl.reason_code
		,dvl.rec_no
		,dvl.rec_line_no
		,dvl.terms_desc
		,dvl.terms_days
		,dvl.a_alert_id_ls
		,dvl.disc_amt
		,dvl.doc_amt
		,dvl.part_no
		,dvl.packing_list_no
		,case when ('' = 'CREDIT' and dvl.doc_amt < 0 ) or ('' = 'DEBIT' and dvl.doc_amt > 0) then 0
		      when not (('' = 'CREDIT' and dvl.doc_amt < 0 ) or ('' = 'DEBIT' and dvl.doc_amt > 0)) then
		          (case when 'LOCAL' = 'FX' then COALESCE (dvl.fx_doc_amt,0) else COALESCE (dvl.doc_amt,0) end) - (case when 'LOCAL' = 'FX' then COALESCE (apl.fx_doc_paid,0) else COALESCE (apl.doc_paid,0) end)
		      else dvl.amt end as amt
		,dvl.pm_claim_type
		,dvl.pm_claim_desc
		,dvl.var_no
		,dvl.amt as localamt
		,dvl.usd_amt as usdamt
		,dvl.entry_id
		,dvl.entry_datetime
		,dvl.vend_name
		,dvl.pm_vcm_code
		,dvl.pm_vcm_code_desc
		,dvl.var_no_desc
		,dvl.pm_claim_type_desc
		,dvl.claim_cmmt
		,dvl.claim_cmmt_max_ln
		,dvl.ap_analyst_id
		,dvl.ap_analyst_logid
		,dvl.ap_cnanalyst_id
		,dvl.ap_cnanalyst_logid
		,dvl.vcm_analyst_id
		,dvl.vcm_analyst_logid
		,dvl.org_vend_no
		,dvl.wht_amt
		,dvl.item_type

		,fx_disc_amt
		,fx_doc_amt
		,fx_wht_amt
		,rpt_br_item_type

   ,ROW_NUMBER() OVER(PARTITION BY dvl.doc_no ORDER BY dvl.date_flag) as idn
   from temp_detail_report dvl
   left join temp_tt_applied apl on apl.Region = dvl.Region and apl.doc_no = dvl.doc_no
  ) t where (t.doc_no > 0 and t.idn=1) or t.doc_no <= 0
)
,temp_detail_report_ah as (
	 select
	    dvl.Region
		,dvl.doc_no
		,dvl.vend_no
		,dvl.uv_type
		,dvl.ah_type
		,dvl.vd_type
		,case when dvl.ah_type ='U' then null else dvl.doc_type end as doc_type
		,case when dvl.ah_type ='U' then null else dvl.doc_date end as doc_date
		,case when dvl.ah_type ='U' then null else dvl.doc_due_date end as doc_due_date
		,dvl.doc_entry_datetime
		,case when dvl.ah_type ='U' then null else dvl.doc_terms end as doc_terms
		,dvl.doc_ref
		,dvl.vend_inv_no
		,dvl.doc_applied
		,dvl.days
		,dvl.inv_disc_date
		,dvl.order_no
		,dvl.order_type
		,dvl.rec_datetime
		,dvl.terms_no
		,dvl.order_line_no
		,dvl.ln
		,case when dvl.order_type =27 then dvl.reason_code else null end as reason_code
		,dvl.rec_no
		,dvl.rec_line_no
		,dvl.terms_desc
		,dvl.terms_days
		,dvl.a_alert_id_ls
		,case when 'LOCAL' = 'FX' then COALESCE(dvl.fx_disc_amt,0) else COALESCE(dvl.disc_amt,0) end as disc_amt
		,case when 'LOCAL' = 'FX' then COALESCE(dvl.fx_doc_amt,0) else COALESCE(dvl.doc_amt,0) end as doc_amt
		,dvl.part_no
		,case when dvl.order_type =27 then dvl.packing_list_no else null end as packing_list_no
		,case when dvl.localamt !=0 and 'LOCAL' != 'FX' and dvl.uv_type !='V' then dvl.localamt
		      when dvl.usdamt !=0 and 'LOCAL' = 'FX' and dvl.uv_type !='V' then dvl.usdamt
		      else dvl.amt end as amt
		,dvl.pm_claim_type
		,dvl.pm_claim_desc
		,case when dvl.order_type =27 then dvl.var_no else null end as var_no
		,dvl.localamt
		,dvl.usdamt
		,dvl.entry_id
		,dvl.entry_datetime
		,dvl.idn
		,dvl.vend_name
		,case when dvl.order_type =27 then dvl.pm_vcm_code else null end as pm_vcm_code
		,case when dvl.order_type =27 then dvl.pm_vcm_code_desc else null end as pm_vcm_code_desc
		,case when dvl.order_type =27 then dvl.var_no_desc else null end as var_no_desc
		,case when dvl.order_type =27 then dvl.pm_claim_type_desc else null end as pm_claim_type_desc
		,case when dvl.order_type =27 then dvl.claim_cmmt else null end as claim_cmmt
		,case when dvl.order_type =27 then dvl.claim_cmmt_max_ln else null end as claim_cmmt_max_ln
		,dvl.ap_analyst_id
		,dvl.ap_analyst_logid
		,dvl.ap_cnanalyst_id
		,dvl.ap_cnanalyst_logid
		,dvl.vcm_analyst_id
		,dvl.vcm_analyst_logid
		,case when 'N' !='Y' then null else dvl.org_vend_no end as org_vend_no
		,case when 'LOCAL' = 'FX' then COALESCE(dvl.fx_wht_amt,0) else COALESCE(dvl.wht_amt,0) end as wht_amt
		,dvl.item_type as item_type
	  from temp_detail_report_rm_dup dvl
)
select
     dvl.Region
	,dvl.doc_no
	,dvl.vend_no
	,dvl.uv_type
	,dvl.doc_due_date
	,dvl.doc_entry_datetime
	,dvl.amt
from temp_detail_report_ah dvl
;

DROP TABLE IF EXISTS rds_hyve_ap_aging_8443;
CREATE LOCAL TEMPORARY TABLE rds_hyve_ap_aging_8443 ON COMMIT PRESERVE ROWS AS
WITH RECURSIVE
-- 1. original quarter end
quarter_last_day AS (
SELECT max(date_flag) as original_last_day
FROM dim_us.dim_dw_calendar
WHERE fq = (
		SELECT fq
		FROM dim_us.dim_dw_calendar
		WHERE date_flag = CURRENT_DATE ()
		)

),
-- 2. adjust QE last day
adjusted_last_day AS (
    SELECT
        CASE
            WHEN DAYOFWEEK(original_last_day) IN (5,6,7) -- Thu, Fri, Sat
                THEN original_last_day
            ELSE original_last_day - ((DAYOFWEEK(original_last_day) ) % 7) * INTERVAL '1 day'
        END AS last_day
    FROM quarter_last_day
) ,
   weeks AS (
    SELECT
        1 AS week_no,
        last_day - INTERVAL '6 days' AS week_start,
        last_day AS week_end
    FROM adjusted_last_day
    UNION ALL
    SELECT
        week_no + 1,
        week_start - INTERVAL '7 days',
        week_end - INTERVAL '7 days'
    FROM weeks
    WHERE week_no < 6
)
SELECT
    a.Region,
	a.vend_no,
    SUM(CASE WHEN doc_due_date > w1.week_end THEN amt ELSE 0 END) AS week0,
    SUM(CASE WHEN doc_due_date BETWEEN w1.week_start AND w1.week_end THEN amt ELSE 0 END) AS week1,
    SUM(CASE WHEN doc_due_date BETWEEN w2.week_start AND w2.week_end THEN amt ELSE 0 END) AS week2,
    SUM(CASE WHEN doc_due_date BETWEEN w3.week_start AND w3.week_end THEN amt ELSE 0 END) AS week3,
    SUM(CASE WHEN doc_due_date BETWEEN w4.week_start AND w4.week_end THEN amt ELSE 0 END) AS week4,
    SUM(CASE WHEN doc_due_date BETWEEN w5.week_start AND w5.week_end THEN amt ELSE 0 END) AS week5,
    SUM(CASE WHEN doc_due_date BETWEEN w6.week_start AND w6.week_end THEN amt ELSE 0 END) AS week6,
    SUM(CASE WHEN doc_due_date < w6.week_start THEN amt ELSE 0 END) AS week7
FROM rds_hyve_ap_aging_detail_8443 a
JOIN (SELECT * FROM weeks WHERE week_no = 1) w1 ON 1=1
JOIN (SELECT * FROM weeks WHERE week_no = 2) w2 ON 1=1
JOIN (SELECT * FROM weeks WHERE week_no = 3) w3 ON 1=1
JOIN (SELECT * FROM weeks WHERE week_no = 4) w4 ON 1=1
JOIN (SELECT * FROM weeks WHERE week_no = 5) w5 ON 1=1
JOIN (SELECT * FROM weeks WHERE week_no = 6) w6 ON 1=1
GROUP BY a.Region,
	a.vend_no
;

drop table if exists rds_hyve_final_8443;
create local temporary table rds_hyve_final_8443 on commit preserve rows as
 SELECT
	a.*
	,b.week7 	AS 'Past Due'
	,b.week6 	AS '6 weeks to QE'
	,b.week5	AS '5 weeks to QE'
	,b.week4	AS '4 weeks to QE'
	,b.week3	AS '3 weeks to QE'
	,b.week2	AS '2 weeks to QE'
	,b.week1 	AS 'Last week to QE'
	,b.week0 	AS 'Future week'
FROM rds_hyve_report_8443 a
INNER JOIN rds_hyve_ap_aging_8443 b ON a.Region = b.Region and a.vend_no = b.vend_no
order by a.Region
;

drop table if exists rdsetl.rds_tmp;
create table rdsetl.rds_tmp as
select * from  rds_hyve_final_8443 ;

drop table if exists rdsetl.rds_tmp_body;
create table rdsetl.rds_tmp_body as
select 1 as flag
	,'Standard' as body_type
	,count(*) as cnt
from rdsetl.rds_tmp;