import { spawnSync } from "node:child_process";

const candidates = process.platform === "win32"
  ? [["py", ["-3.13"]], ["py", ["-3.12"]], ["python", []]]
  : [["python3", []], ["python", []]];

let selected;
for (const [command, prefix] of candidates) {
  const probe = spawnSync(command, [...prefix, "-c", "import sys; print(sys.version_info[:2])"], { stdio: "ignore" });
  if (probe.status === 0) { selected = [command, prefix]; break; }
}
if (!selected) {
  console.error("No usable Python 3 interpreter was found.");
  process.exit(1);
}
const [command, prefix] = selected;
const completed = spawnSync(command, [...prefix, ...process.argv.slice(2)], { stdio: "inherit" });
process.exit(completed.status ?? 1);
