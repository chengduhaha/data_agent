import { describe, expect, it } from "vitest";
import {
  extractClarificationFromInterrupt,
  formatClarificationAnswer,
  isClarificationInterrupt,
} from "./clarification";

describe("clarification helpers", () => {
  it("extracts nested clarification payloads", () => {
    const payload = {
      interrupts: [
        {
          value: {
            type: "clarification",
            reason: "Need a period",
            questions: [
              {
                question: "Which period?",
                options: [{ label: "FY26 Q1" }, { label: "Last month" }],
              },
            ],
          },
        },
      ],
    };
    const found = extractClarificationFromInterrupt(payload);
    expect(found?.questions[0]?.question).toBe("Which period?");
    expect(isClarificationInterrupt(payload)).toBe(true);
  });

  it("formats multi-select and free-text answers", () => {
    expect(
      formatClarificationAnswer(
        { question: "Dims?", multi_select: true, options: [{ label: "Cust" }] },
        ["Cust", "Vend"],
        ""
      )
    ).toBe("Cust, Vend");
    expect(
      formatClarificationAnswer(
        { question: "Dims?", options: [{ label: "Cust" }] },
        ["Cust"],
        "Other grain"
      )
    ).toBe("Other grain");
  });
});
