# 17. Load settings from the environment, with secrets in Doppler

Date: 2026-10-11

## Status

Accepted

## Context

The app needs settings that differ between machines and must not be
committed, starting with the CSRF secret (ADR-0003) and the database
location (ADR-0013).

Options considered for reading settings in the app:

- **pydantic-settings**: reads environment variables and `.env` files and
  validates types. It adds pydantic and pydantic-settings as dependencies.
- **A frozen dataclass filled from `os.environ`**: plain Python with no new
  dependencies.

Options considered for supplying secrets on a developer machine:

- **A `.env` file**: a local, git-ignored file of secret values.
- **Doppler**: a hosted secrets manager. `doppler run -- <command>` fetches
  the secrets for the project and passes them to the command as environment
  variables, so no secret is stored in the repository folder.

## Decision

- Secrets are stored in Doppler. The repository folder is linked to the
  Doppler project with `doppler setup`.
- The development server is started through Doppler:
  `doppler run -- uv run litestar run --reload`, wrapped in the mise `dev`
  task.
- There is no `.env` file.
- `app/core/config.py` reads settings from environment variables into a
  frozen dataclass. Required secrets have no default; non-secret settings,
  such as the development database location, have defaults.

## Consequences

- The app only reads environment variables, so it does not depend on where
  they come from: Doppler locally, or the host's settings in production.
- The app fails at startup if a required secret is missing.
- Tests build their settings directly with test values, so `uv run pytest`
  and CI run without Doppler or network access.
- Running the development server requires the Doppler CLI and a logged-in
  account.
- No new Python dependencies are added.
