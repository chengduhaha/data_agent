# b-report-us Bitbucket ETL snapshot (disty_brpt_dw)

Exported: 2026-07-16
Updated: 2026-07-16 (removed BD_manual_load, init, z_reload_data folders; restored z_reload_data for dwd_disty_brpt_orders_pl_di and dwd_disty_brpt_orders_pl_etl_mi)

Source list: source/ref/us_lineage_write_tables_with_bitbucket_b-report-us.md
Local source repo: C:/Users/T154858D.TDSNX/Desktop/git_repo_v1/disty_brpt_dw
Destination: source/contracts/b-report-us/bitbicket_etl/{table_name}/{repo_relative_path}

## Excluded folder types

- BD_manual_load/
- init/
- z_reload_data/ (except `dwd_disty_brpt_orders_pl_di` and `dwd_disty_brpt_orders_pl_etl_mi`, which retain their `z_reload_data/` scripts)

## Restored z_reload_data exceptions

| Table | Relative path |
|---|---|
| dwd_disty_brpt_orders_pl_di | z_reload_data/dwd_disty_brpt_orders_pl_di.py |
| dwd_disty_brpt_orders_pl_etl_mi | z_reload_data/dwd_disty_brpt_orders_pl_etl_mi.py |

## Summary

- Table folders with ETL files: 88
- ETL files retained: 88
- Folders removed in cleanup: 59 (BD_manual_load / init / z_reload_data, except the two DWD tables above)

## pub_dw tables (not in disty_brpt_dw repo)

These tables are in the b-report-us lineage list but their Bitbucket paths point to the pub_dw project.

| Table |
|---|
dim_pub_customer_info |
dim_pub_date |
dim_pub_order_type |
dim_pub_part_info |
dim_pub_sales_cust_type |
dim_pub_vendor_info |
dim_pub_vendor_segment |
dim_pub_vpl_hierarchy_info |
dim_pub_vpl_info |

## Copied ETL files by table

| Table | Copied file count | Relative paths |
|---|---:|---|
| dm_disty_brpt_bd_rep_1d | 1 | BD\sql\dm_disty_brpt_bd_rep_1d.py |
| dm_disty_brpt_bd_rep_comb_mtd | 1 | BD\python\dm_disty_brpt_bd_rep_comb_mtd.py |
| dm_disty_brpt_bd_rep_mtd | 1 | BD\python\dm_disty_brpt_bd_rep_mtd.py |
| dm_disty_brpt_bd_rep_wtd | 1 | BD\python\dm_disty_brpt_bd_rep_wtd.py |
| dm_disty_brpt_buyer_1d | 1 | Product\sql\dm_disty_brpt_buyer_1d.py |
| dm_disty_brpt_buyer_comb_mtd | 1 | Product\python\dm_disty_brpt_buyer_comb_mtd.py |
| dm_disty_brpt_buyer_mtd | 1 | Product\python\dm_disty_brpt_buyer_mtd.py |
| dm_disty_brpt_buyer_wtd | 1 | Product\python\dm_disty_brpt_buyer_wtd.py |
| dm_disty_brpt_pm_1d | 1 | Product\sql\dm_disty_brpt_pm_1d.py |
| dm_disty_brpt_pm_comb_mtd | 1 | Product\python\dm_disty_brpt_pm_comb_mtd.py |
| dm_disty_brpt_pm_mtd | 1 | Product\python\dm_disty_brpt_pm_mtd.py |
| dm_disty_brpt_pm_wtd | 1 | Product\python\dm_disty_brpt_pm_wtd.py |
| dm_disty_brpt_sales_1d | 1 | Customer\sql\dm_disty_brpt_sales_1d.py |
| dm_disty_brpt_sales_comb_mtd | 1 | Customer\python\dm_disty_brpt_sales_comb_mtd.py |
| dm_disty_brpt_sales_mtd | 1 | Customer\python\dm_disty_brpt_sales_mtd.py |
| dm_disty_brpt_sales_wtd | 1 | Customer\python\dm_disty_brpt_sales_wtd.py |
| dwd_disty_brpt_orders_pl_di | 1 | z_reload_data\dwd_disty_brpt_orders_pl_di.py |
| dwd_disty_brpt_orders_pl_etl_mi | 1 | z_reload_data\dwd_disty_brpt_orders_pl_etl_mi.py |
| dws_disty_brpt_bd_1d | 1 | Common\bd\dws_disty_brpt_bd_1d_v2.py |
| dws_disty_brpt_bd_cust_1d | 1 | BD\sql\dws_disty_brpt_bd_cust_1d.py |
| dws_disty_brpt_bd_cust_comb_mtd | 1 | BD\python\dws_disty_brpt_bd_cust_comb_mtd.py |
| dws_disty_brpt_bd_cust_mtd | 1 | BD\python\dws_disty_brpt_bd_cust_mtd.py |
| dws_disty_brpt_bd_cust_wtd | 1 | BD\python\dws_disty_brpt_bd_cust_wtd.py |
| dws_disty_brpt_bd_mtd | 1 | Common\bd\dws_disty_brpt_bd_mtd_v2.py |
| dws_disty_brpt_bd_part_1d | 1 | BD\sql\dws_disty_brpt_bd_part_1d.py |
| dws_disty_brpt_bd_part_comb_mtd | 1 | BD\python\dws_disty_brpt_bd_part_comb_mtd.py |
| dws_disty_brpt_bd_part_mtd | 1 | BD\python\dws_disty_brpt_bd_part_mtd.py |
| dws_disty_brpt_bd_part_wtd | 1 | BD\python\dws_disty_brpt_bd_part_wtd.py |
| dws_disty_brpt_bd_proj_task_1d | 1 | BD\sql\dws_disty_brpt_bd_proj_task_1d.py |
| dws_disty_brpt_bd_proj_task_comb_mtd | 1 | BD\python\dws_disty_brpt_bd_proj_task_comb_mtd.py |
| dws_disty_brpt_bd_proj_task_mtd | 1 | BD\python\dws_disty_brpt_bd_proj_task_mtd.py |
| dws_disty_brpt_bd_proj_task_wtd | 1 | BD\python\dws_disty_brpt_bd_proj_task_wtd.py |
| dws_disty_brpt_bd_vend_1d | 1 | BD\sql\dws_disty_brpt_bd_vend_1d.py |
| dws_disty_brpt_bd_vend_comb_mtd | 1 | BD\python\dws_disty_brpt_bd_vend_comb_mtd.py |
| dws_disty_brpt_bd_vend_mtd | 1 | BD\python\dws_disty_brpt_bd_vend_mtd.py |
| dws_disty_brpt_bd_vend_wtd | 1 | BD\python\dws_disty_brpt_bd_vend_wtd.py |
| dws_disty_brpt_bd_vpl_1d | 1 | BD\sql\dws_disty_brpt_bd_vpl_1d.py |
| dws_disty_brpt_bd_vpl_comb_mtd | 1 | BD\python\dws_disty_brpt_bd_vpl_comb_mtd.py |
| dws_disty_brpt_bd_vpl_mtd | 1 | BD\python\dws_disty_brpt_bd_vpl_mtd.py |
| dws_disty_brpt_bd_vpl_wtd | 1 | BD\python\dws_disty_brpt_bd_vpl_wtd.py |
| dws_disty_brpt_cross_cvv_1d | 1 | Cross\sql\dws_disty_brpt_cross_cvv_1d.py |
| dws_disty_brpt_cross_cvv_comb_mtd | 1 | Cross\python\dws_disty_brpt_cross_cvv_comb_mtd.py |
| dws_disty_brpt_cross_cvv_mtd | 1 | Cross\python\dws_disty_brpt_cross_cvv_mtd.py |
| dws_disty_brpt_cross_cvv_wtd | 1 | Cross\python\dws_disty_brpt_cross_cvv_wtd.py |
| dws_disty_brpt_cross_dccv_1d | 1 | Cross\sql\dws_disty_brpt_cross_dccv_1d.py |
| dws_disty_brpt_cross_dccv_comb_mtd | 1 | Cross\python\dws_disty_brpt_cross_dccv_comb_mtd.py |
| dws_disty_brpt_cross_dccv_mtd | 1 | Cross\python\dws_disty_brpt_cross_dccv_mtd.py |
| dws_disty_brpt_cross_dccv_wtd | 1 | Cross\python\dws_disty_brpt_cross_dccv_wtd.py |
| dws_disty_brpt_cross_mpc_1d | 1 | Cross\sql\dws_disty_brpt_cross_mpc_1d.py |
| dws_disty_brpt_cross_mpc_comb_mtd | 1 | Cross\python\dws_disty_brpt_cross_mpc_comb_mtd.py |
| dws_disty_brpt_cross_mpc_mtd | 1 | Cross\python\dws_disty_brpt_cross_mpc_mtd.py |
| dws_disty_brpt_cross_mpc_wtd | 1 | Cross\python\dws_disty_brpt_cross_mpc_wtd.py |
| dws_disty_brpt_cross_svddc_1d | 1 | Cross\sql\dws_disty_brpt_cross_svddc_1d.py |
| dws_disty_brpt_cross_svddc_comb_mtd | 1 | Cross\python\dws_disty_brpt_cross_svddc_comb_mtd.py |
| dws_disty_brpt_cross_svddc_mtd | 1 | Cross\python\dws_disty_brpt_cross_svddc_mtd.py |
| dws_disty_brpt_cross_svddc_wtd | 1 | Cross\python\dws_disty_brpt_cross_svddc_wtd.py |
| dws_disty_brpt_cust_1d | 1 | Customer\sql\dws_disty_brpt_cust_1d.py |
| dws_disty_brpt_cust_comb_mtd | 1 | Customer\python\dws_disty_brpt_cust_comb_mtd.py |
| dws_disty_brpt_cust_mtd | 1 | Customer\python\dws_disty_brpt_cust_mtd.py |
| dws_disty_brpt_cust_type_1d | 1 | Customer\sql\dws_disty_brpt_cust_type_1d.py |
| dws_disty_brpt_cust_type_comb_mtd | 1 | Customer\python\dws_disty_brpt_cust_type_comb_mtd.py |
| dws_disty_brpt_cust_type_mtd | 1 | Customer\python\dws_disty_brpt_cust_type_mtd.py |
| dws_disty_brpt_cust_type_wtd | 1 | Customer\python\dws_disty_brpt_cust_type_wtd.py |
| dws_disty_brpt_cust_wtd | 1 | Customer\python\dws_disty_brpt_cust_wtd.py |
| dws_disty_brpt_division_1d | 1 | Customer\sql\dws_disty_brpt_division_1d.py |
| dws_disty_brpt_division_comb_mtd | 1 | Customer\python\dws_disty_brpt_division_comb_mtd.py |
| dws_disty_brpt_division_mtd | 1 | Customer\python\dws_disty_brpt_division_mtd.py |
| dws_disty_brpt_division_wtd | 1 | Customer\python\dws_disty_brpt_division_wtd.py |
| dws_disty_brpt_part_1d | 1 | Product\sql\dws_disty_brpt_part_1d.py |
| dws_disty_brpt_part_comb_mtd | 1 | Product\python\dws_disty_brpt_part_comb_mtd.py |
| dws_disty_brpt_part_mtd | 1 | Product\python\dws_disty_brpt_part_mtd.py |
| dws_disty_brpt_part_wtd | 1 | Product\python\dws_disty_brpt_part_wtd.py |
| dws_disty_brpt_pl_extend_1d | 1 | Common\python\dws_disty_brpt_pl_extend_1d.py |
| dws_disty_brpt_pl_extend_comb_mtd | 1 | Common\python\dws_disty_brpt_pl_extend_comb_mtd.py |
| dws_disty_brpt_pl_extend_mtd | 1 | Common\python\dws_disty_brpt_pl_extend_mtd.py |
| dws_disty_brpt_pl_extend_wtd | 1 | Common\python\dws_disty_brpt_pl_extend_wtd.py |
| dws_disty_brpt_terr_1d | 1 | Customer\sql\dws_disty_brpt_terr_1d.py |
| dws_disty_brpt_terr_comb_mtd | 1 | Customer\python\dws_disty_brpt_terr_comb_mtd.py |
| dws_disty_brpt_terr_mtd | 1 | Customer\python\dws_disty_brpt_terr_mtd.py |
| dws_disty_brpt_terr_wtd | 1 | Customer\python\dws_disty_brpt_terr_wtd.py |
| dws_disty_brpt_vend_1d | 1 | Product\sql\dws_disty_brpt_vend_1d.py |
| dws_disty_brpt_vend_comb_mtd | 1 | Product\python\dws_disty_brpt_vend_comb_mtd.py |
| dws_disty_brpt_vend_mtd | 1 | Product\python\dws_disty_brpt_vend_mtd.py |
| dws_disty_brpt_vend_wtd | 1 | Product\python\dws_disty_brpt_vend_wtd.py |
| dws_disty_brpt_vpl_1d | 1 | Product\sql\dws_disty_brpt_vpl_1d.py |
| dws_disty_brpt_vpl_comb_mtd | 1 | Product\python\dws_disty_brpt_vpl_comb_mtd.py |
| dws_disty_brpt_vpl_mtd | 1 | Product\python\dws_disty_brpt_vpl_mtd.py |
| dws_disty_brpt_vpl_wtd | 1 | Product\python\dws_disty_brpt_vpl_wtd.py |
