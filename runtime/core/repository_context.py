"""Active Repository Context — explicit ingress for repository-local AESM persistence.

The Active Repository Context is the authoritative, immutable binding between
an AESM Runtime session and its repository.  It is the sole mechanism through
which a repository root enters the ProcessStore.

Architectural invariant:

    Execution Environment
            │
            │ establishes repository context
            ▼
    Runtime initialization
            │
            ▼
    ActiveRepositoryContext
            │
            ▼
    ProcessStore
            │
            ▼
    <repository-root>/.aesm

No other component may independently select or discover the AESM persistence root.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ActiveRepositoryContext:
    """Immutable, validated binding of an AESM session to a repository root.

    The context is frozen: it cannot be mutated after construction.
    Changing repositories requires a new Runtime/session context.

    Validation rules (enforced at construction):
    - ``repository_root`` must be provided (non-empty)
    - ``repository_root`` must exist in the filesystem
    - ``repository_root`` must be a directory

    The context does NOT perform git-repository detection or any other form
    of implicit repository discovery.  The caller — the Execution Environment —
    is responsible for supplying the correct, intended repository root.
    """

    repository_root: Path

    def __post_init__(self) -> None:
        # Allow str input for ergonomics; coerce to Path internally.
        # frozen=True means we must use object.__setattr__ to set coerced value.
        if isinstance(self.repository_root, str):
            object.__setattr__(self, "repository_root", Path(self.repository_root))

        root = self.repository_root

        if not root:
            raise ValueError("repository_root must be a non-empty path")

        if not root.exists():
            raise ValueError(
                f"repository_root does not exist: {root}"
            )

        if not root.is_dir():
            raise ValueError(
                f"repository_root is not a directory: {root}"
            )

    def aesm_root(self) -> Path:
        """Return the authoritative AESM persistence root for this repository.

        Resolves to ``<repository_root>/.aesm``.

        This is the only path component injected into ProcessStore.
        ProcessStore never discovers this path independently.
        """
        return self.repository_root / ".aesm"
