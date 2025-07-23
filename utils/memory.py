# ════════════════════════════════════════════════════════════════════
#  utils/memory.py – lightweight conversation memory façade
# ════════════════════════════════════════════════════════════════════
"""
Simple save/load layer for previous chat turns.

Back-ends
---------
• in-process **IN_MEMORY**  (default, zero deps)
• **REDIS**                 (network, redis-py)
• **SQLITE**                (file-based, std-lib)
• “persistent” alias = redis → sqlite → in-memory
"""

from __future__ import annotations

import logging
import importlib
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Tuple

__all__ = ["MemoryBackend", "Memory", "memory"]

# ─────────────────────────── Backend registry ────────────────────────────
def _redis_factory() -> Any | None:
    try:
        RedisMB = importlib.import_module(
            "memory.backends.redis_memory_backend"
        ).RedisMemoryBackend
        return RedisMB()
    except Exception:
        return None            # import error or constructor failure

def _sqlite_factory() -> Any | None:
    try:
        SQLiteMB = importlib.import_module(
            "memory.backends.sqlite_memory_backend"
        ).SQLiteMemoryBackend
        return SQLiteMB()
    except Exception:
        return None

_BACKEND_FACTORIES: dict[str, Callable[[], Any | None]] = {
    "redis"     : _redis_factory,
    "sqlite"    : _sqlite_factory,
    "in_memory" : lambda: None,
    "none"      : lambda: None,
}

# ─────────────────────────── Helper: resolve backend ─────────────────────
class MemoryBackend(str, Enum):
    NONE       = "none"
    IN_MEMORY  = "in_memory"
    REDIS      = "redis"
    SQLITE     = "sqlite"

def create_memory(req: str | MemoryBackend) -> Tuple[MemoryBackend, Any | None]:
    """
    Return (resolved_enum, impl|None) for requested backend string/enum.
    Accepts 'persistent' alias → redis ⟶ sqlite ⟶ in_memory.
    """
    name = req.value if isinstance(req, MemoryBackend) else str(req).lower()

    # persistent chain
    if name == "persistent":
        for cand in ("redis", "sqlite"):
            resolved, impl = create_memory(cand)
            if resolved != MemoryBackend.IN_MEMORY and not (
                impl and getattr(impl, "_using_fallback", False)
            ):
                return resolved, impl
        return MemoryBackend.IN_MEMORY, None

    # normal lookup
    factory = _BACKEND_FACTORIES.get(name)
    if factory is None:
        logging.error("[Memory] unknown backend '%s' – using in_memory", name)
        return MemoryBackend.IN_MEMORY, None

    try:
        impl = factory()
        try:
            resolved = MemoryBackend(name)
        except ValueError:               # safety for weird strings
            resolved = MemoryBackend.IN_MEMORY
        logging.info("[Memory] backend resolved → %s", resolved.value)
        return resolved, impl
    except Exception as exc:
        logging.warning("[Memory] %s backend failed (%s) – using in_memory", name, exc)
        return MemoryBackend.IN_MEMORY, None

# ─────────────────────────────── Singleton ───────────────────────────────
class Memory:
    """Facade wrapping the active backend."""
    backend: MemoryBackend
    _instance: Optional["Memory"] = None
    _store: Dict[str, List[Dict[str, Any]]] = {}
    _impl: Optional[Any] = None

    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            resolved, impl = create_memory(backend)
            cls._instance.backend = resolved
            cls._instance._impl   = impl
        return cls._instance

    # ─────────────────────────────── load ───────────────────────────────
    def load(self, session_id: str = "default") -> List[Dict[str, Any]]:
        if self.backend == MemoryBackend.NONE:
            return []
        if self.backend == MemoryBackend.IN_MEMORY:
            return self._store.get(session_id, [])
        return self._impl.get_recent(cid=session_id)          # type: ignore

    # ─────────────────────────────── save ───────────────────────────────
    def save(self, msg: Dict[str, Any], *, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.NONE:
            return
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.setdefault(session_id, []).append(msg)
            return
        self._impl.add_turn(msg["role"], msg["content"], cid=session_id)  # type: ignore

    # ─────────────────────────────── clear ──────────────────────────────
    def clear(self, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.pop(session_id, None)
        elif self.backend != MemoryBackend.NONE:
            self._impl.flush(cid=session_id)                  # type: ignore

# ──────────────────────────── bootstrap singleton ────────────────────────────
from config.settings_loader import load_settings

_settings       = load_settings()
DEFAULT_BACKEND = _settings.get("memory", {}).get("backend", "none")

memory: Memory = Memory(backend=DEFAULT_BACKEND)
