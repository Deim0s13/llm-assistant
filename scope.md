# Version History and Feature Scope

## v0.2.0

### Core Feature Set

- Introduced multi-turn conversation tracking using structured history (`role`, `content`).
- Loaded base system prompt (`prompt_template.txt`) from external file.

- Added **dynamic prompt injection:** keyword matching to switch prompts from `specialized_prompts.json`.

- Gradio UI with generation parameter sliders:

  - Max New Tokens
  - Temperature
  - Top-p
  - Do Sample toggle

- Enhanced debugging with logging:

  - Context sent to model
  - Generated outputs
  - Generation parameters used

### v0.2.1

**Improvements:**

- Upgraded prompt matching to handle smart quotes normalization.
- Expanded **specialized prompts**.
- Improved error handling for loading files.
- Debug output refined with clearer logs.

### v0.2.2

**Enhancements:**

- **Model Upgrade:** Switched from `google/flan-t5-small` to `google/flan-t5-base`.
- Better specialized prompt matching reliability.
- Expanded base prompt examples for stronger in-context learning.

### v0.2.3

**Developer Diagnostics:**

- **Prompt Source Diagnostics:** Now shows whether the assistant used the `base prompt` or a `specialized prompt` in each interaction.
- Cleaner internal functions for prompt sourcing.

### v0.2.4

**Major UI and Developer Improvements:**

- **Developer Playground Panel:**

  - Input a test message
  - See matched concept
  - View resolved specialized prompt
  - Preview generated model output

- **Fuzzy Matching Toggle:**

- Optionally enable approximate keyword matching.
- Helps catch small typos or variations.

**Advanced Settings Panel:**

- Collapsible area housing extra settings like fuzzy matching.

**More Structured Debugging:**

- Better formatting for logs.
- Cleaner separation of diagnostics vs normal flow.

**Minor Cleanup and Polishing:**

**Code Refactoring:**

- Minor improvements to specialized prompt matching logic for better readability and consistency.

**Debug Enhancements:**

- Clearer debug output formatting.
- Show fuzzy match scores when applicable (if fuzzy matching is enabled).

**Error Handling Improvements:**

- More graceful fallback behaviour if prompt selection fails.
- Cleaner assistant responses on errors.

**UI Label Improvements:**

- Minor polishing of labels for settings like fuzzy matching toggle.

**Comment and Documentation Cleanup:**

- Clarified function docstrings and important in-line comments.
- Corrected typos and inconsistencies across code and `README.md`.

## Current Version: v0.2.4

## Upcoming Version: v0.2.5 (Planned)