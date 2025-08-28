import os, contextlib, sqlite3, tempfile, pathlib, logging, pytest
from utils.memory import Memory, MemoryBackend

logging.basicConfig(level=logging.DEBUG, format="[Memory-tests] %(message)s")

# ── helper: spin up fake Redis (no external server) ─────────────────────────
try:
    import fakeredis
except ImportError:  # requirements-dev.txt already lists it, but guard anyway
    fakeredis = None

@contextlib.contextmanager
def fake_redis_server():
    if not fakeredis:                       # should never happen in CI
        pytest.skip("fakeredis missing")
    server = fakeredis.FakeServer()
    yield fakeredis.FakeRedis(server=server)

# ── parametrised fixture ────────────────────────────────────────────────────
@pytest.fixture(params=["in_memory", "redis", "sqlite"])
def mem(request, tmp_path, monkeypatch):
    backend = request.param
    logging.debug(f"backend = {backend}")

    # --- in_memory ---------------------------------------------------------
    if backend == "in_memory":
        m = Memory(backend=MemoryBackend.IN_MEMORY)
        m.clear()
        yield m
        return

    # --- redis -------------------------------------------------------------
    if backend == "redis":
        with fake_redis_server() as r:
            monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
            # monkey-patch redis.Redis to return our fake connection
            import redis
            monkeypatch.setattr(redis, "from_url", lambda *_, **__: r)
            m = Memory(backend=MemoryBackend.REDIS)
            m.clear()
            yield m
        return

    # --- sqlite ------------------------------------------------------------
    if backend == "sqlite":
        db_file = tmp_path / "test.sqlite"
        monkeypatch.setenv("MEMORY_DB_PATH", str(db_file))
        m = Memory(backend=MemoryBackend.SQLITE)
        m.clear()
        yield m
        # optional: sanity check row-count vs. file on disk
        with sqlite3.connect(db_file) as con:
            assert con.execute("SELECT COUNT(*) FROM turns").fetchone()[0] == 0
        return