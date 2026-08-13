import { test, expect, type Page } from "@playwright/test";

const QUESTION = `我用vertica mcp执行这个sql
SELECT order_no, SUM(IFNULL(ngm_amt, 0)) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag = DATE '2026-04-30'
  AND segment_exclude = 'N'
GROUP BY order_no
HAVING SUM(IFNULL(ngm_amt, 0)) < 0
ORDER BY ngm_amt ASC
LIMIT 10`;

const ORDER_IDS = [
  "-77294", "621286", "657888", "141692", "413709",
  "173937798", "124858", "529859", "303148", "695266",
];

async function waitForChatReady(page: Page) {
  await page.locator("textarea.chat-textarea").waitFor({ state: "visible", timeout: 180_000 });
}

/** Wait until streaming settles: Send button becomes enabled again (done event). */
async function waitForStreamEnd(page: Page, timeout: number) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const enabled = await page
      .getByRole("button", { name: "Send" })
      .isEnabled()
      .catch(() => false);
    const paused = await page
      .getByText(/Run paused|tool-step limit/i)
      .first()
      .isVisible()
      .catch(() => false);
    if (enabled || paused) return { sendEnabled: enabled, paused };
    await page.waitForTimeout(2000);
  }
  return { sendEnabled: false, paused: false };
}

test("real E2E: ask same question, capture assistant output", async ({ page }) => {
  test.setTimeout(360_000);

  await page.goto("/");
  await waitForChatReady(page);

  await page.locator("textarea.chat-textarea").fill(QUESTION);
  await page.getByRole("button", { name: "Send" }).click();

  const end = await waitForStreamEnd(page, 300_000);
  console.log(`\nSTREAM END: sendEnabled=${end.sendEnabled} paused=${end.paused}`);

  // Capture full markdown + all table cell text AFTER streaming finished.
  const fullText = await page.locator(".markdown-body").innerText().catch(() => "");
  const tableCells: string[] = [];
  const cells = page.locator(".markdown-body td");
  const nCells = await cells.count();
  for (let i = 0; i < nCells; i++) tableCells.push((await cells.nth(i).innerText()).trim());

  const found = ORDER_IDS.filter((id) => fullText.includes(id));
  const missing = ORDER_IDS.filter((id) => !fullText.includes(id));

  console.log("TABLE_CELLS: " + JSON.stringify(tableCells));
  console.log(`\nORDER_MATCHES: ${found.length}/${ORDER_IDS.length}`);
  console.log("MISSING_ORDERS: " + (missing.join(", ") || "(none)"));

  // The decisive diagnostic: report whether all 10 rendered. We do NOT hard-fail
  // when the model picked an ontology-trace route (no data table), but we do fail
  // if a 10-row table was expected yet fewer rows rendered.
  expect(missing, `orders missing after stream end: ${missing.join(", ")}`).toEqual([]);
});