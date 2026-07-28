# Metric Index - part_sku

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: part_sku

## Purpose

- Metric-first routing index for the part_sku domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### asc606

- aliases:
- business_definition: Revenue recognition type
- final_effective_formula_sql: `ASC606/SKU`, active`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### renewal_flag

- aliases:
- business_definition: Renewal product indicator
- final_effective_formula_sql: `ASC606/SKU`, active, `profile_i=1` → `'Yes'` else `'No'`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### sku_map

- aliases:
- business_definition: Minimum advertised price
- final_effective_formula_sql: `MAP/PRIC`, active`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### hwsw_comb

- aliases:
- business_definition: HW+SW combination code
- final_effective_formula_sql: `HWSW-COMB/SKU`, active → `profile_c`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### series_desc

- aliases:
- business_definition: Series description substring
- final_effective_formula_sql: `VPC_ALT1/VEND`, active → `SUBSTRING(profile_c, 7, 60)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### std_whls_price

- aliases:
- business_definition: Standard wholesale price index
- final_effective_formula_sql: `WHLS_INDEX/PRIC`, active → `profile_f`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### iqc_req

- aliases:
- business_definition: IQC requirement flag
- final_effective_formula_sql: `IQC_REQ/HYVE`, active, sku_no not null → `'Y'` else `'N'`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### s1_id

- aliases:
- business_definition: S1 / family code (= `level2.s1_id`)
- final_effective_formula_sql: `L0 / Family`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: ETL run time.
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
