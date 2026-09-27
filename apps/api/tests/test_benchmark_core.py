from __future__ import annotations

import pytest

from apps.api.core import benchmark
from apps.api.schemas import BenchmarkRequest, DatasetConfig


def test_summary_statistics_median_min_max_and_nearest_rank_p95() -> None:
    summary = benchmark.summarize_samples([8.0, 1.0, 4.0, 2.0, 100.0])
    assert summary == {"medianMs": 4.0, "minMs": 1.0, "maxMs": 100.0, "p95Ms": 100.0}
    assert benchmark.summarize_samples([3.0, 1.0, 2.0, 4.0])["medianMs"] == 2.5


@pytest.mark.parametrize("samples", [[], [-1.0], [float("inf")], [float("nan")]])
def test_summary_statistics_reject_invalid_or_empty_samples(samples: list[float]) -> None:
    with pytest.raises(ValueError):
        benchmark.summarize_samples(samples)


def test_seeded_dataset_is_reproducible_and_honors_shapes() -> None:
    for kind in ("random", "sorted", "reverse-sorted", "nearly-sorted", "duplicate-heavy"):
        config = DatasetConfig(kind=kind, size=100, min_value=-50, max_value=50, density=0.2)
        first = benchmark.generate_dataset(config, 73)
        second = benchmark.generate_dataset(config, 73)
        assert first == second
        assert len(first) == 100
        if kind == "sorted":
            assert first == sorted(first)
        if kind == "reverse-sorted":
            assert first == sorted(first, reverse=True)
        if kind == "duplicate-heavy":
            assert len(set(first)) <= 16


def test_warmups_execute_but_are_excluded_from_samples(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def operation() -> None:
        calls.append("run")

    monkeypatch.setattr(benchmark, "_python_operation", lambda _slug, _data, _config: (operation, 17))
    ticks = iter([0, 1_000_000, 2_000_000, 5_000_000, 8_000_000, 12_000_000])
    monkeypatch.setattr(benchmark.time, "perf_counter_ns", lambda: next(ticks))
    request = BenchmarkRequest(
        algorithms=["merge-sort"], language="python",
        dataset=DatasetConfig(size=4), warmups=2, measured_runs=3, seed=42,
    )
    result = benchmark._measure("merge-sort", request)
    assert len(calls) == 5
    assert result["samplesMs"] == [1.0, 3.0, 4.0]
    assert result["operations"] == 17
