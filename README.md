# 🧠 LLM‑Assistant Starter Kit

A hands‑on project for **learning** how to structure, prompt, extend, *and eventually fine‑tune* LLM‑powered applications. What began as a single‑file chatbot has grown into a modular playground for **prompt engineering**, **memory handling**, **summarisation**, and (next) **RAG** & **fine‑tuning**.

---

## Key Objectives

* **Learn by doing** – iterate on prompts, context windows, safety & memory techniques.
* **Repeatable workflows** – versioned releases, Pytest + Ruff checks, GitHub Projects for kan‑ban.
* **Modular code** – swap back‑ends (Redis memory, vector DB, containers) with minimal friction.

---

## Project Status

| Track             | Version      | Notes                                                                                           |
| ----------------- | ------------ | ----------------------------------------------------------------------------------------------- |
| **Latest stable** | **`v0.4.3`** | In‑memory backend, summarise scaffold, first wave of unit‑tests                                 |
| **In progress**   | **`v0.4.4`** | 🔧 **RedisMemoryBackend** (persistent memory), 📝 Summarise MVP, 🤖 CI pipeline (pytest + Ruff) |
| **Planned next**  | **`v0.4.5`** | 🧩 Vector‑DB memory, 🪄 RAG prototype, Docker/Podman containers                                 |

*See the full history → **[Release Notes](./docs/release_notes.md)**.*

---

## Directory Map <small>(key paths only)</small>

```text
.
├── main.py                         # Gradio chat loop & prompt pipeline
├── memory/                         # Unified façade + concrete back‑ends
│   ├── __init__.py                 # Memory.create(<backend>) factory
│   ├── backends/
│   │   ├── in_memory_backend.py    # default volatile store
│   │   └── redis_memory_backend.py # v0.4.4 persistent store
│   └── summariser.py               # summarise_context() scaffold
├── utils/
│   ├── aliases.py                  # Keyword → concept mappings
│   ├── prompt_utils.py             # Order‑preserving alias helper
│   └── safety_filters.py           # Profanity & safety checks
├── config/
│   ├── settings.json               # Runtime config (memory, model, logging …)
│   ├── prompt_template.txt         # Base system prompt
│   └── specialised_prompts.json
├── tests/                          # PyTest suites (memory, summariser …)
├── scripts/
│   └── activate_tests.sh           # helper → sets PYTHONPATH + runs smoke tests
└── docs/                           # Roadmap · Scope · Dev checklist · …
```

---

## Workflow & Planning

Work is managed in **GitHub Projects** → ▶ [LLM Project Board](https://github.com/users/Deim0s13/projects/4/views/1)

```
Initiative → Epic → Milestone (version) → Issue (task)
```

* Every change starts as an **Issue** linked to its Epic & Milestone.
* PR flow: **feature → dev → main** with `Fixes #<id>` semantics.

See full contributor guidelines in **[`CONTRIBUTING.md`](./docs/CONTRIBUTING.md)**.

---

## Quick‑start 🏃‍♂️

```bash
git clone https://github.com/<you>/llm-assistant.git
cd llm-assistant

python -m venv venv          # optional but recommended
source venv/bin/activate     # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

### Run with Redis (optional)

```bash
# Local Redis via Docker
podman run --name redis -p 6379:6379 -d docker.io/redis:7-alpine

export REDIS_URL="redis://localhost:6379/0"
python main.py --memory redis       # or edit config/settings.json
```

If Redis is unavailable the app automatically falls back to volatile memory.

---

### Environment Overrides (`.env`)

Drop a `.env` in the project root to override `settings.json` without touching tracked config:

```env
DEBUG_MODE=true
MAX_HISTORY_TURNS=6
MODEL_DEVICE=mps      # cpu | cuda | mps
```

Supported keys & examples → **docs/dev\_checklist.md**

---

### Platform Setup 💻

| OS                   | Key steps                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **macOS (M‑series)** | Install Python 3.10+, then `pip install torch torchvision torchaudio` (MPS wheels)                                      |
| **Windows + CUDA**   | Install CUDA Toolkit then `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121` |

More detail & troubleshooting → **Cross‑Platform Dev Checklist**.

---

## Unit‑tests 🧪

Run smoke tests & memory‑toggle checks:

```bash
source scripts/activate_tests.sh       # sets PYTHONPATH + runs tests
# or
pytest -q                              # full suite
```

CI (GitHub Actions) kicks off in **v0.4.4** (Ruff + PyTest on every PR).

---

## Learning Roadmap

1. **Phase 1** – Prompt engineering & baseline chatbot *(v0.1 → v0.4.x)*
2. **Phase 2** – Fine‑tuning playground *(v0.5 → v0.7)*
3. **Phase 3** – Packaging, scaling & RAG *(v0.8 → v1.0)*

See **[`ROADMAP.md`](./docs/roadmap.md)** for milestone‑level detail.

---

## Useful Links

* 🗂 Board – [https://github.com/users/Deim0s13/projects/4/views/1](https://github.com/users/Deim0s13/projects/4/views/1)
* 📑 [Scope](./docs/scope.md)
* 🪵 [Release Notes](./docs/release_notes.md)
* 🔬 [Experiments Tracker](./docs/experiments_tracker.md)
* 📝 [Summarisation Planning](./docs/summarisation_planning.md)
* 🗄️ [Memory Flow](./docs/memory_flow.md)

---

## Future Vision ✨

* Vector‑DB (FAISS / Milvus) for semantic memory
* Automated regression tests & CI matrix
* RAG pipelines for knowledge‑base answers
* Containerised deployment (Podman / OpenShift)
* Dev‑agent capabilities & self‑evaluation loops

> **Stay curious. Iterate often. Share your learnings.**
