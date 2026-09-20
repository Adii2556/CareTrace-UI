# Latest handoff

## Step

Railway deployment and live verification.

## Status

COMPLETE — deployed and verified on 2026-09-20.

## Completed

Deployed the fictional CareTrace Django demo from GitHub to Railway with production
settings, HTTPS, a public domain, health checks, automatic deployments and one
persistent volume for SQLite and media. Seeded the fictional `ananya` and `arjun`
accounts and verified both live role-aware entry flows.

## Files

`config/settings.py`, `care/tests.py`, `README.md`, `docs/ARCHITECTURE.md`,
`docs/agent/CURRENT_STEP.md`, `docs/agent/ROADMAP.md` and this handoff.

## Decisions

Keep HTTPS enforcement for every user-facing route and exempt only `/health/` for
Railway's private HTTP probe. Keep the demo at one replica because SQLite and media
share an attached volume. Store credentials only in Railway/user handoff, never Git.

## Verification

- Railway deployment and `/health/`: online.
- Patient login (`ananya`) and dashboard: passed in the live browser.
- Clinician login (`arjun`) and referral workspace: passed in the live browser.
- Browser console warnings/errors: none.
- `python manage.py check`: passed.
- `python manage.py check --deploy`: passed with only the intentionally disabled
  HSTS subdomain/preload notices.
- `python manage.py makemigrations --check --dry-run`: no changes.
- `python manage.py test`: 17 tests passed.
- Ruff lint/format, static collection and `pip check`: passed.

## Issues

Railway-managed backups/PITR require a Pro plan and were not purchased. The workspace
shows a trial allowance of three days or $5 remaining, so continued availability
requires the owner to choose a Railway plan before the trial expires. The service is
a fictional-data prototype and makes no compliance claim.

## Next

Owner decision on Railway billing and backups. Do not begin another roadmap item
without an explicit instruction.
