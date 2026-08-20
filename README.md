# AI-Assisted Engineering System Model

AESM is a system model for persistent, governed engineering execution in which engineering meaning, execution semantics, operational state, human participation, and AI participation remain explicitly separated.

## Documentation

The canonical AESM documentation is now maintained as one unified documentation set under `docs/`.

Start with [`docs/README.md`](docs/README.md).

The documentation is organized around the knowledge required to understand and use AESM rather than around the historical development documents.

## Core model

```text
Engineering Process Model (EPM)
        ↓
Process Execution Model (PEM)
        ↓
Runtime
        ↓
Persistent Process Instance
        ↔
Execution Context
        ↓
Human / AI Participants
        ↓
Replaceable Execution Environment
```

The defining property of AESM is persistent, governed engineering execution that is independent of any particular Agent session or Execution Environment.
