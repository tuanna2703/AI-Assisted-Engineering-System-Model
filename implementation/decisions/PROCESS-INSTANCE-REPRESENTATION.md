# Process Instance Implementation Representation

## Purpose

This document records the implementation decision for representing an AESM Process Instance in the initial prototype. It translates existing AESM semantics into implementation requirements without introducing new AESM semantics.

## Semantic Baseline

A Process Instance is one execution of the Engineering Process Model for a specific engineering objective and is the persistent identity of that engineering work. It is independent of an Agent, conversation, Agent context window, IDE session, Runtime process lifetime, and Execution Environment.

A Process Instance must have a stable identity across continuation, Agent replacement, Runtime restart, and Execution Environment replacement. It must also retain an explicit binding to the applicable EPM definition, including a recoverable version or revision where applicable.

Process Instance and Execution Context remain semantically distinct: the Process Instance identifies which engineering execution exists; the Execution Context records the authoritative operational situation now.

## Minimal Required Representation

| Field | Required | Role |
|---|---|---|
| `process_instance_id` | Yes | Stable identity of the engineering execution. |
| `engineering_objective` | Yes | Specific engineering objective of this Process Instance. |
| `epm` | Yes | Explicit binding to the applicable EPM definition and version/revision where applicable. |

Additional fields may exist as implementation metadata, but must not silently become new AESM semantic requirements.

## Existing Prototype Representation

The existing Python representation contains `process_instance_id`, `engineering_objective`, `lifecycle`, `execution_context_ref`, `epm`, `pem`, `created_at`, and `updated_at`.

**Decision: ADAPT, not REPLACE.**

- `process_instance_id`: keep; generate once and persist.
- `engineering_objective`: keep; remain recoverable independently of conversation history.
- `epm`: keep and constrain; the binding must be explicit and recoverable.
- `lifecycle`: keep as process-lifecycle metadata, but do not conflate it with engineering completion or Runtime termination.
- `execution_context_ref`: keep as a physical storage reference; this is an implementation choice, not an AESM semantic requirement.
- `created_at` / `updated_at`: keep as implementation metadata.
- `pem`: retain temporarily for compatibility, but do not treat it as a normative Process Instance requirement until its necessity is separately validated.

## Explicit Non-Requirements

Do not add Agent identity, conversation/session identity, IDE or Execution Environment identity, Runtime process identity, workflow-specific step lists, transient Agent memory, or environment-specific configuration as Process Instance identity or AESM semantics.

## Verification Requirements

The creation and persistence implementation must demonstrate:

1. Stable unique Process Instance identity.
2. Required engineering objective.
3. Explicit EPM binding.
4. Loading without conversation history.
5. Identity preservation after reload.
6. Identity preservation across Runtime/Agent replacement.
7. Distinction between Process Instance identity and Execution Context state.
8. No accidental promotion of implementation fields into AESM semantics.
