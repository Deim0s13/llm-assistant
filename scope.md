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

It complements the `README.md` (current version overview) and the `release_notes.md` (full version history and detailed feature notes).

---

## v0.2.0

### Core Feature Set

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

## v0.2.1

**Improvements:**

- Upgraded prompt matching to handle smart quotes normalisation.
- Expanded **specialised prompts**.
- Improved error handling for loading files.
- Debug output refined with clearer logs.

---

## v0.2.2

**Enhancements:**

- **Model Upgrade**: Switched from `google/flan-t5-small` to `google/flan-t5-base`.
- Improved specialised prompt matching reliability.
- Expanded base prompt examples for stronger in-context learning.

---

## v0.2.3

**Developer Diagnostics:**

- **Prompt Source Diagnostics**: Now shows whether the assistant used the `base prompt` or a `specialised prompt` in each interaction.
- Cleaner internal functions for prompt sourcing.

---

## v0.2.4

**Major UI and Developer Improvements:**

- **Developer Playground Panel**:
  - Input a test message
  - See matched concept
  - View resolved specialised prompt
  - Preview generated model output
- **Fuzzy Matching Toggle**:
  - Optionally enable approximate keyword matching.
  - Helps catch small typos or variations.
- **Advanced Settings Panel**:
  - Collapsible area housing extra settings like fuzzy matching.
- **More Structured Debugging**:
  - Better formatting for logs.
  - Clearer separation of diagnostics vs normal flow.

---

## v0.2.5

**Minor Enhancements and Polish:**

- **Codebase Improvements**:
  - Renamed `initialized_model()` ➔ `initialize_model()` for naming consistency.
  - Aligned function naming to present tense for consistency.
- **Prompt Library Enhancements**:
  - Added new concepts (e.g., `science_fact`, `tech_summary`, `motivational_quote`).
  - Normalised prompt alias mappings.
- **Improved Fuzzy Matching Handling**:
  - Fuzzy match scores now logged during developer testing.
- **Auto-preview for Developer Playground**:
  - Playground can optionally auto-generate outputs while typing.
- **UI Polish**:
  - Improved labels, tooltips, and collapsible panels for a more consistent UI.
- **Bug Fixes and Error Handling**:
  - Prevent empty playground generations unless explicitly triggered.

---

## Version: v0.3.0

### Experimentation Playground Expansion

#### Objective

Shift focus from only chatbot functionality to hands-on learning with prompt engineering, model reasoning, and generation control.

#### Core Focus Areas

- **Prompt Engineering Experiments:**
  - Introduce and test variations in prompt phrasing.
  - Explore impact of instructional style and few-shot examples.
- **Chain-of-Thought Reasoning:**
  - Implement prompts that encourage step-by-step reasoning (“Let’s solve this step-by-step”).
  - Compare outputs with and without chain-of-thought prompting.
- **Decoding Strategy Exploration:**
  - Systematic experiments with temperature and top-p.
  - Introduce beam search decoding as a new selectable option.
  - Observe the trade-offs between creativity and precision.
- **Output Evaluation Development:**
  - Begin manual output evaluation for quality, completeness, and reasoning.
  - (Optional) Simple rating panel within Gradio to capture observations.

#### Deliverables

- Experimental prompts and chain-of-thought techniques integrated.
- Ability to toggle between decoding strategies: Sampling vs Beam Search.
- Updated Gradio UI (basic if needed) to support experiments.
- Documentation of findings and examples.
- Updated README.md reflecting the new experimentation purpose.

---

## Current Version: v0.4.0

### Enhanced Prompt Matching

#### Objective

Improve the chatbot’s ability to detect and apply the correct specialized prompt by refining keyword alias logic, expanding coverage, and reducing false negatives.

#### Why This Matters

- Several inputs fallback to the base prompt unnecessarily, even when similar phrases are covered by aliases.
- Better prompt matching will increase reliability, user satisfaction, and overall prompt response quality.

#### Key Deliverables

- [ ] Expand and refine `prompt_aliases.json` with broader keyword coverage.
- [ ] Add multi-word and phrase matching capabilities (e.g., regex or token-based heuristics).
- [ ] Improve logging and diagnostics for better prompt-matching transparency.
- [ ] Add unit tests to validate alias ➜ concept mapping.
- [ ] Optional: Build a testing tool to run alias coverage reports.

#### Out of Scope

- Full natural language classification (that's a larger future effort).
- Safety guardrails and context chaining (planned for v0.4.1 and v0.4.2).

#### Dependencies

- Existing structure in `get_specialized_prompt()`
- `prompt_aliases.json` and `specialized_prompts.json`

#### Success Criteria

- Fewer fallbacks to base prompt when semantically valid keywords are present.
- No regression in existing alias matches.
- Clear logs showing matched aliases and fallback decisions.

---

## Planned Version: v0.4.1

### Safety Guardrails & Sensitivity Controls

#### Objective

Introduce lightweight safety guardrails for user inputs and system responses, including configurable sensitivity settings (e.g., profanity tolerance), to allow for more responsible and adaptable behaviour.

#### Why This Matters

- Currently, the assistant does not evaluate input for harmful or inappropriate content, nor moderate its responses.
- As the chatbot becomes more useful in broader settings, it's important to support safe, respectful, and controlled outputs — especially in public or shared environments.
- Configurable filters will also allow developers to tailor the behaviour for context-specific use (e.g., educational vs. casual).

#### Key Deliverables

- [ ] Add a lightweight content filter to scan user input and model responses for predefined safety triggers.
- [ ] Introduce a `settings.json` or similar config file to allow sensitivity levels to be toggled (e.g., allow mild profanity).
- [ ] Log when safety rules are triggered (e.g., “Profanity filtered”, “Blocked sensitive response”).
- [ ] UI checkbox to enable/disable safety mode (optional if time permits).
- [ ] Add unit tests to validate safety handling and configuration toggles.

#### Out of Scope

- Advanced AI moderation or third-party safety models (e.g., OpenAI moderation endpoint).
- Real-time abuse detection or emotional sentiment analysis.

#### Dependencies

- Centralized `settings.json` or config object to manage feature toggles.
- Chat generation logic (`chat()` function) for post-processing and filter injection.

#### Success Criteria

- Clearly logged safety rule applications when triggered.
- Ability to toggle profanity filtering via config file or UI.
- No regressions in prompt response flow or generation performance.

---
