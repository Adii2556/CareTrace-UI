# Current development step

Step: Feature 1 — Create Referral
Status: COMPLETE

## Objective

Add a permission-aware product workflow for an authorized clinician to create a
referral, select relevant patient records, and review referral list/detail pages while
preserving the existing patient-consent and destination-clinician access boundaries.

## Existing verified scope

- Shared responsive shell and supplied CareTrace visual system.
- Patient dashboard, timeline, records, filtering, upload, explainer, emergency and privacy views.
- Referral selection, explicit consent, tracking and clinician workspace.
- Patient ownership, clinician assignment, consent checks and locked referral packages.
- Railway-compatible Gunicorn/WhiteNoise configuration and CI.
- Migrations, fictional demo seed, README and automated/browser verification.

## Feature boundary

Implement only Create Referral. Do not begin Global Search, language switching,
AI4Bharat or any later incremental feature. Do not expose an unrestricted patient
directory or allow a receiving clinician to view selected medical records before
patient consent. Stop after verified completion and wait for explicit `GO`.

## Result

Completed and verified on 2026-09-21. Clinicians can create referrals for connected
patients, select patient-owned records, and use permission-scoped referral history and
detail pages. The patient and referring clinician can review the prepared context;
the destination clinician receives clinical context only after patient consent.

Next approval gate: Feature 2 — Global Search Bar. Do not start without explicit `GO`.
