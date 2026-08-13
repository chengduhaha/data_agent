import { defineConfig } from "@playwright/test";

/**
 * Live end-to-end config — requires a running data_agent (backend :8000 +
 * frontend :6641), anonymous/local auth, and real LLM + Vertica MCP access.
 * Run manually; do NOT include in CI. Example:
 *
 *   PLAYWRIGHT_SKIP_WEBSERVER=1 npx playwright test --config=playwright.live.config.ts
 */
export default defineConfig({
  testDir: "./e2e-live",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: "line",
  timeout: 360_000,
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://127.0.0.1:6641",
    trace: "retain-on-failure",
  },
  webServer: undefined,
});