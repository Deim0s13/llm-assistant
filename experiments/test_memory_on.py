from main import prepare_context, load_base_prompt, load_specialized_prompts
from experiments.memory_test_utils import set_memory_enabled
from utils.memory import memory

# 1) Turn memory **on**
SETTINGS = set_memory_enabled(True)

# 2) Pre-seed memory with two turns
memory.clear()
memory.save({"role": "user", "content": "Hello"})
memory.save({"role": "assistant", "content": "Hi, how can I help?"})

# 3) Fake a short live history
live_history = [
    {"role": "user", "content": "What's the weather?"},
]

ctx, _ = prepare_context(
    "Tell me a joke.",           # current user message
    live_history,                # live convo
    load_base_prompt(),
    load_specialized_prompts(),
    fuzzy=True
)

print("=== MEMORY ENABLED ===")
print(ctx)
