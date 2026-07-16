#!/usr/bin/env python3
"""Sync contract-guided skill + b-report-us docs from bigdata_wiki_llm_1 into data_agent bundle + runtime."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = Path("/data/workplace/bigdata_wiki_llm_1")
BUNDLE = ROOT / "backend/defaults/b_report"
RUNTIME_SKILL = ROOT / "backend/defaults/b_report/skills/contract-guided-data-analysis"
RUNTIME_FILES = ROOT / "workspace/local/files"
RUNTIME_RULES = ROOT / "workspace/local/rules"

WIKI_SKILL = WIKI / ".cursor/skills/contract-guided-data-analysis"
DA_SKILL = BUNDLE / "skills/contract-guided-data-analysis"
APPEND_SQL = BUNDLE / "fragments/sql-planning.data-agent-append.md"
VERTICA_FRAG = BUNDLE / "fragments/contract-data-analysis-vertica.md"
WIKI_VERTICA_MDC = WIKI / ".cursor/rules/contract-data-analysis-vertica.mdc"

PATH_REPLACEMENTS = [
    (r"`source/contracts/", "`/workspace/source/contracts/"),
    (r"`source/ref/", "`/workspace/source/ref/"),
    (r" source/contracts/", " /workspace/source/contracts/"),
    (r" source/ref/", " /workspace/source/ref/"),
    (r"`target/storage/", "`/workspace/target/storage/"),
    (r"`target/knowledgebase/", "`/workspace/target/knowledgebase/"),
    (r"target/storage/wkb/", "/workspace/target/storage/wkb/"),
    (r"target/knowledgebase/", "/workspace/target/knowledgebase/"),
    (r"user-gateway-vertica-prod", "gateway-vertica-prod"),
    (r"\.\./\.\./rules/contract-data-analysis-vertica\.mdc", "/rules/contract-data-analysis-vertica.md"),
    (r"\.cursor/rules/contract-data-analysis-vertica\.mdc", "/rules/contract-data-analysis-vertica.md"),
    (r"from cwd `/workspace`", "from cwd `/workspace`"),
]


def adapt_paths(text: str) -> str:
    for old, new in PATH_REPLACEMENTS:
        text = re.sub(old, new, text)
    # collapse accidental double prefixes
    while "/workspace//workspace/" in text:
        text = text.replace("/workspace//workspace/", "/workspace/")
    return text


def extract_mdc_body(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---"):
        end = raw.find("---", 3)
        if end != -1:
            return raw[end + 3 :].lstrip()
    return raw


def merge_vertica_rule() -> str:
    wiki_body = extract_mdc_body(WIKI_VERTICA_MDC)
    wiki_body = adapt_paths(wiki_body)
    wiki_body = wiki_body.replace(
        "**Server:** `gateway-vertica-prod`",
        "**Server:** `gateway-vertica-prod`",
    )
    if VERTICA_FRAG.exists():
        da = VERTICA_FRAG.read_text(encoding="utf-8")
        # Keep data_agent harness extras if wiki mdc lacks them
        extras = []
        for line in da.splitlines():
            if any(
                k in line
                for k in (
                    "/workspace/",
                    "gateway-vertica-prod",
                    "mom_pct",
                    "pl_item",
                    "comb_mtd",
                    "month_flag",
                    "target/analysis",
                )
            ):
                extras.append(line)
        if "**Server:** `gateway-vertica-prod`" not in wiki_body:
            wiki_body = wiki_body.replace(
                "**Server:** `user-gateway-vertica-prod`",
                "**Server:** `gateway-vertica-prod`",
            )
        # Prefer data_agent fragment as base (already merged harness); inject wiki-only bullets
        base = da
        if "order filters (non-default)" in wiki_body and "order filters" not in base:
            insert = (
                "- **b-report-us order filters (non-default):** do **not** apply "
                "`dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1` "
                "unless the question explicitly asks for shipped orders only. "
                "For DWD profitability pulls, still use `segment_exclude = 'N'` per "
                "`/workspace/source/ref/b-report-us/special_logic.txt`.\n"
            )
            base = base.replace(
                "- `dw_us.dwd_disty_brpt_orders_pl_etl_mi`:",
                insert + "- `dw_us.dwd_disty_brpt_orders_pl_etl_mi`:",
            )
        return base
    return wiki_body


def build_skill_md() -> str:
    wiki = (WIKI_SKILL / "SKILL.md").read_text(encoding="utf-8")
    # strip wiki write-analysis tail; data_agent uses chat-only output
    lines = wiki.splitlines()
    out: list[str] = []
    skip = False
    for line in lines:
        if line.strip() == "## Output" and "target/analysis" in wiki:
            break
        if "| `write_analysis`" in line:
            continue
        if line.strip().startswith("13. Write"):
            continue
        out.append(line)
    text = "\n".join(out).rstrip() + "\n"

    if "**Answers render in chat only**" not in text:
        text = text.replace(
            "See [`references/local-research-first.md`](references/local-research-first.md).",
            "See [`references/local-research-first.md`](references/local-research-first.md).\n\n"
            "**Answers render in chat only** — do not write analysis files under `/workspace/target/analysis/`.",
        )

    # Patch workflow to wiki question-shape + output-contract while keeping /workspace paths
    text = re.sub(
        r"1\. Classify intent \+ domain —.*",
        "1. Classify intent + domain — [`references/question-shape.md`](references/question-shape.md)",
        text,
        count=1,
    )
    text = re.sub(
        r"3\. `source/contracts/",
        "3. `source/contracts/",
        text,
    )
    text = re.sub(
        r"4\. `source/contracts/",
        "4. `source/contracts/",
        text,
    )
    text = re.sub(
        r"5\. Optional `source/contracts/",
        "5. Optional `source/contracts/",
        text,
    )
    text = re.sub(
        r"6\. Special logic check —.*\n",
        "6. Special logic check — [`references/special-logic-check.md`](references/special-logic-check.md) "
        "→ `source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` "
        "(when present); always check `special_logic.txt` for logic tied to the resolved table(s)\n",
        text,
        count=1,
    )
    text = re.sub(
        r"7\. Storage layer metadata search —.*\n",
        "7. Storage layer metadata search — [`references/wkb-retrieval.md`](references/wkb-retrieval.md) "
        "→ `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` before opening knowledgebase docs\n",
        text,
        count=1,
    )
    text = re.sub(
        r"8\. Knowledgebase table docs →.*\n",
        "8. Knowledgebase table docs → `target/knowledgebase/{domain}/{stem}.md` where "
        "**`stem = FQN.split(\".\")[-1]`**. On 404, `ls` the knowledgebase folder and retry. "
        "**NEVER** read `source/contracts/{domain}/tables/*.md`\n",
        text,
        count=1,
    )
    text = re.sub(
        r"10\. Entity Phase-1 \(if labels\) —.*\n",
        "10. Entity Phase-1 (if labels) — bounded dim probe per [`references/entity-resolution.md`](references/entity-resolution.md)\n",
        text,
        count=1,
    )
    text = re.sub(
        r"12\. Synthesize —.*\n",
        "12. Synthesize three-section chat answer — [`references/output-contract.md`](references/output-contract.md) "
        "and [`references/confidence-provenance.md`](references/confidence-provenance.md)\n",
        text,
        count=1,
    )

    text += """
**Path note:** `/workspace/` is the correct virtual root in data_agent (seeded from `backend/defaults/b_report/workspace/`). Do not look for host paths under `defaults/` at runtime.

## Output (chat only)

- Do **not** write files under `/workspace/target/analysis/`
- Include `metric-index.md` citations; `result_status: data_found | no_data_found`
- Three sections: **Summary** / **Evidence** / **Analysis approach & confidence**
- Vertica rule: `/rules/contract-data-analysis-vertica.md`

## Validation checklist

See [`references/analysis-output.md`](references/analysis-output.md) § Validation scenarios.
"""
    return adapt_paths(text)


def sync_skill() -> None:
    if DA_SKILL.exists():
        shutil.rmtree(DA_SKILL)
    shutil.copytree(WIKI_SKILL, DA_SKILL)
    (DA_SKILL / "SKILL.md").write_text(build_skill_md(), encoding="utf-8")
    for path in DA_SKILL.rglob("*"):
        if path.is_file() and path.name == "SKILL.md":
            continue
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            path.write_text(adapt_paths(path.read_text(encoding="utf-8")), encoding="utf-8")
    # Append data_agent SQL harness notes
    sql = DA_SKILL / "references" / "sql-planning.md"
    append = APPEND_SQL.read_text(encoding="utf-8")
    body = sql.read_text(encoding="utf-8")
    if "P&L item semantics (NGM decomposition) — data_agent" not in body:
        sql.write_text(body.rstrip() + "\n" + append, encoding="utf-8")
    # Chat-only: drop write_analysis stage from manifest copy
    manifest = DA_SKILL / "references" / "_manifest.yaml"
    m = manifest.read_text(encoding="utf-8")
    m = re.sub(r"\n  write_analysis:.*?(?=\n\S|\Z)", "", m, flags=re.S)
    manifest.write_text(m, encoding="utf-8")


def sync_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def sync_workspace() -> None:
    sync_tree(
        WIKI / "source/contracts/b-report-us",
        BUNDLE / "workspace/source/contracts/b-report-us",
    )
    sync_tree(
        WIKI / "source/ref/b-report-us",
        BUNDLE / "workspace/source/ref/b-report-us",
    )
    kb_dest = BUNDLE / "workspace/target/knowledgebase/b-report-us"
    kb_dest.mkdir(parents=True, exist_ok=True)
    for f in (WIKI / "target/knowledgebase/b-report-us").glob("*.md"):
        shutil.copy2(f, kb_dest / f.name)


def sync_runtime() -> None:
    if RUNTIME_SKILL.parent.exists():
        if RUNTIME_SKILL.exists():
            shutil.rmtree(RUNTIME_SKILL)
        shutil.copytree(DA_SKILL, RUNTIME_SKILL)
    ws_contracts = RUNTIME_FILES / "source/contracts/b-report-us"
    ws_ref = RUNTIME_FILES / "source/ref/b-report-us"
    ws_kb = RUNTIME_FILES / "target/knowledgebase/b-report-us"
    sync_tree(BUNDLE / "workspace/source/contracts/b-report-us", ws_contracts)
    sync_tree(BUNDLE / "workspace/source/ref/b-report-us", ws_ref)
    ws_kb.mkdir(parents=True, exist_ok=True)
    for f in (BUNDLE / "workspace/target/knowledgebase/b-report-us").glob("*.md"):
        shutil.copy2(f, ws_kb / f.name)
    merged = merge_vertica_rule()
    VERTICA_FRAG.write_text(merged, encoding="utf-8")
    if RUNTIME_RULES.exists():
        (RUNTIME_RULES / "contract-data-analysis-vertica.md").write_text(
            merged, encoding="utf-8"
        )


def main() -> int:
    if not WIKI.is_dir():
        print(f"wiki not found: {WIKI}", file=sys.stderr)
        return 1
    print("==> Syncing skill from wiki")
    sync_skill()
    print("==> Syncing b-report-us contracts, ref, knowledgebase")
    sync_workspace()
    print("==> Syncing runtime workspace/local (personal overrides only)")
    sync_runtime()
    print("==> Done. Run scripts/seed_b_report.sh to rebuild WKB index if needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
