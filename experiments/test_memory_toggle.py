import re
import pytest
from main import prepare_context, load_base_prompt, load_specialized_prompts
from experiments.memory_test_utils import set_memory_enabled
from utils.memory import memory

BASE = load_base_prompt()
SPEC = load_specialized_prompts()

@pytest.mark.parametrize("flag", [True, False])
def test_memory_toggle(flag):
    set_memory_enabled(flag)
    memory.clear()

    # seed memory ONLY if flag is True
    if flag:
        memory.save({"role": "user", "content": "Hello"})
        memory.save({"role": "assistant", "content": "Hi!"})

    live = [{"role": "user", "content": "Ping"}]

    ctx, _ = prepare_context("Pong", live, BASE, SPEC, fuzzy=True)

    # --- assertions ---
    assert ctx.startswith(BASE[:50]), "Base prompt missing"
    assert "User: Pong" in ctx,       "Current turn missing"

    if flag:
        # Memory should be present
        assert re.search(r"Hello", ctx), "Expected memory not injected"
    else:
        # No memory text at all
        assert "Hello" not in ctx,       "Memory surfaced when disabled"
