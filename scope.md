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

## Current Version: v0.2.4

## Upcoming Version: v0.2.5 (Planned)

**Planned Improvements:**

- **Better Error Recovery:**

  - Assistant gracefully responds when fuzzy matching fails.

- **Prompt Matching Preview in Debug Mode:**

- Show fuzzy match score when applicable.

**Prompt and Concept Library Management:**

- Normalize and enrich specialized prompt examples.

**Developer Playground Autopreview (optional):**

- Optional automatic generation after text input.

**Code Cleanup:**

- Remove redundant logic and ensure efficiency.

**README.md and scope.md alignment:**

- Keep full feature history recorded accurately.