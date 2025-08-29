# ════════════════════════════════════════════════════════════════════
#  experiments/test_prepare_context_summary.py – summary insertion tests
# ════════════════════════════════════════════════════════════════════

from collections.abc import Generator
from copy import deepcopy

import pytest

from config.settings_loader import load_settings
from main import SETTINGS, prepare_context

# ───────────────────────────── Helpers ─────────────────────────────


def _build_naive_context(history: list[dict[str, str]], msg: str, base_prompt: str) -> str:
    # mirror the simple build() used in prepare_context (no summary)
    ctx: str = base_prompt
    for turn in history:
        ctx += f"\n{turn['role'].capitalize()}: {turn['content']}"
    ctx += f"\nUser: {msg}\nAssistant:"
    return ctx


# ───────────────────────────── Fixtures ────────────────────────────


@pytest.fixture(autouse=True)
def restore_settings() -> Generator[None, None, None]:
    # snapshot & restore global SETTINGS so tests don't leak config
    # Load fresh settings and make a deep copy
    clean_settings = load_settings()
    original_settings = deepcopy(SETTINGS)

    # Clear and reset BEFORE the test runs
    SETTINGS.clear()
    SETTINGS.update(deepcopy(clean_settings))

    yield

    # Restore the original settings after the test
    SETTINGS.clear()
    SETTINGS.update(original_settings)


@pytest.fixture
def sample_history() -> list[dict[str, str]]:
    # 10 alternating user/assistant turns – enough to trigger by turns
    hist: list[dict[str, str]] = []
    for i in range(10):
        role = "user" if i % 2 == 0 else "assistant"
        hist.append({"role": role, "content": f"{role.capitalize()} message {i}"})
    return hist


# ─────────────────── Summary insertion (enabled) ───────────────────


def test_summary_injected_when_triggered_by_turns(sample_history: list[dict[str, str]]) -> None:
    # configure: enabled + low min_turns → guaranteed trigger
    SETTINGS.setdefault("summarisation", {})
    SETTINGS["summarisation"].update(
        {
            "enabled": True,
            "strategy": "bullet",
            "min_turns": 8,
            "max_chars": 512,
        }
    )
    # avoid unrelated token trimming in these tests
    SETTINGS["context"]["max_prompt_tokens"] = 100_000
    SETTINGS["context"]["max_history_turns"] = 100

    msg: str = "what is the weather?"
    base_prompt: str = "you are a helpful assistant."
    spec_prompts: dict[str, str] = {}
    fuzzy: bool = False

    # make history *long* so summarisation compresses it
    long_history: list[dict[str, str]] = []
    for i in range(10):
        role = "user" if i % 2 == 0 else "assistant"
        # repeat each message to ensure substantial length
        content = (f"{role.capitalize()} message {i}. " * 30).strip()
        long_history.append({"role": role, "content": content})

    pre_ctx: str = _build_naive_context(long_history, msg, base_prompt)
    context, _ = prepare_context(msg, long_history, base_prompt, spec_prompts, fuzzy)

    # a) summary present (heuristic returns bullet lines)
    assert ("• " in context) or ("Summary" in context)

    # b) summary appears before the current "User:" line
    bullet_pos = context.find("• ")
    if bullet_pos == -1:
        bullet_pos = context.find("Summary")
    assert bullet_pos != -1
    assert bullet_pos < context.rfind("\nUser:")

    # c) assistant suffix remains last
    assert context.strip().endswith("Assistant:")

    # d) summary reduces overall context length (compression effect)
    assert len(context) <= len(pre_ctx), (
        f"Expected shorter or equal context after summarisation: {len(context)} vs {len(pre_ctx)}"
    )


# ─────────────── Regression: disabled → no summary ────────────────


def test_no_summary_when_disabled(sample_history: list[dict[str, str]]) -> None:
    SETTINGS.setdefault("summarisation", {})
    SETTINGS["summarisation"].update(
        {
            "enabled": False,
            "min_turns": 8,
            "strategy": "bullet",
        }
    )
    SETTINGS["context"]["max_prompt_tokens"] = 100_000
    SETTINGS["context"]["max_history_turns"] = 100

    msg: str = "how does it work?"
    base_prompt: str = "you are a helpful assistant."
    spec_prompts: dict[str, str] = {}
    fuzzy: bool = False

    context, _ = prepare_context(msg, sample_history, base_prompt, spec_prompts, fuzzy)

    # no summary markers when disabled
    assert "• " not in context
    assert "Summary" not in context

    # assistant suffix remains last
    assert context.strip().endswith("Assistant:")


# ─────────────── Order & formatting sanity checks ────────────────


def test_summary_order_and_format(sample_history: list[dict[str, str]]) -> None:
    SETTINGS.setdefault("summarisation", {})
    SETTINGS["summarisation"].update(
        {
            "enabled": True,
            "min_turns": 6,
            "strategy": "bullet",
            "max_chars": 512,
        }
    )
    SETTINGS["context"]["max_prompt_tokens"] = 100_000
    SETTINGS["context"]["max_history_turns"] = 100

    msg: str = "tell me about openai."
    base_prompt: str = "you are a helpful assistant."
    spec_prompts: dict[str, str] = {}
    fuzzy: bool = False

    context, _ = prepare_context(msg, sample_history, base_prompt, spec_prompts, fuzzy)

    # expect bullets near the top (after the base prompt line)
    lines = context.splitlines()
    window = "\n".join(lines[:6])
    assert ("• " in window) or ("Summary" in window)

    # assistant suffix remains last
    assert context.strip().endswith("Assistant:")
