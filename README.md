# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.3.0) leverages the instruction-tuned model `google/flan-t5-base` to create a robust multi-turn conversation interface with enhanced prompt control.

---

## Current Version (v0.4.0)

This version focuses on enhancing the way the chatbot identifies and responds to different types of user queries. Improvements include:

- **Expanded Prompt Matching**: The `prompt_aliases.json` file has been significantly expanded with more keyword variants and paraphrases, allowing better mapping of user input to specialized prompt templates.
- **In-Order Token Alias Detection**: Introduced a smarter matching function that checks for multi-token aliases occurring in sequence within user input (e.g., "explain like I'm five").
- **Improved Diagnostics**: Logging now provides better visibility into which aliases were scanned, which were matched, and why a fallback was used—supporting better transparency and future debugging.
- **Codebase Clean-Up**: Matching logic was modularized to keep `main.py` maintainable and easier to extend in future versions.

These changes lay the foundation for future improvements to safety guardrails and memory handling in v0.4.1 and v0.4.2.

For more detail, see [release_notes.md](release_notes.md).

---

## Planned Version (v0.4.1)

### Features in Version 0.4.1

- Introduced configurable **Safety Guardrails** to moderate content and improve responsible behaviour.
- Added a lightweight filtering layer to detect and optionally block profanity and sensitive input/output.
- Implemented support for a 'settings.json' configuration file to control safety features like profanity tolerance.
- Enhanced logging to clearly show when safety filters are triggered (e.g., “Profanity removed from response”).
- Maintains modular design to support future expansion (e.g., more granular filter categories or external moderation tools).

**Why this matters:**
As the chatbot becomes more capable, it’s important to ensure safe and adaptable usage across contexts (e.g., personal, educational, or public-facing environments). This version lays the foundation for tunable behaviour aligned with different use cases.

---

## Project Structure and Documentation Standards

As part of ongoing improvements, the project now maintains:

- **Structured Documentation:** Each major topic (features, versioning, scope, experiments) has its own dedicated markdown file.
- **Versioning Model:** Only the current version is detailed in the main README. Historical version details are moved to `release_notes.md`.
- **Scope Management:** The `scope.md` file captures planned and delivered scope for each version, keeping development focused and visible.
- **Experiments Tracker:** The `experiments_tracker.md` file logs all structured experiments, findings, and insights as part of hands-on LLM learning.

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

### Scope and Feature Tracking

In addition to capturing experiment learnings, this project maintains a [scope.md](scope.md) file.

The `scope.md` file serves as the **official tracker** for:

- Defining each planned version and its intended features.
- Documenting which improvements have been completed, planned, or deferred.
- Keeping development aligned with the broader learning goals and project focus.

This ensures we have a clear, evolving roadmap without losing sight of the original hands-on learning objectives.

---

## 📚 Documentation Index

| File                                  | Description                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| [README.md](./README.md)              | Project overview, setup instructions, and current version details.          |
| [scope.md](./scope.md)                | Defines the scope and goals for each version or feature set.                |
| [release_notes.md](./release_notes.md)| Chronological version history with highlights and major changes.            |
| [CONTRIBUTING.md](./CONTRIBUTING.md)  | Guidelines for contributing, including branch strategy and naming standards.|
| [test_experiments.md](./test_experiments.md) | Master tracker for all tests and experiments.                       |
| [ROADMAP.md](./ROADMAP.md)            | Long-term learning and development plan across project phases.              |
| [experiments/](./experiments/)        | Folder containing detailed experiment and test logs by version.             |

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

We maintain a central index of all structured tests and behavioural experiments conducted on the assistant. This includes results, observations, and guidance for running future tests.

[Test & Experiment Index](experiments/test_experiments_index.md)

---

## Future Roadmap

This project is part of a multi-phase LLM learning journey. We track our roadmap in [`ROADMAP.md`](./ROADMAP.md), which includes:

- Learning phases (e.g., chatbot basics, fine-tuning, deployment)
- Feature planning and milestones
- Links to related experiments and versions

---

## Previous Versions

### Version History

Looking for earlier versions? See [Release Notes ➔](release_notes.md) for full details of previous features and improvements.

---
