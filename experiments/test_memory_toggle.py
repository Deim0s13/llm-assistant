# experiments/test_memory_toggle.py
import re, pytest, importlib
from pathlib import Path

from experiments.memory_test_utils import set_memory_enabled
from utils.memory import memory
import main as _main

# ──────────────────────────────────────────────────────────────
# Patch prompt paths so the test uses *tiny* files, ensuring
# our injected memory won’t be truncated.
# ──────────────────────────────────────────────────────────────
_MAIN = importlib.reload(_main)

tiny_prompt_path = Path(__file__).with_suffix(".base_prompt.txt")
tiny_prompt_path.write_text("You are a **test** assistant.")
_MAIN.BASE_PROMPT_PATH = str(tiny_prompt_path)          # type: ignore[attr-defined]

empty_spec_path = Path(__file__).with_suffix(".spec.json")
empty_spec_path.write_text("{}")
_MAIN.SPECIALIZED_PROMPTS_PATH = str(empty_spec_path)   # type: ignore[attr-defined]

BASE = _MAIN.load_base_prompt()
SPEC = _MAIN.load_specialized_prompts()

_MAIN.SETTINGS["context"]["max_prompt_tokens"] = 2048

# ──────────────────────────────────────────────────────────────
@pytest.mark.parametrize("mem_on", [True, False])
def test_memory_toggle(mem_on):
    set_memory_enabled(mem_on)
    _MAIN.SETTINGS["memory"]["enabled"] = mem_on  # keep prepare_context in sync
    _MAIN.memory.clear()

    if mem_on:
        _MAIN.memory.save({"role": "user", "content": "Hello"})
        _MAIN.memory.save({"role": "assistant", "content": "Hi!"})

    live_history = [{"role": "user", "content": "Ping"}]

    ctx, _ = _MAIN.prepare_context("Pong", live_history, BASE, SPEC, fuzzy=False)

    # common assertions
    assert ctx.startswith(BASE), "Base prompt missing or altered"
    assert "User: Pong" in ctx,  "Current turn missing"

    # mode-specific assertions
    if mem_on:
        assert any(tok in ctx for tok in ("Hello", "Hi!")), \
            "Memory not injected while enabled"
    else:
        assert all(tok not in ctx for tok in ("Hello", "Hi!")), \
            "Memory surfaced even though disabled"
