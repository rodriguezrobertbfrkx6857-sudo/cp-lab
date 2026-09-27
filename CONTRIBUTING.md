# Contributing

## Add or change an algorithm

1. Add complete metadata and explanation fields in
   `packages/catalog/algorithms.json` with a stable lowercase slug.
2. Add the contest-oriented C++20 implementation to
   `algorithms/cpp/include/cp_algorithms.hpp`.
3. Add the equivalent Python implementation to
   `algorithms/python/cp_algorithms.py`.
4. Add normal, minimum, edge, large, and randomized/reference-model tests.
5. Add a deterministic adapter in `apps/api/core/visualization.py`.
6. If benchmarking is meaningful, add bounded trusted adapters for both runtimes
   in `apps/api/core/benchmark.py` and `algorithms/cpp/benchmark_runner.cpp`.
7. Provide example input/output, edge cases, and related slugs in the catalog.
8. Check the detail, playground, benchmark, compare, and mobile views.
9. Run every command in the README testing section.

Do not add arbitrary code execution, fabricated results, or a visualization that
is disconnected from algorithm state. Keep changes accessible and deterministic.

## Pull requests

Explain the correctness oracle, include new tests, note complexity or benchmark
methodology changes, and keep unrelated refactors separate. All CI jobs must pass.
