# ════════════════════════════════════════════════════════════════════
#  main.py – Gradio chat loop, prompt pipeline & memory integration
# ════════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────── Logging ──
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),            # console
        logging.FileHandler("debug.log")    # persistent file
    ],
)

# ───────────────────────────────────────────────────────── Imports ──
import json, difflib, gradio as gr, torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from utils.aliases        import KEYWORD_ALIASES
from utils.prompt_utils   import alias_in_message
from utils.safety_filters import apply_profanity_filter, evaluate_safety
from utils.memory         import memory, MemoryBackend
from config.settings_loader import load_settings

# ─────────────────────────────────────────── Globals / Helpers ──
DEBUG_MODE  = True
SETTINGS    = load_settings()

def count_tokens(text: str) -> int:
    """Return #tokens a string yields with current tokenizer."""
    return len(tokenizer(text, return_tensors="pt").input_ids[0])

# ─────────────────────────────────── Model initialisation ──
def initialize_model(model_name: str = "google/flan-t5-base"):
    """Load tokenizer/model and move model onto best device."""
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    tok.pad_token = tok.eos_token
    mdl.to(device)
    logging.debug("[System] Torch device → %s", device)
    return tok, mdl, device

# ───────────────────────────────────── Prompt-file loaders ──
BASE_PROMPT_PATH         = "config/prompt_template.txt"
SPECIALIZED_PROMPTS_PATH = "config/specialized_prompts.json"

def load_base_prompt(path=BASE_PROMPT_PATH) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()

def load_specialized_prompts(path=SPECIALIZED_PROMPTS_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    logging.info("[Prompt] Loaded %d specialised prompts", len(data))
    return data

# ─────────────────────────────── Memory convenience helper ──
def _memory_turns(max_turns: int, session: str = "default") -> list[dict]:
    """Return last `max_turns` messages from Memory (or [])."""
    if not SETTINGS["memory"]["enabled"]:
        return []
    return memory.load(session)[-max_turns:]

# ─────────────────────────────── Prompt-selection logic ──
def get_specialized_prompt(msg: str, prompts: dict, fuzzy: bool):
    """Return (prompt_text, concept, match_score|None).  Empty if base."""
    norm = msg.lower().replace("’", "'")
    tokens = norm.split()

    # direct alias
    for alias, concept in KEYWORD_ALIASES.items():
        if alias_in_message(alias, tokens) and concept in prompts:
            ptxt = prompts[concept]
            logging.debug("[Prompt] Direct '%s' → %s", alias, concept)
            return ptxt, concept, None

    # fuzzy alias
    if fuzzy:
        best, score = None, 0.0
        for alias in KEYWORD_ALIASES:
            sim = difflib.SequenceMatcher(None, norm, alias).ratio()
            if sim > score and sim >= 0.7:
                best, score = alias, sim
        if best and KEYWORD_ALIASES[best] in prompts:
            concept = KEYWORD_ALIASES[best]
            logging.debug("[Prompt] Fuzzy '%s' (%.2f) → %s", best, score, concept)
            return prompts[concept], concept, score

    logging.debug("[Prompt] No prompt match")
    return "", "base_prompt", None

# ─────────────────────────────────── Context preparation ──
def prepare_context(msg, history, base_prompt, spec_prompts, fuzzy):
    max_turns  = SETTINGS["context"]["max_history_turns"]
    max_tokens = SETTINGS["context"]["max_prompt_tokens"]

    spec_prompt, src, _ = get_specialized_prompt(msg, spec_prompts, fuzzy)

    mem_turns  = _memory_turns(max_turns)          # from Memory
    live_turns = history[-max_turns:]              # on-screen chat
    combined   = (mem_turns + live_turns)[-max_turns:]

    def build(hist_slice):
        ctx = spec_prompt or base_prompt
        for turn in hist_slice:
            ctx += f"\n{turn['role'].capitalize()}: {turn['content']}"
        ctx += f"\nUser: {msg}\nAssistant:"
        return ctx

    context = build(combined)
    tok_ct  = count_tokens(context)

    # trim until within token budget
    while tok_ct > max_tokens and len(combined) > 1:
        combined = combined[1:]
        context  = build(combined)
        tok_ct   = count_tokens(context)

    if DEBUG_MODE:
        logging.debug("[Context] kept=%d tokens=%d", len(combined), tok_ct)

    return context, src

# ───────────────────────────────────── Chat generation ──
def chat(msg, history, mx, temp, top_p, sample, fuzzy):
    allowed, block_msg = evaluate_safety(msg, SETTINGS)
    if not allowed:
        logging.debug("[Safety] blocked input")
        history += [{"role": "user", "content": msg},
                    {"role": "assistant", "content": block_msg}]
        return history, "blocked"

    ctx, src = prepare_context(msg, history, BASE_PROMPT, SPECIALIZED_PROMPTS, fuzzy)

    gen = {"max_new_tokens": int(mx), "do_sample": sample,
           "temperature": float(temp), "top_p": float(top_p)}
    logging.debug("[Gen] %s", gen)

    ids = tokenizer(ctx, return_tensors="pt").input_ids.to(device)
    out = tokenizer.decode(model.generate(ids, **gen)[0], skip_special_tokens=True).strip()

    if SETTINGS["safety"]["sensitivity_level"] == "moderate":
        out = apply_profanity_filter(out)

    memory.save({"role": "user", "content": msg})
    memory.save({"role": "assistant", "content": out})

    history += [{"role": "user", "content": msg},
                {"role": "assistant", "content": out}]
    return history, src

# ─────────────────────────────────────── Gradio wrapper ──
def respond(msg, history, *slider_vals):
    mx, temp, top_p, sample, fuzzy, safety = slider_vals
    SETTINGS["safety"]["sensitivity_level"] = safety
    history = history or []
    new_hist, src = chat(msg, history, mx, temp, top_p, sample, fuzzy)
    return "", new_hist, f"Prompt source: {src}"

# ───────────────────────────────────────────── Boot phase ──
BASE_PROMPT          = load_base_prompt()
SPECIALIZED_PROMPTS  = load_specialized_prompts()
tokenizer, model, device = initialize_model()

# (Playground + Gradio UI definition – unchanged from previous version)

if __name__ == "__main__":
    logging.debug("🚀 Launching Gradio demo …")
    demo.launch()
