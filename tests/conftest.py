# Ensure project root is importable for tests
import sys
from pathlib import Path

import contextlib
import logging
import sqlite3
from collections.abc import Generator
from typing import Any
from utils.memory import Memory, MemoryBackend

import pytest
import redis

ROOT = str(Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    import fakeredis
except ImportError:  # requirements-dev.txt already lists it, but guard anyway
    fakeredis = None  # type: ignore[assignment]

logging.basicConfig(level=logging.DEBUG, format="[Memory-tests] %(message)s")

# ── helper: spin up fake Redis (no external server) ─────────────────────────


@contextlib.contextmanager
def fake_redis_server() -> Generator[Any, None, None]:
    if not fakeredis:  # should never happen in CI
        pytest.skip("fakeredis missing")
    server = fakeredis.FakeServer()
    yield fakeredis.FakeRedis(server=server)


# ── parametrised fixture ────────────────────────────────────────────────────


@pytest.fixture(params=["in_memory", "redis", "sqlite"])
def mem(
    request: pytest.FixtureRequest, tmp_path: Any, monkeypatch: Any
) -> Generator[Memory, None, None]:
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
            def fake_redis_factory(*_args: Any, **_kwargs: Any) -> Any:
                return r

            monkeypatch.setattr(redis, "from_url", fake_redis_factory)
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
        with sqlite3.connect(str(db_file)) as con:
            assert con.execute("SELECT COUNT(*) FROM turns").fetchone()[0] == 0
        return
