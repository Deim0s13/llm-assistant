# LLM‑Assistant Project — Scope & Roadmap 📑

*Last updated: **v0.4.4** (Redis‑backed memory + CI scaffold)*

This document couples the **learning journey** with the **delivery roadmap** so anyone can see **why** we ship a feature, **what** is in‑scope, and **how** each piece maps to GitHub Milestones.

---

## 1 Learning Phases & Goals

| Phase | Version Range | Theme                          | Key Take‑away                                                    |
| ----- | ------------- | ------------------------------ | ---------------------------------------------------------------- |
| **1** | v0.1 → v0.4.x | *Baseline LLM‑powered chatbot* | Prompt engineering, safety, memory, summarisation                |
| **2** | v0.5 → v0.7.x | *Fine‑tuning playground*       | Collect data, LoRA/QLoRA tuning, evaluation harness              |
| **3** | v0.8 → v1.0   | *Packaging & scaling*          | Container images, persistent semantic memory, RAG & integrations |

---

## 2 Version Milestones

| Version           | Focus / Epic                                            | Status           |
| ----------------- | ------------------------------------------------------- | ---------------- |
| **0.1.0**         | Minimal static chatbot                                  | ✅ Done           |
| **0.2.0 – 0.2.5** | Multi‑turn context, UI sliders, specialised prompts     | ✅ Done           |
| **0.3.0**         | Experiments framework & diagnostics                     | ✅ Done           |
| **0.4.0**         | Alias‑driven prompt matching                            | ✅ Done           |
| **0.4.1**         | Safety guardrails (strict / moderate / relaxed)         | ✅ Done           |
| **0.4.2**         | Context trimming & debug logging                        | ✅ Done           |
| **0.4.3**         | Volatile **In‑memory backend** + summarisation scaffold | ✅ Done           |
| **0.4.4**         | **Persistent memory (Redis) + Summarise MVP + CI**      | 🔄 *In Progress* |
| **0.4.5**         | Vector memory & evaluation harness                      | 🔜 Planned       |
| **0.5.0**         | Containerisation & full CI matrix                       | 🔜 Planned       |
| **0.6.x**         | RAG prototype (file‑based Q\&A)                         | 🔜 Planned       |
| **0.7.x**         | Fine‑tuning foundation                                  | 🔜 Planned       |

> **Sync note:** Milestone names mirror the GitHub Project board.

---

## 3 Completed Highlights (≤ v0.4.3)

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

* Profanity filter (strict | moderate | relaxed).
* Configurable refusal template.

### v0.4.2 — Context Hygiene

* Turn‑count + token‑budget trimming.
* `.env` overrides; GitHub Projects migration.

### v0.4.3 — Volatile Memory & Summaries

* **`memory/backends/in_memory_backend.py`** default store.
* Memory toggle in `settings.json`.
* Summarisation function stub + initial unit tests.

---

## 4 Current Cycle — **v0.4.4**  🔧📝🧪

| Track         | Deliverable                                                                  | Status                 |
| ------------- | ---------------------------------------------------------------------------- | ---------------------- |
| **Memory**    | **`memory/backends/redis_memory_backend.py`** – LPUSH/LRANGE + auto‑fallback | ✅ Code drafted         |
|               | `settings.json → memory.backend = "redis"` & env `REDIS_URL`                 | ✅                      |
| **Summaries** | `summariser.py::summarise_context()` MVP (real LLM call)                     | 🟡 coding              |
| **Dev Ops**   | GitHub Actions – Ruff → PyTest → Podman build                                | 🟡 workflow\.yml draft |
| **Tests**     | *fakeredis* fixture; memory stress & fallback tests                          | 🟡                     |
| **Docs**      | Updated README, Release Notes, Scope (this file)                             | ✅                      |

*Success criteria*
✔ Chat persists turns across restarts when Redis is up.
✔ Falls back transparently when Redis is down (no crashes).
✔ CI passes Ruff + PyTest on `dev` & `main` branches.
✔ Summarisation trims token use ≥ 30 % in long chats (manual spot‑check).

---

## 5 Upcoming Roadmap

1. **v0.4.5 — Vector Memory & Evaluation Harness**

   * Vector DB (FAISS / Qdrant) backend.
   * Prompt‑regression corpus & JSON expectations.
   * Scoring dashboard (pass/fail diff).

2. **v0.5.0 — Container & Full CI**

   * Podman image (GPU + CPU), multi‑arch.
   * Matrix tests: Mac M‑series, Linux CUDA.

3. **v0.6.x — RAG Prototype**

   * File embedding + retrieval – “Ask my PDF.”

4. **v0.7.x — Fine‑tuning Playground**

   * LoRA/QLoRA scripts, W\&B integration.

---

## 6 Key Config Flags

| Key                         | Since | Notes                                |
| --------------------------- | ----- | ------------------------------------ |
| `memory.enabled`            | 0.4.3 | Master toggle (bool)                 |
| `memory.backend`            | 0.4.3 | `"in_memory"` / `"redis"` / `"none"` |
| `REDIS_URL` (env)           | 0.4.4 | `redis://[:password]@host:port/db`   |
| `context.max_history_turns` | 0.2.0 | Pre‑memory live turn cap             |
| `context.max_prompt_tokens` | 0.2.0 | Hard prompt budget                   |

All can be overridden in `.env` (see README).

---

## 7 Process Recap

1. **Issue** ↔ Epic ↔ Milestone created on GitHub Projects.
2. Scoped here in `scope.md`.
3. Feature branch → PR → `dev` → squash merge.
4. Release tag → `release_notes.md` update.

> *Keep this file in sync with planning sessions to avoid “doc drift.”* 🚀
