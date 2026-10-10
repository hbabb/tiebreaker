# 7. Use Conventional Commits

Date: 2026-10-10

## Status

Accepted

## Context

Git does not enforce any commit message format. A consistent format makes
the history easy to scan on GitHub and allows changelogs and version bumps to
be generated from commit types later.

## Decision

Commit messages follow the Conventional Commits 1.0.0 specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- Types: `feat` and `fix` from the specification, plus `build`, `chore`,
  `ci`, `docs`, `style`, `refactor`, `perf`, and `test`.
- Scopes match the feature folders: `accounts`, `polls`, `voting`, `core`.
- A change that fits more than one type is split into separate commits.

The full rules and examples are in `CONTRIBUTING.md`.

## Consequences

- Local `commit-msg` hooks cannot enforce the format because jj does not run
  Git hooks (see ADR-0006). Enforcement will be added as a CI check on pull
  requests.
- Until that check exists, the format is followed by convention.
