# Project context

CareTrace is a hackathon healthcare continuity prototype, not a production-certified
medical platform. It now implements the supplied CareTrace visual workflow as a
server-rendered Django application.

The working product includes authentication, patient and clinician roles, a patient
dashboard, longitudinal timeline, medical records and protected uploads, referral
record selection, explicit patient consent, referral tracking, consent-gated clinician
access, privacy/access history, emergency profile and an optional NVIDIA/Nemotron
plain-language explanation service.

The authoritative implementation is the Django source in the repository root. The
static source-of-truth design pack remains under `docs/design/caretrace-ui/` for visual
comparison. Demo data is fictional and can be recreated with `seed_demo`.

See `docs/ARCHITECTURE.md` for boundaries, `README.md` for setup and verification,
and `docs/agent/HANDOFF.md` for the latest verified state.
