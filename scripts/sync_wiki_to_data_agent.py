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
RUNTIME_FILES = ROOT / "workspace/local/files"
RUNTIME_RULES = ROOT / "workspace/local/rules"

WIKI_SKILL = WIKI / ".cursor/skills/contract-guided-data-analysis"
DA_SKILL = BUNDLE / "skills/contract-guided-data-analysis"
APPEND_SQL = BUNDLE / "fragments/sql-planning.data-agent-append.md"
VERTICA_FRAG = BUNDLE / "fragments/contract-data-analysis-vertica.md"
CLARIFICATION_FRAG = BUNDLE / "fragments/AGENTS.analysis-clarification.md"
WIKI_VERTICA_MDC = WIKI / ".cursor/rules/contract-data-analysis-vertica.mdc"
WIKI_CLARIFICATION_MDC = WIKI / ".cursor/rules/analysis-clarification-before-routing.mdc"

ORG_PREFIX = "/knowledge/org"

# data_agent-specific reference files — restored after wiki copy (not overwritten by wiki)
OVERLAY_REL_PATHS = (
    "references/wkb-retrieval.md",
    "references/analysis-output.md",
)

PATH_REPLACEMENTS = [
    (r"`source/contracts/", f"`{ORG_PREFIX}/source/contracts/"),
    (r"`source/ref/", f"`{ORG_PREFIX}/source/ref/"),
    (r" source/contracts/", f" {ORG_PREFIX}/source/contracts/"),
    (r" source/ref/", f" {ORG_PREFIX}/source/ref/"),
    (r"`target/storage/", f"`{ORG_PREFIX}/target/storage/"),
    (r"`target/knowledgebase/", f"`{ORG_PREFIX}/target/knowledgebase/"),
    (r"target/storage/wkb/", f"{ORG_PREFIX}/target/storage/wkb/"),
    (r"target/knowledgebase/", f"{ORG_PREFIX}/target/knowledgebase/"),
    (r"`/workspace/source/contracts/", f"`{ORG_PREFIX}/source/contracts/"),
    (r"`/workspace/source/ref/", f"`{ORG_PREFIX}/source/ref/"),
    (r"`/workspace/target/storage/", f"`{ORG_PREFIX}/target/storage/"),
    (r"`/workspace/target/knowledgebase/", f"`{ORG_PREFIX}/target/knowledgebase/"),
    (r"/workspace/source/contracts/", f"{ORG_PREFIX}/source/contracts/"),
    (r"/workspace/source/ref/", f"{ORG_PREFIX}/source/ref/"),
    (r"/workspace/target/storage/", f"{ORG_PREFIX}/target/storage/"),
    (r"/workspace/target/knowledgebase/", f"{ORG_PREFIX}/target/knowledgebase/"),
    (r"user-gateway-vertica-prod", "gateway-vertica-prod"),
    (
        r"\.\./\.\./rules/contract-data-analysis-vertica\.mdc",
        "/rules/org/contract-data-analysis-vertica.md",
    ),
    (
        r"\.cursor/rules/contract-data-analysis-vertica\.mdc",
        "/rules/org/contract-data-analysis-vertica.md",
    ),
    (r"/rules/contract-data-analysis-vertica\.md", "/rules/org/contract-data-analysis-vertica.md"),
]

DEFAULT_FRONTMATTER = """---
name: contract-guided-data-analysis
description: |
  Contract-first business data analysis with local md/WKB research before Vertica evidence SQL.
  Use when: KPI lookup, ranking, trend, comparison, variance drivers, POS/B Report metrics, validate numbers, data anomaly.
    Routes via source/contracts domain-knowledge → metric-index → source/ref special_logic → storage-layer (l1_catalog) → knowledgebase.
  Don't use when: ETL change requests, flow edits, DDL/DML, unrestricted warehouse exploration, email intake (use etl-email-change-intake).
extensions:
  rules:
    - /rules/org/AGENTS.contract-skill.md
    - /rules/org/AGENTS.analysis-clarification.md
    - /rules/org/contract-data-analysis-vertica.md
  tools: [wkb_query]
  mcp: [gateway-vertica-prod]
harness:
  phases: [research, execute, synthesize]
  tool_budgets:
    run_query_safely: 12
    execute_query_paginated: 12
    wkb_query: 8
  require_synthesis: true
---"""


def adapt_paths(text: str) -> str:
    for old, new in PATH_REPLACEMENTS:
        text = re.sub(old, new, text)
    while f"{ORG_PREFIX}//" in text:
        text = text.replace(f"{ORG_PREFIX}//", f"{ORG_PREFIX}/")
    while "/knowledge/org/knowledge/org/" in text:
        text = text.replace("/knowledge/org/knowledge/org/", "/knowledge/org/")
    return text


def extract_yaml_frontmatter(path: Path) -> str:
    if not path.is_file():
        return DEFAULT_FRONTMATTER
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return DEFAULT_FRONTMATTER
    end = raw.find("---", 3)
    if end == -1:
        return DEFAULT_FRONTMATTER
    block = raw[: end + 3]
    if "extensions:" not in block or "harness:" not in block:
        return DEFAULT_FRONTMATTER
    if "/rules/org/AGENTS.analysis-clarification.md" not in block:
        block = block.replace(
            "    - /rules/org/AGENTS.contract-skill.md\n",
            "    - /rules/org/AGENTS.contract-skill.md\n"
            "    - /rules/org/AGENTS.analysis-clarification.md\n",
        )
    return block


def sync_clarification_fragment() -> None:
    if not WIKI_CLARIFICATION_MDC.is_file():
        return
    body = adapt_paths(extract_mdc_body(WIKI_CLARIFICATION_MDC))
    body = body.replace(
        ".cursor/skills/contract-guided-data-analysis/references/output-contract.md",
        "/skills/org/contract-guided-data-analysis/references/output-contract.md",
    )
    body = body.replace(
        "`target/analysis/*.md`",
        "chat analysis answers",
    )
    CLARIFICATION_FRAG.write_text(body.rstrip() + "\n", encoding="utf-8")


def backup_overlays() -> dict[str, str]:
    backups: dict[str, str] = {}
    for rel in OVERLAY_REL_PATHS:
        path = DA_SKILL / rel
        if path.is_file():
            backups[rel] = path.read_text(encoding="utf-8")
    return backups


def restore_overlays(backups: dict[str, str]) -> None:
    for rel, content in backups.items():
        (DA_SKILL / rel).write_text(content, encoding="utf-8")


def extract_mdc_body(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---"):
        end = raw.find("---", 3)
        if end != -1:
            return raw[end + 3 :].lstrip()
    return raw


def merge_vertica_rule() -> str:
    wiki_body = adapt_paths(extract_mdc_body(WIKI_VERTICA_MDC))
    if VERTICA_FRAG.exists():
        da = VERTICA_FRAG.read_text(encoding="utf-8")
        base = da
        if "order filters (non-default)" in wiki_body and "order filters" not in base:
            insert = (
                "- **b-report-us order filters (non-default):** do **not** apply "
                "`dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1` "
                "unless the question explicitly asks for shipped orders only. "
                "For DWD profitability pulls, still use `segment_exclude = 'N'` per "
                f"`{ORG_PREFIX}/source/ref/b-report-us/special_logic.txt`.\n"
            )
            base = base.replace(
                "- `dw_us.dwd_disty_brpt_orders_pl_etl_mi`:",
                insert + "- `dw_us.dwd_disty_brpt_orders_pl_etl_mi`:",
            )
        return adapt_paths(base)
    return wiki_body


def strip_markdown_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3 :].lstrip()
    return text


def build_skill_md(frontmatter: str) -> str:
    wiki = strip_markdown_frontmatter((WIKI_SKILL / "SKILL.md").read_text(encoding="utf-8"))
    lines = wiki.splitlines()
    out: list[str] = []
    for line in lines:
        if line.strip() == "## Output" and "target/analysis" in wiki:
            break
        if "| `write_analysis`" in line:
            continue
        if "| `golden_cases_match`" in line:
            continue
        if "Optional " in line and "eval/golden_cases.md" in line:
            continue
        if "`/knowledge/org/source/contracts/{domain}/eval/golden_cases.md`" in line:
            continue
        if "`source/contracts/{domain}/eval/golden_cases.md`" in line:
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

    text = re.sub(
        r"1\. Classify intent \+ domain —.*",
        "1. Classify intent + domain — [`references/question-shape.md`](references/question-shape.md)",
        text,
        count=1,
    )
    text = re.sub(
        r"5\. Special logic check —.*\n",
        "5. Special logic check — [`references/special-logic-check.md`](references/special-logic-check.md) "
        f"→ `{ORG_PREFIX}/source/ref/{{domain}}/special_logic.txt`, `table list.txt`, `table relationship.txt` "
        "(when present); always check `special_logic.txt` for logic tied to the resolved table(s)\n",
        text,
        count=1,
    )
    text = re.sub(
        r"6\. Storage layer metadata search —.*\n",
        "6. Storage layer metadata search — [`references/wkb-retrieval.md`](references/wkb-retrieval.md) "
        "→ use `wkb_query` before opening knowledgebase docs (no `l1_catalog` JSON pagination)\n",
        text,
        count=1,
    )
    text = re.sub(
        r"7\. Knowledgebase table docs →.*\n",
        f"7. Knowledgebase table docs → `{ORG_PREFIX}/target/knowledgebase/{{domain}}/{{stem}}.md` where "
        '**`stem = FQN.split(".")[-1]`**. On 404, `ls` the knowledgebase folder and retry. '
        f"**NEVER** read `{ORG_PREFIX}/source/contracts/{{domain}}/tables/*.md`\n",
        text,
        count=1,
    )
    text = re.sub(
        r"9\. Entity Phase-1 \(if labels\) —.*\n",
        "9. Entity Phase-1 (if labels) — bounded dim probe per [`references/entity-resolution.md`](references/entity-resolution.md)\n",
        text,
        count=1,
    )
    text = re.sub(
        r"11\. Synthesize —.*\n",
        "11. Synthesize three-section chat answer — [`references/output-contract.md`](references/output-contract.md) "
        "and [`references/confidence-provenance.md`](references/confidence-provenance.md)\n",
        text,
        count=1,
    )

    text = adapt_paths(text)
    text = text.replace(" → optional eval/golden_cases", "")
    text += f"""
**Path note:** Org contracts / WKB / knowledgebase live under `{ORG_PREFIX}/` (mounted read-only from `backend/defaults/b_report/workspace/`). Personal writable files are under `/workspace/`. Do not look for host paths under `defaults/` at runtime.

## Output (chat only)

- Do **not** write files under `/workspace/target/analysis/`
- Include `metric-index.md` citations; `result_status: data_found | no_data_found`
- Three sections: **Summary** / **Evidence** / **Analysis approach & confidence** — no SQL in those sections
- Executed Vertica SQL is appended automatically by the platform under **## Vertica validation**; reference it instead of pasting SQL
- Vertica rule: `/rules/org/contract-data-analysis-vertica.md`

## Validation checklist

See [`references/analysis-output.md`](references/analysis-output.md) § Validation scenarios.
"""
    return frontmatter.rstrip() + "\n\n" + text.lstrip()


def apply_data_agent_overlays() -> None:
    """Post-sync overlays not present in wiki (sql append, manifest write_analysis removal)."""
    sql = DA_SKILL / "references" / "sql-planning.md"
    if sql.is_file() and APPEND_SQL.is_file():
        body = sql.read_text(encoding="utf-8")
        body = re.sub(
            rf"\n1\. `{re.escape(ORG_PREFIX)}/source/contracts/\{{domain\}}/eval/golden_cases\.md` routing-certified case \(when file exists and matches\)\n",
            "\n",
            body,
        )
        body = body.replace(
            "2. `/knowledge/org/source/contracts/{domain}/metric-index.md`",
            "1. `/knowledge/org/source/contracts/{domain}/metric-index.md`",
        )
        body = body.replace("3. Selected table L6", "2. Selected table L6")
        body = body.replace("4. Entity Resolution", "3. Entity Resolution")
        body = body.replace("5. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md`", "4. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md`")
        body = body.replace("6. Table L3", "5. Table L3")
        body = body.replace(
            "**Forbidden:** `golden-questions.md`. Do not borrow time logic from unrelated domains.",
            "**Forbidden:** `golden-questions.md`, `eval/golden_cases.md`. Do not borrow time logic from unrelated domains.",
        )
        append = APPEND_SQL.read_text(encoding="utf-8")
        if "P&L item semantics (NGM decomposition) — data_agent" not in body:
            sql.write_text(body.rstrip() + "\n" + append, encoding="utf-8")
        else:
            sql.write_text(body, encoding="utf-8")

    replacements = {
        "references/README.md": [
            (r"\n\| `golden-cases-match\.md` \| Optional `eval/golden_cases\.md` matching \|", ""),
            (" (domain-knowledge, metric-index, eval/golden_cases)", " (domain-knowledge, metric-index)"),
        ],
        "references/local-research-first.md": [
            (r"\n\| Golden eval \| `/knowledge/org/source/contracts/\{domain\}/eval/golden_cases\.md` \(if file exists\) \|", ""),
        ],
        "references/scope-guardrail.md": [
            (r"\n- `/knowledge/org/source/contracts/\{domain\}/eval/golden_cases\.md` \(when present\)", ""),
        ],
        "references/domain-routing.md": [
            (r"\n\s*eval/golden_cases\.md\s*# optional; not in all domains", ""),
        ],
    }
    for rel, rules in replacements.items():
        path = DA_SKILL / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in rules:
            text = re.sub(old, new, text)
        path.write_text(text, encoding="utf-8")

    manifest = DA_SKILL / "references" / "_manifest.yaml"
    if manifest.is_file():
        m = manifest.read_text(encoding="utf-8")
        m = re.sub(r"\n  write_analysis:.*?(?=\n\S|\Z)", "", m, flags=re.S)
        m = re.sub(r"\n  golden_cases_match:.*?(?=\n  \w|\Z)", "", m, flags=re.S)
        if "eval/golden_cases.md" not in m:
            m = m.replace(
                "forbidden_paths:\n",
                "forbidden_paths:\n  - /knowledge/org/source/contracts/**/eval/golden_cases.md\n",
                1,
            )
        manifest.write_text(m, encoding="utf-8")

    analysis = DA_SKILL / "references" / "analysis-output.md"
    if analysis.is_file():
        text = analysis.read_text(encoding="utf-8")
        text = re.sub(
            r"Never cite or reference `golden-questions\.md`(?: or `eval/golden_cases\.md`)?",
            "Never cite or reference `golden-questions.md` or `eval/golden_cases.md`",
            text,
        )
        text = re.sub(
            r"Agent never opens `golden-questions\.md`(?:, `eval/golden_cases\.md`,)? or `source/contracts/\{domain\}/tables/\*\.md`",
            "Agent never opens `golden-questions.md`, `eval/golden_cases.md`, or `source/contracts/{domain}/tables/*.md`",
            text,
        )
        analysis.write_text(text, encoding="utf-8")

    wkb = DA_SKILL / "references" / "wkb-retrieval.md"
    if wkb.is_file():
        text = wkb.read_text(encoding="utf-8")
        text = text.replace(
            "Validation ideas; prefer `/knowledge/org/source/contracts/{domain}/eval/golden_cases.md` when present",
            "Validation ideas; use metric-index routing checks only — do not read `eval/golden_cases.md`",
        )
        wkb.write_text(text, encoding="utf-8")


def sync_skill(overlay_backups: dict[str, str]) -> None:
    frontmatter = DEFAULT_FRONTMATTER
    if DA_SKILL.exists() and (DA_SKILL / "SKILL.md").is_file():
        existing = extract_yaml_frontmatter(DA_SKILL / "SKILL.md")
        if "extensions:" in existing and "harness:" in existing:
            frontmatter = existing
            frontmatter = re.sub(
                r"optional eval/golden_cases → ",
                "",
                frontmatter,
            )
            frontmatter = frontmatter.replace(
                "metric-index → source/ref",
                "metric-index → source/ref",
            )
    if DA_SKILL.exists():
        shutil.rmtree(DA_SKILL)
    shutil.copytree(WIKI_SKILL, DA_SKILL)
    (DA_SKILL / "SKILL.md").write_text(build_skill_md(frontmatter), encoding="utf-8")
    for path in DA_SKILL.rglob("*"):
        if path.is_file() and path.name == "SKILL.md":
            continue
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            path.write_text(adapt_paths(path.read_text(encoding="utf-8")), encoding="utf-8")
    restore_overlays(overlay_backups)
    apply_data_agent_overlays()


def sync_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def sync_knowledgebase(wiki_kb_root: Path, dest_kb_root: Path) -> None:
    """Sync every domain folder under target/knowledgebase/."""
    dest_kb_root.mkdir(parents=True, exist_ok=True)
    if not wiki_kb_root.is_dir():
        return
    for src in sorted(wiki_kb_root.iterdir()):
        if not src.is_dir():
            continue
        sync_tree(src, dest_kb_root / src.name)


def sync_workspace() -> None:
    sync_tree(
        WIKI / "source/contracts/b-report-us",
        BUNDLE / "workspace/source/contracts/b-report-us",
    )
    sync_tree(
        WIKI / "source/ref/b-report-us",
        BUNDLE / "workspace/source/ref/b-report-us",
    )
    sync_knowledgebase(
        WIKI / "target/knowledgebase",
        BUNDLE / "workspace/target/knowledgebase",
    )
    l1_src = WIKI / "target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog"
    l1_dest = (
        BUNDLE / "workspace/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog"
    )
    if l1_src.is_dir():
        sync_tree(l1_src, l1_dest)
    pos_dk = WIKI / "source/contracts/pos/domain-knowledge.md"
    pos_dest = BUNDLE / "workspace/source/contracts/pos/domain-knowledge.md"
    if pos_dk.is_file():
        pos_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pos_dk, pos_dest)


def sync_runtime() -> None:
    if not RUNTIME_FILES.parent.exists():
        return
    ws_contracts = RUNTIME_FILES / "source/contracts/b-report-us"
    ws_ref = RUNTIME_FILES / "source/ref/b-report-us"
    ws_kb_root = RUNTIME_FILES / "target/knowledgebase"
    sync_tree(BUNDLE / "workspace/source/contracts/b-report-us", ws_contracts)
    sync_tree(BUNDLE / "workspace/source/ref/b-report-us", ws_ref)
    sync_knowledgebase(BUNDLE / "workspace/target/knowledgebase", ws_kb_root)
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
    overlay_backups = backup_overlays()
    print("==> Syncing skill from wiki")
    sync_skill(overlay_backups)
    print("==> Syncing b-report-us contracts, ref, full knowledgebase, l1_catalog")
    sync_workspace()
    print("==> Syncing org rule fragments (vertica, analysis-clarification)")
    sync_clarification_fragment()
    merged = merge_vertica_rule()
    VERTICA_FRAG.write_text(merged, encoding="utf-8")
    print("==> Syncing runtime workspace/local (personal overrides only)")
    sync_runtime()
    print("==> Done. Rebuild WKB index: cd backend/defaults/b_report/workspace && python3 -m tools.wkb.indexing.index_builder")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
