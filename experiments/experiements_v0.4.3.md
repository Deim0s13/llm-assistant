#### 🔬 Summariser Smoke-Test

```python
from utils.summariser import summarise_context

history = [
    {"role": "user", "content": "Hi there"},
    {"role": "assistant", "content": "Hello!"},
]

print(summarise_context(history))
# ➜ "Summary of prior discussion (placeholder – real summarisation TBD)"
