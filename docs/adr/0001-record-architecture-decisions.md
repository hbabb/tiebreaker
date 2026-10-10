# 1. Record architecture decisions

Date: 2026-10-10

## Status

Accepted

## Context

Tiebreaker is built from a Frontend Mentor product challenge, which provides a
product spec but no design or technical stack. Every technical choice is made
by this project, and the reasoning behind those choices needs to stay
available to anyone reading the code later, including future contributors and
reviewers of this portfolio project.

## Decision

We will record architecture decisions as Architecture Decision Records
(ADRs), using the format described by Michael Nygard: Title, Status, Context,
Decision, and Consequences.

ADRs live in `docs/adr/`, numbered sequentially with four digits
(`0001-…`, `0002-…`). An accepted ADR is not edited to change its decision.
When a decision changes, a new ADR is written, and the old one's status is
updated to "Superseded by ADR-NNNN".

Day-to-day rules that follow from these decisions (setup steps, commit
format, branching) are written in `CONTRIBUTING.md`.

## Consequences

- The reasoning behind each decision, including the options rejected, is
  kept in the repository next to the code.
- Decisions made before this ADR are backfilled as ADRs 0002 onward, in the
  order they were made.
- Each significant decision takes a few minutes to write up.
