# Test & Experiment Index

This document is the **central hub** for every test set, experiment run, and observation made during development.
It keeps a living record of what was explored, why it mattered, and any decisions that resulted.

---

## Purpose

A structured tracker gives us:

* 📜 **Transparency** – know exactly what was tried and when
* 📈 **Regression safety‑net** – compare behaviour across versions
* 🤝 **Shared context** – team‑mates see prior findings before repeating work

---

## 📂 Experiment & Test Tracker

| Version | Status             | Main Focus                                     | Test File / Notes                                 |
| ------- | ------------------ | ---------------------------------------------- | ------------------------------------------------- |
| v0.2.4  | ✅ **Done**         | Initial specialised prompt scaffolding         | [experiments\_v0.2.4.md](./experiments_v0.2.4.md) |
| v0.3.0  | ✅ **Done**         | Prompt‑matching baseline & output analysis     | [experiments\_v0.3.0.md](./experiments_v0.3.0.md) |
| v0.4.0  | ✅ **Done**         | Enhanced alias logic & diagnostics             | [experiments\_v0.4.0.md](./experiments_v0.4.0.md) |
| v0.4.1  | ✅ **Done**         | Safety guard‑rails & refusal patterns          | [experiments\_v0.4.1.md](./experiments_v0.4.1.md) |
| v0.4.2  | ✅ **Done**         | Context trimming & memory injection            | [experiments\_v0.4.2.md](./experiments_v0.4.2.md) |
| v0.4.3  | 🔄 **In Progress** | Memory backend toggle & summarisation scaffold | *(running)*                                       |
| v0.5.x  | 🔼 **Planned**     | Containerisation & deployment tests            | *(TBD)*                                           |

> **Legend**  ✅ Done  ·  🔄 In Progress  ·  🔼 Planned
> All markdown files live under `/experiments/`.

---

## Folder Convention

```text
experiments/
├── experiments_v0.2.4.md
├── experiments_v0.3.0.md
├── experiments_v0.4.0.md
├── experiments_v0.4.1.md
├── experiments_v0.4.2.md
└── …
```

---

## Adding a New Experiment

1. **Create** a file named `experiments_vX.Y.Z.md` in `/experiments/`.

2. Follow the template:

   * **Input**
   * **Matched Concept** / **Prompt Source**
   * **Resolved Prompt Snippet**
   * **Output**
   * **Observations / Next Steps**

3. **Link** the new file in the tracker table above.

---

## Version Highlights

### v0.4.2 – Context Memory Integration

* Combined persistent memory with live history.
* Verified trimming logic respects token budget.
* Added rich debug logging for injected vs. live turns.

### v0.4.1 – Safety Guard‑Rails

* Implemented profanity list & sensitivity modes.
* Block/Filter pathways confirmed with five test cases.

### v0.4.0 – Improved Prompt Matching

* Multi‑token alias detection & fuzzy fallback.
* Diagnostic logs for direct / fuzzy hits.

*For earlier details see their respective markdown files.*

---

## Navigation

* [README.md](../README.md)
* [release\_notes.md](../docs/release_notes.md)
* [scope.md](../docs/scope.md)
* [ROADMAP.md](../docs/roadmap.md)
* [contributing.md](../docs/contributing.md)
* [Summarisation Planning](./docs/summarisation_planning.md)

---

> *This index is updated every time new experiments land in **main**.*
