# Backend Specification

## Stack

- FastAPI
- Python 3
- Pydantic
- SQLite where persistence is useful

## Responsibilities

- algorithm metadata serving
- visualization-step generation where backend-owned
- benchmark orchestration
- benchmark result persistence
- compare data aggregation
- health endpoint

## Suggested modules

```txt
apps/api/
  main.py
  api/
  core/
  models/
  schemas/
  services/
  repositories/
  benchmark/
  visualization/
```

## Persistence

V1 database can remain intentionally small.

Suggested persisted entities:
- BenchmarkRun
- BenchmarkSeries
- ExperimentPreset

Algorithm content can remain source-controlled metadata/files.

## Error handling

Return structured errors with:
- machine-readable code
- human-readable message
- optional details

Never expose stack traces in production responses.

## Observability

At minimum:
- startup log
- endpoint error log
- benchmark failure log
- request correlation id if practical
