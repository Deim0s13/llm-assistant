# ════════════════════════════════════════════════════════════════════
#  utils/safety_filters.py – profanity masking & safety gating
# ════════════════════════════════════════════════════════════════════
"""
Basic profanity detection / masking plus a pre-generation safety check.

The API intentionally stays light-weight so stricter classifiers (e.g.
OpenAI moderation, Perspective API, custom models) can later replace the
`evaluate_safety()` stub without changing the main chat flow.
"""

# ───────────────────────────────  Imports ───────────────────────────────

from __future__ import annotations

import logging
import re
from typing import Tuple, Optional
from functools import lru_cache

# ─────────────────────────────── Static data ───────────────────────────────

_DEFAULT_PROFANITY = ["damn", "hell", "shit", "fuck"]

@lru_cache(maxsize=8)
def _build_profanity_regex(strict_terms: tuple[str, ...] = (),
                           extra_terms : tuple[str, ...] = ()) -> re.Pattern:
    """
    Lazily compile  ❱  ( default ∪ strict_terms ∪ extra_terms )  ❰
    into a single *whole-word* regex.  Cached for speed.
    """
    wordlist = set(_DEFAULT_PROFANITY) | set(strict_terms) | set(extra_terms)
    pattern  = r"\b(" + "|".join(map(re.escape, sorted(wordlist))) + r")\b"
    return re.compile(pattern, flags=re.IGNORECASE)

# ───────────────────────────────  Profanity masking ───────────────────────────────

def apply_profanity_filter(text: str, regex: re.Pattern | None = None) -> str:
    """
    Mask profane words with asterisks (same length, preserves case count).
    A pre-compiled *regex* can be passed in from evaluate_safety() so
    we don't compile twice
    """

    regex = regex or _build_profanity_regex()

    def _mask(match: re.Match) -> str:
        return "*" * len(match.group())

    return regex.sub(_mask, text)

# ─────────────────────────────── Safety pre-generation ───────────────────────────────

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
    strict_terms = tuple(config.get("strict_terms", []))
    whitelist = set(w.lower() for w in config.get("relaxed_whitelist", []))
    extra_terms = tuple(config.get("extra_phrases", {}).keys())

    regex = _build_profanity_regex(strict_terms, extra_terms)

    refusal_text = config.get(
        "blocked_response_template",
        "I'm unable to respond to that request due to safety policies.",
    )

    # Detect profanity
    match   = regex.search(message)
    profane = bool(match and match.group(0).lower() not in whitelist)
    if match and log_triggers:
        logging.debug(
            "[Safety] profanity=%s term=%s level=%s msg=%s",
            profane, match.group(0), level, message,
        )

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
