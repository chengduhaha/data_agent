# dm_us.dm_disty_brpt_pm_wtd

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dm_us.dm_disty_brpt_pm_wtd
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (wtd) by business slice

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dm_us.dm_disty_brpt_pm_wtd`
- Layer: DM
- Canonical/Derived: Derived aggregation/serving
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dm_us.dm_disty_brpt_pm_wtd`

### Grain, Scope, Exclusions

- Grain: week-to-date cumulative through each date_flag
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive (`dw_us`/`dm_us`/`dim_us`): table family present; prefer canonical name without suffix variants.
- Vertica: same schema families mirrored; Vertica may lag Hive by several days on detail facts.
- Reconciliation: compare `MIN(date_flag)`, `MAX(date_flag)`, row counts when auditing cross-engine parity.

### Column Catalog (100% columns)

- documented_column_count: 127
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| week_no | int | engine metadata not exposed | — | 1 | — | key | week no | integer | not_null_expected|dim_fk_check_recommended | week no; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| date_flag | date | engine metadata not exposed | — | 2 | — | key | date flag | YYYY-MM-DD | not_null_expected|dim_fk_check_recommended | Business date partition; use month-end row for MTD month totals. | `dim_us.dim_pub_date.date_flag` |
| pm_id | int | engine metadata not exposed | — | 3 | — | key | pm id | integer | not_null_expected|dim_fk_check_recommended | pm id; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | `dim_us.dim_pub_vpl_hierarchy_info.pm_id` |
| pm_name | varchar(100) | engine metadata not exposed | — | 4 | — | dimension | pm name | categorical_or_expression_text | domain_value_check_recommended | pm name; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pm_mgr_id | int | engine metadata not exposed | — | 5 | — | key | pm mgr id | integer | not_null_expected|dim_fk_check_recommended | pm mgr id; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pm_manager_name | varchar(100) | engine metadata not exposed | — | 6 | — | dimension | pm manager name | categorical_or_expression_text | domain_value_check_recommended | pm manager name; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pm_dir_id | int | engine metadata not exposed | — | 7 | — | key | pm dir id | integer | not_null_expected|dim_fk_check_recommended | pm dir id; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pm_director_name | varchar(100) | engine metadata not exposed | — | 8 | — | dimension | pm director name | categorical_or_expression_text | domain_value_check_recommended | pm director name; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pm_vp_id | int | engine metadata not exposed | — | 9 | — | key | pm vp id | integer | not_null_expected|dim_fk_check_recommended | pm vp id; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pm_vp_name | varchar(100) | engine metadata not exposed | — | 10 | — | dimension | pm vp name | categorical_or_expression_text | domain_value_check_recommended | pm vp name; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| seg_code | varchar(100) | engine metadata not exposed | — | 11 | — | dimension | seg code | categorical_or_expression_text | domain_value_check_recommended | seg code; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| company_no | int | engine metadata not exposed | — | 12 | — | key | company no | integer | not_null_expected|dim_fk_check_recommended | company no; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| gross_sales | numeric(20,8) | engine metadata not exposed | — | 13 | — | measure | gross sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | gross sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| net_sales | numeric(20,8) | engine metadata not exposed | — | 14 | — | measure | net sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | net sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| gross_cost | numeric(20,8) | engine metadata not exposed | — | 15 | — | measure | gross cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | gross cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| net_cost | numeric(20,8) | engine metadata not exposed | — | 16 | — | measure | net cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | net cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| scm_usage | numeric(20,8) | engine metadata not exposed | — | 17 | — | measure | scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | scm usage; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ds_sales | numeric(20,8) | engine metadata not exposed | — | 18 | — | measure | ds sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ds sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| stock_sales | numeric(20,8) | engine metadata not exposed | — | 19 | — | measure | stock sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | stock sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ds_cost | numeric(20,8) | engine metadata not exposed | — | 20 | — | measure | ds cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ds cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| stock_cost | numeric(20,8) | engine metadata not exposed | — | 21 | — | measure | stock cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | stock cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ds_scm_usage | numeric(20,8) | engine metadata not exposed | — | 22 | — | measure | ds scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ds scm usage; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| stock_scm_usage | numeric(20,8) | engine metadata not exposed | — | 23 | — | measure | stock scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | stock scm usage; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| total_unit | int | engine metadata not exposed | — | 24 | — | measure | total unit | integer | non_negative_expected|outlier_check_recommended | total unit; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| total_weight | numeric(20,8) | engine metadata not exposed | — | 25 | — | measure | total weight | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | total weight; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cgp | numeric(20,8) | engine metadata not exposed | — | 26 | — | measure | cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cgp; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| total_btl | numeric(20,8) | engine metadata not exposed | — | 27 | — | measure | total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | total btl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| tgm_amt | numeric(20,8) | engine metadata not exposed | — | 28 | — | measure | tgm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | tgm amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| gm_amt | numeric(20,8) | engine metadata not exposed | — | 29 | — | measure | gm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | gm amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ngm_amt | numeric(20,8) | engine metadata not exposed | — | 30 | — | measure | ngm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ngm amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| oplgm_amt | numeric(20,8) | engine metadata not exposed | — | 31 | — | measure | oplgm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | oplgm amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_gross_sales | numeric(20,8) | engine metadata not exposed | — | 32 | — | measure | bo gross sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo gross sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_gross_cost | numeric(20,8) | engine metadata not exposed | — | 33 | — | measure | bo gross cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo gross cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_total_unit | int | engine metadata not exposed | — | 34 | — | measure | bo total unit | integer | non_negative_expected|outlier_check_recommended | bo total unit; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_gm_amt | numeric(20,8) | engine metadata not exposed | — | 35 | — | measure | bo gm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo gm amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_gross_sales | numeric(20,8) | engine metadata not exposed | — | 36 | — | measure | so gross sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so gross sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_gross_cost | numeric(20,8) | engine metadata not exposed | — | 37 | — | measure | so gross cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so gross cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_total_unit | int | engine metadata not exposed | — | 38 | — | measure | so total unit | integer | non_negative_expected|outlier_check_recommended | so total unit; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_gm_amt | numeric(20,8) | engine metadata not exposed | — | 39 | — | measure | so gm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so gm amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_age0_7 | numeric(20,8) | engine metadata not exposed | — | 40 | — | measure | bo age0 7 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age0 7; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_age8_14 | numeric(20,8) | engine metadata not exposed | — | 41 | — | measure | bo age8 14 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age8 14; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_age15_21 | numeric(20,8) | engine metadata not exposed | — | 42 | — | measure | bo age15 21 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age15 21; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| bo_age21_up | numeric(20,8) | engine metadata not exposed | — | 43 | — | measure | bo age21 up | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age21 up; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_age0_7 | numeric(20,8) | engine metadata not exposed | — | 44 | — | measure | so age0 7 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age0 7; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_age8_14 | numeric(20,8) | engine metadata not exposed | — | 45 | — | measure | so age8 14 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age8 14; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_age15_21 | numeric(20,8) | engine metadata not exposed | — | 46 | — | measure | so age15 21 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age15 21; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| so_age21_up | numeric(20,8) | engine metadata not exposed | — | 47 | — | measure | so age21 up | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age21 up; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| reg_inv | numeric(20,8) | engine metadata not exposed | — | 48 | — | measure | reg inv | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | reg inv; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| reg_inv_age0_30 | numeric(20,8) | engine metadata not exposed | — | 49 | — | measure | reg inv age0 30 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | reg inv age0 30; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| reg_inv_age31_60 | numeric(20,8) | engine metadata not exposed | — | 50 | — | measure | reg inv age31 60 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | reg inv age31 60; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| reg_inv_age61_90 | numeric(20,8) | engine metadata not exposed | — | 51 | — | measure | reg inv age61 90 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | reg inv age61 90; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| reg_inv_age90_up | numeric(20,8) | engine metadata not exposed | — | 52 | — | measure | reg inv age90 up | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | reg inv age90 up; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma_inv | numeric(20,8) | engine metadata not exposed | — | 53 | — | measure | rma inv | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma inv; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma_inv_age0_30 | numeric(20,8) | engine metadata not exposed | — | 54 | — | measure | rma inv age0 30 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma inv age0 30; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma_inv_age31_60 | numeric(20,8) | engine metadata not exposed | — | 55 | — | measure | rma inv age31 60 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma inv age31 60; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma_inv_age61_90 | numeric(20,8) | engine metadata not exposed | — | 56 | — | measure | rma inv age61 90 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma inv age61 90; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma_inv_age90_up | numeric(20,8) | engine metadata not exposed | — | 57 | — | measure | rma inv age90 up | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma inv age90 up; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| oh_cost | numeric(20,8) | engine metadata not exposed | — | 58 | — | measure | oh cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | oh cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| oo_cost | numeric(20,8) | engine metadata not exposed | — | 59 | — | measure | oo cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | oo cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| oh_qty | int | engine metadata not exposed | — | 60 | — | dimension | oh qty | integer | domain_value_check_recommended | oh qty; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| oo_qty | int | engine metadata not exposed | — | 61 | — | dimension | oo qty | integer | domain_value_check_recommended | oo qty; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ap_finance | numeric(20,8) | engine metadata not exposed | — | 62 | — | measure | ap finance | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ap finance; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| inv_cost | numeric(20,8) | engine metadata not exposed | — | 63 | — | measure | inv cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | inv cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| inv_reserve | numeric(20,8) | engine metadata not exposed | — | 64 | — | measure | inv reserve | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | inv reserve; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cr_risk_cterm | numeric(20,8) | engine metadata not exposed | — | 65 | — | measure | cr risk cterm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cr risk cterm; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| flr_synnex | numeric(20,8) | engine metadata not exposed | — | 66 | — | measure | flr synnex | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | flr synnex; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| direct_credit | numeric(20,8) | engine metadata not exposed | — | 67 | — | measure | direct credit | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | direct credit; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| csgn_edi_fee | numeric(20,8) | engine metadata not exposed | — | 68 | — | measure | csgn edi fee | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | csgn edi fee; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| corporate | numeric(20,8) | engine metadata not exposed | — | 69 | — | measure | corporate | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | corporate; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| sfs | numeric(20,8) | engine metadata not exposed | — | 70 | — | measure | sfs | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | sfs; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| scm_risk | numeric(20,8) | engine metadata not exposed | — | 71 | — | measure | scm risk | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | scm risk; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| flr_vendor | numeric(20,8) | engine metadata not exposed | — | 72 | — | measure | flr vendor | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | flr vendor; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_finance_sales | numeric(20,8) | engine metadata not exposed | — | 73 | — | measure | cust finance sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust finance sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_pmt_disc | numeric(20,8) | engine metadata not exposed | — | 74 | — | measure | cust pmt disc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust pmt disc; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cvr_rm | numeric(20,8) | engine metadata not exposed | — | 75 | — | measure | cvr rm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cvr rm; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ar_fin_recovery | numeric(20,8) | engine metadata not exposed | — | 76 | — | measure | ar fin recovery | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ar fin recovery; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| mfg_oh | numeric(20,8) | engine metadata not exposed | — | 77 | — | measure | mfg oh | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | mfg oh; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_finance | numeric(20,8) | engine metadata not exposed | — | 78 | — | measure | cust finance | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust finance; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma | numeric(20,8) | engine metadata not exposed | — | 79 | — | measure | rma | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| hc_sales | numeric(20,8) | engine metadata not exposed | — | 80 | — | measure | hc sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | hc sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| order_overhead | numeric(20,8) | engine metadata not exposed | — | 81 | — | measure | order overhead | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | order overhead; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| margin_share | numeric(20,8) | engine metadata not exposed | — | 82 | — | measure | margin share | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | margin share; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ap_adj | numeric(20,8) | engine metadata not exposed | — | 83 | — | measure | ap adj | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ap adj; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pdt | numeric(20,8) | engine metadata not exposed | — | 84 | — | measure | pdt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pdt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| scm_cost | numeric(20,8) | engine metadata not exposed | — | 85 | — | measure | scm cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | scm cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| infrastructure | numeric(20,8) | engine metadata not exposed | — | 86 | — | measure | infrastructure | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | infrastructure; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| marketing | numeric(20,8) | engine metadata not exposed | — | 87 | — | measure | marketing | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | marketing; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| coop | numeric(20,8) | engine metadata not exposed | — | 88 | — | measure | coop | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | coop; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| one_time_btl | numeric(20,8) | engine metadata not exposed | — | 89 | — | measure | one time btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | one time btl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| hbtl | numeric(20,8) | engine metadata not exposed | — | 90 | — | measure | hbtl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | hbtl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| scm_profit_adj | numeric(20,8) | engine metadata not exposed | — | 91 | — | measure | scm profit adj | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | scm profit adj; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| hc_pm | numeric(20,8) | engine metadata not exposed | — | 92 | — | measure | hc pm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | hc pm; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| hc_bd | numeric(20,8) | engine metadata not exposed | — | 93 | — | measure | hc bd | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | hc bd; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| btl | numeric(20,8) | engine metadata not exposed | — | 94 | — | measure | btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | btl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| btl_sales | numeric(20,8) | engine metadata not exposed | — | 95 | — | measure | btl sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | btl sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| btl_backout | numeric(20,8) | engine metadata not exposed | — | 96 | — | measure | btl backout | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | btl backout; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_rebate | numeric(20,8) | engine metadata not exposed | — | 97 | — | measure | cust rebate | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust rebate; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| mof | numeric(20,8) | engine metadata not exposed | — | 98 | — | measure | mof | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | mof; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_out_load | numeric(20,8) | engine metadata not exposed | — | 99 | — | measure | frt out load | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt out load; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_out_exp | numeric(20,8) | engine metadata not exposed | — | 100 | — | measure | frt out exp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt out exp; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| whoh_pack | numeric(20,8) | engine metadata not exposed | — | 101 | — | measure | whoh pack | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | whoh pack; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_ob_recovery | numeric(20,8) | engine metadata not exposed | — | 102 | — | measure | frt ob recovery | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt ob recovery; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_ib_recovery | numeric(20,8) | engine metadata not exposed | — | 103 | — | measure | frt ib recovery | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt ib recovery; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| others | numeric(20,8) | engine metadata not exposed | — | 104 | — | measure | others | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | others; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| others_sales | numeric(20,8) | engine metadata not exposed | — | 105 | — | measure | others sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | others sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| scm_disc | numeric(20,8) | engine metadata not exposed | — | 106 | — | measure | scm disc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | scm disc; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| scm_ndisc | numeric(20,8) | engine metadata not exposed | — | 107 | — | measure | scm ndisc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | scm ndisc; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_in | numeric(20,8) | engine metadata not exposed | — | 108 | — | measure | frt in | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt in; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| trans_btl | numeric(20,8) | engine metadata not exposed | — | 109 | — | measure | trans btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | trans btl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| trans_btl_sales | numeric(20,8) | engine metadata not exposed | — | 110 | — | measure | trans btl sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | trans btl sales; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 111 | — | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| fx_cost | numeric(20,8) | engine metadata not exposed | — | 112 | — | measure | fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | fx cost; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| dt_week | varchar(100) | engine metadata not exposed | — | 113 | — | dimension | dt week | categorical_or_expression_text | domain_value_check_recommended | dt week; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| btl_sales_for_opl | numeric(20,8) | engine metadata not exposed | — | 114 | — | measure | btl sales for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | btl sales for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| trans_btl_sales_for_opl | numeric(20,8) | engine metadata not exposed | — | 115 | — | measure | trans btl sales for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | trans btl sales for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| pdt_for_opl | numeric(20,8) | engine metadata not exposed | — | 116 | — | measure | pdt for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pdt for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_rebate_for_opl | numeric(20,8) | engine metadata not exposed | — | 117 | — | measure | cust rebate for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust rebate for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cvr_rm_for_opl | numeric(20,8) | engine metadata not exposed | — | 118 | — | measure | cvr rm for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cvr rm for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| btl_backout_for_opl | numeric(20,8) | engine metadata not exposed | — | 119 | — | measure | btl backout for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | btl backout for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_pmt_disc_for_opl | numeric(20,8) | engine metadata not exposed | — | 120 | — | measure | cust pmt disc for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust pmt disc for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| cust_finance_sales_for_opl | numeric(20,8) | engine metadata not exposed | — | 121 | — | measure | cust finance sales for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cust finance sales for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| rma_for_opl | numeric(20,8) | engine metadata not exposed | — | 122 | — | measure | rma for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rma for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| ar_fin_recovery_for_opl | numeric(20,8) | engine metadata not exposed | — | 123 | — | measure | ar fin recovery for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ar fin recovery for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| order_overhead_for_opl | numeric(20,8) | engine metadata not exposed | — | 124 | — | measure | order overhead for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | order overhead for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_out_exp_for_opl | numeric(20,8) | engine metadata not exposed | — | 125 | — | measure | frt out exp for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt out exp for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| frt_ob_recovery_for_opl | numeric(20,8) | engine metadata not exposed | — | 126 | — | measure | frt ob recovery for opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | frt ob recovery for opl; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |
| oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 127 | — | measure | oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | oplgm plus amt; MTD cumulative measure or dimension on `dm_us.dm_disty_brpt_pm_wtd` B Report serving slice. | — |


### Lineage

(N-degree)
- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: No Lineage Evidence Found
  - hop: 0
  - relation_type: —
  - via_job_or_view: —
- downstream_n_hops:
  - table_fqn: No Lineage Evidence Found
  - hop: 0
  - relation_type: —
  - via_job_or_view: —
- lineage_last_verified_at: 2026-06-22T05:16:14Z
  - source_type: compass
  - confidence: low
- lineage_notes:
  - Compass catalog lookup executed first; CK lineage used as fallback evidence.
### Column Lineage and Derivation
- column_lineage:
  - column_name: key_metric_bundle
  - lineage_type: derived
  - source_columns:
    - source_table: —
    - source_column: —
  - derivation_formula: sync.target.where: where sum_level = 'B1-SPKPVV' and date_flag = '${date_flag}'
  - etl_sql_ref:

### Freshness and Load Path

- Expected completion window: 03:00-03:20 PT (America/Los_Angeles) for core disty B-report daily/addition flows
- Load pattern: Azkaban-scheduled Spark SQL ETL with Hive write and Vertica sync
- Freshness note: aggregated `*_mtd`/`*_comb_mtd` tables refresh daily; detail fact may show Hive/Vertica date lag

## L2 Declarative Knowledge

### Business Definitions

- Domain: US B Report shipped-order profitability and operating performance analytics.
- Trust tier: governed serving
- Key context: - Business definitions: Uses B Report P&L ontology (BTL/PDT/NGM/OPL/TGM and related adjustment items).
- Key metrics or fields: net_sales, gross_sales, gm_amt, tgm_amt, ngm_amt, oplgm_amt
- Trust tier: curated

### Dimension Keys and Lookup Reference

- `cust_no` → `dim_us.dim_pub_customer_info` (`cust_name`, `cust_type`, `sales_terr`)
- `vend_no` → `dim_us.dim_pub_vendor_info` (`vend_name`, `master_vend_no`, `vend_seg_code`)
- `sku_no` → `dim_us.dim_pub_part_info` (`part_no`, `short_desc`, `vpl_no`)
- `vpl_no` → `dim_us.dim_pub_vpl_info` (`vpl_code`, `vpl_desc`, `vend_no`)
- `pm_id` → `dim_us.dim_pub_vpl_hierarchy_info` (PM/Buyer hierarchy attributes)

### Time Field Semantics

- `date_flag`: business date; primary filter field for natural-month and as-of-date queries.
- `month_no`: internal fiscal period index from `dim_us.dim_pub_date.m`; **not** YYYYMM — map via date dimension.
- `*_mtd`/`*_comb_mtd` columns: month-to-date cumulative values through `date_flag`; for month-total reporting use month-end `date_flag` row only.
- `*_1d` columns: single-day snapshot values for `date_flag`.
- `*_wtd` columns: week-to-date cumulative through `date_flag`.

### Metrics Served

- net_sales: canonical formula in `metric-index.md`
- gross_sales: canonical formula in `metric-index.md`
- gm_amt: canonical formula in `metric-index.md`
- tgm_amt: canonical formula in `metric-index.md`
- ngm_amt: canonical formula in `metric-index.md`
- oplgm_amt: canonical formula in `metric-index.md`
- oplgm_plus_amt: canonical formula in `metric-index.md`
- total_btl: canonical formula in `metric-index.md`

## L3 Procedural Knowledge

### Query and Routing Rules

- Prefer this table when required dimensions and time suffix match the question grain.
- Fall back to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` for order-line recalculation or missing dimensions.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary keys: —
- Common join keys: date_flag/dt_week/dt_month and entity keys (sku_no, cust_no, vend_no, vpl_no, pm, buyer, sales, BD hierarchy by table group).
- High-risk join pitfalls: Mixing 1d/wtd/mtd/comb_mtd grains in one aggregation causes double counting.

### Key Filters and ETL Business Logic

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For profitability metrics on this table, always filter `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

### Standard Time-Filter SQL (3 snippets)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dm_us.dm_disty_brpt_pm_wtd
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dm_disty_brpt_pm_wtd
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dm_us.dm_disty_brpt_pm_wtd
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dm_disty_brpt_pm_wtd t
JOIN dim_us.dim_pub_date f
  ON t.date_flag = f.date_flag
WHERE f.fyear = 2026
  AND f.month IN (1, 2)
GROUP BY f.fyear, f.month
ORDER BY f.fyear, f.month;
```

3) Recent N-month trend without double counting

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dm_us.dm_disty_brpt_pm_wtd
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT d.month_start, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dm_disty_brpt_pm_wtd t
JOIN (
  SELECT date_flag,
         date_trunc('MM', date_flag) AS month_start,
         ROW_NUMBER() OVER (PARTITION BY date_trunc('MM', date_flag) ORDER BY date_flag DESC) AS rn
  FROM dim_us.dim_pub_date
  WHERE date_flag >= add_months(current_date, -6)
) d
  ON t.date_flag = d.date_flag
WHERE d.rn = 1
GROUP BY d.month_start
ORDER BY d.month_start;
```

### Metric Selection Guidance

- Use this table for dashboard and period-comparison queries when dimensions match.
- Use DWD base for formula debugging, order_type adjustments, and transaction-level audit.
- Canonical metric formulas and routing: see `metric-index.md`.

## L4 Validation

### Data Quality Checks

- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).

### Metric Recompute Spot-Checks

- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.

### Conflicts and Open Questions

- Conflict item:
  - claim_a: Multiple pre-aggregated tables may serve same metric at different slices/grains.
  - claim_b: Routing precedence across sibling tables not explicitly documented.
  - status: Needs Clarification
  - user_decision: awaiting governed routing precedence confirmation
- Open: PM/Buyer hierarchy unmatched-rate baseline across full month window not yet decomposed by fallback branch.

## L5 Runtime View

### Query Path and Engine Preference

- Primary: Vertica `dw_us`/`dm_us` for BI dashboards (fresher on detail facts).
- Fallback: Hive for reconciliation or when Vertica unavailable.
- Metadata: domain table docs and `metric-index.md` for routing.

### Access Constraints

- Standard `dw_us`/`dm_us`/`dim_us` role-based access applies.
- No table-specific ACL exceptions documented.

## L6 Access and Consumption

### Primary Consumers and Use Cases

- Consumers: PM, Sales, Buyer, BD and executive analysis views.
- Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: audit
table_fqn: dm_us.dm_disty_brpt_pm_wtd
anti_use: daily date_flag scan only; not routing_certified; do not copy for ranking
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt, SUM(net_sales) AS net_sales
FROM dm_us.dm_disty_brpt_pm_wtd
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```