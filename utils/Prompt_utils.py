# ════════════════════════════════════════════════════════════════════
#  utils/prompt_utils.py – helper utilities for prompt detection
# ════════════════════════════════════════════════════════════════════
"""
Utilities that support prompt selection, alias matching, and related
token-level helpers.

Currently only `alias_in_message()` is needed, but we keep this as a
separate module so future prompt-utility functions stay in one place.
"""

# ───────────────────────────────────────────────────────── Imports ──


# ──────────────────────────────────── Public helpers ──
def alias_in_message(alias: str, message_tokens: list[str]) -> bool:
    """
    Return **True** if *all* tokens of `alias` appear *in order* inside
    `message_tokens`.

    Parameters
    ----------
    alias : str
        Multi-word alias string (e.g. "explain like i'm five").
    message_tokens : List[str]
        Lower-case, whitespace-split tokens of the user message.

    Notes
    -----
    * Matching is **in-order** but not necessarily contiguous.
    * Case-insensitive – `alias` should already be lower-cased by caller.
    """
    alias_tokens = alias.lower().split()
    idx = 0  # pointer into alias_tokens

    for tok in message_tokens:
        if tok == alias_tokens[idx]:
            idx += 1
            if idx == len(alias_tokens):  # found all alias tokens
                return True
    return False
