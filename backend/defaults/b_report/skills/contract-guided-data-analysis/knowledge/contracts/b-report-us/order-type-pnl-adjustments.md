# Order Type P&L Adjustments (Virtual / Negative Order Types)

- contract_version: v2.0.0
- artifact_type: reference
- artifact_id: b-report-us.order-type-pnl-adjustments
- domain: b-report-us
- related_dim: `dim_us.dim_pub_order_type`
- related_fact: `dw_us.dwd_disty_brpt_orders_pl_etl_mi`

## Purpose

Catalog of **virtual / negative `order_type` codes** used in B Report P&L allocation and adjustment logic. These codes are not ordinary CIS sales order types; they represent finance/ops adjustments that assign P&L impact to customer, vendor, VPC, part, or other scopes — often **with no revenue**.

Use this file when interpreting:

- Negative or special `order_type` values on B Report / POS order-line facts
- Adjustment P&L buckets (`CUST_FINANCE`, `INV_COST`, `ONE_TIME_BTL`, etc.)
- Revenue assignment vs allocation behavior for NGM / OPL investigations

Canonical dimension join remains `dim_us.dim_pub_order_type.order_type`. CIS master list for positive operational codes: `source/ref/platform/order_type_info 2.md`.

## Semantics

| Concept | Meaning |
|---------|---------|
| **Order Type** | Virtual/negative order type code used for P&L adjustment rows |
| **Adj P&L** | P&L component(s) or bucket adjusted by this order type |
| **Business Impacted** | Business entity / program scope the adjustment targets |
| **Revenue Assignment** | How revenue is attributed (often none) and how allocation is applied |
| **Description** | Business intent of the adjustment |

## Adjustment order type catalog

| Order Type | Adj P&L | Business Impacted | Revenue Assignment | Description |
|---|---|---|---|---|
| -2 | CUST_FINANCE / CVR | Customer | Customer with no revenue | Customer Finance/CVR adjustment |
| -3 | INV_COST / AP_FINANCE / INV_RESERVE | Part | Part with no revenue | Inventory Cost, AP Finance, Inventory Reserve adjustment |
| -4 | AP_FINANCE | Part / Customer | Part/Customer with no revenue | AP Finance adjustment |
| -5 | ONE_TIME_BTL / HBTL / SCM_PROFIT_ADJ / HC_PM / HC_BD | VPC | VPC with no revenue | Vendor Product Category adjustment |
| -6 | ONE_TIME_BTL / HBTL / SCM_PROFIT_ADJ / HC_PM / HC_BD | Vendor | Vendor with no revenue | Vendor-level adjustment |
| -8 | CUST_FINANCE / CVR | Customer / VPC | Customer/VPC with no revenue | Customer Finance/CVR adjustment |
| -9 | RMA | Customer / Vendor | Customer/Vendor with no revenue | RMA adjustment |
| -10 | Labor Charge from SCMs | Vendor | Vendor allocation | Insert virtual OT -10 to charge unit_price for specific vendors |
| -16 | FRT_OUT_EXP | Sharp | Vendor allocation | Include 1tmBTL freight recovery moved to Freight Out in OPL calculation |
| -39 | Offset transaction | PCO | NGM impact | Remove OT114 and OT1, keep OT101 rebill only |
| -41 | ONE_TIME_BTL | Sharp | Vendor allocation | Sharp Freight Recovery 1tmBTL moved to Freight Out Expense |
| -43 | OTHERS | Late Fee | Customer/Vendor allocation | Allocate customer late fee charges to vendor line based on sales |
| -50 | CUST_FINANCE_SALES | Cisco / Cloud | Customer allocation | Cisco/Cloud OT127 P&L adjustments |
| -51 | AP_FINANCE | EP Discount Vendors | Vendor allocation | Add AP Finance benefit to vendors, increasing NGM |
| -52 | CUST_FINANCE | Cisco Hyve Interco | Customer allocation | Credit back Customer Finance charges |
| -53 | INV_COST | Sandisk | Vendor allocation | Update inventory cost to purchase price for aging inventory calculation |
| -54 | PDT | NEC | Vendor allocation | Apply 2% PDT to NEC 17057 P&L |
| -55 | CUST_PMT_DISC | SHI, C2FO, BJ's, Walmart, Costco, BestBuy | Customer allocation | Customer Payment Discount adjustment |
| -56 | INV_COST / CR_RISK_CTERM | Broadcom / Avago | Vendor allocation | CIS B11 & B30 report adjustment |
| -57 | INV_RESERVE | Sharp | Vendor allocation | Inventory Reserve adjustment for vendor 75225 |
| -58 | ONE_TIME_BTL | HP PSG | Vendor allocation | Reallocate HP PSG 1tmBTL |
| -59 | OTHERS | Cisco / Cloud | Customer/Vendor allocation | Cisco/Cloud OT127 P&L adjustments |
| -60 | Offset INV_COST / INV_RESERVE / INFRASTRUCTURE | Unassigned Customer | Unassigned Customer | Offset P&L in B30 Unassigned |
| -61 | Reallocate INV_COST / INV_RESERVE / INFRASTRUCTURE | Unassigned Customer | Customer allocation | Look back 12 months and allocate P&L to customers |

## Analysis routing notes

- **No-revenue adjustments** (for example -2, -3, -4, -5, -6, -8, -9): expect P&L impact without corresponding net sales; do not treat missing revenue as a data quality defect by default.
- **Vendor / customer allocation** types: impact may be reassigned across entities; reconcile at the intended allocation grain (vendor, customer, VPC, part).
- **Program-specific types** (Sharp, Cisco/Cloud, NEC, Sandisk, HP PSG, etc.): filter by the documented business scope before attributing variance to the broader vendor/customer population.
- **OT -39**: special offset behavior involving OT114 / OT1 removal while retaining OT101 rebill — do not apply generic credit-memo filters without checking this rule.
- Dimension label lookup alone may be incomplete for negative codes; prefer this catalog for Adj P&L / allocation semantics.

## Cross-references

| Resource | Path |
|----------|------|
| B Report domain knowledge | `source/contracts/b-report-us/domain-knowledge.md` |
| POS domain knowledge | `source/contracts/pos/domain-knowledge.md` |
| Order type dimension contract | `source/contracts/b-report-us/tables/dim_pub_order_type.md` |
| Order type knowledgebase (ETL + human layer) | `target/knowledgebase/order/dim_pub_order_type.md` |
| CIS positive order type master | `source/ref/platform/order_type_info 2.md` |
| B Report metric definitions | `source/contracts/b-report-us/metric-index.md` |

## Provenance

- Source: business SME order-type P&L adjustment matrix (ingested 2026-07-17)
- Authority: human / finance operations knowledge for B Report allocation semantics
- Not a substitute for ETL SQL evidence when diagnosing load defects
