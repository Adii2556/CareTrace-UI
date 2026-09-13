# CareTrace — Master Development Control Checklist

Use this checklist throughout development.

A step is not considered complete until all applicable items are checked.

---

# A. Workflow Control

## Before starting a step

- [ ] `AGENTS.md` exists and is current
- [ ] `docs/agent/PROJECT_CONTEXT.md` is current
- [ ] `docs/agent/ROADMAP.md` is current
- [ ] `docs/agent/DECISIONS.md` reflects major decisions
- [ ] `docs/agent/HANDOFF.md` reflects the last completed step
- [ ] `docs/agent/CURRENT_STEP.md` contains exactly one approved development step
- [ ] Current step status is `READY`
- [ ] Scope is clearly defined
- [ ] Out-of-scope items are explicitly defined
- [ ] Completion criteria are defined
- [ ] Required tests are defined
- [ ] No next-step functionality is mixed into the current task
- [ ] Human approval has been given before Codex starts

## During implementation

- [ ] Codex changes status to `IN_PROGRESS`
- [ ] Codex modifies only relevant areas
- [ ] Existing architecture is reused
- [ ] Existing working code is not rewritten unnecessarily
- [ ] No speculative features are added
- [ ] No major dependency is added without justification
- [ ] No agreed technology is replaced
- [ ] No secrets are committed
- [ ] New architecture decisions are recorded
- [ ] Blockers are documented instead of guessed around
- [ ] Codex does not start another roadmap step

## After implementation

- [ ] Current step requirements are fully implemented
- [ ] All required tests pass
- [ ] Previous tests still pass
- [ ] Django checks pass
- [ ] Ruff passes
- [ ] Migrations are valid
- [ ] Relevant browser flow was manually tested
- [ ] Documentation matches implementation
- [ ] `HANDOFF.md` is updated
- [ ] `CURRENT_STEP.md` is marked `COMPLETE`
- [ ] `ROADMAP.md` is updated
- [ ] Codex stops
- [ ] ChatGPT reviews before the next step is approved

---

# B. Locked Technology Stack

These should remain unchanged unless explicitly approved.

- [x] Python
- [x] Django
- [x] Django Templates
- [x] Bootstrap 5
- [x] Vanilla JavaScript
- [x] SQLite for hackathon MVP
- [x] Django ORM
- [x] Django Authentication
- [x] Django Media Storage initially
- [x] NVIDIA Nemotron for later AI functionality
- [x] Git + GitHub
- [x] Ruff
- [x] GitHub Actions CI
- [x] Gunicorn
- [x] WhiteNoise
- [x] Railway planned for deployment
- [x] Environment variables for secrets

Do not introduce without approval:

- [ ] React
- [ ] Vue
- [ ] Angular
- [ ] Node.js backend
- [ ] Django REST Framework
- [ ] Redis
- [ ] Celery
- [ ] Docker
- [ ] MongoDB
- [ ] Microservices
- [ ] Kubernetes
- [ ] PostgreSQL before an approved migration step

---

# C. Development Roadmap

## Step 1 — Project Foundation

- [x] Django project created
- [x] Settings architecture
- [x] Environment variables
- [x] Dependency management
- [x] Custom user foundation
- [x] Template architecture
- [x] Static architecture
- [x] Media configuration
- [x] Ruff configuration
- [x] Test foundation
- [x] Git configuration
- [x] GitHub Actions CI
- [x] Architecture documentation
- [x] Development rules
- [x] README
- [x] Local verification

Status: **COMPLETE**

---

# D. Step 1.5 — Agent / Repository Workflow

- [ ] Root `AGENTS.md`
- [ ] `docs/agent/PROJECT_CONTEXT.md`
- [ ] `docs/agent/ROADMAP.md`
- [ ] `docs/agent/CURRENT_STEP.md`
- [ ] `docs/agent/HANDOFF.md`
- [ ] `docs/agent/DECISIONS.md`
- [ ] `docs/agent/STEP_TEMPLATE.md`
- [ ] AI-assisted workflow documented in README
- [ ] Human approval boundary documented
- [ ] Codex completion protocol documented
- [ ] Existing tests still pass
- [ ] No application behavior changed

Status: **CURRENT**

---

# E. Step 2 — Authentication & Account

## Module

`apps/accounts/`

## Features

- [ ] User registration
- [ ] Login
- [ ] Logout
- [ ] Protected application shell
- [ ] Account/profile page
- [ ] Edit basic account data
- [ ] Authentication-aware navbar
- [ ] Django messages
- [ ] Password validation
- [ ] Proper redirects

## Architecture rules

- [ ] Account user remains separate from patient medical profile
- [ ] No healthcare fields added to user
- [ ] No roles yet unless explicitly approved
- [ ] Django authentication reused
- [ ] No custom authentication engine

## Tests

- [ ] Registration page loads
- [ ] Valid registration works
- [ ] Invalid registration rejected
- [ ] Duplicate identity handled
- [ ] Password stored hashed
- [ ] Valid login works
- [ ] Invalid login rejected
- [ ] Logout terminates session
- [ ] Protected route rejects anonymous user
- [ ] Protected route allows authenticated user
- [ ] Profile visible only appropriately
- [ ] Step 1 regression tests pass

---

# F. Step 3 — Patient Profile Domain

## Module

`apps/patients/`

## Features

- [ ] Patient profile model
- [ ] Link patient profile to account
- [ ] Basic demographics
- [ ] Date of birth
- [ ] Gender/sex field only if required by project design
- [ ] Contact data where appropriate
- [ ] Emergency contact if approved
- [ ] Profile creation
- [ ] Profile editing
- [ ] Profile display

## Explicit separation

- [ ] User authentication data remains separate
- [ ] Medical records are not stored directly on patient model
- [ ] No AI logic
- [ ] No referral logic

## Tests

- [ ] Patient profile creation
- [ ] Ownership enforcement
- [ ] Editing
- [ ] Invalid data rejection
- [ ] Anonymous access blocked
- [ ] Cross-user access blocked
- [ ] Model constraints
- [ ] Existing authentication tests pass

---

# G. Step 4 — Medical Records Domain

## Module

`apps/records/`

## Core models

- [ ] MedicalRecord
- [ ] Record type/category
- [ ] Record date
- [ ] Healthcare provider/source
- [ ] Description/title
- [ ] Patient relation
- [ ] Created/updated timestamps

Potential categories:

- [ ] Prescription
- [ ] Laboratory report
- [ ] Imaging report
- [ ] Discharge summary
- [ ] Consultation
- [ ] Procedure
- [ ] Bill
- [ ] Vaccination
- [ ] Other

## Tests

- [ ] Record creation
- [ ] Record ownership
- [ ] Patient relationship
- [ ] Valid categories
- [ ] Required metadata validation
- [ ] Unauthorized access blocked
- [ ] Delete/update permissions
- [ ] Regression tests

---

# H. Step 5 — Medical Document Upload

## Features

- [ ] Upload documents
- [ ] Supported file types defined
- [ ] File-size limit defined
- [ ] Safe file handling
- [ ] Media storage integration
- [ ] Document linked to MedicalRecord
- [ ] Download/view capability
- [ ] Original filename preserved safely if needed
- [ ] Metadata stored separately

## Security

- [ ] MIME/file extension validation
- [ ] File-size validation
- [ ] Path traversal impossible
- [ ] User cannot access another patient's files
- [ ] Executable uploads rejected
- [ ] Secrets never embedded in file URLs

## Tests

- [ ] Valid upload
- [ ] Invalid type rejected
- [ ] Oversized file rejected
- [ ] Ownership enforced
- [ ] Missing file handled
- [ ] Delete behavior verified

---

# I. Step 6 — Longitudinal Medical Timeline

## Module

May live under patients/records or dedicated `timeline/` only if justified.

## Features

- [ ] Records displayed chronologically
- [ ] Date sorting
- [ ] Category display
- [ ] Record summary
- [ ] Timeline detail view
- [ ] Empty-state UI
- [ ] Pagination if needed

## Tests

- [ ] Correct chronological ordering
- [ ] Records belong to correct patient
- [ ] No cross-user leakage
- [ ] Empty timeline handled
- [ ] Invalid dates handled

---

# J. Step 7 — Search, Filter & Organization

## Features

- [ ] Search by title/description
- [ ] Filter by record type
- [ ] Filter by date range
- [ ] Sort newest/oldest
- [ ] Clear filters
- [ ] Useful no-results state

## Tests

- [ ] Search results correct
- [ ] Category filtering correct
- [ ] Date filtering correct
- [ ] Combined filters work
- [ ] Other users' data never appears
- [ ] Invalid query parameters handled

---

# K. Step 8 — Family / Linked Profiles

Only implement after the data model is deliberately approved.

## Features

- [ ] Family member profile concept defined
- [ ] Relationship type
- [ ] Ownership/permission model
- [ ] Profile switcher
- [ ] Separate timelines
- [ ] Family health context without merging records

## Tests

- [ ] User can access authorized linked profile
- [ ] Unauthorized access blocked
- [ ] Data remains separated
- [ ] Relationship validation
- [ ] Profile switching correct

---

# L. Step 9 — Referral Workflow

## Features

- [ ] Referral model
- [ ] Origin/provider information
- [ ] Destination information
- [ ] Referral reason
- [ ] Relevant-record selection
- [ ] Generated medical summary
- [ ] Shareable referral package
- [ ] Appropriate expiry/access controls if sharing externally

## Tests

- [ ] Referral creation
- [ ] Correct patient relation
- [ ] Selected records only
- [ ] Unauthorized records excluded
- [ ] Summary generation deterministic where non-AI
- [ ] Share/access permissions
- [ ] Referral status handling

---

# M. Step 10 — AI Service Architecture

## Module

Prefer isolated service layer such as:

`services/ai/`

or equivalent project convention.

## Features

- [ ] Nemotron client abstraction
- [ ] API key from environment
- [ ] Timeout handling
- [ ] Error handling
- [ ] Retry policy if appropriate
- [ ] Response validation
- [ ] Logging without medical-content leakage
- [ ] Mockable interface for tests

## Rules

- [ ] AI logic not embedded directly in views
- [ ] API key never exposed frontend-side
- [ ] AI responses clearly treated as generated explanations
- [ ] No diagnosis claims added
- [ ] No unsupported treatment recommendation workflow

## Tests

- [ ] API client mocked
- [ ] Successful response handling
- [ ] API failure
- [ ] Timeout
- [ ] Invalid response
- [ ] Missing API key
- [ ] No real paid API calls in normal test suite

---

# N. Step 11 — Medical Terminology Simplification

## Features

- [ ] User selects record/text
- [ ] Text sent through AI service
- [ ] Plain-language explanation returned
- [ ] Original text preserved
- [ ] AI explanation visually distinguished
- [ ] Appropriate disclaimer/context
- [ ] Failure state

## Tests

- [ ] Correct service call
- [ ] Correct user ownership
- [ ] Empty content blocked
- [ ] Service failures handled
- [ ] Generated content stored only if explicitly intended
- [ ] Other users cannot trigger explanation on inaccessible records

---

# O. Step 12 — Test / Medicine Explanation

## Features

- [ ] Explain why a test may have been recommended
- [ ] Explain medication purpose from provided context
- [ ] Plain-language output
- [ ] Context preservation
- [ ] No fabricated certainty
- [ ] Clear distinction between explanation and medical advice

## Tests

- [ ] Input validation
- [ ] AI integration mocked
- [ ] Failure handling
- [ ] Authorization
- [ ] Output rendering
- [ ] No unsafe assumptions from missing context

---

# P. Step 13 — Main Dashboard

Build only after core functionality exists.

## Features

- [ ] Patient overview
- [ ] Recent records
- [ ] Timeline shortcut
- [ ] Upload shortcut
- [ ] Referral shortcut
- [ ] AI explanation shortcut
- [ ] Family profile switch where implemented
- [ ] Clear navigation

## Rules

- [ ] No fake analytics
- [ ] No invented health scores
- [ ] No meaningless charts
- [ ] Every dashboard element links to working functionality

## Tests

- [ ] Correct user data
- [ ] Empty-state behavior
- [ ] No cross-user data
- [ ] Navigation works
- [ ] Responsive rendering sanity check

---

# Q. Step 14 — UI / UX Polish

## Global

- [ ] Consistent typography
- [ ] Consistent spacing
- [ ] Consistent cards
- [ ] Consistent forms
- [ ] Consistent buttons
- [ ] Consistent alerts
- [ ] Responsive layout
- [ ] Mobile navigation
- [ ] Accessible labels
- [ ] Keyboard accessibility where practical
- [ ] Focus states
- [ ] Empty states
- [ ] Loading states where required
- [ ] Error states
- [ ] Confirmation for destructive actions

## CareTrace experience

- [ ] Medical timeline easy to scan
- [ ] Record types visually distinguishable
- [ ] Upload workflow understandable
- [ ] AI explanations clearly separate from source records
- [ ] Referral flow understandable within seconds
- [ ] No unnecessary text-heavy screens

---

# R. Step 15 — Security & Hardening

## Authentication

- [ ] All private routes protected
- [ ] Ownership checks everywhere
- [ ] Session behavior verified
- [ ] Password validation active
- [ ] CSRF enabled

## Input

- [ ] Server-side validation
- [ ] File validation
- [ ] Query parameter validation
- [ ] Form validation
- [ ] Safe redirects

## Data

- [ ] No medical information exposed publicly
- [ ] No patient identifiers in unsafe logs
- [ ] No secrets in Git
- [ ] No secrets exposed to browser
- [ ] Environment configuration verified

## Django

- [ ] `DEBUG=False` behavior tested
- [ ] Allowed hosts configured
- [ ] Secure production settings reviewed
- [ ] Static handling verified
- [ ] Error pages do not expose internals

---

# S. Step 16 — Deployment & Demo Hardening

## Railway

- [ ] Production dependencies complete
- [ ] Gunicorn works
- [ ] WhiteNoise works
- [ ] Environment variables configured
- [ ] `DEBUG=False`
- [ ] Allowed hosts correct
- [ ] Static files collected
- [ ] Migrations execute
- [ ] App starts successfully
- [ ] Health route if required

## Live verification

- [ ] Registration
- [ ] Login
- [ ] Patient profile
- [ ] Record creation
- [ ] Document upload
- [ ] Timeline
- [ ] Search/filter
- [ ] AI explanation
- [ ] Referral flow
- [ ] Logout

---

# T. Test Pyramid

Every feature should be evaluated against these layers.

## Model tests

- [ ] Constraints
- [ ] Relationships
- [ ] Defaults
- [ ] Validation
- [ ] Ownership

## Form tests

- [ ] Valid input
- [ ] Invalid input
- [ ] Required fields
- [ ] Edge cases

## View tests

- [ ] Authentication
- [ ] Authorization
- [ ] Correct HTTP status
- [ ] Redirect behavior
- [ ] Correct template
- [ ] Correct context

## Service tests

- [ ] Successful behavior
- [ ] Failure behavior
- [ ] External services mocked
- [ ] Invalid responses handled

## Integration tests

- [ ] Multi-model behavior
- [ ] Complete feature workflows
- [ ] Permissions across modules

## Regression tests

- [ ] Previously completed features remain functional

## Manual smoke tests

- [ ] Critical browser flow works
- [ ] No visible template errors
- [ ] Static assets load
- [ ] Mobile/basic responsive behavior works

---

# U. Mandatory Per-Step Quality Gate

No step can become `COMPLETE` unless:

- [ ] Feature behaves correctly
- [ ] Scope matches `CURRENT_STEP.md`
- [ ] No next-step work was added
- [ ] Tests were added where meaningful
- [ ] Full existing test suite passes
- [ ] `python manage.py check` passes
- [ ] Ruff passes
- [ ] Migration state is clean
- [ ] Relevant browser flow verified
- [ ] No secrets committed
- [ ] Documentation updated where required
- [ ] `HANDOFF.md` updated
- [ ] Significant decisions logged
- [ ] Current step marked COMPLETE
- [ ] Codex stops

---

# V. ChatGPT Review Gate

Before approving the next Codex step, ChatGPT should review:

- [ ] `HANDOFF.md`
- [ ] `CURRENT_STEP.md`
- [ ] Git diff / changed files
- [ ] New migrations
- [ ] New dependencies
- [ ] Test results
- [ ] New models
- [ ] Authentication/authorization changes
- [ ] Architectural changes
- [ ] `DECISIONS.md`
- [ ] Roadmap status
- [ ] Any unresolved issue

Then determine:

- [ ] Implementation matches specification
- [ ] No scope creep occurred
- [ ] Architecture remains coherent
- [ ] No security regression is apparent
- [ ] No unnecessary dependency was introduced
- [ ] No healthcare data was placed in the wrong domain
- [ ] Current step is genuinely complete
- [ ] Next step is safe to begin

Only then should the next `CURRENT_STEP.md` become `READY`.

---

# W. Dependency Control

Before accepting any new package:

- [ ] Is it actually required?
- [ ] Can Django/Python already do it?
- [ ] Is it maintained?
- [ ] Is it appropriate for the hackathon?
- [ ] Does it create deployment complexity?
- [ ] Does it introduce security concerns?
- [ ] Is it documented in `requirements/`?
- [ ] Is the reason recorded if architecturally significant?

If the answer to “Is it actually required?” is no:

**Do not add it.**

---

# X. Database Change Control

Before any model change:

- [ ] Domain ownership is clear
- [ ] Field actually belongs on this model
- [ ] Relationship type is correct
- [ ] Null/blank behavior is deliberate
- [ ] Index/uniqueness requirements considered
- [ ] Migration generated
- [ ] Migration inspected
- [ ] Migration tested
- [ ] Existing records remain compatible
- [ ] No medical fields are added to authentication user simply for convenience

---

# Y. AI Change Control

Before adding any AI feature:

- [ ] Non-AI feature flow already works
- [ ] Exact AI input defined
- [ ] Exact expected output defined
- [ ] AI failure behavior defined
- [ ] Sensitive data exposure considered
- [ ] API cost considered
- [ ] Timeout behavior defined
- [ ] Prompt stored centrally
- [ ] Output is clearly identified as AI-generated
- [ ] Tests use mocks
- [ ] AI is enhancing—not replacing—core deterministic functionality

---

# Z. Hackathon Completion Definition

CareTrace MVP is considered demo-ready when this complete journey works reliably:

- [ ] User registers
- [ ] User logs in
- [ ] User creates patient profile
- [ ] User uploads medical record/document
- [ ] Record is organized correctly
- [ ] Record appears on longitudinal timeline
- [ ] Records can be searched/filtered
- [ ] User can open record details
- [ ] AI can explain supported medical content simply
- [ ] Relevant records can be assembled for referral
- [ ] Referral/medical summary can be demonstrated
- [ ] Family-linked profile capability works if retained in MVP
- [ ] Main dashboard ties features together
- [ ] UI looks coherent and professional
- [ ] Critical flows work on deployed version
- [ ] No known critical security/access-control flaw
- [ ] Demo data is prepared
- [ ] Demo sequence has been rehearsed
- [ ] Recovery path exists if AI/API fails during presentation

---

# Final Control Rule

The development loop must always remain:

```text
PLAN
  ↓
APPROVE
  ↓
IMPLEMENT ONE STEP
  ↓
TEST
  ↓
HANDOFF
  ↓
REVIEW
  ↓
APPROVE NEXT STEP
```

Never:

```text
PLAN
  ↓
"BUILD EVERYTHING"
```

CareTrace should grow through small, verified, reversible development units.
