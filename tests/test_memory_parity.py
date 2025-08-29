# ─────────────────────────────────────────────────────── Imports ──
from memory.backends.sqlite_memory_backend import SQLiteMemoryBackend

# ─────────────────────────────────────────────────────── Constants ──
EXPECTED_TURNS = 2

# ─────────────────────────────────────────────────────── Test ──────
mem = SQLiteMemoryBackend(db_path=":memory:", persist=False)

mem.add_turn("user", "ping")
mem.add_turn("assistant", "pong")

turns = mem.get_recent(limit=10)
assert turns[0]["content"] == "pong"
assert len(turns) == EXPECTED_TURNS
print("✅ Memory parity test passed")
