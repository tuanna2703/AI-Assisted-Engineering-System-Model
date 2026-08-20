# Documentation Source Map

This document records how the validated content of the former AESM documentation set was decomposed into the unified documentation set.

It is a transformation trace, not a second conceptual model.

| Former source | Principal content retained | New destination |
|---|---|---|
| AESM Architecture Model | AESM identity and purpose | `01-Overview.md` |
| AESM Architecture Model | Entities, layers, boundaries, authority | `02-System-Model.md` |
| AESM Architecture Model | Process Instance primacy | `01-Overview.md`, `05-Process-Instance-and-Execution-Context.md` |
| AESM Architecture Model | Persistent Execution Context | `05-Process-Instance-and-Execution-Context.md` |
| AESM Architecture Model | Canonical operational scenario | `09-Operational-Guide.md` |
| AESM Architecture Model | Architectural invariants | `02-System-Model.md`, `10-Reference.md` |
| AESM Operational Flow | End-to-end engineering flow | `09-Operational-Guide.md` |
| AESM Operational Flow | Process Instance lifecycle | `05-Process-Instance-and-Execution-Context.md`, `09-Operational-Guide.md` |
| AESM Operational Flow | Iteration and reconsideration | `03-Engineering-Model.md`, `08-Continuity-Traceability-and-Reconsideration.md` |
| Engineering Process Model | Engineering meaning | `03-Engineering-Model.md` |
| Engineering Process Model | Requirements, Constraints, Investigation, Evidence | `03-Engineering-Model.md` |
| Engineering Process Model | Solutions and Engineering Decisions | `03-Engineering-Model.md` |
| Engineering Process Model | Process States and Decision Gates | `03-Engineering-Model.md` |
| Engineering Process Model | Verification, progress, reconsideration, completion | `03-Engineering-Model.md`, `08-Continuity-Traceability-and-Reconsideration.md` |
| Process Execution Model | Execution semantics | `04-Execution-Model.md` |
| Process Execution Model | Observe/Evaluate/Plan/Execute/Verify/Update cycle | `04-Execution-Model.md` |
| Process Execution Model | Execution Determination | `04-Execution-Model.md`, `10-Reference.md` |
| Process Execution Model | Recognition and controlled mutation | `04-Execution-Model.md`, `07-Runtime-and-Conformance.md` |
| Process Execution Model | Failure, uncertainty, suspension, resumption | `04-Execution-Model.md`, `08-Continuity-Traceability-and-Reconsideration.md` |
| Agent Execution Contract | Agent boundary | `06-Participants-and-Agent-Participation.md` |
| Agent Execution Contract | Agent capabilities and restrictions | `06-Participants-and-Agent-Participation.md` |
| Agent Execution Contract | Authority-preservation invariants | `06-Participants-and-Agent-Participation.md`, `10-Reference.md` |
| Agent Execution Contract | Controlled contribution and continuity | `06-Participants-and-Agent-Participation.md`, `08-Continuity-Traceability-and-Reconsideration.md` |
| Runtime Conformance Model | Runtime definition and responsibilities | `07-Runtime-and-Conformance.md` |
| Runtime Conformance Model | Runtime control boundary | `07-Runtime-and-Conformance.md` |
| Runtime Conformance Model | Recognition, mutation, state transition, gates | `07-Runtime-and-Conformance.md` |
| Runtime Conformance Model | Continuity, recovery, lifecycle | `05-Process-Instance-and-Execution-Context.md`, `07-Runtime-and-Conformance.md` |
| Runtime Conformance Model | Conformance requirements and evidence | `07-Runtime-and-Conformance.md` |

## Transformation rules

1. Repeated concepts were consolidated around one canonical explanation.
2. Perspective-specific semantics were retained where they add meaning rather than being treated as accidental duplication.
3. Development-phase metadata was not carried into the conceptual documentation unless it affects current semantics.
4. Implementation-specific details remain non-normative unless explicitly required by AESM semantics.
5. The new documentation is organized for reader comprehension rather than historical document ownership.
6. The source documents were validated before transformation; this map does not establish new AESM semantics.

## Completeness criterion

The replacement set is considered structurally complete when every substantive concept in the former six documents has a destination in the unified set and no former document remains necessary as a source of AESM meaning.
