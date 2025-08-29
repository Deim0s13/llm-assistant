# tests/test_safety.py
"""
Unit tests for utils.safety_filters
──────────────────────────────────
Covers:
• Level-based blocking (strict / moderate / relaxed)
• Profanity masking
• Whitelist vs. strict override behaviour
• Multi-word extra phrase detection
"""

from __future__ import annotations

import os
import sys
from copy import deepcopy

import pytest

# ─────────────────────────────  ensure repo root on PYTHONPATH ─────────────────────────────

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config.settings_loader import load_settings
from utils import safety_filters as sf

# ───────────────────────────── pristine baseline  ─────────────────────────────

BASE_SETTINGS = load_settings()


def _cfg(level: str = "moderate", **kv) -> dict:
    """Return a cloned settings dict with safety section tweaked."""
    cfg = deepcopy(BASE_SETTINGS)
    cfg.setdefault("safety", {})
    cfg["safety"]["sensitivity_level"] = level
    cfg["safety"].update(kv)
    return cfg


@pytest.mark.parametrize(
    "level, expected",
    [("strict", False), ("moderate", True), ("relaxed", True)],
)
def test_level_blocking(level, expected):
    allowed, _ = sf.evaluate_safety("oh shit", _cfg(level))
    assert allowed is expected, f"{level=} mis-classified"


def test_masking_moderate():
    allowed, _ = sf.evaluate_safety("damn!", _cfg("moderate"))
    assert allowed
    assert sf.apply_profanity_filter("damn!") == "****!"


def test_whitelist_passes():
    cfg = _cfg("strict", relaxed_whitelist=["hell"])
    allowed, _ = sf.evaluate_safety("what the hell ?", cfg)
    assert allowed, "Whitelisted term was blocked"


def test_strict_terms_override_relaxed():
    cfg = _cfg("relaxed", strict_terms=["foobar"])
    allowed, _ = sf.evaluate_safety("you foobar", cfg)
    assert not allowed, "Custom strict term not blocked"


def test_extra_phrases():
    cfg = _cfg("strict", extra_phrases={"kick ass": "offensive"})
    allowed, _ = sf.evaluate_safety("kick ass", cfg)
    assert not allowed, "Multi-word phrase missed"
