# Metric Index - ar

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: ar

## Purpose

- Metric-first routing index for the ar domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### applied_2lc

- aliases:
- business_definition: Proportional 2LC applied amount
- final_effective_formula_sql: `IF applied<>0 AND amount<>0 AND amount_2lc IS NOT NULL AND mismatch THEN ROUND(applied*amount_2lc/amount, 2) ELSE applied_2lc`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age0_less

- aliases:
- business_definition: Outstanding amount not yet due
- final_effective_formula_sql: `NVL((amount-applied) * SIGN(1-SIGN(DATEDIFF(date_flag, due_date)-0)), 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age1_30

- aliases:
- business_definition: 1–30 days overdue
- final_effective_formula_sql: `NVL((amount-applied) * SIGN(1-SIGN(1-datediff)) * SIGN(1-SIGN(datediff-30)), 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### total

- aliases:
- business_definition: Total outstanding
- final_effective_formula_sql: `NVL(amount-applied, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### who_pays

- aliases:
- business_definition: Default to empty string if NULL
- final_effective_formula_sql: `COALESCE(d.who_pays, '')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### gross_price

- aliases:
- business_definition: Default 0 if NULL
- final_effective_formula_sql: `COALESCE(d.gross_price, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### net_price

- aliases:
- business_definition: Default 0 if NULL
- final_effective_formula_sql: `COALESCE(d.net_price, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### flooring_rate

- aliases:
- business_definition: Default 0 if NULL
- final_effective_formula_sql: `COALESCE(d.flooring_rate, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### ship_qty

- aliases:
- business_definition: Total shipped quantity
- final_effective_formula_sql: `SUM(ship_qty)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### vpl_no

- aliases:
- business_definition: Vendor product line number (0 if none)
- final_effective_formula_sql: `NVL(b.vpl_no, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### age30_up_percent

- aliases:
- business_definition: Share of AR more than 30 days past due
- final_effective_formula_sql: `SUM(age>=31) / SUM(total)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### past_due_percent

- aliases:
- business_definition: Share of AR past due at all
- final_effective_formula_sql: `SUM(overdue) / SUM(total)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### usd_past_due_percent

- aliases:
- business_definition: USD version
- final_effective_formula_sql: `SUM(usd overdue) / SUM(usd_total)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### outstanding_amt

- aliases:
- business_definition: Unpaid portion in local currency
- final_effective_formula_sql: `amount - applied`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### outstanding_usd

- aliases:
- business_definition: Unpaid portion in USD
- final_effective_formula_sql: `usd_amt - usd_applied`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### past_due

- aliases:
- business_definition: Total past-due AR
- final_effective_formula_sql: `SUM(CASE WHEN days_overdue > 0 THEN outstanding_amt ELSE 0 END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### pay_sum

- aliases:
- business_definition: Total payment + discount applied per document
- final_effective_formula_sql: `SUM(pay_amt + disc_amt_taken)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### usd_pay_sum

- aliases:
- business_definition: USD equivalent of the above
- final_effective_formula_sql: `SUM(usd_pay_amt + usd_disc_taken)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### exchange_rate_date_2lc

- aliases:
- business_definition: Latest rate date at or before doc_date
- final_effective_formula_sql: `MAX(exc.date)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### amount_2lc

- aliases:
- business_definition: Computes 2LC amount from rate only when source is NULL
- final_effective_formula_sql: `IF exchange_rate_2lc IS NOT NULL AND amount_2lc IS NULL THEN ROUND(amount / exchange_rate_2lc, 2) ELSE amount_2lc`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### amt_current

- aliases:
- business_definition: Amount not yet due as of snapshot date
- final_effective_formula_sql: `IF due_date > date_flag+1 THEN (amount - applied) ELSE 0`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### due_date_agedays

- aliases:
- business_definition: Days past due (positive = overdue, negative = not yet due)
- final_effective_formula_sql: `DATEDIFF(date_flag+1, due_date)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### doc_date_agedays

- aliases:
- business_definition: Age of the document from its creation date
- final_effective_formula_sql: `DATEDIFF(date_flag+1, doc_date)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### new_applied

- aliases:
- business_definition: Corrected applied amount including application records
- final_effective_formula_sql: `IF order_type=22 THEN amount+nvl(pay_sum,0) ELSE nvl(pay_sum,0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### usd_amt

- aliases:
- business_definition: For BR: recalculated from trade-currency rate; otherwise from source
- final_effective_formula_sql: `IF em.exchange_rate IS NOT NULL THEN ROUND(ht.amount / em.exchange_rate, 2) ELSE ht.usd_amt`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### fx_currency

- aliases:
- business_definition: Trade currency from BR rate lookup, else from document
- final_effective_formula_sql: `NVL(em.fx_currency, ht.fx_currency)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### profile_type

- aliases:
- business_definition: Resolves `REF` type to the actual reference code label from the list box
- final_effective_formula_sql: `CASE WHEN pf.profile_type='REF' THEN cd.code_value ELSE pf.profile_type END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### nsls

- aliases:
- business_definition: Net sales in local currency
- final_effective_formula_sql: `SUM(ship_qty * (u_price + u_sum_expense))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### usd_nsls

- aliases:
- business_definition: USD-converted net sales
- final_effective_formula_sql: `SUM(ship_qty * (u_price + u_sum_expense) * rate_first)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### ave_day

- aliases:
- business_definition: MTD average payment days
- final_effective_formula_sql: `SUM(diff_date) / SUM(mon_diff_cnt)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
