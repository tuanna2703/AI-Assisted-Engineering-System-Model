# Minimum Executable AESM — Requirements-to-Implementation Traceability

**Date:** 2026-08-19  
**Purpose:** Bridge the frozen AESM semantic foundation to the first executable system without defining a new normative specification layer.  
**Status:** Analysis / Implementation Planning Artifact  
**Authority:** Informative; does not modify or supersede frozen EPM, PEM, Operational Model, Agent Execution Contract, MRAP, or RCM semantics.

---

## 1. Purpose and Governing Question

The AESM semantic foundation through Phase 6 is established. The next question is therefore not which additional specification should be created, but whether the frozen model can be instantiated as a minimal executable system capable of persistent, resumable, AI-assisted engineering work.

The governing question is:

> Can a Process Instance and its authoritative Execution Context survive the lifetime of an Agent conversation and Runtime session, and can a later Runtime/Agent continue the same engineering work without relying on transient conversational memory?

This document derives the minimum implementation capabilities and first end-to-end proof scenario required to answer that question.

This document is **not** a Phase 7 specification and does not authorize a Phase 7. Any future phase shall be justified by implementation evidence and governed separately.

---

## 2. Source Baseline

The implementation is derived from the frozen semantic hierarchy:

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
Runtime Implementation
 ↓
Execution Environment
```

The EPM defines engineering meaning and validity; it explicitly leaves Runtime architecture, Execution Context storage, Participant interaction mechanics, and implementation technologies outside its scope. The PEM defines execution semantics, including Process Instance execution, Execution Context, continuity, Participant coordination, and the execution cycle. The RCM then makes explicit the semantic obligations of a conforming Runtime, including establishment/recovery of authoritative Execution Context, recognition, Execution Determination, execution, verification, controlled mutation, traceability, reconsideration, continuity, suspension, resumption, recovery, and termination.

The first implementation must therefore instantiate these existing obligations rather than redefine them.

---

## 3. Operational Success Criterion

The minimum executable system is successful only if the following invariant can be demonstrated:

```text
Conversation A
    ↓
Agent participates in Process Instance P
    ↓
Runtime persists authoritative state
    ↓
Runtime terminates
    ↓
Conversation A is unavailable
    ↓
Runtime B starts
    ↓
Runtime B loads Process Instance P
    ↓
Runtime B recovers authoritative Execution Context
    ↓
Agent B participates
    ↓
Engineering continues from authoritative state
```

The continuation must not depend on:

- the original Agent's hidden memory;
- the original conversation transcript;
- transient Runtime memory;
- undocumented implementation state;
- assumptions invented during recovery.

The RCM explicitly requires recovery from authoritative state rather than assumptions about prior conversation or undocumented Runtime memory.

---

## 4. Minimum Executable System

The smallest meaningful implementation consists of five capability areas:

```text
                    Human / AI Agent
                           │
                    Agent Contract
                           │
                           ▼
                    ┌─────────────┐
                    │   Runtime   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   Process Instance   Execution Context   Workspace
       Manager             Store          / Tools
```

### 4.1 Process Instance Manager

Must provide the ability to:

- create a Process Instance;
- identify a Process Instance independently of a conversation;
- load an existing Process Instance;
- attach a Runtime to it;
- suspend / resume it where applicable;
- expose lifecycle state needed for execution;
- distinguish Process Instance lifecycle from Runtime lifecycle.

### 4.2 Execution Context Store

Must provide persistent authoritative state sufficient to reconstruct the current operational situation.

It must support:

- create;
- read;
- controlled update;
- history / traceability preservation;
- recovery after Runtime restart;
- consistent reconstruction;
- explicit failure when authoritative state is unavailable rather than silent invention.

The physical storage technology is intentionally not prescribed by the frozen models.

### 4.3 Runtime Execution Loop

Must instantiate the PEM/RCM execution semantics:

```text
Observe
  ↓
Evaluate
  ↓
Plan
  ↓
Execute
  ↓
Verify
  ↓
Update Context
  ↓
Repeat
```

The implementation must preserve the distinctions between observation, recognition, Execution Determination, Engineering Decision, Execution Action, Execution Result, verification, and state mutation.

### 4.4 Agent Boundary Adapter

Must allow an AI Agent to participate through the Agent Execution Contract / MRAP boundary.

It must support the semantic operation classes required by the frozen protocol without allowing protocol receipt to become authority or unrestricted state mutation.

The Agent must remain a Participant. The Runtime remains the execution control boundary.

### 4.5 Workspace / Tool Adapter

Must expose sufficient engineering capabilities to perform the first proof task, for example:

- inspect repository files;
- modify files;
- execute relevant commands/tests;
- obtain environment observations;
- return execution results.

These capabilities are implementation/environment concerns and do not become engineering authority merely because they are available to the Runtime or Agent.

---

## 5. Requirements-to-Implementation Traceability

| ID | Frozen semantic obligation | Required executable capability | Minimum implementation evidence | Source layer |
|---|---|---|---|---|
| IMPL-01 | Process Instance represents one engineering execution | Persistent Process Instance identity and lifecycle | Same instance can be loaded after restart | EPM / PEM / RCM |
| IMPL-02 | Execution Context is authoritative operational state | Persistent Context Store | Fresh Runtime reconstructs current state | PEM / RCM |
| IMPL-03 | Runtime must establish/attach/recover Context | Runtime initialization and recovery path | Restart test passes without conversation | RCM |
| IMPL-04 | Execution is continuous/adaptive | Runtime execution loop | Multiple observe/evaluate/execute cycles occur | PEM |
| IMPL-05 | Observation does not mutate state | Separate observation path | Observation-only operation leaves authoritative state unchanged | PEM / RCM |
| IMPL-06 | Recognition is Runtime-controlled | Recognition/evaluation boundary | Incoming Agent data cannot directly mutate state | RCM |
| IMPL-07 | Execution Determination is distinct from Engineering Decision | Separate execution and engineering records | Runtime can determine next action without creating Engineering Decision | PEM / RCM |
| IMPL-08 | Execution Action/Result/Verification are distinct | Action/result/verification lifecycle | Failed verification can prevent progression | PEM / RCM |
| IMPL-09 | State Mutation is controlled | Mutation gate | Only recognized/permitted changes enter Context | RCM |
| IMPL-10 | Traceability is persistent | Event/relationship recording | Material conclusion can be reconstructed to its basis | EPM / RCM |
| IMPL-11 | Reconsideration preserves history | Versioned/history-preserving state change | Old Decision remains reconstructable after reconsideration | EPM / RCM |
| IMPL-12 | Failure/uncertainty are explicit | Failure/uncertainty representation | Interrupted/failed action does not appear successful | PEM / RCM |
| IMPL-13 | Continuity survives Runtime replacement | Durable state independent of Runtime instance | Runtime B resumes Process Instance created by Runtime A | PEM / RCM |
| IMPL-14 | Agent is Participant, not Runtime | Agent boundary adapter | Agent can be replaced without replacing Process Instance | PEM / Contract / RCM |
| IMPL-15 | Protocol is not authority | Protocol validation + Runtime recognition | Valid message can still be rejected/not recognized | Contract / MRAP / RCM |
| IMPL-16 | Workspace actions are execution actions | Environment/tool adapter | Runtime can execute a bounded engineering task and capture result | RCM / Environment |
| IMPL-17 | Engineering completion differs from Runtime termination | Separate lifecycle state | Runtime can stop while Process Instance remains resumable | EPM / PEM / RCM |
| IMPL-18 | Engineering completion requires verification | Verification gate | Process cannot be marked complete solely because files changed | EPM / PEM |
| IMPL-19 | Missing authoritative state must not be invented | Recovery integrity check | Recovery fails explicitly when required state is absent/corrupt | RCM |
| IMPL-20 | Conversation is not authoritative continuity state | No dependency on transcript for recovery | Original conversation can be discarded before continuation | EPM / PEM / RCM |

---

## 6. Capability Ownership Matrix

The first implementation should keep ownership boundaries explicit.

| Capability | EPM | PEM | Operational Model | Contract / MRAP | RCM | Runtime | Environment |
|---|---:|---:|---:|---:|---:|---:|---:|
| Engineering validity | **A** | C | R | I | I | I | I |
| Process execution semantics | I | **A** | R | I | R | I | I |
| Operational state representation | I | R | **A** | I | R | I | I |
| Agent participation boundary | I | R | R | **A** | R | I | I |
| Runtime semantic obligations | I | R | R | R | **A** | I | I |
| Actual execution | I | I | I | I | C | **A** | C |
| Persistent Process Instance storage | I | C | R | I | **R** | **A** | C |
| Workspace access | I | I | I | I | C | **A** | **A** |
| Concrete serialization/database/API | I | I | I | I | I | **A** | C |

Legend:

- **A** — authoritative owner of the semantic concern;
- **R** — defines/requires the concern at the applicable semantic layer;
- **C** — participates/consumes/coordinates;
- **I** — informative or outside the layer's authority.

This table is an implementation analysis, not a new normative authority model.

---

## 7. Minimum Persistent Execution Context

The first implementation should persist only what is required to reconstruct authoritative continuation state, while preserving the engineering information needed by the frozen EPM.

Conceptually:

```text
Execution Context
├── Process Instance identity
├── applicable model/version references
├── Engineering Objective
├── current Process State
├── execution mode
├── Requirements + resolution state
├── Constraints
├── Evidence references
├── Assumptions
├── Risks
├── Candidate Solutions / evaluations
├── Engineering Decisions
├── Decision Gates
├── Artifact references + status
├── verification status
├── unresolved matters
├── pending execution work
├── Execution Determination / continuation position
├── execution history
├── traceability relationships
├── failure / uncertainty state
└── continuity / recovery metadata
```

The exact storage schema is deliberately left open at this stage.

The implementation question is not:

> “What database schema should AESM use?”

It is:

> “What authoritative information must be recoverable for a new Runtime to continue correctly?”

Only after that requirement is proven should concrete storage design be optimized.

---

## 8. First End-to-End Proof Scenario

### 8.1 Scenario

A user submits:

> Implement feature X.

The feature should be deliberately selected so that the task requires some investigation and at least one verification step, but does not require a large production system.

### 8.2 Execution

```text
User Request
    ↓
Create Process Instance P
    ↓
Initialize Execution Context C0
    ↓
Attach Agent A
    ↓
Investigate workspace
    ↓
Record Evidence
    ↓
Establish / update Requirements
    ↓
Evaluate Candidate Solutions
    ↓
Establish Engineering Decision
    ↓
Execute bounded implementation
    ↓
Persist partial state Cn
    ↓
STOP RUNTIME A
    ↓
DISCARD / MAKE UNAVAILABLE CONVERSATION A
    ↓
START RUNTIME B
    ↓
LOAD PROCESS INSTANCE P
    ↓
RECOVER EXECUTION CONTEXT Cn
    ↓
ATTACH AGENT B
    ↓
Continue execution
    ↓
Verify implementation
    ↓
Persist final state Cf
    ↓
Reach engineering completion
```

### 8.3 Required proof assertions

The test is successful only if all of the following are true:

1. Process Instance identity is unchanged.
2. Engineering Objective is unchanged unless explicitly reconsidered.
3. Previously recognized Evidence remains available.
4. Requirements and their resolution states remain reconstructable.
5. Previous Engineering Decisions remain reconstructable.
6. Previous execution history remains reconstructable.
7. Pending work remains identifiable.
8. Verification status remains correct.
9. The new Runtime can determine what is currently permissible without the old conversation.
10. A new Agent can participate without becoming the owner of the Process Instance.
11. No state is invented merely because recovery information is missing.
12. Final completion is supported by verification and applicable progression conditions.

---

## 9. Deliberate Interruption Tests

The proof should include at least these interruption points:

### Test A — Before any Agent contribution

```text
create Process Instance
→ persist
→ terminate
→ reload
```

Expected: same Process Instance and initial Context are recovered.

### Test B — After investigation

```text
investigate
→ persist Evidence
→ terminate
→ reload
```

Expected: Evidence and its traceability remain available.

### Test C — After Engineering Decision

```text
Decision established
→ persist
→ terminate
→ reload
```

Expected: Decision remains authoritative and distinguishable from a proposal.

### Test D — During implementation

```text
partial implementation
→ persist
→ terminate
→ reload
```

Expected: Runtime identifies incomplete work rather than assuming completion.

### Test E — Verification failure

```text
implementation
→ verification fails
→ persist failure
→ terminate
→ reload
```

Expected: Process remains incomplete/reconsiderable; failure is not erased.

### Test F — Agent replacement

```text
Agent A
→ persist
→ Agent A unavailable
→ Agent B
→ reload
→ continue
```

Expected: Process Instance continuity does not depend on Agent identity or conversation continuity.

### Test G — Runtime replacement

```text
Runtime A
→ persist
→ Runtime A unavailable
→ Runtime B
→ reload
→ continue
```

Expected: Runtime replacement does not create a new Process Instance.

---

## 10. What Is Not Required for the First Proof

The following are deliberately excluded from the minimum implementation unless implementation evidence makes them necessary:

- distributed Runtime architecture;
- multiple Runtime coordination;
- certification;
- interoperability standards;
- new protocol layers;
- organizational governance frameworks;
- generalized plugin ecosystems;
- production-grade multi-tenant security model;
- advanced VS Code UI;
- multiple Agent providers;
- autonomous long-running scheduling;
- formal conformance certification infrastructure.

Their absence does not prevent the core continuity proof.

If implementation later demonstrates a genuine semantic gap, that gap should be documented first and only then considered for specification change.

---

## 11. Implementation Order

The recommended order is:

```text
1. Process Instance identity + lifecycle
        ↓
2. Persistent Execution Context
        ↓
3. Load / recover / resume
        ↓
4. Minimal Runtime execution loop
        ↓
5. Controlled state mutation + history
        ↓
6. Minimal workspace/tool execution
        ↓
7. Agent boundary adapter
        ↓
8. Agent replacement test
        ↓
9. End-to-end interruption/recovery test
        ↓
10. VS Code integration
```

This order intentionally proves continuity before optimizing user experience.

---

## 12. Implementation Gap Categories

Any failure discovered during implementation should be classified before changing specifications.

### Category A — Implementation Defect

The frozen semantics are sufficient, but the implementation does not realize them correctly.

Action: fix implementation; do not modify normative specifications.

### Category B — Representation Gap

The semantics are sufficient, but the chosen machine-readable or storage representation cannot represent a required state faithfully.

Action: improve implementation representation; if the frozen representation itself is normative and insufficient, initiate controlled change review.

### Category C — Environment Capability Gap

The Runtime semantics are sufficient, but the Execution Environment lacks a required capability.

Action: adapt or extend the environment integration.

### Category D — Agent Capability Gap

The Runtime can execute correctly, but the participating Agent cannot provide a contribution required by the engineering process.

Action: improve Agent integration/capability; do not transfer Runtime authority to the Agent.

### Category E — Semantic Gap

The implementation reaches a situation for which the frozen EPM/PEM/Operational Model/Contract/MRAP/RCM do not provide sufficient semantics to determine valid behavior.

Action: document the concrete counterexample and assess whether a controlled specification change is necessary.

Only Category E is a strong candidate for a future specification phase.

---

## 13. Decision: No Phase 7 Yet

Based on the current semantic foundation, no new normative phase is justified yet.

The immediate work is implementation instantiation and proof.

The next project milestone should therefore be expressed as:

> **Minimum Executable AESM Instantiation and Continuity Proof**

This is an implementation milestone, not a new specification phase.

A future formal phase may be proposed only if the implementation produces evidence that the frozen semantic foundation is insufficient or requires controlled extension.

---

## 14. Immediate Next Task

The next concrete task is to define the **Minimum Executable AESM architecture and repository structure** from this analysis, including:

- Runtime boundary;
- Process Instance representation;
- Execution Context representation;
- persistence abstraction;
- execution loop;
- Agent adapter boundary;
- workspace/tool boundary;
- first proof harness;
- restart/recovery test strategy.

That architecture should remain implementation-specific and should be explicitly prevented from becoming a new normative AESM semantic layer.
