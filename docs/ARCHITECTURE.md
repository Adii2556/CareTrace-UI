# Architecture — Step 2

CareTrace is a Django monolith with authentication and a protected empty app shell.
No healthcare functionality exists.

Browser → Django Templates / Bootstrap / Vanilla JS → Django views and future
forms/domain logic → Django ORM → SQLite.

## Responsibilities

- `config/`: settings, root routing, WSGI and ASGI entry points.
- `apps/core/`: public placeholder home, GET/HEAD liveness, and protected app shell.
- `apps/accounts/`: minimal `AbstractUser`, Django admin registration, registration
  form/view, native login/logout integration, and basic account editing. No roles
  or medical profiles. Its templates live under root `templates/accounts/`.
- `templates/`: shared base, reusable page layout, components, partials, errors.
- `static/`: source assets, including pinned Bootstrap 5.3.8 and its MIT license.
- `media/`: ignored local development uploads; no upload feature exists.
- `tests/`: built-in Django tests. No pytest dependency.
- `requirements/`: pinned shared, development, and production dependencies.
- `.github/`: verification only; no deployment pipeline.

## Decisions

The user model is established before the first migration because changing
AUTH_USER_MODEL after creating dependent tables is disruptive. `accounts` is
the sole additional foundation app; its User adds no fields or business logic.
Future relations must reference settings.AUTH_USER_MODEL or get_user_model().

## Authentication and routes

| Route | Access | Responsibility |
| --- | --- | --- |
| `/` | Public | Placeholder home and state-aware navigation |
| `/health/` | Public | Liveness only |
| `/accounts/register/` | Public | Django UserCreationForm; signs in after creation |
| `/accounts/login/` | Public | Django LoginView and AuthenticationForm |
| `/accounts/logout/` | POST with CSRF | Django LogoutView; redirects home |
| `/accounts/profile/` | Authenticated | View/edit current user's basic account fields |
| `/app/` | Authenticated | Welcome placeholder; no medical modules |
| `/admin/` | Django staff permissions | Existing standard Django administration |

Username remains the login identifier. Django handles unique username/password
validation and password hashing. Name/email are optional; email is neither unique
nor verified and is not a login or recovery identifier. No schema change was needed.
Authenticated visitors to registration/login return to the app. Registration uses
a fixed app redirect; native LoginView validates `next` destinations against the
request host and scheme. Logout is POST-only and terminates the session.

`login_required` protects app/account views. AccountForm explicitly permits only
first_name, last_name, and email, and is always bound to request.user. Submitted
IDs, usernames, passwords, and privilege flags cannot change that selection.
Protected responses use `never_cache`; server-side guards remain authoritative.
CSRF middleware and Django password validators remain enabled. Registration marks
password POST parameters sensitive for Django exception reporting. No view logs
credentials or submitted account data.

Shared form markup supplies labels, help, errors, and Django-generated accessible
input attributes. BootstrapFormMixin handles styling only. Templates remain
autoescaped. Navigation offers only routes that exist. No extra packages added.

Password change/reset, email verification, and login throttling are not part of
this step; review abuse protections before exposing registration publicly.

Base settings own shared configuration; development enables configurable debug;
production forbids debug and requires explicit hosts and a strong secret.
Local .env is read without overriding process variables. Set the settings module
in the process environment or use --settings; it is not selected through .env.
Management commands default to development; WSGI/ASGI default to production.

Production enables secure cookies, HTTPS redirect, a short HSTS policy, and
WhiteNoise compressed manifest storage. The proxy trust switch defaults off.
Only security.W005/W021 are silenced: HSTS subdomain coverage and browser preload
require review of the eventual domain. All other deployment checks stay active.
Confirm hosting proxy behavior before enabling it during deployment. SQLite and
media paths are configurable for a future persistent volume. No Railway service
or deployment infrastructure exists yet. Gunicorn is for Linux hosting; Windows
development uses runserver.

Development media routing is a temporary generic upload convenience. Before
medical uploads are implemented, replace public media serving with authorized
download views in all environments. WhiteNoise serves static assets only.

The health endpoint is liveness, not database readiness. The independent 500
template deliberately avoids static storage and context dependencies so it can
render when normal page rendering fails.

## Future boundaries (not implemented)

Create apps only for approved coherent domains. Add services, query helpers,
forms, or validators when real complexity justifies them, not as empty layers.
External integrations will use server-side adapters owned by the relevant app.
No Nemotron, medical, hospital, referral, role, or healthcare API logic exists.

## References

- Django custom users: https://docs.djangoproject.com/en/6.0/topics/auth/customizing/
- WhiteNoise: https://whitenoise.readthedocs.io/en/stable/django.html
- Bootstrap source: https://github.com/twbs/bootstrap/tree/v5.3.8
