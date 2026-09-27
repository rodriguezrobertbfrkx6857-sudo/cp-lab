from __future__ import annotations

import json
import math
import os
import pathlib
import platform
import random
import sqlite3
import statistics
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from algorithms.python import cp_algorithms as alg
from apps.api.schemas import BenchmarkRequest, DatasetConfig

ROOT = pathlib.Path(__file__).resolve().parents[3]
def _database_path() -> pathlib.Path:
    configured = os.getenv("CP_LAB_DATABASE_URL", "sqlite:///./cp_lab.db")
    prefix = "sqlite:///"
    if not configured.startswith(prefix):
        raise ValueError("CP_LAB_DATABASE_URL must use a sqlite:/// URL")
    raw_path = configured[len(prefix):]
    path = pathlib.Path(raw_path)
    return path if path.is_absolute() else ROOT / path


DATABASE = _database_path()
BENCHMARKABLE = {
    "euclidean-gcd", "binary-exponentiation", "prime-factorization", "eratosthenes-sieve",
    "euler-linear-sieve", "euler-phi", "bfs", "dfs", "dijkstra", "dsu",
    "fenwick-tree", "segment-tree", "binary-search", "merge-sort", "quick-sort",
    "naive-gcd", "naive-power", "trial-prime", "dsu-basic", "naive-prefix",
}
SUITES = {
    "naive-gcd-vs-euclidean": ["naive-gcd", "euclidean-gcd"],
    "naive-power-vs-binary-exponentiation": ["naive-power", "binary-exponentiation"],
    "trial-prime-vs-sieve": ["trial-prime", "eratosthenes-sieve"],
    "eratosthenes-vs-euler-sieve": ["eratosthenes-sieve", "euler-linear-sieve"],
    "bfs-vs-dfs": ["bfs", "dfs"],
    "dsu-path-compression": ["dsu-basic", "dsu"],
    "fenwick-vs-naive-prefix": ["naive-prefix", "fenwick-tree"],
    "merge-sort-vs-quick-sort": ["merge-sort", "quick-sort"],
}
_LOCK = threading.Lock()


def initialize_database() -> None:
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS benchmark_runs (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT NOT NULL)")


def load_run(run_id: str) -> dict[str, Any] | None:
    initialize_database()
    with sqlite3.connect(DATABASE) as connection:
        row = connection.execute("SELECT payload FROM benchmark_runs WHERE id = ?", (run_id,)).fetchone()
    return json.loads(row[0]) if row else None


def list_runs(limit: int = 10) -> list[dict[str, Any]]:
    initialize_database()
    with sqlite3.connect(DATABASE) as connection:
        rows = connection.execute(
            "SELECT payload FROM benchmark_runs ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [json.loads(row[0]) for row in rows]


def run_benchmark(request: BenchmarkRequest) -> dict[str, Any]:
    unsupported = [slug for slug in request.algorithms if slug not in BENCHMARKABLE]
    if unsupported:
        raise ValueError(f"benchmark is not supported for: {', '.join(unsupported)}")
    with _LOCK:
        results = [_measure(slug, request) for slug in request.algorithms]
    run_id = str(uuid.uuid4())
    payload = {
        "id": run_id, "status": "completed", "results": results,
        "environment": {
            "language": request.language,
            "runtime": platform.python_version() if request.language == "python" else _compiler_version(),
            "os": platform.platform(), "cpu": platform.processor() or "unavailable",
            "buildMode": "CPython optimized runtime" if request.language == "python" else "C++20 -O2",
            "timestamp": datetime.now(timezone.utc).isoformat(), "seed": request.seed,
            "warmupRuns": request.warmups, "measuredRuns": request.measured_runs,
            "measurementLocation": "backend",
        },
        "dataset": request.dataset.model_dump(),
    }
    initialize_database()
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("INSERT INTO benchmark_runs VALUES (?, ?, ?)", (run_id, payload["environment"]["timestamp"], json.dumps(payload)))
    return payload


def _measure(slug: str, request: BenchmarkRequest) -> dict[str, Any]:
    if request.language == "cpp":
        samples = _measure_cpp(slug, request)
        operations = None
    else:
        data = generate_dataset(request.dataset, request.seed)
        operation, operations = _python_operation(slug, data, request.dataset)
        for _ in range(request.warmups): operation()
        samples = []
        for _ in range(request.measured_runs):
            started = time.perf_counter_ns(); operation(); samples.append((time.perf_counter_ns() - started) / 1_000_000)
    summary = summarize_samples(samples)
    return {
        "algorithm": slug, "language": request.language, "samplesMs": samples,
        **summary, "operations": operations, "memoryBytes": None,
        "memoryNote": "Not reported: portable trustworthy per-operation memory measurement is unavailable.",
    }


def summarize_samples(samples: list[float]) -> dict[str, float]:
    if not samples:
        raise ValueError("at least one measured sample is required")
    if any(not math.isfinite(value) or value < 0 for value in samples):
        raise ValueError("measured samples must be finite non-negative values")
    ordered = sorted(samples)
    p95_index = min(len(ordered) - 1, math.ceil(0.95 * len(ordered)) - 1)
    return {
        "medianMs": statistics.median(samples),
        "minMs": ordered[0],
        "maxMs": ordered[-1],
        "p95Ms": ordered[p95_index],
    }


def generate_dataset(config: DatasetConfig, seed: int) -> list[int]:
    rng = random.Random(seed)
    values = [rng.randint(config.min_value, config.max_value) for _ in range(config.size)]
    if config.kind == "sorted": values.sort()
    elif config.kind == "reverse-sorted": values.sort(reverse=True)
    elif config.kind == "nearly-sorted":
        values.sort()
        for _ in range(max(1, config.size // 20)):
            left, right = rng.randrange(config.size), rng.randrange(config.size); values[left], values[right] = values[right], values[left]
    elif config.kind == "duplicate-heavy": values = [rng.randint(0, 15) for _ in range(config.size)]
    return values


def _python_operation(slug: str, data: list[int], config: DatasetConfig | None = None) -> tuple[Callable[[], Any], int | None]:
    safe_positive = [abs(value) + 1 for value in data]
    if slug == "naive-gcd":
        def naive_gcd() -> int:
            left, right = safe_positive[0], safe_positive[-1]
            while left != right:
                if left > right: left -= right
                else: right -= left
            return left
        return naive_gcd, None
    if slug == "euclidean-gcd": return lambda: alg.euclidean_gcd(safe_positive[0], safe_positive[-1]), None
    if slug == "naive-power": return lambda: _naive_power(safe_positive[0], safe_positive[-1] % 100_000, 1_000_000_007), safe_positive[-1] % 100_000
    if slug == "binary-exponentiation": return lambda: alg.binary_exponentiation(safe_positive[0], safe_positive[-1] % 100_000, 1_000_000_007), None
    if slug == "prime-factorization": return lambda: alg.prime_factorization(safe_positive[0]), None
    if slug == "trial-prime": return lambda: [_is_prime(value) for value in safe_positive], None
    if slug == "eratosthenes-sieve": return lambda: alg.eratosthenes_sieve(len(data) * 10), len(data) * 10
    if slug == "euler-linear-sieve": return lambda: alg.euler_linear_sieve(len(data) * 10), len(data) * 10
    if slug == "euler-phi": return lambda: [alg.euler_phi(value) for value in safe_positive], len(data)
    if slug == "binary-search":
        ordered = sorted(data); targets = ordered[: min(256, len(ordered))]
        return lambda: [alg.binary_search(ordered, target) for target in targets], len(targets) * max(1, math.ceil(math.log2(len(ordered))))
    if slug == "merge-sort": return lambda: alg.merge_sort(data), max(1, len(data) * math.ceil(math.log2(len(data))))
    if slug == "quick-sort": return lambda: alg.quick_sort(data), None
    if slug == "dsu":
        def dsu_run() -> int:
            structure = alg.DisjointSetUnion(len(data))
            for index in range(1, len(data)): structure.union(index - 1, index)
            return structure.find(len(data)-1)
        return dsu_run, max(0, len(data)-1)
    if slug == "dsu-basic":
        def basic_dsu() -> int:
            parent = list(range(len(data)))
            def find(value: int) -> int:
                while parent[value] != value: value = parent[value]
                return value
            for index in range(1, len(data)): parent[find(index)] = find(index-1)
            return find(len(data)-1)
        return basic_dsu, max(0, len(data)-1)
    if slug == "naive-prefix": return lambda: [sum(data[:index+1]) for index in range(len(data))], len(data) * (len(data)+1) // 2
    if slug in {"fenwick-tree", "segment-tree"}:
        def tree_run() -> list[int]:
            tree = alg.FenwickTree(data) if slug == "fenwick-tree" else alg.SegmentTree(data)
            return [tree.prefix_sum(index) if slug == "fenwick-tree" else tree.range_sum(0, index+1) for index in range(len(data))]
        return tree_run, len(data)
    if slug in {"bfs", "dfs", "dijkstra"}:
        size = len(data)
        kind = config.kind if config else "chain-graph"
        pairs: list[tuple[int, int]] = []
        if kind == "dense-graph":
            threshold = int((config.density if config else 0.15) * 10_000)
            pairs = [(left, right) for left in range(size) for right in range(left + 1, size) if ((safe_positive[left] * 31 + safe_positive[right] * 17 + left * 13 + right) % 10_000) < threshold]
        elif kind == "random-tree":
            pairs = [(safe_positive[index] % index, index) for index in range(1, size)]
        elif kind == "sparse-graph":
            pairs = [(index - 1, index) for index in range(1, size)] + [(index, index + 2) for index in range(0, size - 2, 7)]
        else:
            pairs = [(index - 1, index) for index in range(1, size)]
        if slug == "dijkstra":
            graph = [[] for _ in range(size)]
            for left, right in pairs:
                weight=abs(data[right])%100+1; graph[left].append((right,weight)); graph[right].append((left,weight))
            return lambda: alg.dijkstra(graph,0), 2 * len(pairs)
        graph = [[] for _ in range(size)]
        for left, right in pairs: graph[left].append(right); graph[right].append(left)
        return (lambda: alg.bfs(graph,0)) if slug == "bfs" else (lambda: alg.dfs(graph,0)), 2 * len(pairs)
    raise ValueError(f"unsupported benchmark algorithm: {slug}")


def _naive_power(base: int, exponent: int, modulus: int) -> int:
    result = 1
    for _ in range(exponent): result = result * base % modulus
    return result


def _is_prime(value: int) -> bool:
    if value < 2: return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0: return False
        divisor += 1
    return True


def _cpp_binary() -> pathlib.Path:
    build = ROOT / "build" / "cpp"; build.mkdir(parents=True, exist_ok=True)
    binary = build / ("benchmark_runner.exe" if os.name == "nt" else "benchmark_runner")
    source = ROOT / "algorithms" / "cpp" / "benchmark_runner.cpp"
    header = ROOT / "algorithms" / "cpp" / "include" / "cp_algorithms.hpp"
    if not binary.exists() or binary.stat().st_mtime < max(source.stat().st_mtime, header.stat().st_mtime):
        command = [os.environ.get("CP_LAB_CPP_COMPILER", "g++"), "-std=c++20", "-O2", "-I", "algorithms/cpp/include", "algorithms/cpp/benchmark_runner.cpp", "-o", "build/cpp/benchmark_runner.exe" if os.name == "nt" else "build/cpp/benchmark_runner"]
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    return binary


def _measure_cpp(slug: str, request: BenchmarkRequest) -> list[float]:
    binary = _cpp_binary(); total_runs = request.warmups + request.measured_runs
    command = [str(binary.relative_to(ROOT)), slug, str(request.dataset.size), str(request.seed), str(total_runs), request.dataset.kind]
    completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, timeout=30)
    return [float(value) for value in json.loads(completed.stdout)][request.warmups:]


def _compiler_version() -> str:
    try:
        output = subprocess.run([os.environ.get("CP_LAB_CPP_COMPILER", "g++"), "--version"], capture_output=True, text=True, timeout=3, check=True).stdout
        return output.splitlines()[0]
    except (OSError, subprocess.SubprocessError):
        return "C++20 compiler (version unavailable)"
