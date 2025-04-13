# LLM Chatbot Starter Kit

This project is a starting point for building an LLM-based chatbot using Hugging Face's Transformers and Gradio. The current baseline (version 0.1.0) leverages the instruction-tuned model `google/flan-t5-small` to create a robust multi-turn conversation interface.

## Features in Version 0.2.0

- **Enhanced Conversation Context:**  
  The chatbot maintains multi-turn conversation history, enabling more coherent responses by incorporating previous exchanges into the prompt.

- **Externalized Prompts:**  
  The base system prompt is stored in an external file (`prompt_template.txt`), allowing easy updates to the assistant’s initial instructions without modifying the code.

- **Dynamic Instruction Injection:**  
  Specialized prompts are stored in a JSON file (`specialized_prompts.json`) and dynamically injected based on the user's query (e.g., providing a historical quote when requested).

- **Structured Conversation History:**  
  Conversation exchanges are maintained in a structured format (using dictionaries with `role` and `content` keys), which is neatly displayed by the Gradio interface.

- **Tunable Generation Parameters:**  
  New UI controls allow you to adjust key generation parameters on the fly:

  - **Max New Tokens:** Controls the maximum number of tokens generated.
  
  - **Temperature:** Controls randomness in output (lower values yield more deterministic results, while higher values foster creativity).

  - **Top-p (Nucleus Sampling):** Adjusts how much probability mass is considered for next-token selection.
  
  - **Do Sample:** Toggle between sampling-based and deterministic generation.

  These adjustments enable real-time experimentation to refine output quality and response characteristics.

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

## Testing and Experimentation

### • Generation Parameter Tuning

Use the sliders and checkbox in the Gradio interface to adjust:

- **Max New Tokens**: Suggested range: 50–200  
- **Temperature**: Range: 0.1–1.0  
- **Top-p**: Range: 0.5–1.0  
- **Do Sample**: Toggle to switch between sampling (creative) and deterministic (greedy) responses.

Experiment by sending the same message with different parameter settings and observe changes in response length, creativity, and coherence.

### • Conversation Context Testing

Engage in multi-turn conversations to ensure that the conversation history is correctly incorporated into the prompt and that the responses reflect the desired behavior.

## Next Steps

### • Further Parameter Fine-Tuning and Prompt Refinement

Continue experimenting with the sliders and possibly update prompt content based on your observations to further improve output quality.

### • Future Enhancements

Future versions might include:

- Containerizing the application using **Podman**  
- Fine-tuning the model on a **custom dataset** for domain-specific improvements
