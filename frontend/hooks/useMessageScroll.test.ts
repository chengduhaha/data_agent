import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

describe("useMessageScroll (F2)", () => {
  it("uses container scrollTo auto-follow, not global smooth scrollIntoView", () => {
    const hook = readFileSync(path.join(__dirname, "useMessageScroll.ts"), "utf8");
    expect(hook).toContain("root.scrollTo({ top: root.scrollHeight, behavior");
    expect(hook).toContain('if (shouldAutoFollow()) scrollToBottom("auto")');
    expect(hook).toContain("ResizeObserver");
    expect(hook).toContain("streaming");
    expect(hook).toContain("resetFollow");

    const chat = readFileSync(
      path.join(__dirname, "..", "components", "ChatWindow.tsx"),
      "utf8"
    );
    expect(chat).not.toMatch(/scrollIntoView\s*\(/);
    expect(chat).toContain("useMessageScroll");
    expect(chat).toContain("{ streaming }");
  });
});
