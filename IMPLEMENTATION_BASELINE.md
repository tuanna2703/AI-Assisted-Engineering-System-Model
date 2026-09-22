# AESM Implementation Baseline

## Purpose

This document records the current repository boundary for implementing AESM. It is not a second semantic specification.

## Current Repository Boundary

- `docs/` — canonical AESM knowledge and normative semantics.
- `runtime/` — AESM Runtime implementation and authoritative execution control.
- `bridge/` — Agent access to Runtime; it does not own Runtime authority.
- `tests/` — executable verification and regression evidence.
- `.aesm/` — repository-local authoritative Process Instance / Execution Context persistence when a repository is an active AESM engineering scope.
- `plan/` — planning governance surface; entry point is `plan/README.md`.
- `IMPLEMENTATION_PLAN.md` — superseded legacy planning document; retained for migration/reconciliation only.
- `IMPLEMENTATION_BASELINE.md` — this implementation boundary record.
- `implementation/` — selected durable engineering records only.
- `README.md` — repository orientation.

## Work-Record Boundary

The repository intentionally has **one** Markdown work-record directory: `implementation/`.

`execution/` is not a permanent repository surface. Historical execution records were reconciled against:

- canonical `docs/`;
- executable `runtime/`, `bridge/`, and `tests/`;
- repository-local `.aesm/` state;
- current implementation planning.

Records whose unique value had already been promoted or superseded were removed from the active tree. Git history preserves their exact prior versions.

## Retained Engineering Records

The retained records are limited to durable evidence:

- empirical DBP execution findings;
- Runtime/Agent mechanism validation;
- multi-project behavioral validation;
- scope-binding implementation validation;
- normative documentation reconciliation;
- repository-portable continuation protocol.

These records are evidence and history, not alternate AESM authority.

## Exclusions

Do not add the following to `implementation/`:

- canonical AESM semantics;
- source code;
- tests or test fixtures;
- authoritative Process Instance state;
- current task instructions that belong in `IMPLEMENTATION_PLAN.md`;
- duplicate summaries of existing records;
- conversation/session transcripts;
- temporary scratch notes;
- every gate or intermediate checkpoint as a separate document.

## Baseline Principle

The repository should preserve the smallest set of surfaces needed to answer five different questions:

```
What does AESM mean?        → docs/
How is AESM implemented?   → runtime/ + bridge/
What proves behavior?      → tests/
What is authoritative now? → .aesm/
What durable engineering evidence remains? → implementation/
```
