# Contributing Guidelines

Welcome, and thank you for your interest in contributing to this project! This document outlines the standards and workflow we follow to keep things organised, traceable, and easy to collaborate on.

---

## Purpose

This project started as a learning journey into LLMs and has grown into a structured exploration tool for prompt behaviour, model response control, and AI experimentation. Contributions are welcome — especially those that align with the project's learning-first mindset and structured development approach.

---

## Branching Strategy

We follow a simplified branching model:

- **`main`**: Contains stable, production-ready code. Each release is tagged here.
- **`dev`**: [NEW] A development integration branch. All new features, bugfixes, and docs PRs are merged into `dev` first.
- **`feature/*`, `bugfix/*`, `docs/*`**: Use these for active work. Create a new branch for each isolated change.

Once your feature is complete and tested, submit a PR to `dev`. We merge to `main` only when cutting a new version.

---

## Feature Branch Naming Convention

To help maintain clarity as the project grows, we use **versioned and categorised** branch names.

### Format:

[type]/v[major.minor.patch]-[short-description]

### Examples:

feature/v0.3.1-context-window-expansion
bugfix/v0.3.1-token-limit-fix
docs/v0.3.1-readme-cleanup

Use lowercase and hyphenate descriptive parts for readability.

---

## Commits

Use clear, present-tense messages. You may optionally use Conventional Commits style:

feat: add temperature slider to playground
fix: correct alias mapping bug
docs: update scope.md with v0.3.0 summary

---

## Pull Requests

Pull Requests should:

- Target the `dev` branch
- Reference the relevant issue or experiment ID if applicable
- Include a brief summary of **why** the change is being made
- Pass linting and include test data if applicable

---

## File Locations of Interest

- `README.md`: High-level overview of the project
- `scope.md`: Tracks current and planned features by version
- `experiments_tracker.md`: Detailed log of all experiments performed

---

## Resources

- Hugging Face Transformers: https://huggingface.co/docs/transformers/index
- Gradio: https://www.gradio.app/
- Markdownlint: https://github.com/DavidAnson/markdownlint

---

Thanks again for helping improve this project — and deepen our understanding of LLM behaviour in the process!
