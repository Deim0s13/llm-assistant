# ════════════════════════════════════════════════════════════════════
#  redis_memory_backend.py – Redis-powered Memory backend
# ════════════════════════════════════════════════════════════════════

# ─────────────────────────────── Imports ───────────────────────────────
from __future__ import annotations

import json, logging, os
from typing import Dict, List, Optional, Tuple, Any, cast

try:
    import redis                      # network client
    _REDIS_AVAILABLE = True
except ModuleNotFoundError:           # dev boxes w/out redis-py
    _REDIS_AVAILABLE = False

# ─────────────────────────────── Logging ───────────────────────────────
LOGGER = logging.getLogger(__name__)

# ─────────────────────────────── Interface ─────────────────────────────
class BaseMemoryBackend:
    """Minimal contract every concrete backend must fulfil."""

    def add_turn(self, role: str, content: str, *, cid: str = "default") -> None:
        raise NotImplementedError

    def get_recent(
        self, *, limit: int = 50, cid: str = "default"
    ) -> List[Dict[str, str]]:
        raise NotImplementedError

    def flush(self, *, cid: str = "default") -> None:
        raise NotImplementedError

# ────────────────────────────── Fallback ───────────────────────────────
class InMemoryBackend(BaseMemoryBackend):
    """Volatile list-based store (same semantics as utils.memory.IN_MEMORY)."""

    def __init__(self) -> None:
        self._store: Dict[str, List[Tuple[str, str]]] = {}

    def add_turn(self, role: str, content: str, *, cid: str = "default") -> None:
        self._store.setdefault(cid, []).append((role, content))

    def get_recent(self, *, limit: int = 50, cid: str = "default") -> List[Dict[str, str]]:
        turns = self._store.get(cid, [])[-limit:][::-1]              # newest-first
        return [{"role": r, "content": c} for r, c in turns]

    def flush(self, *, cid: str = "default") -> None:
        self._store.pop(cid, None)

# ─────────────────────────────── Backend ───────────────────────────────

class RedisMemoryBackend(BaseMemoryBackend):
    """
    Persist chat turns in Redis and auto-fallback to RAM if Redis is missing or
    unreachable.  No add/get/flush logic yet – we’re wiring the connection flag.
    """

    _KEY_TMPL = "chat:{cid}:turns"          # will be namespaced later

    # ─────────────────────────── ctor / connect ──────────────────────────
    def __init__(
        self,
        *,
        redis_url : Optional[str] = None,
        host      : str           = "localhost",
        port      : int           = 6379,
        db        : int           = 0,
        password  : Optional[str] = None,
        key_prefix: str           = "chat:",
        max_turns : int           = 10_000,
        fallback  : Optional[BaseMemoryBackend] = None,
    ) -> None:

        self._key_prefix = key_prefix
        self._max_turns  = max_turns
        self._fallback   = fallback or InMemoryBackend()

        # 1 redis-py missing → immediate fallback
        if not _REDIS_AVAILABLE:
            LOGGER.warning("redis-py not installed – using in-memory backend.")
            self._client, self._using_fallback = None, True
            return

        # 2 build connection
        redis_url = redis_url or os.getenv("REDIS_URL")
        try:
            self._client = (
                redis.from_url(redis_url, decode_responses=True)
                if redis_url else
                redis.Redis(host=host, port=port, db=db,
                            password=password, decode_responses=True)
            )
            self._client.ping()                 # raises if server down
            self._using_fallback = False
            LOGGER.debug("[Redis] Connected ✔")
        except Exception as exc:
            LOGGER.warning("Redis unavailable (%s) – falling back to RAM", exc)
            self._client, self._using_fallback = None, True

    # ───────────────────────────── helpers ───────────────────────────────
    def _key(self, cid: str) -> str:
        """Return the Redis key for a conversation id (namespaced)."""
        return self._KEY_TMPL.format(cid=cid).replace("chat:", self._key_prefix)

    # ─────────────────────────── add_turn ───────────────────────────────
    def add_turn(self, role: str, content: str, *, cid: str = "default") -> None:
        """
        Persist a single chat turn.
        • If Redis is active → LPUSH + optional LTRIM.
        • If fallback → delegate to self._fallback.
        """
        if self._using_fallback:
            return self._fallback.add_turn(role, content, cid=cid)

        payload = json.dumps({"role": role, "content": content})
        key     = self._key(cid)
        try:
            # mypy: after the assert, _client is sync redis.Redis
            assert self._client is not None
            client = cast("redis.Redis", self._client)
            pipe = client.pipeline()
            (
                pipe
                .lpush(key, payload)
                .ltrim(key, 0, self._max_turns - 1)  # type: ignore[union-attr]
                .execute()
            )
        except Exception as exc:
            LOGGER.error("Redis add_turn failed (%s) – switching to fallback", exc)
            self._using_fallback = True
            self._fallback.add_turn(role, content, cid=cid)

    # ─────────────────────────── get_recent ─────────────────────────────
    def get_recent(
        self, *, limit: int = 50, cid: str = "default"
    ) -> List[Dict[str, str]]:
        """
        Return the most-recent `limit` turns (newest-first).
        Falls back to the RAM store on any Redis error.
        """
        if self._using_fallback:
            return self._fallback.get_recent(limit=limit, cid=cid)

        key = self._key(cid)
        try:
            assert self._client is not None
            client = cast("redis.Redis", self._client)
            raw = client.lrange(key, 0, limit - 1)
            return [json.loads(x) for x in cast(List[str], raw)]
        except Exception as exc:
            LOGGER.error("Redis get_recent failed (%s) – switching to fallback", exc)
            self._using_fallback = True
            return self._fallback.get_recent(limit=limit, cid=cid)

    # ───────────────────────────── flush ────────────────────────────────
    def flush(self, *, cid: str = "default") -> None:
        """
        Delete all stored turns for a conversation id.
        """
        if self._using_fallback:
            return self._fallback.flush(cid=cid)

        try:
            assert self._client is not None
            cast("redis.Redis", self._client).delete(self._key(cid))
        except Exception as exc:
            LOGGER.error("Redis flush failed (%s) – switching to fallback", exc)
            self._using_fallback = True
            self._fallback.flush(cid=cid)
