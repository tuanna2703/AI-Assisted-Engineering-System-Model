# Minimum Executable AESM Runtime

This directory contains the first implementation experiment for AESM.

## Scope

The implementation is intentionally small and exists to test the frozen semantic foundation empirically. It currently focuses on:

- persistent Process Instance identity;
- persistent authoritative Execution Context;
- append-only execution history;
- Runtime attachment and replacement;
- controlled mutation through the Runtime surface;
- explicit recognition before authoritative Engineering Decision state is recorded;
- explicit recognition of applicable engineering completion conditions;
- explicit recovery failure when authoritative Context is unavailable.

This code is implementation-specific and does not modify the normative AESM model.

## Recognition boundary

The Runtime does not independently determine engineering validity. Authoritative Engineering Decision and engineering-completion mutations require explicit recognition records supplied by the governing execution semantics.

In particular:

- an Agent or participant proposal is not sufficient to establish an Engineering Decision;
- successful verification is evidence that may support completion, but is not by itself a universal engineering-completion rule;
- the Runtime records recognized outcomes and controls their mutation into authoritative Execution Context.

The recognition records are deliberately lightweight implementation scaffolding. They do not constitute a new architectural layer or redefine EPM/PEM semantics.

## First proof

Run:

```text
python -m pytest -q
```

The continuity tests are designed to demonstrate that a new Runtime can load the same Process Instance and recover its persisted Context without the original conversation.

## Current limitation

Agent/MRAP and workspace/tool adapters are not yet implemented. They should be added only after the persistence/recovery foundation is exercised successfully.
