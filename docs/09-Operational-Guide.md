# AESM Operational Guide

## Purpose

This guide shows how the major AESM concepts work together during an engineering effort. It is explanatory; the governing semantics remain in the applicable EPM and PEM concepts.

## 1. Receive an engineering objective

A user or other authorized participant initiates engineering work.

The system creates or loads a Process Instance representing that work.

## 2. Establish authoritative state

The Runtime establishes or restores the Execution Context required to continue the Process Instance.

The system must not substitute conversation memory for missing authoritative state.

## 3. Interpret the engineering situation

The current objective, Requirements, Constraints, Process State, Artifacts, Evidence, Decisions, risks, assumptions, and unresolved questions are examined according to EPM.

## 4. Execute according to PEM

The Runtime applies the execution cycle:

```text
Observe → Evaluate → Plan → Execute → Verify → Update Context → Repeat
```

## 5. Perform engineering work

Depending on the current engineering situation, work may include:

- investigation;
- evidence gathering;
- requirement clarification;
- solution evaluation;
- decision making;
- implementation;
- verification;
- stakeholder interaction;
- reconsideration.

There is no universal fixed sequence that every engineering task must follow.

## 6. Maintain the boundary between engineering and execution

During execution, keep these distinctions explicit:

```text
Engineering Decision
        ≠
Execution Determination

Engineering validity
        ≠
Runtime capability

Agent capability
        ≠
Agent authority
```

EPM determines engineering validity. PEM and the Runtime govern execution.

## 7. Record results

Engineering and execution results are incorporated into authoritative state through applicable recognition and mutation rules.

The Runtime should preserve sufficient traceability to understand what happened and why.

## 8. Verify

Verification evaluates whether the current result satisfies applicable conditions.

If verification succeeds, progression may be possible.

If verification fails, the process may need more investigation, revision, reconsideration, or return to an earlier concern.

## 9. Determine progress

Progress is determined from engineering conditions rather than from elapsed time or Agent activity.

The Process Instance may:

- continue;
- advance;
- wait for a Decision or Participant;
- become blocked;
- enter reconsideration;
- suspend;
- complete;
- terminate according to applicable semantics.

## 10. Continue across interruptions

When an Agent session ends or an environment closes, the Process Instance does not automatically end.

Later execution begins from authoritative Execution Context.

## Example

```text
Human: "Implement feature X"
        ↓
Create Process Instance
        ↓
Initialize Execution Context
        ↓
Observe current engineering situation
        ↓
Investigate unknowns
        ↓
Gather Evidence
        ↓
Clarify Requirements
        ↓
Evaluate Solutions
        ↓
Make Engineering Decision
        ↓
Implement
        ↓
Verify
        ↓
Verification fails
        ↓
New Evidence
        ↓
Reconsider Solution / Decision
        ↓
Implement again
        ↓
Verify
        ↓
Persist current state
        ↓
Continue / Complete
```

The important property is not the exact sequence but the governed, persistent, iterative nature of the execution.

## What should never happen silently

An AESM implementation should not silently:

- replace authoritative state with conversation memory;
- treat Agent output as automatically authoritative;
- bypass a Decision Gate;
- redefine EPM or PEM semantics;
- convert capability into authority;
- erase material historical state;
- conceal material uncertainty or failed verification;
- terminate a Process Instance merely because an Agent or Runtime stopped.
