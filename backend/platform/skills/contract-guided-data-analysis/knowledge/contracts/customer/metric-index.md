# Metric Index - customer

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: customer

## Purpose

- Metric-first routing index for the customer domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### address1

- aliases:
- business_definition: Single combined address line 1
- final_effective_formula_sql: `IF(address1b IS NULL, address1a, CONCAT(NVL(address1a,''), ' ', NVL(address1b,'')))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### format_phone_no

- aliases:
- business_definition: Digits-only primary phone
- final_effective_formula_sql: `CASE WHEN phone_no IS NOT NULL THEN regexp_replace(phone_no, '[^0-9]', '') END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### format_phone_no2

- aliases:
- business_definition: Digits-only secondary phone
- final_effective_formula_sql: `CASE WHEN phone_no2 IS NOT NULL THEN regexp_replace(phone_no2, '[^0-9]', '') END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### format_cell_no

- aliases:
- business_definition: Digits-only mobile number
- final_effective_formula_sql: `CASE WHEN cell_no IS NOT NULL THEN regexp_replace(cell_no, '[^0-9]', '') END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: LA-timezone load timestamp
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### insurance_limit

- aliases:
- business_definition: Highest insurance limit ever recorded for the customer
- final_effective_formula_sql: `max(insurance_limit)` grouped by `cust_no`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### end_date

- aliases:
- business_definition: Latest insurance policy end date, excluding deleted records
- final_effective_formula_sql: `max(end_date)` grouped by `cust_no`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### final_insurance_limit

- aliases:
- business_definition: In-force insurance limit at the latest active end date
- final_effective_formula_sql: `max(ci.insurance_limit)` grouped by `ci.cust_no, ed.end_date`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### last_edi_or_xml_date

- aliases:
- business_definition: Last date an EDI or XML order shipped for this customer
- final_effective_formula_sql: `max(CASE WHEN system_type IN ('EDI','XML') THEN ship_date ELSE null END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### last_ec_order_date

- aliases:
- business_definition: Last date an EC Express order shipped for this customer
- final_effective_formula_sql: `max(CASE WHEN system_type = 'EC EXPRESS' THEN ship_date ELSE null END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### mcust_no

- aliases:
- business_definition: Master customer number; self-references if no MASTER_SUB xref
- final_effective_formula_sql: `IF(cx.xref_no IS NULL, ch.cust_no, cx.xref_no)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### outside_sales_rep

- aliases:
- business_definition: Manager user ID matched by lower(name) = lower(profile_c)
- final_effective_formula_sql: `max(mgr.userid)` grouped by `cust_no, profile_c`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### last_update_comb

- aliases:
- business_definition: Latest profile change timestamp
- final_effective_formula_sql: `max(greatest(cp.entry_datetime, cp.update_datetime))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_channel

- aliases:
- business_definition: Sales channel
- final_effective_formula_sql: `MAX(CASE WHEN profile_type='CHANNEL' AND profile_cat='CUST' THEN profile_c END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### varnex_members

- aliases:
- business_definition: VARNEX membership value
- final_effective_formula_sql: `MAX(CASE WHEN profile_type='VARNEX' THEN profile_c END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### price_grid

- aliases:
- business_definition: Pricing tier; defaults to `'SGM'` if null
- final_effective_formula_sql: `MAX(CASE WHEN profile_type='MPG' THEN NVL(profile_c,'SGM') END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### m_xref_no

- aliases:
- business_definition: Master account number
- final_effective_formula_sql: `MAX(CASE WHEN xref_type='MASTER_SUB' THEN xref_no END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### fin_xref_no

- aliases:
- business_definition: Finance master number
- final_effective_formula_sql: `MAX(CASE WHEN xref_type='FINAN_SUB' THEN xref_no END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### p_xref

- aliases:
- business_definition: Program analyst xref
- final_effective_formula_sql: `MAX(CASE WHEN xref_type='CUST_PROG' THEN xref END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### s_xref

- aliases:
- business_definition: Service analyst xref
- final_effective_formula_sql: `MAX(CASE WHEN xref_type='CUST_CSREP' THEN xref END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### buy_xref_no

- aliases:
- business_definition: Buying group number
- final_effective_formula_sql: `MAX(CASE WHEN xref_type='BUY_SUB' THEN xref_no END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_acct_type

- aliases:
- business_definition: Human-readable account type
- final_effective_formula_sql: `CASE ch.cust_acct_type WHEN 'RS' THEN 'Reseller' WHEN 'EU' THEN 'End User' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### data_source

- aliases:
- business_definition: Source system identifier
- final_effective_formula_sql: `CASE data_source WHEN 'ods_cis_corp_customer_header' THEN 'CIS' WHEN 'ods_his_corp_customer_header' THEN 'HIS' ELSE '' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### credit_analyst

- aliases:
- business_definition: Customer-level analyst overrides territory default
- final_effective_formula_sql: `NVL(ch.cred_analyst, t.cred_analyst)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### collector_id

- aliases:
- business_definition: Customer-level collector overrides territory default
- final_effective_formula_sql: `NVL(ch.reviewer, t.reviewer)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### currency

- aliases:
- business_definition: Customer profile currency; falls back to company-level currency
- final_effective_formula_sql: `NVL(cp.currency, ci.currency)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### is_share_credit_limit

- aliases:
- business_definition: `'Y'` only when customer has a finance master and is not in excluded terms or territory lists
- final_effective_formula_sql: `CASE WHEN tcac.finance_master IS NULL OR tg.doc_terms IS NOT NULL OR sy.doc_year IS NOT NULL THEN 'N' ELSE 'Y' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### logo_url

- aliases:
- business_definition: Logo from Engage first; PRM as fallback
- final_effective_formula_sql: `COALESCE(loc.logo_url, prm.ext_value)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### customer_communities

- aliases:
- business_definition: MDM community label or xref number
- final_effective_formula_sql: `COALESCE(cii.community_value, ci.xref_no)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### m_nsales

- aliases:
- business_definition: Net sales for the period.
- final_effective_formula_sql: `nvl(SUM((u_price + nvl(u_sum_expense,0)) * ship_qty), 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### m_ncost

- aliases:
- business_definition: Net cost for the period.
- final_effective_formula_sql: `nvl(SUM((nvl(sales_cost,u_cost) + nvl(u_sum_expense,0)) * ship_qty), 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### m_cpl

- aliases:
- business_definition: OPLGM amount; zero when net sales are zero.
- final_effective_formula_sql: `nvl(SUM(CASE WHEN net_sales=0 THEN 0 ELSE OPLGM_amt END), 0)` as decimal(20,8)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_type

- aliases:
- business_definition: Replaces the -3 placeholder with the actual cust_type from the dimension when available.
- final_effective_formula_sql: `CASE WHEN c2.cust_type IS NOT NULL AND c1.cust_type = -3 THEN c2.cust_type ELSE c1.cust_type END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_terr

- aliases:
- business_definition: Replaces the -3 placeholder with the actual territory from the dimension when available.
- final_effective_formula_sql: `CASE WHEN c2.cust_no IS NOT NULL AND c1.cust_terr = -3 THEN c2.sales_terr ELSE c1.cust_terr END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### nsales

- aliases:
- business_definition: Picks the relevant period's sales depending on which month this customer is active in.
- final_effective_formula_sql: `CASE WHEN SUM(m1)=1 THEN SUM(m_nsales) ELSE SUM(pm_nsales) END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cnt_credit

- aliases:
- business_definition: Customers with no matching NONTERMS entry — effectively no credit terms.
- final_effective_formula_sql: `SUM(CASE WHEN tg.terms_no IS NULL THEN 1 ELSE 0 END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cnt_none_sales

- aliases:
- business_definition: No-credit customers with no purchase in the last 2 months.
- final_effective_formula_sql: `SUM(CASE WHEN tg.terms_no IS NULL AND last_purchase/entry_datetime < add_months(date_flag,-2) THEN 1 ELSE 0 END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cnt_none_terms

- aliases:
- business_definition: Customers who do have a terms group.
- final_effective_formula_sql: `SUM(CASE WHEN tg.terms_no IS NOT NULL THEN 1 ELSE 0 END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### sales_total

- aliases:
- business_definition: Gross sales — unit price × quantity, null-safe.
- final_effective_formula_sql: `SUM(nvl(u_price * ship_qty, 0))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### rev_seq

- aliases:
- business_definition: Placeholder; populated later in `temp_cust_temp_3`.
- final_effective_formula_sql: `CAST(NULL AS INT)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### primary_contact_flag

- aliases:
- business_definition: Marks this contact as the primary contact for the location when their contact number matches the location's designated primary contact.
- final_effective_formula_sql: `IF(ec.contact_no = el.primary_contact, 'Y', 'N')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
