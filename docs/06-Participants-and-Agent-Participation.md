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

## Decision Gates

An Agent may provide information required for a Decision Gate. It may not bypass a gate, fabricate satisfaction, or represent a recommendation as an established gate outcome.

## Continuity

An Agent resumes work from authoritative Execution Context supplied by the AESM execution system. Its own conversational memory is not authoritative merely because it is available internally.

## Failure and uncertainty

The Agent must explicitly report material uncertainty, insufficient evidence, contradiction, failed verification, unmet preconditions, blocked conditions, inability to continue, and information requiring reconsideration.

Forward progress is not a justification for fabricating certainty.

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