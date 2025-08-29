# ════════════════════════════════════════════════════════════════════
#  tests for SQLiteMemoryBackend
# ════════════════════════════════════════════════════════════════════
import stat

from memory.backends.redis_memory_backend import InMemoryBackend
from memory.backends.sqlite_memory_backend import SQLiteMemoryBackend

# ─────────────────────────────────────────────────────── Constants ──
EXPECTED_ROWS = 3


# ────────────────────────── helpers ──────────────────────────
def mk_sqlite(max_rows=10_000, *, path=":memory:", fallback=None):
    return SQLiteMemoryBackend(db_path=path, max_rows_per_session=max_rows, fallback=fallback)


# ────────────────────────── tests ────────────────────────────
def test_roundtrip_default():
    mem = mk_sqlite()
    mem.add_turn("user", "hi")
    mem.add_turn("assistant", "hello")
    turns = mem.get_recent(limit=10)
    assert turns[0]["content"] == "hello"
    assert turns[1]["content"] == "hi"


def test_trim_oldest():
    mem = mk_sqlite(max_rows=3)
    for i in range(6):
        mem.add_turn("user", f"msg{i}")
    rows = mem.get_recent(limit=10)
    assert len(rows) == EXPECTED_ROWS
    assert rows[0]["content"] == "msg5"
    assert rows[-1]["content"] == "msg3"  # oldest kept


def test_flush():
    mem = mk_sqlite()
    mem.add_turn("user", "bye")
    mem.flush()
    assert mem.get_recent(limit=5) == []


def test_fallback_on_unwritable(tmp_path):
    # simulate unwritable dir
    db_dir = tmp_path / "locked"
    db_dir.mkdir()
    db_dir.chmod(stat.S_IREAD)

    fallback = InMemoryBackend()
    mem = mk_sqlite(path=db_dir / "chat.sqlite", fallback=fallback)

    # should be in fallback mode
    assert mem._using_fallback is True
    mem.add_turn("user", "hello")
    assert fallback.get_recent(limit=1)[0]["content"] == "hello"
