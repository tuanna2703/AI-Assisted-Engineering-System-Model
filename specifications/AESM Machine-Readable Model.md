# AESM Machine-Readable Model

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 3 — Machine-Readable AESM Model  
**Status:** Candidate — Implementation Baseline  
**Version:** 0.1.0  
**Derived from:** `specifications/AESM Operational Model.md`

---

## 1. Purpose

The AESM Machine-Readable Model defines the canonical software-consumable representation of the AESM Operational Model.

Its purpose is to make the operational semantics explicit to software without requiring software to interpret the Markdown specification directly.

The Machine-Readable Model is a **model definition**, not an engineering Process Instance. It defines the operational entity vocabulary, field semantics, relationships, operation classes, and operational invariants from which later Runtime data schemas and interfaces can be derived.

It MUST preserve the semantic authority of the EPM and PEM and MUST NOT introduce implementation-specific Runtime, Agent, protocol, database, or environment semantics.

---

## 2. Scope

Phase 3 covers:

1. canonical machine-readable model identity and versioning;
2. serialization rules;
3. entity vocabulary;
4. entity identity strategy;
5. field/type/cardinality representation;
6. typed relationships;
7. operation-class representation;
8. operational invariant representation;
9. extension boundaries;
10. structural validation of the machine-readable model itself;
11. repository artifact organization.

Phase 3 does **not** define:

- Agent request/response messages;
- Agent authority or execution contract details;
- protocol transport;
- Runtime API;
- environment capability API;
- physical Process Instance storage;
- conformance test implementation;
- IDE integration.

Those belong to later phases.

---

## 3. Relationship to the Operational Model

The authority chain is:

```text
EPM
  ↓
PEM
  ↓
AESM Operational Model
  ↓
AESM Machine-Readable Model
```

The Machine-Readable Model is a representation of the Operational Model. It is not a replacement for the Operational Model and MUST NOT redefine its semantics.

If a machine-readable artifact conflicts with the Operational Model, the artifact is non-conforming and MUST be corrected rather than used to redefine the Operational Model.

The Machine-Readable Model therefore has a **representation authority**, not an independent engineering authority.

---

## 4. What Constitutes the Machine-Readable AESM Model

The Phase 3 model consists of two normative artifact classes:

### 4.1 Model Schema

The model schema defines the structure of a valid Machine-Readable AESM Model document.

Artifact:

`schemas/aesm-machine-readable-model.schema.json`

The schema uses JSON Schema Draft 2020-12.

### 4.2 Canonical Model Definition

The canonical model definition is the machine-readable representation of the current AESM Operational Model.

Artifact:

`model/aesm-operational-model.json`

It defines the entities, relationships, operation classes, and invariants that software must understand to consume the operational model.

These two artifacts have different responsibilities:

```text
Model Schema
= validates the shape of the machine-readable model

Canonical Model Definition
= represents AESM operational semantics in machine-readable form
```

---

## 5. One Model, Multiple Schemas

AESM uses **one canonical operational model definition** rather than multiple competing model definitions.

The canonical model is decomposed into entity definitions internally, but those definitions remain members of one coherent model identified by:

```text
modelId = aesm.operational-model
modelVersion = MAJOR.MINOR.PATCH
```

Later Runtime data schemas MAY be split into multiple files for maintainability or implementation purposes. Such schemas MUST derive from this canonical model and MUST NOT become independent semantic authorities.

This establishes:

```text
One canonical semantic model
        ↓
Multiple derived implementation schemas, where useful
```

---

## 6. Serialization Strategy

### 6.1 Canonical Format

The Phase 3 canonical serialization format is **JSON encoded as UTF-8**.

JSON is selected because it provides:

- broad software support;
- deterministic machine-readable structure;
- direct compatibility with JSON Schema;
- straightforward interchange;
- suitability for later protocol and Runtime layers.

The choice of JSON is a serialization decision for Phase 3. It does not require a specific Runtime architecture.

### 6.2 Schema Dialect

The normative schema dialect is:

`https://json-schema.org/draft/2020-12/schema`

### 6.3 Human-Readable Specifications

Markdown remains the normative human-readable specification format.

The relationship is therefore:

```text
Markdown specification
        ↓
Machine-readable representation
```

Neither format silently supersedes the other.

---

## 7. Identity and Versioning

### 7.1 Model Identity

The canonical model has the stable identifier:

`aesm.operational-model`

Entity kinds use stable symbolic names such as:

- `ProcessInstance`
- `ExecutionContext`
- `Requirement`
- `EngineeringDecision`
- `ExecutionAction`
- `ExecutionTrace`

### 7.2 Entity Identity

Operational entities MUST use stable opaque identities.

The identity strategy MUST NOT require database-generated numeric IDs, filesystem paths, IDE identifiers, or Runtime-local object addresses.

An implementation MAY encode identities differently internally provided the externally represented identity remains stable within its intended scope.

### 7.3 Versioning

The model and schema use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

A change that breaks the meaning or compatibility of existing machine-readable consumers requires a MAJOR version change.

A backward-compatible addition requires a MINOR version change.

A correction that does not change the intended model semantics or compatibility contract requires a PATCH version change.

### 7.4 Specification References

The machine-readable model MUST identify the source specifications from which it is derived, including the EPM, PEM, and AESM Operational Model.

---

## 8. Entity Representation

Each entity definition MUST identify:

- entity kind;
- identity field and identity strategy;
- fields;
- field types;
- required/optional status;
- cardinality where relevant;
- reference targets where relevant;
- controlled vocabularies where required.

The machine-readable model MUST retain the semantic identity of AESM entities.

It MUST NOT collapse distinct concepts into generic structures merely for implementation convenience.

For example:

```text
EngineeringDecision
≠ ExecutionDetermination

ParticipantInput
≠ ParticipantContribution

TransitionRule
≠ Transition

EngineeringTraceability
≠ ExecutionTrace
```

---

## 9. Relationship Representation

Relationships are represented explicitly rather than inferred solely from arbitrary field names.

Each relationship definition identifies:

- relationship type;
- source entity;
- target entity;
- cardinality;
- whether the relationship is required.

This allows software to distinguish entity existence from relationship semantics.

Examples include:

```text
ProcessInstance → ExecutionContext
ProcessInstance → EngineeringObjective
ProcessState → TransitionRule
Transition → TransitionRule
Evidence → EngineeringDecision
ExecutionAction → ExecutionResult
Participant → ParticipantContribution
ExecutionTrace → ProcessInstance
```

A Runtime MAY store these relationships using references, embedded objects, database relations, or another physical representation, provided the semantic relationships remain recoverable.

---

## 10. Validation Representation

Phase 3 separates three concerns:

### Structural Model Validation

The model schema determines whether the machine-readable model document has valid structure, types, required properties, and controlled vocabularies.

### Semantic Validation

The model definition identifies semantic relationships and invariants that later Runtime validation must preserve.

### Execution Validation

PEM-derived execution validation remains a Runtime responsibility and is not replaced by JSON Schema.

Therefore:

```text
JSON Schema
= structural validation

Operational Model
= semantic operational rules

PEM Runtime
= execution validation
```

JSON Schema MUST NOT be treated as sufficient to establish engineering validity.

---

## 11. Operational Invariants

The canonical machine-readable model explicitly represents the Operational Model invariants.

Each invariant has:

- stable invariant identity;
- normative statement;
- ownership layer;
- enforcement classification.

The model includes the distinctions established by Phase 2, including:

- EPM authority;
- PEM execution authority;
- Execution Context authority;
- Agent/Runtime separation;
- Engineering Decision/Execution Determination separation;
- Engineering Completion/Runtime Termination separation;
- knowledge-state distinctions;
- non-mutating observation;
- traceability;
- continuity;
- controlled mutation;
- reconsideration history;
- condition-driven progression;
- objective integrity;
- Requirement resolution versus satisfaction.

---

## 12. Extension Rules

The model supports explicit extensions without allowing extensions to silently redefine core semantics.

An extension MUST:

1. have a stable extension identifier;
2. declare its purpose;
3. use an identifiable namespace where appropriate;
4. avoid redefining a core entity, relationship, or invariant;
5. remain distinguishable from the canonical model;
6. preserve forward compatibility where possible.

Extensions MAY add implementation-specific properties or domain-specific entities, but MUST NOT change the meaning of a core AESM entity.

---

## 13. Repository Artifact Structure

Phase 3 establishes the following structure:

```text
specifications/
└── AESM Machine-Readable Model.md

schemas/
└── aesm-machine-readable-model.schema.json

model/
└── aesm-operational-model.json
```

The separation is intentional:

```text
specifications/
= normative human-readable semantics

schemas/
= machine validation structures

model/
= canonical machine-readable semantic model
```

This structure does not prescribe how an eventual Runtime stores engineering Process Instances.

---

## 14. Derivation of Later Runtime Data Schemas

Phase 3 establishes the semantic source from which later implementation schemas can be derived.

The intended derivation is:

```text
Canonical Operational Model
        ↓
Entity definitions + relationships + invariants
        ↓
Runtime data schemas
        ↓
Agent Execution Contract
        ↓
Agent Protocol
```

Later schemas MAY separate entities into individual files, but they MUST remain derivable from the canonical model.

The Runtime MUST NOT introduce a second, conflicting definition of AESM operational entities.

---

## 15. Conformance Expectations for Phase 3

A Phase 3 implementation is conforming when:

1. the canonical model is valid JSON;
2. the canonical model validates against the Phase 3 model schema;
3. the model identifies EPM, PEM, and Operational Model sources;
4. all primary Operational Model entity classes are represented;
5. entity identity is explicit and stable;
6. relationships are explicitly represented;
7. operation classes are represented without becoming API definitions;
8. Operational Model invariants are represented;
9. JSON Schema is used only for structural validation;
10. engineering validity remains owned by EPM;
11. execution semantics remain owned by PEM;
12. the Agent/Runtime boundary is preserved;
13. the model is implementation-independent;
14. extensions cannot silently redefine core semantics;
15. the model can serve as the machine-readable semantic source for Phase 4.

---

## 16. Phase 3 Freeze Criteria

Phase 3 may be frozen when review confirms that:

- the machine-readable model faithfully represents the frozen Operational Model;
- no core operational entity has been omitted;
- no critical distinction has been collapsed;
- relationships required for operational interpretation are explicit;
- identity and versioning are stable and documented;
- serialization and validation strategy are explicit;
- the canonical model validates structurally;
- later Runtime schemas can be derived without inventing core operational semantics;
- the model does not prematurely define the Agent Execution Contract or protocol;
- the repository structure clearly separates specifications, schemas, and the canonical model;
- the resulting artifacts provide a sufficient machine-readable foundation for Phase 4.

If these criteria are satisfied, the project may proceed to **Phase 4 — Agent Execution Contract**.
