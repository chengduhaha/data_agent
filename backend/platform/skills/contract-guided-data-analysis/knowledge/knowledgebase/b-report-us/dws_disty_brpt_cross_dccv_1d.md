# DWS: B Report profitability serving aggregation (1d) by business slice (`dw_us.dws_disty_brpt_cross_dccv_1d`)

- artifact_type: etl_table
- artifact_id: dw_us.dws_disty_brpt_cross_dccv_1d
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (1d) by business slice
- layer_type: DWS
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py
- knowledgebase_path: target/knowledgebase/b-report-us/dws_disty_brpt_cross_dccv_1d.md
- contract_source: source/contracts/b-report-us/tables/dws_disty_brpt_cross_dccv_1d.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dws_disty_brpt_cross_dccv_1d`
- **Layer type:** DWS
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** daily snapshot (single business date)
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `date_flag` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `vend_no`, `master_vend_no`, `company_no`, `daily`, `snapshot`, `single`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country}.dws_disty_brpt_cross_dccv_1d` | ETL target in Bitbucket script |
| Vertica | yes | `dw_us.dws_disty_brpt_cross_dccv_1d` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dws_disty_brpt_cross_dccv_1d` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dw_us_dws_disty_brpt_cross_dccv_1d.json` |
| **column_count** | 117 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dws_disty_brpt_cross_dccv_1d schema" --intent find_table_schema` |

### Lineage
- **upstream:** dw_us.dws_disty_brpt_cross_cvv_1d — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dws_disty_brpt_cross_dccv_1d.md`

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
| — | — | No explicit JOIN clauses parsed | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py` |

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
FROM dw_us.dws_disty_brpt_cross_dccv_1d
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dw_us.dws_disty_brpt_cross_cvv_1d).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dw_us.dws_disty_brpt_cross_dccv_1d` partition `date_flag`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dw_us_dws_disty_brpt_cross_dccv_1d["dw_us.dws_disty_brpt_cross_dccv_1d"]
  src0["dw_us.dws_disty_brpt_cross_cvv_1d"]
  src0 --> dw_us_dws_disty_brpt_cross_dccv_1d
  consumers["B Report dashboards / DM serving"]
  dw_us_dws_disty_brpt_cross_dccv_1d --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dw_us.dws_disty_brpt_cross_cvv_1d` | source |
| `dw_us.dws_disty_brpt_cross_dccv_1d` | target |

### Step-by-step logic
N/A — no procedural steps parsed from ETL SQL.

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cust_terr` | `cust_terr` | `cust_terr` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:17` |
| `terr_name` | `terr_name` | `terr_name` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:18` |
| `terr_sub_group` | `terr_sub_group` | `terr_sub_group` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:19` |
| `sub_group_desc` | `sub_group_desc` | `sub_group_desc` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:20` |
| `terr_group` | `terr_group` | `terr_group` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:21` |
| `terr_group_desc` | `terr_group_desc` | `terr_group_desc` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:22` |
| `cust_type` | `cust_type` | `cust_type` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:23` |
| `cust_type_desc` | `cust_type_desc` | `cust_type_desc` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:24` |
| `division` | `division` | `division` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:25` |
| `division_desc` | `division_desc` | `division_desc` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:26` |
| `vend_no` | `vend_no` | `vend_no` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:28` |
| `vend_name` | `vend_name` | `vend_name` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:29` |
| `master_vend_no` | `master_vend_no` | `master_vend_no` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:30` |
| `master_vend_name` | `master_vend_name` | `master_vend_name` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:31` |
| `seg_code` | `seg_code` | `seg_code` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:32` |
| `company_no` | `company_no` | `company_no` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:33` |
| `gross_sales` | `sum(gross_sales)` | `gross_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:35` |
| `net_sales` | `sum(net_sales)` | `net_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:36` |
| `gross_cost` | `sum(gross_cost)` | `gross_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:37` |
| `net_cost` | `sum(net_cost)` | `net_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:38` |
| `scm_usage` | `sum(scm_usage)` | `scm_usage` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:39` |
| `ds_sales` | `sum(ds_sales)` | `ds_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:40` |
| `stock_sales` | `sum(stock_sales)` | `stock_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:41` |
| `ds_cost` | `sum(ds_cost)` | `ds_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:42` |
| `stock_cost` | `sum(stock_cost)` | `stock_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:43` |
| `ds_scm_usage` | `sum(ds_scm_usage)` | `ds_scm_usage` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:44` |
| `stock_scm_usage` | `sum(stock_scm_usage)` | `stock_scm_usage` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:45` |
| `total_unit` | `sum(total_unit)` | `total_unit` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:46` |
| `total_weight` | `sum(total_weight)` | `total_weight` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:47` |
| `cgp` | `sum(cgp)` | `cgp` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:49` |
| `total_btl` | `sum(total_btl)` | `total_btl` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:50` |
| `tgm_amt` | `sum(tgm_amt)` | `tgm_amt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:51` |
| `gm_amt` | `sum(gm_amt)` | `gm_amt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:52` |
| `ngm_amt` | `sum(ngm_amt)` | `ngm_amt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:53` |
| `oplgm_amt` | `sum(oplgm_amt)` | `oplgm_amt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:54` |
| `bo_gross_sales` | `sum(bo_gross_sales)` | `bo_gross_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:56` |
| `bo_gross_cost` | `sum(bo_gross_cost)` | `bo_gross_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:57` |
| `bo_total_unit` | `sum(bo_total_unit)` | `bo_total_unit` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:58` |
| `bo_gm_amt` | `sum(bo_gm_amt)` | `bo_gm_amt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:59` |
| `so_gross_sales` | `sum(so_gross_sales)` | `so_gross_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:60` |
| `so_gross_cost` | `sum(so_gross_cost)` | `so_gross_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:61` |
| `so_total_unit` | `sum(so_total_unit)` | `so_total_unit` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:62` |
| `so_gm_amt` | `sum(so_gm_amt)` | `so_gm_amt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:63` |
| `bo_age0_7` | `sum(bo_age0_7)` | `bo_age0_7` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:64` |
| `bo_age8_14` | `sum(bo_age8_14)` | `bo_age8_14` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:65` |
| `bo_age15_21` | `sum(bo_age15_21)` | `bo_age15_21` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:66` |
| `bo_age21_up` | `sum(bo_age21_up)` | `bo_age21_up` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:67` |
| `so_age0_7` | `sum(so_age0_7)` | `so_age0_7` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:68` |
| `so_age8_14` | `sum(so_age8_14)` | `so_age8_14` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:69` |
| `so_age15_21` | `sum(so_age15_21)` | `so_age15_21` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:70` |
| `so_age21_up` | `sum(so_age21_up)` | `so_age21_up` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:71` |
| `ap_finance` | `sum(ap_finance)` | `ap_finance` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:73` |
| `inv_cost` | `sum(inv_cost)` | `inv_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:74` |
| `inv_reserve` | `sum(inv_reserve)` | `inv_reserve` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:75` |
| `cr_risk_cterm` | `sum(cr_risk_cterm)` | `cr_risk_cterm` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:76` |
| `flr_synnex` | `sum(flr_synnex)` | `flr_synnex` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:77` |
| `direct_credit` | `sum(direct_credit)` | `direct_credit` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:78` |
| `csgn_edi_fee` | `sum(csgn_edi_fee)` | `csgn_edi_fee` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:79` |
| `corporate` | `sum(corporate)` | `corporate` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:80` |
| `sfs` | `sum(sfs)` | `sfs` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:81` |
| `scm_risk` | `sum(scm_risk)` | `scm_risk` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:82` |
| `flr_vendor` | `sum(flr_vendor)` | `flr_vendor` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:83` |
| `cust_finance_sales` | `sum(cust_finance_sales)` | `cust_finance_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:84` |
| `cust_pmt_disc` | `sum(cust_pmt_disc)` | `cust_pmt_disc` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:85` |
| `cvr_rm` | `sum(cvr_rm)` | `cvr_rm` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:86` |
| `ar_fin_recovery` | `sum(ar_fin_recovery)` | `ar_fin_recovery` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:87` |
| `mfg_oh` | `sum(mfg_oh)` | `mfg_oh` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:88` |
| `cust_finance` | `sum(cust_finance)` | `cust_finance` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:89` |
| `rma` | `sum(rma)` | `rma` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:90` |
| `hc_sales` | `sum(hc_sales)` | `hc_sales` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:91` |
| `order_overhead` | `sum(order_overhead)` | `order_overhead` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:92` |
| `margin_share` | `sum(margin_share)` | `margin_share` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:93` |
| `ap_adj` | `sum(ap_adj)` | `ap_adj` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:94` |
| `pdt` | `sum(pdt)` | `pdt` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:95` |
| `scm_cost` | `sum(scm_cost)` | `scm_cost` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:96` |
| `infrastructure` | `sum(infrastructure)` | `infrastructure` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:97` |
| `marketing` | `sum(marketing)` | `marketing` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:98` |
| `coop` | `sum(coop)` | `coop` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:99` |
| `one_time_btl` | `sum(one_time_btl)` | `one_time_btl` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:100` |
| `hbtl` | `sum(hbtl)` | `hbtl` | `dw_${country}.dws_disty_brpt_cross_cvv_1d` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:101` |

_Showing 80 of 117 columns; full list in L3 `*_column_derivations.json` sidecar._

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
FROM dw_us.dws_disty_brpt_cross_dccv_1d
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vend_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cross_dccv_1d
WHERE date_flag = '${partition_value}'
GROUP BY vend_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vend_no, master_vend_no, company_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_cross_dccv_1d
WHERE date_flag = '${partition_value}'
GROUP BY vend_no, master_vend_no, company_no, date_flag
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
| **Query for reporting** | `dw_us.dws_disty_brpt_cross_dccv_1d` | `dw_us.dws_disty_brpt_cross_dccv_1d` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py` | yes |
| **Hive alternative** | `dw_us.dws_disty_brpt_cross_dccv_1d` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dw_us.dws_disty_brpt_cross_dccv_1d` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py` | — |

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
FROM dw_us.dws_disty_brpt_cross_dccv_1d
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_us.dws_disty_brpt_cross_cvv_1d` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dws_disty_brpt_cross_dccv_1d.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py:15`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dws_disty_brpt_cross_dccv_1d.py` — primary Bitbucket ETL for `dws_disty_brpt_cross_dccv_1d` — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_1d/Cross/sql/dws_disty_brpt_cross_dccv_1d.py` with B Report contract enrichment when available.*
