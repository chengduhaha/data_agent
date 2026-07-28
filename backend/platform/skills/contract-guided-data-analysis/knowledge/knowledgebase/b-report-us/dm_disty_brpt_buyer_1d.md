# DM: B Report profitability serving aggregation (1d) by business slice (`dm_us.dm_disty_brpt_buyer_1d`)

- artifact_type: etl_table
- artifact_id: dm_us.dm_disty_brpt_buyer_1d
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (1d) by business slice
- layer_type: DM
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py
- knowledgebase_path: target/knowledgebase/b-report-us/dm_disty_brpt_buyer_1d.md
- contract_source: source/contracts/b-report-us/tables/dm_disty_brpt_buyer_1d.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dm_us.dm_disty_brpt_buyer_1d`
- **Layer type:** DM
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** daily snapshot (single business date)
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `date_flag` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `buyer_id`, `buyer_mgr_id`, `buyer_dir_id`, `buyer_vp_id`, `company_no`, `daily`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dm_${country}.dm_disty_brpt_buyer_1d` | ETL target in Bitbucket script |
| Vertica | yes | `dm_us.dm_disty_brpt_buyer_1d` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dm_us.dm_disty_brpt_buyer_1d` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dm_us_dm_disty_brpt_buyer_1d.json` |
| **column_count** | 124 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dm_disty_brpt_buyer_1d schema" --intent find_table_schema` |

### Lineage
- **upstream:** dw_us.dws_disty_brpt_part_1d, ods_us.ods_cis_corp_manager — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dm_disty_brpt_buyer_1d.md`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | INSERT OVERWRITE partition reload (per ETL SQL) |
| Schedule | Not documented in repository |
| Parameters | country, date_flag |

---

## L2 Declarative Knowledge

### Business purpose
B Report profitability serving aggregation (1d) by business slice

This Knowledgebase entry documents the Bitbucket ETL load script in `source/contracts/b-report-us/bitbicket_etl/`. Business semantics align with the B Report US contract catalog when present.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: PM, Sales, Buyer, BD and executive analysis views. |
| **Sales / PM / finance** | Shipped-order and margin metrics at documented grain (daily snapshot). |
| **Data engineering** | Verified upstream/downstream objects with `file:line` evidence from ETL SQL. |

### Fact key resolution
- Order-line hub for B Report P&L: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` when debugging transaction-level metrics.
- This table grain: daily snapshot (single business date).
- Label-on/off and order_type adjustments: see `source/contracts/b-report-us/metric-index.md`.

### Time field semantics
- **`date_flag`:** primary partition / filter for this load; value supplied by Azkaban `conf.get` parameters (see L4).
- **Period semantics:** daily snapshot.


### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `bo_gm_amt` | `bo_gm_amt` | bo_gm_amt at daily grain |
| P&L adjustment / measure | `bo_gross_cost` | `bo_gross_cost` | bo_gross_cost at daily grain |
| P&L adjustment / measure | `bo_gross_sales` | `bo_gross_sales` | bo_gross_sales at daily grain |
| P&L adjustment / measure | `btl_sales` | `btl_sales` | btl_sales at daily grain |
| P&L adjustment / measure | `cust_finance_sales` | `cust_finance_sales` | cust_finance_sales at daily grain |
| P&L adjustment / measure | `ds_cost` | `ds_cost` | ds_cost at daily grain |
| P&L adjustment / measure | `ds_sales` | `ds_sales` | ds_sales at daily grain |
| P&L adjustment / measure | `fx_cost` | `fx_cost` | fx_cost at daily grain |
| Governed profitability | `gm_amt` | `gm_amt` | gm_amt at daily grain |
| P&L adjustment / measure | `gross_cost` | `gross_cost` | gross_cost at daily grain |
| Governed profitability | `gross_sales` | `gross_sales` | gross_sales at daily grain |
| P&L adjustment / measure | `hc_sales` | `hc_sales` | hc_sales at daily grain |
| P&L adjustment / measure | `inv_cost` | `inv_cost` | inv_cost at daily grain |
| P&L adjustment / measure | `net_cost` | `net_cost` | net_cost at daily grain |
| Governed profitability | `net_sales` | `net_sales` | net_sales at daily grain |
| Governed profitability | `ngm_amt` | `ngm_amt` | ngm_amt at daily grain |
| P&L adjustment / measure | `oh_cost` | `oh_cost` | oh_cost at daily grain |
| P&L adjustment / measure | `oo_cost` | `oo_cost` | oo_cost at daily grain |
| Governed profitability | `oplgm_amt` | `oplgm_amt` | oplgm_amt at daily grain |
| Governed profitability | `oplgm_plus_amt` | `oplgm_plus_amt` | oplgm_plus_amt at daily grain |
| P&L adjustment / measure | `others_sales` | `others_sales` | others_sales at daily grain |
| P&L adjustment / measure | `scm_cost` | `scm_cost` | scm_cost at daily grain |
| P&L adjustment / measure | `so_gm_amt` | `so_gm_amt` | so_gm_amt at daily grain |
| P&L adjustment / measure | `so_gross_cost` | `so_gross_cost` | so_gross_cost at daily grain |
| P&L adjustment / measure | `so_gross_sales` | `so_gross_sales` | so_gross_sales at daily grain |
| P&L adjustment / measure | `stock_cost` | `stock_cost` | stock_cost at daily grain |
| P&L adjustment / measure | `stock_sales` | `stock_sales` | stock_sales at daily grain |
| Governed profitability | `tgm_amt` | `tgm_amt` | tgm_amt at daily grain |
| Governed profitability | `total_btl` | `total_btl` | total_btl at daily grain |
| P&L adjustment / measure | `trans_btl_sales` | `trans_btl_sales` | trans_btl_sales at daily grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `bo_gm_amt` | daily | `bo_gm_amt` | Not in metric-index.md |
| `bo_gross_cost` | daily | `bo_gross_cost` | Not in metric-index.md |
| `bo_gross_sales` | daily | `bo_gross_sales` | Not in metric-index.md |
| `btl_sales` | daily | `btl_sales` | Not in metric-index.md |
| `cust_finance_sales` | daily | `cust_finance_sales` | Not in metric-index.md |
| `ds_cost` | daily | `ds_cost` | Not in metric-index.md |
| `ds_sales` | daily | `ds_sales` | Not in metric-index.md |
| `fx_cost` | daily | `fx_cost` | Not in metric-index.md |
| `gm_amt` | daily | `gm_amt` | `source/contracts/b-report-us/metric-index.md#gm_amt` |
| `gross_cost` | daily | `gross_cost` | Not in metric-index.md |
| `gross_sales` | daily | `gross_sales` | `source/contracts/b-report-us/metric-index.md#gross_sales` |
| `hc_sales` | daily | `hc_sales` | Not in metric-index.md |
| `inv_cost` | daily | `inv_cost` | Not in metric-index.md |
| `net_cost` | daily | `net_cost` | Not in metric-index.md |
| `net_sales` | daily | `net_sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |
| `ngm_amt` | daily | `ngm_amt` | `source/contracts/b-report-us/metric-index.md#ngm_amt` |
| `oh_cost` | daily | `oh_cost` | Not in metric-index.md |
| `oo_cost` | daily | `oo_cost` | Not in metric-index.md |
| `oplgm_amt` | daily | `oplgm_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_amt` |
| `oplgm_plus_amt` | daily | `oplgm_plus_amt` | `source/contracts/b-report-us/metric-index.md#oplgm_plus_amt` |
| `others_sales` | daily | `others_sales` | Not in metric-index.md |
| `scm_cost` | daily | `scm_cost` | Not in metric-index.md |
| `so_gm_amt` | daily | `so_gm_amt` | Not in metric-index.md |
| `so_gross_cost` | daily | `so_gross_cost` | Not in metric-index.md |
| `so_gross_sales` | daily | `so_gross_sales` | Not in metric-index.md |
| `stock_cost` | daily | `stock_cost` | Not in metric-index.md |
| `stock_sales` | daily | `stock_sales` | Not in metric-index.md |
| `tgm_amt` | daily | `tgm_amt` | `source/contracts/b-report-us/metric-index.md#tgm_amt` |
| `total_btl` | daily | `total_btl` | `source/contracts/b-report-us/metric-index.md#total_btl` |
| `trans_btl_sales` | daily | `trans_btl_sales` | Not in metric-index.md |

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
| — | — | No explicit JOIN clauses parsed | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py` |

### Key filters and ETL business logic
- `date_flag between '${firstday_of_month}' and '${date_flag}'` — inferred from ETL WHERE clause
- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For profitability metrics on this table, always filter `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

### Standard time-filter SQL
```sql
-- Reporting filter pattern (replace partition value from L4 trace)
SELECT *
FROM dm_us.dm_disty_brpt_buyer_1d
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dw_us.dws_disty_brpt_part_1d, ods_us.ods_cis_corp_manager).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dm_us.dm_disty_brpt_buyer_1d` partition `date_flag`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dm_us_dm_disty_brpt_buyer_1d["dm_us.dm_disty_brpt_buyer_1d"]
  src0["dw_us.dws_disty_brpt_part_1d"]
  src0 --> dm_us_dm_disty_brpt_buyer_1d
  src1["ods_us.ods_cis_corp_manager"]
  src1 --> dm_us_dm_disty_brpt_buyer_1d
  consumers["B Report dashboards / DM serving"]
  dm_us_dm_disty_brpt_buyer_1d --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dm_us.dm_disty_brpt_buyer_1d` | target |
| `dw_us.dws_disty_brpt_part_1d` | source |
| `ods_us.ods_cis_corp_manager` | source |

### Step-by-step logic
#### Step 1 — CTE `table_dws`

**Source:** intermediate aggregation inside ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py`

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `buyer_id` | `buyer_id` | `buyer_id` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:20` |
| `buyer_name` | `concat_ws(' ', table_manager.firstname, table_manager.lastname)` | `concat_ws`, `firstname`, `lastname` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:156` |
| `buyer_mgr_id` | `buyer_mgr_id` | `buyer_mgr_id` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:21` |
| `buyer_mgr_name` | `concat_ws(' ', table_manager2.firstname, table_manager2.lastname)` | `concat_ws`, `firstname`, `lastname` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:158` |
| `buyer_dir_id` | `buyer_dir_id` | `buyer_dir_id` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:22` |
| `buyer_dir_name` | `concat_ws(' ', table_manager3.firstname, table_manager3.lastname)` | `concat_ws`, `firstname`, `lastname` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:160` |
| `buyer_vp_id` | `buyer_vp_id` | `buyer_vp_id` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:23` |
| `buyer_vp_name` | `concat_ws(' ', table_manager4.firstname, table_manager4.lastname)` | `concat_ws`, `firstname`, `lastname` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | udf | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:162` |
| `company_no` | `company_no` | `company_no` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:24` |
| `gross_sales` | `sum(gross_sales)` | `gross_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:25` |
| `net_sales` | `sum(net_sales)` | `net_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:26` |
| `gross_cost` | `sum(gross_cost)` | `gross_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:27` |
| `net_cost` | `sum(net_cost)` | `net_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:28` |
| `scm_usage` | `sum(scm_usage)` | `scm_usage` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:29` |
| `ds_sales` | `sum(ds_sales)` | `ds_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:30` |
| `stock_sales` | `sum(stock_sales)` | `stock_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:31` |
| `ds_cost` | `sum(ds_cost)` | `ds_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:32` |
| `stock_cost` | `sum(stock_cost)` | `stock_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:33` |
| `ds_scm_usage` | `sum(ds_scm_usage)` | `ds_scm_usage` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:34` |
| `stock_scm_usage` | `sum(stock_scm_usage)` | `stock_scm_usage` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:35` |
| `total_unit` | `sum(total_unit)` | `total_unit` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:36` |
| `total_weight` | `sum(total_weight)` | `total_weight` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:37` |
| `cgp` | `sum(cgp)` | `cgp` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:39` |
| `total_btl` | `sum(total_btl)` | `total_btl` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:40` |
| `tgm_amt` | `sum(tgm_amt)` | `tgm_amt` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:41` |
| `gm_amt` | `sum(gm_amt)` | `gm_amt` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:42` |
| `ngm_amt` | `sum(ngm_amt)` | `ngm_amt` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:43` |
| `oplgm_amt` | `sum(oplgm_amt)` | `oplgm_amt` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:44` |
| `bo_gross_sales` | `sum(bo_gross_sales)` | `bo_gross_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:46` |
| `bo_gross_cost` | `sum(bo_gross_cost)` | `bo_gross_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:47` |
| `bo_total_unit` | `sum(bo_total_unit)` | `bo_total_unit` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:48` |
| `bo_gm_amt` | `sum(bo_gm_amt)` | `bo_gm_amt` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:49` |
| `so_gross_sales` | `sum(so_gross_sales)` | `so_gross_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:50` |
| `so_gross_cost` | `sum(so_gross_cost)` | `so_gross_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:51` |
| `so_total_unit` | `sum(so_total_unit)` | `so_total_unit` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:52` |
| `so_gm_amt` | `sum(so_gm_amt)` | `so_gm_amt` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:53` |
| `bo_age0_7` | `sum(bo_age0_7)` | `bo_age0_7` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:54` |
| `bo_age8_14` | `sum(bo_age8_14)` | `bo_age8_14` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:55` |
| `bo_age15_21` | `sum(bo_age15_21)` | `bo_age15_21` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:56` |
| `bo_age21_up` | `sum(bo_age21_up)` | `bo_age21_up` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:57` |
| `so_age0_7` | `sum(so_age0_7)` | `so_age0_7` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:58` |
| `so_age8_14` | `sum(so_age8_14)` | `so_age8_14` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:59` |
| `so_age15_21` | `sum(so_age15_21)` | `so_age15_21` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:60` |
| `so_age21_up` | `sum(so_age21_up)` | `so_age21_up` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:61` |
| `reg_inv` | `sum(reg_inv)` | `reg_inv` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:63` |
| `reg_inv_age0_30` | `sum(reg_inv_age0_30)` | `reg_inv_age0_30` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:64` |
| `reg_inv_age31_60` | `sum(reg_inv_age31_60)` | `reg_inv_age31_60` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:65` |
| `reg_inv_age61_90` | `sum(reg_inv_age61_90)` | `reg_inv_age61_90` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:66` |
| `reg_inv_age90_up` | `sum(reg_inv_age90_up)` | `reg_inv_age90_up` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:67` |
| `rma_inv` | `sum(rma_inv)` | `rma_inv` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:68` |
| `rma_inv_age0_30` | `sum(rma_inv_age0_30)` | `rma_inv_age0_30` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:69` |
| `rma_inv_age31_60` | `sum(rma_inv_age31_60)` | `rma_inv_age31_60` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:70` |
| `rma_inv_age61_90` | `sum(rma_inv_age61_90)` | `rma_inv_age61_90` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:71` |
| `rma_inv_age90_up` | `sum(rma_inv_age90_up)` | `rma_inv_age90_up` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:72` |
| `oh_cost` | `sum(oh_cost)` | `oh_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:73` |
| `oo_cost` | `sum(oo_cost)` | `oo_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:74` |
| `oh_qty` | `sum(oh_qty)` | `oh_qty` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:75` |
| `oo_qty` | `sum(oo_qty)` | `oo_qty` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:76` |
| `ap_finance` | `sum(ap_finance)` | `ap_finance` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:78` |
| `inv_cost` | `sum(inv_cost)` | `inv_cost` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:79` |
| `inv_reserve` | `sum(inv_reserve)` | `inv_reserve` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:80` |
| `cr_risk_cterm` | `sum(cr_risk_cterm)` | `cr_risk_cterm` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:81` |
| `flr_synnex` | `sum(flr_synnex)` | `flr_synnex` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:82` |
| `direct_credit` | `sum(direct_credit)` | `direct_credit` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:83` |
| `csgn_edi_fee` | `sum(csgn_edi_fee)` | `csgn_edi_fee` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:84` |
| `corporate` | `sum(corporate)` | `corporate` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:85` |
| `sfs` | `sum(sfs)` | `sfs` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:86` |
| `scm_risk` | `sum(scm_risk)` | `scm_risk` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:87` |
| `flr_vendor` | `sum(flr_vendor)` | `flr_vendor` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:88` |
| `cust_finance_sales` | `sum(cust_finance_sales)` | `cust_finance_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:89` |
| `cust_pmt_disc` | `sum(cust_pmt_disc)` | `cust_pmt_disc` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:90` |
| `cvr_rm` | `sum(cvr_rm)` | `cvr_rm` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:91` |
| `ar_fin_recovery` | `sum(ar_fin_recovery)` | `ar_fin_recovery` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:92` |
| `mfg_oh` | `sum(mfg_oh)` | `mfg_oh` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:93` |
| `cust_finance` | `sum(cust_finance)` | `cust_finance` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:94` |
| `rma` | `sum(rma)` | `rma` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:95` |
| `hc_sales` | `sum(hc_sales)` | `hc_sales` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:96` |
| `order_overhead` | `sum(order_overhead)` | `order_overhead` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:97` |
| `margin_share` | `sum(margin_share)` | `margin_share` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:98` |
| `ap_adj` | `sum(ap_adj)` | `ap_adj` | `table_dws`, `ods_${country}.ods_cis_corp_manager` | agg | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:99` |

_Showing 80 of 124 columns; full list in L3 `*_column_derivations.json` sidecar._

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
FROM dm_us.dm_disty_brpt_buyer_1d
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT buyer_id, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_brpt_buyer_1d
WHERE date_flag = '${partition_value}'
GROUP BY buyer_id
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT buyer_id, buyer_mgr_id, buyer_dir_id, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_disty_brpt_buyer_1d
WHERE date_flag = '${partition_value}'
GROUP BY buyer_id, buyer_mgr_id, buyer_dir_id, date_flag
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
| **Query for reporting** | `dm_us.dm_disty_brpt_buyer_1d` | `dm_us.dm_disty_brpt_buyer_1d` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py` | yes |
| **Hive alternative** | `dm_us.dm_disty_brpt_buyer_1d` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dm_us.dm_disty_brpt_buyer_1d` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py` | — |

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
SELECT date_flag, SUM(net_sales) AS net_sales, SUM(ngm_amt) AS ngm_amt
FROM dm_us.dm_disty_brpt_buyer_1d
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dws_disty_brpt_part_1d` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py` |
| `ods_us.ods_cis_corp_manager` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dm_disty_brpt_buyer_1d.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py:152`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dm_disty_brpt_buyer_1d.py` — primary Bitbucket ETL for `dm_disty_brpt_buyer_1d` — `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_1d/Product/sql/dm_disty_brpt_buyer_1d.py` with B Report contract enrichment when available.*
