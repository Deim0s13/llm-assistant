# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.2.1) leverages the instruction-tuned model `google/flan-t5-small` to create a robust multi-turn conversation interface with enhanced prompt control.

## Features in Version 0.2.1

## Key Features

### • Enhanced Conversation Context

The chatbot continues to maintain multi-turn conversation history, enabling more coherent responses by incorporating previous exchanges into the prompt.

### • Externalized Prompts

- **Base Prompt** is stored in `prompt_template.txt`, enabling easy iteration on the assistant’s personality and tone.  
- **Specialized Prompts** are stored in `specialized_prompts.json` and dynamically injected based on user queries to better tailor responses (e.g., “explain like I’m five”, “give me a fun fact”).

### • Keyword-Based Prompt Switching

A new mechanism scans user input for relevant keywords and loads a specialized prompt when appropriate, overriding the base instructions for that interaction. This allows lightweight prompt engineering without hardcoding logic into the model.

### • Structured Conversation History

Exchanges are tracked using structured `role`/`content` pairs (user, assistant), improving clarity and ensuring predictable formatting across turns.

### • Tunable Generation Parameters

The Gradio interface allows real-time experimentation with the following controls:

- **Max New Tokens**  
- **Temperature**  
- **Top-p** (Nucleus Sampling)  
- **Do Sample**

These options help shape response style, creativity, and determinism for better control during development.

### • Debug Logging for Development

Debug mode (`DEBUG_MODE = True`) outputs detailed logs showing:

- Which prompt is being used  
- Full context passed to the model  
- Raw generated output  
- Token generation settings  

This allows fine-grained introspection during testing and refinement.

## Setup

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate

2. **Install dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

3. **Run the chatbot:**

   ```bash
   python main.py

This will launch a local Gradio interface in your browser

## External Files

- **prompt_template.txt:**
  Contains the base instruction for the assistant’s behavior and tone.

- **specialized_prompts.json**
  Maps trigger keywords (e.g., `“explain like I’m five”`, `“historical quote”`) to alternate system prompts used when those phrases are detected in the input.

## Testing and Experimentation

### • Generation Parameter Tuning

Use the sliders and checkbox in the Gradio interface to adjust:

- **Max New Tokens**: Suggested range: 50–200  
- **Temperature**: Range: 0.1–1.0  
- **Top-p**: Range: 0.5–1.0  
- **Do Sample**: Toggle to switch between sampling (creative) and deterministic (greedy) responses.

Test different values and note how they influence tone, accuracy, and creativity.

### • Prompt Matching Debugging

Turn on `DEBUG_MODE` to confirm when a specialized prompt is used. Matched prompts are logged with `[Prompt Match]`, and unmatched queries will fall back to the base.

### • Few-Shot Examples (in prompt_template.txt)

Simple in-context examples improve model grounding. Review and revise thse to better your use case.

## Next Steps

### • Prompt Refinement and Few-Shot Tuning

Improve the examples and phrasing in both `prompt_template.txt` and `specialized_prompts.json` for more consistent behaviours acros topics.

### • Future Enhancements

Future versions might include:

- Containerizing with **Podman**.
- Introducing **GitHub Copilot-like suggestions**  
- Fine-tuning the model with domain-specific samples.
- Adding support for **chat history saving** or **multi-user session memory**
