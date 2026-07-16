<!-- Local copy for contract-guided-data-analysis. Paths adapted to source/contracts. Do not depend on external skill trees. -->

# Confidence and Provenance

## Purpose

Every final answer must help the business user understand:

- what was answered;
- what data source was used;
- how time was resolved;
- how reliable the answer is;
- what assumptions or limitations apply.

---

## Source Tier

Classify the answer source tier:

| Tier | Meaning | Confidence implication |
|------|---------|------------------------|
| `deterministic_metric_tool` | Answer came from a deterministic metric/planner tool with KB-certified logic. | High if inputs resolved. |
| `routing_certified_golden` | Answer used routing-certified golden SQL or certified pattern. | High if scope matches. |
| `curated_kb_table` | Answer used active-pack table docs and approved metric logic. | Medium to high depending on ambiguity. |
| `repaired_known_table_sql` | SQL was repaired within the same KB strategy. | Medium unless repair was trivial and verified. |
| `inferred_due_to_kb_gap` | Part of the answer required model inference because KB lacked deterministic support. | Medium/low. |
| `unsupported` | Active pack cannot support the request. | Refuse or clarify. |

---

## Time Scope Disclosure

The final answer must disclose how time was resolved.

### User-specified time

Chinese:

`时间范围：用户指定了 <period>。`

English:

`Time scope: user specified <period>.`

### Relative anchored time

Chinese:

`时间范围：将"<relative expression>"根据数据新鲜度锚点解析为 <period>。`

English:

`Time scope: "<relative expression>" was resolved to <period> using the data freshness anchor.`

### KB-assembled default time

Chinese:

`时间范围：用户未明确给出时间；根据当前知识包的认证默认周期，使用 <business period label>。`

English:

`Time scope: the user did not specify a period; the active knowledge pack's certified default period was used: <business period label>.`

### Clarification required

Chinese:

`需要先确认时间范围，因为当前知识包没有为该问题定义可安全使用的默认业务周期。`

English:

`A time range is needed because the active knowledge pack does not define a safe default period for this question.`

---

## Confidence Statements

### High confidence

Use when:

- metric definition is KB-certified;
- table role and grain match;
- entity and time are resolved;
- evidence SQL executed successfully;
- no material KB gaps.

Chinese:

`信心：高。指标定义、表粒度、实体范围和时间范围均由当前知识包认证，并由执行结果支持。`

English:

`Confidence: high. Metric definition, table grain, entity scope, and time scope are certified by the active knowledge pack and supported by executed evidence.`

### Medium confidence

Use when:

- SQL was repaired but strategy remained the same;
- minor ambiguity was resolved by documented defaults;
- default period was KB-certified but not user-specified.

Chinese:

`信心：中。结论由当前知识包和执行结果支持，但包含已披露的默认假设或轻微修复。`

English:

`Confidence: medium. The conclusion is supported by the active knowledge pack and executed evidence, but includes disclosed default assumptions or minor repairs.`

### Medium/low confidence

Use when:

- typo correction was applied;
- KB lacks deterministic support for part of the interpretation;
- attribution relies on observed contribution rather than causal proof.

Chinese:

`信心：中/偏低。部分解释依赖模型推断或存在已披露的不确定性。`

English:

`Confidence: medium/low. Part of the interpretation relies on model inference or disclosed uncertainty.`

---

## Typo Correction Disclosure

If typo correction was applied:

Chinese:

`模型已自动更正疑似拼写：<original> → <corrected>。结论可能与用户输入的字面含义存在偏差。`

English:

`The model auto-corrected suspected typo(s): <original> → <corrected>. Results may differ from the exact wording entered by the user.`

Confidence must not be high when typo correction was applied.
