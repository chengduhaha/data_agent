# DWS: B Report profitability serving aggregation (wtd) by business slice (`dw_us.dws_disty_brpt_bd_vpl_wtd`)

- artifact_type: etl_table
- artifact_id: dw_us.dws_disty_brpt_bd_vpl_wtd
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (wtd) by business slice
- layer_type: DWS
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py
- knowledgebase_path: target/knowledgebase/b-report-us/dws_disty_brpt_bd_vpl_wtd.md
- contract_source: source/contracts/b-report-us/tables/dws_disty_brpt_bd_vpl_wtd.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dws_disty_brpt_bd_vpl_wtd`
- **Layer type:** DWS
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** week-to-date cumulative through each date_flag
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `date_flag` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `week_no`, `project_no`, `task_no`, `company_no`, `vpl_no`, `vpc_group_id`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country}.dws_disty_brpt_bd_vpl_wtd` | ETL target in Bitbucket script |
| Vertica | yes | `dw_us.dws_disty_brpt_bd_vpl_wtd` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dws_disty_brpt_bd_vpl_wtd` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dw_us_dws_disty_brpt_bd_vpl_wtd.json` |
| **column_count** | 118 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dws_disty_brpt_bd_vpl_wtd schema" --intent find_table_schema` |

### Lineage
- **upstream:** dim_us.dim_pub_date, dw_us.dws_disty_brpt_bd_vpl_1d — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dws_disty_brpt_bd_vpl_wtd.md`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | INSERT OVERWRITE partition reload (per ETL SQL) |
| Schedule | Not documented in repository |
| Parameters | country, date_flag |

---

## L2 Declarative Knowledge

### Business purpose
B Report profitability serving aggregation (wtd) by business slice

This Knowledgebase entry documents the Bitbucket ETL load script in `source/contracts/b-report-us/bitbicket_etl/`. Business semantics align with the B Report US contract catalog when present.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: PM, Sales, Buyer, BD and executive analysis views. |
| **Sales / PM / finance** | Shipped-order and margin metrics at documented grain (week-to-date cumulative). |
| **Data engineering** | Verified upstream/downstream objects with `file:line` evidence from ETL SQL. |

### Fact key resolution
- Order-line hub for B Report P&L: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` when debugging transaction-level metrics.
- This table grain: week-to-date cumulative through each date_flag.
- Label-on/off and order_type adjustments: see `source/contracts/b-report-us/metric-index.md`.

### Time field semantics
- **`date_flag`:** primary partition / filter for this load; value supplied by Azkaban `conf.get` parameters (see L4).
- **Period semantics:** week-to-date cumulative.


### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `bo_gm_amt` | `bo_gm_amt` | bo_gm_amt at wtd grain |
| P&L adjustment / measure | `bo_gross_cost` | `bo_gross_cost` | bo_gross_cost at wtd grain |
| P&L adjustment / measure | `bo_gross_sales` | `bo_gross_sales` | bo_gross_sales at wtd grain |
| P&L adjustment / measure | `btl_sales` | `btl_sales` | btl_sales at wtd grain |
| P&L adjustment / measure | `cust_finance_sales` | `cust_finance_sales` | cust_finance_sales at wtd grain |
| P&L adjustment / measure | `ds_cost` | `ds_cost` | ds_cost at wtd grain |
| P&L adjustment / measure | `ds_sales` | `ds_sales` | ds_sales at wtd grain |
| P&L adjustment / measure | `fx_cost` | `fx_cost` | fx_cost at wtd grain |
| Governed profitability | `gm_amt` | `gm_amt` | gm_amt at wtd grain |
| P&L adjustment / measure | `gross_cost` | `gross_cost` | gross_cost at wtd grain |
| Governed profitability | `gross_sales` | `gross_sales` | gross_sales at wtd grain |
| P&L adjustment / measure | `hc_sales` | `hc_sales` | hc_sales at wtd grain |
| P&L adjustment / measure | `inv_cost` | `inv_cost` | inv_cost at wtd grain |
| P&L adjustment / measure | `net_cost` | `net_cost` | net_cost at wtd grain |
| Governed profitability | `net_sales` | `net_sales` | net_sales at wtd grain |
| Governed profitability | `ngm_amt` | `ngm_amt` | ngm_amt at wtd grain |
| Governed profitability | `oplgm_amt` | `oplgm_amt` | oplgm_amt at wtd grain |
| Governed profitability | `oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at wtd grain |
| P&L adjustment / measure | `others_sales` | `others_sales` | others_sales at wtd grain |
| P&L adjustment / measure | `scm_cost` | `scm_cost` | scm_cost at wtd grain |
| P&L adjustment / measure | `so_gm_amt` | `so_gm_amt` | so_gm_amt at wtd grain |
| P&L adjustment / measure | `so_gross_cost` | `so_gross_cost` | so_gross_cost at wtd grain |
| P&L adjustment / measure | `so_gross_sales` | `so_gross_sales` | so_gross_sales at wtd grain |
| P&L adjustment / measure | `stock_cost` | `stock_cost` | stock_cost at wtd grain |
| P&L adjustment / measure | `stock_sales` | `stock_sales` | stock_sales at wtd grain |
| Governed profitability | `tgm_amt` | `tgm_amt` | tgm_amt at wtd grain |
| Governed profitability | `total_btl` | `total_btl` | total_btl at wtd grain |
| P&L adjustment / measure | `trans_btl_sales` | `trans_btl_sales` | trans_btl_sales at wtd grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `bo_gm_amt` | wtd | `bo_gm_amt` | Not in metric-index.md |
| `bo_gross_cost` | wtd | `bo_gross_cost` | Not in metric-index.md |
| `bo_gross_sales` | wtd | `bo_gross_sales` | Not in metric-index.md |
| `btl_sales` | wtd | `btl_sales` | Not in metric-index.md |
| `cust_finance_sales` | wtd | `cust_finance_sales` | Not in metric-index.md |
| `ds_cost` | wtd | `ds_cost` | Not in metric-index.md |
| `ds_sales` | wtd | `ds_sales` | Not in metric-index.md |
| `fx_cost` | wtd | `fx_cost` | Not in metric-index.md |
| `gm_amt` | wtd | `gm_amt` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `gross_cost` | wtd | `gross_cost` | Not in metric-index.md |
| `gross_sales` | wtd | `gross_sales` | `source/contracts/b-report-us/metric-index.md#gross_sales` |
| `hc_sales` | wtd | `hc_sales` | Not in metric-index.md |
| `inv_cost` | wtd | `inv_cost` | Not in metric-index.md |
| `net_cost` | wtd | `net_cost` | Not in metric-index.md |
| `net_sales` | wtd | `net_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `ngm_amt` | wtd | `ngm_amt` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oplgm_amt` | wtd | `oplgm_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | wtd | `oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `others_sales` | wtd | `others_sales` | Not in metric-index.md |
| `scm_cost` | wtd | `scm_cost` | Not in metric-index.md |
| `so_gm_amt` | wtd | `so_gm_amt` | Not in metric-index.md |
| `so_gross_cost` | wtd | `so_gross_cost` | Not in metric-index.md |
| `so_gross_sales` | wtd | `so_gross_sales` | Not in metric-index.md |
| `stock_cost` | wtd | `stock_cost` | Not in metric-index.md |
| `stock_sales` | wtd | `stock_sales` | Not in metric-index.md |
| `tgm_amt` | wtd | `tgm_amt` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | wtd | `total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `trans_btl_sales` | wtd | `trans_btl_sales` | Not in metric-index.md |

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
| — | — | No explicit JOIN clauses parsed | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` |

### Key filters and ETL business logic
- `date_flag between '${week_begin_of_firstday}' and '${date_flag}') as table_left` — inferred from ETL WHERE clause
- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For profitability metrics on this table, always filter `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

### Standard time-filter SQL
```sql
-- Reporting filter pattern (replace partition value from L4 trace)
SELECT *
FROM dw_us.dws_disty_brpt_bd_vpl_wtd
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dim_us.dim_pub_date, dw_us.dws_disty_brpt_bd_vpl_1d).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dw_us.dws_disty_brpt_bd_vpl_wtd` partition `date_flag`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dw_us_dws_disty_brpt_bd_vpl_wtd["dw_us.dws_disty_brpt_bd_vpl_wtd"]
  src0["dim_us.dim_pub_date"]
  src0 --> dw_us_dws_disty_brpt_bd_vpl_wtd
  src1["dw_us.dws_disty_brpt_bd_vpl_1d"]
  src1 --> dw_us_dws_disty_brpt_bd_vpl_wtd
  consumers["B Report dashboards / DM serving"]
  dw_us_dws_disty_brpt_bd_vpl_wtd --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_date` | source |
| `dw_us.dws_disty_brpt_bd_vpl_1d` | source |
| `dw_us.dws_disty_brpt_bd_vpl_wtd` | target |

### Step-by-step logic
N/A — no procedural steps parsed from ETL SQL.

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `week_no` | `table_dim.w` | `w` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:14` |
| `date_flag` | `table_dim.max_date_flag` | `max_date_flag` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:15` |
| `project_no` | `project_no` | `project_no` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:17` |
| `project_name` | `project_name` | `project_name` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:18` |
| `task_no` | `task_no` | `task_no` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:19` |
| `task_name` | `task_name` | `task_name` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:20` |
| `company_no` | `company_no` | `company_no` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:21` |
| `vpl_no` | `vpl_no` | `vpl_no` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:22` |
| `vpl_code` | `vpl_code` | `vpl_code` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:23` |
| `vpc_group_id` | `vpc_group_id` | `vpc_group_id` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:24` |
| `vpc_group_desc` | `vpc_group_desc` | `vpc_group_desc` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:25` |
| `vend_no` | `vend_no` | `vend_no` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:26` |
| `vend_name` | `vend_name` | `vend_name` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:27` |
| `master_vend_no` | `master_vend_no` | `master_vend_no` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:28` |
| `master_vend_name` | `master_vend_name` | `master_vend_name` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:29` |
| `seg_code` | `seg_code` | `seg_code` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:30` |
| `gross_sales` | `sum(gross_sales)` | `gross_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:32` |
| `net_sales` | `sum(net_sales)` | `net_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:33` |
| `gross_cost` | `sum(gross_cost)` | `gross_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:34` |
| `net_cost` | `sum(net_cost)` | `net_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:35` |
| `scm_usage` | `sum(scm_usage)` | `scm_usage` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:36` |
| `ds_sales` | `sum(ds_sales)` | `ds_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:37` |
| `stock_sales` | `sum(stock_sales)` | `stock_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:38` |
| `ds_cost` | `sum(ds_cost)` | `ds_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:39` |
| `stock_cost` | `sum(stock_cost)` | `stock_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:40` |
| `ds_scm_usage` | `sum(ds_scm_usage)` | `ds_scm_usage` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:41` |
| `stock_scm_usage` | `sum(stock_scm_usage)` | `stock_scm_usage` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:42` |
| `total_unit` | `sum(total_unit)` | `total_unit` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:43` |
| `total_weight` | `sum(total_weight)` | `total_weight` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:44` |
| `cgp` | `sum(cgp)` | `cgp` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:46` |
| `total_btl` | `sum(total_btl)` | `total_btl` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:47` |
| `tgm_amt` | `sum(tgm_amt)` | `tgm_amt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:48` |
| `gm_amt` | `sum(gm_amt)` | `gm_amt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:49` |
| `ngm_amt` | `sum(ngm_amt)` | `ngm_amt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:50` |
| `oplgm_amt` | `sum(oplgm_amt)` | `oplgm_amt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:51` |
| `bo_gross_sales` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_gross_sales else 0 end)` | `date_flag`, `max_date_flag`, `bo_gross_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_gross_cost` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_gross_cost else 0 end)` | `date_flag`, `max_date_flag`, `bo_gross_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_total_unit` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_total_unit else 0 end)` | `date_flag`, `max_date_flag`, `bo_total_unit` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_gm_amt` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_gm_amt else 0 end)` | `date_flag`, `max_date_flag`, `bo_gm_amt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_gross_sales` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_gross_sales else 0 end)` | `date_flag`, `max_date_flag`, `so_gross_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_gross_cost` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_gross_cost else 0 end)` | `date_flag`, `max_date_flag`, `so_gross_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_total_unit` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_total_unit else 0 end)` | `date_flag`, `max_date_flag`, `so_total_unit` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_gm_amt` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_gm_amt else 0 end)` | `date_flag`, `max_date_flag`, `so_gm_amt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_age0_7` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_age0_7 else 0 end)` | `date_flag`, `max_date_flag`, `bo_age0_7` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_age8_14` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_age8_14 else 0 end)` | `date_flag`, `max_date_flag`, `bo_age8_14` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_age15_21` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_age15_21 else 0 end)` | `date_flag`, `max_date_flag`, `bo_age15_21` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `bo_age21_up` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then bo_age21_up else 0 end)` | `date_flag`, `max_date_flag`, `bo_age21_up` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_age0_7` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_age0_7 else 0 end)` | `date_flag`, `max_date_flag`, `so_age0_7` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_age8_14` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_age8_14 else 0 end)` | `date_flag`, `max_date_flag`, `so_age8_14` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_age15_21` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_age15_21 else 0 end)` | `date_flag`, `max_date_flag`, `so_age15_21` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `so_age21_up` | `SUM(case when table_left.date_flag = table_dim.max_date_flag then so_age21_up else 0 end)` | `date_flag`, `max_date_flag`, `so_age21_up` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | case | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:53` |
| `ap_finance` | `sum(ap_finance)` | `ap_finance` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:70` |
| `inv_cost` | `sum(inv_cost)` | `inv_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:71` |
| `inv_reserve` | `sum(inv_reserve)` | `inv_reserve` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:72` |
| `cr_risk_cterm` | `sum(cr_risk_cterm)` | `cr_risk_cterm` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:73` |
| `flr_synnex` | `sum(flr_synnex)` | `flr_synnex` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:74` |
| `direct_credit` | `sum(direct_credit)` | `direct_credit` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:75` |
| `csgn_edi_fee` | `sum(csgn_edi_fee)` | `csgn_edi_fee` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:76` |
| `corporate` | `sum(corporate)` | `corporate` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:77` |
| `sfs` | `sum(sfs)` | `sfs` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:78` |
| `scm_risk` | `sum(scm_risk)` | `scm_risk` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:79` |
| `flr_vendor` | `sum(flr_vendor)` | `flr_vendor` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:80` |
| `cust_finance_sales` | `sum(cust_finance_sales)` | `cust_finance_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:81` |
| `cust_pmt_disc` | `sum(cust_pmt_disc)` | `cust_pmt_disc` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:82` |
| `cvr_rm` | `sum(cvr_rm)` | `cvr_rm` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:83` |
| `ar_fin_recovery` | `sum(ar_fin_recovery)` | `ar_fin_recovery` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:84` |
| `mfg_oh` | `sum(mfg_oh)` | `mfg_oh` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:85` |
| `cust_finance` | `sum(cust_finance)` | `cust_finance` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:86` |
| `rma` | `sum(rma)` | `rma` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:87` |
| `hc_sales` | `sum(hc_sales)` | `hc_sales` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:88` |
| `order_overhead` | `sum(order_overhead)` | `order_overhead` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:89` |
| `margin_share` | `sum(margin_share)` | `margin_share` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:90` |
| `ap_adj` | `sum(ap_adj)` | `ap_adj` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:91` |
| `pdt` | `sum(pdt)` | `pdt` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:92` |
| `scm_cost` | `sum(scm_cost)` | `scm_cost` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:93` |
| `infrastructure` | `sum(infrastructure)` | `infrastructure` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:94` |
| `marketing` | `sum(marketing)` | `marketing` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:95` |
| `coop` | `sum(coop)` | `coop` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:96` |
| `one_time_btl` | `sum(one_time_btl)` | `one_time_btl` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:97` |
| `hbtl` | `sum(hbtl)` | `hbtl` | `dw_${country}.dws_disty_brpt_bd_vpl_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:98` |

_Showing 80 of 118 columns; full list in L3 `*_column_derivations.json` sidecar._

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
| — | — | Parameters not parsed from ETL wrapper |

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
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_bd_vpl_wtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT week_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_bd_vpl_wtd
WHERE date_flag = '${partition_value}'
GROUP BY week_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT week_no, project_no, task_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_bd_vpl_wtd
WHERE date_flag = '${partition_value}'
GROUP BY week_no, project_no, task_no, date_flag
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
| **Query for reporting** | `dw_us.dws_disty_brpt_bd_vpl_wtd` | `dw_us.dws_disty_brpt_bd_vpl_wtd` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` | yes |
| **Hive alternative** | `dw_us.dws_disty_brpt_bd_vpl_wtd` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dw_us.dws_disty_brpt_bd_vpl_wtd` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` | — |

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
FROM dw_us.dws_disty_brpt_bd_vpl_wtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_date` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` |
| `dw_us.dws_disty_brpt_bd_vpl_1d` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dws_disty_brpt_bd_vpl_wtd.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:12`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dws_disty_brpt_bd_vpl_wtd.py` — primary Bitbucket ETL for `dws_disty_brpt_bd_vpl_wtd` — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` with B Report contract enrichment when available.*
