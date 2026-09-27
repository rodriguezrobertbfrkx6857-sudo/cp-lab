import { expect, test, type Page } from "@playwright/test";

const browserErrors = new WeakMap<Page, string[]>();
test.beforeEach(async ({ page }) => {
  const errors: string[] = [];
  browserErrors.set(page, errors);
  page.on("pageerror", (error) => errors.push(`pageerror: ${error.message}`));
  page.on("console", (message) => { if (message.type() === "error") errors.push(`console: ${message.text()}`); });
});
test.afterEach(async ({ page }) => {
  expect(browserErrors.get(page) ?? []).toEqual([]);
});

test("dashboard and explorer navigation", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Explore algorithms/ })).toBeVisible();
  await expect(page.getByText("20", { exact: true }).first()).toBeVisible();
  await page.getByRole("link", { name: "Algorithms", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Algorithm Explorer" })).toBeVisible();
  await page.getByLabel("Search algorithms").fill("Dijkstra");
  await page.getByRole("heading", { name: "Dijkstra", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Dijkstra", exact: true })).toBeVisible();
});

test("visualization can step and play", async ({ page }) => {
  await page.goto("/playground/euclidean-gcd");
  await expect(page.getByText(/Start with the two integers/)).toBeVisible();
  await page.getByRole("button", { name: "Next step" }).click();
  await expect(page.getByText(/mod/)).toBeVisible();
  await page.getByRole("button", { name: "Play" }).click();
  await expect(page.getByText("Playing")).toBeVisible();
  await page.getByRole("button", { name: "Pause" }).click();
  await page.getByRole("button", { name: "Last step" }).click();
  await expect(page.getByText(/Algorithm complete/)).toBeVisible();
  await page.getByRole("button", { name: "Restart" }).click();
  await expect(page.getByText(/Start with the two integers/)).toBeVisible();
  await page.getByRole("button", { name: "2×" }).click();
  await expect(page.getByRole("button", { name: "2×" })).toHaveClass(/active/);
});

test("benchmark runs trusted backend code", async ({ page }) => {
  await page.goto("/benchmark");
  await page.getByLabel("Input size").fill("30");
  await page.getByLabel("Warmups").fill("1");
  await page.getByLabel("Measured runs").fill("3");
  await page.getByRole("button", { name: /Run benchmark/ }).click();
  await expect(page.getByRole("heading", { name: "Runtime by run" })).toBeVisible({ timeout: 30_000 });
  await expect(page.getByText("backend timing")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Measurement status" })).toBeVisible();
  await expect(page.getByText("No value is estimated or fabricated.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Recent measured runs" })).toBeVisible();
});

test("compare loads two algorithms", async ({ page }) => {
  await page.goto("/compare");
  await page.getByRole("button", { name: "Compare concepts" }).click();
  await expect(page.getByText(/Choose based on input constraints/)).toBeVisible();
  await expect(page.getByRole("heading", { name: "Merge Sort" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Quick Sort" })).toBeVisible();
  await page.getByRole("button", { name: "Measure both" }).click();
  await expect(page.getByRole("heading", { name: "Median runtime" })).toBeVisible({ timeout: 30_000 });
  await expect(page.getByText("python backend")).toBeVisible();
});

test("mobile navigation remains usable", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await page.getByRole("button", { name: "Open navigation" }).click();
  await expect(page.getByRole("link", { name: "Benchmark", exact: true })).toBeVisible();
  await page.getByRole("link", { name: "Benchmark", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Benchmark trusted implementations" })).toBeVisible();
});

test("docs, about, and designed 404 render", async ({ page }) => {
  await page.goto("/docs");
  await expect(page.getByRole("heading", { name: "How CP-Lab works" })).toBeVisible();
  await page.goto("/about");
  await expect(page.getByRole("heading", { name: /Built to make algorithm behavior inspectable/ })).toBeVisible();
  await page.goto("/not-a-real-route");
  await expect(page.getByRole("heading", { name: /This path has no algorithm/ })).toBeVisible();
  expect(browserErrors.get(page)).toEqual(["console: Failed to load resource: the server responded with a status of 404 (Not Found)"]);
  browserErrors.set(page, []);
});

test("explorer empty state and command palette are interactive", async ({ page }) => {
  await page.goto("/algorithms");
  await page.getByLabel("Search algorithms").fill("no-such-algorithm");
  await expect(page.getByRole("heading", { name: "No algorithms match" })).toBeVisible();
  await page.keyboard.press("Control+k");
  await expect(page.getByLabel("Search commands")).toBeVisible();
  await page.getByLabel("Search commands").fill("Benchmark");
  await expect(page.getByRole("button", { name: /Benchmark/ }).first()).toBeVisible();
});

test("mobile playground stacks without horizontal overflow", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/playground/dijkstra");
  await expect(page.getByText("Visualization canvas")).toBeVisible();
  await expect(page.getByText("Input controls")).toBeVisible();
  await expect(page.getByText("State inspector")).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBe(false);
  const canvasTop = await page.getByText("Visualization canvas").boundingBox();
  const controlsTop = await page.getByText("Input controls").boundingBox();
  expect(canvasTop?.y ?? 0).toBeLessThan(controlsTop?.y ?? 0);
});
