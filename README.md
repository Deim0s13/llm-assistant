# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.4.0) leverages the instruction-tuned model `google/flan-t5-base` to create a robust multi-turn conversation interface with enhanced prompt control.

---

## Current Version: v0.4.1

### Key Focus

- Introduced configurable safety guardrails for input and output handling.
- Added sensitivity modes: strict, moderate, relaxed.
- Enabled dynamic safety level selection through the developer UI panel.

See full details in [release_notes.md](./release_notes.md).

---

## Upcoming Version: v0.4.2 (Planning)

Planned focus areas:

- Introduce basic memory and context chaining between user turns.
- Improve conversation coherence across multiple interactions.

Details coming soon!

---

## Project Structure and Documentation Standards

As part of ongoing improvements, the project now maintains:

- **Structured Documentation:** Each major topic (features, versioning, scope, experiments) has its own dedicated markdown file.
- **Versioning Model:** Only the current version is detailed in the main README. Historical version details are moved to `release_notes.md`.
- **Scope Management:** The `scope.md` file captures planned and delivered scope for each version, keeping development focused and visible.
- **Experiments Tracker:** The `test_experiments.md` file logs all structured experiments, findings, and insights as part of hands-on LLM learning.

These changes were progressively introduced around version `v0.3.0` but are considered *foundational practices* going forward rather than tied to any single release.

---

### Documentation Improvements

- **Updated `README.md`**  
  Refocused to highlight current project goals, clearer versioning, and linked structured experiments.

- **Introduced `release_notes.md`**  
  Externalised all previous version history (v0.1.0 to v0.2.5) to keep the README concise and maintain detailed changelogs separately.

- **Enhanced `scope.md`**  
  Added a formal introduction and purpose section to explain its role in planning, version tracking, and decision-making.

- **Linked all major documents** (Scope, Release Notes, Experiments Tracker) for easier navigation and maintainability.

---

## 📚 Documentation Index

| File                                         | Description                                                                 |
|----------------------------------------------|-----------------------------------------------------------------------------|
| [README.md](./README.md)                     | Project overview, setup instructions, and current version details.          |
| [scope.md](./docs/scope.md)                  | Defines the scope and goals for each version or feature set.                |
| [release_notes.md](./docs/release_notes.md)  | Chronological version history with highlights and major changes.            |
| [CONTRIBUTING.md](./docs/contributing.md)    | Guidelines for contributing, including branch strategy and naming standards.|
| [test_experiments.md](./docs/test_experiments.md) | Master tracker for all tests and experiments.                       |
| [ROADMAP.md](./docs/ROADMAP.md)              | Long-term learning and development plan across project phases.              |
| [experiments/](./experiments/)               | Folder containing detailed experiment and test logs by version.             |

---

## Setup

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate

2. **Install dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

3. **Run the chatbot:**

   ```bash
   python main.py

Access the Gradio UI locally on `http://127.0.0.1:7860/`

---

## External Files

- **prompt_template.txt:**
  Contains the base instruction for the assistant’s behavior and tone.

- **specialized_prompts.json**
  Maps trigger keywords (e.g., `“explain like I’m five”`, `“historical quote”`) to alternate system prompts used when those phrases are detected in the input.

- **aliases.py**
  Maps common input phrases to those normalised concepts for flexible and reslient keywork matching.

---

## Experiments & Testing

We maintain a central index of all structured tests and behavioural experiments conducted on the assistant.  
This includes results, observations, and guidance for running future tests.

📄 [Test & Experiment Tracker](./experiments/test_experiments_index.md)

Each version's experiments are stored under the `/experiments` directory, allowing us to document findings, regressions, and improvements over time.

---

## Future Roadmap

This project is part of a multi-phase LLM learning journey.  
We track long-term goals and development phases in the [`ROADMAP.md`](./docs/ROADMAP.md):

- Learning stages (e.g., chatbot fundamentals, fine-tuning, deployment)
- Versioned milestones and development progress
- Links to experiments, scoped features, and stretch goals

---

## Previous Versions

Looking for earlier version details?

See the [Release Notes](./docs/release_notes.md) for a complete history of version highlights and feature introductions.
