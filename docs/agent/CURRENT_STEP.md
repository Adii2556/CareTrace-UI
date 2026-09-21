# Current development step

Step: Feature 2 — Global Search Bar
Status: COMPLETE

## Objective

Replace the decorative top-bar search placeholder with a real permission-aware Django
ORM search for existing CareTrace patients, referrals and medical records. Results must
be grouped, useful on empty/no-match states, linked to authorized product pages and
responsive without exposing data outside the signed-in user's existing access.

## Existing verified scope

- Feature 1 Create Referral is complete, deployed and security-reviewed.
- Patient record ownership, referral creator/destination separation and explicit
  consent boundaries are enforced server-side.
- The shared top bar currently contains a decorative search placeholder and the `/`
  keyboard shortcut already focuses a real search input when one exists.

## Feature boundary

Implement only Global Search Bar. Use simple Django ORM queries and existing entities.
Do not add a search service, autocomplete API, language switching, AI4Bharat, referral
filters or later roadmap features. Stop after verified completion and wait for explicit
`GO`.

## Result

The shared top bar now submits to a grouped search page using permission-aware ORM
queries. Patient, referral and medical-record matches are partial and case-insensitive;
empty/no-result states, the existing `/` shortcut and responsive layouts are verified.
No model, migration, dependency or environment-variable change was required.

Follow-up: the `/` keyboard badge now has explicit CareTrace foreground/background
styles and remains visible at the mobile breakpoint instead of inheriting Bootstrap's
white key text and the static reference pack's mobile hiding rule.
