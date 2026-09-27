import { chromium } from "playwright";
import { mkdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "screenshots");
const assets = path.join(root, "assets");
const frames = path.join(root, "build", "capture-frames");
await mkdir(output, { recursive: true });
await mkdir(assets, { recursive: true });
for (const name of ["dashboard", "dijkstra", "benchmark"]) await mkdir(path.join(frames, name), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 1 });

async function shot(route, name) {
  await page.goto(`http://127.0.0.1:3000${route}`, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(output, name), fullPage: false });
}

await shot("/", "dashboard-16x9.png");
await shot("/algorithms", "explorer-16x9.png");
await shot("/algorithms/dijkstra", "detail-16x9.png");
await shot("/playground/dijkstra", "playground-16x9.png");
await shot("/playground/eratosthenes-sieve", "sieve-16x9.png");

await page.goto("http://127.0.0.1:3000/benchmark", { waitUntil: "networkidle" });
await page.getByLabel("Input size").fill("40");
await page.getByLabel("Warmups").fill("1");
await page.getByLabel("Measured runs").fill("3");
await page.getByRole("button", { name: /Run benchmark/ }).click();
await page.getByRole("heading", { name: "Runtime by run" }).waitFor({ timeout: 30_000 });
await page.locator("canvas").first().waitFor({ timeout: 15_000 });
await page.screenshot({ path: path.join(output, "benchmark-16x9.png") });
await page.goto("http://127.0.0.1:3000/compare", { waitUntil: "networkidle" });
await page.getByRole("button", { name: "Measure both" }).click();
await page.getByRole("heading", { name: "Median runtime" }).waitFor({ timeout: 30_000 });
await page.screenshot({ path: path.join(output, "compare-16x9.png") });

await page.setViewportSize({ width: 390, height: 844 });
await shot("/playground/dijkstra", "mobile-9x16.png");

await page.setViewportSize({ width: 1440, height: 810 });
await page.goto("http://127.0.0.1:3000/", { waitUntil: "networkidle" });
for (let index = 0; index < 12; index++) {
  await page.evaluate((y) => window.scrollTo({ top: y, behavior: "instant" }), index * 38);
  await page.screenshot({ path: path.join(frames, "dashboard", `${String(index).padStart(3,"0")}.png`) });
}

await page.goto("http://127.0.0.1:3000/playground/dijkstra", { waitUntil: "networkidle" });
await page.getByText(/Visit node/).first().waitFor();
for (let index = 0; index < 12; index++) {
  await page.screenshot({ path: path.join(frames, "dijkstra", `${String(index).padStart(3,"0")}.png`) });
  await page.getByRole("button", { name: "Next step" }).click();
}

await page.goto("http://127.0.0.1:3000/benchmark", { waitUntil: "networkidle" });
for (let index = 0; index < 5; index++) await page.screenshot({ path: path.join(frames, "benchmark", `${String(index).padStart(3,"0")}.png`) });
await page.getByLabel("Input size").fill("40"); await page.getByLabel("Warmups").fill("1"); await page.getByLabel("Measured runs").fill("3");
await page.getByRole("button", { name: /Run benchmark/ }).click();
await page.getByRole("heading", { name: "Runtime by run" }).waitFor({ timeout: 30_000 });
await page.locator("canvas").first().waitFor({ timeout: 15_000 });
for (let index = 5; index < 12; index++) { await page.evaluate((y) => window.scrollTo({ top: y, behavior: "instant" }), (index-5)*24); await page.screenshot({ path: path.join(frames, "benchmark", `${String(index).padStart(3,"0")}.png`) }); }

const dashboard = await readFile(path.join(output, "dashboard-16x9.png"));
await page.setViewportSize({ width: 1280, height: 640 });
await page.setContent(`<!doctype html><html><style>
  *{box-sizing:border-box}body{margin:0;width:1280px;height:640px;overflow:hidden;background:#edf0f5;font-family:Inter,Arial,sans-serif;color:#111318}
  main{position:relative;width:100%;height:100%;padding:58px 64px;background:radial-gradient(circle at 88% 10%,#e3dfff 0,transparent 34%),#edf0f5}
  .copy{position:relative;z-index:2;width:480px}.mark{display:inline-grid;place-items:center;width:52px;height:52px;border-radius:16px;background:#111318;color:white;font:700 17px monospace}
  h1{margin:26px 0 8px;font-size:68px;letter-spacing:-.065em;line-height:.95}.tag{font-size:18px;color:#6558d9;font-weight:700;white-space:nowrap}.description{font-size:18px;line-height:1.5;color:#69717d;max-width:450px}
  .product{position:absolute;left:540px;top:82px;width:820px;height:478px;object-fit:cover;object-position:left top;border:1px solid rgba(17,24,39,.12);border-radius:24px;box-shadow:0 34px 80px rgba(32,39,55,.19);transform:rotate(-1.2deg)}
</style><main><div class="copy"><div class="mark">&lt;/&gt;</div><h1>CP-Lab</h1><p class="tag">Visualize · Experiment · Benchmark · Compare</p><p class="description">A production-style competitive-programming algorithm laboratory with trusted C++20 and Python execution.</p></div><img class="product" alt="CP-Lab dashboard" src="data:image/png;base64,${dashboard.toString("base64")}"></main></html>`);
await page.screenshot({ path: path.join(assets, "github-social-preview.png") });

await browser.close();
console.log(`Captured product assets in ${output}`);
