# Project Scope and Planning Overview

## Introduction

This document defines the scope, goals, and boundaries for the LLM Chatbot Starter Kit project.  
It provides a centralised view of what each version aims to achieve, ensuring that the project evolves in a focused and intentional manner over time.

As the chatbot matures, this scope document helps maintain alignment between:

- The initial project vision (hands-on learning about LLMs, prompt design, and behaviour exploration)
- Technical implementations in each version
- Strategic choices about future development directions

---

## Purpose of This Document

The `scope.md` exists to:

- **Record the project vision**: Maintain clarity about the *why* behind feature choices and experiments.
- **Track version goals**: Outline the key objectives, enhancements, and limitations for each project version.
- **Support future planning**: Serve as a living reference when deciding new feature work, technical improvements, or pivots.
- **Improve traceability**: Connect learning-focused activities (such as LLM experiments) with formal version deliverables.

It complements the [`README.md`](../README.md) (current version overview) and the [`release_notes.md`](./release_notes.md) (full version history and detailed feature notes).

---

## v0.2.0 – Core Feature Set

- Introduced multi-turn conversation tracking using structured history (`role`, `content`).
- Loaded base system prompt (`prompt_template.txt`) from external file.
- Added **dynamic prompt injection**: keyword matching to switch prompts from `specialized_prompts.json`.
- Gradio UI with generation parameter sliders:
  - Max New Tokens
  - Temperature
  - Top-p
  - Do Sample toggle
- Enhanced debugging with logging:
  - Context sent to model
  - Generated outputs
  - Generation parameters used

---

## v0.2.1 – Improvements

- Upgraded prompt matching to handle smart quotes normalisation.
- Expanded **specialised prompts**.
- Improved error handling for loading files.
- Debug output refined with clearer logs.

---

## v0.2.2 – Enhancements

- **Model Upgrade**: Switched from `google/flan-t5-small` to `google/flan-t5-base`.
- Improved specialised prompt matching reliability.
- Expanded base prompt examples for stronger in-context learning.

---

## v0.2.3 – Developer Diagnostics

- **Prompt Source Diagnostics**: Now shows whether the assistant used the `base prompt` or a `specialised prompt` in each interaction.
- Cleaner internal functions for prompt sourcing.

---

## v0.2.4 – UI and Developer Improvements

- **Developer Playground Panel**:
  - Input a test message
  - See matched concept
  - View resolved specialised prompt
  - Preview generated model output
- **Fuzzy Matching Toggle**: Approximate keyword matching for typo resilience.
- **Advanced Settings Panel**: Collapsible UI for toggling dev features.
- **Structured Debug Logging**: Clearer separation of diagnostics and output.

---

## v0.2.5 – Minor Enhancements and Polish

- Renamed `initialized_model()` ➔ `initialize_model()` for naming consistency.
- Expanded prompt library: new categories (e.g., `science_fact`, `motivational_quote`).
- Fuzzy match scores logged during developer testing.
- Auto-preview toggle for Playground.
- UI polish: Improved labelling and collapsible panels.
- Error handling for blank generations.

---

## v0.3.0 – Experimentation Playground Expansion

### Objective

Shift focus from only chatbot functionality to hands-on learning with prompt engineering, model reasoning, and generation control.

### Focus Areas

- Prompt Engineering Experiments
- Chain-of-Thought Reasoning
- Decoding Strategy Exploration
- Output Evaluation with Optional Rating Tools

### Deliverables

- Prompt variations with few-shot examples
- Support for beam search decoding
- Experiment-driven UI changes
- Documented learnings and use cases

---

## v0.4.0 – Enhanced Prompt Matching

### Objective

Improve prompt detection and application by refining alias logic and diagnostics.

### Why This Matters

- Reduces base prompt fallback
- Increases reliability of prompt injection

### Key Deliverables

- Expanded `prompt_aliases.json`
- Multi-word alias matching logic
- Improved prompt match logging
- Unit test coverage for alias ➜ concept
- Alias diagnostic logging

### Success Criteria

- Reduced false negatives
- No regressions in alias detection
- Clear fallback and match logging

---

## v0.4.1 – Safety Guardrails & Sensitivity Controls (Current Version)

### Objective

Introduce lightweight filters to moderate chatbot input/output, with adjustable safety settings.

### Why This Matters

- Current implementation has no profanity/safety filter
- Helps adapt behaviour for educational or public settings

### Key Deliverables

- Add safety trigger filters (user and response)
- Configurable `settings.json` for profanity thresholds
- Log safety rule activations
- Optional UI toggle for Safety Mode
- Tests for filter coverage

### Out of Scope

- Full moderation or third-party safety APIs

### Success Criteria

- Logs show when safety rules apply
- Filter can be toggled via config
- Stable behaviour with no regressions

---

## v0.4.2 – Context Memory Handling & Project Hygiene (Planned)

### Objective

Begin improving the chatbot’s ability to remember and respond to earlier parts of a conversation while introducing structured project management using GitHub Projects.

### Why This Matters

- Current memory is limited to a basic context window; more realistic conversations require persistent recall.
- Task tracking has outgrown markdown-only tracking — introducing GitHub Projects enables better backlog management and collaboration.

### Key Deliverables

- Enable turn history recall across multiple exchanges
- Add configurable memory window (e.g. max turns to retain) via settings.json
- Log memory handling in debug mode
- Create GitHub Project board with backlog, labels, and workflow states
- Migrate markdown-based progress tracking to GitHub Issues/Projects
- Update README.md and CONTRIBUTING.md to reflect new workflow

### Out of Scope

- Persistent memory storage (e.g. Redis, database)
- AI-based summarisation of long conversations (future version)

### Success Criteria

- Responses correctly reflect earlier conversation turns
- GitHub Project board is created and actively used
- Documentation updated to reflect new project workflow
