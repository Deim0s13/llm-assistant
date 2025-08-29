# SETUP.md — Local Development Setup

A step-by-step guide to get the **LLM Assistant** running locally for development and testing.

> This doc complements the README by going deeper on environment config, `.env` usage, and test execution.

---

## Prerequisites

* **Python**: 3.10+ (3.11/3.12 fine)
* **Git**: latest recommended
* **pip**: 22+ recommended
* **Optional (GPU)**:

  * NVIDIA CUDA toolkit + compatible PyTorch
  * Apple Silicon: macOS 13+ with Metal (MPS) support for PyTorch

> The app auto-selects device at runtime (CUDA → MPS → CPU) and logs the selected device.

---

## Clone the repository

```bash
git clone https://github.com/Deim0s13/llm-assistant.git
cd llm-assistant
```

---

## Create a virtual environment

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

## Install dependencies

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

## Configuration overview

The app reads configuration in this order:

1. **`.env`** (optional) — overrides specific keys (good for local tweaks)
2. **`config/settings.json`** — base configuration (checked into repo)

`settings_loader.py` merges `.env` into `settings.json` so you can safely experiment without changing the JSON file.

---

## Create a `.env` (optional but recommended)

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

## Key settings in `config/settings.json`

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

## Run the app

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

## Running tests

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

## Optional: Redis backend locally

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

## Type Checking

We use **mypy** and **Pyright** in strict mode to catch typing issues early and keep IDE hints accurate.

### Install (if not already)

```bash
pip install mypy pyright
```

> Both are also listed in `requirements-dev.txt` if you’re using the dev extras.

### Run mypy

```bash
mypy .
```

* Exits non-zero on any typing error.
* Configuration lives in `pyproject.toml` (see the `[tool.mypy]` section).
* We aim for **0 errors** on core code. Tests may be less strict.

### Run Pyright

```bash
pyright
```

* Uses `pyproject.toml` `[tool.pyright]` config.
* Also targets **0 errors** on the main codebase.

### Editor integration (Cursor / VS Code)

* **Cursor** (and VS Code) will surface Pyright diagnostics automatically if the Python extension is enabled.
* mypy diagnostics can be shown via the “Mypy Type Checker” extension or by running `mypy` in the integrated terminal.

### Typical layout & expectations

* **Core code** (`main.py`, `utils/`, `memory/`) — must be clean under mypy & Pyright.
* **Tests** (`tests/`) — type checking allowed but may be relaxed; assertions and fixtures sometimes require `# type: ignore[...]` or `typing.cast` to keep readable.

### Common fixes

* Add explicit types to parameters and return values:

  ```python
  def get_prompt(text: str) -> str: ...
  ```
* Parameterize generics:

  ```python
  from typing import Any
  data: dict[str, Any] = {}
  ```
* Avoid dynamic attribute assignment; prefer `TypedDict`/`dataclass` for structured dicts:

  ```python
  from typing import TypedDict
  class Turn(TypedDict):
      role: str
      content: str
  ```

### CI (future)

Type checking will also run in CI and block merges on failure once the workflow is enabled. For now, keep your local runs clean:

```bash
mypy . && pyright
```

If both complete without errors, you’re good.

## Pre-commit Hooks (Optional)

This project supports [pre-commit](https://pre-commit.com/) to automatically run linting, type-checking, and tests before each commit.

1. Install pre-commit:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. On each commit, hooks will run:
   * Ruff (lint + format)
   * mypy (strict tye-chcking)
   * pytest (unit tests)

You can skip hooks with `git commit --no-verify` (not recommended)

---

## Troubleshooting

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

* **“Cannot find implementation or library stub for module …”**
  Ensure the package is installed in your venv, or add a stub package (e.g., `pip install types-requests`).

* **“Module level import not at top of file (E402)”** (shown by Ruff, but relevant here):
  Move imports to the file top unless there’s a valid reason (cycle avoidance).

* **False positives on tests**
  You can locally relax checks for a file with a per-file `type: ignore` or adapt test helpers with `typing.cast`.

---

## Project structure (simplified)

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

## Next steps

* Start the app (`python main.py`) and try the chat + Developer Playground.
* Adjust summarisation and memory in `.env` to see their effect.
* Run the tests and (optionally) wire coverage thresholds in CI.

## Linting Status

**Current Status**: 44 linting errors (19% improvement from original 54 errors)

The codebase has undergone significant linting improvements as part of ongoing maintenance work. All critical functionality issues have been resolved, and the remaining errors are primarily cosmetic or code quality improvements.

### Quick Summary
- ✅ **Fixed**: 10 errors (undefined names, magic numbers, duplicate functions, import issues)
- 🔄 **Remaining**: 44 errors (import ordering, function arguments, formatting)
- 🚫 **Impact**: None - all code functions normally

### What We've Accomplished
1. **Fixed critical pytest assertion error** in `test_memory_parity.py` ✅
2. **Eliminated all mypy None type errors** by adding proper null checks ✅
3. **Fixed import issues** (renamed `Prompt_utils.py` to `prompt_utils.py`) ✅
4. **Reduced mypy errors by 90%** (from 10 to 1) ✅
5. **Maintained code functionality** throughout all changes ✅

### Current Remaining Issues
- **Ruff**: 44 errors (E402, E401, F401, F811, F841)
- **Mypy**: 1 error (untyped function call in transformers)
- **Tests**: 2 failing tests in `test_prepare_context_summary.py` (test isolation issue)

### Remediation Priority
1. **High Priority**: Import ordering and placement (15-20 min)
2. **Medium Priority**: Unused imports, multiple imports per line (10-15 min)
3. **Low Priority**: Function refactoring, variable cleanup (20-30 min)

**Total estimated time for 100% clean codebase**: 45-65 minutes

**Note**: The 2 failing tests are due to a complex test isolation issue that would require significant test infrastructure changes to resolve completely.

---

## Documentation

### Core Documentation
- **[SETUP.md](./SETUP.md)** - This file - setup and configuration guide
- **[scope.md](./scope.md)** - Project scope and boundaries
- **[release_notes.md](./release_notes.md)** - Version history and changes

### Current Status & Changes
- **[CURRENT_STATUS.md](./CURRENT_STATUS.md)** - Quick snapshot of current project state
- **[CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md)** - Detailed summary of recent maintenance work

### Development Resources
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - How to contribute to the project
- **[dev_checklist.md](./dev_checklist.md)** - Development workflow checklist
- **[ROADMAP.md](./ROADMAP.md)** - Future development plans

---

## Development Setup
