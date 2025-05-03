# LLM Chatbot Project Roadmap

This document outlines the learning roadmap and development trajectory for the LLM-powered chatbot project. It reflects our original goals and breaks down progress into practical, version-aligned milestones.

---

## Learning Phases & Goals

### Phase 1: Basic LLM-Powered Chatbot (In Progress)

**Tech Stack:**

* Python
* Hugging Face Transformers
* Gradio UI
* (Optional) FAISS/Chroma for RAG

**Goals:**

* ✅ Load and run pre-trained models (e.g., FLAN-T5, Mistral)
* ✅ Build basic chat interface with history
* ✅ Externalise prompts and structure code
* ✅ Learn prompt structure, token limits

**Stretch Goals:**

* 🟡 Add RAG capabilities for document Q\&A
* 🟡 Containerize using Podman or Docker

---

### Phase 2: Fine-Tuning Your Own Model (Upcoming)

**Tools:**

* Hugging Face Transformers + Datasets
* LoRA / QLoRA
* Red Hat OpenShift AI or local GPU (if available)
* Weights & Biases or TensorBoard for tracking

**Goals:**

* Collect or build a small dataset (e.g., FAQs, dialogues)
* Fine-tune a small model (TinyLLaMA, Mistral 7B)
* Evaluate and compare with base model outputs
* Save/load and deploy the fine-tuned model

---

### Phase 3: Packaging, Scaling, Integration (Planned)

**Focus Areas:**

* Build a containerised version with Podman
* Deploy to OpenShift Local or OpenShift AI
* Add persistent memory and context management
* Integrate with tools like Slack, Telegram, or APIs

---

## Feature Milestones by Version

| Version       | Focus Area                                  | Status     |
| ------------- | ------------------------------------------- | ---------- |
| v0.1.0        | Basic static chatbot with base prompt       | Done     |
| v0.2.0–v0.2.5 | Multi-turn memory, specialized prompts, UI  | Done     |
| v0.3.0        | Structured experiments, diagnostics         | Done     |
| v0.4.0        | Improved prompt matching and alias logic    | Done     |
| v0.4.1        | Safety guardrails (post-filtering, refusal) | Planned |
| v0.4.2        | Context memory chaining improvements        | Planned |
| v0.5.0        | Podman containerisation                     | Planned |
| v0.6.x        | RAG prototype (basic file-based Q\&A)       | Planned |
| v0.7.x        | Fine-tuning foundation setup                | Planned |

---

## Learning Outcomes Along the Way

* Tokenization, prompt engineering, and token limits
* Transformer architecture basics (encoders, decoders)
* Practical debugging of model behaviour
* Prompt design, chaining, and user conditioning
* Fine-tuning flow using LoRA/QLoRA
* Experiment tracking and structured development practices
* Serving models and building AI tools (not just apps)

---

## Related Documents

* [`README.md`](./README.md)
* [`release_notes.md`](./release_notes.md)
* [`experiments_tracker.md`](./experiments_tracker.md)
* [`scope.md`](./scope.md)
* [`contributing.md`](./contributing.md)

---

> This roadmap is a living document. Each milestone will be updated as progress continues and priorities evolve.
