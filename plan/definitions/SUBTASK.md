# Subtask

## Definition

A **Subtask** is a concrete, executable action within a Work Unit. It is the
smallest unit in the planning hierarchy.

```text
Task
  └── Work Unit
        └── Subtask   ← this level
```

## Required Properties

A Subtask must be specific enough that an Agent can determine, without ambiguity:

1. **What to inspect or change** — the target file, system, or concept.
2. **Expected result** — what the state should be after the Subtask is done.
3. **Completion condition** — how to confirm the Subtask is complete.

A Subtask that cannot be evaluated without relying solely on Agent memory or
conversation history is not a valid Subtask. Rewrite it with explicit references
to files, records, or observable states.

## Prohibited Patterns

Do not create Subtasks that are:

- Vague instructions ("do the necessary work")
- Duplicate descriptions of the Work Unit objective
- Atomic to a meaningless degree ("open the file")
- Status-only labels with no action content

## Format

Within a Task file, Subtasks are expressed as:

```markdown
- [ ] <concrete action statement>
- [/] <action currently in progress>
- [x] <completed action — evidence: <where result can be verified>>
```

## Evidence Contract

A completed Subtask must contain an evidence reference that allows an independent
reader to locate or reproduce the result.

Prefer one of:

- **Artifact evidence:** repository path plus the relevant property/result.
- **Execution evidence:** exact command plus observed result.
- **Test evidence:** test identifier or suite plus pass/fail result.
- **Version-control evidence:** commit or diff reference.
- **Finding/block evidence:** explicit reason why required verification could not occur.

Examples:

```markdown
- [x] Add the validation test — evidence: tests/planning/test_recovery.py; 8 tests pass.
- [x] Update the recovery protocol — evidence: plan/README.md §Recovery Protocol; stale-CURRENT cases covered.
- [x] Review the complete diff — evidence: commit abc1234; diff --check passes.
```

The following are insufficient by themselves:

```text
evidence: verified
evidence: done
evidence: file created
```

If the result has no durable evidence, record that as a finding or block the Subtask
rather than treating the Agent assertion as evidence.

Planning evidence does not constitute AESM Runtime evidence.

## Status Values

See STATUS.md for the full list of allowed status values and their meanings.
For Subtasks, the relevant states are:

| Marker | Meaning |
|--------|---------|
| `[ ]`  | Not started |
| `[/]`  | In progress |
| `[x]`  | Complete |
| `[!]`  | Blocked — reason must be recorded immediately after the marker |

## Blocked Subtask (`[!]`) — Recovery Protocol

A blocked Subtask is not simply an unfinished one. It records a condition that
prevents legitimate progress.

Format:

```markdown
- [!] <action that cannot proceed>
  BLOCKED: <precise reason why execution cannot continue>
```

When a fresh Agent encounters `[!]` as the next required Subtask:

1. Read the text immediately following the `[!]` marker to identify the blocker.
2. Inspect the recorded evidence to understand the blocking condition.
3. Determine whether the blocking condition has actually been resolved — from
   repository state, not from conversation history.
4. If the blocker remains unresolved:
   - Surface the blocking condition to the human.
   - Stop execution of that blocked work.
   - Do not invent a workaround.
   - Do not silently substitute another Task.
   - Do not reinterpret the blocker as authorization to change scope.
5. Resume blocked work only when the blocking condition has been explicitly
   resolved in the planning record and the marker updated accordingly.

**Structural state vs. substantive evidence:** The `[!]` marker is structural
state. The blocking reason recorded after it is substantive evidence. Correct
the structural state (the marker) when the blocking condition resolves. Do not
alter the blocking reason text to make the marker appear consistent — correct
the marker to match the actual evidence.

## Granularity Rule

Do not create arbitrary micro-checklists. A Subtask should represent a coherent
action whose completion meaningfully advances the Work Unit.

If a sequence of Subtasks can only be verified together (because partial
completion has no observable result), consider merging them or expressing the
sequence as a single Subtask with an ordered description.

## Completion

A Subtask is complete when:

1. The action has been performed.
2. The result exists in the repository, test output, or another referenced artifact.
3. The evidence reference is independently checkable.
4. The Task file records completion with the evidence reference.

An Agent claim is not completion. The evidence reference is part of the completion
record.
