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
