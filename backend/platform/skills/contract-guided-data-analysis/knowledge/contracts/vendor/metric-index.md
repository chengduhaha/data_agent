# Metric Index - vendor

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: vendor

## Purpose

- Metric-first routing index for the vendor domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### sys_company_no

- aliases:
- business_definition: Hardcoded per branch: 100/500/425/422
- final_effective_formula_sql: `Source country/system identifier`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### format_phone_no

- aliases:
- business_definition: Copied from country-level source tables
- final_effective_formula_sql: `Digits-only phone normalization`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### master_mapped_vendor_rate

- aliases:
- business_definition: Data quality and hierarchy coverage
- final_effective_formula_sql: `Share with non-null `master_vend_no``
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### diversity_coded_vendors

- aliases:
- business_definition: Supplier diversity analysis
- final_effective_formula_sql: `Count of vendors with non-null `diversity_status``
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: Pacific load timestamp
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
