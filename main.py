import json
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr
import torch
import difflib
from aliases import KEYWORD_ALIASES

# Configuration constants
MODEL_NAME = "google/flan-t5-base"
BASE_PROMPT_PATH = "prompt_template.txt"
SPECIALIZED_PROMPTS_PATH = "specialized_prompts.json"
MAX_HISTORY_TURNS = 5
DEBUG_MODE = True

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load the base prompt template from an external file.
def load_base_prompt(filepath=BASE_PROMPT_PATH):
    try:
        with open(filepath, "r") as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error loading prompt template: {e}")

# Function to load specialized prompts from a JSON file.
def load_specialized_prompts(filepath=SPECIALIZED_PROMPTS_PATH):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            prompts = json.load(file)
            if not isinstance(prompts, dict):
                raise ValueError("Specialized prompts JSON must be a dictionary")
            logging.info(f"[Prompt Loader] Loaded {len(prompts)} specialized prompts.")
            logging.debug(f"[Prompt Loader] Keywords: {list(prompts.keys())}")
            return prompts
    except Exception as e:
        logging.error(f"[Prompt Loader] Error loading specialized prompts: {e}")
        return {}

# Function to get specialized prompt based on the user's message
def get_specialized_prompt(message, specialized_prompts, fuzzy_matching_enabled):
    message_lower = message.lower().replace("’", "'") # Normalise smart quotes
    tokens = message_lower.split()

    # Define token-level in-order alias matcher
        def alias_in_message(alias, message_tokens):
        alias_tokens = alias.lower().split()
        pos = 0
        for token in message_tokens:
            if token == alias_tokens[pos]:
                pos += 1
            if pos == len(alias_tokens):
                return True
            return False

    # Track diagnostics
    scanned_aliases = []
    match_details = []

    # First: Token-level alias matching
    for alias, concept in KEYWORD_ALIASES.items():
        scanned_aliases.append(alias)
        if alias_in_message(alias, message_tokens):  
            if concept in specialized_prompts:
                prompt = specialized_prompts[concept]
                if DEBUG_MODE:
                    logging.debug(f"[Prompt Match] Matched alias '{alias}' ➔ concept '{concept}'")
                    logging.debug(f"[Prompt Match] Prompt snippet: {prompt[:80]}...")
                return prompt, concept, None # No match scope for direct match
            else:
                match_details.append((alias, concept, "Concept not found in prompt list"))
            
    # Second: Fuzzy matching (fallback)
    if fuzzy_matching_enabled:
        all_aliases = list(KEYWORD_ALIASES.keys())
        close_matches = difflib.get_close_matches(message_lower, all_aliases, n=1, cutoff=0.7)

        if close_matches:
            best_match = close_matches[0]
            similarity = difflib.SequenceMatcher(None, message_lower, best_match).ratio()
            concept = KEYWORD_ALIASES[best_match]
            if concept and concept in specialized_prompts:
                prompt = specialized_prompts[concept]
                if DEBUG_MODE:
                    logging.debug(f"[Prompt Match - Fuzzy] Best fuzzy match '{best_match}' ➔ concept '{concept}'")
                    logging.debug(f"[Prompt Match - Fuzzy] Prompt snippet: {prompt[:80]}...")
                return prompt, concept, similarity
            else:
                logging.debug(f"[Prompt Match - Fuzzy] Match found but concept '{concept}' not in prompt list")
    
    # Log fallback details
    logging.debug(f"[Prompt Match - Fallback] No direct or fuzzy match found..")
    logging.debug(f"[Prompt Match - Fallback] Scanned aliasses: {scanned_aliases} ")
    if match_details:
        logging.debug(f"[Prompt Match - Diagnostics] Matched alias but missing prompt entries: {match_details}")

    return "", "base_prompt", None

# Initialize the model
def initialize_model(model_name=MODEL_NAME):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model.to(device)
    logging.info(f"Model initialized on {device}")
    return tokenizer, model, device

# Prepare the context for the model
def prepare_context(message, history, base_prompt, specialized_prompts, fuzzy_matching_enabled):
    specialized_prompt, source, _ = get_specialized_prompt(message, specialized_prompts, fuzzy_matching_enabled)
    context = specialized_prompt if specialized_prompt else base_prompt
    recent_history = history[-MAX_HISTORY_TURNS:] if len(history) > MAX_HISTORY_TURNS else history
    for entry in recent_history:
        context += f"\n{entry['role'].capitalize()}: {entry['content']}"
    context += f"\nUser: {message}\nAssistant: "
    return context, source

# Generate model response
def chat(message, history, max_new_tokens, temperature, top_p, do_sample, fuzzy_matching_enabled):
    try:
        context, source = prepare_context(message, history, BASE_PROMPT, SPECIALIZED_PROMPTS, fuzzy_matching_enabled)
        if DEBUG_MODE:
            logging.debug("Full context sent to model")
            logging.debug(context)
        input_ids = tokenizer(context, return_tensors="pt", padding=True, truncation=True).input_ids.to(device)
        generation_params = {
            "max_new_tokens": int(max_new_tokens),
            "do_sample": do_sample,
            "temperature": float(temperature),
            "top_p": float(top_p),
        }
        output_ids = model.generate(input_ids, **generation_params)
        output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        if DEBUG_MODE:
            logging.debug("Full generated output:")
            logging.debug(output_text)
            logging.debug("Extracted new response:")
            logging.debug(output_text)
            logging.debug("Generation parameters:")
            logging.debug(generation_params)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": output_text})
        return history, source
    except Exception as e:
        logging.error(f"Error in chat function: {e}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "I encountered an error processing your request."})
        return history, "error"

# Respond function for Gradio
def respond(message, history, max_new_tokens, temperature, top_p, do_sample, fuzzy_matching_enabled):
    history = history or []
    updated_history, source = chat(message, history, max_new_tokens, temperature, top_p, do_sample, fuzzy_matching_enabled)
    diagnostics = f"Prompt Source: {source}"
    return "", updated_history, diagnostics

def run_playground(test_input, max_new_tokens, temperature, top_p, do_sample, fuzzy_matching_enabled, force_run):
    """
    Simulates the specialized prompt resolution and generation pipeline.
    """
    if not force_run:
        return "","","",""

    # Updated: Now also handles fuzzy matching and match score
    prompt_text, concept, match_score = get_specialized_prompt(test_input, SPECIALIZED_PROMPTS, fuzzy_matching_enabled)
    resolved_prompt = prompt_text if prompt_text else BASE_PROMPT

    concept_display = f"{concept}" if concept != "base_prompt" else "Base Prompt Used (no match found)"

    context = f"{resolved_prompt.strip()}\nUser: {test_input.strip()}\nAssistant:"

    logging.debug("[Playground] Context used:")
    logging.debug(context)

    encoded_input = tokenizer(context, return_tensors="pt", padding=True, truncation=True)
    input_ids = encoded_input.input_ids.to(device)

    generation_params = {
        "max_new_tokens": int(max_new_tokens),
        "do_sample": do_sample,
        "temperature": float(temperature),
        "top_p": float(top_p),
    }

    output_ids = model.generate(input_ids, **generation_params)
    generation_output = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

    # Format match score nicely
    match_score_display = f"{match_score:.2f}" if match_score is not None else "N/A"

    return f"{concept_display} (Confidence: {match_score_display})", resolved_prompt.strip(), generation_output

# Load resources at startup
BASE_PROMPT = load_base_prompt()
SPECIALIZED_PROMPTS = load_specialized_prompts()
tokenizer, model, device = initialize_model()

# Build Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Chatbot with Tunable Generation Parameters")
    chatbot = gr.Chatbot(type="messages")
    state = gr.State([])
    diagnostics_box = gr.Textbox(label="Diagnostics", interactive=False)

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter your message and press Enter")

    with gr.Row():
        max_new_tokens_slider = gr.Slider(minimum=50, maximum=200, value=100, label="Max New Tokens")
        temperature_slider = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, label="Temperature")
        top_p_slider = gr.Slider(minimum=0.5, maximum=1.0, value=0.9, label="Top-p")
        do_sample_checkbox = gr.Checkbox(value=True, label="Do Sample")
        fuzzy_match_checkbox = gr.Checkbox(value=True, label="Enable Fuzzy Matching")
        autopreview_checkbox = gr.Checkbox(value=False, label="Auto-run Playground")

    with gr.Accordion("Developer Prompt Playground", open=False):
        gr.Markdown("Enter a test input to preview prompt handling and output generation.")

        test_input = gr.Textbox(
            label="Test Input Message", 
            placeholder="e.g., Can you explain gravity like I'm five?"
        )
        run_button = gr.Button("Run Playground Test")

        matched_concept = gr.Textbox(label="Matched Concept", interactive=False)
        resolved_prompt_preview = gr.Textbox(label="Resolved Prompt", lines=6, interactive=False)
        generated_preview = gr.Textbox(label="Generated Output", lines=6, interactive=False)

        # 1. Button click always forces the playground to run
        run_button.click(
            run_playground,
            inputs=[
                test_input,
                max_new_tokens_slider,
                temperature_slider,
                top_p_slider,
                do_sample_checkbox,
                fuzzy_match_checkbox,
                gr.State(True) # Force_run = True when manually clicking
            ],
            outputs=[
                matched_concept,
                resolved_prompt_preview,
                generated_preview
            ]
        )

        # 2. Typing triggers playground ONLY if autoprivew is enabled
        test_input.input(
            run_playground,
            inputs=[
                test_input,
                max_new_tokens_slider,
                temperature_slider,
                top_p_slider,
                do_sample_checkbox,
                fuzzy_match_checkbox,
                autopreview_checkbox # Conditional based on this checkbox
            ],
            outputs=[
                matched_concept,
                resolved_prompt_preview,
                generated_preview
            ]
        )

    txt.submit(
        respond,
        [txt, state, max_new_tokens_slider, temperature_slider, top_p_slider, do_sample_checkbox, fuzzy_match_checkbox],
        [txt, chatbot, diagnostics_box]
    )


if __name__ == "__main__":

    logging.debug("🚀 Launching Gradio demo...")
    demo.launch()
