# CP-Lab V1 QA Report

Date: 2026-09-20

## Acceptance Checklist

### Product

- [x] Exactly 20 canonical algorithms and unique slugs, each with C++20, Python, detail, and Playground coverage.
- [x] Deterministic normalized visualization steps with full playback, seeking, speeds, inspector, renderers, and line mapping.
- [x] Trusted Python/C++ benchmarks with raw samples, eight suites, SQLite history, and supported same-workload Compare.
- [x] Explorer search/filter/sort/empty state and responsive desktop/mobile workflows.

### Quality

- [x] Python algorithms: 20 passed.
- [x] C++20: all 20 passed edge/randomized/reference checks.
- [x] Backend/API/benchmark: 16 passed.
- [x] Frontend unit/interaction: 6 passed across 5 files.
- [x] Next.js 16.3.5 production build: 49 routes/pages.
- [x] Playwright Chromium: 8/8 passed in 6.7s.
- [x] No unexpected browser `console.error` or uncaught `pageerror`.
- [x] Designed 404, no production TODO/FIXME markers, no premature benchmark success state.
- [x] Production npm dependency audit: 0 vulnerabilities.

### Engineering and Handoff

- [x] Docker Compose parses; both Dockerfiles and a dedicated Linux CI build job exist.
- [ ] Local Docker image build completed. The local Linux engine was unresponsive, so this is not reported as a pass.
- [x] CI covers lint, typecheck, frontend/API/algorithm tests, production build, E2E, Compose validation, and Docker build.
- [x] Environment, architecture, contribution, security, and release documents exist; `.env.example` contains no secrets.
- [x] Seven 1440×810 desktop captures, one 390×844 mobile capture, three six-second GIFs, and one 1280×640 social preview.

## Strengthened Verification

Python checks modular identities, factor reconstruction, brute-force sieve/phi references, `math.comb`, CRT substitution, traversal/topological invariants, and search/sort properties. C++ mirrors this confidence level with randomized and reference-driven checks.

Benchmark tests directly verify summaries, nearest-rank P95, invalid/empty samples, seeded reproducibility, generated shapes, and excluded warmups. Endpoint tests verify history persistence, oversized/invalid visualization input, Dijkstra distances, and final path edges.

## End-to-End Scenarios

1. Dashboard → Explorer → algorithm detail.
2. Playground first/previous/play/pause/next/last/timeline/restart/speed.
3. Real backend benchmark, result analysis, and history.
4. Two-algorithm measured comparison.
5. Mobile navigation.
6. Docs, About, and designed 404.
7. Explorer empty state and command palette.
8. Mobile Playground stacking with no horizontal overflow.

## Fixes Verified

Earlier work corrected test aliasing, C++ assertion parsing, compiler behavior on a non-ASCII path, generated-directory linting, DOM cleanup, type-generation ordering, API CORS, mobile selectors, vulnerable dependencies, Next tracing, and development-origin configuration. Release hardening additionally corrected binary-search benchmark input, graph dataset semantics, stale benchmark UI state, benchmark history presentation, visualization resource bounds, Dijkstra final-state data, and weak randomized/reference coverage.

## Command Evidence

| Command | Result |
| --- | --- |
| `npm run check` | PASS |
| `npm run test:web` | 6/6 PASS |
| `npm run test:api` | 16/16 PASS |
| `npm run test:algorithms` | Python 20 PASS; C++20 all 20 PASS |
| `npm run build` | PASS; 49 routes/pages |
| `npm run test:e2e` | 8/8 PASS in 6.7s |
| `npm audit --omit=dev --audit-level=high --registry=https://registry.npmjs.org` | 0 vulnerabilities |
| `docker compose config --quiet` | PASS |
| `docker compose build` | Not completed: local engine unresponsive |

## Remaining External Verification

- Observe Docker image construction on a responsive Linux engine or hosted GitHub Actions.
- Push to a Git remote for hosted CI, tag, and release evidence.
- Supply hosting credentials and a domain/public URL for live deployment.

No remaining item is replaced by a fake or bypass inside the application.
