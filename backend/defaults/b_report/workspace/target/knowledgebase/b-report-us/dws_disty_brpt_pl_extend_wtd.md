# DWS: B Report profitability serving aggregation (wtd) by business slice (`dw_us.dws_disty_brpt_pl_extend_wtd`)

- artifact_type: etl_table
- artifact_id: dw_us.dws_disty_brpt_pl_extend_wtd
- domain: b-report-us
- one_line_purpose: B Report profitability serving aggregation (wtd) by business slice
- layer_type: DWS
- source_kind: etl_sql
- evidence_source: source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py
- knowledgebase_path: target/knowledgebase/b-report-us/dws_disty_brpt_pl_extend_wtd.md
- contract_source: source/contracts/b-report-us/tables/dws_disty_brpt_pl_extend_wtd.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dws_disty_brpt_pl_extend_wtd`
- **Layer type:** DWS
- **Canonical / derived:** Derived aggregation/serving (ETL-loaded)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** week-to-date cumulative through each date_flag
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `date_flag` — resolved from Azkaban/bootstrap parameters (see L4).
- **Natural key:** `week_no`, `cust_no`, `mcust_no`, `sales_rep_id`, `sales_sup_id`, `sales_mgr_id`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country}.dws_disty_brpt_pl_extend_wtd` | ETL target in Bitbucket script |
| Vertica | yes | `dw_us.dws_disty_brpt_pl_extend_wtd` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dws_disty_brpt_pl_extend_wtd` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dw_us_dws_disty_brpt_pl_extend_wtd.json` |
| **column_count** | 128 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog and/or VERTICA/vcdisty DDL |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dws_disty_brpt_pl_extend_wtd schema" --intent find_table_schema` |

### Lineage
- **upstream:** dim_us.dim_pub_date, dw_us.dws_disty_brpt_pl_extend_1d — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py`
- **downstream:** B Report DM/DWS serving and dashboards (per contract L6 when present) — `source/contracts/b-report-us/tables/dws_disty_brpt_pl_extend_wtd.md`

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
| P&L adjustment / measure | `stock_cost` | `stock_cost` | stock_cost at wtd grain |
| P&L adjustment / measure | `stock_sales` | `stock_sales` | stock_sales at wtd grain |
| Governed profitability | `tgm_amt` | `tgm_amt` | tgm_amt at wtd grain |
| Governed profitability | `total_btl` | `total_btl` | total_btl at wtd grain |
| P&L adjustment / measure | `trans_btl_sales` | `trans_btl_sales` | trans_btl_sales at wtd grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
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
| — | — | No explicit JOIN clauses parsed | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` |

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
FROM dw_us.dws_disty_brpt_pl_extend_wtd
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. Read upstream warehouse objects (dim_us.dim_pub_date, dw_us.dws_disty_brpt_pl_extend_1d).
2. Apply CTE aggregations and business joins inside ETL SQL.
3. INSERT OVERWRITE into `dw_us.dws_disty_brpt_pl_extend_wtd` partition `date_flag`.
4. Sync to Vertica for B Report consumption (sync job not verified in this repository unless cited below).

```mermaid
flowchart LR
  dw_us_dws_disty_brpt_pl_extend_wtd["dw_us.dws_disty_brpt_pl_extend_wtd"]
  src0["dim_us.dim_pub_date"]
  src0 --> dw_us_dws_disty_brpt_pl_extend_wtd
  src1["dw_us.dws_disty_brpt_pl_extend_1d"]
  src1 --> dw_us_dws_disty_brpt_pl_extend_wtd
  consumers["B Report dashboards / DM serving"]
  dw_us_dws_disty_brpt_pl_extend_wtd --> consumers
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_date` | source |
| `dw_us.dws_disty_brpt_pl_extend_1d` | source |
| `dw_us.dws_disty_brpt_pl_extend_wtd` | target |

### Step-by-step logic
N/A — no procedural steps parsed from ETL SQL.

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `week_no` | `table_dim.w` | `w` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:14` |
| `date_flag` | `table_dim.max_date_flag` | `max_date_flag` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | rename | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:15` |
| `3` | `nvl(table_left.cust_no,-3)` | `cust_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:17` |
| `cust_name` | `table_left.cust_name` | `cust_name` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:18` |
| `3` | `nvl(table_left.mcust_no,-3)` | `mcust_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:19` |
| `mcust_name` | `table_left.mcust_name` | `mcust_name` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:20` |
| `3` | `nvl(table_left.cust_terr,-3)` | `cust_terr` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:21` |
| `terr_name` | `table_left.terr_name` | `terr_name` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:22` |
| `3` | `nvl(table_left.cust_type,-3)` | `cust_type` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:23` |
| `cust_type_desc` | `table_left.cust_type_desc` | `cust_type_desc` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:24` |
| `3` | `nvl(table_left.division,-3)` | `division` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:25` |
| `division_desc` | `table_left.division_desc` | `division_desc` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:26` |
| `3` | `nvl(table_left.terr_sub_group,-3)` | `terr_sub_group` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:27` |
| `sub_group_desc` | `table_left.sub_group_desc` | `sub_group_desc` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:28` |
| `3` | `nvl(table_left.terr_group,-3)` | `terr_group` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:29` |
| `terr_group_desc` | `table_left.terr_group_desc` | `terr_group_desc` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:30` |
| `3` | `nvl(table_left.sales_rep_id,-3)` | `sales_rep_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:32` |
| `3` | `nvl(table_left.sales_sup_id,-3)` | `sales_sup_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:33` |
| `3` | `nvl(table_left.sales_mgr_id,-3)` | `sales_mgr_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:34` |
| `3` | `nvl(table_left.sales_dir_id,-3)` | `sales_dir_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:35` |
| `3` | `nvl(table_left.sales_vp_id,-3)` | `sales_vp_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:36` |
| `3` | `nvl(table_left.sku_no,-3)` | `sku_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:38` |
| `part_no` | `table_left.part_no` | `part_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:39` |
| `mfg_partno` | `table_left.mfg_partno` | `mfg_partno` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:40` |
| `3` | `nvl(table_left.vpl_no,-3)` | `vpl_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:41` |
| `vpl_code` | `table_left.vpl_code` | `vpl_code` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:42` |
| `3` | `nvl(table_left.vpc_group_id,-3)` | `vpc_group_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:43` |
| `vpc_group_desc` | `table_left.vpc_group_desc` | `vpc_group_desc` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:44` |
| `3` | `nvl(table_left.vend_no,-3)` | `vend_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:45` |
| `vend_name` | `table_left.vend_name` | `vend_name` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:46` |
| `3` | `nvl(table_left.master_vend_no,-3)` | `master_vend_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:47` |
| `master_vend_name` | `table_left.master_vend_name` | `master_vend_name` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:48` |
| `3` | `nvl(table_left.group_id,-3)` | `group_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:49` |
| `seg_code` | `table_left.seg_code` | `seg_code` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | passthrough | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:50` |
| `3` | `nvl(table_left.pm_id,-3)` | `pm_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:52` |
| `3` | `nvl(table_left.pm_mgr_id,-3)` | `pm_mgr_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:53` |
| `3` | `nvl(table_left.pm_dir_id,-3)` | `pm_dir_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:54` |
| `3` | `nvl(table_left.pm_vp_id,-3)` | `pm_vp_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:55` |
| `3` | `nvl(table_left.buyer_id,-3)` | `buyer_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:56` |
| `3` | `nvl(table_left.buyer_mgr_id,-3)` | `buyer_mgr_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:57` |
| `3` | `nvl(table_left.buyer_dir_id,-3)` | `buyer_dir_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:58` |
| `3` | `nvl(table_left.buyer_vp_id,-3)` | `buyer_vp_id` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:59` |
| `1` | `nvl(table_left.company_no,1)` | `company_no` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | coalesce | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:61` |
| `0` | `nvl(sum(gross_sales),0)` | `gross_sales` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:63` |
| `0` | `nvl(sum(net_sales),0)` | `net_sales` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:64` |
| `0` | `nvl(sum(gross_cost),0)` | `gross_cost` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:65` |
| `0` | `nvl(sum(net_cost),0)` | `net_cost` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:66` |
| `0` | `nvl(sum(scm_usage),0)` | `scm_usage` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:67` |
| `0` | `nvl(sum(ds_sales),0)` | `ds_sales` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:68` |
| `0` | `nvl(sum(stock_sales),0)` | `stock_sales` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:69` |
| `0` | `nvl(sum(ds_cost),0)` | `ds_cost` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:70` |
| `0` | `nvl(sum(stock_cost),0)` | `stock_cost` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:71` |
| `0` | `nvl(sum(ds_scm_usage),0)` | `ds_scm_usage` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:72` |
| `0` | `nvl(sum(stock_scm_usage),0)` | `stock_scm_usage` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:73` |
| `0` | `nvl(sum(total_unit),0)` | `total_unit` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:74` |
| `0` | `nvl(sum(total_weight),0)` | `total_weight` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:75` |
| `0` | `nvl(sum(cgp),0)` | `cgp` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:77` |
| `0` | `nvl(sum(total_btl),0)` | `total_btl` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:78` |
| `0` | `nvl(sum(tgm_amt),0)` | `tgm_amt` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:79` |
| `0` | `nvl(sum(gm_amt),0)` | `gm_amt` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:80` |
| `0` | `nvl(sum(ngm_amt),0)` | `ngm_amt` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:81` |
| `0` | `nvl(sum(oplgm_amt),0)` | `oplgm_amt` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:82` |
| `0` | `nvl(sum(ap_finance),0)` | `ap_finance` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:84` |
| `0` | `nvl(sum(inv_cost),0)` | `inv_cost` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:85` |
| `0` | `nvl(sum(inv_reserve),0)` | `inv_reserve` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:86` |
| `0` | `nvl(sum(cr_risk_cterm),0)` | `cr_risk_cterm` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:87` |
| `0` | `nvl(sum(flr_synnex),0)` | `flr_synnex` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:88` |
| `0` | `nvl(sum(direct_credit),0)` | `direct_credit` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:89` |
| `0` | `nvl(sum(csgn_edi_fee),0)` | `csgn_edi_fee` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:90` |
| `0` | `nvl(sum(corporate),0)` | `corporate` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:91` |
| `0` | `nvl(sum(sfs),0)` | `sfs` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:92` |
| `0` | `nvl(sum(scm_risk),0)` | `scm_risk` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:93` |
| `0` | `nvl(sum(flr_vendor),0)` | `flr_vendor` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:94` |
| `0` | `nvl(sum(cust_finance_sales),0)` | `cust_finance_sales` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:95` |
| `0` | `nvl(sum(cust_pmt_disc),0)` | `cust_pmt_disc` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:96` |
| `0` | `nvl(sum(cvr_rm),0)` | `cvr_rm` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:97` |
| `0` | `nvl(sum(ar_fin_recovery),0)` | `ar_fin_recovery` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:98` |
| `0` | `nvl(sum(mfg_oh),0)` | `mfg_oh` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:99` |
| `0` | `nvl(sum(cust_finance),0)` | `cust_finance` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:100` |
| `0` | `nvl(sum(rma),0)` | `rma` | `dw_${country}.dws_disty_brpt_pl_extend_1d`, `dim_${country}.dim_pub_date` | agg | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:101` |

_Showing 80 of 128 columns; full list in L3 `*_column_derivations.json` sidecar._

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
FROM dw_us.dws_disty_brpt_pl_extend_wtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT week_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_pl_extend_wtd
WHERE date_flag = '${partition_value}'
GROUP BY week_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT week_no, cust_no, mcust_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_pl_extend_wtd
WHERE date_flag = '${partition_value}'
GROUP BY week_no, cust_no, mcust_no, date_flag
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
| **Query for reporting** | `dw_us.dws_disty_brpt_pl_extend_wtd` | `dw_us.dws_disty_brpt_pl_extend_wtd` | overwrite / incremental | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` | yes |
| **Hive alternative** | `dw_us.dws_disty_brpt_pl_extend_wtd` | same as reporting table | — | ETL target table | — |
| **ETL internal** | `dw_us.dws_disty_brpt_pl_extend_wtd` | n/a | INSERT OVERWRITE | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` | — |

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
FROM dw_us.dws_disty_brpt_pl_extend_wtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_date` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` |
| `dw_us.dws_disty_brpt_pl_extend_1d` | ETL source | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report dashboards / sibling DM tables | `source/contracts/b-report-us/tables/dws_disty_brpt_pl_extend_wtd.md:L6` |

#### Operational detail (verified)
- Load pattern: INSERT OVERWRITE (partitioned) per ETL SQL — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:12`
- ETL script path: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py`

#### Not documented in repository
- Azkaban `.flow` orchestration for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dws_disty_brpt_pl_extend_wtd.py` — primary Bitbucket ETL for `dws_disty_brpt_pl_extend_wtd` — `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py`

---

*Document generated from `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` with B Report contract enrichment when available.*
