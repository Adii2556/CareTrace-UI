# CareTrace

CareTrace is a Django healthcare continuity prototype that helps a patient keep a longitudinal record, choose exactly which records accompany a referral, explicitly approve access, and review an access trail. Clinicians can open a referral workspace only after patient consent.

This repository rebuilds the supplied CareTrace interface as a dynamic application. The original static reference remains the visual source of truth; this implementation adds server-rendered data, authentication, ownership checks, consent enforcement, protected downloads, and tested workflows without introducing a JavaScript framework.

## Stack

- Python 3.14 and Django 6.1
- SQLite
- Django templates and forms
- Bootstrap 5 plus project CSS
- Vanilla JavaScript
- WhiteNoise for collected static files in the deployed Django service
- Optional NVIDIA API integration for plain-language record explanations

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo --password "choose-a-local-demo-password"
python manage.py runserver
```

Open `http://127.0.0.1:8000/accounts/login/` and sign in as either demo user:

- Patient: `ananya`
- Clinician: `arjun`

Both accounts use the password supplied to `seed_demo`. Demo records are fictional.

### Temporary judge demo access

For a time-limited judging environment, set `DJANGO_DEMO_QUICK_LOGIN=True` after
running `python manage.py seed_demo --unusable-password`. The login page then offers only the fixed fictional `ananya`
patient and `arjun` clinician profiles through a CSRF-protected POST action. Normal
credential login remains available under **Use account credentials**.

This mode intentionally lets any visitor enter those synthetic accounts. Never enable
it for real patient information. Disable it immediately after judging by setting
`DJANGO_DEMO_QUICK_LOGIN=False`; no code rollback or database change is required.
The recommended deployment command gives the two demo accounts unusable passwords,
so they cannot bypass the fixed quick-login flow through credential authentication.

The project reads configuration from environment variables. Django does not parse `.env` automatically, so load those values through your shell or hosting provider. Never commit a production secret or NVIDIA API key.

## Key workflows

- Patient dashboard, longitudinal timeline, record search/filtering, upload, and protected download
- Clinician referral creation for already-connected patients with validated destination,
  clinical context and priority
- Permission-scoped referral history and detail pages for patients and clinicians
- Global partial-match search for authorized patients, referrals and medical records
- Referral package selection with patient-owned records only
- Explicit, unchecked-by-default consent or rejection
- Clinician referral workspace gated by consent and permitted record IDs
- Server-validated referral status transitions
- Privacy/access log and emergency summary
- Plain-language record explanation with a safe unavailable/error state when NVIDIA is not configured

## Security and privacy boundaries

- Authorization is enforced in Django views, forms and querysets. Hiding a link is
  never treated as an access-control boundary.
- Referral creation lists only patients for whom the signed-in clinician previously
  created a referral. Being named as a destination does not grant referring-clinician
  access or access to the patient's complete record set.
- Destination clinicians receive clinical context and the selected referral package
  only after the patient explicitly approves sharing.
- Global search reuses these same ownership and consent-aware query boundaries; it is
  not a directory of all patients or records.
- State-changing forms use Django CSRF protection, templates keep automatic escaping,
  and medical downloads are served through ownership-aware views.

CareTrace is a fictional-data prototype and does not claim regulatory compliance.

## Quality checks

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

For a production-oriented configuration check:

```powershell
$env:DJANGO_DEBUG="False"
$env:DJANGO_SECRET_KEY="replace-with-a-long-random-value"
$env:DJANGO_ALLOWED_HOSTS="your-domain.example"
python manage.py check --deploy
```

## Environment variables

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required when debug mode is disabled |
| `DJANGO_DEBUG` | `True` locally; `False` in production |
| `DJANGO_DEMO_QUICK_LOGIN` | Temporary fixed-profile judge access; defaults to `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated HTTPS origins |
| `DJANGO_SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS; defaults on in production |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | Enable only when every subdomain is HTTPS-only |
| `DJANGO_SECURE_HSTS_PRELOAD` | Enable only after reviewing HSTS preload requirements |
| `DJANGO_TIME_ZONE` | Defaults to `Asia/Kolkata` |
| `DJANGO_DB_PATH` | Optional SQLite path |
| `NVIDIA_API_KEY` | Optional; enables generation of new explanations |
| `NVIDIA_MODEL` | Optional NVIDIA model override |

## Railway deployment

Create a Python service from this repository, set the production environment variables above, and use the included `Procfile`. Run migrations before serving the app:

```powershell
python manage.py migrate
python manage.py collectstatic --noinput
```

SQLite and uploaded files require persistent storage on a hosted service. Mount a Railway volume, set `DJANGO_DB_PATH` to a file on that volume, and preserve the `media` directory there. For a multi-instance production deployment, migrate the same Django models to a managed relational database and durable object storage rather than sharing SQLite.

Configure Railway's health-check path as `/health/`. That endpoint is exempt from
Django's HTTPS redirect because Railway probes it over the private HTTP network;
all user-facing routes remain HTTPS-only.

The fictional-data demonstration is deployed at
[`https://web-production-ef1db6.up.railway.app/`](https://web-production-ef1db6.up.railway.app/).
Password credentials are not stored in this repository. Temporary judge access is
controlled only by the environment flag described above.

## Project layout

- `accounts/` — role-aware profiles and authentication
- `care/` — records, referrals, consent, access logs, forms, views, and tests
- `ai_services/` — isolated NVIDIA API client
- `templates/` — reusable Django template shell and feature pages
- `static/` — CareTrace design tokens, reference styling, icons, fonts, and interaction JavaScript

Medical and identity data in this repository is synthetic and intended only for demonstration and development.

## Project documentation

- `docs/ARCHITECTURE.md` documents authorization, storage and deployment boundaries.
- `docs/agent/HANDOFF.md` records the latest verified implementation state.
- `docs/design/caretrace-ui/` preserves the original 17-screen visual source pack.
