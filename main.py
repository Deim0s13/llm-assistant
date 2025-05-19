import json
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr
import torch
import difflib

from utils.aliases import KEYWORD_ALIASES
from utils.prompt_utils import alias_in_message
from config.settings_loader import load_settings
from utils.safety_filters import apply_profanity_filter, evaluate_safety

# Configuration
DEBUG_MODE = True
SETTINGS = load_settings()

# Initialize the model
def initialize_model(model_name="google/flan-t5-base"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else (
        "mps" if torch.backends.mps.is_available() else "cpu"
    )
    tokenizer.pad_token = tokenizer.eos_token # Ensure pad_token is set
    model.to(device)
    logging.info(f"Model initializeed on {device}")
    return tokenizer, model, device

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load prompt resources
BASE_PROMPT_PATH = "config/prompt_template.txt"
SPECIALIZED_PROMPTS_PATH = "config/specialized_prompts.json"

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

    # Track diagnostics
    scanned_aliases = []
    match_details = []

    # Direct Alias Match
    for alias, concept in KEYWORD_ALIASES.items():
        scanned_aliases.append(alias)
        if alias_in_message(alias, tokens):  
            if concept in specialized_prompts:
                prompt = specialized_prompts[concept]
                if DEBUG_MODE:
                    logging.debug(f"[Prompt Match] Matched alias '{alias}' ➔ concept '{concept}'")
                    logging.debug(f"[Prompt Match] Prompt snippet: {prompt[:80]}...")
                return prompt, concept, None # No match scope for direct match
            else:
                match_details.append((alias, concept, "Concept not found in prompt list"))
            
    # Fuzzy Matching (Fallback)
    if fuzzy_matching_enabled:
        all_aliases = list(KEYWORD_ALIASES.keys())
        close_matches = difflib.get_close_matches(message_lower, all_aliases, n=1, cutoff=0.7)

        if close_matches:
            best_match = close_matches[0]
            similarity = difflib.SequenceMatcher(None, message_lower, best_match).ratio()
            concept = KEYWORD_ALIASES[best_match]
            if concept in specialized_prompts:
                prompt = specialized_prompts[concept]
                if DEBUG_MODE:
                    logging.debug(f"[Prompt Match Debug] Fuzzy match: '{message_lower}' ➔ '{best_match}' (Score: {similarity:.2f})")
                    logging.debug(f"[Prompt Match Debug] Fuzzy concept: '{concept}'")
                    logging.debug(f"[Prompt Match Debug] Prompt preview: {prompt[:80]}...")
                return prompt, concept, similarity
            else:
                logging.debug(f"[Prompt Match Debug] Fuzzy match concept '{concept}' not in specialized prompts")
    
    # Fallback - No Match Found
    if DEBUG_MODE:
        logging.debug(f"[Prompt Match Debug] No prompt match found (direct or fuzzy)")
        logging.debug(f"[Prompt Match Debug] Scanned aliases: {scanned_aliases} ")
        if match_details:
            logging.debug(f"[Prompt Match Debug] Skipped concepts due to missing prompt entries: {match_details}")

    return "", "base_prompt", None

# Prepare the context for the model
def prepare_context(message, history, base_prompt, specialized_prompts, fuzzy_matching_enabled):
    max_turns = SETTINGS.get("context", {}).get("max_history_turns", 5)
    max_tokens = SETTINGS.get("context", {}).get("max_prompt_tokens", 512)

    if DEBUG_MODE:
        logging.debug(f"[Context] Retaining last {max_turns} turns and {max_tokens} tokens.")

    specialized_prompt, source, _ = get_specialized_prompt(message, specialized_prompts, fuzzy_matching_enabled)
    recent_history = history[-max_turns:] if len(history) > max_turns else history

    # Build context string
    def build_context(history_slice):
        ctx = specialized_prompt if specialized_prompt else base_prompt
        for entry in history_slice:
            ctx += f"\n{entry['role'].capitalize()}: {entry['content']}"
        ctx += f"\nUser: {message}\nAssistant:"
        return ctx
    
    context = build_context(recent_history)

    # Tokenize and trim if too long
    while True:
        tokenized = tokenizer(context, return_tensors="pt", padding=False, truncation=False)
        input_ids = tokenized["input_ids"]
        num_tokens = input_ids.shape[1] if len(input_ids.shape) == 2 else input_ids.shape[0]

        if DEBUG_MODE:
            logging.debug(f"[Context] Final token count: {num_tokens} with {len(recent_history)} retained turns.")

        if num_tokens <= max_tokens or len(recent_history) <= 1:
            break
        recent_history = recent_history[1:]
        context = build_context(recent_history)

        if DEBUG_MODE:
            logging.debug(f"[Context Debug] Final retained turns: {len(recent_history)}")
            logging.debug(f"[Context Debug] Final token count: {num_tokens}")
            logging.debug("f[Context Debug] Context preview:\n{context[:400]}...")

    return context, source

# Generate model response
def chat(message, history, max_new_tokens, temperature, top_p, do_sample, fuzzy_matching_enabled):
    try:
        # Safety evaluation before prompt generation
        allowed, blocked_message = evaluate_safety(message, SETTINGS)
        if not allowed:
            if DEBUG_MODE:
                logging.debug("[Safety Debug] Message blocked by pre-generation safety filter.")
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": blocked_message})
            return history, "blocked_by_safety"
        
        context, source = prepare_context(message, history, BASE_PROMPT, SPECIALIZED_PROMPTS, fuzzy_matching_enabled)
        
        if DEBUG_MODE:
            logging.debug("[Generation Debug] Generating response with the following settings:")
            logging.debug(f"[Generation Debug] Source: {source}")
            logging.debug(f"[Generation Debug] Context preview:\n{context[:300]}...\n")
        
        input_ids = tokenizer(context, return_tensors="pt", padding=True, truncation=True).input_ids.to(device)
        generation_params = {
            "max_new_tokens": int(max_new_tokens),
            "do_sample": do_sample,
            "temperature": float(temperature),
            "top_p": float(top_p),
        }

        if DEBUG_MODE:
            logging.debug(f"[Generation Debug] Generation parameters: {generation_params}")

        output_ids = model.generate(input_ids, **generation_params)
        output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

        # Profanity filtering if applicable
        if SETTINGS.get("safety", {}).get("sensitivity_level") == "moderate":
            filtered_output = apply_profanity_filter(output_text)
            if DEBUG_MODE:
                logging.debug("[Safety Debug] Output filtered for profanity (moderate mode)")
                logging.debug(f"[Safety Debug] Filtered output: {filtered_output[:200]}...")
            output_text = filtered_output

        if DEBUG_MODE:
            logging.debug("[Generation Debug] Raw model output:")
            logging.debug(output_text[:500])

        # Add to chat history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": output_text})
        
        return history, source
    
    except Exception as e:
        logging.error(f"Error in chat function: {e}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "I encountered an error processing your request."})
        return history, "error"

# Respond function for Gradio
def respond(message, history, max_new_tokens, temperature, top_p, do_sample, fuzzy_matching_enabled, safety_level):
    SETTINGS["safety"]["sensitivity_level"] = safety_level
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

        safety_mode_dropdown = gr.Dropdown(
            choices=["strict", "moderate", "relaxed"],
            value=SETTINGS["safety"].get("sensitivity_level", "moderate"),
            label="Safety Mode [Dev]"
        )

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
        [txt, state, max_new_tokens_slider, temperature_slider, top_p_slider, do_sample_checkbox, fuzzy_match_checkbox, safety_mode_dropdown],
        [txt, chatbot, diagnostics_box]
    )


if __name__ == "__main__":

    logging.debug("🚀 Launching Gradio demo...")
    demo.launch()
