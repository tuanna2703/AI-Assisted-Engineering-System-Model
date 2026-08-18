# Machine-Readable Agent Protocol

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 5 — Machine-Readable Agent Protocol  
**Status:** DRAFT — Phase 5 Consistency Correction  
**Authority:** Derived from the frozen Agent Execution Contract, AESM Operational Model, PEM, and EPM  
**Date:** 2026-08-18

---

## 1. Purpose

The Machine-Readable Agent Protocol (MRAP) defines the implementation-independent machine-readable representation of semantic interaction across the Agent Execution Contract boundary.

MRAP translates the frozen Agent Execution Contract into explicit protocol structures without redefining the semantics established by EPM, PEM, the AESM Operational Model, or the Contract.

MRAP is a representation boundary. It is not an authority layer, Runtime, Execution Context, engineering process, or transport implementation.

---

## 2. Governing Relationship

```text
EPM
 ↓ engineering meaning and validity
PEM
 ↓ execution semantics and control
AESM Operational Model
 ↓ authoritative operational representation
Agent Execution Contract
 ↓ permitted semantic interaction
Machine-Readable Agent Protocol
 ↓ machine-readable representation
Runtime / Agent / Environment implementation
```

The protocol shall remain subordinate to all preceding normative layers.

---

## 3. Normative Boundaries

The following invariants are mandatory:

- Agent ≠ Runtime.
- Agent capability ≠ authority.
- Agent output ≠ automatically authoritative state.
- Protocol representation ≠ semantic authority.
- Protocol message ≠ authoritative Execution Context.
- Message receipt ≠ automatic recognition.
- Recognition ≠ unrestricted mutation.
- Observation ≠ mutation.
- Participant Input ≠ automatic state mutation.
- Candidate Contribution ≠ authoritative engineering fact.
- Proposal ≠ authorization.
- Engineering Decision ≠ Execution Determination.
- Engineering completion ≠ Runtime termination.
- Protocol semantics ≠ transport semantics.
- Protocol structure ≠ implementation architecture.

No protocol field, message category, or successful exchange may by itself establish authority that the governing models do not grant.

---

## 4. Protocol Model

An MRAP interaction consists conceptually of:

```text
Interaction Envelope
        +
Semantic Operation
        +
Operation-specific Payload
        +
Context / Correlation References
        +
Traceability References
        +
Outcome / Failure information where applicable
```

The protocol representation is transient interaction data unless and until recognized by the Runtime under applicable EPM/PEM semantics.

The envelope schema establishes common structure. Operation-specific payload semantics are defined by this specification and may require operation-specific schema constraints in a conforming implementation.

---

## 5. Interaction Envelope

Every protocol interaction shall have an envelope containing, as applicable:

| Element | Meaning |
|---|---|
| `protocol` | Identifies the protocol family and version. |
| `message_id` | Unique identity of the protocol message. |
| `interaction_id` | Identity of the semantic interaction represented by the message. |
| `operation` | Protocol operation class and semantic operation name. |
| `direction` | Semantic information-flow direction relative to the Runtime. |
| `sender` | Actor/source producing the representation. |
| `recipient` | Intended semantic recipient. |
| `process_instance_ref` | Reference to the relevant Process Instance when applicable. |
| `execution_context_ref` | Reference to relevant authoritative context when permitted and applicable. |
| `causation_ref` | Reference to the interaction that caused this interaction, where applicable. |
| `trace_ref` | Reference supporting execution traceability. |
| `artifact_refs` | References to relevant artifacts or evidence when applicable. |
| `action_ref` | Reference to a relevant Execution Action when applicable. |
| `result_ref` | Reference to a relevant Execution Result or other result when applicable. |
| `verification_ref` | Reference to a relevant verification activity/result when applicable. |
| `payload` | Operation-specific semantic content. |
| `outcome` | Outcome information where the operation produces an outcome. |
| `failure` | Material failure or uncertainty information where applicable. |

The exact wire encoding of these elements is implementation-specific and is outside this specification.

---

## 6. Actor and Source Boundary

The protocol uses a neutral `actor/source` concept so that protocol representation does not collapse distinct semantic categories.

The normative categories are:

```text
Human Participant
AI Agent
Runtime
Tool
Environment
```

The semantic relationships are:

```text
Participant
├── Human Participant
└── AI Agent

Runtime

Other Source / Capability
├── Tool
└── Environment
```

An AI Agent is therefore a Participant.

A Tool or Environment source is not thereby a Participant and does not acquire Participant authority merely by being represented in a protocol message.

Runtime is neither a Participant nor an Agent. It is the execution mechanism implementing PEM.

Actor/source identity identifies the origin or intended recipient of information. It does not itself establish authority.

---

## 7. Direction

`direction` represents semantic information flow relative to the Runtime only.

The normative values are:

```text
to_runtime
from_runtime
```

`to_runtime` means that the represented information is flowing toward the Runtime from a source/actor.

`from_runtime` means that the represented information is flowing from the Runtime toward a recipient/source.

The direction field does not prescribe:

- whether the source is an Agent, Human Participant, Tool, or Environment;
- network direction;
- transport endpoint;
- API method;
- process/thread ownership;
- communication technology.

The sender and recipient categories provide the actor/source distinction independently of direction.

---

## 8. Context References

`process_instance_ref` identifies the Process Instance to which the interaction relates.

`execution_context_ref` identifies the relevant authoritative Execution Context when such a reference is applicable and permitted.

A context reference is not itself an Execution Context mutation.

The message carrying a context reference does not become authoritative merely because it contains a context identifier.

The Runtime determines how the referenced context is resolved under PEM semantics.

---

## 9. Operation Classes

The protocol defines the following semantic operation families.

### 9.1 Context Interaction

Used to request or provide information required to continue an interaction or resume work.

Examples include:

- context inspection request;
- continuation request;
- continuation result.

Context interaction shall preserve the distinction between protocol continuation information and authoritative Execution Context.

### 9.2 Observation Report

Represents an observation made by an Agent, Participant, Tool, or Environment.

An observation is information about something perceived or measured. It is not automatically an authoritative state mutation.

### 9.3 Participant Input

Represents information explicitly supplied by a Human Participant or AI Agent as a Participant.

Participant Input shall not be fabricated by an Agent and shall not automatically become authoritative state.

### 9.4 Candidate Contribution

Represents a candidate contribution offered for consideration.

A Candidate Contribution may contain analysis, evidence, interpretation, proposal, or other useful material, but it does not become an authoritative engineering fact merely because it is transmitted.

### 9.5 Proposal / Recommendation

Represents a proposed plan, decision, action, or other candidate determination.

```text
Proposal ≠ authorization
Proposal ≠ Engineering Decision
Proposal ≠ Execution Determination
```

### 9.6 Execution Interaction

Represents an interaction concerning permitted work or an execution action.

An Agent's representation of a requested action does not itself authorize execution. The Runtime applies applicable PEM control and authorization semantics.

### 9.7 Execution Result

Represents the result of an execution action.

The result may be evidence for subsequent processing, verification, or state mutation, but transmission of the result does not itself establish its authoritative interpretation.

### 9.8 Verification Result

Represents a verification activity result as reported by a Participant or other permitted source.

A protocol field or payload indicating that a source reports verification success is not itself authoritative recognition of that verification result. Recognition remains governed by the applicable EPM/PEM and Runtime semantics.

### 9.9 Failure / Uncertainty Report

Represents material failure, inability, uncertainty, contradiction, blocked progress, unmet preconditions, or inability to establish a reliable result.

Material uncertainty shall not be silently converted into certainty.

### 9.10 Reconsideration Signal

Represents information indicating that previously established reasoning, interpretation, or determination may require reconsideration.

A reconsideration signal does not erase historical state. It initiates applicable reconsideration under governing semantics.

---

## 10. Operation Classification

Every operation shall be classified according to its semantic effect.

At minimum:

```text
INFORMATIONAL
CANDIDATE
EXECUTION-RELATED
MUTATION-RELEVANT
OUTCOME
FAILURE
CONTINUATION
```

The classification describes the semantic role of the operation. It does not grant authority.

The normative operation-to-class mapping is:

| Operation | Required Class |
|---|---|
| `context_inspection` | `INFORMATIONAL` |
| `continuation` | `CONTINUATION` |
| `observation_report` | `INFORMATIONAL` |
| `participant_input` | `INFORMATIONAL` |
| `candidate_contribution` | `CANDIDATE` |
| `proposal` | `CANDIDATE` |
| `execution_request` | `EXECUTION-RELATED` or `MUTATION-RELEVANT` according to represented action semantics |
| `execution_result` | `OUTCOME` |
| `verification_result` | `OUTCOME` |
| `failure_uncertainty` | `FAILURE` |
| `reconsideration` | `CONTINUATION` |

A conforming schema or validator shall reject an operation/class combination that contradicts this mapping, except for the explicitly conditional `execution_request` classification.

---

## 11. Recognition Boundary

The protocol represents information exchanged across the Agent Execution Contract boundary.

The semantic processing path is:

```text
Protocol Representation
        ↓
Runtime-controlled interpretation
        ↓
Recognition under applicable EPM/PEM semantics
        ↓
Authorized State Mutation, if permitted
        ↓
Execution Context / Trace
```

A received message is therefore not equivalent to recognized authoritative information.

The protocol shall not define an independent recognition authority.

---

## 12. Mutation Boundary

A protocol interaction may carry information relevant to a potential mutation.

The following distinction is mandatory:

```text
Message carries mutation-relevant information
        ≠
Message mutates authoritative state
```

Mutation can occur only through the controlled execution path established by PEM and represented by the AESM Operational Model.

Historical state must remain reconstructable after mutation or reconsideration.

---

## 13. Authority Metadata

Where the protocol requires metadata describing authority, permission, recognition, or mutation classification, that metadata is descriptive of governing semantics.

It shall not create authority by declaration.

For example, a message field equivalent to `authorized: true` must never be interpreted as granting authority independently of the governing Runtime, EPM, and PEM rules.

Protocol metadata may communicate:

- requested action class;
- candidate mutation class;
- required recognition class;
- verification status as reported by a source;
- permission context reference.

The authoritative interpretation remains outside the protocol representation itself.

---

## 14. Payload Semantics

Payloads shall contain semantic content appropriate to the operation class.

A payload shall not silently mix semantically distinct categories when doing so would destroy distinctions required by the Contract.

For example, the protocol shall preserve distinctions among:

```text
observation
participant input
candidate contribution
proposal
execution request
execution result
verification result
failure / uncertainty
```

An implementation may use a common envelope or serialization mechanism, but semantic categories remain distinct.

The base schema intentionally leaves `payload.content` structurally open because payload structure is operation-specific. The normative operation semantics and required content are defined by this specification; specialized schemas may further constrain individual operation payloads without changing the protocol semantics.

---

## 15. Traceability

Material interactions shall expose sufficient references to support reconstruction of:

```text
Interaction
 → Contribution / Action
 → Result
 → Verification where applicable
 → Recognition
 → State Mutation where applicable
 → Execution Trace
```

Traceability references may include:

- interaction identity;
- causation;
- Process Instance reference;
- Execution Context reference;
- artifact/evidence references;
- action reference;
- result reference;
- verification reference.

The protocol shall not require conversational memory as the sole source of material interaction history.

---

## 16. Failure and Uncertainty

Failure and uncertainty are first-class protocol outcomes where materially relevant.

A failure representation may identify:

- failure class;
- affected operation;
- known cause or diagnostic information;
- whether retry/reconsideration may be appropriate;
- affected context/reference;
- uncertainty level where applicable.

An Agent must not fabricate a successful result when the underlying work failed or material uncertainty remains.

---

## 17. Continuity and Resumption

The protocol shall support controlled continuation across interaction boundaries.

A continuation interaction may carry:

- Process Instance reference;
- Execution Context reference;
- last-known interaction reference;
- relevant trace references;
- requested continuation point;
- continuation-specific information.

However:

```text
Continuation message
≠
Execution Context
```

The authoritative state remains owned by the execution system as defined by the Operational Model and PEM.

---

## 18. Versioning

Protocol messages shall identify the protocol version applicable to their representation.

Versioning shall not be used to redefine frozen EPM, PEM, Operational Model, or Contract semantics silently.

A semantic change that cannot remain compatible with the governing Contract requires change control at the appropriate authoritative layer before protocol adoption.

---

## 19. Transport Independence

MRAP does not prescribe transport.

Possible implementations may use APIs, message queues, streams, files, local calls, or other mechanisms, but such mechanisms are external to this specification.

Therefore:

```text
Transport
 ↓ carries
Protocol representation
 ↓ represents
Contract-defined interaction
```

not:

```text
Transport API
 ↓ defines
Protocol semantics
```

---

## 20. Implementation Independence

The protocol is independent of:

- programming language;
- serialization library;
- network stack;
- Agent framework;
- Runtime implementation;
- storage technology;
- deployment topology.

An implementation may add operational metadata, provided that such additions do not conflict with the normative protocol semantics.

---

## 21. Required Validation Invariants

A conforming implementation or schema validator shall be able to verify, as applicable:

1. every message has a valid protocol identity/version;
2. every message has an operation classification;
3. message identity is distinguishable from interaction identity;
4. sender/recipient categories preserve Human Participant, AI Agent, Runtime, Tool, and Environment distinctions;
5. direction represents information flow relative to Runtime and does not encode transport;
6. Process Instance references are structurally valid when required;
7. Execution Context references do not become embedded authoritative state;
8. operation classes preserve Contract distinctions;
9. mutation-relevant messages are not treated as automatic mutations;
10. proposal messages are not represented as authoritative decisions;
11. execution results are distinguishable from execution determinations;
12. verification results reported by sources remain distinguishable from authoritative recognition;
13. failures and uncertainty are representable;
14. continuity references support reconstruction without conversational memory;
15. transport-specific fields do not become normative semantic requirements;
16. material interactions remain traceable.

---

## 22. Contract Traceability Principle

Every normative protocol capability shall trace to an applicable governing Contract concept.

Conversely, every Contract interaction capability requiring machine-readable representation shall be represented by the protocol or have an explicit documented reason for non-representation.

The Phase 5 Contract-to-Protocol Traceability Matrix is the authoritative review artifact for this mapping.

The protocol specification itself does not replace that matrix.

---

## 23. Conformance Boundary

An implementation conforms to MRAP only if it:

- represents required protocol semantics;
- preserves required distinctions;
- does not grant authority through protocol representation;
- preserves traceability;
- supports required failure/uncertainty semantics;
- preserves continuity requirements;
- does not depend on a particular transport to establish semantic validity.

Implementation-specific extensions may exist outside the normative core.

---

## 24. Relationship to Frozen Contract

The Agent Execution Contract remains authoritative for Agent interaction semantics.

MRAP is subordinate to it:

```text
Agent Execution Contract
        ↓ defines
permitted semantic interaction
        ↓ represented by
Machine-Readable Agent Protocol
```

If a conflict is discovered between MRAP and the frozen Contract, MRAP is defective and shall be corrected through the Phase 5 revision process.

The conflict shall not be resolved by silently changing the Contract.

---

## 25. Status

This document is currently:

> **DRAFT — PHASE 5 CONSISTENCY CORRECTION**

It is not yet authoritative and is not frozen.

Required next activities:

1. re-run Consistency Review;
2. perform mandatory Boundary Review;
3. perform structural and semantic validation;
4. correct and revalidate any defects;
5. conduct Freeze Review;
6. canonicalize and freeze if all criteria pass.
