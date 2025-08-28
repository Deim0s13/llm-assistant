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
| **v0.5.0** | 🔼 *Planned* | Automated Test Suite & CI Enablement (Podman/Actions)         |
| **v0.5.1** | 🔼 *Planned* | Containerisation & E2E Test Matrix                           |
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

### v0.4.5 – Summarisation MVP & Technical Spec *(Completed)*

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

## Upcoming Roadmap

### v0.5.0 – Automated Test Suite & CI Enablement

* Full PyTest coverage for critical modules, typing checks
* GitHub Action: lint, test, coverage, branch protection
* Optional pre-commit hooks

### v0.5.1 – Containerisation & E2E Test Matrix

* Podman image, multi-arch builds, end-to-end test matrix

### v0.6.x – RAG Prototype

* File embedding + retrieval ("Ask my PDF" flow)

### v0.7.x – Fine-tuning Playground

* LoRA/QLoRA scripts, W&B integration

---

Stay tuned — each milestone will be appended here upon completion. 🚀
