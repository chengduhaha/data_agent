# Metric Index - ap

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: ap

## Purpose

- Metric-first routing index for the ap domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### days

- aliases:
- business_definition: Calculated from due/discount/receipt dates, terms, tolerance, and order type `27` DND rules.
- final_effective_formula_sql: `Aging-days input.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### total_po_cost

- aliases:
- business_definition: Aggregated from AP hold or vendor document cost components.
- final_effective_formula_sql: `Total AP hold or PO-cost amount in the row.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### total_document_amount

- aliases:
- business_definition: Vendor balance reporting.
- final_effective_formula_sql: `Sum of document-line amounts for each summary level.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### inventory_cost

- aliases:
- business_definition: Compare AP exposure against inventory on hand.
- final_effective_formula_sql: `Regular, RMA, and combined inventory cost attached to vendor/product rows.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### new_applied

- aliases:
- business_definition: Current applied amount minus payments entered after the run date when later applications exist.
- final_effective_formula_sql: `Snapshot-applied amount.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### new_usd_applied

- aliases:
- business_definition: Current USD applied amount minus later USD payment and discount applications.
- final_effective_formula_sql: `Snapshot-applied amount in USD.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
