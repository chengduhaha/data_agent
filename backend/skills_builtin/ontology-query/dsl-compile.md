# Object DSL → SQL 编译

基础编译规则见下文；**周期对比、时间粒度、跨对象 JOIN、比率、多步下钻**见 [dsl-patterns.md](dsl-patterns.md)。

## 0. 编译顺序（强制）

```
intent_json → Object Query DSL → 按 mapping 编译 SQL → Ontology trace → run_query_safely
```

## 1. 解析 object_type

```yaml
- id: Customer
  physical_source: dim_us.dim_pub_customer_info
  properties:
    - name: custNo
      mapping: cust_no
```

| DSL | YAML |
|-----|------|
| `object_type: Customer` | `id` |
| 表 | `physical_source` |
| `property: custNo` | `mapping: cust_no` |

### inline SQL（ShippedOrderLine）

```yaml
physical_source: SELECT ... calc_net_sales ... FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi WHERE segment_exclude ='N'
```

→ `FROM (SELECT ... ) AS hub`

## 2. object_search

```json
{
  "query_type": "object_search",
  "object_type": "Vendor",
  "filters": [{"property": "vendNo", "operator": "=", "value": 13208}],
  "select": ["vendNo", "vendName"],
  "limit": 50
}
```

```sql
SELECT vend_no AS vendNo, vend_name AS vendName
FROM dim_us.dim_pub_vendor_info
WHERE vend_no = 13208
LIMIT 50
```

## 3. object_aggregate

```sql
SELECT SUM(net_sales) AS total_net_sales
FROM (SELECT ... calc_net_sales AS net_sales ... FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi WHERE segment_exclude ='N') AS hub
WHERE date_flag BETWEEN '2025-12-01' AND '2026-02-28'
LIMIT 1
```

### 聚合函数

| function | SQL |
|----------|-----|
| COUNT | `COUNT(col)` |
| COUNT_DISTINCT | `COUNT(DISTINCT col)` |
| SUM | `SUM(col)` |
| AVG | `AVG(col)` |
| MIN / MAX | `MIN` / `MAX` |
| RATIO | `SUM(num) / NULLIF(SUM(den), 0)` — 见 [dsl-patterns.md](dsl-patterns.md) 模式 5 |

带 `group_by` → `GROUP BY <mapping>`；`time_grain` → `TO_CHAR`；`period_slices` → `CASE WHEN`；`order_by` + `limit` → Top N。

## 4. 嵌套 filter

```json
{
  "operator": "AND",
  "conditions": [
    {"property": "dateFlag", "operator": ">=", "value": "2025-12-01"},
    {"property": "dateFlag", "operator": "<=", "value": "2026-02-28"}
  ]
}
```

## 5. JOIN（relations.yaml）

```yaml
join_logic: ShippedOrderLine.custNo=Customer.custNo
```

解析两侧 mapping，编译为：

```sql
SELECT c.sales_terr_name, SUM(h.calc_net_sales) AS net_sales
FROM (SELECT ... FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi WHERE segment_exclude ='N') AS hub
JOIN dim_us.dim_pub_customer_info c ON hub.cust_no = c.cust_no
WHERE hub.date_flag BETWEEN '2025-12-01' AND '2026-02-28'
GROUP BY c.sales_terr_name
ORDER BY net_sales DESC
LIMIT 100
```

**未在 relations.yaml 声明的关系 → 禁止 JOIN。**

## 6. metrics.yaml 编译

示例 `NET_SALES`：

```yaml
physical_source:
  - type: table
    measure: ShippedOrderLine.netSales
dimensions:
  - name: salesTerr
    mapping: Territory.salesTerr
date:
  - name: dateFlag
    mapping: Date.dateFlag
```

→ 在 hub 表上 `SUM(net_sales)`，按 dimensions 做 GROUP BY，按 date 做时间 filter。

读 metric `description` 获取计算公式（如 NGM 的多项加总）。

## 7. Vertica 注意

- schema 限定：`dim_us.`、`dw_us.`
- 字符串单引号转义
- SELECT only + LIMIT

## 编译前检查（全部通过才可调用 MCP）

- [ ] 已先输出 `intent_json` 与 Object Query DSL（未跳过）
- [ ] 每个 property 在 object_type 上存在
- [ ] SQL 中无逻辑名泄漏（仅物理列名 / alias）
- [ ] 每个 `FROM` / `JOIN` 表来自某 `object_type.physical_source`
- [ ] 每个 SELECT / WHERE / GROUP BY 列来自某 `property.mapping` 或 metric measure
- [ ] 每个 JOIN 均有 `relations.yaml` 的 `join_logic` 依据
- [ ] `ShippedOrderLine` 使用 `objects.yaml` 声明的完整 inline `physical_source`，未自行改写
- [ ] 聚合匹配问题类型
- [ ] 有 LIMIT
- [ ] **未**调用 `get_table_structure` 等 schema 探查工具
- [ ] **未**手写任何无法追溯到本体的表名或列名
- [ ] SQL 含 `CASE WHEN` → DSL 含 `period_slices`（见 dsl-patterns.md）
- [ ] SQL 含 `TO_CHAR` → DSL `group_by` 含 `time_grain`
- [ ] SQL 含 `<>` / `NOT IN` → DSL `filters` 有对应 operator
- [ ] SQL 含比率除法 → DSL 含 `function: RATIO`
- [ ] 已输出 **Ontology trace** 对照表

## 禁止示例

以下均属**违规**，不得执行：

```sql
-- 禁止：未在本体声明的列或自行猜表
SELECT * FROM dw_us.some_unknown_table LIMIT 10

-- 禁止：DSL 未声明 period_slices 就写周期对比 CASE WHEN
SELECT dim_vpl_no, SUM(CASE WHEN date_flag >= '2026-02-01' ...) ...

-- 禁止：relations.yaml 未声明的 JOIN
FROM hub JOIN some_table s ON hub.foo = s.bar

-- 禁止：跳过 DSL 直接写 SQL（即使 SQL 元素可追溯到本体）
```

正确做法：先输出 intent_json + Object Query DSL（含 `period_slices` / `time_grain` / `joins` / `RATIO`），再编译 SQL，再输出 Ontology trace。详见 [dsl-patterns.md](dsl-patterns.md)。
