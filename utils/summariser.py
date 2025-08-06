# ════════════════════════════════════════════════════════════════════
#  utils/summariser.py – context-summarisation helper (heuristic)
# ════════════════════════════════════════════════════════════════════
"""
summariser.py
~~~~~~~~~~~~~
Lightweight, deterministic context summariser.

- v0.4.5: Implements first-pass heuristic summarisation for long chat history.
- Future: Add LLM-powered compression, topic-aware summarisation, config integration.

Features:
---------
• Bullet-point summary of most recent user turns (up to 3 bullets).
• Consistent placeholder and "no user" messages for edge-cases.
• Easy to extend for future strategies.
"""

from __future__ import annotations
from typing import List, Dict

__all__ = ["summarise_context"]

# ─────────────────────────────── Summariser ──────────────────────────────


def summarise_context(
    history: List[Dict[str, str]],
    *,
    style: str = "brief",
    max_chars: int = 512,
) -> str:
    """
    Returns a simple, deterministic summary (≤ 3 bullet points) of recent user turns.
    If not enough context, returns a placeholder message.

    Parameters
    ----------
    history : list[dict]
        Chat turns, e.g. [{"role": "user"|"assistant", "content": str}]
    style : str
        Reserved for future use.
    max_chars : int
        Reserved for future use.

    Returns
    -------
    str : summary text
    """

    # --- Configurable knobs (make config-driven later) ---
    PLACEHOLDER = "• (no prior context to summarise)\n"
    NO_USER_MSG = "• (no user turns to summarise)\n"
    MIN_TURNS = 8
    MAX_BULLETS = 3
    BULLET_CHAR_LIMIT = 120

    # ────────────────────────────── Edge Cases ──────────────────────────────
    if not history:
        return PLACEHOLDER

    user_turns = [turn["content"] for turn in history if turn.get("role") == "user"]
    if not user_turns:
        return NO_USER_MSG

    if len(history) < MIN_TURNS:
        return PLACEHOLDER

    # ────────────────────────── Heuristic Summary ───────────────────────────
    last_n = user_turns[-MIN_TURNS:]
    bullets = []
    for line in last_n[-MAX_BULLETS:]:
        bullet = line.strip().replace("\n", " ")
        if len(bullet) > BULLET_CHAR_LIMIT:
            bullet = bullet[: BULLET_CHAR_LIMIT - 1].rstrip() + "…"
        bullets.append(f"• {bullet}")

    return "\n".join(bullets) or PLACEHOLDER
