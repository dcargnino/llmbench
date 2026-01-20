"""Constants used throughout the LLM benchmark application."""

# Token estimation constants
TOKENS_PER_WORD = 1.3
CHARS_PER_TOKEN = 3.0

# Random prompt generation constants
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 10
DEFAULT_NUM_WORDS = 100
PROMPT_INSTRUCTION = "Please reply back the following section unchanged:"

# Default configuration values
DEFAULT_MAX_TOKENS = 512
DEFAULT_CONCURRENCY = [1]

# Latency measurement constants
DEFAULT_LATENCY_ATTEMPTS = 5

# Output formatting
DEFAULT_MARKDOWN_FILENAME = "benchmark_results.md"