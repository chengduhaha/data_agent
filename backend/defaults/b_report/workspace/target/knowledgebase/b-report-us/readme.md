# B Report US Knowledgebase

Table catalog documents converted from [`source/contracts/b-report-us/tables/`](../../source/contracts/b-report-us/tables/).

| Item | Path |
|------|------|
| Hub fact (order-line P&L) | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` |
| Domain knowledge | `source/contracts/b-report-us/domain-knowledge.md` |
| Metric index | `source/contracts/b-report-us/metric-index.md` |
| Converter | `tools/ingest/b_report_contract_to_knowledgebase.py` |

Regenerate all docs:

```bash
python tools/ingest/b_report_contract_to_knowledgebase.py --write-seeds
python -m tools.wkb.indexing.index_builder
python -m tools.wkb.indexing.run_query --query "b-report-us dwd_disty_brpt_orders_pl_etl_mi schema" --intent find_table_schema
```
