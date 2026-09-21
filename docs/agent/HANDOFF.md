# Latest handoff

## Step

Feature 2 — Global Search Bar.

## Status

COMPLETE — implemented and verified on 2026-09-21.

## Completed

Replaced the decorative top-bar placeholder with a real GET search form and added a
grouped results page for existing patients, referrals and medical records. Matching is
case-insensitive and partial. Results follow existing patient ownership, referral
relationship and consent rules; no global patient or record directory was introduced.

## Files

Search view/URL/tests, shared top bar, search-results template, responsive styles,
README, architecture/decision/roadmap/current-step docs and `DEVELOPMENT_LOG.md`.

## Decisions

Use one server-rendered Django ORM results page with a 100-character query limit and
20-result cap per group. Search only existing entities and provider snapshot fields;
do not add autocomplete, an API or a separate search service.

## Verification

- Django check and migration drift check: passed.
- Six focused search tests and the full 32-test suite: passed.
- Ruff lint/format and pip dependency checks: passed.
- Static collection: passed.
- Production-style deploy check: only deliberate HSTS subdomain/preload notices.
- Patient and clinician browser flows at 1440 x 900 and 390 x 844: passed with no
  horizontal overflow or browser console warnings/errors.

## Issues

The first test invocation used the system Python without project dependencies; all
tests were rerun successfully with `.venv`. No database, dependency, secret or
environment-variable change was required.

## Next

Feature 3 — Language Switcher, only after the user explicitly replies `GO`.
