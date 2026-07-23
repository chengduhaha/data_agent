# Analysis clarification before routing

When answering business data / KPI / variance / ranking / comparison questions under KB-guided or contract-guided analysis:

## Ask first (stop before analysis output)

If the question is **ambiguous or missing context** and the detail is **not enough to decide local routing**, ask a concise clarification **before** evidence SQL, three-section analysis answers, or chat analysis answers.

Ask only when the question is unclear for routing — do not invent a comparison sense, period, or filter scope when those slots are open and material to the answer. If the question already specifies sense, period, and scope clearly, proceed without asking.

Typical gaps (ask only when KB has no certified default for that slot):

1. **Variance / top drivers** without a breakdown angle → ask dimension (customer, P&L, VPC, vendor, …).
2. **Vague grouping** ("item", "line", "category") with multiple pack meanings → ask definition.
3. **Unresolved business term / acronym / project label** → ask what it refers to.
4. Ambiguous **entity / metric name / grain / geography / currency** among user-facing choices.
5. **Time range** when required by question shape (see below).
6. **Comparison / ranking sense** when comparative words lack a baseline → ask what “less / lower / low / hurt / worst” means (see below).
7. **Population / filter scope** when open ranking could mean all entities or a subset (PM, VPC, segment, named vendor list, …) → ask scope if it changes the answer.

Authoritative detail: `/skills/org/contract-guided-data-analysis/references/output-contract.md` § Ambiguity Handling.  
Also: `/rules/org/contract-data-analysis-vertica.md` (must clarify before Vertica evidence).

## Comparison / ranking sense (`comparison_sense`)

Comparative or evaluative language without a clear baseline is **underspecified**. Ask before routing.

| User wording (examples) | Ask (offer concrete options) |
|-------------------------|------------------------------|
| “gm_amt is less for vendor level” | Lowest GM vendors (ranking)? Negative GM only? Lower vs prior period / YoY? Lower vs a peer set or target? |
| “hurt NGM the most”, “worst margin” | Absolute $ impact? Rate/bps? vs prior period? Top-N size? |
| “low net sales, high impact” | Explicit definition of “low” / “high impact” if not pack-certified |

Do **not** silently pick “top-N lowest” or “MoM decline” when the user only said “less” / “low”.

## Time range clarification

Do not invent a reporting period. Use `temporal_obligation` from the analysis skill; for these shapes, prefer `user_must_specify` when time is absent and not entity-anchored.

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

- User stated an explicit or relative period (`March`, `last month`, `YTD`, …).
- Time is **entity-anchored** — the question ties the period to a pinpoint object (e.g. an order’s month).
- `temporal_obligation = kb_default_eligible` **and** Stage-2 confirms a certified KB default (disclose it). Do **not** treat person/PM portfolio ranking, multi-person KPI lookup, or open vendor/customer ranking as KB-default-eligible when time is absent.

Example that does **not** require time clarification:

- `For Order#169010235, Compare this order to similar profitable ones by same product with Order#169010235's same month`  
  → Period is anchored to the order’s month (`kb_anchor_resolve` / entity-relative cue). Proceed after resolving that month from the order.

## Clarification style

- Ask **one focused question** or a short numbered list covering only missing routing slots.
- Offer **concrete alternatives** (comparison sense, period examples, scope options).
- Do **not** emit Summary/Evidence analysis, answer-shaped SQL, or chat analysis answers until required clarifications are resolved.

## Do not ask the user

Never ask for KB-owned technical facts:

- ETL / business logic
- table names or FQNs
- metric formulas / column expressions
- flow / Azkaban / pipeline config
- joins, partitions, schema discovery details
- whether `segment_exclude = 'N'` or which vendor key (`dim_vend_no` vs `vend_no`) to use — resolve from KB / special_logic

Resolve from the knowledge pack; if missing → fail closed / unsupported / no data found — do not interview the user to fill KB gaps.
