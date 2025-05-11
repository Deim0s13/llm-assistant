# Progress Tracker

**Deprecated Tracker**

> This progress tracker is no longer in use as of `v0.4.2`.  
> All planning, tasks, and version tracking are now managed via GitHub Issues and the [LLM Project Board](https://github.com/users/<your-username>/projects/<project-id>/views/<view-id>).

---

## Progress Tracker v0.4.1

### v0.4.1 Safety Guardrails — Progress Tracker

This tracker helps monitor development progress for the v0.4.1 release focused on safety guardrails and configurable content moderation.

---

## Task Breakdown

| Task Area                  | Sub-Task                                                                 | Status       | Notes                                                                 |
|---------------------------|--------------------------------------------------------------------------|--------------|-----------------------------------------------------------------------|
| **1. Safety Configuration** | Create `safety_config.json` with modes and flags                         | ✅ Done | Fully handled via the `safety` block in `settings.json`.             |
|                           | Load config at startup in `main.py` or `safety_filters.py`                | ✅ Done | `load_settings()` used globally.                                     |
| **2. Safety Evaluation**   | Implement `evaluate_safety(message, config)` logic                        | ✅ Done | Function exists but not yet called on *input* message.               |
|                           | Integrate into `chat()` pipeline **before prompt generation**             | ✅ Done | Only used post-generation for filtering output.                      |
| **3. Dynamic Responses**   | Add refusal response templates                                            | ✅ Done | `blocked_response_temlate` exists (with typo); not yet applied.      |
|                           | Allow disclaimers or adjustments for relaxed modes                        | ✅ Done | No logic to branch on `sensitivity_level` yet.                       |
| **4. UI Integration**      | Add safety level toggle in Gradio dev panel (optional)                    | ✅ Done | Optional, not present in current Gradio UI.                          |
| **5. Testing**             | Create/extend `test_experiments.md` with safety test cases                | ✅ Done | No coverage yet for input blocks or output filtering.                |
|                           | Run tests across each mode (strict, moderate, relaxed)                    | ✅ Done | Can be simulated with Gradio.                                        |
| **6. Logging & Debugging** | Add logs for safety decisions and config used                             | ✅ Done | Profanity logs only; `evaluate_safety()` logs pending.               |
|                           | Ensure visibility in debug mode                                           | ✅ Done | Controlled by `debug_mode` and `log_triggered_filters`.              |

---


## Progress Tracker – v0.4.2

This tracker helps monitor development progress for version **v0.4.2**, focused on improving context memory handling and introducing GitHub Projects as the primary planning and tracking mechanism.

---

### 🧠 Version Goals

> Refer to [`scope.md`](./scope.md) for high-level objectives.

---

### Task Breakdown

| Task Area                 | Sub-Task                                                                 | Status        | Notes                                                            |
|--------------------------|--------------------------------------------------------------------------|---------------|------------------------------------------------------------------|
| **1. GitHub Integration**| Create GitHub Project board                                               | ☐ Not Started | Kanban-style for backlog, active, done                          |
|                          | Add remaining v0.4.2 tasks as Issues/cards                                | ☐ Not Started | Link them to this tracker as needed                             |
|                          | Add README note referencing GitHub Projects                               | ☐ Not Started | Clarify where tasks are now managed                             |
| **2. Context Handling**  | Design context window expansion logic                                     | ☐ Not Started | Plan rules for history retention, token trimming, or summarisation |
|                          | Update `prepare_context()` to support expanded chaining                   | ☐ Not Started | Consider edge cases with long chat histories                    |
|                          | Add test cases to verify context correctness                              | ☐ Not Started | Use varying conversation lengths and observe response accuracy  |
|                          | Add logging to show context size and trimmed tokens                       | ☐ Not Started | Useful for debugging and tuning                                 |
| **3. Memory Strategy**   | Draft placeholder for future memory implementation (v0.4.3+)              | ☐ Not Started | Plan optional vector-based or database memory layer             |
| **4. Testing**           | Create `test_experiments_v0.4.2.md` and define memory/context tests        | ☐ Not Started | Focus on prompt integrity across longer dialogues               |
|                          | Validate no regressions in prompt selection or diagnostics                | ☐ Not Started | Use history-heavy and prompt-match test cases                   |
| **5. Documentation**     | Update `README.md` to reflect v0.4.2 scope and planning shift             | ☐ Not Started | Replace static changelog section                                |
|                          | Add section to `contributing.md` on project tracking expectations         | ☐ Not Started | Encourage PRs linked to GitHub issues or tasks                  |

---

### Completion Criteria

- GitHub Projects is the single source of truth for v0.4.2 tasks
- Context management updated and verifiably working in chat flow
- `README.md` and `scope.md` reflect v0.4.2 purpose and structure
- Tests and logs confirm stability and improvement over prior versions

---

### Version Status: `In Planning`

> Once the GitHub Project board is active, this file will link to it and serve as a legacy overview.
