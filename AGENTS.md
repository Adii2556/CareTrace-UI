# CareTrace agent entry point

CareTrace is a healthcare hackathon MVP developed one approved step at a time.

## Read before each step

1. [Project context](docs/agent/PROJECT_CONTEXT.md)
2. [Current step](docs/agent/CURRENT_STEP.md)
3. [Decisions](docs/agent/DECISIONS.md)
4. [Architecture](docs/ARCHITECTURE.md)
5. [Development rules](docs/DEVELOPMENT_RULES.md)
6. [README](README.md)

Inspect current code and Git status before editing. Consult the
[roadmap](docs/agent/ROADMAP.md) for broader context and the
[handoff](docs/agent/HANDOFF.md) for the latest result.

## Operating rules

- Implement only CURRENT_STEP plus an explicit human invocation. READY alone is
  not approval. Explicit direct user instructions override planning documents.
- Preserve working architecture and Django conventions; make the smallest coherent
  change. No speculative features or next roadmap step; mention future work in handoff.
- Approved stack: Python, Django, Django Templates, Bootstrap 5, Vanilla JavaScript,
  SQLite for MVP, Django ORM/Authentication/Media Storage, Git/GitHub, Gunicorn,
  WhiteNoise, and environment variables. Nemotron API and Railway are later steps.
- No major technology changes without approval: React, Vue, Node backend, DRF,
  Docker, Redis, Celery, MongoDB, microservices, PostgreSQL migration, or external
  cloud infrastructure. Do not silently replace agreed technologies.
- Never commit secrets or put API keys in code/docs; use environment variables.
  Treat future medical data as sensitive, validate server-side, and preserve
  Django security protections. Account identity is not a patient healthcare profile.
- Follow development rules for coding. Run README's exact verification commands:
  relevant tests, Django checks, Ruff lint/format, migration checks (required for
  model changes), and relevant behavior verification. Preserve passing tests unless
  an approved architecture change makes them obsolete.

## Lifecycle and completion

Set the approved current step IN_PROGRESS when starting, COMPLETE only after
successful verification, or BLOCKED if a major issue prevents safe progress.
Resolve minor choices independently. For a blocker, explain it in HANDOFF and stop.
See [workflow](README.md#ai-assisted-development-workflow) for approval and review.

At completion, replace HANDOFF with short Step, Status, Completed, Files, Decisions,
Verification, Issues, Next sections; update the implemented step's status and roadmap.
Update DECISIONS only for meaningful architecture/product choices, and relevant
authoritative docs when architecture materially changes. Avoid unrelated rewrites.
After each completed, verified step, commit the intended project changes and push
to https://github.com/Adii2556/CareTrace-UI.git as authorized by the human. Include
the updated handoff; exclude secrets/runtime files. Preserve remote history, never
force-push, and verify upstream sync and working-tree status. Report any push blocker.
End with a short **Handoff for ChatGPT**: Completed, Files, Decisions/Issues, Next.
STOP for explicit instruction; completion never authorizes the next step.
