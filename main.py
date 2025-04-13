import json
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr
import torch

#Configuration constants

MODEL_NAME = "google/flan-t5-small"
BASE_PROMPT_PATH = "prompt_template.txt"
SPECIALIZED_PROMPTS_PATH = "specialized_prompts.json"
MAX_HISTORY_TURNS = 5
DEBUG_MODE = True

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load the base prompt template from an external file.
def load_base_prompt(filepath=BASE_PROMPT_PATH):
    """
    Load the base prompt template from a text file.
    
    Args:
        filepath (str): Path to the prompt template file
        
    Returns:
        str: The loaded prompt template
    """
    try:
        with open(filepath, "r") as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error loading prompt template: {e}")

# Function to load specialized prompts from a JSON file.
def load_specialized_prompts(filepath=SPECIALIZED_PROMPTS_PATH):
    """
    Load specialized prompts from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file containing specialized prompts
        
    Returns:
        dict: Dictionary of keyword-prompt pairs
    """
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading specialized prompts: {e}")
        return {}
    
# Funtion to get specialized prompt based on the user's message
def get_specialized_prompt(message, specialized_prompts):
    """
        Find a specialized prompt based on keywords in the user's message.
    
    Args:
        message (str): The user's input message
        specialized_prompts (dict): Dictionary of keyword-prompt pairs
        
    Returns:
        str: The specialized prompt if a keyword match is found, otherwise an empty string
    """
    message_lower = message.lower()
    for keyword, prompt in specialized_prompts.items():
        if keyword in message_lower:
            return prompt
    return ""

def initialized_model(model_name=MODEL_NAME):
    """
        Initialize the tokenizer and model.
    
    Args:
        model_name (str): Name of the model to load
        
    Returns:
        tuple: (tokenizer, model, device)
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model.to(device)
    logging.info(f"Model initialized on {device}")
    return tokenizer, model, device

def prepare_context(message, history, base_prompt, specialized_prompts):
    """
    Prepare the context for the model by combining the prompt and conversation history.
    
    Args:
        message (str): The user's input message
        history (list): List of previous conversation turns
        base_prompt (str): The base prompt template
        specialized_prompts (dict): Dictionary of specialized prompts
        
    Returns:
        str: The prepared context for the model
    """
    # Check for specialized prompt
    specialized_prompt = get_specialized_prompt(message, specialized_prompts)

    # Use specialized prompt if available; otherwise, use the base prompt
    context = specialized_prompt if specialized_prompt else base_prompt

    # Use only the most recent conversation if history is long
    recent_history = history[-MAX_HISTORY_TURNS:] if len(history) > MAX_HISTORY_TURNS else history

    # Append the current user message
    for entry in recent_history:
        if entry["role"] == "user":
            context += f"\nUser: {entry['content']}"
        elif entry["role"] == "assistant":
            context += f"\nAssistant: {entry['content']}"

    # Append the current user message
    context += f"\nUser: {message}\nAssistant: "

    return context

def chat(message, history, max_new_tokens, temperature, top_p, do_sample):
    """
    Process a user message and generate a response using the LLM.
    
    Args:
        message (str): The user's input message
        history (list): List of previous conversation turns
        max_new_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in generation
        top_p (float): Controls diversity via nucleus sampling
        do_sample (bool): Whether to use sampling or greedy decoding
        
    Returns:
        list: Updated conversation history with the new response
    """
    try:
        # Prepare the context for the model
        context = prepare_context(message, history, BASE_PROMPT, SPECIALIZED_PROMPTS)

        if DEBUG_MODE:
            logging.debug("Full context sent to model")
            logging.debug(context)

        # Tokenize with padding and truncation
        encoded_input = tokenizer(context, return_tensors="pt", padding=True, truncation=True)
        input_ids = encoded_input.input_ids.to(device)

        # Generation parameters from UI
        generation_params = {
            "max_new_tokens": int(max_new_tokens),
            "do_sample": do_sample,
            "temperature": float(temperature),
            "top_p": float(top_p),
        }

        output_ids = model.generate(input_ids, **generation_params)
        output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        if DEBUG_MODE:
            logging.debug("Full generated output:")
            logging.debug(output_text)

        new_response = output_text.strip()

        if DEBUG_MODE:
            logging.debug("Extracted new response:")
            logging.debug(new_response)

        if DEBUG_MODE:
            logging.debug("Generation parameters:")
            logging.debug(generation_params)

        # Update conversation history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": new_response})

        return history
    except Exception as e:
        logging.error(f"Error in chat function: {e}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "I encountered an error processing your request."})
        return history
    
def respond(message, history, max_new_tokens, temperature, top_p, do_sample):
    """
    Wrapper function for the chat function to match Gradio's expected interface.
    
    Args:
        message (str): The user's input message
        history (list): List of previous conversation turns
        max_new_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in generation
        top_p (float): Controls diversity via nucleus sampling
        do_sample (bool): Whether to use sampling or greedy decoding
        
    Returns:
        tuple: (empty string, updated history)
    """
    history = history or []
    return "", chat(message, history, max_new_tokens, temperature, top_p, do_sample)

# Load resources at startup
BASE_PROMPT = load_base_prompt()
SPECIALIZED_PROMPTS = load_specialized_prompts()

# Initialize model at startup
tokenizer, model, device = initialized_model()

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Chatbot with Tunable Generation Parameters")
    # Chatbot component displays conversation history
    chatbot = gr.Chatbot(type="messages")
    state = gr.State([])
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter your message and press Enter")
    with gr.Row():
        max_new_tokens_slider = gr.Slider(minimum=50, maximum=200, value=100, label="Max New Tokens")
        temperature_slider = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, label="Temperature")
        top_p_slider = gr.Slider(minimum=0.5, maximum=1.0, value=0.9, label="Top-p")
        do_sample_checkbox = gr.Checkbox(value=True, label="Do Sample")
    # Submit now passes 6 parameters
    txt.submit(
        respond,
        [txt, state, max_new_tokens_slider, temperature_slider, top_p_slider, do_sample_checkbox],
        [txt, chatbot]
    )

if __name__ == "__main__":
    demo.launch()