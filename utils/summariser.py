# ════════════════════════════════════════════════════════════════════
#  utils/summariser.py – placeholder context-summarisation helper
# ════════════════════════════════════════════════════════════════════
"""
summariser.py
~~~~~~~~~~~~~
A *stub* entry point for future summarisation.
For now it simply returns a constant placeholder string so callers can
integrate it without worrying about real summarisation logic.

Road-map
--------
• v0.5.x  : naive extractive summary (e.g. last N sentences)
• v0.6.x+ : LLM-powered compression / vector-based summary
"""

from __future__ import annotations
from typing import List, Dict

__all__ = ["summarise_context"]


def summarise_context(
    history: List[Dict[str, str]],
    *,
    style: str = "brief",
    max_chars: int = 512,
) -> str:
    """
    Return a **placeholder** summary of the supplied history.

    Parameters
    ----------
    history : list[dict]
        Chat turns `{"role": "user" | "assistant", "content": str}`
    style : str
        Future knob for 'brief', 'detailed', etc.  Ignored for now.
    max_chars : int
        Target upper bound for summary length once implemented.

    Returns
    -------
    str
        Stub text to prove the call path works.
    """
    del style, max_chars  # unused until real impl

    if not history:
        return "• (no prior context to summarise)\n"

    return "• Summary of prior discussion (placeholder – real summarisation TBD)\n"
