# AESM Reference

## Core definitions

| Term | Meaning |
|---|---|
| AESM | AI-Assisted Engineering System Model for persistent, governed engineering execution |
| EPM | Engineering Process Model; defines engineering meaning and validity |
| PEM | Process Execution Model; defines execution semantics |
| Runtime | Implementation of PEM that executes Process Instances |
| Process Instance | One execution of an Engineering Process Model for a specific engineering objective |
| Execution Context | Authoritative operational state required to continue a Process Instance |
| Participant | Entity contributing to Process Instance execution |
| Human Participant | Human participating in engineering execution |
| AI Agent | AI-based Participant in engineering execution |
| Execution Environment | Replaceable environment through which participants interact with the Runtime and engineering tools |
| Artifact | Persistent representation of engineering knowledge produced or consumed during execution |
| Evidence | Information supporting engineering conclusions and Decisions |
| Assumption | Proposition accepted without sufficient Evidence |
| Engineering Decision | Accepted engineering conclusion or commitment affecting engineering direction or outcome |
| Execution Determination | Execution-level determination of what may or should occur next |
| Verification | Evaluation of whether a result, Artifact, Decision, or state satisfies applicable conditions |
| Process State | Current stage of engineering work within a Process Instance |
| Decision Gate | Condition governing whether progression is permitted |
| Recognition | Runtime-controlled determination that information corresponds to a semantically meaningful input under applicable rules |
| State Mutation | Controlled change to authoritative Process Instance state |

## Critical distinctions

```text
EPM ≠ PEM
PEM ≠ Runtime
Agent ≠ Runtime
Runtime ≠ Execution Context
Execution Environment ≠ Runtime
Conversation ≠ Process Instance
Conversation ≠ authoritative Execution Context
Capability ≠ authority
Proposal ≠ authorization
Observation ≠ mutation
Receipt ≠ recognition
Recognition ≠ unrestricted mutation
Engineering Decision ≠ Execution Determination
Execution Result ≠ Execution Determination
Verification Result ≠ automatic authoritative recognition
Engineering completion ≠ Process Instance termination
Process Instance termination ≠ Runtime termination
```

## Authority map

```text
EPM
  engineering meaning and validity
        ↓
PEM
  execution semantics
        ↓
Runtime
  concrete execution and operational control
        ↓
Process Instance / Execution Context
  persistent operational state
        ↓
Participants
  human and AI contributions
        ↓
Execution Environment
  interaction and tooling surface
```

## Engineering chain

```text
Objective
 ↓
Requirements / Constraints
 ↓
Investigation
 ↓
Evidence
 ↓
Candidate Solutions
 ↓
Evaluation
 ↓
Engineering Decision
 ↓
Implementation / Artifacts
 ↓
Verification
 ↓
Progress / Reconsideration / Completion
```

## Execution chain

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
Update Execution Context
 ↓
Repeat
```

## Controlled contribution chain

```text
Participant / Agent / Tool / Environment
        ↓
Observation / Input / Candidate Contribution
        ↓
Runtime recognition
        ↓
EPM / PEM conditions
        ↓
Permitted mutation
        ↓
Execution Context / Trace
```

## Core invariants

1. Process Instance is the persistent unit of engineering execution.
2. Execution Context is authoritative operational state.
3. EPM and PEM remain distinct.
4. Runtime implements PEM and does not redefine engineering validity.
5. Agent is a Participant, not the Runtime.
6. Capability does not by itself establish authority.
7. Agent output is not automatically authoritative.
8. Decision Gates may not be bypassed or fabricated.
9. Historical state must remain reconstructable.
10. Material uncertainty and failure must remain explicit.
11. Execution must support continuity across interruptions and replacements.
12. Engineering completion, Process Instance termination, and Runtime termination remain distinct.
13. Implementation technology does not become normative merely because one Runtime uses it.

## Where to look

- **What is AESM?** → `01-Overview.md`
- **What entities exist?** → `02-System-Model.md`
- **What does engineering work mean?** → `03-Engineering-Model.md`
- **How is execution controlled?** → `04-Execution-Model.md`
- **How does continuity work?** → `05-Process-Instance-and-Execution-Context.md` and `08-Continuity-Traceability-and-Reconsideration.md`
- **What can an Agent do?** → `06-Participants-and-Agent-Participation.md`
- **What must a Runtime do?** → `07-Runtime-and-Conformance.md`
- **How does an engineering effort look end-to-end?** → `09-Operational-Guide.md`
