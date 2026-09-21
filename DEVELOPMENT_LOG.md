# CareTrace development log

## Codebase audit — 2026-09-20

### Current architecture

- Django 6.1 monolith using server-rendered templates, Bootstrap 5, project CSS and
  vanilla JavaScript.
- `accounts` owns Django authentication and one-to-one `PatientProfile` role and
  identity metadata.
- `care` owns records, files, medications, appointments, referrals, consent and
  access history.
- `ai_services` isolates the optional NVIDIA/Nemotron request and safe fallback.
- SQLite is accessed through the Django ORM. Railway stores the database at
  `/app/media/db.sqlite3` on the persistent `/app/media` volume.
- Gunicorn serves Django, WhiteNoise serves collected static assets, and production
  settings are supplied through environment variables.

### Existing features

- Patient and clinician authentication with server-side role checks.
- Patient dashboard, medical timeline, record filtering and protected uploads and
  downloads.
- Referral record selection, explicit patient consent, tracking, clinician workspace
  and server-validated status transitions.
- Privacy/access history, emergency profile and optional plain-language record
  explanations through the existing NVIDIA service boundary.
- Static source-of-truth CareTrace design pack under `docs/design/caretrace-ui/`.

### Important models and relationships

- `PatientProfile`: one-to-one with Django `User`; role is `patient` or `clinician`.
- `MedicalRecord`, `Medication`, `Appointment`: foreign keys to the patient `User`.
- `Referral`: patient and assigned clinician foreign keys, selected-records
  many-to-many relationship, consent/status timestamps and provider snapshot fields.
- `AccessLog`: belongs to a referral and records consent/access/status activity.

### Important routes

- `/accounts/login/`, `/accounts/logout/`: authentication.
- `/dashboard/`, `/timeline/`, `/records/`: patient surfaces.
- `/referrals/<id>/select-records/`: existing clinician package selection.
- `/referrals/<id>/consent/`, `/referrals/<id>/tracking/`: patient referral flow.
- `/referrals/<id>/workspace/`, `/referrals/<id>/status/`: consent-gated clinician
  access and status updates.
- `/privacy/`, `/profile/emergency/`, `/health/` and `/admin/`.

### Known issues and constraints

- Referral creation/list/detail is available only through Django Admin; no product UI
  exists yet.
- The existing referral model does not distinguish the referring clinician from the
  destination clinician and has no structured speciality, clinical summary,
  diagnosis or notes fields.
- Clinician-to-patient authorization has no separate care-team/access-grant model.
  Feature work must not turn the patient selector into an all-patient directory.
- Current search is limited to patient-owned timeline/record filters; the top-bar
  search is a non-functional visual placeholder.
- Django i18n is enabled but there is no language switcher or translation catalogue.
- Railway-managed backups/PITR require a paid Pro plan and are not enabled.

### Development environment and testing method

- Windows PowerShell, Python 3.14, Django 6.1.1 and the repository `.venv`.
- Baseline on 2026-09-20: `manage.py check` passed, migration drift check passed and
  all 17 tests passed.
- Each feature uses focused Django tests, the full regression suite, Ruff lint/format,
  migration checks when applicable, production settings checks and browser validation
  of the rendered workflow.

### Planned implementation order

1. Create Referral.
2. Global Search Bar, after explicit `GO`.
3. Language Switcher, after explicit `GO`.
4. AI4Bharat integration, after explicit `GO` and official-service research.
5. Referral Search and Filtering.
6. Referral Tracking Timeline.
7. Patient Medical Timeline.
8. Medical Document Management Improvements.
9. Simple Medical Terminology Explanation.
10. Dashboard Improvements.

Only the currently approved feature may be implemented.

## Feature

Create Referral

## Objective

Give an authorized clinician a secure product workflow to create a referral for an
already-connected patient, choose relevant records and let the patient review the
request without weakening the existing consent boundary.

## Changes

- Added clinician referral creation with server-side validation and provider identity
  derived from authenticated clinician profiles.
- Added permission-scoped referral history and detail pages for patients, referring
  clinicians and destination clinicians.
- Added speciality, clinical summary, diagnosis, notes, creator and generated reference
  fields while continuing to use the existing referral status convention.
- Reused patient medications, allergies and medical records instead of copying them into
  the referral; only selected records belong to the referral package.
- Restricted the patient selector to patients already linked to the referring clinician
  by an existing referral. A submitted ID outside that queryset is rejected.
- Kept destination clinical context and selected records hidden until patient consent,
  while allowing the patient and referring clinician to prepare and review the package.
- Connected desktop and mobile referral navigation to the new history page and added
  responsive CareTrace styling and empty/error states.
- Updated the fictional demo seed so its existing referral records the referring
  clinician and the new structured context.

## Files Modified

- `care/admin.py`
- `care/forms.py`
- `care/management/commands/seed_demo.py`
- `care/migrations/0003_referral_clinical_summary_referral_created_by_and_more.py`
- `care/models.py`
- `care/tests.py`
- `care/urls.py`
- `care/views.py`
- `templates/care/referral_create.html`
- `templates/care/referral_detail.html`
- `templates/care/referral_list.html`
- `templates/components/mobile_nav.html`
- `templates/components/sidebar.html`
- `static/css/app.css`
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/agent/CURRENT_STEP.md`
- `docs/agent/DECISIONS.md`
- `docs/agent/HANDOFF.md`
- `docs/agent/ROADMAP.md`
- `DEVELOPMENT_LOG.md`

## Database Changes

Migration `care.0003` adds referral creator/context fields, constrained priority choices,
automatic reference IDs and an automatic creation timestamp. Its data migration copies
the assigned clinician into `created_by` for existing referrals so legacy referral
preparation remains authorized. No existing rows are deleted or reset.

## Tests Performed

- Baseline before implementation: Django check and migration drift check passed; 17 tests
  passed.
- `python manage.py test care`: 25 tests passed.
- `python manage.py test`: 25 tests passed.
- `python manage.py check`: passed with no issues.
- `python manage.py makemigrations --check --dry-run`: no changes detected.
- `python -m ruff check .`: passed.
- `python -m ruff format --check .`: 54 files already formatted.
- `python -m pip check`: no broken requirements.
- `python manage.py collectstatic --noinput`: passed; one changed static file collected.
- `python manage.py check --deploy` with production-style environment values: passed
  with only the intentionally disabled HSTS subdomain/preload notices.
- Fresh isolated SQLite migration and `seed_demo`: passed through `care.0003`; seeded
  referral retained its creator, speciality, status and four selected records.
- Browser verification at desktop and 390 x 844: clinician list, invalid form, successful
  create, record selection, detail, patient list/detail and consent navigation passed;
  no horizontal overflow or browser console warnings/errors.
- GitHub/Railway deployment smoke: commit `465cd80` reached `origin/main`; Railway
  returned HTTP 200 for `/health/` and the new authenticated create route returned the
  expected HTTP 302 login redirect after the deployment restart.

## Bugs Found

- Ruff identified generated migration import ordering/formatting and two long-format
  differences during the first quality pass.

## Fixes

- Applied Ruff's safe import fix and formatter to the affected Python files, then reran
  lint, format, migrations and tests successfully.

## Result

Working. Feature 1 is implemented, verified and deployed without starting any later
feature.

## Known Limitations

- There is no independent care-team or patient-access-grant model. To avoid exposing a
  global patient directory, a clinician can create a referral only for a patient with an
  existing referral relationship; an administrator must establish the first connection.
- New referrals use the existing `pending`/"Consent required" state rather than adding a
  separate draft state.
- Referral event history/timeline remains Feature 6; this feature shows the current
  persisted status only.

## Security follow-up — 2026-09-21

- Reviewed the Feature 1 referral diff and its frontend/documentation boundaries.
- Found that a destination clinician on a pending referral was included in the create
  form's patient queryset. That clinician could create a second referral, become its
  creator and reach the all-record selection view before patient consent.
- Restricted referral creation to patients for whom the signed-in clinician previously
  created a referral. Destination assignment no longer grants this capability.
- Added a regression test for the destination-clinician bootstrap path and clarified
  the create-form copy, README security boundaries, architecture and decision record.
- The focused reproduction failed before the fix with an HTTP 302 success redirect and
  passed after the fix with server-side validation rejection. The full suite now passes
  26 tests; Django checks, migration drift, Ruff and dependency checks also pass.
