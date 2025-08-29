# experiments/test_history_exact.py

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import main
from config.settings_loader import load_settings

DEBUG_MODE = True
SETTINGS = load_settings()
SETTINGS["context"]["max_history_turns"] = 5
SETTINGS["context"]["max_prompt_tokens"] = 512

base_prompt = main.load_base_prompt()
specialized_prompts = main.load_specialized_prompts()
fuzzy_matching_enabled = False

# Exactly 5 history turns (should all be retained)
history = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello there!"},
    {"role": "user", "content": "Can you help with science?"},
    {"role": "assistant", "content": "Sure, what topic?"},
    {"role": "user", "content": "Tell me about frogs"},
]

msg = "How do frogs breathe?"

context, source = main.prepare_context(
    msg, history, base_prompt, specialized_prompts, fuzzy_matching_enabled
)

print("\n=== Exact History Test ===")
print(f"Source: {source}")
print("Final Context:\n", context)
