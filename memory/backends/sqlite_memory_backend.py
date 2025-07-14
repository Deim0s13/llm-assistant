# ════════════════════════════════════════════════════════════════════
#  sqlite_memory_backend.py – SQLite-powered Memory backend
# ════════════════════════════════════════════════════════════════════

# ────────────────────────────── Imports ─────────────────────────────
from __future__ import annotations

import json, logging, os, time, sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, cast

from memory.backends.redis_memory_backend import BaseMemoryBackend, InMemoryBackend

# ────────────────────────────── Logging ─────────────────────────────
LOGGER = logging.getLogger(__name__)

# ─────────────────────────────── Class ──────────────────────────────
class SQLiteMemoryBackend(BaseMemoryBackend):
    """
    File-based chat-turn store. Falls back to RAM if the DB path is unwritable.
    """

    _DDL = """
    CREATE TABLE IF NOT EXISTS turns (
        session  TEXT    NOT NULL,
        ts       INTEGER NOT NULL,
        role     TEXT    NOT NULL,
        content  TEXT    NOT NULL,
        PRIMARY KEY (session, ts)
    );
    """

    # ────────────────────────── ctor / connect ─────────────────────────
    def __init__(
        self,
        *,
        db_path: str | Path = "data/memory.sqlite",
        max_rows_per_session: int = 10_000,
        fallback: Optional[BaseMemoryBackend] = None,
    ) -> None:

        self._db_path  = Path(db_path)
        self._max      = max_rows_per_session
        self._fallback = fallback or InMemoryBackend()

        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL;")
            self._conn.execute(self._DDL)
            self._using_fallback = False
            LOGGER.debug("[SQLite] Connected → %s", self._db_path)
        except Exception as exc:
            LOGGER.warning("SQLite unavailable (%s) – falling back to RAM", exc)
            self._conn, self._using_fallback = None, True

    # ─────────────────────────── add_turn ───────────────────────────────
    def add_turn(self, role: str, content: str, *, cid: str = "default") -> None:
        """
        Persist a single chat turn.

        ┌──────────── Pipeline ────────────┐
        │ 1  INSERT row (session, ts…)   │
        │ 2  TRIM: keep newest N rows    │
        │ 3  COMMIT (implicit via `with`)│
        └──────────────────────────────────┘

        Fallback → delegate to RAM store on any DB error.
        """
        if self._using_fallback:
            return self._fallback.add_turn(role, content, cid=cid)

        ts_now = time.time_ns()                           # monotonic timestamp – sort DESC

        try:
            # BEGIN IMMEDIATE; auto-commits (or rolls back) on exit
            with self._conn:                              # type: ignore[attr-defined]
                # 1  insert row
                self._conn.execute(
                    "INSERT INTO turns (session, ts, role, content) VALUES (?, ?, ?, ?)",
                    (cid, ts_now, role, json.dumps(content)),
                )

                # 2  trim oldest beyond max_rows_per_session
                self._conn.execute(
                    """
                    DELETE FROM turns
                    WHERE session = ?
                      AND ts NOT IN (
                          SELECT ts FROM turns
                          WHERE session = ?
                          ORDER BY ts DESC
                          LIMIT ?
                      )
                    """,
                    (cid, cid, self._max),
                )

        except Exception as exc:
            LOGGER.error("SQLite add_turn failed (%s) – switching to fallback", exc)
            self._using_fallback = True
            self._fallback.add_turn(role, content, cid=cid)

    # ─────────────────────────── get_recent ────────────────────────────
    def get_recent(
        self, *, limit: int = 50, cid: str = "default"
    ) -> List[Dict[str, str]]:
        """
        Return the most-recent `limit` turns (newest-first).
        Falls back to RAM store on DB error.
        """
        if self._using_fallback:
            return self._fallback.get_recent(limit=limit, cid=cid)

        try:
            cur = self._conn.execute(  # type: ignore[attr-defined]
                """
                SELECT role, content FROM turns
                WHERE session = ?
                ORDER BY ts DESC
                LIMIT ?
                """,
                (cid, limit),
            )
            rows = cur.fetchall()
            # convert JSON string back to plain str
            return [{"role": r, "content": json.loads(c)} for r, c in rows]
        except Exception as exc:
            LOGGER.error("SQLite get_recent failed (%s) – switching to fallback", exc)
            self._using_fallback = True
            return self._fallback.get_recent(limit=limit, cid=cid)

    # ───────────────────────────── flush ───────────────────────────────
    def flush(self, *, cid: str = "default") -> None:
        """
        Delete all stored turns for a conversation id.
        """
        if self._using_fallback:
            return self._fallback.flush(cid=cid)

        try:
            with self._conn:  # type: ignore[attr-defined]
                self._conn.execute("DELETE FROM turns WHERE session = ?", (cid,))
        except Exception as exc:
            LOGGER.error("SQLite flush failed (%s) – switching to fallback", exc)
            self._using_fallback = True
            self._fallback.flush(cid=cid)
