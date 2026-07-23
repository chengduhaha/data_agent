# Ontology Query Skill

从 `az_ck_agent` ontology_agent 提取的**可移植查数 skill**：本体探索 + SQL 拼接 + MCP 查询。

当前主域：**b_report** v1.0.44（Vertica）

## 内容

```
ontology-query-skill/
├── SKILL.md
├── workflow.md
├── dsl-compile.md
├── dsl-patterns.md      # 强制四段输出、period_slices、time_grain、多步下钻
├── mcp-tools.md
├── examples.md
└── domains/b_report/
    ├── domain.yaml
    └── ontology/
        ├── objects.yaml      # v1.0.44
        ├── relations.yaml
        ├── metrics.yaml
        ├── main.yaml
        └── agent_query_workflow.md
```

## 安装

**Cursor：**

```bash
cp -r ontology-query-skill ~/.cursor/skills/ontology-query
```

**Claude Code：**

```bash
cp -r ontology-query-skill ~/.claude/skills/ontology-query
```

配置官方 Vertica MCP（如 `gateway-vertica-prod`），见 [mcp-tools.md](mcp-tools.md)。

## 使用

在任意支持 skill + MCP 的 agent 中：

1. 加载本 skill
2. 用户提问 b_report 相关问题
3. Agent 读本体 → 输出 intent_json + DSL + SQL + Ontology trace → **仅** `run_query_safely`

**约束**：禁止 schema 探查；禁止跳过 DSL 手写 SQL；`CASE WHEN`/`TO_CHAR`/比率须先在 DSL 声明。详见 [SKILL.md](SKILL.md)、[dsl-patterns.md](dsl-patterns.md)。

## 更新本体

从源仓库同步最新版本：

```bash
SRC=bigdata-onto-agent/ontology_agent/backend/app/domains/b_report/ontology/versions
cp $SRC/1.0.44/{objects,relations,metrics,main}.yaml \
   ontology-query-skill/domains/b_report/ontology/
```

## 新增域

复制 `domains/_template/`，填入 ontology YAML 和 `domain.yaml`。
