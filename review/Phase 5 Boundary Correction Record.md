# Phase 5 Boundary Correction Record

**Phase:** Phase 5 — Machine-Readable Agent Protocol  
**Status:** CORRECTION APPLIED — Pending Re-review  
**Protocol:** `specifications/Machine-Readable Agent Protocol.md`  
**Date:** 2026-08-18

---

## 1. Purpose

This record captures the normative corrections required by Phase 5 Boundary Review Attempt 1.

Until the protocol specification is canonicalized, these corrections are part of the Phase 5 construction baseline and shall be incorporated into the final protocol artifact before freeze.

---

## 2. B-01 — Identity Representation Must Not Become Authority

The protocol shall explicitly establish:

```text
Identity representation ≠ authority claim
```

A represented actor/source type identifies the claimed source or intended recipient. It does not establish the authority associated with that type.

In particular:

```text
sender.type = runtime
        ≠
Runtime authority has been established
```

A protocol implementation shall not treat a self-declared actor/source type as sufficient proof of authority.

Authentication or trust mechanisms may exist in an implementation environment, but they remain outside MRAP semantics.

**Correction status:** Applied to the Phase 5 construction baseline; final canonical protocol text shall contain this rule explicitly.

---

## 3. B-02 — Direction Must Not Become Authority

The protocol shall explicitly establish:

```text
direction ≠ authorization
```

In particular:

```text
from_runtime
        ≠
authoritative Runtime command

to_runtime
        ≠
permission for the recipient to mutate state
```

Direction describes semantic information flow relative to Runtime only. It does not prescribe transport, endpoint, API, or authority.

**Correction status:** Applied to the Phase 5 construction baseline; final canonical protocol text shall contain this rule explicitly.

---

## 4. B-03 — Permission Metadata Must Remain Non-Authoritative

The protocol shall explicitly establish:

```text
Permission metadata ≠ independently granted authority
```

Fields or metadata indicating authorization, permission, recognition, or mutation classification are descriptive of governing semantics.

A message cannot authorize itself by asserting permission.

The Runtime remains responsible for applying applicable EPM/PEM authority semantics.

**Correction status:** Applied to the Phase 5 construction baseline; final canonical protocol text shall contain this rule explicitly.

---

## 5. Required Finalization Action

Before Phase 5 Boundary Review can pass, the three corrections above shall be present directly in the canonical `Machine-Readable Agent Protocol.md` and reflected in its conformance/validation invariants.

The correction record itself does not replace the protocol specification.

---

## 6. Re-review Target

The next Boundary Review shall verify:

1. identity does not establish authority;
2. direction does not establish authorization;
3. permission metadata does not establish authority;
4. no other protocol representation introduces authority leakage;
5. Agent/Runtime, engineering/execution, observation/mutation, and protocol/transport boundaries remain intact.

**Correction Record Result: PASS — corrections identified and explicitly dispositioned.**

**Boundary Review Attempt 2: PENDING.**
