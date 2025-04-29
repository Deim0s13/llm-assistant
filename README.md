# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.3.0) leverages the instruction-tuned model `google/flan-t5-base` to create a robust multi-turn conversation interface with enhanced prompt control.

---

## Current Version

### Features in Version 0.3.0

In this version, the project focus intentionally shifted from purely building application features to a more **hands-on experimental approach**.

The goal was to better understand how large language models (LLMs) behave under different conditions — including prompt phrasing, generation settings, multi-turn context, and safety handling — and to use these insights to guide future development directions.

This experiments phase allowed us to:

- Explore LLM strengths and weaknesses systematically.
- Validate assumptions about prompt design, context management, and parameter tuning.
- Identify gaps where future improvements (like specialised prompts, safety mechanisms, or memory handling) could be prioritised.

### Key Updates in v0.3.0

- Introduced a structured experiments framework to explore LLM behaviours and limitations.
- Captured experimental results around prompt engineering, context management, temperature/top-p effects, response chaining, and safety/bias handling.
- Documented learnings and insights in the [experiments_tracker.md](experiments_tracker.md) file for future reference and ongoing refinement.

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

### Documentation Overview

- [`experiments_tracker.md`](./experiments_tracker.md): Records structured LLM experiments, findings, and insights.
- [`scope.md`](./scope.md): Tracks planned features, changes by version, and priorities.
- [`CONTRIBUTING.md`](./CONTRIBUTING.md): Development workflow, branching strategy, and naming conventions.
- [`release_notes.md`](./release_notes.md): Detailed historical summaries of all previous versions.

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

## Testing and Experimentation

### • Prompt Match Validation

Try input like:

- "Tell me something like I'm five"
- "Summarise this text"
- "Can you give me a fun fact"

Then check the logs to verify correct alias mapping and prompt injection.

### • Generation Parameter Tuning

Use the sliders and checkbox in the Gradio interface to adjust:

- **Max New Tokens**: Suggested range: 50–200  
- **Temperature**: Range: 0.1–1.0  
- **Top-p**: Range: 0.5–1.0  
- **Do Sample**: Toggle to switch between sampling (creative) and deterministic (greedy) responses.

Test different values and note how they influence tone, accuracy, and creativity.

### • Prompt Matching Debugging

Turn on `DEBUG_MODE` to confirm when a specialized prompt is used. Matched prompts are logged with `[Prompt Match]`, and unmatched queries will fall back to the base.

### • Few-Shot Examples (in prompt_template.txt)

Simple in-context examples improve model grounding. Review and revise thse to better your use case.

### • Debugging Prompt Matches

Turn on DEBUG_MODE = True to see full matching diagnostics in the console.

### • Testing Playground

Use the Developer Playground panel to verify concept matching and output without impacting user conversation history.

### • Testing Fuzzy Matching

Enable or disable fuzzy matching dynamically from the UI to see the effects of relaxed keywork matching.

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
