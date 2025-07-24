#!/usr/bin/env python
"""
migrate_memory.py  –  one-shot export of an in-memory session → SQLite file

Usage
-----
$ python migrate_memory.py
$ python migrate_memory.py --session mychat
$ python migrate_memory.py --db-path /tmp/chat.sqlite
"""

from __future__ import annotations
import argparse, pathlib, logging, sys

# ── project imports ────────────────────────────────────────────────────────
sys.path.append(".")                            # ensure repo root on PYTHONPATH
from utils.memory import Memory, MemoryBackend          # type: ignore
from memory.backends.sqlite_memory_backend import SQLiteMemoryBackend

# ── cli flags ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Export in-memory chat turns to SQLite")
parser.add_argument("--session", default="default",
                    help="Session / conversation id (default: %(default)s)")
parser.add_argument("--db-path", default="data/memory.sqlite",
                    help="Target SQLite file (default: %(default)s)")
args = parser.parse_args()

# ── fetch turns from in-memory store ───────────────────────────────────────
mem_src = Memory(backend=MemoryBackend.IN_MEMORY)
turns   = mem_src.load(args.session)
if not turns:
    print(f"Nothing to migrate: session “{args.session}” is empty.")
    sys.exit(0)

# ── write to SQLite (auto-creates file + table) ────────────────────────────
db_path = pathlib.Path(args.db_path).expanduser()
db_path.parent.mkdir(parents=True, exist_ok=True)

mem_dst = SQLiteMemoryBackend(db_path=db_path)
mem_dst.flush(cid=args.session)                 # idempotent
for t in reversed(turns):
    mem_dst.add_turn(t["role"], t["content"], cid=args.session)

print(f"Migrated {len(turns)} turns  →  {db_path}  (session “{args.session}”).")