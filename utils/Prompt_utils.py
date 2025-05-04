# utils.py

def alias_in_message(alias, message_tokens):
    alias_tokens = alias.lower().split()
    pos = 0
    for token in message_tokens:
        if token == alias_tokens[pos]:
            pos += 1
        if pos == len(alias_tokens):
            return True
    return False