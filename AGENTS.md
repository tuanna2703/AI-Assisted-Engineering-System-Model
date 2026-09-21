# AESM Agent Operating Guidance

This file is persistent Agent guidance for an Execution Environment that loads repository-level `AGENTS.md` instructions.

It does not redefine AESM semantics. The canonical `docs/` set remains authoritative for EPM, PEM, Process Instance, Execution Context, Runtime, and Execution Environment semantics.

## Operating Rules

- Treat AESM as the governing engineering-process model for work performed under this repository.
- Keep these roles distinct:
  - **Human / AI Agent:** performs and reasons about engineering work.
  - **Execution Environment:** provides the interaction and tooling surface.
  - **Runtime:** governs authoritative process execution and state mutation.
  - **Process Instance / Execution Context:** persistent process state and operational context.
- Conversation history is not authoritative Process Instance state.
- Before continuing an AESM-governed task, obtain the current authoritative Process Instance / Execution Context through the available Runtime interface when one is available.
- Do not fabricate Process Instance state, Runtime-recognized evidence, decisions, artifacts, verification, lifecycle state, or completion status from conversation text alone.
- Treat Runtime responses and persisted Process Instance / Execution Context state as authoritative for governed state.
- Use Runtime-mediated operations for authoritative state mutations. Do not bypass Runtime authority by directly editing authoritative state files.
- Distinguish engineering work from recognition of its process-state consequences. Completing an engineering action does not by itself prove that the corresponding AESM state transition or evidence has been recognized by Runtime.
- When process continuity matters, recover the existing Process Instance rather than creating a replacement solely because the Agent/session changed.
- Record relevant evidence, decisions, artifacts, and verification through the established Runtime interface when those capabilities are applicable.
- Do not introduce MCP, skills, IDE-specific extensions, new persistence stores, or generalized orchestration unless a demonstrated implementation gap requires them.

## Working Sequence

For an AESM-governed engineering request:

1. Read the applicable canonical guidance in `docs/`.
2. Establish or recover the relevant persistent Process Instance.
3. Obtain the authoritative Execution Context.
4. Perform the engineering investigation and implementation work.
5. Use Runtime-mediated operations to recognize applicable process evidence, decisions, artifacts, verification, and state changes.
6. Re-read authoritative state after Runtime mutations when continuing execution.
7. Verify the engineering result independently.
8. Do not claim AESM participation unless the execution provides observable evidence that the Agent interacted with the Process Instance / Runtime.

## Evidence Discipline

The following are not, by themselves, evidence of AESM participation:

- the presence of this file;
- the presence of AESM documentation;
- a successful unit test of the Runtime or bridge;
- an Agent statement that it followed AESM;
- a Process Instance created without Agent interaction;
- manually fabricated or backfilled process evidence after engineering work.

The minimum useful evidence for an empirical AESM execution includes an Agent-mediated Process Instance interaction, authoritative Context acquisition, at least one Runtime-mediated mutation caused by the Agent's work, persisted resulting state/history, the engineering artifact, and verification evidence.

## Authority Boundary

This guidance is intentionally limited to Agent behavior. It does not grant the Agent authority to redefine AESM semantics or mutate Runtime-owned authoritative state outside supported Runtime operations.

For semantic questions, consult the canonical `docs/` material rather than extending this file with new AESM rules.


## Repository Work Records

- `docs/` is the canonical AESM knowledge surface. It defines what AESM means and must not be replaced by implementation records.
- `runtime/`, `bridge/`, and other executable directories contain implementation, not engineering records.
- `tests/` contains executable verification. Test results are evidence; do not duplicate test logic in Markdown records.
- `.aesm/` is repository-local authoritative Process Instance / Execution Context state where present. Do not treat Markdown records as execution state.
- `IMPLEMENTATION_PLAN.md` contains current authorized work and progress.
- `IMPLEMENTATION_BASELINE.md` records the current implementation baseline.
- `implementation/` contains only selected, concise, non-canonical engineering records that preserve important implementation findings, empirical validation, reconciliation, or other durable evidence not already represented adequately by docs, source, tests, or `.aesm/`.
- Do not create a separate top-level `execution/` directory. Execution is an activity/state governed by Runtime and persisted under `.aesm/`; Markdown descriptions of that activity belong in `implementation/` only when they have durable value.
- Do not use `implementation/` as a session transcript, task scratchpad, duplicate plan, duplicate specification, or archive of every intermediate step.
- When a record is fully superseded by canonical documentation, executable tests, current implementation, or a later durable validation record, remove it rather than creating another historical copy.
