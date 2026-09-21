# Decisions

| Date | Decision | Reason | Status |
| --- | --- | --- | --- |
| 2026-09-13 | Django monolith with templates, Bootstrap 5, vanilla JavaScript and SQLite | Keep the hackathon implementation understandable | Accepted |
| 2026-09-13 | Environment variables for configuration and secrets | Prevent committed credentials | Accepted |
| 2026-09-13 | WhiteNoise and Gunicorn for Linux hosting | Railway-compatible static and WSGI serving | Accepted |
| 2026-09-20 | Use Django's built-in User with a one-to-one `PatientProfile` | Keep authentication native while separating healthcare metadata | Accepted |
| 2026-09-20 | Assign each referral to a concrete clinician account | Prevent cross-clinician ID-based access | Accepted |
| 2026-09-20 | Require explicit unchecked consent and lock the selected package afterward | Preserve patient control over the exact shared scope | Accepted |
| 2026-09-20 | Serve medical downloads through authorization-aware views | Avoid public media exposure | Accepted |
| 2026-09-20 | Keep NVIDIA/Nemotron calls in `ai_services` and degrade safely | Isolate credentials/failures and keep the app usable offline | Accepted |
| 2026-09-20 | Preserve the static design pack alongside the dynamic product | Retain the visual source of truth and prior repository work | Accepted |
| 2026-09-21 | Separate the referral creator from the destination clinician and derive provider snapshots from authenticated profiles | Preserve who initiated a transfer without trusting submitted identity fields | Accepted |
| 2026-09-21 | Limit referral creation to patients previously referred by the signed-in clinician | Avoid exposing an unrestricted patient directory or letting destination assignment bootstrap referring-clinician access | Accepted |
