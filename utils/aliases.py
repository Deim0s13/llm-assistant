# ════════════════════════════════════════════════════════════════════
#  utils/aliases.py – alias-to-concept mapping loader
# ════════════════════════════════════════════════════════════════════
"""
Load `config/aliases.json` and expose it as the module-level constant
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

LOGGER = logging.getLogger(__name__)  # (inherit root config set in main)

# ───────────────────────────────────────────────────────── Imports ──
import json
from pathlib import Path
from typing import Any

# ─────────────────────────────────────────── File-system helpers ──
# utils/aliases.py  →  utils/  →  project root  →  config/
_CURRENT_DIR = Path(__file__).resolve().parent
PROMPT_ALIAS_PATH = Path("config/aliases.json")


# ───────────────────────────────────────────── Loader function ──
def load_prompt_aliases(path: str | Path = PROMPT_ALIAS_PATH) -> dict[str, str]:
    """
    Return {alias_phrase: canonical_concept} mapping.

    Falls back to empty dict on error but logs the problem.
    """
    p = Path(path)
    try:
        with p.open(encoding="utf-8") as fh:
            data: Any = json.load(fh)

        if not isinstance(data, dict):
            LOGGER.error("[Aliases] %s is not a JSON object of str→str.", p)
            return {}

        aliases: dict[str, str] = {}
        for k, v in data.items():
            if not isinstance(k, str) or not isinstance(v, str):
                LOGGER.error("[Aliases] %s must map strings to strings.", p)
                return {}

        aliases = dict(data)  # safe: validated above
        LOGGER.info("[Aliases] loaded %d aliases from %s", len(aliases), p)
        return aliases

    except FileNotFoundError:
        LOGGER.info("[Aliases] no alias file at %s (using empty map).", p)
        return {}
    except Exception as exc:  # broad on purpose – file, JSON, perms, …
        LOGGER.error("[Aliases] failed to load %s – %s", p, exc)
        return {}


# ─────────────────────────────────── Module-level constant ──
KEYWORD_ALIASES: dict[str, str] = load_prompt_aliases()
