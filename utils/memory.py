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
from typing import List, Dict, Any, Optional

__all__ = ["MemoryBackend", "Memory", "memory"]

# ─────────────────────────────────────────────── Back-end enum ──
class MemoryBackend(str, Enum):
    NONE       = "none"
    IN_MEMORY  = "in_memory"
    # TODO: REDIS = "redis", SQLITE = "sqlite"

# ───────────────────────────────────────────── Singleton class ──
class Memory:
    """Façade implementing load / save / clear for the active back-end."""

    backend: MemoryBackend
    _instance: Optional["Memory"] = None
    _store: Dict[str, List[Dict[str, Any]]] = {}  # session → list[turn]

    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.backend = MemoryBackend(backend)
            logging.debug("[Memory] backend=%s", cls._instance.backend.value)
        return cls._instance

    # ------------------------------------------------ API -------
    def load(self, session_id: str = "default") -> List[Dict[str, Any]]:
        if self.backend == MemoryBackend.NONE:
            return []
        if self.backend == MemoryBackend.IN_MEMORY:
            return self._store.get(session_id, [])
        raise NotImplementedError(self.backend.value)

    def save(self, msg: Dict[str, Any], *, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.NONE:
            return
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.setdefault(session_id, []).append(msg)
            return
        raise NotImplementedError(self.backend.value)

    def clear(self, session_id: str = "default") -> None:
        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.pop(session_id, None)

# ─────────────────────────────────── Singleton initialisation ──
from config.settings_loader import load_settings  # late import to avoid cycle

_settings           = load_settings()
DEFAULT_BACKEND     = _settings.get("memory", {}).get("backend", "none")

memory: Memory = Memory(backend=DEFAULT_BACKEND)
