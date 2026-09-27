# Security Specification

## V1 threat reduction

Do not execute arbitrary user-supplied code.

Trusted execution only:
- repository C++ implementations
- repository Python implementations

Users may modify:
- inputs
- parameters
- dataset configuration
- seed

## Input validation

Validate:
- numeric bounds
- array lengths
- graph size
- graph weights
- benchmark iteration limits
- seed format
- enum values

## Resource limits

Set practical limits for:
- input size
- benchmark duration
- request body size
- concurrent expensive work

## Production basics

- no debug stack traces
- sanitize logs
- no secrets in repository
- `.env.example` only
- dependency updates
- least-privilege deployment configuration

## Out of scope

A sandboxed arbitrary-code runner is a separate future feature and must not be improvised inside V1.
