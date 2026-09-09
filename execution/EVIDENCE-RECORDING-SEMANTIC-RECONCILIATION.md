# Evidence Recording Semantic Reconciliation

## Purpose

This document establishes the implementation boundary for the next controlled Runtime work unit: **Evidence Recording Implementation**.

It is an implementation-oriented reconciliation, not a new normative AESM specification. The existing AESM documentation remains authoritative. No change to the frozen conceptual baseline is justified by the current evidence.

## Current semantic basis

The existing AESM model already defines Evidence as a core engineering concept and as part of authoritative operational knowledge.

Evidence is information used to support engineering conclusions and Engineering Decisions. It may originate from documentation, source code, experiments, measurements, stakeholders, operational systems, or other appropriate sources.

Evidence must remain distinguishable from assumptions and unsupported claims.

Investigation is objective-driven and exists to gather sufficient evidence to support confident engineering decisions or conclusions.

Engineering Decisions should remain traceable to the Evidence, Requirements, Constraints, evaluation, and other reasoning that support them.

Verification also produces Evidence for progression decisions.

The Execution Context may contain Evidence as part of the Process Instance's knowledge state, while historical/traceability information preserves material evidence and its relationship to execution and engineering conclusions.

These semantics are already present in the current documentation set and do not require expansion merely to implement a minimal recording capability.

## Semantic distinction: contribution versus accepted evidence

The Runtime must preserve the distinction between:

```text
Agent / Participant contribution
        ↓
Runtime interpretation / recognition
        ↓
Evidence recognized as relevant under applicable semantics
        ↓
Authoritative recording where applicable
        ↓
Traceability to the engineering situation
```

A submitted statement, observation, document, experiment result, or Agent assertion is not automatically authoritative Evidence merely because it was received.

Recognition does not itself establish truth, sufficiency, verification, authorization, or engineering validity.

The Runtime must therefore not silently convert arbitrary Agent output into authoritative Evidence.

## Minimum semantic content

AESM does not prescribe a universal Evidence schema. The implementation must nevertheless retain enough information to preserve the meaning of a recorded evidence item within the current Process Instance.

At minimum, the implementation should be able to distinguish:

- the evidence content or representation;
- its source/provenance where available and material;
- its relationship to the current Process Instance;
- the engineering concern, requirement, constraint, decision, verification, or investigation context it supports where applicable;
- its recognition/recording status where the implementation distinguishes candidate information from accepted authoritative knowledge;
- material time/order information where required for reconstruction;
- material relationships to other recorded process knowledge.

These are semantic information requirements, not a prescribed field-level data model.

## Evidence versus adjacent concepts

### Evidence and assumptions

An Assumption is a proposition accepted without sufficient Evidence.

Recording an assumption must not silently convert it into Evidence.

### Evidence and unsupported claims

A claim or assertion may be contributed by an Agent or Participant without being established as Evidence.

The Runtime must preserve this distinction where the applicable process semantics require it.

### Evidence and observations

An observation is an input or contribution received during execution. An observation may become relevant Evidence after recognition and applicable engineering interpretation, but receipt alone does not establish that result.

### Evidence and artifacts

Artifacts are persistent representations of engineering knowledge. An Artifact may provide Evidence, contain Evidence, or be the object being evaluated, but Artifact existence alone does not establish engineering validity.

### Evidence and verification

Verification evaluates whether an Artifact, Decision, result, or Process State satisfies applicable requirements and conditions. Verification produces Evidence for progression decisions.

Verification is therefore not interchangeable with Evidence; it is an engineering evaluation activity whose result may itself become Evidence.

### Evidence and Engineering Decisions

Evidence supports Engineering Decisions. Evidence is not itself an Engineering Decision.

The Runtime must not collapse the evidence-to-decision relationship by treating a recorded evidence item as an accepted engineering conclusion.

## Authority boundary

The Agent or Participant may provide Evidence candidates and supporting information.

The Runtime controls recognition and authoritative operational-state mutation according to applicable EPM/PEM semantics.

The Runtime must not become the source of engineering judgment. Recording Evidence does not mean the Runtime determines whether the engineering conclusion supported by that Evidence is correct.

Conversely, the Agent must not be able to bypass Runtime-controlled authoritative persistence merely by asserting that information is Evidence.

## Persistence boundary

Evidence that is part of the authoritative knowledge state required for continuation must be persisted in the authoritative Process Instance/Execution Context representation.

Material evidence history must remain reconstructable when required for traceability, reconsideration, verification, or recovery.

The implementation must not rely on transient Agent memory, conversation history, or Runtime-local memory as the authoritative store for recorded Evidence.

The persistence mechanism remains implementation-dependent.

## Mutation boundary

Recording Evidence is an authoritative state mutation when the applicable semantics establish the submitted information as recorded process knowledge.

Therefore the Runtime must preserve the established mutation sequence:

```text
Input / contribution
        ↓
Interpretation
        ↓
Recognition
        ↓
Applicable conditions
        ↓
Permitted mutation
        ↓
Updated Execution Context
        ↓
Traceability
```

If authoritative Evidence cannot be recorded consistently, the Runtime must reject, defer, or explicitly represent the failure rather than leaving a partially committed state.

This follows the existing authoritative-state consistency requirement; it does not introduce a new persistence model.

## Traceability boundary

Evidence recording must preserve the relationships needed to reconstruct why the evidence matters.

At minimum, material recorded Evidence should remain traceable to the relevant Process Instance and, where applicable, to:

```text
Requirement / Objective
        ↓
Investigation / Observation
        ↓
Evidence
        ↓
Evaluation
        ↓
Engineering Decision
        ↓
Implementation / Artifact
        ↓
Verification
```

The implementation need not materialize this entire graph for every evidence item. It must not, however, destroy material relationships that the applicable Process Instance needs for continuation or engineering traceability.

## Continuity requirements

A replacement Agent must be able to recover recorded Evidence from authoritative Process Instance state without depending on the previous conversation.

Evidence therefore belongs to persistent process knowledge when it is material to the ongoing engineering execution.

Recovery must preserve the distinction between:

- previously recorded Evidence;
- unresolved questions;
- assumptions;
- new contributions awaiting recognition;
- conclusions already established.

## Reconsideration requirements

New Evidence may justify reconsidering an earlier Requirement interpretation, Candidate Solution, Engineering Decision, implementation choice, or verification conclusion.

Recording new Evidence must not erase the historical existence or basis of earlier conclusions.

The implementation must therefore support additive or otherwise historically reconstructable evidence evolution rather than silently replacing prior evidence history with only the latest value.

## What this work unit does not establish

This reconciliation does **not** establish:

- a universal Evidence database schema;
- a mandatory Evidence API shape;
- a particular storage engine;
- a universal evidence taxonomy;
- automatic truth verification;
- automatic confidence scoring;
- automatic source credibility scoring;
- a requirement that every Agent response become an Evidence record;
- a new EPM state;
- a new PEM transition;
- a new lifecycle state;
- a generalized knowledge graph.

Those would be semantic or architectural expansions not justified by the current implementation objective.

## Minimum Runtime capability boundary

The next implementation should provide only the smallest Runtime capability necessary to:

1. receive an Evidence contribution;
2. associate it with the correct Process Instance;
3. recognize whether it is recordable under the applicable process semantics;
4. persist the resulting authoritative Evidence state consistently;
5. preserve required provenance/context and traceability;
6. make the recorded Evidence recoverable through Execution Context;
7. avoid silently converting assumptions, claims, or arbitrary Agent output into authoritative Evidence.

The Runtime should not evaluate the engineering truth of the Evidence merely because it records it. Engineering interpretation remains governed by the applicable EPM and performed through the appropriate Agent/Participant and process semantics.

## Required validation boundary

Before Evidence Recording Implementation is marked complete, validation should demonstrate at least:

- successful recording of a valid evidence contribution;
- persistence across Runtime replacement/session loss;
- recovery of the recorded evidence from authoritative state;
- distinction between evidence and assumptions/unsupported claims where the slice requires it;
- traceability to the relevant engineering context;
- failure-safe persistence without partial authoritative mutation;
- preservation of prior evidence when new evidence is recorded or reconsideration occurs;
- no unauthorized Process State, lifecycle, or Engineering Decision mutation caused merely by recording evidence.

## Reconciliation conclusion

**Semantic status: Sufficiently defined for minimal implementation.**

The current AESM documentation provides enough semantic basis to implement Evidence Recording without expanding the normative model.

The next step is therefore **implementation of the minimum Runtime Evidence Recording capability**, followed by targeted behavioral and persistence validation.
