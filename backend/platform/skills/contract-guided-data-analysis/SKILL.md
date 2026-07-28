---
name: contract-guided-data-analysis
description: >
  Contract-first business data analysis: resolve KPIs, rankings, trends, comparisons,
  variance drivers, and POS/B Report metrics from local contracts and WKB knowledge,
  then run aggregate-only Vertica SQL for evidence. Use when the user asks for revenue,
  margin, NGM, POS metrics, B Report numbers, KPI lookup, ranking, trend, comparison,
  validate numbers, or data anomaly investigation. Do NOT use for ETL change requests,
  flow edits, DDL/DML, unrestricted warehouse exploration, or email/ticket intake.
---

# Contract-Guided Data Analysis

Answer business data questions using **bundled contracts + WKB index + knowledgebase**, then **Vertica MCP** for aggregated evidence only.

**Skill root:** all paths below are relative to the directory containing this `SKILL.md`.

## When to use

- User asks about KPIs, rankings, trends, comparisons, variance drivers, or POS/B Report metrics
- User wants to validate a business number, or look up margin / revenue / NGM
- User mentions metrics under business entities such as customer, vendor, order, SKU, PMID

**Do not use this skill for:**

- ETL changes, flow edits, DDL/DML
- Unrestricted warehouse exploration
- Email/ticket-style ETL impact analysis (use a dedicated intake skill)

## Prerequisites

1. Install this skill package (unzip into the agent’s skills directory)
2. Configure **Vertica MCP** (see [`references/mcp-setup.md`](references/mcp-setup.md))
3. Python 3.9+ (required only for WKB retrieval scripts)

## Workflow

Policy lives in [`references/_manifest.yaml`](references/_manifest.yaml) — load only references for the current stage.

| Stage | Responsibility |
|-------|----------------|
| `read_question` | Intent, domain cue, `query_spec`, temporal obligation; ambiguity handling via [`references/analysis-clarification.md`](references/analysis-clarification.md) |
| `local_research` | Local-first gate; forbidden MCP discovery |
| `resolve_domain` | Contract paths for resolved domain |
| `golden_cases_match` | **Disabled by default** — see [`references/golden-cases-match.md`](references/golden-cases-match.md); only consult `eval/golden_cases.md` when the user explicitly asks |
| `special_logic_check` | `knowledge/ref/{domain}/special_logic.txt` etc. |
| `plan_queries` | Metric/table routing, SQL plan, fiscal time |
| `retrieve_tables` | WKB short-list → ≤3 knowledgebase table sections |
| `compile_sql` | Local column catalog only; gate before MCP |
| `execute_evidence` | Vertica `run_query_safely` aggregate-first |
| `synthesis` | Three-section answer or **no data found** |
| `write_analysis` | Persist analysis markdown (optional; path configurable) |

### Routing steps

0. **Clarification gate** — ask **only** when the question or data has a genuine ambiguity that blocks routing (time when `user_must_specify`, unresolved business term, true entity/metric name clash, vague “item” with multiple pack meanings, ranking sense when baseline is undefined and material). If clear enough to proceed, **do not ask**. When blocked: ask first and **stop** ([`references/analysis-clarification.md`](references/analysis-clarification.md); [`references/output-contract.md`](references/output-contract.md) § Ambiguity Handling). Do **not** ask for breakdown dimension on attribution / root-cause — proceed with multi-angle exploration (`pipeline_mode=diagnose`) unless another hard slot is open. Do not invent “less” = top-N lowest. Fiscal year+quarter labels (e.g. `2026 Q1`) follow [`references/fiscal-calendar.md`](references/fiscal-calendar.md).
1. Classify intent + domain — [`references/question-shape.md`](references/question-shape.md)
2. **Local research gate** — no Bitbucket/Vertica metadata until routing complete
3. `knowledge/contracts/{domain}/domain-knowledge.md`
4. `knowledge/contracts/{domain}/metric-index.md`
5. `knowledge/contracts/{domain}/eval/golden_cases.md` — **skip by default** (disabled; see [`references/golden-cases-match.md`](references/golden-cases-match.md)); only consult when the user explicitly asks to use golden cases
6. Special logic — [`references/special-logic-check.md`](references/special-logic-check.md) → `knowledge/ref/{domain}/`
7. WKB retrieval — [`references/wkb-retrieval.md`](references/wkb-retrieval.md) → `python scripts/wkb_query.py`
8. Knowledgebase — `knowledge/knowledgebase/{domain}/{stem}.md` (L2/L3/L6); **NEVER** read `knowledge/contracts/{domain}/tables/*.md`
9. Compile SQL from local contracts; cannot compile → **no data found**. When intent is `rds_report_generation` (RDS SQL / report generation, not KPI-only lookup), load [`references/rds-report-sql.md`](references/rds-report-sql.md) as a mode pointer before compiling.
10. Entity Phase-1 (if labels) — [`references/entity-resolution.md`](references/entity-resolution.md)
11. Execute — [`references/vertica-query.md`](references/vertica-query.md)
12. Synthesize — [`references/output-contract.md`](references/output-contract.md)
13. Write (optional) — [`references/analysis-output.md`](references/analysis-output.md)

Clarification policy: [`references/analysis-clarification.md`](references/analysis-clarification.md)

## Knowledge layout

```
knowledge/
├── contracts/{domain}/     # domain-knowledge.md, metric-index.md, eval/
├── ref/{domain}/           # special_logic.txt, table list.txt, ...
├── knowledgebase/{domain}/ # per-table L1–L6 docs
└── storage/wkb/            # l1_catalog JSON + retrieval indexes
```

### Source priority

1. `knowledge/contracts/{domain}/domain-knowledge.md`
2. `knowledge/contracts/{domain}/metric-index.md`
3. `knowledge/contracts/{domain}/eval/golden_cases.md` — **disabled by default, do not consult unless the user explicitly asks** (see [`references/golden-cases-match.md`](references/golden-cases-match.md)); never `golden-questions.md`
4. `knowledge/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt`
5. `knowledge/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` via `scripts/wkb_query.py`
6. `knowledge/knowledgebase/{domain}/*.md`

**NEVER** read `knowledge/contracts/b-report-us/tables/**` or `knowledge/contracts/pos/tables/**`.

**No cross-domain fallback.** Missing routing or empty Vertica → **no data found** with scope.

## How to use

### WKB retrieval

```bash
# From skill root
python scripts/wkb_query.py \
  --query "<metric> <entity> <table cue>" \
  --intent nl2sql_metric \
  --prefilter-k 200 \
  --per-layer-k 8
```

Rebuild indexes after a knowledge update:

```bash
python scripts/wkb_index_builder.py
```

### Vertica execution

- Server: configure per [`references/mcp-setup.md`](references/mcp-setup.md)
- Allowed: `run_query_safely` (aggregate-first), bounded dim probe `LIMIT 20`
- Forbidden: schema discovery tools, exploratory `SELECT *`
- Full rules: [`references/vertica-rules.md`](references/vertica-rules.md)

### Governance red lines

See [`references/local-research-first.md`](references/local-research-first.md):

- Never read `golden-questions.md`
- Never use Bitbucket or Vertica metadata for discovery
- Never read contract `tables/*.md` tree

## Notes / edge cases

- Clarify **only** when question/data ambiguity blocks routing (see `analysis-clarification.md`); for attribution questions do not ask for breakdown — use `pipeline_mode=diagnose`; never ask the user for table names or formulas
- When time range is missing, follow `temporal_obligation` from `question-shape.md`
- Zero-row results → **no data found**; do not fall back across domains
- If the agent supports chat output only (no file write): skip `write_analysis` and emit the three-section structure in the conversation

## Output format

Three sections (see [`references/output-contract.md`](references/output-contract.md)):

1. **Summary**
2. **Evidence**
3. **Analysis approach & confidence**

- `result_status: data_found | no_data_found`
- Cite `metric-index.md` paths
- No raw SQL in the three sections (SQL may appear in appendix if agent supports it)

Optional file output: `{output_dir}/{slug}_{YYYYMMDD}.md` (default `{output_dir}` = skill root / `output/`). `write_analysis` never writes under wiki `target/analysis/**` — that path is outside this skill.

## Additional references

- Progressive load manifest: [`references/_manifest.yaml`](references/_manifest.yaml)
- Install guide: [`INSTALL.md`](INSTALL.md)
- Pack metadata: [`pack.yaml`](pack.yaml)
