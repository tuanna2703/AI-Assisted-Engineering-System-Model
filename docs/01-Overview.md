# AESM Overview

## What AESM is

The **AI-Assisted Engineering System Model (AESM)** is a system model for persistent, governed engineering execution.

AESM treats engineering work as a **persistent Process Instance**, rather than as a prompt, chat session, Agent session, IDE session, or transient workflow. The Process Instance is governed by an **Engineering Process Model (EPM)** and executed according to a **Process Execution Model (PEM)** by a Runtime.

Humans and AI Agents participate in the work. Execution Environments such as IDEs, terminals, and web development environments provide interaction surfaces but do not own the process.

## The central idea

```text
Engineering Process Model
        │ defines engineering meaning and validity
        ▼
Process Execution Model
        │ defines execution semantics
        ▼
Runtime
        │ executes
        ▼
Persistent Process Instance
        │ has authoritative operational state
        ▼
Execution Context
        │
        ├── Human Participants
        └── AI Agents
                │
                ▼
        Execution Environment
```

The defining property of AESM is **persistent, governed engineering execution that is independent of any particular Agent session or Execution Environment**.

## Why AESM exists

Ordinary AI-assisted engineering often treats a conversation as the unit of work. That creates a continuity problem: when a context window ends, an Agent changes, an IDE closes, or a Runtime restarts, important engineering knowledge can become dependent on transient memory.

AESM makes the engineering process itself persistent. Requirements, Evidence, Decisions, Artifacts, verification state, unresolved issues, execution state, history, and next actions belong to the Process Instance and its authoritative Execution Context.

## What AESM is not

AESM is not merely:

- a prompt library;
- an Agent system prompt;
- a single AI Agent;
- an IDE extension;
- a CLI application;
- a conversation history;
- a linear checklist or waterfall workflow;
- a particular AI model or model provider;
- a particular storage technology or programming language.

These may participate in an AESM implementation without defining AESM itself.

## Defining properties

### Persistent process identity

The Process Instance remains the identity of the engineering work across Agent, Runtime, and Execution Environment changes.

### Separation of engineering meaning and execution

EPM defines what engineering work means and when it is valid. PEM defines how that work is executed. A Runtime implements PEM and must not redefine engineering validity.

### Controlled authority

Capability does not imply authority. An Agent can propose, analyze, implement, or verify without thereby becoming the Runtime or acquiring unrestricted authority over Process Instance state.

### Human and AI collaboration

Humans and AI Agents are both Participants. AESM is AI-assisted, not inherently AI-controlled.

### Evidence and verification

Engineering progression is evidence-oriented. Verification can expose deficiencies and cause controlled reconsideration rather than forcing linear progress.

### Continuity

Execution can be suspended, resumed, recovered, or transferred because authoritative operational state is persistent and independently recoverable.

### Iteration

AESM supports feedback loops. Verification, new Evidence, changed Requirements, or discovered problems can cause earlier engineering concerns to be reconsidered.

## A minimal AESM scenario

```text
User requests engineering work
        ↓
Process Instance created or loaded
        ↓
Execution Context initialized or restored
        ↓
Engineering work proceeds under EPM/PEM
        ↓
Artifacts, Evidence, Decisions, and verification are recorded
        ↓
Process state is updated
        ↓
Runtime or Agent may stop
        ↓
Process Instance remains persistent
        ↓
Another Agent / Environment resumes from authoritative state
```

This scenario captures the architectural property AESM is designed to provide.