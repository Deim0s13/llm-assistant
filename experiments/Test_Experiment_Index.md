# Test & Experiment Index

This document serves as the central hub for all tests and experiments conducted in the project.
It tracks experiment outcomes, methods, observations, and any decisions resulting from those activities.
Each test or experiment is versioned and linked to its corresponding markdown file.

---

## Purpose

As the project evolves, it's important to have a structured way to validate assumptions, measure behavioural changes in the LLM's outputs, and explore new features or enhancements.

This file ensures:

* Transparency of what was tested and why
* A record of behavioural regressions or improvements
* Shared understanding for collaborators

---

## 📂 Experiment & Test Tracker

| Version | Status         | Summary Focus                             | Test File or Notes                                |
| ------- | -------------- | ----------------------------------------- | ------------------------------------------------- |
| v0.2.4  | ✅ Done         | Initial specialised prompt scaffolding    | [experiments\_v0.2.4.md](./experiments_v0.2.4.md) |
| v0.3.0  | ✅ Done         | Prompt matching baseline, output analysis | [experiments\_v0.3.0.md](./experiments_v0.3.0.md) |
| v0.4.0  | 🔄 In Progress | Enhanced alias matching, diagnostics      | [experiments\_v0.4.0.md](./experiments_v0.4.0.md) |
| v0.4.1  | 🔼 Planned     | Safety guardrails, refusal patterns       | *(Planned)*                                       |
| v0.4.2  | 🔼 Planned     | Context memory improvements               | *(Planned)*                                       |

---

## Folder Structure

All experiment documents live under the `/experiments/` folder using the naming convention:

```plaintext
experiments_v[version].md
```

Example:

```plaintext
experiments/
├── experiments_v0.2.4.md
├── experiments_v0.3.0.md
├── experiments_v0.4.0.md
```

---

## How to Contribute a New Test Set

1. Create a new file in `/experiments/` named `experiments_vX.Y.Z.md`.
2. Follow the format used in previous versions:

   * **Input**
   * **Matched Concept**
   * **Resolved Prompt**
   * **Output**
   * **Observations**
3. Add a new row to the tracker table above with a short description and link.

---

## Versioned Experiment Details

### **v0.4.0 – Prompt Matching Enhancements**

**Focus:**
Improved alias matching logic, multi-token phrase detection, diagnostics logging, and fallback handling.

[experiments\_v0.4.0.md](./experiments_v0.4.0.md)

---

### **v0.3.0 – Structured Prompting & Safety Exploration**

**Focus:**
Baseline testing of prompt matching, safety-related query responses, and decoding behaviour.

[experiments\_v0.3.0.md](./experiments_v0.3.0.md)

---

### **v0.2.4 – Initial Specialized Prompt Scaffolding**

**Focus:**
First tests with `specialized_prompts.json` and alias resolution.
Basic prompt injection and developer playground testing.

[experiments\_v0.2.4.md](./experiments_v0.2.4.md)

---

## Navigation

* [README.md](../README.md)
* [release\_notes.md](../docs/release_notes.md)
* [scope.md](../docs/scope.md)
* [ROADMAP.md](../docs/ROADMAP.md)
* [contributing.md](../docs/contributing.md)
