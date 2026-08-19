# AI-Assisted Engineering System Model — Operational Flow

**Status:** Standard operational flow
**Authority:** Normative operational baseline for AESM
**Scope:** How AESM processes engineering work
**Repository:** `tuanna2703/AI-Assisted-Engineering-System-Model`

---

## 1. Purpose

This document defines the standard operational flow of the **AI-Assisted Engineering System Model (AESM)**.

It describes how a user request becomes persistent engineering work, how that work is carried out by humans and AI Agents, and how the work continues until it is completed, paused, blocked, or requires reconsideration.

This flow MUST be followed by AESM implementations and future AESM work.

The flow is governed by the AESM Architecture Model. It MUST NOT introduce concepts or responsibilities outside that architecture.

---

## 2. Standard Flow

The complete AESM operational flow is:

```text
User Request
    ↓
Create / Load Process Instance
    ↓
Initialize / Restore Execution Context
    ↓
Interpret according to EPM
    ↓
Execute according to PEM
    ↓
Investigate
    ↓
Gather Evidence
    ↓
Form / Update Requirements
    ↓
Evaluate Solutions
    ↓
Make Engineering Decisions
    ↓
Implement
    ↓
Verify
    ↓
Update Execution Context
    ↓
Determine Progress
    ↓
┌──────────────────────────────────────────────┐
│                                              │
│ Continue ────────────────────────────────────┤
│                                              │
│ Reconsider ──────────────────────────────────┤
│                                              │
│ Block / Await Human ─────────────────────────┤
│                                              │
│ Complete                                     │
│                                              │
└──────────────────────────────────────────────┘
```

The flow is iterative. It is not a one-way sequence.

---

## 3. Step 1 — User Request

A human provides an engineering request through an Execution Environment.

Example:

```text
"Implement feature X."
```

The request is the starting point for an engineering Process Instance.

The Agent MUST NOT treat the request as permission to immediately modify the project without first operating through the AESM process.

---

## 4. Step 2 — Create / Load Process Instance

The Runtime determines whether the request starts new engineering work or relates to an existing Process Instance.

For new work:

```text
User Request
    ↓
Create Process Instance
```

For continuing work:

```text
User Request / Continue Request
    ↓
Load existing Process Instance
```

The Process Instance becomes the persistent identity of the work.

---

## 5. Step 3 — Initialize / Restore Execution Context

For a new Process Instance, the Runtime initializes the Execution Context.

For an existing Process Instance, the Runtime restores the persisted Execution Context.

The Execution Context provides the authoritative information required to continue the work.

The Agent MUST use this state rather than relying on its previous conversation as the source of truth.

---

## 6. Step 4 — Interpret According to EPM

The engineering request and current Process Instance are interpreted according to the Engineering Process Model (EPM).

The purpose of this step is to understand what engineering work is required and what information is needed to make progress.

The Agent and human participant may contribute to this interpretation.

The Runtime does not replace EPM; it executes according to PEM while the engineering work is understood according to EPM.

---

## 7. Step 5 — Execute According to PEM

The Runtime governs execution according to the Process Execution Model (PEM).

PEM determines how the Process Instance proceeds, how its state is maintained, how participants interact with it, and how execution can continue, pause, resume, or complete.

The Agent performs engineering activities within this governed execution.

---

## 8. Step 6 — Investigate

The participants investigate the problem sufficiently to support engineering progress.

Investigation may include examining:

- existing source code;
- project structure;
- documentation;
- configuration;
- tests;
- existing behavior;
- relevant external information;
- constraints;
- possible causes of observed behavior.

Investigation is not a fixed checklist. The required investigation depends on what is needed to make a confident engineering decision.

---

## 9. Step 7 — Gather Evidence

Information discovered during investigation is gathered as evidence relevant to the engineering work.

Evidence supports:

- understanding the current system;
- requirements;
- solution evaluation;
- engineering decisions;
- implementation;
- verification.

Evidence MUST remain connected to the Process Instance so that later participants can understand why the work proceeded as it did.

---

## 10. Step 8 — Form / Update Requirements

Requirements are formed or updated using the available request and evidence.

Requirements may become clearer as investigation continues.

New evidence may therefore cause existing requirements to be clarified, changed, or reconsidered.

The process MUST allow this to happen rather than assuming that all requirements are completely known at the beginning.

---

## 11. Step 9 — Evaluate Solutions

Possible solutions are evaluated against the requirements, evidence, existing system, and relevant constraints.

The purpose is to determine which available approach can satisfy the engineering need with sufficient confidence.

Evaluation may reveal that more investigation or evidence is required.

When that happens, execution returns to the appropriate earlier activity.

---

## 12. Step 10 — Make Engineering Decisions

An engineering decision is made based on the available requirements, evidence, evaluated solutions, and constraints.

The decision becomes part of the persistent Process Instance state.

A later participant must be able to understand the decision without depending on the original Agent conversation.

If new evidence invalidates a decision, the decision may be reconsidered.

---

## 13. Step 11 — Implement

The selected solution is implemented in the engineering environment.

Implementation may be performed by:

- an AI Agent;
- a human programmer;
- both working together.

Implementation MUST remain connected to the current Process Instance so that its relationship to requirements and engineering decisions is preserved.

---

## 14. Step 12 — Verify

The implementation is verified against the requirements and intended behavior.

Verification may include appropriate tests, inspection, execution, review, or other engineering checks.

Verification produces information that affects the next process decision.

A successful verification may allow progress toward completion.

A failed or insufficient verification may produce new evidence and require reconsideration.

---

## 15. Step 13 — Update Execution Context

After meaningful engineering activity, the Runtime updates the persistent Execution Context.

The updated state must reflect the current understanding of the work, including relevant:

- requirements;
- evidence;
- decisions;
- implementation state;
- verification state;
- unresolved issues;
- participant actions;
- progress;
- next required action.

This step is essential for continuity across Agent and Execution Environment boundaries.

---

## 16. Step 14 — Determine Progress

The current Process Instance is evaluated to determine what should happen next.

There are four fundamental outcomes:

### Continue

The work can proceed with the current understanding and decision.

```text
Determine Progress
       ↓
   Continue
       ↓
Next engineering activity
```

### Reconsider

New evidence or verification results indicate that an earlier requirement, solution, or decision must be reconsidered.

```text
Determine Progress
       ↓
   Reconsider
       ↓
Earlier engineering activity
```

### Block / Await Human

The process cannot safely proceed without additional information, authorization, intervention, or work from a human participant.

```text
Determine Progress
       ↓
Block / Await Human
       ↓
Process remains persistent
       ↓
Human responds
       ↓
Continue execution
```

### Complete

The engineering work has satisfied its requirements and verification conditions and no further process work is required.

```text
Determine Progress
       ↓
    Complete
       ↓
Process Instance remains as a record of the completed work
```

---

## 17. Reconsideration and Feedback

AESM is inherently iterative.

Any significant result may change what is understood about the engineering problem.

A typical feedback path is:

```text
Implement
    ↓
Verify
    ↓
Verification fails
    ↓
Gather Evidence
    ↓
Update Requirements or Evaluate Solutions
    ↓
Make Engineering Decision
    ↓
Implement
    ↓
Verify
```

Another possible path is:

```text
Investigate
    ↓
Gather Evidence
    ↓
Requirements change
    ↓
Investigate again
```

The Runtime MUST preserve the resulting state and history so that reconsideration is understandable and traceable.

---

## 18. Persistence and Continuation

Persistence applies throughout the entire flow.

The Process Instance MUST remain available when:

- an Agent session ends;
- an Execution Environment closes;
- work is paused;
- a human must intervene;
- another Agent takes over;
- the work is resumed later.

A later participant continues from the persisted Process Instance and Execution Context.

The intended behavior is:

```text
Agent A
   ↓
Process Instance
   ↓
Persistent Execution Context
   ↓
Agent A session ends
   ↓
Time passes
   ↓
Agent B
   ↓
Load same Process Instance
   ↓
Restore Execution Context
   ↓
Continue
```

The previous conversation is not required as the authoritative source of process state.

---

## 19. Human and Agent Participation

Human programmers and AI Agents participate in the same Process Instance.

The flow does not require that every activity be performed by an Agent.

For example:

```text
Investigate        → Agent
Gather Evidence    → Agent + Human
Requirements       → Human + Agent
Evaluate Solutions → Agent
Decision            → Human + Agent
Implement           → Agent
Verify              → Human + Agent
```

The actual participant for each activity depends on the process and the authority provided by the human participant.

---

## 20. Complete Operational Example

A complete execution may therefore look like this:

```text
Human
  │
  │ "Implement feature X"
  ↓
Execution Environment
  ↓
Runtime
  ↓
Create Process Instance
  ↓
Initialize Execution Context
  ↓
Interpret according to EPM
  ↓
Execute according to PEM
  ↓
Investigate
  ↓
Gather Evidence
  ↓
Form / Update Requirements
  ↓
Evaluate Solutions
  ↓
Make Engineering Decisions
  ↓
Implement
  ↓
Verify
  ↓
Update Execution Context
  ↓
Determine Progress
  │
  ├── Continue ────────────────→ Continue engineering
  │
  ├── Reconsider ──────────────→ Revisit earlier work
  │
  ├── Block / Await Human ─────→ Persist and wait
  │                              ↓
  │                         Human responds
  │                              ↓
  │                         Continue
  │
  └── Complete ────────────────→ Process complete
```

At every point where the process continues, the Runtime operates on the persistent Process Instance and current Execution Context.

---

## 21. Operational Rules

The following rules are mandatory:

1. A user request starts or continues a Process Instance; it is not merely a prompt to an Agent.
2. The Process Instance is persistent.
3. The Execution Context is the authoritative state required for continuation.
4. EPM defines the engineering meaning of the work.
5. PEM governs execution.
6. The Runtime implements PEM.
7. Humans and AI Agents participate in the process.
8. Investigation is driven by what is needed to make confident engineering progress.
9. Evidence, requirements, solutions, decisions, implementation, and verification remain connected to the Process Instance.
10. Execution is iterative and may return to earlier engineering work.
11. Meaningful process state is persisted before execution depends on it for future continuation.
12. A different Agent must be able to continue the same Process Instance without depending on the previous Agent's conversation.
13. Closing an Execution Environment does not terminate the Process Instance unless the process is explicitly completed or terminated according to PEM.
14. The flow MUST NOT be expanded with additional mandatory steps or concepts without an explicit consensus decision.

---

## 22. Standard Flow Governance

This document is the **standard AESM operational flow**.

All AESM implementations and future development work MUST conform to this flow.

A change MUST NOT be introduced because an implementation, Agent, IDE, CLI, or development convenience appears to require it.

If a proposed change would alter the standard flow, the work MUST first identify the affected part of the flow, explain why the current flow is insufficient, and obtain an explicit consensus decision.

Until that decision is made, this flow remains authoritative and unchanged.

**The standard flow MUST NOT expand by implementation drift.**

---

## 23. Standard Flow Statement

The standard AESM operational flow is:

```text
User Request
    ↓
Create / Load Process Instance
    ↓
Initialize / Restore Execution Context
    ↓
Interpret according to EPM
    ↓
Execute according to PEM
    ↓
Investigate
    ↓
Gather Evidence
    ↓
Form / Update Requirements
    ↓
Evaluate Solutions
    ↓
Make Engineering Decisions
    ↓
Implement
    ↓
Verify
    ↓
Update Execution Context
    ↓
Determine Progress
    ↓
Continue / Reconsider / Block / Complete
```

This is the standard flow to be followed by AESM until a future consensus decision explicitly changes it.
