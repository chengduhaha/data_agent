# Analysis clarification before routing

When answering business data / KPI / variance questions under KB-guided or contract-guided analysis:

## Ask only when blocked (stop before analysis output)

Ask **only** when the **question or data** has a genuine ambiguity that blocks local routing. If the question is clear enough to proceed, **do not ask**.

If a hard routing slot is open so routing is impossible, ask a concise clarification **before** evidence SQL, three-section analysis answers, or `{output_dir}/*.md`.

Do not invent a comparison sense, period, or filter scope when those slots are open and material. If sense, period, and scope are already clear, proceed without asking.

Typical gaps (ask only when the question/data is ambiguous **and** KB has no certified default for that slot):

1. **Vague grouping** ("item", "line", "category") with multiple pack meanings → ask definition.
2. **Unresolved business term / acronym / project label** → ask what it refers to.
3. Ambiguous **entity / metric name / grain / geography / currency** among user-facing choices.
4. **Time range** when required by question shape (see below).
5. **Comparison / ranking sense** when comparative words lack a baseline and the choice is material → ask what “less / lower / low / hurt / worst” means.
6. **Population / filter scope** when open ranking could mean all entities or a subset (PM, VPC, segment, named vendor list, …) → ask scope if it changes the answer.

**Attribution / root-cause without a named angle** → do **not** ask for breakdown dimension. Enter `pipeline_mode=diagnose`, generate pack-supported candidate dimensions, run evidence, eliminate weak explanations, and converge on the most likely causes. Ask only if another hard slot above is blocked (e.g. time).

Authoritative detail: `references/output-contract.md` § Ambiguity Handling.

## Do not ask / do not wait

Do **not**:

- Ask the user to confirm an exploration / drill-down plan before investigating.
- Present a menu of driver dimensions (customer, vendor, P&L, VPC, …) for open-ended why / what-drove / top-drivers questions.
- Wait for confirmation of candidate hypotheses when pack-supported angles can be explored with evidence.

## Time range clarification

Do not invent a reporting period. Use `temporal_obligation` from the analysis skill; for these shapes, prefer `user_must_specify` when time is absent and not entity-anchored.

### Fiscal / financial year quarters (CIS)

When the user states a year+quarter such as `2026 Q1`, `FY2026 Q1`, or `Q1 2026` **without** saying calendar quarter, treat it as **CIS financial (fiscal) year**, not calendar year.

- CIS fiscal year starts in **December**.
- **FY2026 Q1** = `2025-12` ~ `2026-02` (months `2025/12`, `2026/01`, `2026/02`).
- General pattern: **FY{N} Q1** = `{N-1}-12` ~ `{N}-02`; do not map `2026 Q1` to calendar Jan–Mar 2026.
- Full FY and other quarter boundaries: see `references/fiscal-calendar.md`.
- Only ask calendar vs fiscal if the user explicitly conflicts with this (e.g. “calendar Q1 2026” vs “FY2026 Q1”) or the active pack overrides CIS fiscal policy.

### Ask for time (`time_range`)

When the user gives **no period** and time is **not** implied by a pinpoint transaction/order, ask before analysis for:

- **Person-scoped** revenue / margin / KPI lookup (one or more people) with no period.
- **PM / portfolio-scoped** ranking, hurt-most, or high-impact SKU / product lists with no period.
- **Vendor- / customer- / open-portfolio ranking or “who is lowest/highest”** with no period.
- Other open portfolio aggregates or rankings with no period and no safe entity-anchored period.

Examples that **require** time clarification:

- `tell me the revenue/margin for Kris Cheng And Thi Dao`
- `I am a PM, PMID=706187, Show low‑net sales, high‑impact net gross margin items(SKU)`
- `I am a PM, PMID=706187, Which products hurt NGM the most?`
- `is gm_amt less for vendor level` / `which vendors have lower GM`

### Do not ask for time

When any of these already resolves the period:

- User stated an explicit or relative period (`March`, `last month`, `YTD`, `2026 Q1` / `FY2026 Q1`, …). Resolve year+quarter labels via the CIS fiscal rule above (e.g. `2026 Q1` → `2025-12` ~ `2026-02`).
- Time is **entity-anchored** — the question ties the period to a pinpoint object (e.g. an order’s month).
- `temporal_obligation = kb_default_eligible` **and** Stage-2 confirms a certified KB default (disclose it). Do **not** treat person/PM portfolio ranking, multi-person KPI lookup, or open vendor/customer ranking as KB-default-eligible when time is absent.

Example that does **not** require time clarification:

- `For Order#169010235, Compare this order to similar profitable ones by same product with Order#169010235's same month`  
  → Period is anchored to the order’s month (`kb_anchor_resolve` / entity-relative cue). Proceed after resolving that month from the order.

## Clarification style

- Ask **only** when the question or data has a genuine ambiguity that blocks routing (hard slot open). If the question is clear enough to proceed, **do not ask**.
- When asking is required: **one focused question** or a short numbered list covering only the blocking slot(s); offer concrete alternatives when helpful.
- Do **not** emit Summary/Evidence analysis, answer-shaped SQL, or `{output_dir}/*.md` until required clarifications are resolved.

## Do not ask the user

Never ask for KB-owned technical facts:

- ETL / business logic
- table names or FQNs
- metric formulas / column expressions
- flow / Azkaban / pipeline config
- joins, partitions, schema discovery details
- whether `segment_exclude = 'N'` or which vendor key (`dim_vend_no` vs `vend_no`) to use — resolve from KB / special_logic

Resolve from the knowledge pack; if missing → fail closed / unsupported / no data found — do not interview the user to fill KB gaps.
