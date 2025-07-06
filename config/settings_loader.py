"""
settings_loader.py  –  centralised settings utility

• loads config/settings.json
• falls back to hard-coded defaults when the file is missing/invalid
• applies optional overrides from a .env file (python-dotenv)

The resulting dict can be imported anywhere in the project:
    from config.settings_loader import load_settings
    SETTINGS = load_settings()
"""

from dotenv import load_dotenv
import json
import logging
import os

#  ───────────────────────────────  Paths & defaults ───────────────────────────────

DEFAULT_SETTINGS_PATH = "config/settings.json"

FALLBACK_SETTINGS = {
    "safety": {
        "profanity_filter": True,
        "sensitivity_level": "moderate",
        "log_triggered_filters": True,
        "blocked_response_template": "I'm unable to respond to that request due to safety policies."
    },
    "memory": {                     # ← new default block
        "backend": "none",          # "in_memory", "redis", …
        "enabled": False
    },
    "prompt_matching": {
        "fuzzy_matching_enabled": True,
        "fuzzy_cutoff": 0.7,
        "enable_alias_diagnostics": True
    },
    "generation": {
        "max_new_tokens": 100,
        "temperature": 0.5,
        "top_p": 0.9,
        "do_sample": True
    },
    "logging": {
        "debug_mode": True,
        "log_level": "DEBUG",
        "log_to_file": False,
        "log_file_path": "logs/chatbot_debug.log",
        "prompt_preview": False
    },
    "ui": {
        "enable_playground_autorun": False,
        "show_advanced_settings": True
    },
    "context": {
        "max_history_turns": 5,
        "max_prompt_tokens": 512
    }
}

#  ───────────────────────────────  Loader   ───────────────────────────────

def load_settings(filepath: str = DEFAULT_SETTINGS_PATH) -> dict:
    """Load settings from JSON and apply .env overrides."""
    load_dotenv()  # make .env variables available via os.getenv

    #  ─────────────────────────────── read file or fall back ───────────────────────────────

    try:
        if not os.path.exists(filepath):
            logging.warning("[Settings] %s not found – using defaults", filepath)
            settings = FALLBACK_SETTINGS.copy()
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                settings = json.load(f)
            if not isinstance(settings, dict):
                raise ValueError("settings.json must contain a JSON object")
            logging.info("[Settings] Loaded from %s", filepath)
    except Exception as e:
        logging.error("[Settings] Failed to load %s: %s – using defaults", filepath, e)
        settings = FALLBACK_SETTINGS.copy()

    #  ─────────────────────────────── .env overrides #  ───────────────────────────────

    def env_bool(name: str, default: bool) -> bool:
        val = os.getenv(name)
        return default if val is None else val.lower() == "true"

    # logging
    settings["logging"]["debug_mode"] = env_bool("DEBUG_MODE", settings["logging"]["debug_mode"])
    # context
    if (v := os.getenv("MAX_HISTORY_TURNS")):
        settings.setdefault("context", {})["max_history_turns"] = int(v)
    # memory backend / enable
    mem_backend = os.getenv("MEMORY_BACKEND")
    mem_enabled = os.getenv("MEMORY_ENABLED")
    if mem_backend:
        settings.setdefault("memory", {})["backend"] = mem_backend
    if mem_enabled is not None:
        settings.setdefault("memory", {})["enabled"] = mem_enabled.lower() == "true"

   #  ─────────────────────────────── debug prints ───────────────────────────────

    logging.debug("[Settings] DEBUG_MODE = %s", settings["logging"]["debug_mode"])
    logging.debug("[Settings] MAX_HISTORY_TURNS = %s", settings["context"]["max_history_turns"])
    logging.debug("[Settings] MEMORY backend = %s | enabled = %s",
                  settings["memory"]["backend"], settings["memory"]["enabled"])

    return settings
