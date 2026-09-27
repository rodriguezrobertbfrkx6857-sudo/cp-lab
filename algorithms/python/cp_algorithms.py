"""Contest-oriented reference implementations for the CP-Lab V1 catalog."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from math import gcd
from typing import Iterable


def euclidean_gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    if old_r < 0:
        return -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def binary_exponentiation(base: int, exponent: int, modulus: int | None = None) -> int:
    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    if modulus is not None and modulus <= 0:
        raise ValueError("modulus must be positive")
    result = 1 if modulus is None else 1 % modulus
    base = base if modulus is None else base % modulus
    while exponent:
        if exponent & 1:
            result = result * base if modulus is None else result * base % modulus
        base = base * base if modulus is None else base * base % modulus
        exponent >>= 1
    return result


def modular_inverse(value: int, modulus: int) -> int:
    if modulus <= 1:
        raise ValueError("modulus must exceed one")
    divisor, x, _ = extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError("inverse does not exist")
    return x % modulus


def prime_factorization(value: int) -> list[tuple[int, int]]:
    if value < 1:
        raise ValueError("value must be positive")
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= value:
        exponent = 0
        while value % divisor == 0:
            value //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append((value, 1))
    return factors


def eratosthenes_sieve(limit: int) -> list[int]:
    if limit < 2:
        return []
    prime = bytearray(b"\x01") * (limit + 1)
    prime[0:2] = b"\x00\x00"
    for value in range(2, int(limit**0.5) + 1):
        if prime[value]:
            prime[value * value : limit + 1 : value] = b"\x00" * (((limit - value * value) // value) + 1)
    return [value for value in range(2, limit + 1) if prime[value]]


def euler_linear_sieve(limit: int) -> tuple[list[int], list[int]]:
    if limit < 0:
        raise ValueError("limit must be non-negative")
    smallest = [0] * (limit + 1)
    primes: list[int] = []
    for value in range(2, limit + 1):
        if smallest[value] == 0:
            smallest[value] = value
            primes.append(value)
        for prime in primes:
            composite = prime * value
            if composite > limit:
                break
            smallest[composite] = prime
            if prime == smallest[value]:
                break
    return primes, smallest


def euler_phi(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    result, remaining = value, value
    for prime, _ in prime_factorization(value):
        result -= result // prime
        while remaining % prime == 0:
            remaining //= prime
    return result


def combination(n: int, k: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    row = [1] + [0] * k
    for current in range(1, n + 1):
        for choice in range(min(current, k), 0, -1):
            row[choice] += row[choice - 1]
    return row[k]


def chinese_remainder(congruences: Iterable[tuple[int, int]]) -> tuple[int, int]:
    residue, modulus = 0, 1
    for next_residue, next_modulus in congruences:
        if next_modulus <= 0:
            raise ValueError("moduli must be positive")
        divisor, coefficient, _ = extended_gcd(modulus, next_modulus)
        difference = next_residue - residue
        if difference % divisor:
            raise ValueError("incompatible congruences")
        reduced = next_modulus // divisor
        step = (difference // divisor * coefficient) % reduced
        residue += modulus * step
        modulus *= reduced
        residue %= modulus
    return residue, modulus


def bfs(graph: list[list[int]], source: int) -> tuple[list[int], list[int]]:
    if not 0 <= source < len(graph):
        raise ValueError("source is out of range")
    order: list[int] = []
    distance = [-1] * len(graph)
    distance[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if not 0 <= neighbor < len(graph):
                raise ValueError("edge endpoint is out of range")
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return order, distance


def dfs(graph: list[list[int]], source: int) -> list[int]:
    if not 0 <= source < len(graph):
        raise ValueError("source is out of range")
    order: list[int] = []
    visited = [False] * len(graph)
    stack = [source]
    while stack:
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        order.append(node)
        for neighbor in reversed(graph[node]):
            if not 0 <= neighbor < len(graph):
                raise ValueError("edge endpoint is out of range")
            if not visited[neighbor]:
                stack.append(neighbor)
    return order


def dijkstra(graph: list[list[tuple[int, int]]], source: int) -> list[int | None]:
    if not 0 <= source < len(graph):
        raise ValueError("source is out of range")
    infinity = 10**30
    distance = [infinity] * len(graph)
    distance[source] = 0
    heap = [(0, source)]
    while heap:
        current_distance, node = heappop(heap)
        if current_distance != distance[node]:
            continue
        for neighbor, weight in graph[node]:
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative weights")
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    return [None if value == infinity else value for value in distance]


def topological_sort(graph: list[list[int]]) -> list[int]:
    indegree = [0] * len(graph)
    for neighbors in graph:
        for neighbor in neighbors:
            indegree[neighbor] += 1
    queue = deque(index for index, degree in enumerate(indegree) if degree == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != len(graph):
        raise ValueError("graph contains a cycle")
    return order


class DisjointSetUnion:
    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("size must be non-negative")
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, value: int) -> int:
        while value != self.parent[value]:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True

    def connected(self, left: int, right: int) -> bool:
        return self.find(left) == self.find(right)


class FenwickTree:
    def __init__(self, values: Iterable[int]) -> None:
        materialized = list(values)
        self.tree = [0] * (len(materialized) + 1)
        for index, value in enumerate(materialized):
            self.add(index, value)

    def add(self, index: int, delta: int) -> None:
        index += 1
        while index < len(self.tree):
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, end: int) -> int:
        result = 0
        end += 1
        while end > 0:
            result += self.tree[end]
            end -= end & -end
        return result

    def range_sum(self, left: int, right: int) -> int:
        if left > right:
            return 0
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left else 0)


class SegmentTree:
    def __init__(self, values: Iterable[int]) -> None:
        values = list(values)
        self.length = len(values)
        self.size = 1
        while self.size < self.length:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        self.tree[self.size : self.size + self.length] = values
        for index in range(self.size - 1, 0, -1):
            self.tree[index] = self.tree[index * 2] + self.tree[index * 2 + 1]

    def update(self, index: int, value: int) -> None:
        if not 0 <= index < self.length:
            raise IndexError(index)
        index += self.size
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[index * 2] + self.tree[index * 2 + 1]

    def range_sum(self, left: int, right: int) -> int:
        if not 0 <= left <= right <= self.length:
            raise ValueError("expected a half-open range inside the array")
        left, right = left + self.size, right + self.size
        result = 0
        while left < right:
            if left & 1:
                result += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                result += self.tree[right]
            left //= 2
            right //= 2
        return result


def binary_search(values: list[int], target: int) -> int:
    low, high = 0, len(values) - 1
    while low <= high:
        middle = low + (high - low) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def merge_sort(values: Iterable[int]) -> list[int]:
    result = list(values)
    width = 1
    while width < len(result):
        for start in range(0, len(result), 2 * width):
            middle, end = min(start + width, len(result)), min(start + 2 * width, len(result))
            result[start:end] = _merge(result[start:middle], result[middle:end])
        width *= 2
    return result


def _merge(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index]); left_index += 1
        else:
            merged.append(right[right_index]); right_index += 1
    return merged + left[left_index:] + right[right_index:]


def quick_sort(values: Iterable[int]) -> list[int]:
    result = list(values)
    if not result:
        return result
    stack = [(0, len(result) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = result[low + (high - low) // 2]
        left, right = low, high
        while left <= right:
            while result[left] < pivot:
                left += 1
            while result[right] > pivot:
                right -= 1
            if left <= right:
                result[left], result[right] = result[right], result[left]
                left, right = left + 1, right - 1
        if low < right:
            stack.append((low, right))
        if left < high:
            stack.append((left, high))
    return result


ALGORITHM_FUNCTIONS = {
    "euclidean-gcd": euclidean_gcd, "extended-gcd": extended_gcd,
    "binary-exponentiation": binary_exponentiation, "modular-inverse": modular_inverse,
    "prime-factorization": prime_factorization, "eratosthenes-sieve": eratosthenes_sieve,
    "euler-linear-sieve": euler_linear_sieve, "euler-phi": euler_phi,
    "combination": combination, "crt": chinese_remainder, "bfs": bfs, "dfs": dfs,
    "dijkstra": dijkstra, "topological-sort": topological_sort,
    "binary-search": binary_search, "merge-sort": merge_sort, "quick-sort": quick_sort,
}
