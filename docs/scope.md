# LLM Chatbot Project — Scope & Roadmap 📑

*Last updated: **v0.4.5** (Persistent Memory + Summarisation MVP)*

This document unifies the **learning journey** and the **delivery roadmap** so everyone can see **why** each feature ships, **what** is in-scope for a release, and **how** it maps to GitHub Milestones.

---

## 1 Learning Phases & Goals

| Phase | Version Range      | Theme                    | Key Take-away                           |
|-------|--------------------|--------------------------|-----------------------------------------|
| **1** | v0.1 → v0.4.x      | *Basic LLM-powered chatbot* | Core chat loop, prompt engineering, safety, memory, summarisation |
| **2** | v0.6.x → v0.7.x    | *Fine-tuning playground* | Collect data, apply LoRA/QLoRA, compare results |
| **3** | v0.8.x → v1.0.0    | *Packaging & scaling*    | Container images, persistent memory, integrations |

---

## 2 Version Milestones

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
| **0.5.0**         | Automated Test Suite & CI Enablement (Podman/Actions)   | 🔜 Planned     |
| **0.5.1**         | Containerisation & E2E Test Matrix                      | 🔜 Planned     |
| **0.6.x**         | RAG prototype (file-based Q&A)                          | 🔜 Planned     |
| **0.7.x**         | Fine-tuning foundation                                  | 🔜 Planned     |

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

### v0.4.3 — Volatile Memory & Summarisation Scaffold
* In-memory backend and context builder injection.
* Summarisation function stub and playground.

### v0.4.4 — Persistent Memory
* Redis and SQLite memory backends, auto-fallback chain.
* `settings.json` → backend selection, full persistence tests.
* Updated `SETUP.md`, `README.md`, and developer docs.

---

## 4 Current Cycle — **v0.4.5**  📝🧪

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

## 5 Upcoming Roadmap

1. **v0.5.0 — Automated Test Suite & CI Enablement**
   * Full PyTest coverage for critical modules, typing checks.
   * GitHub Action: lint, test, coverage, branch protection.
   * Pre-commit hooks (optional).

2. **v0.5.1 — Containerisation & E2E Test Matrix**
   * Podman image, multi-arch builds, end-to-end test pipeline.

3. **v0.6.x — RAG Prototype**
   * File embedding + retrieval “Ask my PDF” flow.

4. **v0.7.x — Fine-tuning Playground**
   * LoRA/QLoRA scripts, W&B integration.

---

## 6 Key Config Flags

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

## 7 Process Recap

1. **Issue** ↔ Epic ↔ Milestone created on GitHub Projects.
2. Scoped here in `scope.md`.
3. Feature branch → PR → `dev` → squash merge.
4. Release tag → `release_notes.md` update.

> *Keep this file updated each planning session to avoid “doc drift”.* 🚀
