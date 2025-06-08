# Contributing Guidelines

Welcome, and thank you for your interest in contributing to this project! This document outlines the standards and workflow we follow to keep things organised, traceable, and easy to collaborate on.

---

## Purpose

This project began as a hands-on exploration into large language models (LLMs) and has grown into a modular, roadmap-driven experimentation platform for prompt engineering, memory handling, summarisation, and more.

Contributions are welcome — especially those that align with our structured, learning-focused development model.

---

## How We Plan & Track Work

All work is tracked using GitHub Projects:
[LLM Project Board](https://github.com/users/Deim0s13/projects/4/views/1)

### Planning Hierarchy

- **Initiatives** – High-level goals (e.g. AI Assistant, Agent Simulator)
- **Epics** – Feature themes (e.g. Prompt Matching, Memory Integration)
- **Milestones** – Versioned releases (e.g. `v0.4.2`, `v0.4.3`)
- **Issues** – Individual trackable tasks

> Create **Issues** for all new work — no markdown-based planning.
> Link Issues to Epics and Milestones where appropriate.
> Use `fixes #issue_number` in PRs to auto-close issues on merge.

---

## Branching Strategy

We follow a stable → dev → feature model:

- **`main`** — Stable, production-ready code. Releases are tagged here.
- **`dev`** — Development integration branch for new features.
- **`feature/*`**, **`bugfix/*`**, **`docs/*`** — Work branches off `dev`.

### Always

- Branch **from `dev`**, not `main`
- Submit Pull Requests **to `dev`**
- Let CI/tests pass before merge
- Use issues and link them to PRs

---

## Branch Naming Convention

Use clear, versioned branch names to track changes.

**Format:**

```bash
[type]/v[major.minor.patch]-[short-description]
```

**Examples:**

- `feature/v0.4.2-context-trimming`
- `bugfix/v0.4.2-token-truncation`
- `docs/v0.4.3-memory-setup`

Use lowercase and hyphenate descriptive parts.

---

## Commit Guidelines

Use clear, short, present-tense commit messages.

Optionally follow [Conventional Commits](https://www.conventionalcommits.org/).

**Examples:**

- `feat: add summarise_context() scaffold`
- `fix: fallback to base prompt when alias fails`
- `docs: update scope.md for v0.4.3 planning`

---

## Pull Requests

Pull Requests should:

- Target the `dev` branch
- Reference an issue (e.g. `fixes #42`)
- Include a short description of what and why
- Pass all tests and linters

---

## Environment & Code Expectations

- Store machine-specific settings in a `.env` file (not committed)
- Use `.env.example` to share config structure
- Run formatting or lint checks before PR (optional for now)

> Additional environment setup and platform-specific steps are documented in `SETUP.md` and `docs/cross-platform-checklist.md`

---

## Local Development Requirements

Before contributing, please review the [Cross-Platform Dev Checklist](./docs/dev_checklist.md) for platform-specific setup, environment variables, and troubleshooting.

---

## File & Directory Highlights

- `main.py` – App entry point with Gradio UI
- `memory.py` – In-memory placeholder backend (from v0.4.3)
- `utils/` – Prompt prep, aliasing, filters, etc.
- `experiments/` – Testing and exploratory code per version
- `docs/` – Planning: roadmap, scope, test logs
- `config/` – Prompt templates and settings files
- `tests/` – Unit tests for context and logic

---

## Resources

- [Project Board](https://github.com/users/Deim0s13/projects/4/views/1)
- [Roadmap](./docs/roadmap.md)
- [Scope](./docs/scope.md)
- [Release Notes](./docs/release_notes.md)
- [Test Experiments Tracker](./docs/experiments_tracker.md)

---

Thanks again for helping to shape this project — and for contributing to an open, structured exploration of what’s possible with LLMs
