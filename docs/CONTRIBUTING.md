# Contributing Guidelines

Welcome, and thank you for your interest in contributing to this project! This document outlines the standards and workflow we follow to keep things organised, traceable, and easy to collaborate on.

---

## Purpose

This project started as a learning journey into LLMs and has grown into a structured exploration tool for prompt behaviour, model response control, and AI experimentation. Contributions are welcome — especially those that align with the project's learning-first mindset and structured development approach.

---

## Branching Strategy

We follow a simplified branching model:

- **`main`** — Stable, production-ready code. Each release is tagged here.
- **`dev`** — Integration branch for upcoming changes. All new features, bugfixes, and documentation updates go here first.
- **`feature/*`**, **`bugfix/*`**, **`docs/*`** — Used for active development. Each isolated change should use a separate branch.

> 🚧 Developers must branch from `dev`, not `main`.  
> Once your feature or fix is complete and tested, submit a PR to `dev`.  
> Merges to `main` are only done when cutting a new version.

---

## Feature Branch Naming Convention

To maintain clarity, we use **versioned and categorised** branch names.

### Format

[type]/v[major.minor.patch]-[short-description]

### Examples

feature/v0.3.1-context-window-expansion
bugfix/v0.3.1-token-limit-fix
docs/v0.3.1-readme-cleanup

- Use lowercase.
- Hyphenate the descriptive part for readability.

---

## Commits

Use clear, present-tense commit messages. Optionally follow the [Conventional Commits](https://www.conventionalcommits.org/) style.

### Examples

feat: add temperature slider to playground
fix: correct alias mapping bug
docs: update scope.md with v0.3.0 summary

---

## Pull Requests

Pull Requests should:

- Target the `dev` branch
- Reference a related issue or experiment (if applicable)
- Include a brief summary of **what** and **why**
- Pass any linting or basic tests

---

## File Locations of Interest

- [`README.md`](./README.md) — Project overview and current version
- [`docs/scope.md`](./docs/scope.md) — Planned and in-progress features by version
- [`docs/release_notes.md`](./docs/release_notes.md) — Historical release summaries
- [`docs/experiments_tracker.md`](./docs/experiments_tracker.md) — Index of experiment/test results
- [`experiments/`](./experiments/) — Per-version testing and experiment logs
- [`prompt_aliases.json`](./data/prompt_aliases.json) — Maps input phrases to prompt concepts
- [`specialized_prompts.json`](./data/specialized_prompts.json) — Contains prompt templates used by concept

---

## Resources

- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Gradio](https://www.gradio.app/)
- [Markdownlint](https://github.com/DavidAnson/markdownlint)

---

Thanks again for helping improve this project — and deepen our understanding of LLM behaviour in the process!
