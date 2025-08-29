import sys
from pathlib import Path

from memory.backends.sqlite_memory_backend import SQLiteMemoryBackend

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# ─────────────────────────────────────────────────────── Constants ──
EXPECTED_TURNS = 10

# ─────────────────────────────────────────────────────── Main ──────
mem = SQLiteMemoryBackend(db_path=":memory:", persist=False)

for i in range(EXPECTED_TURNS):
    mem.add_turn("assistant", f"reply {i}")

assert len(mem.get_recent(limit=10)) == EXPECTED_TURNS
print("✅ Created in-memory data successfully")
