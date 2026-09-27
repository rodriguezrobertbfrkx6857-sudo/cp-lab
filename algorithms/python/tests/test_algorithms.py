from __future__ import annotations

import random
from collections import Counter
from math import comb, gcd

import pytest
from hypothesis import given, strategies as st

from algorithms.python.cp_algorithms import (
    DisjointSetUnion, FenwickTree, SegmentTree, bfs, binary_exponentiation,
    binary_search, chinese_remainder, combination, dfs, dijkstra,
    eratosthenes_sieve, euler_linear_sieve, euler_phi, euclidean_gcd,
    extended_gcd, merge_sort, modular_inverse, prime_factorization, quick_sort,
    topological_sort,
)


@given(st.integers(-10**12, 10**12), st.integers(-10**12, 10**12))
def test_gcd_matches_standard_library(a: int, b: int) -> None:
    result = euclidean_gcd(a, b)
    assert result == gcd(a, b)
    if result:
        assert a % result == b % result == 0


@given(st.integers(-10**6, 10**6), st.integers(-10**6, 10**6))
def test_extended_gcd_bezout_identity(a: int, b: int) -> None:
    divisor, x, y = extended_gcd(a, b)
    assert divisor == gcd(a, b)
    assert a * x + b * y == divisor


def test_number_theory_algorithms() -> None:
    assert binary_exponentiation(3, 13, 100) == pow(3, 13, 100)
    assert modular_inverse(3, 11) == 4
    with pytest.raises(ValueError):
        modular_inverse(6, 9)
    assert prime_factorization(360) == [(2, 3), (3, 2), (5, 1)]
    assert eratosthenes_sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert euler_linear_sieve(20)[0] == eratosthenes_sieve(20)
    assert euler_phi(36) == 12
    assert [euler_phi(value) for value in range(1, 6)] == [1, 1, 2, 2, 4]
    assert combination(30, 7) == comb(30, 7)
    assert chinese_remainder([(2, 3), (3, 5)]) == (8, 15)
    assert chinese_remainder([(2, 6), (5, 9)]) == (14, 18)
    with pytest.raises(ValueError):
        chinese_remainder([(0, 2), (1, 2)])


def test_graph_algorithms() -> None:
    graph = [[1, 2], [3], [3], []]
    assert bfs(graph, 0) == ([0, 1, 2, 3], [0, 1, 1, 2])
    assert dfs(graph, 0) == [0, 1, 3, 2]
    assert topological_sort(graph) == [0, 1, 2, 3]
    with pytest.raises(ValueError):
        topological_sort([[1], [0]])
    weighted = [[(1, 4), (2, 1)], [], [(1, 2)]]
    assert dijkstra(weighted, 0) == [0, 3, 1]
    with pytest.raises(ValueError):
        dijkstra([[ (0, -1) ]], 0)


def test_data_structures_against_naive_model() -> None:
    rng = random.Random(42)
    values = [rng.randint(-100, 100) for _ in range(100)]
    fenwick, segment = FenwickTree(values), SegmentTree(values)
    for _ in range(100):
        left, right = sorted(rng.sample(range(len(values) + 1), 2))
        assert fenwick.range_sum(left, right - 1) == sum(values[left:right])
        assert segment.range_sum(left, right) == sum(values[left:right])
    for _ in range(50):
        index, value = rng.randrange(len(values)), rng.randint(-100, 100)
        fenwick.add(index, value - values[index]); segment.update(index, value); values[index] = value
    assert segment.range_sum(0, len(values)) == sum(values)
    assert fenwick.range_sum(0, len(values) - 1) == sum(values)


def test_dsu_against_component_labels() -> None:
    dsu = DisjointSetUnion(8)
    groups = [{index} for index in range(8)]
    for left, right in [(0, 1), (2, 3), (1, 3), (5, 6), (6, 7)]:
        dsu.union(left, right)
        merged = next(group for group in groups if left in group) | next(group for group in groups if right in group)
        groups = [group for group in groups if left not in group and right not in group] + [merged]
    for left in range(8):
        for right in range(8):
            assert dsu.connected(left, right) == any(left in group and right in group for group in groups)


@given(st.lists(st.integers(-10**6, 10**6), max_size=100))
def test_sorting_matches_canonical(values: list[int]) -> None:
    assert merge_sort(values) == sorted(values)
    assert quick_sort(values) == sorted(values)


def test_binary_search_present_and_missing() -> None:
    values = [1, 3, 5, 7, 9]
    assert binary_search(values, 7) == 3
    assert binary_search(values, 2) == -1


def test_minimum_and_large_cases_across_catalog() -> None:
    assert euclidean_gcd(0, 0) == 0
    assert extended_gcd(0, 9)[0] == 9
    assert binary_exponentiation(2, 1000) == 2**1000
    assert modular_inverse(1, 2) == 1
    assert prime_factorization(1) == []
    assert len(eratosthenes_sieve(10_000)) == 1229
    assert euler_linear_sieve(10_000)[0][-1] == 9973
    assert euler_phi(99_991) == 99_990
    assert combination(100, 50) == comb(100, 50)
    assert chinese_remainder([]) == (0, 1)
    assert bfs([[]], 0) == ([0], [0])
    assert dfs([[]], 0) == [0]
    assert dijkstra([[]], 0) == [0]
    assert topological_sort([]) == []
    assert DisjointSetUnion(1).connected(0, 0)
    assert FenwickTree([7]).range_sum(0, 0) == 7
    assert SegmentTree([7]).range_sum(0, 1) == 7
    assert binary_search([], 3) == -1
    values = list(range(2000, -1, -1))
    assert merge_sort(values) == sorted(values)
    assert quick_sort(values) == sorted(values)


def test_random_dijkstra_against_bellman_ford_reference() -> None:
    rng = random.Random(19)
    for size in range(2, 9):
        graph: list[list[tuple[int, int]]] = [[] for _ in range(size)]
        edges: list[tuple[int, int, int]] = []
        for left in range(size):
            for right in range(size):
                if left != right and rng.random() < 0.25:
                    weight = rng.randint(0, 20)
                    graph[left].append((right, weight)); edges.append((left, right, weight))
        expected = [10**30] * size; expected[0] = 0
        for _ in range(size - 1):
            for left, right, weight in edges:
                expected[right] = min(expected[right], expected[left] + weight)
        assert dijkstra(graph, 0) == [None if value == 10**30 else value for value in expected]


@pytest.mark.parametrize("base,exponent,modulus", [(-7, 0, 13), (2, 63, 97), (10**9, 12345, 1_000_000_007)])
def test_binary_exponentiation_matches_pow(base: int, exponent: int, modulus: int) -> None:
    assert binary_exponentiation(base, exponent, modulus) == pow(base, exponent, modulus)


@given(st.integers(2, 10_000), st.integers(1, 10_000))
def test_modular_inverse_property(modulus: int, value: int) -> None:
    if gcd(value, modulus) == 1:
        inverse = modular_inverse(value, modulus)
        assert 0 <= inverse < modulus
        assert value * inverse % modulus == 1
    else:
        with pytest.raises(ValueError):
            modular_inverse(value, modulus)


@given(st.integers(1, 10**9))
def test_prime_factorization_reconstructs_input(value: int) -> None:
    factors = prime_factorization(value)
    reconstructed = 1
    for prime, exponent in factors:
        assert prime >= 2 and exponent >= 1
        assert all(prime % divisor for divisor in range(2, int(prime**0.5) + 1))
        reconstructed *= prime**exponent
    assert reconstructed == value


def test_sieves_and_phi_against_brute_force() -> None:
    for limit in range(120):
        reference = [value for value in range(2, limit + 1) if all(value % divisor for divisor in range(2, int(value**0.5) + 1))]
        assert eratosthenes_sieve(limit) == reference
        assert euler_linear_sieve(limit)[0] == reference
    for value in range(1, 150):
        assert euler_phi(value) == sum(gcd(value, candidate) == 1 for candidate in range(1, value + 1))


@given(st.integers(0, 60), st.integers(-3, 63))
def test_combination_matches_math_comb(n: int, k: int) -> None:
    assert combination(n, k) == (comb(n, k) if 0 <= k <= n else 0)


def test_crt_result_satisfies_every_congruence() -> None:
    rng = random.Random(2026)
    for _ in range(40):
        moduli = rng.sample([3, 5, 7, 11, 13, 17], 3)
        congruences = [(rng.randrange(modulus), modulus) for modulus in moduli]
        residue, modulus = chinese_remainder(congruences)
        assert modulus == moduli[0] * moduli[1] * moduli[2]
        assert all(residue % item_modulus == item_residue for item_residue, item_modulus in congruences)


def test_random_graph_traversal_and_topological_invariants() -> None:
    rng = random.Random(73)
    for size in range(1, 20):
        dag = [[] for _ in range(size)]
        undirected = [[] for _ in range(size)]
        for left in range(size):
            for right in range(left + 1, size):
                if rng.random() < 0.18:
                    dag[left].append(right)
                    undirected[left].append(right)
                    undirected[right].append(left)
        order = topological_sort(dag)
        position = {node: index for index, node in enumerate(order)}
        assert all(position[left] < position[right] for left, edges in enumerate(dag) for right in edges)
        bfs_order, distances = bfs(undirected, 0)
        dfs_order = dfs(undirected, 0)
        assert len(bfs_order) == len(set(bfs_order))
        assert set(bfs_order) == set(dfs_order)
        assert distances[0] == 0
        assert all(distances[right] <= distances[left] + 1 for left, edges in enumerate(undirected) if distances[left] >= 0 for right in edges)


@given(st.lists(st.integers(-1000, 1000), max_size=150), st.integers(-1000, 1000))
def test_binary_search_and_sort_multiset(values: list[int], target: int) -> None:
    ordered = sorted(values)
    index = binary_search(ordered, target)
    assert (index == -1) == (target not in ordered)
    if index >= 0:
        assert ordered[index] == target
    for implementation in (merge_sort, quick_sort):
        result = implementation(values)
        assert result == ordered
        assert Counter(result) == Counter(values)
