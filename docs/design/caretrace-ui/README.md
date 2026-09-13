# CareTrace static UI screen pack

High-fidelity presentation artwork for the approved SIH 2026 design brief.
All people, providers, records and events are fictional demonstration content.
The screens depict a product concept, not implemented healthcare functionality.

## Use the deliverables

- Open [the visual gallery](index.html) to browse every screen at full resolution.
- Download [the PNG screen pack](CareTrace-UI-Screens.zip) for slides and documentation.
- View [the contact sheet](contact-sheet.png) for the complete visual sequence.
- Read [research and design decisions](RESEARCH.md) for sources and conventions.

PNG exports use 2× resolution. Desktop layouts are 1440 × 1000, exported at
2880 × 2000. The mobile presentation frame is 3840 × 2400, the journey frame
3840 × 2160, and individual mobile screens 780 × 1688.

| Frame | Deliverable |
| --- | --- |
| 01 | [Design System / UI Kit](screens/01-design-system.png) |
| 02 | [Patient Dashboard](screens/02-patient-dashboard.png) |
| 03 | [Medical Timeline](screens/03-medical-timeline.png) |
| 04 | [Medical Records](screens/04-medical-records.png) |
| 05 | [Select Records for Referral](screens/05-select-records.png) |
| 06 | [Patient Consent](screens/06-patient-consent.png) |
| 07 | [Referral Tracking](screens/07-referral-tracking.png) |
| 08 | [Receiving Doctor Workspace](screens/08-doctor-workspace.png) |
| 09 | [AI Record Explainer](screens/09-ai-record-explainer.png) |
| 10 | [Emergency Profile](screens/10-emergency-profile.png) |
| 11 | [Privacy & Access](screens/11-privacy-access.png) |
| 12 | [Mobile Experience](screens/12-mobile-experience.png) |
| 13 | [CareTrace Journey Overview](screens/13-journey-overview.png) |

The screen pack also includes separate mobile dashboard, timeline, consent and
referral-status PNGs. The demo date is 02 September 2026: early screens show a
pending request; tracking, doctor and audit views show the same referral after
09:20 consent. The 08 September appointment is therefore upcoming.

## Rendering source

`source/build.cjs` composes static HTML from shared components and fictional data;
`source/styles.css` defines the visual system; `source/icons.json` contains the
Lucide subset with its adjacent license. `pages/` contains the generated markup.
These files exist only to render deterministic screenshots. They are independent
of Django, have no backend or database, and do not implement the pictured controls.

Use the existing host's Node and Playwright installations; no project dependency
or service is required. On the current rendering host, from the repository root:

```powershell
$env:NODE_PATH = 'C:\Users\adity\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
node docs/design/caretrace-ui/source/build.cjs
node docs/design/caretrace-ui/source/render.cjs
```

The renderer opens local files in headless Microsoft Edge. Segoe UI must be
available for identical typography. The PNGs are portable and need no fonts or
runtime. Open `index.html` directly to inspect the exported artwork.

## Verification

All 17 rendered outputs were inspected and checked for viewport overflow,
footer/navigation overlap and browser errors. Mobile action targets were checked
against 44 × 44 CSS pixels. [Render results](verification.json) record the outcome.
[Content and contrast review](quality-review.json) records package/consent checks
and eight text/background pairings; the lowest checked ratio is 5.15:1.

Existing repository verification passed: pip check, Ruff lint and format,
Django system check, migration drift check and all 20 Django tests. This is a
static design review, not user testing, clinical validation or accessibility
certification of an implemented application.
