# Latest handoff

## Step

Feature 1 — Create Referral.

## Status

COMPLETE — implemented and verified on 2026-09-21.

## Completed

Added a permission-aware referral creation form, list and detail experience. Referring
provider identity is derived from the authenticated clinician, the patient choice is
limited to an existing clinical relationship, selected records remain patient-owned,
and destination clinical context remains consent-gated.

## Files

Referral model/migration, form, views, URLs, tests, seed/admin integration, three care
templates, shared referral navigation/style, README, architecture/decision/roadmap docs
and `DEVELOPMENT_LOG.md`.

## Decisions

Store referring clinician separately from destination clinician. Restrict patient
choices to existing referral relationships until a dedicated access-grant model exists.
Keep the established pending/shared/received/closed/rejected status convention.

## Verification

- Django check and migration drift check: passed.
- Full/focused Django suite: 25 tests passed.
- Ruff lint/format and pip dependency checks: passed.
- Fresh isolated migration and fictional seed: passed.
- Static collection: passed.
- Production-style deploy check: only deliberate HSTS subdomain/preload notices.
- Desktop and 390px browser flows: passed with no console errors or overflow.

## Issues

The first patient-clinician connection still requires administration because CareTrace
does not yet have a care-team/access-grant model. Railway backups/PITR remain a separate
paid-plan limitation. No new dependency or environment variable was introduced.

## Next

Feature 2 — Global Search Bar, only after the user explicitly replies `GO`.
