# Step 1 verification

Completed: technical foundation only. The workspace was empty before this step.
No healthcare features, roles, public authentication UI, or demo data were added.

## Verified locally

- Installed pinned dependencies in `.venv`; `pip check` found no broken requirements.
- Initial accounts and Django migrations applied successfully to an empty SQLite database.
- Django system checks passed; migration drift check found no changes.
- All six Django tests passed.
- Ruff lint and format checks passed.
- Production checks passed with only documented W005/W021 exceptions silenced.
- WhiteNoise manifest/compression static collection completed successfully.
- Temporary local servers served home, liveness, Bootstrap CSS/JS, and custom
  CSS/JS successfully under development and production settings. Production
  smoke requests simulated a trusted HTTPS proxy. Both servers were stopped.
- Git initialized on main; runtime secrets, database, virtual environment, media,
  and collected static files are ignored. No commit or remote push was made.

## Limits

GitHub Actions is configured but has not run remotely. Gunicorn execution is
covered by the Linux CI job and was not run on Windows. No deployment occurred.
Full visual design and browser interaction testing belong to an approved UI step.
Windows sandbox restrictions required elevated dependency/bootstrap downloads.

## Next review

Review the foundation before approving the next bounded UI/layout step.
