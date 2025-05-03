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

### Documentation Index

- [`scope.md`](scope.md) – Defines the project’s current and future goals, boundaries, and focus areas.
- [`release_notes.md`](release_notes.md) – Tracks version history, feature additions, and important changes across releases.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) – Guidelines for contributing, including branch naming, development flow, and coding standards.
- [`experiments/test_experiments_index.md`](experiments/test_experiments_index.md) – Master index of all experiments and structured tests, with links to detailed results.

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

- Enhance specialized prompt coverage.
- Introduce lightweight safety guardrails for dangerous queries.
- Improve context memory handling across multi-turn chains.
- Experiment with external knowledge retrieval (RAG) methods.
- Expand playground features for even faster prompt iteration.

---

## Previous Versions

### Version History

Looking for earlier versions? See [Release Notes ➔](release_notes.md) for full details of previous features and improvements.

---
