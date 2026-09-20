# Current development step

Step: Railway deployment and live verification
Status: COMPLETE

## Objective

Deploy the verified CareTrace Django application to Railway with production settings,
persistent SQLite/media storage, a public HTTPS domain and fictional demo accounts;
then verify the live patient and clinician entry flows.

## Existing verified scope

- Shared responsive shell and supplied CareTrace visual system.
- Patient dashboard, timeline, records, filtering, upload, explainer, emergency and privacy views.
- Referral selection, explicit consent, tracking and clinician workspace.
- Patient ownership, clinician assignment, consent checks and locked referral packages.
- Railway-compatible Gunicorn/WhiteNoise configuration and CI.
- Migrations, fictional demo seed, README and automated/browser verification.

## Deployment boundary

The deployment remains a fictional-data demonstration and makes no regulatory-compliance
claim. Do not add family profiles, third-party healthcare exchange or public emergency
access. Stop if Railway requires a paid-plan purchase or if persistent storage cannot be
configured safely.

## Result

The fictional-data demo is live at
`https://web-production-09eb0.up.railway.app/` with a persistent Railway volume,
production environment settings, automatic GitHub deployments and verified patient
and clinician login flows. Railway-managed backups/PITR require a Pro plan and were
not enabled or purchased.
