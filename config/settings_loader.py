import json
import logging
import os

DEFAULT_SETTINGS_PATH = "config/settings.json"

# Default fallback settings (in case file is missing or invalid)
FALLBACK_SETTINGS = {
        "safety": {
        "profanity_filter": True,
        "sensitivity_level": "moderate",
        "log_triggered_filters": True,
        "blocked_response_template": "I'm unable to respond to that request due to safety policies."
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
        "log_file_path": "logs/chatbot_debug.log"
    },
    "ui": {
        "enable_playground_autorun": False,
        "show_advanced_settings": True
    }
}

def load_settings(filepath: str = DEFAULT_SETTINGS_PATH) -> dict:
    """Load settings from a JSON file, falling back to defaults if needed."""
    try:
        if not os.path.exists(filepath):
            logging.warning(f"[Settings] File not found at {filepath}. Using fallback defaults.")
            return FALLBACK_SETTINGS
        
        with open(filepath, "r", encoding="utf-8") as f:
            settings = json.load(f)

        if not isinstance(settings, dict):
            raise ValueError("Settings must be a dictionary")
        
        logging.info(f"[Settings] Loaded settings from {filepath}")
        return settings
    
    except Exception as e:
        logging.error(f"[Settings] Faile to load settings from {filepath}: {e}")
        return FALLBACK_SETTINGS
