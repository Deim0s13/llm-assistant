# ════════════════════════════════════════════════════════════════════
#  utils/safety_filters.py – profanity masking & safety gating
# ════════════════════════════════════════════════════════════════════
"""
Basic profanity detection / masking plus a pre-generation safety check.

The API intentionally stays light-weight so stricter classifiers (e.g.
OpenAI moderation, Perspective API, custom models) can later replace the
`evaluate_safety()` stub without changing the main chat flow.
"""

# ───────────────────────────────────────────────────────── Imports ──
from __future__ import annotations

import logging
import re
from typing import Tuple, Optional


# ──────────────────────────────────────── Static data ──
# A **very** small placeholder list; expand or externalise later.
PROFANITY_LIST = ["damn", "hell", "shit", "fuck"]

# Compiled regex so we do the heavy work once
_PROFANITY_REGEX = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in PROFANITY_LIST) + r")\b",
    flags=re.IGNORECASE,
)


# ─────────────────────────────────── Profanity masking ──
def apply_profanity_filter(text: str) -> str:
    """
    Replace each profane word in *text* with the equivalent number of
    asterisks, preserving capitalisation length only.

    Example
    -------
    >>> apply_profanity_filter("That is damn funny")
    'That is **** funny'
    """

    def _mask(match: re.Match) -> str:  # local helper
        return "*" * len(match.group())

    return _PROFANITY_REGEX.sub(_mask, text)


# ─────────────────────────────── Safety pre-generation ──
def evaluate_safety(
    message: str,
    settings: dict,
) -> Tuple[bool, Optional[str]]:
    """
    Light safety gate that checks *input* for profanity before we even
    call the model.

    Returns
    -------
    allowed : bool
        Whether the message is safe to continue processing.
    blocked_message : Optional[str]
        If blocked, a pre-formatted refusal text to send back.

    Behaviour by *sensitivity_level* in ``settings['safety']``:
    ┌────────────┬───────────────────────────────────────────────┐
    │ strict     │ Always block if profanity match.             │
    │ moderate   │ Allow but note that output should be filtered │
    │ relaxed    │ No blocking, no filtering.                    │
    └────────────┴───────────────────────────────────────────────┘
    """
    config = settings.get("safety", {})
    level = config.get("sensitivity_level", "moderate").lower()
    log_triggers = config.get("log_triggered_filters", False)
    refusal_text = config.get(
        "blocked_response_template",
        "I'm unable to respond to that request due to safety policies.",
    )

    # Detect profanity
    profane = bool(_PROFANITY_REGEX.search(message))
    if profane and log_triggers:
        logging.debug("[Safety] Profanity detected (level=%s): %s", level, message)

    if not profane:
        return True, None  # safe

    # Profanity found – act according to level
    if level == "strict":
        return False, refusal_text
    elif level == "moderate":
        # Allowed, but caller should run apply_profanity_filter() on output
        return True, None
    else:  # "relaxed" or unknown
        return True, None
