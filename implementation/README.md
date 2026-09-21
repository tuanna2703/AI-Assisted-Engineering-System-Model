# Implementation Records

## Purpose

`implementation/` is the repository's single durable work-record surface.

It preserves concise engineering evidence that is useful after implementation but does not belong in canonical documentation, executable source, tests, authoritative `.aesm/` state, or the current implementation plan.

## Keep

Retain a record only when it captures durable:

- implementation findings;
- empirical validation;
- reconciliation;
- important implementation evidence;
- a protocol whose future repeatability matters.

## Do Not Keep

Do not use this directory for:

- AESM semantics that belong in `docs/`;
- source code or tests;
- authoritative Process Instance state;
- active task planning;
- conversation transcripts;
- temporary notes;
- duplicate or superseded records.

When a finding becomes part of the canonical AESM model, the canonical documentation becomes the authority. The engineering record may be removed when its remaining historical value is not material.

## Current Records

The current records are deliberately limited to validated or durable work:

- DBP empirical execution evidence
- Runtime/Agent mechanism validation
- multi-project behavioral validation
- scope-binding validation
- normative documentation reconciliation
- repository-portable continuation protocol

`execution/` is intentionally absent. Execution is a Runtime-governed activity, while persistent execution state belongs under repository-local `.aesm/`.
