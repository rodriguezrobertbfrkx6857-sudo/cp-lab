from __future__ import annotations

import logging
import os
import uuid
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.api.core.benchmark import BENCHMARKABLE, SUITES, initialize_database, list_runs, load_run, run_benchmark
from apps.api.core.catalog import algorithm_by_slug, algorithms, code_sources
from apps.api.core.visualization import visualize
from apps.api.schemas import BenchmarkRequest, CompareRequest, VisualizationRequest

APP_VERSION = "1.0.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("cp-lab")


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    logger.info("CP-Lab API %s starting", APP_VERSION)
    yield


app = FastAPI(title="CP-Lab API", version=APP_VERSION, docs_url="/api/docs", lifespan=lifespan)
cors_origins = [origin.strip() for origin in os.getenv(
    "CP_LAB_CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))[:128]
    if request.headers.get("content-length") and int(request.headers["content-length"]) > 1_000_000:
        return JSONResponse(status_code=413, content={"error": {"code": "PAYLOAD_TOO_LARGE", "message": "Request body exceeds 1 MB."}, "requestId": request_id})
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(HTTPException)
async def http_error(_: Request, exception: HTTPException) -> JSONResponse:
    detail = exception.detail
    if isinstance(detail, dict) and "code" in detail:
        error = detail
    else:
        error = {"code": "HTTP_ERROR", "message": str(detail)}
    return JSONResponse(status_code=exception.status_code, content={"error": error})


@app.exception_handler(Exception)
async def unhandled_error(_: Request, exception: Exception) -> JSONResponse:
    logger.exception("Unhandled endpoint error", exc_info=exception)
    return JSONResponse(status_code=500, content={"error": {"code": "INTERNAL_ERROR", "message": "The request could not be completed."}})


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": APP_VERSION, "service": "cp-lab-api"}


@app.get("/algorithms", tags=["algorithms"])
def list_algorithms(
    category: str | None = None, difficulty: str | None = None,
    visualization: bool | None = None, benchmark: bool | None = None,
    query: str | None = Query(default=None, max_length=100),
) -> list[dict[str, Any]]:
    items = algorithms()
    if category: items = [item for item in items if item["category"].casefold() == category.casefold()]
    if difficulty: items = [item for item in items if item["difficulty"].casefold() == difficulty.casefold()]
    if visualization is not None: items = [item for item in items if item["visualization"] is visualization]
    if benchmark is not None: items = [item for item in items if item["benchmark"] is benchmark]
    if query:
        needle = query.casefold()
        items = [item for item in items if needle in " ".join([item["title"], item["shortDescription"], *item.get("tags", [])]).casefold()]
    return items


@app.get("/algorithms/{slug}", tags=["algorithms"])
def get_algorithm(slug: str) -> dict[str, Any]:
    item = algorithm_by_slug(slug)
    if not item:
        raise HTTPException(404, {"code": "ALGORITHM_NOT_FOUND", "message": f"Unknown algorithm: {slug}"})
    return {**item, "code": code_sources()}


@app.post("/visualize", tags=["visualization"])
def create_visualization(payload: VisualizationRequest) -> dict[str, Any]:
    item = algorithm_by_slug(payload.algorithm)
    if not item:
        raise HTTPException(404, {"code": "ALGORITHM_NOT_FOUND", "message": f"Unknown algorithm: {payload.algorithm}"})
    if not item["visualization"]:
        raise HTTPException(422, {"code": "VISUALIZATION_UNSUPPORTED", "message": "This algorithm has no visualization adapter."})
    try:
        return visualize(payload.algorithm, payload.input, payload.parameters, payload.seed)
    except (ValueError, IndexError, TypeError) as error:
        raise HTTPException(422, {"code": "INVALID_ALGORITHM_INPUT", "message": str(error)}) from error


@app.post("/benchmark", tags=["benchmark"])
def create_benchmark(payload: BenchmarkRequest) -> dict[str, Any]:
    try:
        return run_benchmark(payload)
    except ValueError as error:
        raise HTTPException(422, {"code": "INVALID_BENCHMARK_CONFIG", "message": str(error)}) from error


@app.get("/benchmark-suites", tags=["benchmark"])
def benchmark_suites() -> dict[str, list[str]]:
    return SUITES


@app.get("/benchmark/{run_id}", tags=["benchmark"])
def get_benchmark(run_id: str) -> dict[str, Any]:
    result = load_run(run_id)
    if not result:
        raise HTTPException(404, {"code": "BENCHMARK_NOT_FOUND", "message": "Benchmark run not found."})
    return result


@app.get("/benchmark-history/recent", tags=["benchmark"])
def benchmark_history(limit: int = Query(default=10, ge=1, le=50)) -> list[dict[str, Any]]:
    return list_runs(limit)


@app.post("/compare", tags=["compare"])
def compare(payload: CompareRequest) -> dict[str, Any]:
    left, right = algorithm_by_slug(payload.algorithm_a), algorithm_by_slug(payload.algorithm_b)
    if not left or not right:
        raise HTTPException(404, {"code": "ALGORITHM_NOT_FOUND", "message": "One or both comparison algorithms are unknown."})
    benchmark_result = None
    if payload.benchmark:
        configured = payload.benchmark.model_copy(update={"algorithms": [payload.algorithm_a, payload.algorithm_b]})
        if all(slug in BENCHMARKABLE for slug in configured.algorithms): benchmark_result = run_benchmark(configured)
    return {
        "algorithmA": left, "algorithmB": right,
        "benchmark": benchmark_result,
        "guidance": "Choose based on input constraints, guarantees, memory, and data shape—not a universal winner.",
    }
