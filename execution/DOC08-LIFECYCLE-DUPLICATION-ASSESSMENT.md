# Doc 08 Lifecycle Duplication Assessment

## Scope

This assessment reviews the lifecycle-related material in:

- `docs/08-Continuity-Traceability-and-Reconsideration.md`
- `docs/11-Applicable-Process-Instance-Lifecycle-Semantics.md`

The purpose is to determine whether Doc 08 contains duplicated detailed Process Instance lifecycle semantics and whether any semantic conflict exists with Doc 11.

This is a bounded documentation-authority assessment. No runtime, test, or implementation changes were made as part of the assessment.

## Authority Baseline

Doc 11 identifies itself as a **Normative semantic specification** and explicitly defines the applicable Process Instance lifecycle semantics, including lifecycle applicability, suspension, resumption, termination, authority, preservation, conflict handling, and lifecycle traceability.

Doc 08 is the continuity, traceability, and reconsideration document. Its lifecycle material is appropriate where it explains how lifecycle concepts relate to continuity, historical reconstruction, and reconsideration, but detailed lifecycle meaning should be owned by Doc 11.

## Lifecycle Material Classification

### Process Instance lifecycle section

**Doc 08 material:**

- identifies Process Instance lifecycle as distinct from Process State, engineering completion, Runtime lifetime, Agent/conversation lifetime, and Execution Environment lifetime;
- defines `ACTIVE`, `SUSPENDED`, and `TERMINATED`;
- defines the universal transition possibilities;
- states termination finality;
- states that lifecycle transitions require applicable execution semantics;
- distinguishes engineering completion from lifecycle termination.

**Classification:** **Duplicated lifecycle semantics**.

**Reason:** These statements independently define canonical lifecycle states, transition paths, transition authorization conditions, finality, and the distinction between completion and termination. Doc 11 already owns each of these semantics.

### Suspension and resumption section

**Doc 08 material:**

- defines suspension as `ACTIVE → SUSPENDED`;
- defines preservation obligations;
- distinguishes recovery from resumption;
- specifies the recovery/observation/evaluation/resumption sequence;
- states that persisted `next_action` is expected continuation information rather than an imperative command;
- identifies possible reevaluation outcomes.

**Classification:** **Duplicated lifecycle semantics**.

**Reason:** These are detailed suspension, preservation, recovery, reevaluation, and resumption rules. Doc 11 defines the same semantics normatively.

### Lifecycle traceability section

**Doc 08 material:**

- requires material lifecycle transitions to remain reconstructable;
- gives the prior-state → trigger → authority → semantic-basis → transition → resulting-state → consequence chain;
- states that current lifecycle state alone is insufficient evidence.

**Classification:** **Contextual summary** with **duplicated detailed semantics**.

**Reason:** Lifecycle traceability is directly relevant to Doc 08's continuity and traceability purpose and therefore some local explanation is required. However, the detailed reconstruction requirements and chain are already normatively defined by Doc 11. Doc 08 should retain a concise relationship-level explanation and defer detailed requirements to Doc 11.

### Historical state reference

**Doc 08 material:**

- states that material historical state should remain reconstructable;
- identifies lifecycle transition reconstruction as one use of historical preservation.

**Classification:** **Required local explanation**.

**Reason:** Historical reconstructability is directly relevant to continuity, traceability, auditing, reconsideration, recovery, and Runtime replacement. The passage does not need to define lifecycle mechanics and should remain in Doc 08.

### Continuity across Agents and Environments

**Doc 08 material:**

- states that a Process Instance can remain active or suspended while an Agent stops participating;
- states that the Process Instance may move between Execution Environments;
- states that Agent/conversation/environment state is not the authoritative source of process state.

**Classification:** **Required local explanation**.

**Reason:** These passages establish the continuity argument of Doc 08. They use lifecycle concepts but do not need to redefine detailed lifecycle semantics.

### Core continuity invariants

**Doc 08 material:**

- `Process Instance survives Agent changes while not terminated`;
- `Process Instance survives Environment changes while not terminated`;
- `Material lifecycle history remains reconstructable`;
- `Recovery does not itself imply resumption`;
- `Termination does not imply Runtime termination`.

**Classification:** **Required local explanation**, with detailed meanings deferred to Doc 11.

**Reason:** These invariants connect lifecycle semantics directly to the continuity argument. They should remain, but they should not be expanded into another lifecycle specification.

## Authority Assessment

Doc 08 currently contains detailed lifecycle definitions rather than merely referencing lifecycle semantics. In particular, its dedicated lifecycle, suspension/resumption, and lifecycle-traceability sections independently establish rules that are already normative in Doc 11.

Therefore, Doc 08 currently functions as an accidental secondary detailed lifecycle authority.

The intended authority relationship should be restored as follows:

> **Doc 08 explains how continuity, traceability, and reconsideration relate to lifecycle semantics; Doc 11 defines the lifecycle semantics themselves.**

## Conflict Assessment

No semantic conflict was identified between Doc 08 and Doc 11 in the reviewed lifecycle material.

The documents are substantially aligned on:

- the lifecycle states `ACTIVE`, `SUSPENDED`, and `TERMINATED`;
- permitted lifecycle transitions;
- termination finality;
- separation of lifecycle state from Process State and engineering completion;
- separation of recovery from resumption;
- reevaluation before resumption;
- preservation of authoritative state;
- lifecycle traceability;
- non-equivalence of Runtime/Agent/Environment shutdown and lifecycle termination or suspension.

The issue is therefore duplication of semantic ownership, not contradiction.

## Recommended Resolution

Proceed to the bounded **Lifecycle Content Resolution** work unit.

Preserve in Doc 08:

- historical-state context;
- continuity implications of lifecycle state;
- continuity across Agents and Execution Environments;
- concise lifecycle context needed to understand traceability and reconsideration;
- core continuity invariants that depend on lifecycle distinctions.

Reduce or remove from Doc 08:

- canonical lifecycle-state definitions;
- detailed transition graphs and transition rules;
- detailed suspension and resumption semantics;
- detailed preservation and reevaluation requirements;
- detailed lifecycle authority rules;
- detailed lifecycle traceability requirements.

Replace detailed duplicated material with concise references to Doc 11 where necessary.

## Change Boundary

This assessment authorizes only the following subsequent work:

1. bounded editing of Doc 08 to restore lifecycle semantic ownership to Doc 11;
2. authority/reference verification;
3. documentation/reference validation and existing regression testing;
4. a focused follow-up evidence report.

It does **not** authorize:

- runtime changes;
- test implementation changes;
- new lifecycle semantics;
- broad repository cleanup;
- unrelated documentation restructuring.

## Assessment Result

**PASS — No Semantic Conflict; Lifecycle Duplication Confirmed**

The duplication is sufficiently clear to proceed with controlled content resolution without requiring a separate semantic decision.

## Assessment Integrity

No changes were made to Doc 08, Doc 11, `runtime/`, or `tests/` during this assessment.
