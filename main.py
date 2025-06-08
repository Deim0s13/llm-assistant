# ─────────────────────────────────────────────────────────
#  Configure logging (console + debug.log)
# ─────────────────────────────────────────────────────────
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),            # terminal
        logging.FileHandler("debug.log")    # file
    ]
)

# ─────────────────────────────────────────────────────────
#  Imports
# ─────────────────────────────────────────────────────────
import json
import difflib
import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from utils.aliases import KEYWORD_ALIASES
from utils.prompt_utils import alias_in_message
from config.settings_loader import load_settings
from utils.safety_filters import apply_profanity_filter, evaluate_safety

# ─────────────────────────────────────────────────────────
#  Globals & Helpers
# ─────────────────────────────────────────────────────────
DEBUG_MODE = True
SETTINGS = load_settings()

def count_tokens(txt: str) -> int:
    return len(tokenizer(txt, return_tensors="pt").input_ids[0])

# ─────────────────────────────────────────────────────────
#  Model initialisation (CUDA ▸ MPS ▸ CPU)
# ─────────────────────────────────────────────────────────
def initialize_model(model_name="google/flan-t5-base"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    tokenizer.pad_token = tokenizer.eos_token
    model.to(device)
    logging.debug(f"[System] Torch detected device: {device}")
    return tokenizer, model, device

# ─────────────────────────────────────────────────────────
#  Prompt-template loaders
# ─────────────────────────────────────────────────────────
BASE_PROMPT_PATH = "config/prompt_template.txt"
SPECIALIZED_PROMPTS_PATH = "config/specialized_prompts.json"

def load_base_prompt(path=BASE_PROMPT_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_specialized_prompts(path=SPECIALIZED_PROMPTS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    logging.info(f"[Prompt Loader] Loaded {len(data)} specialized prompts.")
    logging.debug(f"[Prompt Loader] Keys: {list(data.keys())}")
    return data

# ─────────────────────────────────────────────────────────
#  Prompt-matching
# ─────────────────────────────────────────────────────────
def get_specialized_prompt(message, specialized_prompts, fuzzy_enabled):
    msg = message.lower().replace("’", "'")
    tokens = msg.split()

    # Direct alias search
    for alias, concept in KEYWORD_ALIASES.items():
        if alias_in_message(alias, tokens) and concept in specialized_prompts:
            prompt = specialized_prompts[concept]
            if DEBUG_MODE:
                logging.debug(f"[Prompt Debug] Direct match '{alias}' → {concept}")
            return prompt, concept, None

    # Fuzzy fallback
    if fuzzy_enabled:
        best, score = None, 0.0
        for alias in KEYWORD_ALIASES:
            sim = difflib.SequenceMatcher(None, msg, alias).ratio()
            if sim > score and sim >= 0.7:
                best, score = alias, sim
        if best:
            concept = KEYWORD_ALIASES[best]
            if concept in specialized_prompts:
                prompt = specialized_prompts[concept]
                logging.debug(f"[Prompt Debug] Fuzzy '{best}' (score={score:.2f}) → {concept}")
                return prompt, concept, score

    logging.debug("[Prompt Debug] No prompt match (direct or fuzzy)")
    return "", "base_prompt", None

# ─────────────────────────────────────────────────────────
#  Context preparation
# ─────────────────────────────────────────────────────────
def prepare_context(msg, history, base_prompt, spec_prompts, fuzzy):
    max_turns = SETTINGS.get("context", {}).get("max_history_turns", 5)
    max_tokens = SETTINGS.get("context", {}).get("max_prompt_tokens", 512)

    def build(hist_slice):
        ctx = (spec_prompt or base_prompt)
        for entry in hist_slice:
            ctx += f"\n{entry['role'].capitalize()}: {entry['content']}"
        ctx += f"\nUser: {msg}\nAssistant:"
        return ctx

    spec_prompt, source, _ = get_specialized_prompt(msg, spec_prompts, fuzzy)
    recent = history[-max_turns:] if len(history) > max_turns else history

    raw_context = build(recent)
    before_tok = count_tokens(raw_context)

    # trim loop
    while before_tok > max_tokens and len(recent) > 1:
        recent = recent[1:]
        raw_context = build(recent)
        before_tok = count_tokens(raw_context)

    if DEBUG_MODE:
        logging.debug(
            "[Context Debug] Turns kept: %d  | Tokens: %d",
            len(recent), before_tok
        )
        if SETTINGS["logging"].get("prompt_preview", False):
            logging.debug("[Prompt Preview]\n%s\n···", raw_context[:400])

    return raw_context, source

# ─────────────────────────────────────────────────────────
#  Chat-generation
# ─────────────────────────────────────────────────────────
def chat(msg, history, max_tokens, temp, top_p, sample, fuzzy):
    allowed, block_msg = evaluate_safety(msg, SETTINGS)
    if not allowed:
        if DEBUG_MODE:
            logging.debug("[Safety Debug] Input blocked by safety filter.")
        history += [{"role": "user", "content": msg},
                    {"role": "assistant", "content": block_msg}]
        return history, "blocked"

    context, src = prepare_context(msg, history, BASE_PROMPT, SPECIALIZED_PROMPTS, fuzzy)

    gen_params = {
        "max_new_tokens": int(max_tokens),
        "do_sample": sample,
        "temperature": float(temp),
        "top_p": float(top_p),
    }

    if DEBUG_MODE:
        logging.debug("[Generation Debug] Params: %s", gen_params)

    ids_in = tokenizer(context, return_tensors="pt").input_ids.to(device)
    out_ids = model.generate(ids_in, **gen_params)
    output = tokenizer.decode(out_ids[0], skip_special_tokens=True).strip()

    # profanity filter
    if SETTINGS["safety"]["sensitivity_level"] == "moderate":
        filtered = apply_profanity_filter(output)
        if filtered != output:
            logging.debug("[Safety Debug] Profanity filter applied.")
        output = filtered

    if DEBUG_MODE:
        logging.debug("[Generation Debug] Output (preview): %s", output[:300])

    history += [{"role": "user", "content": msg},
                {"role": "assistant", "content": output}]
    return history, src

# ─────────────────────────────────────────────────────────
#  Gradio wrappers
# ─────────────────────────────────────────────────────────
def respond(msg, history, mx, temp, top_p, sample, fuzzy, safety):
    SETTINGS["safety"]["sensitivity_level"] = safety
    history = history or []
    new_hist, src = chat(msg, history, mx, temp, top_p, sample, fuzzy)
    return "", new_hist, f"Prompt source: {src}"

# (Playground unchanged)

# ─────────────────────────────────────────────────────────
#  Boot
# ─────────────────────────────────────────────────────────
BASE_PROMPT = load_base_prompt()
SPECIALIZED_PROMPTS = load_specialized_prompts()
tokenizer, model, device = initialize_model()

# ─────────────────────────────────────────────────────────
# Build Gradio UI
# ─────────────────────────────────────────────────────────
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

        # ─────────────────────────────────────────────────────────
        # 1. Button click always forces the playground to run
        # ─────────────────────────────────────────────────────────
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

        # ─────────────────────────────────────────────────────────
        # 2. Typing triggers playground ONLY if autoprivew is enabled
        # ─────────────────────────────────────────────────────────
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
