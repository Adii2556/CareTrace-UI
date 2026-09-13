# Step 2 — Authentication and account foundation

## Completed

- Username registration using Django UserCreationForm, with automatic session login.
- Native Django login/logout, safe return destinations, and POST-only logout.
- Protected `/app/` welcome shell and `/accounts/profile/` account view/edit page.
- Basic first name, last name, and email editing restricted to request.user.
- State-aware navigation, reusable accessible Bootstrap form markup, and messages.
- No roles, medical fields/features, schema changes, dependencies, or deployment.

## Decisions

The existing custom user is unchanged. Username identifies the account; optional
email is unverified contact information and may be shared by multiple accounts.
Password reset/change and medical profiles are deferred. Accounts and medical
domain data remain separate. Authenticated pages prevent browser caching.

## Verification

- Complete suite: 20 tests passed, including all six Step 1 tests.
- Registration validation, duplicate usernames, hashing, valid/invalid/inactive
  login, logout, route guards, safe redirects, account isolation, forbidden field
  submissions, escaping, and CSRF enforcement verified.
- Fresh migrations succeeded on a separate temporary SQLite database.
- Browser flow passed: home → registration → app → account update → logout →
  protected-route login redirect → login → app with the updated name.
- Account layout inspected at 375px width with usable navigation and forms.

GitHub CI and Linux Gunicorn execution remain unverified remotely; no deployment.
The browser smoke test used a disposable database, not the development database.

## Next

Review Step 2 and explicitly define/approve the next bounded development step.
