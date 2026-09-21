# CareTrace architecture

CareTrace is a compact Django monolith for the SIH 2026 prototype.

```text
Browser
  -> Django templates + Bootstrap 5 + project CSS + vanilla JavaScript
  -> Django views, forms and authorization decorators
  -> Django ORM
  -> SQLite and protected Django media storage
```

## Modules

- `accounts/`: Django `User` companion profile, patient/clinician role and identity metadata.
- `care/`: medical records, appointments, medications, referrals, consent, access logs and workflows.
- `ai_services/`: isolated NVIDIA/Nemotron client with timeout and malformed-response handling.
- `templates/`: shared shell plus patient and clinician pages.
- `static/`: generated CareTrace styling, Manrope, Lucide icon data, QR and vanilla JavaScript.
- `docs/design/caretrace-ui/`: preserved visual source pack and verification artifacts.

## Security boundaries

Patient pages require the patient role and always query through `request.user`.
Referral creation records an authenticated referring clinician separately from the
destination clinician. To avoid a global patient directory without inventing a new
care-team model, the create form offers only patients for whom the signed-in clinician
previously created a referral. Destination assignment alone never grants the stronger
referring-clinician capability. Provider names and organizations are derived server-side
from the authenticated profiles rather than trusted from submitted text.

The patient and referring clinician can review the prepared referral. A destination
clinician can see referral routing metadata, but clinical context and selected records
require recorded patient consent. The referral package is locked after patient review.
Global search is server-rendered through the Django ORM and follows those same scopes:
patients see only their own referrals and records; clinicians see only referral-linked
patients and referrals; a destination clinician sees selected record metadata only
after consent. Search results are capped per group and do not create a separate index.
Downloads are served by an authorized Django view, not exposed as public media URLs.
Uploads validate extension, content type, size and ownership. Logout and all state
changes use POST with CSRF.

Temporary judge access is an explicit demo-only exception at the authentication entry
point, not an authorization bypass. When `DJANGO_DEMO_QUICK_LOGIN` is enabled, a
POST-only CSRF-protected endpoint maps two fixed selections to the synthetic `ananya`
patient and `arjun` clinician accounts. It verifies that the account is active and has
the expected role, rejects unsafe return URLs and starts a normal Django session. The
feature is disabled by default and does not alter any downstream ownership, consent or
download checks.

The application does not claim regulatory compliance. All committed/demo clinical
content is fictional.

## Deployment

Shared settings are environment-driven. Production disables debug, requires a secret
and hosts, enables HTTPS/security controls, serves collected static assets through
WhiteNoise and runs through Gunicorn. SQLite and media require persistent storage on
Railway. The private `/health/` liveness endpoint is the sole HTTPS-redirect
exception so Railway can probe it internally without weakening user-facing routes.
The deployed demonstration uses one replica, `/app/media/db.sqlite3` for SQLite and
`/app/media` as its persistent volume mount. Railway-managed backups and point-in-time
recovery are not enabled because they require a Pro plan.

Judge quick access is enabled or reverted with one Railway environment variable. Demo
accounts and fictional records are seeded once through the existing `seed_demo`
management command rather than being silently recreated during every application start.
