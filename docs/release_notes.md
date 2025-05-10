# Release Notes

This file tracks detailed version histories for the LLM Chatbot Starter Kit project.

---

## Version Table

| Version | Highlights |
|:--------|:-----------|
| **v0.1.0** | Basic chatbot with static base prompt, no memory. |
| **v0.2.0** | Introduced multi-turn conversation memory, tunable generation settings, and externalised prompt files. |
| **v0.2.1** | Added specialised prompt injection (keyword triggers specialised prompts) and improved debug logging. |
| **v0.2.2** | Upgraded model from `google/flan-t5-small` ➔ `google/flan-t5-base`, expanded prompt library, improved specialised matching. |
| **v0.2.3** | Introduced alias mapping for flexible keyword detection, normalised specialised prompts, added prompt match diagnostics in debug mode. |
| **v0.2.4** | Added fuzzy matching toggle in the UI, Developer Prompt Playground panel, expanded debug output, added Advanced Settings collapsible UI section. |
| **v0.2.5** | Bugfix release: improved internal logging, enhanced error handling for missing specialised prompts, consistency fixes for prompt matching logic. |
| **v0.3.0** | Introduced documentation restructuring, separated release notes, added `scope.md`, and improved maintainability through branch and contribution conventions. |
| **v0.4.0** | Enhancements to prompt matching: expanded `prompt_aliases.json`, introduced in-order token alias detection, improved logging diagnostics, and laid groundwork for upcoming safety and memory improvements. |
| **v0.4.1** | Introduced configurable safety guardrails, content moderation, and sensitivity-based input/output handling. |

---

## Version 0.1.0

### Initial Proof of Concept

- Static chatbot based on a single fixed system prompt.
- No conversation history — each turn was independent.
- Minimal UI — basic Gradio textbox chat.
- No specialized prompts, no diagnostics, no tuning parameters.

---

## Version 0.2.0

### Core Feature Set

- **Multi-Turn Conversation:**
  - History tracked across turns (role and content) for natural dialogue flow.
- **Base System Prompt Externalized:**
  - Read from prompt_template.txt for easy editing.
- **Dynamic Specialized Prompt Injection:**
  - Based on matching keywords in user inputs (specialized_prompts.json).
- **Gradio UI with Generation Controls:**
  - Sliders for max_new_tokens, temperature, top_p.
  - Checkbox for do_sample.
- **Enhanced Debug Logging:**
  - Logs generation parameters, full prompts, outputs, and matching info.

---

## Features in Version 0.2.1

### • Enhanced Conversation Context

The chatbot continues to maintain multi-turn conversation history, enabling more coherent responses by incorporating previous exchanges into the prompt.

### • Externalized Prompts

- **Base Prompt** is stored in `prompt_template.txt`, enabling easy iteration on the assistant’s personality and tone.  
- **Specialized Prompts** are stored in `specialized_prompts.json` and dynamically injected based on user queries to better tailor responses (e.g., “explain like I’m five”, “give me a fun fact”).

### • Keyword-Based Prompt Switching

A new mechanism scans user input for relevant keywords and loads a specialized prompt when appropriate, overriding the base instructions for that interaction. This allows lightweight prompt engineering without hardcoding logic into the model.

### • Structured Conversation History

Exchanges are tracked using structured `role`/`content` pairs (user, assistant), improving clarity and ensuring predictable formatting across turns.

### • Tunable Generation Parameters

The Gradio interface allows real-time experimentation with the following controls:

- **Max New Tokens**  
- **Temperature**  
- **Top-p** (Nucleus Sampling)  
- **Do Sample**

These options help shape response style, creativity, and determinism for better control during development.

### • Debug Logging for Development

Debug mode (`DEBUG_MODE = True`) outputs detailed logs showing:

- Which prompt is being used  
- Full context passed to the model  
- Raw generated output  
- Token generation settings  

This allows fine-grained introspection during testing and refinement.

---

## Features in Version 0.2.2

### • Model Upgrade

Upgraded from `google/flan-t5-small` to `google/flan-t5-base` for significantly improved comprehension and output quality.

### • Concept-Based Prompt Matching

- Specialized prompts are now matched using concept _aliases_ (e.g. "explain simple", "like I'm five" → `explain_simple`), ensuring greater flexibility and reducing false negatives.

- Keyword mappings are maintained in `aliases.py`, decoupling logic from prompt content.

### • Diagnostic Logging

- Logs explicitly indicate:
  - Whether a specialized or base prompt was selected
  - What alias was matched (if any)
  - Full prompt context sent to the model
- Makes debugging prompt behaviour much easier

---

## Features in Version 0.2.3

### • Keyword Aliases Introduced

Commonly used phrases mapped to a normalized concept (e.g., “explain like i’m five” ➔ `explain_simple`).

### • Normalized Specialized Prompt Structure

Specialized prompts use concepts as keys (e.g., `historical_quote`, `explain_simple`).

### • Improved Specialized Prompt Matching

Instead of relying only on direct string search, aliases enable more robust trigger matching.

### • Prompt Source Diagnostics

When responding, the chatbot now identifies whether it used a base prompt or specialized prompt.

---

## Features in Version 0.2.4

### • Enhanced Prompt Selection

- Specialized prompts are triggered by keywords or phrases from user input.
- **Developer diagnostics** show whether the base or specialized prompt was used.
- **Fuzzy matching toggle** allows more flexible input matching (e.g., small typos still match).

### • Developer Prompt Playground

- A dedicated panel where developers can test different inputs to:
  - See matched concept (alias ➔ concept mapping)
  - View the resolved specialized prompt
  - Preview the generated output
- Helpful for testing and improving specialized prompts.

### • Tunable Generation Parameters

- **Max New Tokens**
- **Temperature**
- **Top-p** (nucleus sampling)
- **Sampling toggle (Do Sample)**

### • Advanced UI Improvements

- Collapsible “Advanced Settings” panel to hide developer options by default.
- Improved layout separation between user chat and developer controls.

### • Debug Mode Enhancements

- Full context printed to logs before generation.
- Fuzzy match candidate suggestions printed in debug logs.
- Extracted generation result separately logged.

---

## Features in Version 0.2.5

### • Codebase and Naming Improvements

- Renamed `initialized_model()` to `initialize_model()` for consistent naming.
- All functions now consistently use present-tense verbs for readability.

### • Prompt and Alias Library Enhancements

- Expanded `specialized_prompts.json` with more categories (e.g., `science_fact`, `tech_summary`).
- Normalised alias mapping in `prompt_aliases.json` for more robust trigger detection.

### • Improved Fuzzy Matching

- Fuzzy match scores logged and displayed during developer testing.
- More graceful fallback to base prompt when matching fails.

### • Developer Playground Enhancements

- New **Auto-Preview Mode**:  
  Automatically generates prompt previews while typing (optional toggle).

- Clearer separation of **manual run** vs **auto-run** behaviour.

### • UI and Debugging Improvements

- Consistent labelling for advanced developer settings.
- Cleaner error handling for playground generation.
- Expanded debug logging for fuzzy matches and scores.

---

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

## Features in Version 0.4.0

### Enhanced Prompt Matching and Diagnostics

This version focuses on making the chatbot smarter and more transparent about how it chooses which prompt to use.

#### Key Enhancements

- **Token-Level Alias Detection**  
  Multi-word aliases (e.g. _“explain like I’m five”_) now match even when tokens are spread across the input text.

- **Alias Coverage Expansion**  
  Updated `prompt_aliases.json` with broader and more natural language variants to increase match coverage.

- **Refactored Prompt Matching Logic**  
  Introduced a new `alias_in_message()` helper in `prompt_utils.py` to support better in-order token detection.  
  Maintains separation of concerns, reducing clutter in `main.py`.

- **Improved Fallback Logging**  
  New diagnostic logs show:
  - All aliases scanned
  - Why a match failed (e.g. concept not found in `specialized_prompts.json`)
  - Whether fuzzy matching was used and what confidence it returned

- **Consistent Debug Experience**  
  Fuzzy match scores and reasoning are consistently displayed in both the UI and debug logs.  
  Maintains clarity during testing and prompt tuning.

### Testing Support

- Ran structured tests using real-world prompt examples to validate matching behaviour.
- Created [v0.4.0 Test & Experiment Tracker](./experiments/v0.4.0.md) to document test cases and results.

### Internal Cleanups

- Introduced new folder structure to separate `utils`, `data`, `experiments`, and `docs`.
- Updated documentation, links, and developer references to reflect the new structure.

---

## Planned Features in Version 0.4.1 (Stable Version)

### Safety & Output Configuration

This version introduces the ability to configure output tone and safety controls — including profanity filtering, response strictness, and moderation modes — giving developers more control over the chatbot's personality and appropriateness in different environments.

#### Key Deliverables

- **Safety Config System**
  - Create a dedicated JSON or Python-based config (e.g. `safety_config.json`) to control behaviour.
  - Allow setting parameters like:
    - `allow_mild_profanity`: true/false
    - `suppress_controversial_topics`: true/false
    - `tone`: “friendly”, “neutral”, “sarcastic”, etc. (optional)

- **Integrated Enforcement**
  - Dynamically modify the base prompt or response logic based on the config settings.
  - Use light prompt-injection to enforce tone or restrict unsafe topics.

- **Settings Preview Panel**
  - In Gradio UI, add a small developer section showing the current safety settings.
  - Possibly allow toggling basic flags in real-time (for dev use only).

- **Unit Tests**
  - Add test cases to validate safety setting toggles.
  - Ensure output changes appropriately when settings change.

### Out of Scope

- Full moderation pipeline using APIs or classifiers
- Fine-tuned tone control via embeddings or model-level customization (planned in future)

### Dependencies

- `prompt_utils.py` for tone/prompt modifications
- Clean config loading structure (`config.py` or JSON)
- Existing prompt system that supports override injection

### Success Criteria

- Developers can control chatbot tone and safety levels via config
- Users see appropriately filtered output based on flags
- No regression in existing functionality (prompt matching, diagnostics, etc.)

---

Once these features are completed and tested, this section will be updated and moved to the stable **v0.4.1** entry in the table above.
