# Progress Tracker

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
