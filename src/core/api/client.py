import asyncio
import time
from typing import Optional, Tuple

from openai import AsyncOpenAI

from src.core.constants import CHARS_PER_TOKEN, TOKENS_PER_WORD


async def ask_openai(
    client: AsyncOpenAI,
    model: str,
    prompt: str,
    max_tokens: int,
    progress_callback: Optional[callable] = None,
) -> Tuple[float, int, int]:
    """Send a prompt to the OpenAI API and process the streaming response.

    Makes a chat completion request with streaming enabled and measures time to first token,
    while counting prompt and completion tokens.

    Args:
        client: Configured AsyncOpenAI client instance.
        model: Model name to use for the completion.
        prompt: Input prompt text.
        max_tokens: Maximum tokens to generate.
        progress_callback: Optional callback function called with token count updates.

    Returns:
        Tuple of (time_to_first_token_seconds, completion_tokens, prompt_tokens).

    Raises:
        Exception: If API call fails or streaming encounters errors.
    """
    start = time.time()

    time_to_first_token = 0.0
    first_token_seen = False
    last_usage = None
    accumulated_content = ""
    estimated_tokens = 0

    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=1,
        stream=True,
        stream_options={"include_usage": True},
    )

    async for chunk in stream:
        if not first_token_seen and chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content.strip()
            if content:
                time_to_first_token = time.time() - start
                first_token_seen = True

        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            if content:
                accumulated_content += content
                new_tokens = estimate_tokens(content)
                estimated_tokens += new_tokens
                if progress_callback:
                    progress_callback(new_tokens)

        if chunk.usage:
            last_usage = chunk.usage

    prompt_tokens = last_usage.prompt_tokens if last_usage else 0
    completion_tokens = last_usage.completion_tokens if last_usage else estimated_tokens

    # Adjust progress bar if needed
    if progress_callback and last_usage and last_usage.completion_tokens:
        diff = last_usage.completion_tokens - estimated_tokens
        if diff != 0:
            progress_callback(diff)

    return time_to_first_token, completion_tokens, prompt_tokens


async def ask_openai_random_input(
    client: AsyncOpenAI,
    model: str,
    num_words: int,
    max_tokens: int,
    progress_callback: Optional[callable] = None,
) -> Tuple[float, int, int]:
    """Send a randomly generated prompt to the OpenAI API.

    Generates a random phrase and sends it as a prompt, returning the same metrics
    as ask_openai.

    Args:
        client: Configured AsyncOpenAI client instance.
        model: Model name to use for the completion.
        num_words: Number of words to include in the random prompt.
        max_tokens: Maximum tokens to generate.
        progress_callback: Optional callback function for token progress updates.

    Returns:
        Tuple of (time_to_first_token_seconds, completion_tokens, prompt_tokens).
    """
    from src.core.api.prompts import generate_random_phrase
    prompt = generate_random_phrase(num_words)
    return await ask_openai(client, model, prompt, max_tokens, progress_callback)


def estimate_tokens(content: str) -> int:
    """Estimate the number of tokens in a text string.

    Uses a heuristic approach: ~1.3 tokens per word for word-based content,
    or ~3 characters per token for non-word content.

    Args:
        content: Text content to estimate tokens for.

    Returns:
        Estimated number of tokens (minimum 1).
    """
    if not content:
        return 0

    content = content.strip()
    if not content:
        return 0

    words = content.split()
    word_count = len(words)

    if word_count > 0:
        # ~1.3 tokens per word
        return max(1, int(word_count * TOKENS_PER_WORD))
    else:
        # Character-based: ~3 characters per token
        char_count = len(content)
        return max(1, int(char_count / CHARS_PER_TOKEN))


async def get_first_available_model(client: AsyncOpenAI) -> str:
    """Retrieve the first available model from the API.

    Queries the models endpoint and returns the ID of the first available model.

    Args:
        client: Configured AsyncOpenAI client instance.

    Returns:
        Model ID string of the first available model.

    Raises:
        ValueError: If no models are available in the API response.
    """
    model_list = await client.models.list()
    if not model_list.data:
        raise ValueError("No models available")
    return model_list.data[0].id