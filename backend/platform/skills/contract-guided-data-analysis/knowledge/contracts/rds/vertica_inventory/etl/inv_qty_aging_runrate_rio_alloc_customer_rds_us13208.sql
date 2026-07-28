-- Typical Inventory example: comprehensive US inventory qty/aging/runrate/RIO/customer output.
-- Source: user-provided US inventory example (vendor 13208)

ALTER SESSION SET PARAMETER WithClauseMaterialization=0;

DROP TABLE IF EXISTS inv_qty_temp;
CREATE LOCAL TEMPORARY TABLE inv_qty_temp ON COMMIT PRESERVE ROWS AS
WITH sku_inv_loc
AS (
	SELECT '2024-04-23' AS date_flag
		,diq.loc_no
		,diq.inv_type
		,diq.sku_no
		,ifnull(iq.ave_cost_sku_cost,0) as ave_cost
		,ifnull(iq.base_cost_sku_cost,0) as base_cost
		,ifnull(iq.ave_cost_fx_sku_cost,0) as ave_cost_fx 
		,ifnull(iq.base_cost_fx_sku_cost,0) as base_cost_fx 
		,CASE 
			WHEN iq.sku_no IS NOT NULL AND pm.prod_type='K' and pm.bundle_kit='Y'
			   THEN iq.kwo_oh_qty
			WHEN iq.sku_no IS NOT NULL AND pm.prod_type!='K'			
			THEN iq.on_hand_qty
			ELSE 0
			END AS on_hand_qty
		,CASE 
			WHEN iq.sku_no IS NOT NULL 
				THEN iq.on_order_qty
			ELSE 0
			END AS on_order_qty
		,CASE 
			WHEN iq.sku_no IS NOT NULL
				THEN iq.bo_qty
			ELSE 0
			END AS bo_qty
		,CASE 
			WHEN iq.sku_no IS NOT NULL
				THEN iq.intran_in
			ELSE 0
			END AS intran_in
		,CASE 
			WHEN iq.sku_no IS NOT NULL
				THEN iq.alloc_qty
			ELSE 0
			END AS alloc_qty
		,CASE 
			WHEN iq.sku_no IS NOT NULL
				THEN iq.wip_qty
			ELSE 0
			END AS wip_qty
		,CASE 
			WHEN iq.sku_no IS NOT NULL
				THEN iq.intran_out
			ELSE 0
			END AS intran_out
		,pm.bundle_kit
		,pm.prod_type
		,pm.mfg_partno
		,pm.part_no
		,pm.prod_code
		,pm.vend_no
		,pm.abc_code
		,pm.vpl_no
		,pm.short_desc
		,pm.long_desc
		,CASE 
			WHEN (pm.mar_end_date < DATE(TO_CHAR(sysdate, 'YYYY-MM-DD')))
				THEN NULL
			ELSE pm.mar_comment
			END AS mar_comment
		,pm.vpl_code
		,pm.weight
		,pm.cu_length
		,pm.cu_width
		,pm.cu_height
		,pm.part_cust_no AS custno
		,pm.forecast_cat
		,pm.fx_flag
		,pm.vend_currency
		,pm.vend_name
		,pm.pp_code
		,pm.pp_data_no
	FROM (
			SELECT DISTINCT loc_no
				,inv_type
				,sku_no
			FROM dw_us.dwd_disty_inv_qty_df
			WHERE date_flag = '2024-04-08'
			UNION
			SELECT DISTINCT a.loc_no
				,a.inv_type
				,a.sku_no
			FROM ods_us.ods_cis_corp_inv_qty a
			LEFT JOIN dw_us.dwd_disty_inv_qty_df b ON a.sku_no = b.sku_no
				AND a.inv_type = b.inv_type
			WHERE b.date_flag ='2024-04-08'
		 ) diq
	LEFT JOIN dw_us.dwd_pub_pur_inv_qty_rt iq ON diq.loc_no = iq.loc_NO
		AND diq.inv_type = iq.inv_type
		AND diq.sku_no = iq.sku_no
	INNER JOIN dim_us.dim_pub_part_info pm ON diq.sku_no = pm.sku_no
	 INNER JOIN dim_us.dim_pub_vendor_info pvi ON pvi.vend_no = pm.vend_no
	WHERE 1 = 2
		 AND (pm.vend_no IN (13208) OR pvi.pur_vend_no IN (13208))
		
		
		
		
		
		 AND pm.prod_type IN ('A','B','K','R','S')
		 AND pm.abc_code IN ('A','B','C','E','T')
		 AND diq.inv_type IN (1)
		
	)
    ,inv_qty_temp
AS (
		SELECT TO_CHAR(diq.date_flag, 'YYYY-MM-DD') AS date_flag
			,diq.loc_no
			,diq.inv_type
			,diq.sku_no
			,ifnull(diq.ave_cost,0) as ave_cost
			,ifnull(diq.base_cost,0) as base_cost
			,ifnull(diq.ave_cost_fx,0) as ave_cost_fx
			,ifnull(diq.base_cost_fx,0) as base_cost_fx
			,case when pm.prod_type='K' and pm.bundle_kit='Y' then diq.kwo_oh_qty else diq.on_hand_qty end as on_hand_qty
			,diq.on_order_qty
			,diq.bo_qty
			,diq.intran_in
			,diq.alloc_qty
			,diq.wip_qty
			,diq.intran_out
			,pm.bundle_kit
			,pm.prod_type
			,pm.mfg_partno
			,pm.part_no
			,pm.prod_code
			,pm.vend_no
			,pm.abc_code
			,pm.vpl_no
			,pm.short_desc
			,pm.long_desc
			,CASE 
				WHEN (pm.mar_end_date < DATE(TO_CHAR(sysdate, 'YYYY-MM-DD')))
					THEN NULL
				ELSE pm.mar_comment
				END AS mar_comment
			,pm.vpl_code
			,pm.weight
			,pm.cu_length
			,pm.cu_width
			,pm.cu_height
			,pm.part_cust_no AS custno
			,pm.forecast_cat
			,pm.fx_flag
			,pm.vend_currency
			,pm.vend_name
			,pm.pp_code
			,pm.pp_data_no
		FROM dw_us.dwd_disty_inv_qty_df diq
		INNER JOIN dim_us.dim_pub_part_info pm ON diq.sku_no = pm.sku_no
		 INNER JOIN dim_us.dim_pub_vendor_info pvi ON pvi.vend_no = pm.vend_no
		WHERE diq.date_flag = '2024-04-08'
			 AND (pm.vend_no IN (13208) OR pvi.pur_vend_no IN (13208))
			
			
			
			
			
			 AND pm.prod_type IN ('A','B','K','R','S')
			 AND pm.abc_code IN ('A','B','C','E','T')
			 AND diq.inv_type IN (1)
			
        UNION ALL
        SELECT
         sil.date_flag
        ,sil.loc_no
        ,sil.inv_type
        ,sil.sku_no
        ,sil.ave_cost
        ,sil.base_cost
        ,sil.ave_cost_fx 
        ,sil.base_cost_fx 
        ,sil.on_hand_qty
        ,sil.on_order_qty
        ,sil.bo_qty
        ,sil.intran_in
        ,sil.alloc_qty
        ,sil.wip_qty
        ,sil.intran_out
        ,sil.bundle_kit
        ,sil.prod_type
        ,sil.mfg_partno
        ,sil.part_no
        ,sil.prod_code
        ,sil.vend_no
        ,sil.abc_code
        ,sil.vpl_no
        ,sil.short_desc
        ,sil.long_desc
        ,sil.mar_comment
        ,sil.vpl_code
        ,sil.weight
        ,sil.cu_length
        ,sil.cu_width
        ,sil.cu_height
        ,sil.custno
        ,sil.forecast_cat
        ,sil.fx_flag
        ,sil.vend_currency
        ,sil.vend_name
        ,sil.pp_code
        ,sil.pp_data_no
        FROM sku_inv_loc sil
	)
    ,max_week
AS (
	SELECT max(week) AS max_week
	FROM dw_us.dws_disty_pur_ips_runrate_1w
	WHERE sum_type = 'WITYPESTD'
		 AND inv_type IN (1)
	)
    ,only_runrate_skus
AS (
	SELECT DISTINCT '2024-04-08' AS date_flag
		,pm.sku_no
		,dr.inv_type
		,pm.ave_cost
		,pm.po_cost
		,pm.bundle_kit
		,pm.prod_type
		,pm.mfg_partno
		,pm.part_no
		,pm.prod_code
		,pm.vend_no
		,pm.abc_code
		,pm.vpl_no
		,pm.short_desc
		,pm.long_desc
		,CASE 
			WHEN (pm.mar_end_date < DATE(TO_CHAR(sysdate, 'YYYY-MM-DD')))
				THEN NULL
			ELSE pm.mar_comment
			END AS mar_comment
		,pm.vpl_code
		,pm.weight
		,pm.cu_length
		,pm.cu_width
		,pm.cu_height
		,pm.part_cust_no AS custno
		,pm.forecast_cat
		,pm.fx_flag
		,pm.vend_currency
		,pm.vend_name
		,pm.pp_code
		,pm.pp_data_no
	FROM dim_us.dim_pub_part_info pm
	 INNER JOIN dim_us.dim_pub_vendor_info pvi ON pvi.vend_no = pm.vend_no
	INNER JOIN dw_us.dws_disty_pur_ips_runrate_1w dr ON pm.sku_no = dr.sku_no
	CROSS JOIN max_week mw
	WHERE dr.sum_type = 'WITYPESTD'
		AND pm.sku_no NOT IN (
				SELECT DISTINCT sku_no
				FROM inv_qty_temp
				)
		
		
		 AND (pm.vend_no IN (13208) OR pvi.pur_vend_no IN (13208))
		
		
		
		
		
		 AND pm.prod_type IN ('A','B','K','R','S')
		 AND pm.abc_code IN ('A','B','C','E','T')
		 AND dr.inv_type IN (1)
		
	GROUP BY pm.sku_no
		,dr.inv_type
		,pm.ave_cost
		,pm.po_cost
		,pm.bundle_kit
		,pm.prod_type
		,pm.mfg_partno
		,pm.part_no
		,pm.prod_code
		,pm.vend_no
		,pm.abc_code
		,pm.vpl_no
		,pm.short_desc
		,pm.long_desc
		,CASE 
			WHEN (pm.mar_end_date < DATE(TO_CHAR(sysdate, 'YYYY-MM-DD')))
				THEN NULL
			ELSE pm.mar_comment
			END
		,pm.vpl_code
		,pm.weight
		,pm.cu_length
		,pm.cu_width
		,pm.cu_height
		,pm.part_cust_no
		,pm.forecast_cat
		,pm.fx_flag
		,pm.vend_currency
		,pm.vend_name
		,pm.pp_code
		,pm.pp_data_no
	HAVING sum(CASE 
				WHEN dr.week BETWEEN mw.max_week - 10
						AND mw.max_week
					THEN dr.runrate_qty
				ELSE 0
				END) > 0
	)
	SELECT
		date_flag
		,sku_no
		,inv_type
		,ave_cost
		,base_cost
		,bundle_kit
		,prod_type
		,mfg_partno
		,part_no
		,prod_code
		,vend_no
		,abc_code
		,vpl_no
		,short_desc
		,long_desc
		,mar_comment
		,vpl_code
		,loc_no
		,ave_cost_fx
		,base_cost_fx
		,on_hand_qty
		,on_order_qty
		,bo_qty
		,intran_in
		,alloc_qty
		,wip_qty
		,intran_out
		,weight
		,cu_length
		,cu_width
		,cu_height
		,custno
		,forecast_cat
		,fx_flag
		,vend_currency
		,vend_name
		,pp_code
		,pp_data_no
	FROM inv_qty_temp
	UNION ALL
	SELECT date_flag
		,sku_no
		,inv_type
		,ifnull(ave_cost, 0)
		,ifnull(po_cost, 0)
		,bundle_kit
		,prod_type
		,mfg_partno
		,part_no
		,prod_code
		,vend_no
		,abc_code
		,vpl_no
		,short_desc
		,long_desc
		,mar_comment
		,vpl_code
		,0
		,0
		,0
		,0
		,0
		,0
		,0
		,0
		,0
		,0
		,weight
		,cu_length
		,cu_width
		,cu_height
		,custno
		,forecast_cat
		,fx_flag
		,vend_currency
		,vend_name
		,pp_code
		,pp_data_no
	FROM only_runrate_skus
;

DROP TABLE IF EXISTS dim_pub_sku_cost;
CREATE LOCAL TEMPORARY TABLE dim_pub_sku_cost ON COMMIT PRESERVE ROWS AS
SELECT DISTINCT
  iq.sku_no,
  sc.ave_cost,
  sc.base_cost,
  sc.ave_cost_fx,
  sc.base_cost_fx
FROM inv_qty_temp iq
INNER JOIN dim_us.dim_pub_sku_cost sc
	ON iq.sku_no = sc.sku_no
;

UPDATE inv_qty_temp iq
SET ave_cost = a.ave_cost
FROM (
	SELECT DISTINCT a1.sku_no
		,a1.ave_cost
	FROM inv_qty_temp a1
	INNER JOIN (
		SELECT sku_no
			,count(DISTINCT ave_cost) icount
		FROM inv_qty_temp
		WHERE on_hand_qty > 0
		GROUP BY sku_no
		HAVING count(DISTINCT ave_cost) = 1
		) b1 ON a1.sku_no = b1.sku_no
	WHERE a1.on_hand_qty > 0
	) a
WHERE iq.sku_no = a.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT ave_cost) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT ave_cost) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET ave_cost = sc.ave_cost
FROM dim_pub_sku_cost sc
WHERE iq.sku_no = sc.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT ave_cost) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT ave_cost) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET ave_cost_fx = a.ave_cost_fx
FROM (
	SELECT DISTINCT a1.sku_no
		,a1.ave_cost_fx
	FROM inv_qty_temp a1
	INNER JOIN (
		SELECT sku_no
			,count(DISTINCT ave_cost_fx) icount
		FROM inv_qty_temp
		WHERE on_hand_qty > 0
		GROUP BY sku_no
		HAVING count(DISTINCT ave_cost_fx) = 1
		) b1 ON a1.sku_no = b1.sku_no
	WHERE a1.on_hand_qty > 0
	) a
WHERE iq.sku_no = a.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT ave_cost_fx) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT ave_cost_fx) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET ave_cost_fx = sc.ave_cost_fx
FROM dim_pub_sku_cost sc
WHERE iq.sku_no = sc.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT ave_cost_fx) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT ave_cost_fx) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET base_cost = a.base_cost
FROM (
	SELECT DISTINCT a1.sku_no
		,a1.base_cost
	FROM inv_qty_temp a1
	INNER JOIN (
		SELECT sku_no
			,count(DISTINCT base_cost) icount
		FROM inv_qty_temp
		WHERE on_hand_qty > 0
		GROUP BY sku_no
		HAVING count(DISTINCT base_cost) = 1
		) b1 ON a1.sku_no = b1.sku_no
	WHERE a1.on_hand_qty > 0
	) a
WHERE iq.sku_no = a.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT base_cost) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT base_cost) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET base_cost = sc.base_cost
FROM dim_pub_sku_cost sc
WHERE iq.sku_no = sc.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT base_cost) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT base_cost) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET base_cost_fx = a.base_cost_fx
FROM (
	SELECT DISTINCT a1.sku_no
		,a1.base_cost_fx
	FROM inv_qty_temp a1
	INNER JOIN (
		SELECT sku_no
			,count(DISTINCT base_cost_fx) icount
		FROM inv_qty_temp
		WHERE on_hand_qty > 0
		GROUP BY sku_no
		HAVING count(DISTINCT base_cost_fx) = 1
		) b1 ON a1.sku_no = b1.sku_no
	WHERE a1.on_hand_qty > 0
	) a
WHERE iq.sku_no = a.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT base_cost_fx) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT base_cost_fx) > 1
			) AS b
		);

UPDATE inv_qty_temp iq
SET base_cost_fx = sc.base_cost_fx
FROM dim_pub_sku_cost sc
WHERE iq.sku_no = sc.sku_no
	AND iq.sku_no IN (
		SELECT sku_no
		FROM (
			SELECT sku_no
				,count(DISTINCT base_cost_fx) icount
			FROM inv_qty_temp
			GROUP BY sku_no
			HAVING count(DISTINCT base_cost_fx) > 1
			) AS b
		);


ALTER SESSION SET PARAMETER WithClauseMaterialization=1;

WITH part_info
AS (
	SELECT DISTINCT
	  sku_no
	FROM inv_qty_temp
    )
    ,all_loc_no
AS (
	SELECT
	  loc_no,
	  ifnull(ext_no, loc_no) AS ext_no,
	  loc_no || '-' || loc_char AS loc_char
	FROM dim_us.dim_pub_location_info
	WHERE loc_no IN (3,4,5,6,7,8,9,12,16,50,502,503,504,505,506,9715,9716,9915,9916) OR ext_no IN (3,4,5,6,7,8,9,12,16,50,502,503,504,505,506,9715,9716,9915,9916)
    )
    ,qtysum_all
AS (
	SELECT
		 iq.sku_no
		,iq.mfg_partno
		,iq.part_no
		,iq.prod_code
		,iq.vend_no
		,iq.vend_name
		,iq.inv_type
		,iq.abc_code
		,iq.prod_type
		,iq.pp_code
		,iq.pp_data_no
		,CASE 
			WHEN iq.forecast_cat = 0
				THEN 'Forecast Category1'
			WHEN iq.forecast_cat = 1
				THEN 'Forecast Category2'
			ELSE NULL
			END AS forecast_category
		,CASE 
			WHEN vx.xref_no IS NOT NULL
				THEN vx.xref_no
			ELSE iq.vend_no
			END AS purch_vend_no
		,CASE 
			WHEN vx.xref_no IS NOT NULL
				THEN vm.vend_name
			ELSE iq.vend_name
			END AS purch_vend_name
		,CASE 
			WHEN loc.loc_no IS NOT NULL
				THEN loc.loc_no
			ELSE -99
			END AS loc_no
		,CASE 
			WHEN loc.loc_no IS NOT NULL
				THEN loc.loc_char
			ELSE 'Others'
			END AS loc_char
		,iq.bundle_kit
		,iq.vpl_no
		,iq.ave_cost --Sys Cost
		,iq.base_cost AS po_cost 
		,iq.fx_flag
		,CASE 
			WHEN iq.fx_flag = 'Y'
				THEN iq.ave_cost_fx
			ELSE 0
			END ave_cost_fx
		,CASE 
			WHEN iq.fx_flag = 'Y'
				THEN iq.base_cost_fx
			ELSE 0
			END po_cost_fx
		,iq.short_desc
		,iq.long_desc
		,iq.vend_currency
		,iq.vpl_code
		,iq.mar_comment
		,sum(ifnull(iq.on_hand_qty, 0)) AS on_hand_qty --OH
		,sum(ifnull(iq.on_order_qty, 0)) AS on_order_qty --OO
		,sum(ifnull(iq.bo_qty, 0)) AS bo_qty --BO
		,sum(ifnull(iq.intran_in, 0)) AS intran_in --IT
		,sum(ifnull(iq.alloc_qty, 0)) AS alloc_qty
		,sum(ifnull(iq.wip_qty, 0)) AS wip_qty --WIP
		,sum(ifnull(iq.on_hand_qty, 0) - ifnull(iq.bo_qty, 0) - ifnull(iq.alloc_qty, 0) - ifnull(iq.wip_qty, 0) - ifnull(iq.intran_out, 0)) AS avail_qty
		,CASE 
			WHEN iq.fx_flag = 'Y'
				THEN sum(iq.ave_cost_fx * ifnull(iq.on_hand_qty, 0))
			END usd_ext_cost
		,CASE 
			WHEN iq.fx_flag = 'N'
				THEN sum(iq.ave_cost * ifnull(iq.on_hand_qty, 0))
			END ext_cost
		,iq.weight,iq.cu_length,iq.cu_width,iq.cu_height,iq.custno
	FROM inv_qty_temp iq
	LEFT JOIN all_loc_no loc ON iq.loc_no = loc.loc_no
	LEFT JOIN dim_us.dim_pub_vendor_xref vx ON iq.vend_no = vx.vend_no AND vx.xref_type = 'VEND_PURCH' AND vx.active = 'Y' 
	LEFT JOIN dim_us.dim_pub_vendor_info vm ON vm.vend_no = vx.xref_no
	WHERE iq.date_flag = '2024-04-08'
	GROUP BY iq.sku_no
		,iq.mfg_partno
		,iq.part_no
		,iq.prod_code
		,iq.vend_no
		,iq.vend_name
		,iq.inv_type
		,iq.abc_code
		,iq.prod_type
		,iq.pp_code
		,iq.pp_data_no
		,CASE 
			WHEN iq.forecast_cat = 0
				THEN 'Forecast Category1'
			WHEN iq.forecast_cat = 1
				THEN 'Forecast Category2'
			ELSE NULL
			END  
		,CASE 
			WHEN vx.xref_no IS NOT NULL
				THEN vx.xref_no
			ELSE iq.vend_no
			END
		,CASE 
			WHEN vx.xref_no IS NOT NULL
				THEN vm.vend_name
			ELSE iq.vend_name
			END
		,CASE 
			WHEN loc.loc_no IS NOT NULL
				THEN loc.loc_no
			ELSE -99
			END
		,CASE 
			WHEN loc.loc_no IS NOT NULL
				THEN loc.loc_char
			ELSE 'Others'
			END
		,iq.bundle_kit
		,iq.vpl_no
		,iq.ave_cost
		,iq.base_cost
		,CASE 
			WHEN iq.fx_flag = 'Y'
				THEN iq.ave_cost_fx
			ELSE 0
			END
		,CASE 
			WHEN iq.fx_flag = 'Y'
				THEN iq.base_cost_fx
			ELSE 0
			END
		,iq.short_desc
		,iq.long_desc
		,iq.vend_currency
		,iq.vpl_code
		,iq.mar_comment
		,iq.fx_flag
		,iq.weight,iq.cu_length,iq.cu_width,iq.cu_height,iq.custno
    )
    ,inv_aging
AS (
	SELECT DISTINCT dia.inv_type
		,dia.sku_no
		,ifnull(dia.qty1_30,0) AS age1 --0-30
        ,ifnull(dia.qty31_60,0) AS age2 --31-60
        ,ifnull(dia.qty61_90,0) AS age3 --61-90
        ,ifnull(dia.qty90_up,0) AS age4 --91+
        ,ifnull(dia.qty91_120,0) AS age5 --91-120
        ,ifnull(dia.qty121_150,0) AS age6 --121-150
        ,ifnull(dia.qty151_180,0) AS age7 --151-180
        ,ifnull(dia.qty181_210,0) AS age8 --181-210
        ,ifnull(dia.qty211_240,0) AS age9 --211-240
        ,ifnull(dia.qty240_up,0) AS age91 --240+
        ,ifnull(dia.qty241_270,0) AS age10 --241-270
        ,ifnull(dia.qty271_300,0) AS age11 --271-300
        ,ifnull(dia.qty301_330,0) AS age12 --301-330
        ,ifnull(dia.qty331_360,0) AS age13 --331-360
        ,ifnull(dia.qty360_up,0) AS age14 --360+
	FROM dw_us.dwd_disty_inv_aging_df dia
	INNER JOIN part_info sl ON dia.sku_no = sl.sku_no
	WHERE dia.view_level = 'IT_PART'
		AND dia.date_flag = '2024-04-08' --@date
	)
	,sku_inv_list
AS (
	SELECT qa.sku_no
		,qa.inv_type
		,row_number() OVER (ORDER BY qa.sku_no,qa.inv_type) AS row_id
		,sum(qa.on_hand_qty+qa.intran_in) as oh
		,sum(qa.on_order_qty) as oo
		,sum(ifnull(ia.age4,0)) as aging90
	FROM qtysum_all qa
	 left join inv_aging ia on ia.sku_no=qa.sku_no and ia.inv_type =qa.inv_type
	WHERE 1 = 1
	GROUP BY qa.sku_no
		,qa.inv_type
		 
		
		
		 
		 
		 
		 
	)
	,sku_list_final
AS (
	SELECT
		 sku_no
		,inv_type
		,row_id
		,(SELECT max(row_id) AS total_count FROM sku_inv_list)
	FROM sku_inv_list
	WHERE  row_id >= 1 AND row_id <= 25
		)
	,runrate
AS (
	--@rr_type=WITYPESTD
	SELECT
		 dr.sku_no
		,dr.inv_type
		,sum(CASE 
			WHEN dr.week = mw.max_week
				THEN dr.runrate_qty
			ELSE 0
			END) AS rr0 --WTD
		,sum(CASE 
				WHEN dr.week = mw.max_week - 1
					THEN dr.runrate_qty
				ELSE 0
				END) AS rr1 --1W
		,sum(CASE 
				WHEN dr.week BETWEEN mw.max_week - 2
						AND mw.max_week - 1
					THEN dr.runrate_qty
				ELSE 0
				END) AS rr2 --2W
		,sum(CASE 
				WHEN dr.week BETWEEN mw.max_week - 4
						AND mw.max_week - 1
					THEN dr.runrate_qty
				ELSE 0
				END) AS rr4 --4W
		,sum(CASE 
				WHEN dr.week BETWEEN mw.max_week - 10
						AND mw.max_week - 1
					THEN dr.runrate_qty --10W
				ELSE 0
				END) AS rr10
		,sum(CASE 
				WHEN dr.week BETWEEN mw.max_week - 11
						AND mw.max_week - 1
					THEN dr.runrate_qty --11W
				ELSE 0
				END) AS rr11
	FROM sku_list_final sil
	INNER JOIN dw_us.dws_disty_pur_ips_runrate_1w dr ON sil.sku_no = dr.sku_no AND sil.inv_type = dr.inv_type
	CROSS JOIN (
				SELECT max(week) AS max_week
				FROM dw_us.dws_disty_pur_ips_runrate_1w
				WHERE sum_type = 'WITYPESTD'
					 AND inv_type IN (1)
				) mw
	WHERE dr.sum_type = 'WITYPESTD'
		AND mw.max_week - 10 <= dr.week
	
	
	GROUP BY dr.sku_no
		,dr.inv_type
	)
	,alloc_sum_qty
AS (
    SELECT
       ril.sku_no
      ,ril.inv_type
      ,SUM(ril.alloc_so) AS alloc_so
      ,SUM(ril.alloc_rio) AS alloc_rio
      ,SUM(ril.alloc_kwo) AS alloc_kwo
      ,SUM(ril.avail_qty) AS avail_qty
    FROM dm_us.dm_disty_sales_rio_sku_inv_loc ril
	INNER JOIN part_info part ON ril.sku_no = part.sku_no
	WHERE ril.prod_type = 'K'
		AND ril.bundle_kit = 'Y'
    GROUP BY
       ril.sku_no
      ,ril.inv_type
	)
	,rio_loc
AS (
    SELECT
       ril.sku_no
      ,ril.inv_type
      ,ril.loc_no
      ,SUM(ril.rio_qty) AS rio_qty
    FROM dm_us.dm_disty_sales_rio_sku_inv_loc ril
	INNER JOIN part_info part ON ril.sku_no = part.sku_no
    GROUP BY
       ril.sku_no
      ,ril.inv_type
      ,ril.loc_no
	)
	,rio_loc_total
AS (
    SELECT
       ril.sku_no
      ,ril.inv_type
      ,SUM(ril.rio_qty) AS rio_qty
    FROM rio_loc ril
    GROUP BY
       ril.sku_no
      ,ril.inv_type
	)
	,cnt
AS (
	SELECT MAX(row_id) OVER() AS row_cnt
		,row_id
	FROM sku_inv_list
	)

SELECT cnt.row_cnt
	,sl.row_id
	,qa.abc_code --ABC
	,qa.prod_type --PT
	,qa.pp_code --PP(days)
	,qa.purch_vend_no
	,qa.vend_no
	,qa.prod_code --PM
	,qa.vpl_no
	,qa.vpl_code
	,qa.part_no
	,qa.sku_no
	,qa.inv_type
	,qa.forecast_category
	,ifnull(qa.po_cost,0) as po_cost --base cost
	,ifnull(qa.ave_cost,0) as ave_cost  --sys cost
	
	,qa.po_cost_fx
	,qa.ave_cost_fx
	
	,ia.age1 --0-30
	,ia.age2 --31-60
	,ia.age3 --61-90
	,ia.age4 --91+
	,ia.age5 --91-120
	,ia.age6 --121-150
	,ia.age7 --151-180
	,ia.age8 --181-210 
	,ia.age9 --211-240
	,ia.age91 as age_91 --241+
	,ia.age10  as age_10--241-270
	,ia.age11 as age_11 --271-300
	,ia.age12  as age_12--301-330
	,ia.age13 as age_13 --331-360
	,ia.age14  as age_14--360+
	
	,qa.on_hand_qty --OH
	,qa.on_order_qty --OO
	,qa.bo_qty --BO
	,case when asq.sku_no is not null then ifnull(asq.alloc_kwo,0)+ifnull(asq.alloc_rio,0)+ifnull(asq.alloc_so,0) else qa.alloc_qty end as alloc_qty
	--,asq.alloc_rio
	,asq.alloc_kwo
	,asq.alloc_so
	,qa.intran_in --IT
	,qa.wip_qty --WIP
	,case when asq.sku_no is not null then asq.avail_qty else qa.avail_qty end as avail_qty --Avail Qty
	,qa.usd_ext_cost --Ext Amt($)
	,qa.ext_cost
	
	,qa.loc_no
	,qa.loc_char
	,rl.rio_qty
	
	,qa.bundle_kit
	,qa.vend_currency
	
	,rr.rr10 as rr_10
	,rr.rr4
	,rr.rr2
	,rr.rr1
	,rr.rr0
	
	,qa.mfg_partno
	,qa.purch_vend_name
	,qa.vend_name
	,qa.short_desc
	,qa.long_desc
	,qa.mar_comment
	,case when asq.alloc_rio is null then ifnull(rlt.rio_qty ,0) else asq.alloc_rio end as alloc_rio
	,ifnull(qa.on_hand_qty,0)+ifnull(qa.intran_in,0) as total
	,qa.pp_data_no
	,qa.weight,qa.cu_length,qa.cu_width,qa.cu_height,qa.custno || '-' || ch.cust_name as custno
FROM qtysum_all qa
INNER JOIN sku_list_final sl ON qa.sku_no = sl.sku_no AND qa.inv_type = sl.inv_type
LEFT JOIN inv_aging ia ON qa.sku_no = ia.sku_no	AND qa.inv_type = ia.inv_type
LEFT JOIN runrate rr ON qa.sku_no = rr.sku_no AND qa.inv_type = rr.inv_type
LEFT JOIN rio_loc rl ON qa.sku_no = rl.sku_no AND qa.inv_type = rl.inv_type AND qa.loc_no=rl.loc_no
LEFT JOIN rio_loc_total rlt ON qa.sku_no = rlt.sku_no AND qa.inv_type = rlt.inv_type
LEFT JOIN alloc_sum_qty asq ON qa.sku_no = asq.sku_no AND qa.inv_type = asq.inv_type
LEFT JOIN cnt ON sl.row_id = cnt.row_id
LEFT JOIN dim_us.dim_pub_customer_info ch ON qa.custno = ch.cust_no
ORDER BY sl.row_id ASC
;