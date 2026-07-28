# Metric Index - common

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: common

## Purpose

- Metric-first routing index for the common domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### budget_amount

- aliases:
- business_definition: Uses actual when posted
- final_effective_formula_sql: `CASE WHEN posting_date IS NULL THEN budget_amount ELSE actual_amount END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### foreign_bug_amount

- aliases:
- business_definition: Foreign currency equivalent
- final_effective_formula_sql: `CASE WHEN posting_date IS NULL THEN foreign_bug_amount ELSE foreign_act_amount END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### week2

- aliases:
- business_definition: Adds or subtracts 1 from the original week when the year's first day is Sunday, anchoring weeks to Sunday starts
- final_effective_formula_sql: `CASE WHEN dow<>7 AND DAYOFWEEK(trunc(date_flag,'YYYY'))=7 THEN week+1 WHEN dow=7 AND DAYOFWEEK(trunc(date_flag,'YYYY'))<>7 THEN week-1 ELSE week END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### w2

- aliases:
- business_definition: Corrected week flag (flag version of week2)
- final_effective_formula_sql: `CASE WHEN dow=7 THEN w-1 ELSE w END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### week_flag

- aliases:
- business_definition: Zero-padded calendar week label "YYYY-Www"
- final_effective_formula_sql: `CASE WHEN week>=10 THEN concat(year,'-W',week) ELSE concat(year,'-W0',week) END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### month_flag

- aliases:
- business_definition: Zero-padded month label "YYYY-MM"
- final_effective_formula_sql: `CASE WHEN month>=10 THEN concat(year,'-',month) ELSE concat(year,'-0',month) END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### dt_week

- aliases:
- business_definition: Sunday-anchored week label "YYYY-Www"
- final_effective_formula_sql: `CASE WHEN week2>=10 THEN concat(year,'-W',week2) ELSE concat(year,'-W0',week2) END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: Load timestamp in Pacific time
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### max_currency_date

- aliases:
- business_definition: Latest available rate date on or before `date_flag`
- final_effective_formula_sql: `MAX(date)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### company_no

- aliases:
- business_definition: Normalizes company_no to 1 when company_no equals cis_server (except for server 2203), indicating the primary company
- final_effective_formula_sql: `CASE WHEN a.company_no = a.cis_server AND a.cis_server <> 2203 THEN 1 ELSE a.company_no END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### name

- aliases:
- business_definition: Full name combining first + last, null-safe
- final_effective_formula_sql: `concat(if(firstname is null,'',firstname),' ',if(lastname is null,'',lastname))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
