# 13. Use SQLite and SQLAlchemy for development

Date: 2026-10-10

## Status

Accepted

## Context

The app stores creator accounts, polls, options, suggestions, and votes, so
it needs a database during development. Litestar integrates with SQLAlchemy
through its `sqlalchemy` extra, which installs Advanced Alchemy.

The production database is tied to the choice of deployment target, which
has not been made.

## Decision

- **Database (development):** SQLite, stored as a file in `data/`.
- **Database access:** SQLAlchemy, through Advanced Alchemy, installed with
  `litestar[sqlalchemy]`.
- **Driver:** `aiosqlite`, so database calls are async like the rest of the
  app.

## Consequences

- No database server to install or run locally.
- `.gitignore` excludes `data/*.db*`, so database files are never committed.
- Advanced Alchemy brings Alembic for database migrations, which go in
  `migrations/` (ADR-0005).
- The production database, such as a SQLite file on the server or Turso,
  will be decided together with the deployment target in a later ADR.
