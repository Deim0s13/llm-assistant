# Release Notes 📜

A chronological changelog for the **LLM‑Assistant Starter Kit**. Each entry lists the headline features, notable refactors, and links to deeper docs/tests where useful.

---

## Version Summary Table

| Version   | State      | Headline Highlights                                                |
|:---------:|:----------:|--------------------------------------------------------------------|
| **v0.1.0** | ✅ *Done* | Static base prompt, no memory, minimal Gradio UI                  |
| **v0.2.x** | ✅ *Done* | Multi-turn history, specialised prompts, alias mapping, diagnostics |
| **v0.3.0** | ✅ *Done* | Structured "experiments" framework & documentation re-org          |
| **v0.4.0** | ✅ *Done* | Robust alias detection, fuzzy matching, improved logging           |
| **v0.4.1** | ✅ *Done* | Configurable *Safety Guardrails* (profanity, sensitivity modes)    |
| **v0.4.2** | ✅ *Done* | Context-window trimming, cross-platform device detection, `.env`   |
| **v0.4.3** | ✅ *Done* | In-process **Memory backend**, optional summarisation scaffold     |
| **v0.4.4** | ✅ *Done* | **Persistent memory (Redis/SQLite)**, settings auto-fallback, expanded tests |
| **v0.4.5** | ✅ *Done* | **Summarisation MVP, Technical Spec, Planning docs**       |
| **v0.5.0** | ✅ *Done* | **Multi-environment CI matrix** (Linux/macOS/Windows), Python 3.10+3.11, Containerisation |
| **v0.5.1** | ✅ *Done* | **GHCR publishing** + **in-container test execution** with coverage |

| **v0.5.2** | 🔼 *Planned* | Model upgrade (FLAN → Mistral 7B) + config toggle          |
| **v0.5.3** | 🔼 *Planned* | Prompt/response quality improvements & structured outputs   |
| **v0.5.4** | 🔼 *Planned* | CI enhancements: coverage thresholds, test dashboards      |
| **v0.5.5** | 🔼 *Planned* | Consolidated evaluation harness & model comparison          |
| **v0.6.x** | 🔼 *Planned* | RAG prototype (file-based Q&A)                                |
| **v0.7.x** | 🔼 *Planned* | Fine-tuning foundation                                        |

---

## v0.1.0 – First Proof‑of‑Concept *(2025‑04‑05)*

* Static system prompt embedded in code.
* No history; each user turn isolated.
* Bare‑bones Gradio textbox UI.

---

## v0.2.x – From Single‑Turn to Specialised Prompts *(2025‑04‑15 → 05‑02)*

### v0.2.0

* **Conversation History** – maintains role/content pairs.
* External **`prompt_template.txt`** and tunable generation sliders.

### v0.2.1 → v0.2.5 Highlights

* **Specialised Prompt Injection** via `specialized_prompts.json`.
* **Alias Mapping** (`prompt_aliases.json`) for flexible triggers.
* **Fuzzy Matching Toggle**, **Developer Playground**, **Advanced UI**.
* Model upgrade to `google/flan‑t5‑base`.
* Continuous debug‑log refinements & bug‑fixes.

*Patch‑level notes:* `experiments/experiments_v0.2.*.md`.

---

## v0.3.0 – Experiments Framework 📊 *(2025‑05‑10)*

* Introduced **/experiments/** folder & markdown logs.
* Captured systematic tests on prompt phrasing, safety modes, token limits.
* Docs restructure: `scope.md`, `roadmap.md`, dedicated release notes.
* Insights fed into later prompt‑matching & safety design.

---

## v0.4.x Track – Stability, Safety, Memory

### v0.4.0 – Alias & Prompt Matching Overhaul *(2025‑05‑30)*

* Token‑level alias detection (`alias_in_message`).
* Expanded alias library & diagnostics (`[Prompt] …` logs).
* Clear fallback reasoning when no match found.

### v0.4.1 – Configurable Safety Guardrails *(2025‑06‑10)*

* **`settings.json → safety`**: `sensitivity_level`, `profanity_filter`.
* Modes: **strict · moderate · relaxed**.
* Runtime filtering (moderate) or blocking (strict).
* Refusal template driven by config.
* Manual tests recorded in `experiments_v0.4.1.md`.

### v0.4.2 – Context Window & Dev Hygiene *(2025‑06‑25)*

* **Context Trimming** based on `max_history_turns` & `max_prompt_tokens`.
* Debug logs show retained turns & token counts.
* **Device Auto‑Select**: CUDA → MPS → CPU, logged at startup.
* `.env` overrides via `python‑dotenv`.
* Migration to **GitHub Projects** board; docs (`README`, `CONTRIBUTING`) updated.

### v0.4.3 – Volatile Memory & Summarisation Scaffold *(2025‑07‑08)*

* **`memory/backends/in_memory_backend.py`** – volatile list‑based store.
* Memory toggle (`settings.json → memory.backend`).
* `prepare_context()` merges persisted turns with live chat.
* **Summarisation scaffold** – `summariser.py` placeholder + experiments.
* **PyTest** smoke suite (`tests/test_memory_basic.py`).

---

### v0.4.4 – Persistent Memory *(2025‑07‑30)*

* **Redis and SQLite memory backends**
* Auto-fallback chain (persistent → volatile)
* Backend selection in `settings.json`
* Complete persistence tests
* Updated `SETUP.md`, `README.md`, and developer docs

---

### v0.4.5 – Summarisation MVP & Technical Spec *(2025‑08‑15)*

* **Summarisation trigger logic**: formal technical spec in `/docs/Technical_Specification_Summarisation_Trigger_Logic.md`
* **Threshold-based summarisation**: summarise when token/turn limits are reached  
* **Summary block insertion**: old turns replaced by generated summary with proper formatting
* **Minimum user turns logic**: prevents meaningless summaries from short conversations (MIN_USER_TURNS=3)
* **Bug fixes**: resolved test failures and summary injection mechanics
  - Fixed summary role formatting (summary vs user role)
  - Fixed context building with direct summary content insertion
  - Fixed token trimming logic to preserve summary blocks
* **Unit tests**: coverage for summarisation triggers and edge cases
* **Test isolation**: improved fixtures to prevent test contamination  
* **Planning doc updates**: scope, README, design docs all refreshed

---

## v0.5.x Track – CI/CD Infrastructure & Automation

### v0.5.0 – Multi-Environment CI Matrix *(2025‑11‑03)*

**Headline**: Comprehensive CI/CD implementation with multi-platform testing, containerization, and automated validation.

#### Multi-Platform Testing
* **GitHub Actions workflow** (`.github/workflows/ci.yml`) with OS matrix:
  - **Ubuntu Linux** (ubuntu-latest)
  - **macOS** (macos-latest)
  - **Windows** (windows-latest)
* **Python version matrix**: 3.10 and 3.11
* **6 parallel test jobs**: 3 OS × 2 Python versions
* **Quality checks**: Ruff (lint + format), mypy, Pyright type checking
* **Test artifacts**: JUnit XML, coverage reports, debug logs

#### Python 3.10/3.11 Compatibility
* **Conditional imports** for `typing.override` decorator:
  - Import from `typing` on Python 3.12+
  - Import from `typing_extensions` on Python 3.10/3.11
* **Files updated**:
  - `memory/backends/sqlite_memory_backend.py`
  - `memory/backends/redis_memory_backend.py`
* **Dependencies added**: `typing-extensions>=4.8.0` to `requirements-dev.txt`

#### Cross-Platform Fixes
* **Case-sensitivity fix**: Renamed `utils/Prompt_utils.py` → `utils/prompt_utils.py`
  - Resolved `ModuleNotFoundError` on Linux (case-sensitive filesystem)
  - Windows and macOS were unaffected (case-insensitive)
* **Windows test handling**: Documented and skipped SQLite tests with known timing issues:
  - `test_migrate_in-memory_sqlite_script.py` - subprocess execution
  - `test_sqlite_bckend.py::test_fallback_on_unwritable` - permission handling
  - `test_sqlite_bckend.py::test_roundtrip_default` - timing issues
  - `test_sqlite_bckend.py::test_trim_oldest` - timing issues

#### Container Build Pipeline
* **Docker/Podman image builds** on Linux runners
* **Container validation**: Automated startup tests
* **Layer caching**: GitHub Actions cache for faster rebuilds
* **Build artifacts**: Container logs for debugging

#### Documentation
* **Created `docs/CI.md`**: Comprehensive CI/CD documentation
  - Workflow triggers and jobs
  - Caching strategies
  - Troubleshooting guide
  - Platform-specific handling
* **Updated `docs/CONTAINER.md`**: Container setup and usage
* **Updated `README.md`**: CI badge and quick-start instructions

---

### v0.5.1 – GHCR Publishing & In-Container Testing *(2025‑11‑03)*

**Headline**: Automated container publishing to GitHub Container Registry with in-container test execution and coverage reporting.

#### Container Publishing to GHCR
* **Automated publishing** on `main` branch pushes and version tags
* **Registry**: `ghcr.io/deim0s13/llm-assistant`
* **Multi-architecture builds**: `linux/amd64` and `linux/arm64`
* **Smart tagging strategy**:
  - `latest` - Latest main branch build
  - Semantic versions - `1.2.3`, `1.2`, `1` for release tags
  - Commit SHAs - `sha-8a88e19` for traceability
* **Metadata action**: Automated tag and label generation
* **Permissions**: Proper GITHUB_TOKEN permissions for package publishing

#### Disk Space Optimization
* **GitHub Actions cleanup**: Pre-build removal of unnecessary software
  ```bash
  sudo rm -rf /usr/share/dotnet /usr/local/lib/android /opt/ghc
  sudo docker image prune --all --force
  ```
  - Freed ~15GB of disk space
* **CPU-only PyTorch**: Reduced image size by ~4GB (50% reduction)
  ```dockerfile
  RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
  ```
  - Final image size: ~4GB (down from ~8GB)

#### In-Container Test Execution
* **Full pytest suite** runs inside built container image
* **Test dependencies**: Runtime installation of `pytest-cov` and `fakeredis`
  - Keeps production image lean
  - Ensures test dependencies available for CI
* **Coverage reporting**: 
  - JUnit XML for test results
  - Cobertura XML for coverage analysis
* **Artifacts**: 30-day retention for test results and coverage
* **Container-specific handling**:
  - Skip `test_prepare_context_summary.py` - test isolation issues
  - Skip `test_sqlite_bckend.py::test_fallback_on_unwritable` - permission handling

#### Build Summary Output
* **GitHub Actions summary**: Formatted output with published tags
* **Pull commands**: Auto-generated for easy copy-paste
* **Traceability**: Commit SHA and metadata in image labels

#### Documentation Updates
* **`docs/CONTAINER.md`**: Prioritized GHCR over local builds
  - Pull and run instructions
  - Environment variables
  - Redis integration examples
* **`docs/CI.md`**: Updated with GHCR publishing details
  - Tagging strategy table
  - In-container testing section
  - Artifact descriptions
* **`README.md`**: Added GHCR quick-start
  ```bash
  docker pull ghcr.io/deim0s13/llm-assistant:latest
  docker run --rm -p 7860:7860 ghcr.io/deim0s13/llm-assistant:latest
  ```

#### CI Pipeline Enhancements
* **Job dependencies**: Proper ordering with `needs` keyword
* **Aggregated status**: `ci-success` job for branch protection
* **Fail-fast disabled**: All OS matrix jobs run to completion
* **PowerShell compatibility**: Fixed multi-line commands for Windows

---

## Upcoming Roadmap

### v0.5.2 – Model Upgrade & Configuration

* Model upgrade from FLAN-T5 to Mistral 7B
* Enhanced configuration management
* Model switching capabilities

### v0.5.2 – Prompt & Response Quality

* Base prompt improvements
* Structured output capabilities
* Response quality enhancements

### v0.5.3 – CI Enhancements

* Coverage thresholds implementation
* Artefact uploads and management
* Advanced CI pipeline features

### v0.5.4 – Container Publishing

* Podman build automation
* GitHub Container Registry integration
* Docker Hub publishing

### v0.5.5 – Evaluation & Model Comparison

* Consolidated evaluation harness
* Prompt quality assessment
* Model comparison framework

### v0.6.x – RAG Prototype

* File embedding + retrieval ("Ask my PDF" flow)
* Vector database integration
* Document Q&A capabilities

### v0.7.x – Fine-tuning Foundation

* LoRA/QLoRA scripts
* Weights & Biases integration
* Fine-tuning pipeline setup

---

Stay tuned — each milestone will be appended here upon completion. 🚀

---

## Additional Documentation

For detailed information about recent maintenance work and current status, see:
- **[CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md)** - Comprehensive documentation of recent linting remediation and improvements
- **[CURRENT_STATUS.md](./CURRENT_STATUS.md)** - Current project status and next steps
