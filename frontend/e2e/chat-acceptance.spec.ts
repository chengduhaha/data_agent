import { test, expect, type Page } from "@playwright/test";
import {
  acceptanceChatStream,
  encodeSse,
  streamingScrollStream,
} from "./helpers/sse";

async function waitForChatReady(page: Page) {
  const textarea = page.locator("textarea.chat-textarea");
  try {
    await textarea.waitFor({ state: "visible", timeout: 15_000 });
  } catch {
    // Dev server may still be compiling after a prod build; one reload usually fixes it.
    await page.reload();
    await textarea.waitFor({ state: "visible", timeout: 60_000 });
  }
}

async function stubChatApis(page: Page, streamBody: string) {
  const authConfig = {
    enabled: false,
    button_label: "Log in with Microsoft Entra",
    idle_timeout_seconds: 86400,
  };

  await page.route("**/api/auth/config", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(authConfig),
    });
  });
  await page.route("**/api/auth/bootstrap", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ config: authConfig, user: null }),
    });
  });
  await page.route("**/api/auth/me", async (route) => {
    await route.fulfill({ status: 401, body: "unauthorized" });
  });
  await page.route("**/api/skills", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ skills: [] }),
    });
  });
  await page.route("**/api/chat/threads", async (route) => {
    if (route.request().method() === "GET") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ threads: [] }),
      });
      return;
    }
    await route.continue();
  });
  await page.route("**/api/chat/stream", async (route) => {
    await route.fulfill({
      status: 200,
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
      },
      body: streamBody,
    });
  });
  await page.route("**/api/providers", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ providers: [] }),
    });
  });
  await page.route("**/api/model-catalog", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        provider_id: "test",
        provider_name: "Test",
        description: "",
        default_model: "",
        defaults: { temperature: 0, max_tokens: 4096 },
        models: [],
      }),
    });
  });
  await page.route("**/api/config", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        model: {
          provider: "test",
          model: "",
          api_key: "",
          base_url: "",
          temperature: 0,
          api_key_set: false,
        },
        system_prompt: "test",
        approve_writes: false,
        approve_execute: false,
        enabled_tools: {},
        permissions: [],
      }),
    });
  });
}

test.describe("Chat acceptance F1–F3", () => {
  test("F1: narrative is separate from SQL appendix (not in narrative code block)", async ({
    page,
  }) => {
    await stubChatApis(page, encodeSse(acceptanceChatStream()));
    await page.goto("/");
    await waitForChatReady(page);
    await page.locator("textarea.chat-textarea").fill("Revenue trend");
    await page.getByRole("button", { name: "Send" }).click();

    const agentBubble = page.getByText("Revenue is up 5% QoQ.").locator("xpath=ancestor::div[contains(@class,'rounded-2xl')][1]");
    await expect(page.getByText("Revenue is up 5% QoQ.")).toBeVisible();

    const narrativePre = agentBubble.locator(":scope > div.text-sm pre");
    await expect(narrativePre).toHaveCount(0);

    const appendix = page.getByTestId("query-appendix");
    await expect(appendix).toBeVisible();
    await expect(appendix.getByText(/Query validation \(1 query\)/)).toBeVisible();
    await expect(appendix.locator("pre")).toHaveCount(0);

    await appendix.getByRole("button").click();
    await expect(appendix.getByText("SELECT revenue FROM fact_sales LIMIT 1")).toBeVisible();
  });

  test("F2: scroll position stays put while user reads scrollback during streaming", async ({
    page,
  }) => {
    await stubChatApis(page, encodeSse(streamingScrollStream()));
    await page.goto("/");
    await waitForChatReady(page);
    await page.locator("textarea.chat-textarea").fill("Long stream");
    await page.getByRole("button", { name: "Send" }).click();

    const scroll = page.getByTestId("chat-scroll");
    await expect(scroll).toBeVisible();
    await expect(page.getByText("Line 10:")).toBeVisible();
    await scroll.evaluate((el) => {
      el.scrollTop = 0;
    });

    await page.waitForTimeout(600);
    const scrollTop = await scroll.evaluate((el) => el.scrollTop);
    expect(scrollTop).toBeLessThan(40);
  });

  test("scroll UX: input stays visible and message pane follows stream at bottom", async ({
    page,
  }) => {
    await stubChatApis(page, encodeSse(streamingScrollStream()));
    await page.goto("/");
    await waitForChatReady(page);

    const textarea = page.locator("textarea.chat-textarea");
    await textarea.fill("Long stream");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(textarea).toBeInViewport();

    const scroll = page.getByTestId("chat-scroll");
    await expect(scroll).toBeVisible();
    await expect(page.getByText("Line 40:")).toBeVisible();

    await expect
      .poll(async () =>
        scroll.evaluate((el) => {
          const distance = el.scrollHeight - el.scrollTop - el.clientHeight;
          return distance < 48;
        })
      )
      .toBe(true);

    const bodyScrollTop = await page.evaluate(() => document.documentElement.scrollTop);
    expect(bodyScrollTop).toBe(0);
  });

  test("F3: new chat clears step/budget bar", async ({ page }) => {
    await stubChatApis(page, encodeSse(acceptanceChatStream()));
    await page.goto("/");
    await waitForChatReady(page);
    await page.locator("textarea.chat-textarea").fill("Budget bar test");
    await page.getByRole("button", { name: "Send" }).click();

    const budgetBar = page.getByTestId("context-budget-bar");
    await expect(budgetBar).toBeVisible();
    await expect(budgetBar.getByText("Agent steps")).toBeVisible();

    await page.getByRole("button", { name: "New" }).click();
    await expect(budgetBar).toHaveCount(0);
  });

  test("UX: RunPhaseBar, budget during run, collapsible SQL appendix", async ({ page }) => {
    await stubChatApis(page, encodeSse(acceptanceChatStream()));
    await page.goto("/");
    await waitForChatReady(page);
    await page.locator("textarea.chat-textarea").fill("UX checks");
    await page.getByRole("button", { name: "Send" }).click();

    const budgetBar = page.getByTestId("context-budget-bar");
    await expect(budgetBar.getByText("Research")).toBeVisible();
    await expect(budgetBar.getByText("Execute")).toBeVisible();
    await expect(budgetBar.getByText("Synthesize")).toBeVisible();
    await expect(budgetBar.getByText(/8\s*\/\s*150/)).toBeVisible();

    const appendix = page.getByTestId("query-appendix");
    await expect(appendix.getByText("▸")).toBeVisible();
    await appendix.getByRole("button").click();
    await expect(appendix.getByText("▾")).toBeVisible();
  });
});
