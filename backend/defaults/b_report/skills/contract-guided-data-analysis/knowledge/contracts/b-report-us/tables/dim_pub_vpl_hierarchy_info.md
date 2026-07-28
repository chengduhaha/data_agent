# dim_us.dim_pub_vpl_hierarchy_info

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_vpl_hierarchy_info
- domain: b-report-us
- one_line_purpose: PM/Buyer organizational hierarchy by VPL — map `pm_id`/`buyer_id` to management chain

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_vpl_hierarchy_info`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_vpl_hierarchy_info`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive: `dim_us.dim_pub_vpl_hierarchy_info` verified present.
- Vertica: `dim_us.dim_pub_vpl_hierarchy_info` verified present.
- Row count (Vertica, 2026-06-25): 98,593 rows; `vpl_no` unique at grain (one hierarchy row per VPL).
- Role cardinality: 292 distinct `pm_id`; 167 distinct `buyer_id`.
- Snapshot variant: `dim_pub_vpl_hierarchy_info_df` for as-of hierarchy in serving ETL.

### Column Catalog (100% columns)

- documented_column_count: 107
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| vend_no | int | engine metadata not exposed | — | 1 | vend # from ods_cis_dbo_dw_vend_pl | key | vend no | integer | not_null_expected|dim_fk_check_recommended | vend no; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | `dim_us.dim_pub_vendor_info.vend_no` |
| vpl_no | int | engine metadata not exposed | — | 2 | Unique ID for VPC (Vendor Product Code) | key | vpl no | integer | not_null_expected|dim_fk_check_recommended | vpl no; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | `dim_us.dim_pub_vpl_info.vpl_no` |
| buyer_vp_id | int | engine metadata not exposed | — | 3 | buyer vp id | key | buyer vp id | integer | not_null_expected|dim_fk_check_recommended | buyer vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_vp_name | varchar(200) | engine metadata not exposed | — | 4 | buyer vp name | dimension | buyer vp name | categorical_or_expression_text | domain_value_check_recommended | buyer vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_vp_email | varchar(200) | engine metadata not exposed | — | 5 | buyer vp email | dimension | buyer vp email | categorical_or_expression_text | domain_value_check_recommended | buyer vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_director_id | int | engine metadata not exposed | — | 6 | buyer's director id | key | buyer director id | integer | not_null_expected|dim_fk_check_recommended | buyer director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_director_name | varchar(200) | engine metadata not exposed | — | 7 | buyer's director name | dimension | buyer director name | categorical_or_expression_text | domain_value_check_recommended | buyer director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_director_email | varchar(200) | engine metadata not exposed | — | 8 | buyer's director email | dimension | buyer director email | categorical_or_expression_text | domain_value_check_recommended | buyer director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_manager_id | int | engine metadata not exposed | — | 9 | buyer's manager id | key | buyer manager id | integer | not_null_expected|dim_fk_check_recommended | buyer manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_manager_name | varchar(200) | engine metadata not exposed | — | 10 | buyer manager's name | dimension | buyer manager name | categorical_or_expression_text | domain_value_check_recommended | buyer manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_manager_email | varchar(200) | engine metadata not exposed | — | 11 | buyer's manager email | dimension | buyer manager email | categorical_or_expression_text | domain_value_check_recommended | buyer manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_id | int | engine metadata not exposed | — | 12 | buyer's id | key | buyer id | integer | not_null_expected|dim_fk_check_recommended | buyer id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | `dim_us.dim_pub_vpl_hierarchy_info.buyer_id` |
| buyer_name | varchar(200) | engine metadata not exposed | — | 13 | buyer's name | dimension | buyer name | categorical_or_expression_text | domain_value_check_recommended | buyer name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_email | varchar(200) | engine metadata not exposed | — | 14 | buyer's email | dimension | buyer email | categorical_or_expression_text | domain_value_check_recommended | buyer email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_primary_backup_id | int | engine metadata not exposed | — | 15 | buyer's primary backup id | key | buyer primary backup id | integer | not_null_expected|dim_fk_check_recommended | buyer primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_primary_backup_name | varchar(200) | engine metadata not exposed | — | 16 | buyer's primary backup name | dimension | buyer primary backup name | categorical_or_expression_text | domain_value_check_recommended | buyer primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| buyer_primary_backup_email | varchar(200) | engine metadata not exposed | — | 17 | buyer's primary backup email | dimension | buyer primary backup email | categorical_or_expression_text | domain_value_check_recommended | buyer primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_vp_id | int | engine metadata not exposed | — | 18 | bjbr's vp id | key | bjbr vp id | integer | not_null_expected|dim_fk_check_recommended | bjbr vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_vp_name | varchar(200) | engine metadata not exposed | — | 19 | bjbr's vp name | dimension | bjbr vp name | categorical_or_expression_text | domain_value_check_recommended | bjbr vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_vp_email | varchar(200) | engine metadata not exposed | — | 20 | bjbr's vp email | dimension | bjbr vp email | categorical_or_expression_text | domain_value_check_recommended | bjbr vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_director_id | int | engine metadata not exposed | — | 21 | bjbr's director id | key | bjbr director id | integer | not_null_expected|dim_fk_check_recommended | bjbr director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_director_name | varchar(200) | engine metadata not exposed | — | 22 | bjbr's director name | dimension | bjbr director name | categorical_or_expression_text | domain_value_check_recommended | bjbr director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_director_email | varchar(200) | engine metadata not exposed | — | 23 | bjbr's director email | dimension | bjbr director email | categorical_or_expression_text | domain_value_check_recommended | bjbr director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_manager_id | int | engine metadata not exposed | — | 24 | bjbr's manager id | key | bjbr manager id | integer | not_null_expected|dim_fk_check_recommended | bjbr manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_manager_name | varchar(200) | engine metadata not exposed | — | 25 | bjbr's manager name | dimension | bjbr manager name | categorical_or_expression_text | domain_value_check_recommended | bjbr manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_manager_email | varchar(200) | engine metadata not exposed | — | 26 | bjbr's manager email | dimension | bjbr manager email | categorical_or_expression_text | domain_value_check_recommended | bjbr manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_id | int | engine metadata not exposed | — | 27 | bjbr's id | key | bjbr id | integer | not_null_expected|dim_fk_check_recommended | bjbr id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_name | varchar(200) | engine metadata not exposed | — | 28 | bjbr's name | dimension | bjbr name | categorical_or_expression_text | domain_value_check_recommended | bjbr name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_email | varchar(200) | engine metadata not exposed | — | 29 | bjbr's email | dimension | bjbr email | categorical_or_expression_text | domain_value_check_recommended | bjbr email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_primary_backup_id | int | engine metadata not exposed | — | 30 | bjbr's primary backup id | key | bjbr primary backup id | integer | not_null_expected|dim_fk_check_recommended | bjbr primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_primary_backup_name | varchar(200) | engine metadata not exposed | — | 31 | bjbr's primary backup name | dimension | bjbr primary backup name | categorical_or_expression_text | domain_value_check_recommended | bjbr primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbr_primary_backup_email | varchar(200) | engine metadata not exposed | — | 32 | bjbr's primary backup email | dimension | bjbr primary backup email | categorical_or_expression_text | domain_value_check_recommended | bjbr primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_vp_id | int | engine metadata not exposed | — | 33 | bjbn's vp id | key | bjbn vp id | integer | not_null_expected|dim_fk_check_recommended | bjbn vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_vp_name | varchar(200) | engine metadata not exposed | — | 34 | bjbn's vp name | dimension | bjbn vp name | categorical_or_expression_text | domain_value_check_recommended | bjbn vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_vp_email | varchar(200) | engine metadata not exposed | — | 35 | bjbn's vp email | dimension | bjbn vp email | categorical_or_expression_text | domain_value_check_recommended | bjbn vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_director_id | int | engine metadata not exposed | — | 36 | bjbn's director id | key | bjbn director id | integer | not_null_expected|dim_fk_check_recommended | bjbn director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_director_name | varchar(200) | engine metadata not exposed | — | 37 | bjbn's director name | dimension | bjbn director name | categorical_or_expression_text | domain_value_check_recommended | bjbn director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_director_email | varchar(200) | engine metadata not exposed | — | 38 | bjbn's director email | dimension | bjbn director email | categorical_or_expression_text | domain_value_check_recommended | bjbn director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_manager_id | int | engine metadata not exposed | — | 39 | bjbn's manager id | key | bjbn manager id | integer | not_null_expected|dim_fk_check_recommended | bjbn manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_manager_name | varchar(200) | engine metadata not exposed | — | 40 | bjbn's manager name | dimension | bjbn manager name | categorical_or_expression_text | domain_value_check_recommended | bjbn manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_manager_email | varchar(200) | engine metadata not exposed | — | 41 | bjbn's manager email | dimension | bjbn manager email | categorical_or_expression_text | domain_value_check_recommended | bjbn manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_id | int | engine metadata not exposed | — | 42 | bjbn's id | key | bjbn id | integer | not_null_expected|dim_fk_check_recommended | bjbn id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_name | varchar(200) | engine metadata not exposed | — | 43 | bjbn's name | dimension | bjbn name | categorical_or_expression_text | domain_value_check_recommended | bjbn name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_email | varchar(200) | engine metadata not exposed | — | 44 | bjbn's email | dimension | bjbn email | categorical_or_expression_text | domain_value_check_recommended | bjbn email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_primary_backup_id | int | engine metadata not exposed | — | 45 | bjbn's primary backup id | key | bjbn primary backup id | integer | not_null_expected|dim_fk_check_recommended | bjbn primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_primary_backup_name | varchar(200) | engine metadata not exposed | — | 46 | bjbn's primary backup name | dimension | bjbn primary backup name | categorical_or_expression_text | domain_value_check_recommended | bjbn primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| bjbn_primary_backup_email | varchar(200) | engine metadata not exposed | — | 47 | bjbn's primary backup email | dimension | bjbn primary backup email | categorical_or_expression_text | domain_value_check_recommended | bjbn primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_vp_id | int | engine metadata not exposed | — | 48 | vcm's vp id | key | vcm vp id | integer | not_null_expected|dim_fk_check_recommended | vcm vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_vp_name | varchar(200) | engine metadata not exposed | — | 49 | vcm's vp name | dimension | vcm vp name | categorical_or_expression_text | domain_value_check_recommended | vcm vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_vp_email | varchar(200) | engine metadata not exposed | — | 50 | vcm's vp email | dimension | vcm vp email | categorical_or_expression_text | domain_value_check_recommended | vcm vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_director_id | int | engine metadata not exposed | — | 51 | vcm's director id | key | vcm director id | integer | not_null_expected|dim_fk_check_recommended | vcm director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_director_name | varchar(200) | engine metadata not exposed | — | 52 | vcm's director name | dimension | vcm director name | categorical_or_expression_text | domain_value_check_recommended | vcm director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_director_email | varchar(200) | engine metadata not exposed | — | 53 | vcm's director email | dimension | vcm director email | categorical_or_expression_text | domain_value_check_recommended | vcm director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_manager_id | int | engine metadata not exposed | — | 54 | vcm's manager id | key | vcm manager id | integer | not_null_expected|dim_fk_check_recommended | vcm manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_manager_name | varchar(200) | engine metadata not exposed | — | 55 | vcm's manager name | dimension | vcm manager name | categorical_or_expression_text | domain_value_check_recommended | vcm manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_manager_email | varchar(200) | engine metadata not exposed | — | 56 | vcm's manager email | dimension | vcm manager email | categorical_or_expression_text | domain_value_check_recommended | vcm manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_id | int | engine metadata not exposed | — | 57 | vcm's id | key | vcm id | integer | not_null_expected|dim_fk_check_recommended | vcm id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_name | varchar(200) | engine metadata not exposed | — | 58 | vcm's name | dimension | vcm name | categorical_or_expression_text | domain_value_check_recommended | vcm name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_email | varchar(200) | engine metadata not exposed | — | 59 | vcm's email | dimension | vcm email | categorical_or_expression_text | domain_value_check_recommended | vcm email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_primary_backup_id | int | engine metadata not exposed | — | 60 | vcm's primary backup id | key | vcm primary backup id | integer | not_null_expected|dim_fk_check_recommended | vcm primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_primary_backup_name | varchar(200) | engine metadata not exposed | — | 61 | vcm's primary backup name | dimension | vcm primary backup name | categorical_or_expression_text | domain_value_check_recommended | vcm primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| vcm_primary_backup_email | varchar(200) | engine metadata not exposed | — | 62 | vcm's primary backup email | dimension | vcm primary backup email | categorical_or_expression_text | domain_value_check_recommended | vcm primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_vp_id | int | engine metadata not exposed | — | 63 | marketing's vp id | key | marketing vp id | integer | not_null_expected|dim_fk_check_recommended | marketing vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_vp_name | varchar(200) | engine metadata not exposed | — | 64 | marketing's vp name | dimension | marketing vp name | categorical_or_expression_text | domain_value_check_recommended | marketing vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_vp_email | varchar(200) | engine metadata not exposed | — | 65 | marketing's vp email | dimension | marketing vp email | categorical_or_expression_text | domain_value_check_recommended | marketing vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_director_id | int | engine metadata not exposed | — | 66 | marketing's director id | key | marketing director id | integer | not_null_expected|dim_fk_check_recommended | marketing director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_director_name | varchar(200) | engine metadata not exposed | — | 67 | marketing's director name | dimension | marketing director name | categorical_or_expression_text | domain_value_check_recommended | marketing director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_director_email | varchar(200) | engine metadata not exposed | — | 68 | marketing's director email | dimension | marketing director email | categorical_or_expression_text | domain_value_check_recommended | marketing director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_manager_id | int | engine metadata not exposed | — | 69 | marketing's manager id | key | marketing manager id | integer | not_null_expected|dim_fk_check_recommended | marketing manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_manager_name | varchar(200) | engine metadata not exposed | — | 70 | marketing's manager name | dimension | marketing manager name | categorical_or_expression_text | domain_value_check_recommended | marketing manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_manager_email | varchar(200) | engine metadata not exposed | — | 71 | marketing's manager email | dimension | marketing manager email | categorical_or_expression_text | domain_value_check_recommended | marketing manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_id | int | engine metadata not exposed | — | 72 | marketing's id | key | marketing id | integer | not_null_expected|dim_fk_check_recommended | marketing id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_name | varchar(200) | engine metadata not exposed | — | 73 | marketing's name | dimension | marketing name | categorical_or_expression_text | domain_value_check_recommended | marketing name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_email | varchar(200) | engine metadata not exposed | — | 74 | marketing's email | dimension | marketing email | categorical_or_expression_text | domain_value_check_recommended | marketing email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_primary_backup_id | int | engine metadata not exposed | — | 75 | marketing's primary backup id | key | marketing primary backup id | integer | not_null_expected|dim_fk_check_recommended | marketing primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_primary_backup_name | varchar(200) | engine metadata not exposed | — | 76 | marketing's primary backup name | dimension | marketing primary backup name | categorical_or_expression_text | domain_value_check_recommended | marketing primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| marketing_primary_backup_email | varchar(200) | engine metadata not exposed | — | 77 | marketing's primary backup email | dimension | marketing primary backup email | categorical_or_expression_text | domain_value_check_recommended | marketing primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_vp_id | int | engine metadata not exposed | — | 78 | pm's vp id | key | pm vp id | integer | not_null_expected|dim_fk_check_recommended | pm vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_vp_name | varchar(200) | engine metadata not exposed | — | 79 | pm's vp name | dimension | pm vp name | categorical_or_expression_text | domain_value_check_recommended | pm vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_vp_email | varchar(200) | engine metadata not exposed | — | 80 | pm's vp email | dimension | pm vp email | categorical_or_expression_text | domain_value_check_recommended | pm vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_director_id | int | engine metadata not exposed | — | 81 | pm's director id | key | pm director id | integer | not_null_expected|dim_fk_check_recommended | pm director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_director_name | varchar(200) | engine metadata not exposed | — | 82 | pm's director name | dimension | pm director name | categorical_or_expression_text | domain_value_check_recommended | pm director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_director_email | varchar(200) | engine metadata not exposed | — | 83 | pm's director email | dimension | pm director email | categorical_or_expression_text | domain_value_check_recommended | pm director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_manager_id | int | engine metadata not exposed | — | 84 | pm's manager id | key | pm manager id | integer | not_null_expected|dim_fk_check_recommended | pm manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_manager_name | varchar(200) | engine metadata not exposed | — | 85 | pm's manager name | dimension | pm manager name | categorical_or_expression_text | domain_value_check_recommended | pm manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_manager_email | varchar(200) | engine metadata not exposed | — | 86 | pm's manager email | dimension | pm manager email | categorical_or_expression_text | domain_value_check_recommended | pm manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_id | int | engine metadata not exposed | — | 87 | pm's id | key | pm id | integer | not_null_expected|dim_fk_check_recommended | pm id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | `dim_us.dim_pub_vpl_hierarchy_info.pm_id` |
| pm_name | varchar(200) | engine metadata not exposed | — | 88 | pm's name | dimension | pm name | categorical_or_expression_text | domain_value_check_recommended | pm name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_email | varchar(200) | engine metadata not exposed | — | 89 | pm's email | dimension | pm email | categorical_or_expression_text | domain_value_check_recommended | pm email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_primary_backup_id | int | engine metadata not exposed | — | 90 | pm's primary backup id | key | pm primary backup id | integer | not_null_expected|dim_fk_check_recommended | pm primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_primary_backup_name | varchar(200) | engine metadata not exposed | — | 91 | pm's primary backup name | dimension | pm primary backup name | categorical_or_expression_text | domain_value_check_recommended | pm primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pm_primary_backup_email | varchar(200) | engine metadata not exposed | — | 92 | pm's primary backup email | dimension | pm primary backup email | categorical_or_expression_text | domain_value_check_recommended | pm primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_vp_id | int | engine metadata not exposed | — | 93 | pana's vp id | key | pana vp id | integer | not_null_expected|dim_fk_check_recommended | pana vp id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_vp_name | varchar(100) | engine metadata not exposed | — | 94 | pana's vp name | dimension | pana vp name | categorical_or_expression_text | domain_value_check_recommended | pana vp name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_vp_email | varchar(100) | engine metadata not exposed | — | 95 | pana's vp email | dimension | pana vp email | categorical_or_expression_text | domain_value_check_recommended | pana vp email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_director_id | int | engine metadata not exposed | — | 96 | pana's director id | key | pana director id | integer | not_null_expected|dim_fk_check_recommended | pana director id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_director_name | varchar(100) | engine metadata not exposed | — | 97 | pana's director name | dimension | pana director name | categorical_or_expression_text | domain_value_check_recommended | pana director name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_director_email | varchar(100) | engine metadata not exposed | — | 98 | pana's director email | dimension | pana director email | categorical_or_expression_text | domain_value_check_recommended | pana director email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_manager_id | int | engine metadata not exposed | — | 99 | pana's manager id | key | pana manager id | integer | not_null_expected|dim_fk_check_recommended | pana manager id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_manager_name | varchar(100) | engine metadata not exposed | — | 100 | pana's manager name | dimension | pana manager name | categorical_or_expression_text | domain_value_check_recommended | pana manager name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_manager_email | varchar(100) | engine metadata not exposed | — | 101 | pana's manager email | dimension | pana manager email | categorical_or_expression_text | domain_value_check_recommended | pana manager email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_id | int | engine metadata not exposed | — | 102 | pana's id | key | pana id | integer | not_null_expected|dim_fk_check_recommended | pana id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_name | varchar(100) | engine metadata not exposed | — | 103 | pana's name | dimension | pana name | categorical_or_expression_text | domain_value_check_recommended | pana name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_email | varchar(100) | engine metadata not exposed | — | 104 | pana's email | dimension | pana email | categorical_or_expression_text | domain_value_check_recommended | pana email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_primary_backup_id | int | engine metadata not exposed | — | 105 | pana's primary backup id | key | pana primary backup id | integer | not_null_expected|dim_fk_check_recommended | pana primary backup id; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_primary_backup_name | varchar(100) | engine metadata not exposed | — | 106 | pana's primary backup name | dimension | pana primary backup name | categorical_or_expression_text | domain_value_check_recommended | pana primary backup name; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |
| pana_primary_backup_email | varchar(100) | engine metadata not exposed | — | 107 | pana's primary backup email | dimension | pana primary backup email | categorical_or_expression_text | domain_value_check_recommended | pana primary backup email; PM/Buyer hierarchy on `dim_us.dim_pub_vpl_hierarchy_info`; join on `vpl_no` or `pm_id`/`buyer_id`. | — |

### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_userinfo_mymdm_vendor_dna_group`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_vpl_dimension_us.dim_pub_vpl_hierarchy_info`
  - table_fqn: `ods_us.ods_userinfo_mymdm_vendor_dna_members`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: primary/backup/manager/director/VP role IDs per VPL
  - table_fqn: `dim_us.dim_pub_manager`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: manager name/email resolution
- downstream_n_hops:
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `pm_id`, `buyer_id` hierarchy columns
  - table_fqn: `dm_us.dm_disty_brpt_pm_mtd`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: PM performance mart
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high


### Column Lineage and Derivation

- `vpl_no`, `vend_no`: anchor keys for hierarchy row.
- `pm_id`, `pm_mgr_id`, `pm_dir_id`, `pm_vp_id`: pivoted from vendor DNA members with `member_role` filters.
- Equivalent buyer hierarchy IDs from same MDM group/member source.
- Manager names resolved via `dim_pub_manager`.


### Freshness and Load Path

- Producer: `public_vpl_dimension_us.dim_pub_vpl_hierarchy_info`; Vertica sync daily.
- Snapshot: `dim_pub_vpl_hierarchy_info_df` used by B Report common pre-load dependencies.
- Expected completion window: 02:00-05:00 PT.


## L2 Declarative Knowledge

### Business Definitions

- Domain: PM and Buyer organizational hierarchy mapped to VPL/vendor grain.
- Grain: typically one hierarchy row per `vpl_no` (and vendor).
- Used for PM/Buyer rollups on B Report serving tables (`pm_id`, `buyer_id` columns).



### Dimension Keys and Lookup Reference

- Anchor keys: `vpl_no`, `vend_no` — tie hierarchy row to product line and vendor.
- PM chain: `pm_id`, `pm_name`, `pm_manager_id`, `pm_director_id`, `pm_vp_id` (+ `*_name`, `*_email` at each level).
- Buyer chain: `buyer_id`, `buyer_name`, `buyer_manager_id`, `buyer_director_id`, `buyer_vp_id` (+ names/emails).
- Additional role families: `bjbr_*`, `bjbn_*`, `vcm_*`, `marketing_*`, `pana_*` — specialized PM/buyer variants per VPL DNA group.
- Manager names resolved via `dim_us.dim_pub_manager` during ETL.

### Dimension Lookup / Join Reference

- `vend_no` → `dim_us.dim_pub_vendor_info.vend_no` | join: `dim_pub_vpl_hierarchy_info.vend_no = dim_pub_vendor_info.vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `vpl_no` → `dim_us.dim_pub_vpl_info.vpl_no` | join: `dim_pub_vpl_hierarchy_info.vpl_no = dim_pub_vpl_info.vpl_no` | lookup labels: `vpl_code`, `vpl_desc` | cardinality: many:1 | confidence: high (KB-wide ref index)


### Identifier Search Profile

- searchable_identifier_columns:
  - column: `pm_name`
    data_type: varchar
    match_mode: exact then contains_like
  - column: `buyer_name`
    data_type: varchar
    match_mode: exact then contains_like
  - column: `pm_manager_name`
    data_type: varchar
    match_mode: contains_like
  - column: `buyer_manager_name`
    data_type: varchar
    match_mode: contains_like
- non_searchable_key_columns: `pm_id`, `buyer_id`, `vpl_no`, `vend_no`, all `*_id` hierarchy keys — integer only
- user_facing_aliases: `pm`, `product manager`, `buyer`, `purchasing manager` → search `pm_name` / `buyer_name`
- resolution_flow: user PM/buyer name → `ILIKE` on `pm_name` or `buyer_name` → obtain `pm_id` or `buyer_id` → join serving on `fact.pm_id` or filter `pl_extend.pm_id`

### Column Profiling (key vs label)

| column_name | distinct_count | total_rows | uniqueness | safe_for_group_by | notes |
| --- | --- | --- | --- | --- | --- |
| vpl_no | 98593 | 98593 | unique | yes | grain key with vendor |
| pm_id | 292 | 98593 | non_unique | yes | PM roll-up key |
| buyer_id | 167 | 98593 | non_unique | yes | buyer roll-up key |
| pm_name | — | 98593 | non_unique | no | search only |

### Time Field Semantics

- Use `dim_pub_vpl_hierarchy_info_df` with `date_flag` for as-of hierarchy in serving ETL.

### Metrics Served

- Dimension attributes only; no fact metrics stored on this table


## L3 Procedural Knowledge

### Query and Routing Rules

- Use when question scopes by PM or Buyer person name rather than integer `pm_id`/`buyer_id`.
- PM performance metrics: prefer `dm_us.dm_disty_brpt_pm_mtd` — see golden `pm-735781-ngm`.
- Join path for VPL-level PM: `fact.vpl_no = dim_pub_vpl_hierarchy_info.vpl_no` to expand management chain.
- Join path for PM-scoped serving: `fact.pm_id = dim_pub_vpl_hierarchy_info.pm_id` (many VPL rows per PM — do not use for VPL-grain metrics without care).
- Use `dim_pub_vpl_hierarchy_info_df` with `date_flag` when historical PM assignment matters.

### Dimension Join Patterns

- VPL grain: `fact.vpl_no = dim_pub_vpl_hierarchy_info.vpl_no` (1:1 at VPL grain)
- PM grain: `fact.pm_id = dim_pub_vpl_hierarchy_info.pm_id` (1:many — one PM covers many VPLs)
- Buyer grain: `fact.buyer_id = dim_pub_vpl_hierarchy_info.buyer_id`
- Vendor context: `dim_pub_vpl_hierarchy_info.vend_no = dim_pub_vendor_info.vend_no`
- High-risk pitfalls: joining on `pm_name` instead of `pm_id`; double-counting when expanding VPL→PM at wrong grain

### Key Filters and ETL Business Logic

- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard Time-Filter SQL (3 snippets)

Time-filter snippets below apply to **fact/serving tables** joined to this dimension for metric questions. This dimension has no `date_flag`; use `*_df` snapshot variants when as-of attributes are required.

1) Natural month (month-end snapshot)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_pub_vpl_hierarchy_info
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dim_us.dim_pub_vpl_hierarchy_info
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi t
JOIN dim_us.dim_pub_date f
  ON t.date_flag = f.date_flag
WHERE f.fyear = 2026
GROUP BY f.fyear, f.month;
```

3) Recent N-month trend without double counting

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dim_us.dim_pub_vpl_hierarchy_info
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_trunc('MM', date_flag) AS month_start, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= add_months(current_date, -6)
GROUP BY date_trunc('MM', date_flag)
ORDER BY month_start;
```

### Metric Selection Guidance

- Use this table for dashboard and period-comparison queries when dimensions match.
- Use DWD base for formula debugging, order_type adjustments, and transaction-level audit.
- Canonical metric formulas and routing: see `metric-index.md`.

## L4 Validation

### Data Quality Checks

- Verify row count stability day-over-day; expect slow growth as new customers/vendors/parts onboard.
- Monitor duplicate-key risk on business keys (`cust_no`, `vend_no`, `sku_no`, `vpl_no`) — each should be unique at stated grain.
- For label columns used in user search (`*_name`, `part_no`, `vpl_code`), spot-check null rate and trim/whitespace anomalies.
- When joining to facts, validate match rate on integer FK columns; unmatched keys often indicate inactive master or cross-company scope mismatch.

### Metric Recompute Spot-Checks

- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.

### Conflicts and Open Questions

- No active conflicts on dimension grain or key semantics as of 2026-06-25.

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

- Consumers: `dws_disty_brpt_pl_extend_1d`, `dm_disty_brpt_pm_mtd`, B Report PM performance dashboards.
- Use cases: PM/Buyer name resolution, management hierarchy expansion, VPL-to-PM assignment context.

### Representative Query Patterns

- No `routing_certified` patterns on this dimension table alone; certified metric SQL lives on serving marts (`dws_disty_brpt_*`, `dm_disty_brpt_*`) with dimension joins documented in `golden-questions.md`.

<!-- sql-artifact
snippet_type: illustrative
intent: scalar_lookup
table_fqn: dim_us.dim_pub_vpl_hierarchy_info
anti_use: lookup only; PM metrics on dm_disty_brpt_pm_mtd
-->
```sql
SELECT vpl_no, vend_no, pm_id, pm_name, pm_manager_name, buyer_id, buyer_name
FROM dim_us.dim_pub_vpl_hierarchy_info
WHERE pm_name ILIKE '%SMITH%'
ORDER BY vpl_no
LIMIT 20;
```

Certified PM metric lookup: `golden-questions.md` → `pm-735781-ngm`.
