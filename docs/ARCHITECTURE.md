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
Clinician referral access requires both assignment and recorded patient consent.
The referral package is locked after patient review. Downloads are served by an
authorized Django view, not exposed as public media URLs. Uploads validate extension,
content type, size and ownership. Logout and all state changes use POST with CSRF.

The application does not claim regulatory compliance. All committed/demo clinical
content is fictional.

## Deployment

Shared settings are environment-driven. Production disables debug, requires a secret
and hosts, enables HTTPS/security controls, serves collected static assets through
WhiteNoise and runs through Gunicorn. SQLite and media require persistent storage on
Railway. The repository contains deployment-compatible configuration, not a live
deployment or managed backup policy.
