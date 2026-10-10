# 4. Use mise and uv for tooling

Date: 2026-10-10

## Status

Accepted

## Context

The project needs a pinned Python version, isolated dependencies, and a
lockfile so every machine gets the same environment.

Options considered:

- **pip and venv**: no lockfile by default.
- **Dev Containers, Devbox, or Toolbx**: container- or Nix-based
  environments. They duplicate what mise and uv already provide, and the app
  needs nothing beyond Python and its packages.
- **mise and uv**: mise pins tool versions per project; uv manages packages,
  the virtual environment, and the lockfile.

## Decision

- **mise** pins Python 3.14 in `mise.toml`.
- **uv** manages dependencies in `pyproject.toml` and `uv.lock`, and the
  virtual environment in `.venv/`.
- The project was created with `uv init --bare`, so uv does not write a
  `.python-version` file. mise is the only place the Python version is set.
- Commands run through uv: `uv run litestar run`.

## Consequences

- Anyone with mise and uv can reproduce the environment from the repository.
- `.venv/` is listed in `.gitignore` and never committed.
- Docker may still be added later for production deployment; that is a
  separate decision.
