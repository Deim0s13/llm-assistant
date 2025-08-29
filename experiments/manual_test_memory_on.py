#!/usr/bin/env python
"""
Quick manual smoke-test: memory ENABLED
───────────────────────────────────────
• Memory flag switched on
• Pre-seed two memory turns
• Verify injected memory + live history
"""

from experiments.memory_test_utils import set_memory_enabled
from main import (
    load_base_prompt,
    load_specialized_prompts,
    prepare_context,
)
from utils.memory import memory

# 1) Enable memory and clear any previous state
set_memory_enabled(True)
memory.clear()

# 2) Pre-seed conversation memory
memory.save({"role": "user", "content": "Hello"})
memory.save({"role": "assistant", "content": "Hi, how can I help?"})

# 3) Minimal live history
history = [{"role": "user", "content": "What's the weather?"}]

ctx, _ = prepare_context(
    "Tell me a joke.",
    history,
    load_base_prompt(),
    load_specialized_prompts(),
    fuzzy=False,
)

print("=== MEMORY ENABLED ===")
print(ctx)
