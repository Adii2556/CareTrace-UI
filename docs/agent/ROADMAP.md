# Roadmap

Directional, revisable by ChatGPT/human review; never permission to implement multiple
steps. Only one step normally has READY or IN_PROGRESS status.

| Step | Scope | Status |
| --- | --- | --- |
| 1 | Django foundation | COMPLETE |
| 1.5 | Agent/repository workflow | COMPLETE |
| 2 | Authentication + account foundation | READY |
| 3 | Patient profile/domain foundation | PLANNED |
| 4 | Medical records/documents | PLANNED |
| 5 | Medical timeline | PLANNED |
| 6 | Upload/category/metadata workflow | PLANNED |
| 7 | Record viewing/search/filtering | PLANNED |
| 8 | Family-linked profiles | PLANNED |
| 9 | Referral/shareable summary workflow | PLANNED |
| 10 | AI/Nemotron service architecture | PLANNED |
| 11 | Medical information simplification | PLANNED |
| 12 | Test/medicine explanation features | PLANNED |
| 13 | Integrated CareTrace dashboard | PLANNED |
| 14 | UI/UX refinement | PLANNED |
| 15 | Security/integration/final testing | PLANNED |
| 16 | Railway deployment + demo hardening | PLANNED |

Statuses: PLANNED (direction only), READY (specified, awaiting invocation),
IN_PROGRESS (approved work underway), BLOCKED (cannot safely continue), COMPLETE
(implemented and verified). Human invocation of CURRENT_STEP is required to begin.

Step 2 READY is the requested planning state, not a claim that authentication is
absent: [existing Step 2 report](../STEP_2.md) and code predate this workflow.
Reconcile that baseline during review before invoking Step 2. Step 1.5 did not
start Step 2 implementation. See [current specification](CURRENT_STEP.md).

## Separately approved design deliverable

2026-09-13 — Static healthcare UI screen brief: **COMPLETE**. Thirteen presentation
frames and four individual mobile screenshots are in
[the design screen pack](../design/caretrace-ui/README.md). This is a visual concept,
not completion of roadmap healthcare modules or Step 14 implementation. The existing
Step 2 working-file status was preserved; no development step was advanced here.

2026-09-16 — Explicitly approved visual refinement: **COMPLETE**. Shared palette,
Manrope, semantic surfaces, referral/timeline/consent styling and all 17 exports
updated and verified. This remains static design work, not roadmap Step 14
application implementation.
