# Latest handoff

## Step

Shared authenticated application shell and HTMX navigation.

## Status

COMPLETE — implemented and verified on 2026-09-22.

## Completed

Added `base_app.html` as the shared authenticated shell, extracted footer/loading/page
header components and updated all authenticated feature templates to use the shell.
Primary GET navigation and global search now replace only `#app-content`, push normal
URLs and show a restrained loading bar. Shared JavaScript reinitializes page controls
and synchronizes active navigation after swaps and browser history restoration.

Standardized shell sizing with shared CSS variables, stable scrollbar gutters and
responsive overflow fixes. HTMX history snapshots are disabled to prevent medical page
content from being stored in browser `localStorage`.

## Files

Authenticated templates and shell components, `static/css/app.css`,
`static/js/app.js`, `care/tests.py`, README, architecture, decision, roadmap,
current-step, handoff and development-log documentation.

## Decisions

Use HTMX only as progressive enhancement for authenticated GET navigation. Keep every
response as a complete Django page and leave all state-changing forms on their existing
CSRF-protected full-request paths. Keep `base.html` as a compatibility alias.

## Verification

- Three focused shared-shell/HTMX tests passed; the full 44-test suite passed.
- Django checks and migration drift checks passed; no migration was created.
- Ruff lint/format, JavaScript syntax and whitespace checks passed.
- Desktop/tablet and 390 x 844 browser flows passed across Dashboard, Referrals,
  Records and Timeline. URLs, titles, active navigation, Back/Forward, the record modal,
  one-time asset loading and zero document overflow were verified.
- A clean browser run reported no warnings or errors.

## Issues

Rendered QA found and fixed tablet referral-action overflow, mobile timeline/filter
overflow, and stale active navigation after browser history restoration. The feature
adds one pinned CDN dependency; full-page navigation remains the fallback if it is
unavailable.

## Next

Language Switcher remains the next approval-gated product feature. It was not started.
