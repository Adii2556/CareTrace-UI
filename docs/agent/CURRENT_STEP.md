# Current Development Step

Step: 2 — Authentication and Account Foundation
Status: READY
Objective: Build CareTrace's account/authentication layer and protected application
shell using Django's native authentication architecture.

## Context

Use the minimal custom User created in Step 1. Step 1.5 initializes this specification
only; there is no authorization to implement it during the workflow task.
READY requires a separate explicit human invocation before IN_PROGRESS.

**Baseline discrepancy:** this checkout already contains the listed routes, forms,
views and tests, and [STEP_2.md](../STEP_2.md) reports completion. Preserve them.
The human/reviewer should reconcile the existing result with this requested READY
specification before invocation. On approval, inspect and verify existing coverage
first; do not duplicate implementation or infer permission for Step 3.

## In Scope

- Registration, login and logout using native Django authentication.
- Authentication-required application shell and minimal account/profile page.
- Safe non-medical account editing, authentication-aware navigation, messages, tests.

## Out of Scope

Patient healthcare profiles, timeline, medical records, document upload, prescriptions,
reports, OCR, AI, Nemotron, referrals, doctors, hospitals, family medical history,
ABHA, ABDM, FHIR, APIs, DRF and role dashboards. Password reset/change and email
verification remain deferred under the existing architecture. No deployment.

## Functional Requirements

- Registration validates inputs/passwords server-side and uses Django password hashing.
  Preserve username login and optional non-unique, unverified contact email.
- Native Django login/logout; logout is CSRF-protected POST. Preserve safe local
  return destinations and existing registration-to-app redirect.
- Protect app/account views server-side. Bind account editing to request.user;
  permit only first_name, last_name and email, never IDs or privilege fields.
- Provide an empty protected welcome shell, a minimal account page, state-aware
  shared navigation and appropriate success/error messages using existing templates.
- Namespaced, named routes: /accounts/register/, /accounts/login/,
  /accounts/logout/, /accounts/profile/, /app/, following current URL conventions.

## Architecture Constraints

Account identity and patient healthcare profile are separate concepts. Do not add
medical data to User or create another user model. Do not introduce doctor/patient/
hospital roles. If an unavoidable dependency requires them, document the blocker
and stop rather than inventing role architecture. No model changes are expected.
Follow [architecture](../ARCHITECTURE.md), [decisions](DECISIONS.md), and
[development rules](../DEVELOPMENT_RULES.md). Preserve CSRF, password validation,
session protections, escaping, and existing security behavior. No new stack/dependencies.

## Expected Files / Areas

Existing apps/accounts/ forms, views and URLs; apps/core/ shell; templates/accounts/,
templates/core/ and shared navigation/components; tests/test_accounts.py; relevant
documentation. Inspect first; this is not a requirement to modify every area.

## Testing Requirements

Cover registration page access, valid/invalid registration, password hashing,
successful/failed login, logout, anonymous restriction, authenticated protected
access, account ownership/access and all Step 1 regressions. Preserve existing
tests for CSRF, safe redirects, forbidden fields, escaping and inactive login.
Run all [README verification commands](../../README.md#verification), including
Django checks, Ruff lint/format and migration drift checks. Verify relevant rendered
behavior; use disposable data for any manual registration smoke test.

## Completion Criteria

Scope works against the inspected baseline; required checks pass; previously passing
tests remain; no excluded functionality or security weakening; architecture/docs
reflect any material change. Report whether existing implementation satisfied scope
or actual changes were needed. Reconcile the earlier completion report explicitly.

## Handoff Requirements

Replace [HANDOFF](HANDOFF.md) with Step, Status, Completed, Files, Decisions,
Verification, Issues, Next. Record actual verification and limitations. Mark this
step and roadmap COMPLETE only after verification; if blocked, mark BLOCKED and
explain why. Update decisions only for meaningful choices. Stop for human review;
do not prepare or implement Step 3 automatically.
