# ════════════════════════════════════════════════════════════════════
#  utils/memory.py – lightweight conversation memory façade
# ════════════════════════════════════════════════════════════════════
"""
Simple save/load layer for previous chat turns.

Back-ends
---------
• **IN_MEMORY** (default) – Python dict; zero external deps
• **NONE**           – disable memory
• Future: Redis, SQLite, vector DB …

Public API
----------
>>> from utils.memory import memory
>>> memory.save({"role": "user", "content": "Hi"})
>>> memory.load()[-1]
{'role': 'user', 'content': 'Hi'}
"""

from __future__ import annotations

import logging
from enum   import Enum
from typing import Any, Dict, List, Optional, cast

__all__ = ["MemoryBackend", "Memory", "memory"]

#  ─────────────────────────────── Back-end enum ───────────────────────────────

class MemoryBackend(str, Enum):
    NONE       = "none"
    IN_MEMORY  = "in_memory"
    REDIS      = "redis"
    SQLITE     = "sqlite"

#  ─────────────────────────────── Singleton class ───────────────────────────────

class Memory:
    """Façade implementing load / save / clear for the active back-end."""

    backend: MemoryBackend
    _instance: Optional["Memory"] = None
    _store: Dict[str, List[Dict[str, Any]]] = {}  # session → list[turn]
    _impl: Optional[Any] = None                     # backend implementation

    # ───────────────────────── helper for 'persistent' ─────────────────────────
    @staticmethod
    def _resolve_persistent() -> tuple["MemoryBackend", Optional[Any]]:
        """
        Return (resolved_backend, impl_object|None).
        Chain: Redis → SQLite → In-memory.
        """
        # 1. Try Redis
        try:
            from memory.backends.redis_memory_backend import RedisMemoryBackend
            impl = RedisMemoryBackend()
            if not impl._using_fallback:                       # connected
                return MemoryBackend.REDIS, impl
        except Exception:
            pass

        # 2. Try SQLite
        try:
            from memory.backends.sqlite_memory_backend import SQLiteMemoryBackend
            impl = SQLiteMemoryBackend()
            if not impl._using_fallback:
                return MemoryBackend.SQLITE, impl
        except Exception:
            pass

        # 3. Fallback
        return MemoryBackend.IN_MEMORY, None

    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            if backend == "persistent":
                    resolved, impl = cls._instance._resolve_persistent()
                    cls._instance.backend = resolved
                    cls._instance._impl  = impl
                    logging.info("[Memory] persistent → %s", resolved.value)

            else:
                cls._instance.backend = MemoryBackend(backend)
                # … existing REDIS / SQLITE / else wiring …

            # ───────────── backend implementation object ──────────────

            if cls._instance.backend == MemoryBackend.REDIS:
                from memory.backends.redis_memory_backend import RedisMemoryBackend
                cls._instance._impl = RedisMemoryBackend()        # type: ignore

            elif cls._instance.backend == MemoryBackend.SQLITE:
                from memory.backends.sqlite_memory_backend import SQLiteMemoryBackend
                cls._instance._impl = SQLiteMemoryBackend()       # type: ignore

            else:  # IN_MEMORY or NONE
                cls._instance._impl = None                        # fallback for other modes

        return cls._instance

# ───────────────────────────────────  API ───────────────────────────────────

    # ─────────────────────────────── load ───────────────────────────────

    def load(self, session_id: str = "default") -> List[Dict[str, Any]]:
        if self.backend == MemoryBackend.NONE:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("[Memory] load skipped – backend NONE")
            return []

        if self.backend == MemoryBackend.IN_MEMORY:
            hist = self._store.get(session_id, [])
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug(
                    "[Memory] load → %d turns (session=%s)", len(hist), session_id,
                )
            return hist

        elif self.backend == MemoryBackend.REDIS:
            return self._impl.get_recent(cid=session_id)            # type: ignore
        elif self.backend == MemoryBackend.SQLITE:
            return self._impl.get_recent(cid=session_id)

        # ⇢ future back-ends
        raise NotImplementedError(f"backend '{self.backend}' not implemented")


    # ─────────────────────────────── save ───────────────────────────────

    def save(self, message: Dict[str, Any], *, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.NONE:
            logging.debug("[Memory] save skipped – backend NONE")
            return

        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.setdefault(session_id, []).append(message)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug(
                    "[Memory] save (%s) role=%s  preview=%s",
                    session_id,
                    message.get("role"),
                    message.get("content", "")[:40],
                )
            return

        elif self.backend == MemoryBackend.REDIS:
            self._impl.add_turn(message["role"], message["content"], cid=session_id)  # type: ignore
        elif self.backend == MemoryBackend.SQLITE:
            self._impl.add_turn(message["role"], message["content"], cid=session_id)
        else:
            raise NotImplementedError(f"backend '{self.backend}' not implemented")


    # ─────────────────────────────── clear ──────────────────────────────

    def clear(self, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.pop(session_id, None)

        elif self.backend == MemoryBackend.REDIS:
            self._impl.flush(cid=session_id)                        # type: ignore
        elif self.backend == MemoryBackend.SQLITE:
            self._impl.flush(cid=session_id)

# ─────────────────────────────────── Singleton initialisation ───────────────────────────────────

from config.settings_loader import load_settings  # late import to avoid cycle

_settings           = load_settings()
DEFAULT_BACKEND     = _settings.get("memory", {}).get("backend", "none")

memory: Memory = Memory(backend=DEFAULT_BACKEND)
