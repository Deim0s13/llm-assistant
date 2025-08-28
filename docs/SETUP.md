# SETUP.md — Local Development Setup

A step-by-step guide to get the **LLM Assistant** running locally for development and testing.

> This doc complements the README by going deeper on environment config, `.env` usage, and test execution.

---

## 1) Prerequisites

* **Python**: 3.10+ (3.11/3.12 fine)
* **Git**: latest recommended
* **pip**: 22+ recommended
* **Optional (GPU)**:

  * NVIDIA CUDA toolkit + compatible PyTorch
  * Apple Silicon: macOS 13+ with Metal (MPS) support for PyTorch

> The app auto-selects device at runtime (CUDA → MPS → CPU) and logs the selected device.

---

## 2) Clone the repository

```bash
git clone https://github.com/Deim0s13/llm-assistant.git
cd llm-assistant
```

---

## 3) Create a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> You should now see `(venv)` in your shell prompt.

---

## 4) Install dependencies

Install the runtime and dev tools:

```bash
pip install --upgrade pip
pip install -r requirements.txt
# (optional) developer extras
pip install -r requirements-dev.txt
```

If you plan to use the Redis memory backend locally:

```bash
pip install redis fakeredis
```

---

## 5) Configuration overview

The app reads configuration in this order:

1. **`.env`** (optional) — overrides specific keys (good for local tweaks)
2. **`config/settings.json`** — base configuration (checked into repo)

`settings_loader.py` merges `.env` into `settings.json` so you can safely experiment without changing the JSON file.

---

## 6) Create a `.env` (optional but recommended)

Create a file named `.env` in the project root. Example:

```env
# Logging / debug
DEBUG_MODE=true

# Model and device overrides
MODEL_NAME=google/flan-t5-base
MODEL_DEVICE=auto   # options: auto | cpu | cuda | mps

# Context / prompt budgets (override JSON if needed)
MAX_HISTORY_TURNS=50
MAX_PROMPT_TOKENS=2048

# Summarisation controls (v0.4.5)
SUMMARISATION_ENABLED=true
SUMMARISATION_STRATEGY=bullet
SUMMARISATION_MIN_TURNS=8
SUMMARISATION_MAX_CHARS=512
SUMMARISATION_TRIGGER_BY_TOKENS=false
SUMMARISATION_MAX_CONTEXT_TOKENS=2000

# Memory backend
MEMORY_ENABLED=true
MEMORY_BACKEND=in_memory   # options: in_memory | redis

# Redis (if using redis backend)
REDIS_URL=redis://localhost:6379/0
```

> Any of the above keys map to the structured fields in `config/settings.json`. If a key appears in both places, `.env` wins.

---

## 7) Key settings in `config/settings.json`

Typical sections:

```json
{
  "context": {
    "max_history_turns": 50,
    "max_prompt_tokens": 2048
  },
  "summarisation": {
    "enabled": true,
    "strategy": "bullet",
    "min_turns": 8,
    "max_chars": 512,
    "trigger_by_tokens": false,
    "max_context_tokens": 2000
  },
  "memory": {
    "enabled": true,
    "backend": "in_memory"
  },
  "safety": {
    "sensitivity_level": "moderate",
    "profanity_filter": true
  }
}
```

* **Summarisation**: injects a brief bullet summary as history grows.
* **Memory**: choose `in_memory` (default) or `redis` (requires a local Redis).
* **Safety**: `strict | moderate | relaxed`.

---

## 8) Run the app

```bash
python main.py
```

You’ll see:

```
* Running on local URL:  http://127.0.0.1:7860
```

Open that URL in your browser.

### Tips

* Live debug logs are written to `debug.log`. Console logs show high-level events; detailed traces go to the file handler.
* Developer Playground (inside the UI) lets you test alias-matched prompts and preview generations.

---

## 9) Running tests

All automated tests live under `tests/`.

```bash
pytest -q
```

With coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

Common suites include:

* **Memory backends**: in-memory + (optionally) Redis via `fakeredis`
* **Context**: trimming by history length and token budget
* **Summarisation**: insertion order, triggers, and toggles

> If Redis isn’t available, tests that require it will **skip** gracefully.

---

## 10) Optional: Redis backend locally

1. Install Redis:

* macOS (brew): `brew install redis && brew services start redis`
* Linux: use your package manager or Docker

2. Set `.env`:

```env
MEMORY_BACKEND=redis
REDIS_URL=redis://localhost:6379/0
```

3. Run the app and verify the boot log shows the Redis backend.

---

## 11) Troubleshooting

* **Port already in use (7860)**
  Run with a different port:
  `python main.py` then set `share=True` in `demo.launch()` if needed, or export `GRADIO_SERVER_PORT`.

* **Very slow generations**
  Confirm device selection in the logs. If CPU is selected but you have a GPU:

  * NVIDIA: install the CUDA-enabled torch wheel from [https://pytorch.org](https://pytorch.org)
  * Apple: ensure macOS + Xcode CLT are up-to-date; MPS shows as “mps” in the log

* **Token/sequence length warnings**
  Increase `context.max_prompt_tokens` or reduce the number/length of history turns. Summarisation helps; tune `summarisation.min_turns` / `max_chars`.

* **Import errors in tests**
  Ensure you activated the `venv`, and run tests from the repo root so `tests/` can import project modules.

---

## 12) Project structure (simplified)

```text
.
├── main.py
├── config/
│   ├── settings.json
│   ├── prompt_template.txt
│   └── specialized_prompts.json
├── utils/
│   ├── aliases.py
│   ├── prompt_utils.py
│   ├── safety_filters.py
│   └── summariser.py
├── memory/
│   ├── __init__.py
│   └── backends/
│       ├── in_memory_backend.py
│       └── redis_memory_backend.py
├── tests/
│   ├── conftest.py
│   ├── test_context_trimming.py
│   ├── test_memory_backends.py
│   └── test_summary_on_off.py
├── docs/
│   ├── SETUP.md          ← this file
│   ├── scope.md
│   └── release_notes.md
└── requirements*.txt
```

---

## 13) Next steps

* Start the app (`python main.py`) and try the chat + Developer Playground.
* Adjust summarisation and memory in `.env` to see their effect.
* Run the tests and (optionally) wire coverage thresholds in CI.
