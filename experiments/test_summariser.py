# ════════════════════════════════════════════════════════════════════
#  tests/test_summariser.py – unit tests for context summarisation
# ════════════════════════════════════════════════════════════════════

from utils.summariser import summarise_context

# ──────────────────────── Test Data Fixtures ───────────────────────

SHORT_HISTORY = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there."},
]

ENOUGH_TURNS = [
    {"role": "user", "content": "First question."},
    {"role": "assistant", "content": "First answer."},
    {"role": "user", "content": "Second question, more detail here!"},
    {"role": "assistant", "content": "Second answer."},
    {"role": "user", "content": "Third question?"},
    {"role": "assistant", "content": "Third answer."},
    {"role": "user", "content": "Fourth question! Extra punctuation!!!"},
    {"role": "assistant", "content": "Fourth answer."},
    {"role": "user", "content": "Fifth user turn to test trimming and limits."},
]

NO_USER_TURNS = [
    {"role": "assistant", "content": "Just the bot talking."},
    {"role": "assistant", "content": "Still just the bot."},
]

# ──────────────────────────── Unit Tests ───────────────────────────


def test_empty_history() -> None:
    assert "no prior context" in summarise_context([])


def test_short_history_returns_placeholder() -> None:
    result = summarise_context(SHORT_HISTORY)
    assert "no prior context" in result


def test_no_user_turns() -> None:
    result = summarise_context(NO_USER_TURNS)
    assert "no user turns" in result


def test_enough_turns_gives_bullets() -> None:
    result = summarise_context(ENOUGH_TURNS)
    # Should produce up to 3 bullets
    lines = [line for line in result.splitlines() if line.startswith("• ")]
    assert 1 <= len(lines) <= 3
    # Bullets should match last few user turns
    assert lines[-1].startswith("• Fifth user turn")
    assert all(len(line) <= 122 for line in lines)  # bullet + char limit


def test_bullet_trimming_and_format() -> None:
    custom_history = [
        {"role": "user", "content": "A" * 200},
        {"role": "user", "content": "B" * 200},
        {"role": "user", "content": "C" * 200},
        {"role": "user", "content": "D" * 200},
        {"role": "user", "content": "E" * 200},
        {"role": "user", "content": "F" * 200},
        {"role": "user", "content": "G" * 200},
        {"role": "user", "content": "H" * 200},
        {"role": "user", "content": "I" * 200},
    ]
    result = summarise_context(custom_history)
    lines = [line for line in result.splitlines() if line.startswith("• ")]
    # Should be 3 bullets, each trimmed to 120 + "• " chars
    assert len(lines) == 3
    for line in lines:
        assert len(line) == 122


def test_ignore_assistant_lines() -> None:
    history = [
        {"role": "user", "content": "User 1."},
        {"role": "assistant", "content": "Assistant 1."},
        {"role": "user", "content": "User 2."},
        {"role": "assistant", "content": "Assistant 2."},
        {"role": "user", "content": "User 3."},
        {"role": "user", "content": "User 4."},
        {"role": "user", "content": "User 5."},
        {"role": "user", "content": "User 6."},
        {"role": "user", "content": "User 7."},
        {"role": "user", "content": "User 8."},
    ]
    result = summarise_context(history)
    lines = [line for line in result.splitlines() if line.startswith("• ")]
    assert lines[-1] == "• User 8."
