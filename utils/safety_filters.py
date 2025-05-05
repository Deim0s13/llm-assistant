import re

# A small example list - replace or expand as needed
PROFANITY_LIST = ["damn", "hell", "shit", "fuck"]

def apply_profanity_filter(text: str) -> str:
    """
    Replaces known profane words in the text with asterisks or [filtered].
    """
    def mask_word(word):
        return "*" * len(word)
    
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in PROFANITY_LIST) + r')\b', flags=re.IGNORECASE)
    filtered_text = pattern.sub(lambda match: mask_word(match.group()), text)

    return filtered_text