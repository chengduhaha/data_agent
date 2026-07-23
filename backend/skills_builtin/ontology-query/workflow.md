# Workflow: 本体探索 → DSL 构建 → SQL 编译 → MCP 查询

## Step 0: 强制输出格式（每次 MCP 前）

见 [dsl-patterns.md](dsl-patterns.md)。每一次 `run_query_safely` 前必须输出：

1. **intent_json**
2. **Object Query DSL**（完整 JSON）
3. **Compiled SQL**
4. **Ontology trace**（SQL 元素 → 本体来源对照表）

多步下钻：Query 1、Query 2… 各有一套四段产物。**禁止**合并为一次 SQL 或跳过 DSL。

## Step 1: 本体探索

读 `domains/b_report/ontology/`：

| 文件 | 用途 |
|------|------|
| `objects.yaml` | `objects_type_entities[].id` = object_type；`properties[].name` = 逻辑属性；`mapping` = 物理列（编译时用） |
| `relations.yaml` | `links[].join_logic` = JOIN 条件 |
| `metrics.yaml` | `metrics[].name`、measure、dimensions、filter、date |
| `main.yaml` | 版本与域描述 |
| `agent_query_workflow.md` | 域业务规则 |

探索策略：

1. 从用户问题提取实体词（客户、供应商、净销售额、区域…）
2. 在 `objects.yaml` 搜索匹配的 `id` 和 `description`
3. 指标类问题先查 `metrics.yaml`（如 `NET_SALES`、`NGM`）
4. 跨对象问题查 `relations.yaml` 是否有声明 link
5. **不要**通读整个 YAML；按关键词定位相关段落即可

### b_report hub 模型

大多数事实查询围绕 **`ShippedOrderLine`**：

- `physical_source` 是 inline SELECT（含 `calc_net_sales`、`NGM_PCT` 等）
- 维表（Customer、Vendor、Territory…）通过 `relations.yaml` 与 hub JOIN

## Step 2: 构建 Object Query DSL（强制，不可跳过）

**必须先输出完整 Object Query DSL，再进入 Step 3。** 禁止根据经验或猜测直接写 SQL。

仅用逻辑层：

- `object_type` ← `objects_type_entities[].id`
- `property` ← `properties[].name`
- 禁止在 DSL 中出现 `mapping`、`physical_source`

若无法从用户问题映射到已声明的 `object_type` / `property` / `join_logic`，停止并告知用户，**禁止**调用任何 MCP 工具探库。

扩展 DSL 字段见 [dsl-patterns.md](dsl-patterns.md)：

| 用户意图 | DSL 字段 |
|----------|----------|
| Feb vs Mar、同比 | `period_slices` |
| 按月/年分组 | `group_by[].time_grain` |
| 排除某客户/供应商 | `filters` + `operator: "<>"` |
| 按客户名/VPC 描述分组 | `joins` + `group_by[].object_type` |
| NGM% 等比率 | `function: RATIO` |
| 根因多步下钻 | `query_plan` 或分步 Query 1/2/3 |

### query_kind 路由

| 用户信号 | query_kind |
|----------|------------|
| 查某个 ID/名称 | lookup |
| 列出、哪些 | list |
| 多少、总额 | aggregate |
| 净销售额、NGM | metric |
| Top N、排名最高 | top_n |
| A vs B | comparison |

## Step 3: 编译 SQL（仅允许从 DSL 编译）

见 [dsl-compile.md](dsl-compile.md) 与 [dsl-patterns.md](dsl-patterns.md)。

**禁止手写非本体 SQL。** SQL 中的每个元素必须有本体来源：

1. `object_type` → `physical_source`（表名或 inline SQL 子查询）
2. `property` → `mapping`（列名）
3. `relations.yaml` → JOIN
4. `metrics.yaml` → SUM/COUNT 表达式与 filter
5. Vertica 方言；schema 前缀如 `dim_us.`、`dw_us.`
6. inline SQL 的 `physical_source`：`FROM (<sql>) AS hub`（必须使用 `objects.yaml` 中声明的完整 inline SQL，不得改写或裁剪）

编译后执行 [dsl-compile.md](dsl-compile.md) 中的「编译前检查」；任一项不通过则不得调用 MCP。

## Step 4: MCP 查询

**唯一允许的查数工具：`run_query_safely`。**

**绝对禁止**调用以下 MCP 工具（及同类 schema/元数据探查工具）：

- `get_table_structure`
- `get_schema_tables` / `get_database_schemas` / `get_schema_views`
- `get_table_projections`
- `profile_query`
- `analyze_system_performance` / `generate_health_dashboard` / `database_status`

执行步骤：

1. 调用 `run_query_safely`，传入**从 DSL 编译**的 SELECT（参数名 `query`）
2. 失败时仅可修正 DSL 并重新编译；**禁止**为排错去探库或手写新 SQL
3. 空结果如实告知

## Step 5: 回答

- 数字必须来自 MCP 返回的 rows
- 多列用 Markdown 表格
- 说明用了哪个 object_type、哪些 filter；可引用 Ontology trace
- 不编造、不手算比率

## 合规自检（回答前）

| 维度 | 要求 |
|------|------|
| 禁止 schema 探查 | 仅 `run_query_safely` |
| SQL 可追溯本体 | 每列有 mapping / join_logic 来源 |
| 先 DSL 后 SQL | 本次每个 Query 均已输出四段产物 |
| SQL 扩展合规 | 有 `CASE WHEN` → 有 `period_slices`；有 `TO_CHAR` → 有 `time_grain` |

## 何时追问用户

- 时间范围真正歧义且域规则无默认
- 多个 object_type 同等匹配且无法从上下文判断
- 需要 JOIN 但 `relations.yaml` 无声明关系

**不要**追问：财年 Q1（b_report 默认财年历）、「本月」「最近 7 天」等可推理的时间。
