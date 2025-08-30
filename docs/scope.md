# LLM‑Assistant Project — Scope & Roadmap 📑

*Last updated: **v0.4.5** (Persistent Memory + Summarisation MVP)*

This document couples the **learning journey** with the **delivery roadmap** so anyone can see **why** we ship a feature, **what** is in‑scope, and **how** each piece maps to GitHub Milestones.

---

## 1 Learning Phases & Goals

| Phase | Version Range      | Theme                    | Key Take-away                           |
|-------|--------------------|--------------------------|-----------------------------------------|
| **1** | v0.1 → v0.4.x      | *Basic LLM-powered chatbot* | Core chat loop, prompt engineering, safety, memory, summarisation |
| **2** | v0.6.x → v0.7.x    | *Fine-tuning playground* | Collect data, apply LoRA/QLoRA, compare results |
| **3** | v0.8.x → v1.0.0    | *Packaging & scaling*    | Container images, persistent memory, integrations |

---

## 2 Version Milestones

| Version           | Focus / Epic                                             | Status         |
|-------------------|---------------------------------------------------------|----------------|
| **0.1.0**         | Minimal static chatbot                                  | ✅ Done        |
| **0.2.0 → 0.2.5** | Multi-turn context, UI sliders, specialised prompts     | ✅ Done        |
| **0.3.0**         | Experiments framework & diagnostics panel               | ✅ Done        |
| **0.4.0**         | Alias-driven prompt matching                            | ✅ Done        |
| **0.4.1**         | Safety guardrails (strict / moderate / relaxed)         | ✅ Done        |
| **0.4.2**         | Context trimming & debug logging                        | ✅ Done        |
| **0.4.3**         | In-memory backend + summarisation scaffold              | ✅ Done        |
| **0.4.4**         | **Persistent memory (Redis/SQLite)**                    | ✅ Done        |
| **0.4.5**         | **Summarisation MVP + Technical Spec + Planning**       | 🔄 In Progress |
| **0.5.0**         | Containerisation & full CI matrix                       | 🔜 Planned     |
| **0.5.1**         | Model upgrade (FLAN → Mistral 7B) + config toggle      | 🔜 Planned     |
| **0.5.2**         | Prompt/response quality improvements & structured outputs | 🔜 Planned     |
| **0.5.3**         | CI enhancements: coverage thresholds, artefact uploads  | 🔜 Planned     |
| **0.5.4**         | Container publishing (Podman build → GHCR/DockerHub)    | 🔜 Planned     |
| **0.5.5**         | Consolidated evaluation harness & model comparison     | 🔜 Planned     |
| **0.6.x**         | RAG prototype (file-based Q&A)                          | 🔜 Planned     |
| **0.7.x**         | Fine-tuning foundation                                  | 🔜 Planned     |

> **Sync note:** Milestone names mirror the GitHub Project board.

---

## 3 Completed Highlights (≤ v0.4.3)

### v0.2.x — Core Features

* Multi‑turn history, external base prompt, generation controls.
* Early specialised prompt injection & alias diagnostics.

### v0.3.0 — Experiments Framework
* `/experiments/` notebooks & logs.
* Findings informed alias & safety designs.

### v0.4.0 — Alias Overhaul
* Token‑level multi‑word alias detection.
* Expanded `prompt_aliases.json`; richer debug logs.

### v0.4.1 — Safety Guardrails
* Profanity filter (strict | moderate | relaxed).
* Configurable refusal template.

### v0.4.2 — Context Hygiene
* Turn‑count + token‑budget trimming.
* `.env` overrides; GitHub Projects migration.

### v0.4.3 — Volatile Memory & Summarisation Scaffold
* **`memory/backends/in_memory_backend.py`** default store.
* Memory toggle in `settings.json`.
* Summarisation function stub + initial unit tests.

---

## 4 Current Cycle — **v0.4.5**  📝🧪

| Track         | Deliverable                                                  | Status         |
|---------------|-------------------------------------------------------------|----------------|
| **Summaries** | Summarisation MVP: trigger logic, insertion, config, docs   | 🔄 In Progress |
|               | Technical specification in `/docs/summarisation_trigger_logic.md` | 🔄             |
|               | Unit tests: summary insertion & regression                   | 🔄             |
| **Docs**      | Planning doc, scope, and README updated                      | 🔄             |

*Success criteria*
✔ Summarisation triggers and compresses history when token/turn limits are reached
✔ Control flow, insertion, and config options documented and tested
✔ Spec and code reviewed, linked to planning docs

---

## 5 Upcoming Roadmap

1. **v0.5.0 — Containerisation & Full CI Matrix**
   * Containerisation with Podman/Docker
   * Full CI matrix and automated testing
   * Deployment pipeline setup

2. **v0.5.1 — Model Upgrade & Configuration**
   * Model upgrade from FLAN-T5 to Mistral 7B
   * Enhanced configuration management
   * Model switching capabilities

3. **v0.5.2 — Prompt & Response Quality**
   * Base prompt improvements
   * Structured output capabilities
   * Response quality enhancements

4. **v0.5.3 — CI Enhancements**
   * Coverage thresholds implementation
   * Artefact uploads and management
   * Advanced CI pipeline features

5. **v0.5.4 — Container Publishing**
   * Podman build automation
   * GitHub Container Registry integration
   * Docker Hub publishing

6. **v0.5.5 — Evaluation & Model Comparison**
   * Consolidated evaluation harness
   * Prompt quality assessment
   * Model comparison framework

7. **v0.6.x — RAG Prototype**
   * File embedding + retrieval "Ask my PDF" flow
   * Vector database integration
   * Document Q&A capabilities

8. **v0.7.x — Fine-tuning Foundation**
   * LoRA/QLoRA scripts
   * Weights & Biases integration
   * Fine-tuning pipeline setup

---

## 6 Key Config Flags

| Key                         | Since | Notes                                          |
|-----------------------------|-------|------------------------------------------------|
| `memory.enabled`            | 0.4.3 | Master toggle (bool)                           |
| `memory.backend`            | 0.4.4 | `"in_memory"`, `"redis"`, `"sqlite"`, `"none"` |
| `summarisation.enabled`     | 0.4.5 | Turn summarisation on/off                      |
| `summarisation.strategy`    | 0.4.5 | `"heuristic"`, `"llm"`, `"none"`               |
| `summarisation.token_threshold` | 0.4.5 | Max prompt token length for summary trigger    |
| `summarisation.turn_threshold`  | 0.4.5 | Max turn count before summary trigger          |
| `context.max_history_turns` | 0.2.0 | Pre-memory live turn cap                       |
| `context.max_prompt_tokens` | 0.2.0 | Hard prompt budget                             |

All can be overridden in `.env` (see README).

---

## 7 Process Recap

1. **Issue** ↔ Epic ↔ Milestone created on GitHub Projects.
2. Scoped here in `scope.md`.
3. Feature branch → PR → `dev` → squash merge.
4. Release tag → `release_notes.md` update.

> *Keep this file in sync with planning sessions to avoid "doc drift."* 🚀
