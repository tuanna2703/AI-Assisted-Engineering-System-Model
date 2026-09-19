"""AESM Persistence Concurrency and Freshness Policy — authoritative record.

This module records the governing concurrency rules for AESM Process Instance
persistence.  These rules are enforced by ProcessStore at runtime.

================================================================================
CONCURRENCY POLICY (initial)
================================================================================

Single-writer rule
------------------
A Process Instance has ONE active Runtime writer at a time.

    PI-A
     └── Runtime A     ← active writer       ✓ supported

    PI-A
     ├── Runtime A     ← writer              ✗ NOT supported
     └── Runtime B     ← writer

Relaxing this restriction requires a separate architectural decision.
No automatic locking mechanism is implemented in the initial model.
The single-writer rule is operationally enforced by the Execution Environment.

================================================================================
FRESHNESS / STALE-WRITE POLICY
================================================================================

A Runtime must not blindly overwrite newer persisted state.

Mechanism: ``ProcessStore.save_context()`` reads the currently persisted
``version`` field before writing.  If ``persisted_version > in_memory_version``,
the write is rejected with ``PersistenceError("stale write rejected: ...")``.

Example scenario this guards against:

    Runtime A loaded context at version N
    Environment B persists context at version N+1
    Runtime A attempts write based on version N  →  REJECTED

================================================================================
GIT DIVERGENCE / CONFLICT POLICY
================================================================================

The initial implementation does NOT provide semantic merging of AESM PI state.

If two environments independently modify the same PI and Git produces a conflict:

    Unresolved AESM Git conflict
            ↓
    No Process Instance execution
            ↓
    Explicit resolution required

Mechanism: ``ProcessStore.load_instance()``, ``load_context()``, and
``history()`` check for Git conflict markers (``<<<<<<<``, ``=======``,
``>>>>>>>``) before parsing any PI file.  Presence of a conflict marker raises
``PersistenceError("unresolved Git conflict in PI state: ...")``.

Automatic semantic merging is deferred to a future architectural decision.
"""
