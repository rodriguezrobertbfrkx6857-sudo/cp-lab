import { defineConfig, devices } from "@playwright/test";

const python = process.platform === "win32" ? "py -3.13" : "python";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: { baseURL: "http://127.0.0.1:3000", trace: "retain-on-failure", screenshot: "only-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    { command: `${python} -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000`, cwd: "../..", url: "http://127.0.0.1:8000/health", reuseExistingServer: !process.env.CI, timeout: 120_000 },
    { command: "npm run dev", url: "http://127.0.0.1:3000", reuseExistingServer: !process.env.CI, timeout: 120_000 },
  ],
});
