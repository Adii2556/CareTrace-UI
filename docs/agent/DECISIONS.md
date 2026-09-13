# Decisions

Dates below are recording dates (2026-09-13), not invented historical adoption
dates. These capture the existing architecture and approved direction.

| Date | Decision | Reason | Status |
| --- | --- | --- | --- |
| 2026-09-13 | Django monolith; no unnecessary microservices | Small hackathon MVP with coherent app boundaries | Accepted |
| 2026-09-13 | Django Templates, Bootstrap 5, Vanilla JavaScript | Simple shared UI without SPA infrastructure | Accepted |
| 2026-09-13 | SQLite and Django ORM | Minimal MVP persistence; migration requires approval | Accepted |
| 2026-09-13 | Native Django Authentication; minimal custom User before first migrations | Reuse security conventions and avoid disruptive later user substitution | Accepted |
| 2026-09-13 | Account identity separate from patient healthcare data | Keep domain ownership out of authentication | Accepted |
| 2026-09-13 | Username login; optional unverified contact email | Preserve existing account implementation; email is not recovery identity | Existing baseline |
| 2026-09-13 | Local Django Media Storage initially | Simple local storage; future medical files require authorized download views | Accepted |
| 2026-09-13 | Environment variables for configuration/secrets | Keep credentials out of code and documentation | Accepted |
| 2026-09-13 | WhiteNoise static assets and Gunicorn for Linux hosting | Existing production configuration; no hosting yet | Accepted |
| 2026-09-13 | NVIDIA Nemotron through a future service adapter | Keep external AI separate from domain logic | Planned; separate approval required |
| 2026-09-13 | Railway deployment later | Defer hosting until an approved deployment step | Planned; separate approval required |
| 2026-09-13 | No speculative dependencies/features | Preserve scope and understandable architecture | Accepted |
| 2026-09-13 | Markdown + Git/GitHub coordination, with human approval per step | Transparent planning, implementation and review without orchestration infrastructure | Accepted |

See [architecture](../ARCHITECTURE.md) for details. Add entries only for meaningful
changes to data architecture, storage, integrations, authentication, major dependencies,
domain ownership or deployment. Do not log variable renames, spacing or import order.
