# 3. Server-rendered HTML with HTMX

Date: 2026-10-10

## Status

Accepted

## Context

The vote page is the most-visited screen and is usually opened on a phone
from a link in a group chat. It needs to load fast and work with no account.
The app also needs partial page updates: casting a vote without a reload,
live results, and moderating suggestions.

Options considered:

- **A separate single-page app** (React or Vue) calling a JSON API: two
  codebases, an API contract to keep in sync, and more JavaScript sent to
  phones.
- **Server-rendered HTML with HTMX**: the server returns HTML, and HTMX
  attributes in the markup fetch small HTML fragments and swap them into the
  page.

## Decision

We will render HTML on the server with Jinja2 templates and use HTMX for
partial updates.

- Full pages extend `templates/base.html`.
- Fragments that HTMX swaps in are separate templates prefixed with `_`
  (for example `_results.html`), the same convention Rails uses for
  partials.
- Litestar's CSRF token is sent with every HTMX request through
  `hx-headers` on `<body>`, using the `x-csrftoken` header.
- Routes return HTML, not JSON. There is no public API, so routes are not
  versioned. If a JSON API is added later, it gets its own versioned
  location (`app/api/v1/`).
- JavaScript is limited to browser-only features HTMX does not cover, such as
  copying the poll link, the native share sheet, and the winner reveal.

## Consequences

- One codebase and one deployment for both the creator side and the vote
  page.
- Pages are usable as soon as the HTML arrives.
- The HTMX script file is served from `app/static/js/`; Litestar's HTMX
  plugin handles the server side only.
- How live results are delivered (HTMX polling or Server-Sent Events) is left
  to a later decision.
- Whether to write the small amount of client script as JavaScript, JS with
  JSDoc types, or TypeScript is not yet decided.
