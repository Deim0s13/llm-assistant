# Progress Tracker

## Progress Tracker v0.4.1

# ✅ v0.4.1 Safety Guardrails — Progress Tracker

This tracker helps monitor development progress for the v0.4.1 release focused on safety guardrails and configurable content moderation.

---

## Task Breakdown

| Task Area                  | Sub-Task                                                                 | Status       | Notes       |
|---------------------------|---------------------------------------------------------------------------|--------------|-------------|
| **1. Safety Configuration** | Create `safety_config.json` with modes and flags                         | ☐ Not Started |             |
|                           | Load config at startup in `main.py` or new `safety.py` module              | ☐ Not Started |             |
| **2. Safety Evaluation**   | Implement `evaluate_safety(message, config)` logic                        | ☐ Not Started |             |
|                           | Integrate into `chat()` pipeline before prompt generation                 | ☐ Not Started |             |
| **3. Dynamic Responses**   | Add refusal response templates                                            | ☐ Not Started |             |
|                           | Allow disclaimers or adjustments for relaxed modes                        | ☐ Not Started |             |
| **4. UI Integration**      | Add safety level toggle in Gradio dev panel (optional)                    | ☐ Not Started | Optional     |
| **5. Testing**             | Create/extend `test_experiments.md` with safety test cases                | ☐ Not Started |             |
|                           | Run tests across each mode (strict, moderate, relaxed)                    | ☐ Not Started |             |
| **6. Logging & Debugging** | Add logs for safety decisions and config used                             | ☐ Not Started |             |
|                           | Ensure visibility in debug mode                                           | ☐ Not Started |             |

---
