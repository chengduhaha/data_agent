<!-- Local copy for contract-guided-data-analysis. Paths adapted to knowledge/contracts. Do not depend on external skill trees. -->

## Typo Tolerance (Mandatory)

User questions often contain spelling mistakes in vendor names, customer labels, product codes, person names, or metric aliases (for example `CICSO` vs `CISCO`).

### Detection and auto-correction

1. **Before** entity resolution, metric routing, or SQL planning, scan the user message for likely typos against:
   - KB Entity Ontology / Business Perspective known entities
   - Active pack aliases, entity ontology, typo dictionary, or documented searchable labels
   - Metric aliases in `metric-index.md`
2. When a typo is **more likely than literal match** (edit distance, phonetic similarity, or domain-known canonical spelling), **auto-correct** and continue the pipeline using the corrected token.
3. Record each correction explicitly:
   - `original_token` — as typed by the user
   - `corrected_token` — value used for filters, dim search, and SQL
   - `field` — entity type or filter key when known (optional)
   - `reason` — short business-readable rationale (for example "common vendor misspelling")
4. Apply corrected tokens to:
   - `entity_filters` / entity hypotheses
   - dim label `ILIKE` probes (Phase-1 validation)
   - planner and synthesizer scope narrative
5. **Do not** ask the user to confirm minor typos when a single high-confidence correction exists; proceed with analysis.
6. **Do** ask clarification when multiple equally plausible corrections exist (not a typo — ambiguity).

### Relationship to fuzzy match

- Typo tolerance applies **before** SQL execution — it chooses which token to search.
- Fuzzy `ILIKE` retry (entity-resolution) still applies **after** exact match on the corrected token fails.
- Do not treat every zero-row result as a typo; distinguish invalid identifier vs no activity data.

### Relationship to Question Shape

Typo correction must not change `temporal_obligation`.

If a suspected typo appears in an entity token:

1. Correct only when a single high-confidence canonical entity exists.
2. Continue entity validation using the corrected token.
3. Do not use typo correction as a reason to invent time scope.
4. If typo correction is applied and KB default period is also used, disclose both in the confidence section.

### Confidence impact (mandatory disclosure)

Auto-corrected typos introduce interpretation risk. In section 3 (**Analysis approach & confidence** / **分析思路与信心**):

1. State clearly that the model **auto-corrected** one or more tokens and list `original → corrected`.
2. Warn that the answer may **not match the user's exact wording**.
3. **Lower confidence** to at most **medium** (or **medium/low** if KB gaps also exist). Never claim **high** confidence when typo auto-correction was applied.

Suggested English line:

`Confidence: medium/low. The model auto-corrected suspected typo(s) (<original> → <corrected>). Results may differ from your exact wording.`

Suggested Chinese line:

`信心：中/偏低。模型已自动更正疑似拼写（<原文> → <更正后>），结论可能与您输入的字面含义存在偏差。`
