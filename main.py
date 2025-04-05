import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr
import torch

# Function to load the base prompt template from an external file.
def load_base_prompt(filepath="prompt_template.txt"):
    try:
        with open(filepath, "r") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error loading prompt template: {e}")
        return ""

# Function to load specialized prompts from a JSON file.
def load_specialized_prompts(filepath="specialized_prompts.json"):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading specialized prompts: {e}")
        return {}

# Function to get a specialized prompt based on the user's message.
def get_specialized_prompt(message, specialized_prompts):
    message_lower = message.lower()
    # Iterate through the keywords in the specialized prompts.
    for keyword, prompt in specialized_prompts.items():
        if keyword in message_lower:
            return prompt
    return ""

# Load the specialized prompts once at startup.
SPECIALIZED_PROMPTS = load_specialized_prompts()

# Use an instruction-tuned model: google/flan-t5-small.
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Use Apple's MPS if available, otherwise CPU.
device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)

def chat(message, history):
    # Load the base prompt from the external file.
    base_prompt = load_base_prompt()
    # Check for a specialized prompt based on the user's message.
    specialized_prompt = get_specialized_prompt(message, SPECIALIZED_PROMPTS)
    
    # Use the specialized prompt if available; otherwise, use the base prompt.
    if specialized_prompt:
        context = specialized_prompt
    else:
        context = base_prompt
    
    # Append previous conversation history.
    for entry in history:
        if entry["role"] == "user":
            context += f"\nUser: {entry['content']}"
        elif entry["role"] == "assistant":
            context += f"\nAssistant: {entry['content']}"
    
    # Append the current user message.
    context += f"\nUser: {message}\nAssistant: "
    
    print("DEBUG: Full context sent to model:")
    print(context)
    
    # Tokenize the context with padding and truncation.
    encoded_input = tokenizer(context, return_tensors="pt", padding=True, truncation=True)
    input_ids = encoded_input.input_ids.to(device)
    
    # Set generation parameters from UI inputs.
    generation_params = {
        "max_new_tokens": int(max_new_tokens),
        "do_sample": do_sample,
        "temperature": float(temperature),
        "top_p": float(top_p),
    }
    
    output_ids = model.generate(input_ids, **generation_params)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    print("DEBUG: Full generated output:")
    print(output_text)
    
    # For seq2seq models like Flan-T5, assume the entire output is the new response.
    new_response = output_text.strip()
    print("DEBUG: Extracted new response:")
    print(new_response)
    
    # Update conversation history.
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": new_response})
    
    return history

def respond(message, history):
    history = history or []
    updated_history = chat(message, history)
    return "", updated_history

# Build the Gradio interface.
with gr.Blocks() as demo:
    gr.Markdown("# Enhanced Chatbot with External Prompt Templates")

    # Chatbot component for displaying structure conversation history
    chatbot = gr.Chatbot(type="messages")
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter your message and press Enter")
    txt.submit(respond, [txt, state], [txt, chatbot])

    # Add sliders and checkbox for generation parameters
    with gr.Row():
        max_new_tokens_slider = gr.Slider(minimum=50, maximum=200, value=100, label="Max New Tokens")
        temperature_slider = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, label="Temperature")
        top_p_slider = gr.Slider(minimum=0.5, maximum=1.0, value=0.9, label="Top-p")
        do_sample_checkbox = gr.Checkbox(value=True, label="Do Sample")

    txt.submit(
        respond,
        [txt, state, max_new_tokens_slider, temperature_slider, top_p_slider, do_sample_checkbox],
        [txt, chatbot]
    )

# Launch locally.
demo.launch()