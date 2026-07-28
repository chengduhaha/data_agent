# Metric Index - inventory

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: inventory

## Purpose

- Metric-first routing index for the inventory domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### trans_type

- aliases:
- business_definition: Custom snapshot trans_type code or default 1001
- final_effective_formula_sql: `nvl(doc_num, 1001)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### amt

- aliases:
- business_definition: Monthly writedown amount attributable to each vendor/SKU by source type
- final_effective_formula_sql: `Sum of cost amounts by type (see per-type logic below)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### qty1_30

- aliases:
- business_definition: Newest inventory bucket
- final_effective_formula_sql: `On-hand allocated to transactions 1–30 days old`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### avg_landed_cost

- aliases:
- business_definition: Weighted-average landed cost per SKU
- final_effective_formula_sql: `sum(nvl(landed_cost,0) * (nvl(intran_in,0) + nvl(rec_qty,0) - nvl(ship_qty,0))) / nullif(sum(net_qty), 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### rio_qty

- aliases:
- business_definition: Default to 0 if null
- final_effective_formula_sql: `nvl(a.rio_qty, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### company_no

- aliases:
- business_definition: Location company takes precedence over vendor company
- final_effective_formula_sql: `nvl(lo.company_no, d.company_no)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cyc

- aliases:
- business_definition: Dollar value of cycle-count dispositions
- final_effective_formula_sql: `cyc_qty * system_cost` (if non-SWA trans_type 38 exists and value > 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### total_trans

- aliases:
- business_definition: Dollar value of the disposition (0 if no part master match)
- final_effective_formula_sql: `trans_qty * nvl(b.ave_cost, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age10e

- aliases:
- business_definition: Starting gross 360+ day aging value (dollar)
- final_effective_formula_sql: `SUM(age360_up)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age10eback

- aliases:
- business_definition: Backup of starting gross aging — preserved as `old_age360` in target
- final_effective_formula_sql: `SUM(age360_up)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age10e_qty

- aliases:
- business_definition: Starting gross 360+ day aging quantity
- final_effective_formula_sql: `SUM(qty360_up)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age10eback_qty

- aliases:
- business_definition: Backup of starting gross qty
- final_effective_formula_sql: `SUM(qty360_up)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cat

- aliases:
- business_definition: Category placeholder; set in step 11
- final_effective_formula_sql: `cast(null as string)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### pct_mfg

- aliases:
- business_definition: Percentage of on-hand qty held at loc_no 19 (manufacturing location)
- final_effective_formula_sql: `nvl(sum(CASE WHEN loc_no = 19 THEN on_hand_qty ELSE 0 END) * 100 / nullif(sum(on_hand_qty), 0), 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: ETL run timestamp converted to Los Angeles local time
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### invalid_flag

- aliases:
- business_definition: `'Y'` if the location is in the DSL-or-non-C1 invalid set; `'N'` for all standard operational locations
- final_effective_formula_sql: `CASE WHEN ti.loc_no IS NOT NULL THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### it_ave_cost

- aliases:
- business_definition: In-transit average cost selected by inv_type cost_from rule (Q/L/M ASCII sign trick)
- final_effective_formula_sql: `(1-abs(sign(ascii(cost_from)-ascii('Q'))))*nvl(iq.ave_cost,0) + (1-abs(sign(ascii(cost_from)-ascii('L'))))*nvl(avg_landed_cost,0) + (1-abs(sign(ascii(cost_from)-ascii('M'))))*nvl(pm.ave_cost,0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
