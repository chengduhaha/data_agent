<!-- Local copy for contract-guided-data-analysis. Paths adapted to knowledge/contracts. Do not depend on external skill trees. -->

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
   - if breakdown dimension / driver angle is missing → do **not** ask; enter `pipeline_mode=diagnose` and run hypothesis-driven multi-angle drill-down using pack-supported dimensions only ([Ambiguity Handling](#ambiguity-handling));
   - do not stop at one-layer descriptive comparison;
   - perform progressive drill-down on candidate angle(s) until:
     - a most likely root cause is identified with evidence, or
     - KB boundary is reached and further causal confirmation is unsupported.

## Ambiguity Handling

Ask clarification **before generating analysis output** **only** when the **question or data** has a genuine ambiguity that blocks routing — i.e. the agent cannot decide analysis scope from the user wording plus KB defaults. If the question is clear enough to proceed, **do not ask**.

Do **not** invent a routing choice and proceed when that choice would materially change the answer shape. Do **not** ask to confirm exploration plans, candidate hypotheses, or which reasonable driver angles to try.

Gate: ask only when ambiguity is about **business analysis intent / scope** and routing is blocked. Do **not** ask the user to supply facts the active knowledge pack is supposed to own (see **Do not ask the user** below).

### When clarification is required (routing underspecified)

Ask a concise clarification and stop before evidence SQL / analysis artifact when **any** of the following holds **and** the question/data is ambiguous for that slot **and** KB does not certify a safe default:

| Gap | Clarification target | Typical ask |
|-----|----------------------|-------------|
| Vague business grouping word ("item", "line", "category", "component") with multiple KB-plausible meanings | `grouping_definition` | What "item" (or similar) means in this question |
| Business term / acronym / project label that cannot be resolved from pack ontology | `business_term` | What the term refers to (entity family + identifier) |
| Time missing and `temporal_obligation = user_must_specify` (or no safe KB default) | `time_range` | Confirm period |
| Entity / geography / currency / grain ambiguous among user-facing choices | matching target | Offer the concrete alternatives |
| Comparison / ranking sense when comparative words lack a baseline and the choice is material | ranking / comparison sense | What “less / lower / low / hurt / worst” means |
| Open ranking population / filter scope ambiguous (all entities vs a subset — PM, VPC, segment, named vendor list, …) and the choice changes the answer | `population_scope` | Ask which population/subset the ranking should cover |

Also ask when:

- metric **name among user-facing metrics** is ambiguous (e.g. NGM$ vs NGM%) and both are valid in pack;
- geography/region, entity family, or reporting grain is underspecified and changes routing.

**Attribution / root-cause:** When the user asks why / what drove / top drivers / variance attribution and does **not** name a breakdown dimension, do **not** ask for `breakdown_dimension`. Auto-run multi-angle exploration: generate pack-supported candidate dimensions, run evidence, eliminate weak explanations, and converge on the most likely causes. Ask only if another hard slot is blocked (e.g. time under `user_must_specify`, unresolved business term, vague “item” with multiple pack meanings).

### Do not ask the user (KB-owned technical facts)

Never ask the user to clarify or supply:

- ETL / business **logic** explanations that belong in KB;
- **table** names, FQNs, or which physical table to use;
- **metric formulas**, column expressions, or calculation steps;
- Azkaban / **flow config**, job names, schedule, or pipeline wiring;
- join keys, partition keys, or schema/catalog details.

Resolve those from the active knowledge pack (`metric-index`, table docs, golden patterns, domain-knowledge, special logic). If the pack cannot support the request after local research → refuse / **no data found** / unsupported with scope — do **not** interview the user for missing KB content.

**Never ask** (resolve from KB or fail closed):

- `Which Vertica table holds NGM?`
- `What is the NGM% formula?` / `Which columns?`
- `Which flow builds inv cost?` / Azkaban job or schedule questions
- `Is segment_exclude = 'N' correct?` / which vendor key to use
- Join keys, partition keys, or schema/catalog discovery questions

Do **not** teach or default to interview menus for routing. When a hard slot above is truly blocked, ask one focused clarification; otherwise proceed (attribution: auto-explore) or fail closed.

### Time Ambiguity

Do not automatically ask for time just because the user omitted a time expression — but **do** ask when the question shape has no safe period (see below).

Use `temporal_obligation` from [question-shape.md](./question-shape.md).

| temporal_obligation | Behavior |
|---------------------|----------|
| `user_already_specified` | Parse and apply the user's explicit time. Ask only if the expression has multiple plausible meanings that CIS calendar policy cannot resolve. |
| `kb_anchor_resolve` | Resolve relative time using CIS fiscal calendar, data freshness, runtime anchor, selected table max date, and active pack Time Scope Ontology. Includes **entity-anchored** cues (e.g. "same month as this order"). Do not ask for a year merely because the user said "last month" or similar. |
| `kb_default_eligible` | Do not ask for time in Stage-1. Stage-2 must verify whether the active pack provides certified default period assembly. Ask for time only if no safe KB default exists. **Not** eligible for person/PM portfolio KPI lookup or ranking when time is absent (those are `user_must_specify`). |
| `user_must_specify` | Ask a concise time clarification before evidence SQL. |

#### Time range required (ask `time_range`)

When time is **absent** and **not** entity-anchored, set `user_must_specify` and ask before analysis for:

- Person-scoped revenue / margin / KPI (one or more names) with no period.
- PM / portfolio-scoped ranking, "hurt most", or high-impact SKU / product lists with no period.
- Other open portfolio aggregates/rankings with no period and no KB-certified default for that shape.

Examples:

- `tell me the revenue/margin for Kris Cheng And Thi Dao` → ask time.
- `I am a PM, PMID=706187, Show low‑net sales, high‑impact net gross margin items(SKU)` → ask time.
- `I am a PM, PMID=706187, Which products hurt NGM the most?` → ask time.

#### Time range not required

Do **not** ask for time when:

- User gave explicit or relative period; or
- Period is **entity-anchored** (pinpoint order/transaction implies the window, e.g. "same month as Order#…"); or
- True `kb_default_eligible` path is confirmed by Stage-2 for a shape that allows it (disclose the default).

Example:

- `For Order#169010235, Compare this order to similar profitable ones by same product with Order#169010235's same month` → resolve the order’s month; do not ask for a separate time range.

### Time clarification must not mask other issues

Do not ask for time when the real issue is:

- invalid entity;
- ambiguous entity;
- missing metric definition in KB (fail closed — do not ask user for the formula);
- missing table routing in KB (fail closed — do not ask user for the table);
- unsupported attribution;
- out-of-scope request.

Missing breakdown dimension on a variance/driver question is **not** a time issue and is **not** a clarification gate — auto-explore pack-supported angles (see Attribution / root-cause above).

### Other ambiguities (user-facing scope)

Ask clarification before querying when any of these is ambiguous **as business scope**:

- which user-facing metric among pack candidates (name clash, not formula);
- grain (daily/weekly/monthly/QTD/YTD) when not defaultable;
- geography/region scope;
- entity scope (customer, vendor, BD rep, buyer, etc.);
- currency/unit;
- grouping definition when a vague word ("item", "line", "category") has multiple pack meanings (see table above).

Do **not** ask which driver dimension to use for open-ended attribution / root-cause — explore pack-supported candidates instead.

Do not guess when ambiguity can materially change routing or results.

### Clarification style

- Ask **only** when the question or data has a genuine ambiguity that blocks routing (hard slot open). If the question is clear enough to proceed, **do not ask**.
- When asking is required: **one focused question** (or a short numbered list) covering only the blocking slot(s); offer concrete alternatives drawn from pack-supported dimensions/terms when helpful.
- Do **not** generate Summary/Evidence analysis output, SQL plans presented as the answer, or `{output_dir}/*.md` until required clarifications are resolved.
- Match the user's language ([Response Language](#response-language)).

### Examples

**Good — ask (underspecified routing):**

1. Vague "item":  
   `For Vendor #13208 in April 2026, show Value, MoM%, YoY% for each item in April NGM`  
   → Ask what "item" means (P&L line, VPC, part, …).

2. Unresolved term + missing time:  
   `Check inv cost details for B33 BD project 16428`  
   → Ask what B33 BD refers to (if not resolvable from pack) and which time range (if `user_must_specify` / no KB default).

3. Person / PM portfolio with no period (ask time):  
   - `tell me the revenue/margin for Kris Cheng And Thi Dao` → ask `time_range`.  
   - `PMID=706187, Show low‑net sales, high‑impact NGM items (SKU)` → ask `time_range`.  
   - `PMID=706187, Which products hurt NGM the most?` → ask `time_range`.

**Good — do not ask time (entity-anchored):**

`For Order#169010235, Compare this order to similar profitable ones by same product with Order#169010235's same month`  
→ Resolve the order’s month; do not ask for a separate time range.

**Good — time clarification wording:**

`请确认要分析的时间范围，例如最近一个月、某个财政季度或某个财年。`

**Bad — ask user for KB-owned facts:**

- `Which table should I query for inv cost?`
- `What is the NGM formula / which columns?`
- `Which Azkaban flow loads this?`

**Bad — ask for driver dimension or plan confirmation (attribution):**

- Asking which breakdown to use (customer, vendor, P&L, VPC, …) for an open-ended why / what-drove / top-drivers question.
- Asking the user to confirm a drill-down plan or candidate hypotheses before running evidence.

**Bad — premature or wrong clarification:**

`请提供年份。` when the user said "上个月" and a freshness anchor exists.

`请提供时间范围。` when the question is an entity-scoped scalar KPI eligible for KB default assembly.

`请确认 metric 计算公式` when the formula is (or should be) in `metric-index` — resolve from KB or fail closed.

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

Executed SQL is shown in the analysis execution trace only. Do not repeat SQL in the user-facing answer.

## Response Language

Match the user's question language in every user-facing part of the answer and thought-process trace.

- **Chinese question** (contains CJK characters): write in Simplified Chinese. Section headings: **摘要**, **证据**, **分析思路与信心**.
- **English question** (no CJK): write in English. Section headings: **Summary**, **Evidence**, **Analysis approach & confidence**.
- **Mixed Chinese + English**: default to Chinese (typically Chinese-primary); preserve English metric/table codes in evidence.

## Output Contract (Fixed)

User-facing answers must focus on business-readable content. **Do not include SQL** in the reply — queries are already visible in the analysis process / observability panel.

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

- SQL queries (fenced blocks, "SQL used", "Executed SQL", or similar)
- Trial/error or intermediate SQL
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
- No SQL repeated in the user-facing answer.
- Attribution question: multi-angle exploration ran when angle was absent (no ask for breakdown dimension); evidence chain and conclusion are in Summary/Evidence; drill-down limits noted in section 3.
- Did not ask the user for KB-owned facts (tables, formulas, flow config, ETL logic).
- Soft signals (`Evidence completeness note`, `entity_scope_set`, other unrecognized `planning_hints`) were reasoned about against the actual evidence rows, not rubber-stamped or reflexively refused.

## Memory Coverage Rule

Before final synthesis, compare the answer against `question_contract`.
The final answer must address requested metrics, requested entities, time scope,
and requested grain, or explicitly state which part remains unresolved and why.
