#!/usr/bin/env python
"""
Quick manual smoke-test: memory DISABLED
────────────────────────────────────────
• Memory flag switched off
• Memory store cleared
• Context should contain *only* the live turn
"""

from experiments.memory_test_utils import set_memory_enabled
from main import (
    load_base_prompt,
    load_specialized_prompts,
    prepare_context,
)
from utils.memory import memory

# 1) Disable memory and reset singleton state
set_memory_enabled(False)
memory.clear()

# 2) Live history for this test
history = [{"role": "user", "content": "Who painted the Mona Lisa?"}]

ctx, _ = prepare_context(
    "And what year?",
    history,
    load_base_prompt(),
    load_specialized_prompts(),
    fuzzy=False,
)

print("=== MEMORY DISABLED ===")
print(ctx)
