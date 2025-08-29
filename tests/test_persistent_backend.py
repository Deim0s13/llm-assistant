import memory.backends.redis_memory_backend as rb
import memory.backends.sqlite_memory_backend as sb
from utils.memory import Memory, MemoryBackend

"""
Tests for MEMORY_BACKEND="persistent" resolution chain:
Redis  → SQLite → In-memory
"""

# ───────────────────────── helpers ─────────────────────────


class FakeImpl:
    """Mimics a backend impl with configurable fallback flag."""

    def __init__(self, use_fallback: bool):
        self._using_fallback = use_fallback


def new_memory(monkeypatch, *, redis_ok=True, sqlite_ok=True):
    """
    Reset singleton, monkey-patch backends, then return Memory instance
    with backend="persistent".
    """
    # patch Redis backend
    monkeypatch.setattr(
        rb,
        "RedisMemoryBackend",
        lambda *a, **k: FakeImpl(use_fallback=not redis_ok),
    )

    # patch SQLite backend
    monkeypatch.setattr(
        sb,
        "SQLiteMemoryBackend",
        lambda *a, **k: FakeImpl(use_fallback=not sqlite_ok),
    )

    # reset singleton before every scenario
    Memory._instance = None
    return Memory(backend="persistent")


# ───────────────────────── tests ─────────────────────────


def test_persistent_prefers_redis(monkeypatch):
    mem = new_memory(monkeypatch, redis_ok=True, sqlite_ok=True)
    assert mem.backend == MemoryBackend.REDIS


def test_persistent_falls_to_sqlite(monkeypatch):
    mem = new_memory(monkeypatch, redis_ok=False, sqlite_ok=True)
    assert mem.backend == MemoryBackend.SQLITE


def test_persistent_falls_to_in_memory(monkeypatch):
    mem = new_memory(monkeypatch, redis_ok=False, sqlite_ok=False)
    assert mem.backend == MemoryBackend.IN_MEMORY
