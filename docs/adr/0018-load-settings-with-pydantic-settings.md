# 18. Load settings with pydantic-settings

Date: 2026-10-15

## Status

Accepted

Supersedes [ADR-0017](0017-load-environment-settings-with-doppler.md)

## Context

ADR-0017 stored secrets in Doppler and read settings into a frozen
dataclass filled from `os.environ`, to avoid adding dependencies.

A review of that code found two problems:

- **The secret was printed with the settings.** A dataclass's printed form
  includes every field, so logging the settings, or a traceback that shows
  local variables, would expose `TIEBREAKER_SECRET_KEY`.
- **Bad values were not caught clearly.** A missing secret raised a bare
  `KeyError` deep in a traceback, and an empty secret was accepted, so CSRF
  tokens would be signed with an empty string.

Fixing both by hand means writing and maintaining validation code that
libraries already provide.

Options considered:

- **Keep the dataclass and add our own checks**: no new dependencies, but
  every new setting needs its own hand-written checks.
- **msgspec**: already installed as a Litestar dependency. It validates
  types and lengths with clear errors, but it has no way to hide a field
  when printed, so the secret would still need custom code.
- **pydantic-settings**: built for loading application settings. It reads
  environment variables directly, validates every field, reports all
  problems in one error, and its `SecretStr` type prints as `**********`.

## Decision

- Settings are defined in `app/core/config.py` as a pydantic-settings
  `BaseSettings` class, with `env_prefix="TIEBREAKER_"` and `frozen=True`.
- Secrets use the `SecretStr` type. Code reads the real value only where it
  is needed, with `get_secret_value()`.
- Required secrets have a minimum length of 1, so an empty value is
  rejected the same way as a missing one.
- `pydantic` and `pydantic-settings` are added as dependencies.
- Doppler still supplies secrets as environment variables through
  `doppler run`, as recorded in ADR-0017. There is still no `.env` file;
  pydantic-settings' `.env` loading is not turned on.

## Consequences

- A missing or invalid setting stops the app at startup with a
  `ValidationError` that names the setting and the problem.
- Secrets stay hidden when settings are printed or logged.
- Tests set environment variables with pytest's `monkeypatch` fixture, or
  build `Settings` directly with test values, so tests still run without
  Doppler or network access.
- Pyright cannot tell that `BaseSettings` fills required fields from the
  environment, so the one place that calls `Settings()` with no arguments,
  `load_settings()`, carries a `pyright: ignore` comment explaining why.
- New dependencies: `pydantic`, `pydantic-settings`, and the packages they
  bring in (`pydantic-core`, `annotated-types`, `typing-inspection`).
- Pydantic is available for validating request data in later features.
