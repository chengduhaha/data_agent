import { describe, expect, it } from "vitest";
import { isPlanningOnly, splitAssistantContent } from "./messageContent";

describe("splitAssistantContent", () => {
  it("returns plain narrative unchanged when there is no appendix", () => {
    const result = splitAssistantContent("## Summary\n\nRevenue is up 5%.");
    expect(result.narrative).toBe("## Summary\n\nRevenue is up 5%.");
    expect(result.queryAppendix).toEqual([]);
    expect(result.appendixOnly).toBe(false);
  });

  it("splits narrative from a legacy inline query validation section", () => {
    const content =
      "## Summary\n\nRevenue is up 5%.\n\n---\n\n## Query validation\n\n```sql\nSELECT 1\n```\n";
    const result = splitAssistantContent(content);
    expect(result.narrative).toBe("## Summary\n\nRevenue is up 5%.");
    expect(result.queryAppendix).toEqual([{ sql: "SELECT 1" }]);
    expect(result.appendixOnly).toBe(false);
  });

  it("still recognizes the legacy '## Vertica validation' heading", () => {
    const content = "Answer here.\n\n---\n\n## Vertica validation\n\n```sql\nSELECT 2\n```\n";
    const result = splitAssistantContent(content);
    expect(result.narrative).toBe("Answer here.");
    expect(result.queryAppendix).toEqual([{ sql: "SELECT 2" }]);
  });

  it("flags a message that is only a bare SQL block as appendixOnly (incomplete answer)", () => {
    const content = "```sql\nSELECT * FROM foo\n```";
    const result = splitAssistantContent(content);
    expect(result.narrative).toBe("");
    expect(result.appendixOnly).toBe(true);
    expect(result.queryAppendix).toEqual([{ sql: "SELECT * FROM foo" }]);
  });

  it("handles empty content", () => {
    const result = splitAssistantContent("");
    expect(result.narrative).toBe("");
    expect(result.queryAppendix).toEqual([]);
    expect(result.appendixOnly).toBe(false);
  });

  it("parses multiple SQL blocks in the appendix", () => {
    const content =
      "Findings.\n\n---\n\n## Query validation\n\n```sql\nSELECT 1\n```\n\n```sql\nSELECT 2\n```\n";
    const result = splitAssistantContent(content);
    expect(result.queryAppendix).toEqual([{ sql: "SELECT 1" }, { sql: "SELECT 2" }]);
  });
});

describe("isPlanningOnly", () => {
  it("detects a short planning sentence", () => {
    expect(isPlanningOnly("Now let me query the revenue table.")).toBe(true);
  });

  it("does not flag a full markdown answer", () => {
    expect(isPlanningOnly("## Summary\nRevenue is up 5%.")).toBe(false);
  });

  it("does not flag long text even with a planning prefix", () => {
    const long = "I will " + "x".repeat(250);
    expect(isPlanningOnly(long)).toBe(false);
  });
});
