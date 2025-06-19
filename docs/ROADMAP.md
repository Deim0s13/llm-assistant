# LLM Chatbot Project — Learning & Delivery Roadmap

This living roadmap combines the original learning journey with the current
GitHub-Projects release cadence. Each version milestone is tracked as a
GitHub Milestone and reflected on the project board.

---

## Learning Phases & Goals

### Phase 1 — Basic LLM-Powered Chatbot  *(v0.1 → v0.4.x)*  ✅ *Under way*

**Stack**

* Python 3.10+  |  Hugging Face Transformers
* Gradio UI
* (optional) FAISS / Chroma for RAG prototyping

**Core Goals**

| Status | Item |
|----|------|
| ✅ | Load & run pre-trained models (FLAN-T5, Mistral-7B) |
| ✅ | Gradio chat UI with multi-turn history |
| ✅ | Externalise prompts, specialised prompt matching |
| ✅ | Add safety guard-rails (strict / moderate / relaxed) |
| 🟡 | **Stretch** – add RAG file-based Q&A |
| 🟡 | **Stretch** – containerise with Podman / Docker |

---

### Phase 2 — Fine-Tuning Your Own Model  *(planned: v0.6.x → v0.7.x)*

* Hugging Face Datasets + LoRA / QLoRA
* Run locally or on OpenShift AI
* Weights & Biases for experiment tracking

Goals → build a small niche dataset, fine-tune TinyLLaMA or Mistral-7B, and
compare against the base model.

---

### Phase 3 — Packaging, Scaling, Integration  *(v0.8.x → v1.0.0)*

* Podman / OpenShift deployment
* Persistent memory back-end (Redis / SQLite / Vector DB)
* API or Slack / Telegram bot integration
* Observability (token counts, latency metrics)

---

## Delivery Milestones by Version

| Version | Focus Area (Epic)                               | Status |
|---------|-------------------------------------------------|--------|
| **v0.1.0** | Minimal static chatbot (single prompt)         | ✅ Done |
| **v0.2.0 – 0.2.5** | Multi-turn memory, specialised prompts, UI polish | ✅ Done |
| **v0.3.0** | Structured experiments & diagnostics panel     | ✅ Done |
| **v0.4.0** | Alias-driven prompt matching                   | ✅ Done |
| **v0.4.1** | Safety guard-rails & post-filtering            | ✅ Done |
| **v0.4.2** | Context trimming & debug logging               | ✅ Done |
| **v0.4.3** | *Current* – In-memory backend + summarise scaffold | 🔄 In Progress |
| **v0.4.4** | **Persistent memory (Redis/SQLite) + Summarise-MVP** | 🔜 Planned |
| **v0.4.5** | Evaluation harness & expanded guard-rails      | 🔜 Planned |
| **v0.5.0** | Containerisation & CI pipeline (Podman / OpenShift) | 🔜 Planned |
| **v0.6.x** | RAG prototype (file-based Q&A)                 | 🔜 Planned |
| **v0.7.x** | Fine-tuning foundation setup                   | 🔜 Planned |

*(milestone titles match what will be created in GitHub → feel free to rename)*

---

## Learning Outcomes Along the Way

* Prompt design & token-budget management
* Transformer architecture basics (encoder/decoder, LoRA adapters)
* Practical debugging of model behaviour & safety filters
* Building memory layers and context summarisation
* Experiment tracking, CI, and deployment practices
* Serving LLMs as modular, testable services

---

## Related Docs

* [`README.md`](../README.md) — high-level project overview
* [`docs/release_notes.md`](./release_notes.md) — full changelog
* [`docs/experiments_tracker.md`](./experiments_tracker.md) — test logs per version
* [`docs/scope.md`](./scope.md) — feature scope & cut-lines
* [`docs/contributing.md`](./contributing.md) — workflow & branch naming

> *Remember: this document is expected to evolve every cycle.
> Keep the **Version table** and **Learning Phases** in sync with the Project board for zero-surprises planning.*
