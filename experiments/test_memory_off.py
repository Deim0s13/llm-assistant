from main import prepare_context, load_base_prompt, load_specialized_prompts
from experiments.memory_test_utils import set_memory_enabled
from utils.memory import memory

# 1) Turn memory **off**
SETTINGS = set_memory_enabled(False)

# 2) Clear any previous memory to prove fallback
memory.clear()

live_history = [
    {"role": "user", "content": "Who painted the Mona Lisa?"},
]

ctx, _ = prepare_context(
    "And what year?",            # current user message
    live_history,
    load_base_prompt(),
    load_specialized_prompts(),
    fuzzy=True
)

print("=== MEMORY DISABLED ===")
print(ctx)
