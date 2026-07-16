# POS domain — Knowledgebase index

Documentation for **US POS / RDS reporting** tables, converted from the POS v2 table contract catalog (`data_analysis_agent_brpt/knowledge/POS/tables`).

## Coverage summary

| Category | Count | Notes |
|----------|------:|-------|
| POS contract source files | 81 | Full catalog in external repo |
| Documented in `target/knowledgebase/pos/` | 59 | 57 new table contracts + 2 territory-load scripts |
| Already documented in other domains | 24 | Skipped during ingest (see cross-domain list) |
| WKB L1/L3/L6 seeds (Vertica) | 57 | Synthetic DDL from POS column catalog |
| WKB L2/L4/L5 per-table seeds | 57 | From POS contract L2–L5 sections |
| WKB folder seeds (L2/L4/L5) | 3 | `pos_knowledgebase_folder_seed.json` |

## Hub table

- **`dwd_disty_common_pos_di.md`** — US shipped POS order-line fact; primary Vertica query target for POS/RDS reports.

## Tables in this folder

| Document | Qualified name (US baseline) |
|----------|------------------------------|
| `dim_disty_bd_project_cust.md` | `dim_us.dim_disty_bd_project_cust` |
| `dim_disty_bd_project_sku.md` | `dim_us.dim_disty_bd_project_sku` |
| `dim_disty_pm_authority_program_cust.md` | `dim_us.dim_disty_pm_authority_program_cust` |
| `dim_disty_pm_authority_program_sku.md` | `dim_us.dim_disty_pm_authority_program_sku` |
| `dim_pub_bd_hierarchy.md` | `dim_pub.dim_pub_bd_hierarchy` |
| `dim_pub_cust_profile_all.md` | `dim_pub.dim_pub_cust_profile_all` |
| `dim_pub_cust_xref_all.md` | `dim_pub.dim_pub_cust_xref_all` |
| `dim_pub_customer_info_rt.md` | `dim_us.dim_pub_customer_info_rt` |
| `dim_pub_eu_custom_map_view.md` | `dim_pub.dim_pub_eu_custom_map_view` |
| `dim_pub_inv_type_view.md` | `dim_pub.dim_pub_inv_type_view` |
| `dim_pub_part_info_rt.md` | `dim_us.dim_pub_part_info_rt` |
| `dim_pub_project_info.md` | `dim_pub.dim_pub_project_info` |
| `dim_pub_sales_hierarchy_by_terr_user_role.md` | `dim_pub.dim_pub_sales_hierarchy_by_terr_user_role` |
| `dim_pub_sales_hierarchy_primary_role_by_terr_view.md` | `dim_pub.dim_pub_sales_hierarchy_primary_role_by_terr_view` |
| `dim_pub_ship_method.md` | `dim_pub.dim_pub_ship_method` |
| `dim_pub_sku_profile_rt.md` | `dim_us.dim_pub_sku_profile_rt` |
| `dim_pub_sku_xref_all.md` | `dim_pub.dim_pub_sku_xref_all` |
| `dim_pub_terms_file_view.md` | `dim_pub.dim_pub_terms_file_view` |
| `dim_pub_vendor_info_rt.md` | `dim_us.dim_pub_vendor_info_rt` |
| `dim_pub_vendor_xref.md` | `dim_pub.dim_pub_vendor_xref` |
| `dim_pub_vpc_group_view.md` | `dim_pub.dim_pub_vpc_group_view` |
| `dim_pub_vpc_group_xref_view.md` | `dim_pub.dim_pub_vpc_group_xref_view` |
| `dm_disty_pos_order_kit_di.md` | `dw_us.dm_disty_pos_order_kit_di` |
| `dm_disty_pur_purch_forecast461_rtv2.md` | `dw_us.dm_disty_pur_purch_forecast461_rtv2` |
| `dm_disty_sales_close_cpo_di.md` | `dw_us.dm_disty_sales_close_cpo_di` |
| `dm_disty_sales_open_cpo.md` | `dw_us.dm_disty_sales_open_cpo` |
| `dm_disty_sales_rio_sku_inv_loc.md` | `dw_us.dm_disty_sales_rio_sku_inv_loc` |
| `dm_pur_unieta_boso_detail_rt.md` | `dw_us.dm_pur_unieta_boso_detail_rt` |
| `dwd_disty_ap_hold_df.md` | `dw_us.dwd_disty_ap_hold_df` |
| `dwd_disty_ar_cust_doc_df.md` | `dw_us.dwd_disty_ar_cust_doc_df` |
| `dwd_disty_ar_payment_cust_application.md` | `dw_us.dwd_disty_ar_payment_cust_application` |
| `dwd_disty_ar_payment_cust_payment.md` | `dw_us.dwd_disty_ar_payment_cust_payment` |
| `dwd_disty_brpt_bo_detail_df.md` | `dw_us.dwd_disty_brpt_bo_detail_df` |
| `dwd_disty_brpt_orders_pl_etl_mi.md` | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` |
| `dwd_disty_common_cpo_header.md` | `dw_us.dwd_disty_common_cpo_header` |
| `dwd_disty_common_po_basic.md` | `dw_us.dwd_disty_common_po_basic` |
| `dwd_disty_common_pos_di.md` | `dw_us.dwd_disty_common_pos_di` |
| `dwd_disty_inv_aging_df.md` | `dw_us.dwd_disty_inv_aging_df` |
| `dwd_disty_inv_aging_rollover_rtv2_df.md` | `dw_us.dwd_disty_inv_aging_rollover_rtv2_df` |
| `dwd_disty_inv_qty_df.md` | `dw_us.dwd_disty_inv_qty_df` |
| `dwd_disty_inv_rio_req_detail.md` | `dw_us.dwd_disty_inv_rio_req_detail` |
| `dwd_disty_inv_rio_request_header.md` | `dw_us.dwd_disty_inv_rio_request_header` |
| `dwd_disty_pm_cost_factor_vpl.md` | `dw_us.dwd_disty_pm_cost_factor_vpl` |
| `dwd_disty_pm_report_goal.md` | `dw_us.dwd_disty_pm_report_goal` |
| `dwd_disty_sales_eu_custom_di.md` | `dw_us.dwd_disty_sales_eu_custom_di` |
| `dwd_disty_sales_open_cpo_detail_extend.md` | `dw_us.dwd_disty_sales_open_cpo_detail_extend` |
| `dwd_disty_sales_open_cpo_header_extend.md` | `dw_us.dwd_disty_sales_open_cpo_header_extend` |
| `dwd_disty_sales_open_order_detail.md` | `dw_us.dwd_disty_sales_open_order_detail` |
| `dwd_disty_sales_order_soldto_di.md` | `dw_us.dwd_disty_sales_order_soldto_di` |
| `dwd_disty_scm_pm_claim.md` | `dw_us.dwd_disty_scm_pm_claim` |
| `dwd_disty_tm_order_frt_detail_di.md` | `dw_us.dwd_disty_tm_order_frt_detail_di` |
| `dwd_pub_common_history_detail_date.md` | `dw_us.dwd_pub_common_history_detail_date` |
| `dwd_pub_common_history_header_extend.md` | `dw_us.dwd_pub_common_history_header_extend` |
| `dwd_pub_common_order_header_extend.md` | `dw_us.dwd_pub_common_order_header_extend` |
| `dwd_stellr_billing_history_di.md` | `dw_us.dwd_stellr_billing_history_di` |
| `dws_disty_brpt_cust_mtd.md` | `dw_us.dws_disty_brpt_cust_mtd` |
| `dws_disty_pur_ips_runrate_1w.md` | `dw_us.dws_disty_pur_ips_runrate_1w` |
| `load_comp_orders_apply_terr_change.md` | ETL script (territory change) |
| `load_single_orders_apply_terr_change.md` | ETL script (territory change) |

## Cross-domain duplicates (not copied to `pos/`)

These **24** POS catalog tables already had Knowledgebase docs under other domains:

| Table stem | Existing doc |
|------------|--------------|
| `dim_dw_calendar` | `target/knowledgebase/common/dim_pub_date/dim_dw_calendar.md` |
| `dim_pub_customer_address_contacts_info` | `target/knowledgebase/customer/dim_pub_customer_address_contacts_info.md` |
| `dim_pub_customer_credit_info` | `target/knowledgebase/customer/dim_pub_customer_credit_info.md` |
| `dim_pub_customer_info` | `target/knowledgebase/customer/dim_pub_customer_info.md` |
| `dim_pub_date` | `target/knowledgebase/common/dim_pub_date/dim_pub_date.md` |
| `dim_pub_exchange_rate` | `target/knowledgebase/common/public_common_dimension/dim_pub_exchange_rate.md` |
| `dim_pub_list_box_detail` | `target/knowledgebase/common/public_common_dimension/dim_pub_list_box_detail.md` |
| `dim_pub_location_info` | `target/knowledgebase/inventory/public_inventory_dimension/dim_pub_location_info.md` |
| `dim_pub_manager` | `target/knowledgebase/common/public_common_dimension/dim_pub_manager.md` |
| `dim_pub_order_type` | `target/knowledgebase/order/dim_pub_order_type.md` |
| `dim_pub_part_info` | `target/knowledgebase/part_sku/dim_pub_part_info.md` |
| `dim_pub_pm_vpc_matrix` | `target/knowledgebase/vendor/dim_pub_pm_vpc_matrix.md` |
| `dim_pub_sales_cust_type` | `target/knowledgebase/customer/dim_pub_sales_cust_type.md` |
| `dim_pub_sku_profile_all` | `target/knowledgebase/part_sku/dim_pub_sku_profile_all.md` |
| `dim_pub_sku_profile_extend` | `target/knowledgebase/part_sku/dim_pub_sku_profile_extend.md` |
| `dim_pub_vendor_info` | `target/knowledgebase/vendor/dim_pub_vendor_info.md` |
| `dim_pub_vpl_hierarchy_info` | `target/knowledgebase/vendor/dim_pub_vpl_hierarchy_info.md` |
| `dim_pub_vpl_info` | `target/knowledgebase/vendor/dim_pub_vpl_info.md` |
| `dim_pub_vpl_pm_hierarchy_info` | `target/knowledgebase/vendor/dim_pub_vpl_pm_hierarchy_info.md` |
| `dwd_disty_common_dw_orders_pl_extend_di` | `target/knowledgebase/order/dwd_disty_common_dw_orders_pl_extend_di.md` |
| `dwd_disty_common_order_serial_no_di` | `target/knowledgebase/order/dwd_disty_common_order_serial_no_di.md` |
| `dwd_disty_scm_open_order_spa_df` | `target/knowledgebase/order/dwd_disty_scm_open_order_spa_df.md` |
| `dwd_disty_scm_shipped_order_spa_di` | `target/knowledgebase/order/dwd_disty_scm_shipped_order_spa_di.md` |
| `dwd_pub_common_shipped_order_scm_spa_detail_di` | `target/knowledgebase/order/dwd_pub_common_shipped_order_scm_spa_detail_di.md` |

## Provenance and limits

- **Source:** POS v2 contracts (`artifact_id`, L1–L6 column catalog and lineage sections).
- **ETL lineage:** Step-by-step temp-table logic is **not in this wiki repo** for most POS tables; docs note contract-derived grain, keys, and Vertica mapping.
- **DDL seeds:** Synthetic `CREATE TABLE` from contract column types; `ddl_source.repo` = `POS-CONTRACT/data_analysis_agent_brpt`.
- **Bitbucket DDL:** Not fetched in this batch; Bitbucket ingest can replace synthetic seeds when Hive/Vertica DDL is available.

## Regenerate

```bash
python tools/ingest/pos_contract_to_knowledgebase.py --write-seeds
python tools/ingest/pos_contract_to_knowledgebase.py --write-seeds --seeds-only   # refresh WKB layers only
python -m tools.wkb.indexing.index_builder
python -m tools.wkb.indexing.run_query --query "pos dwd_disty_common_pos_di schema" --intent find_table_schema
```

WKB layer mapping: see `.cursor/skills/etl-knowledgebase-docs/pos-contract-reference.md`.
