# Minimum Executable AESM Architecture

**Date:** 2026-08-19  
**Status:** Implementation Architecture / Planning Artifact  
**Authority:** Informative; implementation-specific; does not modify or supersede frozen AESM semantics.  
**Purpose:** Define the smallest executable architecture capable of instantiating and testing the frozen AESM model.

---

## 1. Governing Principle

This architecture is a bridge from the frozen AESM semantic foundation to executable software.

It MUST NOT become an additional normative AESM semantic layer.

The implementation shall realize the semantics already established by:

```text
EPM
 ↓
PEM
 ↓
AESM Operational Model
 ↓
Agent Execution Contract
 ↓
Machine-Readable Agent Protocol
 ↓
Runtime Conformance Model
 ↓
This implementation
```

If an implementation requirement cannot be derived from the frozen layers, it shall initially be treated as an implementation choice, not as new AESM semantics.

---

## 2. Primary Objective

The first executable system exists to prove one property:

> A Process Instance can survive the lifetime of an Agent conversation and Runtime session, retain authoritative Execution Context, and continue engineering work later under a different Runtime and/or Agent.

The architecture is therefore optimized for **continuity proof**, not production scalability or IDE integration.

---

## 3. Minimal Runtime Architecture

```text
                         ┌─────────────────────┐
                         │ Human / AI Agent    │
                         │ Participant         │
                         └──────────┬──────────┘
                                    │
                         Contract / MRAP boundary
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────┐
│                         AESM Runtime                          │
│                                                              │
│  ┌────────────────┐   ┌──────────────────┐                   │
│  │ Agent Adapter  │──▶│ Runtime Control  │                   │
│  └────────────────┘   │ Loop             │                   │
│                       └────────┬─────────┘                   │
│                                │                             │
│                 ┌──────────────┼──────────────┐              │
│                 ▼              ▼              ▼              │
│        ┌──────────────┐ ┌─────────────┐ ┌──────────────┐    │
│        │ Recognition  │ │ Execution   │ │ Verification │    │
│        │ / Evaluation │ │ Coordinator │ │ Coordinator  │    │
│        └──────────────┘ └──────┬──────┘ └──────────────┘    │
│                                │                             │
│                        ┌───────▼────────┐                    │
│                        │ State Mutation │                    │
│                        │ Boundary       │                    │
│                        └───────┬────────┘                    │
└────────────────────────────────┼─────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
          ┌──────────────────┐      ┌──────────────────┐
          │ Process Instance │      │ Workspace / Tool │
          │ + Context Store  │      │ Adapter          │
          └──────────────────┘      └──────────────────┘
```

The boxes are implementation components, not new AESM semantic entities.

---

## 4. Component Responsibilities

### 4.1 Runtime Control Loop

The Runtime Control Loop is the top-level execution coordinator.

Responsibilities:

- load or create Process Instance;
- obtain authoritative Execution Context;
- evaluate current execution situation;
- coordinate recognition;
- determine permissible execution;
- invoke actions through adapters;
- collect results;
- coordinate verification;
- apply permitted state mutations;
- persist updated Context;
- determine whether to continue, suspend, reconsider, or complete.

It MUST NOT independently redefine engineering validity.

### 4.2 Process Instance Manager

Responsibilities:

- create Process Instance identity;
- load Process Instance identity;
- associate the current Runtime instance;
- expose lifecycle state;
- distinguish Process Instance lifecycle from Runtime lifecycle.

It does not own engineering semantics.

### 4.3 Execution Context Repository

The first implementation should use a simple durable local repository.

Recommended initial implementation:

```text
JSON / JSONL files on local filesystem
```

This is deliberately a development choice, not a normative storage requirement.

The repository must support:

```text
create(process_instance)
load(process_instance_id)
save(context)
append_history(event)
validate(context)
```

The physical representation may later be replaced by a database or another store without changing the semantic boundary.

### 4.4 Recognition / Evaluation Component

Responsibilities:

- inspect incoming information;
- classify its semantic role;
- determine whether it is recognizable under current conditions;
- distinguish informational, candidate, execution-related, outcome, failure, and continuation information;
- provide the Runtime with recognized information for subsequent execution handling.

This component MUST NOT directly mutate authoritative Context.

### 4.5 Execution Coordinator

Responsibilities:

- represent Execution Determination at implementation level;
- coordinate permissible Execution Actions;
- maintain pending work;
- invoke Workspace / Tool Adapter;
- capture Execution Results.

It MUST preserve the distinction:

```text
Engineering Decision
        ≠
Execution Determination
```

### 4.6 Verification Coordinator

Responsibilities:

- invoke or coordinate verification activities;
- capture Verification Results;
- evaluate whether applicable progression conditions can be advanced;
- report verification failure explicitly.

It MUST NOT convert a reported verification result directly into authoritative completion without applicable recognition and progression semantics.

### 4.7 State Mutation Boundary

All authoritative Context mutations pass through one explicit boundary.

Conceptually:

```text
Observation / Input / Result
          ↓
Recognition
          ↓
Applicable Conditions
          ↓
Mutation Decision
          ↓
State Mutation
          ↓
History / Trace
          ↓
Durable Context
```

The first implementation should make this boundary mechanically visible in code rather than allowing arbitrary component writes to the Context store.

### 4.8 Agent Adapter

The Agent Adapter translates between the implementation's Agent integration and MRAP semantic operations.

It is responsible for:

- constructing context supplied to the Agent;
- receiving Agent contributions;
- validating structural MRAP representation;
- associating interaction/correlation references;
- passing received information into Runtime recognition.

It is NOT responsible for:

- declaring Engineering Decisions;
- directly mutating authoritative Context;
- determining engineering validity;
- becoming the Runtime.

### 4.9 Workspace / Tool Adapter

The first implementation should expose only a small capability set:

```text
inspect_file
list_files
search_repository
write_file
run_command
read_command_result
```

The adapter records sufficient information to associate an external action and result with the current Process Instance execution trace.

The exact tool implementation is not part of AESM semantics.

---

## 5. Authoritative Persistence Boundary

The most important implementation boundary is:

```text
Transient Runtime State
        │
        │ may disappear
        ▼
┌─────────────────────────────┐
│ Persistent Authoritative    │
│ Process Instance State      │
│                             │
│ Execution Context           │
│ History / Trace             │
└─────────────────────────────┘
```

The following MUST NOT be required for continuation:

- Agent hidden memory;
- conversation transcript;
- in-memory Runtime objects;
- IDE session state;
- temporary process handles;
- undocumented caches.

Runtime-specific caches may exist, but recovery must remain possible from authoritative persisted state.

---

## 6. Proposed Repository Structure

The implementation should be isolated from the existing specification hierarchy.

```text
AI-Assisted-Engineering-System-Model/
│
├── specifications/
│   └── ... frozen / governed semantic artifacts ...
│
├── schemas/
│   └── ... governed machine-readable artifacts ...
│
├── review/
│   └── ... phase/review records ...
│
├── analysis/
│   ├── Minimum Executable AESM — Requirements-to-Implementation Traceability.md
│   └── Minimum Executable AESM Architecture.md
│
├── runtime/
│   ├── core/
│   │   ├── runtime
│   │   ├── process_instance
│   │   ├── execution_context
│   │   ├── recognition
│   │   ├── execution
│   │   ├── verification
│   │   └── mutation
│   │
│   ├── persistence/
│   │   ├── process_store
│   │   ├── context_store
│   │   └── history_store
│   │
│   ├── agent/
│   │   └── adapter
│   │
│   └── environment/
│       └── workspace_adapter
│
├── tests/
│   ├── unit/
│   ├── runtime/
│   ├── continuity/
│   └── end_to_end/
│
└── examples/
    └── first-proof/
```

This is a proposed implementation layout, not a required AESM architecture.

The Runtime implementation should initially be kept small enough that its entire persistence and recovery path can be inspected directly.

---

## 7. Process Instance Representation

The implementation should initially represent a Process Instance as an independently identifiable durable object.

Conceptually:

```json
{
  "process_instance_id": "...",
  "epm": {"name": "...", "version": "..."},
  "pem": {"name": "...", "version": "..."},
  "engineering_objective": "...",
  "lifecycle": "active",
  "execution_context_ref": "...",
  "created_at": "...",
  "updated_at": "..."
}
```

The exact field names are implementation choices unless later adopted through governed schema work.

The identity MUST remain stable across:

- Agent replacement;
- Runtime restart;
- Runtime replacement;
- conversation loss.

---

## 8. Execution Context Representation

The first implementation should favor explicitness over optimization.

A practical initial structure is:

```text
process-instance/
└── <process-instance-id>/
    ├── context.json
    ├── history.jsonl
    └── artifacts.json
```

`context.json` contains the latest authoritative operational state.

`history.jsonl` contains append-only material execution/state events required for reconstruction and traceability.

`artifacts.json` contains durable references to relevant workspace artifacts where needed.

The implementation should use atomic persistence semantics so that a Runtime crash does not leave a partially written authoritative Context undetectable.

A corrupted or incomplete Context MUST result in explicit recovery failure rather than invented state.

---

## 9. Runtime Execution Loop

The minimum Runtime loop is:

```text
load Process Instance
        ↓
load + validate Context
        ↓
evaluate current situation
        ↓
identify required contribution/action
        ↓
interact with Agent / Environment
        ↓
recognize returned information
        ↓
determine permissible next execution
        ↓
execute
        ↓
capture result
        ↓
verify where applicable
        ↓
apply controlled mutation
        ↓
persist Context + history
        ↓
re-evaluate
```

The loop must support interruption after every persistence boundary.

The implementation should not rely on a monolithic in-memory workflow object whose destruction makes continuation impossible.

---

## 10. Agent Interaction Boundary

The first implementation should not attempt to support every possible Agent integration.

One adapter is sufficient.

The adapter should expose a narrow interface conceptually equivalent to:

```text
request_contribution(context_view)
receive_contribution()
```

The Runtime decides what context information is appropriate to expose.

The Agent returns a semantic contribution represented through MRAP-compatible operations.

The Runtime then performs recognition.

The control sequence is:

```text
Runtime
  ↓
Agent request/context view
  ↓
Agent
  ↓
MRAP operation
  ↓
Agent Adapter
  ↓
Structural validation
  ↓
Runtime recognition
  ↓
Execution semantics
```

A valid protocol message may still be rejected, deferred, or treated as non-authoritative.

---

## 11. Context View vs Authoritative Context

The Agent should generally receive a **Context View**, not unrestricted access to the authoritative Context store.

```text
Authoritative Execution Context
              │
              ▼
       Runtime-controlled
         Context View
              │
              ▼
             Agent
```

This provides a strong implementation boundary:

```text
Agent can inspect what Runtime exposes
        ≠
Agent can mutate authoritative state
```

The first implementation should make Context View generation explicit.

---

## 12. Recovery Model

Recovery is a first-class execution path.

```text
Runtime startup
      ↓
identify Process Instance
      ↓
load persisted Context
      ↓
validate Context
      ↓
load required history/references
      ↓
reconstruct execution situation
      ↓
re-evaluate current conditions
      ↓
continue / suspend / recover-fail
```

Recovery MUST NOT replay the old conversation as a substitute for authoritative state.

Recovery MUST NOT assume that the last Runtime action completed merely because the Runtime previously attempted it.

Where the persisted state indicates an incomplete or uncertain action, the new Runtime must process that condition according to the applicable semantics.

---

## 13. Runtime Replacement Model

Runtime replacement is intentionally simple in the first proof.

```text
Runtime A
   │
   ├── Process Instance P
   ├── Context Cn
   └── persisted history

Runtime A terminates

Runtime B
   │
   ├── load P
   ├── load Cn
   ├── load history
   └── continue
```

Runtime-specific identity may change.

Process Instance identity MUST NOT change.

The implementation must therefore never use the Runtime process ID, memory identity, or Agent conversation ID as the Process Instance identity.

---

## 14. First Proof Harness

The proof harness should be deterministic and should simulate loss of Runtime and conversation state.

Minimum sequence:

```text
TEST-01
create P
persist C0
assert reload(P) == C0

TEST-02
attach Agent A
record observation
persist C1
terminate Runtime A
reload P with Runtime B
assert observation exists

TEST-03
establish Engineering Decision D
persist C2
terminate
reload
assert D remains reconstructable

TEST-04
perform partial implementation
persist C3
terminate
reload
assert pending work remains pending

TEST-05
force verification failure
persist failure C4
terminate
reload
assert failure remains explicit

TEST-06
replace Agent A with Agent B
reload P
assert Agent B can continue without Agent A conversation

TEST-07
complete implementation
verify
persist Cf
assert engineering completion
assert Runtime termination remains separate
```

The harness should intentionally delete or isolate the old conversation representation before recovery.

Success must therefore demonstrate that the old conversation is unnecessary.

---

## 15. Initial Test Layers

### Layer 1 — Persistence Tests

Prove that Process Instance and Context survive process termination.

### Layer 2 — Recovery Tests

Prove that a fresh Runtime can reconstruct the execution situation.

### Layer 3 — Authority Tests

Prove that Agent/tool/environment outputs cannot bypass Runtime recognition and mutation control.

### Layer 4 — Continuity Tests

Prove Agent and Runtime replacement.

### Layer 5 — Engineering Execution Tests

Prove investigation, decision, implementation, and verification can participate in one Process Instance.

### Layer 6 — End-to-End Proof

Prove the full interruption/recovery scenario.

VS Code integration comes after these layers pass.

---

## 16. First Proof Task Selection

The first real engineering task should be intentionally small but semantically non-trivial.

Recommended characteristics:

- repository-local;
- requires inspection before editing;
- has at least one explicit Requirement;
- permits at least two plausible implementation approaches;
- requires an Engineering Decision;
- produces a tangible Artifact change;
- has an objective verification command/test;
- can be interrupted after implementation but before verification;
- can be completed within one short engineering session when uninterrupted.

A trivial one-file edit is insufficient because it would not adequately test investigation, decision, execution, verification, and continuity semantics.

---

## 17. VS Code Boundary

VS Code is an Execution Environment integration, not the Runtime itself.

The eventual arrangement should be:

```text
VS Code
   │
   ├── workspace
   ├── UI / terminal
   └── AESM integration
          │
          ▼
       Runtime
          │
          ├── Process Store
          ├── Context Store
          ├── Agent Adapter
          └── Workspace Adapter
```

The first proof should be executable without VS Code.

VS Code integration becomes a later adapter once Runtime continuity is proven independently.

---

## 18. Explicit Non-Goals

The first implementation does not attempt to establish:

- a production database architecture;
- distributed execution;
- multi-agent coordination;
- cloud deployment;
- certification infrastructure;
- protocol interoperability standards;
- autonomous scheduling;
- enterprise security architecture;
- a generalized plugin ecosystem;
- a formal new AESM specification layer.

These remain open implementation or future-governance questions.

---

## 19. Gap Classification During Implementation

Every discovered problem must first be classified:

```text
Implementation defect
        ↓
Representation/storage defect
        ↓
Environment capability gap
        ↓
Agent capability gap
        ↓
Semantic gap
```

Only the last category is prima facie evidence that the frozen semantic foundation may require controlled change.

The implementation team MUST NOT resolve implementation failures by silently redefining frozen semantics.

---

## 20. Immediate Implementation Sequence

```text
Step 1
Create runtime/ skeleton

Step 2
Implement Process Instance identity/lifecycle

Step 3
Implement durable Context Store

Step 4
Implement Context validation + atomic persistence

Step 5
Implement Runtime load/recover/resume

Step 6
Implement controlled mutation boundary

Step 7
Implement execution/result/verification skeleton

Step 8
Implement local Workspace Adapter

Step 9
Implement one Agent Adapter

Step 10
Implement interruption/recovery harness

Step 11
Run first end-to-end proof

Step 12
Classify every discovered gap

Step 13
Only then decide whether further specification work is necessary
```

---

## 21. Architecture Decision

The first executable AESM should be:

```text
local
single-runtime
single-process-instance-at-a-time
persistent
restartable
agent-replaceable
workspace-capable
implementation-specific
```

This is deliberately smaller than a production system.

Its purpose is to establish the architectural fact on which the entire AESM objective depends:

> **Authoritative engineering continuity belongs to the persisted Process Instance / Execution Context, not to an Agent conversation or Runtime session.**

---

## 22. Next Action

The architecture is now sufficiently defined to begin implementation.

The next concrete engineering action is to create the initial `runtime/` implementation skeleton and the persistence/recovery test harness, without yet integrating VS Code or a production Agent provider.

The implementation should be kept small and inspectable so that any semantic gap discovered during execution can be traced back to the frozen AESM layers.
