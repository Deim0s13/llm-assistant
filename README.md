# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.1.0) leverages the instruction-tuned model `google/flan-t5-small` to create a robust multi-turn conversation interface.

## Features in Version 0.1.0

- **Enhanced Conversation Context:**  
  The chatbot maintains multi-turn conversation history, enabling more coherent responses by incorporating previous exchanges into the prompt.

- **Externalized Prompts:**  
  The base system prompt is stored in an external file (`prompt_template.txt`), allowing easy updates to the assistant’s initial instructions without modifying the code.

- **Dynamic Instruction Injection:**  
  Specialized prompts are stored in a JSON file (`specialized_prompts.json`) and dynamically injected based on the user's query (e.g., providing a historical quote when requested).

- **Structured Conversation History:**  
  Conversation exchanges are maintained in a structured format (using dictionaries with `role` and `content` keys), which is neatly displayed by the Gradio interface.

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
  Contains the base prompt that defines the overall behaviour of the assistant

- **specialized_prompts.json**
  Contains specialised instructions keyed by certain phrases (e.g., "historical quote", "famous artist" ) that override the base prompt when applicable.

## Next Steps

- **Experiment with Generation Parameters and Prompt Engineering:**
  Enhance output quality by adding UI controls to dynamically adjust parameters such as `max_new_tokens`, `temperature`, and `top_p`.

- **Enhance Conversation Handling:**
  Improve the chat function to better manage longer dialogues or summarize earlier parts of the conversation.

- **Containerize the Application:**
  Use Podman to deploy a containerized version of the chatbot for easier distribution and scalability.
