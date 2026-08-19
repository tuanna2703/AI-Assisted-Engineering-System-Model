# Minimum Executable AESM Runtime

This directory contains the first implementation experiment for AESM.

## Scope

The implementation is intentionally small and exists to test the frozen semantic foundation empirically. It currently focuses on:

- persistent Process Instance identity;
- persistent authoritative Execution Context;
- append-only execution history;
- Runtime attachment and replacement;
- controlled mutation through the Runtime surface;
- explicit verification before engineering completion;
- explicit recovery failure when authoritative Context is unavailable.

This code is implementation-specific and does not modify the normative AESM model.

## First proof

Run:

```text
python -m pytest -q
```

The continuity tests are designed to demonstrate that a new Runtime can load the same Process Instance and recover its persisted Context without the original conversation.

## Current limitation

Agent/MRAP and workspace/tool adapters are not yet implemented. They should be added only after the persistence/recovery foundation is exercised successfully.
