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

Evidence is required on completion. An Agent marking a Subtask complete must be
able to state where the result of that Subtask can be verified. If no persistent
evidence exists, that is itself a finding to record.

## Status Values

See STATUS.md for the full list of allowed status values and their meanings.
For Subtasks, the relevant states are:

| Marker | Meaning |
|--------|---------|
| `[ ]`  | Not started |
| `[/]`  | In progress |
| `[x]`  | Complete |
| `[!]`  | Blocked — reason must be recorded immediately after |

## Granularity Rule

Do not create arbitrary micro-checklists. A Subtask should represent a coherent
action whose completion meaningfully advances the Work Unit.

If a sequence of Subtasks can only be verified together (because partial
completion has no observable result), consider merging them or expressing the
sequence as a single Subtask with an ordered description.

## Completion

A Subtask is complete when:
1. The action has been performed.
2. The result exists in the repository or is verifiable from a referenced artifact.
3. The Task file records completion with available evidence.

An Agent claim is not completion. The evidence reference is the completion record.
