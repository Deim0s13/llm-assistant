# tests/test_memory.py
"""
Unit-tests for the conversation-memory layer and its interaction with
`prepare_context()`.

Covered scenarios
────────────────────────────────────────────────────────────
1. Memory enabled  + data present            → mem lines injected
2. Memory enabled  + empty store             → live turns only
3. Memory disabled via settings flag         → live turns only
4. Backend forced to NONE (simulated error)  → behave like disabled
"""
from __future__ import annotations

import importlib
import json
from copy import deepcopy

import pytest

import main
from config.settings_loader import load_settings


# ───────────────────────────── helper utils ─────────────────────────────
def _reload_main():
    """Reload `main` after we monkey-patch settings so changes take effect."""
    return importlib.reload(main)


def _fake_settings(*, enabled: bool, backend: str) -> dict:
    """Return a minimal settings dict with a specific memory config."""
    base = deepcopy(load_settings())
    base["memory"].update({"enabled": enabled, "backend": backend})
    base["context"].update({"max_history_turns": 4, "max_prompt_tokens": 512})
    base.setdefault("logging", {})["prompt_preview"] = False
    return base


def _turn(role: str, text: str) -> dict:
    return {"role": role, "content": text}


# ────────────────────────────── fixtures ────────────────────────────────
@pytest.fixture()
def base_prompt(tmp_path, monkeypatch):
    """Create a throw-away base prompt file and patch the path in `main`."""
    fp = tmp_path / "prompt_template.txt"
    fp.write_text("You are a test assistant.")
    monkeypatch.setattr("main.BASE_PROMPT_PATH", str(fp))
    return fp.read_text().strip()


@pytest.fixture()
def specialised_prompts(tmp_path, monkeypatch):
    """Provide an empty specialised-prompts file to keep tests isolated."""
    sp = tmp_path / "specialised_prompts.json"
    sp.write_text(json.dumps({}))
    monkeypatch.setattr("main.SPECIALIZED_PROMPTS_PATH", str(sp))
    return {}


# ───────────────────────────── test cases ───────────────────────────────
def test_memory_enabled_with_data(monkeypatch, base_prompt, specialised_prompts):
    """Memory ON – stored turns must precede live history."""
    from utils import memory as mem_mod

    # 1) Patch settings
    monkeypatch.setattr(
        "config.settings_loader.load_settings",
        lambda filepath=None: _fake_settings(enabled=True, backend="in_memory"),
    )

    # 2) Reset singleton & preload two memory turns
    importlib.reload(mem_mod)
    mem_mod.memory.save(_turn("user", "hello from memory"))
    mem_mod.memory.save(_turn("assistant", "hi from memory"))

    m = _reload_main()

    live_history = [_turn("user", "latest question")]
    ctx, _ = m.prepare_context("latest question", live_history,
                               base_prompt, specialised_prompts, fuzzy=False)

    assert "hello from memory" in ctx
    before, _ = ctx.split("latest question", 1)
    assert "hello from memory" in before   # mem lines appear first


def test_memory_enabled_empty(monkeypatch, base_prompt, specialised_prompts):
    """Memory ON but empty – context should contain only live history."""
    from utils import memory as mem_mod

    monkeypatch.setattr(
        "config.settings_loader.load_settings",
        lambda filepath=None: _fake_settings(enabled=True, backend="in_memory"),
    )
    importlib.reload(mem_mod)  # empty store
    m = _reload_main()

    live_history = [_turn("user", "just now")]
    ctx, _ = m.prepare_context("just now", live_history,
                               base_prompt, specialised_prompts, False)

    assert ctx.count("just now") == 2          # in history + user line
    assert "hello from memory" not in ctx      # nothing injected


def test_memory_disabled(monkeypatch, base_prompt, specialised_prompts):
    """Memory OFF via settings – behaves as if no memory exists."""
    monkeypatch.setattr(
        "config.settings_loader.load_settings",
        lambda filepath=None: _fake_settings(enabled=False, backend="in_memory"),
    )
    m = _reload_main()

    live_history = [_turn("user", "no-mem turn")]
    ctx, _ = m.prepare_context("no-mem turn", live_history,
                               base_prompt, specialised_prompts, False)

    assert "no-mem turn" in ctx
    assert "hello from memory" not in ctx


def test_memory_backend_none(monkeypatch, base_prompt, specialised_prompts):
    """Backend NONE even with memory enabled – fall back to live context."""
    monkeypatch.setattr(
        "config.settings_loader.load_settings",
        lambda filepath=None: _fake_settings(enabled=True, backend="none"),
    )
    m = _reload_main()

    live_history = [_turn("user", "fallback check")]
    ctx, _ = m.prepare_context("fallback check", live_history,
                               base_prompt, specialised_prompts, False)

    assert "fallback check" in ctx
    assert "hello from memory" not in ctx
