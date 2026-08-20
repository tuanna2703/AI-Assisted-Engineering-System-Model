# AI-Assisted Engineering System Model (AESM)

## Documentation

This directory is the canonical documentation set for AESM.

AESM is a system model for persistent, governed engineering execution in which an Engineering Process Model defines engineering meaning, a Process Execution Model defines execution semantics, and a Runtime executes persistent Process Instances through replaceable Execution Environments with Human and AI Agent participation.

The documentation is organized around **what a reader needs to understand**, rather than around the historical documents from which the model was developed.

## Start here

1. **[AESM Overview](01-Overview.md)** — what AESM is, why it exists, and its defining properties.
2. **[System Model](02-System-Model.md)** — entities, relationships, boundaries, and authority.
3. **[Engineering Model](03-Engineering-Model.md)** — what engineering work means in AESM.
4. **[Execution Model](04-Execution-Model.md)** — how engineering work is executed.
5. **[Process Instance and Execution Context](05-Process-Instance-and-Execution-Context.md)** — the persistent unit of work and its authoritative operational state.
6. **[Participants and Agent Participation](06-Participants-and-Agent-Participation.md)** — Human and AI participation and the Agent boundary.
7. **[Runtime and Conformance](07-Runtime-and-Conformance.md)** — Runtime responsibilities and conformance obligations.
8. **[Continuity, Traceability, and Reconsideration](08-Continuity-Traceability-and-Reconsideration.md)** — persistence, recovery, history, and controlled change.
9. **[Operational Guide](09-Operational-Guide.md)** — how the pieces work together during an engineering effort.
10. **[Reference](10-Reference.md)** — terminology, distinctions, invariants, and quick-reference relationships.
11. **[Documentation Source Map](11-Documentation-Source-Map.md)** — traceability from the former documentation into the unified set.
12. **[AI Agent Guide](12-AI-Agent-Guide.md)** — how an AI Agent should understand and participate in AESM.
13. **[Runtime Implementer Guide](13-Runtime-Implementer-Guide.md)** — implementation-oriented guidance for Runtime developers.

## Reading paths

### New to AESM

`Overview → System Model → Operational Guide → Reference`

### Engineer using AESM

`Overview → Engineering Model → Execution Model → Operational Guide`

### AI Agent

`Overview → System Model → AI Agent Guide → Execution Model → Continuity`

### Runtime implementer

`System Model → Execution Model → Process Instance and Execution Context → Runtime and Conformance → Runtime Implementer Guide`

### Need a precise definition

Use **Reference** first, then follow the concept to the governing model.

## Documentation status and authority

This is a **unified replacement documentation set**. The former `docs/` and `specifications/` document organization is no longer part of the canonical AESM knowledge surface.

The documents contain both explanatory and normative material. Explanatory material exists to make AESM understandable; normative statements define or preserve AESM semantics and must not be weakened by implementation convenience.

The conceptual authority relationship is:

```text
Engineering Process Model (EPM)
        ↓ engineering meaning and validity
Process Execution Model (PEM)
        ↓ execution semantics
Runtime
        ↓ concrete execution
Process Instance + Execution Context
        ↓ operational state
Human / AI Participants
        ↓ contributions and actions
Execution Environment
        ↓ interaction and tooling surface
```

The distinction between these layers is fundamental. In particular:

- EPM is not PEM.
- PEM is not a Runtime implementation.
- A Runtime is not an Agent.
- An Agent is not authoritative merely because it can act.
- Conversation history is not authoritative Process Instance state.
- Execution Environment is not the Runtime.

## Documentation principles

The final documentation follows these rules:

1. Concepts are defined once and explained from relevant perspectives where necessary.
2. Historical development status is not treated as conceptual meaning.
3. Implementation details do not become normative merely because a particular Runtime uses them.
4. Every substantive concept remains traceable to the validated AESM model.
5. The documentation describes an iterative engineering system, not a waterfall checklist.
6. Persistent Process Instance state is treated as the continuity boundary.
7. AI Agents and Runtime implementers receive dedicated reader-oriented guidance without creating alternative semantics.
