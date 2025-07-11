# ════════════════════════════════════════════════════════════════════
#  utils/aliases.py – alias-to-concept mapping loader
# ════════════════════════════════════════════════════════════════════
"""
Load `prompt_aliases.json` and expose it as the module-level constant
`KEYWORD_ALIASES`.

Each alias string → canonical concept (key that matches
`specialized_prompts.json`).

Example
-------
>>> from utils.aliases import KEYWORD_ALIASES
>>> KEYWORD_ALIASES["explain like i'm five"]
'explain_simple'
"""

# ───────────────────────────────────────────────────────── Logging ──
import logging
logging.getLogger(__name__)         # (inherit root config set in main)

# ───────────────────────────────────────────────────────── Imports ──
import json, os
from pathlib import Path

# ─────────────────────────────────────────── File-system helpers ──
# utils/aliases.py  →  utils/  →  project root  →  config/
_CURRENT_DIR = Path(__file__).resolve().parent
PROMPT_ALIAS_PATH = (_CURRENT_DIR / ".." / "config" / "prompt_aliases.json").resolve()

# ───────────────────────────────────────────── Loader function ──
def load_prompt_aliases(path: str | Path = PROMPT_ALIAS_PATH) -> dict:
    """
    Return {alias_phrase: canonical_concept} mapping.

    Falls back to empty dict on error but logs the problem.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            aliases = json.load(fh)
        logging.info("[Aliases] loaded %d aliases from %s", len(aliases), path)
        return aliases
    except Exception as exc:  # broad on purpose – file, JSON, perms, …
        logging.error("[Aliases] failed to load %s – %s", path, exc)
        return {}

# ─────────────────────────────────── Module-level constant ──
KEYWORD_ALIASES: dict[str, str] = load_prompt_aliases()
