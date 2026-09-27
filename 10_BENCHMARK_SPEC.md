# Benchmark Specification

## Goal

Benchmarking must be reproducible and honest.

## Default methodology

- warmup runs: 3
- measured runs: 10
- deterministic seed: 42 unless overridden
- report median
- report min
- report max
- report P95 when sample size supports it

## Environment metadata

Record where feasible:
- language
- compiler/interpreter
- runtime version
- OS
- CPU model if exposed by backend
- build mode / optimization flags
- timestamp
- seed
- warmup count
- measured run count

## C++ benchmark

Recommended:
- C++20
- optimized release build
- explicit compiler flags
- never compare debug C++ against optimized Python or vice versa without labeling

## Python benchmark

Use a consistent interpreter and environment.
Avoid import/setup time inside the measured region unless that is intentionally measured.

## Browser vs backend

Never present browser JavaScript timing as C++ timing.

UI labels must distinguish:
- browser-local benchmark
- backend benchmark

## Dataset generators

V1:
- Random
- Sorted
- Reverse Sorted
- Nearly Sorted
- Duplicate Heavy
- Sparse Graph
- Dense Graph
- Chain Graph
- Random Tree

Parameters:
- size
- seed
- min value
- max value
- graph density where applicable

## Built-in comparison suites

1. naive repeated-subtraction GCD vs Euclidean GCD
2. naive exponentiation vs binary exponentiation
3. trial prime detection vs sieve
4. Eratosthenes vs Euler linear sieve
5. BFS vs DFS on traversal scenarios
6. DSU with vs without path compression
7. Fenwick tree vs repeated prefix recomputation
8. Merge Sort vs Quick Sort

## Safety

Do not accept arbitrary user-uploaded C++ or Python for execution in V1.
Benchmark only trusted repository algorithms.
