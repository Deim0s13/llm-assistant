"""
experiments/memory_test_utils.py
Helpers used by the memory-toggle experiment scripts.
"""

from utils.memory           import memory, MemoryBackend
from config.settings_loader import load_settings

# ------------------------------------------------------------------ #
# toggle helper                                                      #
# ------------------------------------------------------------------ #
def set_memory_enabled(enabled: bool) -> None:
    """
    Enable / disable conversation memory *at runtime* for tests.

    • Updates the in-process settings dict.
    • Swaps the singleton's backend (IN_MEMORY ⟷ NONE).
    • Clears any stored turns so tests start clean.
    """
    settings = load_settings()
    settings.setdefault("memory", {})
    settings["memory"]["enabled"] = enabled

    # swap backend
    memory.backend = (
        MemoryBackend.IN_MEMORY if enabled else MemoryBackend.NONE
    )

    # start every test from a clean slate
    memory.clear()

    state = "ON" if enabled else "OFF"
    print(f"[Test Helper] Memory toggle → {state}")
