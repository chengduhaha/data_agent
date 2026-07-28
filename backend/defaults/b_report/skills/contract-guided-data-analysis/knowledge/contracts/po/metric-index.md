# Metric Index - po

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: po

## Purpose

- Metric-first routing index for the po domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### rec_qty

- aliases:
- business_definition: Received quantity; defaults to 0 if null (no receipts yet).
- final_effective_formula_sql: `NVL(od.rec_qty, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### date_flag

- aliases:
- business_definition: Snapshot date — the run date parameter cast as a proper date type.
- final_effective_formula_sql: `CAST('${curr_date}' AS DATE)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
