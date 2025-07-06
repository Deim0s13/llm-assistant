# LLM Chatbot Project — Scope & Roadmap 📑

*Last updated: **v0.4.3** (Memory façade + summarisation scaffold)*

This document unifies the **learning journey** and the **delivery roadmap** so everyone can see **why** each feature ships, **what** is in-scope for a release, and **how** it maps to GitHub Milestones.

---

## 1 Learning Phases & Goals

| Phase | Version Range | Theme | Key Take-away |
|-------|---------------|-------|--------------|
| **1** | v0.1 → v0.4.x | *Basic LLM-powered chatbot* | Core chat loop, prompt engineering, safety, memory |
| **2** | v0.6.x → v0.7.x | *Fine-tuning playground* | Collect data, apply LoRA/QLoRA, compare results |
| **3** | v0.8.x → v1.0.0 | *Packaging & scaling* | Container images, persistent memory, integrations |

---

## 2 Version Milestones

| Version | Focus / Epic | Status |
|---------|--------------|--------|
| **0.1.0** | Minimal static chatbot | ✅ Done |
| **0.2.0 → 0.2.5** | Multi-turn context, UI sliders, specialised prompts | ✅ Done |
| **0.3.0** | Experiments framework & diagnostics panel | ✅ Done |
| **0.4.0** | Alias-driven prompt matching | ✅ Done |
| **0.4.1** | Safety guardrails (strict / moderate / relaxed) | ✅ Done |
| **0.4.2** | Context trimming & debug logging | ✅ Done |
| **0.4.3** | In-memory backend + summarisation scaffold | 🔄 *In Progress* |
| **0.4.4** | **Persistent memory (Redis/SQLite) + Summarise MVP** | 🔜 Planned |
| **0.4.5** | Evaluation harness + expanded guardrails | 🔜 Planned |
| **0.5.0** | Containerisation & CI (Podman / OpenShift) | 🔜 Planned |
| **0.6.x** | RAG prototype (file-based Q&A) | 🔜 Planned |
| **0.7.x** | Fine-tuning foundation | 🔜 Planned |

> **Consistency check**: all milestone names match the GitHub Project board.

---

## 3 Completed Highlights

### v0.2.x — Core Features

* Multi-turn history, external base prompt, generation controls.
* Early specialised prompt injection & alias diagnostics.

### v0.3.0 — Experiments Framework

* `/experiments/` notebooks & logs.
* Findings fed into later alias and safety work.

### v0.4.0 — Alias Overhaul

* Token-level multi-word detection.
* Expanded `prompt_aliases.json`, richer debug logs.

### v0.4.1 — Safety Guardrails

* Profanity filter with strict | moderate | relaxed modes.
* Configurable refusal template.

### v0.4.2 — Context Hygiene

* Turn-count + token-budget trimming.
* `.env` overrides; GitHub Projects migration.

---

## 4 Current Cycle — **v0.4.3**  🗄️📝

| Track | Deliverable | Status |
|-------|-------------|--------|
| **Memory** | `utils/memory.py` singleton (`IN_MEMORY` / `NONE`) | ✅ |
| | `settings.json → memory.enabled / backend` | ✅ |
| | Context builder injects *Memory → Live* | ✅ |
| **Summaries** | `utils/summariser.py::summarise_context()` scaffold | ✅ |
| | Playground prototype (`experiments/summarisation_playground.py`) | ✅ |
| **Tests** | **First unit-test suite** → memory on/off, context trim | ✅ |
| | Smoke-script `scripts/activate_tests.sh` | ✅ |
| **Docs** | `summarisation_planning.md`, scope & README refresh | ✅ |

*Success criteria*
✔ All `pytest` tests pass in DEBUG and non-DEBUG modes.
✔ Chat behaves identically with memory **on or off**.
✔ Debug logs show `[Memory] injected / live / combined`.
✔ Summarisation entry-point ready for real logic in v0.4.4.

---

## 5 Upcoming Roadmap

1. **v0.4.4 — Persistent Memory + Summarise MVP + CI**
   * Redis / SQLite backend, nightly summary roll-ups.
   * **Expand PyTest coverage** → safety filters, summariser accuracy.
   * GitHub Action: `ruff`, `pytest`, coverage badge.

2. **v0.4.5 — Evaluation Harness & Guard-rail Edge-cases**
   * Structured prompt-regression corpus, JSON expectation files.
   * Scoring dashboard (pass/fail diff).

3. **v0.5.0 — Container & CI**
   * Podman image, multi-arch builds, end-to-end test matrix.

4. **v0.6.x — RAG Prototype**
   * File embedding + retrieval “Ask my PDF” flow.

5. **v0.7.x — Fine-tuning Playground**
   * LoRA/QLoRA scripts, W&B integration.

---

## 6 Key Config Flags

| Key | Since | Notes |
|-----|-------|-------|
| `memory.enabled` | 0.4.3 | Master toggle (bool) |
| `memory.backend` | 0.4.3 | `"in_memory"` / `"none"` → future `"redis"`, `"sqlite"` |
| `context.max_history_turns` | 0.2.0 | Pre-memory live turn cap |
| `context.max_prompt_tokens` | 0.2.0 | Hard prompt budget |

All can be overridden in `.env` (see README).

---

## 7 Process Recap

1. **Issue** ↔ Epic ↔ Milestone created on GitHub Projects.
2. Scoped here in `scope.md`.
3. Feature branch → PR → `dev` → squash merge.
4. Release tag → `release_notes.md` update.

> *Keep this file updated each planning session to avoid “doc drift”.* 🚀
