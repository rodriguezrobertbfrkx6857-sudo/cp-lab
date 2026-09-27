from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class VisualizationRequest(StrictModel):
    algorithm: str = Field(pattern=r"^[a-z0-9-]+$")
    parameters: dict[str, Any] = Field(default_factory=dict)
    input: Any = None
    seed: int = Field(default=42, ge=0, le=2**31 - 1)


class DatasetConfig(StrictModel):
    kind: Literal[
        "random", "sorted", "reverse-sorted", "nearly-sorted", "duplicate-heavy",
        "sparse-graph", "dense-graph", "chain-graph", "random-tree"
    ] = "random"
    size: int = Field(default=1000, ge=1, le=100_000)
    min_value: int = Field(default=0, ge=-1_000_000, le=1_000_000)
    max_value: int = Field(default=1_000_000, ge=-1_000_000, le=1_000_000)
    density: float = Field(default=0.15, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_bounds(self) -> "DatasetConfig":
        if self.min_value > self.max_value:
            raise ValueError("min_value must not exceed max_value")
        if self.kind == "dense-graph" and self.size > 1_000:
            raise ValueError("dense graph datasets are limited to 1000 nodes")
        if self.kind in {"sparse-graph", "chain-graph", "random-tree"} and self.size > 20_000:
            raise ValueError("graph datasets are limited to 20000 nodes")
        return self


class BenchmarkRequest(StrictModel):
    algorithms: list[str] = Field(min_length=1, max_length=4)
    language: Literal["python", "cpp"] = "python"
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    warmups: int = Field(default=3, ge=0, le=10)
    measured_runs: int = Field(default=10, ge=3, le=30)
    seed: int = Field(default=42, ge=0, le=2**31 - 1)


class CompareRequest(StrictModel):
    algorithm_a: str
    algorithm_b: str
    benchmark: BenchmarkRequest | None = None
