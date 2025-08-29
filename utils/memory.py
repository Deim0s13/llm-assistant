# ════════════════════════════════════════════════════════════════════
#  utils/memory.py – lightweight conversation-memory façade
# ════════════════════════════════════════════════════════════════════
"""
Simple save / load layer for previous chat turns.

Back-ends
---------
• **IN_MEMORY**  (default, zero deps, oldest→newest order)
• **REDIS**      (network)        – newest-first → flipped once on load
• **SQLITE**     (file-based)     – newest-first → flipped once on load
• “persistent” alias = redis → sqlite → in-memory
"""

from __future__ import annotations

import importlib
import json
import logging
import os
from collections.abc import Callable
from enum import Enum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

__all__ = ["MemoryBackend", "Memory", "memory"]

# --------------------------------------------------------------------
# One-shot env key used only as a bridge for the migration subprocess.
# We WRITE this snapshot when saving/clearing IN_MEMORY.
# The migration script READS it if needed. We do NOT auto-load it here.
# --------------------------------------------------------------------
_ENV_KEY = "LLM_MEM_STORE_JSON"


# ───────────────────────────── Backend factories ────────────────────────────
def _redis_factory() -> Any | None:
    try:
        return importlib.import_module("memory.backends.redis_memory_backend").RedisMemoryBackend()
    except Exception:
        return None


def _sqlite_factory() -> Any | None:
    """
    Build the SQLite backend.

    • honours $MEMORY_DB_PATH so tests can point at a tmpfile
    • falls back to data/memory.sqlite for normal runs
    • default persist=False (façade parity tests don’t write to disk)
    """
    db_path = os.getenv("MEMORY_DB_PATH", "data/memory.sqlite")
    try:
        SQLiteMB = importlib.import_module(
            "memory.backends.sqlite_memory_backend"
        ).SQLiteMemoryBackend
        return SQLiteMB(db_path=db_path, persist=False)
    except Exception:
        return None


_BACKEND_FACTORIES: dict[str, Callable[[], Any | None]] = {
    "redis": _redis_factory,
    "sqlite": _sqlite_factory,
    "in_memory": lambda: None,
    "none": lambda: None,
}


# ───────────────────────────── Helper / enum ───────────────────────────────
class MemoryBackend(str, Enum):
    NONE = "none"
    IN_MEMORY = "in_memory"
    REDIS = "redis"
    SQLITE = "sqlite"


def _normalise(raw: str) -> str:
    """Collapse things like 'MemoryBackend.SQLITE' → 'sqlite' (lower-case)."""
    raw = raw.lower()
    if raw.startswith("memorybackend."):
        raw = raw.split(".", 1)[1]
    return raw


@runtime_checkable
class _BackendProto(Protocol):  # noqa: F811
    def add_turn(self, role: str, content: str, *, cid: str = "default") -> None: ...
    def get_recent(self, *, limit: int = 50, cid: str = "default") -> list[dict[str, Any]]: ...
    def flush(self, *, cid: str = "default") -> None: ...


def create_memory(req: str | MemoryBackend) -> tuple[MemoryBackend, Any | None]:
    """Return (<resolved enum>, <backend instance | None>)."""
    raw = req.value if isinstance(req, MemoryBackend) else str(req)
    name = _normalise(raw)

    # persistent chain – redis → sqlite → in_memory
    if name == "persistent":
        for candidate in ("redis", "sqlite"):
            resolved, impl = create_memory(candidate)
            if resolved != MemoryBackend.IN_MEMORY and not (
                impl and getattr(impl, "_using_fallback", False)
            ):
                return resolved, impl
        return MemoryBackend.IN_MEMORY, None

    factory = _BACKEND_FACTORIES.get(name)
    if factory is None:
        logging.error("[Memory] unknown backend '%s' – using in_memory", name)
        return MemoryBackend.IN_MEMORY, None

    try:
        impl = factory()
        if impl is None:
            resolved = MemoryBackend.NONE if name == "none" else MemoryBackend.IN_MEMORY
            return resolved, None

        resolved = MemoryBackend(name)
        logging.info("[Memory] backend resolved → %s", resolved.value)
        return resolved, impl

    except Exception as exc:
        logging.warning("[Memory] %s backend failed (%s) – using in_memory", name, exc)
        return MemoryBackend.IN_MEMORY, None


# ─────────────────────────────── Singleton façade ───────────────────────────
class Memory:
    """Unified `.save / .load / .clear` wrapper around the active backend."""

    backend: MemoryBackend
    _instance: Memory | None = None
    _store: dict[str, list[dict[str, Any]]] = {}  # in-process store
    _impl: Any | None = None  # real backend instance

    # ───────────────────────── ctor / (re)configure ─────────────────────────
    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY) -> Memory:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.backend = MemoryBackend.NONE
            cls._instance._impl = None

        raw = backend.value if isinstance(backend, MemoryBackend) else str(backend)
        req = _normalise(raw)

        if cls._instance.backend.value != req:
            resolved, impl = create_memory(req)
            cls._instance.backend = resolved
            cls._instance._impl = impl

        return cls._instance

    # ─────────────────────────────── load ────────────────────────────────
    def load(self, session_id: str = "default") -> list[dict[str, Any]]:
        # NONE → empty
        if self.backend == MemoryBackend.NONE:
            return []

        # IN_MEMORY → read from in-process dict (oldest → newest)
        if self.backend == MemoryBackend.IN_MEMORY:
            return list(self._store.get(session_id, []))

        # Persistent backends → newest-first; we flip to chronological once
        if not self._impl:
            return []
        turns = self._impl.get_recent(cid=session_id)
        return list(reversed(turns))

    # ─────────────────────────────── save ────────────────────────────────
    def save(self, msg: dict[str, Any], *, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.NONE:
            return
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.setdefault(session_id, []).append(msg)
            os.environ[_ENV_KEY] = json.dumps(self._store)
            return

        # Guard backend instance
        if not self._impl:
            return
        self._impl.add_turn(msg["role"], msg["content"], cid=session_id)

    # ─────────────────────────────── clear ───────────────────────────────
    def clear(self, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.pop(session_id, None)
            os.environ[_ENV_KEY] = json.dumps(self._store)  # keep snapshot in sync
        elif self.backend != MemoryBackend.NONE:
            if self._impl is not None:
                self._impl.flush(cid=session_id)


# ───────────────────────── bootstrap default singleton ─────────────────────
from config.settings_loader import load_settings  # late import to avoid cycles

DEFAULT_BACKEND = load_settings().get("memory", {}).get("backend", "none")
memory: Memory = Memory(backend=DEFAULT_BACKEND)
