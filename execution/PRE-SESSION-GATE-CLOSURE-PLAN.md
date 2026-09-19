# Pre-Session Gate Closure — Execution Plan

## Purpose

Close the controller-owned readiness gates for the Fresh-Agent DBP Continuation experiment without starting Session A.

This work unit is complete only when the Human Controller has directly observed and recorded all mandatory pre-session conditions. Repository inspection alone cannot close the environment gates.

## Controlled work sequence

### Controller authorization record

Record:
- Authorized target: Yes/No
- Exact approval timestamp
- Controller identity
- Session-A authorization: No until all other mandatory gates pass

The target is the already-selected `Edit_Review_Form` change recorded in the Controller workbook. Do not begin DBP implementation during gate closure.

### Separate-Agent capability verification

Directly demonstrate:
1. A fresh Agent session can be started.
2. The new session is independently distinguishable from the current session.
3. The first Agent session can end without reusing its conversation context.

Record the session identifiers or equivalent evidence. A failed check is an Environment Defect.

### ProcessStore root identification

Record the exact filesystem path of the selected ProcessStore root.

The root must be the environment's existing authoritative ProcessStore root. Do not create a replacement root merely for this experiment.

Record how the root was established and verify that both independent Agent sessions can access the same location.

### ProcessStore persistence boundary test

Using the selected root and the authorized PI bootstrap:

1. In the first Agent session, perform an authoritative ProcessStore write.
2. Confirm `process.json`, `context.json`, and `history.jsonl` exist under the PI directory.
3. End the first Agent session.
4. Start a genuinely separate Agent session.
5. Supply only the permitted continuation bootstrap information.
6. Independently read/recover the PI from the same ProcessStore root.
7. Confirm the recovered identity and authoritative state originate from persisted artifacts rather than conversation history or copied context.

Record the PI ID, root, relevant versions, representative history entry, session identifiers, timestamps, and artifact paths.

### PI bootstrap authorization

Record exactly one of:
- Existing PI ID authorized for the experiment; or
- Explicit authorization for Session A to create a new PI.

Do not allow Session A to invent an unrecorded bootstrap policy.

### Gate closure

Update the Controller workbook and validation artifact from direct observations.

Session-A authorization becomes `Yes` only when:
- authorized target = Yes;
- all separate-Agent capability checks = Pass;
- all ProcessStore persistence checks = Pass;
- ProcessStore root is recorded;
- PI bootstrap is explicitly authorized.

Otherwise Session-A authorization remains `No`.

## Evidence preservation

Retain:
- the prior readiness-guard failure report;
- exact ProcessStore root;
- PI bootstrap record;
- session identifiers;
- timestamps;
- persisted PI artifacts;
- representative `history.jsonl` entries;
- any command/output or screenshots used for direct observation.

Do not overwrite or reinterpret failed readiness evidence.

## Stop conditions

Stop before Session A if:
- the selected ProcessStore root cannot be identified;
- the root is not persistent across independent sessions;
- a fresh Agent session cannot be demonstrated;
- recovery requires transcript/context copying;
- PI bootstrap authorization is missing;
- any mandatory gate fails.

Classify an environment capability failure as `Environment Defect`.

## Explicit non-goals

This work unit does not:
- implement the DBP change;
- start Session A;
- start Session B;
- modify AESM Runtime semantics;
- redefine the locked evidence contract;
- declare the continuation experiment successful.

## Completion condition

The work unit is ready to hand off to Session A only after the Human Controller has filled the gate records from direct observation and explicitly recorded Session-A authorization as `Yes`.
