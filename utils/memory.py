"""
memory.py – lightweight conversation-memory interface
-----------------------------------------------------

Purpose
~~~~~~~
Provide a simple, pluggable layer for **saving** and **retrieving** past
(user, assistant) message pairs.  The default backend is an *in-process*
dictionary so no external services are required.

Roadmap placeholders (⇢) show where future persistent back-ends (Redis,
SQLite, Vector DB, etc.) can be wired in without changing caller code.

Usage
~~~~~
>>> from utils.memory import Memory, MemoryBackend
>>> mem = Memory(backend="in_memory")   # default
>>> mem.save({"role": "user", "content": "Hi"})
>>> mem.load()[-1]
{'role': 'user', 'content': 'Hi'}
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
import logging

__all__ = ["Memory", "MemoryBackend"]


# --------------------------------------------------------------------------- #
#  ENUM – Available back-end types (extend later)                             #
# --------------------------------------------------------------------------- #
class MemoryBackend(str, Enum):
    NONE = "none"           # disables memory
    IN_MEMORY = "in_memory" # Python dict(list) only
    # ⇢ add "redis", "sqlite", "vector" in future versions


# --------------------------------------------------------------------------- #
#  MEMORY SINGLETON                                                           #
# --------------------------------------------------------------------------- #
class Memory:
    """
    A minimal singleton façade around the chosen back-end.

    For v0.4.3 we only support the in-process store; other back-ends raise
    NotImplementedError to remind devs where to plug in later.
    """

    backend: MemoryBackend

    _instance: Optional["Memory"] = None  # singleton ref

    # in-memory store: {session_id: [msg, msg, …]}
    _store: Dict[str, List[Dict[str, Any]]] = {}

    def __new__(cls, *, backend: str | MemoryBackend = MemoryBackend.IN_MEMORY):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.backend = MemoryBackend(backend)
            logging.debug("[Memory] Initialised backend: %s", cls._instance.backend)
        return cls._instance

    # --------------------------------------------------------------------- #
    #  PUBLIC API                                                           #
    # --------------------------------------------------------------------- #
    def load(self, session_id: str = "default") -> List[Dict[str, Any]]:
        """
        Return the history list for a session.
        """
        if self.backend == MemoryBackend.NONE:
            return []

        if self.backend == MemoryBackend.IN_MEMORY:
            return self._store.get(session_id, [])

        # ⇢ implement persistent back-ends here
        raise NotImplementedError(f"Memory backend '{self.backend}' not implemented.")

    def save(self, message: Dict[str, Any], *, session_id: str = "default") -> None:
        """
        Append a single message (`{'role': ..., 'content': ...}`) to session history.
        """
        if self.backend == MemoryBackend.NONE:
            return  # no-op

        if self.backend == MemoryBackend.IN_MEMORY:
            self._store.setdefault(session_id, []).append(message)
            return

        # ⇢ implement persistent back-ends here
        raise NotImplementedError(f"Memory backend '{self.backend}' not implemented.")

    def clear(self, session_id: str = "default") -> None:
        """
        Remove all stored messages for a session.
        """
        if self.backend == MemoryBackend.IN_MEMORY and session_id in self._store:
            del self._store[session_id]


# --------------------------------------------------------------------------- #
#  CONVENIENCE: module-level singleton accessor                              #
# --------------------------------------------------------------------------- #
memory: Memory = Memory()  # default in-memory instance
