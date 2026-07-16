<!-- Local copy for contract-guided-data-analysis. Paths adapted to source/contracts. Do not depend on external skill trees. -->

# Fiscal Calendar and Relative Time Policy

## Applicability

This reference applies when:

1. `temporal_obligation = user_already_specified`
   - Parse explicit fiscal/calendar periods.

2. `temporal_obligation = kb_anchor_resolve`
   - Resolve relative expressions such as last month, current quarter, recent N months.

3. Stage-2 has confirmed `temporal_plan.mode = kb_assembly_default`
   - Interpret or label the KB-provided default period using CIS fiscal calendar.

This reference is not sufficient by itself to create a default time period when the user omitted time.

For `temporal_obligation = kb_default_eligible`:

- first verify certified default-period assembly in the active knowledge pack;
- then use this calendar policy only to interpret or label the period.

---

## CIS Fiscal Calendar Default

Unless the active pack overrides it:

- CIS fiscal year starts in December.
- Fiscal periods must be resolved using CIS fiscal calendar policy.
- Fiscal quarter and fiscal year boundaries must not be inferred manually if the selected table documents a different pattern.
- Use documented table time columns and certified time-filter snippets.

### Verified examples (unless active pack overrides)

- `2025/12`, `2026/01`, `2026/02` belong to `FY2026 Q1`.
- `FY2026` means `2025-12-01` to `2026-11-30`.
- On `dim_us.dim_pub_date`, use verified columns `fyear`, `month`, `m`, `fqtr` — never `fiscal_year` / `fiscal_period` unless KB explicitly documents them.

---

## Relative Time Without Explicit Year

When the user says "last month", "上个月", "recent N months", or similar:

1. Do not require the user to provide `20XX` merely because the expression lacks a year.
2. Resolve using:
   - data freshness anchor when available;
   - selected table's documented maximum business date when needed;
   - active pack Time Scope Ontology;
   - CIS timezone policy.
3. If no anchor exists, ask a concise clarification.
4. Do not invent `month_no = YYYYMM` unless the selected table catalog documents that encoding.

For words like "today", "tomorrow", "yesterday", compute date using runtime clock converted to PT.

Use script/runtime evaluation; do not rely on manual mental date arithmetic.

---

## Timezone Policy

Use table-local timezone according to CIS policy unless the active pack overrides it.

- US tables: PT.
- CA tables: America/Toronto.

If table-specific timezone is documented, table-specific policy wins.

Keep business date filters aligned to table-local timezone.
