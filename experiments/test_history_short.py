# experiments/test_history_short.py

from main import prepare_context, load_base_prompt, load_specialized_prompts
from config.settings_loader import load_settings

DEBUG_MODE = True
SETTINGS = load_settings()
SETTINGS["context"]["max_history_turns"] = 5
SETTINGS["context"]["max_prompt_tokens"] = 512

base_prompt = load_base_prompt()
specialized_prompts = load_specialized_prompts()
fuzzy_matching_enabled = False

history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What's the weather like today?"},
]

message = "Tell me a joke."

context, source = prepare_context(
    message=message,
    history=history,
    base_prompt=base_prompt,
    specialized_prompts=specialized_prompts,
    fuzzy_matching_enabled=fuzzy_matching_enabled
)

print("\n=== Short History Test ===")
print(f"Source: {source}")
print("Final Context:\n", context)