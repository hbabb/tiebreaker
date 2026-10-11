# 16. Use Google-style docstrings

Date: 2026-10-11

## Status

Accepted

## Context

Code is documented in two ways: docstrings (the triple-quoted text at the
top of a module, class, or function) describe what something is for, and
comments explain non-obvious lines. Docstrings need one consistent format so
they read the same across the project and can be checked automatically.

Options considered:

- **Google style**: sections such as `Args:` and `Returns:` with indented
  entries.
- **NumPy style**: sections underlined with dashes, with each parameter's
  type written in the docstring.
- **reStructuredText (Sphinx)**: field tags such as `:param:` and
  `:returns:`.

Every function already has type hints, and Pyright checks them (ADR-0012).
Types written inside a docstring are not checked by anything and can fall
out of date when a signature changes.

## Decision

Docstrings follow the Google style.

- Types live in the function signature; the docstring describes what each
  value means.
- Ruff checks docstrings (ADR-0011) with its `pydocstyle` rules set to the
  Google convention:

  ```toml
  [tool.ruff.lint]
  extend-select = ["D"]

  [tool.ruff.lint.pydocstyle]
  convention = "google"
  ```

- Comments are used for lines whose purpose is not obvious from the code.

## Consequences

- `extend-select` adds the docstring rules on top of Ruff's defaults rather
  than replacing them.
- Every public module, class, and function needs a docstring, including
  test files and `__init__.py` files.
  - Edit: this consequence has been removed by updating the rulls for ruff with per-file-ignores.
- The existing `app/main.py` and `tests/test_app.py` need docstrings to pass
  `ruff check`.
