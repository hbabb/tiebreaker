# 5. Feature-based project layout

Date: 2026-10-10

## Status

Accepted

## Context

Litestar does not impose a folder structure. The layout needs to keep
shared setup separate from feature code, keep the product's name for the
product rather than for a settings folder, and make it obvious where a
given piece of code belongs.

## Decision

Code is grouped by feature inside an `app/` package:

```
tiebreaker/
├── app/
│   ├── main.py          ← creates the Litestar app, registers features
│   ├── core/            ← shared setup: config, database, security
│   ├── accounts/        ← creator sign-up, log in, log out
│   ├── polls/           ← creator side: dashboard, create, moderate, close/reopen
│   ├── voting/          ← public side: vote page, results, live updates
│   ├── templates/       ← base.html, errors/, and one folder per feature
│   └── static/          ← css/, js/, img/
├── data/                ← SQLite database file
├── migrations/          ← database migration files
├── tests/               ← one folder per feature
├── docs/adr/
├── mise.toml
├── pyproject.toml
└── uv.lock
```

- Each feature folder holds `models.py` (tables), `routes.py` (handlers),
  and `rules.py` where the feature has logic of its own. Rules are plain
  functions with no web or database code, so they can be tested directly.
- `core/` holds only shared setup, never feature code.
- `templates/` and `tests/` mirror the feature folders.
- `app/main.py` is found automatically by `litestar run`, which looks for an
  app in modules named `app`, including its submodules.

## Consequences

- Finding code for a feature means opening one folder.
- New features follow the same pattern: a folder in `app/`, `templates/`,
  and `tests/`.
- Files are created when a feature needs them, not up front.
