# Release Notes 📜

Detailed changelog for the **LLM-Chatbot Starter Kit**.
Each entry lists the headline features, notable refactors, and links to deeper docs/tests where relevant.

---

## Version Summary Table

| Version | State      | Headline Highlights                                                |
|:-------:|:----------:|--------------------------------------------------------------------|
| **v0.1.0** | ✅ *Done* | Static base prompt, no memory, minimal Gradio UI                  |
| **v0.2.x** | ✅ *Done* | Multi-turn history, specialised prompts, alias mapping, diagnostics |
| **v0.3.0** | ✅ *Done* | Structured “experiments” framework & documentation re-org          |
| **v0.4.0** | ✅ *Done* | Robust alias detection, fuzzy matching, improved logging          |
| **v0.4.1** | ✅ *Done* | Configurable *Safety Guardrails* (profanity, sensitivity modes)    |
| **v0.4.2** | ✅ *Done* | Context-window trimming, cross-platform device detection, `.env`  |
| **v0.4.3** | 🔄 *In Progress* | In-process **Memory backend**, optional summarisation scaffold |
| **v0.4.4** | 🔼 *Planned* | Automated tests & CI, RAG prototype kickoff                    |

---

## v0.1.0 – First Proof-of-Concept

* Static system prompt embedded in code
* No history (each user turn isolated)
* Bare-bones Gradio textbox interface

---

## v0.2.x – From Single-Turn to Specialised Prompts

### v0.2.0
* **Conversation History** – maintains role/content pairs
* External **`prompt_template.txt`** (base) & **tunable generation sliders**

### v0.2.1 → v0.2.5 Highlights
* **Specialised Prompt Injection** via `specialized_prompts.json`
* **Alias Mapping** (`prompt_aliases.json`) for flexible triggers
* **Fuzzy Matching Toggle**, **Developer Playground**, **Advanced UI**
* Upgrade model to `google/flan-t5-base`
* Continuous **debug-log** improvements & minor bug-fixes

*Full per-patch notes live in* `experiments/experiments_v0.2.*.md`

---

## v0.3.0 – Experiments Framework 📊

* Introduced **/experiments/** folder & markdown logs
* Captured systematic tests on prompt phrasing, safety modes, token limits
* Docs restructure: `scope.md`, `roadmap.md`, dedicated release notes
* Learnings fed into later prompt-matching & safety design

---

## v0.4.x Track – Stability, Safety, Memory

### v0.4.0 – Alias & Prompt Matching Overhaul
* Token-level alias detection (`alias_in_message`)
* Expanded alias library & diagnostics (`[Prompt] …` logs)
* Clear fallback reasoning when no match found

### v0.4.1 – Configurable Safety Guardrails
* **`settings.json → safety`** section: `sensitivity_level`, `profanity_filter`
* Three modes: **strict · moderate · relaxed**
* Runtime filtering of output (moderate) or blocking (strict)
* Refusal template driven by config
* Unit-style manual tests recorded in `experiments_v0.4.1.md`

### v0.4.2 – Context Window & Dev Hygiene
* **Context Trimming** based on `max_history_turns` & `max_prompt_tokens`
* Debug logs show retained turns & token counts
* **Device Auto-Select**: CUDA → MPS → CPU, logged at startup
* **`.env` overrides** via `python-dotenv` (e.g. `DEBUG_MODE`, `MODEL_DEVICE`)
* Migration to **GitHub Projects** board; docs (`README`, `CONTRIBUTING`) updated

### v0.4.3 – Memory Integration (🏗 In Progress)
* **`utils/memory.py`** – singleton façade with `IN_MEMORY` / `NONE` back-end
* **Memory toggle & backend field** in `settings.json`
* `prepare_context()` now merges *memory* & *live* history; logs injection counts
* Placeholder `summarise_context()` scaffold (experiments)
* New dev scripts: `experiments/test_memory_on.py` & `test_memory_off.py`

> Planned sub-releases
> *v0.4.3-b* – basic context summarisation prototype
> *v0.4.3-c* – Memory stress tests & fallback refinements

---

## Upcoming

### v0.4.4 – Automated Testing & CI
* PyTest suites for context, memory, safety filters
* GitHub Actions: **ruff lint → pytest → container build**
* Coverage badge in README

### v0.5.x – Containerisation & RAG Prototype
* Podman/Docker image with GPU/CPU variants
* Minimum viable **RAG** (file-based embedding + retrieval)
* Deployment scripts for OpenShift Local

Stay tuned — each milestone will be appended here with full details upon completion. 🚀
