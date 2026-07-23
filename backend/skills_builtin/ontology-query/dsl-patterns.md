# DSL 模式与编译约定

本文档定义 **Object Query DSL 的扩展字段** 及 **DSL → SQL 编译规则**。  
凡 SQL 中出现的 `CASE WHEN`、`TO_CHAR`、排除过滤、跨对象 `GROUP BY`，**必须先在 DSL 中声明**，再按本节编译。

## 强制输出格式（每次 MCP 前）

**每一次** `run_query_safely` 调用前，Agent 必须按顺序输出以下四段（缺一不可）：

```markdown
### Query <N>: <查询目的>

#### 1. intent_json
{ ... }

#### 2. Object Query DSL
{ ... }

#### 3. Compiled SQL
```sql
SELECT ...
```

#### 4. Ontology trace
| SQL 元素 | 本体来源 |
|----------|----------|
| hub 子查询 | ShippedOrderLine.physical_source |
| dim_pm_id | ShippedOrderLine.dimPmId → dim_pm_id |
| JOIN Customer | relations.yaml: ShippedOrderLine_to_Customer |
```

**禁止**：读完本体后直接写 SQL 并调 MCP。  
**多步下钻**：每一步单独一套 intent_json + DSL + SQL + trace（Query 1、Query 2…）。

---

## 模式 1：周期对比 `period_slices`

用于「Feb vs Mar」「2024 vs 2025」等 `query_kind: comparison`。

### DSL

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [
    {"property": "dimPmId", "operator": "=", "value": 706187},
    {"property": "dateFlag", "operator": ">=", "value": "2026-02-01"},
    {"property": "dateFlag", "operator": "<=", "value": "2026-03-31"}
  ],
  "period_slices": [
    {
      "label": "feb_2026",
      "filters": [
        {"property": "dateFlag", "operator": ">=", "value": "2026-02-01"},
        {"property": "dateFlag", "operator": "<=", "value": "2026-02-28"}
      ]
    },
    {
      "label": "mar_2026",
      "filters": [
        {"property": "dateFlag", "operator": ">=", "value": "2026-03-01"},
        {"property": "dateFlag", "operator": "<=", "value": "2026-03-31"}
      ]
    }
  ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "net_sales", "per_period": true},
    {"function": "SUM", "property": "ngmAmt", "alias": "ngm_amt", "per_period": true},
    {
      "function": "RATIO",
      "alias": "ngm_pct",
      "per_period": true,
      "numerator": {"function": "SUM", "property": "ngmAmt"},
      "denominator": {"function": "SUM", "property": "netSales"}
    }
  ],
  "limit": 10
}
```

### 编译规则

每个 `period_slices[].label` → 一组 `CASE WHEN <slice filters on mapping> THEN <expr> ELSE 0 END`：

```sql
SUM(CASE WHEN hub.date_flag >= '2026-02-01' AND hub.date_flag <= '2026-02-28'
         THEN hub.calc_net_sales ELSE 0 END) AS net_sales_feb_2026
```

`RATIO` + `per_period: true` → 先编译分子分母 CASE 列，再：

```sql
SUM(CASE WHEN ... THEN hub.ngm_amt ELSE 0 END)
  / NULLIF(SUM(CASE WHEN ... THEN hub.calc_net_sales ELSE 0 END), 0) AS ngm_pct_feb_2026
```

**禁止**在 DSL 未声明 `period_slices` 时手写 `CASE WHEN` 做周期对比。

---

## 模式 2：时间粒度 `time_grain`

用于「按月」「按周」分组。

### DSL

```json
{
  "group_by": [
    {"property": "dateFlag", "time_grain": "month", "alias": "month_label"}
  ]
}
```

| time_grain | 编译为（Vertica） |
|------------|-------------------|
| `month` | `TO_CHAR(<dateFlag mapping>, 'YYYY-MM')` |
| `year` | `TO_CHAR(<dateFlag mapping>, 'YYYY')` |
| `day` | `<dateFlag mapping>`（不加函数） |

**禁止**在 DSL 未声明 `time_grain` 时手写 `TO_CHAR(date_flag, ...)`。

---

## 模式 3：排除过滤 `operator: "<>"`

### DSL

```json
{"property": "custNo", "operator": "<>", "value": 802609}
```

编译为：`hub.cust_no <> 802609`

支持的操作符：`=`、`!=` / `<>`、`>`、`>=`、`<`、`<=`、`IN`、`NOT IN`、`BETWEEN`、`IS NULL`、`IS NOT NULL`。

---

## 模式 4：跨对象 `group_by` + `joins`

按客户名、供应商名、VPC 描述分组时，DSL 必须声明 JOIN。

### DSL

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [
    {"property": "dimPmId", "operator": "=", "value": 706187},
    {"property": "dateFlag", "operator": ">=", "value": "2026-03-01"},
    {"property": "dateFlag", "operator": "<=", "value": "2026-03-31"}
  ],
  "joins": [
    {"link": "ShippedOrderLine_to_Customer"}
  ],
  "group_by": [
    {"object_type": "Customer", "property": "custNo"},
    {"object_type": "Customer", "property": "custName"}
  ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "net_sales"},
    {"function": "SUM", "property": "ngmAmt", "alias": "ngm_amt"},
    {
      "function": "RATIO",
      "alias": "ngm_pct",
      "numerator": {"function": "SUM", "property": "ngmAmt"},
      "denominator": {"function": "SUM", "property": "netSales"}
    }
  ],
  "order_by": [{"property": "net_sales", "direction": "DESC"}],
  "limit": 15
}
```

### 编译规则

1. `joins[].link` → 查 `relations.yaml` 中 `name` 匹配的 `join_logic`
2. `group_by` 中带 `object_type` 的项 → 用该对象 `properties[].mapping`
3. hub 上可直接分组的属性（如 `dimVplNo`）可写 `{"property": "dimVplNo"}`，无需 JOIN

按 VPC 描述分组示例：

```json
"joins": [{"link": "ShippedOrderLine_to_VendorProductLine"}],
"group_by": [
  {"object_type": "VendorProductLine", "property": "vplNo"},
  {"object_type": "VendorProductLine", "property": "vplDesc"}
]
```

---

## 模式 5：比率指标 `function: RATIO`

用于 NGM%、毛利率等，**禁止 LLM 手算**。

### DSL

```json
{
  "function": "RATIO",
  "alias": "ngm_pct",
  "numerator": {"function": "SUM", "property": "ngmAmt"},
  "denominator": {"function": "SUM", "property": "netSales"}
}
```

编译为：

```sql
SUM(hub.ngm_amt) / NULLIF(SUM(hub.calc_net_sales), 0) AS ngm_pct
```

若 metric 在 `metrics.yaml` 有预定义（如 `NGM_PCT`），优先引用 `ShippedOrderLine.ngmPct` 或在 DSL 注明 `"metric": "NGM_PCT"`。

---

## 模式 6：多步下钻 `query_plan`

根因分析、逐层 drill-down 时，先输出计划，再逐步执行。

### DSL（计划层，可选顶层字段）

```json
{
  "query_plan": [
    {
      "step": 1,
      "purpose": "Portfolio NGM% Feb vs Mar",
      "query_type": "object_aggregate",
      "object_type": "ShippedOrderLine",
      "period_slices": [ ... ],
      "aggregations": [ ... ]
    },
    {
      "step": 2,
      "purpose": "By VPC — period compare",
      "query_type": "object_aggregate",
      "object_type": "ShippedOrderLine",
      "joins": [{"link": "ShippedOrderLine_to_VendorProductLine"}],
      "group_by": [ ... ],
      "period_slices": [ ... ],
      "aggregations": [ ... ],
      "order_by": [{"property": "sales_delta", "direction": "DESC"}],
      "limit": 15
    },
    {
      "step": 3,
      "purpose": "By customer — March large deals",
      "query_type": "object_aggregate",
      "object_type": "ShippedOrderLine",
      "joins": [{"link": "ShippedOrderLine_to_Customer"}],
      "filters": [ ... ],
      "group_by": [ ... ],
      "aggregations": [ ... ],
      "having": [
        {"property": "net_sales", "operator": ">=", "value": 500000}
      ],
      "order_by": [
        {"property": "net_sales", "direction": "DESC"},
        {"property": "ngm_pct", "direction": "ASC"}
      ],
      "limit": 20
    }
  ]
}
```

每一步执行时仍须输出完整的四段产物（intent_json 可合并到 step 级）。

---

## 模式 7：`having` 聚合后过滤

### DSL

```json
"having": [
  {"aggregation_alias": "net_sales_mar", "operator": ">", "ref_alias": "net_sales_feb"},
  {"aggregation_alias": "ngm_pct_mar", "operator": "<", "ref_alias": "ngm_pct_feb"}
]
```

编译为 SQL `HAVING` 子句，仅引用已声明的 `aggregations` / `period_slices` alias。

---

## 合规自检（DSL 层）

在调用 MCP 前，对照 DSL 检查：

| 检查项 | 要求 |
|--------|------|
| SQL 有 `CASE WHEN` | DSL 必须有 `period_slices` |
| SQL 有 `TO_CHAR` | DSL `group_by` 必须有 `time_grain` |
| SQL 有 `<>` / `NOT IN` | DSL `filters` 必须有对应 operator |
| SQL 有 `JOIN` | DSL 必须有 `joins[].link`，且存在于 relations.yaml |
| SQL 有除法比率 | DSL 必须有 `function: RATIO` 或 metric 引用 |
| 多表查询 | 每步独立 DSL；不得一步 SQL 混写未声明逻辑 |
