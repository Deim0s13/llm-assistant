# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.2.2) leverages the instruction-tuned model `google/flan-t5-base` to create a robust multi-turn conversation interface with enhanced prompt control.

## Naming Convention Update (From v0.2.4 Onwards)

### Previous Format

Branch names were descriptive and focused on what was being delivered, e.g.:

- `specialized-prompts-upgrade`
- `model-upgrade`
- `alias-matching`

### New Format (from v0.2.4 onward)

Branch names now include the version for clarity and traceability:

- `feature/v0.2.4-ui-devtools`
- `bugfix/v0.2.5-token-logging`
- `docs/v0.2.6-readme-refresh`

This will make versioning clearer during merges and retrospectives, especially as the project grows. If you ever need to roll back or trace changes, this structure makes it easier.

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

## External Files

- **prompt_template.txt:**
  Contains the base instruction for the assistant’s behavior and tone.

- **specialized_prompts.json**
  Maps trigger keywords (e.g., `“explain like I’m five”`, `“historical quote”`) to alternate system prompts used when those phrases are detected in the input.

- **aliases.py**
  Maps common input phrases to those normalised concepts for flexible and reslient keywork matching.

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

## Next Steps

### • Prompt Refinement and Few-Shot Tuning

Improve the examples and phrasing in both `prompt_template.txt` and `specialized_prompts.json` for more consistent behaviours across topics.

### • Future Enhancements

Future versions might include:

• Containerization with **Podman**
• Domain-specific model fine-tuning
• Multi-user or persistent session memory
• Prompt quality scoring or fallback strategies
• GitHub Copilot-style suggestion flow

## Previous Versions

### Version History

| Version | Highlights |
|:--------|:-----------|
| **v0.1.0** | Basic chatbot with static base prompt, no memory. |
| **v0.2.0** | Introduced multi-turn conversation memory, tunable generation settings, and externalised prompt files. |
| **v0.2.1** | Added specialised prompt injection (keyword triggers specialised prompts), and improved debug logging. |
| **v0.2.2** | Upgraded model from `google/flan-t5-small` ➔ `google/flan-t5-base`, expanded prompt library, improved specialised matching. |
| **v0.2.3** | Introduced alias mapping for flexible keyword detection, normalised specialised prompts, added prompt source diagnostics. |
| **v0.2.4** | Added fuzzy matching toggle, Developer Playground panel, expanded debug output, Advanced Settings panel. |
| **v0.2.5** | Code clean-up, improved fuzzy matching, expanded prompt libraries, auto-preview for developer playground. |

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

## Features in Version 0.2.3

### • Keyword Aliases Introduced

Commonly used phrases mapped to a normalized concept (e.g., “explain like i’m five” ➔ `explain_simple`).

### • Normalized Specialized Prompt Structure

Specialized prompts use concepts as keys (e.g., `historical_quote`, `explain_simple`).

### • Improved Specialized Prompt Matching

Instead of relying only on direct string search, aliases enable more robust trigger matching.

### • Prompt Source Diagnostics

When responding, the chatbot now identifies whether it used a base prompt or specialized prompt.

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
