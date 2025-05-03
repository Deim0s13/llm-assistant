# Test & Experiment Index

This document serves as the central hub for all tests and experiments conducted in the project. It tracks experiment outcomes, methods, observations, and any decisions resulting from those activities. Each test or experiment is versioned and linked to its corresponding markdown file.

---

## Purpose

As the project evolves, it's important to have a structured way to validate assumptions, measure behavioural changes in the LLM's outputs, and explore new features or enhancements.

This file ensures:

- Transparency of what was tested and why
- A record of behavioural regressions or improvements
- Shared understanding for collaborators

---

## Experiment & Test Tracker

This document provides a master index of all experiment and test documentation conducted across project versions. Each version may link to a dedicated experiment log if applicable.

| Version  | Status        | Summary Focus                            | Test File or Notes                                            |
|----------|---------------|------------------------------------------|---------------------------------------------------------------|
| v0.2.4   | Done        | Initial specialized prompt scaffolding    | [`v0.2.4-experiments.md`](experiments/v0.2.4-experiments.md)  |
| v0.3.0   | Done        | Prompt matching baseline, output analysis | [`v0.3.0-experiments.md`](experiments/v0.3.0-experiments.md)  |
| v0.4.0   | In Progress | Enhanced alias matching, diagnostics       | [`v0.4.0-experiments.md`](experiments/v0.4.0-experiments.md)  |
| v0.4.1   | Planned     | Safety guardrails, refusal patterns       | *(Planned)*                                                   |
| v0.4.2   | Planned     | Context memory improvements                | *(Planned)*                                                   |

---

### Folder Structure

All documents live under the `/experiments/` folder using the naming convention: `v[version]_experiments.md`.

---

## How to Contribute a New Test Set

1. Create a new file in `/experiments/` named `experiments_vX.Y.Z.md`.
2. Follow the format used in previous versions: include test inputs, matched concept (if any), resolved prompt, generated output, and observations.
3. Add the new entry and a short description here under the correct version header.

---

## Versioned Experiments

### **v0.4.0 – Prompt Matching Enhancements**

**Focus:** Improved alias matching logic, diagnostics logging, and fuzzy fallback handling.

- [`experiments_v0.4.0.md`](experiments/experiments_v0.4.0.md): Covers prompt alias audit, edge-case prompts, and diagnostics validation.

### **v0.3.0 – Structured Prompting & Safety Exploration**

**Focus:** Prompt matching behaviours, safety issues, and response consistency at different temperatures.

- [`experiments_v0.3.0.md`](experiments/experiments_v0.3.0.md): Full results from manually run tests (e.g. "Can I drink bleach?", "Tell me a joke", etc.), diagnostic outputs, and observations.

---

## Notes

- Each test set should reflect the features introduced in that version.
- When doing follow-up regression testing, use the same prompts as in earlier versions to measure changes in output.
- Future expansions may include automated test harnesses.

---

Navigate | [README.md](../README.md) • [release_notes.md](../release_notes.md) • [scope.md](../scope.md)