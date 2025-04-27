# Version History and Feature Scope

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

## v0.2.1

**Improvements:**

- Upgraded prompt matching to handle smart quotes normalisation.
- Expanded **specialised prompts**.
- Improved error handling for loading files.
- Debug output refined with clearer logs.

## v0.2.2

**Enhancements:**

- **Model Upgrade**: Switched from `google/flan-t5-small` to `google/flan-t5-base`.
- Improved specialised prompt matching reliability.
- Expanded base prompt examples for stronger in-context learning.

## v0.2.3

**Developer Diagnostics:**

- **Prompt Source Diagnostics**: Now shows whether the assistant used the `base prompt` or a `specialised prompt` in each interaction.
- Cleaner internal functions for prompt sourcing.

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

## Current Version: v0.2.5

## Upcoming Version: v0.3.0 (Planned)