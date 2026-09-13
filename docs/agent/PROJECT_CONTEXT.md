# Project context

CareTrace is a **hackathon-oriented MVP**, not a production-certified healthcare
platform. Its intended healthcare scope is a longitudinal patient medical timeline,
organized reports/prescriptions/records, preserved history, and continuity during
hospital referrals. Later approved phases may simplify difficult medical information
using AI, explain recommended tests/medications, and support family-linked health context.

## What exists

The Django foundation is documented in [Step 1](../STEP_1.md). This checkout also
already contains authentication, basic account editing and a protected empty app
shell, documented in [Step 2](../STEP_2.md). No healthcare functionality exists.
Step 1.5 adds repository coordination only; it does not implement or remove that code.
[CURRENT_STEP](CURRENT_STEP.md) retains Step 2 READY as explicitly requested,
pending human review of this planning/baseline discrepancy and a separate invocation.

## Architecture

```text
Browser
   ↓
Django Templates / Bootstrap 5 / Vanilla JavaScript
   ↓
Django Views / Forms
   ↓
Domain / Service Logic (only when real domain complexity requires it)
   ↓
Django ORM
   ↓
SQLite
```

Future integrations, added only through approved steps:

```text
Django Service Layer → External Adapter → Nemotron / Healthcare API / Storage Provider
```

This diagram is a responsibility boundary, not permission to create empty layers.
See [architecture](../ARCHITECTURE.md) for actual modules, routes and security;
[README](../../README.md) for stack versions, setup and verification;
[decisions](DECISIONS.md) for agreed choices.

## Domain boundary

**Authentication User ≠ Patient Healthcare Profile.** The minimal custom Django
user represents login/account identity. Healthcare information belongs in deliberate
future domain models, not a growing authentication record. Model future doctor,
hospital and referral concepts deliberately; do not add them to User by convenience.

## Sources of truth

[AGENTS](../../AGENTS.md) directs reading; [CURRENT_STEP](CURRENT_STEP.md) defines
the work; [development rules](../DEVELOPMENT_RULES.md) govern coding;
[ROADMAP](ROADMAP.md) gives direction; [HANDOFF](HANDOFF.md) records the latest result.
The human approves each implementation. Repository Markdown plus Git is the workflow;
there is no agent orchestration service or automatic deployment.
