#!/usr/bin/env python
"""
migrate_memory.py – one-shot export of an *in-memory* session → SQLite file.

How it works
============
1.  The parent process (your REPL, a test, etc.) serialises the current
    `Memory._store` dict into the environment variable **LLM_MEM_STORE_JSON**.
    The helper code in *utils/memory.py* does this automatically whenever you
    call `Memory.save()` while using the **IN_MEMORY** backend.
2.  When you invoke this script (which runs in a new Python process), the
    import of `utils.memory` re-hydrates that JSON back into RAM, so a
    normal `.load()` call sees the same turns.
3.  We read those turns, write them into an SQLite file (creating the table
    on first-run) and report how many rows were migrated.

Typical usage
-------------
$ python scripts/migrate_memory.py                       # default session → data/memory.sqlite
$ python scripts/migrate_memory.py --session chat42      # pick a session id
$ python scripts/migrate_memory.py --db-path /tmp/chat.sqlite
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

# ── project imports ─────────────────────────────────────────────────────
sys.path.append(".")  # ensure repo root on PYTHONPATH

from utils.memory import Memory, MemoryBackend  # noqa: E402
from importlib import import_module

SQLiteMemoryBackend = import_module(
    "memory.backends.sqlite_memory_backend"
).SQLiteMemoryBackend

_ENV_KEY = "LLM_MEM_STORE_JSON"


def _fallback_turns_from_env(session_id: str) -> list[dict]:
    """If Memory.load() returns empty, try to read the JSON snapshot directly."""
    raw = os.getenv(_ENV_KEY)
    if not raw:
        return []
    try:
        store = json.loads(raw)
        # store is expected to be: {session_id: [ {role, content}, ... ], ...}
        turns = store.get(session_id, [])
        # Ensure structure is as expected
        if isinstance(turns, list) and all(isinstance(t, dict) for t in turns):
            return turns
    except Exception:
        pass
    return []


# ─────────────────────────────── main() ────────────────────────────────
def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        prog="migrate_memory.py",
        description="Export an in-memory chat session to an SQLite file",
    )
    ap.add_argument(
        "--session",
        default="default",
        help="Conversation id (default: %(default)s)",
    )
    ap.add_argument(
        "--db-path",
        default="data/memory.sqlite",
        help="Target SQLite file (default: %(default)s)",
    )
    args = ap.parse_args(argv)

    # 1) pull turns from the (rehydrated) in-memory backend
    turns = Memory(backend=MemoryBackend.IN_MEMORY).load(args.session)

    # Fallback: read directly from the env snapshot if needed
    if not turns:
        turns = _fallback_turns_from_env(args.session)

    if not turns:
        print(f"Nothing to migrate: session “{args.session}” is empty.")
        return

    # 2) dump them into SQLite ──────────────────────────────────────────
    db_path = pathlib.Path(args.db_path).expanduser()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Important: persist=True so we actually write to disk
    mem_dst = SQLiteMemoryBackend(db_path=db_path, persist=True)

    mem_dst.flush(cid=args.session)  # idempotent
    # `turns` are oldest-first already; keep that order when inserting
    for t in turns:
        mem_dst.add_turn(t["role"], t["content"], cid=args.session)

    print(f"Migrated {len(turns)} turns  →  {db_path}  (session “{args.session}”).")


if __name__ == "__main__":
    main()
