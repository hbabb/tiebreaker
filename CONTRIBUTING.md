# Contributing to Tiebreaker

This guide covers how to set up the project, how work moves from a change to
`main`, and how commit messages are written. The reasoning behind each rule
is recorded in [`docs/adr/`](docs/adr/).

## Setup

Requirements: [mise](https://mise.jdx.dev/) and
[uv](https://docs.astral.sh/uv/).

Clone the repository and move into it:

```sh
git clone git@github.com:hbabb/tiebreaker.git
```

```sh
cd tiebreaker
```

Install the pinned Python version (set in `mise.toml`):

```sh
mise install
```

Install dependencies from `uv.lock`:

```sh
uv sync
```

Start the development server:

```sh
uv run litestar run
```

## Branching

This project uses GitHub Flow ([ADR-0008](docs/adr/0008-use-github-flow.md)).

- `main` is always deployable.
- Work happens on a short-lived bookmark created from `main`.
- Changes reach `main` only through a pull request.

Bookmark names use the commit type and a short topic:

```
feat/poll-creation
fix/double-vote
docs/contributing
```

With jj, start a change from `main`:

```sh
jj new main
```

When the work is ready, name the bookmark:

```sh
jj bookmark create feat/poll-creation -r @
```

Push it:

```sh
jj git push --bookmark feat/poll-creation
```

Then open a pull request into `main` on GitHub.

## Commit messages

Commits follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
([ADR-0007](docs/adr/0007-use-conventional-commits.md)).

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- **description**: short, lowercase, written as an instruction ("add", not
  "added"), with no period at the end.
- **body**: optional. Explains what changed and why, separated from the
  description by a blank line.
- **footer**: optional. For example `Refs: #12`, or `BREAKING CHANGE:`
  followed by a description.

### Types

| Type       | Use for                                               |
| ---------- | ----------------------------------------------------- |
| `feat`     | a new feature                                         |
| `fix`      | a bug fix                                             |
| `docs`     | documentation only                                    |
| `style`    | formatting that doesn't change behavior               |
| `refactor` | code changes that neither fix a bug nor add a feature |
| `perf`     | performance improvements                              |
| `test`     | adding or correcting tests                            |
| `build`    | dependencies or the build system                      |
| `ci`       | CI configuration                                      |
| `chore`    | maintenance that doesn't fit another type             |

### Scopes

Scopes match the feature folders in `app/`:

| Scope      | Covers                                                     |
| ---------- | ---------------------------------------------------------- |
| `accounts` | creator sign-up, log in, log out                           |
| `polls`    | creator dashboard, poll creation, moderation, close/reopen |
| `voting`   | public vote page, results, live updates                    |
| `core`     | shared setup: config, database, security                   |

A scope is optional. Leave it off when a change spans the whole project.

### Examples

```
feat(polls): add poll creation form
fix(voting): prevent double vote on refresh
docs: add contributing guide
build: add litestar[standard]
```

### One type per commit

If a change fits more than one type, split it into separate commits.

### Enforcement

jj does not run Git hooks, so a local `commit-msg` hook cannot check the
format ([ADR-0006](docs/adr/0006-use-jujutsu-with-git-backend.md)). The format
will be checked in CI on pull requests.

## Signed commits

Commits pushed to this repository should be signed
([ADR-0009](docs/adr/0009-sign-commits-with-ssh.md)). SSH signing is the
project's approach; any signing method that GitHub shows as **Verified** is
accepted.
