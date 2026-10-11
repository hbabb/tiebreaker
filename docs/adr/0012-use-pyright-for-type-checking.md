# 12. Use Pyright for type checking

Date: 2026-10-10

## Status

Accepted

## Context

Python type hints are only useful if a type checker enforces them. The same
rules should apply in the editor and on the command line, so the two never
disagree.

Options considered:

- **mypy**: mature and pure Python, but it has no language server. Running
  it in the editor means wrapping it as a linter, and an editor-installed
  copy does not see the project's packages without extra configuration.
- **ty**: from Astral (the makers of Ruff and uv), with a language server,
  but in beta (`0.0.x` versions).
- **Pyright**: mature, and already the Python language server in the
  editor. The PyPI `pyright` package runs the same checker from the command
  line.

## Decision

Pyright is the type checker in both the editor and the project.

- `pyright` is a development dependency, so its version is pinned in
  `uv.lock`.
- The command line check runs through uv: `uv run pyright`.
- `[tool.pyright]` in `pyproject.toml` points Pyright at the project's
  virtual environment:

  ```toml
  [tool.pyright]
  venvPath = "."
  venv = ".venv"
  ```

## Consequences

- The editor and the command line read the same `[tool.pyright]` settings.
- Pyright is written in TypeScript and needs Node to run. The PyPI package
  uses Node from the machine's `PATH`, or downloads it into `~/.cache` if
  none is found. Nothing Node-related is added to the repository.
- An editor that installs its own copy of Pyright can drift from the version
  in `uv.lock`. Pointing the editor at `.venv/bin/pyright-langserver` keeps
  them identical.
