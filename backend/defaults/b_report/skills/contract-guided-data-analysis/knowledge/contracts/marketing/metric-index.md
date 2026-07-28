# Metric Index - marketing

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: marketing

## Purpose

- Metric-first routing index for the marketing domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### data_year

- aliases:
- business_definition: Calendar year as integer
- final_effective_formula_sql: `cast(data_year as int)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### units

- aliases:
- business_definition: Unit count
- final_effective_formula_sql: `cast(units as int)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### distributor_revenue

- aliases:
- business_definition: Local currency revenue
- final_effective_formula_sql: `cast(... as DECIMAL(20,8))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### distributor_revenue_usd

- aliases:
- business_definition: USD revenue
- final_effective_formula_sql: `cast(... as DECIMAL(20,8))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: Load timestamp PST
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
