# Current development step

Step: Shared authenticated application shell and HTMX navigation
Status: COMPLETE

## Objective

Make authenticated CareTrace pages feel like one stable application by consolidating
their shell and progressively enhancing primary GET navigation with HTMX. Preserve all
normal Django URLs, security controls, forms and non-JavaScript behavior.

## Feature boundary

- Introduce `base_app.html` as the authenticated shell and keep `base.html` as a
  compatibility alias.
- Keep sidebar, topbar, footer and global assets outside the replaceable main region.
- Enhance only internal GET navigation/search with HTMX and `hx-push-url`.
- Keep state-changing forms as normal CSRF-protected Django submissions.
- Reinitialize page-local vanilla JavaScript after HTMX swaps.
- Standardize shell dimensions and responsive overflow behavior without redesigning
  the established CareTrace visual language.
- Verify Dashboard, Referrals, Records and Timeline navigation at desktop and mobile
  widths, including browser history and no shell replacement.
- Do not begin Language Switcher or any later roadmap feature.

## Result

Authenticated pages now use `base_app.html`, with the sidebar, topbar, footer and
global assets outside a single replaceable `#app-content` region. Primary GET
navigation and global search use pinned HTMX progressive enhancement with pushed URLs;
all normal responses and state-changing forms retain standard Django behavior. The
shell has stable responsive dimensions, a restrained loading indicator and no
document-level overflow on the verified Dashboard, Referrals, Records and Timeline
flows. HTMX history snapshots are embargoed from `localStorage`; Back and Forward
restore content through authenticated server requests. Automated and rendered browser
verification passed.
