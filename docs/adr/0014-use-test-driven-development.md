# 14. Use test-driven development

Date: 2026-10-10

## Status

Accepted

## Context

The challenge defines exact rules that can be checked automatically. For
example: a poll has between 2 and 10 options, votes are refused after the
closing time, a declined suggestion never appears on the ballot, and a
closed poll can be reopened.

In test-driven development (TDD), a test is written first and fails because
the feature does not exist yet; then just enough code is written to make it
pass; then the code is cleaned up with the test still passing.

## Decision

Features are built test first.

- **Test runner:** pytest, as a development dependency.
- **Request-level tests:** Litestar's `TestClient` sends requests to a route
  and checks the response (status code and returned HTML).
- **Rule tests:** functions in a feature's `rules.py` have no web or database
  code (ADR-0005), so they are tested by calling them directly.
- Tests live in `tests/`, in one folder per feature, mirroring `app/`.
- Tests run through uv: `uv run pytest`.

## Consequences

- Every feature arrives with tests that describe its rules.
- The first features take longer while both Litestar and TDD are new.
- Tests check the HTML that comes back, not how the page looks. Layout and
  visual design are checked by eye.
- Tests will run in CI on every pull request once CI is set up (ADR-0008).
