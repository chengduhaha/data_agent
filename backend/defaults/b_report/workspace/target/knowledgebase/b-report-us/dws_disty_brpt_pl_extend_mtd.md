# DWS: B Report profitability serving aggregation (mtd) by business slice (`dw_us.dws_disty_brpt_pl_extend_mtd`)

- artifact_type: etl_table
- artifact_id: dw_us.dws_disty_brpt_pl_extend_mtd
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (mtd) by business slice
- layer_type: DWS
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py
- knowledgebase_path: target/knowledgebase/b-report-us/dws_disty_brpt_pl_extend_mtd.md
- contract_source: source/contracts/b-report-us/tables/dws_disty_brpt_pl_extend_mtd.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dws_disty_brpt_pl_extend_mtd`
- **Layer type:** DWS
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** month-to-date cumulative through each date_flag
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `month_no` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `cust_no`, `mcust_no`, `sales_rep_id`, `sales_sup_id`, `sales_mgr_id`, `sales_dir_id`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country}.dws_disty_brpt_pl_extend_mtd` | ETL target in Bitbucket script |
| Vertica | yes | `dw_us.dws_disty_brpt_pl_extend_mtd` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dws_disty_brpt_pl_extend_mtd` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dw_us_dws_disty_brpt_pl_extend_mtd.json` |
| **column_count** | 156 |
| **partition_keys** | `month_no` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dws_disty_brpt_pl_extend_mtd schema" --intent find_table_schema` |

### Lineage
- **upstream:** dim_us.dim_pub_sales_mgr_dept_df, dim_us.dim_pub_sales_rep_terr_df, dim_us.dim_pub_sales_territory_df, dw_us.dws_disty_brpt_bo_aging_df, git.synnex.org, marvin.ma_tdsynnex.com — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dws_disty_brpt_pl_extend_mtd.md`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | INSERT OVERWRITE partition reload (per ETL SQL) |
| Schedule | Not documented in repository |
| Parameters | `country`, `date_flag`, `dt_month`, `etl_timestamp`, `flow_run_type` |

---

## L2 Declarative Knowledge

### Business purpose
B Report profitability serving aggregation (mtd) by business slice

This Knowledgebase entry documents the Bitbucket ETL load script in `source/contracts/b-report-us/bitbicket_etl/`. Business semantics align with the B Report US contract catalog when present.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: PM, Sales, Buyer, BD and executive analysis views. |
| **Sales / PM / finance** | Shipped-order and margin metrics at documented grain (month-to-date cumulative through each date_flag). |
| **Data engineering** | Verified upstream/downstream objects with `file:line` evidence from ETL SQL. |

### Fact key resolution
- Order-line hub for B Report P&L: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` when debugging transaction-level metrics.
- This table grain: month-to-date cumulative through each date_flag.
- Label-on/off and order_type adjustments: see `source/contracts/b-report-us/metric-index.md`.

### Time field semantics
- **`month_no`:** primary partition / filter for this load; value supplied by Azkaban `conf.get` parameters (see L4).
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
| P&L adjustment / measure | `p91_cost` | `p91_cost` | p91_cost at mtd grain |
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
| `p91_cost` | mtd | `p91_cost` | Not in metric-index.md |
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
**Business filters:** Use `month_no` (or `month_no` for month-indexed DM tables) for reporting scope.
**Technical predicates (load only):** Partition predicate on INSERT OVERWRITE; see Key filters below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| (ETL join) | — | full join (select -- | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| (ETL join) | — | left join (select * from ods_${country}.ods_etl_dw_vend_pl_df | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| (ETL join) | — | left join (select * from dim_${country}.dim_pub_sales_territory_df | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| (ETL join) | — | left join (select * from temp_cust_xref_company | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| (ETL join) | — | left join (select * from ods_${country}.ods_etl_dw_vend_pl_df | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |

### Key filters and ETL business logic
- `date_flag = '${date_flag}'` — inferred from ETL WHERE clause
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
FROM dw_us.dws_disty_brpt_pl_extend_mtd
WHERE month_no = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dim_us.dim_pub_sales_mgr_dept_df, dim_us.dim_pub_sales_rep_terr_df, dim_us.dim_pub_sales_territory_df, dw_us.dws_disty_brpt_bo_aging_df).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dw_us.dws_disty_brpt_pl_extend_mtd` partition `month_no`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dw_us_dws_disty_brpt_pl_extend_mtd["dw_us.dws_disty_brpt_pl_extend_mtd"]
  src0["dim_us.dim_pub_sales_mgr_dept_df"]
  src0 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src1["dim_us.dim_pub_sales_rep_terr_df"]
  src1 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src2["dim_us.dim_pub_sales_territory_df"]
  src2 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src3["dw_us.dws_disty_brpt_bo_aging_df"]
  src3 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src4["git.synnex.org"]
  src4 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src5["marvin.ma_tdsynnex.com"]
  src5 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src6["ods_us.ods_breport_mydaas_breport_parameter"]
  src6 --> dw_us_dws_disty_brpt_pl_extend_mtd
  src7["ods_us.ods_cis_corp_cust_type"]
  src7 --> dw_us_dws_disty_brpt_pl_extend_mtd
  consumers["B Report dashboards / DM serving"]
  dw_us_dws_disty_brpt_pl_extend_mtd --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_sales_mgr_dept_df` | source |
| `dim_us.dim_pub_sales_rep_terr_df` | source |
| `dim_us.dim_pub_sales_territory_df` | source |
| `dw_us.dws_disty_brpt_bo_aging_df` | source |
| `dw_us.dws_disty_brpt_pl_extend_mtd` | target |
| `git.synnex.org` | source |
| `marvin.ma_tdsynnex.com` | source |
| `ods_us.ods_breport_mydaas_breport_parameter` | source |
| `ods_us.ods_cis_corp_cust_type` | source |
| `ods_us.ods_cis_corp_division` | source |
| `ods_us.ods_cis_corp_parameters` | source |
| `ods_us.ods_cis_corp_pl_code` | source |
| `ods_us.ods_cis_corp_vendor_segment` | source |
| `ods_us.ods_etl_cust_xref_all_df` | source |
| `ods_us.ods_etl_dw_vend_pl_df` | source |
| `ods_us.ods_etl_pm_vpc_matrix_df` | source |
| `os.path` | source |
| `python.path` | source |
| `script.deps` | source |
| `sys.path` | source |

### Step-by-step logic
#### Step 1 — CTE `table_tmp`

**Source:** intermediate aggregation inside ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py`

#### Step 2 — CTE `table_dwd`

**Source:** intermediate aggregation inside ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py`

#### Step 3 — dimension and reference joins

**Join keys:** see Dimension join patterns table (parsed from ETL SQL).

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `month_no` | `${month_no}` | `month_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | partial | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:339` |
| `cust_no` | `nvl(table_dwd.cust_no,table_aging.cust_no)` | `cust_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:341` |
| `cust_name_replace` | `table_customer.cust_name_replace` | `cust_name_replace` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:342` |
| `mcust_no` | `coalesce(cxc.cust_no, dbp.icode1, cx.xref_no, table_customer.mcust_no)` | `cust_no`, `icode1`, `xref_no`, `mcust_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:343` |
| `mcust_name` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `cust_terr` | `nvl(table_dwd.cust_terr,table_aging.cust_terr)` | `cust_terr` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:345` |
| `terr_name` | `table_terr.terr_name` | `terr_name` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:346` |
| `cust_type` | `nvl(table_dwd.cust_type,table_aging.cust_type)` | `cust_type` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:347` |
| `cust_type_desc` | `table_cust_type.cust_type_descr` | `cust_type_descr` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:348` |
| `division` | `table_cust_type.division` | `division` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:349` |
| `division_desc` | `table_div.division_desc` | `division_desc` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:350` |
| `terr_sub_group` | `table_terr.sub_group_id` | `sub_group_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:351` |
| `terr_sub_group_desc` | `table_terr.sub_group_desc` | `sub_group_desc` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:352` |
| `terr_group` | `table_terr.group_id` | `group_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:353` |
| `terr_group_desc` | `table_terr.group_desc` | `group_desc` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:354` |
| `sales_rep_id` | `nvl(table1.sales_rep_id,-3)` | `sales_rep_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:356` |
| `sales_sup_id` | `nvl(table2.manager_id, -3)` | `manager_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:203` |
| `sales_mgr_id` | `nvl(table3.manager_id, -3)` | `manager_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:203` |
| `sales_dir_id` | `nvl(table4.manager_id, -3)` | `manager_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:203` |
| `sales_vp_id` | `nvl(table5.manager_id, -3)` | `manager_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:203` |
| `sku_no` | `coalesce(table_dwd.sku_no,table_aging.sku_no)` | `sku_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:362` |
| `part_no` | `table_part.part_no` | `part_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:363` |
| `mfg_partno` | `table_part.mfg_partno` | `mfg_partno` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:364` |
| `vpl_no` | `case when coalesce(table_dwd.sku_no,table_aging.sku_no) >=0 then nvl(table_part_vpl.alt_vpl_no,table_part.vpl_no) whe...` | `sku_no`, `alt_vpl_no`, `vpl_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:365` |
| `vpl_code` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `vpc_group_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `vpc_group_desc` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `vend_no` | `case when coalesce(table_dwd.sku_no,table_aging.sku_no) >=0 then nvl(table_part_vpl.alt_vend_no,table_part_vpl.vend_n...` | `sku_no`, `alt_vend_no`, `vend_no`, `vpl_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:365` |
| `vend_name` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `master_vend_no` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `master_vend_name` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `group_id` | `table_part.group_id` | `group_id` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:385` |
| `seg_code` | `nullif(table_part_vpl2.alt_seg_code, '')` | `nullif`, `alt_seg_code` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | udf | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:386` |
| `pm_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `pm_mgr_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `pm_dir_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `pm_vp_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `buyer_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `buyer_mgr_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `buyer_dir_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `buyer_vp_id` | `null` | — | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:344` |
| `company_no` | `coalesce(table_dwd.company_no,table_aging.company_no)` | `company_no` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:398` |
| `gross_sales` | `sum( nvl(ship_qty,0) * nvl(u_price,0) )` | `ship_qty`, `u_price` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:222` |
| `net_sales` | `sum( net_sales )` | `net_sales` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:223` |
| `gross_cost` | `sum( nvl(ship_qty,0) * coalesce(sales_cost,u_cost,0) )` | `ship_qty`, `sales_cost`, `u_cost` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:224` |
| `net_cost` | `sum( net_cost )` | `net_cost` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:225` |
| `scm_usage` | `sum( nvl(ship_qty,0) * nvl(u_sum_expense,0) )` | `ship_qty`, `u_sum_expense` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:226` |
| `ds_cost` | `sum(case when from_loc_no = 98 and inv_type in (100,200) then nvl(ship_qty,0) * coalesce(sales_cost,u_cost,0) else 0 ...` | `from_loc_no`, `inv_type`, `ship_qty`, `sales_cost`, `u_cost` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:227` |
| `stock_cost` | `sum(case when from_loc_no != 98 and inv_type not in (100,200) then nvl(ship_qty,0) * coalesce(sales_cost,u_cost,0) el...` | `from_loc_no`, `inv_type`, `ship_qty`, `sales_cost`, `u_cost` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:228` |
| `ds_sales` | `sum(case when from_loc_no = 98 and inv_type in (100,200) then nvl(ship_qty,0) * nvl(u_price,0) else 0 end)` | `from_loc_no`, `inv_type`, `ship_qty`, `u_price` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:227` |
| `stock_sales` | `sum(case when from_loc_no != 98 and inv_type not in (100,200) then nvl(ship_qty,0) * nvl(u_price,0) else 0 end)` | `from_loc_no`, `inv_type`, `ship_qty`, `u_price` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:228` |
| `ds_scm_usage` | `sum(case when from_loc_no = 98 and inv_type in (100,200) then nvl(ship_qty,0) * nvl(u_sum_expense,0) else 0 end)` | `from_loc_no`, `inv_type`, `ship_qty`, `u_sum_expense` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:227` |
| `stock_scm_usage` | `sum(case when from_loc_no != 98 and inv_type not in (100,200) then nvl(ship_qty,0) * nvl(u_sum_expense,0) else 0 end)` | `from_loc_no`, `inv_type`, `ship_qty`, `u_sum_expense` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:228` |
| `total_unit` | `sum(case when order_type = 114 then 0 else nvl(ship_qty,0) end )` | `order_type`, `ship_qty` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:233` |
| `total_weight` | `sum( nvl(ship_qty,0) * nvl(l_weight,0) )` | `ship_qty`, `l_weight` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:234` |
| `net_income` | `sum( (nvl(ngm_amt, 0) + nvl( ${fin_cost_rate} * ${total_nsales} * ( nvl(cust_finance, 0) + nvl(ar_fin_recovery, 0) + ...` | `ngm_amt`, `fin_cost_rate`, `total_nsales`, `cust_finance`, `ar_fin_recovery`, `inv_cost`, `ap_finance`, `scm_cost`, `total_fin_cost`, `gap_rate`, `u_price`, `u_sum_expense`, `ship_qty`, `after_tax_rate`, `days` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:203` |
| `invest_capital` | `sum( nvl(CUST_FINANCE / nvl(${cfin}, 0), 0) + nvl(AR_FIN_RECOVERY / nvl(${cfin}, 0), 0) + nvl(INV_COST / nvl(${invc},...` | `CUST_FINANCE`, `cfin`, `AR_FIN_RECOVERY`, `INV_COST`, `invc`, `AP_FINANCE`, `apfi`, `SCM_COST`, `scma`, `total_unvouch`, `total_ap_finance`, `total_intran_inv`, `total_inv_cost`, `emi`, `total_nsales`, `u_price`, `u_sum_expense`, `ship_qty`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:246` |
| `cgp` | `sum( cgp )` | `cgp` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:257` |
| `total_btl` | `sum( total_btl )` | `total_btl` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:258` |
| `tgm_amt` | `sum( tgm_amt )` | `tgm_amt` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:259` |
| `gm_amt` | `sum( gm_amt )` | `gm_amt` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:260` |
| `ngm_amt` | `sum( nvl(ngm_amt,0) )` | `ngm_amt` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:261` |
| `oplgm_amt` | `sum( nvl(oplgm_amt,0) )` | `oplgm_amt` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:262` |
| `rr_unit` | `sum(nvl(ship_qty,0)) * ${days_m} / ${days_mtd}` | `ship_qty`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:265` |
| `rr_sales` | `( sum(if(order_type <> 125, net_sales, 0)) * ${days_m} / ${days_mtd} + sum(if(order_type = 125, net_sales, 0)) )` | `order_type`, `net_sales`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:266` |
| `rr_cost` | `sum(net_cost) * ${days_m} / ${days_mtd}` | `net_cost`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:268` |
| `rr_gm` | `sum(gm_amt) * ${days_m} / ${days_mtd}` | `gm_amt`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:269` |
| `rr_ngm` | `sum(nvl(ngm_amt,0)) * ${days_m} / ${days_mtd}` | `ngm_amt`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:270` |
| `rr_opl` | `sum(nvl(oplgm_amt,0)) * ${days_m} / ${days_mtd}` | `oplgm_amt`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:271` |
| `rr_cgp` | `sum(cgp) * ${days_m} / ${days_mtd}` | `cgp`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:272` |
| `rr_total_btl` | `sum(total_btl) * ${days_m} / ${days_mtd}` | `total_btl`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:273` |
| `rr_tgm` | `sum(tgm_amt) * ${days_m} / ${days_mtd}` | `tgm_amt`, `days_m`, `days_mtd` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:274` |
| `ap_finance` | `sum( nvl(ap_finance,0) )` | `ap_finance` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:277` |
| `inv_cost` | `sum( nvl(inv_cost,0) )` | `inv_cost` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:278` |
| `inv_reserve` | `sum( nvl(inv_reserve,0) )` | `inv_reserve` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:279` |
| `cr_risk_cterm` | `sum( nvl(cr_risk_cterm,0) )` | `cr_risk_cterm` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:280` |
| `flr_synnex` | `sum( nvl(flr_synnex,0) )` | `flr_synnex` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:281` |
| `direct_credit` | `sum( nvl(direct_credit,0) )` | `direct_credit` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:282` |
| `csgn_edi_fee` | `sum( nvl(csgn_edi_fee,0) )` | `csgn_edi_fee` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:283` |
| `corporate` | `sum( nvl(corporate,0) )` | `corporate` | `table_dwd`, `dw_${country}.dws_disty_brpt_bo_aging_df`, `${dim_pub_part_info}`, `${dim_pub_vpl_info}`, `ods_${country}.ods_etl_dw_vend_pl_df`, `${dim_pub_customer_info}`, `ods_${country}.ods_cis_corp_cust_type`, `ods_${country}.ods_cis_corp_division`, `dim_${country}.dim_pub_sales_territory_df`, `dim_${country}.dim_pub_sales_rep_terr_df`, `dim_${country}.dim_pub_sales_mgr_dept_df`, `temp_mcust_no_clean` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:284` |

_Showing 80 of 155 columns; full list in L3 `*_column_derivations.json` sidecar._

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
| 1 | `conf.get('date_flag')` | Business process date (comment: yesterday / @process_date) — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:13` |
| 3 | `conf.get('dt_month')` | Hive partition key `dt_month` (yyyy-MM derived from date_flag) — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:53` |

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
FROM dw_us.dws_disty_brpt_pl_extend_mtd
WHERE month_no = '${partition_value}'
GROUP BY month_no;

-- 2) Metric sum by business dimension (top N)
SELECT cust_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_pl_extend_mtd
WHERE month_no = '${partition_value}'
GROUP BY cust_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT cust_no, mcust_no, sales_rep_id, month_no, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_pl_extend_mtd
WHERE month_no = '${partition_value}'
GROUP BY cust_no, mcust_no, sales_rep_id, month_no
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
| **Query for reporting** | `dw_us.dws_disty_brpt_pl_extend_mtd` | `dw_us.dws_disty_brpt_pl_extend_mtd` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` | yes |
| **Hive alternative** | `dw_us.dws_disty_brpt_pl_extend_mtd` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dw_us.dws_disty_brpt_pl_extend_mtd` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` | — |

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
SELECT month_no, SUM(net_sales) AS net_sales, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dws_disty_brpt_pl_extend_mtd
WHERE month_no = '${partition_value}'
GROUP BY month_no;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_sales_mgr_dept_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `dim_us.dim_pub_sales_rep_terr_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `dim_us.dim_pub_sales_territory_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `dw_us.dws_disty_brpt_bo_aging_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `git.synnex.org` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `marvin.ma_tdsynnex.com` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_breport_mydaas_breport_parameter` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_cis_corp_cust_type` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_cis_corp_division` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_cis_corp_parameters` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_cis_corp_pl_code` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_cis_corp_vendor_segment` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_etl_cust_xref_all_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_etl_dw_vend_pl_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |
| `ods_us.ods_etl_pm_vpc_matrix_df` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dws_disty_brpt_pl_extend_mtd.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py:337`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dws_disty_brpt_pl_extend_mtd.py` — primary Bitbucket ETL for `dws_disty_brpt_pl_extend_mtd` — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_mtd/Common/python/dws_disty_brpt_pl_extend_mtd.py` with B Report contract enrichment when available.*
