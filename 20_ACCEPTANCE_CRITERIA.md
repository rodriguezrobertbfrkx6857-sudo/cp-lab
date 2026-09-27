# Acceptance Criteria

V1 is not complete until the following are verified.

## Product

- [ ] 20 algorithms are present.
- [ ] C++ implementation exists for all 20.
- [ ] Python implementation exists for all 20.
- [ ] Algorithm detail pages render correctly.
- [ ] Required visualization-supported algorithms work.
- [ ] Playground playback works.
- [ ] Benchmark runs real code and does not fabricate data.
- [ ] Compare view works.
- [ ] Search/filter works.
- [ ] Responsive layouts have no major breakage.

## Quality

- [ ] Algorithm tests pass.
- [ ] Backend tests pass.
- [ ] Frontend tests pass.
- [ ] Production frontend build passes.
- [ ] Playwright smoke tests pass.
- [ ] No obvious console errors.
- [ ] No broken internal links.
- [ ] No TODO placeholders in user-facing production paths.
- [ ] No fake success states.

## Engineering

- [ ] Docker development path works.
- [ ] GitHub Actions workflow exists and is valid.
- [ ] Environment variables are documented.
- [ ] `.env.example` contains no real secrets.
- [ ] architecture documentation exists.

## Visual

- [ ] design system is consistent.
- [ ] card radii are consistent.
- [ ] typography hierarchy is consistent.
- [ ] no copied branding from reference images.
- [ ] charts match product styling.
- [ ] loading/error/empty states are designed.

## Handoff

Final implementation must include:
- `FINAL_BUILD_REPORT.md`
- `QA_REPORT.md`

`FINAL_BUILD_REPORT.md`:
- implemented features
- architecture
- algorithms
- test commands/results
- build results
- known limitations
- run instructions
- deployment instructions

`QA_REPORT.md`:
- acceptance checklist
- failures found
- fixes performed
- remaining issues, if any
