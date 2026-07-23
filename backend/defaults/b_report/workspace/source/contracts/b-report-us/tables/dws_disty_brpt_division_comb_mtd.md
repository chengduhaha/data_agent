# dw_us.dws_disty_brpt_division_comb_mtd

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dw_us.dws_disty_brpt_division_comb_mtd
- domain: b-report-us
- one_line_purpose: B Report combined-month profitability serving slice (division_comb_mtd)

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dw_us.dws_disty_brpt_division_comb_mtd`
- Layer: DWS
- Canonical/Derived: Derived aggregation/serving
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dw_us.dws_disty_brpt_division_comb_mtd`

### Grain, Scope, Exclusions

- Grain: month-to-date cumulative through each date_flag
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive (`dw_us`/`dm_us`/`dim_us`): table family present; prefer canonical name without suffix variants.
- Vertica: same schema families mirrored; Vertica may lag Hive by several days on detail facts.
- Reconciliation: compare `MIN(date_flag)`, `MAX(date_flag)`, row counts when auditing cross-engine parity.

### Column Catalog (100% columns)

- documented_column_count: 147
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| month_no | int | engine metadata not exposed | — | 1 | — | key | month no | integer | not_null_expected|dim_fk_check_recommended | Internal fiscal month index from `dim_us.dim_pub_date.m`; not YYYYMM. | `dim_us.dim_pub_date.m` |
| division | int | engine metadata not exposed | — | 2 | — | dimension | division | integer | domain_value_check_recommended | division; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| division_desc | varchar(100) | engine metadata not exposed | — | 3 | — | dimension | division desc | categorical_or_expression_text | domain_value_check_recommended | division desc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| company_no | int | engine metadata not exposed | — | 4 | — | key | company no | integer | not_null_expected|dim_fk_check_recommended | company no; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_sales | numeric(20,8) | engine metadata not exposed | — | 5 | — | measure | d sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_cost | numeric(20,8) | engine metadata not exposed | — | 6 | — | measure | d cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_unit | int | engine metadata not exposed | — | 7 | — | measure | d unit | integer | non_negative_expected|outlier_check_recommended | d unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_gm | numeric(20,8) | engine metadata not exposed | — | 8 | — | measure | d gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_ngm | numeric(20,8) | engine metadata not exposed | — | 9 | — | measure | d ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_opl | numeric(20,8) | engine metadata not exposed | — | 10 | — | measure | d opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_scm_usage | numeric(20,8) | engine metadata not exposed | — | 11 | — | measure | d scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_tgm | numeric(20,8) | engine metadata not exposed | — | 12 | — | measure | d tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_cgp | numeric(20,8) | engine metadata not exposed | — | 13 | — | measure | d cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| d_total_btl | numeric(20,8) | engine metadata not exposed | — | 14 | — | measure | d total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_sales | numeric(20,8) | engine metadata not exposed | — | 15 | — | measure | w sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_cost | numeric(20,8) | engine metadata not exposed | — | 16 | — | measure | w cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_unit | int | engine metadata not exposed | — | 17 | — | measure | w unit | integer | non_negative_expected|outlier_check_recommended | w unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_gm | numeric(20,8) | engine metadata not exposed | — | 18 | — | measure | w gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_ngm | numeric(20,8) | engine metadata not exposed | — | 19 | — | measure | w ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_opl | numeric(20,8) | engine metadata not exposed | — | 20 | — | measure | w opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_scm_usage | numeric(20,8) | engine metadata not exposed | — | 21 | — | measure | w scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_tgm | numeric(20,8) | engine metadata not exposed | — | 22 | — | measure | w tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_cgp | numeric(20,8) | engine metadata not exposed | — | 23 | — | measure | w cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_total_btl | numeric(20,8) | engine metadata not exposed | — | 24 | — | measure | w total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_sales | numeric(20,8) | engine metadata not exposed | — | 25 | — | measure | m sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_cost | numeric(20,8) | engine metadata not exposed | — | 26 | — | measure | m cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_unit | int | engine metadata not exposed | — | 27 | — | measure | m unit | integer | non_negative_expected|outlier_check_recommended | m unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_gm | numeric(20,8) | engine metadata not exposed | — | 28 | — | measure | m gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_ngm | numeric(20,8) | engine metadata not exposed | — | 29 | — | measure | m ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_opl | numeric(20,8) | engine metadata not exposed | — | 30 | — | measure | m opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_scm_usage | numeric(20,8) | engine metadata not exposed | — | 31 | — | measure | m scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_tgm | numeric(20,8) | engine metadata not exposed | — | 32 | — | measure | m tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_scm_disc | numeric(20,8) | engine metadata not exposed | — | 33 | — | measure | m scm disc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m scm disc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_scm_ndisc | numeric(20,8) | engine metadata not exposed | — | 34 | — | measure | m scm ndisc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m scm ndisc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_ds_sales | numeric(20,8) | engine metadata not exposed | — | 35 | — | measure | m ds sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m ds sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_stock_sales | numeric(20,8) | engine metadata not exposed | — | 36 | — | measure | m stock sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m stock sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_ds_cost | numeric(20,8) | engine metadata not exposed | — | 37 | — | measure | m ds cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m ds cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_stock_cost | numeric(20,8) | engine metadata not exposed | — | 38 | — | measure | m stock cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m stock cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_ds_scm_usage | numeric(20,8) | engine metadata not exposed | — | 39 | — | measure | m ds scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m ds scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_stock_scm_usage | numeric(20,8) | engine metadata not exposed | — | 40 | — | measure | m stock scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m stock scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_cgp | numeric(20,8) | engine metadata not exposed | — | 41 | — | measure | m cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_total_btl | numeric(20,8) | engine metadata not exposed | — | 42 | — | measure | m total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_sales | numeric(20,8) | engine metadata not exposed | — | 43 | — | measure | pm sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_cost | numeric(20,8) | engine metadata not exposed | — | 44 | — | measure | pm cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_unit | int | engine metadata not exposed | — | 45 | — | measure | pm unit | integer | non_negative_expected|outlier_check_recommended | pm unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_gm | numeric(20,8) | engine metadata not exposed | — | 46 | — | measure | pm gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_ngm | numeric(20,8) | engine metadata not exposed | — | 47 | — | measure | pm ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_opl | numeric(20,8) | engine metadata not exposed | — | 48 | — | measure | pm opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_scm_usage | numeric(20,8) | engine metadata not exposed | — | 49 | — | measure | pm scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_tgm | numeric(20,8) | engine metadata not exposed | — | 50 | — | measure | pm tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_scm_disc | numeric(20,8) | engine metadata not exposed | — | 51 | — | measure | pm scm disc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm scm disc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_scm_ndisc | numeric(20,8) | engine metadata not exposed | — | 52 | — | measure | pm scm ndisc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm scm ndisc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_ds_sales | numeric(20,8) | engine metadata not exposed | — | 53 | — | measure | pm ds sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm ds sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_stock_sales | numeric(20,8) | engine metadata not exposed | — | 54 | — | measure | pm stock sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm stock sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_ds_cost | numeric(20,8) | engine metadata not exposed | — | 55 | — | measure | pm ds cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm ds cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_stock_cost | numeric(20,8) | engine metadata not exposed | — | 56 | — | measure | pm stock cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm stock cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_ds_scm_usage | numeric(20,8) | engine metadata not exposed | — | 57 | — | measure | pm ds scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm ds scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_stock_scm_usage | numeric(20,8) | engine metadata not exposed | — | 58 | — | measure | pm stock scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm stock scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_cgp | numeric(20,8) | engine metadata not exposed | — | 59 | — | measure | pm cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_total_btl | numeric(20,8) | engine metadata not exposed | — | 60 | — | measure | pm total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_sales | numeric(20,8) | engine metadata not exposed | — | 61 | — | measure | ppm sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_cost | numeric(20,8) | engine metadata not exposed | — | 62 | — | measure | ppm cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_unit | int | engine metadata not exposed | — | 63 | — | measure | ppm unit | integer | non_negative_expected|outlier_check_recommended | ppm unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_gm | numeric(20,8) | engine metadata not exposed | — | 64 | — | measure | ppm gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_ngm | numeric(20,8) | engine metadata not exposed | — | 65 | — | measure | ppm ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_opl | numeric(20,8) | engine metadata not exposed | — | 66 | — | measure | ppm opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_scm_usage | numeric(20,8) | engine metadata not exposed | — | 67 | — | measure | ppm scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_tgm | numeric(20,8) | engine metadata not exposed | — | 68 | — | measure | ppm tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_scm_disc | numeric(20,8) | engine metadata not exposed | — | 69 | — | measure | ppm scm disc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm scm disc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_scm_ndisc | numeric(20,8) | engine metadata not exposed | — | 70 | — | measure | ppm scm ndisc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm scm ndisc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_ds_sales | numeric(20,8) | engine metadata not exposed | — | 71 | — | measure | ppm ds sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm ds sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_stock_sales | numeric(20,8) | engine metadata not exposed | — | 72 | — | measure | ppm stock sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm stock sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_ds_cost | numeric(20,8) | engine metadata not exposed | — | 73 | — | measure | ppm ds cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm ds cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_stock_cost | numeric(20,8) | engine metadata not exposed | — | 74 | — | measure | ppm stock cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm stock cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_ds_scm_usage | numeric(20,8) | engine metadata not exposed | — | 75 | — | measure | ppm ds scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm ds scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_stock_scm_usage | numeric(20,8) | engine metadata not exposed | — | 76 | — | measure | ppm stock scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm stock scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_cgp | numeric(20,8) | engine metadata not exposed | — | 77 | — | measure | ppm cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_total_btl | numeric(20,8) | engine metadata not exposed | — | 78 | — | measure | ppm total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_sales | numeric(20,8) | engine metadata not exposed | — | 79 | — | measure | lm sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_cost | numeric(20,8) | engine metadata not exposed | — | 80 | — | measure | lm cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_unit | int | engine metadata not exposed | — | 81 | — | measure | lm unit | integer | non_negative_expected|outlier_check_recommended | lm unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_gm | numeric(20,8) | engine metadata not exposed | — | 82 | — | measure | lm gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_ngm | numeric(20,8) | engine metadata not exposed | — | 83 | — | measure | lm ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_opl | numeric(20,8) | engine metadata not exposed | — | 84 | — | measure | lm opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_scm_usage | numeric(20,8) | engine metadata not exposed | — | 85 | — | measure | lm scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_tgm | numeric(20,8) | engine metadata not exposed | — | 86 | — | measure | lm tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_scm_disc | numeric(20,8) | engine metadata not exposed | — | 87 | — | measure | lm scm disc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm scm disc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_scm_ndisc | numeric(20,8) | engine metadata not exposed | — | 88 | — | measure | lm scm ndisc | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm scm ndisc; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_ds_sales | numeric(20,8) | engine metadata not exposed | — | 89 | — | measure | lm ds sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm ds sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_stock_sales | numeric(20,8) | engine metadata not exposed | — | 90 | — | measure | lm stock sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm stock sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_ds_cost | numeric(20,8) | engine metadata not exposed | — | 91 | — | measure | lm ds cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm ds cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_stock_cost | numeric(20,8) | engine metadata not exposed | — | 92 | — | measure | lm stock cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm stock cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_ds_scm_usage | numeric(20,8) | engine metadata not exposed | — | 93 | — | measure | lm ds scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm ds scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_stock_scm_usage | numeric(20,8) | engine metadata not exposed | — | 94 | — | measure | lm stock scm usage | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm stock scm usage; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_cgp | numeric(20,8) | engine metadata not exposed | — | 95 | — | measure | lm cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_total_btl | numeric(20,8) | engine metadata not exposed | — | 96 | — | measure | lm total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_gross_sales | numeric(20,8) | engine metadata not exposed | — | 97 | — | measure | bo gross sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo gross sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_gross_cost | numeric(20,8) | engine metadata not exposed | — | 98 | — | measure | bo gross cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo gross cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_total_unit | int | engine metadata not exposed | — | 99 | — | measure | bo total unit | integer | non_negative_expected|outlier_check_recommended | bo total unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_gm_amt | numeric(20,8) | engine metadata not exposed | — | 100 | — | measure | bo gm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo gm amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_gross_sales | numeric(20,8) | engine metadata not exposed | — | 101 | — | measure | so gross sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so gross sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_gross_cost | numeric(20,8) | engine metadata not exposed | — | 102 | — | measure | so gross cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so gross cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_total_unit | int | engine metadata not exposed | — | 103 | — | measure | so total unit | integer | non_negative_expected|outlier_check_recommended | so total unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_gm_amt | numeric(20,8) | engine metadata not exposed | — | 104 | — | measure | so gm amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so gm amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_age0_7 | numeric(20,8) | engine metadata not exposed | — | 105 | — | measure | bo age0 7 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age0 7; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_age8_14 | numeric(20,8) | engine metadata not exposed | — | 106 | — | measure | bo age8 14 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age8 14; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_age15_21 | numeric(20,8) | engine metadata not exposed | — | 107 | — | measure | bo age15 21 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age15 21; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| bo_age21_up | numeric(20,8) | engine metadata not exposed | — | 108 | — | measure | bo age21 up | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | bo age21 up; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_age0_7 | numeric(20,8) | engine metadata not exposed | — | 109 | — | measure | so age0 7 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age0 7; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_age8_14 | numeric(20,8) | engine metadata not exposed | — | 110 | — | measure | so age8 14 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age8 14; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_age15_21 | numeric(20,8) | engine metadata not exposed | — | 111 | — | measure | so age15 21 | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age15 21; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| so_age21_up | numeric(20,8) | engine metadata not exposed | — | 112 | — | measure | so age21 up | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | so age21 up; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_unit | int | engine metadata not exposed | — | 113 | — | measure | rr unit | integer | non_negative_expected|outlier_check_recommended | rr unit; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_sales | numeric(20,8) | engine metadata not exposed | — | 114 | — | measure | rr sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr sales; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_cost | numeric(20,8) | engine metadata not exposed | — | 115 | — | measure | rr cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_gm | numeric(20,8) | engine metadata not exposed | — | 116 | — | measure | rr gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr gm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_ngm | numeric(20,8) | engine metadata not exposed | — | 117 | — | measure | rr ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr ngm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_opl | numeric(20,8) | engine metadata not exposed | — | 118 | — | measure | rr opl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr opl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_cgp | numeric(20,8) | engine metadata not exposed | — | 119 | — | measure | rr cgp | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr cgp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_total_btl | numeric(20,8) | engine metadata not exposed | — | 120 | — | measure | rr total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr total btl; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_tgm | numeric(20,8) | engine metadata not exposed | — | 121 | — | measure | rr tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr tgm; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 122 | — | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| goal_nsales | numeric(20,8) | engine metadata not exposed | — | 123 | — | measure | goal nsales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal nsales; goal target joined from sales goal view at serving grain. | — |
| goal_gm | numeric(20,8) | engine metadata not exposed | — | 124 | — | measure | goal gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal gm; goal target joined from sales goal view at serving grain. | — |
| goal_ngm | numeric(20,8) | engine metadata not exposed | — | 125 | — | measure | goal ngm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal ngm; goal target joined from sales goal view at serving grain. | — |
| goal_opl_gm | numeric(20,8) | engine metadata not exposed | — | 126 | — | measure | goal opl gm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal opl gm; goal target joined from sales goal view at serving grain. | — |
| goal_tgm | numeric(20,8) | engine metadata not exposed | — | 127 | — | measure | goal tgm | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal tgm; goal target joined from sales goal view at serving grain. | — |
| goal_dos | numeric(20,8) | engine metadata not exposed | — | 128 | — | measure | goal dos | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal dos; goal target joined from sales goal view at serving grain. | — |
| goal_pdt | numeric(20,8) | engine metadata not exposed | — | 129 | — | measure | goal pdt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal pdt; goal target joined from sales goal view at serving grain. | — |
| goal_total_btl | numeric(20,8) | engine metadata not exposed | — | 130 | — | measure | goal total btl | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal total btl; goal target joined from sales goal view at serving grain. | — |
| goal_cust_cnt | int | engine metadata not exposed | — | 131 | — | measure | goal cust cnt | integer | non_negative_expected|outlier_check_recommended | goal cust cnt; goal target joined from sales goal view at serving grain. | — |
| d_fx_cost | numeric(20,8) | engine metadata not exposed | — | 132 | — | measure | d fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d fx cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_fx_cost | numeric(20,8) | engine metadata not exposed | — | 133 | — | measure | w fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w fx cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_fx_cost | numeric(20,8) | engine metadata not exposed | — | 134 | — | measure | m fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m fx cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_fx_cost | numeric(20,8) | engine metadata not exposed | — | 135 | — | measure | pm fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm fx cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_fx_cost | numeric(20,8) | engine metadata not exposed | — | 136 | — | measure | ppm fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm fx cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_fx_cost | numeric(20,8) | engine metadata not exposed | — | 137 | — | measure | lm fx cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm fx cost; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| goal_soft_sales | numeric(20,8) | engine metadata not exposed | — | 138 | — | measure | goal soft sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal soft sales; goal target joined from sales goal view at serving grain. | — |
| date_flag | date | engine metadata not exposed | — | 139 | — | key | date flag | YYYY-MM-DD | not_null_expected|dim_fk_check_recommended | Business date partition; use month-end row for MTD month totals. | `dim_us.dim_pub_date.date_flag` |
| d_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 140 | — | measure | d oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | d oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| w_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 141 | — | measure | w oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | w oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| m_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 142 | — | measure | m oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | m oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| pm_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 143 | — | measure | pm oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | pm oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| ppm_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 144 | — | measure | ppm oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ppm oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| lm_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 145 | — | measure | lm oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | lm oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| rr_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 146 | — | measure | rr oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rr oplgm plus amt; MTD cumulative measure or dimension on `dw_us.dws_disty_brpt_division_comb_mtd` B Report serving slice. | — |
| goal_oplgm_plus_amt | numeric(20,8) | engine metadata not exposed | — | 147 | — | measure | goal oplgm plus amt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | goal oplgm plus amt; goal target joined from sales goal view at serving grain. | — |


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
  - confidence: medium
  - source_type: clickhouse
  - confidence: medium
- lineage_notes:
  - Compass catalog lookup executed first; CK lineage used as fallback evidence.
### Column Lineage and Derivation
- column_lineage:
  - column_name: key_metric_bundle
  - lineage_type: derived
  - source_columns:
    - source_table: —
    - source_column: —
  - derivation_formula: full join table_goal
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

### Metric Serving Map

Logical metrics in L2 map to physical `lm_*` / `m_*` / `pm_*` / `ppm_*` columns on this comb_mtd table.
Use these mappings for scalar lookups; formulas remain in `metric-index.md`.

- `net_sales@last_month`: `lm_sales`
- `net_sales@relative`: `lm_sales`
- `net_sales@current_month`: `m_sales`
- `net_sales@prior_month`: `pm_sales`
- `net_sales@prior_prior_month`: `ppm_sales`
- `gm_amt@last_month`: `lm_gm`
- `gm_amt@relative`: `lm_gm`
- `gm_amt@current_month`: `m_gm`
- `gm_amt@prior_month`: `pm_gm`
- `gm_amt@prior_prior_month`: `ppm_gm`
- `ngm_amt@last_month`: `lm_ngm`
- `ngm_amt@relative`: `lm_ngm`
- `ngm_amt@current_month`: `m_ngm`
- `ngm_amt@prior_month`: `pm_ngm`
- `ngm_amt@prior_prior_month`: `ppm_ngm`
- `tgm_amt@last_month`: `lm_tgm`
- `tgm_amt@relative`: `lm_tgm`
- `tgm_amt@current_month`: `m_tgm`
- `tgm_amt@prior_month`: `pm_tgm`
- `tgm_amt@prior_prior_month`: `ppm_tgm`
- `oplgm_amt@last_month`: `lm_opl`
- `oplgm_amt@relative`: `lm_opl`
- `oplgm_amt@current_month`: `m_opl`
- `oplgm_amt@prior_month`: `pm_opl`
- `oplgm_amt@prior_prior_month`: `ppm_opl`
- `oplgm_plus_amt@last_month`: `lm_oplgm_plus_amt`
- `oplgm_plus_amt@relative`: `lm_oplgm_plus_amt`
- `oplgm_plus_amt@current_month`: `m_oplgm_plus_amt`
- `oplgm_plus_amt@prior_month`: `pm_oplgm_plus_amt`
- `oplgm_plus_amt@prior_prior_month`: `ppm_oplgm_plus_amt`
- `total_btl@last_month`: `lm_total_btl`
- `total_btl@relative`: `lm_total_btl`
- `total_btl@current_month`: `m_total_btl`
- `total_btl@prior_month`: `pm_total_btl`
- `total_btl@prior_prior_month`: `ppm_total_btl`


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
table_fqn: dw_us.dws_disty_brpt_division_comb_mtd
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(lm_ngm) AS ngm_amt
FROM dw_us.dws_disty_brpt_division_comb_mtd
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dw_us.dws_disty_brpt_division_comb_mtd
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_division_comb_mtd t
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
table_fqn: dw_us.dws_disty_brpt_division_comb_mtd
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT d.month_start, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_division_comb_mtd t
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

4) Relative last month (comb_mtd snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dw_us.dws_disty_brpt_division_comb_mtd
grain: comb_mtd_lm_snapshot
anti_use: borrow date_flag anchor + lm_* column choice only; not ranking SQL
-->
```sql
SELECT SUM(t.lm_sales) AS net_sales
FROM dw_us.dws_disty_brpt_division_comb_mtd t
WHERE t.date_flag = (
  SELECT MAX(date_flag)
  FROM dw_us.dws_disty_brpt_division_comb_mtd
  WHERE date_flag >= '{{period_start}}'
    AND date_flag < '{{period_end}}'
);
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
table_fqn: dw_us.dws_disty_brpt_division_comb_mtd
anti_use: daily date_flag scan only; not routing_certified; do not copy for ranking
-->
```sql
SELECT date_flag, SUM(lm_ngm) AS ngm_amt, SUM(lm_sales) AS net_sales
FROM dw_us.dws_disty_brpt_division_comb_mtd
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```