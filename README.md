# CareTrace

CareTrace will organize longitudinal patient medical information and support
continuity between healthcare providers. This checkout contains the Django
foundation plus Step 2 authentication, basic account editing, and a protected
application shell. There are no healthcare features or user roles.

Stack: Python 3.14, Django 6.1.1, Django Templates, Bootstrap 5.3.8, Vanilla
JavaScript, SQLite, Django ORM/authentication/media, WhiteNoise, and Gunicorn for
future Linux hosting. NVIDIA Nemotron and Railway integration are deferred.

## Local setup (PowerShell)

Prerequisites: Python 3.14 and Git. Run from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements/development.txt
Copy-Item .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the generated value into `DJANGO_SECRET_KEY` in `.env`, inside single
quotes. The example placeholder is intentionally rejected. Never share or commit
the resulting `.env`. If activation is restricted, use `.\.venv\Scripts\python`
instead of `python` in subsequent commands; changing execution policy is not needed.

```powershell
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/health/.
If the port belongs to another project, use `python manage.py runserver 8001`.
Bootstrap is vendored locally, so pages need no CDN connection at runtime.
Optional: `python manage.py createsuperuser` enables standard `/admin/` access.
No administrator or demo accounts are created automatically.

## Accounts and application access

Select Register from the home page to create an account with a unique username
and a Django-validated password. Registration signs you in and opens `/app/`.
Log in with your username (not email). Name and email fields are optional; email
is contact information only, is not unique or verified, and cannot reset passwords.

`/accounts/profile/` lets you edit your own first name, last name, and email.
Username, password, and privilege fields cannot be edited there. Account data is
login identity, not a medical profile. Log out uses a CSRF-protected POST button.
Anonymous access to the app or account redirects to login and preserves a safe
local destination. Password change/reset and email verification are deferred.

Setup is unchanged from Step 1: no new dependencies or migrations are needed.
See [Step 2 verification](docs/STEP_2.md) for the tested scope and limits.

On Linux/macOS use `python3 -m venv .venv` and `source .venv/bin/activate`,
then the same Python commands. Copy the example with `cp .env.example .env`.

## AI-Assisted Development Workflow

CareTrace uses controlled, step-based development with repository Markdown + Git
as shared context. ChatGPT plans/reviews, Codex implements, and the human approves.

1. Review [latest handoff](docs/agent/HANDOFF.md).
2. Define/review [current step](docs/agent/CURRENT_STEP.md), using the
   [template](docs/agent/STEP_TEMPLATE.md), and obtain human approval.
3. Explicitly ask Codex to implement CURRENT_STEP, following [AGENTS.md](AGENTS.md).
4. Codex runs the required verification.
5. Codex updates HANDOFF and the implemented step's status, commits and pushes
   the verified step to [CareTrace-UI](https://github.com/Adii2556/CareTrace-UI),
   verifies synchronization, then stops (see AGENTS.md).
6. Ask ChatGPT to review the repository implementation and handoff before defining
   and approving the next step. Share a committed/pushed revision or repository
   files the reviewer can actually access; local edits are not automatically synced.

READY → IN_PROGRESS → COMPLETE; use BLOCKED with a factual handoff and stop if a
major issue prevents safe progress. Resolve minor choices using existing conventions.
Only CURRENT_STEP plus explicit invocation authorizes work; a roadmap is not approval.
For this workflow initialization, Step 1.5 is complete and Step 2 remains READY.
Existing Step 2 code predates this task; review the baseline note in CURRENT_STEP.

Standard future Codex instruction:

```text
Implement docs/agent/CURRENT_STEP.md.

Follow AGENTS.md and all referenced repository rules.
Implement only the approved current step.
Run all required verification.
Update docs/agent/HANDOFF.md when complete.
Mark the current step COMPLETE.
Do not start the next roadmap step.
Stop after the handoff.
```

## Verification

```powershell
python -m pip check
python -m ruff check .
python -m ruff format --check .
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Use `python -m ruff format .` when formatting changes. Tests use Django's isolated
test database, not the runtime SQLite database. GitHub Actions runs the same
checks on Linux plus fresh migrations and production static/server checks.

## Configuration and production readiness

`.env` supplies local configuration; existing process variables take precedence.
`DJANGO_DEBUG` accepts true/false/1/0. Hosts and trusted origins are comma-separated.
Timezone defaults to Asia/Kolkata. Optional `DJANGO_DATABASE_PATH` and
`DJANGO_MEDIA_ROOT` override local storage locations; parent directories must exist.

To validate production locally, set the following process variables in a new
PowerShell terminal using the same virtual environment:

```powershell
$env:DJANGO_DEBUG = 'False'
$env:DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1'
python manage.py check --deploy --fail-level WARNING --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
```

Use a generated secret of at least 50 characters. Production always disables
debug, requires explicit hosts, and enables HTTPS redirects and secure cookies.
Set `DJANGO_SETTINGS_MODULE=config.settings.production` in the hosting environment.
`DJANGO_TRUST_PROXY=True` is reserved for a verified trusted HTTPS proxy.
Do not enable it blindly. CSRF trusted origins, when needed, must include scheme.

Future Linux start command after installing `requirements/production.txt`:
`gunicorn config.wsgi:application`. Gunicorn is not the Windows local server.
Deployment must provide persistent SQLite/media storage, HTTPS/proxy verification,
and backup policy. This step does not deploy or provide public medical-file access.

## Structure

`config/` configuration; `apps/` core and minimal accounts; `templates/` shared
markup; `static/` source assets; `media/` ignored uploads; `tests/` Django tests;
`requirements/` dependency sets; `.github/` CI; `docs/` persistent development rules.

Read [architecture](docs/ARCHITECTURE.md) and
[development rules](docs/DEVELOPMENT_RULES.md) before future changes.
