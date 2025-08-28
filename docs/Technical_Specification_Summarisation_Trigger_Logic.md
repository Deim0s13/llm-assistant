# Technical Specification: Summarisation Trigger Logic

---

## 1. Thresholds: When to Summarise

* **Token threshold:**
  Summarisation is triggered when the **total tokens in the constructed prompt** (including system, context, and history turns) would **exceed `max_prompt_tokens`** as defined in `settings.json`.

  * Example: `max_prompt_tokens = 2048`

* **Turn threshold (optional):**
  Summarisation may also trigger if the number of historical turns **exceeds `max_history_turns`**.

  * Example: `max_history_turns = 10`

* **Minimum user turns:**
  The summariser requires at least 3 user turns before generating bullet-point summaries. 
  With fewer than 3 user turns, a placeholder message is returned instead.
  
  * Purpose: Prevents meaningless summaries from very short conversations
  * Implementation: `MIN_USER_TURNS = 3` in `utils/summariser.py`

* **Configurable:**
  Both thresholds are exposed as settings. Either can be used to trigger summarisation, but the token limit is the “hard” constraint.

---

## 2. Insertion Point: Where is the Summary Placed?

* The **summary block** is **inserted** in place of the **oldest turns** that would otherwise be trimmed, so that:

  * The *most recent* (N) turns always remain as “live” context.
  * The summary block sits **just before** the remaining live turns.

* **Order:**

  \[SYSTEM PROMPT]
  \[SUMMARY BLOCK]   <-- summary of trimmed (oldest) turns
  \[N most recent full turns]
  \[USER input]

* **Format:** 
  Summary content is inserted with role="summary" and formatted as bullet points:
  ```
  [SYSTEM PROMPT]
  • User message summary...
  • User message summary...  
  [N most recent full turns]
  [USER input]
  ```

---

## 3. Interaction with Memory (Order of Operations)

* **Memory backend** (Redis, SQLite, In-memory) is **queried for the full session history** first.
* The summarisation logic is applied **after** retrieving all turns, but **before** constructing the final prompt.
* **Summarisation** occurs as a “compression” step, replacing the oldest turns with a summary if thresholds are breached.

---

## 4. Config Keys: `settings.json`

Add the following section to `settings.json`:

```
"summarisation": {
  "enabled": true,
  "strategy": "heuristic",   // "heuristic" | "llm" | "none"
  "token_threshold": 2048,
  "turn_threshold": 10,
  "preserve_user_turns": false, // (optional) always keep last user turns unsummarised
  "debug": false
}
```

* **All keys are validated by `settings_loader.py`.**
* If missing or invalid, fallback to defaults and log a warning.

---

## 5. Extensibility: Future Strategies

* **Strategy pattern:**
  Summarisation logic is selected via the `strategy` key (e.g., `"heuristic"`, `"llm"`).

* **Plug-in:**
  Future strategies (e.g., topic-based, per-user, language-aware) can be added as new classes/functions that implement a shared interface (e.g., `summarise_context(strategy, ...)`).

* **Config-driven:**
  Any new strategy should be selectable from `settings.json`, and may add its own config options under `summarisation`.

---

## 6. Exact Thresholds

* For **v0.4.5**, default to:

  * `"token_threshold": 2048`
  * `"turn_threshold": 10`
* These should be documented in code comments and in `SETUP.md` as the “current defaults.”

---

## 7. Control Flow Diagram

Retrieve all turns from memory
|
v
Does turn or token limit exceed threshold?
|
+---+---+
No       Yes
\|         |
\[Build      \[Summarise oldest turns
prompt      ➜ Insert summary block
as usual]   ➜ Keep recent N full turns]
\|         |
+---+-----+
|
v
\[Send prompt to LLM]

---

## 8. Sample settings.json Block

```
"summarisation": {
  "enabled": true,
  "strategy": "heuristic",
  "token_threshold": 2048,
  "turn_threshold": 10
}
```

---

## 9. Review & Approval

* This spec must be **reviewed and approved by at least one contributor** (or yourself, if solo) before proceeding to implementation.
* The approved spec should be linked or attached to the related GitHub Issue/task.

---

## Summary Table

| Section         | Detail                                                 |
| --------------- | ------------------------------------------------------ |
| Trigger         | Token or turn threshold exceeded                       |
| Insertion Point | Summary replaces oldest turns, just before live turns  |
| Memory          | Summarise after retrieving all turns from memory       |
| Config Keys     | `summarisation.enabled`, `strategy`, `token_threshold` |
| Extensibility   | Strategy pattern, config-driven, plug-in friendly      |
| Control Flow    | See diagram above                                      |
