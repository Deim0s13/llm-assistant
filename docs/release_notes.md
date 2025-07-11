# Release Notes 📜

A chronological changelog for the **LLM‑Assistant Starter Kit**. Each entry lists the headline features, notable refactors, and links to deeper docs/tests where useful.

---

## Version Summary Table

|   Version  |       State      | Headline Highlights                                                      |
| :--------: | :--------------: | ------------------------------------------------------------------------ |
| **v0.1.0** |     ✅ *Done*     | Static base prompt, no memory, minimal Gradio UI                         |
| **v0.2.x** |     ✅ *Done*     | Multi‑turn history, specialised prompts, alias mapping, diagnostics      |
| **v0.3.0** |     ✅ *Done*     | Structured *experiments* framework & documentation re‑org                |
| **v0.4.0** |     ✅ *Done*     | Robust alias detection, fuzzy matching, improved logging                 |
| **v0.4.1** |     ✅ *Done*     | Configurable *Safety Guardrails* (profanity, sensitivity modes)          |
| **v0.4.2** |     ✅ *Done*     | Context‑window trimming, cross‑platform device detection, `.env` support |
| **v0.4.3** |     ✅ *Done*     | ⚡ **In‑Memory backend**, summarisation scaffold, first unit‑tests        |
| **v0.4.4** | 🔄 *In Progress* | 🔧 **RedisMemoryBackend**, Summarise MVP, CI pipeline                    |
| **v0.4.5** |   🔼 *Planned*   | Vector‑DB memory & RAG prototype, container images                       |

*Full diff‑by‑diff details live in `/docs/release_notes.md` for each patch series.*

---

## v0.1.0 – First Proof‑of‑Concept *(2025‑04‑05)*

* Static system prompt embedded in code.
* No history; each user turn isolated.
* Bare‑bones Gradio textbox UI.

---

## v0.2.x – From Single‑Turn to Specialised Prompts *(2025‑04‑15 → 05‑02)*

### v0.2.0

* **Conversation History** – maintains role/content pairs.
* External **`prompt_template.txt`** and tunable generation sliders.

### v0.2.1 → v0.2.5 Highlights

* **Specialised Prompt Injection** via `specialized_prompts.json`.
* **Alias Mapping** (`prompt_aliases.json`) for flexible triggers.
* **Fuzzy Matching Toggle**, **Developer Playground**, **Advanced UI**.
* Model upgrade to `google/flan‑t5‑base`.
* Continuous debug‑log refinements & bug‑fixes.

*Patch‑level notes:* `experiments/experiments_v0.2.*.md`.

---

## v0.3.0 – Experiments Framework 📊 *(2025‑05‑10)*

* Introduced **/experiments/** folder & markdown logs.
* Captured systematic tests on prompt phrasing, safety modes, token limits.
* Docs restructure: `scope.md`, `roadmap.md`, dedicated release notes.
* Insights fed into later prompt‑matching & safety design.

---

## v0.4.x Track – Stability, Safety, Memory

### v0.4.0 – Alias & Prompt Matching Overhaul *(2025‑05‑30)*

* Token‑level alias detection (`alias_in_message`).
* Expanded alias library & diagnostics (`[Prompt] …` logs).
* Clear fallback reasoning when no match found.

### v0.4.1 – Configurable Safety Guardrails *(2025‑06‑10)*

* **`settings.json → safety`**: `sensitivity_level`, `profanity_filter`.
* Modes: **strict · moderate · relaxed**.
* Runtime filtering (moderate) or blocking (strict).
* Refusal template driven by config.
* Manual tests recorded in `experiments_v0.4.1.md`.

### v0.4.2 – Context Window & Dev Hygiene *(2025‑06‑25)*

* **Context Trimming** based on `max_history_turns` & `max_prompt_tokens`.
* Debug logs show retained turns & token counts.
* **Device Auto‑Select**: CUDA → MPS → CPU, logged at startup.
* `.env` overrides via `python‑dotenv`.
* Migration to **GitHub Projects** board; docs (`README`, `CONTRIBUTING`) updated.

### v0.4.3 – Volatile Memory & Summaries *(2025‑07‑08)*

* **`memory/backends/in_memory_backend.py`** – volatile list‑based store.
* Memory toggle (`settings.json → memory.backend`).
* `prepare_context()` merges persisted turns with live chat.
* **Summarisation scaffold** – `summariser.py` placeholder + experiments.
* **PyTest** smoke suite (`tests/test_memory_basic.py`).

---

## v0.4.4 – Persistent Memory & CI *(current milestone – target 2025‑07‑30)*

| Area          | Feature                        | Notes                                                                                                  |
| ------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------ |
| **Memory**    | **`RedisMemoryBackend`**       | Saves chat turns to Redis (LPUSH/LRANGE) with max‑turn trimming and auto‑fallback to in‑process store. |
| **Dev Ops**   | **GitHub Actions CI**          | Lint (`ruff`) → tests (`pytest`) → container build on `main`.                                          |
| **Docs**      | README + Release Notes refresh | Quick‑start with Redis, directory map shows back‑ends.                                                 |
| **Summaries** | **Summarise MVP**              | `summariser.py:summarise_context()` activates when history > `MAX_TURNS`.                              |

Planned sub‑releases:

* **v0.4.4‑b** – memory stress tests with *fakeredis*.
* **v0.4.4‑c** – summarisation evaluation & token‑budget metrics.

---

## Upcoming Roadmap

### v0.4.5 – Vector Memory & RAG

* FAISS / Qdrant semantic memory backend.
* Minimum viable **RAG**: file‑based ingestion → embedding → retrieval.
* Podman/OpenShift deployment scripts.

### v0.5.x – Fine‑Tuning Playground

* LoRA / QLoRA fine‑tuning on TinyLLaMA, Mistral‑7B.
* Training metrics dashboard, checkpoint diff visualiser.

Stay tuned — each milestone will be appended here upon completion. 🚀
