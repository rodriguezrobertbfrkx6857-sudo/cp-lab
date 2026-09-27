# Algorithm Specification

## V1 algorithms

### Number Theory
1. Euclidean GCD
2. Extended GCD
3. Binary Exponentiation
4. Modular Inverse
5. Prime Factorization
6. Eratosthenes Sieve
7. Euler Linear Sieve
8. Euler Phi
9. Combination C(n,k)
10. Chinese Remainder Theorem

### Graph
11. BFS
12. DFS
13. Dijkstra
14. Topological Sort

### Data Structures
15. Disjoint Set Union
16. Fenwick Tree
17. Segment Tree

### Fundamental
18. Binary Search
19. Merge Sort
20. Quick Sort

## Per-algorithm requirements

Every algorithm must have:

- stable slug
- title
- short description
- category
- difficulty
- time complexity
- space complexity
- C++20 implementation
- Python implementation
- example input
- example output
- edge-case notes
- tests
- related algorithms

If `visualization = true`:
- step generator
- step descriptions
- visualization metadata
- playground preset

If `benchmark = true`:
- benchmark adapter
- supported dataset types
- valid input-size bounds
- operation instrumentation if reasonable

## Quality

No pseudo-code masquerading as production implementation.
No unsafe undefined behavior in C++.
Use deterministic behavior where possible.

## Competitive-programming style

Implementations should be:
- understandable,
- correct,
- idiomatic,
- close enough to practical contest use,
- not overengineered.

## Mathematical explanations

Number-theory pages should explain why the algorithm works, not merely state the formula.
