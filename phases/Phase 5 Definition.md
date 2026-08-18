# Phase 5 Definition

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 5 — Machine-Readable Agent Protocol  
**Artifact Type:** Phase Governance / Definition  
**Status:** DEFINED — Construction Authorized  
**Date:** 2026-08-18

---

## 1. Purpose

Phase 5 defines the **Machine-Readable Agent Protocol** layer of AESM.

Its purpose is to translate the frozen **Agent Execution Contract** into a machine-readable protocol specification that can represent Agent↔AESM interaction while preserving the authority, semantic, and execution boundaries established by the frozen EPM, PEM, AESM Operational Model, and Agent Execution Contract.

Phase 5 is therefore a **representation/protocol phase**, not a semantic redesign phase.

The protocol shall make the Contract operationally expressible without changing what the Contract means.

---

## 2. Normative Objective

The Phase 5 objective is:

> **Define a machine-readable Agent Protocol that faithfully represents the frozen Agent Execution Contract and its permitted interaction semantics, while preserving the authority of EPM, PEM, and the AESM Operational Model and avoiding accidental Runtime, engineering, or implementation authority leakage.**

The protocol shall provide a precise machine-readable boundary for Agent↔AESM information exchange.

---

## 3. Scope

Phase 5 shall define, as applicable:

1. protocol message categories;
2. message/envelope identity and correlation;
3. protocol-level interaction direction;
4. request, contribution, proposal, result, failure, and continuation representations;
5. representation of relevant Agent Execution Contract concepts;
6. operation references and semantic intent;
7. required context references;
8. authority/recognition metadata where required;
9. mutation classification where applicable;
10. traceability requirements;
11. failure and uncertainty representation;
12. continuity and resumption information exchange;
13. protocol validation rules;
14. machine-readable schemas and vocabulary constraints;
15. protocol-to-Contract traceability.

The exact concrete message taxonomy shall be established during construction from the Contract rather than assumed to be a generic request/response API model.

---

## 4. Explicit Non-Scope

Phase 5 shall **not** define or redefine:

- EPM engineering semantics;
- PEM execution semantics;
- AESM Operational Model semantics;
- Agent authority;
- Runtime authority;
- Engineering Decision recognition rules;
- Execution Determination semantics;
- authoritative Execution Context semantics;
- engineering progression conditions;
- Runtime architecture;
- Agent architecture;
- storage architecture;
- authentication/identity security policy;
- deployment architecture;
- provider-specific Agent APIs;
- tool-specific invocation protocols;
- a particular transport such as HTTP, WebSocket, RPC, or message queue.

Transport and implementation mechanisms may later bind to the protocol, but they shall remain subordinate to the protocol semantics and governing baselines.

---

## 5. Layer Boundary

The Phase 5 layer is explicitly positioned as:

```text
EPM
  ↓ engineering meaning and validity
PEM
  ↓ execution semantics and control
AESM Operational Model
  ↓ authoritative operational representation
Agent Execution Contract
  ↓ semantic interaction boundary
Machine-Readable Agent Protocol
  ↓ machine-readable interaction representation
Runtime / Agent / Environment implementations
```

The protocol is **not** an alternative authority layer.

It may represent authority, permissions, mutation class, or recognition requirements, but those properties must be derived from the governing semantics rather than invented by the protocol.

---

## 6. Protocol vs Contract Boundary

The Phase 4 Contract intentionally did not define message structures or transport operations. Phase 5 is the authorized layer at which machine-readable interaction structures are introduced.

Therefore:

```text
Contract
= what interaction means and what is permitted

Protocol
= how that interaction is represented in machine-readable form

Transport
= how protocol representations are physically conveyed
```

Phase 5 may define protocol structures, but it shall not silently turn those structures into a transport API or implementation architecture.

---

## 7. Governing Inputs

Phase 5 shall use the following authoritative inputs:

- frozen EPM;
- frozen PEM;
- frozen AESM Operational Model;
- frozen Phase 3 machine-readable model and schema;
- frozen Phase 4 Boundary Matrix;
- frozen Phase 4 Agent Execution Contract;
- Phase 4 Contract Review;
- Phase 4 Freeze Review;
- frozen Phase Lifecycle Workflow;
- relevant validation and historical evidence from prior phases.

The current machine-readable Operational Model already establishes a machine-readable representation and schema boundary for the operational layer. Phase 5 shall extend that machine-readable discipline to Agent interaction without redefining the Operational Model.

---

## 8. Required Phase 5 Artifacts

Phase 5 shall produce, at minimum:

### 8.1 Primary specification

`specifications/Machine-Readable Agent Protocol.md`

This document shall define the normative protocol model, semantics, message categories, relationships, invariants, and protocol-level rules.

### 8.2 Machine-readable protocol schema

A machine-readable schema representing the normative protocol structures, subject to the chosen schema technology and the phase validation requirements.

### 8.3 Contract-to-Protocol Traceability Matrix

A review artifact mapping each normative Agent Execution Contract capability/boundary to its protocol representation and identifying any Contract concept that intentionally has no direct protocol representation.

### 8.4 Protocol Validation Report

A validation artifact recording structural, semantic, authority, mutation, traceability, and continuity checks performed against the protocol.

### 8.5 Freeze artifacts

If Phase 5 reaches freeze:

- Phase 5 Completeness Review;
- Phase 5 Consistency Review;
- Phase 5 Boundary Review;
- Phase 5 Validation Report;
- Phase 5 Freeze Review;
- canonicalization/freeze record.

---

## 9. Protocol Representation Requirements

The protocol shall be capable of representing, as applicable:

### 9.1 Interaction identity

- protocol interaction identity;
- message identity;
- correlation/reference information;
- protocol/version identity.

### 9.2 Participant identity/context

The protocol shall distinguish the participating Agent/Participant from the Runtime and shall not encode Agent identity as Runtime authority.

### 9.3 Semantic intent

A protocol representation shall identify what semantic interaction is being requested, contributed, proposed, reported, or continued.

### 9.4 Context reference

Where interaction depends on authoritative Process Instance or Execution Context state, the protocol shall provide sufficient reference/context information without making the message itself the authoritative Execution Context.

### 9.5 Contribution classification

The protocol shall preserve distinctions including, where applicable:

```text
Observation
Participant Input
Candidate Contribution
Proposal / Recommendation
Execution Request
Execution Result
Verification Result
Failure / Uncertainty
Continuity / Resumption information
```

These categories shall not be collapsed merely because they share a transport representation.

### 9.6 Recognition and mutation

Where a protocol interaction can lead toward state mutation, the protocol representation shall make the relevant mutation/recognition classification explicit enough for the receiving execution system to apply the governing rules.

The protocol shall not itself authorize mutation merely by carrying a mutation-related field.

### 9.7 Traceability

Material protocol interactions shall be traceable to the applicable Process Instance, interaction, contribution, action, result, or state update as required by the Contract and Operational Model.

### 9.8 Failure and uncertainty

The protocol shall support explicit representation of uncertainty, contradiction, blocked conditions, failed verification, unmet preconditions, inability to continue, and other material failure conditions defined by the Contract.

### 9.9 Continuity

The protocol shall support the information required for controlled continuation and resumption, while preserving the distinction:

```text
Protocol continuation data
≠
Authoritative Execution Context
```

---

## 10. Authority Preservation Requirements

The protocol shall preserve at least these invariants:

1. Agent ≠ Runtime.
2. Agent capability ≠ authority.
3. Agent output ≠ automatically authoritative state.
4. Proposal ≠ authorization.
5. Observation ≠ mutation.
6. Participant Input ≠ automatic state mutation.
7. Candidate Contribution ≠ authoritative engineering fact.
8. Engineering Decision ≠ Execution Determination.
9. Protocol representation ≠ semantic authority.
10. Protocol message ≠ authoritative Execution Context.
11. Message receipt ≠ automatic recognition.
12. Recognition ≠ unrestricted mutation.
13. Historical state remains reconstructable.
14. Material uncertainty remains explicit.
15. Transport implementation does not redefine protocol semantics.

---

## 11. Protocol Operation Classes

The protocol shall define operation classes derived from the Contract. The final taxonomy shall be validated during construction, but shall cover the semantic families required by the Contract, such as:

- context inspection / continuation;
- information contribution;
- observation reporting;
- candidate contribution submission;
- proposal/recommendation submission;
- execution request or permitted-work interaction;
- execution-result reporting;
- verification-result reporting;
- failure/uncertainty reporting;
- reconsideration signalling where applicable.

Operation classes shall distinguish informational interactions from mutation-capable interactions.

The protocol shall not imply that every represented operation is executable by every Agent.

---

## 12. Schema and Validation Requirements

Phase 5 validation shall include, as applicable:

### Structural validation

- schema conformance;
- required/optional field correctness;
- type correctness;
- identifier and reference correctness;
- version correctness;
- prohibited additional structures where required.

### Semantic validation

- Contract coverage;
- Operational Model consistency;
- EPM/PEM consistency;
- operation semantics;
- distinction preservation;
- authority-path preservation.

### Boundary validation

- Agent/Runtime separation;
- capability/authority separation;
- semantic/protocol/transport separation;
- observation/mutation separation;
- engineering/execution authority separation.

### Traceability validation

- protocol element → Contract rule;
- protocol operation → applicable semantic operation;
- protocol result → trace requirements;
- continuation interaction → continuity requirements.

### Reconstruction validation

The protocol shall support sufficient information exchange to reconstruct the intended semantic interaction and its relationship to authoritative execution state without requiring undocumented conversational assumptions.

---

## 13. Phase-Specific Boundary Review

Boundary Review is **mandatory** for Phase 5.

The reason is that Phase 5 explicitly crosses the boundary from semantic interaction contract to machine-readable protocol representation.

The review shall pay particular attention to accidental leakage of:

- Runtime authority into Agent messages;
- engineering authority into protocol fields;
- authorization semantics into mere message presence;
- transport assumptions into normative protocol semantics;
- authoritative state into transient message content;
- implementation-specific APIs into the implementation-independent protocol definition.

---

## 14. Acceptance Criteria

Phase 5 shall be considered complete only when:

1. the normative Machine-Readable Agent Protocol specification exists;
2. all material Contract interaction capabilities have a defined protocol representation or explicit documented non-representation rationale;
3. protocol structures are machine-readable and schema-valid;
4. protocol semantics are consistent with the frozen Agent Execution Contract;
5. protocol semantics are consistent with the frozen Operational Model;
6. EPM/PEM authority is preserved;
7. Agent/Runtime separation is preserved;
8. capability/authority separation is preserved;
9. observation/mutation separation is preserved;
10. Engineering Decision / Execution Determination distinction is preserved;
11. semantic protocol/transport separation is preserved;
12. continuity and traceability requirements are represented;
13. failure and uncertainty can be represented without fabrication or silent suppression;
14. protocol validation passes;
15. Boundary Review passes;
16. no unresolved material defect remains;
17. canonical artifact(s) are identified before freeze;
18. historical evidence is preserved.

Completion shall not itself imply freeze.

---

## 15. Freeze Prerequisites

Before Phase 5 Freeze Eligibility, the following shall be satisfied:

- required Phase 5 artifacts exist;
- Completeness Review passes;
- Consistency Review passes;
- mandatory Boundary Review passes;
- protocol validation passes;
- Contract-to-Protocol traceability is complete;
- material defects are resolved or formally dispositioned;
- canonical artifacts are identified;
- competing drafts are dispositioned;
- previous frozen baselines remain unchanged unless separately governed by change control;
- historical review/validation evidence is preserved;
- downstream implications are sufficiently understood.

---

## 16. Known Dependency Condition

Repository inspection during Phase Definition identified a repository-level housekeeping discrepancy: an older root-level `Agent Execution Contract.md` remains present alongside the canonical frozen `specifications/Agent Execution Contract.md`.

The canonical Phase 4 Contract is explicitly the specification-layer artifact. The root-level file is non-canonical, but its continued presence contradicts the previously recorded housekeeping statement that the duplicate had been resolved.

This is not treated as a semantic defect in the frozen Contract. However, the discrepancy shall be resolved or explicitly dispositioned before Phase 5 Freeze Eligibility so that protocol traceability has one unambiguous canonical Contract source.

Phase 5 construction shall use:

`specifications/Agent Execution Contract.md`

as the sole normative Contract source.

---

## 17. Phase Status

Phase 5 has completed Entry and Definition:

```text
Not Started
   ↓
Entered
   ↓
Defined          ← current status
   ↓
In Progress
   ↓
Under Review / Validation
   ↓
Freeze Eligible
   ↓
Frozen
```

Current status:

> **DEFINED — Construction Authorized**

The next authorized activity is **Phase 5 Construction / Work**.

---

## 18. Definition Decision

The Phase 5 objective, scope, required artifacts, boundaries, validation requirements, acceptance criteria, and freeze prerequisites have been explicitly established.

**Definition Status: PASS**  
**Phase Status: DEFINED**  
**Next Stage: PHASE 5 CONSTRUCTION / WORK**
