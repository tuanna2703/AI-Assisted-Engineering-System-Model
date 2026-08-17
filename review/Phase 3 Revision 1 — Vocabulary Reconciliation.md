# Phase 3 Revision 1 — Vocabulary Reconciliation

**Phase:** Phase 3 Revision 1  
**Status:** Resolved — Validator Corrected  
**Authority:** Phase 2 AESM Operational Model and reconciled Phase 3 semantic matrices  
**Related validation failure:** commit `04048369c8f2a5a134c3a0a485365ee242514f13`

## 1. Purpose

This review resolves the vocabulary mismatch exposed by the first executable Phase 3 validation.

The failing validator required two top-level entity kinds that are not part of the reconciled primary entity inventory:

- `OperationDefinition`
- `TraceEvent`

The resolution is based on the semantic role of each concept, not on the validator's previous expectations.

## 2. OperationDefinition

`OperationDefinition` is **not** a primary entity kind.

Operation semantics are represented by the canonical `operationClasses` structure. Each operation carries the required semantic metadata, including:

- operation identity;
- subject;
- inputs;
- outputs;
- authority;
- mutation classification;
- preconditions;
- postconditions; and
- trace requirement.

Therefore introducing `OperationDefinition` as another top-level entity would duplicate the existing operation semantic structure and incorrectly expand Matrix A's primary entity vocabulary.

**Decision:** remove `OperationDefinition` from the validator's required entity vocabulary.

## 3. TraceEvent

`TraceEvent` is a required **structural semantic type**, but it is not a primary entity kind.

The reconciled Matrix A identifies `ExecutionTrace` as the primary trace entity. Matrix B explicitly states that one `ExecutionTrace` belongs to one Process Instance and contains ordered trace events. The canonical model already represents this through the `ExecutionTrace.events` field.

Therefore the correct representation is:

```text
ExecutionTrace
    └── events[]
          └── TraceEvent structural type
```

rather than:

```text
entityTypes
    ├── ExecutionTrace
    └── TraceEvent
```

**Decision:** remove `TraceEvent` from the top-level required entity vocabulary and validate the presence of an explicit event collection on `ExecutionTrace` instead.

## 4. Validator Correction

The Phase 3 semantic validator has been revised to:

1. remove `OperationDefinition` from `REQUIRED_KINDS`;
2. remove `TraceEvent` from `REQUIRED_KINDS`;
3. require `ExecutionTrace` to expose an explicit event collection;
4. validate operation semantics from the top-level `operationClasses` structure;
5. validate invariants from the top-level `invariants` structure; and
6. collect all validation failures before exiting rather than failing on the first missing vocabulary item.

The validator therefore tests the canonical model's intended semantic structure rather than imposing an incorrect flat entity vocabulary.

## 5. Model Change Decision

No canonical-model entity addition is required as a result of this reconciliation.

The existing canonical model already contains:

- `ExecutionTrace` as a primary entity;
- an `events` collection within `ExecutionTrace`; and
- operation definitions under `operationClasses`.

The correction is therefore a **validator and semantic-validation correction**, not a canonical-model expansion.

## 6. Authority Direction

The corrected derivation chain is:

```text
Phase 2 Operational Model
          ↓
Reconciliation Matrices
          ↓
Canonical Model
          ↓
Validator
```

The validator must conform to the canonical semantic model. It must not introduce new primary entities merely because its previous implementation expected them.

## 7. Consequence for Validation

The previous validation result remains valid historical evidence. It recorded the state of commit `279947f54e9f71d588f9b26652bf1c6cba5f3f1d` and correctly reported a validator/model vocabulary mismatch.

That result must not be overwritten.

The corrected validator creates a new validation baseline. The Phase 3 validation gate must now be executed again against the corrected repository revision.

## 8. Freeze Status

Phase 3 remains **NOT FROZEN**.

The next required action is executable re-validation of:

```text
scripts/validate-phase3.py
model/aesm-operational-model.json
schemas/aesm-machine-readable-model.schema.json
```

Only a new execution producing an overall PASS may make Phase 3 eligible for freeze.
