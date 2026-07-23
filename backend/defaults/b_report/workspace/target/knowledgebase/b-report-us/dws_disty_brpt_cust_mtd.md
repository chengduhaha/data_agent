# DWS: Customer-level B Report P&L and goals MTD serving table (cust + territory + sales hierarchy grain) (`dw_us.dws_disty_brpt_cust_mtd`)

- artifact_type: etl_table
- artifact_id: dw_us.dws_disty_brpt_cust_mtd
- domain: b-report-us
- one_line_purpose: Customer-level B Report P&L and goals MTD serving table (cust + territory + sales hierarchy grain)
- layer_type: DWS
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py
- knowledgebase_path: target/knowledgebase/b-report-us/dws_disty_brpt_cust_mtd.md
- contract_source: source/contracts/b-report-us/tables/dws_disty_brpt_cust_mtd.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dws_disty_brpt_cust_mtd`
- **Layer type:** DWS
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** one row per (`date_flag`, `cust_no`, `mcust_no`, `cust_terr`, `cust_type`, `division`, `terr_sub_group`, `terr_group`, sales hierarchy IDs, `company_no`) with MTD-cumulative measures through `date_flag`.
- **Scope:** US disty B Report customer profitability, backorder/open-order aging, run-rate, and sales goals.
- **Partition:** `date_flag` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `one`, `row`, `per`, ``date_flag``, ``cust_no``, ``mcust_no``
- **Exclusions:** Non-US schemas, backup/temp variants (`_bkp`, `_temp`); goal-only rows may appear when `table_goal` has targets without shipped P&L (`cust_no` coalesced to -3).

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country}.dws_disty_brpt_cust_mtd` | ETL target in Bitbucket script |
| Vertica | yes | `dw_us.dws_disty_brpt_cust_mtd` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dws_disty_brpt_cust_mtd` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dw_us_dws_disty_brpt_cust_mtd.json` |
| **column_count** | 145 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dws_disty_brpt_cust_mtd schema" --intent find_table_schema` |

### Lineage
- **upstream:** dim_us.dim_pub_customer_info_df, dim_us.dim_pub_sales_mgr_dept_df, dim_us.dim_pub_sales_rep_terr_df, dim_us.dim_pub_sales_territory_df, dw_us.dwd_disty_sales_report_goal_view, dw_us.dws_disty_brpt_pl_extend_mtd — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dws_disty_brpt_cust_mtd.md`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | INSERT OVERWRITE partition reload (per ETL SQL) |
| Schedule | Not documented in repository |
| Parameters | `country`, `date_flag`, `dt_month`, `etl_timestamp` |

---

## L2 Declarative Knowledge

### Business purpose
Customer-level B Report P&L and goals MTD serving table (cust + territory + sales hierarchy grain)

This Knowledgebase entry documents the Bitbucket ETL load script in `source/contracts/b-report-us/bitbicket_etl/`. Business semantics align with the B Report US contract catalog when present.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: PM, Sales, Buyer, BD and executive analysis views. |
| **Sales / PM / finance** | Shipped-order and margin metrics at documented grain (month-to-date cumulative through each date_flag). |
| **Data engineering** | Verified upstream/downstream objects with `file:line` evidence from ETL SQL. |

### Fact key resolution
- Order-line hub for B Report P&L: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` when debugging transaction-level metrics.
- This table grain: one row per (`date_flag`, `cust_no`, `mcust_no`, `cust_terr`, `cust_type`, `division`, `terr_sub_group`, `terr_group`, sales hierarchy IDs, `company_no`) with MTD-cumulative measures through `date_flag`..
- Label-on/off and order_type adjustments: see `source/contracts/b-report-us/metric-index.md`.

### Time field semantics
- **`date_flag`:** primary partition / filter for this load; value supplied by Azkaban `conf.get` parameters (see L4).
- **Period semantics:** month-to-date cumulative through each date_flag.


### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `bo_gm_amt` | `bo_gm_amt` | bo_gm_amt at mtd grain |
| P&L adjustment / measure | `bo_gross_cost` | `bo_gross_cost` | bo_gross_cost at mtd grain |
| P&L adjustment / measure | `bo_gross_sales` | `bo_gross_sales` | bo_gross_sales at mtd grain |
| P&L adjustment / measure | `btl_sales` | `btl_sales` | btl_sales at mtd grain |
| P&L adjustment / measure | `cust_finance_sales` | `cust_finance_sales` | cust_finance_sales at mtd grain |
| P&L adjustment / measure | `ds_cost` | `ds_cost` | ds_cost at mtd grain |
| P&L adjustment / measure | `ds_sales` | `ds_sales` | ds_sales at mtd grain |
| P&L adjustment / measure | `fx_cost` | `fx_cost` | fx_cost at mtd grain |
| Governed profitability | `gm_amt` | `gm_amt` | gm_amt at mtd grain |
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
| P&L adjustment / measure | `gross_cost` | `gross_cost` | gross_cost at mtd grain |
| Governed profitability | `gross_sales` | `gross_sales` | gross_sales at mtd grain |
| P&L adjustment / measure | `hc_sales` | `hc_sales` | hc_sales at mtd grain |
| P&L adjustment / measure | `inv_cost` | `inv_cost` | inv_cost at mtd grain |
| P&L adjustment / measure | `net_cost` | `net_cost` | net_cost at mtd grain |
| Governed profitability | `net_sales` | `net_sales` | net_sales at mtd grain |
| Governed profitability | `ngm_amt` | `ngm_amt` | ngm_amt at mtd grain |
| Governed profitability | `oplgm_amt` | `oplgm_amt` | oplgm_amt at mtd grain |
| Governed profitability | `oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at mtd grain |
| P&L adjustment / measure | `others_sales` | `others_sales` | others_sales at mtd grain |
| P&L adjustment / measure | `rr_cost` | `rr_cost` | rr_cost at mtd grain |
| Governed profitability | `rr_gm` | `gm_amt` | gm_amt at mtd grain |
| Governed profitability | `rr_ngm` | `ngm_amt` | ngm_amt at mtd grain |
| Governed profitability | `rr_opl` | `oplgm_amt` | oplgm_amt at mtd grain |
| Governed profitability | `rr_oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at mtd grain |
| Governed profitability | `rr_sales` | `net_sales` | net_sales at mtd grain |
| Governed profitability | `rr_tgm` | `tgm_amt` | tgm_amt at mtd grain |
| Governed profitability | `rr_total_btl` | `total_btl` | total_btl at mtd grain |
| P&L adjustment / measure | `scm_cost` | `scm_cost` | scm_cost at mtd grain |
| P&L adjustment / measure | `so_gm_amt` | `so_gm_amt` | so_gm_amt at mtd grain |
| P&L adjustment / measure | `so_gross_cost` | `so_gross_cost` | so_gross_cost at mtd grain |
| P&L adjustment / measure | `so_gross_sales` | `so_gross_sales` | so_gross_sales at mtd grain |
| P&L adjustment / measure | `stock_cost` | `stock_cost` | stock_cost at mtd grain |
| P&L adjustment / measure | `stock_sales` | `stock_sales` | stock_sales at mtd grain |
| Governed profitability | `tgm_amt` | `tgm_amt` | tgm_amt at mtd grain |
| Governed profitability | `total_btl` | `total_btl` | total_btl at mtd grain |
| P&L adjustment / measure | `trans_btl_sales` | `trans_btl_sales` | trans_btl_sales at mtd grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `bo_gm_amt` | mtd | `bo_gm_amt` | Not in metric-index.md |
| `bo_gross_cost` | mtd | `bo_gross_cost` | Not in metric-index.md |
| `bo_gross_sales` | mtd | `bo_gross_sales` | Not in metric-index.md |
| `btl_sales` | mtd | `btl_sales` | Not in metric-index.md |
| `cust_finance_sales` | mtd | `cust_finance_sales` | Not in metric-index.md |
| `ds_cost` | mtd | `ds_cost` | Not in metric-index.md |
| `ds_sales` | mtd | `ds_sales` | Not in metric-index.md |
| `fx_cost` | mtd | `fx_cost` | Not in metric-index.md |
| `gm_amt` | mtd | `gm_amt` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
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
| `gross_cost` | mtd | `gross_cost` | Not in metric-index.md |
| `gross_sales` | mtd | `gross_sales` | `source/contracts/b-report-us/metric-index.md#gross_sales` |
| `hc_sales` | mtd | `hc_sales` | Not in metric-index.md |
| `inv_cost` | mtd | `inv_cost` | Not in metric-index.md |
| `net_cost` | mtd | `net_cost` | Not in metric-index.md |
| `net_sales` | mtd | `net_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `ngm_amt` | mtd | `ngm_amt` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | mtd | `oplgm_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | mtd | `oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `others_sales` | mtd | `others_sales` | Not in metric-index.md |
| `rr_cost` | mtd | `rr_cost` | Not in metric-index.md |
| `gm_amt` | mtd | `rr_gm` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `ngm_amt` | mtd | `rr_ngm` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | mtd | `rr_opl` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | mtd | `rr_oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `net_sales` | mtd | `rr_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `tgm_amt` | mtd | `rr_tgm` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | mtd | `rr_total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `scm_cost` | mtd | `scm_cost` | Not in metric-index.md |
| `so_gm_amt` | mtd | `so_gm_amt` | Not in metric-index.md |
| `so_gross_cost` | mtd | `so_gross_cost` | Not in metric-index.md |
| `so_gross_sales` | mtd | `so_gross_sales` | Not in metric-index.md |
| `stock_cost` | mtd | `stock_cost` | Not in metric-index.md |
| `stock_sales` | mtd | `stock_sales` | Not in metric-index.md |
| `tgm_amt` | mtd | `tgm_amt` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | mtd | `total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `trans_btl_sales` | mtd | `trans_btl_sales` | Not in metric-index.md |

### etl_metrics

Formulas below are sourced from [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md) for logical metrics present on this table.
Index formulas are canonical: this enricher copies them into KB and never overwrites `final_effective_formula_sql` in the metric-index.

#### `gm_amt`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#gm_amt)
- **Business definition:** Core line gross margin before BTL/PDT and full NGM adjustment chain.
```sql
(nvl(u_price,0) - nvl(if(sales_cost is null, u_cost, sales_cost), 0)) * nvl(ship_qty,0)
```

#### `gross_sales`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#gross_sales)
- **Business definition:** Shipped quantity times unit price without sum expense.
```sql
nvl(ship_qty,0) * nvl(u_price,0)
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
**Business filters:** Use `date_flag` (or `month_no` for month-indexed DM tables) for reporting scope.
**Technical predicates (load only):** Partition predicate on INSERT OVERWRITE; see Key filters below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| (ETL join) | — | left join (select * from dim_${country}.dim_pub_sales_territory_df | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |

### Key filters and ETL business logic
- `date_flag = '${date_flag}'` — inferred from ETL WHERE clause
- Upstream P&L already reflects shipped-order scope from `dws_disty_brpt_pl_extend_mtd` (sourced from order-line fact with `dim_pub_order_type.sales = 'Y'`).
- Goal join: `goal_type = 'NORMAL'`, `period = month_no`, `cust_no <> 0`; full join preserves goal-only customers.
- Goal join intentionally omits `terr_sub_group` / `terr_group` on join keys to avoid duplicate rows from dirty goal data (ETL comment in script).
- `mcust_no` for goal rows comes from `dim_pub_customer_info_df`, not the goal table.
- Technical sync: `hive2vertica` uses `where date_flag = '${date_flag}'` only — not a business filter.

### Standard time-filter SQL
```sql
-- Reporting filter pattern (replace partition value from L4 trace)
SELECT *
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dim_us.dim_pub_customer_info_df, dim_us.dim_pub_sales_mgr_dept_df, dim_us.dim_pub_sales_rep_terr_df, dim_us.dim_pub_sales_territory_df).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dw_us.dws_disty_brpt_cust_mtd` partition `date_flag`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dw_us_dws_disty_brpt_cust_mtd["dw_us.dws_disty_brpt_cust_mtd"]
  src0["dim_us.dim_pub_customer_info_df"]
  src0 --> dw_us_dws_disty_brpt_cust_mtd
  src1["dim_us.dim_pub_sales_mgr_dept_df"]
  src1 --> dw_us_dws_disty_brpt_cust_mtd
  src2["dim_us.dim_pub_sales_rep_terr_df"]
  src2 --> dw_us_dws_disty_brpt_cust_mtd
  src3["dim_us.dim_pub_sales_territory_df"]
  src3 --> dw_us_dws_disty_brpt_cust_mtd
  src4["dw_us.dwd_disty_sales_report_goal_view"]
  src4 --> dw_us_dws_disty_brpt_cust_mtd
  src5["dw_us.dws_disty_brpt_pl_extend_mtd"]
  src5 --> dw_us_dws_disty_brpt_cust_mtd
  src6["dws_disty_brpt_cust_mtd.py"]
  src6 --> dw_us_dws_disty_brpt_cust_mtd
  src7["ods_us.ods_cis_corp_cust_type"]
  src7 --> dw_us_dws_disty_brpt_cust_mtd
  consumers["B Report dashboards / DM serving"]
  dw_us_dws_disty_brpt_cust_mtd --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_customer_info_df` | source |
| `dim_us.dim_pub_sales_mgr_dept_df` | source |
| `dim_us.dim_pub_sales_rep_terr_df` | source |
| `dim_us.dim_pub_sales_territory_df` | source |
| `dw_us.dwd_disty_sales_report_goal_view` | source |
| `dw_us.dws_disty_brpt_cust_mtd` | target |
| `dw_us.dws_disty_brpt_pl_extend_mtd` | source |
| `dws_disty_brpt_cust_mtd.py` | source |
| `ods_us.ods_cis_corp_cust_type` | source |
| `ods_us.ods_cis_corp_division` | source |
| `ods_us.ods_cis_corp_territory_group` | source |
| `ods_us.ods_cis_corp_territory_sub_group` | source |

### Step-by-step logic
#### Step 1 — CTE `table_goal`

**Source:** intermediate aggregation inside ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py`

#### Step 2 — CTE `table_dwd`

**Source:** intermediate aggregation inside ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py`

#### Step 3 — dimension and reference joins

**Join keys:** see Dimension join patterns table (parsed from ETL SQL).

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `month_no` | `${month_no}` | `month_no` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | partial | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:48` |
| `cust_no` | `coalesce(table_dwd.cust_no,table_goal.cust_no,-3)` | `cust_no` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:212` |
| `cust_name` | `table_customer.cust_name_replace` | `cust_name_replace` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:213` |
| `mcust_no` | `coalesce(table_dwd.mcust_no,table_customer.mcust_no,-3)` | `mcust_no` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:214` |
| `mcust_name` | `table_mcust.cust_name_replace` | `cust_name_replace` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:215` |
| `cust_terr` | `coalesce(table_dwd.cust_terr,table_goal.cust_terr,-3)` | `cust_terr` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:216` |
| `terr_name` | `table_terr.terr_name` | `terr_name` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:217` |
| `cust_type` | `coalesce(table_dwd.cust_type,table_goal.cust_type,-3)` | `cust_type` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:218` |
| `cust_type_desc` | `table_cust_type.cust_type_descr` | `cust_type_descr` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:219` |
| `division` | `coalesce(table_dwd.division,table_goal.division,-3)` | `division` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:220` |
| `division_desc` | `table_div.division_desc` | `division_desc` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:221` |
| `terr_sub_group` | `coalesce(table_dwd.terr_sub_group, table_terr.sub_group_id,-3)` | `terr_sub_group`, `sub_group_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:222` |
| `sub_group_desc` | `table_sub_group.sub_group_desc` | `sub_group_desc` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:223` |
| `terr_group` | `coalesce(table_dwd.terr_group,table_terr.group_id,-3)` | `terr_group`, `group_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:224` |
| `terr_group_desc` | `table_group.group_desc` | `group_desc` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:225` |
| `3` | `coalesce(table_dwd.sales_rep_id ,table1.sales_rep_id, -3)` | `sales_rep_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:178` |
| `3` | `coalesce(table_dwd.sales_sup_id ,table2.manager_id, -3)` | `sales_sup_id`, `manager_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:178` |
| `3` | `coalesce(table_dwd.sales_mgr_id ,table3.manager_id, -3)` | `sales_mgr_id`, `manager_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:178` |
| `3` | `coalesce(table_dwd.sales_dir_id ,table4.manager_id, -3)` | `sales_dir_id`, `manager_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:178` |
| `3` | `coalesce(table_dwd.sales_vp_id ,table5.manager_id, 3)` | `sales_vp_id`, `manager_id` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:178` |
| `company_no` | `coalesce(table_dwd.company_no,table_goal.company_no)` | `company_no` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:231` |
| `0` | `nvl(table_dwd.gross_sales,0)` | `gross_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:233` |
| `0` | `nvl(table_dwd.net_sales,0)` | `net_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:234` |
| `0` | `nvl(table_dwd.gross_cost,0)` | `gross_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:235` |
| `0` | `nvl(table_dwd.net_cost,0)` | `net_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:236` |
| `0` | `nvl(table_dwd.scm_usage,0)` | `scm_usage` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:237` |
| `0` | `nvl(table_dwd.ds_sales,0)` | `ds_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:238` |
| `0` | `nvl(table_dwd.stock_sales,0)` | `stock_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:239` |
| `0` | `nvl(table_dwd.ds_cost,0)` | `ds_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:240` |
| `0` | `nvl(table_dwd.stock_cost,0)` | `stock_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:241` |
| `0` | `nvl(table_dwd.ds_scm_usage,0)` | `ds_scm_usage` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:242` |
| `0` | `nvl(table_dwd.stock_scm_usage,0)` | `stock_scm_usage` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:243` |
| `0` | `nvl(table_dwd.total_unit,0)` | `total_unit` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:244` |
| `0` | `nvl(table_dwd.total_weight,0)` | `total_weight` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:245` |
| `0` | `nvl(table_dwd.net_income,0)` | `net_income` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:247` |
| `0` | `nvl(table_dwd.invest_capital,0)` | `invest_capital` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:248` |
| `0` | `nvl(table_dwd.cgp,0)` | `cgp` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:250` |
| `0` | `nvl(table_dwd.total_btl,0)` | `total_btl` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:251` |
| `0` | `nvl(table_dwd.tgm_amt,0)` | `tgm_amt` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:252` |
| `0` | `nvl(table_dwd.gm_amt,0)` | `gm_amt` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:253` |
| `0` | `nvl(table_dwd.ngm_amt,0)` | `ngm_amt` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:254` |
| `0` | `nvl(table_dwd.oplgm_amt,0)` | `oplgm_amt` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:255` |
| `0` | `nvl(table_dwd.bo_gross_sales,0)` | `bo_gross_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:257` |
| `0` | `nvl(table_dwd.bo_gross_cost,0)` | `bo_gross_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:258` |
| `0` | `nvl(table_dwd.bo_total_unit,0)` | `bo_total_unit` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:259` |
| `0` | `nvl(table_dwd.bo_gm_amt,0)` | `bo_gm_amt` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:260` |
| `0` | `nvl(table_dwd.so_gross_sales,0)` | `so_gross_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:261` |
| `0` | `nvl(table_dwd.so_gross_cost,0)` | `so_gross_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:262` |
| `0` | `nvl(table_dwd.so_total_unit,0)` | `so_total_unit` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:263` |
| `0` | `nvl(table_dwd.so_gm_amt,0)` | `so_gm_amt` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:264` |
| `0` | `nvl(table_dwd.bo_age0_7,0)` | `bo_age0_7` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:265` |
| `0` | `nvl(table_dwd.bo_age8_14,0)` | `bo_age8_14` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:266` |
| `0` | `nvl(table_dwd.bo_age15_21,0)` | `bo_age15_21` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:267` |
| `0` | `nvl(table_dwd.bo_age21_up,0)` | `bo_age21_up` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:268` |
| `0` | `nvl(table_dwd.so_age0_7,0)` | `so_age0_7` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:269` |
| `0` | `nvl(table_dwd.so_age8_14,0)` | `so_age8_14` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:270` |
| `0` | `nvl(table_dwd.so_age15_21,0)` | `so_age15_21` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:271` |
| `0` | `nvl(table_dwd.so_age21_up,0)` | `so_age21_up` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:272` |
| `0` | `nvl(table_dwd.rr_unit,0)` | `rr_unit` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:274` |
| `0` | `nvl(table_dwd.rr_sales,0)` | `rr_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:275` |
| `0` | `nvl(table_dwd.rr_cost,0)` | `rr_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:276` |
| `0` | `nvl(table_dwd.rr_gm,0)` | `rr_gm` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:277` |
| `0` | `nvl(table_dwd.rr_ngm,0)` | `rr_ngm` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:278` |
| `0` | `nvl(table_dwd.rr_opl,0)` | `rr_opl` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:279` |
| `0` | `nvl(table_dwd.rr_cgp,0)` | `rr_cgp` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:280` |
| `0` | `nvl(table_dwd.rr_total_btl,0)` | `rr_total_btl` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:281` |
| `0` | `nvl(table_dwd.rr_tgm,0)` | `rr_tgm` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:282` |
| `0` | `nvl(table_dwd.ap_finance,0)` | `ap_finance` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:284` |
| `0` | `nvl(table_dwd.inv_cost,0)` | `inv_cost` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:285` |
| `0` | `nvl(table_dwd.inv_reserve,0)` | `inv_reserve` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:286` |
| `0` | `nvl(table_dwd.cr_risk_cterm,0)` | `cr_risk_cterm` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:287` |
| `0` | `nvl(table_dwd.flr_synnex,0)` | `flr_synnex` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:288` |
| `0` | `nvl(table_dwd.direct_credit,0)` | `direct_credit` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:289` |
| `0` | `nvl(table_dwd.csgn_edi_fee,0)` | `csgn_edi_fee` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:290` |
| `0` | `nvl(table_dwd.corporate,0)` | `corporate` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:291` |
| `0` | `nvl(table_dwd.sfs,0)` | `sfs` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:292` |
| `0` | `nvl(table_dwd.scm_risk,0)` | `scm_risk` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:293` |
| `0` | `nvl(table_dwd.flr_vendor,0)` | `flr_vendor` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:294` |
| `0` | `nvl(table_dwd.cust_finance_sales,0)` | `cust_finance_sales` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:295` |
| `0` | `nvl(table_dwd.cust_pmt_disc,0)` | `cust_pmt_disc` | `table_dwd`, `table_goal`, `dim_${country}.dim_pub_customer_info_df`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `ods_${country}.ods_cis_corp_territory_sub_group`, `ods_${country}.ods_cis_corp_territory_group` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:296` |

_Showing 80 of 144 columns; full list in L3 `*_column_derivations.json` sidecar._

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| `-3` | business_filter | Coalesce fallback for unmatched hierarchy keys (inferred from ETL SQL) |
| `goal_type = 'NORMAL'` | business_filter | Sales goal filter when goal view is joined |

---

## L4 Validation

### Resolved partition value
| Step | Source | How `date_flag` is determined |
|------|--------|-----------------------------------------------------|
| 1 | `conf.get('date_flag')` | Business process date (comment: yesterday / @process_date) — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:11` |
| 3 | `conf.get('dt_month')` | Hive partition key `dt_month` (yyyy-MM derived from date_flag) — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:20` |

**Plain language:** The ETL wrapper reads Azkaban-injected `conf` parameters; `date_flag` is the business processing date, and `dt_month` / `month_no` derive month scope for partitioned loads. Downstream reporting must use the same resolved period as the load partition.

### Data quality checks
- Verify row counts and `date_flag` coverage after each monthly close (compare Hive vs Vertica tail dates).
- Check `cust_no` / `mcust_no` match rates against `dim_us.dim_pub_customer_info` on sample `date_flag`.
- Monitor null or sentinel `-3` rates on hierarchy keys (`sales_rep_id`, `terr_sub_group`) after dimension snapshot joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).
- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT one, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY one
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT one, row, per, date_flag, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY one, row, per, date_flag
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- ETL SQL is authoritative for load-time joins; contract catalog is authoritative for column business definitions.
- US schema `dw_us` documented as baseline; other countries use same table names with regional `country` parameter.
- Comb_mtd and multi-period tables require correct period column selection (see L2 Metric serving map).

### Conflicts and open questions
- hive2vertica sync job `file:line` evidence: Not documented in repository (Bitbucket ETL snapshot only).
- Schedule, owner, SLA: Not documented in repository.

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dw_us.dws_disty_brpt_cust_mtd` | `dw_us.dws_disty_brpt_cust_mtd` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` | yes |
| **Hive alternative** | `dw_us.dws_disty_brpt_cust_mtd` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dw_us.dws_disty_brpt_cust_mtd` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` | — |

### Access constraints
- Standard `dw_us` / `dm_us` / `dim_us` role-based access applies.
- Country parameter `${country}` in ETL resolves schema prefix at runtime.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes |
| scan_risk_tier | high |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Consumer | Use case |
|----------|----------|
| Consumers: PM, Sales, Buyer, BD and executive analysis views. | B Report profitability and operating performance |
| Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards. | B Report profitability and operating performance |

### Representative query patterns
```sql
SELECT date_flag, SUM(net_sales) AS net_sales, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_customer_info_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `dim_us.dim_pub_sales_mgr_dept_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `dim_us.dim_pub_sales_rep_terr_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `dim_us.dim_pub_sales_territory_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `dw_us.dwd_disty_sales_report_goal_view` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `dw_us.dws_disty_brpt_pl_extend_mtd` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `dws_disty_brpt_cust_mtd.py` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `ods_us.ods_cis_corp_cust_type` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `ods_us.ods_cis_corp_division` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `ods_us.ods_cis_corp_territory_group` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |
| `ods_us.ods_cis_corp_territory_sub_group` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dws_disty_brpt_cust_mtd.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py:209`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dws_disty_brpt_cust_mtd.py` — primary Bitbucket ETL for `dws_disty_brpt_cust_mtd` — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_mtd/Customer/python/dws_disty_brpt_cust_mtd.py` with B Report contract enrichment when available.*
