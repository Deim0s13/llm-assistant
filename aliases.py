import json
import logging

PROMPT_ALIASES_PATH = "prompt_aliases.json"

def load_prompt_aliases(filepath=PROMPT_ALIASES_PATH):
    """
    Load prompt aliases from a JSON file.

    Args:
        filepath (str): Path to the alias JSON file.

    Returns:
        dict: A dictionary mapping alias phrases to canonical concepts.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            aliases = json.load(f)
            logging.info(f"[Prompt Alias Loader] Loaded {len(aliases)} aliases.")
            return aliases
    except Exception as e:
        logging.error(f"[Prompt Alias Loader] Failed to load aliases: {e}")
        return {}

KEYWORD_ALIASES = load_prompt_aliases()