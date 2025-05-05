import re

# A small example list - replace or expand as needed
PROFANITY_LIST = ["damn", "hell", "shit", "fuck"]

def apply_profanity_filter(text: str) -> str:
    """
    Replaces known profane words in the text with asterisks.
    """
    def mask_word(word):
        return "*" * len(word)
    
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in PROFANITY_LIST) + r')\b', flags=re.IGNORECASE)
    filtered_text = pattern.sub(lambda match: mask_word(match.group()), text)

    return filtered_text

def evaluate_safety(message: str, settings: dict) -> tuple[bool, str | None]:
    """
    Evaluates the input message against basic safety checks (e.g., profanity).
    Returns (allowed: bool, message: Optional[str]) — where message is a blocked response if not allowed.
    """
    safety_config = settings.get("safety", {})
    profanity_filter = safety_config.get("profanity_filter", False)
    log_triggers = safety_config.get("log_triggered_filters", False)
    refusal_template = safety_config.get("blocked_response_template", "Your message was blocked due to safety settings.")

    if profanity_filter:
        for bad_word in PROFANITY_LIST:
            pattern = re.compile(rf"\b({re.escape(bad_word)})\b", re.IGNORECASE)
            if pattern.search(message):
                if log_triggers:
                    import logging
                    logging.debug(f"[Safety] Profanity detected in input: '{bad_word}'")
                return False, refusal_template
            
    return True, None