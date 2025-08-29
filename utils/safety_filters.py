# ════════════════════════════════════════════════════════════════════
#  utils/safety_filters.py – profanity masking & safety gating
# ════════════════════════════════════════════════════════════════════
"""
Basic profanity detection / masking plus a pre-generation safety check.

The API intentionally stays light-weight so stricter classifiers (e.g.
OpenAI moderation, Perspective API, custom models) can later replace the
`evaluate_safety()` stub without changing the main chat flow.
"""

from __future__ import annotations

# ───────────────────────────────────────────────────────── Logging ──
import logging

LOGGER = logging.getLogger(__name__)  # inherit root config from main

# ───────────────────────────────────────────────────────── Imports ──
import re
from functools import lru_cache
from typing import Any, Dict, Optional, Tuple

# ─────────────────────────────────────────────────────── Static data ──
_DEFAULT_PROFANITY: Tuple[str, ...] = ("damn", "hell", "shit", "fuck")


@lru_cache(maxsize=1)
def _default_regex() -> re.Pattern[str]:
    """Cached whole-word regex built from _DEFAULT_PROFANITY."""
    pat = r"\b(" + "|".join(map(re.escape, sorted(_DEFAULT_PROFANITY))) + r")\b"
    return re.compile(pat, re.IGNORECASE)


# ─────────────────────────────── Regex builder (cached) ──────────────
@lru_cache(maxsize=8)
def _build_profanity_regex(
    strict_terms: Tuple[str, ...] = (),
    extra_terms: Tuple[str, ...] = (),
) -> re.Pattern[str]:
    """
    Compile  ❱  ( default ∪ strict_terms ∪ extra_terms )  ❰
    into a single *whole-word* regex. Cached for speed.
    """
    wordlist = set(_DEFAULT_PROFANITY) | set(strict_terms) | set(extra_terms)
    if not wordlist:
        # Compile a regex that never matches to keep types simple downstream.
        return re.compile(r"(?!x)x")
    pattern = r"\b(" + "|".join(map(re.escape, sorted(wordlist))) + r")\b"
    return re.compile(pattern, re.IGNORECASE)


# ───────────────────────────────────── Profanity masking ─────────────
def apply_profanity_filter(text: str, regex: re.Pattern[str] | None = None) -> str:
    """
    Mask profane words with asterisks. If no regex is provided, use a cached
    whole-word default compiled from _DEFAULT_PROFANITY.
    """
    if regex is None:
        regex = _default_regex()

    def _mask(match: re.Match[str]) -> str:
        return "*" * len(match.group(0))

    return regex.sub(_mask, text)


# ─────────────────────────────── Safety pre-generation ───────────────
def evaluate_safety(
    message: str,
    settings: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Light safety gate that checks *input* for profanity before we call the model.

    Returns
    -------
    allowed : bool
        Whether the message is safe to continue processing.
    blocked_message : Optional[str]
        If blocked, a pre-formatted refusal text to send back.

    Behaviour by *sensitivity_level* in ``settings['safety']``:
    ┌────────────┬───────────────────────────────────────────────┐
    │ strict     │ Always block on profanity (or strict term).   │
    │ moderate   │ Allow but caller should mask output.           │
    │ relaxed    │ No blocking.                                   │
    └────────────┴───────────────────────────────────────────────┘
    """
    cfg = settings.get("safety", {})
    level = str(cfg.get("sensitivity_level", "moderate")).lower()
    log_triggers = bool(cfg.get("log_triggered_filters", False))

    # Optional lists/dicts in settings; coerce to expected shapes
    strict_terms: Tuple[str, ...] = tuple(cfg.get("strict_terms", ()))
    whitelist = {str(w).lower() for w in cfg.get("relaxed_whitelist", ())}

    # `extra_phrases` may be a dict of {phrase: …}; keys become terms
    extra_terms: Tuple[str, ...] = tuple(
        getattr(cfg.get("extra_phrases", {}), "keys", lambda: ())()
    )

    regex = _build_profanity_regex(strict_terms, extra_terms)

    refusal_text: str = str(
        cfg.get(
            "blocked_response_template",
            "I'm unable to respond to that request due to safety policies.",
        )
    )

    # ── Detect profanity ────────────────────────────────────────────
    match = regex.search(message)
    matched_word = match.group(0).lower() if match else ""
    profane = bool(match and matched_word not in whitelist)

    if profane and log_triggers:
        LOGGER.debug(
            "[Safety] Profanity detected (level=%s, term=%s): %s",
            level,
            matched_word,
            message,
        )

    # ── Absolute block: any strict term triggers a block ────────────
    if profane and matched_word in strict_terms:
        return False, refusal_text

    # ── Sensitivity ladder ──────────────────────────────────────────
    if not profane:
        return True, None

    if level == "strict":
        return False, refusal_text
    if level == "moderate":
        return True, None  # caller may apply output masking
    # relaxed / unknown
    return True, None
