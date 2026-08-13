import { describe, expect, it } from "vitest";
import {
  looksLikeMarkdown,
  looksLikeProse,
  normalizeNarrativeMarkdown,
  reassembleFragmentedTable,
  repairMarkdownStructure,
  shouldRenderAsMarkdown,
  stripResearchPreamble,
  unwrapProseCodeFences,
} from "./markdownOutput";

describe("looksLikeMarkdown", () => {
  it("detects headings and bullet lists", () => {
    expect(looksLikeMarkdown("### Analysis Approach\n\n- item")).toBe(true);
    expect(looksLikeMarkdown("SELECT 1")).toBe(false);
  });

  it("ignores JSON payloads", () => {
    expect(looksLikeMarkdown('{"rows": []}')).toBe(false);
  });
});

describe("looksLikeProse", () => {
  it("detects agent planning sentences", () => {
    expect(
      looksLikeProse(
        "Let me take a different approach and check the DWD table schema for PMID-706187."
      )
    ).toBe(true);
  });

  it("rejects SQL payloads", () => {
    expect(looksLikeProse("SELECT pm_id, ngm_pct FROM dm_us_om_bisty_bipt_pm_mto")).toBe(false);
  });
});

describe("stripResearchPreamble", () => {
  it("keeps content from ## Summary onward", () => {
    const raw = "Let me read the schema.\n\n## Summary\n\nNGM% fell.";
    expect(stripResearchPreamble(raw)).toBe("## Summary\n\nNGM% fell.");
  });

  it("keeps Based on the database answers after planning", () => {
    const raw =
      "Let me execute the query.\n\nBased on the database query for PM 706187, NGM% fell.";
    expect(stripResearchPreamble(raw)).toBe(
      "Based on the database query for PM 706187, NGM% fell."
    );
  });

  it("does not discard a streamed Chinese answer when wrap-up appends ## Summary", () => {
    const chinese = `C. 供应商维度分析

| Vendor | Feb | Mar |
| :--- | :--- | :--- |
| NVIDIA | 1 | 2 |

D. 订单与交叉维度分析
该单一业务链的 NGM% 从 2 月的 3.783% 降至 3 月的 1.767%。由于其绝对体量巨大，该客户组合是主要驱动因素。`;
    const raw = `Let me dig into vendors.\n\n${chinese}\n\n## Summary\n\nNGM% fell due to mix.`;
    const fixed = stripResearchPreamble(raw);
    expect(fixed).toContain("供应商维度分析");
    expect(fixed).toContain("主要驱动因素");
    expect(fixed).not.toMatch(/^## Summary/);
  });
});

describe("reassembleFragmentedTable", () => {
  it("joins vertically split pipe lines", () => {
    const raw = `|Month

| Segment| PM NetSales

| PMNGM |PM NGM%
| MNet Sales |M NGM`;
    const fixed = reassembleFragmentedTable(raw);
    expect(fixed.split("\n").filter((l) => l.includes("|")).length).toBeLessThan(6);
  });
});

describe("repairMarkdownStructure", () => {
  it("inserts newlines before glued headings", () => {
    const raw = "February vs. March## Summary\n\nNGM% dropped.";
    expect(repairMarkdownStructure(raw)).toContain("February vs. March\n\n## Summary");
  });

  it("splits table separator row onto its own line", () => {
    const raw = "| Metric | Feb | Mar || :--- | :--- | :--- |";
    const fixed = repairMarkdownStructure(raw);
    expect(fixed).toContain("|\n| :---");
  });

  it("adds blank line before table when preceded by prose", () => {
    const raw = "Totals below| A | B |\n| --- | --- |";
    expect(repairMarkdownStructure(raw)).toContain("below\n\n| A");
  });

  it("promotes glued bold answer section labels to headings", () => {
    const raw = "**Analysisapproach & confidence**DataExecution Limitation: query stopped.";
    expect(repairMarkdownStructure(raw)).toBe(
      "## Analysis approach & confidence\n\nData Execution Limitation: query stopped."
    );
  });

  it("splits glued top-N table rows onto separate lines", () => {
    const raw =
      "| ---:|---:|---:|---: | | 1 | -77294 | -$3,685,483.05 | 4,428 | | 2 | 621286 | -$897,747.95 | 619 |";
    const fixed = repairMarkdownStructure(raw);
    const rows = fixed.split("\n").filter((l) => l.trim().startsWith("|"));
    expect(rows.length).toBeGreaterThanOrEqual(3);
    expect(fixed).toContain("| 1 | -77294");
    expect(fixed).toContain("| 2 | 621286");
  });

  it("splits two logical rows glued on one line without double pipe", () => {
    const raw =
      "| Rank | Order | NGM |\n| --- | --- | --- |\n| 1 | -77294 | x | 2 | 621286 | x |";
    const fixed = repairMarkdownStructure(raw);
    expect(fixed).toContain("| 1 | -77294 | x");
    expect(fixed).toContain("| 2 | 621286 | x");
    const dataRows = fixed
      .split("\n")
      .filter((l) => /^\|\s*-?\d+\s*\|/.test(l.trim()));
    expect(dataRows.length).toBe(2);
  });
});

describe("normalizeNarrativeMarkdown", () => {
  it("strips planning and repairs PMID broken table sample", () => {
    const raw = `Let me do the local research first.

Let me execute the evidence query.

Basedon the databasequery forPM ID706187, hereis the NetSales and NGM performance datafor March andApril 2025, broken downby segment (seg_code):

|Month

| Segment| PM NetSales

| PMNGM |PM NGM%
| MNet Sales |M NGM
M NGM %
| :--- | :---
| :--- | :---
| :--- | :---
| :--- | :---
| :--- || March2025
| OTH| $3,018,274.57
|-$88,668.68 | -2.94%
|$5,106,307.14 | $359,906.06
|7.05% || March 2025
| SID| $16,437,951.17
| $845,508.26| 5.14%
| $24,647,052.22 | $406,817.79
|1.65% |KeyNotes:* PM refers tothe current month's performance.`;

    const fixed = normalizeNarrativeMarkdown(raw);
    expect(fixed).not.toMatch(/^Let me /);
    expect(fixed).toContain("Based on the database query");
    expect(fixed).toContain("March 2025");
    expect(fixed).toContain("## Key Notes");
    const pipeLines = fixed.split("\n").filter((l) => l.trim().startsWith("|"));
    expect(pipeLines.length).toBeLessThan(15);
    expect(pipeLines.some((l) => /March 2025.*OTH/i.test(l) || /OTH.*March 2025/i.test(l))).toBe(
      true
    );
  });

  it("unwraps a closed markdown fence", () => {
    const raw = "```markdown\n## Summary\n\nRevenue is up.\n```";
    expect(normalizeNarrativeMarkdown(raw)).toBe("## Summary\n\nRevenue is up.");
  });

  it("unwraps a plain prose fence without language tag", () => {
    const raw =
      "```\nLet me take a different approach.\n\n1. Find the DWS PM table\n```";
    expect(normalizeNarrativeMarkdown(raw)).toBe(
      "Let me take a different approach.\n\n1. Find the DWS PM table"
    );
  });

  it("unwraps streaming prose fences", () => {
    const raw = "```\nLet me take a different approach";
    expect(normalizeNarrativeMarkdown(raw, true)).toBe("Let me take a different approach");
  });

  it("keeps streaming sql fences", () => {
    const raw = "```sql\nSELECT 1";
    expect(normalizeNarrativeMarkdown(raw, true)).toBe(raw);
  });

  it("unwraps embedded prose fences inside a longer answer", () => {
    const raw =
      "Intro.\n\n```\nBased on the vectorsearch results:\n\n### Recommended Table\n```\n\nOutro.";
    expect(normalizeNarrativeMarkdown(raw)).toContain("### Recommended Table");
    expect(normalizeNarrativeMarkdown(raw)).not.toContain("```\nBased on");
  });

  it("repairs negative NGM top-10 glued table sample", () => {
    const raw = `Top 10 negative-NGM orders — 2026-04-30
| Rank | Order

| NGM | Order lines |
| ---:|---:|---:|---: | | 1 | -77294 | -$3,685,483.05 | 4,428 | | 2 | 621286 | -$897,747.95 | 619 |`;

    const fixed = normalizeNarrativeMarkdown(raw);
    const pipeLines = fixed.split("\n").filter((l) => l.trim().startsWith("|"));
    expect(pipeLines.length).toBeGreaterThanOrEqual(4);
    expect(fixed).toContain("| Rank | Order | NGM | Order lines |");
    expect(fixed).toContain("| 1 | -77294");
    expect(fixed).toContain("| 2 | 621286");
  });

  it("renders all 10 rows when pairs are glued per line", () => {
    const glued = `| Rank | Order | NGM |
| --- | --- | --- |
| 1 | -77294 | x | 2 | 621286 | x |
| 3 | 657888 | x | 4 | 141692 | x |
| 5 | 413709 | x | 6 | 173937798 | x |
| 7 | 124858 | x | 8 | 529859 | x |
| 9 | 303148 | x | 10 | 695266 | x |`;
    const fixed = normalizeNarrativeMarkdown(glued);
    const dataRows = fixed
      .split("\n")
      .filter((l) => /^\|\s*-?\d+\s*\|/.test(l.trim()));
    expect(dataRows.length).toBe(10);
  });

  it("keeps all 10 rows of a clean low-column GFM table (regression)", () => {
    // A well-formed 2-column table (the exact shape Vertica top-N answers emit)
    // must not have its rows merged pairwise into "only odd ranks render".
    const clean = `## Summary

Top 10 negative-NGM orders — 2026-04-30

| order_no | ngm_amt |
| :--- | :--- |
| -77294 | -3,685,483.05 |
| 621286 | -897,747.95 |
| 657888 | -703,095.59 |
| 141692 | -485,643.24 |
| 413709 | -415,449.31 |
| 173937798 | -331,151.33 |
| 124858 | -314,671.20 |
| 529859 | -311,374.70 |
| 303148 | -307,996.14 |
| 695266 | -264,985.81 |`;

    const fixed = normalizeNarrativeMarkdown(clean);
    const dataRows = fixed
      .split("\n")
      .filter((l) => /^\|\s*-?\d+\s*\|/.test(l.trim()));
    expect(dataRows.length).toBe(10);
    for (const id of [
      "-77294", "621286", "657888", "141692", "413709",
      "173937798", "124858", "529859", "303148", "695266",
    ]) {
      expect(fixed).toContain(id);
    }
  });
});

describe("unwrapProseCodeFences", () => {
  it("preserves sql blocks", () => {
    const raw = "Before\n\n```sql\nSELECT 1\n```\n\nAfter";
    expect(unwrapProseCodeFences(raw)).toBe(raw);
  });
});

describe("shouldRenderAsMarkdown", () => {
  it("returns true for fenced planning text", () => {
    expect(shouldRenderAsMarkdown("```\nLet me query the DWS table next.\n```")).toBe(true);
  });
});
