# CP-Lab V1 Implementation Plan

This plan maps the authoritative handoff to the acceptance checklist in
`20_ACCEPTANCE_CRITERIA.md`. Work proceeds only after the preceding phase has a
runnable verification baseline.

## Architecture

- **Monorepo root**: npm workspace, shared catalog, scripts, documentation,
  Docker Compose, and CI.
- **`apps/web`**: Next.js App Router, React, TypeScript, Tailwind CSS, ECharts,
  React Flow, Framer Motion, Vitest/Testing Library, and Playwright.
- **`apps/api`**: FastAPI/Pydantic service with structured errors, SQLite-backed
  benchmark history, deterministic visualization adapters, and trusted-code
  benchmark orchestration.
- **`packages/catalog`**: canonical metadata and explanatory content for all 20
  algorithms.
- **`algorithms/python` / `algorithms/cpp`**: practical Python and C++20
  implementations plus language-specific correctness tests.

## Phase gates and acceptance mapping

| Phase | Deliverable and verification | Acceptance criteria covered |
| --- | --- | --- |
| 1. Scaffold | Workspace, app/API start, `/health`, lint/build baseline, Docker files | Docker path, CI skeleton, env docs |
| 2. Design | Tokens, shell, controls, feedback states, responsive navigation | visual consistency, accessibility, loading/error/empty states |
| 3. Frontend | Dashboard, explorer, details, playground, benchmark, compare, docs/about, command palette | all required routes, search/filter, internal navigation |
| 4. Backend | Typed endpoints, validation, errors, metadata and persistence | API happy/error paths, no arbitrary execution |
| 5. Algorithms | 20 Python + 20 C++20 implementations, examples and tests | complete algorithm and language matrix |
| 6. Visualization | deterministic step generators and reusable playback/rendering | all visualization flags, playback and line highlighting |
| 7. Benchmark | seeded generators, warmups/runs, real timing, aggregation/environment, UI charts | truthful benchmarks and compare integration |
| 8. Testing | Python, C++, API, frontend unit, randomized/property, Playwright | all mandated test classes |
| 9. Polish | responsive/accessibility/error review, docs, screenshots, CI | repository and visual acceptance |
| 10. QA | execute every final command, repair failures, record exact outcomes | final reports and acceptance checklist |

## Risks and controls

- **Cross-language timing**: C++ runs only through a repository-owned compiled
  harness; Python uses repository functions. Results always label runtime and
  environment. No browser result is presented as C++.
- **Resource exhaustion**: Pydantic bounds sizes, iterations, seeds, arrays,
  graphs, and request payloads; expensive work is serialized by a service lock.
- **Metadata drift**: the canonical JSON catalog is validated in Python and
  TypeScript tests, including exact count, stable slugs, code files, examples,
  and related links.
- **Visualization drift**: immutable normalized steps are generated once from
  normalized input and replayed client-side.
- **Platform variance**: local scripts are cross-platform where practical;
  Linux containers and CI are the canonical production build environment.
- **E2E availability**: Playwright browser installation is verified before the
  final run; any environmental failure is recorded rather than reported as a
  product pass.

## Definition of done

Every checkbox in `20_ACCEPTANCE_CRITERIA.md` has concrete evidence in
`QA_REPORT.md`. Any unmet item remains explicitly open; it is never replaced by
a simulated success state.
