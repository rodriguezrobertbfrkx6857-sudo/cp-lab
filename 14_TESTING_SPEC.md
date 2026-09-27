# Testing Specification

## Algorithm tests

Each algorithm should include at least:

- normal case
- edge case
- minimum case
- large case
- randomized case where appropriate

## Property tests

Examples:

GCD:
- result divides a
- result divides b
- gcd(a,b) == gcd(b,a)

Sorting:
- output equals canonical sorted copy
- multiset preserved

DSU:
- connectivity relation remains consistent with reference model

Fenwick/Segment Tree:
- compare random queries/updates against naive array implementation

Dijkstra:
- compare small random non-negative graphs against a trusted reference implementation

## Backend tests

- endpoint happy paths
- validation failures
- unknown slugs
- benchmark config validation
- deterministic seed behavior
- health endpoint

## Frontend unit tests

Use:
- Vitest
- React Testing Library

Cover:
- search/filter
- playback controls
- code tab switching
- benchmark form validation
- compare selection
- empty/error states

## E2E

Use Playwright.

At minimum:
1. Dashboard loads.
2. Algorithm opens.
3. Visualization can step/play.
4. Benchmark can run.
5. Compare can load two algorithms.
6. Mobile smoke viewport does not break core navigation.

## CI expectation

Tests are real commands, not documentation claims.
