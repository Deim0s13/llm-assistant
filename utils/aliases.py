import json
import logging
import os

# Get the directory of the current file (i.e. utlis/)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to prompt_aliases.json inside utils/
PROMPT_ALIASES_PATH = os.path.join(CURRENT_DIR, "config/prompt_aliases.json")

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

# Load the aliases at module level
KEYWORD_ALIASES = load_prompt_aliases()