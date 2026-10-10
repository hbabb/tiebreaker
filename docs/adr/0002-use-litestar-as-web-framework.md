# 2. Use Litestar as the web framework

Date: 2026-10-10

## Status

Accepted

## Context

The Tiebreak challenge calls for a deployed product with a database, creator
authentication, a public vote page that needs no account, and live-updating
results. In practice the backend needs:

- server-rendered HTML pages
- creator sign-up, log in, and sessions
- CSRF protection on forms
- a database layer
- live updates (polling or Server-Sent Events)
- rate limiting on voting and suggestions

The project is written in Python. Options considered:

- **Django**: has auth, sessions, CSRF, ORM, and migrations built in, but its
  project layout and conventions did not fit how this project wants to be
  organized.
- **FastAPI**: familiar from previous work, with Jinja2 templates and
  Server-Sent Events built in. Auth, CSRF, and rate limiting would need to
  be assembled from separate packages, and the main auth package, FastAPI
  Users, is in maintenance mode (security updates only, no new features).
- **Litestar**: uses the same decorator-based route style as FastAPI, but
  includes more of what this app needs.

## Decision

We will use Litestar, installed with the `standard` extra
(`litestar[standard]`), which includes Uvicorn and Jinja2.

Built-in Litestar features this project relies on:

- session middleware and session-based authentication, with guards for
  route-level access checks
- CSRF protection (`CSRFConfig`)
- the HTMX plugin (`HTMXPlugin`, `HTMXRequest`, `HTMXTemplate`)
- Jinja2 templating
- Server-Sent Events responses
- rate-limit middleware
- the SQLAlchemy plugin

## Consequences

- Route handlers keep the decorator style already familiar from FastAPI.
- Auth, CSRF, HTMX helpers, and rate limiting come from the framework rather
  than separate packages.
- Litestar does not impose a folder layout, so the project defines its own
  (see ADR-0005).
- Litestar is less widely known than FastAPI or Django, so fewer tutorials
  and examples exist. Its own documentation is the main reference.
