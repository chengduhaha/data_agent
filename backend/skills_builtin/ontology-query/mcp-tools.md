# MCP 数据库查询

Skill 通过 **官方 Vertica MCP** 执行 SQL，不内置数据库驱动或自研 MCP server。

## 前置条件

在 Cursor 中配置官方 Vertica MCP（HTTP gateway 或 stdio），凭证写在 `~/.cursor/mcp.json`，不写进 skill 文件。

在 **data_agent** 中，在用户 Settings → MCP 或 `workspace/{user}/mcp.json` 配置 Vertica MCP（如 `user-gateway-vertica-prod`），工具名 `run_query_safely`。

`domains/b_report/domain.yaml` 声明使用的工具名：

```yaml
mcp_tools:
  - run_query_safely
```

## 工具白名单 / 黑名单

### 允许（唯一查数入口）

| 工具 | 用途 |
|------|------|
| `run_query_safely` | 执行**从 Object Query DSL 编译**的 SELECT |

### 绝对禁止

以下 MCP 工具**不得调用**，即使用户要求或 SQL 报错也不得用其探库：

| 工具 | 禁止原因 |
|------|----------|
| `get_table_structure` | schema 探查 |
| `get_schema_tables` / `get_database_schemas` / `get_schema_views` | schema 探查 |
| `get_table_projections` | schema 探查 |
| `profile_query` | 元数据/探查 |
| `execute_query_paginated` / `execute_query_stream` | 非白名单；统一用 `run_query_safely` |
| `analyze_system_performance` / `generate_health_dashboard` / `database_status` | 与查数无关 |

本体 `objects.yaml` / `relations.yaml` / `metrics.yaml` 是**唯一**的 schema 来源。

## 工具调用

### run_query_safely

用于**从 DSL 编译**的 SELECT 查询，带行数限制与安全检查。

**输入：**

```json
{
  "query": "SELECT cust_no AS custNo, cust_name AS custName FROM dim_us.dim_pub_customer_info WHERE cust_no = 12345 LIMIT 10",
  "page_limit": 100,
  "include_columns": true
}
```

上例 SQL 必须由 `object_type: Customer`、`property: custNo` / `custName` 及 `physical_source` 编译而来，**不得**手写。

参数名是 `query`（不是 `sql`）。

## Agent 行为

1. 先读本体 → 输出 `intent_json` + Object Query DSL → 编译 SQL → 再调 `run_query_safely`
2. SQL 自带 LIMIT；工具可能再次限制行数
3. 错误时**仅可**修正 DSL 并重新编译；**禁止** schema 探查或手写非本体 SQL
4. 用返回的 rows 作答，不为排版重复查询

## 安全

- 仅 SELECT
- 仅 `run_query_safely`
- 凭证在 MCP server 配置中，不在 skill 内
- 默认 LIMIT 防大结果集
