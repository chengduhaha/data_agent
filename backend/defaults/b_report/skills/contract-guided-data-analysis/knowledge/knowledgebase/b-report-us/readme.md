# B Report US Knowledgebase

Table catalog documents for US B Report profitability analytics. **ETL-backed tables** (88) are generated from Bitbucket ETL scripts with L1–L6 structure; remaining contract-only entries (e.g. `dim_pub_*`) retain contract-derived docs until ETL is added.

| Item | Path |
|------|------|
| Hub fact (order-line P&L) | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` |
| Bitbucket ETL snapshot | `source/contracts/b-report-us/bitbicket_etl/` |
| Domain knowledge | `source/contracts/b-report-us/domain-knowledge.md` |
| Metric index | `source/contracts/b-report-us/metric-index.md` |
| ETL → KB converter | `tools/ingest/b_report_etl_to_knowledgebase.py` |
| Contract → KB converter (L1–L6) | `tools/ingest/b_report_contract_l6_to_knowledgebase.py` |
| Legacy contract → KB (flat) | `tools/ingest/b_report_contract_to_knowledgebase.py` |

Regenerate ETL-backed docs (overwrite, no backup):

```bash
python tools/ingest/b_report_etl_to_knowledgebase.py --write-seeds
```

Regenerate contract-only dims (`dim_pub_*`, no Bitbucket ETL in b-report-us):

```bash
python tools/ingest/b_report_contract_l6_to_knowledgebase.py --pattern "dim_pub*" --write-seeds
```

Rebuild indexes:

```bash
python -m tools.wkb.indexing.index_builder
python -m tools.wkb.indexing.run_query --query "b-report-us dwd_disty_brpt_orders_pl_etl_mi schema" --intent find_table_schema
```
