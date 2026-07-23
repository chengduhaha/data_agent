# DM: B Report combined-month profitability serving slice (sales_comb_mtd) (`dm_us.dm_disty_brpt_sales_comb_mtd`)

- artifact_type: etl_table
- artifact_id: dm_us.dm_disty_brpt_sales_comb_mtd
- domain: b-report-us
- one_line_purpose: B Report combined-month profitability serving slice (sales_comb_mtd)
- layer_type: DM
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py
- knowledgebase_path: target/knowledgebase/b-report-us/dm_disty_brpt_sales_comb_mtd.md
- contract_source: source/contracts/b-report-us/tables/dm_disty_brpt_sales_comb_mtd.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dm_us.dm_disty_brpt_sales_comb_mtd`
- **Layer type:** DM
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** month-to-date cumulative through each date_flag
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `month_no` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `sales_rep_id`, `sales_sup_id`, `sales_mgr_id`, `sales_dir_id`, `sales_vp_id`, `company_no`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dm_${country}.dm_disty_brpt_sales_comb_mtd` | ETL target in Bitbucket script |
| Vertica | yes | `dm_us.dm_disty_brpt_sales_comb_mtd` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dm_us.dm_disty_brpt_sales_comb_mtd` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dm_us_dm_disty_brpt_sales_comb_mtd.json` |
| **column_count** | 219 |
| **partition_keys** | `month_no` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dm_disty_brpt_sales_comb_mtd schema" --intent find_table_schema` |

### Lineage
- **upstream:** dim_us.dim_pub_sales_mgr_dept_df, dim_us.dim_pub_sales_rep_terr_df, dim_us.dim_pub_sales_territory_df, ods_us.ods_cis_corp_cust_type, ods_us.ods_cis_corp_division, ods_us.ods_cis_corp_manager — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dm_disty_brpt_sales_comb_mtd.md`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | INSERT OVERWRITE partition reload (per ETL SQL) |
| Schedule | Not documented in repository |
| Parameters | `country`, `date_flag`, `dt_month`, `month_no`, `etl_timestamp`, `end_day_of_last_month`, `end_day_of_last_2month`, `end_day_of_same_month_of_last_year`, `week_begin_of_dateflag` |

---

## L2 Declarative Knowledge

### Business purpose
B Report combined-month profitability serving slice (sales_comb_mtd)

This Knowledgebase entry documents the Bitbucket ETL load script in `source/contracts/b-report-us/bitbicket_etl/`. Business semantics align with the B Report US contract catalog when present.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: PM, Sales, Buyer, BD and executive analysis views. |
| **Sales / PM / finance** | Shipped-order and margin metrics at documented grain (combined month-to-date wide serving (multiple period columns)). |
| **Data engineering** | Verified upstream/downstream objects with `file:line` evidence from ETL SQL. |

### Fact key resolution
- Order-line hub for B Report P&L: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` when debugging transaction-level metrics.
- This table grain: month-to-date cumulative through each date_flag.
- Label-on/off and order_type adjustments: see `source/contracts/b-report-us/metric-index.md`.

### Time field semantics
- **`month_no`:** primary partition / filter for this load; value supplied by Azkaban `conf.get` parameters (see L4).
- **Period semantics:** combined month-to-date wide serving (multiple period columns).


### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `d_cgp` | `cgp` | cgp at daily grain |
| P&L adjustment / measure | `d_cost` | `cost` | cost at daily grain |
| P&L adjustment / measure | `d_fx_cost` | `fx_cost` | fx_cost at daily grain |
| Governed profitability | `d_gm` | `gm_amt` | gm_amt at daily grain |
| Governed profitability | `d_ngm` | `ngm_amt` | ngm_amt at daily grain |
| Governed profitability | `d_opl` | `oplgm_amt` | oplgm_amt at daily grain |
| Governed profitability | `d_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at daily grain |
| Governed profitability | `d_sales` | `net_sales` | net_sales at daily grain |
| P&L adjustment / measure | `d_scm_usage` | `scm_usage` | scm_usage at daily grain |
| Governed profitability | `d_tgm` | `tgm_amt` | tgm_amt at daily grain |
| Governed profitability | `d_total_btl` | `total_btl` | total_btl at daily grain |
| P&L adjustment / measure | `d_unit` | `unit` | unit at daily grain |
| P&L adjustment / measure | `goal_cust_cnt` | `goal_cust_cnt` | goal_cust_cnt at goal_target grain |
| P&L adjustment / measure | `goal_dos` | `goal_dos` | goal_dos at goal_target grain |
| P&L adjustment / measure | `goal_gm` | `goal_gm` | goal_gm at goal_target grain |
| P&L adjustment / measure | `goal_ngm` | `goal_ngm` | goal_ngm at goal_target grain |
| P&L adjustment / measure | `goal_nsales` | `goal_nsales` | goal_nsales at goal_target grain |
| P&L adjustment / measure | `goal_opl_gm` | `goal_opl_gm` | goal_opl_gm at goal_target grain |
| P&L adjustment / measure | `goal_oplgm_plus_amt` | `goal_oplgm_plus_amt` | goal_oplgm_plus_amt at goal_target grain |
| P&L adjustment / measure | `goal_pdt` | `goal_pdt` | goal_pdt at goal_target grain |
| P&L adjustment / measure | `goal_soft_sales` | `goal_soft_sales` | goal_soft_sales at goal_target grain |
| P&L adjustment / measure | `goal_tgm` | `goal_tgm` | goal_tgm at goal_target grain |
| P&L adjustment / measure | `goal_total_btl` | `goal_total_btl` | goal_total_btl at goal_target grain |
| P&L adjustment / measure | `lm_cgp` | `cgp` | cgp at last_month grain |
| P&L adjustment / measure | `lm_cgp_2` | `cgp_2` | cgp_2 at last_month grain |
| P&L adjustment / measure | `lm_cost` | `cost` | cost at last_month grain |
| P&L adjustment / measure | `lm_cost_2` | `cost_2` | cost_2 at last_month grain |
| P&L adjustment / measure | `lm_ds_cost` | `ds_cost` | ds_cost at last_month grain |
| P&L adjustment / measure | `lm_ds_cost_2` | `ds_cost_2` | ds_cost_2 at last_month grain |
| P&L adjustment / measure | `lm_ds_sales` | `ds_sales` | ds_sales at last_month grain |
| P&L adjustment / measure | `lm_ds_sales_2` | `ds_sales_2` | ds_sales_2 at last_month grain |
| P&L adjustment / measure | `lm_ds_scm_usage` | `ds_scm_usage` | ds_scm_usage at last_month grain |
| P&L adjustment / measure | `lm_ds_scm_usage_2` | `ds_scm_usage_2` | ds_scm_usage_2 at last_month grain |
| P&L adjustment / measure | `lm_fx_cost` | `fx_cost` | fx_cost at last_month grain |
| Governed profitability | `lm_gm` | `gm_amt` | gm_amt at last_month grain |
| P&L adjustment / measure | `lm_gm_2` | `gm_2` | gm_2 at last_month grain |
| Governed profitability | `lm_ngm` | `ngm_amt` | ngm_amt at last_month grain |
| P&L adjustment / measure | `lm_ngm_2` | `ngm_2` | ngm_2 at last_month grain |
| Governed profitability | `lm_opl` | `oplgm_amt` | oplgm_amt at last_month grain |
| P&L adjustment / measure | `lm_opl_2` | `opl_2` | opl_2 at last_month grain |
| Governed profitability | `lm_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at last_month grain |
| Governed profitability | `lm_sales` | `net_sales` | net_sales at last_month grain |
| P&L adjustment / measure | `lm_sales_2` | `sales_2` | sales_2 at last_month grain |
| P&L adjustment / measure | `lm_scm_disc` | `scm_disc` | scm_disc at last_month grain |
| P&L adjustment / measure | `lm_scm_disc_2` | `scm_disc_2` | scm_disc_2 at last_month grain |
| P&L adjustment / measure | `lm_scm_ndisc` | `scm_ndisc` | scm_ndisc at last_month grain |
| P&L adjustment / measure | `lm_scm_ndisc_2` | `scm_ndisc_2` | scm_ndisc_2 at last_month grain |
| P&L adjustment / measure | `lm_scm_usage` | `scm_usage` | scm_usage at last_month grain |
| P&L adjustment / measure | `lm_scm_usage_2` | `scm_usage_2` | scm_usage_2 at last_month grain |
| P&L adjustment / measure | `lm_stock_cost` | `stock_cost` | stock_cost at last_month grain |
| P&L adjustment / measure | `lm_stock_cost_2` | `stock_cost_2` | stock_cost_2 at last_month grain |
| P&L adjustment / measure | `lm_stock_sales` | `stock_sales` | stock_sales at last_month grain |
| P&L adjustment / measure | `lm_stock_sales_2` | `stock_sales_2` | stock_sales_2 at last_month grain |
| P&L adjustment / measure | `lm_stock_scm_usage` | `stock_scm_usage` | stock_scm_usage at last_month grain |
| P&L adjustment / measure | `lm_stock_scm_usage_2` | `stock_scm_usage_2` | stock_scm_usage_2 at last_month grain |
| Governed profitability | `lm_tgm` | `tgm_amt` | tgm_amt at last_month grain |
| P&L adjustment / measure | `lm_tgm_2` | `tgm_2` | tgm_2 at last_month grain |
| Governed profitability | `lm_total_btl` | `total_btl` | total_btl at last_month grain |
| P&L adjustment / measure | `lm_total_btl_2` | `total_btl_2` | total_btl_2 at last_month grain |
| P&L adjustment / measure | `lm_unit` | `unit` | unit at last_month grain |
| P&L adjustment / measure | `lm_unit_2` | `unit_2` | unit_2 at last_month grain |
| P&L adjustment / measure | `m_cgp` | `cgp` | cgp at current_month grain |
| P&L adjustment / measure | `m_cost` | `cost` | cost at current_month grain |
| P&L adjustment / measure | `m_ds_cost` | `ds_cost` | ds_cost at current_month grain |
| P&L adjustment / measure | `m_ds_sales` | `ds_sales` | ds_sales at current_month grain |
| P&L adjustment / measure | `m_ds_scm_usage` | `ds_scm_usage` | ds_scm_usage at current_month grain |
| P&L adjustment / measure | `m_fx_cost` | `fx_cost` | fx_cost at current_month grain |
| Governed profitability | `m_gm` | `gm_amt` | gm_amt at current_month grain |
| Governed profitability | `m_ngm` | `ngm_amt` | ngm_amt at current_month grain |
| Governed profitability | `m_opl` | `oplgm_amt` | oplgm_amt at current_month grain |
| Governed profitability | `m_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at current_month grain |
| Governed profitability | `m_sales` | `net_sales` | net_sales at current_month grain |
| P&L adjustment / measure | `m_scm_disc` | `scm_disc` | scm_disc at current_month grain |
| P&L adjustment / measure | `m_scm_ndisc` | `scm_ndisc` | scm_ndisc at current_month grain |
| P&L adjustment / measure | `m_scm_usage` | `scm_usage` | scm_usage at current_month grain |
| P&L adjustment / measure | `m_stock_cost` | `stock_cost` | stock_cost at current_month grain |
| P&L adjustment / measure | `m_stock_sales` | `stock_sales` | stock_sales at current_month grain |
| P&L adjustment / measure | `m_stock_scm_usage` | `stock_scm_usage` | stock_scm_usage at current_month grain |
| Governed profitability | `m_tgm` | `tgm_amt` | tgm_amt at current_month grain |
| Governed profitability | `m_total_btl` | `total_btl` | total_btl at current_month grain |
| P&L adjustment / measure | `m_unit` | `unit` | unit at current_month grain |
| P&L adjustment / measure | `pm_cgp` | `cgp` | cgp at prior_month grain |
| P&L adjustment / measure | `pm_cgp_2` | `cgp_2` | cgp_2 at prior_month grain |
| P&L adjustment / measure | `pm_cost` | `cost` | cost at prior_month grain |
| P&L adjustment / measure | `pm_cost_2` | `cost_2` | cost_2 at prior_month grain |
| P&L adjustment / measure | `pm_ds_cost` | `ds_cost` | ds_cost at prior_month grain |
| P&L adjustment / measure | `pm_ds_cost_2` | `ds_cost_2` | ds_cost_2 at prior_month grain |
| P&L adjustment / measure | `pm_ds_sales` | `ds_sales` | ds_sales at prior_month grain |
| P&L adjustment / measure | `pm_ds_sales_2` | `ds_sales_2` | ds_sales_2 at prior_month grain |
| P&L adjustment / measure | `pm_ds_scm_usage` | `ds_scm_usage` | ds_scm_usage at prior_month grain |
| P&L adjustment / measure | `pm_ds_scm_usage_2` | `ds_scm_usage_2` | ds_scm_usage_2 at prior_month grain |
| P&L adjustment / measure | `pm_fx_cost` | `fx_cost` | fx_cost at prior_month grain |
| Governed profitability | `pm_gm` | `gm_amt` | gm_amt at prior_month grain |
| P&L adjustment / measure | `pm_gm_2` | `gm_2` | gm_2 at prior_month grain |
| Governed profitability | `pm_ngm` | `ngm_amt` | ngm_amt at prior_month grain |
| P&L adjustment / measure | `pm_ngm_2` | `ngm_2` | ngm_2 at prior_month grain |
| Governed profitability | `pm_opl` | `oplgm_amt` | oplgm_amt at prior_month grain |
| P&L adjustment / measure | `pm_opl_2` | `opl_2` | opl_2 at prior_month grain |
| Governed profitability | `pm_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at prior_month grain |
| Governed profitability | `pm_sales` | `net_sales` | net_sales at prior_month grain |
| P&L adjustment / measure | `pm_sales_2` | `sales_2` | sales_2 at prior_month grain |
| P&L adjustment / measure | `pm_scm_disc` | `scm_disc` | scm_disc at prior_month grain |
| P&L adjustment / measure | `pm_scm_disc_2` | `scm_disc_2` | scm_disc_2 at prior_month grain |
| P&L adjustment / measure | `pm_scm_ndisc` | `scm_ndisc` | scm_ndisc at prior_month grain |
| P&L adjustment / measure | `pm_scm_ndisc_2` | `scm_ndisc_2` | scm_ndisc_2 at prior_month grain |
| P&L adjustment / measure | `pm_scm_usage` | `scm_usage` | scm_usage at prior_month grain |
| P&L adjustment / measure | `pm_scm_usage_2` | `scm_usage_2` | scm_usage_2 at prior_month grain |
| P&L adjustment / measure | `pm_stock_cost` | `stock_cost` | stock_cost at prior_month grain |
| P&L adjustment / measure | `pm_stock_cost_2` | `stock_cost_2` | stock_cost_2 at prior_month grain |
| P&L adjustment / measure | `pm_stock_sales` | `stock_sales` | stock_sales at prior_month grain |
| P&L adjustment / measure | `pm_stock_sales_2` | `stock_sales_2` | stock_sales_2 at prior_month grain |
| P&L adjustment / measure | `pm_stock_scm_usage` | `stock_scm_usage` | stock_scm_usage at prior_month grain |
| P&L adjustment / measure | `pm_stock_scm_usage_2` | `stock_scm_usage_2` | stock_scm_usage_2 at prior_month grain |
| Governed profitability | `pm_tgm` | `tgm_amt` | tgm_amt at prior_month grain |
| P&L adjustment / measure | `pm_tgm_2` | `tgm_2` | tgm_2 at prior_month grain |
| Governed profitability | `pm_total_btl` | `total_btl` | total_btl at prior_month grain |
| P&L adjustment / measure | `pm_total_btl_2` | `total_btl_2` | total_btl_2 at prior_month grain |
| P&L adjustment / measure | `pm_unit` | `unit` | unit at prior_month grain |
| P&L adjustment / measure | `pm_unit_2` | `unit_2` | unit_2 at prior_month grain |
| P&L adjustment / measure | `ppm_cgp` | `cgp` | cgp at prior_prior_month grain |
| P&L adjustment / measure | `ppm_cgp_2` | `cgp_2` | cgp_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_cost` | `cost` | cost at prior_prior_month grain |
| P&L adjustment / measure | `ppm_cost_2` | `cost_2` | cost_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ds_cost` | `ds_cost` | ds_cost at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ds_cost_2` | `ds_cost_2` | ds_cost_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ds_sales` | `ds_sales` | ds_sales at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ds_sales_2` | `ds_sales_2` | ds_sales_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ds_scm_usage` | `ds_scm_usage` | ds_scm_usage at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ds_scm_usage_2` | `ds_scm_usage_2` | ds_scm_usage_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_fx_cost` | `fx_cost` | fx_cost at prior_prior_month grain |
| Governed profitability | `ppm_gm` | `gm_amt` | gm_amt at prior_prior_month grain |
| P&L adjustment / measure | `ppm_gm_2` | `gm_2` | gm_2 at prior_prior_month grain |
| Governed profitability | `ppm_ngm` | `ngm_amt` | ngm_amt at prior_prior_month grain |
| P&L adjustment / measure | `ppm_ngm_2` | `ngm_2` | ngm_2 at prior_prior_month grain |
| Governed profitability | `ppm_opl` | `oplgm_amt` | oplgm_amt at prior_prior_month grain |
| P&L adjustment / measure | `ppm_opl_2` | `opl_2` | opl_2 at prior_prior_month grain |
| Governed profitability | `ppm_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at prior_prior_month grain |
| Governed profitability | `ppm_sales` | `net_sales` | net_sales at prior_prior_month grain |
| P&L adjustment / measure | `ppm_sales_2` | `sales_2` | sales_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_scm_disc` | `scm_disc` | scm_disc at prior_prior_month grain |
| P&L adjustment / measure | `ppm_scm_disc_2` | `scm_disc_2` | scm_disc_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_scm_ndisc` | `scm_ndisc` | scm_ndisc at prior_prior_month grain |
| P&L adjustment / measure | `ppm_scm_ndisc_2` | `scm_ndisc_2` | scm_ndisc_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_scm_usage` | `scm_usage` | scm_usage at prior_prior_month grain |
| P&L adjustment / measure | `ppm_scm_usage_2` | `scm_usage_2` | scm_usage_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_stock_cost` | `stock_cost` | stock_cost at prior_prior_month grain |
| P&L adjustment / measure | `ppm_stock_cost_2` | `stock_cost_2` | stock_cost_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_stock_sales` | `stock_sales` | stock_sales at prior_prior_month grain |
| P&L adjustment / measure | `ppm_stock_sales_2` | `stock_sales_2` | stock_sales_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_stock_scm_usage` | `stock_scm_usage` | stock_scm_usage at prior_prior_month grain |
| P&L adjustment / measure | `ppm_stock_scm_usage_2` | `stock_scm_usage_2` | stock_scm_usage_2 at prior_prior_month grain |
| Governed profitability | `ppm_tgm` | `tgm_amt` | tgm_amt at prior_prior_month grain |
| P&L adjustment / measure | `ppm_tgm_2` | `tgm_2` | tgm_2 at prior_prior_month grain |
| Governed profitability | `ppm_total_btl` | `total_btl` | total_btl at prior_prior_month grain |
| P&L adjustment / measure | `ppm_total_btl_2` | `total_btl_2` | total_btl_2 at prior_prior_month grain |
| P&L adjustment / measure | `ppm_unit` | `unit` | unit at prior_prior_month grain |
| P&L adjustment / measure | `ppm_unit_2` | `unit_2` | unit_2 at prior_prior_month grain |
| P&L adjustment / measure | `rr_cgp` | `cgp` | cgp at run_rate grain |
| P&L adjustment / measure | `rr_cost` | `cost` | cost at run_rate grain |
| Governed profitability | `rr_gm` | `gm_amt` | gm_amt at run_rate grain |
| Governed profitability | `rr_ngm` | `ngm_amt` | ngm_amt at run_rate grain |
| Governed profitability | `rr_opl` | `oplgm_amt` | oplgm_amt at run_rate grain |
| Governed profitability | `rr_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at run_rate grain |
| Governed profitability | `rr_sales` | `net_sales` | net_sales at run_rate grain |
| Governed profitability | `rr_tgm` | `tgm_amt` | tgm_amt at run_rate grain |
| Governed profitability | `rr_total_btl` | `total_btl` | total_btl at run_rate grain |
| P&L adjustment / measure | `rr_unit` | `unit` | unit at run_rate grain |
| P&L adjustment / measure | `w_cgp` | `cgp` | cgp at wtd grain |
| P&L adjustment / measure | `w_cost` | `cost` | cost at wtd grain |
| P&L adjustment / measure | `w_fx_cost` | `fx_cost` | fx_cost at wtd grain |
| Governed profitability | `w_gm` | `gm_amt` | gm_amt at wtd grain |
| Governed profitability | `w_ngm` | `ngm_amt` | ngm_amt at wtd grain |
| Governed profitability | `w_opl` | `oplgm_amt` | oplgm_amt at wtd grain |
| Governed profitability | `w_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at wtd grain |
| Governed profitability | `w_sales` | `net_sales` | net_sales at wtd grain |
| P&L adjustment / measure | `w_scm_usage` | `scm_usage` | scm_usage at wtd grain |
| Governed profitability | `w_tgm` | `tgm_amt` | tgm_amt at wtd grain |
| Governed profitability | `w_total_btl` | `total_btl` | total_btl at wtd grain |
| P&L adjustment / measure | `w_unit` | `unit` | unit at wtd grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `cgp` | daily | `d_cgp` | Not in metric-index.md |
| `cost` | daily | `d_cost` | Not in metric-index.md |
| `fx_cost` | daily | `d_fx_cost` | Not in metric-index.md |
| `gm_amt` | daily | `d_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `ngm_amt` | daily | `d_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | daily | `d_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | daily | `d_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | daily | `d_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `scm_usage` | daily | `d_scm_usage` | Not in metric-index.md |
| `tgm_amt` | daily | `d_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | daily | `d_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `unit` | daily | `d_unit` | Not in metric-index.md |
| `goal_cust_cnt` | goal_target | `goal_cust_cnt` | Not in metric-index.md |
| `goal_dos` | goal_target | `goal_dos` | Not in metric-index.md |
| `goal_gm` | goal_target | `goal_gm` | Not in metric-index.md |
| `goal_ngm` | goal_target | `goal_ngm` | Not in metric-index.md |
| `goal_nsales` | goal_target | `goal_nsales` | Not in metric-index.md |
| `goal_opl_gm` | goal_target | `goal_opl_gm` | Not in metric-index.md |
| `goal_oplgm_plus_amt` | goal_target | `goal_oplgm_plus_amt` | Not in metric-index.md |
| `goal_pdt` | goal_target | `goal_pdt` | Not in metric-index.md |
| `goal_soft_sales` | goal_target | `goal_soft_sales` | Not in metric-index.md |
| `goal_tgm` | goal_target | `goal_tgm` | Not in metric-index.md |
| `goal_total_btl` | goal_target | `goal_total_btl` | Not in metric-index.md |
| `cgp` | last_month | `lm_cgp` | Not in metric-index.md |
| `cgp_2` | last_month | `lm_cgp_2` | Not in metric-index.md |
| `cost` | last_month | `lm_cost` | Not in metric-index.md |
| `cost_2` | last_month | `lm_cost_2` | Not in metric-index.md |
| `ds_cost` | last_month | `lm_ds_cost` | Not in metric-index.md |
| `ds_cost_2` | last_month | `lm_ds_cost_2` | Not in metric-index.md |
| `ds_sales` | last_month | `lm_ds_sales` | Not in metric-index.md |
| `ds_sales_2` | last_month | `lm_ds_sales_2` | Not in metric-index.md |
| `ds_scm_usage` | last_month | `lm_ds_scm_usage` | Not in metric-index.md |
| `ds_scm_usage_2` | last_month | `lm_ds_scm_usage_2` | Not in metric-index.md |
| `fx_cost` | last_month | `lm_fx_cost` | Not in metric-index.md |
| `gm_amt` | last_month | `lm_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `gm_2` | last_month | `lm_gm_2` | Not in metric-index.md |
| `ngm_amt` | last_month | `lm_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `ngm_2` | last_month | `lm_ngm_2` | Not in metric-index.md |
| `oplgm_amt` | last_month | `lm_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `opl_2` | last_month | `lm_opl_2` | Not in metric-index.md |
| `oplgm_plus_amt` | last_month | `lm_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | last_month | `lm_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `sales_2` | last_month | `lm_sales_2` | Not in metric-index.md |
| `scm_disc` | last_month | `lm_scm_disc` | Not in metric-index.md |
| `scm_disc_2` | last_month | `lm_scm_disc_2` | Not in metric-index.md |
| `scm_ndisc` | last_month | `lm_scm_ndisc` | Not in metric-index.md |
| `scm_ndisc_2` | last_month | `lm_scm_ndisc_2` | Not in metric-index.md |
| `scm_usage` | last_month | `lm_scm_usage` | Not in metric-index.md |
| `scm_usage_2` | last_month | `lm_scm_usage_2` | Not in metric-index.md |
| `stock_cost` | last_month | `lm_stock_cost` | Not in metric-index.md |
| `stock_cost_2` | last_month | `lm_stock_cost_2` | Not in metric-index.md |
| `stock_sales` | last_month | `lm_stock_sales` | Not in metric-index.md |
| `stock_sales_2` | last_month | `lm_stock_sales_2` | Not in metric-index.md |
| `stock_scm_usage` | last_month | `lm_stock_scm_usage` | Not in metric-index.md |
| `stock_scm_usage_2` | last_month | `lm_stock_scm_usage_2` | Not in metric-index.md |
| `tgm_amt` | last_month | `lm_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `tgm_2` | last_month | `lm_tgm_2` | Not in metric-index.md |
| `total_btl` | last_month | `lm_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `total_btl_2` | last_month | `lm_total_btl_2` | Not in metric-index.md |
| `unit` | last_month | `lm_unit` | Not in metric-index.md |
| `unit_2` | last_month | `lm_unit_2` | Not in metric-index.md |
| `cgp` | current_month | `m_cgp` | Not in metric-index.md |
| `cost` | current_month | `m_cost` | Not in metric-index.md |
| `ds_cost` | current_month | `m_ds_cost` | Not in metric-index.md |
| `ds_sales` | current_month | `m_ds_sales` | Not in metric-index.md |
| `ds_scm_usage` | current_month | `m_ds_scm_usage` | Not in metric-index.md |
| `fx_cost` | current_month | `m_fx_cost` | Not in metric-index.md |
| `gm_amt` | current_month | `m_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `ngm_amt` | current_month | `m_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | current_month | `m_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | current_month | `m_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | current_month | `m_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `scm_disc` | current_month | `m_scm_disc` | Not in metric-index.md |
| `scm_ndisc` | current_month | `m_scm_ndisc` | Not in metric-index.md |
| `scm_usage` | current_month | `m_scm_usage` | Not in metric-index.md |
| `stock_cost` | current_month | `m_stock_cost` | Not in metric-index.md |
| `stock_sales` | current_month | `m_stock_sales` | Not in metric-index.md |
| `stock_scm_usage` | current_month | `m_stock_scm_usage` | Not in metric-index.md |
| `tgm_amt` | current_month | `m_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | current_month | `m_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `unit` | current_month | `m_unit` | Not in metric-index.md |
| `cgp` | prior_month | `pm_cgp` | Not in metric-index.md |
| `cgp_2` | prior_month | `pm_cgp_2` | Not in metric-index.md |
| `cost` | prior_month | `pm_cost` | Not in metric-index.md |
| `cost_2` | prior_month | `pm_cost_2` | Not in metric-index.md |
| `ds_cost` | prior_month | `pm_ds_cost` | Not in metric-index.md |
| `ds_cost_2` | prior_month | `pm_ds_cost_2` | Not in metric-index.md |
| `ds_sales` | prior_month | `pm_ds_sales` | Not in metric-index.md |
| `ds_sales_2` | prior_month | `pm_ds_sales_2` | Not in metric-index.md |
| `ds_scm_usage` | prior_month | `pm_ds_scm_usage` | Not in metric-index.md |
| `ds_scm_usage_2` | prior_month | `pm_ds_scm_usage_2` | Not in metric-index.md |
| `fx_cost` | prior_month | `pm_fx_cost` | Not in metric-index.md |
| `gm_amt` | prior_month | `pm_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `gm_2` | prior_month | `pm_gm_2` | Not in metric-index.md |
| `ngm_amt` | prior_month | `pm_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `ngm_2` | prior_month | `pm_ngm_2` | Not in metric-index.md |
| `oplgm_amt` | prior_month | `pm_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `opl_2` | prior_month | `pm_opl_2` | Not in metric-index.md |
| `oplgm_plus_amt` | prior_month | `pm_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | prior_month | `pm_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `sales_2` | prior_month | `pm_sales_2` | Not in metric-index.md |
| `scm_disc` | prior_month | `pm_scm_disc` | Not in metric-index.md |
| `scm_disc_2` | prior_month | `pm_scm_disc_2` | Not in metric-index.md |
| `scm_ndisc` | prior_month | `pm_scm_ndisc` | Not in metric-index.md |
| `scm_ndisc_2` | prior_month | `pm_scm_ndisc_2` | Not in metric-index.md |
| `scm_usage` | prior_month | `pm_scm_usage` | Not in metric-index.md |
| `scm_usage_2` | prior_month | `pm_scm_usage_2` | Not in metric-index.md |
| `stock_cost` | prior_month | `pm_stock_cost` | Not in metric-index.md |
| `stock_cost_2` | prior_month | `pm_stock_cost_2` | Not in metric-index.md |
| `stock_sales` | prior_month | `pm_stock_sales` | Not in metric-index.md |
| `stock_sales_2` | prior_month | `pm_stock_sales_2` | Not in metric-index.md |
| `stock_scm_usage` | prior_month | `pm_stock_scm_usage` | Not in metric-index.md |
| `stock_scm_usage_2` | prior_month | `pm_stock_scm_usage_2` | Not in metric-index.md |
| `tgm_amt` | prior_month | `pm_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `tgm_2` | prior_month | `pm_tgm_2` | Not in metric-index.md |
| `total_btl` | prior_month | `pm_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `total_btl_2` | prior_month | `pm_total_btl_2` | Not in metric-index.md |
| `unit` | prior_month | `pm_unit` | Not in metric-index.md |
| `unit_2` | prior_month | `pm_unit_2` | Not in metric-index.md |
| `cgp` | prior_prior_month | `ppm_cgp` | Not in metric-index.md |
| `cgp_2` | prior_prior_month | `ppm_cgp_2` | Not in metric-index.md |
| `cost` | prior_prior_month | `ppm_cost` | Not in metric-index.md |
| `cost_2` | prior_prior_month | `ppm_cost_2` | Not in metric-index.md |
| `ds_cost` | prior_prior_month | `ppm_ds_cost` | Not in metric-index.md |
| `ds_cost_2` | prior_prior_month | `ppm_ds_cost_2` | Not in metric-index.md |
| `ds_sales` | prior_prior_month | `ppm_ds_sales` | Not in metric-index.md |
| `ds_sales_2` | prior_prior_month | `ppm_ds_sales_2` | Not in metric-index.md |
| `ds_scm_usage` | prior_prior_month | `ppm_ds_scm_usage` | Not in metric-index.md |
| `ds_scm_usage_2` | prior_prior_month | `ppm_ds_scm_usage_2` | Not in metric-index.md |
| `fx_cost` | prior_prior_month | `ppm_fx_cost` | Not in metric-index.md |
| `gm_amt` | prior_prior_month | `ppm_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `gm_2` | prior_prior_month | `ppm_gm_2` | Not in metric-index.md |
| `ngm_amt` | prior_prior_month | `ppm_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `ngm_2` | prior_prior_month | `ppm_ngm_2` | Not in metric-index.md |
| `oplgm_amt` | prior_prior_month | `ppm_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `opl_2` | prior_prior_month | `ppm_opl_2` | Not in metric-index.md |
| `oplgm_plus_amt` | prior_prior_month | `ppm_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | prior_prior_month | `ppm_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `sales_2` | prior_prior_month | `ppm_sales_2` | Not in metric-index.md |
| `scm_disc` | prior_prior_month | `ppm_scm_disc` | Not in metric-index.md |
| `scm_disc_2` | prior_prior_month | `ppm_scm_disc_2` | Not in metric-index.md |
| `scm_ndisc` | prior_prior_month | `ppm_scm_ndisc` | Not in metric-index.md |
| `scm_ndisc_2` | prior_prior_month | `ppm_scm_ndisc_2` | Not in metric-index.md |
| `scm_usage` | prior_prior_month | `ppm_scm_usage` | Not in metric-index.md |
| `scm_usage_2` | prior_prior_month | `ppm_scm_usage_2` | Not in metric-index.md |
| `stock_cost` | prior_prior_month | `ppm_stock_cost` | Not in metric-index.md |
| `stock_cost_2` | prior_prior_month | `ppm_stock_cost_2` | Not in metric-index.md |
| `stock_sales` | prior_prior_month | `ppm_stock_sales` | Not in metric-index.md |
| `stock_sales_2` | prior_prior_month | `ppm_stock_sales_2` | Not in metric-index.md |
| `stock_scm_usage` | prior_prior_month | `ppm_stock_scm_usage` | Not in metric-index.md |
| `stock_scm_usage_2` | prior_prior_month | `ppm_stock_scm_usage_2` | Not in metric-index.md |
| `tgm_amt` | prior_prior_month | `ppm_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `tgm_2` | prior_prior_month | `ppm_tgm_2` | Not in metric-index.md |
| `total_btl` | prior_prior_month | `ppm_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `total_btl_2` | prior_prior_month | `ppm_total_btl_2` | Not in metric-index.md |
| `unit` | prior_prior_month | `ppm_unit` | Not in metric-index.md |
| `unit_2` | prior_prior_month | `ppm_unit_2` | Not in metric-index.md |
| `cgp` | run_rate | `rr_cgp` | Not in metric-index.md |
| `cost` | run_rate | `rr_cost` | Not in metric-index.md |
| `gm_amt` | run_rate | `rr_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `ngm_amt` | run_rate | `rr_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | run_rate | `rr_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | run_rate | `rr_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | run_rate | `rr_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `tgm_amt` | run_rate | `rr_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | run_rate | `rr_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `unit` | run_rate | `rr_unit` | Not in metric-index.md |
| `cgp` | wtd | `w_cgp` | Not in metric-index.md |
| `cost` | wtd | `w_cost` | Not in metric-index.md |
| `fx_cost` | wtd | `w_fx_cost` | Not in metric-index.md |
| `gm_amt` | wtd | `w_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `ngm_amt` | wtd | `w_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | wtd | `w_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | wtd | `w_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | wtd | `w_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `scm_usage` | wtd | `w_scm_usage` | Not in metric-index.md |
| `tgm_amt` | wtd | `w_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | wtd | `w_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `unit` | wtd | `w_unit` | Not in metric-index.md |

### etl_metrics

Formulas below are sourced from [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md) for logical metrics present on this table.
Index formulas are canonical: this enricher copies them into KB and never overwrites `final_effective_formula_sql` in the metric-index.

#### `gm_amt`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#gm_amt)
- **Business definition:** Core line gross margin before BTL/PDT and full NGM adjustment chain.
```sql
(nvl(u_price,0) - nvl(if(sales_cost is null, u_cost, sales_cost), 0)) * nvl(ship_qty,0)
```

#### `net_sales`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#net_sales)
- **Business definition:** Shipped quantity times unit price plus per-unit sum expense (net of returns scope per order_type filter).
```sql
nvl(ship_qty,0) * (nvl(u_price,0) + nvl(u_sum_expense,0))
```

#### `ngm_amt`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#ngm_amt)
- **Business definition:** Net Gross Margin — final P&L profitability metric for PM/executive use after full adjustment chain.
```sql
( (nvl(u_price,0)-nvl(if(sales_cost is null,u_cost,sales_cost),0))*nvl(ship_qty,0)
      + nvl(BTL,0) + nvl(TRANS_BTL,0) + nvl(ONE_TIME_BTL,0) + nvl(HBTL,0) + nvl(SCM_PROFIT_ADJ,0)
      + nvl(BTL_BACKOUT,0) + nvl(PDT,0) + nvl(AP_FINANCE,0) + nvl(SCM_COST,0) + nvl(SCM_RISK,0)
      + nvl(INV_COST,0) + nvl(INV_RESERVE,0) + nvl(INFRASTRUCTURE,0) + nvl(MARKETING,0)
      + nvl(FRT_OUT_LOAD,0) + nvl(FRT_OUT_EXP,0) + nvl(FRT_OB_RECOVERY,0) + nvl(FRT_IB_RECOVERY,0)
      + nvl(WHOH_PACK,0) + nvl(CSGN_EDI_FEE,0) + nvl(CUST_FINANCE,0) * nvl(c.NGM_CFN_RATE,1)
      + nvl(AR_FIN_RECOVERY,0) + nvl(CR_RISK_CTERM,0) * nvl(c.NGM_CRCT_RATE,1)
      + nvl(CUST_PMT_DISC,0) + nvl(CUST_REBATE,0) + nvl(CVR_RM,0) + nvl(DIRECT_CREDIT,0)
      + nvl(FLR_SYNNEX,0) + nvl(RMA,0) + nvl(MOF,0) + nvl(MARGIN_SHARE,0) + nvl(AP_ADJ,0)
      + nvl(CORPORATE,0) + nvl(HC_PM,0) + nvl(HC_BD,0) + nvl(HC_SALES,0) + nvl(ORDER_OVERHEAD,0)
      + nvl(OTHERS,0) + nvl(MFG_OH,0) + nvl(SFS,0) )
```

#### `oplgm_amt`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#oplgm_amt)
- **Business definition:** Order Profit and Loss for sales commission logic.
```sql
( (nvl(u_price,0)-nvl(if(sales_cost is null,u_cost,sales_cost),0))*nvl(ship_qty,0)
      + nvl(BTL_BACKOUT,0) + nvl(BTL_SALES,0) + nvl(TRANS_BTL_SALES,0)
      + nvl(PDT,0) + nvl(CUST_PMT_DISC,0) + nvl(CUST_REBATE,0) + nvl(CVR_RM,0)
      + nvl(FRT_OUT_LOAD,0) + nvl(FRT_OUT_EXP,0) + nvl(FRT_OB_RECOVERY,0)
      + nvl(MOF,0) + nvl(CUST_FINANCE_SALES,0) * nvl(c.CPL_CFN_RATE,1)
      + nvl(AR_FIN_RECOVERY,0) + nvl(CR_RISK_CTERM,0) * nvl(c.CPL_CRCT_RATE,1)
      + nvl(FLR_SYNNEX,0) + nvl(DIRECT_CREDIT,0) + nvl(WHOH_PACK,0) + nvl(RMA,0)
      + nvl(ORDER_OVERHEAD,0) + nvl(CSGN_EDI_FEE,0) + nvl(FRT_IB_RECOVERY,0)
      + nvl(OTHERS_SALES,0) + nvl(SFS,0)
      + (nvl(u_price,0)+nvl(u_sum_expense,0))*nvl(ship_qty,0) * nvl(c.CPL_COOP_RATE,0) )
```

#### `oplgm_plus_amt`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#oplgm_plus_amt)
- **Business definition:** Extended OPL metric including additional direct cost/expense components beyond base OPL.
```sql
derived from oplgm_amt chain with additional OPL+ components (see oplgm_plus_amt_calcproc column on DWD)
```

#### `tgm_amt`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#tgm_amt)
- **Business definition:** Gross margin with core BTL/PDT and related trade-term add-backs (pre-full NGM overhead chain).
```sql
gm_amt + nvl(BTL,0) + nvl(TRANS_BTL,0) + nvl(ONE_TIME_BTL,0) + nvl(HBTL,0) + nvl(SCM_PROFIT_ADJ,0) + nvl(BTL_BACKOUT,0) + nvl(PDT,0)
```

#### `total_btl`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#total_btl)
- **Business definition:** Aggregate of Below-The-Line trade term adjustment components (BTL, TRANS_BTL, ONE_TIME_BTL, HBTL, etc.).
```sql
nvl(BTL,0) + nvl(TRANS_BTL,0) + nvl(ONE_TIME_BTL,0) + nvl(HBTL,0) + nvl(SCM_PROFIT_ADJ,0) + nvl(BTL_BACKOUT,0)
```

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use `month_no` (or `month_no` for month-indexed DM tables) for reporting scope.
**Technical predicates (load only):** Partition predicate on INSERT OVERWRITE; see Key filters below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| (ETL join) | — | left join (select * from dim_${country}.dim_pub_sales_territory_df | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |

### Key filters and ETL business logic
- `date_flag = '${date_flag}') as table_dwd` — inferred from ETL WHERE clause
- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For profitability metrics on this table, always filter `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

### Standard time-filter SQL
```sql
-- Reporting filter pattern (replace partition value from L4 trace)
SELECT *
FROM dm_us.dm_disty_brpt_sales_comb_mtd
WHERE month_no = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dim_us.dim_pub_sales_mgr_dept_df, dim_us.dim_pub_sales_rep_terr_df, dim_us.dim_pub_sales_territory_df, ods_us.ods_cis_corp_cust_type).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dm_us.dm_disty_brpt_sales_comb_mtd` partition `month_no`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dm_us_dm_disty_brpt_sales_comb_mtd["dm_us.dm_disty_brpt_sales_comb_mtd"]
  src0["dim_us.dim_pub_sales_mgr_dept_df"]
  src0 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src1["dim_us.dim_pub_sales_rep_terr_df"]
  src1 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src2["dim_us.dim_pub_sales_territory_df"]
  src2 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src3["ods_us.ods_cis_corp_cust_type"]
  src3 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src4["ods_us.ods_cis_corp_division"]
  src4 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src5["ods_us.ods_cis_corp_manager"]
  src5 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src6["ods_us.ods_cis_corp_territory_group"]
  src6 --> dm_us_dm_disty_brpt_sales_comb_mtd
  src7["ods_us.ods_cis_corp_territory_sub_group"]
  src7 --> dm_us_dm_disty_brpt_sales_comb_mtd
  consumers["B Report dashboards / DM serving"]
  dm_us_dm_disty_brpt_sales_comb_mtd --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_sales_mgr_dept_df` | source |
| `dim_us.dim_pub_sales_rep_terr_df` | source |
| `dim_us.dim_pub_sales_territory_df` | source |
| `dm_us.dm_disty_brpt_sales_comb_mtd` | target |
| `ods_us.ods_cis_corp_cust_type` | source |
| `ods_us.ods_cis_corp_division` | source |
| `ods_us.ods_cis_corp_manager` | source |
| `ods_us.ods_cis_corp_territory_group` | source |
| `ods_us.ods_cis_corp_territory_sub_group` | source |

### Step-by-step logic
#### Step 1 — dimension and reference joins

**Join keys:** see Dimension join patterns table (parsed from ETL SQL).

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `month_no` | `table_dwd.month_no` | `month_no` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:520` |
| `sales_rep_id` | `nvl(table1.sales_rep_id,-3)` | `sales_rep_id` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:522` |
| `sales_rep_name` | `concat_ws(' ', table_manager.firstname, table_manager.lastname)` | `concat_ws`, `firstname`, `lastname` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:523` |
| `sales_sup_id` | `nvl(table2.manager_id,-3)` | `manager_id` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:524` |
| `sales_sup_name` | `concat_ws(' ', table_manager2.firstname, table_manager2.lastname)` | `concat_ws`, `firstname`, `lastname` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:525` |
| `sales_mgr_id` | `nvl(table3.manager_id,-3)` | `manager_id` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:526` |
| `sales_mgr_name` | `concat_ws(' ', table_manager3.firstname, table_manager3.lastname)` | `concat_ws`, `firstname`, `lastname` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:527` |
| `sales_dir_id` | `nvl(table4.manager_id,-3)` | `manager_id` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:528` |
| `sales_dir_name` | `concat_ws(' ', table_manager4.firstname, table_manager4.lastname)` | `concat_ws`, `firstname`, `lastname` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:529` |
| `sales_vp_id` | `nvl(table5.manager_id,-3)` | `manager_id` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:530` |
| `sales_vp_name` | `concat_ws(' ', table_manager5.firstname, table_manager5.lastname)` | `concat_ws`, `firstname`, `lastname` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:531` |
| `company_no` | `table_dwd.company_no` | `company_no` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:532` |
| `3` | `nvl(table_dwd.cust_terr,-3)` | `cust_terr` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:533` |
| `3` | `nvl(table_dwd.terr_sub_group,-3)` | `terr_sub_group` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:534` |
| `3` | `nvl(table_dwd.terr_group,-3)` | `terr_group` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:535` |
| `3` | `nvl(table_dwd.cust_type,-3)` | `cust_type` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:536` |
| `3` | `nvl(table_dwd.division,-3)` | `division` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:537` |
| `goal_nsales` | `table_dwd.goal_nsales` | `goal_nsales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:539` |
| `goal_gm` | `table_dwd.goal_gm` | `goal_gm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:540` |
| `goal_ngm` | `table_dwd.goal_ngm` | `goal_ngm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:541` |
| `goal_opl_gm` | `table_dwd.goal_opl_gm` | `goal_opl_gm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:542` |
| `goal_tgm` | `table_dwd.goal_tgm` | `goal_tgm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:543` |
| `goal_dos` | `table_dwd.goal_dos` | `goal_dos` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:544` |
| `goal_pdt` | `table_dwd.goal_pdt` | `goal_pdt` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:545` |
| `goal_total_btl` | `table_dwd.goal_total_btl` | `goal_total_btl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:546` |
| `goal_cust_cnt` | `table_dwd.goal_cust_cnt` | `goal_cust_cnt` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:547` |
| `d_sales` | `table_dwd.d_sales` | `d_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:548` |
| `d_cost` | `table_dwd.d_cost` | `d_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:549` |
| `d_unit` | `table_dwd.d_unit` | `d_unit` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:550` |
| `d_gm` | `table_dwd.d_gm` | `d_gm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:551` |
| `d_ngm` | `table_dwd.d_ngm` | `d_ngm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:552` |
| `d_opl` | `table_dwd.d_opl` | `d_opl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:553` |
| `d_scm_usage` | `table_dwd.d_scm_usage` | `d_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:554` |
| `d_tgm` | `table_dwd.d_tgm` | `d_tgm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:555` |
| `d_cgp` | `table_dwd.d_cgp` | `d_cgp` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:556` |
| `d_total_btl` | `table_dwd.d_total_btl` | `d_total_btl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:557` |
| `w_sales` | `table_dwd.w_sales` | `w_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:558` |
| `w_cost` | `table_dwd.w_cost` | `w_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:559` |
| `w_unit` | `table_dwd.w_unit` | `w_unit` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:560` |
| `w_gm` | `table_dwd.w_gm` | `w_gm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:561` |
| `w_ngm` | `table_dwd.w_ngm` | `w_ngm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:562` |
| `w_opl` | `table_dwd.w_opl` | `w_opl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:563` |
| `w_scm_usage` | `table_dwd.w_scm_usage` | `w_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:564` |
| `w_tgm` | `table_dwd.w_tgm` | `w_tgm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:565` |
| `w_cgp` | `table_dwd.w_cgp` | `w_cgp` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:566` |
| `w_total_btl` | `table_dwd.w_total_btl` | `w_total_btl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:567` |
| `m_sales` | `table_dwd.m_sales` | `m_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:568` |
| `m_cost` | `table_dwd.m_cost` | `m_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:569` |
| `m_unit` | `table_dwd.m_unit` | `m_unit` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:570` |
| `m_gm` | `table_dwd.m_gm` | `m_gm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:571` |
| `m_ngm` | `table_dwd.m_ngm` | `m_ngm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:572` |
| `m_opl` | `table_dwd.m_opl` | `m_opl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:573` |
| `m_scm_usage` | `table_dwd.m_scm_usage` | `m_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:574` |
| `m_tgm` | `table_dwd.m_tgm` | `m_tgm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:575` |
| `m_scm_disc` | `table_dwd.m_scm_disc` | `m_scm_disc` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:576` |
| `m_scm_ndisc` | `table_dwd.m_scm_ndisc` | `m_scm_ndisc` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:577` |
| `m_ds_sales` | `table_dwd.m_ds_sales` | `m_ds_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:578` |
| `m_stock_sales` | `table_dwd.m_stock_sales` | `m_stock_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:579` |
| `m_ds_cost` | `table_dwd.m_ds_cost` | `m_ds_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:580` |
| `m_stock_cost` | `table_dwd.m_stock_cost` | `m_stock_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:581` |
| `m_ds_scm_usage` | `table_dwd.m_ds_scm_usage` | `m_ds_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:582` |
| `m_stock_scm_usage` | `table_dwd.m_stock_scm_usage` | `m_stock_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:583` |
| `m_cgp` | `table_dwd.m_cgp` | `m_cgp` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:584` |
| `m_total_btl` | `table_dwd.m_total_btl` | `m_total_btl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:585` |
| `pm_sales` | `table_dwd.pm_sales` | `pm_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:586` |
| `pm_cost` | `table_dwd.pm_cost` | `pm_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:587` |
| `pm_unit` | `table_dwd.pm_unit` | `pm_unit` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:588` |
| `pm_gm` | `table_dwd.pm_gm` | `pm_gm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:589` |
| `pm_ngm` | `table_dwd.pm_ngm` | `pm_ngm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:590` |
| `pm_opl` | `table_dwd.pm_opl` | `pm_opl` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:591` |
| `pm_scm_usage` | `table_dwd.pm_scm_usage` | `pm_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:592` |
| `pm_tgm` | `table_dwd.pm_tgm` | `pm_tgm` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:593` |
| `pm_scm_disc` | `table_dwd.pm_scm_disc` | `pm_scm_disc` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:594` |
| `pm_scm_ndisc` | `table_dwd.pm_scm_ndisc` | `pm_scm_ndisc` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:595` |
| `pm_ds_sales` | `table_dwd.pm_ds_sales` | `pm_ds_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:596` |
| `pm_stock_sales` | `table_dwd.pm_stock_sales` | `pm_stock_sales` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:597` |
| `pm_ds_cost` | `table_dwd.pm_ds_cost` | `pm_ds_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:598` |
| `pm_stock_cost` | `table_dwd.pm_stock_cost` | `pm_stock_cost` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:599` |
| `pm_ds_scm_usage` | `table_dwd.pm_ds_scm_usage` | `pm_ds_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:600` |
| `pm_stock_scm_usage` | `table_dwd.pm_stock_scm_usage` | `pm_stock_scm_usage` | `dm_${country}.dm_disty_brpt_sales_comb_mtd`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:601` |

_Showing 80 of 218 columns; full list in L3 `*_column_derivations.json` sidecar._

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| `-3` | business_filter | Coalesce fallback for unmatched hierarchy keys (inferred from ETL SQL) |
| `goal_type = 'NORMAL'` | business_filter | Sales goal filter when goal view is joined |

---

## L4 Validation

### Resolved partition value
| Step | Source | How `month_no` is determined |
|------|--------|-----------------------------------------------------|
| 1 | `conf.get('date_flag')` | Business process date (comment: yesterday / @process_date) — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:19` |
| 2 | `conf.get('month_no')` | Fiscal month index used in SELECT/goal joins — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:32` |
| 3 | `conf.get('dt_month')` | Hive partition key `dt_month` (yyyy-MM derived from date_flag) — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:20` |
| — | `conf.get('end_day_of_last_month')` | Period anchor for comb_mtd wide columns — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:28` |
| — | `conf.get('week_begin_of_dateflag')` | Period anchor for comb_mtd wide columns — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:31` |
| — | `conf.get('end_day_of_same_month_of_last_year')` | Period anchor for comb_mtd wide columns — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:30` |

**Plain language:** The ETL wrapper reads Azkaban-injected `conf` parameters; `date_flag` is the business processing date, and `dt_month` / `month_no` derive month scope for partitioned loads. Downstream reporting must use the same resolved period as the load partition.

### Data quality checks
- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).
- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.
- Conflict item:

### Validation SQL
```sql
-- 1) Row count by partition
SELECT month_no, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_brpt_sales_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY month_no;

-- 2) Metric sum by business dimension (top N)
SELECT sales_rep_id, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_brpt_sales_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY sales_rep_id
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT sales_rep_id, sales_sup_id, sales_mgr_id, month_no, COUNT(*) AS cnt
FROM dm_us.dm_disty_brpt_sales_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY sales_rep_id, sales_sup_id, sales_mgr_id, month_no
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- ETL SQL is authoritative for load-time joins; contract catalog is authoritative for column business definitions.
- US schema `dm_us` documented as baseline; other countries use same table names with regional `country` parameter.
- Comb_mtd and multi-period tables require correct period column selection (see L2 Metric serving map).

### Conflicts and open questions
- hive2vertica sync job `file:line` evidence: Not documented in repository (Bitbucket ETL snapshot only).
- Schedule, owner, SLA: Not documented in repository.

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dm_us.dm_disty_brpt_sales_comb_mtd` | `dm_us.dm_disty_brpt_sales_comb_mtd` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` | yes |
| **Hive alternative** | `dm_us.dm_disty_brpt_sales_comb_mtd` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dm_us.dm_disty_brpt_sales_comb_mtd` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` | — |

### Access constraints
- Standard `dw_us` / `dm_us` / `dim_us` role-based access applies.
- Country parameter `${country}` in ETL resolves schema prefix at runtime.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes |
| scan_risk_tier | medium |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Consumer | Use case |
|----------|----------|
| Consumers: PM, Sales, Buyer, BD and executive analysis views. | B Report profitability and operating performance |
| Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards. | B Report profitability and operating performance |

### Representative query patterns
```sql
SELECT month_no, SUM(net_sales) AS net_sales, SUM(ngm_amt) AS ngm_amt
FROM dm_us.dm_disty_brpt_sales_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY month_no;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_sales_mgr_dept_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `dim_us.dim_pub_sales_rep_terr_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `dim_us.dim_pub_sales_territory_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `ods_us.ods_cis_corp_cust_type` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `ods_us.ods_cis_corp_division` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `ods_us.ods_cis_corp_manager` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `ods_us.ods_cis_corp_territory_group` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |
| `ods_us.ods_cis_corp_territory_sub_group` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dm_disty_brpt_sales_comb_mtd.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:254`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dm_disty_brpt_sales_comb_mtd.py` — primary Bitbucket ETL for `dm_disty_brpt_sales_comb_mtd` — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` with B Report contract enrichment when available.*
