# CareTrace visual direction

Research reviewed 13 September 2026. These are design references, not integrations
or claims that CareTrace has the referenced products' capabilities.

| Primary reference | Relevant pattern | CareTrace adaptation |
| --- | --- | --- |
| [NHS design principles](https://service-manual.nhs.uk/design-system/design-principles) | Inclusive, contextual services with simple, trustworthy interactions | Plain language, stable navigation, visible identity and restrained hierarchy |
| [NHS design system](https://service-manual.nhs.uk/design-system) and [accessibility guidance](https://service-manual.nhs.uk/accessibility) | Consistent components and accessibility throughout delivery | One type scale, visible field boundaries, labelled states and large mobile targets |
| [MyChart record sharing](https://www.mychart.org/l/en-us/features/share/) | Source attribution and continuity across organizations | Provider and date attached to every record; referral progress linked to access history |
| [Apple Health sharing](https://support.apple.com/en-au/guide/iphone/iph5ede58c3d/ios) | People choose shared topics and can review shared data | Explicit recipient, purpose and itemized package before an unselected consent checkbox |
| [MedlinePlus CBC](https://www.medlineplus.gov/lab-tests/complete-blood-count-cbc/) | CBC terminology and the role of clinical interpretation | Short definitions grounded in the four displayed synthetic report rows; no diagnosis or treatment |

## System established before screen assembly

- Desktop canvas 1440 × 1000 CSS pixels, sidebar 232, header 72, page inset 32.
  Main content spans 1144 pixels within the 1208-pixel application area.
- Manrope variable, bundled locally with its SIL Open Font License.
  32/22/17/15/13-pixel hierarchy; titles 700, sections 650, body 400.
- Blue #155A8A, teal #13877E, ink #17324A, warm-neutral canvas #F6F8F7.
  All palette values live in source/tokens.json and generate the UI-kit swatches.
- Darker text variants preserve contrast on semantic washes: success #216A4D,
  pending #80540E, destructive #AE3535, privacy #0F766E. Color has a text label.
- 8-pixel spacing rhythm with 4/12-pixel subdivisions; 10–14px surface corners,
  9px controls, subtle 2px/8px elevation only on working surfaces. Flat timelines
  and activity lists contrast with blue referral priority and teal privacy areas.
- One Lucide outline icon family at 1.75-pixel stroke. Icons support labels.
- Shared sidebar, header, patient strip, buttons, inputs, tabs, record rows,
  timeline nodes, referral summary, status chips, banners and audit rows.
- 390 × 844 mobile canvases, separately composed rather than shrunken desktop
  pages. Bottom navigation targets are at least 44 × 44 CSS pixels.

## Narrative and boundaries

The demo is set on 02 September 2026, so the 08 September appointment is upcoming.
Dashboard, timeline and consent depict the request before 09:20. Tracking,
receiving-clinician and audit screens depict the same referral after consent.
The records screen is a patient-owned library; the receiving workspace contains
only the four selected records. Earlier dental and dermatology items appear only
in patient history and the referring clinician's selection view.

Emergency information is shown in the patient's own session, with no implied
public or anonymous access. No invented phone number, access expiry, revocation
policy, offline guarantee, government integration or clinical finding is added.
Lab numbers are synthetic presentation content, not a real medical report.
The AI explanation is static explanatory copy, with the requested persistent
disclaimer. Product controls are visual only.

The human brief overrides decorative skill defaults: no cinematic effects,
gradients, giant headings, glass, motion, nested bezels or pill controls.

## Visual refinement · 16 September 2026

Revisited NHS design principles and MyChart sharing, and reviewed
[One Medical](https://www.onemedical.com/) for a warmer, human healthcare tone.
The resulting design uses clear information grouping, contextual source labels,
restrained category colors and explicit provider-to-provider transfer motifs.
It retains the original workflow, content hierarchy and presentation dimensions.

[Manrope source and license](https://github.com/google/fonts/tree/main/ofl/manrope)
provide a consistent local typeface without adding a package dependency. The
existing responsive rules remain in place. Mobile compositions retain 44px targets.
