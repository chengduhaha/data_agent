# b_report 示例

每个示例均展示 **完整流程**：intent_json → Object Query DSL → Compiled SQL → MCP。  
扩展模式见 [dsl-patterns.md](dsl-patterns.md)。

---

## 1. 查客户名称（object_search）

**用户**：「客户编号 12345 的名称是什么？」

#### intent_json

```json
{
  "raw_question": "客户编号 12345 的名称是什么？",
  "query_kind": "lookup",
  "object_candidates": ["Customer"],
  "metric_candidates": [],
  "required_concepts": ["custNo 12345"],
  "aggregation": "none",
  "confidence": "high"
}
```

#### Object Query DSL

```json
{
  "query_type": "object_search",
  "object_type": "Customer",
  "filters": [{"property": "custNo", "operator": "=", "value": 12345}],
  "select": ["custNo", "custName"],
  "limit": 1
}
```

#### Compiled SQL

```sql
SELECT cust_no AS custNo, cust_name AS custName
FROM dim_us.dim_pub_customer_info
WHERE cust_no = 12345
LIMIT 1
```

#### Ontology trace

| SQL 元素 | 本体来源 |
|----------|----------|
| `dim_us.dim_pub_customer_info` | Customer.physical_source |
| `cust_no`, `cust_name` | Customer.custNo, Customer.custName |

---

## 2. FY26 Q1 净销售额（object_aggregate）

**用户**：「FY26 Q1 净销售额是多少？」

**域规则**：财年 Q1 = 2025-12-01 ~ 2026-02-28

#### intent_json

```json
{
  "raw_question": "FY26 Q1 净销售额是多少？",
  "query_kind": "metric",
  "object_candidates": ["ShippedOrderLine"],
  "metric_candidates": ["NET_SALES"],
  "required_concepts": ["FY26 Q1", "NET_SALES"],
  "aggregation": "sum",
  "confidence": "high"
}
```

#### Object Query DSL

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [
    {"property": "dateFlag", "operator": ">=", "value": "2025-12-01"},
    {"property": "dateFlag", "operator": "<=", "value": "2026-02-28"}
  ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "total_net_sales"}
  ],
  "limit": 1
}
```

---

## 3. PM 按 VPC 查 2025 收入与 NGM（top_n + joins）

**用户**：「我是 PM 706187，2025 年各 VPC 收入与 NGM，按收入降序、NGM 升序 Top 5」

#### intent_json

```json
{
  "raw_question": "PM 706187, 2025 revenue and NGM by VPC top 5",
  "query_kind": "top_n",
  "object_candidates": ["ShippedOrderLine", "VendorProductLine", "PM"],
  "metric_candidates": ["NET_SALES", "NGM"],
  "required_concepts": ["PM 706187", "2025", "VPC", "NET_SALES", "NGM"],
  "aggregation": "top_n",
  "confidence": "high"
}
```

#### Object Query DSL

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [
    {"property": "dimPmId", "operator": "=", "value": 706187},
    {"property": "dateFlag", "operator": ">=", "value": "2025-01-01"},
    {"property": "dateFlag", "operator": "<=", "value": "2025-12-31"}
  ],
  "joins": [{"link": "ShippedOrderLine_to_VendorProductLine"}],
  "group_by": [
    {"object_type": "VendorProductLine", "property": "vplNo", "alias": "vpc_no"},
    {"object_type": "VendorProductLine", "property": "vplDesc", "alias": "vpc_desc"}
  ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "revenue_2025"},
    {"function": "SUM", "property": "ngmAmt", "alias": "ngm_2025"}
  ],
  "order_by": [
    {"property": "revenue_2025", "direction": "DESC"},
    {"property": "ngm_2025", "direction": "ASC"}
  ],
  "limit": 5
}
```

#### Compiled SQL（结构示意）

```sql
SELECT vpl.vpl_no AS vpc_no, vpl.vpl_desc AS vpc_desc,
       SUM(hub.calc_net_sales) AS revenue_2025,
       SUM(hub.ngm_amt) AS ngm_2025
FROM (<ShippedOrderLine.physical_source>) AS hub
JOIN dim_us.dim_pub_vpl_info vpl ON hub.dim_vpl_no = vpl.vpl_no
WHERE hub.dim_pm_id = 706187
  AND hub.date_flag >= '2025-01-01' AND hub.date_flag <= '2025-12-31'
GROUP BY vpl.vpl_no, vpl.vpl_desc
ORDER BY revenue_2025 DESC, ngm_2025 ASC
LIMIT 5
```

---

## 4. PM NGM% 环比下降根因（comparison + 多步下钻）

**用户**：「PM 706187，3 月 NGM% 比 2 月低，从 cust / vend / order 找根因」

### Query 1：Portfolio Feb vs Mar NGM%

#### intent_json

```json
{
  "raw_question": "PM 706187 NGM% lower in March vs February",
  "query_kind": "comparison",
  "object_candidates": ["ShippedOrderLine", "PM"],
  "metric_candidates": ["NET_SALES", "NGM", "NGM_PCT"],
  "required_concepts": ["Feb 2026", "Mar 2026", "NGM%"],
  "aggregation": "ratio",
  "confidence": "high"
}
```

#### Object Query DSL

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

> `period_slices` 编译为 `CASE WHEN` 列；见 [dsl-patterns.md](dsl-patterns.md) 模式 1。

### Query 2：按 VPC 对比（joins + period_slices + having）

#### Object Query DSL（节选）

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [
    {"property": "dimPmId", "operator": "=", "value": 706187},
    {"property": "dateFlag", "operator": ">=", "value": "2026-02-01"},
    {"property": "dateFlag", "operator": "<=", "value": "2026-03-31"}
  ],
  "joins": [{"link": "ShippedOrderLine_to_VendorProductLine"}],
  "group_by": [
    {"object_type": "VendorProductLine", "property": "vplNo"},
    {"object_type": "VendorProductLine", "property": "vplDesc"}
  ],
  "period_slices": [ "...同上..." ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "net_sales", "per_period": true},
    {
      "function": "RATIO", "alias": "ngm_pct", "per_period": true,
      "numerator": {"function": "SUM", "property": "ngmAmt"},
      "denominator": {"function": "SUM", "property": "netSales"}
    }
  ],
  "having": [
    {"aggregation_alias": "net_sales_mar_2026", "operator": ">", "ref_alias": "net_sales_feb_2026"},
    {"aggregation_alias": "ngm_pct_mar_2026", "operator": "<", "ref_alias": "ngm_pct_feb_2026"}
  ],
  "order_by": [{"property": "net_sales_mar_2026", "direction": "DESC"}],
  "limit": 15
}
```

### Query 3：按客户 + 订单下钻（March 大单）

#### Object Query DSL（节选）

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
    {"link": "ShippedOrderLine_to_Customer"},
    {"link": "ShippedOrderLine_to_Vendor"}
  ],
  "group_by": [
    {"property": "orderNo"},
    {"property": "orderType"},
    {"object_type": "Customer", "property": "custNo"},
    {"object_type": "Customer", "property": "custName"},
    {"object_type": "Vendor", "property": "vendNo"},
    {"object_type": "Vendor", "property": "vendName"}
  ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "net_sales"},
    {"function": "SUM", "property": "ngmAmt", "alias": "ngm_amt"},
    {
      "function": "RATIO", "alias": "ngm_pct",
      "numerator": {"function": "SUM", "property": "ngmAmt"},
      "denominator": {"function": "SUM", "property": "netSales"}
    }
  ],
  "having": [{"aggregation_alias": "net_sales", "operator": ">=", "value": 500000}],
  "order_by": [
    {"property": "net_sales", "direction": "DESC"},
    {"property": "ngm_pct", "direction": "ASC"}
  ],
  "limit": 20
}
```

---

## 反例

| 错误 | 正确 |
|------|------|
| 读本体后直接写 SQL 调 MCP | 先输出 intent_json + DSL，再编译 SQL |
| SQL 有 `CASE WHEN` 但 DSL 无 `period_slices` | DSL 声明 `period_slices`，再编译 |
| SQL 有 `TO_CHAR` 但 DSL 无 `time_grain` | `group_by` 加 `"time_grain": "month"` |
| `cust_no <> 802609` 无 DSL 对应项 | `filters` 加 `{"property":"custNo","operator":"<>","value":802609}` |
| 返回 10 行就说「共 10 笔」 | `COUNT` 或 `SUM` 在 SQL 中 |
| 未声明关系自行 JOIN | DSL `joins` 引用 relations.yaml link 名 |
| LLM 手算 NGM 比率 | DSL `function: RATIO` 编译进 SQL |
