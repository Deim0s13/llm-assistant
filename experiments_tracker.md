# 🧪 LLM Experiments Tracker

This file tracks all experiments conducted as part of the `feature/v0.3.0-llm-experiments` branch.

| Experiment ID | Title                         | Status  | Notes                                                         |
|:--------------|:------------------------------|:--------|:--------------------------------------------------------------|
| 1             | Prompt Engineering Basics     | Done | Explore how different phrasings change model responses        |
| 2             | Context Window Size Effects   | Done | Study how much previous history influences output             |
| 3             | Generation Parameter Tuning   | Planned | Test temperature, top-p, and max_new_tokens                   |
| 4             | Response Chaining (Self-Loop)  | Planned | Pass output back into the model for follow-up conversations   |
| 5             | Safety and Bias Exploration   | Planned | Deliberately test for hallucinations, bias, and safety issues |

---

## Progress Status

- **Planned** = Experiment idea written but not yet started
- **Active** = Currently being worked on
- **Done** = Completed with observations/notes

---

## Experiment Log

---

## Experiment ID: 1

**Title:** Prompt Engineering Basics  
**Status:** Done  
**Date:** 28 April 2025

---

### Objective

Explore how different phrasings of a user input related to "explaining photosynthesis" affect prompt matching and model output.

---

### Setup

- **Model:** `google/flan-t5-base`
- **Prompt Examples:**
  - "Explain photosynthesis"
  - "Explain photosynthesis simply"
  - "Explain photosynthesis to a 5-year-old"
  - "Explain photosynthesis as if I’m five"
- **Parameters:**
  - Max New Tokens: 100
  - Temperature: 0.5
  - Top-p: 0.9
  - Do Sample: True
- **Other Settings:**
  - Fuzzy Matching: Enabled
  - Developer Playground Panel used.

---

### Observations

| Test Input | Matched Concept | Confidence | Notes |
|:-----------|:----------------|:-----------|:------|
| Explain photosynthesis | Base Prompt Used (no match found) | N/A | Model used few-shot example from base prompt |
| Explain photosynthesis simply | Base Prompt Used (no match found) | N/A | Same fallback behaviour |
| Explain photosynthesis to a 5-year-old | Base Prompt Used (no match found) | N/A | Same fallback behaviour |
| Explain photosynthesis as if I’m five | `explain_simple` | N/A | Matched specialised prompt, but output was too technical (mentioned photons) |

**Extra Notes:**

- For all first three variations, the assistant "borrowed" from the few-shot examples inside the base prompt.
- Only the fourth phrasing ("as if I'm five") triggered the `explain_simple` specialised prompt.
- **Surprise:** The `explain_simple` specialised prompt produced a *more technical* answer instead of a child-friendly one.

---

### Insights

- The **few-shot examples** inside the base prompt heavily influence behaviour — often stronger than specialised prompt overrides.
- Specialised prompt `explain_simple` **needs improvement** — not sufficiently guiding the model toward simple language for children.
- Minor variations in phrasing (e.g., "explain simply" vs "explain like I'm five") **drastically change** the matching outcome.

---

### Next Actions

- **Improve** the `explain_simple` specialised prompt with stronger, simpler language guidance.
- **Expand** alias mappings to better catch variants like "explain simply" and "explain simply to a child."
- **Consider refining** few-shot examples in the base prompt if the goal is to encourage using specialised prompts more intentionally.

---

## Experiment ID: 2

**Title:** Context Window Size Effects  
**Status:** Done  
**Date:** 28 April 2025

---

### Objective

To observe whether prior conversation history affects the model's outputs, and whether small additions of unrelated context cause hallucination or confusion.

---

### Setup

- **Model:** `google/flan-t5-base`
- **Prompt Example:** User first asks a question unrelated to photosynthesis, and then follows up.
- **Parameters:**
  - Max New Tokens: 100
  - Temperature: 0.5
  - Top-p: 0.9
  - Do Sample: True
- **Other Settings:**
  - Context window is preserved (last several user/assistant turns are passed into each new prompt).

---

### Observations

- **Single message (`What is the capital of Germany?`)**
  - Correctly responded: **Berlin is the capital of Germany.**

- **Multiple messages (`Tell me about the Eiffel Tower. What is the capital of Germany?`)**
  - Output: **Germany is the capital of France.**
  - Hallucination — the model incorrectly confused Germany and France.

- **Separate `Tell me about the Eiffel Tower` message**
  - Output: **The Eiffel Tower is located on the Eiffel Tower in Paris, France.**
  - Minor hallucination — repetition error ("located on the Eiffel Tower").

- **Another fresh input (`What is the capital of Germany?`)**
  - Output: **Germany is located in the North Rhine.**
  - Geographic confusion — while North Rhine is a region, it’s not the capital.

---

### Insights

- Even a small increase in context (adding one prior unrelated question) can degrade factual accuracy.
- Hallucination risk increases if multiple knowledge retrievals are implicitly expected within the same context window.
- The model performs better when each question is clear and isolated, rather than bundled.
- Context history must be carefully curated when aiming for high factual precision.

---

## Next Actions

- For production-quality bots, prune unrelated history aggressively or structure memory better.
- Test tighter prompt control (e.g., system prompts reminding model to only answer the latest user message).
- Potential follow-up experiment: chain memory management improvements or "reset" context periodically.

---

## Experiment ID: 3

**Title:** Generation Parameter Tuning  
**Status:** Done  
**Date:** 29 April 2025

---

### Objective

To observe how varying individual generation parameters — temperature, top-p, max new tokens — affects response quality, style, and accuracy. Focused on the same input prompt:  
**Prompt:** "Describe the Eiffel Tower in Paris."

---

### Setup

- **Model:** `google/flan-t5-base`
- **Base Prompt:** Used (no specialized match)
- **Do Sample:** True
- **Fuzzy Matching:** Off
- **Prompt Input:** _"Describe the Eiffel Tower in Paris."_

---

### Observations

#### 🔹 Temperature Variation (Top-p = 0.9, Max Tokens = 100)

| Temperature | Output                                                                 |
|-------------|------------------------------------------------------------------------|
| 0.2         | "The Eiffel Tower is a tall building in Paris."                        |
| 0.5         | "The Eiffel Tower is a tall structure in Paris."                       |
| 0.8         | "I'm here to answer your question about the Eiffel Tower."             |

→ Higher temperature = vaguer, sometimes less informative output.

---

#### 🔹 Top-p Variation (Temp = 0.5, Max Tokens = 100)

| Top-p | Output                                                                  |
|--------|-------------------------------------------------------------------------|
| 0.7    | "The Eiffel Tower is located in Paris."                                 |
| 0.9    | "I can provide you with information about the Eiffel Tower."            |
| 1.0    | "I can provide you with information about the Eiffel Tower in Paris."   |

→ Lower top-p = more direct/factual. Higher = verbose or generic phrasing.

---

#### 🔹 Max New Tokens Variation (Temp = 0.5, Top-p = 0.9)

| Max Tokens | Output                                                       |
|------------|--------------------------------------------------------------|
| 50         | "I can help you with the Eiffel Tower in Paris."             |
| 100        | "The Eiffel Tower is a tall building in Paris."              |
| 150        | "The Eiffel Tower is located in Paris."                      |

→ More tokens didn't meaningfully increase detail (likely input too short to need it).

---

#### 🔹 Combined "Creative" Settings (Temp = 0.8, Top-p = 1.0, Max Tokens = 150)

**Output:** "The Eiffel Tower is located at Paris' Eiffel Tower and is a landmark in Paris."

→ Repetition and mild nonsense — creativity comes at the cost of coherence.

---

### Insights

- **Lower temperatures (0.2–0.5)** produce more accurate, structured responses.
- **Higher temperatures (0.8+)** increase creativity but reduce precision.
- **Top-p 0.7–0.9** yields grounded answers, but **1.0** becomes verbose/generic.
- **Max Tokens** didn’t matter much for short prompts; longer input may benefit more.
- Combined high-creative settings can cause semantic drift or hallucination.

---

### Next Actions

- Test with longer, multi-turn prompts to observe token effects more clearly.
- Try “explain” vs “summarise” prompts under varying settings.
- Begin tracking hallucinations and factual deviations under higher creativity settings.

---