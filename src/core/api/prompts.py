"""Utilities for generating random prompts for benchmarking."""

import random
import string

from src.core.constants import (
    MAX_WORD_LENGTH,
    MIN_WORD_LENGTH,
    PROMPT_INSTRUCTION,
)


def generate_random_word() -> str:
    """Generate a single random word of variable length.

    Creates a word using lowercase ASCII letters with length between
    MIN_WORD_LENGTH and MAX_WORD_LENGTH.

    Returns:
        A randomly generated word string.
    """
    word_length = random.randint(MIN_WORD_LENGTH, MAX_WORD_LENGTH)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(word_length))


def generate_random_phrase(num_words: int) -> str:
    """Generate a random phrase consisting of multiple words.

    Creates a phrase by joining random words and wraps it in a standard
    instruction prompt for the LLM to respond unchanged.

    Args:
        num_words: Number of random words to include in the phrase.

    Returns:
        Complete prompt string with instruction and random content.
    """
    random_words = [generate_random_word() for _ in range(num_words)]
    random_phrase = ' '.join(random_words)
    return f"{PROMPT_INSTRUCTION} {random_phrase}"