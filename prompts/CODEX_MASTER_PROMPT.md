# Codex Master Prompt — CP-Lab V1

You are implementing CP-Lab V1 from the specification package in this repository.

## Priority order

1. Correctness
2. Real functionality
3. Testability
4. Cohesive UX
5. Performance
6. Documentation polish

## Mandatory behavior

Before coding:
1. Read every numbered specification file.
2. Read `visual_reference/VISUAL_REFERENCE_GUIDE.md`.
3. Inspect all JSON schemas and mock data.
4. Create an implementation plan mapped to the acceptance criteria.

Then execute in phases.

### Phase 0 — Inspect
- summarize architecture
- identify risks
- identify required dependencies
- do not code before understanding the specs

### Phase 1 — Scaffold
- monorepo
- Next.js web app
- FastAPI API
- packages/directories
- lint/test/build baseline
- Docker/dev setup

### Phase 2 — Design system
- tokens
- layout primitives
- cards
- buttons
- inputs
- shell
- responsive foundations

### Phase 3 — Frontend core
- Dashboard
- Explorer
- Detail page
- docs/about shells
- command palette

### Phase 4 — Backend core
- algorithm metadata
- API schemas
- validation
- health
- benchmark models

### Phase 5 — Algorithms
- all 20 C++ implementations
- all 20 Python implementations
- metadata
- examples
- tests

### Phase 6 — Visualization
- normalized step schema
- playback engine
- number theory views
- graph views
- data structure views
- code-line highlighting

### Phase 7 — Benchmark
- deterministic generators
- warmup/measured runs
- result aggregation
- environment metadata
- benchmark UI
- compare integration

### Phase 8 — Testing
- unit
- property/randomized where useful
- backend API
- frontend
- E2E

### Phase 9 — Final polish
- responsive review
- accessibility
- loading/empty/error states
- screenshots
- README
- documentation
- CI

### Phase 10 — Final QA
Run:
- lint
- type check
- all unit tests
- backend tests
- algorithm tests
- production build
- E2E smoke tests

Fix failures before declaring completion.

## Never do these

- Do not silently reduce scope.
- Do not replace real functionality with static mock UI.
- Do not fabricate benchmark results.
- Do not write "tests passed" without running tests.
- Do not delete existing work just to simplify a failing implementation.
- Do not replace required C++ implementations with TypeScript-only demos.
- Do not copy the visual references.
- Do not reuse their branding, people, names, logos, text or watermarks.
- Do not leave unfinished TODO placeholders in production user flows.
- Do not add authentication, AI, cloud sync or arbitrary code execution in V1.
- Do not introduce unnecessary infrastructure.

## Visual target

Use the references for general visual language only:
- soft white/gray surfaces
- restrained accents
- rounded large cards
- subtle shadows
- strong hierarchy
- premium dashboard feel
- center-canvas workbench layout

Avoid:
- neon
- cyberpunk
- giant gradients
- excessive glass
- generic Bootstrap look
- giant marketing hero typography

## Deliverables

At the end create:
- `FINAL_BUILD_REPORT.md`
- `QA_REPORT.md`

The final report must state real commands executed and real outcomes.

A feature is not complete merely because the UI exists.
