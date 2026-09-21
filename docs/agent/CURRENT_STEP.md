# Current development step

Step: Temporary Judge Demo Access
Status: COMPLETE

## Objective

Let hackathon judges enter one of two fixed fictional CareTrace profiles from the login
page without receiving or typing credentials. Preserve Django sessions, CSRF protection,
role checks and the normal credential form.

## Feature boundary

- Gate the feature behind `DJANGO_DEMO_QUICK_LOGIN`, disabled by default.
- Map only the fixed `ananya` patient and `arjun` clinician demo accounts.
- Use a POST-only, CSRF-protected Django endpoint and reject missing, inactive or
  role-mismatched accounts.
- Keep all existing authorization and medical-data access rules unchanged.
- Make rollback a single environment-variable change.
- Do not begin Language Switcher or any later roadmap feature.

## Result

The login page now presents an environment-gated selector for the fixed fictional
patient and clinician profiles. The endpoint is POST-only, CSRF-protected, validates
account activity and role, rejects unsafe return URLs and creates a normal Django
session. Password login remains available as a collapsed fallback. Desktop and mobile
browser flows for both roles passed; disabling `DJANGO_DEMO_QUICK_LOGIN` hides the UI
and returns 404 from the endpoint.
