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
    # TODO: SQLITE = "sqlite"

#  ─────────────────────────────── Singleton class ───────────────────────────────
class Memory:
    """Façade implementing load / save / clear for the active back-end."""

    backend: MemoryBackend
    _instance: Optional["Memory"] = None
    _store: Dict[str, List[Dict[str, Any]]] = {}  # session → list[turn]
    _impl: Optional[Any] = None                     # backend implementation

    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.backend = MemoryBackend(backend)
            logging.debug("[Memory] backend=%s", cls._instance.backend.value)

            # ───────────── backend implementation object ──────────────
            if cls._instance.backend == MemoryBackend.REDIS:
                from memory.backends.redis_memory_backend import RedisMemoryBackend
                cls._instance._impl = RedisMemoryBackend()            # type: ignore
            else:
                cls._instance._impl = None                            # other modes

        return cls._instance                       # fallback for other modes

    # ───────────────────────────────────  API ───────────────────────────────────
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

        # ⇢ future back-ends
        raise NotImplementedError(f"backend '{self.backend}' not implemented")


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
            return

        # ⇢ future back-ends
        raise NotImplementedError(f"backend '{self.backend}' not implemented")


    def clear(self, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.pop(session_id, None)

        elif self.backend == MemoryBackend.REDIS:
            self._impl.flush(cid=session_id)                        # type: ignore

# ─────────────────────────────────── Singleton initialisation ───────────────────────────────────
from config.settings_loader import load_settings  # late import to avoid cycle

_settings           = load_settings()
DEFAULT_BACKEND     = _settings.get("memory", {}).get("backend", "none")

memory: Memory = Memory(backend=DEFAULT_BACKEND)
