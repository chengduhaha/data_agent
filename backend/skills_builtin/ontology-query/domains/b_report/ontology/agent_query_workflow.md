# B-Report 经营报表域 — 查数工作流

本域 **Vertica** 查数：**读本体 YAML → 拼 Object DSL → 编译 SQL → MCP `run_query_safely`**。

## 域模型要点

- **中心对象**：`ShippedOrderLine`（已发货订单行，hub 表）
- **主数据**：`Customer`、`MasterCustomer`、`Vendor`、`Part`、`Territory`、`Division` 等
- **人员/项目**：`PM`、`PMManager`、`BDProject` 等，经 `relations.yaml` 与 hub 关联
- **指标**：`metrics.yaml` 中 `NET_SALES`、`NGM` 等，measure 多在 `ShippedOrderLine` 上

`ShippedOrderLine.physical_source` 是 inline SQL（含 `calc_net_sales`、`NGM_PCT` 等计算列），编译时用 `FROM (<inline_sql>) AS hub`。

## 必做顺序

1. **读本体**：`objects.yaml` 匹配 `object_type`；`metrics.yaml` 匹配指标名；`relations.yaml` 确认 JOIN 是否已声明。
2. **构建 intent_json**：含 `raw_question`、`query_kind`、`object_candidates`、`metric_candidates`、`required_concepts`（**必须先输出**）。
3. **构建 Object Query DSL**：仅用逻辑 `property` 名（**必须先输出，禁止跳过**）。
4. **编译 SQL**：按 skill `dsl-compile.md` 从 DSL 编译；引擎 Vertica；**禁止手写非本体 SQL**。
5. **MCP 执行**：**仅** `run_query_safely`，SELECT only + LIMIT（参数名 `query`）。

## 绝对禁止

- 调用 `get_table_structure`、`get_schema_tables` 等任何数据库 schema/元数据探查 MCP 工具
- 跳过 Object Query DSL 直接写 SQL
- 使用本体未声明的表、列、JOIN
- 为排错或补全信息而探库；本体缺失时告知用户并停止

## 财季

用户说「Q1 2026」「FY26 Q1」时，**默认财年 Q1** = 上一自然年 12 月 + 当年 1–2 月。勿反问日历年 Q1（1–3 月），除非用户明确要求 calendar quarter。

时间过滤用 `ShippedOrderLine.dateFlag` 或 `Date.dateFlag`（见 metrics.yaml `date` 段）。

## 标量 / 比率 / 排名

「多少」「总额」「环比」「Top N」「各销售区净销售额」→ `object_aggregate` 或按 `metrics.yaml` 编译 metric SQL。

- `NET_SALES`：measure = `ShippedOrderLine.netSales`（或 inline SQL 中的 `calc_net_sales`）
- `NGM`：margin 相关，见 metric `description` 中的公式

禁止用列表行数或 LLM 除法代替 SQL 聚合。

## JOIN 规则

- **仅**使用 `relations.yaml` 中已声明的 `join_logic` 做 JOIN
- 未声明关系时：**不要**凭物理表同名字段自行 JOIN；改分步查询或告知用户关系未定义
- `ShippedOrderLine` 连维表：查 `relations.yaml` 中 `from: ShippedOrderLine` 或 `to: ShippedOrderLine` 的 link

## 列表示例（各销售区净销售额）

一次 `object_aggregate`：

- `object_type`: `ShippedOrderLine`
- `group_by`: 区域属性（如 `salesTerr` 或经 JOIN `Territory.salesTerrName`）
- `aggregations`: `SUM` on `netSales` 或 metric `NET_SALES`
- 加用户时间 filter

用返回行作答，不要为了展示再查 Top N。

## 回答

所有数字必须来自 MCP 查询结果；Markdown 仅做简短解读。

## DSL → SQL 强制流程

每一次 MCP 调用前必须输出（见 skill [dsl-patterns.md](../../../dsl-patterns.md)）：

1. intent_json  
2. Object Query DSL  
3. Compiled SQL  
4. Ontology trace  

根因分析等多步下钻：每步独立一套四段产物。SQL 中的 `CASE WHEN` / `TO_CHAR` / 排除过滤 / 比率 **必须**在 DSL 中先声明。
