# Process Instance and Execution Context

## Process Instance

A **Process Instance** is one execution of the Engineering Process Model for a specific engineering objective.

It is the persistent identity of the engineering work.

A Process Instance is independent of:

- a particular Agent;
- a conversation;
- an Agent context window;
- an IDE session;
- a Runtime process lifetime;
- an Execution Environment.

Multiple Agents and environments may participate in the same Process Instance.

## Execution Context

The **Execution Context** is the authoritative operational state required to continue a Process Instance consistently at a specific point in time.

It is a logical concept, not a required storage format.

The physical representation may be a database, files, service state, or another mechanism. What matters is that the authoritative state is persistent, recoverable, portable, and sufficient for continuation.

## What the context represents

The context may include:

### Process status

- Process Instance identity
- Engineering Objective
- current Process State
- execution mode

### Engineering state

- Requirements
- Constraints
- Artifacts
- implementation status
- verification status
- completed and remaining work

### Decision state

- accepted Engineering Decisions
- pending Decisions
- Decision Gate conditions

### Knowledge state

- Evidence
- Assumptions
- Risks
- unresolved questions
- relevant contradictions

### Continuity state

- interruption point
- pending activities
- next expected action
- conditions needed for resumption

### History and traceability

- material observations and inputs
- recognized contributions
- execution determinations
- execution actions and results
- verification outcomes
- material state changes
- reconsideration history

The exact schema is implementation-dependent, but authoritative continuation information must not depend on transient conversation memory.

## Authority boundary

Execution Context is authoritative for the **operational state of the Process Instance**. It does not override EPM engineering meaning or PEM execution semantics.

Conversational memory, an Agent's internal state, a protocol message, or transient Runtime memory is not authoritative merely because it contains similar information.

## Continuity

The purpose of persistent context is to make continuation possible across interruptions and replacements.

```text
Agent A
   ↓
Process Instance
   ↓
Execution Context
   ↓
Agent A stops
   ↓
Runtime / Environment changes
   ↓
Agent B
   ↓
Same Process Instance
   ↓
Restore authoritative context
   ↓
Continue
```

## Recovery

A Runtime recovering an interrupted Process Instance must use authoritative state rather than inventing missing history from assumptions or conversation memory.

If required authoritative information is missing, the system should represent the condition explicitly rather than silently fabricate state.

## Historical state

Material historical state must remain reconstructable. Reconsideration may replace current conclusions, but it does not erase the fact that previous conclusions existed or the basis on which they were reached.

## Process continuity invariant

The Process Instance is the continuity boundary:

```text
Conversation may end
Agent may change
IDE may close
Runtime may restart
Environment may change

        ↓

Process Instance remains
Execution Context remains authoritative
```
