# Contributing Guidelines 🤝

Welcome, and thank you for your interest in helping out!
This document explains **how we plan, branch, commit, and review code** so collaboration stays smooth and traceable.

---

## 1 · Project Purpose & Scope

This repo started as a hands-on LLM sandbox and has grown into a **modular, roadmap-driven platform** for prompt engineering, memory, summarisation, and more.
We value:

* 🎯 **Structured learning** – every feature ties to a doc & test
* 📊 **Traceability** – GitHub Projects for planning, Issues for tasks
* 🔍 **Experimentation** – dedicated `/experiments/` and markdown logs

Contributions that embrace these principles are especially welcome!

---

## 2 · Planning & Tracking

We use the GitHub **LLM Project Board** → https://github.com/users/Deim0s13/projects/4

| Level        | Example                              | Rule                                             |
|--------------|--------------------------------------|--------------------------------------------------|
| Initiative   | *AI-Powered Knowledge Assistant*     | Broad, multi-release theme                       |
| Epic         | *Memory Integration*                 | Group of related milestones/tasks                |
| Milestone    | `v0.4.3`                             | Target release version                           |
| Issue / PR   | `Task: Inject Memory`                | Single piece of work – **every change has one**  |

> In your PR description use **`fixes #123`** (or `closes`) so the Issue auto-closes when merged.

---

## 3 · Branch Strategy

* **`main`** — always deployable, tagged releases only
* **`dev`**  — rolling integration of finished features
* **`feature/*`**, **`bugfix/*`**, **`docs/*`** — work branches off `dev`

Example:

    # create a new feature branch
    git checkout dev
    git pull
    git switch -c feature/v0.4.4-rag-prototype

Always re-base onto `dev` if you fall behind; avoid merging `main` into feature branches.

---

## 4 · Branch Naming

`<type>/v<major.minor.patch>-<slug>`

* `feature/v0.4.3-memory-pipeline`
* `bugfix/v0.4.2-safety-regex`
* `docs/v0.4.4-testing-guide`

Lower-case, hyphen-separated, concise.

---

## 5 · Commit Messaging

Short + present tense. Conventional-Commit style is optional but welcome.

* `feat: add summarise_context scaffold`
* `fix: handle empty memory load`
* `docs: refresh contributing guide`

---

## 6 · Pull Requests

* **Target** `dev`
* **Reference** an Issue (`fixes #42`)
* **Describe** the what & why (1-2 sentences)
* **Pass** all tests / linters before merge

---

## 7 · Environment & Setup

* Copy `.env.example` ➜ `.env` for local overrides (never commit creds)
* Platform steps live in **`docs/cross-platform-dev-checklist.md`**
* Extra setup notes live in `SETUP.md`

> macOS M-series uses **`mps`** automatically.
> Windows + NVIDIA uses CUDA wheels (see checklist).

---

## 8 · Local Dev Requirements

* Python 3.10+
* `pip install -r requirements.txt`
* Run `ruff check .` (lint) before PR (optional but appreciated)

---

## 9 · Automated Tests (coming in v0.5.0)

The **“Automated Testing & CI”** epic will introduce:

* PyTest suites for context trimming & memory
* GitHub Actions workflow (`lint → test → build`)
* Coverage badge in the README

Want to help? Open an Issue!

---

## 10 · Key Directories

| Path / File                 | Purpose                                           |
|-----------------------------|---------------------------------------------------|
| `main.py`                   | Gradio entry point & prompt pipeline              |
| `utils/memory.py`           | In-process memory backend (plug-in ready)         |
| `utils/`                    | Prompt utils, safety filters, alias loader        |
| `config/`                   | Prompts, settings.json, aliases                   |
| `experiments/`              | **Exploratory scripts & prototypes** – one-off research, development utilities, playgrounds |
| `tests/`                    | **Automated test suite** – pytest unit & integration tests, CI-ready |
| `docs/`                     | Roadmap, scope, dev checklist, release notes      |

### Testing vs Experimentation

**Two distinct approaches for quality assurance:**

| Directory | Purpose | When to Use |
|-----------|---------|-------------|
| **`tests/`** | Automated testing, CI/CD, regression prevention | Unit tests, integration tests, functionality validation |
| **`experiments/`** | Manual exploration, prototyping, research | One-off scripts, development utilities, proof-of-concepts |

**Examples:**
- `tests/test_summariser.py` → Automated unit tests for summarisation logic
- `experiments/summarisation_playground.py` → Manual exploration of summarisation approaches
- `tests/test_memory_parity.py` → Automated backend compatibility testing  
- `experiments/memory_test_utils.py` → Development utilities for manual testing

---

### Quick Links

* **Project Board** – https://github.com/users/Deim0s13/projects/4
* **Roadmap** – `docs/roadmap.md`
* **Scope** – `docs/scope.md`
* **Release Notes** – `docs/release_notes.md`
* **Experiments Tracker** – `docs/experiments_tracker.md`
* **Cross-Platform Dev Checklist** – `docs/cross-platform-dev-checklist.md`

---

Thanks again for contributing! Your PRs help push this exploration of LLM tooling forward 🚀
