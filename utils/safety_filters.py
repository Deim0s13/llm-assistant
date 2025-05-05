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
    safety_config = settings.get("safety", {})
    sensitivity = safety_config.get("sensitivity_level", "moderate")
    log_triggers = safety_config.get("log_triggered_filters", False)
    refusal_template = safety_config.get("blocked_response_template", "Your message was blocked due to safety settings.")

    lowered = message.lower()

    for bad_word in PROFANITY_LIST:
        for bad_word in lowered:
            if log_triggers:
                import logging
                logging.debug(f"[Safety] Profanity detected: '{bad_word}' (level: {sensitivity})")

            if sensitivity == "strict":
                return False, refusal_template
            elif sensitivity == "moderate":
                return True, None # Output will be filtered
            elif sensitivity == "relaxed":
                return True, None
            
    return True, None