# Development rules

1. Implement only the requested step; stop after reporting its result.
2. Inspect existing code and these documents before changing architecture.
3. Make the smallest coherent change; preserve compatibility where practical.
4. Keep the agreed Django/Templates/Bootstrap/Vanilla JS/SQLite stack.
5. No speculative features, fake data, or empty abstraction layers.
6. Keep dependencies minimal and pinned; update pins deliberately and verify them.
7. Never commit secrets, runtime databases, uploads, or generated static output.
8. Each app owns one coherent domain. Keep views small and templates presentation-only.
9. Prefer Django forms, validators, and ORM; validate inputs on the server.
10. Use descriptive names, PEP 8, explicit imports, small functions, and useful
    type hints/comments. Settings inheritance is the only wildcard import exception.
11. Use named URLs. Do not duplicate logic or scatter configuration constants.
12. Add meaningful tests; run Django checks, migration checks, tests, and Ruff.
13. Update architecture/setup documentation when behavior or conventions change.
14. Do not add React, Node, Docker, Redis, Celery, microservices, external services,
    or a replacement database without explicit approval.
15. Do not treat a feature request as permission to redesign the whole project.

## UI rules

Prefer Bootstrap components before custom components. Extend shared layouts;
extract repeated markup into components/partials. No inline CSS or large inline
scripts. Use semantic HTML, accessible form labels, keyboard-friendly controls,
consistent spacing/page widths, and responsive navigation. Keep custom assets
centralized. Do not refine the full visual identity or invent navigation/features
until requested. Render untrusted text with Django autoescaping enabled.

## Completion rule

Use [AGENTS.md](../AGENTS.md) as the workflow entry point and
[CURRENT_STEP.md](agent/CURRENT_STEP.md) plus explicit human invocation as the
implementation boundary. Coding rules remain authoritative here; workflow status
and handoff rules live in AGENTS.md. Keep material architecture changes in the
relevant authoritative document rather than duplicating them across planning files.

Report actual checks and material limitations. End with an extremely short
`Handoff for ChatGPT`: **Completed**, **Files**, **Decisions/Issues**, **Next**.
Do not begin the next step automatically.
