# Domain Knowledge — order

- contract_version: v1.0.0
- artifact_type: domain-knowledge
- artifact_id: order
- domain: order

## Domain Scope

- **Domain name:** order
- **Business scope:** Shipped and open order header/detail modeling, SCM SPA, freight, pricing adjustments, and order-line extensions in the disty warehouse.
- **Geographic scope:** US-primary (`dw_us`, `dim_us`); regional schemas mirror US naming.
- **Hub tables:** `dw_us.dwd_pub_shipped_order_header_di` (shipped header), `dw_us.dwd_disty_common_dw_orders_pl_extend_di` (order-line extend).

## Grain Standards

| Grain | Keys | Usage |
|-------|------|-------|
| Order header | `order_no`, `order_type` | Header-level attributes |
| Order line | `order_no`, `order_type`, `order_line_no` | Default detail grain |
| Time filter | `date_flag` or load partition column per table | Always required in reporting |

## Entity Ontology

- entity_type: order | business_role: shipped order header at line grain | join_key: order_no, order_type | dim_fqn: dw_us.dwd_pub_shipped_order_header_di
- entity_type: customer | business_role: channel customer on order facts | join_key: cust_no | dim_fqn: dim_us.dim_pub_customer_info
- entity_type: vendor | business_role: upstream vendor on order lines | join_key: vend_no | dim_fqn: dim_us.dim_pub_vendor_info
- entity_type: product | business_role: sellable SKU on order lines | join_key: sku_no | dim_fqn: dim_us.dim_pub_part_info
- entity_type: order_type | business_role: sales vs credit order classification | join_key: order_type | dim_fqn: dim_us.dim_pub_order_type

## Cross-Table Routing Rules

1. Resolve grain (header vs line) before joining enrichment tables.
2. Use LEFT JOIN from order facts to preserve driving rows.
3. Pre-aggregate one-to-many partners (SPA, serial, freight) when grain must stay order-line.
4. Prefer curated DWD/DIM over ODS unless a required field is unavailable in warehouse tables.
