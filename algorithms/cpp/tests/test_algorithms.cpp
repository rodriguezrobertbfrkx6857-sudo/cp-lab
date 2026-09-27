#include "cp_algorithms.hpp"
#include <algorithm>
#include <cassert>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <set>

using cplab::i64;

static bool is_prime(int value) {
    if (value < 2) return false;
    for (int divisor = 2; divisor <= value / divisor; ++divisor)
        if (value % divisor == 0) return false;
    return true;
}

int main() {
    using namespace cplab;
    std::mt19937 rng(20260920);

    assert(euclidean_gcd(0, 0) == 0);
    for (int iteration = 0; iteration < 500; ++iteration) {
        i64 a = static_cast<i64>(rng()) - static_cast<i64>(rng());
        i64 b = static_cast<i64>(rng()) - static_cast<i64>(rng());
        const auto divisor = euclidean_gcd(a, b);
        assert(divisor == std::gcd(a, b));
        assert(divisor == euclidean_gcd(b, a));
        if (divisor) assert(a % divisor == 0 && b % divisor == 0);
        auto [extended, x, y] = extended_gcd(a, b);
        assert(extended == divisor && a * x + b * y == extended);
    }

    for (i64 base = -7; base <= 7; ++base)
        for (i64 exponent = 0; exponent <= 40; ++exponent) {
            i64 reference = 1, modulus = 97;
            for (i64 i = 0; i < exponent; ++i) reference = static_cast<i64>((__int128)reference * base % modulus);
            reference = (reference % modulus + modulus) % modulus;
            assert((binary_exponentiation(base, exponent, modulus) + modulus) % modulus == reference);
        }

    for (i64 modulus = 2; modulus < 100; ++modulus)
        for (i64 value = 1; value < modulus; ++value)
            if (std::gcd(value, modulus) == 1) assert(value * modular_inverse(value, modulus) % modulus == 1);

    for (i64 value = 1; value <= 5000; ++value) {
        i64 rebuilt = 1;
        for (auto [prime, exponent] : prime_factorization(value)) {
            assert(is_prime(static_cast<int>(prime)));
            for (int count = 0; count < exponent; ++count) rebuilt *= prime;
        }
        assert(rebuilt == value);
    }

    for (int limit = 0; limit <= 300; ++limit) {
        std::vector<int> reference;
        for (int value = 2; value <= limit; ++value) if (is_prime(value)) reference.push_back(value);
        assert(eratosthenes_sieve(limit) == reference);
        assert(euler_linear_sieve(limit).first == reference);
    }

    for (int value = 1; value <= 250; ++value) {
        int reference = 0;
        for (int candidate = 1; candidate <= value; ++candidate) reference += std::gcd(value, candidate) == 1;
        assert(euler_phi(value) == reference);
    }
    assert(combination(0, 0) == 1 && combination(8, 3) == 56 && combination(8, 9) == 0);
    for (int n = 1; n <= 30; ++n)
        for (int k = 0; k <= n; ++k) assert(combination(n, k) == combination(n, n - k));

    for (int iteration = 0; iteration < 80; ++iteration) {
        std::vector<std::pair<i64, i64>> system{{static_cast<i64>(rng() % 3), 3}, {static_cast<i64>(rng() % 5), 5}, {static_cast<i64>(rng() % 7), 7}};
        auto [residue, modulus] = chinese_remainder(system);
        assert(modulus == 105);
        for (auto [expected, mod] : system) assert(residue % mod == expected);
    }

    std::vector<std::vector<int>> graph{{1, 2}, {3}, {3}, {4}, {}};
    auto [bfs_order, distances] = bfs(graph, 0);
    assert(bfs_order == std::vector<int>({0, 1, 2, 3, 4}));
    assert(distances == std::vector<int>({0, 1, 1, 2, 3}));
    auto dfs_order = dfs(graph, 0);
    assert(std::set<int>(dfs_order.begin(), dfs_order.end()) == std::set<int>({0, 1, 2, 3, 4}));
    auto topo = topological_sort(graph);
    std::vector<int> position(graph.size());
    for (int index = 0; index < static_cast<int>(topo.size()); ++index) position[topo[index]] = index;
    for (int left = 0; left < static_cast<int>(graph.size()); ++left)
        for (int right : graph[left]) assert(position[left] < position[right]);

    for (int iteration = 0; iteration < 40; ++iteration) {
        const int size = 2 + rng() % 12;
        std::vector<std::vector<std::pair<int, i64>>> weighted(size);
        std::vector<std::tuple<int, int, i64>> edges;
        for (int left = 0; left < size; ++left)
            for (int right = 0; right < size; ++right)
                if (left != right && rng() % 5 == 0) {
                    i64 weight = rng() % 30;
                    weighted[left].push_back({right, weight});
                    edges.push_back({left, right, weight});
                }
        auto actual = dijkstra(weighted, 0);
        const i64 infinity = std::numeric_limits<i64>::max();
        std::vector<i64> reference(size, infinity); reference[0] = 0;
        for (int pass = 1; pass < size; ++pass)
            for (auto [left, right, weight] : edges)
                if (reference[left] != infinity && reference[left] + weight < reference[right]) reference[right] = reference[left] + weight;
        assert(actual == reference);
    }

    DisjointSetUnion dsu(40);
    std::vector<int> labels(40); std::iota(labels.begin(), labels.end(), 0);
    for (int iteration = 0; iteration < 200; ++iteration) {
        int left = rng() % 40, right = rng() % 40;
        int old_left = labels[left], old_right = labels[right];
        dsu.unite(left, right);
        for (int& label : labels) if (label == old_right) label = old_left;
        for (int a = 0; a < 40; ++a) for (int b = 0; b < 40; ++b) assert(dsu.connected(a, b) == (labels[a] == labels[b]));
    }

    std::vector<i64> values(128);
    for (auto& value : values) value = static_cast<int>(rng() % 2001) - 1000;
    FenwickTree fenwick(values); SegmentTree segment(values);
    for (int iteration = 0; iteration < 300; ++iteration) {
        int left = rng() % values.size(), right = rng() % values.size();
        if (left > right) std::swap(left, right);
        i64 expected = std::accumulate(values.begin() + left, values.begin() + right + 1, i64{0});
        assert(fenwick.range_sum(left, right) == expected);
        assert(segment.range_sum(left, right + 1) == expected);
        if (iteration % 4 == 0) {
            int index = rng() % values.size(); i64 replacement = static_cast<int>(rng() % 2001) - 1000;
            fenwick.add(index, replacement - values[index]); segment.update(index, replacement); values[index] = replacement;
        }
    }

    for (int iteration = 0; iteration < 300; ++iteration) {
        std::vector<i64> input(rng() % 160);
        for (auto& value : input) value = static_cast<int>(rng() % 101) - 50;
        auto expected = input; std::sort(expected.begin(), expected.end());
        assert(merge_sort(input) == expected);
        assert(quick_sort(input) == expected);
        for (i64 target = -55; target <= 55; target += 5) {
            int index = binary_search(expected, target);
            assert((index == -1) == !std::binary_search(expected.begin(), expected.end(), target));
            if (index >= 0) assert(expected[index] == target);
        }
    }

    std::cout << "20 C++ algorithms passed edge, randomized, and reference checks\n";
}
