<!-- Local copy for contract-guided-data-analysis. Paths adapted to source/contracts. Do not depend on external skill trees. -->

## Intent Recognition and Classification

Classify each request into one of:

- Metric lookup (single KPI value)
- Metric comparison (period, segment, entity)
- Trend/time series
- Ranking/top-N
- Diagnostic slice (dimension breakdown)
- Attribution/root-cause analysis (why changed, what drove movement)
- Unsupported/out-of-KB

If category is unsupported/out-of-KB, reject.

Intent routing policy:

1. Factual-data questions:
   - focus on direct metric retrieval/comparison/trend/ranking output;
   - keep response in the standard three-section business format (see Output Contract).
2. Attribution questions:
   - do not stop at one-layer descriptive comparison;
   - perform multi-angle exploration and progressive drill-down until:
     - a most likely root cause is identified with evidence, or
     - KB boundary is reached and further causal confirmation is unsupported.

## Ambiguity Handling

Ask clarification only when ambiguity materially changes the answer and cannot be resolved by the active knowledge pack.

### Time Ambiguity

Do not automatically ask for time just because the user omitted a time expression.

Use `temporal_obligation` from [question-shape.md](./question-shape.md).

| temporal_obligation | Behavior |
|---------------------|----------|
| `user_already_specified` | Parse and apply the user's explicit time. Ask only if the expression has multiple plausible meanings that CIS calendar policy cannot resolve. |
| `kb_anchor_resolve` | Resolve relative time using CIS fiscal calendar, data freshness, runtime anchor, selected table max date, and active pack Time Scope Ontology. Do not ask for a year merely because the user said "last month" or similar. |
| `kb_default_eligible` | Do not ask for time in Stage-1. Stage-2 must verify whether the active pack provides certified default period assembly. Ask for time only if no safe KB default exists. |
| `user_must_specify` | Ask a concise time clarification before evidence SQL. |

### Time clarification must not mask other issues

Do not ask for time when the real issue is:

- invalid entity;
- ambiguous entity;
- missing metric definition;
- missing table routing;
- unsupported attribution;
- out-of-scope request.

### Other ambiguities

Ask clarification before querying when any of these is ambiguous:

- metric name/definition
- grain (daily/weekly/monthly/QTD/YTD)
- geography/region scope
- entity scope (customer, vendor, BD rep, buyer, etc.)
- currency/unit

Do not guess when ambiguity can materially change metric definition or results.

### Examples

Good:

`请确认要分析的时间范围，例如最近一个月、某个财政季度或某个财年。`

Bad:

`请提供年份。`

when the user said "上个月" and a freshness anchor exists.

Bad:

`请提供时间范围。`

when the question is an entity-scoped scalar KPI eligible for KB default assembly.

## Analysis Workflow

1. Validate scope against KB (reject if out-of-scope).
2. Classify intent.
3. Resolve metric and table path from KB (`metric-index.md` then table docs).
4. Check ambiguity; ask follow-up if needed.
4b. When `entity_filters` are present, run Entity Scope Pre-Validation Phase-1 (dim/label validation) before fact metric SQL.
5. Run pre-SQL metric-column validation:
   - Confirm whether each required metric is stored physically or defined logically in the selected table.
   - Finalize SQL references accordingly (direct column vs formula expression) before execution.
6. Route by intent:
   - Factual-data path:
     1. Build one final SQL that matches approved metric logic and grain.
     2. Execute SQL on Vertica MCP (or Hive MCP only when Vertica unavailable).
   - Attribution path:
     1. Define the target change signal (what changed, between which periods/entities).
     2. Generate candidate explanatory angles from KB-supported dimensions only (for example customer, vendor, region, product line, sales motion).
     3. Run evidence queries by angle and rank contribution/impact.
     4. Drill down layer by layer on top contributors until root cause is stable or KB support runs out.
     5. For each inference step, keep explicit evidence linkage (metric movement -> slice decomposition -> narrowed driver).
     6. Stop when additional drill-down no longer changes conclusion materially.
7. Format response with the fixed output contract below.

Executed SQL is appended automatically by the data_agent chat UI under **## Vertica validation** after your answer. Do **not** duplicate SQL in Summary, Evidence, or Analysis approach & confidence — you may reference "see Vertica validation below".

## Response Language

Match the user's question language in every user-facing part of the answer and thought-process trace.

- **Chinese question** (contains CJK characters): write in Simplified Chinese. Section headings: **摘要**, **证据**, **分析思路与信心**.
- **English question** (no CJK): write in English. Section headings: **Summary**, **Evidence**, **Analysis approach & confidence**.
- **Mixed Chinese + English**: default to Chinese (typically Chinese-primary); preserve English metric/table codes in evidence.

## Output Contract (Fixed)

User-facing answers must focus on business-readable content. **Do not include SQL** in the three main sections — the platform appends executed queries automatically at the end of the chat message under **## Vertica validation** (wiki-style fenced `sql` blocks).

### Standard answer structure (all intents)

Use exactly these three sections (markdown headings recommended):

1. **Summary** — Plain-language conclusion that directly answers the question.
   - Write for a business reader, not a data engineer.
   - Lead with the takeaway; avoid column names and SQL jargon unless the user used them.
   - Attribution: state the current best root-cause judgment here.

2. **Evidence** — Concrete numbers that support the summary.
   - Single scalar: show key metric values clearly (inline or short bullet list).
   - Ranking / diagnostic slice with 2+ rows: **markdown table** (required).
   - Period comparison / trend: show compared values and delta where relevant.
   - Attribution: show the decomposition chain — baseline movement, top contributing slices, narrowed driver(s).

3. **Analysis approach & confidence** — How this answer was derived, in **business language** a non-technical stakeholder can follow, plus confidence.
   - **Start with question understanding**: restate what the user is asking in plain language (your final interpretation of the question).
   - **State the business intent** (metric lookup, comparison, ranking, breakdown, attribution) — not pipeline/node names.
   - **Explain scope**: metrics, entity/filter scope, and time period in business terms.
   - **Explain the data path**: which knowledge-pack business context was used, which certified **business data table** was queried (table name is fine; briefly say what it contains), and what the query returned.
   - If typo auto-correction was applied, state the original vs corrected token(s) and warn the answer may differ from the user's exact wording ([typo-tolerance.md](./typo-tolerance.md)).
   - Disclose how time was resolved (see Time Scope Disclosure below).
   - End with a confidence statement per [confidence-provenance.md](./confidence-provenance.md).
   - **Do NOT** describe IT execution steps (KB retrieval, planner, entity-slot extraction, SQL repair, reflection, MCP, trace steps, node names).
   - **UI note:** clients render this section in subdued styling (smaller gray text) as supplementary context, not part of the primary business answer. Keep the section title line exactly `**Analysis approach & confidence**` on its own line for reliable parsing.

### Do NOT include in user-facing answers

- SQL queries in Summary / Evidence / Analysis approach & confidence (fenced blocks, "SQL used", "Executed SQL", or similar) — the platform adds **## Vertica validation** automatically
- Trial/error or intermediate SQL in the main answer body
- Raw warehouse/MCP tooling references unless the user explicitly asked

### Intent-specific notes

- **metric_lookup / metric_comparison / trend**: Summary + Evidence + Analysis approach & confidence.
  - **metric_lookup with one entity / one aggregated row**: present key metrics inline or as short bullets in Evidence.
  - **metric_lookup with multiple entities or multiple evidence rows** (e.g. two people named in the question): use a **markdown table** in Evidence with entity label column(s) plus each resolved metric.
  - Let executed evidence row count and columns drive layout; do not assume a fixed row count.
- **ranking / diagnostic_slice**: Evidence section must use a markdown table when 2+ rows.
  - **Row-list / top-N** (evidence SQL has no `GROUP BY`): preserve all identifier and metric columns returned by the executed SQL in the Evidence table; do not collapse to a single breakdown dimension.
  - **Aggregated breakdown** (evidence SQL includes `GROUP BY`): use one breakdown dimension column plus metric columns.
- **attribution** (`pipeline_mode=diagnose`): Summary carries root-cause judgment; Evidence carries the multi-step chain; Analysis approach describes angles drilled and KB limits. Multi-round hypothesis pivot and follow-up SQL are allowed until `max_diagnose_rounds` is reached; synthesis should consolidate the full evidence chain.

### Time Scope Disclosure

In **Analysis approach & confidence** / **分析思路与信心**, disclose how time was resolved:

- **User-specified:**
  - English: `Time scope: user specified <period>.`
  - Chinese: `时间范围：用户指定了 <period>。`
- **Relative anchored:**
  - English: `Time scope: "<relative expression>" was resolved to <period> using the data freshness anchor.`
  - Chinese: `时间范围：将"<relative expression>"根据数据新鲜度锚点解析为 <period>。`
- **KB default:**
  - English: `Time scope: the user did not specify a period; the active knowledge pack's certified default period was used: <business period label>.`
  - Chinese: `时间范围：用户未明确给出时间；根据当前知识包的认证默认周期，使用 <business period label>。`
- **Clarification required:**
  - English: `A time range is needed because the active knowledge pack does not define a safe default period for this question.`
  - Chinese: `需要先确认时间范围，因为当前知识包没有为该问题定义可安全使用的默认周期。`

## Confidence Disclosure Rule

Include confidence in section 3 (Analysis approach & confidence).

See [confidence-provenance.md](./confidence-provenance.md) for source tier, confidence statements, and typo disclosure templates.

See [typo-tolerance.md](./typo-tolerance.md) for typo correction rules.

## Soft-signal reflection policy

Several pipeline stages surface **soft signals** instead of hard blocks — Python has deliberately stopped pre-judging content it cannot verify mechanically, and instead hands the LLM a structured note to reason about. Treat every soft signal as a prompt to **reflect**, not as a verdict to rubber-stamp or to reflexively refuse.

Soft signals you may see, and how to react:

- **`Evidence completeness note` (metric lookup)** — the SQL plausibly targeted the requested scope and returned numeric rows, but Python's mechanical name-match could not confirm every requested metric column landed. Read the raw evidence rows yourself:
  - If the rows actually answer the question (metric present under a different but equivalent expression/alias), answer normally — do not manufacture a caveat that isn't true.
  - If a requested metric is genuinely missing from the rows, answer with what is available and state clearly which requested item is missing, rather than refusing the whole answer.
  - Only fall back to a clarification/refusal if the rows are truly irrelevant to the question (this case is still hard-blocked upstream before you see it).
- **`entity_scope_set` hint (multi-hit identifier/label probe)** — Python ran a KB-certified probe and found more than one matching row; it is not asserting ambiguity. Decide, from the question and KB routing policy, whether the set is a valid `IN (...)` business scope (proceed and encode it — see [entity-resolution.md](./entity-resolution.md#multi-candidate-label-is-a-fact-not-ambiguity)) or genuinely conflicting meanings the user must disambiguate (ask, listing the candidates).
- **Any other `planning_hints` entry you don't recognize** — these are facts recorded by upstream nodes (bind/plan/review), not instructions. Reason about what they imply for the current stage; do not skip a stage just because a hint exists, and do not treat an unfamiliar hint as an error.

General rule: Python's role at these checkpoints is limited to (a) safety/structural validity and (b) surfacing what it observed. Business correctness — is this evidence good enough, does this candidate set answer the question, should we proceed or ask — is always the LLM's call, made fresh from the evidence at hand.

## Answer check (`double-check-answer`)

When `double_check_answer` rejects answer shape:

- **Failed stage `plan-queries`:** return to `plan_queries` with correction hints.
- **Failed stage `evidence` or `review-evidence`:** replan or re-run evidence per review policy.
- **Failed stage `synthesis`:** re-synthesize via `write_answer` without replanning when evidence is sufficient.

Align trace names with runtime: `read-question`, `plan-queries`, `review-evidence`, `write-answer`, `double-check-answer`.

## Quality Checklist Before Responding

- Question is KB-related business scope.
- Intent class identified.
- Metric extraction logic mapped from KB.
- Metric-to-column validation completed (physical column vs logical formula).
- Table role check completed (slice vs global canonical).
- Correct table chosen for requested grain.
- Anti-dup check completed before SUM/aggregation.
- Pre-aggregated serving table preferred when applicable.
- Question shape classified; temporal_obligation derived.
- If time omitted: did not ask prematurely when `kb_default_eligible`; verified KB default assembly before using default period.
- Time/fiscal/timezone rules applied correctly; time scope disclosed.
- Schema taken from KB first; no unnecessary live schema probes.
- Entity identifier resolution: alphanumeric tokens on varchar label columns only; int FK after dim resolve.
- Entity scope pre-validation: Phase-1 dim/label validation completed before fact metric SQL when entity filters present.
- Invalid identifier vs no-activity-data distinction stated when applicable.
- Dimension tables taken only from KB `dimension_reference`; no invented `dim_*` names.
- No SQL referenced tables outside retrieved KB allowlist (no `v_catalog.tables` discovery).
- Fuzzy match retry attempted when exact scoped lookup returns zero rows.
- Typo auto-correction: suspected misspellings corrected before entity SQL; disclosed in section 3 with lowered confidence ([typo-tolerance.md](./typo-tolerance.md)).
- Column type predicate gate: no string literal compared to int/numeric columns.
- Vertica first; Hive only on Vertica unavailability.
- Answer follows three-section contract: Summary, Evidence, Analysis approach & confidence.
- No SQL in the three main sections (platform appends Vertica validation SQL automatically).
- Attribution question: evidence chain and conclusion are in Summary/Evidence; drill-down limits noted in section 3.
- Soft signals (`Evidence completeness note`, `entity_scope_set`, other unrecognized `planning_hints`) were reasoned about against the actual evidence rows, not rubber-stamped or reflexively refused.

## Memory Coverage Rule

Before final synthesis, compare the answer against `question_contract`.
The final answer must address requested metrics, requested entities, time scope,
and requested grain, or explicitly state which part remains unresolved and why.
