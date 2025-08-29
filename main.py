# ════════════════════════════════════════════════════════════════════
#  main.py – Gradio chat loop, prompt pipeline & memory integration
# ════════════════════════════════════════════════════════════════════

# ───────────────────────────── Imports ─────────────────────────────

import os
import difflib
import json
import logging
from typing import Any

import gradio as gr
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from config.settings_loader import load_settings
from utils.aliases import KEYWORD_ALIASES
from utils.memory import memory
from utils.prompt_utils import alias_in_message
from utils.safety_filters import apply_profanity_filter, evaluate_safety
from utils.summariser import summarise_context

IS_CI: bool = (
    os.getenv("CI", "").lower() in ("1", "true") or os.getenv("SKIP_MODEL_INIT", "") == "1"
)

# ────────────────────────── Constants ─────────────────────────────

SIMILARITY_THRESHOLD = 0.7

# ────────────────────────── Logging Configuration ──────────────────
DEBUG_MODE: bool = True

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler("debug.log"),  # Persistent file
    ],
)

# ────────────── Globals & Initialisation (Settings, Model) ──────────────
SETTINGS: dict[str, Any] = load_settings()

_mem_cfg: dict[str, Any] = SETTINGS.get("memory", {})
logging.debug(
    "[Memory] Enabled=%s | Backend=%s",
    _mem_cfg.get("enabled", False),
    _mem_cfg.get("backend", "none"),
)


def initialize_model(model_name: str = "google/flan-t5-base") -> tuple[Any, Any, str]:
    """Load tokenizer/model and move model onto best device."""
    tok = AutoTokenizer.from_pretrained(model_name)  # type: ignore[attr-defined]
    mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)  # type: ignore[attr-defined]
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    tok.pad_token = tok.eos_token  # type: ignore[attr-defined]
    mdl.to(device)  # type: ignore[attr-defined]
    logging.debug("[System] Torch device → %s", device)
    return tok, mdl, device


BASE_PROMPT_PATH: str = "config/prompt_template.txt"
SPECIALIZED_PROMPTS_PATH: str = "config/specialized_prompts.json"


def load_base_prompt(path: str = BASE_PROMPT_PATH) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def load_specialized_prompts(path: str = SPECIALIZED_PROMPTS_PATH) -> dict[str, str]:
    with open(path, encoding="utf-8") as fh:
        data: dict[str, str] = json.load(fh)
    logging.info("[Prompt] Loaded %d specialised prompts", len(data))
    return data


# ─────────────── Memory Helper ───────────────


def _memory_turns(max_turns: int, session: str = "default") -> list[dict[str, Any]]:
    """Return last `max_turns` messages from Memory (or [])."""
    if not SETTINGS["memory"]["enabled"]:
        return []
    return memory.load(session)[-max_turns:]


# ─────────────── Prompt Selection ───────────────


def get_specialized_prompt(
    msg: str, prompts: dict[str, str], fuzzy: bool
) -> tuple[str, str, float | None]:
    """
    Return (prompt_text, concept, match_score|None).
    If no match → ("", "base_prompt", None)
    """
    norm: str = msg.lower().replace("’", "'")
    tokens: list[str] = norm.split()

    # direct alias
    for alias, concept in KEYWORD_ALIASES.items():
        if alias_in_message(alias, tokens) and concept in prompts:
            logging.debug("[Prompt] Direct '%s' → %s", alias, concept)
            return prompts[concept], concept, None

    # fuzzy alias
    if fuzzy:
        best: str | None = None
        score: float = 0.0
        for alias in KEYWORD_ALIASES:
            sim = difflib.SequenceMatcher(None, norm, alias).ratio()
            if sim > score and sim >= SIMILARITY_THRESHOLD:
                best, score = alias, sim
        if best and KEYWORD_ALIASES[best] in prompts:
            concept = KEYWORD_ALIASES[best]
            logging.debug("[Prompt] Fuzzy '%s' (%.2f) → %s", best, score, concept)
            return prompts[concept], concept, score

    logging.debug("[Prompt] No prompt match")
    return "", "base_prompt", None


# ─────────────── Context Preparation ───────────────


def prepare_context(
    msg: str,
    history: list[dict[str, Any]],
    base_prompt: str,
    spec_prompts: dict[str, str],
    fuzzy: bool,
) -> tuple[str, str]:
    """
    Build the full prompt string that is passed to the model.
    """
    max_turns: int = SETTINGS["context"]["max_history_turns"]
    max_tokens: int = SETTINGS["context"]["max_prompt_tokens"]

    spec_prompt, src, _ = get_specialized_prompt(msg, spec_prompts, fuzzy)

    session_id: str = "default"
    mem_turns: list[dict[str, Any]] = _memory_turns(max_turns)
    live_turns: list[dict[str, Any]] = history[-max_turns:]
    combined: list[dict[str, Any]] = (mem_turns + live_turns)[-max_turns:]

    # ── Summarisation trigger & injection (replace oldest with a single summary) ──
    summ_cfg = SETTINGS.get("summarisation", {})
    summ_enabled: bool = bool(summ_cfg.get("enabled", True))
    min_summary_turns: int = int(summ_cfg.get("min_turns", 8))
    summ_strategy: str = str(summ_cfg.get("strategy", "brief"))
    max_summary_chars: int = int(summ_cfg.get("max_chars", 512))

    total_context_str: str = " ".join(t.get("content", "") for t in combined)
    trigger_by_turns: bool = len(combined) >= min_summary_turns
    trigger_by_tokens: bool = bool(summ_cfg.get("trigger_by_tokens", False)) and count_tokens(
        total_context_str
    ) > int(summ_cfg.get("max_context_tokens", 2000))

    summary_text: str | None = None
    if summ_enabled and (trigger_by_turns or trigger_by_tokens):
        if summ_strategy not in {"brief", "bullet"}:
            logging.warning(
                "[Summary] Unknown strategy '%s', falling back to 'brief'",
                summ_strategy,
            )
            summ_strategy = "brief"

        produced = summarise_context(
            combined, style=summ_strategy, max_chars=max_summary_chars
        ).strip()
        if produced:
            summary_text = produced
            summary_turn = {"role": "summary", "content": summary_text}
            # Keep a compressed tail (e.g., half the turns) and prepend summary
            keep_count = max(1, len(combined) // 2)
            tail = combined[-keep_count:]
            combined = [summary_turn] + tail
            logging.debug(
                "[Summary] Injected summary (trigger: %s), turns=%d, chars=%d",
                "turns" if trigger_by_turns else "tokens",
                len(combined),
                len(summary_text),
            )

    if DEBUG_MODE:
        logging.debug(
            "[Memory] session=%s | injected=%d | live=%d | combined=%d",
            session_id,
            len(mem_turns),
            len(live_turns),
            len(combined),
        )

    def build(hist_slice: list[dict[str, Any]]) -> str:
        ctx: str = spec_prompt or base_prompt
        for turn in hist_slice:
            if turn["role"] == "summary":
                # Summary content is already formatted with bullets, include directly
                ctx += f"\n{turn['content']}"
            else:
                ctx += f"\n{turn['role'].capitalize()}: {turn['content']}"
        ctx += f"\nUser: {msg}\nAssistant:"
        return ctx

    # Build then trim to token budget, preserving summary if present
    context: str = build(combined)
    tok_ct: int = count_tokens(context)

    while tok_ct > max_tokens and len(combined) > 1:
        if summary_text is not None and combined and combined[0].get("role") == "summary":
            # preserve summary at index 0, drop next-oldest
            combined = [combined[0]] + combined[2:]
        else:
            combined = combined[1:]
        context = build(combined)
        tok_ct = count_tokens(context)

    if DEBUG_MODE:
        logging.debug("[Context] kept=%d tokens=%d", len(combined), tok_ct)

    return context, src


# ─────────────── Chat Generation ───────────────


def chat(  # noqa: PLR0913
    msg: str,
    history: list[dict[str, Any]],
    mx: int,
    temp: float,
    top_p: float,
    sample: bool,
    fuzzy: bool,
) -> tuple[list[dict[str, Any]], str]:
    allowed, block_msg = evaluate_safety(msg, SETTINGS)
    if not allowed:
        logging.debug("[Safety] blocked input")
        history += [
            {"role": "user", "content": msg},
            {"role": "assistant", "content": block_msg},
        ]
        return history, "blocked"

    ctx, src = prepare_context(msg, history, BASE_PROMPT, SPECIALIZED_PROMPTS, fuzzy)

    gen_cfg: dict[str, Any] = {
        "max_new_tokens": int(mx),
        "do_sample": sample,
        "temperature": float(temp),
        "top_p": float(top_p),
    }
    logging.debug("[Gen] %s", gen_cfg)

    # Check if tokenizer and model are available
    if tokenizer is None or model is None:
        return history, "Model not available"

    ids = tokenizer(ctx, return_tensors="pt").input_ids.to(device)
    out = model.generate(ids, **gen_cfg)
    text = tokenizer.decode(out[0], skip_special_tokens=True).strip()

    if SETTINGS["safety"]["sensitivity_level"] == "moderate":
        text = apply_profanity_filter(text)

    memory.save({"role": "user", "content": msg})
    memory.save({"role": "assistant", "content": text})

    history += [
        {"role": "user", "content": msg},
        {"role": "assistant", "content": text},
    ]
    return history, src


# ─────────────── Gradio Wrappers ───────────────


def respond(  # noqa: PLR0913
    msg: str,
    history: list[dict[str, Any]],
    mx: int,
    temp: float,
    top_p: float,
    sample: bool,
    fuzzy: bool,
    safety: str,
) -> tuple[str, list[dict[str, Any]], str]:
    SETTINGS["safety"]["sensitivity_level"] = safety
    history = history or []
    new_hist, src = chat(msg, history, mx, temp, top_p, sample, fuzzy)
    return "", new_hist, f"Prompt source: {src}"

# ─────────────── Boot Phase ───────────────

BASE_PROMPT: str = load_base_prompt()
SPECIALIZED_PROMPTS: dict[str, str] = load_specialized_prompts()

tokenizer = None
model = None
device = "cpu"

if not IS_CI:
    tokenizer, model, device = initialize_model()


def count_tokens(text: str) -> int:
    """Token count with a safe fallback when tokenizer isn't initialized (CI)."""
    if tokenizer is None:  # CI/import-safe fallback
        return max(1, len(text.split()))
    return len(tokenizer(text, return_tensors="pt").input_ids[0])

# ─────────────── Playground Helper ───────────────


def run_playground(  # noqa: PLR0913
    test_in: str,
    mx: int,
    temp: float,
    top_p: float,
    sample: bool,
    fuzzy: bool,
    force: bool,
) -> tuple[str, str, str]:
    if not force:
        return "", "", ""
    ptxt, concept, score = get_specialized_prompt(test_in, SPECIALIZED_PROMPTS, fuzzy)
    prompt = ptxt or BASE_PROMPT
    ctx = f"{prompt}\nUser: {test_in}\nAssistant:"
    
    # Check if tokenizer and model are available
    if tokenizer is None or model is None:
        return "Model not available", prompt, ""
    
    ids = tokenizer(ctx, return_tensors="pt").input_ids.to(device)
    preview = tokenizer.decode(
        model.generate(
            ids,
            max_new_tokens=int(mx),
            do_sample=sample,
            temperature=float(temp),
            top_p=float(top_p),
        )[0],
        skip_special_tokens=True,
    ).strip()
    score_s = f"{score:.2f}" if score else "N/A"
    return f"{concept} (conf {score_s})", prompt, preview


# ─────────────── Gradio UI ───────────────

with gr.Blocks() as demo:
    gr.Markdown("# Chatbot with Tunable Generation Parameters")

    chatbot = gr.Chatbot(type="messages")
    state = gr.State([])
    diag_box = gr.Textbox(label="Diagnostics", interactive=False)

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter your message and press Enter")

    # sliders & toggles
    with gr.Row():
        mx_slider = gr.Slider(50, 200, value=100, label="Max New Tokens")
        t_slider = gr.Slider(0.1, 1.0, value=0.5, label="Temperature")
        top_p_slider = gr.Slider(0.5, 1.0, value=0.9, label="Top-p")
        sample_chk = gr.Checkbox(True, label="Do Sample")
        fuzzy_chk = gr.Checkbox(True, label="Enable Fuzzy")
        auto_chk = gr.Checkbox(False, label="Auto-run Playground")

    # playground
    with gr.Accordion("Developer Prompt Playground", open=False):
        test_in = gr.Textbox(label="Test Input")
        run_btn = gr.Button("Run Test")

        matched = gr.Textbox(label="Matched Concept", interactive=False)
        prompt_p = gr.Textbox(label="Resolved Prompt", lines=6, interactive=False)
        gen_prev = gr.Textbox(label="Generated Preview", lines=6, interactive=False)

        safety_dd = gr.Dropdown(
            ["strict", "moderate", "relaxed"],
            value=SETTINGS["safety"]["sensitivity_level"],
            label="Safety Mode (Dev)",
        )

        # manual run
        run_btn.click(
            run_playground,
            [
                test_in,
                mx_slider,
                t_slider,
                top_p_slider,
                sample_chk,
                fuzzy_chk,
                gr.State(True),
            ],
            [matched, prompt_p, gen_prev],
        )

        # auto preview
        test_in.input(
            run_playground,
            [
                test_in,
                mx_slider,
                t_slider,
                top_p_slider,
                sample_chk,
                fuzzy_chk,
                auto_chk,
            ],
            [matched, prompt_p, gen_prev],
        )

    # main submit
    txt.submit(
        respond,
        [
            txt,
            state,
            mx_slider,
            t_slider,
            top_p_slider,
            sample_chk,
            fuzzy_chk,
            safety_dd,
        ],
        [txt, chatbot, diag_box],
    )

# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.debug("Launching Gradio demo...")
    demo.launch()
