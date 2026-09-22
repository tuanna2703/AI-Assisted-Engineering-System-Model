# Repository-Scoped DBP Continuation Validation

## Identity

Task ID:
repository-scoped-dbp-continuation-validation

Status:
not-started

Source:
IMPLEMENTATION_PLAN.md — "Mechanism Validation Gate" decision and post-hardening
direction. Explicitly deferred during Planning System Restructuring.

Concern tags:
dbp, continuation, fresh-agent, repository-scoped, empirical-validation

---

## Objective

Validate that a fresh Agent can continue a DBP-related Process Instance from a
repository checkout, using the established Runtime/scope-resolution mechanism —
demonstrating that the operational chain governs a real engineering scope rather
than just the AESM-self-development scope.

---

## Context

The mechanism validation gate (now recorded in plan/completed/agent-boundary-mechanism-validation.md)
established: "READY FOR DBP EMPIRICAL EXECUTION."

The DBP empirical execution (plan/completed/dbp-empirical-execution.md) identified
that no authoritative Process Instance, Execution Context, or Runtime participation
was established during that original execution.

The scope resolution work (plan/completed/engineering-scope-identity-and-scope-resolution.md)
established the mechanisms needed for deterministic scope-to-Process-Instance binding.

The repository-portable continuation validation demonstrated Git portability and
fresh-Agent recovery for the AESM self-development repository.

This task would validate whether those mechanisms work for a real DBP engineering
scope — establishing or recovering a DBP Process Instance, obtaining authoritative
Context, performing Runtime-mediated work, and demonstrating cross-session continuity.

---

## Governing Constraints

**This task must not be executed autonomously by an Agent.**

Promotion from backlog to active requires explicit human authorization.

The following boundaries must be observed when this task is authorized:

1. Do not fabricate a DBP Process Instance or AESM evidence retroactively from
   the original DBP execution. A new controlled execution is required.
2. Do not claim repository-scoped DBP continuation validation has passed
   unless the full evidence chain is established.
3. The DBP engineering code changes must be controlled and bounded (not free-ranging
   requirement implementation).
4. A separate planning authorization instruction must activate this task.

---

## Dependencies

- repository-portable-continuation-validation (COMPLETE — demonstrates Git portability)
- engineering-scope-identity-and-scope-resolution (COMPLETE — provides scope resolution mechanism)
- runtime-consistency-and-continuity-hardening (COMPLETE — Runtime is hardened)
- planning-system-restructuring (must be COMPLETE — establishes planning governance)

---

## Decisions Still in Effect (from prerequisite tasks)

All decisions from prerequisite completed tasks apply. Key relevant ones:

1. Remote Git round trip remains explicitly unclaimed from prior validations.
   This task's evidence scope should include the remote round trip if authorized.
2. No fabrication of retroactive AESM evidence from the original DBP execution.
3. Agent-boundary mechanism validation gate closed — do not reopen bridge or
   guidance interface semantics unless new evidence directly requires it.

---

## Proposed Work Units (draft — subject to revision at authorization)

These work units are candidate structure. They must be reviewed and approved
before this task is activated.

### Fixture Establishment
Establish the controlled DBP experiment fixture: repository, bounded request,
Process Instance baseline.

### Session A — Process Instance Creation
In an initial Agent session: create a DBP Process Instance through scope resolution
and Runtime bridge, perform bounded Runtime-mediated work, persist state.

### Session B — Fresh-Agent DBP Continuation
In a separate Agent session with only repository/checkout context: discover the
existing DBP Process Instance, obtain authoritative Context, perform a bounded
continuation, persist evidence.

### Evidence Reconciliation
Reconcile CONTROLLER, AGENT, RUNTIME, PERSISTED, and VERIFICATION evidence.
Classify result as PASS or identify specific gaps.

---

## Acceptance Criteria (draft)

1. A DBP Process Instance exists with authoritative .aesm/ state.
2. Session A and Session B use distinct OS process and Agent session identities.
3. Session B discovered the Process Instance independently, without being given
   the Process Instance ID directly.
4. Runtime-mediated mutations are evidenced by persisted history with session
   attribution from both sessions.
5. The operational chain from scope resolution through continuation is complete.
6. Result is classified as PASS or specific gaps are documented.

---

## Authorization Status

**Not authorized. Requires explicit human instruction to activate.**

Do not move this file to plan/active/ without an explicit planning decision.
