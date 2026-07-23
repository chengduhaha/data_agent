# POS domain — Knowledgebase index

Documentation for **US POS / RDS reporting** tables.

Primary sources:
- POS v2 table contracts (preserved under each file’s **Preserved pre-L1-L6 content**)
- Load ETL under `source/contracts/pos/bitbucket-etl/` (L1–L6 lineage, joins, filters, column derivations)
- Cross-project references under `source/contracts/**` and `target/knowledgebase/**` (L6 downstream)

## Coverage summary

| Category | Count | Notes |
|----------|------:|-------|
| Knowledgebase markdown files | 87 | includes `readme.md` + `error_formula.md` |
| Table / ETL docs (below) | 85 | |
| L1–L6 layered docs | 85 | |
| Evidence from bitbucket-etl | 81 | primary SQL/Python in bundle |
| Contract-only (ETL missing in repo) | 0 | see MANIFEST `etl_scripts_missing` |
| bitbucket-etl bundles | 66 | `source/contracts/pos/bitbucket-etl/MANIFEST.md` |

## Hub table

- **`dwd_disty_common_pos_di.md`** — US shipped POS order-line fact; primary Vertica query target for POS/RDS reports.
- **Primary ETL:** `source/contracts/pos/bitbucket-etl/dwd_disty_common_pos_di/loading_pos_data.sql`

## How docs were refreshed

1. `python -m tools.ingest.batch_pos_bitbucket_etl_kb_upgrade` — upgrade/create from each ETL bundle + cross-project L6 consumers
2. `python -m tools.ingest.enrich_pos_contract_only_lineage` — L1–L6 wrapper for stems without a bitbucket-etl bundle

## Tables in this folder

| Document | artifact_id | Layers | Evidence |
|----------|-------------|--------|----------|
| `dim_disty_bd_project_cust.md` | `dim_us.dim_disty_bd_project_cust` | L1–L6 | bitbucket-etl |
| `dim_disty_bd_project_sku.md` | `dim_us.dim_disty_bd_project_sku` | L1–L6 | bitbucket-etl |
| `dim_disty_pm_authority_program_cust.md` | `dim_us.dim_disty_pm_authority_program_cust` | L1–L6 | bitbucket-etl |
| `dim_disty_pm_authority_program_sku.md` | `dim_us.dim_disty_pm_authority_program_sku` | L1–L6 | bitbucket-etl |
| `dim_dw_calendar.md` | `dim_${country_code}.dim_dw_calendar` | L1–L6 | bitbucket-etl |
| `dim_pub_bd_hierarchy.md` | `dim_us.dim_pub_bd_hierarchy` | L1–L6 | bitbucket-etl |
| `dim_pub_cust_profile_all.md` | `dim_us.dim_pub_cust_profile_all` | L1–L6 | bitbucket-etl |
| `dim_pub_cust_xref_all.md` | `dim_us.dim_pub_cust_xref_all` | L1–L6 | bitbucket-etl |
| `dim_pub_customer_address_contacts_info.md` | `dim_${country_code}.dim_pub_customer_address_contacts_info` | L1–L6 | bitbucket-etl |
| `dim_pub_customer_credit_info.md` | `dim_${country_code}.dim_pub_customer_credit_info` | L1–L6 | bitbucket-etl |
| `dim_pub_customer_info.md` | `dim_${country_code}.dim_pub_customer_info` | L1–L6 | bitbucket-etl |
| `dim_pub_customer_info_rt.md` | `dim_us.dim_pub_customer_info_rt` | L1–L6 | bitbucket-etl |
| `dim_pub_date.md` | `dim_${country_code}.dim_pub_date` | L1–L6 | bitbucket-etl |
| `dim_pub_eu_custom_map_view.md` | `dim_us.dim_pub_eu_custom_map_view` | L1–L6 | bitbucket-etl |
| `dim_pub_exchange_rate.md` | `dim_${country_code}.dim_pub_exchange_rate` | L1–L6 | bitbucket-etl |
| `dim_pub_inv_type_view.md` | `dim_us.dim_pub_inv_type_view` | L1–L6 | bitbucket-etl |
| `dim_pub_list_box_detail.md` | `dim_${country_code}.dim_pub_list_box_detail` | L1–L6 | bitbucket-etl |
| `dim_pub_location_info.md` | `dim_${country_code}.dim_pub_location_info` | L1–L6 | bitbucket-etl |
| `dim_pub_manager.md` | `dim_${country_code}.dim_pub_manager` | L1–L6 | bitbucket-etl |
| `dim_pub_order_type.md` | `dim_${country_code}.dim_pub_order_type` | L1–L6 | bitbucket-etl |
| `dim_pub_part_info.md` | `dim_${country_code}.dim_pub_part_info` | L1–L6 | bitbucket-etl |
| `dim_pub_part_info_rt.md` | `dim_us.dim_pub_part_info_rt` | L1–L6 | bitbucket-etl |
| `dim_pub_pm_vpc_matrix.md` | `dim_${country_code}.dim_pub_pm_vpc_matrix` | L1–L6 | bitbucket-etl |
| `dim_pub_project_info.md` | `dim_us.dim_pub_project_info` | L1–L6 | bitbucket-etl |
| `dim_pub_sales_cust_type.md` | `dim_${country_code}.dim_pub_sales_cust_type` | L1–L6 | bitbucket-etl |
| `dim_pub_sales_hierarchy_by_terr_user_role.md` | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role` | L1–L6 | bitbucket-etl |
| `dim_pub_sales_hierarchy_primary_role_by_terr_view.md` | `dim_us.dim_pub_sales_hierarchy_primary_role_by_terr_view` | L1–L6 | bitbucket-etl |
| `dim_pub_ship_method.md` | `dim_us.dim_pub_ship_method` | L1–L6 | bitbucket-etl |
| `dim_pub_sku_profile_all.md` | `dim_${country_code}.dim_pub_sku_profile_all` | L1–L6 | bitbucket-etl |
| `dim_pub_sku_profile_extend.md` | `dim_${country_code}.dim_pub_sku_profile_extend` | L1–L6 | bitbucket-etl |
| `dim_pub_sku_profile_rt.md` | `dim_us.dim_pub_sku_profile_rt` | L1–L6 | bitbucket-etl |
| `dim_pub_sku_xref_all.md` | `dim_us.dim_pub_sku_xref_all` | L1–L6 | bitbucket-etl |
| `dim_pub_terms_file_view.md` | `dim_us.dim_pub_terms_file_view` | L1–L6 | bitbucket-etl |
| `dim_pub_vendor_info.md` | `dim_${country_code}.dim_pub_vendor_info` | L1–L6 | bitbucket-etl |
| `dim_pub_vendor_info_rt.md` | `dim_us.dim_pub_vendor_info_rt` | L1–L6 | bitbucket-etl |
| `dim_pub_vendor_xref.md` | `dim_us.dim_pub_vendor_xref` | L1–L6 | bitbucket-etl |
| `dim_pub_vpc_group_view.md` | `dim_us.dim_pub_vpc_group_view` | L1–L6 | bitbucket-etl |
| `dim_pub_vpc_group_xref_view.md` | `dim_us.dim_pub_vpc_group_xref_view` | L1–L6 | bitbucket-etl |
| `dim_pub_vpl_hierarchy_info.md` | `dim_${country_code}.dim_pub_vpl_hierarchy_info` | L1–L6 | bitbucket-etl |
| `dim_pub_vpl_info.md` | `dim_${country_code}.dim_pub_vpl_info` | L1–L6 | bitbucket-etl |
| `dim_pub_vpl_pm_hierarchy_info.md` | `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info` | L1–L6 | bitbucket-etl |
| `dm_disty_pos_order_kit_di.md` | `dm_us.dm_disty_pos_order_kit_di` | L1–L6 | bitbucket-etl |
| `dm_disty_pur_purch_forecast461_rtv2.md` | `dm_us.dm_disty_pur_purch_forecast461_rtv2` | L1–L6 | bitbucket-etl |
| `dm_disty_sales_close_cpo_di.md` | `dm_us.dm_disty_sales_close_cpo_di` | L1–L6 | bitbucket-etl |
| `dm_disty_sales_open_cpo.md` | `dm_us.dm_disty_sales_open_cpo` | L1–L6 | bitbucket-etl |
| `dm_disty_sales_rio_sku_inv_loc.md` | `dm_us.dm_disty_sales_rio_sku_inv_loc` | L1–L6 | bitbucket-etl |
| `dm_pur_unieta_boso_detail_rt.md` | `dm_us.dm_pur_unieta_boso_detail_rt` | L1–L6 | bitbucket-etl |
| `dwd_disty_ap_hold_df.md` | `dw_us.dwd_disty_ap_hold_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_ar_cust_doc_df.md` | `dw_us.dwd_disty_ar_cust_doc_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_ar_payment_cust_application.md` | `dw_us.dwd_disty_ar_payment_cust_application` | L1–L6 | bitbucket-etl |
| `dwd_disty_ar_payment_cust_payment.md` | `dw_us.dwd_disty_ar_payment_cust_payment` | L1–L6 | bitbucket-etl |
| `dwd_disty_brpt_bo_detail_df.md` | `dw_us.dwd_disty_brpt_bo_detail_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_brpt_orders_pl_etl_mi.md` | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | L1–L6 | bitbucket-etl |
| `dwd_disty_common_cpo_header.md` | `dw_us.dwd_disty_common_cpo_header` | L1–L6 | bitbucket-etl |
| `dwd_disty_common_dw_orders_pl_extend_di.md` | `dw_${country_code}.dwd_disty_common_dw_orders_pl_extend_di` | L1–L6 | bitbucket-etl |
| `dwd_disty_common_order_serial_no_di.md` | `dw_${country_code}.dwd_disty_common_order_serial_no_di` | L1–L6 | bitbucket-etl |
| `dwd_disty_common_po_basic.md` | `dw_us.dwd_disty_common_po_basic` | L1–L6 | bitbucket-etl |
| `dwd_disty_common_pos_di.md` | `dw_us.dwd_disty_common_pos_di` | L1–L6 | bitbucket-etl |
| `dwd_disty_inv_aging_df.md` | `dw_us.dwd_disty_inv_aging_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_inv_aging_rollover_rtv2_df.md` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_inv_qty_df.md` | `dw_us.dwd_disty_inv_qty_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_inv_rio_req_detail.md` | `dw_us.dwd_disty_inv_rio_req_detail` | L1–L6 | bitbucket-etl |
| `dwd_disty_inv_rio_request_header.md` | `(unresolved).dwd_disty_inv_rio_request_header` | L1–L6 | bitbucket-etl |
| `dwd_disty_pm_cost_factor_vpl.md` | `dw_us.dwd_disty_pm_cost_factor_vpl` | L1–L6 | bitbucket-etl |
| `dwd_disty_pm_report_goal.md` | `dw_us.dwd_disty_pm_report_goal` | L1–L6 | bitbucket-etl |
| `dwd_disty_sales_eu_custom_di.md` | `dw_us.dwd_disty_sales_eu_custom_di` | L1–L6 | bitbucket-etl |
| `dwd_disty_sales_open_cpo_detail_extend.md` | `dw_us.dwd_disty_sales_open_cpo_detail_extend` | L1–L6 | bitbucket-etl |
| `dwd_disty_sales_open_cpo_header_extend.md` | `dw_us.dwd_disty_sales_open_cpo_header_extend` | L1–L6 | bitbucket-etl |
| `dwd_disty_sales_open_order_detail.md` | `dw_us.dwd_disty_sales_open_order_detail` | L1–L6 | bitbucket-etl |
| `dwd_disty_sales_order_soldto_di.md` | `dw_us.dwd_disty_sales_order_soldto_di` | L1–L6 | bitbucket-etl |
| `dwd_disty_scm_open_order_spa_df.md` | `dw_${country_code}.dwd_disty_scm_open_order_spa_df` | L1–L6 | bitbucket-etl |
| `dwd_disty_scm_pm_claim.md` | `dw_us.dwd_disty_scm_pm_claim` | L1–L6 | bitbucket-etl |
| `dwd_disty_scm_shipped_order_spa_di.md` | `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di` | L1–L6 | bitbucket-etl |
| `dwd_disty_tm_order_frt_detail_di.md` | `dw_us.dwd_disty_tm_order_frt_detail_di` | L1–L6 | bitbucket-etl |
| `dwd_pub_common_history_detail_date.md` | `dw_us.dwd_pub_common_history_detail_date` | L1–L6 | bitbucket-etl |
| `dwd_pub_common_history_header_extend.md` | `dw_us.dwd_pub_common_history_header_extend` | L1–L6 | bitbucket-etl |
| `dwd_pub_common_order_header_extend.md` | `dw_us.dwd_pub_common_order_header_extend` | L1–L6 | bitbucket-etl |
| `dwd_pub_common_shipped_order_scm_spa_detail_di.md` | `dw_${country_code}.dwd_pub_common_shipped_order_scm_spa_detail_di` | L1–L6 | bitbucket-etl |
| `dwd_stellr_billing_history_di.md` | `dw_us.dwd_stellr_billing_history_di` | L1–L6 | bitbucket-etl |
| `dws_disty_brpt_cust_mtd.md` | `dw_us.dws_disty_brpt_cust_mtd` | L1–L6 | bitbucket-etl |
| `dws_disty_pur_ips_runrate_1w.md` | `dw_us.dws_disty_pur_ips_runrate_1w` | L1–L6 | bitbucket-etl |
| `load_comp_orders_apply_terr_change.md` | `dwd_disty_sales_comp_orders_di` | L1–L6 | other/prior |
| `load_comp_orders_di.md` | `${target_db}.dwd_disty_sales_comp_for_calc_di` | L1–L6 | other/prior |
| `load_single_orders_apply_terr_change.md` | `dwd_disty_sales_single_orders_di` | L1–L6 | other/prior |
| `load_single_orders_di.md` | `${target_db}.dwd_disty_sales_orders_di` | L1–L6 | other/prior |

## Cross-domain / missing ETL notes

- Stems listed in `source/contracts/pos/bitbucket-etl/MANIFEST.md` under **etl_scripts_missing** still have contract narrative only (no load SQL in this wiki repo).
- Territory load scripts (`load_*_orders*`) may also appear under other domain knowledgebases; prefer the POS copies when answering POS questions.
- Schedule / owner / SLA remain **Not documented in repository** unless a FLOW file cites them.

## Related tooling

- Batch upgrade: `tools/ingest/batch_pos_bitbucket_etl_kb_upgrade.py`
- Contract-only enrich: `tools/ingest/enrich_pos_contract_only_lineage.py`
- Column derivations: `python -m tools.ingest.sql_column_derivation`
