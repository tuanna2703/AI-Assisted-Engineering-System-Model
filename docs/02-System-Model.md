# AESM System Model

## System entities

AESM is composed conceptually of the following entities and boundaries:

- **Engineering Process Model (EPM)** — defines engineering meaning and validity.
- **Process Execution Model (PEM)** — defines execution semantics.
- **Runtime** — implements PEM and governs execution.
- **Process Instance** — represents one concrete execution of engineering work.
- **Execution Context** — authoritative operational state required to continue a Process Instance.
- **Participants** — Humans and AI Agents that contribute to execution.
- **Execution Environment** — the environment through which participants interact with the Runtime and engineering tools.
- **Artifacts** — persistent representations of engineering knowledge produced or consumed during work.

## Layer relationships

```text
EPM
 │ engineering meaning and validity
 ▼
PEM
 │ execution semantics
 ▼
Runtime
 │ concrete execution
 ▼
Process Instance ↔ Execution Context
 │
 ├── Human Participant
 └── AI Agent
        │
        ▼
Execution Environment
```

These are conceptual boundaries, not a required software architecture.

## Authority boundaries

| Concern | Governing authority |
|---|---|
| Engineering meaning and validity | EPM |
| Execution semantics | PEM |
| Concrete execution and operational control | Runtime |
| Current operational state | Process Instance / Execution Context |
| Engineering contributions | Participants under applicable process rules |
| Interaction and tooling surface | Execution Environment |
| Engineering artifacts | Applicable engineering and execution semantics |

The Runtime is an implementation of PEM. It is not an independent source of engineering meaning.

## Critical distinctions

```text
EPM ≠ PEM
PEM ≠ Runtime
Agent ≠ Runtime
Runtime ≠ Execution Context
Execution Context ≠ conversation history
Execution Environment ≠ Runtime
Capability ≠ authority
Proposal ≠ authorization
Engineering Decision ≠ Execution Determination
```

These distinctions prevent implementation convenience from silently changing the system model.

## Process Instance primacy

A Process Instance represents one engineering effort for a particular objective. It persists independently of:

- a chat conversation;
- an Agent context window;
- an individual Agent;
- an IDE session;
- a Runtime process lifetime;
- an Execution Environment.

Multiple Agents or environments may participate in the same Process Instance.

## Execution Environment

An Execution Environment is a replaceable interaction and engineering-work surface. Examples include IDEs, CLI/terminal environments, and cloud/web development environments.

An Execution Environment does not redefine EPM or PEM and does not become the authoritative owner of Process Instance state.

Tools and services used through an environment are not automatically Execution Environments.

## Participants

A Participant contributes information, analysis, engineering work, judgment, Decisions, verification, authorization where applicable, or other permitted input.

AESM explicitly supports:

- Human Participants;
- AI Agents.

Participation does not automatically grant unrestricted authority. Applicable EPM and PEM semantics determine how contributions are recognized and incorporated into authoritative state.

## Architecture invariant

The system must preserve the following relationship:

```text
EPM
 ↓
PEM
 ↓
Runtime
 ↓
Persistent Process Instance / Execution Context
 ↓
Participants
 ↓
Execution Environment
```

A lower layer must not silently redefine the semantics or authority of an upper layer.