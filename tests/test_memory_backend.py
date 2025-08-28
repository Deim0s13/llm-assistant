# tests/test_memory_backends.py
import importlib
import pytest, fakeredis

from utils.memory import Memory, MemoryBackend

# ───────────────────────── helpers ─────────────────────────

def _reset_singleton():
    """Clear the global singleton so each test gets a fresh instance."""
    Memory._instance = None            # type: ignore[attr-defined]

# ───────────────────────── fixtures ─────────────────────────

@pytest.fixture(params=["in_memory", "redis"])
def mem(request, monkeypatch):
    backend = request.param

    if backend == "redis":
        # patch BEFORE backend import so RedisMemoryBackend uses FakeRedis
        import memory.backends.redis_memory_backend as rb
        monkeypatch.setattr(rb, "redis", fakeredis.FakeRedis, raising=True)
        importlib.reload(rb)           # re-evaluate with fake client

    _reset_singleton()
    yield Memory(backend=backend)

    if backend == "redis":
        # restore for any subsequent tests / IDE analysis
        import memory.backends.redis_memory_backend as rb
        import redis as redis_real
        monkeypatch.setattr(rb, "redis", redis_real, raising=True)
        importlib.reload(rb)

# ───────────────────────── Tests ─────────────────────────

def test_round_trip(mem):
    mem.clear()
    mem.save({"role": "user", "content": "hello"})
    assert mem.load()[-1]["content"] == "hello"

def test_clear(mem):
    mem.save({"role": "assistant", "content": "bye"})
    mem.clear()
    assert mem.load() == []
