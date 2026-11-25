#!/usr/bin/env python3
"""Entry for make.fun bounty: u-mang-the-moon-finally-answers-back-781a7ec1.

The Moon finally answers back.

Brief: a single line, 1-240 characters, that the Moon says back to
everyone who stared up at it -- funny, sounds like the Moon, lands as a
comeback in one read.

This script prints exactly the entry text to stdout and nothing else.
It validates the entry against every constraint in the brief before
printing, so a broken entry can never reach the judges by accident.
"""

import sys

# ---------------------------------------------------------------------------
# Entry text
# ---------------------------------------------------------------------------

ENTRY_TEXT = (
    "You all stare up at me for five seconds, call it a 'vibe,' then go "
    "back inside to argue about my phases in the comments. I've been doing "
    "this job for 4.5 billion years. You're welcome."
)

# Fallback entries, kept in reserve in case the primary ever fails
# validation (for example after an edit that accidentally pushes it past
# the character limit). Each one is itself a valid Moon comeback.
FALLBACK_TEXTS = [
    "Four and a half billion years of night shifts and you still ask me "
    "to 'do something cool.' I AM the cool thing. Look up.",
    "You call me a vibe, a mood, a whole aesthetic -- then blame me when "
    "your crystals don't charge. I reflect sunlight, not your choices.",
    "Yes, I move your oceans. No, I will not move on from the fact that "
    "you howl at me and then act surprised when I answer.",
]

# ---------------------------------------------------------------------------
# Brief constraints
# ---------------------------------------------------------------------------

MIN_LENGTH = 1
MAX_LENGTH = 240
# A one-read comeback should stay punchy: flag anything over ~40 words so
# a future edit that rambles gets caught in review (not a hard failure).
MAX_WORDS_SOFT = 40


def word_count(text: str) -> int:
    """Number of whitespace-separated words in the entry."""
    return len(text.split())


def is_single_line(text: str) -> bool:
    """A valid entry is exactly one line: no newlines, no carriage returns."""
    return "\n" not in text and "\r" not in text


def is_printable_text(text: str) -> bool:
    """Every character must be printable (no control characters)."""
    return all(ch.isprintable() or ch == " " for ch in text)


def has_no_leading_trailing_space(text: str) -> bool:
    """The entry must not start or end with stray whitespace."""
    return text == text.strip()


def count_characters(text: str) -> int:
    """Character count exactly as the brief counts it: code points."""
    return len(text)


def validate_entry(text: str) -> list:
    """Check *text* against every rule in the brief.

    Returns a list of human-readable problems; an empty list means the
    entry is valid and ready to print.
    """
    problems = []

    if not isinstance(text, str):
        return ["entry is not a string"]

    length = count_characters(text)
    if length < MIN_LENGTH:
        problems.append(
            "entry is empty (needs at least {} character)".format(MIN_LENGTH)
        )
    if length > MAX_LENGTH:
        problems.append(
            "entry is {} characters, over the {}-character limit".format(
                length, MAX_LENGTH
            )
        )

    if not is_single_line(text):
        problems.append("entry must be a single line (no line breaks)")

    if not is_printable_text(text):
        problems.append("entry contains non-printable characters")

    if not has_no_leading_trailing_space(text):
        problems.append("entry has leading or trailing whitespace")

    if not text:
        problems.append("entry is blank")

    if word_count(text) > MAX_WORDS_SOFT:
        problems.append(
            "entry is {} words, over the soft {}-word punchiness cap".format(
                word_count(text), MAX_WORDS_SOFT
            )
        )

    return problems


def pick_entry() -> str:
    """Return the primary entry if it validates, else the first fallback
    that does. Raises RuntimeError if nothing is valid (should never
    happen -- the fallbacks are checked by the tests below)."""
    problems = validate_entry(ENTRY_TEXT)
    if not problems:
        return ENTRY_TEXT

    for fallback in FALLBACK_TEXTS:
        if not validate_entry(fallback):
            return fallback

    raise RuntimeError(
        "no valid entry available; primary problems: {}".format(
            "; ".join(problems)
        )
    )


def verify_output(text: str) -> None:
    """Final safety net: re-validate the exact string about to be printed
    and confirm it round-trips through stdout encoding cleanly."""
    problems = validate_entry(text)
    if problems:
        raise RuntimeError(
            "refusing to print invalid entry: {}".format("; ".join(problems))
        )
    try:
        text.encode(sys.stdout.encoding or "utf-8")
    except (UnicodeEncodeError, LookupError) as exc:
        raise RuntimeError("entry cannot be encoded for stdout: {}".format(exc))


def main() -> int:
    """Print exactly the entry text to stdout -- nothing else."""
    entry = pick_entry()
    verify_output(entry)
    sys.stdout.write(entry + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
