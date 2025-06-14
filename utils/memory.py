"""
memory.py – lightweight conversation-memory interface
-----------------------------------------------------

Purpose
~~~~~~~
Provide a simple, pluggable layer for **saving** and **retrieving** past
(user, assistant) message pairs.  The default backend is an *in-process*
dictionary so no external services are required.

Road-map placeholders (⇢) show where future persistent back-ends (Redis,
SQLite, Vector DB, etc.) can be wired in without changing caller code.

Usage
~~~~~
>>> from utils.memory import memory, MemoryBackend
>>> memory.save({"role": "user", "content": "Hi"})
>>> memory.load()[-1]
{'role': 'user', 'content': 'Hi'}
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import List, Dict, Any, Optional

__all__ = ["Memory", "MemoryBackend", "memory"]

# --------------------------------------------------------------------------- #
#  ENUM – Available back-end types                                            #
# --------------------------------------------------------------------------- #
class MemoryBackend(str, Enum):
    NONE = "none"           # disables memory
    IN_MEMORY = "in_memory" # Python dict-list only
    # ⇢ add "redis", "sqlite", "vector" in future versions


# --------------------------------------------------------------------------- #
#  MEMORY SINGLETON IMPLEMENTATION                                            #
# --------------------------------------------------------------------------- #
class Memory:
    """
    Minimal façade around the chosen back-end.

    • v0.4.3 ships with the in-process store only.
    • Other back-ends raise NotImplementedError until implemented.
    """

    backend: MemoryBackend
    _instance: Optional["Memory"] = None  # singleton ref

    # in-memory store: {session_id: [msg, msg, …]}
    _store: Dict[str, List[Dict[str, Any]]] = {}

    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.backend = MemoryBackend(backend)
            logging.debug("[Memory] Initialised backend: %s", cls._instance.backend.value)
        return cls._instance

    # --------------------------------------------------------------------- #
    #  PUBLIC API                                                           #
    # --------------------------------------------------------------------- #
    def load(self, session_id: str = "default") -> List[Dict[str, Any]]:
        """Return a list of messages for a session (empty if none)."""
        if self.backend == MemoryBackend.NONE:
            return []

        if self.backend == MemoryBackend.IN_MEMORY:
            return self._store.get(session_id, [])

        # ⇢ implement persistent back-ends here
        raise NotImplementedError(f"Memory backend '{self.backend}' not implemented.")

    def save(self, message: Dict[str, Any], *, session_id: str = "default") -> None:
        """Append a single message (`{'role': .., 'content': ..}`) to history."""
        if self.backend == MemoryBackend.NONE:
            return  # no-op

        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.setdefault(session_id, []).append(message)
            return

        # ⇢ implement persistent back-ends here
        raise NotImplementedError(f"Memory backend '{self.backend}' not implemented.")

    def clear(self, session_id: str = "default") -> None:
        """Remove all stored messages for a session."""
        if self.backend == MemoryBackend.IN_MEMORY and session_id in self._store:
            del self._store[session_id]


# --------------------------------------------------------------------------- #
#  Auto-initialise singleton using settings.json /.env                        #
# --------------------------------------------------------------------------- #
from config.settings_loader import load_settings  # noqa: E402  (late import)

_SETTINGS = load_settings()
_DEFAULT_BACKEND = _SETTINGS.get("memory", {}).get("backend", "none")

# public singleton instance
memory: Memory = Memory(backend=_DEFAULT_BACKEND)
