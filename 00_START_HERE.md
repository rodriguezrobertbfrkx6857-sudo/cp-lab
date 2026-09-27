# CP-Lab V1 — Start Here

This package is the authoritative implementation handoff for Codex.

## Mission

Build a polished, production-style V1 of an interactive competitive-programming algorithm laboratory. The product must combine:

- algorithm explanations,
- step-by-step visualization,
- interactive experimentation,
- reproducible benchmarking,
- side-by-side comparison,
- clean software engineering,
- strong GitHub presentation quality.

The intended result is not a toy demo, not a generic "algorithm visualizer", and not a mock dashboard. It should feel like a credible developer tool / educational laboratory.

## Working product name

Internal codename: `CP-Lab`.

The public product name is intentionally not frozen. Keep naming centralized so it can be changed later without invasive refactors.

Recommended config entry:

```ts
export const PRODUCT_NAME = "CP-Lab";
```

Do not scatter the string across the codebase.

## Read order

1. `01_PRODUCT_VISION.md`
2. `02_V1_SCOPE.md`
3. `03_INFORMATION_ARCHITECTURE.md`
4. `04_PAGE_SPECIFICATIONS.md`
5. `05_UI_UX_SPEC.md`
6. `06_DESIGN_SYSTEM.md`
7. `07_COMPONENT_SPEC.md`
8. `08_VISUALIZATION_ENGINE.md`
9. `09_ALGORITHM_SPEC.md`
10. `10_BENCHMARK_SPEC.md`
11. `11_BACKEND_SPEC.md`
12. `12_FRONTEND_SPEC.md`
13. `13_API_SPEC.md`
14. `14_TESTING_SPEC.md`
15. `15_SECURITY_SPEC.md`
16. `16_GITHUB_SPEC.md`
17. `17_DOCUMENTATION_SPEC.md`
18. `18_PROMOTION_SPEC.md`
19. `19_ROADMAP.md`
20. `20_ACCEPTANCE_CRITERIA.md`
21. `prompts/CODEX_MASTER_PROMPT.md`

## Non-negotiable rules

- Do not silently reduce scope.
- Do not replace real functionality with static mock UI.
- Do not fabricate benchmark results.
- Do not claim tests passed without running them.
- Do not delete existing work merely to simplify implementation.
- Do not replace C++ algorithm implementations with TypeScript-only demonstrations.
- Do not copy branding, logos, people, text, watermarks or exact layouts from visual references.
- Do not leave unfinished TODO placeholders in production paths.
- Build, test, fix, and verify each phase before proceeding.
