# Metric Index - cpo

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: cpo

## Purpose

- Metric-first routing index for the cpo domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### last_update_comb

- aliases:
- business_definition: The latest modification timestamp across all contributing sources.
- final_effective_formula_sql: `GREATEST(cpo_entry_datetime, cpo_change_date, spl.last_update_comb, eu_common.entry_datetime)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: ETL run time in Pacific timezone.
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
