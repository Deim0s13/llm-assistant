#!/usr/bin/env python
"""
experiments/summarisation_playground.py
=======================================

A quick-and-dirty sandbox to explore context-summarisation ideas before they’re
wired into the main chat flow.

Current prototype tries three micro-strategies:

1. **Last-N condensation**      – keep the last N user/assistant lines.
2. **User-only extraction**     – keep only user utterances/questions.
3. **Stub summarise_context()** – call our scaffolded helper (placeholder).

Nothing here touches production code; it’s just for experimentation.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from config.settings_loader import load_settings  # just to demo import
from utils.summariser import summarise_context  # scaffold function

settings = load_settings()  # not used yet but handy for future tweaks

# ───────────────────────── Fake chat-history generator ─────────────────────────
USERS = ["Alice", "Bob"]  # (future: per-user summaries)
TOPICS = [
    "Tell me about the history of Rome.",
    "Why is the sky blue?",
    "Explain quantum entanglement simply",
    "What's the weather like tomorrow?",
    "Recommend a sci-fi novel.",
]
ANSWERS = [
    "Sure! Rome was traditionally founded in 753 BC …",
    "The sky appears blue due to Rayleigh scattering …",
    "In short, entanglement is when two particles …",
    "Looks like sunshine with scattered clouds …",
    "You might enjoy *Dune* by Frank Herbert …",
]


def mock_history(turns: int = 12) -> list[dict]:
    """Generate a pseudo conversation with <turns> user/assistant pairs."""
    hist: list[dict] = []
    for _ in range(turns):
        q = random.choice(TOPICS)
        a = random.choice(ANSWERS)
        hist.append({"role": "user", "content": q})
        hist.append({"role": "assistant", "content": a})
    return hist


history = mock_history(10)  # 10 pairs → 20 messages

# ───────────────────────── Strategy 1 – Last-N condensation ────────────────────
N = 4
last_n = history[-N:]

# ───────────────────────── Strategy 2 – User-only extraction ───────────────────
user_only = [t for t in history if t["role"] == "user"]

# ───────────────────────── Strategy 3 – Stub summariser call ───────────────────
scaffold_summary = summarise_context(history)


# ───────────────────────── Nicely print results to console ─────────────────────
def pp(label: str, obj):
    print(f"\n=== {label} ===")
    if isinstance(obj, list):
        for t in obj:
            print(f"{t['role'][:3].upper():>9}: {t['content']}")
    else:
        print(obj)


pp(f"FULL HISTORY (len={len(history)})", history)
pp(f"LAST-{N} TURNS", last_n)
pp("USER-ONLY QUESTIONS", user_only)
pp("SCAFFOLD SUMMARY", scaffold_summary)

# ───────────────────────── Dump to JSON for later comparison ───────────────────
OUT = Path("experiments/out/summarisation_demo.json")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(
        {
            "last_n": last_n,
            "user_only": user_only,
            "scaffold_summary": scaffold_summary,
        },
        indent=2,
    )
)

# Safe relative-path print
try:
    rel = OUT.resolve().relative_to(Path.cwd())
except ValueError:
    rel = OUT.resolve()  # fallback → absolute path
print(f"\nResults written → {rel}")
