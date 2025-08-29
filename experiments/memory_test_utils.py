#!/usr/bin/env python
"""
experiments/memory_test_utils.py
--------------------------------

Tiny helper used by experiment & unit-test scripts to flip memory
behaviour at runtime without restarting the app.

Usage
-----
>>> from experiments.memory_test_utils import set_memory_enabled
>>> set_memory_enabled(True)   # enable + fresh store
>>> set_memory_enabled(False)  # disable completely
"""

from main import SETTINGS
from utils.memory import MemoryBackend, memory


def set_memory_enabled(flag: bool, backend: str = "in_memory") -> dict:
    """
    Toggle conversation-memory ON / OFF for the **current** Python process.

    • Updates the shared SETTINGS dict
    • Switches the live singleton backend
    • Clears stored turns so tests start clean

    Returns the mutated SETTINGS for convenience.
    """
    SETTINGS.setdefault("memory", {})
    SETTINGS["memory"]["enabled"] = flag
    SETTINGS["memory"]["backend"] = backend if flag else "none"

    # swap the active backend on the singleton in real time
    memory.backend = MemoryBackend.IN_MEMORY if flag else MemoryBackend.NONE

    # always begin with an empty store so tests are independent
    memory.clear()

    state = "ON" if flag else "OFF"
    print(f"[Test Helper] Memory toggle → {state} (backend={memory.backend.value})")
    return SETTINGS
