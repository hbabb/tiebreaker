# 11. Use Ruff for linting and formatting

Date: 2026-10-10

## Status

Accepted

## Context

Python code needs a linter (to flag bugs and bad patterns), a formatter (for
consistent style), and import sorting.

Options considered:

- **flake8, black, and isort**: three separate tools with three separate
  configurations.
- **Ruff**: one tool that lints (`ruff check`), formats (`ruff format`), and
  sorts imports (the `I` rules), and also runs as a language server in the
  editor (`ruff server`).

## Decision

Ruff is the linter, formatter, and import sorter.

- Ruff is a development dependency, so its version is pinned in `uv.lock`.
- Commands run through uv: `uv run ruff check` and `uv run ruff format`.

## Consequences

- One tool and one configuration section (`[tool.ruff]` in
  `pyproject.toml`) instead of three.
- Since Ruff 0.16, the default rule set is large (407 rules in 0.17.0) and
  includes import sorting. With no `[tool.ruff]` section, those defaults
  apply.
- Ruff reads the target Python version from `requires-python` in
  `pyproject.toml`.
- Setting `select` replaces the default rules entirely; `extend-select` adds
  to them.
- Ruff does not check types; that is covered by ADR-0012.
