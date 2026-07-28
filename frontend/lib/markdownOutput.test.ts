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
