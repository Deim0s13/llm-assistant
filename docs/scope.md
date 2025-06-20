# Project Scope & Planning Overview 📑

A living document outlining **what** each version of the LLM-Chatbot Starter Kit sets out to achieve — and **why**.

It keeps development aligned with the project’s dual purpose:

1. **Hands-on learning** about LLM behaviour, prompt design, safety & memory techniques.
2. **Modular, production-minded engineering** that can grow into a full assistant stack.

---

## Why keep a formal scope file?

* Record the *vision* behind every feature, not just its code.
* Show the **goal / out-of-scope / success-criteria** for each release.
* Provide quick context when deciding whether a new idea belongs *now* or in a future milestone.
* Tie learning-oriented experiments back to concrete deliverables.

It complements:

* **[`README.md`](../README.md)** – *current* status & quick-start.
* **[`release_notes.md`](./release_notes.md)** – granular changelog.
* **GitHub Projects board** – day-to-day issue tracking.

---

## Completed Versions

### v0.2.x – Core Feature Set 🎯

| Sub-ver | Focus                                       | Key Points |
|---------|---------------------------------------------|------------|
| 0.2.0   | Multi-turn history, sliders, external base prompt | Context window; generation controls |
| 0.2.1   | Specialised prompts & file loading polish   | Expanded prompt library |
| 0.2.2   | **Model upgrade** `flan-t5-base`            | Better comprehension |
| 0.2.3   | Alias diagnostics                           | Prompt-source display |
| 0.2.4   | Dev Playground, fuzzy matching              | Auto-preview toggle |
| 0.2.5   | Naming & UI polish                          | Fuzzy-score logging |

#### Success Snapshot
* Reliable specialised prompt injection.
* Clear debug trail of prompt selection & generation parameters.

---

### v0.3.0 – Experiments Framework 🔬

* Added `/experiments/` markdown logs.
* Ran systematic tests on prompt phrasing, decoding, safety toggles.
* Findings influenced later alias & safety design.

---

### v0.4.0 – Alias Matching Overhaul 🧩

* Token-level multi-word alias detection.
* Expanded `prompt_aliases.json`.
* Richer “[Prompt] …” logs with fallback reasoning.

---

### v0.4.1 – Safety Guardrails 🛡️ **(Done)**

* `settings.json → safety` section (`strict|moderate|relaxed`).
* Profanity filter & configurable refusal template.
* Logged rule triggers; tests recorded in experiments.

---

### v0.4.2 – Context Window & Dev Hygiene 🧹 **(Done)**

* **Turn-limit + token-limit trimming** with debug counts.
* Auto device-select (CUDA ▸ MPS ▸ CPU).
* `.env` overrides; `python-dotenv` bootstrap.
* Migration to **GitHub Projects** board; `README` & `CONTRIBUTING` rewritten.

---

## Active Development

### v0.4.3 – Memory Backend & Summarisation Scaffold 🗄️ **(In Progress)**

| Track | Deliverable | Status |
|-------|-------------|--------|
| Memory | `utils/memory.py` singleton (`IN_MEMORY` / `NONE`) | ✅ Impl |
| Config | `settings.json → memory.enabled/backend`           | ✅ Impl |
| Context | `prepare_context()` merges *memory* + live history | ✅ Impl |
| Logging | `[Memory]` startup status, load/save counts        | ✅ Impl |
| Tests | Scripts for memory *on/off* behaviour                | 🔄 Draft |
| Summarisation | `summarise_context()` placeholder + design notes | 🔄 Draft |
| Docs | Scope/README updated; dev checklist cross-links       | 🔄 Pending |

**Success criteria**

* Chat runs identically with memory *enabled* or *disabled*.
* Debug logs show memory injection counts.
* Future persistent back-ends can drop in via `MemoryBackend` Enum.

---

## Planned / Upcoming

### v0.4.4 – Automated Tests & CI ✅

* **PyTest** suite for context, memory, safety filters.
* **ruff** lint + **pytest** GitHub Action.
* Coverage badge & fail-fast on PRs.

### v0.5.x – Containerisation & RAG Prototype 📦

* Podman / Docker image (CPU + GPU variants).
* Minimal **RAG** pipeline (file embeddings + retrieval).
* Deployment script for OpenShift Local.

### v0.6.x – Fine-Tuning Playground 🎛️

* LoRA / QLoRA notebook.
* W&B (or MLflow) experiment tracking.
* Compare fine-tuned vs base responses inside playground.

---

## Out-of-Scope (for now)

* Full multi-user session management.
* Third-party moderation APIs.
* Production-grade vector DB integration.
* Real-time websocket streaming.

---

## Living Process

1. Proposal → **Issue** (linked to Epic & Milestone).
2. Scoped here in `scope.md`.
3. Implemented in feature branch → PR → `dev`.
4. On merge, Release Notes updated → milestone closed.

> *Scope evolves with each learning cycle. Check this file at every planning session.*
