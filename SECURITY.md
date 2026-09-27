# Security

## Supported version

Security fixes target the current V1 branch.

## Model and controls

CP-Lab never executes user-submitted source code. Only repository-owned Python
and C++20 implementations run. Pydantic strictly rejects unknown fields and
bounds sizes, seeds, iteration counts, and enums. Requests above 1 MB are rejected;
benchmark work is serialized; production errors omit traces; SQLite uses bound
parameters; CORS origins are explicit environment configuration.

Do not commit credentials. Copy `.env.example` and supply deployment values out
of band. Report vulnerabilities privately to repository maintainers before public
disclosure, including impact, reproduction, and affected revision.
