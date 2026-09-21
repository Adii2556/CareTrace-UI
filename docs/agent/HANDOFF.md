# Latest handoff

## Step

Temporary Judge Demo Access.

## Status

COMPLETE — implemented and verified on 2026-09-22.

## Completed

Added a disabled-by-default judge mode that lets a visitor choose the fixed fictional
patient or hospital/clinician profile without receiving a password. The POST-only
endpoint verifies CSRF, account activity and the expected role before starting a normal
Django session. Normal credential login remains available as a collapsed fallback.

## Files

Authentication view/URL/tests, login template, shared CSS, settings, `.env.example`,
README, architecture/decision/roadmap/current-step docs and `DEVELOPMENT_LOG.md`.

## Decisions

Use `DJANGO_DEMO_QUICK_LOGIN`, defaulting to false, as the sole feature switch. Keep
demo account seeding a one-time deployment action and preserve every downstream access
control unchanged. Deployment seeding uses unusable passwords so the public demo
identities cannot also be entered through credential authentication.

## Verification

- Eight focused tests passed, including disabled mode, CSRF, both roles,
  role mismatch and unsafe return URL handling.
- Django checks, migration drift, full regression tests, Ruff, dependency checks,
  production deploy checks and static collection passed.
- Desktop and 390 x 844 browser flows passed for patient and clinician profiles; the
  credential fallback remained usable with no console warnings/errors or overflow.
- Railway deployed the feature at `https://web-production-ef1db6.up.railway.app/`.
  Both public profile flows passed, `/health/` returned 200, GET on the POST-only
  endpoint returned 405 and a POST without CSRF returned 403.
- Production demo accounts were seeded with unusable passwords and verified as
  `has_usable_password() == False`.

## Issues

The Browser plugin and local Playwright commands were unavailable, so rendered QA used
the available in-app browser controls against isolated local data and the Railway demo.
No schema or dependency change was required.

## Next

After judging, set `DJANGO_DEMO_QUICK_LOGIN=False` in Railway and deploy that one
variable change. Language Switcher remains approval-gated and was not started.
