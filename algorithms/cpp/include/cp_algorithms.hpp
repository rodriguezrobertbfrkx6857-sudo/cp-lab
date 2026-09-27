#pragma once

#include <algorithm>
#include <cstdint>
#include <functional>
#include <limits>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <tuple>
#include <utility>
#include <vector>

namespace cplab {

using i64 = std::int64_t;

inline i64 euclidean_gcd(i64 a, i64 b) {
    a = std::abs(a); b = std::abs(b);
    while (b != 0) { const i64 remainder = a % b; a = b; b = remainder; }
    return a;
}

inline std::tuple<i64, i64, i64> extended_gcd(i64 a, i64 b) {
    i64 old_r = a, r = b, old_s = 1, s = 0, old_t = 0, t = 1;
    while (r != 0) {
        const i64 quotient = old_r / r;
        std::tie(old_r, r) = std::pair{i64(r), i64(old_r - quotient * r)};
        std::tie(old_s, s) = std::pair{i64(s), i64(old_s - quotient * s)};
        std::tie(old_t, t) = std::pair{i64(t), i64(old_t - quotient * t)};
    }
    if (old_r < 0) return {-old_r, -old_s, -old_t};
    return {old_r, old_s, old_t};
}

inline i64 binary_exponentiation(i64 base, i64 exponent, i64 modulus) {
    if (exponent < 0 || modulus <= 0) throw std::invalid_argument("invalid exponent or modulus");
    i64 result = 1 % modulus; base %= modulus;
    while (exponent) {
        if (exponent & 1) result = static_cast<i64>((__int128)result * base % modulus);
        base = static_cast<i64>((__int128)base * base % modulus); exponent >>= 1;
    }
    return result;
}

inline i64 modular_inverse(i64 value, i64 modulus) {
    if (modulus <= 1) throw std::invalid_argument("modulus must exceed one");
    auto [divisor, x, unused] = extended_gcd(value, modulus); (void)unused;
    if (divisor != 1) throw std::invalid_argument("inverse does not exist");
    return (x % modulus + modulus) % modulus;
}

inline std::vector<std::pair<i64, int>> prime_factorization(i64 value) {
    if (value < 1) throw std::invalid_argument("value must be positive");
    std::vector<std::pair<i64, int>> result;
    for (i64 divisor = 2; divisor <= value / divisor; divisor += divisor == 2 ? 1 : 2) {
        int exponent = 0;
        while (value % divisor == 0) { value /= divisor; ++exponent; }
        if (exponent) result.emplace_back(divisor, exponent);
    }
    if (value > 1) result.emplace_back(value, 1);
    return result;
}

inline std::vector<int> eratosthenes_sieve(int limit) {
    if (limit < 2) return {};
    std::vector<bool> prime(limit + 1, true); prime[0] = prime[1] = false;
    for (int value = 2; value <= limit / value; ++value)
        if (prime[value]) for (int multiple = value * value; multiple <= limit; multiple += value) prime[multiple] = false;
    std::vector<int> result;
    for (int value = 2; value <= limit; ++value) if (prime[value]) result.push_back(value);
    return result;
}

inline std::pair<std::vector<int>, std::vector<int>> euler_linear_sieve(int limit) {
    if (limit < 0) throw std::invalid_argument("limit must be non-negative");
    std::vector<int> primes, smallest(limit + 1);
    for (int value = 2; value <= limit; ++value) {
        if (smallest[value] == 0) { smallest[value] = value; primes.push_back(value); }
        for (int prime : primes) {
            if (prime > limit / value) break;
            smallest[prime * value] = prime;
            if (prime == smallest[value]) break;
        }
    }
    return {primes, smallest};
}

inline i64 euler_phi(i64 value) {
    if (value < 1) throw std::invalid_argument("value must be positive");
    i64 result = value;
    for (auto [prime, exponent] : prime_factorization(value)) { (void)exponent; result -= result / prime; }
    return result;
}

inline i64 combination(int n, int k) {
    if (n < 0) throw std::invalid_argument("n must be non-negative");
    if (k < 0 || k > n) return 0;
    k = std::min(k, n - k); std::vector<i64> row(k + 1); row[0] = 1;
    for (int current = 1; current <= n; ++current)
        for (int choice = std::min(current, k); choice > 0; --choice) row[choice] += row[choice - 1];
    return row[k];
}

inline std::pair<i64, i64> chinese_remainder(const std::vector<std::pair<i64, i64>>& congruences) {
    i64 residue = 0, modulus = 1;
    for (auto [next_residue, next_modulus] : congruences) {
        if (next_modulus <= 0) throw std::invalid_argument("moduli must be positive");
        auto [divisor, coefficient, unused] = extended_gcd(modulus, next_modulus); (void)unused;
        const i64 difference = next_residue - residue;
        if (difference % divisor != 0) throw std::invalid_argument("incompatible congruences");
        const i64 reduced = next_modulus / divisor;
        i64 step = static_cast<i64>((__int128)(difference / divisor) * coefficient % reduced);
        if (step < 0) step += reduced;
        residue += modulus * step; modulus *= reduced; residue = (residue % modulus + modulus) % modulus;
    }
    return {residue, modulus};
}

inline std::pair<std::vector<int>, std::vector<int>> bfs(const std::vector<std::vector<int>>& graph, int source) {
    if (source < 0 || source >= static_cast<int>(graph.size())) throw std::out_of_range("source");
    std::vector<int> order, distance(graph.size(), -1); std::queue<int> frontier; frontier.push(source); distance[source] = 0;
    while (!frontier.empty()) {
        const int node = frontier.front(); frontier.pop(); order.push_back(node);
        for (int neighbor : graph[node]) if (distance[neighbor] == -1) { distance[neighbor] = distance[node] + 1; frontier.push(neighbor); }
    }
    return {order, distance};
}

inline std::vector<int> dfs(const std::vector<std::vector<int>>& graph, int source) {
    if (source < 0 || source >= static_cast<int>(graph.size())) throw std::out_of_range("source");
    std::vector<int> order, stack{source}; std::vector<bool> visited(graph.size());
    while (!stack.empty()) {
        const int node = stack.back(); stack.pop_back(); if (visited[node]) continue; visited[node] = true; order.push_back(node);
        for (auto iterator = graph[node].rbegin(); iterator != graph[node].rend(); ++iterator) if (!visited[*iterator]) stack.push_back(*iterator);
    }
    return order;
}

inline std::vector<i64> dijkstra(const std::vector<std::vector<std::pair<int, i64>>>& graph, int source) {
    constexpr i64 infinity = std::numeric_limits<i64>::max();
    if (source < 0 || source >= static_cast<int>(graph.size())) throw std::out_of_range("source");
    std::vector<i64> distance(graph.size(), infinity); distance[source] = 0;
    using State = std::pair<i64, int>; std::priority_queue<State, std::vector<State>, std::greater<>> heap; heap.emplace(0, source);
    while (!heap.empty()) {
        auto [current, node] = heap.top(); heap.pop(); if (current != distance[node]) continue;
        for (auto [neighbor, weight] : graph[node]) {
            if (weight < 0) throw std::invalid_argument("negative edge");
            if (current <= infinity - weight && current + weight < distance[neighbor]) { distance[neighbor] = current + weight; heap.emplace(distance[neighbor], neighbor); }
        }
    }
    return distance;
}

inline std::vector<int> topological_sort(const std::vector<std::vector<int>>& graph) {
    std::vector<int> indegree(graph.size()), order; for (const auto& edges : graph) for (int node : edges) ++indegree[node];
    std::queue<int> frontier; for (int node = 0; node < static_cast<int>(graph.size()); ++node) if (indegree[node] == 0) frontier.push(node);
    while (!frontier.empty()) { const int node = frontier.front(); frontier.pop(); order.push_back(node); for (int neighbor : graph[node]) if (--indegree[neighbor] == 0) frontier.push(neighbor); }
    if (order.size() != graph.size()) throw std::invalid_argument("graph contains a cycle");
    return order;
}

class DisjointSetUnion {
    std::vector<int> parent_, size_;
public:
    explicit DisjointSetUnion(int size) : parent_(size), size_(size, 1) { std::iota(parent_.begin(), parent_.end(), 0); }
    int find(int value) { while (value != parent_[value]) { parent_[value] = parent_[parent_[value]]; value = parent_[value]; } return value; }
    bool unite(int left, int right) { left = find(left); right = find(right); if (left == right) return false; if (size_[left] < size_[right]) std::swap(left, right); parent_[right] = left; size_[left] += size_[right]; return true; }
    bool connected(int left, int right) { return find(left) == find(right); }
};

class FenwickTree {
    std::vector<i64> tree_;
public:
    explicit FenwickTree(const std::vector<i64>& values) : tree_(values.size() + 1) { for (int index = 0; index < static_cast<int>(values.size()); ++index) add(index, values[index]); }
    void add(int index, i64 delta) { for (++index; index < static_cast<int>(tree_.size()); index += index & -index) tree_[index] += delta; }
    i64 prefix_sum(int end) const { i64 result = 0; for (++end; end > 0; end -= end & -end) result += tree_[end]; return result; }
    i64 range_sum(int left, int right) const { return left > right ? 0 : prefix_sum(right) - (left ? prefix_sum(left - 1) : 0); }
};

class SegmentTree {
    int length_, size_ = 1; std::vector<i64> tree_;
public:
    explicit SegmentTree(const std::vector<i64>& values) : length_(static_cast<int>(values.size())) { while (size_ < length_) size_ *= 2; tree_.assign(2 * size_, 0); std::copy(values.begin(), values.end(), tree_.begin() + size_); for (int i = size_ - 1; i; --i) tree_[i] = tree_[i * 2] + tree_[i * 2 + 1]; }
    void update(int index, i64 value) { if (index < 0 || index >= length_) throw std::out_of_range("index"); for (tree_[index += size_] = value; index > 1; index /= 2) tree_[index / 2] = tree_[index] + tree_[index ^ 1]; }
    i64 range_sum(int left, int right) const { if (left < 0 || left > right || right > length_) throw std::out_of_range("range"); i64 result = 0; for (left += size_, right += size_; left < right; left /= 2, right /= 2) { if (left & 1) result += tree_[left++]; if (right & 1) result += tree_[--right]; } return result; }
};

inline int binary_search(const std::vector<i64>& values, i64 target) {
    int low = 0, high = static_cast<int>(values.size()) - 1;
    while (low <= high) { const int middle = low + (high - low) / 2; if (values[middle] == target) return middle; if (values[middle] < target) low = middle + 1; else high = middle - 1; }
    return -1;
}

inline std::vector<i64> merge_sort(std::vector<i64> values) {
    std::vector<i64> buffer(values.size());
    for (std::size_t width = 1; width < values.size(); width *= 2)
        for (std::size_t start = 0; start < values.size(); start += 2 * width) {
            const auto middle = std::min(start + width, values.size()), end = std::min(start + 2 * width, values.size());
            std::merge(values.begin() + start, values.begin() + middle, values.begin() + middle, values.begin() + end, buffer.begin() + start);
            std::copy(buffer.begin() + start, buffer.begin() + end, values.begin() + start);
        }
    return values;
}

inline std::vector<i64> quick_sort(std::vector<i64> values) {
    if (values.empty()) return values;
    std::vector<std::pair<int, int>> stack{{0, static_cast<int>(values.size()) - 1}};
    while (!stack.empty()) {
        auto [low, high] = stack.back(); stack.pop_back();
        if (low >= high) continue;
        const i64 pivot = values[low + (high - low) / 2];
        int left = low, right = high;
        while (left <= right) {
            while (values[left] < pivot) ++left;
            while (values[right] > pivot) --right;
            if (left <= right) { std::swap(values[left], values[right]); ++left; --right; }
        }
        if (low < right) stack.emplace_back(low, right);
        if (left < high) stack.emplace_back(left, high);
    }
    return values;
}

}  // namespace cplab
