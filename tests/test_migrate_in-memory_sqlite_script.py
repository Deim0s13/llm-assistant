# tests/test_migration_script.py
import sqlite3
import subprocess

from utils.memory import Memory, MemoryBackend

# ─────────────────────────────────────────────────────── Constants ──
EXPECTED_ROWS = 2


# ─────────────────────────────────────────────────────── Test ──────
def test_migration_default_session(tmp_path):
    # 1) populate RAM
    mem = Memory(backend=MemoryBackend.IN_MEMORY)
    mem.clear()
    mem.save({"role": "user", "content": "hi"})
    mem.save({"role": "assistant", "content": "yo"})

    # 2) run script with tmp db path
    db_path = tmp_path / "chat.sqlite"
    r = subprocess.run(
        ["python", "scripts/migrate_memory.py", "--db-path", str(db_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Migrated 2 turns" in r.stdout

    # 3) verify rows
    con = sqlite3.connect(db_path)
    cur = con.execute("SELECT role, content FROM turns").fetchall()
    assert len(cur) == EXPECTED_ROWS
    assert cur[0][1] == "hi"
