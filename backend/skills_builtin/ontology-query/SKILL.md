---
name: ontology-query
description: >-
  Query business data strictly via ontology YAML: read objects/metrics/relations,
  build Object Query DSL, compile SQL from mappings only, execute with
  run_query_safely. Never use schema-discovery MCP tools or hand-written SQL.
  Use for B-Report (b_report) profitability, net sales, NGM, P&L questions.
---

# Ontology Query Skill

**data_agent:** shared built-in skill at `/skills/builtin/ontology-query/`. Invoke with `/ontology-query` in chat. Independent of `contract-guided-data-analysis`.

三步核心流程：**本体探索 → DSL 构建 → SQL 编译 → MCP 查询**。

```
用户提问 → 读 ontology YAML → intent_json → Object Query DSL → 编译 SQL → Ontology trace → run_query_safely → 回答
```

**每一次 MCP 调用前必须输出四段产物**（见 [dsl-patterns.md](dsl-patterns.md)）：`intent_json` → `Object Query DSL` → `Compiled SQL` → `Ontology trace`。

## Quick Start（b_report）

In **data_agent**, prefix paths with `/skills/builtin/ontology-query/` (e.g. `/skills/builtin/ontology-query/domains/b_report/domain.yaml`).

1. Read [domains/b_report/domain.yaml](domains/b_report/domain.yaml) — Vertica + `run_query_safely`
2. Read [domains/b_report/ontology/](domains/b_report/ontology/) — `objects.yaml` v1.0.44, `relations.yaml`, `metrics.yaml`
3. Read [domains/b_report/ontology/agent_query_workflow.md](domains/b_report/ontology/agent_query_workflow.md)
4. Follow [workflow.md](workflow.md) and [dsl-patterns.md](dsl-patterns.md)

## Workflow Checklist

```
- [ ] 1. 解析意图 → intent_json（必须先输出）
- [ ] 2. 读 objects.yaml / metrics.yaml / relations.yaml 定位对象与属性
- [ ] 3. 应用 agent_query_workflow.md 域规则
- [ ] 4. 构建 Object Query DSL（必须先输出；仅用逻辑 property 名）
- [ ] 5. 按 dsl-compile.md 从 DSL 编译 Vertica SQL（禁止跳过 DSL 直接写 SQL）
- [ ] 6. 自检：SQL 中每个表/列可追溯到本体 mapping（见 dsl-compile.md）
- [ ] 7. MCP run_query_safely（唯一允许的查数工具；SELECT only + LIMIT）
- [ ] 8. 仅根据查询结果回答，禁止 LLM 算术
```

## Hard Rules

| Rule | Detail |
|------|--------|
| **禁止 schema 探查** | **绝对禁止** `get_table_structure`、`get_schema_tables`、`get_database_schemas`、`get_table_projections`、`get_schema_views`、`profile_query` 等一切数据库元数据/探查类 MCP 工具 |
| **禁止非本体 SQL** | **绝对禁止**跳过 Object Query DSL 手写 SQL；SQL 必须由 DSL + 本体 `physical_source` / `mapping` / `join_logic` 编译而来 |
| **必须先 DSL 后 SQL** | 每次查数、每一步下钻，均须先展示四段产物（见 [dsl-patterns.md](dsl-patterns.md)）再调 MCP |
| **SQL 扩展须 DSL 先行** | `CASE WHEN` 对比 → `period_slices`；`TO_CHAR` 按月 → `time_grain`；`<>` 排除 → `filters`；比率 → `function: RATIO` |
| 逻辑名 | filter 用 `custNo`，不用 `cust_no` 或 `dim_us.dim_pub_customer_info` |
| 禁止 LLM 算术 | COUNT/SUM/比率必须在 SQL 中完成 |
| 禁止行数当总数 | 标量问题用 `object_aggregate` |
| SELECT only | MCP 只读；**仅** `run_query_safely` |
| 必须 LIMIT | 列表默认 100 |
| JOIN 限声明关系 | 只用 `relations.yaml` 中的 `join_logic` |
| 本体缺失即停 | 所需 object/property/relation 在本体中不存在时，**告知用户**并停止；**不得**探库补全 |

## Intent JSON

```json
{
  "raw_question": "<用户原话>",
  "query_kind": "lookup | list | aggregate | metric | comparison | top_n | unknown",
  "object_candidates": ["ShippedOrderLine", "Customer"],
  "metric_candidates": ["NET_SALES", "NGM"],
  "required_concepts": ["Q1 2026", "NET_SALES"],
  "aggregation": "none | count | sum | avg | ratio | top_n",
  "confidence": "high | medium | low"
}
```

## Object Query DSL

### 列表 / 明细

```json
{
  "query_type": "object_search",
  "object_type": "Customer",
  "filters": [{"property": "custNo", "operator": "=", "value": 12345}],
  "select": ["custNo", "custName", "salesTerrName"],
  "limit": 50
}
```

### 聚合 / 标量

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
  ]
}
```

### 带 GROUP BY

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [...],
  "group_by": ["salesTerr"],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "net_sales"}
  ],
  "order_by": [{"property": "net_sales", "direction": "DESC"}],
  "limit": 20
}
```

编译规则：[dsl-compile.md](dsl-compile.md) · 扩展模式：[dsl-patterns.md](dsl-patterns.md)

### 周期对比（Feb vs Mar）

```json
{
  "query_type": "object_aggregate",
  "object_type": "ShippedOrderLine",
  "filters": [{"property": "dimPmId", "operator": "=", "value": 706187}],
  "period_slices": [
    {"label": "feb_2026", "filters": [{"property": "dateFlag", "operator": ">=", "value": "2026-02-01"}, {"property": "dateFlag", "operator": "<=", "value": "2026-02-28"}]},
    {"label": "mar_2026", "filters": [{"property": "dateFlag", "operator": ">=", "value": "2026-03-01"}, {"property": "dateFlag", "operator": "<=", "value": "2026-03-31"}]}
  ],
  "aggregations": [
    {"function": "SUM", "property": "netSales", "alias": "net_sales", "per_period": true},
    {"function": "RATIO", "alias": "ngm_pct", "per_period": true,
      "numerator": {"function": "SUM", "property": "ngmAmt"},
      "denominator": {"function": "SUM", "property": "netSales"}}
  ]
}
```

### 跨对象分组 + JOIN

```json
{
  "joins": [{"link": "ShippedOrderLine_to_Customer"}],
  "group_by": [
    {"object_type": "Customer", "property": "custNo"},
    {"object_type": "Customer", "property": "custName"}
  ]
}
```

### 排除过滤

```json
{"property": "custNo", "operator": "<>", "value": 802609}
```

## MCP

```json
{"query": "SELECT ... LIMIT 100", "page_limit": 100, "include_columns": true}
```

工具名：`run_query_safely`（见 domain.yaml；需已配置官方 Vertica MCP）

详情：[mcp-tools.md](mcp-tools.md)

## b_report 关键对象

| 对象 | 用途 |
|------|------|
| `ShippedOrderLine` | Hub：订单行、净销售额、毛利 |
| `Customer` / `MasterCustomer` | 客户 |
| `Vendor` / `Part` | 供应商、SKU |
| `Territory` / `Division` | 区域、事业部 |
| `NET_SALES` / `NGM` | metrics.yaml 预定义指标 |

## Resources

- [workflow.md](workflow.md) — 逐步工作流
- [dsl-compile.md](dsl-compile.md) — DSL → SQL 基础编译
- [dsl-patterns.md](dsl-patterns.md) — **强制输出格式、period_slices、time_grain、joins、多步下钻**
- [mcp-tools.md](mcp-tools.md) — MCP 配置
- [examples.md](examples.md) — 完整 intent → DSL → SQL 示例
- [README.md](README.md) — 安装说明
