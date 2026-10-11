# 15. Deliver live results by polling

Date: 2026-10-10

## Status

Accepted

## Context

The challenge requires results that update live while a poll is open.
ADR-0003 left open how those updates reach the browser.

Options considered:

- **Server-Sent Events (SSE)**: the browser keeps one connection open and
  the server pushes new results when a vote arrives. This needs the separate
  `htmx-ext-sse` extension and Litestar's `ServerSentEvent` response. A vote
  received by one worker process has to reach the connections held by every
  other worker, which needs Litestar Channels; its in-memory backend does not
  work across multiple processes, so Redis or PostgreSQL would be required.
- **Polling**: the browser asks for the latest results on a fixed interval
  using HTMX's `hx-trigger="every …"`.

## Decision

Live results are delivered by HTMX polling, for these reasons:

- Every update is an ordinary request, so it works on any host with any
  number of workers.
- There is no need for Litestar Channels, or for Redis or PostgreSQL to pass
  messages between workers.
- It avoids the browser's limit of 6 SSE connections per site on HTTP/1.1.
- The server can stop it when a poll closes by replying with status `286`
  (Litestar's `HXStopPolling` response).

## Consequences

- Results reach the browser up to one polling interval after a vote is cast.
- A request is sent every interval, whether or not the results have changed.
- The results fragment is a partial template (`_results.html`, ADR-0003).
- The polling interval is not yet decided.
