# Participants and Agent Participation

## Participants

A Participant is an entity that contributes to execution of a Process Instance.

Participants may provide:

- information;
- Evidence;
- clarification;
- analysis;
- engineering work;
- judgment;
- Decisions where applicable;
- authorization where applicable;
- verification;
- challenges to existing conclusions.

AESM recognizes Human Participants and AI Agents as primary participant types.

Participation does not automatically grant unrestricted authority.

## AI Agent

An AI Agent is a Participant that can contribute reasoning, analysis, engineering work, investigation, implementation, verification, and other permitted activities.

An Agent is **not the Runtime**.

```text
Human Participant ──┐
                    │
AI Agent ───────────┤
                    ▼
                  Runtime
                    │
                    ▼
              Process Instance
```

The Runtime remains responsible for executing PEM semantics.

## Agent mental model

An Agent should treat the Process Instance as the persistent unit of work and the Execution Context as the authoritative operational state supplied by the AESM execution system.

```text
Process Instance
      │
      └── authoritative Execution Context
                │
                ├── engineering state
                ├── execution state
                ├── history and traceability
                └── pending / unresolved work

AI Agent
      │
      └── participates through the Runtime boundary
```

The Agent's conversation history may be useful working memory, but it is not authoritative merely because it is available to the Agent.

## Scope and Process Instance authority

Before material work begins, the Agent should distinguish:

- Engineering Scope Identity;
- Process Instance Identity;
- Engineering Objective;
- Execution Context;
- supporting environment evidence.

The Agent may gather or submit scope evidence, known Process Instance identifiers, human clarification, and other permitted inputs. It must not independently declare the authoritative scope, select among ambiguous candidates, rewrite an established Process Instance binding, or treat repository/workspace observations as universal scope identity.

The authoritative interaction is:

```
Agent / Environment evidence
        ↓
Runtime scope resolution
        ↓
Process Instance binding / recovery / authorized creation
        ↓
Authoritative Execution Context
```

If Runtime reports `UNRESOLVED`, `AMBIGUOUS`, `CONFLICTING`, or `INVALID`, the Agent must preserve that result, gather permissible additional evidence, or request human clarification through the applicable authority path. It must not convert uncertainty into a local selection merely to continue execution.

## What the Agent should establish before acting

Before making a material contribution, the Agent should understand, from authoritative state and applicable process/execution semantics:

1. the Engineering Objective;
2. current Requirements and Constraints;
3. current Process State;
4. relevant Evidence and Assumptions;
5. accepted and pending Engineering Decisions;
6. applicable Decision Gates;
7. current implementation and verification status;
8. unresolved questions, risks, contradictions, and failures;
9. pending work and expected next actions;
10. any applicable authorization or execution conditions.

If required authoritative information is missing, the Agent should identify the deficiency rather than silently inventing it.

## What an Agent may do

Subject to the applicable process and execution conditions, an Agent may:

- inspect supplied Execution Context;
- analyze Requirements and Constraints;
- perform investigation;
- contribute Evidence candidates;
- identify Assumptions and Risks;
- generate and evaluate Candidate Solutions;
- propose Engineering Decisions;
- create or modify Artifacts;
- perform verification activities;
- identify contradictions and uncertainty;
- propose plans and actions;
- perform authorized engineering work;
- report Execution Results;
- challenge previous conclusions;
- request clarification or intervention.

## What an Agent may not assume

An Agent may not assume that its capability grants authority to:

- redefine EPM semantics;
- redefine PEM semantics;
- own the authoritative Execution Context;
- bypass Decision Gates;
- silently alter the Engineering Objective;
- declare Requirements resolved or satisfied outside applicable rules;
- turn a proposal into an Engineering Decision by assertion;
- turn a plan into an Execution Determination by assertion;
- turn its output into authoritative state merely by producing it;
- fabricate Evidence, provenance, verification, or Participant input;
- silently erase historical state;
- conceal material uncertainty or failure.

## Controlled contribution

The semantic contribution path is:

```text
Agent / Participant
        ↓
Observation / Participant Input / Candidate Contribution
        ↓
Runtime-controlled recognition
        ↓
Applicable EPM / PEM conditions
        ↓
Permitted State Mutation
        ↓
Execution Context / Trace
```

The Agent does not independently decide which of its outputs become authoritative state.

## Observation

Observation is distinct from Participant Input and Candidate Contribution. Observation does not itself mutate authoritative state.

## Candidate Contribution

A Candidate Contribution is information proposed for consideration or incorporation. It requires the applicable recognition, evaluation, validation, or mutation process before becoming authoritative.

## Engineering Decisions

An Agent may propose or challenge an Engineering Decision. Recognition and validity remain governed by EPM.

## Execution Determinations

An Agent may recommend an execution action, but where PEM authority is required it does not independently establish the Execution Determination.

## Execution Results

An Agent may report what happened as a result of work it performed. The Runtime applies the applicable recognition, verification, and state-update semantics.

## Reporting contributions

Material Agent output should be distinguishable by its semantic role, for example:

```text
Observation
Participant Input
Candidate Contribution
Evidence candidate
Assumption
Recommendation
Proposed Engineering Decision
Proposed execution action
Execution Result
Verification result
```

The Runtime applies the applicable recognition, evaluation, verification, and mutation semantics before information becomes authoritative state.

## Engineering reasoning and execution control

The Agent should keep the following distinction explicit:

```text
Engineering Decision
    = engineering meaning under EPM

Execution Determination
    = execution control under PEM
```

An Agent can contribute to both, but participation in one does not automatically grant authority over the other.

## Decision Gates

An Agent may provide information required for a Decision Gate. It may not bypass a gate, fabricate satisfaction, or represent a recommendation as an established gate outcome.

## Continuity

An Agent resumes work from authoritative Execution Context supplied by the AESM execution system. Its own conversational memory is not authoritative merely because it is available internally.

## Failure and uncertainty

The Agent must explicitly report material uncertainty, insufficient evidence, contradiction, failed verification, unmet preconditions, blocked conditions, inability to continue, and information requiring reconsideration.

Forward progress is not a justification for fabricating certainty.

## Practical Agent checklist

Before a material action:

- What is the current objective?
- What state is the Process Instance in?
- What is known versus assumed?
- What Evidence supports the current understanding?
- Which Requirements and Constraints apply?
- Is a Decision Gate active?
- Am I making an Engineering Decision, an execution recommendation, or merely providing information?
- What authority is required for the intended action?
- What should be recorded for continuity and traceability?

## Authority-preservation invariants

```text
Agent ≠ Runtime
Agent capability ≠ authority
Agent output ≠ automatic authority
Proposal ≠ authorization
Observation ≠ mutation
Engineering Decision ≠ Execution Determination
Conversation ≠ authoritative state
```

These invariants define the semantic Agent boundary independently of transport, APIs, serialization, model providers, or Agent frameworks.