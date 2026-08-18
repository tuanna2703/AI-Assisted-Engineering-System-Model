# Phase 4 — Contract Boundary Matrix

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 4 — Agent Execution Contract  
**Artifact:** Contract Boundary Matrix  
**Status:** Working Baseline — Review Revision 1  
**Basis:** Frozen Phase 3 AESM Operational Model

---

## 1. Purpose

This artifact establishes the semantic boundary between the AESM operational system and an Agent before the Agent Execution Contract is specified in detail.

It defines:

- what the AESM system provides to an Agent;
- what the Agent may inspect, propose, or perform;
- what the Agent may return;
- which outputs are candidate contributions rather than authoritative state;
- where EPM, PEM, the AESM Operational Model, Runtime, and Agent authority begin and end;
- the continuity boundary between Agent interaction state and authoritative Execution Context.

This matrix is a boundary specification. It does not define a transport protocol, API, message format, serialization format, authentication mechanism, Agent framework, or Runtime architecture.

---

## 2. Normative Authority

The following authority order is preserved:

```text
EPM
  ↓ engineering meaning and validity
PEM
  ↓ execution semantics and control
AESM Operational Model
  ↓ authoritative operational representation
Agent Execution Contract
  ↓ Agent-facing semantic interface
Agent
```

A lower layer MUST NOT redefine the semantics or authority of a higher layer.

The Agent Execution Contract MUST therefore be derived from the frozen Operational Model and MUST NOT introduce an independent engineering process model.

---

## 3. Fundamental Boundary

The Agent is a participant in AESM execution.

The following distinctions are normative:

```text
Agent ≠ Runtime
Agent ≠ EPM
Agent ≠ PEM
Agent ≠ Execution Context
Agent output ≠ authoritative state
Agent proposal ≠ authorized execution
Agent execution result ≠ Engineering Decision
```

The Agent may contribute to engineering work and execution, but authoritative state changes remain subject to the applicable EPM, PEM, validation, and state-mutation rules.

---

## 4. Contract Boundary Matrix

| Boundary | AESM provides | Agent may do | Agent returns | Authority / state effect |
|---|---|---|---|---|
| **Context** | Authoritative Execution Context and relevant Process State | Inspect and use authoritative context | Context-dependent response | AESM Operational Model; inspection is non-mutating |
| **Engineering Objective** | Current objective and applicable objective history | Interpret, analyze, identify implications, propose changes where permitted | Analysis or candidate objective-change proposal | EPM governs meaning; objective changes require explicit controlled handling |
| **Requirements** | Relevant Requirements and resolution/satisfaction state | Analyze, assess implications, identify gaps, propose requirement-related contributions | Candidate analysis, evidence, evaluation, or proposal | EPM governs validity; Agent does not silently resolve or satisfy Requirements |
| **Constraints** | Applicable Constraints | Evaluate compliance and implications | Candidate evaluation or proposal | EPM governs engineering validity |
| **Investigation** | Investigation objective, scope/context, current evidence, and sufficiency state | Conduct permitted investigation activities and analyze results | Investigation contributions, Evidence candidates, sufficiency assessment | EPM governs investigation objective and sufficiency |
| **Evidence** | Accepted and relevant Evidence with provenance/context where available | Inspect, analyze, compare, assess relevance/reliability | Evidence candidate or assessment | Agent output is not automatically accepted Evidence |
| **Assumptions** | Current Assumptions and status | Assess, challenge, propose, or provide basis for assumptions | Candidate Assumption or assessment | EPM-controlled knowledge mutation |
| **Risks** | Relevant Risks and treatment/status | Identify, assess, propose treatment | Candidate Risk contribution or assessment | EPM-controlled engineering state |
| **Candidate Solutions** | Existing candidate solutions and evaluations | Generate, compare, evaluate, refine | Candidate Solution and evaluation | Candidate state until appropriately validated |
| **Evaluation** | Applicable criteria and available evidence/context | Perform permitted analysis/evaluation | Candidate Evaluation | Evaluation becomes authoritative only through applicable validation/state mutation |
| **Engineering Decision** | Existing accepted/pending Decisions, rationale, gates, and basis | Analyze and propose a Decision | Proposed Engineering Decision and rationale | EPM authority; Agent cannot unilaterally make authoritative engineering state |
| **Verification** | Verification requirements, criteria, and relevant state | Perform or assist permitted verification | Verification Result candidate | EPM determines validity; result must pass applicable validation |
| **Artifact** | Relevant Artifacts and status/version information | Create, inspect, modify, or validate artifacts when authorized | Artifact result/reference | Artifact state follows applicable validation and execution rules |
| **Process State** | Current Process State, conditions, gates, and valid Transition Rules | Evaluate supplied state and identify what is required next | State analysis or execution/progression proposal | Process State semantics belong to EPM; PEM controls execution |
| **Decision Gates** | Applicable gates and current evaluation status | Evaluate supplied evidence/context and propose gate assessment | Gate evaluation candidate | Gate validity is governed by EPM; dependent transition remains controlled by PEM |
| **Observation** | Observable context/environment information | Observe and analyze without directly mutating authoritative state | Observation | Observation is non-authoritative until applicable validation/state mutation |
| **Planning** | Execution conditions, authorization basis, and relevant state | Propose or refine an execution Plan where permitted | Plan proposal/update | PEM controls execution planning |
| **Execution Determination** | PEM-defined execution conditions and authority | Provide information supporting determination; request/prepare execution | Execution determination proposal/request where contract permits | Execution Determination is distinct from Engineering Decision and remains PEM-controlled |
| **Execution Action** | Authorized action specification and preconditions | Perform an authorized action or provide an action proposal, depending on contract | Execution Result | PEM/Runtime authority; Agent cannot bypass authorization |
| **Execution Result** | Result requirements and validation context | Interpret/validate observed result and provide supporting information | Execution Result contribution | Result is subject to PEM-controlled recording and validation |
| **State Mutation** | Authorized mutation pathway | Submit candidate contribution or requested mutation through contract | Mutation request/contribution | Only authorized state mutation may change authoritative Execution Context |
| **Traceability** | Trace requirements and relevant references | Supply provenance, basis, action/result references, and other trace data | Trace-supporting information | PEM/Operational Model preserve reconstructability |
| **Reconsideration** | Trigger conditions and affected engineering state | Identify impact, analyze affected conclusions, propose revisions | Reconsideration analysis and revised candidate conclusions | EPM governs reconsideration semantics; historical state must be preserved |
| **Failure / Uncertainty** | Current state and applicable conditions | Report inability, ambiguity, insufficiency, conflict, or failure | Structured uncertainty/failure contribution | Does not authorize silent progression |
| **Continuity** | Authoritative persisted Execution Context and pending continuation information | Resume work from supplied authoritative state | Contributions/results for continuation | AESM Execution Context remains authoritative; Agent memory is non-authoritative |

---

## 5. Input Boundary

The Agent MAY receive only information that is relevant and authorized for the current interaction.

Inputs SHOULD be organized conceptually into:

```text
Execution Context
Process State
Engineering Knowledge
Execution Conditions
Applicable Authorizations
Relevant History
Observable Environment Information
Interaction Instructions
```

The Agent MUST be able to distinguish, where applicable:

- authoritative state;
- accepted Evidence;
- assumptions;
- unresolved or contested information;
- candidate contributions;
- pending Decisions;
- execution authorization;
- observations.

The Agent MUST NOT infer authority merely from the presence of information in an input.

---

## 6. Inspection Boundary

The following inspection operations correspond to the Phase 3 observation operation class:

- inspect Execution Context;
- inspect Process State;
- inspect Engineering Knowledge;
- inspect Conditions;
- observe Environment.

Inspection is non-mutating.

An Agent MUST NOT treat inspection as permission to modify the inspected state.

---

## 7. Contribution Boundary

Agent-produced engineering content enters AESM as a candidate contribution unless the applicable operation explicitly establishes another status through authorized validation and mutation.

Candidate contribution classes include:

- Participant Input;
- Observation;
- Evidence Candidate;
- Assumption;
- Candidate Solution;
- Evaluation;
- proposed Engineering Decision;
- Verification Result;
- Artifact Result.

The transformation is conceptually:

```text
Agent output
    ↓
Candidate contribution
    ↓
Validation / evaluation
    ↓
Authorized state mutation
    ↓
Authoritative Execution Context
```

An Agent MUST NOT silently skip the validation/state-mutation boundary.

---

## 8. Execution Boundary

Execution is governed by PEM.

The Agent may participate in execution only within the authority provided by the applicable execution context and contract.

The following distinctions MUST remain explicit:

```text
Agent proposal
    ≠
Execution Determination

Execution Determination
    ≠
Execution authorization

Execution authorization
    ≠
Runtime execution

Runtime execution
    ≠
Authoritative engineering conclusion
```

Where the Agent performs an authorized action, the resulting information MUST remain traceable to the action, its authorization basis, its result, and the resulting state update.

---

## 9. State-Mutation Boundary

Only an authorized mutation pathway may change authoritative Execution Context.

Agent output, tool output, environment events, and observations MUST NOT directly mutate authoritative state merely because they are available to the Runtime.

A conforming implementation MUST preserve the Phase 3 authority path:

```text
Participant / Agent / Tool / Environment output
                    ↓
               Observation
                    ↓
          Candidate Contribution
                    ↓
        Validation Assessment
                    ↓
       Authorized State Mutation
                    ↓
          Execution Context
                    ↓
             Execution Trace
```

Implementations MAY represent these stages differently internally, but MUST preserve their semantic distinctions.

---

## 10. Decision Boundary

An Agent may reason about, evaluate, and propose engineering decisions.

An Agent MUST NOT represent a generated conclusion as an accepted Engineering Decision unless the applicable EPM-defined decision authority and validation conditions have been satisfied.

Similarly:

```text
Engineering Decision
        ≠
Execution Determination
```

An execution instruction must not be treated as an engineering decision, and an engineering decision must not be treated as execution authorization merely because the Agent produced it.

---

## 11. Failure and Uncertainty Boundary

The Agent MUST be able to return uncertainty instead of manufacturing unsupported conclusions.

The contract SHOULD support at least these semantic conditions:

- insufficient evidence;
- unresolved requirement;
- conflicting evidence;
- ambiguous instruction/objective;
- failed evaluation;
- failed verification;
- blocked execution;
- unavailable capability;
- invalid or inconsistent context;
- reconsideration required;
- unable to proceed safely.

Such a response MUST NOT be interpreted as successful progression unless the applicable EPM/PEM conditions independently establish that progression is valid.

---

## 12. Continuity Boundary

The Agent's conversational or internal memory is not authoritative engineering state.

A conforming system MUST be able to resume from persisted Execution Context without depending on the Agent remembering a previous conversation.

Therefore:

```text
Agent Session A
      ↓
validated state mutations
      ↓
Authoritative Execution Context
      ↓
Agent Session B
      ↓
continued execution
```

A new Agent session MUST receive sufficient authoritative context to reconstruct the operational situation required for its assigned work.

---

## 13. Prohibited Agent Behaviors

Unless explicitly authorized through the applicable higher-level semantics and execution controls, an Agent MUST NOT:

1. redefine EPM semantics;
2. redefine PEM semantics;
3. silently modify authoritative Execution Context;
4. treat its own output as authoritative engineering knowledge without validation;
5. declare an Engineering Decision accepted merely because it generated it;
6. treat an Engineering Decision as an Execution Determination;
7. bypass required Decision Gates;
8. bypass required verification conditions;
9. perform a prohibited or unauthorized execution action;
10. erase or overwrite historical state in a way that destroys traceability;
11. silently change the Engineering Objective;
12. silently convert an Observation into accepted Evidence;
13. represent uncertainty as established fact;
14. infer engineering progression solely from activity completion;
15. use conversational memory as a substitute for authoritative Execution Context.

---

## 14. Phase 4 Derivation Rule

The subsequent Agent Execution Contract MUST be derivable from this matrix without changing the semantic boundaries established here.

The detailed contract must define, at minimum:

- Agent identity and role;
- input semantics;
- available inspection operations;
- contribution semantics;
- execution participation semantics;
- return/result semantics;
- authority and authorization semantics;
- failure and uncertainty semantics;
- traceability requirements;
- continuity requirements.

Machine-readable protocol structures are deferred to a later phase.

---

## 15. Review Status

**Current status:** Working Baseline — Review Revision 1.

This artifact is the first Phase 4 boundary specification. It is not yet a frozen Agent Execution Contract.

The next review MUST test this matrix against:

- the frozen AESM Operational Model;
- EPM authority boundaries;
- PEM execution-control boundaries;
- Execution Context semantics;
- controlled mutation;
- traceability;
- reconsideration;
- continuity.

Only after those checks pass should the matrix be promoted into the normative **Agent Execution Contract**.
