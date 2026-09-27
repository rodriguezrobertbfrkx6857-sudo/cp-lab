# API Specification

Recommended minimal V1 endpoints.

## Health

`GET /health`

Returns service status/version.

## Algorithms

`GET /algorithms`

Filters may include:
- category
- difficulty
- visualization
- benchmark
- query

`GET /algorithms/{slug}`

Returns:
- metadata
- explanation data
- code references/content
- examples
- related algorithms

## Visualization

`POST /visualize`

Input:
- algorithm slug
- parameters
- input data
- seed

Returns:
- normalized input
- visualization steps
- final result

## Benchmark

`POST /benchmark`

Input:
- algorithms
- language
- dataset config
- warmups
- measured runs
- seed

Returns:
- benchmark run id
- results
- environment metadata

`GET /benchmark/{id}`

Returns saved result if persistence is enabled.

## Compare

`POST /compare`

Input:
- algorithm A
- algorithm B
- optional benchmark configuration

Returns:
- metadata comparison
- supported benchmark information
- generated or referenced benchmark result

## General API rules

- typed schemas
- validation
- stable errors
- no arbitrary code execution
- no silent coercion of malformed inputs
